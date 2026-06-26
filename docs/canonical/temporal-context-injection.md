---
title: "Temporal Context Injection"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["context-engineering", "agentes-orquestracao"]
aliases: ["temporal context timing", "phase-aware context injection", "just-in-time context", "compaction coherence"]
relates-to: ["[[docs/canonical/tiered-context-storage|Tiered Context Storage with Promotion/Demotion]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/deliberate-forgetting|Deliberate Forgetting]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]"]
---

# Temporal Context Injection

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Partial Coverage (High)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Injecting all relevant context at the start of a conversation turn overloads the prompt with information the model does not need yet — and may never need. But removing context that was previously present during prompt compaction creates incoherence when the model has already internalized the removed information and the updated prompt contradicts it. The timing of context injection matters as much as the content selection — and getting timing wrong produces two symmetric failure modes.

The first failure mode is prompt bloat: injecting everything upfront wastes tokens on context the model does not need for the current conversation phase. A customer asking "where's my order?" does not need the agent's full return policy, loyalty program details, and upsell scripts — they need their order status. But injecting nothing about returns means the agent cannot handle "actually, I want to return it" without a context reload.

The second failure mode is compaction incoherence: when prompt compaction removes context that was present earlier, the model may have internalized claims from that context. If the new, compacted prompt contradicts those internalized claims, the model experiences an internal consistency failure — it "remembers" something the current prompt says is false. This is the specific risk Wedeen identifies: "you don't want to yank context that contradicts an updated system prompt."

The Sierra insight is that context injection should be *temporally aware* — show the model everything it needs to do the right thing at each moment, but nothing more. And removal timing must account for what the model has internalized.

## Solution

Temporal context injection is a phase-aware strategy where context is injected only when the conversation phase makes it relevant, and context removal is guarded against compaction incoherence. The key design principle is that the model's working memory of earlier conversation phases is an architectural constraint — you cannot simply delete context the model has internalized and expect coherence.

**Key components:**

1. **Phase-aware context injection**: The conversation is classified into phases (greeting, intent gathering, problem diagnosis, resolution, confirmation, close). Each phase has a defined set of context that is relevant. Domain knowledge about return policies is injected during resolution phase, not during greeting. Customer loyalty status is injected during intent gathering, not after the problem is resolved.

2. **Just-in-time injection triggers**: Context is injected at phase transitions, not at turn start. When the conversation transitions from "intent gathering" to "problem diagnosis," the harness injects diagnostic procedures. When it transitions again to "resolution," it injects resolution options and policies. The agent always sees the right context for the current phase, without carrying context from three phases ago.

3. **Compaction coherence guard**: When prompt compaction removes context, the harness checks whether the removed context made claims that the current prompt might contradict. If the agent was told "the return window is 14 days" in an earlier phase and compaction removes that context, the new prompt must not claim "the return window is 30 days" without explaining the discrepancy. The guard prevents the internal coherence failure where the model "remembers" one thing but is told another.

4. **Temporal layering of context categories**: Different context categories have different temporal profiles:
   - **Persistent** (always present): Agent identity, brand voice, core behavioral rules.
   - **Phase-scoped** (present during relevant phase): Domain knowledge, procedures, policies relevant to the current conversation phase.
   - **Turn-scoped** (present for a single turn): Specific data lookups, tool outputs, intermediate reasoning results.
   - **Expired** (removed after phase): Context from a phase that has concluded and whose claims are not needed for future phases.

**How phase-aware injection works in practice (Sierra's use case):**

1. A customer conversation begins. The harness classifies the phase as "greeting." Only brand voice and identity context is injected.
2. The customer says "I want to return an item." Phase transitions to "intent gathering." The harness injects the return intent classification logic and initial questions to ask.
3. The customer provides the order number. Phase transitions to "problem diagnosis." The harness fetches order data and injects return eligibility rules.
4. The order is within the return window. Phase transitions to "resolution." The harness injects return procedure steps and removes the diagnostic questions from context.
5. The return is initiated. Phase transitions to "confirmation." The harness injects the confirmation template and removes the return procedure details — but the compaction guard verifies that no contradictory claims remain.

At each phase, the agent sees "everything it needs to do the right thing, but nothing more" (Wedeen's phrase).

## Implementation in this repo

### What already exists

From the classification, the concepts are distributed across 5+ docs:

- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]: Progressive disclosure pattern — context revealed in layers. Related but not temporally phased.
- [[docs/canonical/tiered-context-storage|Tiered Context Storage with Promotion/Demotion]]: Storage tiers with retrieval timing — the storage infrastructure for phase-scoped context.
- `curriculum/05-core-concepts/03-context-management.md`: Curriculum coverage of context management including temporal considerations.

### What is missing

From the classification: "No unified 'Temporal Context Injection' pattern. The specific insight that *when* you inject context matters as much as *what* you inject is distributed across docs without explicit temporal framing. No coverage of prompt compaction incoherence risk."

1. **Unified temporal injection pattern**: The concepts exist (phase relevance, progressive disclosure, storage tiers) but are not unified under the temporal framing. No single doc explains that injection timing is a first-class architectural concern.
2. **Phase-aware injection triggers**: No mechanism for classifying conversation phases and injecting phase-specific context.
3. **Compaction coherence guard**: No explicit check for contradictory claims between removed context and current prompt. The repo's compaction patterns ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]) address structure but not semantic coherence across compaction events.
4. **Temporal layering of context categories**: No explicit classification of context by persistence profile (persistent, phase-scoped, turn-scoped, expired).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Reduces prompt bloat by injecting context only when relevant — saves tokens and improves attention quality | Requires accurate phase classification — incorrectly predicted phase transitions inject wrong context or miss the right context |
| Preserves coherence across compaction events by guarding against contradictory claims | Context removal timing must avoid leaving contradictory signals — the guard adds inspection overhead per compaction |
| Enables single-agent architecture by managing what the agent sees at each moment — avoids sub-agent decomposition for context control | Phase transitions can be ambiguous — the boundary between "diagnosis" and "resolution" may not be clear in every conversation |
| Explicit temporal context categories make context engineering decisions measurable | Over-aggressive compaction can degrade understanding of earlier conversation turns if the agent's internalized model of those turns contradicts the compacted representation |

## Relationship to Other Patterns

- **Uses:** [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] — progressive disclosure provides the layered reveal mechanism; temporal injection adds the timeline dimension (when to reveal which layer).
- **Requires:** [[docs/canonical/tiered-context-storage|Tiered Context Storage with Promotion/Demotion]] — the storage infrastructure that holds phase-scoped context and retrieves it at phase transitions.
- **Complements:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] — temporal injection manages when context enters; truncation manages when context leaves.
- **Enables:** [[docs/canonical/deliberate-forgetting|Deliberate Forgetting]] — temporal injection's expired context category feeds into the deliberate forgetting engine for relevance-based discard.

## References

- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] — existing progressive disclosure mechanism.
- Sierra transcript: "Show agents everything they need to do the right thing, but nothing more — at each moment." — Wedeen on the temporal principle.
- Sierra transcript: "You don't want to yank context that contradicts an updated system prompt during compaction." — Wedeen on the compaction coherence risk.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
