---
name: doc-to-canonical
description: "Pipeline simplificado: documento fonte → extração de conhecimento → padrões reutilizáveis → classificação contra repositório → canonical docs. Focado em gerar docs canônicos a partir de um único documento (currículo, análise, transcript). NÃO gera skills, exercícios ou integração profunda de currículo — apenas canonical docs + atualização de tags/aliases + system-of-record. Dispara com: 'canonicalize this document', 'extract canonical from', 'doc to canonical', 'create canonical docs from', 'documento para canonical', 'extrair canônicos de'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: analysis
  priority: high
---

## Harness Modules

Este skill utiliza módulos compartilhados no diretório `harness/`:

- **`harness/cache_bridge.py`**: bridge para o CacheStore do `analyze-and-improve`. Reutiliza cache de fases com SHA-256 source hash keying. Use `from harness.cache_bridge import compute_source_hash, CacheStore` para verificar cache antes de re-executar extração de conhecimento.
- **`harness/refine.py`**: `CanonicalEntry` + `CanonicalRefinementSession` para refinement pós-geração de canonical docs. Preserva `grounding_prompt` imutável com `refinement_history` acumulativo. Use `from harness.refine import save_session, load_session`.

Cache: `~/.kc_analyze_cache/` (chmod 700). Refinement: `refine_session.json` no output_dir.

## Invocation

This skill REQUIRES one mandatory parameter and accepts two optional parameters:

| Parameter | Required | Description |
|---|---|---|
| `source` | **Yes** | Absolute path to the document to analyze. Single file only (unlike `analyze-and-improve`, this skill does NOT aggregate multiple sources). Ex: `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md` |
| `date` | No | Date for output dir. Defaults to today (`YYYY-MM-DD`). Ex: `2026-06-10` |
| `source-slug` | No | Short slug for output dir. Derived from source filename if omitted. Ex: `agent-focus-problems` |

Example invocation:

```
Load doc-to-canonical with source=curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md, date=2026-06-10, source-slug=agent-focus-problems
```

## What I Do

Eu transformo um documento fonte em canonical docs no repositório. O pipeline tem 5 fases, todas delegadas a sub-agentes especializados:

0. *(skip)* — Sem modelo mental. O repo já é conhecido pelo orquestrador.
1. **Knowledge Extraction** — Extrair conhecimento não-óbvio do documento fonte (delegado: `deep`)
2. **Pattern Extraction** — Identificar padrões reutilizáveis (delegado: `ultrabrain`)
3. **Classification** — Classificar cada padrão contra os canônicos existentes (delegado: `deep`)
4. **Canonical Generation** — Criar `docs/canonical/<slug>.md` para padrões Missing e P1 (delegado: `deep` em paralelo)
5. **Integration** — Atualizar tags e aliases do documento fonte + system-of-record (delegado: `quick`)

Diferente de `analyze-and-improve`, esta skill:
- **NÃO** agrega múltiplos sources (single document only)
- **NÃO** executa Phase 0 (mental model do repo)
- **NÃO** gera skills, exercises, ou exemplos (apenas canonical docs)
- **NÃO** executa Phase 6 (curriculum deep integration)
- **SIM** atualiza tags e aliases do documento fonte analisado (Fase 5a e 5b)

## When to Use Me

Load this skill when:

- Você tem um documento do repositório (currículo, análise, transcript) que ensina ou descreve padrões que ainda não têm canonical doc próprio
- Você quer extrair padrões reutilizáveis e formalizá-los como documentação canônica nível 2
- Você quer que o documento fonte ganhe tags rastreáveis e aliases de busca automaticamente
- Você quer um pipeline mais leve que `analyze-and-improve` (sem skills, sem exercises, sem curriculum integration)

Não use quando:

- A fonte é externa e você precisa do modelo mental completo do repo → use `analyze-and-improve`
- Você precisa gerar skills de implementação ou exercícios de currículo → use `analyze-and-improve`
- Você precisa de integração profunda no currículo existente → use `analyze-and-improve` + Phase 6
- O escopo é uma única mudança trivial de tag ou alias
- Você não tem `docs/system-of-record.md` para resolver precedência

## Pre-requisites

Antes de começar, verifique:

