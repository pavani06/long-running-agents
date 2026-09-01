---
title: "Shadow Builds on Separated Compute"
type: canonical
aliases: ["shadow builds", "serving vs development compute", "deploy shadow para artefatos de agente"]
tags: ["production", "agentes-orquestracao", "governanca"]
last_updated: 2026-08-31
relates-to: ["[[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]", "[[docs/canonical/evals-as-brakes|Evals as Brakes]]", "[[docs/canonical/manual-brake-question-gate|Manual-Brake Question Gate]]", "[[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]", "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]", "[[docs/canonical/skills-cli-native-agent-data-access|Skills and CLI as Native Agent Data Access]]"]
sources: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]"]
---
# Shadow Builds on Separated Compute

**Type:** canonical
**Status:** active
**Source:** Inside Clay's Eval Stack (LangChain; shadow target S3 na fonte, generalizado) — `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage — Integration value: Medium (P2)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Agentes que constroem novos data models não podem colocar o serving de produção em risco. A resposta tradicional é revisão humana post-hoc de cada build — que não escala com o volume de builds agent-driven e vira gargalo de autonomia. O dilema: ou o agente não constrói (autonomia zero), ou constrói perto de produção (risco inaceitável), ou cada build espera revisão humana (a autonomia morre no funil).

O problema é arquitetural, não processual: enquanto build e serving dividem o mesmo compute, a segurança depende de política (revisão, permissão) — e política é o que falha sob volume.

## Solution

**Segurança por construção, não por política** (cf. [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]]):

1. **Shadow deployment target** — um alvo de deploy separado (S3 na fonte) para artefatos construídos por agentes: data models novos nascem no shadow, nunca no serving.
2. **Separação arquitetural serving compute vs development compute** — dois planos distintos: o plano de serving atende produção; o plano de development roda builds e experimentos de agente. Experiências não podem derrubar produção *por construção* — não há path de execução do dev compute para o serving.
3. **Guardrails definidos up front, não revisão depois** — o que o agente pode construir, onde deploya e com que orçamento é fixado antes da execução; a autonomia de build é *concedida pelos guardrails*, não concedida e depois auditada.
4. **Promotion path shadow → serving** — o data model shadow é promovido a serving por critérios explícitos (gates de eval ou humanos), fechando o ciclo: construir livremente, promover deliberadamente.

## Implementation in this repo

### What already exists

Mecânicas adjacentes em profundidade:

- **Shadow deployment de comparação** (curriculum): clonar tráfego real, rodar o novo Planner em paralelo, executar contratos em sandbox, promover só quando melhor/igual em 98%+ dos casos (`curriculum/05-core-concepts/02-planning-execution-separation.md:2190-2199`) — shadow de *comparação de comportamento*, não shadow *build de artefato*.
- **Rollout gates staged** declarados Better Implementation pelo próprio repo: "staged shadow tests, regression batteries, N+1 gates, staged canary percentages, production metrics, trace sampling, rollback commands" (`docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:121-131`, via `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:783-790,2434-2444`).
- **Execução separada por construção:** `git worktree add` isolado por issue (`.opencode/skills/issue-start/SKILL.md:72,82`) — superfície de execução separada para trabalho de agente, no plano de código.
- [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] (`docs/system-of-record.md:247`) — agente shadow revisa em paralelo pré-merge; mecânica de shadow de *revisão*, distinta de shadow build.

### What is missing

O núcleo do padrão:

1. Nenhum **shadow deployment target para artefatos construídos por agentes** (data models, outputs de build). NOT_FOUND: grep `shadow build|shadow deploy|shadow deployment|separated compute|dev compute|serving compute` em `*.md` → apenas o pacote-fonte Clay e `02-planning-execution-separation.md:2190`; grep `Athena|\bS3\b` → nenhuma ocorrência de shadow target.
2. **Separação serving vs development compute** como planos arquiteturais não existe nomeada.
3. **"Guardrails defined up front rather than review afterwards" como porta de autonomia de build** — o repo tem gates de pós-construção (eval, review), não guardrails de pré-execução que concedem autonomia.

Add:

1. Um alvo de deploy shadow para artefatos de agente (isolado do path de serving).
2. Declaração dos dois planos de compute no desenho de infraestrutura (serving/development) com proibição estrutural de path entre eles.
3. Contrato de guardrails up front (escopo de build, alvo, budget) que substitui revisão post-hoc de cada artefato.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Experimentos não derrubam produção por construção, não por política | Custo de infraestrutura duplicada (explicitamente incomum para startups na fonte) |
| Guardrails antecipados substituem revisão humana post-hoc de builds de agente | Shadow e serving podem derivar, invalidando resultados shadow |
| Concede autonomia de build e deploy a agentes com segurança | Critérios de promotion ainda exigem gates humanos ou evals próprios |
| Promotion path explícito fecha o ciclo construir-livremente/promover-deliberadamente | Manutenção de paridade shadow/serving vira obrigação contínua |

## Relationship to Other Patterns

- **Instance of:** [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over Compliance]] — a separação de compute é a garantia estrutural; a revisão post-hoc é a compliance.
- **Composes with:** [[docs/canonical/evals-as-brakes|Evals as Brakes]] — o gate de promotion shadow→serving é um eval gate; autonomia de build é função da qualidade do gate de promoção.
- **Complements:** [[docs/canonical/manual-brake-question-gate|Manual-Brake Question Gate]] — guardrails up front respondem as perguntas do freio antes da execução, não durante.
- **Pairs with:** [[docs/canonical/skills-cli-native-agent-data-access|Skills and CLI as Native Agent Data Access]] — execuções goal-level de longa duração deployam naturalmente no shadow target.
- **Distinct from:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] (shadow de revisão pré-merge) e do shadow deployment de comparação do curriculum — mesmo prefixo, mecânica diferente (build de artefato vs revisão vs comparação).

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:206` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md` — §10, classificação Partial Coverage/Medium com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification-batch-2.md` — batch-fonte da classificação.
- `curriculum/05-core-concepts/02-planning-execution-separation.md:2190-2199` — receita de shadow deployment de comparação.
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:121-131` — Better Implementation de canary rollout gate.
- `.opencode/skills/issue-start/SKILL.md:72,82` — worktree isolado por issue.
- `docs/system-of-record.md:247` — shadow-review-pipeline (mecânica distinta).

---

*Created: 2026-08-31 | From: Clay Eval Stack classification | Precedence: canonical*
