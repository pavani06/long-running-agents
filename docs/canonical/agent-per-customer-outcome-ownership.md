---
title: "Agent-Per-Customer Outcome Ownership"
type: canonical
aliases: ["agent per customer", "customer-scoped agent", "per-customer persistent agent", "outcome ownership by customer agent"]
tags: ["agentes-orquestracao", "context-engineering", "production"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]]"
  - "[[docs/canonical/three-tier-memory-persistence|Three-Tier Memory Persistence]]"
  - "[[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
---

# Agent-Per-Customer Outcome Ownership

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Task-scoped agents lose context between interactions and own no outcome; transactional optimization leaves dormant customer value unactivated (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:69`).

Concrete scenario: a customer browsed financing options on the web eight months ago, called once two years ago about a trade-in, and walks into a showroom today. A task-scoped "answer this call" agent greets a stranger, quotes from scratch, and optimizes the single transaction. The web agent, the call agent, and the showroom agent each hit their local KPI while the years-long relationship — the only durable moat in multi-month purchase cycles — evaporates between handoffs.

Root cause: the agent is scoped by **task** instead of by **customer**. No component in the system (a) keys all cross-channel memory to one durable identity, (b) persists a long-term goal across years of interactions, or (c) holds any agent accountable for the customer's lifetime outcome. Kavak's framing at millions-of-customers scale: every day between 100,000 and 200,000 agents get instantiated, each dedicated to one customer with its own virtual machine (`docs/analysis/...-analysis.md:71-73`), each "obsessed" with that customer, each carrying a long-term goal of maximizing lifetime value rather than closing the current interaction (`docs/analysis/...-analysis.md:75-76`).

Before/after: before, success is measured transactionally (cars bought/sold, brake pads purchased); after, agents are assigned to the customer database with the task of maximizing lifetime value — a deliberate shift from transactional to relational metrics (`docs/analysis/...-analysis.md:28`). The economics justify it: activating even 1% of a dormant base via agent-driven relationship management is worth hundreds of millions (`docs/analysis/...-analysis.md:41`).

## Solution

Instantiate **one persistent agent per customer**, running on its own VM, with (1) every historical cross-channel interaction ingested into identity-keyed memory, (2) a long-term goal slot (maximize LTV, convert across products over time), (3) full company API/skill access, and (4) a portfolio constraint layer bounding per-customer optimization by systemic risk. Every new interaction is recorded back into memory; the long-term strategy adjusts under portfolio constraints (`docs/analysis/...-patterns.yaml:94-100`).

Concrete example — a per-customer agent manifest:

```yaml
# agent-manifest.yaml — one per customer, instantiated on wake
customer_agent:
  identity_key: "customer:MX-198.244.11"      # auth-coupled memory key
  vm: "vm-pool/standard-harness"               # own VM per instance
  goal:                                        # long-term, not per-task
    type: maximize_ltv
    horizon: years
    constraints: [portfolio_risk_ceiling, competing_offers_policy]
  memory:
    channels: [web, calls, whatsapp, showroom_visits]   # cross-channel, years back
    key: identity_key                          # retrieval gated by identity resolution
    tiers: [explicit, builder, implicit]       # three-tier persistence
  skills: [financing, trade_in_quoting, insurance, car_advisory]
  api_access: full-company-cli
  writeback: every_interaction -> memory
```

On each customer touchpoint, the same agent wakes (100k–200k instantiated daily), resolves identity, loads the full history, and acts toward the multi-year goal — recording the interaction before sleeping.

## Implementation in this repo

### What already exists

- `docs/canonical/auth-coupled-memory-architecture.md:24` — "Memory products treat storage and retrieval as independent of identity, but extracting the right memories requires knowing *who* the caller is." Identity resolution is the precondition for per-customer memory.
- `docs/canonical/auth-coupled-memory-architecture.md:36` — "Identity resolution as memory key: Every memory item is stored with an identity key (phone number, account ID, session token, or device fingerprint)." The identity key exists; the per-customer agent instance does not.
- `docs/canonical/three-tier-memory-persistence.md:51` — three-tier memory "measurably improved resolution rate" through greeting customers by name (Tier 1) and recalling previous call topics (Tier 1 + Tier 2): the persistence substrate a per-customer agent would read/write.
- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md:719` — "OBJETIVO: Construir relacionamento de longo prazo." The KODA N4 curriculum already teaches long-term relationship goals with LTV metrics.

### What is missing

From the classification justification (`docs/analysis/...-classification.yaml:87-92`):

1. **One persistent agent instance per customer on its own VM** — KODA is a single agent with per-customer state, not a fleet of per-customer agent instances each on its own VM.
2. **Years-spanning cross-channel ingestion** — no mechanism consolidating web visits, years-old calls, and showroom events into one per-customer memory at instantiation time.
3. **Outcome ownership by the per-customer agent** — no agent is accountable for the customer's lifetime outcome; repository agents own tasks, not customers.
4. **Portfolio constraint layer** — personalized pricing/risk optimization bounded by portfolio-level risk, competing offers, and portfolio health has no canonical treatment.

This doc is enrichment for the KODA N4 curriculum rather than a hole in existing coverage (`docs/analysis/...-classification.yaml:92`).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Complete customer history and infinite patience across multi-month decision cycles (`docs/analysis/...-patterns.yaml:80`) | Requires per-agent VM, memory, and evals — costlier than task agents (`docs/analysis/...-patterns.yaml:84`) |
| The relationship window becomes the moat instead of the transaction (`docs/analysis/...-patterns.yaml:81`) | Per-customer optimization must be bounded by portfolio-level constraints (risk, competing offers, portfolio health) (`docs/analysis/...-patterns.yaml:85`) |
| Activating 1% of a dormant base is worth hundreds of millions (`docs/analysis/...-analysis.md:41`) | Humans shift role to skill-builders for the agents (`docs/analysis/...-patterns.yaml:86`) |
| Agent persists context and owns outcomes (LTV) instead of losing both between handoffs (`docs/analysis/...-analysis.md:150`) | Fleet-scale instantiation (100k–200k/day) demands durable state and scheduling primitives the task-scoped design never needed |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] — identity resolution as memory key is what makes per-customer memory retrievable rather than leaky.
- **Depends on:** [[docs/canonical/three-tier-memory-persistence|Three-Tier Memory Persistence]] — the tiered retention policy is the storage substrate the per-customer agent reads and writes.
- **Complements:** [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]] — the long-term LTV goal is the hard goal that the customer-scoped agent persists toward; task-scoped agents cannot own outcomes.
- **Complements:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]] — a per-customer agent that wakes on customer touchpoints needs durable state across sleep cycles.

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:71-76` — agent-per-customer pattern, 100k–200k daily instantiations, persistent cross-channel memory with long-term goal.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:28,41` — relational metrics shift and dormant-base economics.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:68-100` — pattern inputs/outputs/components/flow.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:66-92` — Partial Coverage (Medium) classification with the evidence cited above.
- Source: a16z interview, channel and video_id per `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md:5-8`.
