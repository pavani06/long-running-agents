# Guia: Embrulhando `analyze-and-improve` com o Harness

> Passo a passo para resolver o problema do LLM se perder no meio da execução
> do pipeline `analyze-and-improve`, usando o sistema de harness primitives.

---

## 1. Diagnóstico: por que o LLM se perde?

A skill `analyze-and-improve` ([SKILL.md:46-56]) orquestra 7 fases:

| Fase | Delegado      | Output principal                                |
|------|-------------- |-------------------------------------------------|
| 0    | `ultrabrain`  | `<date>-<source-slug>-mental-model.md` + `.yaml`                     |
| 1    | `deep`        | `<date>-<source-slug>-analysis.md` + `.yaml`                         |
| 2    | `ultrabrain`  | `<date>-<source-slug>-patterns.md` + `.yaml`                         |
| 3    | `deep`        | `<date>-<source-slug>-classification.md` + `.yaml`                   |
| 4    | `deep` (x3)   | artifacts manifest (.md + .yaml) + artefatos concretos   |
| 5    | `quick`       | atualiza system-of-record, índices              |
| 6    | `deep`        | (opcional) integração no curriculum             |

Cada fase delega para um subagente via `task()`. O subagente funciona — tem
contexto fresco, prompt autocontido, outputs definidos. Mas o **orquestrador** (o
LLM que invocou `analyze-and-improve`) precisa:

1. Manter na memória qual fase está rodando (entre 7)
2. Validar que cada fase produziu output corretamente
3. Passar contexto entre fases (output da fase N alimenta fase N+1)
4. Lidar com falhas parciais (fase N quebrou → repetir fase N, não recomeçar tudo)
5. Não se perder se a sessão for interrompida (timeout, crash, troca de contexto)

**O orquestrador falha sistematicamente nos itens 1, 3 e 5.** O harness foi
projetado exatamente para esses 3 problemas.

## 2. Como o harness resolve

| Problema | Solução do harness |
|---|---|
| Esquecer qual fase está rodando | `PROGRESS.md` — estado persistente, lido no início de cada sessão |
| Validar output de cada fase | `guardian` — verifica se evidência existe antes de avançar |
| Passar contexto entre fases | Arquivos em `docs/analysis/<date>-<slug>/` — outputs persistentes que qualquer agente pode ler |
| Lidar com falhas parciais | `test-results.json` — contrato default-FAIL; harness.sh só avança se evaluator der PASS |
| Retomar após interrupção | `harness.sh` — lê `PROGRESS.md` + `test-results.json` e continua de onde parou |
| Agente indo na direção errada | `STEER.md` + `AGENT_STOP` — redirecionamento humano e kill switch |

## 3. Arquitetura da solução

```
┌─────────────────────────────────────────────────────────┐
│                    harness.sh (loop)                     │
│                                                         │
│  1. Lê PROGRESS.md → descobre fase atual                │
│  2. Lê test-results.json → fase tem passes: false?       │
│  3. Lê STEER.md → tem redirecionamento humano?          │
│  4. BUILDER: invoca fase N do analyze-and-improve       │
│  5. GUARDIAN: verifica evidência (outputs da fase)      │
│  6. EVALUATOR: revisa qualidade dos outputs             │
│  7. Se PASS → avança para fase N+1                      │
│     Se NEEDS_WORK → repete fase N com feedback          │
│  8. Commit checkpoint → estado salvo para próxima sessão │
└─────────────────────────────────────────────────────────┘
```

A diferença fundamental: em vez de uma única invocação de skill rodar 7 fases,
cada fase é uma "feature" independente no harness. O harness.sh é o
orquestrador confiável (bash, não LLM) que garante que nada se perde.

## 4. Passo a passo de implementação

### 4.1 Pré-requisitos

- Repositório `long-running-agents` clonado e funcional
- Harness instalado em `~/.config/opencode/harness/` (já foi feito)
- Skill `analyze-and-improve` existente em `.opencode/skills/analyze-and-improve/`
- OpenCode CLI disponível (verificar com `which opencode`)

