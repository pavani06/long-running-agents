---
title: "Mental Model: Stanford CS153 AI-Native Company 1000x Engineer"
type: analysis
tags: ["agentes-orquestracao", "curriculo-conteudo", "context-engineering", "evals", "governanca"]
date: 2026-06-10
aliases: ["modelo CS153", "orientacao CS153", "AI-native mental model", "1000x engineer"]
last_updated: 2026-06-10
relates-to: ["[[docs/system-of-record|System of Record]]", "[[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-mental-model|12-Factor Agents Mental Model]]", "[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-mental-model|Context Management Mental Model]]", "[[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-mental-model|Eval Maturity Mental Model]]"]
sources: ["[[AGENTS|AGENTS]]", "[[README|README]]", "[[docs/system-of-record|System of Record]]", "[[curriculum/README|Curriculum README]]"]
---

# Mental Model: long-running-agents

**Date:** 2026-06-10  
**Repo:** `long-running-agents`  
**Type:** `mental-model`  
**Scope:** repository-only reading before analyzing any external Stanford CS153 source.

## 1. Project Goals

`long-running-agents` is a knowledge base, curriculum, and agent-operations workspace for making AI agents reliable over hours, days, or as long as the task requires. The repo frames the core failure modes as context loss, fragile planning, and blind self-evaluation, and names harnesses as the support structures that manage context, decompose work, and separate generation from evaluation (`README.md:3`, `README.md:7-13`).

- Teach business builders and agent-system builders how to operate long-running agents, from beginner level through production practice (`README.md:15-17`).
- Deliver a 12-week curriculum with 4 levels, 8 core concepts, and 35+ diagrams, applied to KODA, the WhatsApp supplement-sales agent used as the running case study (`curriculum/README.md:10-13`, `curriculum/README.md:20-33`).
- Preserve a source-of-truth hierarchy so accepted ADRs, canonical docs, evidence, analyses, archives, and operational summaries do not compete silently (`docs/system-of-record.md:14-21`, `AGENTS.md:64-75`).
- Operationalize agent work through `.opencode/` agents and skills, with issue lifecycle, worktree isolation, validation gates, review, merge, and cleanup flows (`AGENTS.md:7-12`, `.opencode/skills/issue-start/SKILL.md:12-15`, `.opencode/skills/issue-review/SKILL.md:12-15`, `.opencode/skills/issue-finish/SKILL.md:12-15`).
- Maintain canonical pattern docs that turn prior analyses into reusable architecture and reliability guidance for future curriculum and implementation work (`docs/system-of-record.md:124-149`, `.opencode/skills/analyze-and-improve/SKILL.md:46-57`).

## 2. Architecture

### Core Abstractions

| Abstraction | Role | Evidence |
|---|---|---|
| System of record | Resolves documentation conflicts and maps project domains. | `docs/system-of-record.md:12-21`, `docs/system-of-record.md:23-46` |
| Curriculum | Main product: a 12-week program organized by levels, core concepts, graphs, guides, templates, cases, and references. | `docs/system-of-record.md:48-74`, `curriculum/README.md:56-173` |
| Canonical pattern library | Authoritative layer for active agentic architecture patterns, mostly classified as Active with Partial Coverage or Missing implementation details. | `docs/system-of-record.md:124-149`, `docs/canonical/error-context-hygiene.md:12-16`, `docs/canonical/eval-tier-stratification.md:12-16` |
| `.opencode` agent system | Operational layer for HoP agents, skills, issue workflow, documentation workflow, and analysis workflow. | `docs/system-of-record.md:25-46`, `.opencode/agents/hop-orchestrator-rezek.md:21-39`, `.opencode/skills/analyze-and-improve/SKILL.md:46-57` |
| HoP issue lifecycle | Claim issue, branch from `main`, create worktree, read context, brief, validate, draft PR, second-agent review, merge after approval, and cleanup. | `.opencode/skills/issue-start/SKILL.md:24-89`, `.opencode/skills/issue-review/SKILL.md:24-100`, `.opencode/skills/issue-finish/SKILL.md:25-84` |
| KODA case domain | Practical application domain for product discovery, order processing, fulfillment, customer journeys, and feature design. | `README.md:79-88`, `curriculum/GLOSSARY.md:239-250`, `curriculum/README.md:223-234` |
| Analysis packages | Prior sessions are structured outputs containing analysis, patterns, classification, mental model, and integration roadmap artifacts. | `docs/system-of-record.md:172-197`, `.opencode/skills/analyze-and-improve/SKILL.md:102-119` |
| Stack and tooling | Node >= 20.18, ESM, ESLint, npm validation gates, OpenCode orchestration, Obsidian knowledge management, and static HTML portals. | `README.md:107-113`, `AGENTS.md:53-63`, `docs/system-of-record.md:88-101` |

