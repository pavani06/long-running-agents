---
title: "Deliberate Forgetting"
type: canonical
tags: ["context-engineering", "agentes-orquestracao"]
aliases: ["intentional forgetting", "proactive context discard", "relevance-based forgetting", "context rot prevention"]
last_updated: 2026-06-18
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]"]
sources: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|Memory Selection Problem Analysis]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]"]
---
# Deliberate Forgetting

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-18-memory-selection-problem/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Context windows accumulate noise from irrelevant tokens because forgetting only happens by accident — through truncation when the window fills, or through indiscriminate compression. Neither is an informed decision about what to keep vs. discard.

The design shift: make forgetting a first-class intentional operation. The question is not "how to store everything" but "what can I afford to forget right now." Agent quality becomes a function of exclusion decision quality, not storage capacity.

The repo has the foundations for deliberate context management but treats summarization, compaction, and truncation as reactive budget-driven interventions, not as a proactive relevance-scoring loop.

## Solution

Treat forgetting as an intentional design operation executed at every step: actively decide which tokens are promoted into the active window and which are demoted to cold storage, based on relational relevance to the current task. Every discard is logged with rationale, enabling cold-storage retrieval if discarded context becomes relevant later.

**Key components:**

- **Relevance Evaluator**: Assesses each context unit's relevance to the current task state using relational graph traversal — not similarity scores.
- **Promotion/Demotion Engine**: Executes tier transitions based on relevance scores, moving tokens between hot, warm, and cold storage.
- **Discard Logger**: Records what was dropped and the rationale, enabling retrieval if discarded context becomes relevant later.
- **Budget Gate**: Ensures the evaluation cost of the forgetting decision does not exceed the token savings it generates.

**Flow:**
1. Receive current task state and active context window snapshot.
2. Traverse relational context graph to identify context units connected to the current task.
3. Score each context unit by relevance (connectedness to current task) and recency.
4. Demote low-scoring units to warm/cold storage; log discard decisions with rationale.
5. Promote high-scoring units from warm storage to hot (active window).
6. Verify working set size against token budget; iterate if over budget.

## Implementation in this repo

### What already exists

The repo has extensive context management infrastructure with individual pieces that relate to deliberate forgetting, though not unified:

- **Deliberate context construction**: [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:60 — "Context Builder: What the model sees beyond the prompt... You construct every token deliberately."
- **Explicit compaction triggers**: [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:65 — "orange: Budget em faixa de risco... summarize ou compress."
- **Head-tail truncation with recoverable middle**: [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:37 — "the middle is not discarded. It is stored as exact recoverable content and exposed through an addressable catalog or retrieval tool."
- **Selective history with durable facts**: [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]:32 — separates "recent conversational texture" from "structured durable facts" that must survive compaction.

### What is missing (the gap)

The repo treats context reduction as reactive or budget-driven interventions. The deliberate forgetting concept requires a proactive relevance-scoring loop operating at every step:

1. **Relevance Evaluator**: No mechanism scores context units by relevance to current task using relational graph traversal. The repo has structural layering (hybrid context stack) and topic bucketing (semantic topic bucketing), but not relevance scoring.
2. **Promotion/Demotion Engine**: The repo has a binary keep/omit model. No scored tier transitions (hot/warm/cold) with promotion and demotion decisions.
3. **Discard Logger**: No record of what was dropped and why — compaction is lossy without audit trail.
4. **Budget Gate on evaluation cost**: The ledger tracks token expenditure, but no mechanism ensures the cost of evaluating forgetting decisions does not exceed the savings from discarded tokens.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents context rot accumulation where each appended token degrades subsequent step quality | Requires a relational context graph to make informed forgetting decisions; similarity-based stores cannot support this |
| Shifts design question from "how to store everything" to "what can I afford to forget now" | Aggressive forgetting can drop details whose importance only becomes apparent later |
| Makes agent quality a function of exclusion decision quality, not storage capacity | The forgetting policy itself consumes tokens to evaluate relevance; in extremely tight budgets, the evaluation cost may exceed the savings |
| Reduces near-miss distractors that drive the compounding error rate toward the cliff | The discard logger adds storage overhead for audit trail |

## Relationship to Other Patterns

- **Depends on:** Relational Context Graph (P1) for relevance signals via typed edge traversal.
- **Requires:** Tiered Context Storage (P0) for the hot/warm/cold infrastructure to promote into and demote from.
- **Extends:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] by adding a proactive forgetting step to the control loop.
- **Extends:** [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]] by replacing the binary durable/recent split with scored relevance.
- **Uses:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] for the recoverable discard mechanism.
- **Uses:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] for discard log storage and retrieval handles.
- **Guided by:** [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]] for phase-based forgetting aggression.

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|analysis]] — deliberate forgetting as first-class operation and "what should it be thinking about right now" lesson.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|patterns]]:15-60 — extracted Deliberate Forgetting pattern definition.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|classification]]:19-48 — Partial Coverage classification with evidence and missing mechanics.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:60 — deliberate context construction.
- [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]:32 — selective history with durable facts.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:37 — recoverable middle.
- [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:65 — orange phase compaction trigger.

---

*Created: 2026-06-18 | From: Memory Selection Problem pattern classification | Precedence: canonical*
