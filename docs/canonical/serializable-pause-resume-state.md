---
title: "Serializable Pause/Resume State"
type: canonical
aliases: ["pause resume", "serializable state"]
tags: ["agent-loop", "12-factor-agents"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[curriculum/03-nivel-3-advanced-architecture/02-state-persistence|State Persistence Lesson]]"]
sources: []
---
# Serializable Pause/Resume State

**Type:** Canonical Pattern
**Status:** Active
**Source:** Dex Horthy — "12-Factor Agents" (AI Engineer, 2025), adapted for long-running-agents
**Classification:** Partial Coverage — repo has richer state model, but different mechanism (per `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md`)
**Precedence:** Level 2 (`docs/system-of-record.md:8`)

---

## Problem

Long-running tools (async API calls, human approval waits, scheduled tasks) cannot complete inside a single synchronous model call. The agent must:

1. Launch the work
2. Pause its context
3. Resume later when the result arrives
4. Continue as if nothing happened

Without a serialization mechanism, pauses cause state loss — the agent "forgets" what it was doing.

## Solution

Serialize the entire agent state (context window + execution state + business state) to persistent storage. On resume, deserialize and continue from exactly where the agent paused.

### 12FA Approach: Context Window Serialization

```
PAUSE                          RESUME
  │                              │
  ▼                              ▼
┌─────────────────┐    ┌─────────────────┐
│ Context Window   │    │ Context Window   │
│ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ messages[]   │ │    │ │ messages[]   │ │ ← restored exactly
│ │ state        │ │    │ │ state        │ │
│ │ position     │ │    │ │ position     │ │
│ └─────────────┘ │    │ └─────────────┘ │
│       │         │    │       ▲         │
│       ▼         │    │       │         │
│  Serialize → DB │    │  Deserialize    │
└─────────────────┘    └─────────────────┘
        │                       │
        └─────── PAUSE ─────────┘
              (hours/days)
```

The key property: **the agent doesn't know it was paused**. Context is bit-for-bit identical before and after.

### long-running-agents Approach: State Rebuild

The repo uses a different mechanism with different tradeoffs. Instead of serializing the context window, it **rebuilds state from scratch** each turn.

```
EVERY TURN
  │
  ▼
ConversationStateBuilder.buildState()
  ├── 15+ parallel queries to PostgreSQL, Redis, Pinecone
  ├── Reconstructs: user profile, cart, history (60 msgs), memories, orders
  ├── Applies: current metadata, onboarding constraints, conversation phase
  └── Returns: complete AgentState
  │
  ▼
LangGraph StateGraph (compiled WITHOUT checkpointer)
  └── State lives in DB, not in serialized graph state
```

## Comparison

| Aspect | 12FA Serialization | long-running-agents Rebuild |
|---|---|---|
| **Mechanism** | Save context window bytes to DB | Query 15+ tables and rebuild |
| **State richness** | What fits in the context window | Full relational model (50+ Prisma models) |
| **Pause transparency** | Agent sees same context before/after | Context is reconstructed, may differ subtly |
| **Portability** | Context blob is portable across systems | Tightly coupled to DB schema |
| **Storage cost** | One blob per pause | Distributed across normalized tables |
| **Resume latency** | One deserialize call | 15+ parallel queries (~400ms) |
| **Token fidelity** | Exact — no information loss | Approximate — limited to what queries return |

## When to use each

| Scenario | Recommended approach |
|---|---|
| Mid-reasoning interruption (user closes chat, returns hours later) | **12FA Serialization** — token-level fidelity matters |
| Standard turn-based conversation | **Repo Rebuild** — richer state model matters |
| Cross-system migration (moving agent between servers) | **12FA Serialization** — portable blob |
| Multi-agent coordination (agent A pauses, agent B continues) | **Repo Rebuild** — DB is the shared coordination layer |
| Audit trail required | **Repo Rebuild** — normalized state is queryable |

## Implementation in long-running-agents

### What already exists (Partial Coverage + Better Implementation potential)

The repo implements far richer state persistence than the 12FA pattern describes:

- **4 persistence layers**: semantic memory, conversation context, transactional state, cache (`docs/analysis/mhc-backend/2026-05-26-harness-diagnostic.md:132-169`)
- **PostgreSQL multi-table** with Prisma (50+ models)
- **Memory extraction** via secondary LLM (`gpt-4.1-mini`) in background
- **Time-based expiration** and contradiction detection
- **Core Concept 5 (State Persistence)** in the curriculum

### What's different

The repo's `ConversationStateBuilder.buildState()` rebuilds state from scratch each turn — 15+ parallel queries, no LangGraph checkpointer. The harness diagnostic explicitly confirms:

> "Sem checkpointer no LangGraph. O estado é reconstruído do zero a cada turno pelo ConversationStateBuilder." (`docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence.md`)

### Gap and opportunity

The repo's approach works well for its domain (turn-based WhatsApp conversations) but doesn't support **mid-reasoning pause/resume with token-level fidelity**. If the agent is mid-search (3 products found, about to compare prices) and the user's connection drops, the repo can't resume from that exact reasoning state — it can only rebuild from DB state and start the turn fresh.

The 12FA serialization pattern would add a **complementary mechanism** for scenarios where token-level fidelity across pauses matters. It would not replace the existing state model — it would sit alongside it as an option for specific use cases.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Supports launch/pause/resume like standard APIs | Requires application to own serialization |
| Enables long-running async workflows | Requires reliable state IDs and callback plumbing |
| Agent unaware of pause — seamless continuation | Context blob can be large (10K-100K tokens) |
| Portable across systems | Must distinguish execution state from business state |

## Relationship to Other Patterns

- **Depends on:** Pattern 5 (Token-Level Prompt & Context Builder) — must own the context window to serialize it
- **Complements:** Pattern 3 (Owned Agent Control Loop) — the loop's `pause` intervention point triggers serialization
- **Strengthens:** Pattern 8 (Micro-Agent Islands in DAG) — each island can pause/resume independently
- **Contrasts with:** Repo's State Rebuild approach — different mechanism, different tradeoffs, complementary

## References

- `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md` — classification as Partial Coverage
- `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-patterns.md` — pattern 4 definition
- `docs/analysis/mhc-backend/2026-05-26-harness-diagnostic.md` — Padrao 3, state persistence layers
- `docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence.md` — confirmation of no LangGraph checkpointer
- `curriculum/05-core-concepts/05-state-persistence.md` — Core Concept 5

---

*Created: 2026-06-09 | From: Pattern Classification analysis | Precedence: canonical*