### Relationships

- `docs/system-of-record.md` governs source precedence, while `AGENTS.md` governs behavior for agents changing the repository (`docs/system-of-record.md:14-21`, `AGENTS.md:14-32`).
- The curriculum teaches generic long-running-agent concepts, then Level 4 applies them to KODA through architecture, journeys, feature patterns, rubrics, harness improvements, real-world exercises, and case studies (`curriculum/README.md:177-234`, `curriculum/INDEX.md:374-381`).
- The canonical docs split into three main clusters: agent-loop ownership, context reliability, and eval maturity (`docs/canonical/owned-agent-control-loop.md:31-75`, `docs/canonical/head-tail-context-truncation.md:26-39`, `docs/canonical/pain-signal-eval-progression-gate.md:26-51`).
- The agent-loop cluster links `Owned Agent Control Loop`, `Deterministic Tool Dispatch`, `Serializable Pause/Resume State`, and `Error Context Hygiene`: owned loops expose prompt, context-builder, switch-statement, loop, pause, summarize, break, and error-hygiene intervention points (`docs/canonical/owned-agent-control-loop.md:31-75`, `docs/canonical/deterministic-tool-dispatch.md:22-35`, `docs/canonical/serializable-pause-resume-state.md:31-61`, `docs/canonical/error-context-hygiene.md:93-106`).
- The context-reliability cluster keeps the stable prompt and head/tail anchors active, externalizes the middle behind an addressable catalog, then validates continuity through N+1 and late-failure suites (`docs/canonical/stable-harness-prompt.md:26-41`, `docs/canonical/head-tail-context-truncation.md:26-39`, `docs/canonical/addressable-memory-catalog.md:26-43`, `docs/canonical/n-plus-one-long-session-evals.md:26-40`, `docs/canonical/late-failure-regression-suite.md:26-42`).
- The eval-maturity cluster starts from pain signals, then grows into repeatable spot checks, production sampling, tiered evals, PR gates, production-failure regressions, and correlation tracking (`docs/canonical/pain-signal-eval-progression-gate.md:40-51`, `docs/canonical/repeatable-agent-spot-check-set.md:26-51`, `docs/canonical/production-grounded-eval-sampling.md:26-51`, `docs/canonical/eval-tier-stratification.md:26-49`, `docs/canonical/pr-gated-eval-enforcement.md:26-53`, `docs/canonical/production-failure-regression-flywheel.md:26-54`, `docs/canonical/eval-to-production-correlation-tracking.md:26-50`).
- `.opencode/skills/analyze-and-improve` formalizes the workflow this task belongs to: Phase 0 is a repository mental model, followed by external-source extraction, pattern extraction, classification, improvement generation, integration, and optional curriculum deep integration (`.opencode/skills/analyze-and-improve/SKILL.md:123-190`).

## 3. Patterns

