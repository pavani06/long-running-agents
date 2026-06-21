---
title: "Shared Design Concept Handoff"
type: canonical
tags: ["agentes-orquestracao", "context-engineering", "governanca"]
aliases: ["design concept handoff", "shared mental model handoff", "alignment handoff", "concept contract"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Matt Pocock Classification]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Agentic Patterns from Matt Pocock Workflow]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Classification: Matt Pocock Workflow Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Workflow Analysis]]"]
---
# Shared Design Concept Handoff

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

A written plan cannot carry all tacit product and architecture judgment by itself. When the alignment conversation ends and the PRD is written, something is lost: the human's tone, the agent's interpretation of tradeoffs, the reasoning behind deferred decisions, and the shared understanding of which assumptions are load-bearing.

Without a formal handoff of that shared concept, downstream artifacts (PRDs, issues, review criteria) operate from a shallow summary. The PRD becomes the only downstream contract, but it was never supposed to carry the full weight of alignment. Later agents and reviewers have only the prose artifact, not the shared understanding that produced it. This causes two failure modes: agents implement literally against PRD text without understanding intent, and reviewers check PRD compliance instead of checking whether the implementation preserves the design concept.

The asset that matters is the human-agent conversation after grilling, not any single written artifact. Without a handoff contract, that asset decays the moment the interview ends.

## Solution

Formalize the alignment conversation output as a Shared Design Concept: a durable handoff artifact that captures the agreed destination, unresolved tradeoffs, and a trust boundary for what downstream PRDs, issues, and reviews must preserve.

| Component | Role | Output |
|---|---|---|
| Human product judgment | The human's non-negotiable constraints, taste, ambition level, and strategic intent | Load-bearing decisions that downstream artifacts must not override |
| Agent interpretation | The agent's understanding of constraints, tradeoffs, domain context, and architectural boundaries | Explicit confirmation that the agent understood correctly |
| Decision trail | The ledger of answers from the alignment interview, including rationale | Provenance for every design choice in the shared concept |
| Assumption summary | A compiled list of all assumptions that the alignment revealed, marked as confirmed or deferred | Downstream artifacts know which assumptions are stable and which are still open |
| Downstream PRD and issue generator | A contract specifying how the shared concept maps to PRD sections, issue scope, and review criteria | Traceability from alignment to implementation |

The shared concept is the primary asset; the PRD is a downstream summarization. This reverses the common spec-driven instinct: the workflow trusts the PRD because alignment happened before it, not because the PRD is detailed enough to remove judgment.

Flow:

1. Use the alignment interview to expose assumptions and choices.
2. Summarize the agreed destination, unresolved tradeoffs, and load-bearing assumptions.
3. Feed the shared concept into PRD and issue generation as the primary input.
4. Use later review to check whether the implementation preserved the shared concept, not just PRD prose compliance.

## Implementation in this repo

### What already exists

The repo has adjacent mechanisms that support parts of the handoff:

- [[.opencode/skills/doc-coauthoring/SKILL.md|doc-coauthoring skill]]:28-42 collects meta-context, audience, impact, format, and constraints before drafting a document.
- [[.opencode/skills/issue-start/SKILL.md|issue-start skill]]:111-147 creates an execution brief with objective, success criteria, scope, out-of-scope, strategy, and validation.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:35-41 requires reconciling reviewer outputs, recording disagreements, accepted tradeoffs, and deferred ambition.
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:36-49 includes epistemic status, last verified timestamp, and labels to distinguish stale memory before acting.

### What is missing

The Partial Coverage gap is the absence of a formal handoff layer that treats the alignment conversation as a primary asset and preserves the shared concept as a durable contract for downstream PRD, issue generation, and review. The classification found no canonical doc, skill, or curriculum material that names Shared Design Concept Handoff or defines the handoff contract outside the analysis package [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:58-73.

Missing implementation details:

1. A handoff contract format that captures the shared concept as a structured artifact with explicit trust boundaries.
2. An assumption summary that distinguishes confirmed decisions from deferred ones, so downstream agents know what is safe to act on.
3. Integration between the interview ledger and the execution brief, so the issue-start skill reads alignment output.
4. A review checkpoint that checks implementation against the shared concept, not just the PRD text.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Makes the PRD useful because alignment happened before it | The richest alignment may remain partly conversational and hard to serialize |
| Keeps planning focused on mutual understanding instead of artifact completeness | It decays if later agents receive only a shallow summary from the PRD |
| Gives reviewers a basis for checking intent, not just prose compliance | It does not replace code reading, testing, or final behavior review |
| Creates a trust boundary that prevents downstream agents from silently overriding human decisions | Requires active maintenance to keep the handoff aligned with the current implementation state |

## Relationship to Other Patterns

- **Builds on:** [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]], which produces the decision trail and assumption surface that the handoff summarizes.
- **Feeds into:** [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]], because the handoff clarity determines whether issues are ready for AFK execution.
- **Complements:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]], because the shared concept is what the engineering and product reviewers evaluate against.
- **Precedes:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]], because the shared concept defines the destination that planning, execution, and verification must preserve.
- **Depends on:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] to track the freshness and provenance of shared concept assumptions across sessions.
- **Comes from:** [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Patterns]]:69-97 and its Partial Coverage classification in [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:58-73.

## References

- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|patterns]]:69-97 - extracted pattern definition with components and flow.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:58-73 - Partial Coverage classification and gap note.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|analysis]]:50-54 - shared design concept as the real planning asset.
- [[.opencode/skills/doc-coauthoring/SKILL.md|doc-coauthoring skill]]:28-42 - existing meta-context collection workflow.
- [[.opencode/skills/issue-start/SKILL.md|issue-start skill]]:111-147 - existing execution brief with scope and criteria.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:35-41 - existing reconciliation and deferred ambition recording.
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:36-49 - existing epistemic status tracking for stale memory detection.

---

*Created: 2026-06-11 | From: Matt Pocock workflow pattern classification | Precedence: canonical*
