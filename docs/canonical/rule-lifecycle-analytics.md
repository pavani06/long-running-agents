---
title: "Rule Lifecycle Analytics"
type: canonical
tags: ["evals", "code-review", "knowledge-management", "governanca"]
Status: Active
Source: "AI Engineer talk — Itamar Friedman, Qodo (The Last Human Code Review: Building Trust in AI-Generated Code)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-31
aliases: ["rule lifecycle analytics", "per-rule telemetry", "rule catch rate", "rule retire update keep", "review flywheel garbage collection"]
relates-to:
  - "[[docs/canonical/dual-interface-context-engine|Dual-Interface Context Engine]]"
  - "[[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]]"
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]"
  - "[[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard as Primary Detection Surface]]"
  - "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]"
sources:
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification|Classification]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis|Knowledge Extraction]]"
---

# Rule Lifecycle Analytics

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Itamar Friedman, Qodo ([The Last Human Code Review: Building Trust in AI-Generated Code](https://www.youtube.com/watch?v=s-aixZYJG4c))
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Regras, standards e skills codificados degradam em peso morto sem feedback sobre se pegam alguma coisa ou se são sequer usados (`docs/analysis/...-patterns.md:128`). Regra gravada em pedra não verificada é passivo: consome atenção de review e contexto sem evidência de valor.

O problema é a ausência do garbage collection do flywheel de review: "each one of them. How many times they're being caught, which rules and standards and skill is actually being used during the review process and is useful or not or does it need to get an update?" (`docs/analysis/...-analysis.md:79`). Sem essa telemetria, o context lake degrada em cemitério de padrões (`docs/analysis/...-analysis.md:134`).

## Solução

Telemetria por regra/standard/skill alimentando decisões de manutenção update/retire/keep (`docs/analysis/...-patterns.md:129-135`):

| Componente | Função |
|---|---|
| Contador de catch por regra | Quantas vezes cada regra codificada pegou um issue durante runs de review |
| Telemetria de uso | Uso de cada regra, standard e skill durante o processo de review |
| Julgamento de utilidade | A regra é útil, inútil ou precisa de update |
| Decisão de manutenção | Update, retire ou keep por regra/standard/skill |

Fluxo: instrumentar cada run de review → acumular catches e usos por regra → revisar estatísticas em cadência → decidir update/retire/keep → o conjunto de regras permanece evidence-backed em vez de engraved in stone.

## Implementação neste repositório

### O que já existe

Lifecycle analytics existem para componentes de harness e categorias de eval, com telemetria real por componente (classification:125-134):

- **Telemetria de catch por componente:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — "The Context Loader example showed 59 real preventions in 145K turns, 340 false positives, and only 0.4% accuracy difference in a 50% shadow test" (`docs/canonical/measured-harness-evolution-lifecycle.md:46`).
- **Decisão data-driven de retire/keep:** ROI = "(Erros Prevenidos × Custo Médio do Erro) / (Custo Operacional do Componente)" (`docs/canonical/measured-harness-evolution-lifecycle.md:55`); "A component with ROI below 1x for two consecutive quarters becomes a removal candidate" (`:58`).
- **Cadência de governança:** "Govern cadence with a quarterly cycle... Apply One In, One Out" (`docs/canonical/measured-harness-evolution-lifecycle.md:60`).
- **Sessão de manutenção do conjunto de guardrails:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] — "The session produces concrete outputs: updated lint rules, new or amended skills, revised reviewer prompts, expanded eval cases, or updated NFR documents" (`docs/canonical/garbage-collection-day-meta-loop.md:48`).
- **Superfície contínua:** [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard as Primary Detection Surface]] — "**Real-time pass/fail rates** per eval layer, per category... per agent — updated continuously" (`docs/canonical/eval-dashboard-primary-detection-surface.md:32`).
- **Formato de observação:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — "which surface caught it (review, lint, test, production), and how many instances were observed" (`docs/canonical/failure-pattern-classification-loop.md:46`).

### O que falta

(classification:134) — greps `catch rate|caught|per-rule|rule usage|how many times` em `docs/canonical/` retornam apenas as categorias de agreement do shadow review (`docs/canonical/shadow-review-pipeline.md:56-57`) e o formato de observação de falhas:

1. **Dimensão por regra e por skill** — contadores de catch por regra codificada e telemetria de uso por skill durante runs de review não existem; o repo mede componentes de harness e categorias de eval, não o conjunto de regras codificadas consumido pelo review.
2. **Decisões update/retire/keep sobre a tríade regra/standard/skill** — o ciclo de ROI e o GC Day governam componentes e guardrails; a aplicação explícita ao conjunto de regras de review não está registrada.
3. **Instrumentação contínua de runs de review** — os mecanismos existentes operam em cadência (GC Day semanal, ciclo trimestral) ou sobre evals (dashboard); nenhum instrumenta cada run de review para atribuir catches a regras específicas.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Age como garbage collection do flywheel de review — evita o cemitério de padrões | Exige instrumentação de cada run de review |
| Regras permanecem evidence-backed em vez de gravadas em pedra | Catch-rate isolado não captura qualidade da regra (falsos positivos ficam invisíveis) |
| Esforço de manutenção priorizado por dados, não por opinião | Regras de baixo volume demoram a acumular sinal |

## Relação com outros padrões

- **É o GC de:** [[docs/canonical/dual-interface-context-engine|Dual-Interface Context Engine]] — a camada de contexto codificada precisa desta telemetria para não degradar em cemitério de padrões (`docs/analysis/...-analysis.md:134`).
- **Alimenta:** [[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]] — regras que gateiam approve/block são as que mais precisam de evidência de catch/uso para expandir ou retirar.
- **Estende ao conjunto de regras:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — o ciclo BUILD→STABILIZE→SIMPLIFY→REMOVE com ROI aplicado à tríade regra/standard/skill em vez de componentes.
- **Encaixa em:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] (a sessão semanal seria o venue das decisões update/retire/keep) e [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard as Primary Detection Surface]] (a superfície contínua onde a telemetria por regra apareceria).
- **Reaproveita o formato de:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] (`:46`) — o campo "which surface caught it" generalizado para "which rule caught it".

## Referências

- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md:125-143` — padrão extraído: problema, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification.md:121-136` — classificação Partial Coverage (Medium) com evidência e NOT_FOUND de per-rule telemetry.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis.md:77-79, :134` — analítica por regra como GC do flywheel.
- `docs/canonical/measured-harness-evolution-lifecycle.md:46, :55, :58, :60` — telemetria por componente, ROI, remoção, cadência.
- `docs/canonical/garbage-collection-day-meta-loop.md:48` — sessão semanal produzindo guardrails atualizados.
- `docs/canonical/eval-dashboard-primary-detection-surface.md:32` — pass/fail rates contínuas.
- `docs/canonical/failure-pattern-classification-loop.md:46` — formato de observação com surface e instâncias.
