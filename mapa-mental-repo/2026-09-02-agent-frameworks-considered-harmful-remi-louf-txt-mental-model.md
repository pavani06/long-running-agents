---
title: "Mental Model — long-running-agents Repository (as of 48c5d45)"
type: analysis
date: 2026-09-02
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness-engineering", "governanca", "stack-tooling"]
aliases: ["2026-09-02 agent frameworks considered harmful mental model"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[curriculum/MASTER_PLAN|Master Plan]]", "[[docs/decisions/2026-09-01-vault-federation-consultable-registry|Vault Federation ADR]]"]
---

# Mental Model — long-running-agents Repository

Built for analysis pipeline Phase 0. All claims supported by file:line evidence. Repository state as of `base_commit: 48c5d45`.

## 1. Project Goals

**What the repository builds or teaches.**

The repository is a knowledge base and curriculum program for building AI systems that operate reliably for hours, days, or as long as the task demands, without losing context, planning ability, or quality judgment ([[README|README.md]]:10-12).

Core thesis: AI agents are increasingly capable on short tasks but degrade rapidly as execution lengthens; this is not a model limitation but an engineering gap ([[README|README.md]]:16-19). The discipline that addresses it is **harness engineering** — building the support infrastructure that wraps the model and guarantees reliability on long runs ([[README|README.md]]:20-21).

Three structural failure modes the repository attacks ([[README|README.md]]:24-29):
1. **Context loss** — the token window fills and the agent "forgets"
2. **Fragile planning** — without decomposition the agent tries to solve everything at once
3. **Blind self-evaluation** — the same model that generates also evaluates, approving bad quality as good

The repository has five concurrent goals:
- **Teach** — a 12-week curriculum (4 levels, 8 core concepts, 35+ diagrams) applied to the KODA reference agent ([[README|README.md]]:52-62)
- **Reference** — 176 canonical agentic architecture patterns in `docs/canonical/` ([[README|README.md]]:67)
- **Operationalize** — the `analyze-and-improve` pipeline that ingests external sources and produces canonical docs, skills, and exercises ([[README|README.md]]:136)
- **Govern** — `docs/system-of-record.md` as the single source of truth for documentation precedence and domain routing ([[README|README.md]]:165-166)
- **Template** — a complete `.opencode/` agent system (HoP: 3 agents, 36 skills) reusable as a template ([[README|README.md]]:140)

## 2. Architecture

**Core abstractions and their relationships.**

### Abstractions

- **Harness** — the central abstraction: infrastructure and patterns wrapping one or more agents for long-term reliability ([[curriculum/GLOSSARY|GLOSSARY.md]]:411-424). Components: state persistence, planning, evaluation loops, agent coordination.
- **Owned Agent Control Loop** — decompose framework-controlled loop into Prompt, Context Builder, Switch Statement, Loop with explicit intervention points ([[README|README.md]]:73).
- **Generator/Evaluator** — two-agent architecture separating generation from evaluation; the model that generates must not evaluate its own output ([[README|README.md]]:82).
- **Plan-Execute-Verify** — three-phase task decomposition with per-phase input/output contracts and checkpoints ([[README|README.md]]:83).
- **External State Persistence** — decoupling agent memory from model memory via serializable pause/resume and addressable memory ([[README|README.md]]:76-78).
- **LLM as Fuzzy Compiler** — mental model where the LLM is the compiler backend, the harness is the optimization passes, generated code is a disposable build artifact; durable assets are domain constraints and rubrics ([[curriculum/GLOSSARY|GLOSSARY.md]]:312-326).
- **HoP (Handoff Protocol)** — the agent system model: each agent has a closed scope, an owner, and validation gates ([[docs/system-of-record|system-of-record.md]]:27).
- **System of Record** — six-level documentation precedence (ADR > canonical > evidence > analysis > archive > README) plus domain map ([[docs/system-of-record|system-of-record.md]]:14-21).
- **Obsidian Vault / obsidian-eval** — wikilink-based knowledge management with cross-vault navigation via the `@pavani_org/obsidian-eval` CLI ([[README|README.md]]:159); vault federation is an accepted ADR ([[docs/decisions/2026-09-01-vault-federation-consultable-registry|Vault Federation ADR]]).