- [ ] O parâmetro `source` foi fornecido e o documento fonte existe (path absoluto)
- [ ] Os parâmetros `date` e `source-slug` foram resolvidos (derivados se não fornecidos)
- [ ] O diretório de output `docs/analysis/<date>-<source-slug>/` foi criado
- [ ] O repositório tem `docs/system-of-record.md` para resolver precedência
- [ ] O repositório tem `docs/canonical/` com pelo menos alguns docs existentes para classificação
- [ ] Você leu `AGENTS.md` do repositório alvo para conhecer regras de commit, estilo, e gates

## Target Repository Context

TODA delegação via `task()` nas Phases 1-5 DEVE incluir este bloco no prompt:

```
TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md
  branch: main
```

Isso garante que todo sub-agente sabe:
- Onde escrever arquivos de output (caminho completo)
- Qual repositório será commitado (para mensagens de commit e referências)
- Onde encontrar as regras de precedência (`system-of-record.md`)
- Qual branch usar

## Output Directory Structure

TODOS os outputs das fases 1-3 vão para o mesmo diretório:

```
docs/analysis/<date>-<source-slug>/
  analysis.md            # Phase 1
  analysis.yaml
  patterns.md            # Phase 2
  patterns.yaml
  classification.md      # Phase 3
  classification.yaml
```

Artefatos concretos (canonical docs) gerados na Phase 4 vão para `docs/canonical/`.

---

## Phase 1: Knowledge Extraction

**Objetivo:** Extrair conhecimento não-óbvio do documento fonte. Filtrar ruído. Produzir análise estruturada.

### Regras de extração

| Manter | Ignorar |
|---|---|
| Frameworks, arquiteturas, workflows | Marketing, auto-promoção |
| Detalhes de implementação | Anedotas, histórias pessoais |
| Lições operacionais, falhas, tradeoffs | Repetição, padding, filler |
| Decisões de design com justificativa | Conselhos genéricos sem mecânica |
| Anti-padrões documentados | "É importante fazer X" sem o como |

### Delegação

Delegue para `deep`:

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=false,
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
- docs/analysis/<date>-<source-slug>/analysis.md — structured markdown with sections for:
  1. Frameworks & Models — conceptual structures presented
  2. Patterns & Architectures — reusable designs with mechanics
  3. Operational Lessons — what worked, what failed, what surprised
  4. Tradeoffs — explicit cost/benefit discussions
  5. Failure Patterns — what breaks and why
  6. Synthesis — cross-cutting insights the author may not have named
