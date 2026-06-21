---
title: "Human/AFK Task Routing Gate"
type: canonical
tags: ["agentes-orquestracao", "governanca"]
aliases: ["AFK routing", "human-in-loop gate", "task classifier", "AFK-ready gate", "human/agent routing", "routing gate"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Matt Pocock Classification]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Agentic Patterns from Matt Pocock Workflow]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Classification: Matt Pocock Workflow Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Workflow Analysis]]"]
---
# Human/AFK Task Routing Gate

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Treating every task as autonomous implementation delegates judgment-heavy decisions to agents. When the backlog is a flat list of issues without classification, agents can pick up tasks that require product judgment, architectural design, ambiguity resolution, or final QA -- work that agents cannot do reliably without human taste and accountability.

The failure mode is not that agents produce nothing; it is that they produce plausible-looking output that passes mechanical checks while missing product intent, misinterpreting unresolved requirements, or making irreversible architecture decisions without human oversight. The result is rework, design drift, and eroding trust in the agent system.

The model is not "automate everything." It is "move implementation into bounded queues while keeping judgment at the boundaries." Without an explicit routing gate, the boundary between these two categories is left to whoever picks up the task, and agents are not equipped to make that classification themselves.

## Solution

Install a routing gate between the backlog and the execution queue. The gate classifies every task as AFK-ready (safe for autonomous agent execution) or human-in-loop (requires human judgment before, during, or after execution). The classification is based on four dimensions:

| Dimension | AFK-Ready condition | Human-in-Loop trigger |
|---|---|---|
| Ambiguity | Scope, acceptance criteria, and module boundaries are explicit and unambiguous | Requirements are open to interpretation, product decisions are unresolved, or scope is fuzzy |
| Architecture | The change fits within existing module boundaries with a clear public interface | The change crosses module boundaries, introduces new abstractions, or has system-wide blast radius |
| Feedback loop readiness | Tests, types, linters, runtime checks, and acceptance criteria exist and can gate the change | Feedback loops are incomplete, tests must be designed, or verification requires human taste |
| Product judgment | The change implements a decided feature with clear non-functional requirements | The change involves user-facing design, strategic product calls, or tradeoffs that affect roadmap |

Flow:

1. Inspect each task for ambiguity, dependencies, feedback, and module boundaries.
2. Mark bounded implementation tasks as AFK-ready when all four dimensions are satisfied.
3. Mark planning, ambiguity resolution, architectural decisions, prototype interpretation, QA, and final review tasks as human-in-loop.
4. Escalate or block tasks whose required judgment is not yet resolved by either party.

| Component | Role | Output |
|---|---|---|
| Task classifier | Evaluates each backlog item against the four routing dimensions | AFK-ready or human-in-loop label |
| Ambiguity detector | Checks whether scope, acceptance criteria, and boundaries are explicit | Ambiguity score or explicit unresolved items list |
| Feedback-loop readiness check | Verifies that tests, types, linters, and runtime checks exist for the change surface | Ready, partial, or missing feedback assessment |
| Human escalation path | Defines who resolves each blocked dimension and how the task returns to the queue | Owner assignment for each unresolved judgment point |
| AFK queue | A visible, ordered queue of tasks that are safe for autonomous agent execution | Pullable work for agent sessions |

## Implementation in this repo

### What already exists

The repo has operational routing mechanisms that partially cover task classification:

- [[.opencode/skills/orchestrator/SKILL.md|orchestrator skill]]:51-63 defines priority-based next-task suggestion, skipping tasks with agent:working, blocked status, and open blockers.
- [[.opencode/skills/issue-start/SKILL.md|issue-start skill]]:38-45 prevents stealing work already claimed by agent:working or an assignee.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:32-35 includes priority synthesis, execution routing, and feedback writeback.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:37-41 reserves extra review for high-impact roadmaps, ambiguous bets, and major agent-system changes.
- [[.opencode/skills/orchestrator/SKILL.md|orchestrator skill]]:165-180 documents blocker handling and return to queue for human intervention.

### What is missing

The Partial Coverage gap is the absence of an explicit classification matrix that scores tasks on ambiguity, architecture, feedback-loop readiness, and product judgment to produce an AFK-ready or human-in-loop routing decision. The classification found no skill, canonical doc, or curriculum material that defines Human/AFK Task Routing Gate or the four-dimensional classifier outside the analysis package [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:91-107.

Missing implementation details:

1. A routing matrix or checklist that classifies every backlog item before it enters the ready queue.
2. An ambiguity scoring mechanism that produces explicit unresolved items rather than a binary yes/no.
3. A feedback-loop readiness assessment tied to the change surface (which gates exist, which are missing).
4. Integration with [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] output, since many ambiguity dimensions should be resolved during alignment.
5. A human escalation path that assigns ownership for unresolved judgment to a specific person or role.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps bounded execution autonomous while preserving human taste and accountability at the boundaries | Requires active backlog curation and classification discipline |
| Prevents agents from continuing through unresolved product or architecture calls | Misclassification can send ambiguous work into unsafe automation |
| Makes queue ownership explicit: agents know what is safe to pull, humans know what needs their attention | Human availability becomes a throughput constraint for judgment-heavy work |
| Reduces rework by catching ambiguity before implementation effort is spent | The classification gate itself adds latency before any work begins |

## Relationship to Other Patterns

- **Builds on:** [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]], because the interview should resolve the ambiguity dimension before tasks enter the routing gate.
- **Consumes from:** [[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]], because the handoff clarity determines whether tasks are ready for AFK execution.
- **Complements:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]], which provides the human judgment for roadmap, architecture, and product decisions that the routing gate classifies as human-in-loop.
- **Precedes:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]], because AFK-ready tasks are the only ones that should enter the execute phase without human presence.
- **Connects to:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] and [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]], which provide the feedback loops that make AFK execution safe.
- **Depends on:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] for priority synthesis and execution routing that consume the AFK/human classification.
- **Comes from:** [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Patterns]]:130-158 and its Partial Coverage classification in [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:91-107.

## References

- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|patterns]]:130-158 - extracted pattern definition with components and flow.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:91-107 - Partial Coverage classification and gap note.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|analysis]]:62-66 - human-in-loop vs AFK classification model.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|analysis]]:153-153 - planning remains human-in-loop operational lesson.
- [[.opencode/skills/orchestrator/SKILL.md|orchestrator skill]]:51-63 - existing priority-based next-task suggestion.
- [[.opencode/skills/orchestrator/SKILL.md|orchestrator skill]]:165-180 - existing blocker handling and human escalation.
- [[.opencode/skills/issue-start/SKILL.md|issue-start skill]]:38-45 - existing work-claiming and ownership gates.

---

*Created: 2026-06-11 | From: Matt Pocock workflow pattern classification | Precedence: canonical*
