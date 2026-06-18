---
title: "Neutral Selection Layer"
type: canonical
tags: ["context-engineering", "agentes-orquestracao", "harness-engineering"]
aliases: ["model-agnostic context layer", "vendor-independent selection", "portable context format", "neutral context layer"]
last_updated: 2026-06-18
relates-to: ["[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]"]
sources: ["[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|Memory Selection Problem Analysis]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]"]
---
# Neutral Selection Layer

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-18-memory-selection-problem/
**Classification:** Missing (P0)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Organizations accumulate context as their most durable asset in agentic systems. Models change, architectures evolve, vendors come and go — what persists is the structured record of what agents have learned. But soldering context strategy to vendor-specific memory features makes that asset a hostage to someone else's roadmap: the context that the organization built over months stops working the moment a model is swapped, a vendor deprecates an API, or a new agent needs to reason across sessions that used different models.

The repo's context architecture — [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]], [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]], [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — is designed for a single agent/context flow within a single model ecosystem. There is no model-agnostic, vendor-independent context selection layer. Context is structured for the agent that produced it, not for any agent that might consume it.

## Solution

A model-agnostic selection layer that sits between the model and the store, serving context through a uniform interface regardless of which model, vendor, or session requests it. Three properties define the layer:

1. **Neutral**: Not coupled to a single model. Context is a portable organizational asset, not a hostage to a vendor roadmap. The same context serves any model, present and future.
2. **Horizontal**: Cross-agent, cross-session, cross-model. A system-of-record that no single framework, app, or lab can sustain alone — each only sees its own slice.
3. **Structured**: Relational, not merely storage. Dependencies, provenance, and supersession as typed edges in the context graph.

**Key components:**

- **Model-Agnostic Context Format**: Standardized schema for context units that any model can consume, independent of vendor-specific memory APIs.
- **Context Router**: Receives context queries from any agent/model and routes them to the appropriate selection strategy.
- **Multi-Tenant Registry**: Tracks which context belongs to which agent, session, and model; enforces isolation and sharing policies.
- **Vendor Adapter**: Translates the model-agnostic format into each model's native input format.

**Flow:**
1. Agent generates context unit in model-agnostic format — store in the neutral layer.
2. Any agent (same or different model) queries the selection layer for relevant context.
3. Context Router resolves the query against the relational context graph and tiered storage.
4. Selected context is assembled in the model-agnostic format.
5. Vendor Adapter translates to the target model's native input format.
6. Context is injected into the model's prompt; model reasons and produces output.

## Implementation in this repo

### What already exists

NOT_FOUND across all 85 canonical docs. The repo has philosophical alignment with vendor independence:

- [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] treats code as disposable build artifact and constraints as durable — a compatible philosophy: what survives model migrations should be the durable layer, not the generated output.
- The repo's context infrastructure provides building blocks ([[docs/canonical/hybrid-context-stack|Hybrid Context Stack]], [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]], [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]) but none were designed for cross-model portability.

No standardized context format for multi-model consumption exists. No context router separates query resolution from model-specific translation. No multi-tenant registry tracks ownership across agents, sessions, and models.

### What is missing

1. **Model-Agnostic Context Format**: No standardized schema for context units consumable by any model without vendor-specific translation.
2. **Context Router**: No routing layer that maps agent/model queries to selection strategies independently of the target model.
3. **Multi-Tenant Registry**: No tracking of context ownership by agent, session, and model with isolation and sharing policies.
4. **Vendor Adapter**: No translation layer that converts from agnostic format to model-native input (system prompt, tool definitions, context injection point).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Context survives model migrations — same structured record serves any model | Requires building and maintaining the layer; integration with each model is manual |
| Cross-agent coherence: agents share a unified view of organizational context | Higher initial engineering cost compared to using built-in vendor memory features |
| Vendor independence: the organization's most durable asset is not locked in | Becomes a single point of failure for context delivery if not replicated |
| Composable: the selection layer can evolve independently of both models and storage | The abstraction boundary adds latency — every context query traverses the layer |

## Relationship to Other Patterns

- **Philosophically aligned with:** [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] — both treat generated artifacts as disposable and constraints/formats as durable.
- **Wraps:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] and Tiered Context Storage, providing the vendor-independent interface above them.
- **Uses:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] for stable retrieval handles that survive model migrations.
- **Extends:** [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] by adding model-agnostic format translation.
- **Enables:** Cross-model Deliberate Forgetting and Smallest Sufficient Context by providing a unified format for relevance scoring and selection.

## References

- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis|analysis]] — three properties of the selection layer (neutral, horizontal, structured).
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|patterns]]:199-244 — extracted Neutral Selection Layer pattern definition.
- [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|classification]]:129-151 — Missing classification with locations searched and missing mechanics.
- [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]:25 — model output as disposable artifact, constraints as durable.

---

*Created: 2026-06-18 | From: Memory Selection Problem pattern classification | Precedence: canonical*
