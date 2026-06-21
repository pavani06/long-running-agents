---
title: "Mental Model — long-running-agents Repository"
type: analysis
date: 2026-06-18
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness-engineering", "governanca"]
aliases: ["2026-06-18 memory selection problem mental model"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[curriculum/MASTER_PLAN|Master Plan]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]"]
---

# Mental Model — long-running-agents Repository

Built for analysis pipeline Phase 0. All claims supported by file:line evidence.

## 1. Project Goals

**What the repository builds or teaches.**

The repository is a knowledge base and curriculum program for building AI systems that operate reliably for hours or days without losing context, planning ability, or quality judgment ([[README|README.md]]:10-12).

Core thesis: "Agentes de IA são cada vez mais capazes em tarefas curtas, mas degradam rapidamente conforme a execução se alonga. Não é uma limitação de modelo -- é uma lacuna de engenharia" ([[README|README.md]]:16-19).

Three structural reasons agents fail on long runs ([[README|README.md]]:24-29):
1. **Context loss** — token window fills, agent "forgets" what it was doing
2. **Fragile planning** — without decomposition, agent tries to solve everything at once
3. **Blind self-evaluation** — the same model that generates also evaluates, approving bad quality as good

The solution is **harness engineering**: building support infrastructure that wraps the model and ensures reliability on long executions ([[README|README.md]]:20-21). The repository documents, teaches, and operationalizes these patterns.

Target audience: "Pessoas de negócio com skill em construção de agentes e sistemas agenticos" ([[README|README.md]]:34).

Operational scope:
- Teaching: 12-week curriculum, 4 levels, 8 core concepts ([[curriculum/README|curriculum/README.md]]:1-7)
- Reference: 85+ canonical patterns ([[docs/system-of-record|system-of-record.md]]:144-235)
- Automation: harness pipeline (`analyze-and-improve` in 7 phases) ([[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve SKILL.md]]:49-57)
- Navigation: Obsidian vault with wikilinks, dataview dashboards, knowledge graphs ([[README|README.md]]:110-121)

## 2. Architecture

**Core abstractions and their relationships.**

### 2.1 Harness (Estrutura de Suporte)

The central abstraction. "A infraestrutura e padrões que envolvem um ou mais agentes para fazê-los mais confiáveis por períodos longos" ([[curriculum/GLOSSARY|GLOSSARY.md]]:329-338).

Components: state persistence, planning mechanisms, evaluation loops, agent coordination. Analogy: if agent is an airplane pilot, harness is the airplane + control tower + fuel ([[curriculum/GLOSSARY|GLOSSARY.md]]:338-340).

### 2.2 Owned Agent Control Loop

Decomposes agent execution into 4 components ([[docs/canonical/owned-agent-control-loop|owned-agent-control-loop.md]]:31-52):
1. **Prompt** — versioned, A/B tested instructions
2. **Context Builder** — deliberate token construction, summarization, compression
3. **Switch Statement** — deterministic routing from model JSON to handler code
4. **Loop** — iteration control with intervention points: break, summarize, LM-as-judge, human approval gate, force terminate

### 2.3 Generator-Evaluator

Two-agent architecture separating generation from evaluation ([[docs/canonical/generator-evaluator|generator-evaluator.md]]:29-31):
- **Generator**: creative, user-facing, tight conversation-focused context
- **Evaluator**: impartial, constraint-facing, reads persisted client state, applies rubrics

Quantified gap: self-evaluation detects ~3% of real errors, external evaluation detects ~14%, 11% silent failure rate ([[docs/canonical/generator-evaluator|generator-evaluator.md]]:27).

### 2.4 External State Persistence

Decouples agent memory from model memory ([[docs/canonical/external-state-persistence|external-state-persistence.md]]:57): critical data stored externally, loaded every turn. Comprises 6 component canonical docs: Addressable Memory Catalog, Head-Tail Context Truncation, Serializable Pause/Resume State, Stable Harness Prompt, Epistemic Memory Graph, Closed-Loop Agent OS ([[docs/canonical/external-state-persistence|external-state-persistence.md]]:70-76).