### Relationships

- Harness **contains** Owned Agent Control Loop
- Owned Agent Control Loop **hosts** Error Context Hygiene, Deterministic Tool Dispatch (intervention points)
- Generator/Evaluator **depends on** External State Persistence (Evaluator reads persisted state)
- Generator/Evaluator **depends on** Constraint-Anchored Evaluation
- External State Persistence **is composed of** Addressable Memory Catalog, Head-Tail Context Truncation, Serializable Pause/Resume State
- LLM as Fuzzy Compiler **is governed by** Measured Harness Evolution Lifecycle (BUILD → STABILIZE → SIMPLIFY → REMOVE)
- `analyze-and-improve` pipeline **populates** `docs/canonical/` and **integrates into** `curriculum/`
- System of Record **arbitrates** all documentation conflicts

## 3. Patterns

**Existing design and implementation patterns.** 176 canonical patterns live in `docs/canonical/` ([[README|README.md]]:67). A representative foundation plus the six documented project domains:

| Pattern | Where defined | Maturity |
|---|---|---|
| Owned Agent Control Loop | docs/canonical/owned-agent-control-loop.md | Active (12FA Pattern 3) |
| Deterministic Tool Dispatch | docs/canonical/deterministic-tool-dispatch.md | Active (12FA Pattern 2) |
| Error Context Hygiene | docs/canonical/error-context-hygiene.md | Active (12FA Pattern 6) |
| Serializable Pause/Resume State | docs/canonical/serializable-pause-resume-state.md | Active (12FA Pattern 4) |
| Generator/Evaluator | docs/canonical/generator-evaluator.md | Active |
| Plan-Execute-Verify | docs/canonical/plan-execute-verify.md | Active |
| Head-Tail Context Truncation | docs/canonical/head-tail-context-truncation.md | Active |
| Addressable Memory Catalog | docs/canonical/addressable-memory-catalog.md | Active |
| Eval Tier Stratification | docs/canonical/eval-tier-stratification.md | Active |
| Production Failure Regression Flywheel | docs/canonical/production-failure-regression-flywheel.md | Active |
| Budget-Aware Session Handoff | docs/canonical/budget-aware-session-handoff.md | Active |
| LLM as Fuzzy Compiler | docs/canonical/llm-as-fuzzy-compiler.md | Active |
| Intent Five-Part Primitive | docs/canonical/intent-five-part-primitive.md | Active |
| Constraint Budget Gate | docs/canonical/constraint-budget-gate.md | Active |
| Goal Atomicity Split | docs/canonical/goal-atomicity-split.md | Active |
| Owner of No Role | docs/canonical/owner-of-no-role-design.md | Active |
| Shadow Review Pipeline | docs/canonical/shadow-review-pipeline.md | Active |
| Relational Context Graph | docs/canonical/relational-context-graph.md | Active (foundation of selection patterns) |
| Measured Harness Evolution Lifecycle | docs/canonical/measured-harness-evolution-lifecycle.md | Active |
| Skill-Resolver-Skillify Capability Pipeline | docs/canonical/skill-resolver-skillify-capability-pipeline.md | Active |

The pattern set is organized into domain clusters ([[docs/system-of-record|system-of-record.md]]:174-351): context engineering, token economics, evals, multi-agent coordination, harness lifecycle, code review, governance, plus production-derived patterns from Sierra, Kavak, Snowflake GTM, Qodo, and Clay.

## 4. Abstractions — Key Terminology

