---
title: "Plug-and-Play Eval Harness with BYO Evaluators"
type: canonical
aliases: ["byo evaluators", "harness compartilhado multi-produto", "plug-and-play harness"]
tags: ["evals", "harness-engineering", "harness"]
last_updated: 2026-08-31
relates-to: ["[[docs/canonical/generator-evaluator|Generator/Evaluator]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/cli-first-eval-harness-remote-persistence|CLI-First Eval Harness with Remote Persistence]]"]
sources: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]"]
---
# Plug-and-Play Eval Harness with BYO Evaluators

**Type:** canonical
**Status:** active
**Source:** Inside Clay's Eval Stack (LangChain) — `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage — Integration value: Medium (P2)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Todo novo agente ou produto reconstrói um harness de avaliação do zero: execução, gating, report, persistência, comparação. O custo é pago N vezes, a engenharia de eval vira plumbing em vez de avaliação, e cada produto inventa seu formato de resultado — impossibilitando comparação cross-produto e concentrando o conhecimento de "como se avalia" em ninguém.

O problema é o oposto do single-tenant: quando cada produto tem harness próprio, nenhuma melhoria no mecanismo de avaliação se propaga, e avaliar dois agentes lado a lado exige trabalho de integração ad hoc.

## Solution

Separar o harness (compartilhado) dos evaluators (autorais):

1. **Harness compartilhado** provê a plumbing uniforme: execução de casos, reporting, gates por fase, persistência de resultados, comparação. Uma implementação, todos os produtos.
2. **Suite de eval é do produto** — cada produto traz seus casos, seus datasets e seus thresholds.
3. **Evaluators são BYO** ("bring your own"): o produto autora seus próprios LLM judges e checks; o harness os invoca num contrato padrão (input: run artifacts; output: scores estruturados), sem opinar sobre a semântica da avaliação.
4. **Onboarding path explícito** — um novo produto pluga suite + evaluators no harness existente e recebe infraestrutura de avaliação de graça; só os evaluators são autorados.
5. **Comparabilidade cross-produto** — storage, reporting e formato de resultado uniformes permitem comparar agentes e produtos no mesmo vocabulário.

A fronteira arquitetural é a mesma do [[docs/canonical/generator-evaluator|Generator/Evaluator]]: o harness não avalia; ele executa e registra. Quem avalia é o evaluator do produto.

## Implementation in this repo

### What already exists

O repo tem um harness compartilhado real que onboarding **fontes plugáveis**:

- O pipeline `analyze-and-improve` roda qualquer fonte externa pelas mesmas 7 fases com execução, evaluators, gates e persistência uniforme de artefatos — "Harness com cache, retry, model tiering, schemas, chunking, trajectory, eval, refinement (8 módulos, stdlib)" (`docs/system-of-record.md:46`).
- O parâmetro `source` aceita qualquer path/URL/array (`.opencode/skills/analyze-and-improve/SKILL.md:18`) — a fonte é a parte plugável do harness.
- Evaluator como gate por fase no harness compartilhado (`harness/GUIDE-analyze-and-improve.md:42,53`).
- Fundação de papéis: [[docs/canonical/generator-evaluator|Generator/Evaluator]] separa a autoria do evaluator como papel distinto (`docs/canonical/3-layer-evaluation-architecture.md:94`); [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] formaliza a separação estrutural (`:52-54`).
- Harness de teste uniforme no escopo skills: `skill-testing-conventions` (`docs/system-of-record.md:152`).

### What is missing

O contrato específico do padrão: **onboarding multi-produto com evaluators autoriais**.

1. O harness do repo pluga *fontes de conhecimento*, não *agentes/produtos com suites e evaluators próprios* — não existe doc de contrato de onboarding de novos produtos de agente.
2. Não existe noção de BYO LLM judges num contrato padrão de evaluator (interface, formato de score, registro).
3. Não existe comparabilidade cross-produto de resultados. NOT_FOUND: nenhum doc descreve onboarding multi-produto com evaluators autoriais; [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] trata de ciclo de vida do harness, não de contrato plug-and-play.

Add:

1. Contrato de evaluator (input artifacts → scores estruturados) que qualquer skill/produto implementa.
2. Registro de suites por produto no harness, com formato de resultado uniforme.
3. Guia de onboarding: "novo produto de agente" → declara suite + evaluators → herda execução, gates e persistência.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Novos agentes recebem infraestrutura de avaliação de graça; só evaluators são autorados | O harness compartilhado vira artefato crossroad: mudanças afetam todos os produtos |
| Engenharia de eval foca em judges e checks, não em plumbing | Qualidade do evaluator continua sendo ônus de cada produto |
| Comparabilidade cross-produto de resultados | Premissas do harness podem não caber em produtos com execução exótica |
| Melhorias no harness propagam para todos os produtos de uma vez | Governança do harness precisa de owner e política de versão |

## Relationship to Other Patterns

- **Builds on:** [[docs/canonical/generator-evaluator|Generator/Evaluator]] e [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] — a separação gerador/avaliador é o que torna o evaluator pluggável.
- **Uses:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — os BYO evaluators se encaixam nas camadas deterministic/semantic/behavioral.
- **Uses:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — contrato padrão para checks deterministicos trazidos pelo produto.
- **Composes with:** [[docs/canonical/cli-first-eval-harness-remote-persistence|CLI-First Eval Harness with Remote Persistence]] — o harness compartilhado é o consumidor natural do store remoto de resultados.
- **Constrains:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — o ciclo de vida do harness agora afeta múltiplos produtos e precisa de gates de evolução.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:101` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md` — §5, classificação Partial Coverage/Medium com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification-batch-1.md` — batch-fonte da classificação.
- `docs/system-of-record.md:46,152` — harness `analyze-and-improve` (8 módulos) e `skill-testing-conventions`.
- `.opencode/skills/analyze-and-improve/SKILL.md:18` — parâmetro `source` plugável.
- `harness/GUIDE-analyze-and-improve.md:42,53` — evaluator como gate por fase.
- `docs/canonical/3-layer-evaluation-architecture.md:94`; `docs/canonical/compartmented-evaluation-architecture.md:52-54` — fundação Generator/Evaluator.

---

*Created: 2026-08-31 | From: Clay Eval Stack classification | Precedence: canonical*
