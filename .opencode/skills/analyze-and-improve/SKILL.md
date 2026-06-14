---
name: analyze-and-improve
description: "Pipeline completo: documento fonte → extração de conhecimento → padrões reutilizáveis → classificação contra repositório → melhorias priorizadas por impacto → integração. Consome uma fonte externa de conhecimento (talk, paper, transcript, knowledge base) e gera artefatos concretos no repositório alvo (canonical docs, skills, exercises, roadmap). Dispara com: 'analyze this document', 'extract patterns from', 'classify against repo', 'generate improvements', 'knowledge to improvements', 'analyze and improve', 'turn this talk into patterns'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: analysis
  priority: high
---

## Invocation

This skill REQUIRES one mandatory parameter and accepts three optional parameters:

| Parameter | Required | Description |
|---|---|---|
| `source` | **Yes** | Absolute path, URL, or array of paths to the document(s) to analyze. Single file: `Raw-Knowledge/sources/2026-06-09-slug.md`. Multiple files: array of paths (aggregated before Phase 1). Ex: `["Raw-Knowledge/sources/slug.md", "Raw-Knowledge/concepts/related.md", "Raw-Knowledge/entities/tool.md"]` |
| `date` | No | Date for output dir. Defaults to today (`YYYY-MM-DD`). Ex: `2026-06-09` |
| `source-slug` | No | Short slug for output dir. Derived from source filename if omitted. Ex: `12-factor-agents` |
| `incremental` | No | Boolean, default `false`. When `true`, Phase 0 reuses the most recent mental model from `mapa-mental-repo/` and only updates deltas instead of rebuilding from scratch. |

Example invocations:

```
# Single source
Load analyze-and-improve with source=Raw-Knowledge/sources/2026-06-09-12-factor-agents.md, date=2026-06-09, source-slug=12-factor-agents

# Multiple sources (knowledge base: source + concepts + entity)
Load analyze-and-improve with source=["Raw-Knowledge/sources/slug.md", "Raw-Knowledge/concepts/smart-truncation.md", "Raw-Knowledge/entities/alex.md"], date=2026-06-09, source-slug=context-management
```

### Multi-source aggregation

When `source` is an array of paths:

1. Validar que TODOS os arquivos existem.
2. Agregar em um arquivo temporario (`/tmp/opencode/aggregated-<source-slug>.md`).
3. Estruturar o agregado com uma secao por arquivo, preservando:
   - Metadados de proveniencia (path original, tipo — source/concept/entity)
   - Conteudo completo de cada arquivo
4. Incluir no `meta.original_sources` do `analysis.yaml` os paths originais como array.
5. Passar o path do agregado como `SOURCE DOCUMENT` para a Phase 1.

O arquivo agregado e temporario — nao persiste no repositorio apos a analise.

## What I Do

Eu transformo conhecimento externo em melhorias concretas no repositorio. O pipeline tem 7 fases (Phase 6 executada por default, pode ser pulada), todas delegadas a sub-agentes especializados:

0. **Repository Mental Model** — Construir modelo mental do repositorio alvo (delegado: `ultrabrain`)
1. **Knowledge Extraction** — Extrair conhecimento nao-obvio de um documento fonte (delegado: `deep`)
2. **Pattern Extraction** — Identificar padroes reutilizaveis (delegado: `ultrabrain`)
3. **Classification** — Classificar cada padrao contra o repositorio alvo (delegado: `deep`)
4. **Improvement Generation** — Gerar artefatos em 7 categorias, priorizados por impacto (delegado: `deep` em paralelo)
5. **Integration** — Atualizar system-of-record e indices (delegado: `quick`)
6. **Curriculum Deep Integration** (default) — Integrar Missing e Partial Coverage no curriculo existente com profundidade total (delegado: `deep`). Pode ser pulada se o usuario solicitar.

## When to Use Me

Load this skill when:

- Voce tem uma fonte externa de conhecimento (transcript de talk, paper academico, knowledge base entry, documentacao de biblioteca) e quer extrair padroes aplicaveis ao seu repositorio
- Voce quer classificar padroes extraidos contra o que ja existe no codigo/curriculo
- Voce quer gerar um roadmap de melhorias priorizadas por impacto
- Voce quer seguir o mesmo workflow que produziu `docs/analysis/2026-06-09-12-factor-agents/` no repositorio `long-running-agents`

Nao use quando:

- A fonte ja esta analisada e voce so precisa implementar uma melhoria especifica
- O escopo e uma unica mudanca trivial
- Voce nao tem um repositorio alvo para classificar os padroes

## Pre-requisitos

Antes de comecar, verifique:

- [ ] O parametro `source` foi fornecido e o documento fonte existe e esta acessivel (path absoluto ou URL)
- [ ] Os parametros `date` e `source-slug` foram resolvidos (derivados se nao fornecidos)
- [ ] `PROGRESS.md` e `harness/test-results.json` foram inicializados via `setup-analysis.sh` (ou manualmente conforme o template)
- [ ] O diretorio de output `docs/analysis/<date>-<source-slug>/` foi criado
- [ ] O repositorio alvo tem `docs/system-of-record.md` (ou equivalente) para resolver precedencia
- [ ] Voce leu `AGENTS.md` do repositorio alvo para conhecer regras de commit, estilo, e gates
- [ ] Voce leu `docs/canonical/obsidian-document-conventions.md` (se existir) ou o `AGENTS.md` Rule 16 para conhecer as convencoes de frontmatter, wikilinks, tags, aliases, e relates-to

### Execution mechanism

Este pipeline pode ser executado de duas formas. Escolha a correta para seu contexto:

| Mecanismo | Quando usar |
|---|---|
| **Skill `harness-analyze-and-improve`** | Dentro de uma sessao opencode. Usa `task()` nativo para delegar fases. |
| **Bash `harness/harness-analysis.sh`** | Terminal real (bash externo). Invoca `opencode run` para cada fase. |

Ambos os mecanismos dependem de `PROGRESS.md` + `harness/test-results.json` inicializados.
Use o script de bootstrap para prepara-los:

```bash
./.opencode/skills/analyze-and-improve/harness/setup-analysis.sh \
  --source <path> --date YYYY-MM-DD --source-slug <slug> --target-repo <path>
```

