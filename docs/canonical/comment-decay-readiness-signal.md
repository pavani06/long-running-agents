---
title: "Comment-Decay Readiness Signal"
type: canonical
tags: ["evals", "governanca", "shadow-review", "code-review"]
Status: Active
Source: "AI Engineer talk — Itamar Friedman, Qodo (The Last Human Code Review: Building Trust in AI-Generated Code)"
Classification: "Partial Coverage (P2, Medium integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-31
aliases: ["comment decay readiness", "human comment decay", "100 PRs without human review", "behavioral graduation criterion", "readiness signal automation"]
relates-to:
  - "[[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]]"
  - "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]"
  - "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]]"
  - "[[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]"
sources:
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification|Classification]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis|Knowledge Extraction]]"
---

# Comment-Decay Readiness Signal

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Itamar Friedman, Qodo ([The Last Human Code Review: Building Trust in AI-Generated Code](https://www.youtube.com/watch?v=s-aixZYJG4c))
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Declarar que o review humano não é mais necessário não tem critério observável — e os benchmarks de modelo não servem: "benchmarks for code review did not change a lot throughout the latest model" (`docs/analysis/...-analysis.md:40`). A pergunta "is human code review still optional end of 2026?" (`docs/analysis/...-analysis.md:27`) fica sem resposta operacional.

Sem um sinal comportamental, a graduação para automação vira opinião ou claim de vendor — exatamente a decisão de alto risco que mais precisaria de critério explícito.

## Solução

Métrica comportamental no loop de trabalho real: **volume e tendência de comentários humanos por PR decaindo em direção a zero**, com a contagem acumulada de PRs que passam sem review humano (~100) como critério explícito de graduação (`docs/analysis/...-analysis.md:84`): "you will see that developers are writing less and less comments in the pull request. And then after 100 of these pull requests or human no more human review, you know that you're ready for automation".

| Componente | Função |
|---|---|
| Métrica de volume | Número de comentários humanos por PR |
| Métrica de tendência | Direção do volume ao longo do tempo (decay em direção a zero) |
| Contador acumulado | PRs consecutivos/aprovados sem intervenção humana |
| Threshold de graduação | ~100 PRs sem review humano como gatilho para declarar prontidão |
| Desacoplamento de benchmark | O sinal mede o loop de trabalho, não benchmarks de modelo |

## Implementação neste repositório

### O que já existe

Medição de envolvimento humano e maquinaria de graduação ambas existem — com sinais diferentes do decay comportamental (classification:144-152):

- **Envolvimento humano como métrica de governança:** [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]] — "Treat human presence during agent execution as a governance metric... Measure when the outcome owner was involved, detect when they have been absent too long" (`docs/canonical/presence-in-the-loop-metric.md:31`) — objetivo **oposto**: manter o dono engajado durante a execução, não certificar sua saída; "The signal does not replace the review -- it informs the reviewer about how much ownership was exercised during construction" (`:63`).
- **Graduação por agreement:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] — "agreement metrics determine which AI checks are reliable enough to graduate to blocking status" (`docs/canonical/shadow-review-pipeline.md:31`) — o critério de graduação existe; o sinal é agreement AI-vs-humano, não decay de comentários.
- **Prontidão por eval:** [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] — o tier auto-merge requer `eval_coverage: ">= 0.9 of changed behaviors"` e correlation (`docs/canonical/evals-as-brakes.md:59-63`) — critério eval-based, não comportamental.
- **Estagiamento de retirada humana:** [[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]] — progressão "Observe (human does, agent watches) -> Assist (agent proposes, human approves) -> Own (agent executes, human monitors exceptions)" (`docs/canonical/autonomy-curriculum-sampling.md:60`, citado em `docs/canonical/human-review-staged-workflow-automation.md:67`) — estagia a retirada sem critério observável por PR.

### O que falta

(classification:152) — greps `human comments|comment volume|comments per PR|without human review` em `docs/canonical/` retornam zero matches (os únicos hits de `benchmark` são não-relacionados):

1. **Medição de comentários humanos por PR** — nenhuma doc mede volume/tendência de comentários humanos como sinal.
2. **Contador acumulado de PRs sem review humano** — não existe contador de pass-without-review nem threshold de acumulação.
3. **O threshold ~100-PR** — o número de campo não está registrado em nenhuma superfície (nota: observação de campo, não número validado).
4. **Desacoplamento explícito de benchmarks de modelo** — nenhuma doc estatui que prontidão de automação de review se mede no loop de trabalho, não em benchmark.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Mede confiança no loop de trabalho real em vez de benchmarks de modelo | O threshold de 100 PRs é observação de campo, não número validado |
| Threshold explícito e observável para uma troca organizacional de alto risco | Volume de comentários é proxy: não mede qualidade nem cobertura dos comentários |
| Desacopla a graduação de claims de vendor | Decay só sinaliza prontidão com o context engine rodando por baixo |

## Relação com outros padrões

- **É o gatilho de:** [[docs/canonical/semantic-rule-gated-auto-approve-block|Semantic-Rule-Gated Auto Approve/Block]] — a stack de gating gradual (padrões 5-6 da fonte) aponta para este sinal como critério de quando a automação está pronta (classification:154).
- **Inverte o objetivo de:** [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]] — presença mantém o humano no loop; decay certifica a saída. As duas métricas se complementam: presença durante a construção, decay na graduação do review.
- **Preenche o slot de decisão de:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] — graduação de checks usa agreement; graduação da *automação como um todo* usaria decay.
- **Complementa:** [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] — o tier auto-merge é readiness eval-based; o decay é o sinal comportamental que o acompanha.
- **Fecha a progressão de:** [[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]] / [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — Observe→Assist→Own ganha o critério observável de quando avançar de fase no review.

## Referências

- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md:145-161` — padrão extraído: problema, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification.md:140-154` — classificação Partial Coverage (Medium) com evidência e NOT_FOUND.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis.md:81-84, :40` — mecânica do sinal (decay + 100 PRs) e estagnação de benchmarks.
- `docs/canonical/presence-in-the-loop-metric.md:31, :63` — presença como métrica de governança; sinal informa reviewer.
- `docs/canonical/shadow-review-pipeline.md:31` — graduação por métricas de agreement.
- `docs/canonical/evals-as-brakes.md:59-63` — tier auto-merge com requisitos eval-based.
- `docs/canonical/human-review-staged-workflow-automation.md:67` — progressão Observe→Assist→Own citada.
- `docs/canonical/autonomy-curriculum-sampling.md:60` — phase progression original.