- docs/analysis/<date>-<source-slug>/analysis.yaml — typed mirror with the same structure

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
docs/analysis/<date>-<source-slug>/analysis.md
docs/analysis/<date>-<source-slug>/analysis.yaml
```

### Gate

- [ ] Os arquivos analysis.md e analysis.yaml existem no diretório de output
- [ ] Não contém marketing, anedotas, ou filler
- [ ] O YAML espelha o markdown com campos tipados

---

## Phase 2: Pattern Extraction

**Objetivo:** Identificar padrões reutilizáveis a partir do conhecimento extraído. Delegar para sub-agente `ultrabrain`.

### Regras de extração de padrões

Cada padrão deve ter 6 campos obrigatórios:

| Campo | Descrição |
|---|---|
| **name** | Nome descritivo (ex: "External State Persistence") |
| **problem solved** | Qual problema resolve, em uma frase |
| **inputs** | O que o padrão consome (dados, estado, contexto) |
| **outputs** | O que o padrão produz (decisões, artefatos, ações) |
| **benefits** | O que melhora em relação a não usar o padrão |
| **limitations** | Quando o padrão não funciona ou tem custo alto |

### Delegação

Delegue para `ultrabrain`:

```typescript
task(
  category="ultrabrain",
  load_skills=[],
  run_in_background=false,
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
- docs/analysis/<date>-<source-slug>/patterns.md
- docs/analysis/<date>-<source-slug>/patterns.yaml

KNOWLEDGE EXTRACTION:
<paste the analysis.md from Phase 1>"
)
```

### Output

```
docs/analysis/<date>-<source-slug>/patterns.md
docs/analysis/<date>-<source-slug>/patterns.yaml
```

### Gate

- [ ] Cada padrão tem os 6 campos obrigatórios preenchidos
- [ ] O YAML adiciona `components` e `flow` por padrão

---

## Phase 3: Classification

**Objetivo:** Comparar cada padrão contra o que já existe em `docs/canonical/`. Classificar em 4 categorias com evidência.

### Regras de classificação

| Classe | Significado | Quando usar |
|---|---|---|
| **Already Exists** | Padrão tem canonical doc com profundidade equivalente | Canonical doc cobre nome, mecanismo, tradeoffs |
| **Partial Coverage** | Peças existem em múltiplos canônicos mas falta o doc unificado | Mecanismos estão lá, mas não como padrão nomeado |
| **Missing** | Nenhum canonical doc cobre o padrão | Gap total — nem peça nem nome |
| **Better Implementation** | Repo tem versão superior ou mais madura | Repo vai além do que o padrão descreve |

### Evidência obrigatória

Para cada classificação, forneça:

- **Already Exists**: cite o canonical doc, linha ou seção que comprova (ex: `docs/canonical/error-context-hygiene.md:20-40`)
- **Partial Coverage**: liste cada canonical doc que cobre uma peça E o que falta para unificação
- **Missing**: confirme `NOT_FOUND` após buscar em todos os canônicos e no `system-of-record.md`
- **Better Implementation**: explique por que a versão do repo é superior

### Delegação

Delegue para `deep`:

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=false,
  prompt="TASK: Classify each extracted pattern against the target repository's canonical docs using evidence-based classification.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

CLASSIFICATION RULES:
- Already Exists: canonical doc covers the pattern with equivalent depth (name, mechanism, tradeoffs)
- Partial Coverage: pieces exist across multiple canonical docs but no unified doc
- Missing: no canonical doc covers the pattern at all (NOT_FOUND)
- Better Implementation: repo has a superior version

EVIDENCE REQUIREMENTS:
For every classification, cite file:line references from docs/canonical/.
For 'Missing', confirm NOT_FOUND after reading ALL canonical docs and system-of-record.md.

First, read docs/system-of-record.md to get the list of all existing canonical docs.
Then read each canonical doc that might relate to the pattern.

PATTERNS TO CLASSIFY:
<paste the patterns.md or patterns.yaml from Phase 2>

OUTPUT: Write TWO files in <output_dir>:
- docs/analysis/<date>-<source-slug>/classification.md — one section per pattern with:
  - Classification + justification
  - Evidence (file:line references to canonical docs or NOT_FOUND)
  - Integration value (Low/Medium/High)
  - Summary table at the end
- docs/analysis/<date>-<source-slug>/classification.yaml — typed mirror

Summary table format:
| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | ... | Partial Coverage | High |
| 2 | ... | Missing | High |
| ... | ... | ... | ... |"
)
```

### Output

```
docs/analysis/<date>-<source-slug>/classification.md
docs/analysis/<date>-<source-slug>/classification.yaml
```

### Gate

- [ ] Cada padrão classificado com evidência file:line ou `NOT_FOUND`
- [ ] Tabela-sumário no final do markdown
- [ ] Todos os canônicos existentes foram consultados (via `system-of-record.md`)

---

## Phase 4: Canonical Generation

**Objetivo:** Criar `docs/canonical/<slug>.md` para padrões classificados como Missing ou Partial Coverage com valor High.

### Priorização

| Classification | Integration Value | Ação |
|---|---|---|
| **Missing** | Any | Criar canonical doc (P0) |
| **Partial Coverage** | High | Criar canonical doc com reframe unificado (P1) |
| **Partial Coverage** | Medium | Apenas cross-reference. Não criar canonical doc. |
| **Already Exists** | Any | Apenas cross-reference. Não duplicar. |
| **Better Implementation** | Any | Documentar superioridade. Não duplicar. |

### Formato do canonical doc

Cada canonical doc DEVE seguir esta estrutura exata (observada em `error-context-hygiene.md`, `head-tail-context-truncation.md`, e outros):

