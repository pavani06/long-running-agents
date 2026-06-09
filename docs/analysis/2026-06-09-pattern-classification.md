# Comparative Classification: 12-Factor Agentic Patterns vs. long-running-agents Repo

**Date:** 2026-06-09
**Repo analyzed:** `pavani06/long-running-agents`
**Patterns source:** Dex Horthy — "12-Factor Agents" (AI Engineer, 2025)
**Evidence basis:** `docs/analysis/mhc-backend/`, `curriculum/`, `docs/system-of-record.md`, `AGENTS.md`

---

## Classification Legend

| Class | Meaning |
|---|---|
| Already Exists | Pattern is documented, implemented, or taught with equivalent depth |
| Partial Coverage | Elements exist but missing key mechanics, reframe, or formalization |
| Missing | Not present in any form |
| Better Implementation | Repo has a superior or more mature version of the same idea |

---

## 1. Structured Output Contract

**Classification:** Already Exists

**Why:**
The repo treats structured output as a foundational assumption, deeply embedded across all layers:

- **Curriculum:** Nivel 1 exercise `exercise-02-structured-output.md` teaches this as one of the 5 basic harness patterns. Core Concept 4 (Sprint Contracts) formalizes input/output contracts with Zod.
- **Implementation (mhc-backend):** 20+ `DynamicStructuredTool` with Zod schemas enforcing type-safety at the LLM ↔ code boundary. `routerNode` uses `withStructuredOutput({ strict: true })`. 4-layer output validation pipeline documented in `output-validation-state-persistence.md`.
- **Diagnosis:** The harness diagnostic rates Output Validation at Nivel 2-3 maturity.

**Gap (minor):** The 12FA reframe calls this "the most magical thing LLMs can do" and positions it as THE primitive everything else builds on. The repo treats it as assumed infrastructure rather than a named philosophical stance. The repo's framing is more engineering-focused (contracts, schemas, validation layers) while 12FA's is more architectural (NL→JSON is the agentic primitive).

---

## 2. Deterministic Tool Dispatch

**Classification:** Partial Coverage

**Why:**
The repo IMPLEMENTS the mechanics but doesn't ARTICULATE the reframe:

- **What exists:** Every tool in mhc-backend is a `DynamicStructuredTool` with Zod schema input and typed return. The dispatch is deterministic — LangChain routes JSON to handler code. `docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence.md` documents the full dispatch chain (schema → business validation → handler execution). Sprint Contracts curriculum module (Nivel 2) teaches input/output contract design.
- **What's missing:** The provocative reframe — "tool use is harmful" / "tools are just JSON + deterministic code, there's nothing magical" — is absent. The repo treats this as standard engineering practice without naming it as a distinct pattern. The 12FA's emphasis on testability of the dispatch handler without LLM, audit-logging each dispatch as a software operation, and circuit-breaking at the switch statement level is not explicitly taught.

**Integration value:** The 12FA reframe would give the repo's existing tool architecture a memorable, teachable name and a philosophical anchor ("tools aren't magical, they're just JSON dispatch").

---

## 3. Owned Agent Control Loop

**Classification:** Partial Coverage

**Why:**
The general principle of "own your harness" is a central tenet of the repo. The specific 4-component decomposition is not:

- **What exists:** Nivel 1 `03-basic-harness-patterns.md` (1,436 lines) teaches that "the harness is the structure around the model." Nivel 3 `05-harness-evolution.md` covers evolving harnesses as models improve. Core Concept 6 (Harness Evolution) formalizes the lifecycle. mhc-backend's `OrchestratorAgent.processMessage()` is a production control loop with context building, graph invocation, and response extraction.
- **What's missing:** The 12FA decomposes the loop into exactly 4 owned components — prompt, switch statement, context builder, loop — each with specific intervention points (summarize, LM-as-judge, human approval gate, force termination). The repo's harness philosophy is broader but less atomic. The LangGraph-based implementation delegates loop control to the framework; the 12FA pattern argues for owning the loop directly.

