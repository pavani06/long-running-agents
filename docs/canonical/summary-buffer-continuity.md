---
title: "Summary Buffer Continuity"
type: canonical
aliases: ["buffer de resumo continuo", "rolling summary", "conversation summarization", "resumo de sessao"]
tags: ["context-engineering", "agentes-orquestracao"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Classification]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Classification]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
---

# Summary Buffer Continuity

**Type:** canonical
**Status:** active
**Source:** [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]] and [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]:14-21

---

## Problem

Older conversation often contains critical state, but the full transcript cannot remain verbatim in every model call forever. The token-budgeting source names this directly: Summary Buffer solves the case where older conversation may contain critical state but cannot remain verbatim, by periodically summarizing old or full history into a compact buffer included with recent messages ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:79-85).

The original lesson gives the concrete mechanism: an 80K-token two-hour history is periodically summarized into a 2K-token paragraph that preserves allergy, budget, brand preference, and delivery information ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:250-260). It also shows the expected trigger shape: summarize every 50 messages and focus on critical customer information ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:262-274).

Existing canonical docs cover adjacent pieces but not the lifecycle. [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] makes summarization and compression explicit context-builder interventions ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:60-63). [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] allows reducible history and tool bulk to be summarized, truncated, externalized, or retrieved while preserving the harness prompt ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:28-41). [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] warns that opaque summarization can remove exact details without auditable recovery ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:24) and requires omitted middle content to remain exactly recoverable rather than only summarized ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:59).

The gap is therefore not "can the system summarize?" The gap is a rolling summary-buffer contract with freshness metadata, update rules, target budget, quality checks, and portability as a handoff artifact. The classification records this as Partial Coverage and NOT_FOUND for a canonical summary-buffer lifecycle ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Classification]]:64-72).

## Solution

Maintain a rolling summary buffer as a first-class context block. It is a compact, freshness-stamped summary of older conversation spans that no longer fit verbatim, included alongside the stable harness prompt, durable facts, recoverable memory handles, and recent tail.

The buffer is not a replacement for durable state or exact recovery. Durable facts that drive decisions should live in structured state, and summarized spans should remain recoverable through an addressable memory catalog when exact wording, evidence, or source details matter. The summary buffer exists to preserve broad continuity and reduce active token load between those two layers.

```
+----------------------+      +----------------------+
| older transcript     |----->| summary refresh job  |
| span no longer fits  |      | budget + guardrails  |
+----------------------+      +----------+-----------+
                                      |
                                      v
+----------------------+      +----------------------+
| durable facts        |----->| rolling summary      |
| constraints/state    |      | buffer + freshness   |
+----------------------+      +----------+-----------+
                                      |
                                      v
+----------------------+      +----------------------+
| recent tail          |----->| next active context  |
| latest turns/results |      | prompt assembly      |
+----------------------+      +----------------------+
                                      |
                                      v
                              +----------------------+
                              | handoff payload      |
                              | if session/agent     |
                              | boundary is crossed  |
                              +----------------------+
```

## Contract

The summary buffer should be explicit enough for the context builder, evaluator, and handoff receiver to inspect it without reverse-engineering a prose paragraph.

Minimum fields:

| Field | Purpose |
|---|---|
| `buffer_id` | Stable identifier for audit, eval, and handoff |
| `source_span` | Message range, turn range, timestamps, or catalog IDs folded into the buffer |
| `summary_text` | Compact continuity summary included in active context |
| `target_tokens` | Maximum intended size for the buffer block |
| `fresh_at` | Last turn, timestamp, or event included in the summary |
| `stale_after` | Turn count, elapsed time, token phase, or event condition that requires refresh |
| `durable_fact_refs` | Structured facts that must not be blurred by the summary |
| `recovery_refs` | Addressable memory IDs for exact source recovery |
| `open_threads` | Unresolved decisions, commitments, risks, or user questions |
| `quality_status` | Pass, needs_review, failed, or superseded after quality checks |

The buffer appears in the active context only after the stable harness prompt and durable facts. [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] already defines those blocks as distinct context-builder inputs and lists durable state separately from reducible history ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:30-40). The summary buffer should therefore be treated as reducible old-history context, not as policy, tool contract, or source of truth for durable facts.

## Lifecycle and Update Rules

