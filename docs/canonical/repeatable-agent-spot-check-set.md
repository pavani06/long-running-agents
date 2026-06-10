---
title: "Repeatable Agent Spot-Check Set"
type: canonical
aliases: ["spot check", "repeatable eval"]
tags: ["evals"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"]
sources: ["[[docs/analysis/2026-06-10-eval-maturity-phases/analysis|Eval Maturity Analysis]]"]
---
# Repeatable Agent Spot-Check Set

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-eval-maturity-phases/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Manual prompt trials are not a reliable regression signal for multi-step agent behavior. A reviewer may remember one or two examples, run them informally, and miss regressions in tool use, state handling, expected outcomes, or long-running workflow continuity.

The first eval maturity step should be a small named set of repeatable cases that everyone can run and interpret before heavier production sampling or tiered infrastructure exists.

## Solution

Define a named seed set of spot-check eval cases for critical agent workflows. The set should be small enough to run frequently and structured enough to become automated later.

Each case should include:

| Field | Purpose |
|---|---|
| `case_id` | Stable name for discussion and baseline comparison |
| `workflow` | Critical agent path, task, user intent, or operational scenario |
| `input` | User prompt, task brief, trace segment, or starting event |
| `state_fixture` | Required memory, files, tool state, cart/order state, or prior turns |
| `expected_outcome` | Observable behavior that must happen |
| `acceptable_tool_behavior` | Allowed tool calls, forbidden tool calls, order constraints, or no-tool expectation |
| `baseline` | Saved output, score, trace, or reviewer decision for the current agent version |
| `grading_notes` | Human or rubric instructions for ambiguous cases |
| `owner` | Person or team responsible for refreshing the case |

Operational steps:

1. Choose 5-15 cases that cover the highest-value and highest-risk workflows.
2. Save the fixtures and expected outcomes in a durable location.
3. Record the current prompt, model, tool, and agent-loop baseline result.
4. Run the set before prompt, model, tool, or loop changes merge.
5. Promote recurring failures into broader regression suites when they stop being spot checks.
6. Refresh the seed set when production behavior or product scope changes.

## Implementation in this repo

### What already exists

The repo already has repeatable trace examples and regression-battery guidance:

- The trace-reading curriculum provides four reconstructed real KODA trace cases with trace JSON, manual analysis, script output, diagnosis, and lesson (`curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3876`).
- The same trace-reading module says those cases can be used for practice, training, CI/CD automation, and comparison with new traces (`curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:4580`).
- The harness-evolution playbook includes a component-specific regression battery with concrete long-context and context-limit cases (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`).
- The classification identifies this as repeatable adjacent material but not a named seed-set formalization (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:28`).

### What needs to be added

The missing implementation is the named seed set and its metadata contract.

Add:

1. A canonical name for the repo's first spot-check suite.
2. Case records that include critical workflow, expected outcome, acceptable tool behavior, state fixture, and saved baseline.
3. A lightweight runner or checklist that can be used manually first and automated later.
4. A refresh rule that adds cases from production complaints, trace-reading discoveries, and escaped regressions.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Creates the first repeatable safety net without production-scale infrastructure | Covers mostly known cases from team memory |
| Gives reviewers concrete examples of good agent behavior | Manual execution can become slow as the set grows |
| Produces baselines for future automation | Baselines can become stale after legitimate behavior changes |
| Catches obvious regressions before users find them | Does not prove production-distribution coverage |

## Relationship to Other Patterns

- **First step after:** Pain-Signal Eval Progression Gate when user complaints or reviewer uncertainty justify a minimum eval investment.
- **Feeds:** Production-Grounded Eval Sampling by establishing fixture and baseline conventions before production-sampled cases exist.
- **Feeds:** Eval Tier Stratification as the natural `fast` tier seed.
- **Supports:** PR-Gated Eval Enforcement by producing reviewer-ready baseline deltas for small agent changes.
- **Feeds:** Production Failure Regression Flywheel when a spot-check failure comes from a real escaped issue.
- **Complements:** Trace-reading curriculum and harness regression batteries already present in the repo.

## References

- `docs/analysis/2026-06-10-eval-maturity-phases/patterns.md:37` - extracted pattern definition.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:23` - Partial Coverage classification.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:32` - reconstructed KODA trace case evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:33` - practice, training, CI/CD, and comparison evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:34` - harness regression battery evidence.
- `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3876` - real trace case structure.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741` - regression battery cases.

## Better Implementation Cross-References

Do not create separate canonical docs for Metricized Agent Eval Contract or Canary Eval Rollout Gate from this analysis. The classification says the repo already has better implementations: Sprint Contracts, KODA rubrics, and baseline/candidate score comparison exceed the metricized contract pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:37`), while staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:108`).

---

*Created: 2026-06-10 | From: Eval Maturity pattern classification | Precedence: canonical*