```markdown
---
title: "<Pattern Name in Title Case>"
type: canonical
aliases: ["<alias1>", "<alias2>"]
tags: ["<dominio>", "<subdominio>"]
last_updated: <date>
relates-to: ["[[docs/canonical/<related-slug>|Related Doc]]", "[[<source-doc-path>|Source Document]]"]
sources: ["[[docs/analysis/<date>-<slug>/analysis|Knowledge Extraction]]"]
---

# <Pattern Name>

**Type:** Canonical Pattern
**Status:** Active
**Source:** <origin document path>
**Classification:** <Missing | Partial Coverage>
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

<1-3 paragraphs describing what breaks without this pattern.
Use concrete scenarios. Mention the root cause, not just symptoms.>

## Solution

<Core mechanism described in prose + ASCII diagram showing flow.
Include a table of core rules or components if applicable.
Include before/after examples if the pattern transforms something.>

## Implementation in this repo

### What already exists

<Bullet list of file:line references to existing coverage in canonical docs,
curriculum, or code. Be specific — every claim needs a citation.>

### What is missing

<Numbered list of mechanics, formalizations, or integrations that
the existing coverage does not provide. This is the gap the canonical doc fills.>

## Tradeoffs

| Benefit | Cost |
|---|---|

## Relationship to Other Patterns

- **Depends on:** <canonical docs this pattern needs as prerequisite>
- **Validated by:** <canonical docs that test or prove this pattern>
- **Complements:** <canonical docs that work alongside this pattern>

## References

<Bullet list of file:line citations to analysis, curriculum, and canonical docs>
```

### Delegação (paralela)

Para cada padrão que requer canonical doc (Missing ou P1), dispare um agente `deep` em paralelo:

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=true,  // paralelo com outros canonical docs
  prompt="TASK: Create ONE canonical doc for the pattern below.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

PATTERN TO CANONICALIZE:
Name: <pattern-name>
Problem: <problem-solved>
Classification: <Missing | Partial Coverage>
Evidence from Phase 3: <summary of classification evidence>

Read the source analysis at docs/analysis/<date>-<source-slug>/analysis.md
for deep context on this pattern. Also read the original source document
at <source-path> to capture the author's framing.

THE CANONICAL DOC MUST follow the exact format below:

---
title: '<Pattern Name>'
type: canonical
aliases: [<2-4 search aliases in Portuguese>]
tags: [<1-3 domain tags from system-of-record>]
last_updated: <date>
relates-to: [<wikilinks to related canonical docs and the source document>]
sources: ['[[docs/analysis/<date>-<source-slug>/analysis|Knowledge Extraction]]']
---

# <Pattern Name>

**Type:** Canonical Pattern
**Status:** Active
**Source:** <source document path>
**Classification:** <Missing | Partial Coverage>
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem
<Concrete scenario showing what breaks. Root cause, not just symptoms.>

## Solution
<Mechanism description + ASCII diagram + core rules table + before/after>

## Implementation in this repo
### What already exists
<file:line citations to existing coverage>

### What is missing
<Numbered list of gaps this doc fills>

## Tradeoffs
| Benefit | Cost |
|---|---|

## Relationship to Other Patterns
- **Depends on:** ...
- **Validated by:** ...
- **Complements:** ...

## References
<file:line citations>

Write the file to: docs/canonical/<kebab-case-slug>.md

MUST DO:
- Use the exact format above
- Cite file:line for every claim about repo contents
- Include an ASCII diagram in the Solution section
- Include a tradeoffs table
- Use [[wikilinks]] for all cross-references
- Tags must match domains from docs/system-of-record.md

MUST NOT:
- Invent citations — every file:line must be verified
- Skip the What is missing section
- Use raw markdown links instead of [[wikilinks]]
- Create the file anywhere other than docs/canonical/<slug>.md"
)
```

Os agentes rodam em paralelo (`run_in_background=true`). O orquestrador aguarda todos completarem antes de prosseguir para a Fase 5.

### Ordem de criação

Canonical docs são criados primeiro (nível 2 de precedência no `system-of-record.md`). Eles estabelecem a verdade antes que outros artefatos os referenciem.

### Gate

- [ ] Missing patterns têm canonical doc
- [ ] P1 (Partial Coverage + High value) têm canonical doc
- [ ] Cada canonical doc segue o formato exato (Problem, Solution, Implementation, Tradeoffs, Relationships, References)
- [ ] Cada canonical doc tem [[wikilinks]] no `relates-to` e `sources`
- [ ] Cada canonical doc tem tags que correspondem a domínios do `system-of-record.md`
- [ ] Nenhum canonical doc foi criado para Already Exists ou Better Implementation
- [ ] Nenhum canonical doc foi criado para Partial Coverage + Medium value

---

## Phase 5: Integration

**Objetivo:** Três ações em sequência: (5a) atualizar tags do documento fonte, (5b) revisar aliases do documento fonte, (5c) atualizar `system-of-record.md`.

### 5a — Tag Update

**Regra:** Para cada canonical doc criado na Fase 4, adicionar 2 tags ao documento fonte analisado:
- Nome do padrão em inglês (lowercase, hyphens)
- Nome do padrão em português (lowercase, hyphens)

```
Padrão: External State Persistence
  → tag EN: external-state-persistence
  → tag PT: persistencia-de-estado-externo