### 2.5 Plan-Execute-Verify

Three-phase decomposition with per-phase contracts ([[docs/canonical/plan-execute-verify|plan-execute-verify.md]]:31-73):
- **Plan**: atomic steps + success criteria
- **Execute**: one step at a time, checkpoint after each
- **Verify**: compare results to gates

### 2.6 LLM as Fuzzy Compiler

Mental model treating LLM as compiler backend, harness as optimization passes, code as disposable build artifact ([[docs/canonical/llm-as-fuzzy-compiler|llm-as-fuzzy-compiler.md]]:33-67). Durable assets are constraints/prompts/rubrics, not generated code.

### 2.7 Agent System (HoP — Handoff Protocol)

3 agents defined in `.opencode/agents/` ([[docs/system-of-record|system-of-record.md]]:33-35):
- `hop-orchestrator-rezek`: primary orchestrator — governance, source-of-truth, coordination
- `koda-hop-init-basic`: guided KODA initialization subagent
- `hop-live-whatsapp-tester`: live WhatsApp testing subagent

28 skills in `.opencode/skills/` covering issue workflows, orchestration, documentation, error hygiene, shadow review, token budgets, intent decomposition, etc. ([[README|README.md]]:100-104).

### 2.8 Knowledge Management

Obsidian-based vault with:
- `docs/canonical/`: 85 authoritative pattern descriptions
- `docs/system-of-record.md`: documentation precedence, domain map, active patterns
- `curriculum/`: 12-week program with 4 levels, 8 core concepts, 35+ diagrams
- Wikilinks for all cross-references ([[AGENTS|AGENTS.md]]:166-168)
- Cross-vault navigation via `obsidian-eval` CLI ([[README|README.md]]:159)

### Relationship Map

```
Harness (umbrella concept)
├── Owned Agent Control Loop (execution architecture)
│   ├── Prompt (component 1)
│   ├── Context Builder (component 2) → uses Head-Tail Truncation, Hybrid Context Stack
│   ├── Switch Statement (component 3) → Deterministic Tool Dispatch
│   └── Loop (component 4) → hosts Error Context Hygiene, Plan-Execute-Verify
├── Generator-Evaluator (quality architecture)
│   ├── Uses External State Persistence (Evaluator reads persisted constraints)
│   ├── Uses Constraint-Anchored Evaluation
│   └── Validated by Eval Tier Stratification, Multi-Model Evaluation Council
├── External State Persistence (memory architecture)
│   ├── Addressable Memory Catalog (retrieval handles)
│   ├── Head-Tail Context Truncation (active context management)
│   ├── Serializable Pause/Resume State (persistence mechanics)
│   ├── Stable Harness Prompt (contract preservation)
│   ├── Epistemic Memory Graph (provenance tracking)
│   └── Closed-Loop Agent OS (feedback writeback)
├── Plan-Execute-Verify (task architecture)
│   └── Checkpoints via Serializable Pause/Resume State
└── LLM as Fuzzy Compiler (meta-model)
    ├── Governed by Measured Harness Evolution Lifecycle
    └── Implemented via Invariant-Compensation Split
```

## 3. Patterns

**Existing design and implementation patterns.**

All patterns reside in `docs/canonical/`. The system-of-record lists 85 active canonical patterns ([[docs/system-of-record|system-of-record.md]]:144-235).

### Core Patterns (sampled)

