---
title: "Integration Roadmap: Matt Pocock AI Coding Workflow Patterns → long-running-agents"
type: analysis
date: 2026-06-07
domain: matt-pocock-workflow
aliases: ["roadmap matt pocock", "plano integracao pocock", "matt pocock integration plan", "WFAC integration roadmap"]
tags: ["agentes-orquestracao", "context-engineering", "evals", "governanca", "curriculo-conteudo"]
last_updated: 2026-06-11
relates-to: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|WFAC Classification]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|WFAC Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-mental-model|WFAC Mental Model]]", "[[docs/system-of-record|System of Record]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/plan-execute-verify|Plan Execute Verify]]", "[[docs/canonical/generator-evaluator|Generator Evaluator]]", "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|WFAC Classification]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|WFAC Patterns]]"]
---

> [!warning] Formato legado
> Este arquivo usa o formato histórico `integration-roadmap.md`.
> Sessões a partir de 2026-06-14 usam `<date>-<source-slug>-artifacts.{md,yaml}`.
> Preservado para rastreabilidade e estabilidade de wikilinks.

# Integration Roadmap: Matt Pocock AI Coding Workflow Patterns → long-running-agents

**Date:** 2026-06-07
**Type:** Analysis
**Precedence:** Level 4 (`docs/system-of-record.md:14`)
**Source:** `docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification.md`

---

## Objective

Map each of the 15 agentic coding workflow patterns extracted from Matt Pocock's "Full Walkthrough Workflow for AI Coding" to concrete integration points in the `long-running-agents` repository: canonical documentation, operational skills, curriculum modules, and governance surfaces. The roadmap plans canonical doc creation for all 12 Partial Coverage patterns, maps them to the 4-level curriculum structure, and defines a phase-gated dependency order so downstream patterns are not built on missing upstream contracts.

**Classification summary:** 1 Better Implementation, 2 Already Exists, 12 Partial Coverage. No patterns classified as Missing.

---

## 1. Summary Matrix

| # | Pattern | Classification | Impact | Effort | Priority | Integration Surface |
|---|---|---|---|---|---|---|
| 1 | Smart-Zone Context Management | Better Implementation | Low | Low | Reference | Cross-reference to `docs/canonical/phase-gated-token-health-monitor.md`, `docs/canonical/hybrid-context-stack.md`, `docs/canonical/budget-aware-session-handoff.md` |
| 2 | Grill-Me Alignment Interview | Partial Coverage | High | High | **P0** | New canonical doc `grill-me-alignment-interview.md`, new skill `.opencode/skills/grill-me/`, extension of `doc-coauthoring` skill |
| 3 | Shared Design Concept Handoff | Partial Coverage | High | High | **P0** | New canonical doc `shared-design-concept-handoff.md`, handoff contract between Grill-Me and PRD phases |
| 4 | Destination PRD | Partial Coverage | Medium | Medium | **P1** | New canonical doc `destination-prd.md`, PRD template in `curriculum/08-tools-templates/`, integration with `doc-coauthoring` skill |
| 5 | Human/AFK Task Routing Gate | Partial Coverage | High | Medium | **P1** | New canonical doc `human-afk-task-routing-gate.md`, new skill `.opencode/skills/task-router/`, extension of `orchestrator` skill |
| 6 | Vertical-Slice Issue Generation | Partial Coverage | High | Medium | **P1** | New canonical doc `vertical-slice-issue-generation.md`, extension of `refine-issue` skill, curriculum exercises |
| 7 | Agent Kanban | Partial Coverage | Medium | Medium | **P2** | New canonical doc `agent-kanban.md`, extension of `orchestrator` skill dashboard, GitHub Project board semantics |
| 8 | Ralph/AFK Implementation Loop | Partial Coverage | Medium | Medium | **P2** | New canonical doc `ralph-afk-implementation-loop.md`, new skill `.opencode/skills/afk-loop/`, integration with `issue-start`/`issue-review`/`issue-finish` |
| 9 | Feedback-Loop-Gated Implementation | Already Exists | Low | Low | Reference | Cross-reference to `docs/canonical/plan-execute-verify.md`, `docs/canonical/pr-gated-eval-enforcement.md`, `AGENTS.md` |
| 10 | Fresh-Context Review | Already Exists | Low | Low | Reference | Cross-reference to `docs/canonical/generator-evaluator.md`, `.opencode/skills/issue-review/SKILL.md` |
| 11 | Sandboxed Parallel Agents | Partial Coverage | Medium | Medium | **P2** | New canonical doc `sandboxed-parallel-agents.md`, extension of `issue-start` skill for container/VM isolation, conflict-resolution policy |
| 12 | Sub-Agent Exploration Compression | Partial Coverage | Medium | Low | **P3** | New canonical doc `sub-agent-exploration-compression.md`, update `AGENTS.md` exploration guidelines, schema for sub-agent output contract |
| 13 | Architecture-as-Agent-Affordance Refactoring | Partial Coverage | High | High | **P2** | New canonical doc `architecture-as-agent-affordance-refactoring.md`, new skill `.opencode/skills/arch-affordance/`, curriculum module |
| 14 | Phase-Scoped Documentation Hygiene | Partial Coverage | Medium | Low | **P3** | New canonical doc `phase-scoped-documentation-hygiene.md`, PRD/plan lifecycle labels in `docs/system-of-record.md`, archive/cleanup workflow |
| 15 | QA-to-Backlog Feedback Loop | Partial Coverage | High | Medium | **P2** | New canonical doc `qa-to-backlog-feedback-loop.md`, extension of `orchestrator` skill, QA intake lane in Kanban contract |