Padrão: Plan-Execute-Verify
  → tag EN: plan-execute-verify
  → tag PT: planejar-executar-verificar

Padrão: Constraint-Anchored Evaluation
  → tag EN: constraint-anchored-evaluation
  → tag PT: avaliacao-ancorada-em-constraints
```

O agente lê `classification.md` para identificar quais padrões geraram canonical doc, converte os nomes para slug, e usa `edit` para inserir as tags no array `tags:` do frontmatter do documento fonte.

### 5b — Aliases Review

**Regra:** O `aliases:` do documento fonte deve conter termos de busca alternativos para os padrões que ele ensina. O agente:

1. Lê o documento fonte e extrai os conceitos centrais que ele introduz
2. Para cada padrão da Fase 2 que está sendo ensinado no documento, verifica se existe um alias correspondente
3. Se o alias não existe, adiciona (em português, idioma do documento)
4. Mantém aliases existentes

Critério para inclusão: um termo é candidato a alias se um leitor pudesse usá-lo para encontrar o documento via busca no Obsidian. Não é uma lista exaustiva — são os 3-8 termos de busca mais prováveis para os conceitos e padrões centrais.

### 5c — System of Record Update

Atualiza `docs/system-of-record.md`:
- Adiciona os novos canonical docs à tabela "Padrões canônicos ativos"
- Remove da seção "Documentos esperados quando o domínio correspondente amadurecer" se aplicável
- Atualiza `last_updated` no frontmatter

### Delegação

Delegue para `quick`:

```typescript
task(
  category="quick",
  load_skills=["git-master"],
  run_in_background=false,
  prompt="TASK: Execute Phase 5 integration — update tags, aliases, and system-of-record.

TARGET_REPOSITORY:
  path: <absolute-path-to-repo>
  name: <repo-name>
  output_dir: docs/analysis/<date>-<source-slug>/
  system_of_record: docs/system-of-record.md

SOURCE DOCUMENT: <absolute-path-to-source-document>

Read docs/analysis/<date>-<source-slug>/classification.md to identify
which patterns received canonical docs in Phase 4 (Missing and P1).
Read docs/analysis/<date>-<source-slug>/patterns.md to get pattern names.

STEP 5a — TAG UPDATE on SOURCE DOCUMENT:
For each pattern that received a canonical doc:
1. Convert the pattern name to English slug: lowercase, hyphens (e.g., External State Persistence → external-state-persistence)
2. Convert the pattern name to Portuguese slug: lowercase, hyphens (e.g., External State Persistence → persistencia-de-estado-externo)
3. Use 'edit' to add both tags to the 'tags:' array in the source document's YAML frontmatter
4. Do NOT duplicate tags that already exist

STEP 5b — ALIASES REVIEW on SOURCE DOCUMENT:
1. Read the source document and extract central concepts + patterns it teaches
2. Compare against existing 'aliases:' in the frontmatter
3. Add missing aliases in Portuguese (the document's language) — terms a reader would use to find this document via Obsidian search
4. Keep existing aliases intact
5. Do NOT add more than 8 aliases total (incl. existing)

STEP 5c — SYSTEM OF RECORD UPDATE:
1. Update docs/system-of-record.md:
   - Add each new canonical doc to the 'Padrões canônicos ativos' table with file name and description
   - If any new canonical doc was listed in 'Documentos esperados quando o domínio correspondente amadurecer', remove it from that section
   - Update 'last_updated' in the frontmatter to today's date
2. Verify no duplicate entries

After all edits, run: git diff --stat to confirm scope.
Only these files should be modified:
- <source-document-path> (tags + aliases)
- docs/system-of-record.md (canonical table)
- docs/canonical/<new-files>.md (already created in Phase 4)

Do NOT commit. The orchestrator handles the commit decision."
)
```

### Gate

- [ ] Documento fonte: `tags:` inclui todos os padrões que geraram canonical doc (EN + PT)
- [ ] Documento fonte: `aliases:` cobre os conceitos centrais e padrões ensinados (3-8 termos)
- [ ] `docs/system-of-record.md`: tabela de canônicos ativos inclui os novos docs
- [ ] `docs/system-of-record.md`: `last_updated` reflete a data da sessão
- [ ] Nenhum canonical doc ficou listado como "pendente" se foi criado
- [ ] `git diff --stat` mostra apenas: documento fonte + `system-of-record.md` + `docs/canonical/<novos>.md`

---

## Anti-Patterns

- **Executar fases diretamente em vez de delegar.** Toda fase deve ser uma sub-task via `task()` com categoria adequada — o orquestrador supervisiona, não executa.
- **Pular a classificação** e gerar canonical docs sem evidência do que já existe. Isso produz duplicação.
- **Criar canonical doc para Already Exists.** Só cross-reference.
- **Criar canonical doc para Partial Coverage + Medium.** Só cross-reference. Reserve canonical docs para P0 e P1.
- **Delegar extração de padrões para `quick`.** Precisa de `ultrabrain` — é trabalho de síntese.
- **Esquecer o YAML mirror.** Toda análise e classificação deve ter .md + .yaml. O YAML permite consumo programático futuro.
- **Esquecer a Fase 5a (tag update).** Sem isso, o documento fonte não referencia os canônicos que gerou.
- **Esquecer a Fase 5b (aliases review).** Sem aliases, o documento é difícil de encontrar via busca.
- **Usar `write` em vez de `edit` na Fase 5.** As edições são cirúrgicas — adicionar tags/aliases, não reescrever o arquivo.
- **Ignorar `system-of-record.md`.** A precedência importa — não classifique como Missing sem verificar todos os canônicos.
- **Criar canonical doc sem `relates-to`.** Documento fica ilhado no Obsidian Graph.
- **Criar canonical doc sem [[wikilinks]].** Raw markdown links quebram a convenção do repositório.
- **Invocar a skill sem fornecer o parâmetro `source`.** A skill não tem como adivinhar qual documento analisar.
- **Committar ou dar push sem perguntar ao usuário.** O Commit Gate exige confirmação explícita. O `AGENTS.md` do repo alvo tem a palavra final.

---

## Verification Gates

Depois de completar as 5 fases:

- [ ] O parâmetro `source` foi fornecido e validado antes de qualquer execução
- [ ] `docs/analysis/<date>-<source-slug>/` contém os 3 pares .md+.yaml (analysis, patterns, classification)
- [ ] `docs/canonical/` contém docs para padrões Missing e P1
- [ ] Nenhum canonical doc foi criado para Already Exists, Better Implementation, ou Partial Coverage + Medium
- [ ] Documento fonte: `tags:` atualizadas com nomes dos padrões (EN + PT)
- [ ] Documento fonte: `aliases:` revisados com termos de busca dos conceitos centrais
- [ ] `docs/system-of-record.md` reflete o novo estado com data atualizada
- [ ] Todos os canonical docs têm `relates-to:` preenchido com [[wikilinks]]
- [ ] Todos os canonical docs têm `sources:` apontando para a análise
- [ ] `git status` mostra apenas arquivos relacionados a essa sessão
- [ ] Toda delegação usou `task()` com categoria adequada — nenhuma fase foi executada inline pelo orquestrador
- [ ] Commit Gate: usuário foi perguntado antes de commitar e antes de dar push

---

## Reference: relação com `analyze-and-improve`

| Aspecto | `analyze-and-improve` | `doc-to-canonical` |
|---|---|---|
| Fontes | Single ou múltiplas (agregação) | Single document only |
| Phase 0 (Mental Model) | Sim | Não (repo conhecido) |
| Phase 1-3 (Extract, Patterns, Classify) | Sim | Sim (idêntico) |
| Phase 4 (Generate) | Skills + Exercises + Canonical Docs + Roadmap | Apenas Canonical Docs |
| Phase 5 (Integration) | SOR update + INDEX/README/MASTER_PLAN | SOR + Tags + Aliases |
| Phase 6 (Curriculum) | Sim (opcional) | Não |
| Output principal | Ecossistema completo de artefatos | Foco em documentação canônica |

Use `doc-to-canonical` quando o objetivo é **formalizar padrões já ensinados** em documentos do repo. Use `analyze-and-improve` quando a fonte é **externa** e você quer o pipeline completo com skills e exercícios.

---

*Skill version: 1.0 | Derived from: analyze-and-improve v3.0*
