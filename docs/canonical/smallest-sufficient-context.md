---
title: "Smallest Sufficient Context"
type: canonical
tags: ["context-engineering", "agentes-orquestracao", "harness-engineering"]
aliases: ["minimal sufficient context", "sufficiency estimation", "order-preserving retrieval", "structured context selection"]
last_updated: 2026-06-18
relates-to: ["[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]"]
sources: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|Memory Selection Problem Analysis]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]"]
---
# Smallest Sufficient Context

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-18-memory-selection-problem/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

The instinctive response to agent degradation is to increase the context window, but the reliably usable fraction grows sublinearly — larger windows only raise the ceiling on accumulated noise before the cliff. The degradation is not a capacity problem; it is a selection problem. The model does not need more context — it needs the right context.

The repo assembles context by structural layers ([[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]): stack the harness prompt, durable state, task state, and recent texture in order. This is budget-aware but not sufficiency-aware — it does not determine the minimal subset the model needs for the current reasoning step. The result: context contains tokens that are "structurally well-placed" but relationally irrelevant, consuming budget and attention.

## Solution

Minimize tokens to the sufficiency condition: determine the minimal token set the agent needs to reason correctly about the current step, retrieve only those tokens through relational graph traversal, and assemble them in their original temporal order to preserve coherence.

The key insight: order-preserving retrieval of a few thousand well-chosen tokens outperforms dumping a full 128K window into the model. Selection is driven by structure (relational relevance) rather than similarity (embedding proximity).

**Key components:**

- **Sufficiency Estimator**: Determines the minimum token set needed for the agent to reason correctly about the current step.
- **Relational Traversal Engine**: Walks the context graph along typed edges (dependency, provenance, causation) to collect connected context units.
- **Order-Preserving Assembler**: Assembles retrieved tokens in their original sequence order to preserve temporal coherence.
- **Capacity Profiler**: Maps the model's known head/tail attention bias to place highest-importance tokens at attended positions.

**Flow:**
1. Parse current task step to identify what information is required.
2. Traverse relational graph from the task node along dependency, provenance, and causation edges.
3. Collect all reachable context units up to a relevance-depth threshold.
4. Sort collected units by original temporal order to preserve sequence coherence.
5. Apply capacity profiler: place critical tokens at head/tail positions the model attends to.
6. Trim to token budget; verify sufficiency condition is still met.

## Implementation in this repo

### What already exists

The repo has foundations for budget-aware, layered context assembly:

- **Ordered layer assembly**: [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:36 — "Reserve non-negotiable budget before loading reducible content: model context window, response buffer, safety buffer, stable harness prompt, and tool contracts. Inject durable state and current task state next."
- **Bounded active context**: [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28 — "Preserve a bounded active context made of the stable harness prompt, the head, the tail, and the latest result."
- **Retrieval by handle**: [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28 — "Represent omitted context as an addressable catalog. Each omitted message, tool call, span, prompt fragment, trace segment, or intermediate result receives a stable identifier."
- **Per-call budget awareness**: [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:30 — "Maintain an explicit token budget ledger for each planned model call before dispatch."

### What is missing (the gap)

The core idea of sufficiency estimation — determining the minimal subset by relational graph traversal — is not present. The repo assembles by structural layers, not by relational relevance:

1. **Sufficiency Estimator**: No mechanism determines the minimum token set needed for the current step. The hybrid context stack assembles by structural order (prompt → state → texture), not by relevance to the reasoning step.
2. **Relational Traversal Engine**: Retrieval is by handle or topic, not by dependency/provenance traversal. [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] provides handle-based access but does not traverse typed edges to collect connected context.
3. **Capacity Profiler**: No formal mapping of model attention bias (head/tail) to token placement. The hybrid context stack orders by structural category, not by attention profile.
4. **Order-Preserving Assembly**: Context from different cold/warm storage locations must be reassembled in original temporal order — not currently formalized.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Order-preserving retrieval of a few thousand well-chosen tokens outperforms dumping a full window | Determining sufficiency is itself a hard problem; underestimation causes incomplete context |
| Selection is driven by structure (relational relevance) rather than similarity (embedding proximity) | The relational graph must be maintained with supersession updates and dependency tracking |
| Each reasoning step operates on the cleanest possible context, slowing the compounding error rate | For tasks with highly interconnected dependencies, the minimal sufficient subset may still be large |
| Model attention bias is treated as a resource to optimize (capacity profiling) | Capacity profiling requires model-specific calibration data |

## Relationship to Other Patterns

- **Extends:** [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] by replacing structural layering with relevance-driven sufficiency estimation.
- **Uses:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] for the bounded active window that receives the selected subset.
- **Uses:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] for retrieval handles during graph traversal.
- **Requires:** Relational Context Graph (P1) for the typed edges that drive traversal.
- **Requires:** Tiered Context Storage (P0) for the storage infrastructure to retrieve from.
- **Guided by:** [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] for the budget constraint on the selected subset.

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|analysis]] — selection vs. capacity axis shift and "effective context is far smaller than advertised" lesson.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|patterns]]:61-106 — extracted Smallest Sufficient Context pattern definition.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|classification]]:50-78 — Partial Coverage classification with evidence and missing mechanics.
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:36 — ordered layer assembly.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28 — bounded active context.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28 — retrieval by handle.
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:30 — per-call budget ledger.

---

*Created: 2026-06-18 | From: Memory Selection Problem pattern classification | Precedence: canonical*
