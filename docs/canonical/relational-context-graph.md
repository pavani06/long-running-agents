---
title: "Relational Context Graph"
type: canonical
tags: ["context-engineering", "agentes-orquestracao"]
aliases: ["typed edge context graph", "relational memory graph", "selection-not-retrieval graph", "structured context graph"]
last_updated: 2026-06-18
relates-to: ["[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]"]
sources: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|Memory Selection Problem Analysis]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]"]
---
# Relational Context Graph

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-18-memory-selection-problem/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Embedding stores answer "what is similar to X" — not "what is relevant to this task in this state." Similarity flattens semantic relationships, returning near-misses that act as distractors and accelerate the agent cliff (Link 1 of the degradation loop: unequal context attention). The structural error: treating relevance as proximity in embedding space rather than as a graph property.

A store calibrated for similarity delivers near-misses — exactly the distractors that degrade attention quality. The correction is not a cache in front of an embedding store; the intelligence is not in the lookup, it is in the structure. Relevance is relational: it depends on the graph of dependencies, provenance, supersession, and causation.

## Solution

Replace similarity-based retrieval with relational selection. Build a context graph where nodes represent context units (tool results, decisions, state snapshots, progress notes) and edges carry typed semantic relationships. The query primitive changes: instead of "find similar vectors," traverse the graph along typed edges to collect connected context.

**Four formal edge types:**

| Edge Type | Meaning | Example |
|---|---|---|
| Dependency | A depends on B (B must be present to understand A) | Tool result depends on the tool call that produced it |
| Provenance | A was derived from B (trace derivation chain) | A decision was derived from a specific observation |
| Supersession | A was superseded by B (B is the current version; A is stale) | A state snapshot is replaced by a newer state snapshot |
| Causation | Decision D caused outcome O (link decisions to consequences) | An architectural choice caused a performance regression |

Transformation: traversing the graph by typed relationships converts retrieval (returning what is near) into selection (returning what is relevant).

**Key components:**

- **Node Ingestor**: Creates graph nodes for each new context unit (tool result, decision, state snapshot, note) with metadata.
- **Edge Classifier**: Classifies relationships between nodes into typed edges: dependency, provenance, supersession, causation.
- **Supersession Updater**: Marks obsolete nodes and redirects edges when context is superseded by newer versions.
- **Traversal Engine**: Executes graph traversals along typed edges to collect context connected to a query node.

**Flow:**
1. Intercept every context unit the agent generates (tool result, decision, state snapshot).
2. Create a graph node with metadata (timestamp, agent ID, session ID, task step).
3. Classify relationships to existing nodes: dependency, provenance, supersession, or causation.
4. If supersession detected, update the superseded node's edges and mark it as stale.
5. On context query, traverse the graph from the task node along typed edges.
6. Return traversed context in dependency order, with superseded nodes excluded.

## Implementation in this repo

### What already exists

The repo has significant graph infrastructure:

- **Epistemic memory graph**: [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:28 — "Represent operational memory as a graph whose nodes carry both retrieval metadata and epistemic labels. Minimum node fields: id, kind, epistemic_status, source, owner, validity_scope, retrieval_keys, last_verified."
- **Hybrid retrieval fusion**: [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:47 — "Follow backlinks and explicit graph edges to adjacent decisions, incidents, rubrics, and workflow concepts. Fuse ranked candidates from search, vector retrieval, backlinks, and graph traversal."
- **Provenance tracking**: [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]:94 — "Attach provenance: every durable fact should record its source turn, tool result, artifact, or owner."
- **Node metadata foundations**: [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:30 — "Minimum catalog fields: id, kind, location, preview, scope, fetch, tool, path."

### What is missing (the gap)

The repo's graph infrastructure focuses on epistemic labeling (facts, beliefs, hunches — what is the belief status?), not on structural relationship typing (dependencies, provenance, supersession, causation — what is the relationship between context units?). The gap:

1. **Edge Classifier**: No component classifies relationships into the four formal edge types (dependency, provenance, supersession, causation). The epistemic graph focuses on belief-status labeling of nodes, not on typed edge classification between them.
2. **Supersession Updater**: No mechanism marks obsolete nodes and redirects edges when context is superseded. The epistemic graph has `epistemic_status: stale` as a node label but does not formalize superseption as a graph operation that updates edges.
3. **Node Ingestor for context units**: No automatic graph node creation from tool results and state snapshots. The addressable memory catalog provides metadata for retrieval but does not create graph nodes with typed edges.
4. **Traversal Engine**: Graph traversal exists at the conceptual level (epistemic graph:47) but is not formalized as a component with typed-edge query patterns.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Transforms retrieval into selection: the model receives context connected by real semantic relationships | Graph maintenance is non-trivial: every new context unit must be classified with edge types |
| Supersession edges prevent stale context from entering the window | Bootstrapping requires either manual schema design or a bootstrap phase where edge types are inferred |
| Provenance edges enable debugging: trace any conclusion back through the chain of derivations | Tooling maturity for relational context graphs is far behind embedding stores |
| Causation edges enable learning: link decisions to outcomes across sessions | Graph traversal latency can exceed similarity search for deep dependency chains |

## Relationship to Other Patterns

- **Extends:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] by adding formal typed edges (dependency, provenance, supersession, causation) to the existing epistemic labeling.
- **Uses:** [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]] for provenance tracking on durable facts.
- **Uses:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] for node metadata and retrieval handles.
- **Is foundation of:** All other selection patterns — Deliberate Forgetting (P1), Smallest Sufficient Context (P1), Selection-Budgeted Retrieval (P0).
- **Complements:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] by providing the relational structure for deciding what stays in the active window.

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|analysis]] — similarity is not relevance framework and structured property of the selection layer.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|patterns]]:153-198 — extracted Relational Context Graph pattern definition.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|classification]]:100-128 — Partial Coverage classification with evidence and missing mechanics.
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:28 — node fields with epistemic labels.
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:47 — hybrid retrieval fusion with graph traversal.
- [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]:94 — provenance tracking.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:30 — node metadata foundations.

---

*Created: 2026-06-18 | From: Memory Selection Problem pattern classification | Precedence: canonical*
