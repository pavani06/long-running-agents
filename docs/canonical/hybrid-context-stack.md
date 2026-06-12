---
title: "Hybrid Context Stack"
type: canonical
aliases: ["pilha de contexto hibrida", "layered context", "context stack", "multi-layer context assembly"]
tags: ["context-engineering", "agentes-orquestracao"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
---
# Hybrid Context Stack

**Type:** canonical
**Status:** active
**Source:** [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]:14-21

---

## Problem

No single context-budgeting strategy handles every phase of a long-running agent session. A fixed recent-message window is predictable but can drop distant dependencies; a summary buffer preserves broad continuity but is lossy; compression saves space but can blur exact evidence; durable state keeps critical facts alive but does not preserve conversational texture by itself. The source token-budgeting lesson therefore teaches a hybrid approach that combines a recent window, a summary buffer, and fixed critical context ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:375-424).

The repository already has strong canonical pieces for this stack. [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]] defines context-builder blocks for stable prompt, head, tail, omitted middle, tool or trace bulk, and durable state ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:30-40). [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] defines bounded active context plus recoverable middle ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28-39). [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] defines retrieval metadata for omitted content ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:30-43). [[docs/canonical/external-state-persistence|External State Persistence]] defines loading durable state and merging it with current context ([[docs/canonical/external-state-persistence|External State Persistence]]:31-57).

The gap is assembly policy. The Phase 3 classification found `NOT_FOUND` for a single hybrid context stack with budgeted inclusion order and a context-builder decision trace, even though the component layers exist across canonical docs ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:94-100).

## Solution

A Hybrid Context Stack is a budget-aware context-builder policy that assembles each model call from ordered layers. It does not let stable harness instructions, durable facts, summaries, recent conversational texture, and recoverable omitted content compete as one raw transcript.

The extracted pattern defines the inputs as stable harness prompt and tool contracts, durable structured facts, summary buffer, recent-message window, and optional compressed blocks, topic buckets, or token-health actions. Its outputs are a layered active context under a known token budget, a prioritized inclusion order, and a decision trace explaining what was kept, summarized, compressed, or omitted ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:191-212).

The stack policy is:

1. Reserve non-negotiable budget before loading reducible content: model context window, response buffer, safety buffer, stable harness prompt, and tool contracts.
2. Inject durable state and current task state next, because durable facts must survive windowing, summarization, and session transition.
3. Preserve head and tail anchors: original goal, constraints, current request, latest tool result, unresolved decisions, and immediate next action.
4. Add summary buffers, topic summaries, or compressed blocks only after pinned state has budget.
5. Expose omitted middle through an addressable catalog instead of silently dropping it.
6. Emit a decision trace for every context build.
7. If the stack still exceeds budget, reduce optional layers first, then summarize or compress older reducible content, then hand off to a fresh session rather than weakening the stable harness or losing durable state.

## ASCII Diagram

```text
MODEL CONTEXT WINDOW
+------------------------------------------------------------+
| reserved output buffer + safety buffer                     |
+------------------------------------------------------------+
| stable harness prompt + tool contracts                     |
+------------------------------------------------------------+
| durable state: facts, constraints, current task state       |
+------------------------------------------------------------+
| head anchor: original goal, definitions, hard constraints   |
+------------------------------------------------------------+
| summary / topic / compressed older-history blocks          |
+------------------------------------------------------------+
| tail anchor: recent turns, latest result, current request   |
+------------------------------------------------------------+
| compact catalog: omitted IDs, locations, previews, fetch    |
+------------------------------------------------------------+

EXTERNAL STORES
+----------------------+   +----------------------+   +----------------+
| exact omitted middle |   | durable state store  |   | summary buffer |
| fetch by catalog id  |   | load and merge       |   | refresh policy |
+----------------------+   +----------------------+   +----------------+
```

## Budgeted Inclusion Order

| Order | Layer | Budget policy | If over budget | Canonical basis |
|---|---|---|---|---|
| 1 | Response and safety reserve | Reserve before prompt assembly | Stop assembly and request compaction or handoff | The source calculator reserves response and safety buffers before calculating available context ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:445-451). |
| 2 | Stable harness prompt and tool contracts | Preserve as non-reducible operating contract | Do not truncate through context compaction | Stable harness prompt is separated from reducible payload ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:26-41). |
| 3 | Durable state and current task state | Inject after freshness or provenance checks | Persist, refresh, or omit only non-durable material | External state persistence loads stored critical data and merges it with current context ([[docs/canonical/external-state-persistence|External State Persistence]]:31-57). |
| 4 | Head anchor | Preserve original goal, definitions, and hard constraints inside policy-defined budget | Move non-anchor middle spans to cataloged memory | Head-tail truncation preserves stable prompt, head, tail, and latest result ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28-39). |
| 5 | Summary, topic, or compressed older history | Include only the compact block that helps the next decision | Refresh summary, shrink preview, or move exact source to catalog | Token budgeting source defines summary, compression, semantic bucketing, and hybrid layering as complementary strategies ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:250-424). |
| 6 | Tail anchor and recent-message window | Preserve latest state, recent turns, latest result, and current user request | Shorten older tail first; never remove the current request | Tail carries current state, recent turns, latest tool results, unresolved decisions, and immediate request ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:37-39). |
| 7 | Addressable omitted-memory catalog | Include compact `id`, `kind`, `location`, `preview`, `scope`, and `fetch` metadata | Shrink previews, not stable IDs or fetch handles | Catalog fields make omitted content discoverable and exactly recoverable ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:30-43). |

