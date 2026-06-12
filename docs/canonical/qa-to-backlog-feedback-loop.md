---
title: "QA-to-Backlog Feedback Loop"
type: canonical
tags: ["agentes-orquestracao", "governanca", "evals"]
aliases: ["QA feedback loop", "review-to-backlog", "QA intake lane", "feedback-driven backlog"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Matt Pocock Classification]]", "[[.opencode/skills/issue-workflow/SKILL|issue-workflow skill]]", "[[.opencode/skills/orchestrator/SKILL|orchestrator skill]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Workflow Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Matt Pocock Classification]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Workflow Analysis]]"]
---
# QA-to-Backlog Feedback Loop

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

QA and review findings are often treated as terminal events: find bugs, report them, fix them, close the review. The findings evaporate into informal memory, issue comments, or chat messages after the fix is applied. The workflow closes, and the system loses the discovered knowledge. The source analysis captures this as a recurring failure pattern: treating QA as a pass/fail gate instead of an input to the next bounded agent tasks ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Analysis]]:155-156).

The repository has strong mechanisms for production failures (the Production Failure Regression Flywheel converts incidents into durable eval cases), and the Closed-Loop Agent OS includes feedback writeback as a named surface. But the pipeline from QA observations and review findings to backlog issues that agents can claim is informal. A reviewer who discovers that error messages leak internal state, that the dark-mode toggle shifts layout, or that the order-confirmation email fires twice can comment on the PR and block merge. But after the fix, there is no structured path to convert that finding into a regression check, a backlog item with severity and priority, or a durable slice that prevents recurrence.

The gap is not that findings are ignored; it is that findings leave no structured trace in the agent's operating surface. They become comments on closed PRs and issues, not items on the board ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:270-273).

## Solution

Formalize QA and review findings as backlog inputs that produce vertical-slice issues or regression cases. The loop converts observations into actionable work rather than closing the cycle with a merge.

The pattern from the source defines the mechanics: capture QA and review findings as structured observations, triage each finding for severity, blocker status, and ownership, convert actionable findings into vertical-slice issues or regression cases, and return the new work to the Kanban board instead of leaving it as informal memory ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|patterns]]:469-472).

A finding flows through four stages:

1. **Capture.** Every QA observation or reviewer finding is captured as a structured record with: what was observed, where (behavior, surface, or component), severity (cosmetic, functional, data-loss, security), expected vs actual outcome, and reproduction context. The format is lightweight enough to not slow down review but structured enough to feed triage.

2. **Triage.** Each finding receives a classification: blocker (must fix before merge), regression-risk (should produce a regression check), backlog (actionable but not blocking), or deferred (not actionable or belongs in a separate initiative). Deferred findings are explicitly recorded with a reason so they do not silently disappear.

3. **Convert.** Actionable findings become one of two outputs. For findings that represent new behavior gaps, they become vertical-slice issues with acceptance criteria that encode the expected corrected behavior. For findings that represent regressions (this worked before, this should not happen again), they become regression check issues that create or update eval cases, add fixture data, and link back to the finding's origin.

4. **Return to board.** The new issues enter the Agent Kanban with severity labels, QA-intake metadata (source PR, finding ID, reviewer), and blocker relationships. Agents claim them through the normal ready-queue flow. The original PR that triggered the finding closes independently; the finding lives on as durable backlog work.

The loop closes when a finding produces a resolved issue and the resolution survives review. It does not close when the original PR merges.

## Implementation in this repo

### What already exists

- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] lines 28-40 transforms production failures into durable regression cases with trace, labels, tier assignment, deduplication, and links to incident/PR. This is the closest existing mechanism to a feedback loop, but it is scoped to production failures, not QA/review findings.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] lines 32-35 includes feedback writeback as one of four operating system surfaces, alongside state intake, priority synthesis, and execution routing.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] lines 43-45 requires ownership, validation, and memory update before writeback becomes authoritative.
- [[.opencode/skills/issue-workflow/SKILL|issue-workflow skill]] lines 18-25 mandates updating acceptance criteria and commenting progress, decisions, and blockers during work.
- [[.opencode/skills/orchestrator/SKILL|orchestrator skill]] lines 165-180 handles blocker triage and manual intervention when agents cannot resolve blocking findings after three attempts.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] defines merge-policy gates for eval-sensitive changes, creating a natural point where blocking findings can be injected into the backlog.

### What is missing from the pattern

The Partial Coverage gap is the structured conversion from QA/review findings to backlog items. The classification found that the repo has the flywheel (production failures), writeback surface (Closed-Loop OS), and blocker handling (orchestrator), but no formal intake lane, severity triage, or regression-issue generation from QA/review findings ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:272-273).

Missing pieces:

1. A finding capture format that is lightweight enough for review flow but structured enough for triage.
2. A triage rubric that separates blocker (merge-gate), regression-risk (eval case), backlog (vertical slice), and deferred (out of scope) findings.
3. A severity taxonomy for QA findings: cosmetic, functional, data-loss, and security, each with expected response time and escalation path.
4. A conversion path that maps regression-risk findings into eval cases using the Production Failure Regression Flywheel, and maps backlog findings into vertical-slice issues.
5. An intake lane in the Agent Kanban that surfaces findings as issues with QA-source metadata, making them visible and claimable by agents rather than buried in PR comments.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Turns review and QA into a closed improvement loop instead of a terminal gate | Can expand scope if findings are not triaged with severity and priority |
| Keeps agent work adaptive as real behavior is observed | Low-quality QA creates noisy or duplicate backlog items |
| Prevents discovered defects from remaining as informal memory in closed PRs | Requires human judgment to distinguish defects from new feature ideas |
| Creates durable regression protection from findings that would otherwise recur | Adds triage and issue-creation overhead after each review |

## Relationship to Other Patterns

- **Feeds:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] because QA findings become priority-synthesis inputs and execution-routing targets through the backlog.
- **Uses:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] when regression-risk findings should become durable eval cases with fixtures, labels, and tier assignment.
- **Consumes:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] outputs because the evaluator produces findings that the feedback loop converts into issues.
- **Depends on:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] because the Verify phase is the natural capture point for behavioral findings before they enter the triage pipeline.
- **Integrates with:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] because PR gates produce the findings that the loop routes into the backlog.
- **Comes from:** [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Patterns]]:443-472 and its Partial Coverage classification in [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:256-274.

## References

- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|patterns]]:443-472 - extracted pattern definition with QA observation, reviewer finding, severity/blocker metadata, regression check, and Kanban intake lane.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:256-274 - Partial Coverage classification and gap analysis for QA-to-Backlog feedback loop.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|analysis]]:155-156 - QA creates more work rather than closing the loop permanently.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40 - existing regression case creation from production failures.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:32-45 - existing feedback writeback surface and minimum operating contract.
- [[.opencode/skills/issue-workflow/SKILL|issue-workflow skill]]:18-25 - existing acceptance criteria and progress/blocker commenting.
- [[.opencode/skills/orchestrator/SKILL|orchestrator skill]]:165-180 - existing blocker handling and manual intervention comment.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:28-53 - existing merge-gate policy for eval-sensitive changes.

---

*Created: 2026-06-11 | From: Matt Pocock workflow pattern classification | Precedence: canonical*
