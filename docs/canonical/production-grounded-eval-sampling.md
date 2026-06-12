---
title: "Production-Grounded Eval Sampling"
type: canonical
aliases: ["eval sampling", "production sampling"]
tags: ["evals", "production"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics Concept]]"]
sources: ["[[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis|Eval Maturity Analysis]]"]
---
# Production-Grounded Eval Sampling

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-eval-maturity-phases/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Hand-authored eval sets miss real user distributions and long-tail agent failures. They usually reflect what the team expects users to do, not what production users, traces, tools, and state actually produce.

For long-running agents, this gap is especially risky because failures can depend on conversation length, tool-return shape, state history, user phrasing, or unexpected workflow combinations.

## Solution

Create an end-to-end production-sampled eval dataset that can replay representative real interactions against candidate agent versions.

Required dataset mechanics:

| Component | Requirement |
|---|---|
| Capture | Production interactions, agent traces, tool results, and relevant state snapshots |
| Privacy filters | Redaction or exclusion for secrets, personal data, credentials, payment details, and sensitive business data |
| Retention policy | Time-bound storage rules, deletion process, and allowed use cases |
| Sampling criteria | Representative segments, critical workflows, failure-prone paths, and rare-but-high-risk cases |
| Coverage metadata | Product area, workflow, tool family, traffic segment, session length, language, risk class, and source window |
| Expected-behavior labeling | Human or rubric labels for task success, tool correctness, instruction following, and unacceptable behavior |
| Replay infrastructure | Runner that applies candidate prompt, model, tools, context strategy, and state fixtures against captured cases |
| Refresh cadence | Scheduled and incident-driven dataset updates |

Operational steps:

1. Define which production surfaces are eligible for eval sampling.
2. Filter, redact, and retain only data that is safe and justified for evaluation.
3. Sample cases by coverage metadata, not only random volume.
4. Label expected behavior and unacceptable behavior before using the case as a gate.
5. Replay the dataset against baseline and candidate agent versions.
6. Report quality, latency, cost, and failure-class deltas.
7. Refresh the dataset as traffic, product behavior, and agent architecture change.

## Implementation in this repo

### What already exists

The repo already teaches production-like replay and sampled trace review:

- KODA harness evolution repeatedly requires replay of real anonymized conversations before canary (`curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1552`).
- The harness playbook configures shadow tests with `traffic_sample_percentage`, baseline/candidate comparison, metrics, and manual review of sampled traces (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:710`).
- Canary investigation samples traces by flag, metric, window, and limit (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1669`).
- The classification says these are adjacent mechanics, but not a first-class production-sampled eval corpus (`docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:57`).

### What needs to be added

The missing implementation is a formal corpus with privacy, retention, metadata, labeling, and replay contracts.

Add:

1. A documented production sampling policy with privacy filters and retention limits.
2. A coverage metadata schema for sampled eval cases.
3. Expected-behavior labels for each case before it is used in gates.
4. Replay infrastructure that can run the same captured interaction against baseline and candidate versions.
5. Dataset refresh and deletion procedures tied to product and traffic changes.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Aligns eval distribution with real user behavior | Requires safe capture, redaction, storage, and deletion workflows |
| Finds failures hand-written cases are unlikely to anticipate | Needs enough production volume to sample meaningfully |
| Grounds prompt, model, and tool changes in observed usage | Labeling can be expensive and partially subjective |
| Produces coverage metadata for reviewer confidence | Sampling can still miss rare edge cases |

## Relationship to Other Patterns

- **Triggered by:** Pain-Signal Eval Progression Gate when hand-authored cases no longer explain production complaints.
- **Builds on:** Repeatable Agent Spot-Check Set by reusing fixture, expected-outcome, and baseline conventions.
- **Feeds:** Eval Tier Stratification as the source for medium and deep replay tiers.
- **Feeds:** PR-Gated Eval Enforcement by producing baseline/candidate deltas for risky changes.
- **Feeds:** Production Failure Regression Flywheel when sampled production cases expose failures.
- **Complements:** Existing shadow test, canary trace sampling, and anonymized replay guidance.

## References

- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-patterns.md:79` - extracted pattern definition.
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:52` - Partial Coverage classification.
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:61` - anonymized conversation replay evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:62` - shadow test and sampled trace review evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:63` - canary trace sampling evidence.
- `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1552` - real anonymized conversation replay before canary.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:710` - shadow traffic sample setup.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1669` - canary investigation sampling.

## Better Implementation Cross-References

Do not create separate canonical docs for Metricized Agent Eval Contract or Canary Eval Rollout Gate from this analysis. The classification says the repo already has better implementations: Sprint Contracts, KODA rubrics, and baseline/candidate score comparison exceed the metricized contract pattern (`docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:37`), while staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern (`docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md:108`).

---

*Created: 2026-06-10 | From: Eval Maturity pattern classification | Precedence: canonical*
