---
title: "Grill-Me Alignment Interview"
type: canonical
tags: ["agentes-orquestracao", "context-engineering", "governanca"]
aliases: ["grill-me interview", "alignment interview", "one-question-at-a-time interview", "grilling session", "pre-planning interview"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Matt Pocock Classification]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Agentic Patterns from Matt Pocock Workflow]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Classification: Matt Pocock Workflow Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Workflow Analysis]]"]
---
# Grill-Me Alignment Interview

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Initial prompts hide assumptions and push agents into premature plans. When a human describes a goal in broad terms, the agent fills the gaps with its own defaults: architectural preferences, scope boundaries, product decisions, and domain knowledge it does not actually have. The result is a plan that looks complete but rests on unspoken assumptions that will surface as rework, architectural incoherence, or wrong scope during implementation.

The deeper problem is asymmetry: the human thinks the agent understood because the plan looks structured, while the agent thinks the human approved because the human did not object. Neither side sees the divergence until code hits reality.

## Solution

Run a structured alignment interview before any planning or coding begins. The agent interrogates the human aggressively, one question at a time, to expose hidden constraints, unresolved product calls, architectural assumptions, and domain unknowns.

| Component | Role | Output |
|---|---|---|
| Fresh context | Clear or isolate the planning session so the interview operates below the smart-zone ceiling | Clean reasoning environment for the interview |
| Interview skill | A short, focused skill or prompt that forces the agent into interviewer mode | Structured question flow instead of free-form chat |
| One-question-at-a-time loop | Ask one targeted question about an unresolved branch, wait for the answer, then proceed | No question overload; answers are precise because the question is narrow |
| Recommended-answer generator | For each question, offer concrete suggested answers the human can accept, edit, or reject | Human edits judgment instead of inventing every answer from scratch |
| Decision and deferral ledger | Record every answer and every explicitly deferred decision with rationale | Traceable decision trail that downstream artifacts inherit |

The loop runs until the major decision branches are closed or intentionally deferred. The interview does not need to resolve everything; it needs to make ambiguity explicit and ensure both parties share the same understanding of what is decided and what is still open.

Flow:

1. Clear or isolate the planning context so the interview starts fresh.
2. Ask one targeted question about an unresolved branch (scope, architecture, domain, product, constraints).
3. Offer recommended answers so the human can edit judgment rather than invent from scratch.
4. Record the answer or deferral in the decision ledger.
5. Repeat until the major decision branches are closed or explicitly deferred.

## Implementation in this repo

### What already exists

The repo has adjacent mechanisms that partially cover alignment interviewing:

- [[.opencode/skills/doc-coauthoring/SKILL|doc-coauthoring skill]]:20-23 defines context gathering, refinement, and reader testing for documents.
- [[.opencode/skills/doc-coauthoring/SKILL|doc-coauthoring skill]]:88-98 requires generating 5-10 clarification questions and exiting when those questions demonstrate understanding.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 defines independent engineering and product/destination reviewers with recorded decisions and deferred ambitions.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:32-35 includes priority synthesis and feedback writeback, which would consume the decision ledger.

### What is missing

The Partial Coverage gap is the absence of a structured one-question-at-a-time interview workflow with recommended answers and a formal decision/deferral ledger. The classification found no skill, canonical doc, or curriculum material that names Grill-Me Alignment Interview or defines the interview loop mechanics outside the analysis package [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:41-57.

Missing implementation details:

1. A dedicated interview skill or canonical prompt that enforces one-question-at-a-time with recommended answers.
2. A decision ledger format that records answers, deferrals, rationale, and provenance for downstream consumption.
3. A trigger policy that activates the interview for ambiguous or high-impact work while skipping it for small, obvious changes.
4. Integration points where the interview ledger feeds into PRD generation, issue decomposition, and review criteria.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Converts hidden ambiguity into explicit choices before implementation | Consumes meaningful human attention before any code is written |
| Lets the human edit suggested judgments instead of inventing every answer from scratch | Can feel excessive for small or already-obvious changes |
| Reduces rework caused by discovering major decisions during coding | Works poorly when the human cannot supply the needed product or domain judgment |
| Creates a durable decision trail that downstream agents and reviewers can trust | The richest alignment may remain partly conversational and hard to serialize |

## Relationship to Other Patterns

- **Feeds into:** [[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]], which summarizes the interview output into a shared human-agent mental model that downstream PRDs and issues preserve.
- **Connects to:** [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]], because the interview output determines whether tasks are clear enough for AFK execution or still need human judgment.
- **Complements:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]], which provides a review split for plans that emerge from the interview.
- **Precedes:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]], because the interview must close ambiguity before planning, executing, and verifying begin.
- **Depends on:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] for feedback writeback of interview outcomes into persistent memory.
- **Comes from:** [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Patterns]]:38-67 and its Partial Coverage classification in [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:41-57.

## References

- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|patterns]]:38-67 - extracted pattern definition with components and flow.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:41-57 - Partial Coverage classification and gap note.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|analysis]]:52-54 - shared design concept before plans framing.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|analysis]]:78-82 - grill-me skill pattern description.
- [[.opencode/skills/doc-coauthoring/SKILL|doc-coauthoring skill]]:20-23 - existing context gathering workflow.
- [[.opencode/skills/doc-coauthoring/SKILL|doc-coauthoring skill]]:88-98 - existing clarification question generation.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 - existing dual-rubric review with deferred decisions.

---

*Created: 2026-06-11 | From: Matt Pocock workflow pattern classification | Precedence: canonical*