O skill harness e recomendado para execucao interativa dentro do opencode. O bash harness e util para automacao externa e CI/CD, mas requer ambiente bash completo (grep, python3/jq, date, mkdir) e **nao funciona quando invocado de dentro de uma sessao opencode**.

**Phase 0 e Phase 1 podem rodar em paralelo** quando o documento fonte (parametro `source`) ja esta disponivel no inicio da sessao. A Phase 0 le o repositorio; a Phase 1 le o documento fonte — sao independentes. Dispare ambas com `run_in_background=true` no mesmo turno e colete os resultados antes de prosseguir para Phase 2.

O orquestrador NAO deve pausar entre fases para check-in. O pipeline avanca automaticamente: coleta output → atualiza PROGRESS.md → dispara proxima fase. Interrupcao so por Commit Gate ou comando explicito.

## Target Repository Context

TODA delegacao via `task()` nas Phases 0-6 DEVE incluir este bloco no prompt:

```
TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: <absolute-path-to-repo>/docs/analysis/<date>-<source-slug>/
  system_of_record: <absolute-path-to-repo>/docs/system-of-record.md
  branch: main
```

**CRITICAL**: Todos os paths no bloco devem ser absolutos (ex: `/home/user/repo/docs/analysis/...`). Nunca use paths relativos — sub-agentes podem resolver `docs/analysis/...` a partir de diretorios de trabalho diferentes, escrevendo em locais incorretos. O `output_dir` e `system_of_record` devem ser paths completos.

Isso garante que todo sub-agente sabe:
- Onde escrever arquivos de output (caminho completo)
- Qual repositorio sera commitado (para mensagens de commit e referencias)
- Onde encontrar as regras de precedencia (`system-of-record.md`)
- Qual branch usar

## Output Directory Structure

TODOS os outputs das fases 0-4 vao para o mesmo diretorio:

```
docs/analysis/<date>-<source-slug>/
  <date>-<source-slug>-mental-model.md        # Phase 0
  <date>-<source-slug>-mental-model.yaml
  <date>-<source-slug>-analysis.md            # Phase 1
  <date>-<source-slug>-analysis.yaml
  <date>-<source-slug>-patterns.md            # Phase 2
  <date>-<source-slug>-patterns.yaml
  <date>-<source-slug>-classification.md      # Phase 3
  <date>-<source-slug>-classification.yaml
```

Artefatos concretos (canonical docs, skills, exercises) gerados na Phase 4 vao para seus diretorios definitivos (`docs/canonical/`, `.opencode/skills/`, `curriculum/`).

## Mapa Mental Repository

O diretorio `mapa-mental-repo/` na raiz do repositorio alvo versiona os modelos mentais
com data, servindo como cache canonico para o modo incremental:

```
mapa-mental-repo/
  YYYY-MM-DD-<source-slug>-mental-model.md
  YYYY-MM-DD-<source-slug>-mental-model.yaml
  archive/                              # Modelos alem dos 5 mais recentes ou com > 90 dias
```

**Regras:**
- Todo modelo mental gerado na Phase 0 (full ou incremental) DEVE ser copiado para ca.
- O nome do arquivo inclui a data E o `source-slug` para rastreabilidade bidirecional.
- Manter no maximo 5 modelos ativos na raiz; mover os excedentes para `archive/`.
- Modelos em `archive/` com mais de 90 dias podem ser removidos.
- Este diretorio e versionado no git — faz parte do repositorio.

---

## Phase 0: Repository Mental Model

**Objetivo:** Antes de analisar o documento externo, construir ou atualizar um modelo mental do repositorio alvo — entender goals, arquitetura, padroes, abstracoes e terminologia. Esse modelo serve como contexto canonico para todas as fases subsequentes.

Dois modos de operacao, controlados pelo parametro `incremental`:

### Modo Full Rebuild (`incremental=false` — default)

Comportamento padrao: o agente `ultrabrain` le o repositorio do zero e constroi
o modelo mental completo. Use quando:
- E a primeira execucao no repositorio (`mapa-mental-repo/` vazio)
- O modelo anterior tem mais de 30 dias
- Os deltas detectados somam mais de 10 itens
- Voce quer garantia de consistencia total

#### Delegacao (Full Rebuild)

Delegue para `ultrabrain`:

```typescript
task(
  category="ultrabrain",
  load_skills=[],
  run_in_background=true,
  prompt="TASK: Build a mental model of the target repository.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

First, read and understand the repository by examining:
- AGENTS.md (operational rules, commit style, gates)
- README.md (project goals, overview)
- docs/system-of-record.md (documentation precedence, domain map)
- docs/canonical/ (authoritative descriptions of systems)
- docs/decisions/ (accepted ADRs)
- curriculum/ (structure, levels, concepts, glossary)
- .opencode/agents/ (agent definitions, handoff protocol)
- .opencode/skills/ (existing skills and their domains)

Build a structured mental model covering:
1. Project Goals — what the repository builds or teaches
2. Architecture — core abstractions and their relationships
3. Patterns — existing design and implementation patterns
4. Abstractions — key terminology and concepts (from glossary and canonical docs)
5. Curriculum Structure — progression, levels, exercises
6. Existing Gaps — what is documented as missing or pending

Do not analyze the external source document yet. Focus ONLY on the repository.

OUTPUT: Write TWO files in <output_dir>:
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-mental-model.md — structured markdown with the sections above
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-mental-model.yaml — typed mirror with the same structure

The YAML must use typed fields:
  meta: {title, date, repo, type: 'mental-model'}
  goals: [list of goals]
  architecture: {abstractions: [...], relationships: [...]}
  patterns: [{name, where_defined, maturity}]
  terminology: [{term, definition, source}]
  curriculum: {levels: [...], concepts: [...]}
  gaps: [{what, where_documented}]"
)
```

### Output

```
docs/analysis/<date>-<source-slug>/<date>-<source-slug>-mental-model.md
docs/analysis/<date>-<source-slug>/<date>-<source-slug>-mental-model.yaml
```

#### Gate (Full Rebuild)

- [ ] O modelo mental cobre goals, arquitetura, padroes, abstracoes, terminologia e gaps
- [ ] Ambos os arquivos (.md e .yaml) foram escritos no diretorio correto

### Modo Incremental (`incremental=true`)

