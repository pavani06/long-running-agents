---
title: "PR-Gated Eval Enforcement"
type: canonical
aliases: ["PR gated", "eval enforcement"]
tags: ["evals"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[curriculum/08-tools-templates/evaluation-rubric-template|Evaluation Rubric Template]]"]
sources: ["[[docs/analysis/2026-06-10-eval-maturity-phases/analysis|Eval Maturity Analysis]]"]
---
# PR-Gated Eval Enforcement

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-eval-maturity-phases/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Prompt, model, tool, context, or agent-loop changes can look harmless in a diff while materially changing agent quality, latency, cost, tool behavior, or failure rate. Generic tests and reviewer intuition are not enough evidence for these changes.

The pattern makes eval impact visible on the PR and defines when that impact blocks merge, requires escalation, or can be accepted.

## Solution

Require eval-specific reports on PRs that touch prompt, model, tool, context, memory, scoring, or agent-loop behavior.

A PR eval report should include:

| Field | Requirement |
|---|---|
| `change_scope` | Prompt, model, tool, memory, context strategy, loop, rubric, or scoring change |
| `baseline_version` | Current production or main-branch version used for comparison |
| `candidate_version` | PR version under review |
| `eval_tiers_run` | Fast, medium, and deep tiers run or intentionally skipped |
| `quality_delta` | Task success, rubric score, judge score, or pass-rate delta |
| `latency_delta` | Median, p95, or budget-impact change |
| `cost_delta` | Token, model, tool, or infrastructure cost delta |
| `thresholds` | Blocking, warning, and escalation thresholds |
| `failure_examples` | Links to traces, fixtures, or sampled cases that explain regressions |
| `merge_policy` | Pass, fail, needs-review, hold for deep eval, or approved waiver |

Operational steps:

1. Detect whether a PR touches eval-sensitive surfaces.
2. Select required eval tiers from the Eval Tier Stratification registry.
3. Run baseline and candidate evals using the same fixtures and labels.
4. Attach a summarized report to the PR body or PR artifacts.
5. Block merge when thresholds fail unless an explicit waiver is recorded.
6. Escalate when eval scores and reviewer judgment disagree.
7. Preserve report links for later incident and regression analysis.

## Implementation in this repo

### What already exists

The repo already has strong PR workflow and validation:

- The issue-review skill validates the worktree, creates a draft PR, runs second-agent review, and stops before merge (`.opencode/skills/issue-review/SKILL.md:12`).
- The same skill requires relevant gates from `package.json`, optional surface-specific gates, and validation output summaries for the PR body (`.opencode/skills/issue-review/SKILL.md:44`).
- The PR template requires test evidence and regression-suite verification for crossroad files (`.github/PULL_REQUEST_TEMPLATE.md:11`).
- Issue review says behavior or architecture changes should update relevant canonical docs, guides, evidence, or ADRs and must not contradict accepted ADRs (`.opencode/skills/issue-review/SKILL.md:77`).
- The classification says this is strong PR validation, but not eval-specific PR gating for prompt/model/tool/loop changes (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:84`).

### What needs to be added

The missing implementation is an eval-specific PR report and merge policy.

Add:

1. Change-surface detection for prompt, model, tool, memory, context, rubric, and agent-loop changes.
2. Required eval-tier mapping per change surface.
3. Baseline-vs-candidate report format with quality, latency, and cost deltas.
4. Thresholds that classify results as pass, fail, or needs-review.
5. A waiver policy for justified merges when eval evidence is incomplete or noisy.
6. Links from PR evidence to durable docs or artifacts when results affect future regression suites.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Moves eval from separate activity into daily development workflow | Adds PR overhead for eval-sensitive changes |
| Gives reviewers evidence beyond prompt diffs and intuition | Requires reliable tier selection and thresholds |
| Makes quality, latency, and cost tradeoffs visible before merge | Flaky or expensive evals can slow delivery |
| Creates auditable merge decisions for agent behavior changes | Needs leadership support to prevent bypasses |

## Relationship to Other Patterns

- **Triggered by:** Pain-Signal Eval Progression Gate when PRs merge with unclear quality impact.
- **Requires:** Eval Tier Stratification to define which evals are required for each change type.
- **Consumes:** Repeatable Agent Spot-Check Set for fast PR checks.
- **Consumes:** Production-Grounded Eval Sampling for representative medium or deep PR evidence.
- **Feeds:** Production Failure Regression Flywheel when a PR-gate failure reveals a new durable case.
- **Complements:** Existing issue-review skill, PR template, second-agent review, and documentation precedence rules.

## References

- `docs/analysis/2026-06-10-eval-maturity-phases/patterns.md:121` - extracted pattern definition.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:79` - Partial Coverage classification.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:88` - issue-review workflow evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:89` - PR template evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:90` - behavior and architecture documentation gate evidence.
- `.opencode/skills/issue-review/SKILL.md:44` - current validation step.
- `.opencode/skills/issue-review/SKILL.md:75` - validation output summaries for PR body.
- `.github/PULL_REQUEST_TEMPLATE.md:11` - current test evidence section.

## Better Implementation Cross-References

Do not create separate canonical docs for Metricized Agent Eval Contract or Canary Eval Rollout Gate from this analysis. The classification says the repo already has better implementations: Sprint Contracts, KODA rubrics, and baseline/candidate score comparison exceed the metricized contract pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:37`), while staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:108`).

---

*Created: 2026-06-10 | From: Eval Maturity pattern classification | Precedence: canonical*
