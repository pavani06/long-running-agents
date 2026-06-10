---
title: "Stable Harness Prompt During Context Reduction"
type: canonical
aliases: ["harness prompt", "stable prompt"]
tags: ["harness", "context-engineering"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[curriculum/01-nivel-1-fundamentals/03-basic-harness-patterns|Basic Harness Patterns Lesson]]", "[[curriculum/03-nivel-3-advanced-architecture/05-harness-evolution|Harness Evolution Lesson]]"]
sources: ["[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis|Context Management Analysis]]"]
---
# Stable Harness Prompt During Context Reduction

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-09-how-we-solved-context-management-in-agents/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Context reduction should remove or externalize bulky payload, old history, long tool outputs, and intermediate traces. It should not accidentally trim the harness instructions that define role, policy, tool contracts, safety boundaries, response format, or evaluation behavior.

If the system prompt is treated as just another chunk in a generic truncation algorithm, a long session can degrade not only memory but also the agent's operating contract. The agent may then fail because the harness was weakened, not because the user context was too large.

## Solution

Separate the stable harness prompt from reducible context payload. Context reduction may summarize, truncate, externalize, or retrieve history and tool bulk, but it must preserve the active harness prompt as a first-class input with its own budget and version.

The context builder should therefore assemble each model call from distinct blocks:

| Block | Reduction policy |
|---|---|
| Stable harness prompt | Preserve; version; evaluate separately |
| Head context | Preserve within policy-defined budget |
| Tail context | Preserve current state and latest result |
| Omitted middle | Store externally with catalog handles |
| Tool or trace bulk | Summarize, externalize, or delegate |
| Durable state | Inject from state stores according to freshness rules |

This pattern does not require a prompt to be immutable forever. It requires prompt changes to be deliberate, versioned, and evaluated separately from context compaction. The context-reduction path should not be the mechanism that changes harness instructions.

## Implementation in this repo

### What already exists

The repo already separates prompt ownership from context construction in several places:

- Owned Agent Control Loop treats Prompt as its own component and Context Builder as the separate component that assembles history, memory, tool results, and business state (`docs/canonical/owned-agent-control-loop.md:20`).
- That same canonical doc notes that the repo has a hand-authored system prompt and an excellent context builder, while prompt versioning and evals remain a gap (`docs/canonical/owned-agent-control-loop.md:87`).
- State Persistence describes the context window as including system prompt, recent messages, summaries, tools, and injected state (`curriculum/05-core-concepts/05-state-persistence.md:140`).
- State Persistence also says prompt, rubric, catalog, and schema need versions for replay (`curriculum/05-core-concepts/05-state-persistence.md:1414`).
- The source analysis lists preserving the system prompt during truncation as a tradeoff with explicit cost and benefit (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:203`).

### What is missing

The classification found no explicit rule named `Stable Harness Prompt During Context Reduction` or equivalent `preserve system prompt while truncating payload` outside this analysis output (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/classification.md:80`). Existing documents imply the separation, but they do not state it as a canonical context-reduction invariant.

The missing implementation details are:

1. A context-builder contract that marks the harness prompt as non-reducible by history compaction.
2. Prompt version metadata in replay, eval, and decision artifacts.
3. Tests or evals that fail when context reduction changes prompt instructions unintentionally.
4. Documentation of which blocks are eligible for truncation and which are stable inputs.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps the agent's operating contract stable during long sessions | Reduces fewer tokens than treating all prompt blocks as reducible |
| Makes context-reduction failures easier to diagnose | Requires explicit block boundaries in the context builder |
| Supports replay and eval by tying behavior to prompt versions | Requires prompt versioning discipline |
| Prevents compaction from silently changing safety, tool, or output rules | Prompt bloat becomes more visible and must be managed separately |

## Relationship to Other Patterns

- **Supports:** Head-Tail Context Truncation with Recoverable Middle, because the system prompt is part of the active anchor.
- **Supports:** N+1 Long-Session Evals, because evals should test context reduction under a stable harness contract.
- **Complements:** Owned Agent Control Loop, which separates Prompt and Context Builder as owned components.
- **Complements:** Serializable Pause/Resume State, because prompt version is part of replayable state.
- **Constrains:** Addressable Memory Catalog, because catalog previews and retrieval instructions should not replace harness instructions.

## References

- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:203` — tradeoff entry for preserving the system prompt during truncation.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/classification.md:68` — Partial Coverage classification and gap.
- `docs/canonical/owned-agent-control-loop.md:20` — prompt and context builder as separate components.
- `docs/canonical/owned-agent-control-loop.md:87` — prompt versioning and eval gap.
- `curriculum/05-core-concepts/05-state-persistence.md:140` — context window includes system prompt and other blocks.
- `curriculum/05-core-concepts/05-state-persistence.md:1414` — replay requires prompt, rubric, catalog, and schema versions.
- `curriculum/05-core-concepts/05-state-persistence.md:1834` — prompt version as a decision note for replay.

---

*Created: 2026-06-10 | From: Context Management pattern classification | Precedence: canonical*