Quando `incremental=true`, o orquestrador executa um fluxo de 3 passos.
Apenas o Passo 0b e delegado; os Passos 0a e 0c sao executados diretamente pelo orquestrador.

#### Passo 0a: Validacao rapida (orquestrador — NAO delegar)

1. **Verificar cache**: Liste `mapa-mental-repo/` no repositorio alvo.
   Se o diretorio nao existe ou esta vazio: **fallback imediato para full rebuild**.
2. **Carregar modelo anterior**: Identifique o arquivo `.yaml` mais recente por data no nome
   (use `ls -1 mapa-mental-repo/*.yaml | sort | tail -1`).
   Leia o YAML completo — ele sera a base do modelo atualizado.
3. **Scan rapido de deltas** desde a data do modelo anterior:
   ```bash
   # Novos canonical docs
   find docs/canonical/ -name '*.md' -newer mapa-mental-repo/<ultimo>.yaml
   # Novos ADRs
   find docs/decisions/ -name '*.md' -newer mapa-mental-repo/<ultimo>.yaml
   # Novos arquivos no curriculum
   find curriculum/ -name '*.md' -newer mapa-mental-repo/<ultimo>.yaml
   # Novas skills
   ls -lt .opencode/skills/ | head -20
   # Novos agentes
   ls -lt .opencode/agents/ | head -20
   ```
4. **Classificar deltas** e produzir `docs/analysis/<date>-<source-slug>/delta-report.md`:
   - Cada delta classificado: `novo-canonical-doc`, `novo-adr`, `novo-exercicio`,
     `nova-licao`, `nova-skill`, `novo-agente`, `atualizacao`
   - Para cada delta: path do arquivo, data de modificacao, breve descricao do conteudo
   - Contagem total de deltas
   - Data do modelo anterior usado como base
5. **Decidir modo**: Conte os deltas. Se `total_deltas > 10` OU
   `dias_desde_modelo_anterior > 30`: **fallback para full rebuild**.
   Caso contrario: prossiga para o Passo 0b.

#### Passo 0b: Atualizacao incremental (delegado para `ultrabrain`)

```typescript
task(
  category="ultrabrain",
  load_skills=[],
  run_in_background=true,
  prompt="TASK: Update the repository mental model incrementally using the previous model as base.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: <absolute-path-to-repo>/docs/analysis/<date>-<source-slug>/
  system_of_record: <absolute-path-to-repo>/docs/system-of-record.md
  branch: main

PREVIOUS MENTAL MODEL (YAML) — use this as your base structure:
<paste the FULL content of mapa-mental-repo/<ultimo>-mental-model.yaml>

DELTA REPORT — only these items need attention:
<paste the FULL content of delta-report.md>

INSTRUCTIONS:
1. Load the previous mental model as your base. Keep ALL existing entries
   that are NOT affected by the deltas — do not re-describe them.
2. For each delta in the delta report, decide:
   - NEW ENTRY: add to the relevant section (goals, architecture, patterns,
     terminology, curriculum, gaps). Read the source file to understand it.
   - UPDATE: modify an existing entry's fields. Cite what changed and why.
   - NO CHANGE: the entry already accurately describes the current state.
3. Update meta.date to today's date.
4. Add meta.based_on: pointing to the previous model file name.
5. Update the gaps section: remove gaps that were resolved (new docs, new ADRs),
   add any new gaps discovered during delta analysis.
6. Do NOT re-read the entire repository. Trust the base model for untouched areas
   and only read files referenced in the delta report.

OUTPUT: Write TWO files:
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-mental-model.md — updated markdown
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-mental-model.yaml — updated typed mirror

The YAML must use the same typed fields as full rebuild, plus:
  meta: {title, date, repo, type: 'mental-model', based_on: '<previous-model-filename>'}
  goals: [list of goals]
  architecture: {abstractions: [...], relationships: [...]}
  patterns: [{name, where_defined, maturity}]
  terminology: [{term, definition, source}]
  curriculum: {levels: [...], concepts: [...]}
  gaps: [{what, where_documented}]"
)
```

#### Passo 0c: Salvamento em `mapa-mental-repo/` (orquestrador — sempre executar)

Apos QUALQUER Phase 0 (full rebuild OU incremental), o orquestrador DEVE:

1. **Criar o diretorio se necessario**:
   ```bash
   mkdir -p mapa-mental-repo/archive
   ```
2. **Copiar os arquivos** com timestamp:
   ```bash
   cp docs/analysis/<date>-<source-slug>/mental-model.md  \
      mapa-mental-repo/<date>-<source-slug>-mental-model.md
   cp docs/analysis/<date>-<source-slug>/mental-model.yaml \
      mapa-mental-repo/<date>-<source-slug>-mental-model.yaml
   ```
3. **Enforce o limite de 5 modelos ativos**:
   ```bash
   # Listar modelos .yaml por data, pular os 5 mais recentes, mover o resto
   ls -1 mapa-mental-repo/*-mental-model.yaml | sort -r | tail -n +6 | while read yaml; do
     md="${yaml%.yaml}.md"
     mv "$yaml" "$md" mapa-mental-repo/archive/
   done
   ```
4. **Limpeza de archive (> 90 dias)**:
   ```bash
   find mapa-mental-repo/archive/ -name '*.yaml' -mtime +90 -delete
   find mapa-mental-repo/archive/ -name '*.md' -mtime +90 -delete
   ```
5. **Commit implicito**: Os arquivos em `mapa-mental-repo/` sao parte do repositorio
   e serao commitados junto com os demais artefatos da sessao (respeitando o Commit Gate).

#### Gate (Incremental)

- [ ] `delta-report.md` existe em `docs/analysis/<date>-<source-slug>/`
- [ ] Modelo anterior foi carregado com sucesso e seu path esta registrado
- [ ] Fallback para full rebuild foi considerado e a decisao esta documentada
- [ ] O modelo mental atualizado cobre todas as secoes obrigatorias
- [ ] Ambos os arquivos (.md e .yaml) foram escritos no diretorio correto
- [ ] Passo 0c executado: copias em `mapa-mental-repo/` existem

---

## Phase 1: Knowledge Extraction

**Objetivo:** Extrair conhecimento nao-obvio do documento fonte. Filtrar ruido. Produzir analise estruturada.