```bash
cd /mnt/c/Users/pavan/long-running-agents

# Verificar que a skill existe
ls .opencode/skills/analyze-and-improve/SKILL.md

# Verificar CLI
which opencode  # se não existir, veja seção 4.6 (alternativa sem CLI)
```

### 4.2 Criar a estrutura harness dentro do repositório

```bash
cd /mnt/c/Users/pavan/long-running-agents

# Criar diretório do harness
mkdir -p harness/templates

# Copiar templates base do harness global
cp ~/.config/opencode/harness/templates/test-results.json harness/templates/
cp ~/.config/opencode/harness/templates/STEER.md harness/templates/
```

### 4.3 Criar PROGRESS.md customizado para análise

Crie `PROGRESS.md` na raiz do repositório (ou sobrescreva se já existir):

```markdown
# PROGRESS.md — Análise de fonte externa

> Pipeline analyze-and-improve gerenciado pelo harness.
> Cada fase é uma feature com contrato default-FAIL.
> O harness.sh avança automaticamente entre fases.

## Done

<!-- Fases concluídas e aprovadas pelo evaluator -->
<!-- Formato: - [x] phase-N: descrição - commit abc1234 [evaluator: PASS] -->

## In Progress

<!-- A fase atual. Exatamente UMA por vez. -->

- [ ] phase-0: Repository Mental Model
  - Output esperado: docs/analysis/<date>-<slug>/<date>-<source-slug>-mental-model.md + .yaml
  - Delegado: ultrabrain
  - Bloqueios: nenhum

## Next

- [ ] phase-1: Knowledge Extraction
- [ ] phase-2: Pattern Extraction
- [ ] phase-3: Classification
- [ ] phase-4: Improvement Generation
- [ ] phase-5: Integration
- [ ] phase-6: Curriculum Deep Integration (opcional)

## Analysis Context

- **source**: [URL ou path do documento fonte — preencher]
- **date**: [YYYY-MM-DD — preencher]
- **source-slug**: [slug curto — preencher]
- **output_dir**: docs/analysis/<date>-<source-slug>/

## Notes

- Stack: Node.js, OpenCode agents, Obsidian-compatible markdown
- Rodar: não se aplica (análise de documento, não build de código)
- Testar: `npx tsx scripts/validate-obsidian.ts`
- Evidência: outputs em docs/analysis/<date>-<slug>/
- Commits: `git commit -m "analysis(<slug>): <fase>"`
```

### 4.4 Criar test-results.json com contrato para cada fase

> **Nota:** O script `setup-analysis.sh` gera este arquivo automaticamente. O exemplo abaixo
> documenta o schema para referência. O template canônico está em
> `.opencode/skills/analyze-and-improve/harness/templates/test-results.json`.

Schema (todas as 7 fases seguem o mesmo padrão):

```json
{
  "phase-0": {
    "passes": false,
    "evidence": ["docs/analysis/<date>-<slug>/<date>-<slug>-mental-model.md", "..."],
    "evaluated_by": null,
    "notes": "Modelo mental do repositorio — Phase 0 do analyze-and-improve",
    "duration_seconds": null,
    "retry_count": 0,
    "started_at": null,
    "completed_at": null
  },
  "phase-1": {
    "passes": false,
    "evidence": ["docs/analysis/<date>-<slug>/<date>-<slug>-analysis.md", "..."],
    "evaluated_by": null,
    "notes": "Extracao de conhecimento da fonte — Phase 1",
    "duration_seconds": null,
    "retry_count": 0,
    "started_at": null,
    "completed_at": null
  }
  // ... phases 2-6 seguem o mesmo padrão
}
```

Campos de métricas (registrados automaticamente pelo harness durante a execução):

| Campo | Tipo | Quando é escrito |
|---|---|---|
| `duration_seconds` | number\|null | Calculado pelo harness ao final da fase (completed_at - started_at) |
| `retry_count` | number | Incrementado a cada NEEDS_WORK do evaluator |
| `started_at` | string (ISO 8601)\|null | Registrado pelo builder antes de delegar a fase |
| `completed_at` | string (ISO 8601)\|null | Registrado pelo harness quando o evaluator aprova |

