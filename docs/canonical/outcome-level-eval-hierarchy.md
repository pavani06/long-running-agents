---
title: "Outcome-Level Eval Hierarchy"
type: canonical
aliases: ["outcome-level evals", "business results first eval", "vanity metric rejection", "outcome over proxy KPI"]
tags: ["evals", "production", "agentes-orquestracao"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]]"
  - "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"
  - "[[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
---

# Outcome-Level Eval Hierarchy

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Superficial KPIs (number of calls, minutes on call) give signal without truth; most things break at the conversion level, which those metrics never surface (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:297`).

Concrete scenario: an agent team ships a "customer engagement" improvement. The dashboard is euphoric — calls handled up 30%, average minutes on call up 12%. Conversion is flat. The team spends two more quarters optimizing hold music and greeting scripts because the metrics they measure keep improving. Kavak's diagnosis: "Superficial KPI measurement: measuring number of calls or minutes on call gives signal without truth; most things break at the conversion level, which those metrics never surface" (`docs/analysis/...-analysis.md:160`).

Root cause: the **measurement anchor is activity, not outcome**. Proxy KPIs are cheaper to instrument, arrive faster, and correlate with nothing that pays — while business results (did the customer convert, are they happy to re-engage) are slower, costlier, and true. The repository states the same failure in eval terms: "This creates a misalignment where the technical eval passes but the business outcome fails — the agent is technically correct but business-irrelevant" (`docs/canonical/business-outcome-first-eval-pipeline.md:22`), and "Eval scores become false safety signals when they stop predicting user outcomes" (`docs/canonical/eval-to-production-correlation-tracking.md:22`).

## Solution

Order evaluation as a **strict hierarchy with a single loop**: first-order eval is the business result; only then optimize the agentic architecture; add skills where outcomes reveal gaps; re-measure the outcome. Proxy KPIs are explicitly rejected from the readout (`docs/analysis/...-analysis.md:112`; `docs/analysis/...-patterns.yaml:316-321`).

Concrete example — the loop as a config:

```yaml
# outcome-eval-loop.yaml — one loop, strictly ordered
level_1_outcome:                      # FIRST-ORDER: the only truth source
  metric: [funded_conversions_45d, re_engagement_csat]   # did they convert / re-engage
  banned_from_readout: [call_count, minutes_on_call]     # named rejection
level_2_architecture:                 # optimized ONLY against level-1 results
  variables: [context_policy, memory_tiers, harness_shape, model_choice]
level_3_skills:                       # added ONLY where outcomes reveal gaps
  trigger: outcome_gap_cluster (e.g., trade-in quotes lose deals)
  action: add/extend skill, then re-measure level_1
cadence: re-measure outcome after every architecture/skill change
rule: never substitute a proxy KPI for the level-1 readout
```

The hierarchy composes with the repository's existing anchors: business success defined first, then golden answers from domain experts, then the technical pipeline (`docs/canonical/business-outcome-first-eval-pipeline.md:28`), with production outcomes — task success, complaints, escalations, CSAT proxy, retention (`docs/canonical/eval-to-production-correlation-tracking.md:35`) — as the correlation target that keeps eval scores honest.

## Implementation in this repo

### What already exists

- `docs/canonical/business-outcome-first-eval-pipeline.md:22` — the vanity-metric failure stated as technical-pass/business-fail misalignment (the failure mode this hierarchy rejects).
- `docs/canonical/business-outcome-first-eval-pipeline.md:28` — "Invert the eval pipeline construction sequence: define business success first, then create golden answers from domain experts, then build the technical pipeline to compare agent outputs against business-aligned metrics."
- `docs/canonical/business-outcome-first-eval-pipeline.md:46` — outcome metric table row: "| Deflection | % of queries resolved without human intervention | 60% deflection rate |" — business-anchored metrics already exist.
- `docs/canonical/eval-to-production-correlation-tracking.md:22` — false-safety-signal problem: green suites while production outcomes drift.
- `docs/canonical/eval-to-production-correlation-tracking.md:35` — production outcome variables (task success, complaints, escalations, CSAT proxy, latency, cost, retention) as the correlation target.

### What is missing

From the classification justification (`docs/analysis/...-classification.yaml:307-314`):

1. **The explicit hierarchy as a single loop** — measure business outcome → optimize agentic architecture → add skills where outcomes reveal gaps → re-measure: the ordered loop itself exists nowhere as one named mechanism; the repo has the anchors but not the loop composition.
2. **The named rejection of proxy KPIs** (call counts, minutes on call) as a distinct failure class — NOT_FOUND by the classification's own search (`vanity|proxy KPI|superficial` matched only unrelated reward-hacking and glossary entries).
3. **The banned-from-readout rule** — no canonical doc forbids substituting activity metrics for the outcome readout once outcomes prove slow or noisy.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Truth-anchored optimization: rejects vanity metrics explicitly (`docs/analysis/...-patterns.yaml:305`) | Requires instrumentation of conversion/CSAT-type outcomes end to end (`docs/analysis/...-patterns.yaml:309`) |
| Directly links agent changes to business value (`docs/analysis/...-patterns.yaml:306`) | Outcome attribution can lag behind the agent change that caused it (`docs/analysis/...-patterns.yaml:310`) |
| Provides the measurement foundation for goal-driven agents (`docs/analysis/...-patterns.yaml:307`) | Proxy KPIs remain tempting because they are cheaper to collect (`docs/analysis/...-patterns.yaml:311`) |
| Conversion-level failures become visible instead of hidden behind activity metrics (`docs/analysis/...-analysis.md:160`) | End-to-end outcome instrumentation is a real build cost the team must fund up front |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]] — supplies the business-first construction sequence the hierarchy's level 1 assumes.
- **Validated by:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — the correlation check is what proves the level-1 anchor still predicts reality.
- **Validates:** [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]] — outcome attainment (this hierarchy's level 1) is the only valid measure of a hard goal; step compliance cannot evaluate a goal-driven agent.
- **Complements:** [[docs/canonical/eval-investment-parity|Eval-Investment Parity]] — parity funds the eval build; this hierarchy fixes what the funded evals are allowed to measure.
- **Complements:** [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] — path analysis catches wrong-path-right-answer at the process level while this pattern anchors the result level.

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:111-112` — first-order eval is business results; explicit rejection of superficial KPIs.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:160,175` — superficial-KPI failure pattern; evals as the currency converting capability into velocity.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:296-321` — components/flow/limitations.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:284-314` — Partial Coverage (Medium) classification with the evidence cited above.
- Source: a16z interview, channel and video_id per `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md:5-8`.
