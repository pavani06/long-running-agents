# Deterministic Tool Dispatch

**Type:** Canonical Pattern
**Status:** Active
**Source:** Dex Horthy — "12-Factor Agents" (AI Engineer, 2025), adapted for long-running-agents
**Classification:** Partial Coverage — mechanics exist, philosophical reframe missing (per `docs/analysis/2026-06-09-12-factor-agents/classification.md`)
**Precedence:** Level 2 (`docs/system-of-record.md:8`)

---

## Problem

Frameworks and libraries present "tool use" as a magical agent capability — the model "decides to use a tool" and "the tool executes." This abstraction obscures what actually happens:

1. The model emits JSON (a structured output)
2. Application code reads the JSON
3. A switch statement or router dispatches to a deterministic handler
4. The handler executes and returns a result

Framing tools as "agent magic" makes systems harder to debug, test, and audit because the dispatch mechanism is hidden inside framework internals.

## Reframe

> **Tools are not magical. Tools are JSON + deterministic code.**

The model's job is natural-language-to-JSON conversion. Everything after that is ordinary software engineering: parsing, routing, validation, execution, error handling.

## Mechanism

```
User: "find me whey protein under R$100"

Model → { tool: "search_products", args: { query: "whey protein", max_price: 100 } }
              │
              ▼
     SWITCH STATEMENT (deterministic, testable without LLM)
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
 search_   add_to_   create_
 products  cart      order
    │
    ▼
  Pinecone query → [{name, price, score}...]
    │
    ▼
  Result returned to context (summarized, not blind-appended)
```

### Why deterministic matters

| Property | Deterministic Dispatch | Framework-Managed Tools |
|---|---|---|
| **Testability** | Test the switch statement with JSON fixtures — no LLM needed | Must mock the entire agent loop |
| **Auditability** | Log each dispatch as `{tool, args, handler, result}` | Framework logs may not expose dispatch internals |
| **Circuit breaking** | Can reject tool calls that exceed budget/time/rate limits | Framework may not expose rejection hooks |
| **Observability** | Instrument the switch statement like any other code path | Depends on framework instrumentation |

## Implementation in long-running-agents

### What already exists (Partial Coverage)

The repo implements the mechanics correctly:

- **Every tool** is a `DynamicStructuredTool` with Zod schema input and typed return. The dispatch IS deterministic — LangChain routes JSON to handler code. (`docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence.md`)
- **Sprint Contracts** module (Nivel 2) teaches input/output contract design with Zod.
- **20+ tools** in mhc-backend follow this pattern: `SearchProductsTool`, `CreateOrderTool`, `AddToCartTool`, etc.

### What's missing (the reframe)

The repo treats tool dispatch as standard engineering practice **without naming it as a distinct pattern**. Adding the reframe provides:

1. **A teachable name** — "Deterministic Tool Dispatch" is a handle that makes the practice discussable and teachable
2. **A philosophical anchor** — "tools are not magical" is a reframe that changes how engineers think about agent architecture
3. **Explicit testing guidance** — the pattern's emphasis on testing dispatch handlers without LLM is not currently taught in the curriculum
4. **Audit-logging recommendation** — treating each dispatch as a software operation worth logging

### Curriculum integration points

| Curriculum element | Integration |
|---|---|
| Nivel 2, `02-sprint-contracts.md` | Add "Tools are JSON + Code" sidebar explaining the reframe |
| Nivel 2, `exercises/exercise-02-structured-output.md` | Add a step: "Test your tool dispatch handler with a JSON fixture — no LLM" |
| Core Concept 4 (Sprint Contracts) | Add "Deterministic Dispatch" as a sub-pattern explaining why contracts make tools testable |
| Nivel 3, `01-multi-agent-systems.md` | Frame the routerNode as a deterministic dispatch layer with an LLM-powered classifier |

## Tradeoffs

| Benefit | Cost |
|---|---|
| Tools become testable with normal software techniques | Requires application to own JSON-to-handler mapping |
| Dispatch is auditable and observable | Bad or ambiguous JSON needs handling (not the tool's fault) |
| Reduces reliance on framework internals | Adds engineering effort vs. using framework defaults |
| Circuit-breaking at the switch statement level | The switch statement itself becomes a critical path |

## Relationship to Other Patterns

- **Built on:** Pattern 1 (Structured Output Contract) — deterministic dispatch reads structured JSON; without contracts, dispatch is fragile
- **Enables:** Pattern 3 (Owned Agent Control Loop) — the switch statement is one of the 4 owned components
- **Strengthened by:** Pattern 6 (Error Context Hygiene) — tool results fed back into context benefit from hygiene rules
- **Related to:** Pattern 8 (Micro-Agent Islands in DAG) — each micro-agent's tool dispatch is a deterministic island

## References

- `docs/analysis/2026-06-09-12-factor-agents/classification.md` — classification as Partial Coverage
- `docs/analysis/2026-06-09-12-factor-agents/patterns.md` — pattern 2 definition
- `docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence.md` — dispatch chain documentation
- `curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md` — existing contract teaching

---

*Created: 2026-06-09 | From: Pattern Classification analysis | Precedence: canonical*
