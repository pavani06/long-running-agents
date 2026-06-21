---
title: "Mental Model: long-running-agents"
type: analysis
date: 2026-06-16
aliases: ["modelo mental policy distillation", "phase 0 policy distillation", "long-running-agents mental model", "repository mental model"]
tags: ["agentes-orquestracao", "curriculo-conteudo", "context-engineering", "evals", "governanca", "harness-engineering"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[AGENTS|AGENTS.md]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]", "[[curriculum/GLOSSARY|Glossary]]", "[[.opencode/skills/analyze-and-improve/SKILL.md|Analyze and Improve Skill]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
sources: ["[[AGENTS|AGENTS.md]]", "[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]", "[[curriculum/GLOSSARY|Glossary]]"]
---

# Mental Model: long-running-agents

**Date:** 2026-06-16  
**Repo:** `long-running-agents`  
**Type:** `mental-model`  
**Scope:** Phase 0 repository mental model only. The external policy-distillation source document was not read or analyzed in this phase.

## 1. Project Goals

The repository is a knowledge base, curriculum, and operational agent-work system for building long-running AI agents that remain reliable over hours or days. The README frames the root problem as three structural long-run failures: context loss, fragile planning, and blind self-evaluation; the repository response is harnesses that manage context, decompose work, and separate generation from evaluation (`README.md:3`, `README.md:7-13`).

| Goal | Evidence |
|---|---|
| Build and manage long-running AI agent workflows, with `.opencode/` as the agent/skill system, Node >= 20.18.0 + ESLint as stack, `.runtime/` and `artifacts/` as runtime state, and accepted ADRs in `docs/decisions/` when they exist. | `AGENTS.md:5-12`; `package.json:4-13` |
| Teach a 12-week, 4-level curriculum with 8 core concepts and 35+ diagrams for people building agentic systems. | `curriculum/README.md:11-13`; `curriculum/README.md:17-34` |
| Apply the curriculum to KODA, a WhatsApp supplement-sales agent that must preserve quality in conversations lasting 30 minutes to 4 hours. | `curriculum/README.md:33-34`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:144-159` |
| Maintain documentation governance by explicit precedence: accepted ADRs, active canonical docs, validated evidence, analysis docs, archive docs, then READMEs and operational summaries. | `docs/system-of-record.md:12-21`; `AGENTS.md:80-91` |
| Convert external knowledge into repository improvements through a repeatable analyze-and-improve pipeline: mental model, knowledge extraction, pattern extraction, classification, improvements, integration, and curriculum integration. | `.opencode/skills/analyze-and-improve/SKILL.md:171-270`; `.opencode/skills/analyze-and-improve/SKILL.md:49-57` |
| Operate agent work through HoP-style GitHub issue workflows: claim, worktree, execution brief, validation, draft PR, second-agent review, explicit merge, cleanup. | `.opencode/skills/issue-start/SKILL.md:12-15`; `.opencode/skills/issue-review/SKILL.md:12-15`; `.opencode/skills/issue-finish/SKILL.md:12-24` |

## 2. Architecture

### Core Abstractions

| Abstraction | Role in the repo | Evidence |
|---|---|---|
| System of Record | Resolves documentation conflicts, maps project domains, inventories active canonical sources, and records documented gaps. | `docs/system-of-record.md:12-23`; `docs/system-of-record.md:140-235` |
| Documentation Precedence | Authority order is accepted ADRs > canonical docs > evidence > analysis > archive > READMEs/operational summaries. | `docs/system-of-record.md:14-21`; `AGENTS.md:80-91` |
| Canonical Pattern Catalog | Authoritative pattern library under `docs/canonical/`; the SOR says the directory is no longer empty and records 65 active canonical patterns. | `docs/system-of-record.md:140-146`; `docs/system-of-record.md:148-225` |
| Curriculum | Primary product: 12-week program with 4 levels, 8 concepts, exercises, solutions, KODA applications, knowledge graphs, implementation guides, templates, case studies, and references. | `docs/system-of-record.md:62-88`; `curriculum/README.md:57-186`; `curriculum/MASTER_PLAN.md:182-270` |
| KODA Case Domain | Applied proof surface: a WhatsApp sales agent with 8 internal agents, SQLite + JSON checkpointing, file-based coordination, and a Discovery -> Recommendation -> Cart -> Order -> Payment -> Fulfillment pipeline. | `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:144-159`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:161-173` |
| `.opencode` Agent System / HoP | Operational layer of agents and skills. SOR defines it as HoP with scoped ownership and validation gates; the agent files define a primary Rezek orchestrator plus KODA init and live WhatsApp tester subagents. | `docs/system-of-record.md:25-59`; `.opencode/agents/hop-orchestrator-rezek.md:21-39`; `.opencode/agents/koda-hop-init-basic.md:16-34`; `.opencode/agents/hop-live-whatsapp-tester.md:16-31` |
| Analyze-and-Improve Harness | Knowledge-to-improvement pipeline and harness contract. Phase 0 builds this mental model before any external-source analysis. | `.opencode/skills/analyze-and-improve/SKILL.md:171-173`; `.opencode/skills/analyze-and-improve/SKILL.md:239-270` |
| Issue Lifecycle | Safe GitHub issue lifecycle with isolated worktree setup, review gates, draft PR, and explicit merge confirmation. | `.opencode/skills/issue-start/SKILL.md:24-88`; `.opencode/skills/issue-review/SKILL.md:44-100`; `.opencode/skills/issue-finish/SKILL.md:50-84` |
| Application-Owned Control Plane | Control-plane contract joining versioned prompt, context builder, structured action schema, deterministic dispatch, loop policy, persistent state, and intervention gates. | `docs/canonical/application-owned-agent-control-plane.md:27-75` |
| Context and Memory Stack | Stable prompt, durable state, head/tail anchors, summaries, recoverable omitted middle, addressable memory catalog, token budget, and decision trace. | `docs/canonical/hybrid-context-stack.md:20-42`; `docs/canonical/external-state-persistence.md:31-57` |
| Eval and Regression Stack | Fast/medium/deep eval tiers with runtime, cost, flakiness, trigger, threshold, reporting, owner, and escalation policy. | `docs/canonical/eval-tier-stratification.md:20-49`; `docs/canonical/eval-tier-stratification.md:51-72` |
| Static Portal | Static HTML artifacts and future SPA proposal for course portal, Mermaid graph viewer, and MHC strategic view. | `docs/system-of-record.md:89-100`; `README.md:68-71` |
| Tooling and Validation | Node ESM project with real npm scripts; repository rules require real package scripts instead of invented gates. | `package.json:4-13`; `AGENTS.md:69-78` |

### Relationships

| From | To | Relationship | Evidence |
|---|---|---|---|
| System of Record | All docs and operational summaries | Higher-precedence artifacts control truth. Lower layers are navigation or analysis, not authority when conflicts exist. | `docs/system-of-record.md:12-21`; `AGENTS.md:80-91` |
| Canonical Pattern Catalog | Curriculum | Canonicals name durable patterns and gaps; the curriculum translates them into levels, exercises, templates, case studies, and KODA applications. | `docs/system-of-record.md:62-88`; `docs/system-of-record.md:140-225`; `curriculum/README.md:251-270` |
| Curriculum | KODA | N1-N3 teach generic long-running-agent concepts; N4 applies them to KODA architecture, journeys, feature patterns, rubrics, harness improvements, and real-world exercises. | `curriculum/README.md:190-247`; `curriculum/MASTER_PLAN.md:251-270`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:144-173` |
| `.opencode` Orchestrator | Issue Skills | Orchestrator selects/summarizes work and generates worker prompts; issue-start prepares, issue-review validates and stops, issue-finish merges only after explicit user confirmation. | `.opencode/skills/orchestrator/SKILL.md:12-24`; `.opencode/skills/orchestrator/SKILL.md:74-96`; `.opencode/skills/issue-start/SKILL.md:12-15`; `.opencode/skills/issue-review/SKILL.md:12-15`; `.opencode/skills/issue-finish/SKILL.md:12-24` |
| KODA Init Basic | Live WhatsApp Tester | Init collects the phone and, for option 2, hands off to the live tester with the confirmed phone; the tester accepts that handoff and enters direct chat mode. | `.opencode/agents/koda-hop-init-basic.md:50-52`; `.opencode/agents/hop-live-whatsapp-tester.md:55-59` |
| Application-Owned Control Plane | Owned Agent Control Loop + Deterministic Tool Dispatch | Control plane uses the four owned loop components and JSON-to-handler dispatch as the backbone of testable agent execution. | `docs/canonical/application-owned-agent-control-plane.md:29-75`; `docs/canonical/owned-agent-control-loop.md:29-75`; `docs/canonical/deterministic-tool-dispatch.md:20-67` |
| Context and Memory Stack | Long-session reliability | Long sessions rely on externalized durable facts, deliberate context assembly, addressable omitted memory, and budget-aware reductions instead of append-only transcripts. | `docs/canonical/hybrid-context-stack.md:30-42`; `docs/canonical/external-state-persistence.md:31-57`; `docs/canonical/owned-agent-control-loop.md:60-75` |
| Eval Tier Stratification | Review and release gates | Eval-sensitive changes should select fast/medium/deep validation, report skipped tiers, and tie evidence depth to risk. | `docs/canonical/eval-tier-stratification.md:28-49`; `.opencode/skills/issue-review/SKILL.md:57-85` |
| Closed-Loop Agent OS | Durable memory and prioritization | The OS connects state intake, priority synthesis, execution routing, and feedback writeback so outcomes become trusted future memory. | `docs/canonical/closed-loop-agent-operating-system.md:28-45`; `docs/canonical/closed-loop-agent-operating-system.md:59-68` |

## 3. Existing Patterns

### Pattern Families

| Family | Representative patterns | Mental model |
|---|---|---|
| Harness and control loop | Owned Agent Control Loop, Application-Owned Agent Control Plane, Deterministic Tool Dispatch, Error Context Hygiene, Stable Harness Prompt, Measured Harness Evolution, Tested Degradation Ladder | Own loop boundaries, build context deliberately, route JSON through deterministic code, log decisions, and expose intervention gates. Evidence: `docs/canonical/owned-agent-control-loop.md:20-75`; `docs/canonical/application-owned-agent-control-plane.md:27-75`; `docs/canonical/deterministic-tool-dispatch.md:20-67`; `.opencode/skills/error-context-hygiene/SKILL.md:13-20`. |
| Context engineering and memory | Hybrid Context Stack, External State Persistence, Head-Tail Context Truncation, Addressable Memory Catalog, Explicit Token Budget Ledger, Budget-Aware Session Handoff | Model calls are assembled from ordered layers under a token budget; durable facts and exact recoverable memory live outside the active context. Evidence: `docs/canonical/hybrid-context-stack.md:20-42`; `docs/canonical/external-state-persistence.md:31-57`. |
| Eval and regression architecture | Eval Tier Stratification, PR-Gated Eval Enforcement, Production Failure Regression Flywheel, N+1 Long-Session Evals, Late-Failure Regression Suite, Generator-Evaluator, Constraint-Anchored Evaluation | Evaluation is tiered by cost/risk, separate from generation, and grounded in production failures and constraints. Evidence: `docs/canonical/eval-tier-stratification.md:20-49`; `curriculum/GLOSSARY.md:292-310`; `curriculum/GLOSSARY.md:590-608`. |
| Intent and specification discipline | Intent Five-Part Primitive, Goal Atomicity Split, Two-Implementations Goal Test, Constraint Budget Gate, Constraint-Failure Decision Rule, ICE Craft Separation, Human-Owned Expectations Boundary | Intent is an inspectable artifact, not prose. Missing fields and compound goals are surfaced before execution. Evidence: `docs/canonical/intent-five-part-primitive.md:21-48`; `curriculum/GLOSSARY.md:263-275`; `curriculum/GLOSSARY.md:395-410`; `curriculum/GLOSSARY.md:736-748`. |
| Governance and value gates | Manual Brake Question Gate, Deferred Ledger for Agentic Work, Owner-of-No, Presence-in-the-Loop, Shadow Review Pipeline, Contextual Severity Calibration | The repo restores human value judgment and accountability before cheap agentic generation becomes permanent carry debt. Evidence: `.opencode/skills/manual-brake-question-gate/SKILL.md:13-21`; `docs/canonical/deferred-ledger-agentic-work.md:21-47`; `curriculum/GLOSSARY.md:534-548`. |
| Closed-loop operating system | Closed-Loop Agent Operating System, Skill-Resolver-Skillify Capability Pipeline, Resolver-Based Context Progressive Disclosure | Agents should observe state, select work, route to capabilities, validate outcomes, and write durable memory back. Evidence: `docs/canonical/closed-loop-agent-operating-system.md:20-45`; `curriculum/GLOSSARY.md:583-585`; `curriculum/GLOSSARY.md:158-160`. |
| HoP execution workflow | Orchestrator, issue-start, issue-review, issue-finish, live WhatsApp tester handoff | Work is organized by issue, scoped before editing, validated before PR/merge, and merged only with explicit confirmation. Evidence: `.opencode/skills/orchestrator/SKILL.md:12-24`; `.opencode/skills/issue-start/SKILL.md:24-88`; `.opencode/skills/issue-review/SKILL.md:44-100`; `.opencode/skills/issue-finish/SKILL.md:50-84`. |
| Publishing and repository governance | Quarto publishing architecture, Quarto authoring workflow, Quarto content structure, System of Record, Obsidian conventions | Documentation and publishing are treated as first-class architecture surfaces with frontmatter, wikilinks, tags, aliases, and `relates-to`. Evidence: `AGENTS.md:136-257`; `docs/system-of-record.md:223-225`. |

### Representative Pattern Inventory

| Pattern | Where defined | Maturity |
|---|---|---|
| Application-Owned Agent Control Plane | `docs/canonical/application-owned-agent-control-plane.md:11` | Active canonical, Partial Coverage; unifies loop, prompt, context, dispatch, state, and gates, while still documenting missing single-contract and vocabulary gaps (`docs/canonical/application-owned-agent-control-plane.md:13-17`; `docs/canonical/application-owned-agent-control-plane.md:98-103`). |
| Owned Agent Control Loop | `docs/canonical/owned-agent-control-loop.md:10` | Active canonical, Partial Coverage; 4-component decomposition is the desired frame, while framework-owned loop intervention points remain a gap (`docs/canonical/owned-agent-control-loop.md:12-16`; `docs/canonical/owned-agent-control-loop.md:29-75`; `docs/canonical/owned-agent-control-loop.md:96-107`). |
| Deterministic Tool Dispatch | `docs/canonical/deterministic-tool-dispatch.md:10` | Active canonical, Partial Coverage; the repo has mechanics but the named reframe, LLM-free dispatch testing, and audit guidance are the documented gap (`docs/canonical/deterministic-tool-dispatch.md:12-16`; `docs/canonical/deterministic-tool-dispatch.md:20-36`; `docs/canonical/deterministic-tool-dispatch.md:78-85`). |
| Error Context Hygiene | `.opencode/skills/error-context-hygiene/SKILL.md:13` | Active implementation skill; enforces summarize-don't-dump, clear-on-success, never-blind-append, and keep-only-needed rules for agent error context (`.opencode/skills/error-context-hygiene/SKILL.md:15-20`; `.opencode/skills/error-context-hygiene/SKILL.md:72-104`). |
| Hybrid Context Stack | `docs/canonical/hybrid-context-stack.md:10` | Active canonical, Partial Coverage; component layers exist but single budgeted inclusion order and context-builder trace were the gap (`docs/canonical/hybrid-context-stack.md:12-16`; `docs/canonical/hybrid-context-stack.md:20-42`; `docs/canonical/hybrid-context-stack.md:83-100`). |
| External State Persistence | `docs/canonical/external-state-persistence.md:11` | Active canonical, Partial Coverage; decouples agent memory from model memory and names missing unified persist-vs-context policy (`docs/canonical/external-state-persistence.md:13-17`; `docs/canonical/external-state-persistence.md:31-57`; `docs/canonical/external-state-persistence.md:78-83`). |
| Eval Tier Stratification | `docs/canonical/eval-tier-stratification.md:10` | Active canonical, Partial Coverage; defines fast/medium/deep taxonomy and says missing work is registry, metadata, selection rules, skipped-tier reporting, and quarantine (`docs/canonical/eval-tier-stratification.md:12-16`; `docs/canonical/eval-tier-stratification.md:28-49`; `docs/canonical/eval-tier-stratification.md:62-72`). |
| Closed-Loop Agent Operating System | `docs/canonical/closed-loop-agent-operating-system.md:10` | Active canonical, Partial Coverage with high integration value; connects state intake, priority synthesis, execution routing, and feedback writeback, but still lacks one named OS model and observability (`docs/canonical/closed-loop-agent-operating-system.md:12-16`; `docs/canonical/closed-loop-agent-operating-system.md:28-45`; `docs/canonical/closed-loop-agent-operating-system.md:59-68`). |
| Intent as Five-Part Primitive | `docs/canonical/intent-five-part-primitive.md:11` | Active canonical, Missing at classification time; defines description, constraints, failure scenarios, success scenarios, and connections plus pre-execution completeness gate (`docs/canonical/intent-five-part-primitive.md:13-17`; `docs/canonical/intent-five-part-primitive.md:31-48`; `docs/canonical/intent-five-part-primitive.md:64-75`). |
| Deferred Ledger for Agentic Work | `docs/canonical/deferred-ledger-agentic-work.md:11` | Active canonical, Missing at classification time; tracks Skill Debt, Dependence Debt, and Carry Debt above operational token cost tracking (`docs/canonical/deferred-ledger-agentic-work.md:13-17`; `docs/canonical/deferred-ledger-agentic-work.md:21-47`; `docs/canonical/deferred-ledger-agentic-work.md:68-78`). |
| Manual Brake Question Gate | `.opencode/skills/manual-brake-question-gate/SKILL.md:13` | Active decision skill; asks three value questions and outputs experiment/build/defer/stop with owner and rationale (`.opencode/skills/manual-brake-question-gate/SKILL.md:15-21`; `.opencode/skills/manual-brake-question-gate/SKILL.md:61-90`). |
| Generator/Evaluator | `curriculum/GLOSSARY.md:292` | Mature curriculum concept; separates creation from critique and is the answer to self-evaluation/sycophancy (`curriculum/GLOSSARY.md:292-310`; `curriculum/GLOSSARY.md:590-608`). |
| KODA Handoff Protocol | `.opencode/agents/koda-hop-init-basic.md:50` and `.opencode/agents/hop-live-whatsapp-tester.md:55` | Operationally active in agent definitions; option 2 hands off a confirmed phone to live tester direct-chat mode (`.opencode/agents/koda-hop-init-basic.md:50-52`; `.opencode/agents/hop-live-whatsapp-tester.md:55-59`). |

## 4. Abstractions and Terminology

| Term | Definition | Source |
|---|---|---|
| Agent | Autonomous LLM-based entity that can take actions, use tools, and execute tasks in sequence. | `curriculum/GLOSSARY.md:17-24` |
| Agent Loop | Repeated cycle where an agent receives input, thinks, acts, receives result, and repeats. | `curriculum/GLOSSARY.md:28-35` |
| Context Amnesia | Agent forgets prior context after exceeding the context window; KODA consequence is forgetting customer preferences or constraints. | `curriculum/GLOSSARY.md:37-44`; `docs/canonical/external-state-persistence.md:21-27` |
| Context Window | Maximum tokens a model can process at once, treated as immediate memory. | `curriculum/GLOSSARY.md:145-154` |
| Context Progressive Disclosure | Skills/capabilities loaded by resolver triggers instead of living in a monolithic prompt. | `curriculum/GLOSSARY.md:158-160` |
| Harness | Infrastructure and patterns around agents that make long-running execution reliable. | `curriculum/GLOSSARY.md:329-342` |
| Harness Evolution | Removing or simplifying harness components as model capability improves. | `curriculum/GLOSSARY.md:346-358` |
| Generator | Agent responsible for creating/building an output. | `curriculum/GLOSSARY.md:279-288` |
| Evaluator | Separate agent that evaluates generator output against rubrics. | `curriculum/GLOSSARY.md:179-191` |
| Generator/Evaluator Pattern | Two LLMs collaborate: one generates, another evaluates critically. | `curriculum/GLOSSARY.md:292-310` |
| Sprint Contract | Negotiated agreement between generator and evaluator about what done means before execution. | `curriculum/GLOSSARY.md:165-173`; `curriculum/GLOSSARY.md:650-653` |
| Evaluation Rubric | Measurable criteria for subjective quality. | `curriculum/GLOSSARY.md:195-211` |
| Trace | Detailed log of agent input, reasoning, actions, and output; main debugging surface. | `curriculum/GLOSSARY.md:717-732` |
| Memory / State | Information retained between operations, including short-term, long-term, and file-based storage. | `curriculum/GLOSSARY.md:444-454` |
| Multi-Agent System | Multiple independent agents coordinating, commonly Planner + Generator + Evaluator. | `curriculum/GLOSSARY.md:471-483` |
| Planner | Agent specialized in breaking problems into steps. | `curriculum/GLOSSARY.md:489-503` |
| Token Budget | Conscious management of token capacity and spending. | `curriculum/GLOSSARY.md:673-696`; `docs/canonical/hybrid-context-stack.md:34-42` |
| Intent as Five-Part Primitive | Intent with description, constraints, failure scenarios, success scenarios, and connections, checked before execution. | `curriculum/GLOSSARY.md:395-410`; `docs/canonical/intent-five-part-primitive.md:31-48` |
| ICE Craft Separation | Separates Intent, Context, and Expectations with explicit owners so gaps are closed before execution. | `curriculum/GLOSSARY.md:378-391` |
| Fuzzy Compiler | Mental model where LLM is compiler backend, harness is optimization passes, and generated code is a disposable build artifact. | `curriculum/GLOSSARY.md:230-244` |
| KODA | WhatsApp conversational supplement-sales agent and practical case study for all patterns. | `curriculum/GLOSSARY.md:416-427`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:144-159` |

## 5. Curriculum Structure

The curriculum is organized as top-level navigation, four learning levels, eight core concepts, exercises with solutions, knowledge graphs, implementation guides, templates, case studies, and references (`curriculum/README.md:57-186`; `curriculum/INDEX.md:80-183`). It also has an execution roadmap from weeks 1-2 (foundation) through weeks 7-12 (KODA-specific work) (`curriculum/MASTER_PLAN.md:274-330`).

### Levels

| Level | Focus | Progression and outputs | Evidence |
|---|---|---|---|
| Nivel 1 - Fundamentals | Why agents fail: context windows, token budgeting, and basic harness patterns. | 3-4 hours; three lessons, two exercises, KODA application, completion criteria around explaining failure modes and mapping concepts to KODA. | `curriculum/README.md:192-202`; `curriculum/MASTER_PLAN.md:184-201`; `curriculum/INDEX.md:101-104` |
| Nivel 2 - Practical Patterns | Generator/Evaluator, Sprint Contracts, Rubric Design, and Trace Reading. | 6-8 hours; seven exercises including Error Context Hygiene, Intent Five-Part Primitive, Two Implementations Goal Test, and Goal Atomicity Split. | `curriculum/README.md:206-217`; `curriculum/MASTER_PLAN.md:205-224`; `curriculum/INDEX.md:105-112` |
| Nivel 3 - Advanced Architecture | Multi-agent systems, state persistence, file-based coordination, server-side compaction, and harness evolution. | 8-10 hours; eleven exercises across multi-agent design, state persistence, harness evolution, fuzzy compiler, persona docs, presence, owner-of-no, shadow review, contextual severity, and constraint gates. | `curriculum/README.md:221-232`; `curriculum/MASTER_PLAN.md:228-247`; `curriculum/INDEX.md:114-125` |
| Nivel 4 - KODA-specific | KODA architecture, customer journeys, feature design patterns, KODA rubrics, harness improvements, and real implementation. | Continuous / 10+ hours; real-world exercises, KODA case studies, and production-like improvement work. | `curriculum/README.md:236-247`; `curriculum/MASTER_PLAN.md:251-270`; `curriculum/INDEX.md:127-145`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:144-173` |

### Core Concepts

| # | Concept | Evidence |
|---|---|---|
| 1 | Context Management | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| 2 | Planning vs. Execution | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| 3 | Generator/Evaluator | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367`; `curriculum/GLOSSARY.md:292-310` |
| 4 | Sprint Contracts | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367`; `curriculum/GLOSSARY.md:165-173` |
| 5 | State Persistence | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367`; `docs/canonical/external-state-persistence.md:31-57` |
| 6 | Harness Evolution | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367`; `curriculum/GLOSSARY.md:346-358` |
| 7 | Multi-Agent Coordination | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367`; `curriculum/GLOSSARY.md:471-483` |
| 8 | Evaluation Rubrics | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367`; `curriculum/GLOSSARY.md:195-211` |

### Cross-Cutting Surfaces

| Surface | Role | Evidence |
|---|---|---|
| Exercises | Practice path across N1-N4 with solutions in each level. | `curriculum/INDEX.md:99-133`; `curriculum/MASTER_PLAN.md:196-270` |
| Knowledge graphs | Concept ecosystem, KODA feature dependencies, learning progression, problem-solution mapping, and detailed concept diagrams. | `curriculum/README.md:149-158`; `curriculum/INDEX.md:149-157`; `curriculum/MASTER_PLAN.md:370-379` |
| Templates | Sprint contract, evaluation rubric, knowledge graph, ADR, progress tracker, and learning rubric templates. | `curriculum/README.md:167-173`; `curriculum/INDEX.md:161-170`; `curriculum/MASTER_PLAN.md:160-165` |
| Implementation guides | Setup, team progression, harness checklist, rubrics, trace analysis, and harness evolution playbook. | `curriculum/README.md:159-165`; `curriculum/INDEX.md:174-183`; `curriculum/MASTER_PLAN.md:383-389` |
| Case studies | Retro Game Maker, Browser DAW, and three KODA flows: discovery, order processing, fulfillment. | `curriculum/README.md:175-185`; `curriculum/INDEX.md:137-145`; `curriculum/MASTER_PLAN.md:167-172` |
| Glossary | Shared vocabulary for agentic systems, KODA, harnesses, evals, token budgeting, governance, and specification discipline. | `curriculum/GLOSSARY.md:9-24`; `curriculum/GLOSSARY.md:784-790` |

## 6. Existing Gaps

| Gap | Where documented / observed |
|---|---|
| No formal ADRs exist even though ADRs have highest precedence. | `docs/system-of-record.md:130-138`; direct directory read of `/mnt/c/Users/pavan/long-running-agents/docs/decisions` showed only `.gitkeep`. |
| `docs/canonical/agent-lifecycle.md` is still pending for the claim -> worktree -> implement -> review -> merge -> cleanup lifecycle. | `docs/system-of-record.md:60`; `docs/system-of-record.md:227-235` |
| `docs/canonical/curriculum-model.md` is still pending for level taxonomy, artifact types, and quality criteria. | `docs/system-of-record.md:87`; `docs/system-of-record.md:227-235` |
| `docs/canonical/portal-architecture.md` remains pending until the proposed SPA is implemented. | `docs/system-of-record.md:89-100`; `docs/system-of-record.md:227-235` |
| `docs/canonical/crossroad-change-policy.md` and crossroad files referenced by the PR template do not exist yet; SOR says they should be created when there is source code. | `docs/system-of-record.md:116-129`; `docs/system-of-record.md:227-235` |
| `docs/evidence/` and `docs/archive/` are in the precedence hierarchy, but direct directory reads showed only `.gitkeep` in each. | `docs/system-of-record.md:14-21`; direct reads of `/mnt/c/Users/pavan/long-running-agents/docs/evidence` and `/mnt/c/Users/pavan/long-running-agents/docs/archive`. |
| README's inventory is stale for canonical docs: it still says `docs/canonical/` has 16 active architecture patterns, while the SOR states there are 65 active canonical patterns. | `README.md:53-55`; `README.md:90-105`; `docs/system-of-record.md:140-146` |
| Application-Owned Agent Control Plane still needs a single canonical contract, explicit bridge between source inputs and loop components, persistent-state control-plane view, and unified intervention-gate vocabulary. | `docs/canonical/application-owned-agent-control-plane.md:98-103` |
| Hybrid Context Stack still records the gap of a single stack with budgeted inclusion order and context-builder decision trace. | `docs/canonical/hybrid-context-stack.md:22-32`; `docs/canonical/hybrid-context-stack.md:83-100` |
| External State Persistence still lacks unified persist-vs-context policy and a cohesive external-memory strategy connecting catalog, exact recovery, pause/resume, and writeback. | `docs/canonical/external-state-persistence.md:78-83` |
| Eval Tier Stratification still needs a registry, metadata per suite, selection rules, skipped-tier reporting, and quarantine process. | `docs/canonical/eval-tier-stratification.md:62-72` |
| Intent Five-Part Primitive and Deferred Ledger were classified as Missing when introduced: both now exist as canonicals and skills/exercises, but the docs still record the original repo-wide gap and desired integrations. | `docs/canonical/intent-five-part-primitive.md:13-17`; `docs/canonical/intent-five-part-primitive.md:64-75`; `docs/canonical/deferred-ledger-agentic-work.md:13-17`; `docs/canonical/deferred-ledger-agentic-work.md:68-78` |
| Some curriculum auxiliary directories are exercise-only or placeholders: `03-nivel-arquiteto/`, `03-nivel-3-operational/`, and `04-nivel-operador/` contain only `exercises/`; `04-nivel-4-koda-specific/exercises/` and `koda-applications/` contain only `.gitkeep`. | Direct directory reads of `/mnt/c/Users/pavan/long-running-agents/curriculum/03-nivel-arquiteto`, `/mnt/c/Users/pavan/long-running-agents/curriculum/03-nivel-3-operational`, `/mnt/c/Users/pavan/long-running-agents/curriculum/04-nivel-operador`, `/mnt/c/Users/pavan/long-running-agents/curriculum/04-nivel-4-koda-specific/exercises`, and `/mnt/c/Users/pavan/long-running-agents/curriculum/04-nivel-4-koda-specific/koda-applications`. |
| `issue-review` lists many optional npm gates not present in current `package.json`; AGENTS requires real scripts from `package.json`, so agents must select only existing gates unless the repo adds those scripts. | `.opencode/skills/issue-review/SKILL.md:44-75`; `package.json:8-13`; `AGENTS.md:69-78` |
| KODA agent definitions reference `docs/canonical/operations/`, `docs/canonical/product/`, and `docs/canonical/architecture/` paths that were not present in the direct canonical directory inspection. | `.opencode/agents/koda-hop-init-basic.md:28-34`; `.opencode/agents/hop-live-whatsapp-tester.md:22-31`; direct read/search did not find those directories in `/mnt/c/Users/pavan/long-running-agents/docs/canonical`. |

## Synthesis

The useful mental model is four coupled layers:

1. `docs/system-of-record.md` decides authority and project domains.
2. `docs/canonical/` names reusable agentic patterns, their maturity, and their gaps.
3. `curriculum/` turns those patterns into a 12-week learning path and KODA-specific application surface.
4. `.opencode/` operationalizes work through agents, skills, issue lifecycle, review gates, and analysis pipelines.

For subsequent phases of this analysis, compare the policy-distillation source against those layers in precedence order: first ADRs if any exist, then active canonical docs, then evidence, analyses, curriculum, and finally README/operational summaries. Do not let a new source duplicate an existing canonical pattern unless it adds a materially different mechanism or closes a documented gap.