**Integration value:** The 4-component decomposition would add precision to the repo's harness teaching. The intervention points (particularly `break`, `summarize`, `LM as judge` injected at loop boundaries) are practical techniques the curriculum could absorb.

---

## 4. Serializable Pause/Resume State

**Classification:** Partial Coverage — but also **Better Implementation** potential

**Why:**
The repo has far richer state persistence than 12FA describes, but uses a different mechanism:

- **What exists:** mhc-backend implements 4 persistence layers (semantic memory, conversation context, transactional state, cache). PostgreSQL multi-table + Redis + in-memory cache. Memory extraction via secondary LLM in background. Time-based expiration. Contradiction detection. The curriculum dedicates Core Concept 5 (State Persistence) and Nivel 3 topic 2 to this.
- **What's different:** mhc-backend rebuilds state from scratch each turn via `ConversationStateBuilder.buildState()` (15+ parallel queries). The LangGraph is compiled **without checkpointer** — state lives in the database, not in a serialized context window. The 12FA pattern serializes the entire context window to DB, then reconstitutes it — the agent "doesn't know it was paused." The repo's approach is arguably better for most use cases (richer state model, independent of token representation) but doesn't implement the "transparent pause/resume" property 12FA describes.
- **Gap analysis confirms:** `output-validation-state-persistence.md` explicitly notes: "Sem checkpointer no LangGraph. O estado é reconstruído do zero a cada turno pelo ConversationStateBuilder."

**Integration value:** The 12FA context serialization pattern would add a complementary mechanism for scenarios where token-level fidelity across pauses matters (e.g., mid-reasoning interruption). The repo's state model is richer; 12FA's serialization is simpler and more portable.

---

## 5. Token-Level Prompt and Context Builder

**Classification:** Already Exists

**Why:**
This is the repo's strongest domain — context management is Core Concept #1:

- **Curriculum:** `01-context-management.md` (2,126 lines) covers windowing, token budgeting, metadata layering, and context engineering as a unified discipline. `02-token-budgeting.md` teaches compression, prioritization, and chunking. Nivel 3 `04-server-side-compaction.md` covers server-side context optimization.
- **Implementation analysis:** `2026-05-28-janela-deslizante-contexto.md` documents adaptive windowing (20-60 messages), 4 layers of metadata that never expire, memory extraction pipeline with `gpt-4.1-mini`, and the exact token construction flow (user messages get timestamps, assistant messages don't — to prevent the LLM from learning to echo timestamps).
- **The 12FA emphasis** on "writing every single token by hand" and "context engineering as the unified discipline" is already the repo's thesis. The 12FA pattern adds the "try everything / optimize density" mindset, which the repo already embodies in its analysis docs.

**Nuance:** The repo has MORE depth here than the 12FA pattern. The 12FA version is a concise principle; the repo is a full curriculum with production evidence.

---

## 6. Error Context Hygiene

**Classification:** Missing

**Why:**
This specific operational pattern is not present in any form:

- **What the repo has:** Fallback & retry mechanisms (10 documented in the harness diagnostic). Errors are caught via try/catch, logged, and generic fallback messages are returned. Memory extraction failures are silently swallowed (`.catch()` non-blocking). Redis failures fall back to direct DB queries (fail-open).
- **What's missing:** The pattern of "when a tool call fails then a subsequent one succeeds → clear all pending errors from context; summarize errors; never blind-append; keep only what the model needs for the next decision." The analysis docs explicitly note: "sem retry loop com feedback — o sistema atual apenas re-processa na fila sem modificar o prompt."
- **Gap:** The repo's error handling is infrastructure-level (retry, fallback, degrade gracefully). The 12FA pattern is context-level (curate what the model sees about failures to prevent spiral-out). These are complementary but the context-level hygiene is absent.

**Integration value:** HIGH. This would address a documented gap. The analysis flags that error accumulation in context is a known failure mode, and the 12FA pattern provides a precise recipe for fixing it.

---

## 7. Human Contact Intent Tool

**Classification:** Partial Coverage

**Why:**
Human-in-the-loop exists but the specific first-token mechanism doesn't:

- **What exists:** mhc-backend implements human contact through WhatsApp flows — the agent can request missing data (address, CPF, email) and wait for human response. `CreateOrderTool` has a checkout pipeline that saves state and pauses for human input. `ConversationContext.status` tracks conversation phases including waiting states. The curriculum references human approval in the multi-agent coordination and customer journey modules.
- **What's missing:** The 12FA mechanism of pushing the tool-vs-human decision to the **first natural-language token** the model generates. The repo uses explicit flow states (checkout → missing_data → wait_for_human) rather than intent-token routing. The 12FA's open-ended intent vocabulary ("need clarification" vs "need manager approval" vs "done") expressed through NL tokens is novel.
- **The repo doesn't teach** the design choice of routing by first token vs routing by schema field, nor the tradeoff (fuzzy parsing vs structural guarantees).

**Integration value:** Medium. The first-token mechanism is clever but niche — it works best when the agent has multiple human-facing outcomes. The repo's WhatsApp flow model is more appropriate for its domain.

---

## 8. Micro-Agent Islands in a Deterministic DAG

**Classification:** Already Exists

**Why:**
This is arguably the repo's architectural thesis:

- **Curriculum:** Core Concept 7 (Multi-Agent Coordination, 2,533 lines) teaches exactly this — Search Agent, Filter Agent, Ranking Agent, Recommendation Agent as specialized micro-agents embedded in a deterministic orchestration layer. Nivel 3 `01-multi-agent-systems.md` covers decomposition patterns. Nivel 4 case studies show KODA's product discovery, order processing, and fulfillment workflows as DAGs with agent islands.
- **Implementation (mhc-backend):** 3 specialized agents (coach, ecommerce/KODA, voturuna) coordinated by `routerNode` + `OrchestratorAgent`. Single-agent fast path skips the router. Each agent has its own tools, prompt, and domain. The router is deterministic post-classification.
- **Harness diagnostic confirms:** "Multi-Agent Routing with LangGraph — 3 agentes especializados orquestrados por um nó routerNode." Rated at Nivel 3 maturity.
- **12FA nuance:** The 3-10 step bound per micro-agent and the deploy pipeline example (CI/CD → micro-agent → deterministic tests → rollback agent) are specific instantiations the repo doesn't use as canonical examples. The repo's multi-agent model is more complex (router + specialized agents + tools) while 12FA's is simpler (DAG nodes with small LLM loops).

---

## Summary

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Structured Output Contract | Already Exists | Low — repo has equivalent depth |
| 2 | Deterministic Tool Dispatch | Partial Coverage | Medium — reframe adds teachable framing |
| 3 | Owned Agent Control Loop | Partial Coverage | Medium — 4-component decomposition adds precision |
| 4 | Serializable Pause/Resume State | Partial Coverage | High — complementary mechanism to existing state model |
| 5 | Token-Level Prompt & Context Builder | Already Exists | Low — repo exceeds 12FA depth |
| 6 | Error Context Hygiene | **Missing** | **High** — addresses documented gap |
| 7 | Human Contact Intent Tool | Partial Coverage | Medium — niche mechanism, domain-appropriate alternatives exist |
| 8 | Micro-Agent Islands in Deterministic DAG | Already Exists | Low — repo's architectural thesis already |

**Key insight:** The long-running-agents repo is an implementation-heavy, curriculum-driven codebase that already covers 5 of 8 patterns at equivalent or greater depth. The 12FA patterns add value primarily through NAMING (giving memorable handles to practices the repo already implements) and through two novel contributions: **Error Context Hygiene** (missing, high value) and the **Deterministic Tool Dispatch reframe** (partial coverage, adds philosophical clarity).