## Context-Builder Decision Trace

Every context build should emit a trace that is small enough to log or attach to replay artifacts. The trace exists because the hybrid stack is more complex than a single window or summary, and component interactions can hide bugs unless the context builder is observable ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:209-212).

Minimum trace fields:

| Field | Purpose |
|---|---|
| `model_context_window` | Hard capacity used for this build. |
| `reserved_response_tokens` | Output budget held back before input assembly. |
| `reserved_safety_tokens` | Safety margin that prevents last-token operation. |
| `stable_harness_version` | Version or identifier of the non-reducible harness prompt. |
| `included_layers` | Ordered list of layers included in active context. |
| `layer_token_estimates` | Estimated or measured token cost per layer. |
| `omitted_items` | Catalog IDs or source spans withheld from active context. |
| `transformations` | Summaries, compressions, bucket selections, and preview shrinkage performed. |
| `budget_action` | `continue`, `monitor`, `compress`, `summarize`, `fetch`, or `handoff`. |
| `reason` | Human-readable reason for the final inclusion decision. |

Example trace shape:

```json
{
  "budget_action": "compress",
  "reason": "recent tail and durable state fit, older middle exceeded optional budget",
  "included_layers": [
    "stable_harness",
    "durable_state",
    "head_anchor",
    "summary_buffer",
    "tail_anchor",
    "memory_catalog"
  ],
  "omitted_items": ["turns:31-78", "tool:inventory-check:2026-06-10T12:05:00Z"],
  "transformations": ["summarized turns:31-78 to 1200 tokens"]
}
```

## Implementation in this repo

### What already exists

- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]] defines distinct context-builder blocks and says context reduction may summarize, truncate, externalize, or retrieve history and tool bulk while preserving the harness prompt ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:28-41).
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] keeps active context bounded with stable prompt, head, tail, latest result, and recoverable middle, and it explicitly rejects a universal first-N/last-N heuristic ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28-39).
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] provides the catalog schema needed to inspect omitted memory without reloading the whole archive ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- [[docs/canonical/external-state-persistence|External State Persistence]] defines the durable-state loop: extract critical data, write it externally, load it on the next turn, merge with current context, and generate or evaluate the response ([[docs/canonical/external-state-persistence|External State Persistence]]:31-57).
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] makes Context Builder an owned component and says every token should be constructed deliberately ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:60-62).

### What is missing

1. A canonical stack order that says which context layers are pinned, optional, reducible, recoverable, or handoff-triggering.
2. A per-call budget contract that reserves response and safety budget before optional context assembly.
3. A decision trace that records which layers were included, transformed, omitted, or made recoverable.
4. Evals or replay traces that prove the hybrid stack preserves continuity after compaction.

## Tradeoffs

| Benefit | Cost | Mitigation |
|---|---|---|
| Balances stable instructions, durable facts, summaries, recent turns, and omitted-memory handles instead of relying on one truncation trick | More complex than a recent window or summary alone | Keep a fixed inclusion order and emit a decision trace every build. |
| Preserves decision-critical state while still bounding active prompt size | Requires token estimates for every layer | Use the source budget model: total context minus processed input minus response and safety buffers ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:17-37). |
| Makes omitted content recoverable rather than silently lost | Requires storage and catalog metadata | Use stable IDs, locations, previews, scopes, and fetch handles ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:30-43). |
| Lets the harness adjust strategy by session phase | Needs monitoring and threshold tuning | Use token-health actions such as continue, monitor, compress, summarize, or new session from the extracted monitor pattern ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:59-79). |
| Supports production continuity across long sessions | Summary or compression may still lose nuance | Preserve exact source spans externally and fetch them by handle when needed. |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]], because the stable harness is a pinned layer and not reducible context payload ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:26-41).
- **Depends on:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]], because the hybrid stack uses head and tail anchors plus recoverable middle as the active-context backbone ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28-39).
- **Depends on:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]], because omitted layers must remain inspectable and exactly fetchable by handle ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:30-43).
- **Depends on:** [[docs/canonical/external-state-persistence|External State Persistence]], because durable facts and task state are loaded from outside the model context window and merged into the current turn ([[docs/canonical/external-state-persistence|External State Persistence]]:31-57).
- **Complements:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]], because budget-aware handoff and pause/resume need either exact context serialization or a faithful state rebuild ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-57).
- **Operationalizes:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]], because the Context Builder is the control point that summarizes old history, injects fresh context, and compresses verbose tool results ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:60-75).

## References

- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:34-62 - token budgeting definition and available-space equation.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:375-424 - hybrid approach with recent window, summary buffer, and fixed critical context.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:445-459 - conversation viability calculator with response and safety reserve.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:103-109 - Hybrid Context Stack extraction from source analysis.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:191-212 - reusable Hybrid Context Stack pattern with inputs, outputs, benefits, and limitations.
- `docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns.yaml:288-321` - YAML source flow: reserve budget, inject durable facts, add summaries, add recent window, compress or omit, and log final inclusion decision.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:94-100 - Partial Coverage classification and NOT_FOUND gap.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:30-40 - existing context-builder block list.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28-39 - bounded active context with recoverable middle.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:30-43 - omitted-memory retrieval metadata.
- [[docs/canonical/external-state-persistence|External State Persistence]]:31-57 - external durable-state loading and merge.

---

*Created: 2026-06-10 | From: Token Budgeting pattern classification | Precedence: canonical*
