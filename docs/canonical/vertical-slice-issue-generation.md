---
title: "Vertical-Slice Issue Generation"
type: canonical
tags: ["agentes-orquestracao", "governanca"]
aliases: ["vertical slice issues", "layer-spanning issues", "behavior-path issues", "vertical slice generation"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/classification|Matt Pocock Classification]]", "[[.opencode/skills/refine-issue/SKILL|refine-issue skill]]", "[[.opencode/skills/issue-workflow/SKILL|issue-workflow skill]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/patterns|Matt Pocock Workflow Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/classification|Matt Pocock Classification]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/analysis|Matt Pocock Workflow Analysis]]"]
---
# Vertical-Slice Issue Generation

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Agents tend to implement horizontally: all database changes, then all API changes, then all UI changes, one layer at a time. This delays integration feedback and makes AFK progress look larger than it truly is. The source analysis describes the failure mode as building all infrastructure layers before a single behavior path works, leaving the agent with invisible integration failures that surface only when layers finally meet ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/analysis|Matt Pocock Analysis]]:94-95).

The repository already decomposes issues into executable sub-issues, but the decomposition is organized by file or file pair rather than by observable behavior path. Each sub-issue targets a single file or tightly-coupled pair, defines its dependencies, and gates progress on acceptance criteria and a verification step. This produces clean work items with clear dependencies but can miss the cross-layer integration that makes a slice work end-to-end ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/classification|classification]]:113-121).

A batch of five file-level sub-issues that all complete does not guarantee that the database change, the API handler, and the UI component all agree on the same behavior. The feedback cycle that catches this gap arrives late: at the Verification Gate, at PR review, or during manual QA.

## Solution

Generate issues as vertical slices that cross layers and produce observable behavior. Each slice covers the full path from entry point to persistence to user-visible outcome.

A vertical slice walks one behavior path through all necessary layers:

```
Request/Input → Handler/Controller → Business Logic → Persistence → Response/Output
     ↑                                                                    |
     +--------------------- Test and Verify ←----------------------------+
```

The mechanics differ from file-level decomposition in three ways:

1. **Start from behavior, not from architecture.** Instead of "create the User model, then the UserService, then the UserController," generate one issue: "a new user can sign up with email and password." That slice touches model, service, controller, route, validation, and tests in a single bounded task.

2. **Acceptance criteria describe the path, not the file.** The criteria for a vertical slice are behavioral: "submitting a valid email and matching password returns 201 with a session token; submitting a duplicate email returns 409 with conflict reason; submitting a weak password returns 422 with password rules." These pass only when all layers work together.

3. **Dependencies are behavior-blockers, not file-blockers.** A slice that lets a user view orders depends on the slice that lets a user place orders, not on the file that defines the OrderRepository interface. Dependencies encode the integration graph, not the file graph.

The pattern from the source specifies this as the output of a Destination PRD: convert destination goals into observable behavior paths, slice each path across the layers needed to make one behavior work, attach acceptance checks and blockers, and keep each slice small enough for one AFK implementation session ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/patterns|patterns]]:185-188).

Boundary rules for slice sizing:

- Too small = one function or one file per slice. This is horizontal decomposition.
- Too large = an entire feature narrative in one slice. This defeats parallelism and creates fragile multi-session tasks.
- Right size = one small behavior path that a single agent can implement, test, and verify in one session, and that produces observable integration feedback.

## Implementation in this repo

### What already exists