A geração via `setup-analysis.sh` dispensa o `sed` de PLACEHOLDER — o script faz
a substituição diretamente a partir dos parâmetros `--source`, `--date`, `--source-slug`.

### 4.5 Copiar e adaptar harness.sh

Copie o script base e crie uma versão específica para o pipeline de análise:

```bash
cp ~/.config/opencode/harness/harness.sh harness/harness-analysis.sh
chmod +x harness/harness-analysis.sh
```

Edite `harness/harness-analysis.sh` e faça estas adaptações:

**a) Configuração de paths (linha ~24):**

```bash
# Apontar para os arquivos do harness DENTRO do repo
RESULTS_FILE="${RESULTS_FILE:-harness/test-results.json}"
EVIDENCE_LOG="${EVIDENCE_LOG:-harness/.evidence-reads}"
PROGRESS_FILE="${PROGRESS_FILE:-PROGRESS.md}"
STEER_FILE="${STEER_FILE:-STEER.md}"
STOP_FILE="${STOP_FILE:-AGENT_STOP}"
```

**b) Builder para fases de análise (linha ~192, função `run_builder`):**

O builder padrão faz "implementar feature X". Para análise, precisamos invocar
uma fase específica do `analyze-and-improve`. Substitua a função `run_builder`:

```bash
run_builder() {
    local feature="$1"
    local steer_msg="$2"

    # Extrai o número da fase de "phase-N"
    local phase_num="${feature#phase-}"

    log_section "BUILDER: $feature (Phase $phase_num)"

    # Lê o contexto da sessão de análise
    local source_url date slug output_dir
    source_url=$(grep -oP 'source\*\*: \K.+' "$PROGRESS_FILE" | head -1 || echo "")
    date=$(grep -oP 'date\*\*: \K.+' "$PROGRESS_FILE" | head -1 || echo "")
    slug=$(grep -oP 'source-slug\*\*: \K.+' "$PROGRESS_FILE" | head -1 || echo "")
    output_dir="docs/analysis/${date}-${slug}"

    local prompt="TASK: Run Phase $phase_num of the analyze-and-improve skill.

SOURCE DOCUMENT: $source_url
OUTPUT DIRECTORY: $output_dir
TARGET REPOSITORY: $(pwd)
SYSTEM OF RECORD: docs/system-of-record.md

IMPORTANT: Run ONLY Phase $phase_num. Do NOT run other phases.
The output of this phase goes to $output_dir.

Load the skill 'analyze-and-improve' and execute ONLY Phase $phase_num.
Use the skill's delegation pattern (task() with the correct category and prompt).

After the phase completes:
1. Verify the output files were created in $output_dir
2. Open each output file with Read (this is required evidence)
3. Update PROGRESS.md: move '$feature' to Done
4. Commit with message: 'analysis(${slug}): phase $phase_num'
5. Do NOT modify harness/test-results.json — the harness handles that."

    if [ -n "$steer_msg" ]; then
        prompt="OPERATOR STEERING: $steer_msg

$prompt"
    fi

    log_info "Prompt: $prompt"
    log_info "Executando $AGENT_CLI..."

    $AGENT_CLI -p "$prompt"

    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Builder falhou com código $exit_code"
        return 1
    fi

    log_ok "Builder concluiu Phase $phase_num."
    return 0
}
```

**c) Evaluator adaptado para análise (linha ~249, função `run_evaluator`):**