### Regras de extracao

| Manter | Ignorar |
|---|---|
| Frameworks, arquiteturas, workflows | Marketing, auto-promocao |
| Detalhes de implementacao | Anedotas, historias pessoais |
| Licoes operacionais, falhas, tradeoffs | Repeticao, padding, filler |
| Decisoes de design com justificativa | Conselhos genericos sem mecanica |
| Anti-padroes documentados | "E importante fazer X" sem o como |

### Delegacao

Delegue para `deep`:

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=true,
  prompt="TASK: Extract all non-obvious knowledge from the source document below.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

SOURCE DOCUMENT: <paste full content or provide path>

IGNORE: marketing, anecdotes, personal stories, repetition.
KEEP: frameworks, patterns, architectures, workflows, implementation
details, operational lessons, failures, tradeoffs.

OUTPUT: Write TWO files in <output_dir>:
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-analysis.md — structured markdown with sections for:
  1. Frameworks & Models — conceptual structures presented
  2. Patterns & Architectures — reusable designs with mechanics
  3. Operational Lessons — what worked, what failed, what surprised
  4. Tradeoffs — explicit cost/benefit discussions
  5. Failure Patterns — what breaks and why
  6. Synthesis — cross-cutting insights the author may not have named
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-analysis.yaml — typed mirror with the same structure

The YAML must use typed fields:
  meta: {title, source, date, type: 'analysis'}
  frameworks: [{name, components: [...]}]
  patterns: [{name, problem, mechanism}]
  operational_lessons: [{lesson, context}]
  tradeoffs: [{decision, benefit, cost}]
  failure_patterns: [{pattern, cause, mitigation}]
  synthesis: string"
)
```

### Output

```
docs/analysis/<date>-<source-slug>/<date>-<source-slug>-analysis.md
docs/analysis/<date>-<source-slug>/<date>-<source-slug>-analysis.yaml
```

### Gate

- [ ] Os arquivos analysis.md e analysis.yaml existem no diretorio de output
- [ ] Nao contem marketing, anedotas, ou filler
- [ ] O YAML espelha o markdown com campos tipados
- [ ] `analysis.md` tem frontmatter Obsidian completo: `title`, `type: analysis`, `tags`, `date`, `aliases` (pelo menos 2), `relates-to` (pelo menos 1 wikilink)
- [ ] Rodar `bash scripts/check-obsidian-conventions.sh` (se existir) e corrigir violacoes ANTES de prosseguir para Phase 2. Violacoes nao corrigidas viram falso-positivos em todas as fases subsequentes.

---

## Phase 2: Pattern Extraction

**Objetivo:** Identificar padroes reutilizaveis a partir do conhecimento extraido. Delegar para sub-agente ultrabrain.

### Regras de extracao de padroes

Cada padrao deve ter 6 campos obrigatorios:

| Campo | Descricao |
|---|---|
| **name** | Nome descritivo (ex: "Error Context Hygiene") |
| **problem solved** | Qual problema resolve, em uma frase |
| **inputs** | O que o padrao consome (dados, estado, contexto) |
| **outputs** | O que o padrao produz (decisoes, artefatos, acoes) |
| **benefits** | O que melhora em relacao a nao usar o padrao |
| **limitations** | Quando o padrao nao funciona ou tem custo alto |

### Delegacao

Delegue para `ultrabrain`:

```typescript
task(
  category="ultrabrain",
  load_skills=[],
  run_in_background=true,
  prompt="TASK: Identify reusable patterns from the knowledge extraction below.
Only keep patterns applicable to agentic systems.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

For each pattern, provide: name, problem solved, inputs, outputs,
benefits, limitations. Then produce a YAML mirror adding components
(list of sub-elements) and flow (sequence of steps) per pattern.

OUTPUT: Write TWO files in <output_dir>:
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-patterns.md
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-patterns.yaml

KNOWLEDGE EXTRACTION:
<paste the markdown analysis from Phase 1>"
)
```

### Output

```
docs/analysis/<date>-<source-slug>/<date>-<source-slug>-patterns.md
docs/analysis/<date>-<source-slug>/<date>-<source-slug>-patterns.yaml
```

### Gate

- [ ] Cada padrao tem os 6 campos obrigatorios preenchidos
- [ ] O YAML adiciona `components` e `flow` por padrao

---

## Phase 3: Classification

**Objetivo:** Comparar cada padrao contra o que ja existe no repositorio alvo. Classificar em 4 categorias com evidencia.

> **Batch splitting**: Para fontes com mais de 8 padroes, divida a classificacao em lotes menores (max 8 padroes por agente) e execute em paralelo. Um unico agente `deep` pode abortar por timeout ao classificar muitos padroes. Se `deep` falhar, `ultrabrain` e um fallback confiavel.

### Regras de classificacao

| Classe | Significado | Quando usar |
|---|---|---|
| **Already Exists** | Padrao documentado, implementado, ou ensinado com profundidade equivalente | Repo tem doc, codigo, OU curriculo cobrindo o mesmo terreno |
| **Partial Coverage** | Elementos existem mas faltam mecanicas-chave, reframe, ou formalizacao | Repo faz algo similar mas sem o nome, a decomposicao, ou o framing |
| **Missing** | Nao presente em nenhuma forma | Nem doc, nem codigo, nem curriculo — gap total |
| **Better Implementation** | Repo tem versao superior ou mais madura da mesma ideia | Repo vai alem do que o padrao descreve |

### Evidencia obrigatoria

Para cada classificacao, forneca:

- **Already Exists**: cite o arquivo e a linha ou secao que comprova (ex: `curriculum/05-core-concepts/07-multi-agent-coordination.md:42-78`)
- **Partial Coverage**: liste o que existe E o que falta
- **Missing**: mostre onde procurou e confirme `NOT_FOUND`
- **Better Implementation**: explique porque a versao do repo e superior

### Fontes de evidencia (em ordem de precedencia)

Siga `docs/system-of-record.md`:

1. `docs/decisions/` — ADRs aceitos
2. `docs/canonical/` — documentacao canonica ativa
3. `docs/evidence/` — evidencias validadas
4. `docs/analysis/` — analises e diagnosticos
5. `curriculum/` — material de ensino
6. READMEs e resumos operacionais

### Delegacao

Delegue para `deep`:

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=true,
  prompt="TASK: Classify each extracted pattern against the target repository using evidence-based classification.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

CLASSIFICATION RULES:
- Already Exists: pattern is documented, implemented, or taught at equivalent depth
- Partial Coverage: elements exist but key mechanics, reframe, or formalization are missing
- Missing: not present in any form (doc, code, or curriculum)
- Better Implementation: repo has a superior or more mature version of the same idea

EVIDENCE REQUIREMENTS:
For every classification, cite file:line references. For 'Missing', confirm NOT_FOUND
with the locations searched. Follow the precedence order from system-of-record.md:
decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs.

Read the repository mental model at docs/analysis/<date>-<source-slug>/<date>-<source-slug>-mental-model.md
for quick orientation. Then search the repo (grep, read files) for each pattern.

PATTERNS TO CLASSIFY:
<paste the patterns.md or patterns.yaml from Phase 2>

OUTPUT: Write TWO files in <output_dir>:
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.md — one section per pattern with:
  - Classification + justification
  - Evidence (file:line references or NOT_FOUND)
  - Integration value (Low/Medium/High)
  - Summary table at the end
- docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.yaml — typed mirror

Summary table format:
| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | ... | Already Exists | Low |
| 2 | ... | Partial Coverage | Medium |
| ... | ... | ... | ... |"
)
```

