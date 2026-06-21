---
title: 'Budget-Aware Session Handoff'
type: canonical
aliases: ["handoff por orcamento", "budget-driven handoff", "session transition", "troca de sessao"]
tags: ["context-engineering", "agentes-orquestracao"]
last_updated: 2026-06-19
relates-to: ["[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
---

# Budget-Aware Session Handoff

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] and [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]
**Classification:** Partial Coverage ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:104-112)
**Precedence:** Level 2 canonical documentation per [[docs/system-of-record|System of Record]]:14-21 and [[docs/system-of-record|System of Record]]:124-166

---

## Problem

Long-running agents often treat session transition as a failure mode: the context crashes, quality degrades, or the user sees a discontinuity after the model has already run out of usable context. The token-budgeting source says token exhaustion appears before hard failure as shorter answers, rushed assumptions, reduced empathy, and weaker reasoning, so waiting for visible degradation is already late ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:121-128; [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:510-519).

The missing canonical contract is not generic pause/resume. The repository already covers serializing context window, execution state, and business state for pause/resume ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-57), includes handoff as an explicit loop-controller output ([[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:53-64), connects external state to pause/resume and writeback ([[docs/canonical/external-state-persistence|External State Persistence]]:95-100), and defines recoverable memory handles ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43). What was NOT_FOUND is a handoff trigger tied to token red phase, burn-rate forecast, or active-budget reset ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:104-112).

Without this pattern, a system can have durable state and still choose the wrong moment to use it: it may keep compressing a red-phase session until semantic loss accumulates, or start a fresh session without carrying the objective, open decisions, durable facts, summary buffer, and recoverable handles required for continuity ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:214-235).

## Solution

Make handoff a first-class budget action emitted by the owned loop when token health reaches the red phase. The control plane should treat `new_session` or `handoff` as an intentional product and orchestration flow, not as a crash-recovery path. The source model maps low budget to preparing transition, warning the client that a new conversation is better, and saving state for future context ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:500-509). In the KODA example, red phase offers a new conversation or aggressive compaction, with explicit user-facing continuity messaging ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:555-566).

The canonical flow is:

```
Token Budget Ledger
  |
  v
Burn-Rate Forecast
  |
  v
Token Health Monitor
  |
  +-- green/yellow --> continue or monitor
  |
  +-- orange -------> summarize, compress, or externalize
  |
  +-- red ----------> build handoff payload
                         |
                         v
                 Fresh Session / Next Agent
                         |
                         v
                 Active Context Budget Reset
```

A budget-aware handoff has four required outputs:

| Output | Contract | Evidence |
|---|---|---|
| Handoff trigger | The loop emits handoff when red-phase budget, burn-rate acceleration, or projected runway makes same-session continuation unsafe | [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:214-230; [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-509 |
| Fresh-session payload | The next session receives durable facts, current objective, open decisions, latest state, summary buffer, recoverable memory handles, and handoff instructions | [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:218-226 |
| Continuity message | The user or downstream system sees a deliberate transition rather than a hidden truncation or degraded continuation | [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:223-230; [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:561-565 |
| Budget reset | The active context budget is reset by starting a fresh context with only essential state carried forward | [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:171-179; [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:223-230 |

## Handoff Payload Contract

The handoff payload is not the old transcript. It is a compact, auditable start payload for the next session, agent, or orchestration branch. It should include:

| Field | Purpose | Source pattern |
|---|---|---|
| `trigger` | Trigger type: "manual" (user command), "red-phase" (budget ≤20%, automatic), "orange-phase" (budget ≤40%, state preparation), or "user-request" (another skill/agent). When red-phase, burn-rate and runway reason are recorded via `budget_context`. The full trigger schema is in session-handoff/SKILL.md:212. | Phase-gated token health returns phase, action, and reason ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:59-79) |
| `objective` | Preserves the current user goal or task frame | Budget-aware handoff inputs include current objective and latest state ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:218-226) |
| `relates-to` | Cross-vault wikilinks to durable facts (constraints, preferences) in `facts/<repo>/` and canonical docs in knowledge vaults. Facts are persisted separately via `appendFact()`, not embedded in the handoff frontmatter. | Durable facts survive windowing, summarization, and session transition ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:81-101) |
| `summary_buffer` | Compresses older continuity without spending the new session on full history | Summary buffer creates a portable handoff artifact for new sessions or sub-agents ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:125-145) |
| `memory_handles` | Points to exact recoverable source content that the new session can fetch on demand | Addressable memory uses stable `id`, `kind`, `location`, `preview`, `scope`, `tool`, and `path` fields ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43). The `tool` field specifies the concrete retrieval tool (only `"read"` for automatic fetch), and `path` is the workspace-relative file path validated against an allowlist with realpath canonicalization |
| `open_decisions` | Names unresolved decisions, pending approvals, or next actions so the new session does not restart planning from scratch | The owned control plane makes loop decisions such as continue, pause, handoff, or terminate explicit ([[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:53-64) |
| `continuity_message` | Explains the transition to the user or downstream agent without exposing internal token mechanics unnecessarily | The red-phase KODA example prepares a new specialist handoff message ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:555-566) |

**Nota:** A tabela acima é o contrato canônico mínimo. O schema completo do frontmatter tem 27 campos — ver `session-handoff/SKILL.md:204-227` para a especificação completa. Campos adicionais incluem: `id`, `title`, `type`, `date`, `agent`, `repo`, `status`, `tags`, `budget_context` (burn_rate, accelerating, phase_reason, recovered, previous_error), `planned_budget`, `next_action`, `execution_graph` (futuro), `current_node` (futuro), `relevance_log`, `reflected_at`, `reflection_batch`.

## Implementation in this repo

### What already exists

- [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]] already defines the persistence primitive for saving context window, execution state, and business state before resuming later ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-57).
- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]] already names `handoff` as a loop-controller output alongside continue, summarize, judge, pause, approve, and terminate ([[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:53-64).
- [[docs/canonical/external-state-persistence|External State Persistence]] already separates durable agent memory from model memory and says persistent state survives truncation, pauses, and cross-session return ([[docs/canonical/external-state-persistence|External State Persistence]]:29-57).
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] already defines the recoverable-memory interface needed for a compact payload that can fetch exact omitted content later ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] already requires stable harness prompt, head, tail, omitted middle, tool or trace bulk, and durable state to be separate context-builder blocks with distinct reduction policies ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41).