```bash
run_evaluator() {
    local feature="$1"

    log_section "EVALUATOR: $feature"

    local review_prompt="You are the evaluator (skills/evaluator.md).

Review the analysis phase '$feature' from PROGRESS.md.

CONTEXT: This is a phase from the analyze-and-improve pipeline.
Each phase produces markdown + YAML outputs in docs/analysis/<date>-<slug>/.

TASKS:
1. Read PROGRESS.md to find the current output_dir
2. Read the output files for this phase (listed in harness/test-results.json evidence field)
3. Run 'git diff HEAD~1' to see what changed
4. Evaluate:
   a. Do the output files exist and have substantial content (not empty/templates)?
   b. Does the content match the phase objective (mental model, extraction, patterns, etc.)?
   c. Are Obsidian conventions followed (YAML frontmatter, wikilinks, tags)?
   d. Is the content substantive (not generic, not repetitive)?
5. Run 'npx tsx scripts/validate-obsidian.ts' to verify conventions
6. Return PASS or NEEDS_WORK with specific findings.

If NEEDS_WORK, list exactly what is missing or wrong.
If PASS, state it clearly as the first word of your response."

    log_info "Executando $AGENT_CLI --agent $EVALUATOR_AGENT..."

    local verdict
    verdict=$($AGENT_CLI --agent "$EVALUATOR_AGENT" -p "$review_prompt" 2>&1) || true

    echo "$verdict"

    local verdict_line
    verdict_line=$(echo "$verdict" | head -1)

    if [ "$verdict_line" = "PASS" ]; then
        log_ok "Evaluator: PASS"
        if command -v python3 &>/dev/null; then
            python3 -c "
import json
with open('$RESULTS_FILE') as f:
    data = json.load(f)
if '$feature' in data:
    data['$feature']['evaluated_by'] = 'evaluator'
with open('$RESULTS_FILE', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null
        fi
        return 0
    else
        log_error "Evaluator: NEEDS_WORK"
        echo "$verdict" > NEXT_FINDINGS.md
        log_info "Achados salvos em NEXT_FINDINGS.md"
        return 1
    fi
}
```

### 4.6 Alternativa sem CLI headless (modo semi-automático)

Se `opencode` não tiver um modo CLI headless funcional, o harness.sh não consegue
invocar o agente automaticamente. Nesse caso, use o **modo prompt-a-prompt**:

Em vez de rodar `./harness/harness-analysis.sh`, você mesmo faz o papel do loop.
O harness.sh ainda é útil para guardian e evaluator (que podem ser invocados
manualmente), e os templates garantem que nada se perde.

**Fluxo manual por fase:**

```
1. Leia PROGRESS.md. A fase atual é phase-N.
2. Copie o prompt do builder (seção 4.5b acima) para o OpenCode.
3. O agente executa a fase e gera os outputs.
4. Rode o guardian manualmente:
   "Verifique se os arquivos de evidência para phase-N existem e têm conteúdo."
5. Rode o evaluator manualmente:
   "AVALIE phase-N. Leia PROGRESS.md, veja git diff, abra outputs.
    Retorne PASS ou NEEDS_WORK."
6. Se PASS: mova phase-N para Done no PROGRESS.md, atualize test-results.json.
   Se NEEDS_WORK: corrija e repita do passo 2.
7. Vá para o passo 1 com phase-N+1.
```

Ou, se você quiser um atalho: rode `harness/harness-analysis.sh` com `--once` e
ele fará UMA iteração (uma fase). Depois você pode rodar de novo para a próxima
fase. Se o builder falhar por falta de CLI, você executa o builder manualmente
no OpenCode e depois roda o script de novo — ele detectará a evidência e
pulará para o guardian/evaluator.

### 4.7 Configurar AGENT_CLI

Se você tem `opencode` disponível como CLI:

```bash
# Testar se opencode responde
opencode --help

# Configurar para o harness
export AGENT_CLI="opencode"
export EVALUATOR_AGENT="evaluator"
```

Se usa Claude CLI:

```bash
export AGENT_CLI="claude"
export EVALUATOR_AGENT="evaluator"
```

## 5. Como executar

### 5.1 Preparação da sessão de análise

