---
title: "Tiered Context Storage with Promotion/Demotion"
type: canonical
tags: ["context-engineering", "agentes-orquestracao"]
aliases: ["hot warm cold storage", "context tiering", "tiered memory storage", "promotion demotion engine"]
last_updated: 2026-06-18
relates-to: ["[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]"]
sources: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|Memory Selection Problem Analysis]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]"]
---
# Tiered Context Storage with Promotion/Demotion

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-18-memory-selection-problem/
**Classification:** Missing (P0)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Keeping all context in active memory is unsustainable for long-running agents. Keeping everything in cold storage makes context useless when the model needs to reason. The repo has a binary two-tier model: active context vs. external memory ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]), with retrieval handles for external access ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]). But there is no dynamic tiered architecture that moves context between storage layers based on relevance.

The consequence: every context unit is either in the window or completely outside it. There is no warm tier — no intermediate state for "recently relevant, might need it soon." Without dynamic promotion/demotion, the agent either carries stale context in its window that degrades attention quality, or drops context that becomes unexpectedly relevant on the next step and must be re-fetched from cold storage with latency.

## Solution

A three-tier storage architecture — hot, warm, cold — with a relevance-driven promotion/demotion engine that dynamically moves context between tiers.

```
hot   [in-memory cache]   — what the model is reasoning about now (sub-ms latency)
warm  [NVMe]              — recently relevant, accessible with low latency (~1ms)
cold  [object storage]    — complete history, retrieved on demand (~100ms)
```

The design principle: the working set is kept small on purpose. Between the model and everything it could know, the decision layer selects the relevant subset. Promotion moves context up (`cold → warm → hot`) when relevance signals predict it will be needed. Demotion moves context down (`hot → warm → cold`) when it is no longer needed for current reasoning.

**Key components:**

- **Hot Tier Cache**: In-memory store holding the current active context window.
- **Warm Tier Store**: NVMe-backed store for recently relevant context that may be promoted back to hot.
- **Cold Tier Archive**: Object storage for complete history, supporting on-demand retrieval.
- **Tier Orchestrator**: Executes promotion/demotion decisions based on relevance scores and prefetch predictions.

**Flow:**
1. Monitor active context window in hot tier as the model reasons through the current step.
2. When step completes, evaluate each context unit's continued relevance.
3. Demote irrelevant units: `hot → warm` (if recently relevant) or `hot → cold` (if likely obsolete).
4. Before next step, traverse relational graph to predict which cold/warm units will be needed.
5. Prefetch predicted units: `cold → warm`, `warm → hot`.
6. Assemble new active window in hot tier; verify size against token budget.

## Implementation in this repo

### What already exists

NOT_FOUND across all 85 canonical docs and the system-of-record pattern inventory. The repo has:

- **Binary two-tier model**: active context vs. external memory in [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]].
- **Retrieval handles** for external access via [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]].
- **Layered context assembly** through [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]].

The only "promotion" patterns in the repo are [[docs/canonical/cross-context-knowledge-siloing|Cross-Context Knowledge Siloing]] (knowledge promotion pipeline) and [[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]] (artifact promotion path) — neither relates to storage tier management. The only "tiers" in the repo refer to eval tier stratification (fast/medium/deep) in [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]].

### What is missing

1. **Three-tier storage architecture**: No hot/warm/cold definitions with latency contracts.
2. **Promotion/Demotion Engine**: No dynamic context movement between tiers driven by relevance scores.
3. **Tier Orchestrator**: No relevance-driven tier transitions with prefetch predictions.
4. **Latency-aware storage policies**: No cost model for `cold → hot` retrieval vs. token savings.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps active working set small on purpose, preventing context rot | Promotion/demotion policy must be tuned per domain; generic recency-based policies fail when relevance is non-monotonic |
| Enables on-demand retrieval from cold storage when dropped details become relevant | Cold → hot promotion latency can stall reasoning if not anticipated with prefetch |
| Separates storage concern (where data lives) from selection concern (what the model attends to) | Requires infrastructure for three storage tiers with different latency characteristics |
| Scales linearly with history volume; storage cost in cold tier is negligible | The orchestrator itself consumes tokens to evaluate relevance |

## Relationship to Other Patterns

- **Extends:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] by replacing the binary active/external model with three-tier dynamic promotion/demotion.
- **Uses:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] for stable handles across tiers.
- **Uses:** [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] for structured context assembly within each tier.
- **Requires:** [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] for verifying assembled window size.
- **Enables:** Deliberate Forgetting (P1) by providing the tier structure for relevance-based discard decisions.
- **Enables:** Selection-Budgeted Retrieval (P0) by providing the storage infrastructure for cost-benefit retrieval.
- **Builds on:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] for relevance signals derived from graph relationships.

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|analysis]] — selection layer three-property framework.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|patterns]]:107-151 — extracted Tiered Context Storage pattern definition.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|classification]]:79-98 — Missing classification with locations searched and missing mechanics.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28 — bounded active context with middle in external memory.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28 — addressable catalog for omitted context.

---

*Created: 2026-06-18 | From: Memory Selection Problem pattern classification | Precedence: canonical*