| Pattern | Where Defined | Maturity |
|---|---|---|
| Owned Agent Control Loop | `docs/canonical/owned-agent-control-loop.md` | Active canonical pattern; Partial Coverage because the repo has the general harness principle but still lacks the explicit 4-component decomposition and named intervention points (`docs/canonical/owned-agent-control-loop.md:12-16`, `docs/canonical/owned-agent-control-loop.md:96-107`). |
| Deterministic Tool Dispatch | `docs/canonical/deterministic-tool-dispatch.md` | Active canonical pattern; Partial Coverage because mechanics exist, while the explicit teaching reframe, no-LLM dispatch tests, and audit logging guidance are missing (`docs/canonical/deterministic-tool-dispatch.md:12-16`, `docs/canonical/deterministic-tool-dispatch.md:68-85`). |
| Error Context Hygiene | `docs/canonical/error-context-hygiene.md`; `.opencode/skills/error-context-hygiene/SKILL.md` | Active canonical pattern and implementation skill; canonical status is Missing because the repo has fallback infrastructure but not context-level error curation (`docs/canonical/error-context-hygiene.md:12-16`, `docs/canonical/error-context-hygiene.md:108-135`, `.opencode/skills/error-context-hygiene/SKILL.md:13-20`). |
| Serializable Pause/Resume State | `docs/canonical/serializable-pause-resume-state.md` | Active canonical pattern; Partial Coverage because the repo rebuilds state each turn and lacks token-level mid-reasoning pause/resume fidelity (`docs/canonical/serializable-pause-resume-state.md:12-16`, `docs/canonical/serializable-pause-resume-state.md:59-76`, `docs/canonical/serializable-pause-resume-state.md:118-122`). |
| Stable Harness Prompt During Context Reduction | `docs/canonical/stable-harness-prompt.md` | Active canonical invariant; Partial Coverage because prompt/context separation is implied but not yet a named context-reduction contract (`docs/canonical/stable-harness-prompt.md:12-16`, `docs/canonical/stable-harness-prompt.md:26-41`, `docs/canonical/stable-harness-prompt.md:55-64`). |
| Head-Tail Context Truncation with Recoverable Middle | `docs/canonical/head-tail-context-truncation.md` | Active canonical context pattern; Partial Coverage because the repo teaches adjacent context management but lacks the named head/tail/recoverable-middle policy and eval proof (`docs/canonical/head-tail-context-truncation.md:12-16`, `docs/canonical/head-tail-context-truncation.md:26-39`, `docs/canonical/head-tail-context-truncation.md:52-62`). |
| Addressable Memory Catalog | `docs/canonical/addressable-memory-catalog.md` | Active canonical recovery pattern; Partial Coverage because broad retrieval exists but no deterministic omitted-memory catalog with `id`, `location`, `preview`, `scope`, and `fetch` is formalized (`docs/canonical/addressable-memory-catalog.md:12-16`, `docs/canonical/addressable-memory-catalog.md:28-43`, `docs/canonical/addressable-memory-catalog.md:57-67`). |
| N+1 Long-Session Evals | `docs/canonical/n-plus-one-long-session-evals.md` | Active canonical eval pattern; Partial Coverage because adjacent long-conversation checks exist but no named N-turn plus N+1 fixture shape is formalized (`docs/canonical/n-plus-one-long-session-evals.md:12-16`, `docs/canonical/n-plus-one-long-session-evals.md:26-40`, `docs/canonical/n-plus-one-long-session-evals.md:53-62`). |
| Late-Failure Regression Suite | `docs/canonical/late-failure-regression-suite.md` | Active canonical regression pattern; Partial Coverage because broader regression/canary guidance exists but no suite dedicated to late-session context failures is named (`docs/canonical/late-failure-regression-suite.md:12-16`, `docs/canonical/late-failure-regression-suite.md:26-42`, `docs/canonical/late-failure-regression-suite.md:55-64`). |
| Pain-Signal Eval Progression Gate | `docs/canonical/pain-signal-eval-progression-gate.md` | Active canonical eval-maturity pattern; Partial Coverage because adjacent harness decision habits exist but a named eval progression gate is missing (`docs/canonical/pain-signal-eval-progression-gate.md:12-16`, `docs/canonical/pain-signal-eval-progression-gate.md:26-51`, `docs/canonical/pain-signal-eval-progression-gate.md:63-72`). |
| Repeatable Agent Spot-Check Set | `docs/canonical/repeatable-agent-spot-check-set.md` | Active canonical first-eval pattern; Partial Coverage because repeatable traces and regression batteries exist but not a named seed set and metadata contract (`docs/canonical/repeatable-agent-spot-check-set.md:12-16`, `docs/canonical/repeatable-agent-spot-check-set.md:26-51`, `docs/canonical/repeatable-agent-spot-check-set.md:64-73`). |
| Production-Grounded Eval Sampling | `docs/canonical/production-grounded-eval-sampling.md` | Active canonical production-eval pattern; Partial Coverage because replay and sampled review are taught, while formal corpus, privacy, retention, labels, metadata, and replay contracts are missing (`docs/canonical/production-grounded-eval-sampling.md:12-16`, `docs/canonical/production-grounded-eval-sampling.md:26-51`, `docs/canonical/production-grounded-eval-sampling.md:64-74`). |
| Eval Tier Stratification | `docs/canonical/eval-tier-stratification.md` | Active canonical eval-governance pattern; Partial Coverage because validation layers exist but no explicit fast/medium/deep registry with runtime, cost, flakiness, trigger, and owner metadata exists (`docs/canonical/eval-tier-stratification.md:12-16`, `docs/canonical/eval-tier-stratification.md:26-49`, `docs/canonical/eval-tier-stratification.md:62-72`). |
| PR-Gated Eval Enforcement | `docs/canonical/pr-gated-eval-enforcement.md` | Active canonical PR gate pattern; Partial Coverage because strong PR validation exists but not eval-specific reports and merge policies for prompt/model/tool/context changes (`docs/canonical/pr-gated-eval-enforcement.md:12-16`, `docs/canonical/pr-gated-eval-enforcement.md:26-53`, `docs/canonical/pr-gated-eval-enforcement.md:67-78`). |
| Production Failure Regression Flywheel | `docs/canonical/production-failure-regression-flywheel.md` | Active canonical regression pattern; Partial Coverage because late-context regression exists but the general all-production-failure intake and dedupe flywheel is missing (`docs/canonical/production-failure-regression-flywheel.md:12-16`, `docs/canonical/production-failure-regression-flywheel.md:26-54`, `docs/canonical/production-failure-regression-flywheel.md:67-78`). |
| Eval-to-Production Correlation Tracking | `docs/canonical/eval-to-production-correlation-tracking.md` | Active canonical calibration pattern; Partial Coverage because calibration and dashboards exist, but no named system joins eval history to production outcomes with decay triggers (`docs/canonical/eval-to-production-correlation-tracking.md:12-16`, `docs/canonical/eval-to-production-correlation-tracking.md:26-50`, `docs/canonical/eval-to-production-correlation-tracking.md:65-76`). |
| Analyze-and-improve pipeline | `.opencode/skills/analyze-and-improve/SKILL.md` | Active analysis workflow; it defines repository mental modeling as Phase 0 and writes `YYYY-MM-DD-slug-mental-model.md` plus `YYYY-MM-DD-slug-mental-model.yaml` before external source analysis (`.opencode/skills/analyze-and-improve/SKILL.md:46-57`, `.opencode/skills/analyze-and-improve/SKILL.md:123-190`). |
| Issue lifecycle skills | `.opencode/skills/issue-start/SKILL.md`; `.opencode/skills/issue-review/SKILL.md`; `.opencode/skills/issue-finish/SKILL.md` | Operationally active, but the system-of-record still lists a canonical `agent-lifecycle.md` as pending (`.opencode/skills/issue-start/SKILL.md:12-15`, `.opencode/skills/issue-review/SKILL.md:12-15`, `.opencode/skills/issue-finish/SKILL.md:12-15`, `docs/system-of-record.md:46-47`). |
| Refine Issue | `.opencode/skills/refine-issue/SKILL.md` | Active planning workflow that researches the codebase, decomposes work into single-file-focused sub-issues, orders dependencies, and requires a final Verification Gate (`.opencode/skills/refine-issue/SKILL.md:8-21`, `.opencode/skills/refine-issue/SKILL.md:46-86`). |
| Doc Co-Authoring | `.opencode/skills/doc-coauthoring/SKILL.md` | Active documentation workflow with context gathering, iterative section drafting, and reader testing (`.opencode/skills/doc-coauthoring/SKILL.md:6-23`, `.opencode/skills/doc-coauthoring/SKILL.md:242-331`). |
| Writing Plans | `.opencode/skills/writing-plans/SKILL.md` | Active planning workflow for exact implementation plans saved under `docs/plans/YYYY-MM-DD-<feature-name>.md` (`.opencode/skills/writing-plans/SKILL.md:8-17`, `.opencode/skills/writing-plans/SKILL.md:40-52`). |
| KODA live test handoff | `.opencode/agents/koda-hop-init-basic.md`; `.opencode/agents/hop-live-whatsapp-tester.md` | Operational agent pattern: init collects phone/menu state, option 2 hands off to the live tester, and the live tester captures scenario, response, route, side effects, latency, verdict, gaps, and regression recommendations (`.opencode/agents/koda-hop-init-basic.md:18-27`, `.opencode/agents/koda-hop-init-basic.md:49-52`, `.opencode/agents/hop-live-whatsapp-tester.md:18-20`, `.opencode/agents/hop-live-whatsapp-tester.md:45-76`). |