**Priority rationale:** P0 patterns (Grill-Me, Shared Design Concept Handoff) are the alignment layer that feeds every downstream phase — without them, PRDs, routing gates, and vertical slices operate on weak foundations. P1 patterns (Destination PRD, Human/AFK Routing Gate, Vertical-Slice Issue Generation) are the planning and decomposition layer that converts alignment into executable work. P2 patterns (Agent Kanban, AFK Loop, Sandboxed Parallel Agents, Architecture Affordance, QA-to-Backlog) are the execution and feedback layers. P3 patterns (Sub-Agent Compression, Documentation Hygiene) are cross-cutting enhancements that sharpen existing mechanics.

---

## 2. Artifacts to Create

### 2.1 Canonical Documentation — `docs/canonical/`

The 12 Partial Coverage patterns each need a canonical doc providing authoritative definition, contract, and integration guidance. The filename, pattern, and expected key sections follow.

| File | Pattern | Key Sections |
|---|---|---|
| `grill-me-alignment-interview.md` | 2. Grill-Me Alignment Interview | One-question-at-a-time protocol, recommended-answer generation, deferral register, decision ledger, exit criteria |
| `shared-design-concept-handoff.md` | 3. Shared Design Concept Handoff | Handoff contract fields (assumptions, decisions, deferrals, trust boundary), connection from Grill-Me to PRD, reviewer checklist |
| `destination-prd.md` | 4. Destination PRD | Navigational PRD template, scope/exclusion boundaries, issue-generation source contract, staleness policy, relationship to `doc-coauthoring` |
| `human-afk-task-routing-gate.md` | 5. Human/AFK Task Routing Gate | Classification matrix (ambiguity, architecture, QA, product judgment), AFK-ready criteria, human-in-loop escalations, blocker taxonomy |
| `vertical-slice-issue-generation.md` | 6. Vertical-Slice Issue Generation | Behavior-path decomposition, cross-layer slicing rules, dependency graph, acceptance criteria per slice, relationship to `refine-issue` |
| `agent-kanban.md` | 7. Agent Kanban | Board columns (Ready, Active, Review, Done, Blocked), AFK/human labels, ownership semantics, QA intake lane, concurrency-control contract |
| `ralph-afk-implementation-loop.md` | 8. Ralph/AFK Implementation Loop | Loop phases (claim → explore → implement → verify → report → decide), continue-or-stop policy, ready-issue loader, status reporting |
| `sandboxed-parallel-agents.md` | 11. Sandboxed Parallel Agents | Worktree/container isolation contract, branch-per-agent policy, merge-conflict resolution, integration-validation gates |
| `sub-agent-exploration-compression.md` | 12. Sub-Agent Exploration Compression | Exploration prompt schema, condensed-findings output contract, output_ref format, mandatory main-agent verification rule |
| `architecture-as-agent-affordance-refactoring.md` | 13. Architecture-as-Agent-Affordance Refactoring | Deep module identification, public interface simplification, boundary test patterns, dependency-cluster detection, agent-cognitive-load reduction |
| `phase-scoped-documentation-hygiene.md` | 14. Phase-Scoped Documentation Hygiene | Lifecycle states (active, completed, stale, archived, removed), per-phase cleanup triggers, retrieval-hygiene policy, integration with `docs/system-of-record.md` |
| `qa-to-backlog-feedback-loop.md` | 15. QA-to-Backlog Feedback Loop | QA finding → backlog issue conversion, severity triage, regression-case creation, Kanban intake lane, blocker linking |