- [[.opencode/skills/refine-issue/SKILL|refine-issue skill]] lines 8-21 decomposes an issue into focused sub-issues with dependencies, acceptance criteria, and a Verification Gate. The sub-issue template includes target file, change type, action guidance, verify command, acceptance criteria, blocked-by, and enables relationships.
- [[.opencode/skills/refine-issue/SKILL|refine-issue skill]] lines 46-70 defines sub-issues by file or tightly-coupled pair. The dependency model orders foundation work first (types, interfaces, schemas), flows dependencies down (A imports from B implies B first), pairs tests with implementation, and always places a Verification Gate last.
- [[.opencode/skills/refine-issue/SKILL|refine-issue skill]] lines 80-86 requires a final Verification Gate sub-issue blocked by all implementation sub-issues, which validates all acceptance criteria before the parent issue can complete.
- [[.opencode/skills/issue-workflow/SKILL|issue-workflow skill]] lines 59-82 creates sub-issues with acceptance criteria, progress log, and BLOCKED BY blocks for dependency modeling.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] separates planning, execution, and verification into distinct phases with checkpoints. Vertical slices align with this: each slice is a plan-execute-verify unit whose phases produce observable behavior.

### What is missing from the pattern

The Partial Coverage gap is that issue generation is organized by file/pair rather than by layer-spanning behavior path. The classification found no guidance for vertical-slice generation in docs, curriculum, or skills outside this analysis package ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/classification|classification]]:120-124).

Missing pieces:

1. A vertical-slice heuristic in the refine-issue skill that starts from behavior paths extracted from the Destination PRD rather than from architectural layers.
2. A template for vertical-slice acceptance criteria that spans the entry point, business logic, persistence, and user-visible outcome of a single behavior.
3. A dependency graph orientation that models behavior-blockers (a slice that creates orders blocks the slice that lists orders) rather than file-blockers (the Repository file blocks the Service file).
4. A rule for when file-level decomposition is acceptable (infrastructure-only tasks, shared utilities) and when vertical slices are required (feature work, user-visible behavior changes).
5. A connection between vertical slices and the Agent Kanban so that slices with clear behavior-blocker graphs enable safe parallel agent work.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Integration feedback arrives early, inside each slice, instead of at the Verification Gate or PR review | Requires careful issue design before implementation can begin |
| Makes parallel agent work safer because slices test independent behavior paths | Some infrastructure work does not split cleanly into user-visible behavior paths |
| Gives reviewers a real behavior path to trace instead of disconnected layer changes | Slices that are too small create coordination overhead and fragmented intent |
| Aligns acceptance criteria with user-visible outcomes rather than file completeness | Misclassifying horizontal dependencies as behavior-blockers creates false blocking chains |

## Relationship to Other Patterns

- **Feeds:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] because each vertical slice is a self-contained plan-execute-verify unit with its own checkpoint at the behavior boundary.
- **Consumes:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] because the Destination PRD and behavior paths should pass both engineering review (can this slice be built?) and product review (is this the right behavior to build first?).
- **Enables:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] because each slice produces testable behavior that a separate evaluator can verify against the acceptance criteria.
- **Integrates with:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] because vertical slices populate the ready queue with independently grabbable, cross-layer work items.
- **Depends on:** [[.opencode/skills/refine-issue/SKILL|refine-issue skill]] for the current decomposition workflow and dependency management that vertical-slice generation extends.
- **Comes from:** [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/patterns|Matt Pocock Patterns]]:160-188 and its Partial Coverage classification in [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/classification|classification]]:108-124.

## References

- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/patterns|patterns]]:160-188 - extracted pattern definition with behavior paths, layer-spanning tasks, acceptance checks, and blocker graph.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/classification|classification]]:108-124 - Partial Coverage classification and gap analysis for vertical-slice mechanics.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/analysis|analysis]]:92-98 - vertical-slice issue generation as integration-feedback graph.
- [[.opencode/skills/refine-issue/SKILL|refine-issue skill]]:8-86 - existing decomposition workflow, sub-issue template, dependency model, and Verification Gate.
- [[.opencode/skills/issue-workflow/SKILL|issue-workflow skill]]:59-82 - existing sub-issue creation with acceptance criteria and BLOCKED BY.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:29-73 - three-phase decomposition with plan, execute, verify gates.

---

*Created: 2026-06-11 | From: Matt Pocock workflow pattern classification | Precedence: canonical*