### Output

```
docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.md
docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.yaml
```

### Gate

- [ ] Cada padrao classificado com evidencia file:line ou `NOT_FOUND`
- [ ] Tabela-sumario no final do markdown
- [ ] As fontes de evidencia respeitam a precedencia do `system-of-record.md`

---

## Phase 4: Improvement Generation

**Objetivo:** Gerar artefatos concretos no repositorio, priorizados pelo impacto da classificacao.

### Categorias de melhoria

| Categoria | Onde criar | Exemplo |
|---|---|---|
| **New Skills** | `.opencode/skills/<slug>/SKILL.md` | Skill de implementacao para padrao Missing |
| **New Patterns** | `docs/canonical/<slug>.md` | Doc canonico formalizando padrao Partial |
| **New Examples** | `docs/analysis/examples/` ou inline em exercicios | Before/after de codigo demonstrando o padrao |
| **New Exercises** | `curriculum/0X-nivel-X-*/exercises/exercise-0X.md` | Exercicio hands-on para o curriculo |
| **New Documentation** | `docs/analysis/` ou `docs/canonical/` | Roadmap de integracao, cross-reference |
| **New Agent Architectures** | `docs/canonical/` | Decomposicao arquitetonica com componentes |
| **New Runtime Features** | `.opencode/skills/<slug>/SKILL.md` (patterns section) | Padroes de implementacao code-ready |

### Priorizacao por impacto

| Classification | Priority | Acao |
|---|---|---|
| **Missing** | P0 | Criar canonical doc + skill + exercise + example |
| **Partial Coverage (High value)** | P1 | Criar canonical doc com reframe/naming |
| **Partial Coverage (Medium value)** | P2 | Criar canonical doc, postergar exercise |
| **Already Exists** | — | Apenas cross-reference, nao criar artefatos novos |
| **Better Implementation** | — | Documentar superioridade, nao duplicar |

### Ordem de criacao

1. **Canonical docs primeiro** — `docs/canonical/` e o nivel 2 de precedencia. Docs canonicos estabelecem a verdade antes de exercicios e skills referenciarem eles.
2. **Skills para padroes Missing** — Skills de implementacao tem maior reuso.
3. **Exercises para Missing e P1** — Exercicios solidificam aprendizado.
4. **Roadmap de integracao** — Conecta tudo ao curriculo existente.

### Delegacao (paralela)

Para padroes Missing e P1, dispare agentes `deep` em paralelo — um por tipo de artefato:

**Agente 1: Canonical Docs**

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=true,
  prompt="TASK: Create canonical docs for patterns classified as Missing or P1.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

Read docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.md for the list of patterns
to create canonical docs for (Missing and P1 only).

EACH CANONICAL DOC must contain:
- Type, Status, Source, Classification, Precedence
- Problem (what the pattern solves)
- Solution (detailed mechanism)
- Implementation in this repo (what already exists, what is missing)
- Tradeoffs (benefit vs cost table)
- Relationship to Other Patterns (dependencies and complements)
- References (links to analyses, code, curriculum)

Write files to: docs/canonical/<slug>.md"
)
```

**Agente 2: Skills**

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=true,
  prompt="TASK: Create implementation skills for patterns classified as Missing.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

Read docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.md for Missing patterns.

EACH SKILL must contain:
- Frontmatter with name, description rich in triggers, metadata
- What I Do (contract)
- When to Use Me (positive and negative triggers)
- The Anti-Pattern (wrong code)
- The Pattern (correct code)
- Implementation rules (classifier, summarizer, format rules)
- Integration with existing repo infrastructure
- Quality Gates (verification checklist)
- References

Write files to: .opencode/skills/<slug>/SKILL.md"
)
```

**Agente 3: Exercises**

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=true,
  prompt="TASK: Create curriculum exercises for patterns classified as Missing.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

Read docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.md for Missing patterns.

EACH EXERCISE must follow the curriculum format:
- Narrative prologue (realistic scenario that went wrong)
- Scenario with input data
- Functional and technical requirements
- Task in parts (diagnosis → implementation → pipeline)
- Skeleton code in Python
- Acceptance criteria with asserts
- Evaluation rubric

