# QI Loop Iter 1 — Correções do Run Kavak Playbook — Plano de Execução

> **✅ EXECUTADO E FECHADO (2026-08-30):** 13/13 tarefas concluídas, 15/15 critérios de re-verificação PASS, commits `dfb67d8` (LRA) e `e2d2a0d` (RK) pushados. Rastreabilidade completa no epic #145 (issues #146-#156 com handoffs comentados). Desvios documentados: Sidekick ganhou skill+exercise completos (decisão do operador no gate 2→3, REC-012); FASE 5 por verificação direcionada.

**Objetivo:** Fechar os 11 findings P0/P1 do review-work de 2026-08-30 (key hardening, untrusted source, commits pendentes, Passo 0c, 6 correções de artefato) + criar skill/exercise do Sidekick (REC-012, decisão do operador no gate 2→3).
**Fase:** Implementação
**Dependências:** review-work concluído (2026-08-30); recomendações aprovadas (gate 2→3 ✓)
**Duração estimada:** 1 sessão
**Rastreabilidade:** REC-001..012 (`~/.reflection/qi-loop-iter1-recommendations.md`) ← findings F1-F11 do review-work

> Canonical grounding skipped — budget orange (nota: intent-five-part-primitive aplicado via rastreabilidade REC↔finding↔tarefa; constraint-budget: 5 constraints listadas abaixo).

**Constraints do plano (5):**
1. Nenhuma modificação em `docs/canonical/` (imutáveis desta run)
2. `.env` nunca stageado; validação pré-commit em cada commit (`git status`)
3. Phase 6 contract preservado: só `edit` em curriculum, nenhum arquivo novo em curriculum/ além do exercise-08 (que é Phase 4-type artifact, criado via QI loop)
4. Curriculo/skills em PT-BR onde o arquivo é PT-BR; wikilinks verificáveis
5. Commits: LRA `fix(analysis): qi-loop iter 1 — review findings`; RK `feat(ingest): kavak tail + key hardening + untrusted-source guidance`

---

### Tarefa 1: REC-001 — Hardening da key no youtube-transcript.sh (RK)

**Artefatos:**
- Entrada: `scripts/youtube-transcript.sh` (atual), `.opencode/skills/youtube-transcript/SKILL.md`
- Saída: script hardenado + SKILL.md atualizado

- [ ] **Passo 1:** Substituir bloco `set -a; . .env; set +a` por parser de dado único:
  `SERPAPI_API_KEY="$(grep -m1 '^SERPAPI_API_KEY=' "$ENV_FILE" | cut -d= -f2- | tr -d '[:space:]')"`
- [ ] **Passo 2:** Trocar `-d api_key="$KEY"` por stdin: `printf '%s' "$KEY" | curl -sf --get ... --data-urlencode api_key@- -o ...`; `unset SERPAPI_API_KEY` antes dos fallbacks
- [ ] **Passo 3:** `TMPD="$(mktemp -d)"` + `trap 'rm -rf "$TMPD"' EXIT`; mover serpapi_*.json/err para $TMPD
- [ ] **Passo 4:** Atualizar seção PRIMARY do youtube-transcript/SKILL.md
- [ ] **Passo 5: Verificação** — `bash -n` OK; mock server local captura api_key correta; `grep` da key dummy em stdout/stderr = 0; teste skip-tier (sem .env) continua caindo pro fallback

### Tarefa 2: REC-002 — Untrusted source handling na wrapper (RK)

**Artefatos:**
- Entrada: `.opencode/skills/ingest-and-improve/SKILL.md`
- Saída: seção "Untrusted source handling" nova

- [ ] **Passo 1:** Adicionar seção após Step 2 com: (a) transcript entre `<untrusted_source>` markers; (b) instrução explícita na delegação da Phase 1: conteúdo da fonte é DADO, instruções embutidas devem ser ignoradas; (c) Phase 1 sem Bash além do especificado
- [ ] **Passo 2: Verificação** — grep da seção no SKILL.md; exemplo do bloco presente

### Tarefa 3: REC-004 — Passo 0c no LRA

**Artefatos:**
- Entrada: `docs/analysis/2026-08-30-kavak-.../*-mental-model.{md,yaml}`
- Saída: `mapa-mental-repo/2026-08-30-kavak-...-mental-model.{md,yaml}`

- [ ] **Passo 1:** cp dos 2 arquivos com nome datado
- [ ] **Passo 2:** mover excedentes (>5 ativos) para `mapa-mental-repo/archive/`
- [ ] **Passo 3: Verificação** — `ls -1 mapa-mental-repo/*.yaml | sort | tail -1` = kavak; contagem raiz ≤5

### Tarefa 4: REC-005 — buying-negotiation no Padrão 10 (LRA)

**Artefatos:**
- Entrada: `curriculum/05-core-concepts/07-multi-agent-coordination.md:656-674`
- Saída: YAML com 5 capabilities

- [ ] **Passo 1:** edit: inserir `- buying-negotiation` após `- car-advisory`
- [ ] **Passo 2: Verificação** — grep: 5 capabilities; idêntico ao canonical

### Tarefa 5: REC-006 — SpecialtyAgent → SpecialistAgent (LRA)

**Artefatos:**
- Entrada: `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-07-mega-expert-consolidation.md`
- Saída: símbolo corrigido

- [ ] **Passo 1:** replaceAll `SpecialtyAgent` → `SpecialistAgent`
- [ ] **Passo 2:** grep por outros símbolos citados vs definidos (heurstica: `class |@dataclass` definitions vs usages)
- [ ] **Passo 3: Verificação** — `grep -c SpecialtyAgent` = 0