## 4. Abstractions

| Term | Definition | Source |
|---|---|---|
| Agent | Autonomous AI entity that takes actions, uses tools, and executes sequential tasks. | `curriculum/GLOSSARY.md:16-23` |
| Agent Loop | Repeated input, reasoning, action, result, and repeat cycle. | `curriculum/GLOSSARY.md:27-33` |
| Context Window | Total tokens a model can process at once, treated as immediate memory. | `curriculum/GLOSSARY.md:89-98` |
| Context Amnesia | Forgetting prior context after exceeding the context window. | `curriculum/GLOSSARY.md:36-43` |
| Context Rot | Gradual coherence loss as an agent advances through context. | `curriculum/GLOSSARY.md:80-85` |
| Context Anxiety | Rushed or anxious behavior near the context limit. | `curriculum/GLOSSARY.md:69-76` |
| Token Budget | Conscious accounting of available and consumed tokens. | `curriculum/GLOSSARY.md:466-477` |
| Harness | Infrastructure and patterns around agents that keep them reliable over long periods. | `curriculum/GLOSSARY.md:204-217` |
| Harness Evolution | Simplifying or removing harness components as models improve. | `curriculum/GLOSSARY.md:221-233` |
| Generator | Agent responsible for building or creating something. | `curriculum/GLOSSARY.md:154-163` |
| Evaluator | Separate agent responsible for evaluating and grading generator output. | `curriculum/GLOSSARY.md:116-128` |
| Generator/Evaluator Pattern | Two separate entities collaborate: one generates and the other evaluates. | `curriculum/GLOSSARY.md:167-185` |
| Sprint Contract | Pre-work agreement between generator and evaluator about what done means. | `curriculum/GLOSSARY.md:102-110`, `curriculum/GLOSSARY.md:430-433` |
| Evaluation Rubric | Measurable criteria for judging subjective quality. | `curriculum/GLOSSARY.md:132-148` |
| Memory / State | Information retained across operations, including short-term, long-term, and file-based forms. | `curriculum/GLOSSARY.md:267-277` |
| Multi-Agent System | Multiple independent agents coordinating, commonly Planner plus Generator plus Evaluator. | `curriculum/GLOSSARY.md:294-306` |
| Planner | Agent specialized in decomposing a problem into steps or sprints. | `curriculum/GLOSSARY.md:312-326` |
| Compaction | Compressing or summarizing old context while preserving key information. | `curriculum/GLOSSARY.md:60-66` |
| Trace | Detailed log of agent steps used for behavior debugging. | `curriculum/GLOSSARY.md:480-495` |
| KODA | WhatsApp supplement-sales conversational agent and case study for applying the program. | `curriculum/GLOSSARY.md:239-250` |
| Deterministic Tool Dispatch | Tool use reframed as model-emitted JSON followed by deterministic application code. | `docs/canonical/deterministic-tool-dispatch.md:22-35` |
| Owned Agent Control Loop | Agent architecture decomposed into owned prompt, context builder, switch statement, and loop. | `docs/canonical/owned-agent-control-loop.md:31-75` |
| Addressable Memory Catalog | Compact omitted-context interface with `id`, `kind`, `location`, `preview`, `scope`, and `fetch`. | `docs/canonical/addressable-memory-catalog.md:28-43` |
| N+1 Long-Session Eval | Fixture that loads N realistic turns, applies production context strategy, then grades behavior on turn N+1. | `docs/canonical/n-plus-one-long-session-evals.md:26-40` |