Write files to: curriculum/<appropriate-level>/exercises/exercise-<XX>-<slug>.md"
)
```

<!-- OBSOLETO: Agent 4 (Integration Roadmap) fundido na Phase 5. A geracao do roadmap
     agora e feita como "Artifacts Created Summary" dentro da propria Phase 5. -->

Os agentes 1-3 rodam em paralelo (`run_in_background=true`).

### Gate

- [ ] Missing patterns tem canonical doc + skill + exercise
- [ ] P1 patterns (Partial Coverage High) tem canonical doc
- [ ] P2 patterns (Partial Coverage Medium) tem canonical doc (exercise opcional, a criterio do orquestrador)
- [ ] Integration roadmap conecta todos os artefatos criados
- [ ] Nao foram criados artefatos para Already Exists ou Better Implementation
- [ ] **0 Missing e esperado**: Nem toda fonte produz padroes Missing. Se todos forem Partial Coverage ou Already Exists, as acoes P0 (skill + exercise) simplesmente nao se aplicam. Isso nao e falha do pipeline.
- [ ] **Exercicios novos sao criados na Phase 4, NAO na Phase 6.** A Phase 4 pode criar novos arquivos em `curriculum/` (exercises). A Phase 6 apenas modifica arquivos existentes — nunca cria novos. Se um exercise for necessario, crie-o aqui na Phase 4.

---

## Phase 5: Integration

**Objetivo:** Atualizar documentos de indice que ficaram desatualizados.

### O que verificar

| Documento | O que atualizar |
|---|---|
| `docs/system-of-record.md` | Se canonical/ ou analysis/ ganharam arquivos, atualizar tabelas. Se tinha claim "vazio", corrigir. Atualizar data. |
| `curriculum/INDEX.md` | Se novos exercicios foram criados, adicionar a listagem. |
| `curriculum/README.md` | Se a arvore de diretorios mudou, atualizar diagrama. |
| `curriculum/MASTER_PLAN.md` | Se contagem de exercicios ou topicos mudou, atualizar. |

### Artifacts Created Summary

Antes de atualizar os indices, o agente DEVE ler os outputs da Phase 4 (canonical docs, skills, exercises) e gerar uma secao de "Artifacts Created" dentro do proprio system-of-record.md ou como subsecao da atualizacao. Isso substitui a antiga Agent 4 (Integration Roadmap separado).

### Delegacao

Delegue para `quick`:

```typescript
task(
  category="quick",
  load_skills=["git-master"],
  run_in_background=false,
  prompt="TASK: Update index documents that became stale after improvement generation.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

CHECK AND UPDATE:
1. docs/system-of-record.md — add new canonical docs and skills to tables; update last-modified date
2. curriculum/INDEX.md — add new exercises to the listing
3. curriculum/README.md — update directory tree if changed
4. curriculum/MASTER_PLAN.md — update exercise/topic counts if changed

Then run: git diff --stat to confirm which files were changed.
Do NOT commit. The orchestrator handles the commit decision."
)
```

### Gate

- [ ] `git diff --stat` mostra apenas arquivos relacionados a essa sessao
- [ ] `docs/system-of-record.md` reflete o novo estado (data atualizada)

### Commit Gate

Apos a Phase 5 (e Phase 6 se executada), o orquestrador DEVE:

1. Rodar `git diff --stat` para confirmar o escopo das mudancas.
2. **Perguntar ao usuario:** "Quer commitar?"
3. Se sim: commit com estilo do repo (`type(scope): short description`).
4. **Perguntar ao usuario:** "Quer fazer push?"
5. Se sim: `git push origin main`.

NUNCA commitar ou dar push sem pergunta explicita. O `AGENTS.md` do repositorio alvo tem precedencia — se ele diz "Do not commit unless the user explicitly asks", respeite.

---

## Phase 6: Curriculum Deep Integration (default — pode ser pulada)

Esta fase faz parte do pipeline default. O orquestrador a executa automaticamente apos a Phase 5. O usuario pode pular a Phase 6 explicitamente ("pule a Phase 6", "nao faca a integracao curricular").

**Objetivo:** Integrar padroes Missing e Partial Coverage no curriculo existente. Para Partial Coverage, enriquece modulos que ja tratam do tema com a mecanica que faltava. Para Missing, garante que o novo conceito nao viva isolado — os core concepts, checklists e playbooks que tratam do mesmo dominio ganham a profundidade que o tema merece, indo alem de um simples cross-reference.

### Quando executar

| Classification + Value | Executar Phase 6? | Tratamento |
|---|---|---|
| **Missing** + High | SIM | Canonical doc + skill + exercise (Phase 4) + integracao profunda nos modulos existentes (Phase 6) |
| **Missing** + Medium | SIM | Mesmo tratamento — Missing sempre merece integracao nos modulos que tratam do dominio |
| Partial Coverage + High | SIM | Enriquece modulos existentes com a mecanica que faltava |
| Partial Coverage + Medium | SIM | Phase 6 ou apenas canonical doc, a criterio do orquestrador |
| Already Exists | NAO | So cross-reference nos artefatos da propria sessao |
| Better Implementation | NAO | Documentar superioridade, nao duplicar |

### Fluxo

```
Phase 6: Curriculum Deep Integration
  ├── 6a. Gap analysis — cruzar classification com arquivos do curriculum/
  │     Para Missing: identificar quais core concepts, checklists e playbooks
  │     tratam do mesmo dominio e devem ganhar a nova mecanica.
  │     Para Partial Coverage: identificar quais arquivos ja tratam do tema
  │     e onde falta a mecanica, nome, teste ou gate.
  │     Em ambos os casos: secoes e linhas exatas onde o tema aparece.
  ├── 6b. Insertion plan — mapear arquivo + secao + linha para cada padrao
  │     Respeitar a taxonomia e formato de cada documento do curriculo.
  │     Para Missing: a profundidade e a mesma de Partial Coverage — o conceito
  │     novo merece subsecoes, checklists, gates e exemplos nos modulos existentes.
  ├── 6c. Executor prompt — construir prompt autocontido com instrucoes de `edit`
  │     cirurgicas, sem `write` (nunca reescrever arquivos inteiros)
  ├── 6d. Delegated execution — agente `deep` modifica arquivos do curriculum/
  └── Gate: git diff --stat mostra apenas curriculum/ + system-of-record.md