```bash
cd /mnt/c/Users/pavan/long-running-agents

# Único comando necessário — o script gera PROGRESS.md, test-results.json,
# cria o diretório de output, e configura STEER.md:
./.opencode/skills/analyze-and-improve/harness/setup-analysis.sh \
  --source "Raw-Knowledge/sources/2026-06-11-patterns-for-ai-agents.md" \
  --date "2026-06-11" \
  --source-slug "patterns-for-ai-agents"

# Para preview sem escrever:
./.opencode/skills/analyze-and-improve/harness/setup-analysis.sh \
  --source "Raw-Knowledge/sources/minha-talk.md" --dry-run

# Verificar que está tudo pronto
cat PROGRESS.md
python3 -c "import json; json.load(open('harness/test-results.json'))" && echo "JSON válido"
```
O `setup-analysis.sh` substitui os passos manuais de editar PROGRESS.md, rodar sed
para PLACEHOLDER, e criar diretório de output. Consulte `--help` para todas as opções.

### 5.2 Rodar o loop completo (modo automático)

```bash
# Loop contínuo — roda até todas as 7 fases passarem
./harness/harness-analysis.sh

# Ou uma fase por vez (mais seguro para começar)
./harness/harness-analysis.sh --once
```

### 5.3 Rodar uma fase específica

```bash
# Se a fase 3 falhou e você quer refazê-la
./harness/harness-analysis.sh --feature phase-3
```

### 5.4 Monitoramento

```bash
# Em outro terminal, acompanhar o progresso
watch -n 5 'cat PROGRESS.md'

# Ver quais fases já passaram
python3 -c "import json; d=json.load(open('harness/test-results.json')); [print(f'{k}: {\"PASS\" if v.get(\"evaluated_by\") else \"pendente\"}') for k,v in d.items() if not k.startswith('_')]"
```

## 6. Recuperação de falhas

### 6.1 O LLM se perdeu no meio de uma fase

Isso é exatamente o que o harness resolve. O script detecta que a fase não gerou
evidência (guardian rejeita) ou gerou evidência ruim (evaluator rejeita) e
simplesmente repete a fase.

```bash
# Se o harness.sh estiver rodando, ele já vai repetir sozinho.
# Se você está no modo manual:
# 1. Verifique qual fase estava rodando
cat PROGRESS.md | grep "In Progress"

# 2. Delete outputs parciais (se houver) para evitar confusão
# 3. Rode o builder novamente para essa fase
```

### 6.2 Interrompeu no meio (fechou terminal, crash, etc.)

```bash
# 1. Volte ao diretório
cd /mnt/c/Users/pavan/long-running-agents

# 2. Leia o estado
cat PROGRESS.md
cat harness/test-results.json | python3 -m json.tool

# 3. Continue de onde parou
./harness/harness-analysis.sh
```

O harness.sh lê `PROGRESS.md` e `test-results.json` e retoma automaticamente
da primeira fase com `passes: false`.

### 6.3 Uma fase está em loop (NEEDS_WORK repetidas vezes)

```bash
# 1. Pare o loop
touch AGENT_STOP

# 2. Leia os achados do evaluator
cat NEXT_FINDINGS.md

# 3. Redirecione manualmente
echo "Fase phase-3: o <date>-<source-slug>-classification.md está genérico. Use os patterns extraídos
na fase 2 como input. Compare cada pattern com o que já existe em docs/canonical/.
Seja específico: para CADA pattern, diga se existe (Existing Coverage), existe
parcialmente (Partial Coverage), ou não existe (Missing Coverage)." > STEER.md

# 4. Remova o kill switch e continue
rm AGENT_STOP
./harness/harness-analysis.sh --feature phase-3
```

### 6.4 Quer pular uma fase (ex: phase-6 é opcional)

```bash
# Marcar como PASS manualmente
python3 -c "
import json
with open('harness/test-results.json') as f:
    data = json.load(f)
data['phase-6']['evaluated_by'] = 'human'
data['phase-6']['passes'] = True
data['phase-6']['notes'] = 'Skipped — optional phase'
with open('harness/test-results.json', 'w') as f:
    json.dump(data, f, indent=2)
print('phase-6 marcada como concluída')
"
```

## 7. O que acontece em cada fase (referência rápida)

