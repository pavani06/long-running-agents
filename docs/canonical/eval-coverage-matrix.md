---
title: "Eval Coverage Matrix"
type: canonical
aliases: ["eval portfolio matrix", "matriz de cobertura de evals", "determinism x deployment matrix", "eval quadrant coverage"]
tags: ["evals", "production", "governanca"]
last_updated: 2026-08-31
relates-to:
  - "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]"
  - "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"
  - "[[docs/canonical/perceived-eval|Perceived-Eval]]"
  - "[[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]]"
  - "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]"
  - "[[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/canonical/bulk-in-context-trace-analysis|Bulk In-Context Trace Analysis]]"
sources:
  - "[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns (2026-08-31)]]"
---

# Eval Coverage Matrix

**Type:** Canonical Pattern
**Status:** Active
**Source:** Inside Clay's Eval Stack (300M Agent Runs, One LangSmith Pipeline) — LangChain, via `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage (P1) — integration value High
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Times de agentes sobre-investem num único estilo de avaliação (geralmente goldens offline) e ficam cegos para classes de falha que moram em outras combinações de determinismo × deployment (`docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:15-34`).

O problema é de *portfólio*, não de mecanismo: cada doc de evals do repo olha para um eixo isolado (tipo de mecanismo, ou velocidade/trigger), e nenhuma visão única responde "quais combinações determinismo×deployment temos cobertas, e quais quadrantes estão vazios?". Sem esse vocabulário compartilhado, argumentos sobre "o que falta no nosso eval" são informais.

## Solution

Classificar todo mecanismo de eval em dois eixos — **determinismo** (deterministic vs. nondeterministic) e **deployment** (offline vs. online) — e gerenciar a cobertura como uma matriz 2x2 (`...-patterns.md:19-26`):

| | Offline | Online |
|---|---|---|
| **Deterministic** | goldens, checks estruturados, asserções de trajetória | A/B metrics, telemetria comportamental objetiva |
| **Nondeterministic** | LLM-as-judge, simulated users, bulk trace analysis | online evaluators, perceived-eval (correção do usuário), NPS |

Regras do padrão:

1. **Meta de cobertura: "a few things in each box"** — alguns mecanismos por quadrante, não profundidade em um só. É um piso, não um target.
2. **Gap list explícita** de quadrantes descobertos — o output tão importante quanto a matriz em si.
3. **Alocação de investimento** entre mecanismos, derivada da matriz e das restrições de observabilidade de produção (volume de traces, capacidade de contato com clientes).
4. Sinal online/nondeterministic (qualidade percebida, correção do usuário) vira entrada de eval first-class, não afterthought (`...-patterns.md:29`).

## Implementation in this repo

### What already exists

O catálogo de mecanismos existe, distribuído e profundo — cada mecanismo com doc canônico próprio:

- **Goldens:** [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]] (`docs/canonical/workflow-derived-golden-question-set.md:44-47`) e [[docs/canonical/living-eval-dataset|Living Eval Dataset]] (`docs/canonical/living-eval-dataset.md:79`).
- **Checks estruturados:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] (`docs/canonical/constraint-anchored-evaluation.md:31-33`).
- **LLM-as-judge:** `docs/canonical/3-layer-evaluation-architecture.md:45-59`.
- **Análise comportamental de traces:** [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] (`docs/canonical/behavioral-eval-path-analysis.md:34`).
- **A/B + canary com eval gates:** `docs/articles/evals-ecommerce-koda.md:107`.
- **Eval humano/rubricas:** `curriculum/05-core-concepts/08-evaluation-rubrics.md`.

Mas cada estratificação existente usa um eixo só:

- `docs/canonical/3-layer-evaluation-architecture.md:28` — classifica por **tipo de mecanismo** ("what they evaluate, not by when they run").
- `docs/canonical/eval-tier-stratification.md:32-36` — classifica por **velocidade/trigger** (fast/medium/deep).

### What is missing

A matriz em si (`...-classification.md:15-27`):

1. **A matriz 2x2 (determinismo × offline/online)** não existe formalizada — grep `determinism|deterministic.*nondeterministic|offline.*online` em `docs/canonical/` retorna único hit não relacionado (`llm-as-fuzzy-compiler.md`).
2. **A meta de cobertura por quadrante** ("a few things in each box") — não há noção de piso por quadrante.
3. **A gap list de quadrantes** — nenhum doc enumera quais combinações estão descobertas (o quadrante online/nondeterministic, por exemplo, está vazio até [[docs/canonical/perceived-eval|Perceived-Eval]]).
4. **O vocabulário de portfólio** para discutir alocação de investimento entre mecanismos.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Elimina blind spots de quadrante único: cada classe de falha tem ao menos um detector | Meta de cobertura dilui profundidade — "alguns por caixa" é piso, não alvo |
| Promove sinal online/nondeterministic (perceived-eval) a entrada first-class | Quadrantes online exigem instrumentação de produção e tráfego real |
| Vocabulário compartilhado para argumentar sobre lacunas do portfólio de evals | Rótulos de quadrante escondem grandes diferenças de custo entre mecanismos |
| Conecta docs existentes sob uma visão única de portfólio | A matriz precisa ser mantida: novos mecanismos exigem reclassificação |

## Relationship to Other Patterns

- **Ortogonal a:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] (eixo tipo de mecanismo) e [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] (eixo velocidade/trigger) — esta doc adiciona o terceiro par de eixos (determinismo × deployment); as três lentes compõem, não competem.
- **Popula quadrantes com:** [[docs/canonical/workflow-derived-golden-question-set|Workflow-Derived Golden Question Set]], [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]], [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]], [[docs/canonical/bulk-in-context-trace-analysis|Bulk In-Context Trace Analysis]].
- **Depende de:** [[docs/canonical/perceived-eval|Perceived-Eval]] para o quadrante online/nondeterministic.
- **Alimenta:** [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] — a cobertura por quadrante é a unidade que sustenta a velocidade de shipping permitida.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:15-34` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md:15-27` — classificação Partial Coverage/High com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.yaml:10-30` — evidência estruturada.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-analysis.md` — extração de conhecimento da fonte.

---

*Created: 2026-08-31 | From: Clay eval stack classification (P1) | Precedence: canonical*