### 2.2 New Skills — `.opencode/skills/`

| Directory | Pattern | Purpose |
|---|---|---|
| `grill-me/` | 2. Grill-Me Alignment Interview | Interview workflow: ask one question, offer recommended answer, register decision/deferral, produce ledger output |
| `task-router/` | 5. Human/AFK Task Routing Gate | Classify backlog items as AFK-ready or human-in-loop, apply ambiguity/architecture/QA/product-judgment matrix |
| `afk-loop/` | 8. Ralph/AFK Implementation Loop | Load ready issue, execute implementation loop, verify, report status, decide continue-or-stop |
| `arch-affordance/` | 13. Architecture-as-Agent-Affordance Refactoring | Analyze dependency clusters, propose deep module boundaries, generate boundary tests, produce follow-up issues |

### 2.3 Skill Extensions — existing `.opencode/skills/`

| Skill | Patterns | Extensions |
|---|---|---|
| `doc-coauthoring` | 2, 4 | Add Grill-Me interview mode; add Destination PRD template as coauthoring artifact type |
| `orchestrator` | 5, 7, 15 | Add AFK/human classification signal; add Kanban board semantics with QA intake lane; add QA-to-backlog conversion |
| `refine-issue` | 6 | Add vertical-slice decomposition mode (behavior-path, not file-based); add cross-layer acceptance criteria |
| `issue-start` | 8, 11 | Add AFK loop entry point; add isolation-level selection (worktree vs container) |
| `issue-review` | 9, 10, 15 | Add QA finding → backlog issue conversion; reference fresh-context review as existing gate |

### 2.4 Curriculum Integration Points — `curriculum/`

These are the concrete files where pattern content should be integrated. The "Action" column describes what to add; actual edits are deferred to the implementation phases.