| Pattern | File | Problem Solved | Maturity |
|---|---|---|---|
| Owned Agent Control Loop | `docs/canonical/owned-agent-control-loop.md` | Framework-owned loops prevent intervention | Active — Partial Coverage at creation |
| Error Context Hygiene | `docs/canonical/error-context-hygiene.md` | Context pollution from raw errors | Active — classified as Missing at creation |
| Deterministic Tool Dispatch | `docs/canonical/deterministic-tool-dispatch.md` | Tools treated as framework magic | Active — 12-Factor Agents Pattern 2 |
| Generator-Evaluator | `docs/canonical/generator-evaluator.md` | Self-evaluation confirmation bias | Active — Partial Coverage at creation |
| External State Persistence | `docs/canonical/external-state-persistence.md` | Context amnesia on long runs | Active — Partial Coverage at creation |
| Head-Tail Context Truncation | `docs/canonical/head-tail-context-truncation.md` | Naive truncation loses anchors | Active — Partial Coverage |
| Eval Tier Stratification | `docs/canonical/eval-tier-stratification.md` | Single suite can't serve all depths | Active — Partial Coverage |
| Plan-Execute-Verify | `docs/canonical/plan-execute-verify.md` | Planning-Execution Collapse | Active — Partial Coverage at creation |
| LLM as Fuzzy Compiler | `docs/canonical/llm-as-fuzzy-compiler.md` | Teams treat generated code as durable | Active — classified as Missing at creation |
| Budget-Aware Session Handoff | `docs/canonical/budget-aware-session-handoff.md` | Token budget exhaustion | Active |
| Addressable Memory Catalog | `docs/canonical/addressable-memory-catalog.md` | Omitted memory unrecoverable | Active |
| Hybrid Context Stack | `docs/canonical/hybrid-context-stack.md` | Context assembly policy | Active |

### Pattern Creation Pipeline

New patterns enter via the `analyze-and-improve` pipeline ([[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve SKILL.md]]:49-57):
1. Knowledge Extraction from external source
2. Pattern Extraction into reusable forms
3. Classification against repository (Better Impl, Partial Coverage, Missing)
4. Improvement Generation (canonical docs, skills, exercises, roadmap)
5. Integration into system-of-record and indices

### Pattern Classification Categories

Used during Phase 3 of the pipeline:
- **Better Impl**: repo already has superior implementation
- **Partial Coverage**: repo has components but no unified pattern
- **Missing**: no equivalent exists in repo
- **Exists**: full coverage already present

## 4. Abstractions — Key Terminology

**From GLOSSARY.md and canonical docs.**

| Term | Definition | Source |
|---|---|---|
| Agent | Autonomous AI entity that takes actions, uses tools, executes task sequences | ([[curriculum/GLOSSARY|GLOSSARY.md]]:17-19) |
| Agent Loop | Repetitive cycle: receive input → think → act → get result → repeat | ([[curriculum/GLOSSARY|GLOSSARY.md]]:28-29) |
| Context Amnesia | Agent "forgets" prior context after exceeding context window | ([[curriculum/GLOSSARY|GLOSSARY.md]]:37-39) |
| Context Window | Total tokens a model can process at once — immediate memory | ([[curriculum/GLOSSARY|GLOSSARY.md]]:145-146) |
| Harness | Infrastructure and patterns wrapping agents for long-term reliability | ([[curriculum/GLOSSARY|GLOSSARY.md]]:329-338) |
| Harness Engineering | Discipline of building support infrastructure around the model | ([[README|README.md]]:20-21) |
| Generator | Agent responsible for building/creating (pairs with Evaluator) | ([[curriculum/GLOSSARY|GLOSSARY.md]]:279-280) |
| Evaluator | Separate agent that evaluates Generator's work against rubrics | ([[curriculum/GLOSSARY|GLOSSARY.md]]:179-181) |
| Generator/Evaluator Pattern | Two entities collaborate: one generates, another evaluates | ([[curriculum/GLOSSARY|GLOSSARY.md]]:292-293) |
| Sprint Contract | Negotiated agreement between Generator and Evaluator on done definition | ([[curriculum/GLOSSARY|GLOSSARY.md]]:165-166) |
| Evaluation Rubric | Measurable criteria set for evaluating subjective quality | ([[curriculum/GLOSSARY|GLOSSARY.md]]:195-196) |
| State Persistence | Storing agent context externally to survive token window limits | ([[curriculum/GLOSSARY|GLOSSARY.md]]:337-342 - from glossary entries) |
| Token Budget | Allocation of tokens a session/agent can consume | (derived from head-tail-context-truncation, explicit-token-budget-ledger) |
| Compaction | Process of summarizing/compressing old context to make space | ([[curriculum/GLOSSARY|GLOSSARY.md]]:68-69) |
| Context Progressive Disclosure | Loading context on-demand via resolver triggers, not monolithic prompt | ([[curriculum/GLOSSARY|GLOSSARY.md]]:158-160) |
| Fuzzy Compiler | Mental model: LLM = compiler, harness = optimization passes, code = artifact | ([[curriculum/GLOSSARY|GLOSSARY.md]]:230-241) |
| Constraint Budget Gate | Limit of 5-7 directional business-language constraints per task | ([[curriculum/GLOSSARY|GLOSSARY.md]]:93-101) |
| Goal Atomicity Split | Each goal must be one sentence without conjunctions | ([[curriculum/GLOSSARY|GLOSSARY.md]]:263-271) |
| Owner-of-No | Role whose explicit job is refusing low-value work | ([[docs/canonical/owner-of-no-role-design|owner-of-no-role-design.md]]) |
| KODA | Reference agent: e-commerce supplement sales via WhatsApp (2+ hour conversations) | ([[README|README.md]]:21, [[curriculum/README|curriculum/README.md]]:34) |
| HoP (Handoff Protocol) | Agent system model with closed scopes, owners, validation gates | ([[docs/system-of-record|system-of-record.md]]:27) |
| System of Record | Source of truth for documentation precedence, domains, active patterns | ([[docs/system-of-record|system-of-record.md]]:1-2) |
| Wikilinks | `[[path|display]]` format for all cross-references in markdown | ([[AGENTS|AGENTS.md]]:166-168) |

