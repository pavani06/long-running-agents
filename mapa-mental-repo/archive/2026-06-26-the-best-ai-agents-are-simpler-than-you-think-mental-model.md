# Repository Mental Model — Ecossistema Pavan

**Date:** 2026-06-26  
**Repo:** `ecossistema-pavan`  
**Type:** mental-model  
**Purpose:** Structured understanding of the repository before analyzing external source documents.

---

## 1. Project Goals

This ecosystem builds, teaches, and operates **agentic engineering at production scale**. The unifying thesis: **LLMs are capable but fragile in long-running tasks — the solution is harness engineering, not better prompts or bigger models**.

Three pillars:

1. **Agentic Engineering (Harness Engineering):** The discipline of building infrastructure that surrounds an LLM and guarantees reliability across hours-long execution. The core axiom: "humans steer, agents execute" (source: `raw-knowledge/concepts/harness-engineering.md`). The engineer's role shifts from writing code to defining work, specifying quality bars, building guardrails, and removing blockers. Every human interaction with the agent is a harness failure.

2. **Knowledge Management (Obsidian Vaults + obsidian-eval):** A multi-vault Obsidian ecosystem with typed ontologies, cross-vault wikilinks, and automated pipelines that transform raw sources (talks, papers, transcripts) into interlinked canonical knowledge. The obsidian-eval CLI (`@pavani/obsidian-eval`) is the runtime that unifies all vaults — scan, query, graph, write, epistemic graph, cross-vault wikilinks.

3. **LLM Pipelines (Operational):** Production-grade pipelines that close the learning loop:
   - `analyze-and-improve`: 7-phase pipeline that consumes external knowledge sources → extracts patterns → classifies against repo → generates canonical docs, skills, exercises (harness at `harness/`)
   - **Knowledge Pipeline (C2-C6):** Handoff → compressWorkingMemory (A1) → relevanceScore (B1) → promotePatterns (B2) → buildProvenance (C4) → checkDrift (C5) → appendFact (C2) → cross-vault manifest (C3) → simulation (C6)
   - **Reflection Loop:** Gather → Analyze → Synthesize → Apply (automated via systemd timer at 09:00 BRT)
   - **Learning Flywheel:** Failure patterns → QI findings → corrective action → canonical docs

The practical anchor: **KODA**, a WhatsApp-based e-commerce agent for supplement sales (`mhc-knowledge-base`, `agent-analysis`), which must maintain quality in 2+ hour customer conversations.

---

## 2. Architecture

### 2.1 Core Components