## 5. Curriculum Structure

The curriculum is organized as master documents, 4 content levels, 8 core concepts, knowledge graphs, implementation guides, templates, case studies, and references (`curriculum/README.md:56-173`, `curriculum/MASTER_PLAN.md:331-399`). The execution plan turns that structure into 12 weeks: foundation, patterns, architecture, and KODA application (`curriculum/README.md:261-275`, `curriculum/EXECUTION_PLAN.md:35-58`).

| Level | Focus | Progression and Exercises | Evidence |
|---|---|---|---|
| Level 1 - Fundamentals | Why long tasks fail: context windows, token budgeting, and basic harness patterns. | 3-4h in the curriculum overview; execution plan expands weeks 1-2 with History Windowing and Structured Output exercises. | `curriculum/README.md:177-189`, `curriculum/QUICK_START.md:34-89`, `curriculum/EXECUTION_PLAN.md:64-113` |
| Level 2 - Practical Patterns | Generator/Evaluator, Sprint Contracts, Rubric Design, and Trace Reading. | 6-8h, aimed at applying reliability patterns in real code; exercises cover Generator/Evaluator, Sprint Contracts, Rubric Design, and Error Context Hygiene in the index. | `curriculum/README.md:193-204`, `curriculum/QUICK_START.md:93-157`, `curriculum/INDEX.md:104-109` |
| Level 3 - Advanced Architecture | Multi-agent systems, state persistence, file-based coordination, server-side compaction, and harness evolution. | 8-10h, with 3-agent design, state persistence, and harness evolution exercises. | `curriculum/README.md:208-219`, `curriculum/QUICK_START.md:160-222`, `curriculum/INDEX.md:110-113` |
| Level 4 - KODA-specific | KODA architecture, customer journeys, feature patterns, KODA rubrics, harness improvements, real-world exercises, and case studies. | Continuous application phase from weeks 7-12, including improvements, deployment, lessons learned, mentoring, and next-cycle planning. | `curriculum/README.md:223-234`, `curriculum/QUICK_START.md:226-258`, `curriculum/EXECUTION_PLAN.md:237-310` |