## 5. Curriculum Structure

**Progression, levels, exercises.**

### Overview

12-week complete program teaching construction of long-running agents ([[curriculum/README|curriculum/README.md]]:1-7). Applied to KODA reference system.

### Levels

| Level | Name | Focus | Time | Source |
|---|---|---|---|---|
| 1 | Fundamentos | Context windows, token budgeting, basic harness patterns | 3-4h | ([[README|README.md]]:56-61) |
| 2 | Padrões Práticos | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading | 6-8h | ([[README|README.md]]:56-61) |
| 3 | Arquitetura Avançada | Multi-agent systems, state persistence, file-based coordination, harness evolution | 8-10h | ([[README|README.md]]:56-61) |
| 4 | Aplicação KODA | Architecture, customer journey flows, feature patterns, real implementation | Continuous | ([[README|README.md]]:56-61) |

### 8 Core Concepts

Each with deep explanation, 3 knowledge graphs, KODA application, implementation checklist ([[curriculum/README|curriculum/README.md]]:253-270):
1. Context Management (N1)
2. Planning vs. Execution (N2)
3. Generator/Evaluator (N2)
4. Sprint Contracts (N2)
5. State Persistence (N3)
6. Harness Evolution (N3)
7. Multi-Agent Coordination (N3)
8. Evaluation Rubrics (N2)

### Persona-Based Entry Points

(From [[curriculum/INDEX|INDEX.md]]:17-64 and [[README|README.md]]:36-46):
- **Newcomer**: QUICK_START → Nível 1 (45 min onboarding)
- **LLM-experienced**: "Pule para Prático" → Nível 2 (30 min)
- **Architect/senior**: "Vá Direto para Avançado" → Nível 3 (30 min)
- **KODA team**: Nível 4 → architecture + case studies (continuous)
- **Reference lookup**: GLOSSARY.md / FAQ.md (instant)

### Exercises

(From [[curriculum/INDEX|INDEX.md]]:99-136):
- N1: 2 exercises (fundamentals)
- N2: 7 exercises (generator/evaluator, sprint contracts, rubric design, error context hygiene, intent five-part primitive, two-implementations goal test, goal atomicity split)
- N3: 13 exercises (multi-agent design, state persistence, harness evolution, llm-as-fuzzy-compiler, persona-based-documentation, presence-in-the-loop, constraint-budget-gate, etc.)
- N4: 4+ exercises (KODA real-world: manual brake, deferred ledger, etc.)

