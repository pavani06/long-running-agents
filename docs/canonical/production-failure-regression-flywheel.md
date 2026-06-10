---
title: "Production Failure Regression Flywheel"
type: canonical
aliases: ["regression flywheel", "failure flywheel"]
tags: ["evals", "production", "error-handling"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics Concept]]"]
sources: ["[[docs/analysis/2026-06-10-eval-maturity-phases/analysis|Eval Maturity Analysis]]"]
---
# Production Failure Regression Flywheel

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-eval-maturity-phases/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Production failures repeat when they rely on human memory to become permanent tests. A user complaint, escaped edge case, tool misuse, scoring gap, or incident may be fixed once, but the same class of failure can return after a prompt, model, tool, context, or scoring change.

The repo already has a strong late-session version of this idea. This pattern generalizes the flywheel to all production failures, not only late-session context failures.

## Solution

Every production failure that reveals a behavioral gap should become a durable eval regression case unless it is explicitly rejected as duplicate, unactionable, or out of scope.

Flywheel steps:

1. Intake a production failure, user complaint, incident, escaped edge case, tool misuse, or scoring gap.
2. Capture the interaction, trace, tool results, state snapshot, prompt/model/tool versions, and user-visible outcome.
3. Apply privacy filters and retention rules before preserving any production-derived fixture.
4. Label expected behavior and failure class.
5. Deduplicate against existing cases and update coverage metadata.
6. Add the case to the correct eval tier.
7. Backfill baseline and candidate results to prove the case fails before or passes after the fix.
8. Link the regression case to the incident, PR, or analysis that introduced it.
9. Periodically prune or merge low-value duplicates while preserving unique failure coverage.

Recommended failure taxonomy:

| Failure class | Example |
|---|---|
| Prompt issue | Instruction ignored, tone wrong, constraint missed |
| Tool misuse | Wrong tool, wrong arguments, wrong order, missing tool call |
| Context loss | Prior user preference, decision, or state omitted |
| State persistence | Cart, order, memory, or workflow state corrupted |
| Scoring gap | Eval said pass but user/reviewer judged fail |
| Latency or cost regression | Correct behavior became too slow or expensive |
| Safety or policy issue | Sensitive behavior, unsafe action, or privacy violation |
| Late-session failure | Long-session N+1 or context-reduction failure |

## Implementation in this repo

### What already exists

The repo already has a context-specific version and adjacent rubric guidance:

- Late-Failure Regression Suite says every observed late-session context failure becomes a durable regression case with session shape, context strategy, expected N+1 behavior, and root-cause category (`docs/canonical/late-failure-regression-suite.md:17`).
- That suite should run before context-strategy changes ship, during harness canaries, and after incident fixes (`docs/canonical/late-failure-regression-suite.md:33`).
- The harness evolution playbook says every late context incident generates a permanent regression case with fixture, metadata, gate, and ownership (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1118`).
- The rubric template requires applying rubrics to old incident outputs and includes N+1 long-session fixtures in the regression set (`curriculum/08-tools-templates/evaluation-rubric-template.md:812`).
- The classification says this is strong but not generalized across all production failures, complaints, escaped edge cases, tool misuse, scoring gaps, and suite deduplication (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:98`).

### What needs to be added

The missing implementation is the broad all-failure flywheel.

Add:

1. A failure intake process that accepts incidents, complaints, escaped edge cases, tool misuse, and scoring gaps.
2. A general failure taxonomy beyond late-session context.
3. Required fixture, label, privacy, retention, ownership, and evidence fields.
4. Suite assignment rules using Eval Tier Stratification.
5. Deduplication and pruning rules to prevent regression-suite bloat.
6. Backfill reporting that proves the fixed agent now passes the preserved case.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Converts production incidents into durable development assets | Requires reliable trace capture, redaction, and replay |
| Reduces recurrence of known failures across prompt, tool, model, and loop changes | Can add noise when expected behavior is unclear |
| Preserves institutional memory after incidents and complaints | Needs triage to avoid duplicate or low-value cases |
| Improves eval coverage as real failures emerge | Requires ownership and periodic suite hygiene |

## Relationship to Other Patterns

- **Triggered by:** Pain-Signal Eval Progression Gate when escaped edge cases or complaints repeat.
- **Uses:** Production-Grounded Eval Sampling for safe capture, privacy filters, retention, labels, and replay.
- **Uses:** Eval Tier Stratification to place each new regression in the right tier.
- **Feeds:** PR-Gated Eval Enforcement by making fixed production failures part of future merge evidence.
- **Complements:** Repeatable Agent Spot-Check Set when high-value failures should also be part of fast checks.
- **Generalizes:** Late-Failure Regression Suite from late-session context failures to all production failure classes.

## References

- `docs/analysis/2026-06-10-eval-maturity-phases/patterns.md:142` - extracted pattern definition.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:93` - Partial Coverage classification.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:102` - Late-Failure Regression Suite evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:103` - canonical gate evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:104` - playbook permanent regression evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:105` - rubric incident-output evidence.
- `docs/canonical/late-failure-regression-suite.md:17` - context-specific regression suite.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1118` - permanent late-context regression case rule.
- `curriculum/08-tools-templates/evaluation-rubric-template.md:812` - old incidents as regression examples.

## Better Implementation Cross-References

Do not create separate canonical docs for Metricized Agent Eval Contract or Canary Eval Rollout Gate from this analysis. The classification says the repo already has better implementations: Sprint Contracts, KODA rubrics, and baseline/candidate score comparison exceed the metricized contract pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:37`), while staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:108`).

---

*Created: 2026-06-10 | From: Eval Maturity pattern classification | Precedence: canonical*