```

### Regras

- NUNCA criar arquivos novos no `curriculum/` — apenas modificar existentes.
- NUNCA modificar os canonicos em `docs/canonical/` (ja sao a verdade).
- Respeitar formato, estilo e idioma (PT-BR) de cada arquivo do curriculo.
- Usar `edit` para insercoes cirurgicas, nunca `write`.
- Preservar a ordem de dependencia entre padroes (ex: stable harness antes de head-tail truncation).
- **Missing e Partial Coverage recebem a mesma profundidade de integracao.** A diferenca e o ponto de partida: Missing parte do zero (conceito novo), Partial Coverage parte do que ja existe (enriquece).

### Delegacao

Delegue para `deep`:

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=false,
  prompt="TASK: Execute curriculum deep integration for Missing and Partial Coverage patterns.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

Read docs/analysis/<date>-<source-slug>/<date>-<source-slug>-classification.md for patterns to integrate:
- ALL Missing patterns (regardless of Integration Value)
- Partial Coverage patterns with Integration Value High

PHASE 6a — Gap Analysis:
For each target pattern, cross-reference with curriculum files:
- Search curriculum/ for related content (grep by concept name, mechanism keywords)
- Read matching files to understand format, style, and existing coverage
- Identify exact insertion points: file + section + line range
- For Missing: find the core concepts, checklists, and playbooks that should
  teach this new concept. The bar is: 'se um aluno lesse so os core concepts,
  ele sairia sabendo que esse padrao existe e por que importa?'

PHASE 6b — Insertion Plan:
Map every pattern to specific edit locations. Output a plan with:
- File path, section name, line range
- What to add (subsection, checklist item, test case, dataclass, gate, example)
- How it connects to existing content
- For Missing patterns: plan must include subsections in core concepts (not just
  cross-references), checklist items in harness design, and gates in playbooks —
  same depth as Partial Coverage.

PHASE 6c — Executor Prompt:
Build a self-contained prompt for the execution agent. Include:
- Exact `edit` instructions with oldString/newString pairs
- Order of operations (respect pattern dependencies)
- Verification steps after each edit

PHASE 6d — Execute:
Apply all edits to curriculum files. After all edits:
- Run git diff --stat (only curriculum/ files should be modified)
- Verify docs/canonical/ is untouched
- Report summary of changes grouped by classification (Missing vs Partial)

MUST NOT:
- Create new files in curriculum/
- Modify any file in docs/canonical/
- Use write (use edit for surgical insertions)
- Add shallow 1-line cross-references for Missing — Missing merece a mesma
  profundidade que Partial Coverage (subsecoes, exemplos, checklists, gates)
- Commit changes"
)
```

### Gate

- [ ] Apenas arquivos em `curriculum/` foram modificados (confirmar com `git diff --name-only`)
- [ ] `docs/canonical/` nao foi alterado
- [ ] Nenhum arquivo novo foi criado no `curriculum/`
- [ ] Formato e estilo de cada arquivo foram preservados
- [ ] Missing patterns tem integracao com mesma profundidade que Partial Coverage
- [ ] Commit Gate executado apos esta fase (perguntar ao usuario)

---

## Anti-Patterns

- **Executar fases diretamente em vez de delegar.** Toda fase deve ser uma sub-task via `task()` com categoria adequada — o orquestrador supervisiona, nao executa.
- **Pular a Phase 0.** Sem modelo mental do repositorio, as fases subsequentes classificam sem contexto e produzem duplicacao.
- **Esquecer o bloco TARGET_REPOSITORY em uma delegacao.** Sem ele, o sub-agente nao sabe onde escrever outputs nem qual repo commitara.
- **Usar paths relativos no TARGET_REPOSITORY ou nos prompts.** Sempre use paths absolutos. Sub-agentes podem resolver paths relativos a partir de diretorios de trabalho diferentes, escrevendo arquivos no local errado.
- **Pular a classificacao** e gerar melhorias sem evidencia do que ja existe. Isso produz duplicacao.
- **Criar artefatos para Already Exists.** So cross-reference.
- **Delegar extracao de padroes para quick.** Precisa de ultrabrain — e trabalho de sintese.
- **Esquecer o YAML mirror.** Toda analise e classificacao deve ter .md + .yaml. O YAML permite consumo programatico futuro.
- **Ignorar system-of-record.md.** A precedencia importa — nao classifique como Missing sem verificar canonical/ e decisions/.
- **Criar exercises sem esqueleto de codigo.** O formato do curriculo exige codigo Python com dataclasses e asserts.
- **Atualizar system-of-record sem atualizar a data.** A data de ultima atualizacao no rodape e o unico sinal de frescor.
- **Invocar a skill sem fornecer o parametro `source`.** A skill nao tem como adivinhar qual documento analisar.
- **Agregar multiplos sources sem preservar proveniencia.** Quando `source` for array, o `analysis.yaml` deve incluir `meta.original_sources` com os paths originais. Sem isso, a rastreabilidade e perdida.
- **Executar Phase 6 para Already Exists ou Better Implementation.** So cross-reference — o curriculo ja cobre ou supera o padrao.
- **Tratar Missing com cross-reference raso na Phase 6.** Missing e o gap mais importante — merece a mesma profundidade que Partial Coverage: subsecoes, exemplos, checklists, gates nos modulos existentes.
- **Criar arquivos novos no curriculum/ durante a Phase 6.** A integracao profunda modifica modulos existentes, nunca cria novos. Exercicios novos sao criados na Phase 4, nao na Phase 6.
- **Confundir criacao de arquivos entre Phase 4 e Phase 6.** Phase 4 PODE criar novos arquivos (exercises, skills, canonical docs). Phase 6 NUNCA cria novos arquivos — apenas modifica existentes com `edit` cirurgico.
- **Committar ou dar push sem perguntar ao usuario.** O Commit Gate exige confirmacao explicita. O `AGENTS.md` do repo alvo tem a palavra final.
- **Usar `edit` para atualizar PROGRESS.md.** PROGRESS.md e curto e `edit` frequentemente falha por whitespace. Use `write` (reescrita completa) para atualiza-lo.
- **Deixar `analysis.md` sem `aliases:` no frontmatter.** O check-obsidian-conventions.sh reporta erro que polui todas as fases subsequentes. Preencha `aliases` com pelo menos 2 variantes do titulo.
- **Usar `incremental=true` sem modelos anteriores.** Se `mapa-mental-repo/` esta vazio, o modo incremental faz fallback para full rebuild automaticamente — mas isso indica que o parametro foi usado sem necessidade.
- **Forcar incremental quando o repo mudou muito.** Se deltas > 10 itens ou modelo anterior > 30 dias, faca full rebuild. O custo do full rebuild e menor que o risco de inconsistencia por atualizacao parcial.
- **Delegar o Passo 0a (validacao de deltas).** O scan rapido de deltas e responsabilidade do orquestrador — requer acesso ao filesystem e comandos `find`/`ls`. Nao delegue para sub-agente.
- **Esquecer de executar o Passo 0c.** Sem a copia em `mapa-mental-repo/`, a proxima execucao incremental nao tem base para comparar. Isso quebra o modo incremental silenciosamente.
- **Acumular mais de 5 modelos ativos em `mapa-mental-repo/`.** O Passo 0c ja faz a limpeza automatica, mas se houver falha nesse passo, o diretorio polui e dificulta identificar o modelo mais recente.
- **Esperar input do usuario entre fases.** O pipeline e deterministico: output da fase N e input da N+1. Apos cada `task()` completar, o orquestrador DEVE coletar o resultado, atualizar PROGRESS.md e disparar a proxima fase IMEDIATAMENTE. Os unicos gates que param o pipeline sao o Commit Gate (perguntar antes de commit/push) e interrupcao explicita do usuario.
- **Usar `incremental=true` em repositorios diferentes do long-running-agents.** O modo incremental depende da convencao `mapa-mental-repo/`. So use em repositorios que adotaram essa convencao.
- **Usar sync para fases de leitura pesada.** Fases que leem mais de 5 arquivos ou usam `ultrabrain`/`deep` como categoria DEVEM usar `run_in_background=true`. O harness interpreta silencio como travamento em sync; background tem janela de inatividade maior e evita aborts. Aplica-se a Phases 0, 1, 2 e 3.

