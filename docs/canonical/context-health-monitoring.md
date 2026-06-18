---
title: "Context Health Monitoring"
type: canonical
tags: ["context-engineering", "agentes-orquestracao", "harness-engineering"]
aliases: ["context quality monitoring", "health score aggregator", "near-miss detection", "effective context estimation"]
last_updated: 2026-06-18
relates-to: ["[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]", "[[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]"]
sources: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|Memory Selection Problem Analysis]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]"]
---
# Context Health Monitoring

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-18-memory-selection-problem/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Agents fail catastrophically — they maintain apparent performance and then cliff, rather than degrading gracefully with warning. Binary success/failure monitoring per step cannot detect the approaching inflection point. The failure mode is not gradual erosion but sudden collapse, making it hard to predict, debug, or recover from.

The repo has sophisticated token-budget-oriented health monitoring: [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]] with green/yellow/orange/red phases, [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]] with acceleration detection, and [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] for severity classification. This is a strong implementation of token health monitoring. However, it monitors quantity (how many tokens remain, how fast they are consumed) — not quality (how effective is the context the model is reasoning over?).

## Solution

Extend health monitoring beyond token quantity to context quality. Monitor three semantic dimensions that predict the approach of the cliff before catastrophe:

1. **Effective Context Size**: The fraction of the current window the model is reliably reasoning about — accounting for the well-documented head/tail attention bias where the middle is systematically under-attended.
2. **Near-Miss Rate**: Proportion of retrieved context that is similar but not relevant — distractors that entered the window but do not help the task, directly measuring the quality of the selection layer.
3. **Contradiction Rate**: Frequency of outputs contradicting prior decisions or facts stored in the relational graph — a leading indicator that the model is losing coherence.

Aggregated into a single health trajectory score, these dimensions provide early warning of approaching cliff failure and enable preemptive intervention before degradation becomes catastrophic.

**Key components:**

- **Effective Context Estimator**: Measures the fraction of the current window the model is reliably attending to, accounting for head/tail bias.
- **Near-Miss Detector**: Compares retrieved context against task requirements to flag context that entered the window but was irrelevant.
- **Contradiction Scanner**: Compares each model output against prior decisions and facts to detect inconsistencies.
- **Health Score Aggregator**: Combines effective context size, near-miss rate, and contradiction rate into a single health trajectory score.

**Flow:**
1. After each agent step, compute effective context size from window occupancy and known attention profile.
2. Compare retrieved context against the task's actual requirements to measure near-miss rate.
3. Scan the model's output for contradictions with prior decisions stored in the relational graph.
4. Aggregate the three metrics into a health score and append to the trajectory.
5. If health score crosses warning threshold, emit early warning alert.
6. If health score crosses critical threshold, trigger intervention: pause, flush context, reload from relational graph.

## Implementation in this repo

### What already exists

The repo has a strong foundation for token-level health monitoring — the "quantity" dimension:

- **Phase-gated health monitoring**: [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:29 — "Defina um monitor de saude de tokens que rode em cada turno... O monitor recebe percentual de budget restante, previsao de burn rate, sinal de aceleracao."
- **Burn rate forecasting**: [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]:31 — "Track token usage as a timestamped time series and forecast session runway from current consumption velocity, acceleration, reserved output capacity, and configured safety buffer."
- **Tested degradation ladder**: [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29 — "ordered contract: classify failure, bounded repair, safe fallback or hold, human escalation, outcome log, rung tests."
- **Failure pattern classification**: [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]:31 — "Classify every observed agent failure into a root cause class and map each class to the smallest guardrail surface."
- **Long-session evals**: [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]] and [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]] catch late-session failures.

### What is missing (the gap)

The repo monitors token quantity — not context quality. The missing semantic dimensions:

1. **Effective Context Estimator**: No measurement of attention effectiveness within the window. The repo knows the window size but not what fraction the model is actually attending to.
2. **Near-Miss Detector**: No comparison of retrieved vs. actually relevant context. The repo retrieves by handle and topic but does not measure whether retrieved items were distractors.
3. **Contradiction Scanner**: No detection of outputs contradicting prior decisions. The repo classifies failures post-hoc ([[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]) but does not scan output for semantic contradictions during execution.
4. **Health Score Aggregator**: No combined metric merging context quality dimensions. The phase-gated health monitor combines budget percentage and burn rate, but not effective context, near-miss, and contradiction metrics.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Detects the approach of catastrophic failure before it happens, enabling preemptive intervention | Defining near-miss requires ground truth about what context is actually relevant — circular with the selection problem |
| Shifts monitoring from binary (pass/fail) to continuous (health trajectory), matching the actual failure mode | Contradiction detection requires comparing current outputs against prior decisions, adding token cost |
| Near-miss rate directly measures the quality of the selection layer | Thresholds for health metrics are domain-specific and require calibration from production data |
| Enables automated recovery: when health score drops, trigger context flush and reload | The monitoring system itself consumes context tokens, marginally contributing to the problem it detects |

## Relationship to Other Patterns

- **Extends:** [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]] by adding quality dimensions (effective context, near-miss, contradiction) to the existing quantity dimensions (budget, burn rate).
- **Uses:** [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]] for the token runway context that frames quality decisions.
- **Triggers:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] with quality-based rung transitions.
- **Feeds:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] with semantic failure data (near-miss patterns, contradiction clusters).
- **Feeds:** Agent Degradation Loop Prevention (P1) by identifying which link of the degradation loop is currently dominant.
- **Validated by:** [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]] and [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]] for quality-metric calibration.

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|analysis]] — agents cliff, they don't degrade gracefully and cliff-then-surprise failure mode.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|patterns]]:246-293 — extracted Context Health Monitoring pattern definition.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|classification]]:153-182 — Partial Coverage classification with evidence and missing mechanics.
- [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:29 — phase-gated health monitoring.
- [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]:31 — burn rate forecasting.
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29 — tested degradation ladder.
- [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]:31 — failure pattern classification.

---

*Created: 2026-06-18 | From: Memory Selection Problem pattern classification | Precedence: canonical*
