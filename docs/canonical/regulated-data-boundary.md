---
title: "Regulated Data Boundary"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["agentes-orquestracao", "governanca"]
aliases: ["PCI boundary architecture", "regulated data isolation", "data boundary enforcement", "compliance isolation tier"]
relates-to: ["[[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection PII Prevention]]", "[[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]]"]
---

# Regulated Data Boundary

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Missing (P0)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

LLM providers are not certified for regulated data — no frontier model provider is PCI DSS Level 1 certified, HIPAA-compliant, or authorized to handle authentication tokens. Yet agents increasingly mediate transactions that involve payment information, personal health data, and authentication credentials. Routing all data through the LLM context window creates two problems: (1) regulated data enters an untrusted compute environment, violating compliance requirements, and (2) that data becomes part of the model's context, where it could influence generation in unpredictable ways or leak through prompt injection.

Policy controls alone are insufficient. A policy that says "don't put credit card numbers in prompts" is a rule, not an enforcement mechanism. The model might still surface regulated data through retrieval, or a prompt injection attack might extract it. The security boundary must be architectural — regulated data must live in infrastructure that never touches an LLM.

Sierra solved this by building PCI DSS Level 1 certified payment infrastructure where payment data is structurally isolated from LLM context. The agent can mediate a payment conversation and trigger a payment, but the payment itself executes in regulated infrastructure where no LLM has access. Wedeen describes this as a strategic bet: they built the isolation tier "before it made sense" because they believe agent-mediated commerce will soon exceed e-commerce volume.

## Solution

A regulated data boundary is an architectural isolation pattern: a separate infrastructure tier handling regulated operations that is physically isolated from LLM compute. The key insight is that the boundary is structural, not policy-based — data cannot cross it by accident or by prompt injection because there is no path for it to do so.

**Key components:**

1. **Isolated regulated infrastructure tier**: Separate compute, network, and storage environment with independent certification (PCI DSS Level 1, HIPAA, SOC 2). This tier runs deterministic, auditable code — no LLM components. It handles payment processing, authentication token validation, and other regulated operations.

2. **Boundary enforcement at the harness level**: The agent harness mediates between the conversational LLM loop and the regulated tier. When the conversation reaches a point where regulated data is needed (e.g., "I'd like to pay with credit card ending in 1234"), the harness routes the transaction to the regulated tier without passing card data through the LLM. The LLM might generate "Let me process that payment for you" but never sees the card number.

3. **Tokenized references crossing the boundary**: The LLM context may contain *references* to regulated data (e.g., a payment token, a customer ID), but never the regulated data itself. The regulated tier resolves references to actual data within its isolation boundary.

4. **Independent certification and audit**: Each boundary is independently certified. Adding support for a new regulated data type (e.g., HIPAA in addition to PCI) means certifying a new isolation tier, not modifying existing LLM prompts or policies.

**The boundary in practice (Sierra's use case):**

A customer conversation flows through the conversational agent (LLM). When the customer wants to make a payment:
1. The LLM recognizes the intent and signals the harness: "customer wants to pay."
2. The harness routes the payment request to the regulated payment tier — the LLM never sees the card number, CVV, or billing address.
3. The payment tier processes the transaction using certified infrastructure, returning a success/failure token.
4. The harness injects the result token back into the LLM context: "payment succeeded, confirmation #X."
5. The LLM generates a natural confirmation message to the customer.

At no point does a credit card number, CVV, or authentication token enter a model prompt. The architectural boundary is absolute.

**Why this is not just "PII filtering":** [[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection PII Prevention]] describes policy-based PII prevention — filter PII from context via data catalog tagging and pre/post-generation scanning. That is a *policy* control (rules about what can and cannot be in context). The regulated data boundary is an *architectural* enforcement mechanism (infrastructure where regulated data physically cannot reach an LLM). Policy controls can fail or be bypassed; architectural isolation cannot be bypassed because there is no path.

## Implementation in this repo

### What already exists

- [[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection PII Prevention]]: Policy-based PII prevention via context injection rules. Data catalog PII tagging, pre-generation injection, post-generation deterministic scan as safety net, audit record per query. This is a policy control, not architectural isolation.

### What is missing

From the classification: "The closest match is policy-based PII prevention via context injection rules. This is a policy control (filter PII from context), not an architectural isolation pattern (separate infrastructure cluster for regulated data). The Sierra pattern — PCI DSS Level 1 isolated payment infrastructure where payment data never touches an LLM — has no equivalent."

1. **Isolated regulated infrastructure tier**: No separate infrastructure with independent certification for regulated data. All data paths flow through or near LLM context.
2. **Architectural boundary enforcement**: No structural guarantee that regulated data cannot enter LLM context. The repo relies on policy controls (PII tagging, scanning) rather than infrastructure gaps.
3. **Tokenized reference pattern**: No concept of LLM context containing only references (tokens, IDs) while regulated data stays in isolated infrastructure.
4. **Per-boundary certification**: No infrastructure designed for independent compliance certification (PCI, HIPAA, SOC 2).

The repo's coding-agent harness focus means it does not handle payment data, health records, or authentication tokens in production. The PII prevention canonical doc covers the coding-agent domain adequately. This pattern becomes relevant if the harness is extended to production agent deployments that mediate transactions.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Enables agent-mediated commerce where no LLM provider is PCI-certified — the isolation tier, not the LLM, carries the compliance burden | Adds infrastructure complexity: separate regulated data tier with independent certification, monitoring, and audit |
| Architectural isolation is absolute — regulated data cannot reach an LLM because there is no path | Some agent interactions genuinely require regulated data in context (e.g., the agent needs to verify a specific transaction amount); tokenized references may not be sufficient |
| Built before demand materializes as a strategic bet on agent-mediated commerce growth | Certification processes (PCI, HIPAA) are long and expensive — upfront investment before revenue justifies it |
| Same pattern applies to auth-gated memory — see [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] | Not needed for agents that never touch regulated data; adds architectural weight without value for purely informational agents |

## Relationship to Other Patterns

- **Complements:** [[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection PII Prevention]] — policy controls (PII filtering) are the safety net for non-regulated data; architectural isolation is the enforcement mechanism for regulated data. Both layers should exist.
- **Enables:** [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] — the same isolation architecture applies to authentication-gated memory. Data that must never enter an LLM context window (SSN-level memories, auth tokens) gets isolated infrastructure, not just policy controls.
- **Requires:** Harness-level routing — the agent harness must classify conversation turns and route regulated operations to the isolation tier without exposing raw data to the LLM. This is a harness engineering concern, not a model concern.

## References

-  lines 397-421 — extracted pattern with isolated infrastructure tier, boundary enforcement, PCI DSS Level 1 certification.
-  lines 223-228 — Missing classification with evidence of policy-only coverage.
- [[docs/canonical/governance-context-injection-pii-prevention|Governance Context Injection PII Prevention]] — closest existing pattern (policy control, not architectural isolation).
- Sierra transcript: "We built PCI DSS Level 1 certified payment infrastructure where payment data never touches an LLM. We built it before it made sense strategically." — Wedeen on the strategic bet.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
