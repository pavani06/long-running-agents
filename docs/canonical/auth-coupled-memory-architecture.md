---
title: "Auth-Coupled Memory Architecture"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["agentes-orquestracao", "governanca"]
aliases: ["auth-coupled memory", "identity-gated memory", "memory authentication coupling", "authenticated memory retrieval"]
relates-to: ["[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/three-tier-memory-persistence|Three-Tier Memory Persistence]]", "[[docs/canonical/regulated-data-boundary|Regulated Data Boundary]]"]
---

# Auth-Coupled Memory Architecture

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Missing (P0)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Memory products treat storage and retrieval as independent of identity, but extracting the right memories requires knowing *who* the caller is. A memory system that stores everything and serves it on request is architecturally incomplete — it has no way to distinguish "memories belonging to Harrison" from "memories belonging to anyone named Harrison." Identity resolution and memory retrieval are coupled concerns. Decoupling them produces either insecure retrieval (wrong person's memories served) or useless retrieval (no memories served because identity cannot be confirmed).

Wedeen explains why standalone memory startups haven't broken out: "If I want to buy memory from you, I also need to buy authentication from you." Consumer products like ChatGPT can offer memory freely because users already trust them with identity (they're logged in). B2B vendors face a higher bar: they must couple memory with identity verification, and the coupling must be architectural, not just procedural.

The deeper problem is that not all memories carry equal sensitivity. Recalling "thanks for calling again, Harrison" requires low authentication confidence — getting this wrong is mildly embarrassing. Recalling "your SSN is XXX-XX-1234" requires high authentication confidence — getting this wrong is a compliance and security incident. The memory system needs a sensitivity gradient that gates retrieval by authentication confidence level.

## Solution

An auth-coupled memory architecture where memory storage, retrieval, and sensitivity gating are all keyed by identity. The system maintains an authentication confidence score that gates which memory tier can be accessed — low-confidence identity gets low-sensitivity memories; high-confidence identity gets full access.

**Key components:**

1. **Identity resolution as memory key**: Every memory item is stored with an identity key (phone number, account ID, session token, or device fingerprint). Retrieval always includes an identity resolution step — "who is this?" — before "what do we know about them?"

2. **Authentication confidence score**: Identity resolution produces a confidence score, not a binary yes/no. Calling from a known phone number with a valid session token = high confidence. Calling from an unknown number = low confidence. The confidence score gates what memory tier can be accessed:
   - Low confidence → Tier 1 (explicit, user-initiated memories like "remember my name is Harrison").
   - Medium confidence → Tier 2 (builder-defined memories like purchase history, preference schema).
   - High confidence → Tier 3 (agent-decided implicit memories, sensitive data like SSN or medical history).

3. **Memory sensitivity gradient per business domain**: Each domain defines its own sensitivity policy. In e-commerce, recalling shipping addresses requires medium confidence. In healthcare, recalling medication history requires high confidence. The sensitivity gradient is a business decision, not a technical one — the architecture provides the mechanism; the domain owner provides the policy.

4. **Refusal of decoupled memory products**: The architecture explicitly rejects standalone memory products that lack identity coupling. Memory without authentication is like a file system without permissions — technically functional but operationally useless for multi-tenant production systems.

**The identity-memory coupling in practice (Sierra's use case):**

1. A customer calls. The system performs identity resolution: phone number lookup, account matching, session token validation.
2. The resolution produces an authentication confidence score: 0.95 (high — known phone number, valid session).
3. The memory system gates retrieval: at 0.95 confidence, all memory tiers are accessible. The agent greets the customer by name, recalls their last order, and surfaces their loyalty status.
4. If the resolution produces 0.4 confidence (unknown number, no session), only Tier 1 memories are served. The agent greets generically until the customer provides identifying information.
5. As the conversation progresses and identity is confirmed (the customer provides their account number), the confidence score rises, and Tier 2+3 memories become available.

**Why consumer products have an advantage here:** ChatGPT and Claude can offer memory for free because the user is already authenticated — they have a login, a session, an account. B2B agents serving phone calls, chat widgets, or API integrations must build their own identity resolution layer. This is the "higher bar" Wedeen describes: consumer memory products ship with identity; enterprise memory products must build it.

## Implementation in this repo

### What already exists

NOT_FOUND across `docs/canonical/`, `curriculum/`, `system-of-record.md`, and `.opencode/skills/`.

- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]: Catalog of omitted context with `id`, `location`, `preview`, `scope`, `fetch`. Memory is addressable but not identity-keyed.
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]: Graph of memory with epistemic status and provenance. Tracks where knowledge came from but not who it belongs to.

### What is missing

From the classification: "No auth-to-memory coupling mechanism. No authentication confidence score. No memory sensitivity gating by authentication level (greeting by name = low auth bar, SSN-level memory = high auth bar). The repo's memory patterns treat memory as a purely technical problem without the identity/trust dimension."

1. **Identity-keyed memory storage**: Memory items have no identity dimension — they are keyed by topic, session, or pattern, not by user.
2. **Authentication confidence score**: No concept of graduated identity confidence that gates memory access.
3. **Memory sensitivity policy**: No gradient between "safe to serve at any confidence level" and "requires verified identity."
4. **Identity-memory coupling as architectural principle**: The repo's memory patterns ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]], [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]) treat memory as identity-agnostic, which is correct for a coding-agent harness (single user, authenticated by the IDE session) but insufficient for multi-tenant production agents.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Explains why standalone memory products need identity coupling — the market structure makes sense once you see the architectural dependency | Authentication is imperfect — phone numbers can be shared (office networks, family lines); confidence scoring must handle ambiguity gracefully |
| Enables graduated memory access: greet by name at low confidence, serve sensitive data only at high confidence | Requires explicit sensitivity policy per business domain — no one-size-fits-all gradient |
| Makes identity-memory coupling a first-class architectural concern, not an afterthought | Coupling increases integration cost: adopting memory means adopting identity infrastructure |
| Prevents cross-tenant memory leakage at the architectural level, not just the policy level | Not applicable to anonymous agents that don't persist per-user state — adds complexity without value for single-user systems |

## Relationship to Other Patterns

- **Extends:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — adds identity keys to the existing memory catalog structure.
- **Extends:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — adds identity provenance to the graph (not just "where did this knowledge come from" but "whose knowledge is this").
- **Complements:** [[docs/canonical/three-tier-memory-persistence|Three-Tier Memory Persistence]] — the three-tier authority gradient (user/builder/agent) maps to authentication confidence: Tier 1 (explicit) = low auth bar, Tier 3 (implicit) = high auth bar.
- **Requires:** [[docs/canonical/regulated-data-boundary|Regulated Data Boundary]] — high-sensitivity memories (SSN, health data) should live in infrastructure that never touches an LLM, following the same architectural isolation pattern.

## References

-  lines 423-448 — extracted pattern with identity resolution, authentication confidence, sensitivity gradient.
-  lines 231-236 — Missing classification with NOT_FOUND evidence.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — closest existing pattern (addressable but not identity-keyed memory).
- Sierra transcript: "If I want to buy memory from you, I also need to buy authentication from you." — Wedeen on the architectural coupling.
- Sierra transcript: "Thanks for calling again, Harrison requires less auth confidence than your SSN-related memory." — Wedeen on the sensitivity gradient.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
