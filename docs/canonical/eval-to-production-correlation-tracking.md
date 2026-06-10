# Eval-to-Production Correlation Tracking

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-eval-maturity-phases/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Eval scores become false safety signals when they stop predicting user outcomes. A suite can stay green while production complaints, escalations, latency, cost, retention, or task success move in the wrong direction.

For long-running agents, this is especially risky because prompt, model, tool, context, and workflow changes can shift production behavior without immediately breaking existing eval cases.

## Solution

Create a named correlation-tracking system that audits whether eval scores continue to predict production outcomes over time.

The correlation system should include:

| Component | Requirement |
|---|---|
| Eval history | Eval run IDs, score distributions, suite/tier, rubric version, threshold version, and baseline/candidate version |
| Production outcomes | Task success, complaints, escalations, support tickets, CSAT proxy, latency, cost, retention, or domain-specific success metrics |
| Change markers | Release, model, prompt, tool, memory, context, rubric, and threshold-change events |
| Correlation dashboard | Time-series view of eval scores beside production outcomes and score-to-outcome correlation by suite, segment, and release |
| Decay thresholds | Warning and blocking thresholds for when eval scores no longer predict production movement |
| Recalibration triggers | Required review of rubrics, thresholds, sampling, labels, or suite composition when correlation decays |
| Ownership | Named owner, review cadence, and escalation path for unresolved score/outcome mismatch |

Operational steps:

1. Record eval run metadata in a form that can be joined to release and production metric windows.
2. Select production outcome metrics that the eval suite is expected to predict.
3. Compare score movement against production movement after each release, canary, or scheduled review window.
4. Segment correlation by workflow, traffic class, suite, model, prompt, tool family, and risk class when volume allows.
5. Alert or require review when eval scores improve but production outcomes degrade, or when production outcomes improve without eval scores reflecting the change.
6. Recalibrate rubrics, thresholds, sampling, labels, or suite composition when correlation decay is confirmed.
7. Preserve correlation reports as evidence for PR gates, rollout decisions, and future eval-system changes.

## Implementation in this repo

### What already exists

The repo already has adjacent calibration and production metric mechanics:

- Evaluation Rubrics describes a Continuous Calibration Loop where production rubric scores are compared with real outcomes such as returns, complaints, and repeat purchase, then weights and thresholds are periodically adjusted (`curriculum/05-core-concepts/08-evaluation-rubrics.md:153`).
- The same rubric guidance reserves threshold-based routing and continuous calibration for systems with real production data (`curriculum/05-core-concepts/08-evaluation-rubrics.md:155`).
- The harness playbook shows staging and canary dashboards comparing baseline and candidate metrics such as incomplete response rate, token budget, latency, evaluator rejection rate, and CSAT proxy (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1596`).
- The canary comparison records baseline, candidate, delta, and gate status for production metrics (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1654`).
- Feature readiness requires calibrated rubrics, replayable traces, and canary metrics with no trust regression (`curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md:1193`).
- The classification says these are adjacent mechanics, but not a named correlation-tracking pattern with decay alerts or recalibration triggers (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:127`).

### What needs to be added

The missing implementation is a first-class correlation system that joins eval score history to production outcomes and treats correlation decay as an operational signal.

Add:

1. A correlation dashboard that displays eval scores, production outcomes, release markers, and score-to-outcome correlation over time.
2. Joinable metadata connecting eval runs to baseline/candidate versions, release windows, canary windows, rubric versions, threshold versions, and production metric windows.
3. Explicit production metrics each eval suite claims to predict.
4. Warning and blocking thresholds for score/outcome mismatch and correlation decay.
5. A recalibration workflow for rubrics, thresholds, sampled cases, labels, and suite composition.
6. Durable correlation reports that can be referenced by PR gates, rollout reviews, and incident follow-ups.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Audits whether evals measure useful agent quality | Requires stable production instrumentation and enough outcome data |
| Detects metric theater before eval gates become false confidence | Correlation can be confounded by traffic mix, releases, seasonality, or external events |
| Improves trust in PR and rollout gates by tying scores to outcomes | Needs joinable metadata across eval, release, and observability systems |
| Turns score/outcome mismatch into a recalibration trigger | Low-volume agents may still need qualitative review alongside quantitative tracking |

## Relationship to Other Patterns

- **Requires:** Metricized Agent Eval Contract so eval outputs are trendable and comparable across versions.
- **Consumes:** Production-Grounded Eval Sampling to keep suites aligned with real traffic and outcome distributions.
- **Consumes:** PR-Gated Eval Enforcement reports as change-level score and delta evidence.
- **Consumes:** Canary Eval Rollout Gate data as early production outcome windows after candidate exposure.
- **Feeds:** Production Failure Regression Flywheel when production outcomes reveal cases that eval scores failed to predict.
- **Triggers:** Pain-Signal Eval Progression Gate when score/outcome mismatch shows the current eval maturity is no longer sufficient.
- **Complements:** Existing continuous calibration, baseline/candidate dashboards, and feature-readiness requirements.

## References

- `docs/analysis/2026-06-10-eval-maturity-phases/patterns.md:184` - extracted pattern definition.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:122` - Partial Coverage classification.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:131` - Continuous Calibration Loop evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:132` - baseline/candidate dashboard evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:133` - feature readiness evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:134` - missing named correlation-tracking pattern.
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:153` - production rubric score calibration strategy.
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:156` - outcomes collected and weights/thresholds adjusted.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1596` - staging baseline/candidate dashboard.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1654` - production baseline/candidate delta gate.
- `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md:1193` - feature readiness requirement.

## Better Implementation Cross-References

Do not create separate canonical docs for Metricized Agent Eval Contract or Canary Eval Rollout Gate from this analysis. The classification says the repo already has better implementations: Sprint Contracts, KODA rubrics, and baseline/candidate score comparison exceed the metricized contract pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:37`), while staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:108`).

---

*Created: 2026-06-10 | From: Eval Maturity pattern classification | Precedence: canonical*
