---
title: "Three-Tier Memory Persistence"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["agentes-orquestracao", "context-engineering"]
aliases: ["three-tier memory", "memory authority gradient", "explicit builder implicit memory", "memory persistence tiers"]
relates-to: ["[[docs/canonical/tiered-context-storage|Tiered Context Storage with Promotion/Demotion]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]]"]
---

# Three-Tier Memory Persistence

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Partial Coverage (High)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Memory in agent systems is typically either fully manual ("remember this" — the user must explicitly save every detail) or fully implicit (the agent guesses what matters and remembers everything). Neither extreme is correct. Fully manual memory misses information the user assumes the agent will remember but never explicitly saves. Fully implicit memory captures noise, invents significance where none exists, and risks remembering sensitive information without user awareness.

The missing dimension is authority: *who decides what to persist?* And the answer varies by what is being remembered. A user saying "remember my name is Harrison" is an explicit instruction — authority is with the user. A builder declaring "birthdays matter for this domain" is a domain decision — authority is with the agent designer. An agent noticing that customers who mention a specific product category tend to have higher satisfaction is an implicit observation — authority is with the agent. Each tier represents a different authority gradient and a different risk profile.

Wedeen describes three tiers with increasing automation and correspondingly increasing quality risk:
- **Tier 1 (explicit per-turn)**: The user says "save this to memory." Authority is with the user. Quality risk is low — the user explicitly intended this memory.
- **Tier 2 (builder-defined)**: Agent builders declare what matters upfront — "remember birthdays," "remember customer preferences for organic products." Authority is with the domain expert. Quality risk is medium — the builder's declarations may have gaps.
- **Tier 3 (implicit/agent-decided)**: The agent autonomously determines what to remember based on observed patterns. Authority is with the agent. Quality risk is high — the agent may capture noise, miss significance, or remember inappropriate information.

The three-tier architecture makes the authority gradient explicit and operational, rather than treating memory as a binary on/off decision.

## Solution

A three-tier memory persistence architecture where each tier has a different authority source, persistence mechanism, and quality risk profile. The tiers form an adoption path: start with Tier 1 → add Tier 2 declarations → enable Tier 3 as confidence grows.

**Key components:**

1. **Tier 1 — Explicit Per-Turn Memory**: The user directly controls what is remembered. "Save this to memory" or "remember that my wife's name is Sarah" creates a Tier 1 memory. The persistence mechanism is straightforward — store the memory with a user-initiated flag. Retrieval is deterministic: when the user returns, load all Tier 1 memories. This tier is the safest because the authority (user) and the action (explicit save) are aligned.

2. **Tier 2 — Builder-Defined Memory Schema**: Agent designers declare upfront what matters for their domain. In e-commerce: "remember customer birthday," "remember product preferences," "remember return history." In healthcare: "remember medication allergies," "remember appointment preferences." These schemas are declared as part of the agent specification and drive structured memory extraction during conversations. When the agent encounters information matching a declared schema, it persists it. The builder's authority is domain expertise — they know what will matter for future interactions because they designed the experience.

3. **Tier 3 — Agent-Decided Implicit Memory**: The agent autonomously determines what to remember based on observed patterns. This might include conversational cues (frustration signals, repeated topics, unusual requests), inferred preferences (the customer always asks for same-day shipping but never explicitly says "I prefer speed"), or correlation patterns (customers who mention weather tend to have higher satisfaction). This tier has the highest quality risk — the agent may misinterpret signals, capture noise as signal, or remember information the user considers private.

4. **Authority Gradient and Adoption Path**: The three tiers are not all-or-nothing. A deployment starts with Tier 1 (user-initiated memory), adds Tier 2 schemas as domain understanding matures, and enables Tier 3 selectively as confidence in the agent's implicit memory accuracy grows. The adoption path mirrors the authority gradient: user → builder → agent, each step trading safety for automation.