| Pattern | Curriculum File | Action |
|---|---|---|
| 2. Grill-Me | `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md` | Add alignment interview as pre-planning gate before Generator starts |
| 3. Shared Design Handoff | `curriculum/05-core-concepts/02-planning-execution-separation.md` | Add shared-concept handoff as the bridge between alignment and planning |
| 4. Destination PRD | `curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md` | Add Destination PRD as upstream artifact to Sprint Contracts |
| 4. Destination PRD | `curriculum/07-implementation-guides/03-harness-design-checklist.md` | Add "Is there a navigational PRD?" to pre-implementation checklist |
| 5. AFK Routing Gate | `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` | Add task routing as coordinator responsibility in multi-agent systems |
| 6. Vertical-Slice Issues | `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` | Add vertical-slice decomposition as work-isolation strategy |
| 6. Vertical-Slice Issues | `curriculum/02-nivel-2-practical-patterns/exercises/` | New exercise: decompose a PRD into vertical-slice issues |
| 7. Agent Kanban | `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` | Add Kanban as concurrency-control layer |
| 8. AFK Loop | `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md` | Add AFK loop as the repeatable execution pattern for agents |
| 11. Sandboxed Parallel | `curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination.md` | Add worktree/container isolation as coordination primitive |
| 12. Sub-Agent Compression | `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md` | Add exploration compression as token-preservation tactic |
| 13. Architecture Affordance | `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` | Add architecture-as-affordance as harness evolution strategy |
| 14. Doc Hygiene | `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Add documentation lifecycle to harness evolution playbook |
| 15. QA-to-Backlog | `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md` | Add QA finding → backlog conversion as lifecycle feedback |

### 2.5 Governance and Workflow Artifacts

| Artifact | Pattern | Action |
|---|---|---|
| `.github/ISSUE_TEMPLATE/` | 5, 6, 15 | Add AFK/human routing label to issue template; add vertical-slice acceptance criteria section; add QA-intake issue template |
| `AGENTS.md` | 12 | Add sub-agent exploration compression rule (output_ref, mandatory verification) |
| `docs/system-of-record.md` | 14 | Add PRD/plan lifecycle tracking under documentation precedence |

---

## 3. Cross-Reference Table: Patterns to Curriculum Levels

Each pattern maps to one or more curriculum levels based on its conceptual complexity and operational role.

| # | Pattern | Level 1 Fundamentals | Level 2 Practical | Level 3 Advanced | Level 4 KODA | Core Concepts | Implementation Guides |
|---|---|---|---|---|---|---|---|
| 1 | Smart-Zone Context Mgmt | Taught as context-window limits (`01-why-agents-lose-plot.md`) | — | Governed by phase-gated monitor | KODA session budget policy | Core Concept 1: Context Management | `03-harness-design-checklist.md` |
| 2 | Grill-Me Alignment | — | Pre-planning gate before Generator | — | Applied in product-discovery sessions | Core Concept 2: Planning/Execution | `03-harness-design-checklist.md` |
| 3 | Shared Design Handoff | — | — | Bridge between planning and review | Applied in KODA feature handoffs | Core Concept 2: Planning/Execution | `03-harness-design-checklist.md` |
| 4 | Destination PRD | — | Upstream of Sprint Contracts (`02-sprint-contracts.md`) | — | Applied in KODA feature planning | Core Concept 2: Planning/Execution | `03-harness-design-checklist.md` |
| 5 | AFK Routing Gate | — | First classification exercise (`01-generator-evaluator-pattern.md`) | Coordinator responsibility (`01-multi-agent-systems.md`) | KODA feature triage | Core Concept 7: Multi-Agent Coord | `03-harness-design-checklist.md` |
| 6 | Vertical-Slice Issues | — | Exercise: decompose PRD into slices | Work-isolation strategy (`01-multi-agent-systems.md`) | KODA feature decomposition | Core Concept 7: Multi-Agent Coord | `03-harness-design-checklist.md` |
| 7 | Agent Kanban | — | — | Concurrency-control layer (`01-multi-agent-systems.md`) | KODA board operations | Core Concept 7: Multi-Agent Coord | `06-harness-evolution-playbook.md` |
| 8 | AFK Loop | — | — | Repeatable execution pattern (`01-multi-agent-systems.md`) | KODA autonomous operations | Core Concept 7: Multi-Agent Coord | `06-harness-evolution-playbook.md` |
| 9 | Feedback-Loop-Gated Impl | — | Taught via Sprint Contracts + Rubrics | Plan-Execute-Verify gate | KODA acceptance gates | Core Concepts 3, 4, 8 | `06-harness-evolution-playbook.md` |
| 10 | Fresh-Context Review | — | Generator/Evaluator separation (`01-generator-evaluator-pattern.md`) | `split-brain-planning-review.md` | KODA review workflow | Core Concept 3: Gen/Eval | `06-harness-evolution-playbook.md` |
| 11 | Sandboxed Parallel Agents | — | — | Coordination primitive (`03-file-based-coordination.md`) | KODA parallel feature work | Core Concept 7: Multi-Agent Coord | `06-harness-evolution-playbook.md` |
| 12 | Sub-Agent Compression | Token-preservation tactic (`02-token-budgeting.md`) | Exploration workflow | — | KODA codebase exploration | Core Concept 1: Context Management | `05-trace-analysis-guide.md` |
| 13 | Architecture Affordance | — | — | Harness evolution strategy (`05-harness-evolution.md`) | KODA refactoring governance | Core Concept 6: Harness Evolution | `06-harness-evolution-playbook.md` |
| 14 | Doc Hygiene | — | — | Lifecycle governance | KODA PRD/plan lifecycle | Core Concept 6: Harness Evolution | `06-harness-evolution-playbook.md` |
| 15 | QA-to-Backlog Loop | — | — | Feedback integration | KODA QA workflow (`02-customer-journey-flows.md`) | Core Concept 7: Multi-Agent Coord | `06-harness-evolution-playbook.md` |

**Mapping rationale:** Patterns 1-4 (context, alignment, design, PRD) are upstream planning concerns that feed into Level 2's planning/execution separation and Level 4's practical application. Patterns 5-8 (routing, slicing, Kanban, loop) form the multi-agent coordination spine taught in Level 3. Patterns 9-10 (feedback-gated, fresh review) are already operationalized in Level 2's Generator/Evaluator and Sprint Contract modules. Patterns 11-15 (sandbox, compression, architecture, hygiene, QA feedback) are cross-cutting concerns that enhance Level 3 architecture and Level 4 operations.

---

## 4. Gap Analysis

### 4.1 What Each Partial Coverage Pattern Is Still Missing

For each of the 12 Partial Coverage patterns, this section records what exists today and what implementation must add.

| # | Pattern | What Exists | What Is Still Missing |
|---|---|---|---|
| 2 | Grill-Me Alignment Interview | `doc-coauthoring` has context questions and split-brain review separates engineering/product judgment. | One-question-at-a-time interview protocol, recommended-answer generation, deferral register, decision ledger. No operational skill exists. |
| 3 | Shared Design Concept Handoff | `doc-coauthoring` collects meta-context; `issue-start` creates execution briefs; `split-brain-planning-review` reconciles reviewers. | A formal handoff contract declaring the alignment conversation as the primary asset. No artifact that connects Grill-Me output to PRD input with trust-boundary fields. |
| 4 | Destination PRD | `doc-coauthoring` triggers for PRDs; `writing-plans` and `issue-start` define headers with goals and scope. | A navigational PRD template with explicit validity-by-phase, staleness policy, and relationship to issue generation. PRDs currently treated as general docs, not as ephemeral navigation artifacts. |
| 5 | Human/AFK Task Routing Gate | `orchestrator` suggests next task, skips blocked/agent:working; `issue-start` prevents work theft; `split-brain-planning-review` reserves extra review for high-impact work. | An explicit classification matrix (ambiguity, architecture, QA, product judgment). No formal gate that labels tasks AFK-ready vs human-in-loop before they enter the ready queue. |
| 6 | Vertical-Slice Issue Generation | `refine-issue` decomposes by file/pair with dependencies, acceptance criteria, and verification gates; `issue-workflow` creates sub-issues with BLOCKED BY. | Behavior-path decomposition across layers (DB → API → UI → test). Current decomposition is file-oriented, not behavior-observable-path oriented. |
| 7 | Agent Kanban | `orchestrator` has dashboard with ready/active/blocked states, blocker handling, and next-issue suggestion. `curriculum-completion-strategy.md` defines a GitHub Project Kanban. | Unified contract with AFK/human labels, QA intake lane, ready queue semantics, and ownership as concurrency control. Dashboard exists but lacks canonical board semantics. |
| 8 | Ralph/AFK Implementation Loop | `issue-start` claims, creates worktree, reads context, writes brief; `issue-review` validates gates, stops on failure; `issue-finish` merges, cleans up, releases agent:working. `GLOSSARY.md` records Ralph Loop as replaced by generator/evaluator. | A continue-or-stop policy for chaining ready issues. No operational skill that loads next ready issue, executes, verifies, reports status, and decides whether to keep going. |
| 11 | Sandboxed Parallel Agents | `AGENTS.md` recommends worktrees; `issue-start` creates isolated worktrees from origin/main; `orchestrator` coordinates parallel sessions; `issue-finish` verifies merge readiness. | Container/VM-level isolation policy. Formal conflict-resolution and integration-validation contract for parallel branches beyond PR/merge flow. |
| 12 | Sub-Agent Exploration Compression | `refine-issue` uses Explore agent; `analyze-and-improve` delegates phases to sub-agents; `stable-harness-prompt` allows tool/trace bulk delegation; `addressable-memory-catalog` supports sub-agent output_ref. | A canonical contract with exploration prompt schema, condensed-findings output format, output_ref mechanics, and mandatory main-agent verification rule. |
| 13 | Architecture-as-Agent-Affordance Refactoring | `writing-plans` maps files, boundaries, interfaces; `split-brain-planning-review` evaluates scope, dependencies, tests, risk; `domain-embedded-workflow-automation-wedge` separates deterministic integration from model judgment. | A canonical refactoring framework for dependency clusters, deep module boundaries, simple public interfaces, and boundary tests. No skill or workflow exists for architecture-as-affordance analysis. |
| 14 | Phase-Scoped Documentation Hygiene | `system-of-record.md` defines documentation precedence; `AGENTS.md` enforces Obsidian frontmatter and relates-to; `measured-harness-evolution-lifecycle.md` defines REMOVE with archive/ADR; `epistemic-memory-graph.md` includes epistemic_status and stale labels. | A lifecycle policy specifically for PRDs, plans, and issues: active → completed → stale → archived/removed with explicit status labels. The existing lifecycle applies to harness components, not to planning artifacts. |
| 15 | QA-to-Backlog Feedback Loop | `production-failure-regression-flywheel.md` converts production failures to regression evals; `closed-loop-agent-operating-system.md` includes feedback writeback; `issue-workflow` updates acceptance criteria; `orchestrator` handles blockers. | A formal QA-finding-to-backlog-issue conversion with severity triage, regression-case linking, and Kanban intake lane. QA findings currently handled as terminal events, not as backlog inputs. |

### 4.2 Better Implementation and Already Exists Patterns

| # | Pattern | Treatment |
|---|---|---|
| 1 | Smart-Zone Context Management | Do not create new artifacts. The repo's `phase-gated-token-health-monitor.md`, `hybrid-context-stack.md`, `budget-aware-session-handoff.md`, and `stable-harness-prompt.md` already exceed the extracted pattern in maturity. Add cross-references when editing curriculum context-management modules. |
| 9 | Feedback-Loop-Gated Implementation | Do not create new artifacts. `plan-execute-verify.md`, `pr-gated-eval-enforcement.md`, `AGENTS.md` rules 4 and 7, and the `issue-review` validation gates already cover the pattern. Reference as supporting evidence in curriculum. |
| 10 | Fresh-Context Review | Do not create new artifacts. `generator-evaluator.md`, `issue-review` skill (compact, diff collection, second-agent review, stop-before-merge), and `split-brain-planning-review.md` already implement the builder/evaluator separation. Reference in curriculum review modules. |

### 4.3 Cross-Cutting Gaps Not Tied to a Single Pattern

| Gap | Affected Patterns | Notes |
|---|---|---|
| No unified Agent Lifecycle canonical doc | 5, 6, 7, 8, 11 | `agent-lifecycle.md` is listed as pending in `docs/system-of-record.md:46`. The AFK routing gate, vertical-slice generation, Kanban, AFK loop, and sandboxed agents all feed into this lifecycle. Creating the canonical docs for individual patterns should inform (and be informed by) the lifecycle doc. |
| No formal ADRs recorded | 5, 8, 11, 13 | `docs/decisions/` is empty. Candidates from this roadmap: AFK-vs-human routing policy, autonomous loop continuation policy, worktree-vs-container isolation, and architecture-as-affordance refactoring criteria. |
| No curriculum-model canonical doc | 2, 3, 4, 6 | `curriculum-model.md` is pending in `docs/system-of-record.md:73`. The Grill-Me, shared design, PRD, and vertical-slice patterns all contribute new artifact types (alignment ledgers, handoff contracts, navigational PRDs, behavior slices) that need a place in the curriculum taxonomy. |
| No crossroad-change-policy doc | 13, 14 | Architecture refactoring and documentation hygiene both touch files with high blast radius. The crossroad-change-policy referenced in `.github/PULL_REQUEST_TEMPLATE.md` would govern when these patterns trigger mandatory review. |

---

## 5. Phase-Gated Dependency Order

The 12 Partial Coverage patterns form a pipeline from upstream alignment through downstream feedback. Patterns in earlier phases are prerequisites for patterns in later phases. Cross-cutting patterns (marked with `↔`) can start in parallel with any phase but deliver maximum value when the dependencies they enhance are already in place.

### Phase Dependency Graph

```
Phase 0: Cross-Reference Only (no new artifacts)
  ├── 1. Smart-Zone Context Management
  ├── 9. Feedback-Loop-Gated Implementation
  └── 10. Fresh-Context Review