| Term | Definition | Source |
|---|---|---|
| Agent | Autonomous AI entity (LLM-based) that takes actions, uses tools, executes task sequences | GLOSSARY.md:17-19 |
| Agent Loop | Repetitive cycle: input → think → act → result → repeat | GLOSSARY.md:41-46 |
| Harness | Infrastructure + patterns wrapping agents for long-term reliability | GLOSSARY.md:411-424 |
| Harness Engineering | Discipline of building support infra around the model for reliable long executions | README.md:20-21 |
| Context Window | Total tokens a model processes at once — the agent's immediate memory | GLOSSARY.md:173-181 |
| Context Amnesia | Forgetting prior context after exceeding the window | GLOSSARY.md:50-58 |
| Context Rot | Gradual coherence loss as the agent advances through the window | GLOSSARY.md:164-170 |
| Generator | Agent responsible for creating; pairs with Evaluator | GLOSSARY.md:361-370 |
| Evaluator | Separate agent evaluating Generator's work against rubrics | GLOSSARY.md:248-260 |
| Sprint Contract | Negotiated agreement on "done" before starting | GLOSSARY.md:206-214 |
| Evaluation Rubric | Measurable criteria for evaluating subjective quality | GLOSSARY.md:264-280 |
| Sycophancy | LLM tendency to please, approving bad quality | GLOSSARY.md:810-820 |
| Fuzzy Compiler | LLM = backend, harness = passes, code = disposable build artifact | GLOSSARY.md:312-326 |
| KODA | Reference agent: WhatsApp supplement sales with 2+ hour conversations | README.md:21 |
| HoP (Handoff Protocol) | Agent model: closed scope, owner, validation gates | system-of-record.md:27 |
| System of Record | Precedence + conflict resolution (ADR > canonical > evidence > analysis > archive > README) | system-of-record.md:14-21 |
| ADR | Document recording a significant architecture decision, context, consequences | GLOSSARY.md:61-68 |
| Wikilink | `[[path|Display]]` format for all cross-references | AGENTS.md:166-168 |
| Canonical Doc | Authoritative reference pattern doc (`type: canonical`) | ecosystem-glossary.md:370-382 |

## 5. Curriculum Structure

**Progression, levels, exercises.** A 12-week program, 30-50 hours per person ([[curriculum/README|README.md]]:13, 302).

| Level | Name | Focus | Time |
|---|---|---|---|
| 1 | Fundamentos | Context windows, token budgeting, basic harness patterns — why agents fail | 3-4h |
| 2 | Padrões Práticos | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading | 6-8h |
| 3 | Arquitetura Avançada | Multi-agent systems, state persistence, file-based coordination, harness evolution | 8-10h |
| 4 | Aplicação KODA | KODA architecture, customer journeys, feature patterns, implementation | Continuous |

**8 core concepts** ([[curriculum/README|README.md]]:275-284): Context Management (L1), Planning vs. Execution (L2), Generator/Evaluator (L2), Sprint Contracts (L2), State Persistence (L3), Harness Evolution (L3), Multi-Agent Coordination (L3), Evaluation Rubrics (L2).

Directory layout: `01-nivel-1-fundamentals/` through `04-nivel-4-koda-specific/`, plus `05-core-concepts/`, `06-knowledge-graphs/`, `07-implementation-guides/`, `08-tools-templates/`, `09-case-studies/`, `10-references/` ([[curriculum/README|README.md]]:59-202). Each level has `exercises/`, `koda-applications/`, and (N4) `real-world-exercises/` + `case-studies/`.

## 6. Existing Gaps

**What is documented as missing or pending.**

- **Curriculum artifacts pending** — `docs/canonical/agent-lifecycle.md`, `curriculum-model.md`, `portal-architecture.md` ([[docs/system-of-record|system-of-record.md]]:71, 100, 113, 352-358)
- **Crossroad files referenced but nonexistent** — PR template cites `src/lib/safe-console.js`, `src/lib/logger.js`, `docs/guides/crossroad-change-policy.md` ([[docs/system-of-record|system-of-record.md]]:145)
- **ADRs pending decisions** — stack choice for portal, content chunking, state-persistence strategy, curriculum versioning ([[docs/system-of-record|system-of-record.md]]:164-168)
- **Vault federation follow-ups** — add `mhc-knowledge-base` as 8th `vault-entry`; regenerate federated graph when obsidian-eval/hop-ecosystem-atlas gain Karpathy-pattern index ([[docs/decisions/2026-09-01-vault-federation-consultable-registry|Vault Federation ADR]]:84-85)
- **Skill-Canons Bridge follow-ups** — align system-design to 4-phase budget gate; extract shared module when >5 bridged skills ([[docs/decisions/2026-06-24-skill-canons-bridge-implementation|Skill-Canons Bridge ADR]]:91-93)
- **Drift detection limitation** — lexical only (not semantic); embeddings upgrade planned ([[docs/ecosystem-glossary|ecosystem-glossary.md]]:521)