| Fase | O agente faz | Evidência | Tempo típico |
|------|-------------|-----------|-------------|
| 0 | Lê AGENTS.md, README, system-of-record, canonical docs, curriculum. Constrói modelo mental do repositório. | `<date>-<source-slug>-mental-model.md` + `.yaml` | 3-5 min |
| 1 | Lê o documento fonte (transcrição YouTube). Extrai conhecimento não-óbvio. Filtra ruído. | `<date>-<source-slug>-analysis.md` + `.yaml` | 5-15 min |
| 2 | Identifica padrões reutilizáveis no conhecimento extraído. | `<date>-<source-slug>-patterns.md` + `.yaml` | 3-5 min |
| 3 | Classifica cada padrão contra o repositório: Existing/Partial/Missing Coverage. | `<date>-<source-slug>-classification.md` + `.yaml` | 3-8 min |
| 4 | Gera artefatos em 7 categorias (canonical docs, skills, exercises, ...) priorizados por impacto. | `<date>-<source-slug>-artifacts.yaml` + `.md` + artefatos | 10-30 min |
| 5 | Atualiza system-of-record.md, índices, wikilinks. | `git diff system-of-record.md` | 2-5 min |
| 6 | Integra Missing/Partial Coverage no curriculum existente com profundidade total. | arquivos em `curriculum/` | 5-20 min |

## 8. Exemplo completo: analisando uma talk do YouTube

```bash
cd /mnt/c/Users/pavan/long-running-agents

# Suponha que você tem a transcrição de uma talk em:
# Raw-Knowledge/sources/2026-06-11-patterns-for-ai-agents.md

# 1. Rodar o setup (substitui edição manual de PROGRESS.md, sed de PLACEHOLDER,
#    e criação de diretório):
./.opencode/skills/analyze-and-improve/harness/setup-analysis.sh \
  --source "Raw-Knowledge/sources/2026-06-11-patterns-for-ai-agents.md" \
  --date "2026-06-11" \
  --source-slug "patterns-for-ai-agents"

# 2. Rodar o harness:
./harness/harness-analysis.sh

# O harness vai:
#   Iteração 1: BUILDER phase-0 → GUARDIAN → EVALUATOR → (PASS → próximo)
#   Iteração 2: BUILDER phase-1 → GUARDIAN → EVALUATOR → (PASS → próximo)
#   ...
#   Iteração 7: BUILDER phase-6 → GUARDIAN → EVALUATOR → (PASS → FIM)

# Se em qualquer momento o LLM se perder:
# - O guardian rejeita (sem evidência) → repete a fase
# - O evaluator rejeita (qualidade ruim) → repete com feedback
# - Terminal fechou → na próxima execução, harness.sh lê PROGRESS.md e continua

# Ao final, todos os outputs estão em:
ls docs/analysis/2026-06-11-patterns-for-ai-agents/
# 2026-06-11-patterns-for-ai-agents-mental-model.md    2026-06-11-patterns-for-ai-agents-mental-model.yaml
# 2026-06-11-patterns-for-ai-agents-analysis.md        2026-06-11-patterns-for-ai-agents-analysis.yaml
# 2026-06-11-patterns-for-ai-agents-patterns.md        2026-06-11-patterns-for-ai-agents-patterns.yaml
# 2026-06-11-patterns-for-ai-agents-classification.md  2026-06-11-patterns-for-ai-agents-classification.yaml
# 2026-06-11-patterns-for-ai-agents-artifacts.yaml
# 2026-06-11-patterns-for-ai-agents-artifacts.md
```

## 8.5. O Artifacts Manifest

A partir de 2026-06-14, o output da Phase 4 mudou: em vez de um único `integration-roadmap.md`, o orquestrador gera um **artifacts manifest** — um par de arquivos `.yaml` + `.md` que serve como contrato entre a Phase 4 (geração de artefatos) e a Phase 5 (integração nos índices).

**O que é**: Um manifesto que lista todos os artefatos concretos gerados na Phase 4 (canonical docs, skills, exercises), mapeia cada um para os índices que a Phase 5 deve atualizar (Integration Map), e documenta padrões não gerados (skipped) com justificativa.

