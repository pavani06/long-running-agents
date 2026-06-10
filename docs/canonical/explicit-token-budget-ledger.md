---
title: "Explicit Token Budget Ledger"
type: canonical
aliases: ["registro de orcamento de tokens", "token ledger", "budget tracking"]
tags: ["context-engineering", "agentes-orquestracao"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]"]
---
# Explicit Token Budget Ledger

**Type:** canonical
**Status:** active
**Source:** [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md:17`

---

## Problem

Agent loops that treat context as unbounded cannot know whether the next model call has enough room for the stable harness prompt, tool schemas, accumulated history, fresh tool results, and a useful response. The source curriculum frames token budgeting as planning, allocating, and controlling token use across a session (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:37`), and defines the basic available-space equation as total context minus processed history minus response buffer (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:51`).

Existing material covers the pieces, but not the per-call ledger. The analysis says a viability calculator should identify context window, sum fixed and accumulated consumption, reserve response and safety buffers, compute remaining budget, and forecast remaining messages (`docs/analysis/2026-06-10-token-budgeting/analysis.md:50`). The extracted pattern defines the missing inputs as context-window size, fixed harness/system/tool-schema tokens, accumulated context tokens, and response plus safety buffers (`docs/analysis/2026-06-10-token-budgeting/patterns.md:19`). It also defines the outputs as remaining budget, available-budget percentage, and a breakdown inspectable before context construction (`docs/analysis/2026-06-10-token-budgeting/patterns.md:24`). What remains missing is a canonical schema that records these costs together for every next model call.

Without that ledger, context reduction becomes reactive. The loop may discover token pressure only after quality degrades, after truncation drops important state, or after the model has too little reserved output space to answer well. The curriculum explicitly warns that available context below 20% is a red flag (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:500`) and that the token manager should compute available percentage before choosing actions (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:577`).

## Solution

Maintain an explicit token budget ledger for each planned model call before dispatch. The ledger is a small, auditable record produced by the context builder and consumed by the loop. It separates fixed cost, accumulated reducible cost, output reservation, safety reservation, remaining budget, and remaining percentage.

The ledger should be computed before each call from the prompt blocks that will actually be sent:

```
total_context_window
- fixed_prompt_cost
- tool_schema_cost
- durable_state_cost
- accumulated_context_cost
- planned_new_input_cost
- reserved_response_buffer
- safety_buffer
= remaining_budget

budget_percentage = remaining_budget / total_context_window * 100
```

Canonical ledger fields:

| Field | Meaning | Example source |
|---|---|---|
| `model_context_window` | Hard upper bound for the target model call | The curriculum treats context window as total available budget (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:44`). |
| `fixed_prompt_cost` | Stable harness prompt and non-reducible instructions | Stable Harness Prompt requires preserving the harness prompt as its own first-class input (`docs/canonical/stable-harness-prompt.md:28`). |
| `tool_schema_cost` | Tool or action schemas included in the call | Owned Agent Control Loop separates switch statement and tool dispatch as an owned component (`docs/canonical/owned-agent-control-loop.md:64`). |
| `durable_state_cost` | Critical state injected separately from transcript history | The hybrid strategy keeps critical client facts in a separate layer (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:379`). |
| `accumulated_context_cost` | Recent history, summaries, tail, latest result, and selected recoverable anchors | Head-Tail Context Truncation keeps bounded active context with system prompt, head, tail, and latest result (`docs/canonical/head-tail-context-truncation.md:28`). |
| `planned_new_input_cost` | Immediate user request and newly selected tool outputs | Owned Agent Control Loop says the context builder assembles history, memory, tool results, and business state (`docs/canonical/owned-agent-control-loop.md:60`). |
| `reserved_response_buffer` | Output room held back before generation | The curriculum says output length is unknown and must be reserved in advance (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:97`). |
| `safety_buffer` | Fixed margin that keeps the call away from the hard limit | The analysis says a fixed safety buffer turns context management from reactive truncation into proactive session control (`docs/analysis/2026-06-10-token-budgeting/analysis.md:125`). |
| `remaining_budget` | Tokens left after all planned input and reservations | The analysis names remaining budget as operational room for continuation (`docs/analysis/2026-06-10-token-budgeting/analysis.md:26`). |
| `budget_percentage` | Remaining budget divided by total context window | The curriculum dashboard displays available tokens as a percentage (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:472`). |
| `action` | Decision for the next loop step: continue, monitor, compact, retrieve, or start a new session | The analysis maps budget phases to continue, monitor, compress, or new session (`docs/analysis/2026-06-10-token-budgeting/analysis.md:43`). |

ASCII flow:

```
          next user/tool event
                  |
                  v
        [context builder selects blocks]
                  |
                  v
   +-----------------------------------+
   | explicit token budget ledger      |
   | fixed prompt       = nonreducible |
   | tool schemas       = nonreducible |
   | durable state      = policy-bound |
   | history/summaries  = reducible    |
   | response reserve   = required     |
   | safety reserve     = required     |
   | remaining %        = gate input   |
   +-----------------------------------+
                  |
                  v
      continue | monitor | compact | handoff
```

The ledger is not a generic observability metric after the fact. It is a pre-call gate. If the remaining percentage falls below policy thresholds, the loop must compact, truncate, retrieve selectively, or hand off before it spends the next call.

## Implementation in this repo

### What already exists

The repo already contains the ingredients for this pattern:

- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] defines total context, already-spent history, and future room for messages and responses (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:44`).
- The same lesson teaches input tokens as history plus system instruction plus prompt instruction (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:73`), output tokens as unknown before generation and therefore reserved (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:97`), context window as model maximum (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:122`), and burn rate as input plus output per minute (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:143`).
- The calculator already reserves response and safety buffers, then computes available tokens (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:445`).
- The dashboard already exposes total context, used tokens, reserved tokens, available tokens, available percentage, burn rate, and time remaining (`curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:462`).
- The harness design checklist already asks reviewers to verify which sources entered a prompt and how much token budget each block consumed (`curriculum/07-implementation-guides/03-harness-design-checklist.md:1353`).
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] makes context construction an owned component and says every token should be constructed deliberately (`docs/canonical/owned-agent-control-loop.md:60`).
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]] separates the stable harness prompt from reducible payload (`docs/canonical/stable-harness-prompt.md:28`).
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] defines the bounded active context that a ledger can price before a call (`docs/canonical/head-tail-context-truncation.md:28`).

### What is missing

The gap is not token budgeting as a concept. The gap is a canonical per-call ledger schema. The analysis already says the strongest architecture is a layered context builder plus a monitor that decides when to continue, summarize, compress, or hand off (`docs/analysis/2026-06-10-token-budgeting/analysis.md:227`), but it does not define the record that joins those numbers into a reusable call contract.

Confirmed absence: the classification says canonical docs cover deliberate context construction, block separation, prompt budget boundaries, and context-reduction policies, but `NOT_FOUND` for a canonical ledger schema with response reserve, safety reserve, remaining-budget percentage, and per-call breakdown (`docs/analysis/2026-06-10-token-budgeting/classification.md:18`).

The implementation rule for this repo is:

1. A context builder that prepares a model call must emit a token ledger before dispatch.
2. The ledger must separate non-reducible blocks from reducible blocks.
3. The ledger must reserve response and safety capacity before calculating remaining budget.
4. The loop must use `budget_percentage` and `action` as intervention inputs before the model call, not only as post-call telemetry.
5. The ledger should be retained with traces, eval artifacts, or session state when debugging long-session behavior.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Makes token pressure visible before the next model call | Requires token estimation for every prompt block |
| Prevents response starvation by reserving output capacity up front | Conservative reserves can trigger compaction earlier than strictly necessary |
| Gives the loop a concrete gate for continue, monitor, compact, or handoff | Requires policy thresholds and ownership of intervention behavior |
| Separates fixed harness cost from reducible context cost | Exposes prompt and tool-schema bloat that teams must actively manage |
| Produces auditable traces for late-session failures and eval replay | Adds another artifact that must stay aligned with the actual prompt sent |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]], because the application must own the context builder and loop boundary where the ledger is computed.
- **Constrains:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]], because the ledger marks harness cost as fixed rather than silently reducible.
- **Guides:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]], because remaining budget determines how much head, tail, latest result, and recoverable middle preview can fit.
- **Extends:** [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]], because the lesson's calculator becomes an explicit per-call record rather than an informal dashboard.

## References

- `docs/analysis/2026-06-10-token-budgeting/analysis.md:19` — available-space equation and budget components.
- `docs/analysis/2026-06-10-token-budgeting/analysis.md:50` — viability calculator steps, including response and safety buffers.
- `docs/analysis/2026-06-10-token-budgeting/analysis.md:113` — token health monitor mechanism and action output.
- `docs/analysis/2026-06-10-token-budgeting/analysis.md:189` — missing response buffer failure pattern.
- `docs/analysis/2026-06-10-token-budgeting/analysis.md:227` — layered context builder plus monitor synthesis.
- `docs/analysis/2026-06-10-token-budgeting/patterns.md:15` — extracted Explicit Token Budget Ledger pattern.
- `docs/analysis/2026-06-10-token-budgeting/classification.md:18` — Partial Coverage classification and canonical ledger gap.
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:51` — fundamental available-space equation.
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:428` — token budgeting calculator.
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:462` — dashboard fields for available tokens and percentage.
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:570` — practical token manager implementation.
- `curriculum/07-implementation-guides/03-harness-design-checklist.md:1353` — audit card for per-call context sources and token budget by block.
- `docs/canonical/owned-agent-control-loop.md:60` — deliberate context builder construction.
- `docs/canonical/stable-harness-prompt.md:28` — stable harness prompt separated from reducible payload.
- `docs/canonical/head-tail-context-truncation.md:28` — bounded active context with stable prompt, head, tail, and latest result.

---

*Created: 2026-06-10 | From: Token Budgeting analysis | Precedence: canonical*
