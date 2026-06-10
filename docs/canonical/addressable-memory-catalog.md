---
title: "Addressable Memory Catalog"
type: canonical
aliases: ["memory catalog", "addressable memory"]
tags: ["context-engineering"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]"]
sources: ["[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis|Context Management Analysis]]"]
---
# Addressable Memory Catalog

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-09-how-we-solved-context-management-in-agents/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

External memory does not help an agent if the agent cannot decide what to retrieve without reloading the entire omitted history into the prompt. A memory store that only says "old messages exist" turns recoverability into guesswork.

The agent needs a compact way to inspect omitted content, choose relevant items, and fetch exact details on demand. Without that interface, truncation remains lossy in practice even if the raw data exists somewhere outside the active context.

## Solution

Represent omitted context as an addressable catalog. Each omitted message, tool call, span, prompt fragment, trace segment, or intermediate result receives a stable identifier plus enough metadata for the agent to choose what to fetch.

Minimum catalog fields:

| Field | Purpose |
|---|---|
| `id` | Stable handle for retrieval and audit |
| `kind` | Message, tool call, trace span, prompt, result, decision, or artifact |
| `location` | Turn number, span position, timestamp, distance from current turn, or source path |
| `preview` | Small relevance hint sized to guide retrieval without recreating context bloat |
| `scope` | Session, user, task, trace, or privacy boundary |
| `fetch` | Tool contract or storage pointer used to recover exact content |

The catalog itself can be injected into active context because it is compact. Exact content stays outside the prompt until the agent selects one or more IDs. Retrieval then returns the selected item, not the whole archive.

Preview size is the core design tension. Too little preview hides relevance; too much preview turns the catalog into another large context blob. The catalog should therefore be optimized as an interface for decision-making, not as a summary of everything that happened.

## Implementation in this repo

### What already exists

The repo has several adjacent mechanisms:

- Context Management teaches vector retrieval over conversation chunks, documents, events, query ranking, and filters (`curriculum/05-core-concepts/01-context-management.md:580`).
- The same curriculum warns that retrieval can return a similar but wrong chunk and needs privacy and scope filters (`curriculum/05-core-concepts/01-context-management.md:600`).
- Multi-agent coordination uses `output_ref` handles for internal agent outputs (`curriculum/05-core-concepts/07-multi-agent-coordination.md:552`).
- State persistence asks for a human-readable manifest listing files and decisions used by a response (`curriculum/05-core-concepts/05-state-persistence.md:1864`).
- The source analysis identifies IDs, conversational location, message distance, and previews as the concrete memory-store interface (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:82`).

### What is missing

The classification found no explicit pattern for an omitted-memory catalog with `id + location + preview` in the canonical docs, curriculum, evidence, decisions, or operational skills (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/classification.md:32`). Existing retrieval material is broader and usually semantic; this pattern needs a deterministic catalog for truncated context recovery.

The missing implementation details are:

1. A catalog schema for omitted in-session content.
2. A retrieval contract that fetches exact content by stable ID.
3. Guidance for preview length, privacy scope, and stale-item handling.
4. Observability that records which catalog IDs were offered and which were fetched.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Makes omitted content discoverable without reloading everything | Requires catalog generation and metadata maintenance |
| Enables exact recovery instead of relying only on summaries | The agent can still choose the wrong ID |
| Improves auditability of what was omitted and what was later restored | Preview design is a hard product and token-budget tradeoff |
| Works with both truncation and sub-agent outputs | Requires scope and privacy controls on retrievable items |

## Relationship to Other Patterns

- **Enables:** Head-Tail Context Truncation with Recoverable Middle, because the recoverable middle needs an addressable interface.
- **Strengthens:** Late-Failure Regression Suite, because regressions can record missing or misused catalog IDs as root cause evidence.
- **Complements:** Context-Scoped Sub-Agent Delegation, because sub-agents can return compact `output_ref` entries rather than full intermediate context.
- **Contrasts with:** Pure vector retrieval, because this catalog exposes known omitted items by handle instead of only similarity search.
- **Bounded by:** Memory Tier Separation, because a truncation catalog is not automatically long-term memory.

## References

- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:82` — memory store with IDs, position, and preview.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/patterns.md:37` — extracted reusable pattern.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/classification.md:20` — Partial Coverage classification and gap.
- `curriculum/05-core-concepts/01-context-management.md:580` — existing retrieval coverage.
- `curriculum/05-core-concepts/01-context-management.md:600` — retrieval risk and scope-filter coverage.
- `curriculum/05-core-concepts/07-multi-agent-coordination.md:552` — existing `output_ref` handle practice.
- `curriculum/05-core-concepts/05-state-persistence.md:1864` — manifest and response-reference discipline.

---

*Created: 2026-06-10 | From: Context Management pattern classification | Precedence: canonical*
