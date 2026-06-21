---
title: 'Measured Harness Evolution Lifecycle'
type: canonical
aliases: ["harness lifecycle", "ciclo vida harness", "harness evolution", "BUILD STABILIZE SIMPLIFY REMOVE"]
tags: ["agentes-orquestracao", "harness", "governanca"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]"]
sources: ["[[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction: Harness Evolution]]"]
---

# Measured Harness Evolution Lifecycle

**Type:** Canonical Pattern
**Status:** Active
**Source:** docs/articles/harness-evolution-metodos-construcao.md
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

A harness that was correct for an older model can become the system's own fragility when nobody revalidates its components after model or workflow changes. In the source case, the KODA team had an 11-component harness in December 2025 with 4000ms latency, 3200 tokens, 9 active components, and R$ 0.048 per turn; by September 2026 the essential harness had 6 components, 1300ms latency, 1200 tokens, 3-4 active components, R$ 0.018 per turn, and the same recommendation quality [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:205-215.

The failure scenario this pattern prevents is an 11-component December 2025 harness still running unchanged in September 2026, paying about 3x the latency of the measured essential harness while preserving components whose marginal value may have disappeared [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:209-215. The source frames this as a paradox: the harness exists to create confidence, but unrevised components add bug surface, latency, tokens, complexity, onboarding burden, and maintenance work [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:117-125.

## Solution

Treat harness evolution as a measured lifecycle, not as one-time architecture. Every component moves through four states: BUILD defensively, STABILIZE with production evidence, SIMPLIFY layer by layer, and REMOVE through archived, reversible removal [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:87-114.

```
+----------------+      +----------------+      +----------------+      +----------------+
| BUILD          | ---> | STABILIZE      | ---> | SIMPLIFY       | ---> | REMOVE         |
| defensive      |      | measure value  |      | reduce layers  |      | archive + flag |
+-------+--------+      +-------+--------+      +-------+--------+      +-------+--------+
        ^                       |                       |                       |
        |                       v                       v                       v
        |               ROI + false positives     shadow/canary          component archive
        |                       |                       |                       |
        +-----------------------+-----------------------+-----------------------+
                                reactivation path when regressions recur
```

**BUILD** is defensive because a new model's production limits are still unknown. The source says to use explicit validation components, rigid limits, generous fallbacks, and long detailed system prompts; the original Context Loader used 1200 tokens per turn and added 450ms because a 32K-token model lost attention after 40 minutes [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:91-96.

**STABILIZE** starts after 60+ days in production, when the team can measure real prevented failures, false positives, and full operating cost instead of relying on the imagined value from build time [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:97-101. The Context Loader example showed 59 real preventions in 145K turns, 340 false positives, and only 0.4% accuracy difference in a 50% shadow test with and without the component [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:99-101.

**SIMPLIFY** removes risk by reducing one layer at a time instead of deleting a component in one jump. The source sequence is remove redundancy, relax constraints, consolidate functions, then remove; the Context Loader simplification ran in 3 waves with 7-14 day shadow tests, removed 1200 tokens and 450ms, and only reduced accuracy by 0.2% inside the margin of error [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:103-108.

**REMOVE** is allowed when a component has fulfilled its purpose and removal remains reversible. The Budget Guard had zero triggers for 180 days after the 200K-token model migration and zero regressions after removal; its code was archived under `archive/components/budget-guard-v1/` with a README explaining why it existed, why it was removed, and which model justified removal, while a feature flag allowed reactivation in minutes [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:109-114.

Use ROI as the removal-governance threshold:

```
ROI = (Erros Prevenidos × Custo Médio do Erro) / (Custo Operacional do Componente)
```

A component with ROI below 1x for two consecutive quarters becomes a removal candidate [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:187-193. Count false positives, latency, token cost, infrastructure cost, maintenance hours, and user outcomes as part of the component's measured cost because the extracted pattern defines those metrics as lifecycle inputs [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns.md|Pattern Extraction YAML]]:275-285.

Govern cadence with a quarterly cycle: week 1 reviews model changelogs, metrics, and component classification; weeks 2-3 implement feature flags, shadow tests, and documented removals; weeks 4-12 observe without stacking new harness changes [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:179-182. Apply One In, One Out so each new harness component marks an existing component for removal investigation in the next cycle [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:183-185.

Removal must preserve causal attribution: one removal at a time, independent feature flag per component, 14+ day shadow test, canary from 5% to 25% to 100%, and 14 days of observation between removals [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:195-198. The component archive should include an ADR with decision date, justifying metrics, validation process, and post-removal result, plus code under `archive/components/<nome>/` with a README so future teams can answer why the component no longer exists [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:199-201.

## Implementation in this repo

### What already exists

- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] already requires a decision record with observed pain, source evidence, current capability, chosen next step, owner, expected operating cost, and review date [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:51-51.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] also records adjacent harness-evolution questions: what failure a component prevents, how often it prevents that failure, token/latency/maintenance cost, replay or A/B proof of safe removal, and rollback speed [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:57-60.
- [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] defines production-sampled replay, baseline/candidate comparison, and reporting of quality, latency, cost, and failure-class deltas [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]:28-52.
- [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]] already references regression tests before canary, staged rollout with shadow diffs, canary metrics, rollback decisions, and 14-day observation [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]:50-53.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] defines baseline/candidate PR eval reports with quality delta, latency delta, cost delta, thresholds, failure examples, and merge policy [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:30-43.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] provides the companion classification that separates permanent domain invariants from model-specific compensations before simplification or removal [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:29-70.

### What is missing

- No existing canonical doc defines the complete BUILD/STABILIZE/SIMPLIFY/REMOVE lifecycle with component archive, ROI calculation, reversible removal, and reactivation path [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-classification|Classification]]:160-175.
- No existing canonical doc assigns every harness component to a lifecycle state and then archives removed components with reason, metrics, validation results, rollback path, and reactivation path [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-classification|Classification]]:175-175.
- The missing archive contract is a standard `archive/components/<component>/` record with README, ADR, decision date, metrics, validation process, post-removal outcome, rollback path, and feature-flag reactivation path [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:113-114 [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:199-201.
- The missing governance contract is the ROI threshold plus quarterly review cadence and One In, One Out rule as a single canonical lifecycle rather than adjacent eval or rollout mechanics [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:179-193.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps the harness as small as possible while preserving measured quality [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns.md|Pattern Extraction YAML]]:286-289 | Requires enough traffic, observability, and patience for shadow and canary windows [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns.md|Pattern Extraction YAML]]:290-293 |
| Counts false positives and operating cost as first-class design signals [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns.md|Pattern Extraction YAML]]:286-289 | Slower than big-bang cleanup because only one component changes at a time [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:195-198 |
| Makes removal reversible and institutionally documented instead of destructive [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns.md|Pattern Extraction YAML]]:286-289 | Bad metrics or short observation windows can produce false confidence [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns.md|Pattern Extraction YAML]]:290-293 |
| Can reduce latency, tokens, cost, and component count without changing quality when evidence supports simplification [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:209-215 | Creates documentation and archive surface that must remain organized [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction]]:112-119 |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]], because lifecycle decisions need each component classified as a permanent domain invariant or a model-specific compensation before simplification or removal [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:29-70.
- **Validated by:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]], because STABILIZE and SIMPLIFY need production-sampled replay, baseline/candidate comparisons, and quality, latency, cost, and failure-class deltas [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]:28-52.
- **Validated by:** [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]], because harness canaries and incident fixes need regression, shadow diffs, rollback decisions, and observation windows [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]:50-53.
- **Validated by:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]], because prompt, model, tool, context, memory, scoring, and loop changes need PR-visible quality, latency, cost, threshold, and merge-policy evidence [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:28-53.
- **Complements:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]], because production failures should become durable eval cases that inform future lifecycle reviews [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40.
- **Complements:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]], because both patterns use observed pain, evidence, operating cost, owner, and review date instead of intuition [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:51-60.

## References

- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:87-114 - source lifecycle definition from BUILD through REMOVE.
- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:117-125 - harness ossification cost as bugs, latency, tokens, complexity, onboarding burden, and maintenance.
- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:179-198 - quarterly cadence, One In One Out, ROI threshold, feature flags, shadow tests, canary, and observation window.
- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:199-215 - component archive requirements and measured heavy-to-essential KODA comparison.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction]]:26-33 - extracted BUILD/STABILIZE/SIMPLIFY/REMOVE lifecycle and KODA examples.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction]]:101-110 - operational lessons for measurement, false positives, shadow tests, quarterly cadence, One In One Out, ROI, and harness reduction.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns.md|Pattern Extraction YAML]]:275-307 - structured pattern definition, inputs, outputs, benefits, limitations, components, and flow.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-classification|Classification]]:160-175 - Partial Coverage classification and missing canonical lifecycle contract.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:51-60 - adjacent decision record and harness-evolution questions.
- [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]:28-52 - production-sampled replay and baseline/candidate deltas.
- [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]:50-53 - regression, staged rollout, shadow diffs, canary metrics, rollback, and observation.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:30-43 - PR eval report fields for quality, latency, cost, thresholds, failures, and merge policy.
