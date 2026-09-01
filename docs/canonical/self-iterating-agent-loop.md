---
title: "Self-Iterating Agent Loop"
type: canonical
aliases: ["self-iterating loop", "agent self-improvement loop", "loop auto-iterante de agentes", "agents building better iterations of themselves", "unified foundation closed loop"]
tags: ["agentes-orquestracao", "evals", "data-platform", "production"]
last_updated: 2026-08-31
relates-to:
  - "[[docs/canonical/agent-first-data-foundation|Agent-First Data Foundation]]"
  - "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]"
  - "[[docs/canonical/shared-fleet-learning|Shared Fleet Learning]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]"
  - "[[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/canonical/unified-tool-surface-flywheel|Unified Tool Surface Flywheel]]"
  - "[[docs/canonical/production-to-offline-feedback-loop|Production-to-Offline Feedback Loop]]"
sources:
  - "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns (2026-08-31)]]"
---

# Self-Iterating Agent Loop

**Type:** Canonical Pattern
**Status:** Active
**Source:** Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipeline) — LangChain, via `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage (P1) — integration value High
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

A melhoria de agentes estagna quando os dados sobre os quais os agentes raciocinam estão espalhados por silos do produto em vez de alimentar um único loop fechado (`docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:331-349`).

Loops fechados que melhoram *artefatos externos ao agente* (harness, evals, docs) têm teto: o feedback acumulado existe, mas disperso; nenhum agente raciocina sobre o conjunto. O alvo declarado é autorreferente — agentes construindo *iterações melhores de si mesmos* a partir do feedback acumulado — e exige que todos os elos operem sobre o mesmo substrato de dados.

## Solution

Um loop fechado em que **todas as partes do produto alimentam uma fundação de dados unificada sobre a qual os agentes raciocinam** (`...-patterns.md:335-341`):

1. **Orquestração e execução** de agentes sobre a fundação unificada (dados first-party + third-party num plano só).
2. **Observação** dos resultados de execução de volta no mesmo plano.
3. **Canal de feedback** que retorna ao substrato — não a um doc, não a um eval set isolado, não a um repositório de tickets.
4. **Agentes raciocinando sobre o feedback acumulado para construir iterações melhores de si mesmos** — prompts, skills, tools e data models derivados do próprio histórico, não de especificação humana ex-nihilo.

Propriedades estruturais (`...-patterns.md:342-347`): generaliza o flywheel de tools para o produto inteiro; alvos de melhoria viram dados sobre os quais os próprios agentes agem; arquitetura e loop de eval compartilham o mesmo substrato. É uma arquitetura-alvo declarada, não uma receita pronta — e o elo mais fraco (observação, feedback ou dados) limita o loop inteiro. Auto-iteração não-gateada **amplifica** eval drift: cada iteração herda e agrava os vieses do feedback (`...-patterns.md:348-349`).

## Implementation in this repo

### What already exists

Todos os elos do loop existem como padrões canônicos independentes (`...-classification.md:290-307`):

- **Loop fechado agêntico** — [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] (`docs/canonical/closed-loop-agent-operating-system.md:28-37`): state intake, priority synthesis, execution routing, feedback writeback — "observe state, decide what should happen next, route execution, validate the outcome, and update the records that future agents will trust".
- **Aprendizado em frota** — [[docs/canonical/shared-fleet-learning|Shared Fleet Learning]] (`docs/canonical/shared-fleet-learning.md:37`): erro de um → comportamento de todos; com o elo fraco nomeado: o flywheel daemon "deploys nothing — it surfaces findings for human review" (`:62-63`).
- **Falha → caso durável** — [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (`docs/canonical/production-failure-regression-flywheel.md:28`): feedback como eval, não como dados de auto-melhoria.
- **Meta-loop de melhoria do harness** — [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] (`docs/system-of-record.md:229`): "Converts human observations into accumulating harness leverage" — melhora o harness, não o agente.
- **A tese organizacional** — `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:53`: "aim the recursive self-improvement loop at the organization" — o loop recursivo existe como tese, sem substrato de dados.
- **O gate de segurança** — [[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]] (`docs/system-of-record.md:294`): incorporação gateada por confiança — o que torna auto-iteração segura.

### What is missing

A composição-alvo (`...-classification.md:305`):

1. **O substrato único** — "all parts of the product are feeding into a single unified data foundation that agents can reason over" depende do gap da [[docs/canonical/agent-first-data-foundation|Agent-First Data Foundation]].
2. **A autorreferência** — agentes construindo "better iterations of themselves" a partir do feedback acumulado; os loops do repo melhoram artefatos externos (harness/evals/docs), nunca o agente via substrato de dados.
3. **O doc único unindo orchestration + execution + observation + feedback sobre o mesmo plano de dados** — os quatro elos existem, cada um com doc própria, sem composição.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Generaliza o flywheel de tools para o produto inteiro | Arquitetura-alvo declarada, não receita pronta — não há implementação de referência |
| Alvos de melhoria viram dados sobre os quais os próprios agentes agem | O elo mais fraco (observação, feedback ou dados) limita o loop inteiro |
| Arquitetura e loop de eval compartilham o mesmo substrato | Auto-iteração amplifica eval drift se o loop não for gateado |
| Compõe os loops canônicos existentes (OS, frota, flywheel, meta-loop) numa visão única | Depende da migração para fundação de dados unificada — o maior pré-requisito do repo |

## Relationship to Other Patterns

- **Depende de:** [[docs/canonical/agent-first-data-foundation|Agent-First Data Foundation]] — o substrato único é pré-requisito; sem ele, o loop fecha sobre silos.
- **Compõe:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] (elos de orquestração) + [[docs/canonical/shared-fleet-learning|Shared Fleet Learning]] (propagação) + [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (captura de falha) + [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] (alavancagem de observação humana).
- **Guardado por:** [[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]] e [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] — gates que impedem a auto-iteração de amplificar drift.
- **Alimentado por:** [[docs/canonical/production-to-offline-feedback-loop|Production-to-Offline Feedback Loop]] com sua taxonomia de drift — o diagnóstico que o loop precisa antes de iterar sobre o feedback.
- **Generaliza:** [[docs/canonical/unified-tool-surface-flywheel|Unified Tool Surface Flywheel]] — a tese de superfície única aplicada ao produto inteiro sobre a fundação de dados.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:331-349` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md:290-307` — classificação Partial Coverage/High com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.yaml:277-294` — evidência estruturada.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:53` — recursive self-improvement como tese organizacional.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-analysis.md` — extração de conhecimento da fonte.

---

*Created: 2026-08-31 | From: Clay eval stack classification (P1) | Precedence: canonical*