Phase 1: Alignment Layer ───────────────────────────────────── [P0: blocks all downstream]
  ├── 2. Grill-Me Alignment Interview ◄── prerequisite for 3, 4
  └── 3. Shared Design Concept Handoff  ◄── prerequisite for 4

Phase 2: Planning Layer ────────────────────────────────────── [P1: depends on Phase 1]
  ├── 4. Destination PRD                  ◄── prerequisite for 5, 6
  └── 5. Human/AFK Task Routing Gate      ◄── prerequisite for 7, 8

Phase 3: Decomposition Layer ───────────────────────────────── [P1: depends on Phase 2]
  └── 6. Vertical-Slice Issue Generation  ◄── prerequisite for 7, 8

Phase 4: Execution Layer ───────────────────────────────────── [P2: depends on Phase 3]
  ├── 7. Agent Kanban                     ◄── prerequisite for 8, 15
  ├── 8. Ralph/AFK Implementation Loop    ◄── prerequisite for 15
  └── 11. Sandboxed Parallel Agents       ◄── enhances 7, 8

Phase 5: Feedback Layer ────────────────────────────────────── [P2: depends on Phase 4]
  └── 15. QA-to-Backlog Feedback Loop     ◄── closes the loop with 7

Cross-Cutting (↔): ─────────────────────────────────────────── [P2-P3: parallel-able]
  ├── 13. Architecture-as-Agent-Affordance Refactoring  ↔ enhances all phases
  ├── 14. Phase-Scoped Documentation Hygiene             ↔ maintains all phases
  └── 12. Sub-Agent Exploration Compression              ↔ enhances execution (Phase 4+)