1. **Select source span.** Choose older turns that exceed the active-history budget or have crossed the summarization threshold. The original lesson uses a periodic trigger every 50 messages as a simple example ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:262-274), while the production scenario triggers Summary Buffer in the orange phase and keeps only the latest 10 messages verbatim ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:545-553).
2. **Protect durable facts first.** Extract or refresh structured facts before summarization. Token Budgeting frames critical customer facts as separate context such as allergies, budget, and purchase history ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:191-217), and [[docs/canonical/external-state-persistence|External State Persistence]] separates durable facts from greetings, filler, and ephemeral scratchpads ([[docs/canonical/external-state-persistence|External State Persistence]]:59-65).
3. **Summarize under a target budget.** Produce a compact old-history summary with explicit `target_tokens`. The extracted pattern requires target token budget and freshness metadata as inputs and emits a compact buffer included with recent messages ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]:125-137).
4. **Merge, do not append blindly.** Fold the new span into the existing buffer by replacing stale or superseded claims, preserving open threads, and recording the new `source_span`. The pattern identifies summary drift as a limitation when updates are not anchored to source state ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]:142-145).
5. **Attach freshness metadata.** Set `fresh_at`, `stale_after`, and `quality_status` so the context builder can decide whether to reuse, refresh, or exclude the buffer. The classification gap specifically calls out missing freshness metadata and update rules ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Classification]]:64-70).
6. **Preserve exact recovery.** Store or reference the source span through [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] handles. The catalog provides `id`, `kind`, `location`, `preview`, `scope`, and `fetch` fields for exact omitted-content recovery ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
7. **Include beside recent tail.** Assemble the next context as stable prompt, durable facts, summary buffer, recent messages, latest result, and retrieval handles. This matches the hybrid context-stack idea in the source, which combines critical context, summary buffer, and recent window ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:375-415).

## Quality Checks

Run quality checks before a summary buffer becomes the active continuity layer.

| Check | Pass condition | Evidence anchor |
|---|---|---|
| Durable fact preservation | Constraints, preferences, commitments, and task state are either unchanged in structured state or explicitly referenced | [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:124-127 |
| Source anchoring | Every buffer has `source_span` and `recovery_refs` for exact recovery | [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:56-61 |
| Freshness | `fresh_at` covers the summarized span and `stale_after` tells the context builder when to refresh | [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Classification]]:64-70 |
| Budget fit | `summary_text` stays within `target_tokens` and leaves room for recent tail plus response buffer | [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:50-61 |
| Continuity behavior | N+1 follow-up still resolves old references after the buffer replaces old verbatim turns | [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]:20-40 |
| Drift control | Refresh replaces stale claims rather than accumulating contradictions or vague paraphrases | [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]:142-145 |

## Portability and Handoff

A summary buffer is portable only when it carries enough metadata for the next session, sub-agent, or operator to know what it summarizes and how to recover exact details. The pattern extraction names portability as a benefit: the buffer creates a handoff artifact for new sessions or sub-agents ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]:138-145). Budget-aware session transition also depends on preserving enough state to avoid user-visible discontinuity when the active context budget is reset ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:171-179).

Portable handoff payload:

| Block | Required content |
|---|---|
| `current_objective` | What the agent or user is trying to accomplish now |
| `summary_buffer` | The latest valid buffer with `buffer_id`, `fresh_at`, and `quality_status` |
| `durable_facts` | Structured facts loaded from external state, not inferred only from the summary |
| `recent_tail` | Latest turns or results that have not yet been folded into the buffer |
| `recovery_refs` | Catalog IDs for exact old-history recovery |
| `open_threads` | Decisions, commitments, questions, and risks still active |
| `budget_state` | Why handoff or compaction happened, when known |

## Tradeoffs

| Decision | Benefit | Cost | Guardrail |
|---|---|---|---|
| Keep a rolling summary buffer | Preserves broad continuity while reducing token load | Summary may lose nuance | Keep exact recovery refs and N+1 evals |
| Refresh periodically | Predictable scheduling and simple implementation | Can summarize too early or too often | Combine interval with token-health phase |
| Refresh only under pressure | Avoids extra model calls in healthy sessions | Can happen too late for safe compaction | Trigger before red phase, while there is room to summarize |
| Merge summaries cumulatively | Keeps one compact continuity block | Drift accumulates across generations | Anchor each refresh to source spans and durable facts |
| Use buffer as handoff artifact | Makes new sessions and sub-agents cheaper to start | Receiver may over-trust lossy prose | Include durable facts and recovery handles separately |

## Relationship to Other Patterns

- **Operates inside:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]], because summary refresh is a context-builder and loop intervention ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:60-75).
- **Constrained by:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]], because summarization may reduce history and tool bulk but must not mutate the harness prompt ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:28-41).
- **Must preserve:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]], because summaries are lossy and omitted middle still needs exact recoverability ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:24-39).
- **Uses:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] for `recovery_refs` that let the agent fetch exact old content by stable ID ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- **Complements:** [[docs/canonical/external-state-persistence|External State Persistence]], because durable facts should survive outside the summary and be loaded independently ([[docs/canonical/external-state-persistence|External State Persistence]]:31-65).
- **Validated by:** [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]], because the buffer succeeds only if the next turn behaves correctly after old turns are summarized ([[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]:20-40).

## References

- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:79-85 - Summary Buffer problem, mechanism, and best fit.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:147-151 - Summary Buffer benefit and cost.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]:125-145 - extracted Summary Buffer Continuity inputs, outputs, benefits, and limitations.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Classification]]:64-72 - Partial Coverage evidence and lifecycle gap.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:250-283 - original Summary Buffer lesson and tradeoffs.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:545-553 - orange-phase trigger for activating Summary Buffer.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:60-63 - summarization and compression as context-builder interventions.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:28-41 - reducible context may be summarized while harness prompt remains stable.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:24 - opaque summarization risk.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:59 - exact recoverability requirement for omitted middle.

---

*Created: 2026-06-10 | From: Token Budgeting pattern classification | Precedence: canonical*