| Component | Location | Role |
|---|---|---|
| **long-running-agents** (vault) | `/mnt/c/Users/pavan/long-running-agents/` | Knowledge base: 118 canonical patterns, N1-N4 curriculum, ADRs, analyses, articles, harness |
| **raw-knowledge** (vault) | `/mnt/c/Users/pavan/raw-knowledge/` | Ingested sources ontology: 110 concepts, entities, typed relationships (LLM Wiki / Karpathy pattern) |
| **mhc-knowledge-base** (vault) | `/mnt/c/Users/pavan/mhc-knowledge-base/` | KODA e-commerce domain knowledge, templates, validation scripts |
| **sisyphus-runtime** (vault) | `~/sisyphus-runtime/` | Private runtime vault: session handoffs, durable facts, runtime state, telemetry.db |
| **obsidian-eval** | `/mnt/c/Users/pavan/obsidian-eval/` | CLI & npm library (`@pavani/obsidian-eval`): scan, query, graph, write, epistemic graph, cross-vault wikilinks |
| **agent-analysis** | `/mnt/c/Users/pavan/agent-analysis/` | Architectural diagnosis of KODA using 8 lenses from long-running-agents |
| **livro-agentico** | `/mnt/c/Users/pavan/livro-agentico/` | Quarto book: 10 chapters, 70+ canonical patterns mapped |
| **telemetry** | `~/scripts/telemetry/` | Observability pipeline: tracer, collector, scavenger, SLO checker, 80 tests in 13 suites |
| **.opencode/skills/** | `~/.config/opencode/skills/` (30 skills) | Agent skills: review-work, debugging, canonical-context, budget-monitor, analyze-and-improve, etc. |
| **.opencode/agents/** | `/mnt/c/Users/pavan/.opencode/agents/` (3 agents) | Agent definitions: hop-orchestrator-rezek, koda-hop-init-basic, hop-live-whatsapp-tester |

### 2.2 Key Relationships

```
raw-knowledge (sources ingested)
  │ analyze-and-improve pipeline
  ▼
long-running-agents (canonical docs extracted)
  │ loaded via canonical-context skill
  ▼
.opencode/skills/ (operational agent instructions)
  │ orchestrated by
  ▼
.opencode/agents/ (3 agent personas)
  │ runtime state stored in
  ▼
sisyphus-runtime (handoffs, durable facts, telemetry)
  │ cross-vault wikilinks powered by
  ▼
obsidian-eval (CLI runtime unifying all vaults)
  │ observability via
  ▼
telemetry pipeline (tracer → collector → dashboard → flywheel)
```

### 2.3 Runtime Flow

```
Session Start
  │ canonical-context skill loaded → injects handoff + relevant canonical docs
  ▼
Orchestrator (Sisyphus) decomposes task
  │ delegates via task() to sub-agents
  ▼
Sub-agents (explore, oracle, deep, ultrabrain, etc.)
  │ task-wrapper.sh instruments every call
  ▼
Trace Span → /tmp/trace-state.json
  │ session-end-hook.sh collects
  ▼
telemetry.db → dashboard, SLOs, daily-summary
  │ flywheel-daemon detects failure patterns
  ▼
QI findings → canonical docs updated → curriculum improved
```

### 2.4 ADR Architecture (accepted decisions)

13 ADRs at `/mnt/c/Users/pavan/plans/adr/` (dated 2026-06-20 to 2026-06-25):

| ADR | Topic |
|---|---|
| ADR-001 | Runtime active control system |
| ADR-002 | Evaluator test dedup |
| ADR-003 | Telemetry pipeline stack |
| ADR-004 | Markdown frontmatter as canonical storage |
| ADR-005 | Custom parser (regex + YAML) |
| ADR-006 | `realpathSync` with ENOENT-only catch |
| ADR-007 | Canonical context injection method |
| ADR-008 | Canonical reference selection |
| ADR-009 | Private runtime vault over embedded |
| ADR-010 | Python stdlib shared skill harness |
| ADR-011 | User systemd units (oneshot + timer) |
| ADR-012 | Token budget phase gate encoding |
| ADR-013 | Scavenger pipeline post-hoc inference |

1 ADR at `long-running-agents/docs/decisions/`:
- `2026-06-24-skill-canons-bridge-implementation.md` — Skill-Canons Bridge implementation decisions (waves 0-2)

---

## 3. Patterns

### 3.1 Pattern Catalog

**118 canonical docs** at `/mnt/c/Users/pavan/long-running-agents/docs/canonical/`. Major categories:

**Context Engineering** (managing the agent's token window):
- `error-context-hygiene.md` — Summarize errors, clear on success, never blind-append
- `head-tail-context-truncation.md` — Preserve head (objective) and tail (current state), recoverable middle
- `addressable-memory-catalog.md` — Every omitted item needs id, location, preview, fetch
- `explicit-token-budget-ledger.md` — Calculate prompt cost, reserves, per-step balance
- `phase-gated-token-health-monitor.md` — Green (>50%), Yellow (30-50%), Orange (20-30%), Red (≤20%)
- `budget-aware-session-handoff.md` — Red-phase automatic handoff with state preservation
- `hybrid-context-stack.md` — Prompt + memory + durable state + recoverable omissions
- `tiered-context-storage.md` — Hot/warm/cold layers with promotion/demotion
- `deliberate-forgetting.md` — Forgetting as first-class operation with relevance evaluator
- `smallest-sufficient-context.md` — Estimator + relational traversal + order-preserving assembly
- `relational-context-graph.md` — Typed edges (dependency, provenance, supplantation, causation)

**Agent Control & Orchestration:**
- `owned-agent-control-loop.md` — Decompose into 4 components: Prompt, Context Builder, Switch, Loop
- `application-owned-agent-control-plane.md` — Unified control plane contract
- `deterministic-tool-dispatch.md` — Model converts NL to JSON; rest is deterministic software
- `serializable-pause-resume-state.md` — Serialize state for pause/resume
- `plan-execute-verify.md` — Three phases with explicit checkpoints
- `closed-loop-agent-operating-system.md` — Full OS for long-running agents
- `multi-agent-fault-tolerance.md` — Saga pattern, Circuit Breaker, human escalation

**Evaluation Architecture:**
- `generator-evaluator.md` — Separate generation from evaluation (11% silent failure gap)
- `3-layer-evaluation-architecture.md` — Deterministic (regex), Semantic (LLM-as-Judge), Behavioral (trace path)
- `eval-tier-stratification.md` — Fast (inner loop), Medium (PR gate), Deep (release/canary)
- `pain-signal-eval-progression-gate.md` — Invest in evals guided by real pain signals
- `production-failure-regression-flywheel.md` — Convert production failures into eval cases
- `production-grounded-eval-sampling.md` — Anchor eval sampling in production replay
- `living-eval-dataset.md` — Monotonically growing dataset; every incident adds a permanent case
- `eval-driven-development-timeline.md` — 6 weeks of eval infrastructure before model experiments
- `behavioral-eval-path-analysis.md` — Detect duplicates, loops, wrong tool use, cost attribution
- `centralized-cross-framework-tracing.md` — Unified trace schema across multiple agent frameworks

**Harness Engineering:**
- `measured-harness-evolution-lifecycle.md` — BUILD → STABILIZE → SIMPLIFY → REMOVE
- `invariant-compensation-split.md` — Classify components as domain invariants vs model compensations
- `llm-as-fuzzy-compiler.md` — Code as disposable build artifact; harness controls are the real source
- `garbage-collection-day-meta-loop.md` — Weekly harness cleanup review
- `failure-pattern-classification-loop.md` — Categorize slop and agent misbehavior
- `deferred-ledger-agentic-work.md` — Track agentic debt with sunset gates
- `prompt-as-code-causal-change-management.md` — Causal commit discipline for prompts

**Governance & Quality:**
- `manual-brake-question-gate.md` — Mandatory human intervention before irreversible actions
- `constraint-budget-gate.md` — Max 5-7 constraints per task
- `constraint-failure-decision-rule.md` — Degrade, retry, or escalate
- `intent-five-part-primitive.md` — Goal, Context, Constraints, Verification, Handoff
- `grill-me-alignment-interview.md` — One-question-at-a-time alignment with decision ledger
- `shadow-review-pipeline.md` — AI reviewer runs parallel before merge
- `pre-commit-ai-review-gate.md` — Automatic agent validation before commit

**Knowledge Infrastructure:**
- `epistemic-memory-graph.md` — Graph with epistemic status and provenance (174 nodes, 191 edges)
- `cross-context-knowledge-siloing.md` — Knowledge invisible across agent contexts
- `domain-embedded-workflow-automation-wedge.md` — Evidence-guided automation wedge

**Specific Domains:**
- `institutional-layer-amplification.md` — Regulatory gaps amplifying across institutional layers
- `energy-value-chain-spread-analysis.md` — MWh→tokens→inference value chain analysis
- `social-archetype-classification.md` — Creation, Abundance, Predation taxonomy
- `asymmetric-binary-outcome-positioning.md` — Binary outcome pricing model
- `quarto-publishing-architecture.md` — Quarto book publishing config

### 3.2 Pattern Maturity Levels

- **Established** (active canonical docs used across skills and curriculum): ~80 patterns
- **Emerging** (ADRs accepted, runtime wired): ~15 patterns (active control, telemetry, skill-canons bridge)
- **Experimental** (design phase, pending authorization): 4 patterns (runtime canonical eval gate, handoff RunContext, skill-canons arch fixes)

### 3.3 Anti-Patterns Documented

- `accidental-brake-replacement.md` — Safety gates silently removed
- `symphony-trap-awareness.md` — Over-specification killing adaptability
- `cross-context-knowledge-siloing.md` — Knowledge invisible between agent contexts

---

## 4. Abstractions

### 4.1 Core Terminology (30 cross-cutting terms)

From `/mnt/c/Users/pavan/long-running-agents/docs/ecosystem-glossary.md`:

| Term | Definition | Location |
|---|---|---|
| **Vault** | Markdown knowledge repository managed by obsidian-eval; declares exports/imports in MANIFEST.md | `obsidian-eval/src/types.ts` |
| **MANIFEST.md** | Cross-vault dependency declaration listing exports and imports per vault | `obsidian-eval/src/manifest.ts` |
| **Cross-vault Wikilink** | `[[vault:<name>/<path>]]` syntax referencing documents in another vault | `obsidian-eval/src/index.ts` |
| **Telemetry DB** | SQLite database storing session metrics (tokens, traces, SLOs) | `~/scripts/telemetry/collector.ts` |
| **Trace Span** | Instrumented record of a `task()` call: category, subagent, duration, tokens, success | `~/scripts/telemetry/trace-cli.ts` |
| **Scheduler** | Token estimator that fragments tasks to fit session budget | `obsidian-eval/src/scheduler.ts` |
| **Execution Graph** | DAG of tasks modeling session orchestration (TaskNode with status, parents, children, estimate) | `obsidian-eval/src/execution-graph.ts` |
| **Knowledge Pipeline** | Full flow: handoff → compressWorkingMemory → relevanceScore → promotePatterns → buildProvenance → checkDrift → appendFact → simulation | `obsidian-eval/docs/walkthroughs/pipeline-completo.md` |
| **Handoff** | Snapshot of session state persisted as note in runtime vault (type: session-handoff) | `session-handoff` skill |
| **Session** | Unit of continuous human-agent interaction in OpenCode (ses_...) | OpenCode runtime |
| **Durable Fact** | Persisted knowledge with type (constraint, preference, baseline, diagnostic, principle), temporal validity, provenance | `obsidian-eval/src/types.ts` |
| **Memory Layers** | 3-layer pipeline: Working Memory → Session Memory → Long-term Memory | `obsidian-eval/src/memory-layers.ts` |
| **Relevance Score** | 0-1 score across 5 dimensions: recency, importance, frequency, similarity, confidence | `obsidian-eval/src/relevance.ts` |
| **Promotion Candidate** | Pattern detected in ≥3 similar handoffs, candidate for principle | `obsidian-eval/src/types.ts` |
| **Reflection Loop** | Cross-session pipeline: Gather → Analyze → Synthesize → Apply (automated daily) | `reflection-runner` skill |
| **Temporal Versioning** | Facts have valid_from/valid_to; expired facts penalized in relevanceScore | `obsidian-eval/src/types.ts:93-100` |
| **Canonical Doc** | Authoritative reference document with type: canonical defining a reusable agent design pattern | `long-running-agents/docs/canonical/` |
| **Skill** | Domain-specific instructions and workflows loaded by orchestrator via skill(name="...") | `~/.config/opencode/skills/` |
| **Harness** | Control infrastructure surrounding the agent: tests, reviews, conventions, skills, docs | Various |
| **Token Budget** | Token budget per session: Green (>50%), Yellow (30-50%), Orange (20-30%), Red (≤20%) | `budget-monitor` skill |
| **Orchestrator** | Main agent (Sisyphus) that decomposes tasks and delegates to sub-agents | `.opencode/agents/` |
| **Sub-agent** | Specialized agent invoked by orchestrator: explore, oracle, deep, ultrabrain, quick | `task()` tool |
| **Epistemic Graph** | Auto-extracted entity/relationship graph from runtime vault (174 nodes, 191 edges) | `obsidian-eval/src/epistemic-graph.ts` |
| **Ground Truth** | Human-defined immutable assertions blocking knowledge pipeline contamination (5 active) | `obsidian-eval/src/ground-truth.ts` |
| **Drift Detection** | Verification that candidate principles don't contradict ground truths | `obsidian-eval/src/ground-truth.ts:25-89` |
| **Provenance Chain** | Audit trail recording origin of each durable fact: derived_from, reasoning_summary, premises | `obsidian-eval/src/types.ts:102-116` |
| **Simulation** | Synthetic handoff generation to test emergent pipeline properties (5 asserts) | `obsidian-eval/src/simulate.ts` |
| **System of Record** | Precedence document resolving documentation conflicts (ADRs > canonical > evidence > analysis > archive) | `long-running-agents/docs/system-of-record.md` |
| **MOC (Map of Content)** | Index file aggregating wikilinks for a thematic cluster (prefix `_moc-`) | Convention |
| **Harness Engineering** | Operational discipline: "humans steer, agents execute"; code is free, human attention is scarce | `raw-knowledge/concepts/harness-engineering.md` |

### 4.2 Domain-Specific Terms (from curriculum GLOSSARY)

From `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md` (1002 lines):

| Term | Definition |
|---|---|
| **Agent (Agente)** | Autonomous AI entity that takes actions, uses tools, executes tasks in sequence |
| **Amnesia (Context Amnesia)** | Agent "forgets" earlier context after exceeding context window |
| **Agent Degradation Loop** | 4-link cycle: uneven attention → compounding errors → external state fragmentation → inert memory feedback |
| **Context Window** | Token limit the model can process in a single session |
| **Harness** | Scaffolding that supports the agent: memory management, tool integration, error handling, state persistence |
| **Generator/Evaluator** | Two-agent architecture separating creative generation from impartial evaluation |
| **Sprint Contract** | Explicit agreement on what agent will deliver in a bounded execution block |
| **Rubric** | Structured scoring criteria for evaluating agent output quality |
| **Trace** | Instrumented record of agent execution path (tool calls, decisions, timing) |
| **Compaction** | Summarizing conversation history to reclaim context window space |
| **Control Plane** | Orchestration layer managing agent lifecycle (start, pause, resume, handoff) |

---

## 5. Curriculum Structure

### 5.1 Program Overview

**12 weeks, 4 levels, 8 core concepts, 35+ diagrams, 5 case studies**

Source: `/mnt/c/Users/pavan/long-running-agents/curriculum/` (23 directories/files)

### 5.2 Level Progression

| Level | Focus | Duration | Key Content |
|---|---|---|---|
| **N1 — Fundamentals** | Context windows, token budgeting, basic harness patterns | 3-4h | `01-why-agents-lose-plot.md`, `02-token-budgeting.md`, `03-basic-harness-patterns.md` |
| **N2 — Practical Patterns** | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading | 6-8h | 4 lessons + 7 exercises (error-context-hygiene, two-implementations-goal-test, goal-atomicity-split, constraint-budget-gate) |
| **N3 — Advanced Architecture** | Multi-agent systems, state persistence, file-based coordination, harness evolution | 8-10h | 5 lessons + 11 exercises (llm-as-fuzzy-compiler, persona-based-documentation, autonomy-curriculum-sampling, magnitude-direction-verifier-split, behavioral-eval-path-analysis) |
| **N4 — KODA-Specific** | KODA architecture, customer journeys, feature patterns, implementation | Continuous | 5 lessons + 6 exercises + 3 case studies |

Supplementary levels:
- `03-nivel-arquiteto/` — Architect-specific exercises (owner-of-no-role)
- `04-nivel-3-engenharia-avancada/` — Advanced engineering exercises (behavioral-eval-path-analysis)
- `03-nivel-3-operational/`, `04-nivel-operador/` — Operator-focused tracks

### 5.3 8 Core Concepts

At `/mnt/c/Users/pavan/long-running-agents/curriculum/05-core-concepts/`:

1. **Context Management** — All levels (N1)
2. **Planning vs Execution Separation** — All levels (N2)
3. **Generator/Evaluator Pattern** — All levels (N2)
4. **Sprint Contracts** — All levels (N2)
5. **State Persistence** — Advanced (N3)
6. **Harness Evolution** — Advanced (N3)
7. **Multi-Agent Coordination** — Advanced (N3)
8. **Evaluation Rubrics** — All levels (N2)

Each concept has: deep explanation, 3 Mermaid knowledge graphs, KODA application, implementation checklist.

Additional advanced exercises (N3): `tiered-context-storage`, `neutral-selection-layer`, `selection-budgeted-retrieval`.

### 5.4 Supporting Resources

| Resource | Location | Content |
|---|---|---|
| **Knowledge Graphs** | `curriculum/06-knowledge-graphs/` | 35+ Mermaid diagrams (concept ecosystem, KODA dependencies, learning progression, problem-solution mapping) |
| **Implementation Guides** | `curriculum/07-implementation-guides/` | Setup guide, team progression, harness design checklist, rubric template, trace analysis |
| **Templates** | `curriculum/08-tools-templates/` | Sprint contract, rubric, ADR, progress tracker, knowledge graph, learning assessment |
| **Case Studies** | `curriculum/09-case-studies/` | 5 cases: retro-game-maker, browser-daw, KODA product discovery, order processing, fulfillment workflow |
| **References** | `curriculum/10-references/` | External references, model capability timeline |

### 5.5 Entry Points

| Profile | Entry | Time |
|---|---|---|
| Newcomer | `QUICK_START.md` | 45 min |
| Experienced with LLMs | `MASTER_PLAN.md` > "Pule para Prático" | 30 min |
| Architect / Senior | `MASTER_PLAN.md` > "Vá Direto para Avançado" | 30 min |
| KODA team | `04-nivel-4-koda-specific/` | Continuous |
| Quick reference | `GLOSSARY.md` | Lookup |
| Execution plan | `EXECUTION_PLAN.md` | 30 min |

---

## 6. Existing Gaps

### 6.1 Pending Canonical Docs (from system-of-record.md:291-297)

Listed at `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md` "Documentação canônica pendente":

| Document | What it should cover | Status |
|---|---|---|
| `agent-lifecycle.md` | claim → worktree → implement → review → merge → cleanup cycle | NOT written |
| `curriculum-model.md` | Level taxonomy, artifact types, quality criteria | NOT written |
| `portal-architecture.md` | Portal design decisions, data model, rendering pipeline | NOT written (blocked on SPA implementation) |
| `crossroad-change-policy.md` | Policy for changing high-blast-radius files | NOT written (referenced by PR template but files don't exist yet) |
| `obsidian-document-conventions.md` | AGENTS.md Rule 16 already covers; canonical doc only needed if convention grows beyond a rule | NOT urgent |

### 6.2 Candidate ADR Topics (from system-of-record.md:160-164)

- Stack choice for the portal (vanilla static JS vs. framework)
- Content chunking and on-demand loading model
- State persistence strategy between agents
- Curriculum versioning policy

### 6.3 Blocked/Deferred Plans (from AGENTS.md plan listing)

| Plan | Status | What's pending |
|---|---|---|
| `2026-06-21-runtime-canonical-eval-gate.md` | **Awaiting authorization** | 8 tasks to close Gap 2a (automated evals, P0). Design complete, 12/12 decisions resolved. |
| `2026-06-20-handoff-runcontext-option-b.md` | **Blocked (REV 3)** | Handoff as RunContext — 4 P0 gates pending, ~730 LOC |
| `2026-06-23-skill-canons-bridge-arch-fixes.md` | **Deferred (red team)** | 5 architectural fixes deferred by measured-harness-evolution-lifecycle. Resume after 2026-08-22. |
| `2026-06-23-correction-first-scavenger-pipeline-unified.md` | **Partially complete** | Pending: G2 (classifier calibration with real data), G4 (scavenger dry-run), E2E smoke test (8.4) |

### 6.4 Curriculum Gaps

- All 8 core concepts in `curriculum/05-core-concepts/` are marked as `⏳` (pending) — content exists in files but status indicates incomplete
- `FAQ.md` marked "em construção" (under construction)
- `curriculum-model.md` canonical doc not yet written (documented gap in system-of-record)

### 6.5 Infrastructure Gaps

- PR template in `long-running-agents/.github/PULL_REQUEST_TEMPLATE.md` references files (`src/lib/safe-console.js`, `src/lib/logger.js`, `docs/guides/crossroad-change-policy.md`) that don't exist yet — noted in system-of-record.md:141
- `obsidian-eval` drift detection is currently lexical only (not semantic) — upgrade to embeddings is planned (documented in ecosystem-glossary.md:521)

### 6.6 Telemetry Coverage Gaps

- `is_inferred=1` spans have lower quality (no real latency, no trace_id, no measured tokens) — the scavenger pipeline is a fallback, not equivalent to direct instrumentation
- Classifier calibration with real production data is pending (G2 in scavenger pipeline plan)

---

## Appendix: File Reference Index

| File | Description |
|---|---|
| `/mnt/c/Users/pavan/AGENTS.md` | Workspace-level operational rules (711 lines) |
| `/mnt/c/Users/pavan/long-running-agents/AGENTS.md` | Agent rules for long-running-agents vault (274 lines, 17 rules) |
| `/mnt/c/Users/pavan/long-running-agents/README.md` | Project overview (178 lines) |
| `/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md` | Documentation precedence, domain catalog, ADR status, gap documentation (397 lines) |
| `/mnt/c/Users/pavan/long-running-agents/docs/ecosystem-glossary.md` | 30 cross-cutting terms in 4 levels (606 lines) |
| `/mnt/c/Users/pavan/long-running-agents/docs/canonical/` | 118 canonical pattern documents |
| `/mnt/c/Users/pavan/long-running-agents/curriculum/` | 12-week program: 23 directories/files across 4 levels |
| `/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md` | Curriculum-specific glossary (1002 lines) |
| `/mnt/c/Users/pavan/long-running-agents/curriculum/MASTER_PLAN.md` | Master plan (604 lines) |
| `/mnt/c/Users/pavan/long-running-agents/curriculum/05-core-concepts/` | 8 core concept documents |
| `/mnt/c/Users/pavan/long-running-agents/docs/decisions/` | 1 accepted ADR |
| `/mnt/c/Users/pavan/plans/adr/` | 13 accepted ADRs (ecosystem-wide) |
| `/mnt/c/Users/pavan/raw-knowledge/AGENTS.md` | Ontology schema, page types, typed links, hard rules (323 lines) |
| `/mnt/c/Users/pavan/raw-knowledge/concepts/` | 110 concept pages in typed ontology |
| `/mnt/c/Users/pavan/raw-knowledge/concepts/harness-engineering.md` | Harness engineering concept (126 lines) |
| `/mnt/c/Users/pavan/.opencode/skills/` | 30 agent skills |
| `/mnt/c/Users/pavan/.opencode/agents/` | 3 agent definitions |
