---
title: "Selection-Budgeted Retrieval"
type: canonical
tags: ["context-engineering", "agentes-orquestracao", "harness-engineering"]
aliases: ["budgeted retrieval", "cost-benefit retrieval", "retrieval token budget", "information value retrieval"]
last_updated: 2026-06-18
relates-to: ["[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]", "[[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]"]
sources: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|Memory Selection Problem Analysis]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]"]
---
# Selection-Budgeted Retrieval

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-18-memory-selection-problem/
**Classification:** Missing (P0)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Retrieval systems built to solve the memory problem can become the engine of the degradation loop they were constructed to prevent. Every retrieval adds tokens. Every added token shrinks effective context. The very system that was meant to help becomes the source of failure — this is Link 4 (inert memory feedback) of the agent degradation loop.

The repo has the two foundational pieces that this pattern would bridge: explicit token budget tracking ([[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]) and retrieval infrastructure ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]], [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]]). However, the retrieval itself is not budget-aware. The budget ledger has a `retrieve` action but no mechanism for deciding what to retrieve under budget constraints. The addressable memory catalog enables retrieval by handle but without cost-benefit ranking.

The consequence: when token budget tightens, retrieval continues undifferentiated — the system may fetch near-miss distractors that cost tokens to include and degrade reasoning quality, while leaving genuinely high-value context in cold storage.

## Solution

Make retrieval itself budget-aware by ranking candidates by information value per token and allocating retrieval budget from most to least valuable. The core insight: each retrieval must justify itself by its predicted contribution to the task, not by its similarity score to the query.

**Key components:**

- **Token Cost Estimator**: Computes the token count for each candidate retrieval item.
- **Information Value Predictor**: Estimates the expected reduction in task uncertainty if a given context item is retrieved, using historical utility data.
- **Budget Tracker**: Maintains the remaining token budget per step and allocates between retrieval and reasoning.
- **Utility Feedback Loop**: After the model produces output, checks which retrieved items were actually referenced and updates the predictor.

**Flow:**
1. Identify all candidate context items from the relational graph that could be relevant to the current step.
2. Compute token cost for each candidate.
3. Estimate information value for each candidate using historical utility data.
4. Rank candidates by value/cost ratio; allocate budget from most to least valuable.
5. Retrieve and inject top-ranked candidates into context; log budget consumption.
6. After model output, compare referenced items against retrieved items; update utility predictor.

The feedback loop is critical: without it, the system repeats the same retrieval mistakes. With it, the system learns which retrievals actually matter and improves value prediction across sessions.

## Implementation in this repo

### What already exists

NOT_FOUND as a unified pattern, but the repo has the two foundational halves:

- **Token budget tracking**: [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:63 defines a `retrieve` action for the budget ledger but provides no mechanism for deciding what to retrieve under constraints.
- **Retrieval infrastructure**: [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] enables retrieval by handle with `id`, `kind`, `preview`, `scope`, and `fetch` contracts. [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]] groups context by topic for retrieval.
- **Graph foundation**: [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] provides graph traversal for context selection, but does not incorporate token cost.

The missing bridge: ranking retrieval candidates by predicted value/cost ratio under a known budget constraint.

### What is missing

1. **Information Value Predictor**: No mechanism estimates task uncertainty reduction from retrieving a specific context unit.
2. **Cost-Benefit Ranking**: No ranking of candidates by value divided by token cost under a known budget.
3. **Utility Feedback Loop**: No tracking of which retrieved items were actually referenced by the model in its output.
4. **Token Cost Estimator per candidate**: No pre-retrieval cost estimation — tokens are counted after assembly, not before selection.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents the memory feedback loop by making retrieval itself budget-aware | Information value estimation is hard — utility is only known after the model uses or ignores the context |
| Each retrieval is justified by predicted task contribution, not similarity score | In exploration-heavy tasks, the system may over-penalize retrieval and starve the model of discoveries |
| Historical utility data creates a learning loop across sessions | Requires instrumentation to track which retrieved items the model actually referenced |
| Tokens are conserved for reasoning rather than spent on near-miss distractors | The budgeting logic adds a decision step before every retrieval, increasing per-step latency |

## Relationship to Other Patterns

- **Bridges:** [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]] and [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] by making retrieval budget-aware.
- **Uses:** [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]] for predicting available budget per step.
- **Uses:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] for node relationships that inform value prediction.
- **Uses:** [[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]] for topic-based candidate grouping.
- **Directly counters:** Link 4 (inert memory feedback) of the Agent Degradation Loop (P1).
- **Requires:** Tiered Context Storage (P0) for the storage infrastructure that holds candidates across tiers.
- **Feeds:** [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]] with retrieval-budget consumption data.

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|analysis]] — the memory feedback loop (Link 4) and more-memory-makes-it-worse lesson.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|patterns]]:294-340 — extracted Selection-Budgeted Retrieval pattern definition.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|classification]]:184-209 — Missing classification with locations searched and missing mechanics.
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:63 — `retrieve` action without selection mechanism.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28 — addressable retrieval by handle without cost ranking.

---

*Created: 2026-06-18 | From: Memory Selection Problem pattern classification | Precedence: canonical*