### Supporting Materials

- 5 case studies: retro-game-maker, browser-daw, koda-product-discovery, koda-order-processing, koda-fulfillment-workflow ([[curriculum/INDEX|INDEX.md]]:141-148)
- 35+ Mermaid diagrams in `06-knowledge-graphs/`
- 6 implementation guides in `07-implementation-guides/`
- 6 templates in `08-tools-templates/` (sprint contract, rubric, knowledge graph, ADR, progress tracker, learning rubric)
- 3 references in `10-references/`

## 6. Existing Gaps

**What is documented as missing or pending.**

### 6.1 No Formal ADRs
`docs/decisions/` contains only `.gitkeep` — no Architecture Decision Records have been formally registered ([[docs/system-of-record|system-of-record.md]]:135). Candidates listed:
- Portal stack choice (vanilla JS vs. framework)
- Content chunking model
- Agent state persistence strategy
- Curriculum versioning policy

### 6.2 Pending Canonical Docs
(From [[docs/system-of-record|system-of-record.md]]:237-245):
- `agent-lifecycle.md`: claim → worktree → implement → review → merge → cleanup cycle
- `curriculum-model.md`: taxonomy of levels, artifact types, quality criteria
- `portal-architecture.md`: portal design decisions when SPA is implemented
- `crossroad-change-policy.md`: high-blast-radius file change policy

### 6.3 Canonical Docs Marked as Missing/Partial at Creation
Multiple canonical docs were created from analyses where they were classified as **Missing** or **Partial Coverage**. Each doc documents what existed at creation time and what the doc added:

- `error-context-hygiene.md`: classified as Missing — "no equivalent mechanism exists" ([[docs/canonical/error-context-hygiene|error-context-hygiene.md]]:15)
- `owned-agent-control-loop.md`: Partial Coverage — general principle existed, 4-component decomposition missing ([[docs/canonical/owned-agent-control-loop|owned-agent-control-loop.md]]:15)
- `llm-as-fuzzy-compiler.md`: Missing — concept only in analysis docs, not in repo artifacts ([[docs/canonical/llm-as-fuzzy-compiler|llm-as-fuzzy-compiler.md]]:90-97)
- `generator-evaluator.md`: Partial Coverage — 12+ eval docs, no unified Generator-Evaluator doc ([[docs/canonical/generator-evaluator|generator-evaluator.md]]:96-105)
- `external-state-persistence.md`: Partial Coverage — 6 component docs, no umbrella pattern ([[docs/canonical/external-state-persistence|external-state-persistence.md]]:78-84)
- `plan-execute-verify.md`: Partial Coverage — 7 component docs, no three-phase doc ([[docs/canonical/plan-execute-verify|plan-execute-verify.md]]:86-93)

### 6.4 PR Template References Nonexistent Files
The PR template references `src/lib/safe-console.js`, `src/lib/logger.js`, etc. and `docs/guides/crossroad-change-policy.md` that do not yet exist ([[docs/system-of-record|system-of-record.md]]:131).

### 6.5 Cross-Context Knowledge Siloing
Pattern `cross-context-knowledge-siloing.md` documents a gap: knowledge created in one agent context becomes invisible to agents in another context — two sub-patterns: namespace isolation and burial in non-indexed handoff bodies ([[docs/system-of-record|system-of-record.md]]:235).

### 6.6 Integration Gaps
Several patterns documented as canonical lack integration with the curriculum or implementation:
- No curriculum lesson for LLM as Fuzzy Compiler (compensated by exercise at N3)
- No unified integration guide showing how state persistence + constraint-anchored evaluation + generator-evaluator compose
- No tier registry that maps eval suites to fast/medium/deep ([[docs/canonical/eval-tier-stratification|eval-tier-stratification.md]]:66-72)

---

*Generated: 2026-06-18 | Phase 0: Repository Mental Model | Analysis pipeline*