**Measurable impact (Sierra's results):**

Wedeen reports that three-tier memory "measurably improved resolution rate" through concrete memory applications: greeting customers by name (Tier 1), recalling previous call topics (Tier 1 + Tier 2), recognizing that the customer had a frustrating interaction last time and adjusting tone (Tier 2 + Tier 3). The resolution rate improvement comes from reducing the conversational overhead of re-establishing context — the agent already knows who the customer is, what they last discussed, and what matters to them.

**Distinction from storage tiers:** [[docs/canonical/tiered-context-storage|Tiered Context Storage with Promotion/Demotion]] describes storage tiers (hot/warm/cold) based on retrieval latency. Three-tier memory persistence describes authority tiers (user/builder/agent) based on who decides what to persist. The two patterns are orthogonal — storage tiers answer "how fast can we retrieve this?" while authority tiers answer "who decided this should be remembered and how much do we trust it?" A Tier 3 memory (agent-decided) could live in hot storage; a Tier 1 memory (user-initiated) could be archived to cold storage if never accessed. The tiers compose: authority gradient × storage latency.

## Implementation in this repo

### What already exists

From the classification:

- [[docs/canonical/tiered-context-storage|Tiered Context Storage with Promotion/Demotion]]: Hot/warm/cold storage tiers with latency contracts. Storage tiers, not authority tiers.
- [[docs/canonical/external-state-persistence|External State Persistence]]: External state persistence as unified strategy. Memory persistence exists but without the authority gradient.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]: Addressable memory with retrieval handles. Memory is addressable but not tiered by authority.
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]: Graph of memory with epistemic status and provenance. Provenance ("where did this knowledge come from") is related to authority ("who decided this should be remembered") but not the same.

### What is missing

From the classification: "The three-tier user/builder/agent authority gradient: Tier 1 (user-initiated 'remember this'), Tier 2 (builder-defined 'birthdays matter'), Tier 3 (agent-decided implicit memory). The repo has storage tiers but not the authority gradient that maps to who decides what to persist."

1. **Authority gradient as architectural dimension**: The repo treats memory as a technical problem (storage, retrieval, provenance) but not as an authority problem (who decides what to remember).
2. **Builder-defined memory schemas**: No mechanism for domain experts to declare what matters for their domain as structured memory extraction templates.
3. **Adoption path from Tier 1 to Tier 3**: No documented progression from safe (user-initiated) to automated (agent-decided) memory persistence.
4. **Tier-specific quality risk profiles**: No explicit acknowledgment that Tier 3 memory has higher quality risk than Tier 1 and requires different validation strategies.

The repo has the storage infrastructure ([[docs/canonical/tiered-context-storage|Tiered Context Storage]], [[docs/canonical/external-state-persistence|External State Persistence]]) and the provenance tracking ([[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]). What is missing is the authority dimension — the explicit gradient of who decides what to persist and the adoption path from user-controlled to agent-controlled memory.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Measurably improves resolution rate through memory-driven personalization — greeting by name, recalling preferences, adapting tone | Tier 3 (implicit memory) can capture incorrect or sensitive information without user awareness — the agent may "remember" a false preference or private detail |
| Incremental adoption path from safe (Tier 1) to automated (Tier 3) — deploy Tier 1 immediately, add Tier 2 as domain knowledge matures, enable Tier 3 selectively | Memory quality degrades as automation increases — Tier 3 requires more verification than Tier 1, and verification mechanisms must be tier-aware |
| Explicit authority gradient makes memory decisions auditable — you can trace "why did the agent remember this?" to user instruction, builder declaration, or agent inference | Memory bloat: without pruning across tiers, accumulated memories degrade retrieval relevance regardless of authority source |
| Treats memory as first-class platform primitive, not an afterthought — the three-tier architecture forces explicit design decisions about what to remember and why | Platform-level memory requires integration with identity resolution — see [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] |

## Relationship to Other Patterns

- **Composes with:** [[docs/canonical/tiered-context-storage|Tiered Context Storage with Promotion/Demotion]] — authority tiers (who decides) × storage tiers (how fast) form a two-dimensional memory architecture.
- **Uses:** [[docs/canonical/external-state-persistence|External State Persistence]] — the persistence mechanism for all three authority tiers.
- **Requires:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — structured retrieval handles for memories across all tiers.
- **Builds on:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — provenance tracking provides the audit trail for authority decisions (this memory came from user instruction vs. builder schema vs. agent inference).
- **Requires:** [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] — identity coupling gates which memories are retrieved for which user, across all authority tiers.

## References

-  lines 371-395 — extracted pattern with three-tier authority gradient, adoption path, quality risk profile.
-  lines 209-220 — Partial Coverage classification with evidence of storage tiers but missing authority gradient.
- [[docs/canonical/tiered-context-storage|Tiered Context Storage with Promotion/Demotion]] — existing storage tier infrastructure.
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — existing provenance tracking.
- [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] — identity coupling for memory retrieval.
- Sierra transcript: "Tier 1: user says remember this. Tier 2: builders declare what matters upfront. Tier 3: agent decides what to remember." — Wedeen on the authority gradient.
- Sierra transcript: "Measurably improved resolution rate through greeting by name, recalling previous call topics, recognizing frustrating past interactions." — Wedeen on measurable impact.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
