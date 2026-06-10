# Head-Tail Context Truncation with Recoverable Middle

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-09-how-we-solved-context-management-in-agents/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Long-running agents often need to reduce an oversized conversation, trace, or tool-call payload without losing the original task anchor, the latest state, or the ability to answer follow-up questions about omitted details.

Naive truncation keeps only one side of the payload. Keeping only the beginning preserves setup but drops the latest conversational state. Keeping only the end preserves recency but drops the original goal, constraints, and definitions. Opaque summarization can compress more aggressively, but it can also remove exact details without an auditable recovery path.

## Solution

Preserve a bounded active context made of the stable harness prompt, the head, the tail, and the latest result. Move the middle into external memory with retrieval handles so it can be fetched back when a follow-up depends on omitted detail.

```
large_context  = [head][middle][tail]
active_context = [system_prompt][head][tail][latest_result]
memory_store   = [middle + older messages + long tool calls]
retrieval      = IDs + location + preview
```

The head carries durable setup: the user's initial goal, task frame, definitions, constraints, or trace root. The tail carries current state: recent turns, latest tool results, unresolved decisions, and the immediate user request. The middle is not discarded. It is stored as exact recoverable content and exposed through an addressable catalog or retrieval tool.

The pattern is not a universal `first 100 / last 100` rule. The cut points should be chosen by payload structure and context budget. The invariant is stronger than the heuristic: the active context keeps both anchors, and omitted content remains recoverable rather than being silently lost.

## Implementation in this repo

### What already exists

The repo already teaches the broader context-management ingredients that this pattern needs:

- Level 1 windowing asks learners to keep recent messages, compress old history, preserve critical metadata, and return an optimized context (`curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:13`).
- The harness checklist requires an explicit context policy, a system-prompt budget, structured old-history summaries, durable critical state, and explainability for context blocks (`curriculum/07-implementation-guides/03-harness-design-checklist.md:273`).
- Server-side compaction keeps recent context complete, stores older ranges at different summary densities, and injects external state (`curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:327`).
- The source analysis defines smart truncation as `[system_prompt][head][tail][latest_result]` plus a recoverable memory store (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:65`).

### What is missing

The classification found no explicit canonical or curriculum pattern for preserving both head and tail while making the omitted middle exactly recoverable by handle (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/classification.md:16`). Existing material covers sliding windows, summaries, retrieval, state, and compaction, but it does not name this as a specific compaction variant.

The missing implementation details are:

1. A policy for selecting head, tail, and middle boundaries.
2. A requirement that the middle be stored as exact recoverable content, not only summarized.
3. Retrieval handles that let the agent request omitted spans back into context.
4. Evals that prove follow-up behavior survives after truncation.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Preserves the original task anchor and the latest state in the active context | Requires deliberate boundary selection rather than blind truncation |
| Keeps active context bounded without discarding omitted content | Requires storage for middle content and retrieval metadata |
| More auditable than lossy summarization because exact middle content can be recovered | Can still preserve the wrong spans if the payload structure changes |
| Improves follow-up handling after long sessions | Requires N+1 or late-session evals to prove the policy works |

## Relationship to Other Patterns

- **Depends on:** Addressable Memory Catalog, because the omitted middle needs stable handles, locations, and previews.
- **Depends on:** Stable Harness Prompt During Context Reduction, because the system prompt is an anchor, not truncation bulk.
- **Validated by:** N+1 Long-Session Evals and Late-Failure Regression Suite, which catch over-truncation and late-session forgetting.
- **Complements:** Memory Tier Separation, because recoverable omitted middle is in-session memory, not necessarily long-term user memory.
- **Complements:** Context-Scoped Sub-Agent Delegation, because payloads too large for local compaction can be moved to isolated agent contexts.

## References

- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:65` — smart truncation mechanism.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/patterns.md:14` — extracted reusable pattern.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/classification.md:5` — Partial Coverage classification and gap.
- `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:13` — existing windowing exercise.
- `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:327` — existing server-side compaction coverage.
- `curriculum/07-implementation-guides/03-harness-design-checklist.md:273` — context policy checklist.

---

*Created: 2026-06-10 | From: Context Management pattern classification | Precedence: canonical*