---

## Verification Gates

Depois de completar as fases (0-5 obrigatorias, 6 executada por default — pode ser pulada):

- [ ] O parametro `source` foi fornecido e validado antes de qualquer execucao
- [ ] Se `source` for array: agregacao produziu arquivo temporario com metadados de proveniencia
- [ ] `docs/analysis/<date>-<source-slug>/` contem os 4 pares .md+.yaml (mental-model, analysis, patterns, classification)
- [ ] `docs/system-of-record.md` contem secao "Artifacts Created" listando os outputs da Phase 4 (substitui o antigo integration-roadmap.md)
- [ ] `docs/canonical/` contem docs para padroes Missing e P1
- [ ] `.opencode/skills/` contem skills para padroes Missing
- [ ] `curriculum/` contem exercises para padroes Missing
- [ ] `docs/system-of-record.md` reflete o novo estado com data atualizada
- [ ] `curriculum/INDEX.md` lista os novos exercicios (se houver)
- [ ] Se Phase 6 executada: apenas `curriculum/` foi modificado; `docs/canonical/` intocado
- [ ] `git status` mostra apenas arquivos relacionados a essa sessao
- [ ] Commit Gate: usuario foi perguntado antes de commitar e antes de dar push
- [ ] Commits seguem o estilo `type(scope): short description`
- [ ] Toda delegacao usou `task()` com categoria adequada — nenhuma fase foi executada inline pelo orquestrador
- [ ] Se `incremental=true`: `delta-report.md` existe e o modelo anterior foi carregado com sucesso (ou fallback documentado)
- [ ] Mental model versionado em `mapa-mental-repo/<date>-<source-slug>-mental-model.{md,yaml}`
- [ ] `mapa-mental-repo/` tem no maximo 5 modelos ativos na raiz; excedentes estao em `archive/`
- [ ] Se `incremental=true`, o `mental-model.yaml` tem campo `meta.based_on` apontando para o modelo anterior

---

## Reference Implementations

O workflow completo foi executado em duas sessoes no repositorio `long-running-agents`:

### Sessao 1: 12-Factor Agents (2026-06-09)

**Fonte:** `Raw-Knowledge/sources/2026-06-09-12-factor-agents.md` (Dex Horthy talk) — single source

**Artefatos gerados:**

| Fase | Arquivos |
|---|---|
| Mental Model | `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-mental-model.md` + `.yaml` |
| Knowledge Extraction | `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis.md` + `.yaml` |
| Pattern Extraction | `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-patterns.md` + `.yaml` |
| Classification | `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md` + `.yaml` |
| Improvements | `docs/canonical/{error-context-hygiene,deterministic-tool-dispatch,owned-agent-control-loop,serializable-pause-resume-state}.md` |
| | `.opencode/skills/error-context-hygiene/SKILL.md` |
| | `curriculum/.../exercise-04-error-context-hygiene.md` |
| | `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-integration-roadmap.md` |
| Integration | `docs/system-of-record.md`, `curriculum/INDEX.md`, `curriculum/README.md` |

**Resultado da classificacao:** 3 Already Exists, 4 Partial Coverage, 1 Missing (Error Context Hygiene)

> **Nota sobre Phase 6:** Na sessao 1, a Phase 6 ainda nao existia. Com a skill v3.0, o padrao Missing (Error Context Hygiene) tambem receberia integracao profunda — subsecao em `01-context-management.md`, item no `03-harness-design-checklist.md`, e gate no `06-harness-evolution-playbook.md`.

### Sessao 2: Context Management in Agents (2026-06-10)

**Fonte:** Multi-source aggregation de 4 arquivos do `Raw-Knowledge`:
- `sources/2026-06-09-how-we-solved-context-management-in-agents.md` (video transcript)
- `concepts/smart-truncation.md` (concept page)
- `concepts/long-session-evals.md` (concept page)
- `entities/alex.md` (entity page)

**Artefatos gerados:**

| Fase | Arquivos |
|---|---|
| Mental Model | `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-mental-model.md` + `.yaml` |
| Knowledge Extraction | `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md` + `.yaml` |
| Pattern Extraction | `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-patterns.md` + `.yaml` |
| Classification | `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md` + `.yaml` |
| Improvements | `docs/canonical/{head-tail-context-truncation,addressable-memory-catalog,n-plus-one-long-session-evals,stable-harness-prompt,late-failure-regression-suite}.md` |
| | `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-integration-roadmap.md` |
| Integration | `docs/system-of-record.md` |
| Phase 6 (Curriculum) | 8 arquivos em `curriculum/` modificados (+218 linhas): checklist, core concepts, exercicio windowing, server-side compaction, harness improvements, evolution playbook, rubric template |

**Resultado da classificacao:** 1 Already Exists, 5 Partial Coverage, 1 Better Implementation, 0 Missing

---

*Skill version: 3.2 | Reference sessions: 2026-06-09, 2026-06-10, 2026-06-11*