```

### Phase-by-Phase Blocking Rationale

**Phase 1 (Alignment):** Grill-Me produces the decision ledger and alignment state. Shared Design Concept Handoff formalizes that state as a transferable contract. Without this, downstream PRDs have no validated source of assumptions, and routing gates cannot assess ambiguity against declared decisions.

**Phase 2 (Planning):** Destination PRD converts the shared design concept into navigational scope. The Human/AFK Routing Gate classifies each backlog item using the PRD's scope and ambiguity boundaries. Without a PRD, the routing gate has nothing to classify against; without a routing gate, PRD items flow into the queue without AFK/human labeling.

**Phase 3 (Decomposition):** Vertical-Slice Issue Generation takes AFK-ready PRD items and decomposes them into behavior-path issues across layers. This is the bridge between planning (Phase 2) and execution (Phase 4). Without vertical slices, the Kanban receives file-based issues that lack integration feedback and create false parallelism.

**Phase 4 (Execution):** Agent Kanban provides the board semantics that the AFK loop pulls from. The AFK loop implements the repeatable execution cycle. Sandboxed Parallel Agents provides the isolation that makes parallel Kanban work safe. Kanban defines the queue; AFK loop defines the pull-execute-report cycle; sandboxing defines the safety boundary.

**Phase 5 (Feedback):** QA-to-Backlog Feedback Loop converts review/QA findings into new Kanban items with severity and regression links. This closes the loop from execution back to planning. It depends on Kanban (Phase 4) for intake lane semantics and on the AFK loop for the QA findings that feed it.

**Cross-Cutting:** Architecture-as-Agent-Affordance Refactoring improves the codebase structure that all phases navigate; it can start after Phase 1 when the alignment reveals architectural pain points. Phase-Scoped Documentation Hygiene maintains the freshness of all artifacts (PRDs, plans, issues) created by earlier phases; it can start in parallel but is most valuable after Phase 2 when PRDs exist. Sub-Agent Exploration Compression enhances the AFK loop's implementation phase; it can be created independently since the exploration sub-agent pattern already exists in `refine-issue` and `analyze-and-improve`.

### Recommended Implementation Sequence

| Step | Patterns | Artifacts | Blocks |
|---|---|---|---|
| 1 | 2, 3 | `grill-me-alignment-interview.md`, `shared-design-concept-handoff.md`, `grill-me/` skill | 4, 5, 6, 7, 8, 15 |
| 2 | 4 | `destination-prd.md`, PRD template in `curriculum/08-tools-templates/` | 5, 6 |
| 3 | 5 | `human-afk-task-routing-gate.md`, `task-router/` skill, `orchestrator` extension | 7, 8 |
| 4 | 6 | `vertical-slice-issue-generation.md`, `refine-issue` extension, curriculum exercise | 7, 8 |
| 5 | 7 | `agent-kanban.md`, `orchestrator` kanban extension | 8, 15 |
| 6 | 8, 11 | `ralph-afk-implementation-loop.md`, `sandboxed-parallel-agents.md`, `afk-loop/` skill, `issue-start` extension | 15 |
| 7 | 15 | `qa-to-backlog-feedback-loop.md`, `orchestrator` QA lane extension | — |
| 8 | 13 | `architecture-as-agent-affordance-refactoring.md`, `arch-affordance/` skill | — |
| 9 | 12 | `sub-agent-exploration-compression.md`, `AGENTS.md` update | — |
| 10 | 14 | `phase-scoped-documentation-hygiene.md`, `system-of-record.md` update | — |

Steps 1-7 follow the strict dependency chain. Steps 8-10 are independent of each other and can be parallelized once the dependency chain is clear.

---

## 6. Impact by Category

| Category | Artifacts Created | Highest-Value Gap Addressed |
|---|---|---|
| **New Canonical Docs** | 12 pattern docs in `docs/canonical/` | Formal contracts for alignment, planning, decomposition, execution, and feedback layers |
| **New Skills** | 4 operational skills (grill-me, task-router, afk-loop, arch-affordance) | Autonomous execution of alignment interviews, task classification, implementation loops, and architecture analysis |
| **Skill Extensions** | 5 existing skills extended (doc-coauthoring, orchestrator, refine-issue, issue-start, issue-review) | AFK/human labels, vertical-slice decomposition, Kanban semantics, QA intake lane |
| **Curriculum Integration** | 14 file edits across Levels 1-4, Core Concepts, Implementation Guides, and Exercises | Vertical-slice issue decomposition exercise; alignment interview as pre-planning gate; AFK loop as repeatable execution pattern |
| **Governance Artifacts** | Issue template updates, AGENTS.md rule, system-of-record lifecycle tracking | AFK/human routing label, sub-agent output contract, PRD/plan staleness policy |

---

## 7. Precedence Alignment

Per `docs/system-of-record.md`:

- **Level 2 (canonical):** Once created, the 12 `docs/canonical/` pattern docs take precedence over this analysis roadmap and over README summaries. They become authoritative sources for the patterns they define.
- **Level 4 (analysis):** This roadmap and the classification doc remain at analysis level — they inform integration decisions but do not override canonical docs.
- **Level 1 (ADRs):** `docs/decisions/` remains empty. The strongest ADR candidates from this work are: (a) AFK-vs-human task routing policy, (b) autonomous loop continuation policy, and (c) architecture-as-affordance refactoring criteria.
- **Pending canonical docs:** `agent-lifecycle.md`, `curriculum-model.md`, and `crossroad-change-policy.md` all intersect with this roadmap's patterns. Ideally they are created before or alongside the Phase 4-5 patterns.

---

## 8. References

- `docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification.md` — classification and evidence for all 15 patterns
- `docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns.md` — 15 extracted pattern definitions with 6 fields each
- `docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-mental-model.md` — repository mental model, curriculum structure, and existing gaps
- `docs/system-of-record.md` — documentation precedence and curriculum source map
- `docs/canonical/closed-loop-agent-operating-system.md` — existing OS model with feedback writeback
- `docs/canonical/split-brain-planning-review.md` — separate engineering/product review rubrics
- `docs/canonical/plan-execute-verify.md` — three-phase execution contract
- `docs/canonical/generator-evaluator.md` — builder/evaluator separation
- `docs/canonical/budget-aware-session-handoff.md` — context-reset handoff contract
- `docs/canonical/pr-gated-eval-enforcement.md` — eval evidence at merge gate

---

*Created: 2026-06-07 | Last updated: 2026-06-11 | From: WFAC Pattern Classification | Precedence: analysis*