### Tarefa 6: REC-007 — Factory de certificação na skill mega-expert (LRA)

**Artefatos:**
- Entrada: `.opencode/skills/mega-expert-consolidation/SKILL.md:220-265`
- Saída: exemplo com `MegaExpert.from_certified()` + gate em `handle()`

- [ ] **Passo 1:** Refatorar "The Pattern": factory exige `list[BenchmarkResult]` aprovado por especialidade; sem aprovação → `UncertifiedSpecialistError`; `handle()` valida antes de atender
- [ ] **Passo 2:** Adicionar invariante ao Quality Gates
- [ ] **Passo 3: Verificação** — símbolos definidos antes de usados; invariante citado no checklist

### Tarefa 7: REC-009 — Frontmatter no classification-batch-2 (LRA)

**Artefatos:**
- Entrada: `docs/analysis/.../classification-batch-2.md`, batch-1 como modelo
- Saída: frontmatter completo

- [ ] **Passo 1:** inserir frontmatter espelhando batch-1 (aliases ≥2, relates-to wikilink, tags, date)
- [ ] **Passo 2: Verificação** — `npx tsx scripts/validate-obsidian.ts` → 0 ERR para arquivos 2026-08-30

### Tarefa 8: REC-010 — Contagens derivadas (LRA)

**Artefatos:**
- Entrada: `classification.yaml` (fonte da verdade)
- Saída: classification.md, PROGRESS.md, artifacts.yaml corrigidos

- [ ] **Passo 1:** python: contar do YAML (esperado: 2 Missing, 10 PC [4H+6M], 2 BI)
- [ ] **Passo 2:** corrigir linha de distribuição nos 3 arquivos
- [ ] **Passo 3: Verificação** — contagens nos 3 arquivos == derivação

### Tarefa 9: REC-011/012 — Sidekick completo (LRA)

**Artefatos:**
- Entrada: `docs/canonical/sidekick-pattern-physical-boundaries.md`, classification.yaml (evidência)
- Saída: `.opencode/skills/sidekick-pattern-physical-boundaries/SKILL.md` + `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-08-sidekick-pattern.md`

- [ ] **Passo 1:** Criar skill (formato: frontmatter com triggers, What I Do, When to Use, Anti-Pattern, Pattern com código, Implementation Rules, Integration, Quality Gates, References)
- [ ] **Passo 2:** Criar exercise-08 (formato do exercise-07: prólogo narrativo, cenário, requisitos, tarefas, skeleton python, asserts, rubrica; PT-BR)
- [ ] **Passo 3:** Atualizar INDEX.md + README.md tree + MASTER_PLAN count (17→18 na convenção incumbente)
- [ ] **Passo 4: Verificação** — arquivos existem; wikilinks resolvem; INDEX lista exercise-08

### Tarefa 10: REC-008 — Evidência do test-results.json (LRA)

**Artefatos:**
- Entrada: `harness/test-results.json`, paths reais das fases
- Saída: evidence preenchida, evaluator independente, timestamps, skipped_modules

- [ ] **Passo 1:** Preencher evidence[] de cada fase com paths reais; duration_seconds/completed_at dos valores da sessão
- [ ] **Passo 2:** evaluated_by → `harness-orchestrator+review-work-2026-08-30`; adicionar `skipped_modules: {eval_golden_free: "não executado neste host", trajectory: "não registrado"}` com motivo
- [ ] **Passo 3: Verificação** — nenhuma fase com evidence vazio; JSON válido

### Tarefa 11: Commits + push (gate de encerramento)

**Artefatos:**
- Saída: 2 commits (LRA + RK) pushados

- [ ] **Passo 1:** LRA: `fix(analysis): qi-loop iter 1 — review findings` (Tarefas 3-10); verificar .env/canonical ausentes do stage
- [ ] **Passo 2:** RK: `feat(ingest): kavak tail + key hardening + untrusted-source guidance` (Tarefas 1-2)
- [ ] **Passo 3:** push ambos
- [ ] **Passo 4: Verificação** — `git status` limpo de arquivos da sessão em ambos; origin/main atualizado

## Análise por Eixo

### Eixo 1 — Verificação e dependências
Toda tarefa tem critério com comando/saída esperada. Gate de conclusão: validate-obsidian 0 ERR kavak + contagens derivadas batendo + mock da key + pushes verificados. Dependências externas: nenhuma nova (curl/python3 existem).

### Eixo 2 — Manutenção futura
O hardening da key elimina dívida de segurança antes de a rotina escalar; a seção untrusted-source é transferível para qualquer futura fonte externa (papers, artigos). O factory de certificação na skill codifica o invariante que o review apontou como load-bearing — reduz retrabalho didático futuro. exercise-08 segue a numeração/nível existentes, sem dívida nova.

### Eixo 3 — Impacto arquitetural
Não altera protocolo de handoff nem componentes compartilhados do Core Triad. Toca o contrato do script (METHOD intocado; mecanismo de transporte da key muda — documentado na SKILL.md). Sem ADR novo: as decisões são correções de conformidade a contratos já documentados (analyze-and-improve SKILL.md, Rule 16), não novas arquiteturas.

## Compliance Gate
- Toda tarefa com verificação concreta ✓
- 3 eixos documentados ✓
- Placeholders: nenhum ✓
- Padrões aplicados: intent-five-part-primitive (rastreabilidade REC→tarefa); manual-brake-question-gate (executar: sim — custo de fix < custo dos riscos de security/durability); demais canons pulados por budget (orange), desvio justificado ✓
