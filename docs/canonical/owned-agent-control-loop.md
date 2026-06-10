---
title: "Owned Agent Control Loop"
type: canonical
aliases: ["control loop", "agent loop ownership"]
tags: ["agent-loop", "harness", "12-factor-agents"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]", "[[curriculum/01-nivel-1-fundamentals/03-basic-harness-patterns|Basic Harness Patterns Lesson]]", "[[curriculum/03-nivel-3-advanced-architecture/05-harness-evolution|Harness Evolution Lesson]]"]
sources: []
---
# Owned Agent Control Loop

**Type:** Canonical Pattern
**Status:** Active
**Source:** Dex Horthy — "12-Factor Agents" (AI Engineer, 2025), adapted for long-running-agents
**Classification:** Partial Coverage — general principle exists, specific 4-component decomposition missing (per `docs/analysis/2026-06-09-12-factor-agents/classification.md`)
**Precedence:** Level 2 (`docs/system-of-record.md:8`)

---

## Problem

Most agent frameworks provide a built-in loop: receive message, call model, execute tools, repeat. This loop is a black box. When the agent's behavior degrades on long workflows, developers cannot intervene at the right point because the framework owns the loop boundaries.

Delegating loop control to a framework creates:
- **Unbounded context growth** — the framework appends every message and result, never summarizing or pruning
- **No intervention points** — cannot inject summarization, quality checks, or human approval mid-loop
- **Hard to debug** — when the agent goes wrong, you can't inspect what the loop decided at each step

## Solution

Own the control loop. Decompose it into exactly 4 components, each with explicit intervention points.

### The 4 Components

```
┌──────────────────────────────────────────────────┐
│              OWNED AGENT CONTROL LOOP             │
│                                                   │
│  1. PROMPT                                        │
│     └─ Intervention: evaluate prompt variants     │
│                                                   │
│  2. CONTEXT BUILDER                               │
│     └─ Intervention: summarize, compress, inject  │
│                                                   │
│  3. SWITCH STATEMENT (Dispatch)                   │
│     └─ Intervention: circuit-break, audit-log     │
│                                                   │
│  4. LOOP                                          │
│     └─ Intervention: break, pause, LM-as-judge,   │
│        human approval gate, force terminate        │
└──────────────────────────────────────────────────┘
```

### Component Details

**1. Prompt** — The instructions the model receives each turn.
- You own the prompt text, not the framework.
- Intervention: evaluate prompt variants against evals, A/B test prompt changes, version prompts like code.

**2. Context Builder** — What the model sees beyond the prompt: history, memory, tool results, business state.
- You construct every token deliberately.
- Intervention: summarize old history, inject fresh context, compress verbose tool results.

**3. Switch Statement** — The deterministic router that maps model JSON output to handler code.
- You own the mapping, not the framework.
- Intervention: circuit-break expensive or unauthorized tool calls, audit-log every dispatch.

**4. Loop** — The while/for that runs the agent's turn.
- You control iteration count, exit conditions, and what happens between iterations.
- Intervention points:
  - **break** — stop iteration after N steps or when confidence is low
  - **summarize** — compress context mid-loop to prevent token blowup
  - **LM-as-judge** — run a separate evaluation call to assess the current trajectory
  - **human approval gate** — pause and wait for human input before continuing
  - **force terminate** — kill the loop if it exceeds budget or time

### Contrast: Framework-Owned vs. Developer-Owned

| Aspect | Framework-Owned | Developer-Owned |
|---|---|---|
| **Context management** | Append-only; messages accumulate | Summarize, compress, inject at loop boundaries |
| **Exit conditions** | Max steps (often hidden or config-only) | Explicit `break` with custom logic |
| **Quality gates** | None | LM-as-judge, human approval, confidence threshold |
| **Debugging** | Framework traces (opaque) | Custom traces at each intervention point |
| **Evolution** | Wait for framework release | Evolve harness independently of model capabilities |

## Implementation in long-running-agents

### What already exists

- **Nivel 1, `03-basic-harness-patterns.md`** (1,436 lines) — teaches that "the harness is the structure around the model." This is the philosophical foundation.
- **Nivel 3, `05-harness-evolution.md`** — covers evolving harnesses as models improve.
- **Core Concept 6 (Harness Evolution)** — formalizes the harness lifecycle.
- **`OrchestratorAgent.processMessage()`** — a production control loop with context building, graph invocation, and response extraction.

### What's missing

The 4-component decomposition and the named intervention points:

| Component | Exists? | Gap |
|---|---|---|
| **Prompt** | Yes — system prompt is hand-authored (1800+ lines) | Not versioned or eval'd as a separate component |
| **Context Builder** | Yes — `ConversationStateBuilder` with 15+ queries | Already excellent; exceeds the pattern |
| **Switch Statement** | Yes — `routerNode` + tool dispatch | Covered by Deterministic Tool Dispatch pattern |
| **Loop** | Partial — LangGraph owns the loop | Intervention points (`break`, `summarize`, `LM-as-judge`) are not exposed as developer hooks |

The key insight: **LangGraph owns the loop**. The repo's `OrchestratorAgent` invokes the graph and extracts the result, but the iteration inside the graph (model call → tool execution → model call) is framework-managed. To fully own the loop, the application would need to replace LangGraph's internal iteration with an explicit while/for loop that invokes model and tools separately.

### Integration recommendation

The repo already has stronger harness ownership than most codebases. The 12FA pattern adds precision:

1. Teach the 4-component decomposition in Nivel 3 as an architectural frame (not an implementation mandate — LangGraph is a valid choice)
2. Add intervention point documentation: where would `break`, `summarize`, and `LM-as-judge` go if the loop were owned?
3. For new agent architectures (not the existing mhc-backend), consider owning the loop directly instead of delegating to a framework

## Tradeoffs

| Benefit | Cost |
|---|---|
| Explicit control over when to continue, pause, or exit | More code to write and maintain |
| Easier to reason about agent behavior | Lose framework-provided optimizations |
| Can inject quality gates at precise points | Each intervention point is a potential bug |
| Evolves independently of framework releases | Framework upgrades may break custom loop |

## Relationship to Other Patterns

- **Enables:** Pattern 6 (Error Context Hygiene) — the loop's `summarize` intervention point is where error hygiene rules execute
- **Contains:** Pattern 2 (Deterministic Tool Dispatch) — the switch statement is component 3
- **Complements:** Pattern 8 (Micro-Agent Islands in DAG) — each island has its own loop; the DAG is the meta-loop
- **Built on:** Pattern 5 (Token-Level Prompt & Context Builder) — components 1 and 2

## References

- `docs/analysis/2026-06-09-12-factor-agents/classification.md` — classification as Partial Coverage
- `docs/analysis/2026-06-09-12-factor-agents/patterns.md` — pattern 3 definition
- `curriculum/01-nivel-1-fundamentals/03-basic-harness-patterns.md` — harness ownership foundation
- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` — harness evolution lifecycle

---

*Created: 2026-06-09 | From: Pattern Classification analysis | Precedence: canonical*