Core concepts are: Context Management, Planning vs. Execution, Generator/Evaluator, Sprint Contracts, State Persistence, Harness Evolution, Multi-Agent Coordination, and Evaluation Rubrics (`curriculum/README.md:238-257`, `curriculum/MASTER_PLAN.md:331-348`, `curriculum/INDEX.md:83-95`). Cross-cutting materials include knowledge graphs, templates, implementation guides, and case studies (`curriculum/INDEX.md:135-169`, `curriculum/INDEX.md:123-131`).

## 6. Existing Gaps

| Gap | Where Documented |
|---|---|
| No formal ADR has been recorded; `docs/decisions/` is empty. | `docs/system-of-record.md:114-123`; `docs/decisions/` file search returned no Markdown files. |
| `agent-lifecycle.md` is pending for the full claim -> worktree -> implement -> review -> merge -> cleanup lifecycle. | `docs/system-of-record.md:46-47`, `docs/system-of-record.md:150-155` |
| `curriculum-model.md` is pending for level taxonomy, artifact types, and quality criteria. | `docs/system-of-record.md:73-74`, `docs/system-of-record.md:150-156` |
| `portal-architecture.md` is pending until the proposed SPA architecture matures or is implemented. | `docs/system-of-record.md:75-87`, `docs/system-of-record.md:150-156` |
| `crossroad-change-policy.md` and several crossroad files referenced by governance material do not exist yet. | `docs/system-of-record.md:102-112`, `docs/system-of-record.md:150-157` |
| `docs/system-of-record.md` lists `obsidian-document-conventions.md` as active, but direct file search found only 16 canonical Markdown files and `docs/canonical/obsidian-document-conventions.md` was NOT_FOUND. | `docs/system-of-record.md:124-149`; `NOT_FOUND: docs/canonical/obsidian-document-conventions.md`; `glob: docs/canonical/**/*.md -> 16 files` |
| Error Context Hygiene is a canonical pattern and skill, but the equivalent repository mechanism is still classified as Missing. | `docs/canonical/error-context-hygiene.md:12-16`, `docs/canonical/error-context-hygiene.md:108-135` |
| Context-reduction work still lacks explicit head/tail boundary policy, exact recoverable middle, deterministic memory catalog, N+1 fixture runner, prompt-stability invariant tests, and late-failure suite ownership. | `docs/canonical/head-tail-context-truncation.md:52-62`, `docs/canonical/addressable-memory-catalog.md:57-67`, `docs/canonical/n-plus-one-long-session-evals.md:53-62`, `docs/canonical/stable-harness-prompt.md:55-64`, `docs/canonical/late-failure-regression-suite.md:55-64` |
| Eval-maturity work still lacks a named progression gate, spot-check metadata contract, production corpus, tier registry, PR eval report, generalized production-failure flywheel, and correlation system. | `docs/canonical/pain-signal-eval-progression-gate.md:63-72`, `docs/canonical/repeatable-agent-spot-check-set.md:64-73`, `docs/canonical/production-grounded-eval-sampling.md:64-74`, `docs/canonical/eval-tier-stratification.md:62-72`, `docs/canonical/pr-gated-eval-enforcement.md:67-78`, `docs/canonical/production-failure-regression-flywheel.md:67-78`, `docs/canonical/eval-to-production-correlation-tracking.md:65-76` |
| The KODA `.opencode` agents reference canonical `operations`, `product`, and `architecture` docs that are not present under `docs/canonical/` in this checkout. | `.opencode/agents/koda-hop-init-basic.md:28-34`, `.opencode/agents/hop-live-whatsapp-tester.md:22-31`; `NOT_FOUND: docs/canonical/operations/**`, `NOT_FOUND: docs/canonical/product/**`, `NOT_FOUND: docs/canonical/architecture/**` |
| Curriculum navigation is partially stale: README and INDEX call `FAQ.md` in construction, while the actual FAQ declares itself complete. | `curriculum/README.md:63-68`, `curriculum/README.md:463-465`, `curriculum/INDEX.md:342-349`, `curriculum/FAQ.md:11-15` |
| Level 2 exercise count diverges: `MASTER_PLAN.md` says 3 exercises, while README and INDEX include a fourth Error Context Hygiene exercise. | `curriculum/MASTER_PLAN.md:200-206`, `curriculum/README.md:83-95`, `curriculum/INDEX.md:104-109` |

## Synthesis

The useful mental model is: `long-running-agents` is a curriculum, an operations playbook for agent work, and a canonical pattern lab. The curriculum teaches long-running-agent harnesses through KODA; `.opencode` turns work into traceable HoP issue and testing workflows; `docs/system-of-record.md` resolves authority; `docs/canonical/` records reusable patterns plus maturity gaps. Future external-source analysis should compare new claims against those four layers before proposing changes.