### What this document adds

1. It makes red-phase token health a valid handoff trigger instead of treating handoff only as a human, workflow, or failure-control event ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:104-112).
2. It defines the fresh-session payload as the product of durable facts, current objective, open decisions, latest state, summary buffer, recoverable memory handles, and explicit handoff instructions ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:218-226).
3. It makes active-budget reset an explicit success condition: the new session starts with essential state carried forward, not with the exhausted context window copied forward ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:223-230).

### What was built from this (2026-06-16 — 2026-06-19)

The following runtime components now implement this canonical contract:

- **`session-handoff` skill** (`~/.config/opencode/skills/session-handoff/SKILL.md`, 815 lines): Automates handoff with 4 trigger types, 27-field frontmatter, secret redaction, and durable fact persistence via `obsidian-eval`.
- **`handoff-path.sh`** (`~/scripts/sisyphus/handoff-path.sh`): Deterministic filename generator with UTC timestamps, preventing same-day collisions. Single source of truth for handoff naming.
- **`budget-monitor` skill**: Integrates token budget monitoring with red-phase automatic handoff via real tokenizer (`@goliapkg/tiktoken-wasm`).
- **Vault `sisyphus-runtime`**: 42 handoffs persisted across 6 repos, 33 in `_global/`.
- **Cross-session learning loop**: `reflection-runner` (crontab 09:00 BRT) → `facts/_global/principles.md` → `canonical-context` injection in next session.

### Naming contract (2026-06-19)

The `session-handoff` skill delegates filename generation to `~/scripts/sisyphus/handoff-path.sh` — a deterministic script that is the single source of truth for handoff naming:

```
handoff-path.sh <repo> <agent>
→ sessions/<repo>/<YYYY-MM-DD-HHMMSS-utc>-<agent>-handoff.md
```

This architectural decision (Camada C — Prevention) removes the degree of freedom that caused same-day handoff collisions. The script is complemented by a post-write validation (Camada B — Safety net) that fails the handoff if the written path doesn't match the expected path, ensuring no silent deviation.

## Tradeoffs

| Decision | Benefit | Cost |
|---|---|---|
| New session instead of same-session continuation | Resets active context budget before quality collapse ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:171-179) | Requires enough state capture to avoid user-visible discontinuity ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:231-234) |
| Red-phase handoff instead of late crash recovery | Makes token exhaustion an intentional product or orchestration flow ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:227-230) | Thresholds can be too conservative if the token-health monitor is poorly calibrated ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:76-79) |
| Compact payload instead of full transcript copy | Keeps the fresh session small and auditable through summaries, durable facts, and memory handles ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:41-43) | Handoff quality depends on accurate summaries, durable facts, and handles ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:231-234) |
| Handoff before aggressive compaction | Avoids semantic loss when compaction is too late or too lossy ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:171-179) | May be more visible to the user than silent same-session compression ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:505-509) |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]], because handoff must be an explicit loop-controller output rather than a hidden framework side effect ([[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:53-64).
- **Uses:** [[docs/canonical/external-state-persistence|External State Persistence]] for durable facts and cross-session return, and [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] for exact recoverability of omitted content ([[docs/canonical/external-state-persistence|External State Persistence]]:29-57; [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- **Complements:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]], because budget-aware handoff is a transition to a fresh active budget, while pause/resume preserves state across interruption ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-57).
- **Extends:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] and [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]], because the fresh-session payload should preserve stable instructions and selected anchors while leaving omitted content recoverable by handle ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41; [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:26-39).

## References

- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:34-53 - token budgeting definition and available-space equation.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:143-165 - burn-rate definition and why it matters for planning compaction or strategy change.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:486-509 - red flags for intervention, including accelerated burn rate and preparation for transition below 20 percent available budget.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:555-566 - red-phase KODA flow with new conversation or aggressive compaction.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:39-48 - green/yellow/orange/red phase model.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:50-61 - viability calculator for remaining messages and minutes.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:119-128 - operational lessons that token exhaustion is degradation before crash and session transition can be intentional.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:225-227 - synthesis: layered context builder plus monitor decides when to continue, summarize, compress, or hand off.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:214-235 - extracted Budget-Aware Session Handoff pattern.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:104-112 - Partial Coverage classification and NOT_FOUND gap.

---

*Created: 2026-06-10 | From: Token Budgeting pattern classification | Precedence: canonical*
