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

## What I Do

Eu transformo conhecimento externo em melhorias concretas no repositorio. O pipeline tem 5 fases:

1. **Knowledge Extraction** — Extrair conhecimento nao-obvio de um documento fonte
2. **Pattern Extraction** — Identificar padroes reutilizaveis (via sub-agente ultrabrain)
3. **Classification** — Classificar cada padrao contra o repositorio alvo
4. **Improvement Generation** — Gerar artefatos em 7 categorias, priorizados por impacto
5. **Integration** — Atualizar system-of-record, indices, e commitar

## When to Use Me

Load this skill when:

- Voce tem uma fonte externa de conhecimento (transcript de talk, paper academico, knowledge base entry, documentacao de biblioteca) e quer extrair padroes aplicaveis ao seu repositorio
- Voce quer classificar padroes extraidos contra o que ja existe no codigo/curriculo
- Voce quer gerar um roadmap de melhorias priorizadas por impacto
- Voce quer seguir o mesmo workflow que produziu `docs/analysis/2026-06-09-*` no repositorio `long-running-agents`

Nao use quando:

- A fonte ja esta analisada e voce so precisa implementar uma melhoria especifica
- O escopo e uma unica mudanca trivial
- Voce nao tem um repositorio alvo para classificar os padroes

## Pre-requisitos

Antes de comecar, verifique:

- [ ] O documento fonte existe e esta acessivel (path absoluto ou URL)
- [ ] O repositorio alvo tem `docs/system-of-record.md` (ou equivalente) para resolver precedencia
- [ ] Voce leu `AGENTS.md` do repositorio alvo para conhecer regras de commit, estilo, e gates

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

### Prompt de extracao

Use este prompt com o documento fonte:

```
TASK: Extract all non-obvious knowledge from the document below.
IGNORE: marketing, anecdotes, personal stories, repetition.
KEEP: frameworks, patterns, architectures, workflows, implementation
details, operational lessons, failures, tradeoffs.
OUTPUT: structured markdown with sections for:
1. Frameworks & Models — conceptual structures presented
2. Patterns & Architectures — reusable designs with mechanics
3. Operational Lessons — what worked, what failed, what surprised
4. Tradeoffs — explicit cost/benefit discussions
5. Failure Patterns — what breaks and why
6. Synthesis — cross-cutting insights the author may not have named

After the markdown analysis, produce a YAML mirror with the same structure
using typed fields (frameworks as list of objects with name+components,
patterns with name+problem+mechanism, etc.).
```

### Output

Dois arquivos em `docs/analysis/`:

```
docs/analysis/<date>-<source-slug>-analysis.md
docs/analysis/<date>-<source-slug>-analysis.yaml
```

O YAML deve espelhar o markdown com campos tipados:

```yaml
meta:
  title: "..."
  date: "YYYY-MM-DD"
  source: "..."
frameworks:
  - name: "..."
    components: [...]
patterns:
  - name: "..."
    problem: "..."
    mechanism: "..."
operational_lessons:
  - lesson: "..."
    context: "..."
tradeoffs:
  - decision: "..."
    benefit: "..."
    cost: "..."
failure_patterns:
  - pattern: "..."
    cause: "..."
    mitigation: "..."
synthesis: "..."
```

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

Delegue para `ultrabrain` — esse e um trabalho de sintese que exige raciocinio sobre a analise extraida:

```typescript
task(
  category="ultrabrain",
  load_skills=[],
  run_in_background=false,
  prompt="TASK: Identify reusable patterns from the knowledge extraction below.
           Only keep patterns applicable to agentic systems.

           For each pattern, provide: name, problem solved, inputs, outputs,
           benefits, limitations. Then produce a YAML mirror adding components
           (list of sub-elements) and flow (sequence of steps) per pattern.

           KNOWLEDGE EXTRACTION:
           <paste the markdown analysis from Phase 1>"
)
```

### Output

```
docs/analysis/<date>-agentic-patterns.md
docs/analysis/<date>-agentic-patterns.yaml
```

## Phase 3: Classification

**Objetivo:** Comparar cada padrao contra o que ja existe no repositorio alvo. Classificar em 4 categorias com evidencia.

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

### Output

```
docs/analysis/<date>-pattern-classification.md
docs/analysis/<date>-pattern-classification.yaml
```

O markdown deve ter uma tabela-sumario no final:

```
| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | ... | Already Exists | Low |
| 2 | ... | Partial Coverage | Medium |
| ... | ... | ... | ... |
```

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
5. **Atualizacao de indices** — system-of-record.md, INDEX.md, README.md.

### Conteudo de cada artefato

