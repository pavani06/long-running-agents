---
title: "Semantic-Rule-Gated Auto Approve/Block"
type: canonical
tags: ["code-review", "governanca", "evals"]
Status: Active
Source: "AI Engineer talk — Itamar Friedman, Qodo (The Last Human Code Review: Building Trust in AI-Generated Code)"
Classification: "Partial Coverage (P1, High integration value)"
Precedence: "Level 2 (docs/system-of-record.md)"
last_updated: 2026-08-31
aliases: ["semantic rule gated approve block", "auto approve auto block", "rule-driven PR gating", "semantic rules gating", "rule expansion automation"]
relates-to:
  - "[[docs/canonical/software-graph-review-substrate|Software Graph Review Substrate]]"
  - "[[docs/canonical/dual-interface-context-engine|Dual-Interface Context Engine]]"
  - "[[docs/canonical/comment-decay-readiness-signal|Comment-Decay Readiness Signal]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]"
  - "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]"
  - "[[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]]"
  - "[[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]]"
sources:
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification|Classification]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis|Knowledge Extraction]]"
---

# Semantic-Rule-Gated Auto Approve/Block

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer talk — Itamar Friedman, Qodo ([The Last Human Code Review: Building Trust in AI-Generated Code](https://www.youtube.com/watch?v=s-aixZYJG4c))
**Classification:** Partial Coverage (P1, High integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Delegar decisões de approve/block de PR à discrição de um modelo é inaceitável para governança: a decisão não pode ser auditada nem controlada — "you want to do that not just by letting AI choose by yourself" (`docs/analysis/...-analysis.md:75`). Sem um critério externalizado, cada decisão automatizada é uma caixa-preta.

O problema tem camada: o critério de approve/block é ele próprio conhecimento tribal ("when do you guys approve or block a PR") que precisa ser codificado "as part of your context" (`docs/analysis/...-analysis.md:75`). Gatear sem codificar o critério troca a auditoria do humano pela confiança cega no modelo.

## Solução

Decisões automáticas de approve/block dirigidas **apenas por regras semânticas codificadas**, com o conjunto de regras expandindo gradualmente como contexto acumulado: "step by step by adding more rules for blocking and more rules for approving over time" (`docs/analysis/...-analysis.md:75`).

| Componente | Função |
|---|---|
| Regras semânticas codificadas | Critérios de approve/block externalizados do modelo, escritos como regras auditáveis |
| Contexto acumulado | O conjunto de regras cresce com o tempo como parte da camada de contexto governada |
| Resultado por PR | O review de cada PR produz o input que as regras avaliam |
| Expansão gradual | Automação avança adicionando regras de blocking e de approving incrementalmente, não em big-bang |

Pré-requisitos declarados pela fonte: maturidade do context engine e do grafo (padrões 1-2 do pacote) — "now you're ready to start approving and blocking PRs automatically" só depois do nível de grafo (`docs/analysis/...-patterns.md:111`).

A propriedade que carrega o padrão: os critérios de decisão são auditáveis por construction — humanos podem "trust and audit and control" as decisões porque cada approve/block referencia uma regra codificada, não uma discrição de modelo (`docs/analysis/...-patterns.md:118-119`).

## Implementação neste repositório

### O que já existe

A stack de gating graduada existe em profundidade canônica e é em pontos mais instrumentada que o relato-fonte (classification:106-117):

- **Tier de auto-merge:** [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] — "Full suite green + production-correlation tracked | Auto-merge; deploy on merge" (`docs/canonical/evals-as-brakes.md:51`); o YAML de `velocity_tiers` define `- name: auto-merge` requerendo `eval_coverage: ">= 0.9 of changed behaviors"`, `gates: [pr-eval-report, merge-threshold]` e `correlation: "eval score predicts production outcome"` (`:59-63`).
- **Bloqueio com waiver:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — "Block merge when thresholds fail unless an explicit waiver is recorded" (`docs/canonical/pr-gated-eval-enforcement.md:51`).
- **Graduação advisory→blocking:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] — "After the shadow period, agreement metrics determine which AI checks are reliable enough to graduate to blocking status" (`docs/canonical/shadow-review-pipeline.md:31`) — a mecânica de "adicionar bloqueio ao longo do tempo", data-driven.
- **Política confidence-tiered:** [[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]] — "block when any finding category produces a `fail` result for a high-confidence issue; allow when findings are advisory or low-confidence" (`docs/canonical/pre-commit-ai-review-gate.md:75`); "| High: unambiguous violation of a documented rule | Block: must fix before push |" (`:79`) — o tier High já referencia regra documentada.

### O que falta

(classification:115) — greps `auto-approve|auto approve|automatically approv|automerge|auto-merge` em `docs/canonical/` retornam apenas o tier de `docs/canonical/evals-as-brakes.md:59`:

1. **Substrato de decisão semântica** — nenhum doc frameia approve/block dirigido por conjunto **expansivo de regras semânticas codificadas** acumuladas como contexto auditável; os gates do repo keys em métricas de eval e tiers de confiança, não em regras de review codificadas.
2. **Expansão de regras como mecanismo de automação** — a progressão "more rules for blocking and more rules for approving over time" como caminho gradual de automação não está registrada; a graduação do shadow pipeline adiciona *checks*, não *regras semânticas*.
3. **Contradição declarada com a filosofia do repo:** [[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]] mantém deliberadamente o humano nas ações irreversíveis — "**O envio irreversível permanece humano.**" (`docs/canonical/human-review-staged-workflow-automation.md:58`). Adotar o lado approve deste padrão é uma decisão de filosofia (o espectro velocity-vs-correctness da fonte), não um gap técnico a preencher silenciosamente.

## Tradeoffs

| Benefício | Custo |
|---|---|
| Decisões auditáveis e controláveis: cada approve/block referencia uma regra codificada | Cobertura limitada às regras codificadas; casos não codificados seguem precisando de humano |
| Automação expande gradualmente, construindo confiança em vez de exigi-la | Caminho gradual é mais lento que big-bang |
| Os critérios de gating viram contexto acumulado que melhora com o tempo | Habilitar antes da maturidade de contexto/grafo erode a confiança que deveria construir |
| Coexiste com waivers e tiers existentes (evals, confiança) | Tensão direta com a filosofia repo de envio irreversível humano |

## Relação com outros padrões

- **Depende de:** [[docs/canonical/dual-interface-context-engine|Dual-Interface Context Engine]] e [[docs/canonical/software-graph-review-substrate|Software Graph Review Substrate]] — as regras são a camada de contexto; o grafo é o nível que habilita o gating (pré-requisitos declarados do padrão-fonte).
- **Ponte entre clusters:** conecta o cluster de contexto (padrões 1, 3) ao cluster de freios — [[docs/canonical/evals-as-brakes|Evals-as-Brakes]], [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]], [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]], [[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]] — regras-como-contexto que gateiam decisões (classification:117).
- **Gradua para:** o critério comportamental de quando a stack está pronta é [[docs/canonical/comment-decay-readiness-signal|Comment-Decay Readiness Signal]].
- **Consome a telemetria de:** [[docs/canonical/rule-lifecycle-analytics|Rule Lifecycle Analytics]] — regras que gateiam precisam de catch/usage para decidir update/retire/keep.
- **Tensão declarada com:** [[docs/canonical/human-review-staged-workflow-automation|Human-Review Staged Workflow Automation]] (`:58`) — o lado approve automático contradiz a regra repo de irreversibilidade humana; qualquer adoção exige decisão explícita de filosofia.

## Referências

- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md:105-123` — padrão extraído: problema, inputs, outputs, benefícios, limitações.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-classification.md:102-117` — classificação Partial Coverage (High) com evidência e NOT_FOUND de auto-approve.
- `docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-analysis.md:72-75` — mecânica: regras semânticas, acumulação como contexto, expansão gradual.
- `docs/canonical/evals-as-brakes.md:51, :59-63` — tier auto-merge e velocity_tiers.
- `docs/canonical/pr-gated-eval-enforcement.md:51` — bloqueio de merge com waiver explícito.
- `docs/canonical/shadow-review-pipeline.md:31` — graduação advisory→blocking por métricas de agreement.
- `docs/canonical/pre-commit-ai-review-gate.md:75, :79` — política pass/block por confiança.
- `docs/canonical/human-review-staged-workflow-automation.md:58` — contra-filosofia: envio irreversível humano.