**Quem gera**: O orquestrador, como ação direta (não delegada), após a Phase 4 completar e antes de disparar a Phase 5.

**Formato**: Um par de arquivos em `docs/analysis/<date>-<source-slug>/`:
- `<date>-<source-slug>-artifacts.yaml` — estrutura tipada com `meta`, `artifacts`, `skipped`, `gate`
- `<date>-<source-slug>-artifacts.md` — sumário legível com tabela de artefatos, Integration Map, e seção de skipped

**Exemplo** (baseado na sessão 12-Factor Agents):
```
docs/analysis/2026-06-09-12-factor-agents/
  2026-06-09-12-factor-agents-artifacts.yaml
  2026-06-09-12-factor-agents-artifacts.md
```

O `artifacts.yaml` lista:
```yaml
artifacts:
  canonical_docs:
    - path: docs/canonical/error-context-hygiene.md
      pattern: Error Context Hygiene
      classification: Missing
      priority: P0
    - path: docs/canonical/deterministic-tool-dispatch.md
      pattern: Deterministic Tool Dispatch
      classification: Partial Coverage
      priority: P1
  skills:
    - path: .opencode/skills/error-context-hygiene/SKILL.md
      pattern: Error Context Hygiene
      classification: Missing
  exercises:
    - path: curriculum/02-nivel-2-practical-patterns/exercises/exercise-04-error-context-hygiene.md
      pattern: Error Context Hygiene
      classification: Missing
skipped:
  already_exists:
    - pattern: Serialized Pause/Resume State
      evidence: docs/canonical/serializable-pause-resume-state.md:1
```

O `artifacts.md` contém o Integration Map — uma tabela que conecta cada artefato aos índices que a Phase 5 deve atualizar. A Phase 5 lê o manifesto como input e segue o Integration Map para saber exatamente quais documentos de índice modificar.

> **Nota**: Sessões anteriores a 2026-06-14 usavam `integration-roadmap.md` (formato legacy).
> O conteúdo (rastreabilidade classificação → artefatos → integração) é preservado no novo formato.

## 9. Checklist de verificação

Antes de declarar a análise concluída:

- [ ] PROGRESS.md tem todas as 7 fases em Done
- [ ] test-results.json tem `evaluated_by: "evaluator"` para cada fase
- [ ] `docs/analysis/<date>-<slug>/` contém todos os 10+ arquivos de output
- [ ] `npx tsx scripts/validate-obsidian.ts` passa sem erros
- [ ] system-of-record.md foi atualizado (se Phase 5 rodou)
- [ ] Todos os commits têm mensagens no formato `analysis(<slug>): phase N`
- [ ] Nenhum arquivo temporário ficou em `/tmp/opencode/`

## 10. Próximos passos

Itens ja implementados (2026-06-12):

1. ~~**Automatize o setup**~~ `harness/setup-analysis.sh` criado dentro do skill
   `analyze-and-improve`. Uso: `./harness/setup-analysis.sh --source <path>
   --date YYYY-MM-DD --source-slug <slug> --target-repo <path>`

2. ~~**Skillify o harness wrapper**~~ `harness-analyze-and-improve` ja existe como
   skill nativa no projeto. Usa `task()` para delegar cada fase com suporte a
   `mode=once`, `mode=feature:phase-N`, e `mode=loop`.

3. ~~**Métricas**~~ Campos `duration_seconds`, `retry_count`, `started_at`,
   `completed_at` adicionados ao `test-results.json`. Ambos os orquestradores
   (skill harness e bash harness) registram e reportam metricas com sumario
   de bottlenecks ao final do pipeline.

Pendentes:

4. **Migração para artifacts manifest**: Concluída em 2026-06-14. O formato
   `integration-roadmap.md` foi substituído pelo par `artifacts.{yaml,md}`.
   Sessões históricas mantêm o formato legacy com banner de depreciação.

5. **Paralelize fases independentes**: Phase 0 (modelo mental) e Phase 1
   (extração) podem rodar em paralelo porque não dependem uma da outra
   (a Phase 1 não usa o output da Phase 0).