**Canonical doc** deve conter:
- Type, Status, Source, Classification, Precedence
- Problem (o que o padrao resolve)
- Solution (mecanismo detalhado)
- Implementation in this repo (o que ja existe, o que falta)
- Tradeoffs (tabela beneficio vs custo)
- Relationship to Other Patterns (dependencias e complementos)
- References (links para analises, codigo, curriculo)

**Skill** deve conter:
- Frontmatter com nome, descricao rica em triggers, metadata
- What I Do (contract)
- When to Use Me (triggers positivos e negativos)
- The Anti-Pattern (codigo errado)
- The Pattern (codigo correto)
- Implementation rules (classifier, summarizer, format rules)
- Integration with existing repo infrastructure
- Quality Gates (checklist de verificacao)
- References

**Exercise** deve seguir o formato do curriculo:
- Prologo narrativo (cenario realista que deu errado)
- Cenario com dados de entrada
- Requisitos funcionais e tecnicos
- Tarefa em partes (diagnostico → implementacao → pipeline)
- Codigo esqueleto em Python
- Criterios de aceitacao com asserts
- Rubric de avaliacao

## Phase 5: Integration

**Objetivo:** Atualizar documentos de indice que ficaram desatualizados.

### O que verificar

| Documento | O que atualizar |
|---|---|
| `docs/system-of-record.md` | Se canonical/ ou analysis/ ganharam arquivos, atualizar tabelas. Se tinha claim "vazio", corrigir. Atualizar data. |
| `curriculum/INDEX.md` | Se novos exercicios foram criados, adicionar a listagem. |
| `curriculum/README.md` | Se a arvore de diretorios mudou, atualizar diagrama. |
| `curriculum/MASTER_PLAN.md` | Se contagem de exercicios ou topicos mudou, atualizar. |

### Verificacao pos-integracao

```bash
git diff --stat  # Confirmar quais arquivos foram alterados
```

Commite seguindo o estilo do repo: `type(scope): short description`

## Anti-Patterns

- **Pular a classificacao** e gerar melhorias sem evidencia do que ja existe. Isso produz duplicacao.
- **Criar artefatos para Already Exists**. So cross-reference.
- **Delegar extracao de padroes para quick**. Precisa de ultrabrain — e trabalho de sintese.
- **Esquecer o YAML mirror**. Toda analise e classificacao deve ter .md + .yaml. O YAML permite consumo programatico futuro.
- **Ignorar system-of-record.md**. A precedencia importa — nao classifique como Missing sem verificar canonical/ e decisions/.
- **Criar exercises sem esqueleto de codigo**. O formato do curriculo exige codigo Python com dataclasses e asserts.
- **Atualizar system-of-record sem atualizar a data**. A data de ultima atualizacao no rodape e o unico sinal de frescor.

## Verification Gates

Depois de completar as 5 fases:

- [ ] `docs/analysis/` contem os 3 pares .md+.yaml (knowledge, patterns, classification)
- [ ] `docs/canonical/` contem docs para padroes Missing e P1
- [ ] `.opencode/skills/` contem skills para padroes Missing
- [ ] `curriculum/` contem exercises para padroes Missing
- [ ] `docs/system-of-record.md` reflete o novo estado
- [ ] `curriculum/INDEX.md` lista os novos exercicios
- [ ] `git status` mostra apenas arquivos relacionados a essa sessao
- [ ] Commits seguem o estilo `type(scope): short description`

## Reference Implementation

O workflow completo foi executado em 2026-06-09 no repositorio `long-running-agents`, produzindo:

**Fonte:** `Raw-Knowledge/sources/2026-06-09-12-factor-agents.md` (Dex Horthy talk)

**Artefatos gerados:**

| Fase | Arquivos |
|---|---|
| Knowledge Extraction | `docs/analysis/2026-06-09-12-factor-agents-analysis.md` + `.yaml` |
| Pattern Extraction | `docs/analysis/2026-06-09-agentic-patterns.md` + `.yaml` |
| Classification | `docs/analysis/2026-06-09-pattern-classification.md` + `.yaml` |
| Improvements | `docs/canonical/{error-context-hygiene,deterministic-tool-dispatch,owned-agent-control-loop,serializable-pause-resume-state}.md` |
| | `.opencode/skills/error-context-hygiene/SKILL.md` |
| | `curriculum/.../exercise-04-error-context-hygiene.md` |
| | `docs/analysis/2026-06-09-integration-roadmap.md` |
| Integration | `docs/system-of-record.md`, `curriculum/INDEX.md`, `curriculum/README.md` |

**Resultado da classificacao:** 3 Already Exists, 4 Partial Coverage, 1 Missing (Error Context Hygiene)

---

*Skill version: 1.0 | Reference session: 2026-06-09*
