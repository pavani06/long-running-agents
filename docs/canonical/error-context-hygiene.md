---
title: "Error Context Hygiene"
type: canonical
aliases: ["error hygiene", "failure context"]
tags: ["context-engineering", "error-handling", "12-factor-agents"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]", "[[curriculum/02-nivel-2-practical-patterns/exercises/exercise-04-error-context-hygiene|Error Context Hygiene Exercise]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting Lesson]]"]
sources: []
---
# Error Context Hygiene

**Type:** Canonical Pattern
**Status:** Active
**Source:** Dex Horthy — "12-Factor Agents" (AI Engineer, 2025), adapted for long-running-agents
**Classification:** Missing — no equivalent mechanism exists in the repo (per `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md`)
**Precedence:** Level 2 (`docs/system-of-record.md:8`)

---

## Problem

When agent tool calls fail, naive implementations blindly append raw errors and stack traces to the context window. This causes three failure modes:

1. **Context pollution** — raw errors (stack traces, HTTP 500 bodies, truncated JSON) consume tokens that could carry useful information for the next decision.
2. **Spiral-out** — the model sees multiple accumulated errors and "learns" that failure is the expected state, biasing subsequent decisions toward error-handling loops rather than task progress.
3. **Stale error bias** — after a recovery (tool call fails, subsequent tool call succeeds), pending errors from the earlier failure remain in context and influence decisions that no longer need error awareness.

## Solution

Curate what the model sees about failures. Never blind-append errors. Keep exactly what the model needs for its next decision, nothing more.

### Core Rules

| Rule | Description |
|---|---|
| **Summarize, don't dump** | Convert raw errors into a one-line structured summary before inserting into context |
| **Clear on success** | When a valid tool call succeeds after a failure, remove pending errors from context |
| **Never blind-append** | No error should enter context without deliberate formatting and size control |
| **Keep only what's needed** | The model needs "restriction check failed: lactose" — not the 40-line stack trace |

### Mechanism

```
TOOL CALL FAILS
  │
  ▼
ERROR SUMMARIZER
  ├── Extract: tool name, error type, actionable hint
  ├── Format: "<tool>: <error_type>. <hint>"
  └── Inject SINGLE summarized line into context
  │
  ▼
NEXT TOOL CALL SUCCEEDS
  │
  ▼
CLEAR PENDING ERRORS
  └── Remove all error summaries from active context
```

### Before / After

**Before (blind append — anti-pattern):**

```
[context window]
...conversation history...
Tool call: search_products({query: "whey"})
Error: PineconeServiceError: Connection refused
    at PineconeClient.query (/app/src/services/vector/PineconeClient.ts:47:15)
    at SearchProductsTool.execute (/app/src/agents/tools/SearchProductsTool.ts:89:22)
    at AgentNode.invoke (/app/src/agents/nodes/ecommerceNode.ts:156:10)
    ... 15 more stack frames ...

Tool call: search_products({query: "proteina whey isolate"})
...results...

[model sees stack trace → biased toward "system is unstable"]
```

**After (error context hygiene):**

```
[context window]
...conversation history...
[error] search_products: Pinecone connection refused. Retrying with broader query.

Tool call: search_products({query: "proteina whey isolate"})
...results...

[error cleared — model sees only the successful retry]
```

### Retry Loop Integration

The pattern is most powerful inside an owned agent control loop:

```
for attempt in 1..max_retries:
    result = tool.execute()
    if result.ok:
        clear_pending_errors()
        break
    else:
        error_summary = summarize(result.error)  // max 1 line
        inject_error_hint(error_summary, attempt, max_retries)
```

## Applicability to long-running-agents

### Gap (from harness diagnostic)

`docs/analysis/mhc-backend/2026-05-26-harness-diagnostic.md:320` documents:

> "Sem retry loop com feedback — o sistema atual apenas re-processa na fila sem modificar o prompt."

`docs/analysis/mhc-backend/2026-05-26-nivel-2-diagnostic.md` confirms the same gap at multiple points: errors are caught, logged, and generic fallback messages returned, but the context window is not curated after failures.

### Existing infrastructure to build on

The repo already has 10 fallback mechanisms (harness diagnostic, Padrao 4). These provide the infrastructure layer — the error context hygiene pattern adds the context layer on top:

| Layer | Existing | Added by this pattern |
|---|---|---|
| **Infrastructure** | try/catch, fail-open, Redis→DB fallback, non-blocking `.catch()` | — |
| **Context** | — (gap) | Summarize errors, clear on success, never blind-append |

### Implementation surface

The pattern applies to these repo surfaces:

1. **`OrchestratorAgent.processMessage()`** — wrap tool execution with error summarizer before appending to `messages[]`
2. **`ConversationStateBuilder.buildState()`** — when a query fails (e.g., `getActiveCart()` returns null), inject a summarized hint instead of `null` state
3. **Tool definitions** — each `DynamicStructuredTool` should return `{success, error, hint}` (some already do via `{success: boolean}` convention)
4. **Memory extraction** — `.catch()` currently swallows errors silently; should emit a one-line trace instead of nothing

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents context spiral-out | Requires owning the context window (not delegating to framework) |
| Reduces token waste on errors | Summarizer logic must be maintained per error type |
| Enables model-assisted recovery | If summarization is wrong, model may miss critical error context |
| Composable with existing retry/fallback | Adds a new failure mode: the summarizer itself can fail |

## Relationship to Other Patterns

- **Depends on:** Pattern 5 (Token-Level Prompt & Context Builder) — cannot implement error hygiene without owning context construction
- **Complements:** Pattern 3 (Owned Agent Control Loop) — the loop's `summarize` and `break` intervention points are where hygiene rules execute
- **Strengthens:** Pattern 4 (Fallback & Retry) — error hygiene makes retry loops context-aware instead of blind re-processing

## References

- `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md` — classification as Missing with gap evidence
- `docs/analysis/mhc-backend/2026-05-26-harness-diagnostic.md:320` — "sem retry loop com feedback"
- `docs/analysis/mhc-backend/2026-05-26-nivel-2-diagnostic.md` — multi-point gap analysis
- `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-patterns.md` — pattern 6 definition with inputs/outputs/benefits/limitations
- `.opencode/skills/error-context-hygiene/SKILL.md` — implementation skill for agents

---

*Created: 2026-06-09 | From: Pattern Classification analysis | Precedence: canonical*
