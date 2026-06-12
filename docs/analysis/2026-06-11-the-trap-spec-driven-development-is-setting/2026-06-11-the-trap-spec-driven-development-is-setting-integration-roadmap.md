---
title: "Integration Roadmap: The Trap SDD Patterns → long-running-agents"
type: analysis
date: 2026-06-11
domain: the-trap-spec-driven-development-is-setting
aliases: ["roadmap SDD trap", "plano integracao SDD", "integracao trap SDD", "SDD trap roadmap"]
tags: ["analise", "spec-driven-development", "decision-discipline", "governanca", "harness-engineering", "roadmap"]
relates-to: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]]", "[[docs/canonical/accidental-brake-replacement|Accidental Brake Replacement]]", "[[docs/system-of-record|System of Record]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]"]
---

# Integration Roadmap: The Trap SDD Patterns → long-running-agents

**Date:** 2026-06-11
**Type:** Analysis
**Precedence:** Level 4 (`docs/system-of-record.md:10`)
**Source:** `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification.md`

---

## Objective

Map each of the 10 patterns extracted from "The Trap Spec-Driven Development Is Setting" to concrete integration points in the long-running-agents repo: canonical documentation, skills, curriculum exercises, and future roadmap items. The classification identified 4 Missing, 4 Partial Coverage, and 2 Better Implementation patterns. This roadmap prioritizes the 8 gaps (Missing + Partial Coverage) by impact, effort, and integration surface.

---

## 1. Summary Matrix

| # | Pattern | Classification | Impact | Effort | Priority | Integration Surface |
|---|---|---|---|---|---|---|
| 2 | Manual Brake Question Gate | **Missing** | High | Low | **P0** | Canonical doc, skill, Level 4 exercise |
| 6 | Deferred Ledger for Agentic Work | **Missing** | High | Medium | **P0** | Canonical doc, skill, Level 4 exercise |
| 1 | Value-Gated Agent Control Loop | Partial Coverage | High | Medium | **P1** | Canonical doc, control-plane integration |
| 10 | Carry Debt Sunset Gate | Partial Coverage | High | Medium | **P1** | Canonical doc, harness lifecycle extension |
| 5 | Owner-of-No Role | **Missing** | Medium | Low | **P1** | Canonical doc, skill, curriculum reframe |
| 4 | Continue Decision Checkpoint | Partial Coverage | Medium | Medium | **P2** | Curriculum reframe, loop-control extension |
| 9 | Judgment Exercise Cadence | Partial Coverage | Medium | Medium | **P2** | Curriculum exercise, ritual integration |
| 8 | Accidental Brake Replacement | **Missing** | Low | Medium | **P3** | Canonical doc (enterprise curriculum) |
| 3 | Intent-First Spec Loop | Better Impl. | — | — | Done | No action needed; repo exceeds pattern |
| 7 | Silent Degradation Sentinel Evals | Better Impl. | — | — | Done | No action needed; 15+ eval docs cover this |

**Key insight:** The 4 Missing patterns (Manual Brake, Deferred Ledger, Owner-of-No, Accidental Brake Replacement) all concern value decision-making, organizational risk accounting, and governance -- areas the repo's engineering-focused architecture did not address. The 4 Partial Coverage patterns each have infrastructure in place but lack the specific decision vocabulary and placement that the source analysis described.

---

## 2. Artifacts Created (Phase 4: Improvement Generation)

### 2.1 Canonical Docs — `docs/canonical/`

| File | Pattern | Classification | Status |
|---|---|---|---|
| `manual-brake-question-gate.md` | #2 Manual Brake Question Gate | New Pattern | Done |
| `deferred-ledger-agentic-work.md` | #6 Deferred Ledger for Agentic Work | New Pattern | Done |
| `owner-of-no-role-design.md` | #5 Owner-of-No Role | New Pattern | Done |
| `value-gated-agent-control-loop.md` | #1 Value-Gated Agent Control Loop | Gap Fill | Done |
| `carry-debt-sunset-gate.md` | #10 Carry Debt Sunset Gate | Gap Fill | Done |
| `accidental-brake-replacement.md` | #8 Accidental Brake Replacement | New Pattern | Done |

**Total:** 6 canonical docs (4 new patterns, 2 gap fills)

### 2.2 Skills — `.opencode/skills/`

| Directory | Pattern | Workflow | Status |
|---|---|---|---|
| `manual-brake-question-gate/` | #2 Manual Brake Question Gate | decision | Done |
| `deferred-ledger-agentic-work/` | #6 Deferred Ledger for Agentic Work | governance | Done |
| `owner-of-no-role/` | #5 Owner-of-No Role | governance | Done |

**Total:** 3 skills (2 governance, 1 decision)

### 2.3 Exercises — `curriculum/04-nivel-4-koda-specific/real-world-exercises/`

| File | Pattern | Difficulty | Duration | Status |
|---|---|---|---|---|
| `exercise-05-manual-brake-question-gate.md` | #2 Manual Brake Question Gate | ⭐⭐⭐ | 60-90 min | Done |
| `exercise-06-deferred-ledger-agentic-work.md` | #6 Deferred Ledger for Agentic Work | ⭐⭐⭐⭐ | 90-120 min | Done |

**Total:** 2 Level 4 exercises (decision discipline + risk accounting)

### 2.4 Analysis — `docs/analysis/`

| File | Scope | Status |
|---|---|---|
| `integration-roadmap.md` (this file) | Cross-cutting roadmap with gap analysis | Done |

---

## 3. Cross-Reference: Patterns → Curriculum Levels

Each pattern is mapped to the curriculum level where its concepts are most naturally taught. Level assignments consider the curriculum's progression: Level 1 (fundamentals), Level 2 (practical patterns), Level 3 (advanced architecture), Level 4 (KODA application).

| # | Pattern | Level | Module/Exercise | Rationale |
|---|---|---|---|---|
| 1 | Value-Gated Agent Control Loop | Level 3 | 05-harness-evolution.md | Concerned with control-loop architecture; extends the harness evolution module |
| 2 | Manual Brake Question Gate | Level 4 | exercise-05-manual-brake-question-gate.md | Decision discipline applied to real KODA features; concrete scenarios |
| 3 | Intent-First Spec Loop | Level 3 | 01-multi-agent-systems.md (existing) | Already covered via Grill-Me → Shared Concept → Plan-Execute-Verify pipeline |
| 4 | Continue Decision Checkpoint | Level 3 | 05-harness-evolution.md (future reframe) | Loop intervention point; pairs with Owned Agent Control Loop |
| 5 | Owner-of-No Role | Level 3 | 01-multi-agent-systems.md (future reframe) | Agent role design; extends Core Concept 7 (Multi-Agent Coordination) |
| 6 | Deferred Ledger for Agentic Work | Level 4 | exercise-06-deferred-ledger-agentic-work.md | Financial modeling applied to KODA; risk accounting for production systems |
| 7 | Silent Degradation Sentinel Evals | Level 3 | 04-server-side-compaction.md + eval ecosystem | Already covered by 15+ eval canonical docs; no new material needed |
| 8 | Accidental Brake Replacement | Level 4 | Future case study (enterprise track) | Relevant to enterprise adoption; low priority for current curriculum |
| 9 | Judgment Exercise Cadence | Level 3 | GC Day Meta-Loop reframe | Existing weekly cadence; add judgment calibration layer |
| 10 | Carry Debt Sunset Gate | Level 3 | 05-harness-evolution.md (future reframe) | Extends Measured Harness Evolution Lifecycle to general artifacts |

### Curriculum Level Descriptions (from `[[curriculum/README]]`)

**Level 1 (Fundamentals, 3-4h):** Why agents fail. Context windows, token budgeting, basic harness patterns.
**Level 2 (Practical Patterns, 6-8h):** Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading.
**Level 3 (Advanced Architecture, 8-10h):** Multi-agent systems, state persistence, file-based coordination, harness evolution.
**Level 4 (KODA-Specific, continuous):** KODA architecture, customer journeys, feature design, real-world exercises, case studies.

### Exercise Progression

```
Level 4 Real-World Exercises:
  exercise-01: Generator/Evaluator feature implementation          (pattern: generator-evaluator)
  exercise-02: Customer journey pipeline with 7 agents             (pattern: multi-agent coordination)
  exercise-05: Manual Brake Question Gate — value gate decisions   (pattern: manual-brake)      ← NEW
  exercise-06: Deferred Ledger — debt classification & mitigation  (pattern: deferred-ledger)    ← NEW
```

Exercises 03 and 04 are reserved for future Level 4 patterns (Continue Decision Checkpoint, Judgment Exercise Cadence).

---

## 4. Gap Analysis

### 4.1 Patterns Fully Integrated (No Remaining Gaps)

| # | Pattern | Why Complete |
|---|---|---|
| 3 | Intent-First Spec Loop | Repo exceeds pattern maturity. Grill-Me → Shared Concept → PRD/Issue → Plan → Execute → Verify pipeline is fully documented. |
| 7 | Silent Degradation Sentinel Evals | Repo exceeds pattern maturity. 15+ canonical docs cover eval ecosystem: spot-check sets, production-grounded sampling, correlation tracking, degradation ladder, tier stratification, PR gates, regression flywheel. |

### 4.2 Patterns with Canonical Docs + Skills + Exercises (Integration Complete)

| # | Pattern | Docs | Skill | Exercise | Remaining |
|---|---|---|---|---|---|
| 2 | Manual Brake Question Gate | ✓ | ✓ | ✓ | None. Full integration. |
| 6 | Deferred Ledger for Agentic Work | ✓ | ✓ | ✓ | None. Full integration. |

### 4.3 Patterns with Canonical Docs + Skills Only (Missing Curriculum Integration)

| # | Pattern | Docs | Skill | Exercise | Gap |
|---|---|---|---|---|---|
| 5 | Owner-of-No Role | ✓ | ✓ | — | No Level 3/4 exercise. Could be added to multi-agent-systems module or as standalone exercise. |
| 1 | Value-Gated Agent Control Loop | ✓ | — | — | No skill and no exercise. The canonical doc describes the loop modification but no operational skill exists to execute the value gate. |
| 10 | Carry Debt Sunset Gate | ✓ | — | — | No skill and no exercise. The canonical doc extends the harness lifecycle but no operational skill exists to run artifact inventory and retirement reviews. |
| 8 | Accidental Brake Replacement | ✓ | — | — | No skill and no exercise. Low priority; pattern is enterprise-context only. |

### 4.4 Patterns Without Any New Artifacts (Still Partial Coverage)

| # | Pattern | Classification | What Exists | Gap |
|---|---|---|---|---|
| 4 | Continue Decision Checkpoint | Partial Coverage | Loop controls (break, terminate, human approval gate), harness lifecycle (BUILD/STABILIZE/SIMPLIFY/REMOVE), GC Day weekly review | Missing the experiment-boundary decision vocabulary (Continue/pivot/stop/archive) as an explicit checkpoint. No canonical doc, skill, or exercise created. |
| 9 | Judgment Exercise Cadence | Partial Coverage | GC Day weekly cadence, Split-Brain Planning Review, Grill-Me Alignment Interview, harness lifecycle quarterly cycle | Missing the specific purpose of exercising human value judgment. No canonical doc, skill, or exercise created. |

### 4.5 Artifact Inventory Summary

| Artifact Type | Created | Remaining Gaps |
|---|---|---|
| Canonical Docs | 6 | 0 direct gaps; 2 patterns (#4, #9) need canonical docs |
| Skills | 3 | 3 gaps: Value-Gated ACL (skill), Carry Debt Sunset (skill), Continue Checkpoint (skill) |
| Exercises (Level 4) | 2 | 4 gaps: Owner-of-No (#5), Value-Gated ACL (#1), Continue Checkpoint (#4), Judgment Cadence (#9) |
| Curriculum Modules | 0 new | 3 modules could be reframed: harness-evolution (Level 3), multi-agent-systems (Level 3), GC Day (Level 3) |
| System-of-Record Updates | In progress | `docs/system-of-record.md` needs 6 new canonical doc entries + 3 new skill entries |

---

## 5. Detailed Integration Plan

### P0: Manual Brake Question Gate (Missing → Fully Integrated)

**Why P0:** Only pattern classified as Missing with High impact AND Low effort. The three diagnostic questions are lightweight, immediately usable, and address the core gap the source analysis names: "nada no workflow força a pergunta de valor antes da construção."

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Authoritative pattern with flow, questions, and integration points | `docs/canonical/manual-brake-question-gate.md` | Done |
| Operational skill | Skill that applies the three questions and produces build/experiment/defer/stop classification | `.opencode/skills/manual-brake-question-gate/SKILL.md` | Done |
| Level 4 exercise | Scenario-based exercise applying brake questions to 7 real KODA feature proposals | `curriculum/.../exercise-05-manual-brake-question-gate.md` | Done |
| Grill-Me integration | Incorporate brake questions into alignment interview flow | Future: `docs/canonical/grill-me-alignment-interview.md` update | Future |
| Level 3 reframe | Add "Value Gating" sidebar to harness-evolution module | Future: `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` | Future |

### P0: Deferred Ledger for Agentic Work (Missing → Fully Integrated)

**Why P0:** Missing with High impact. The three debt categories (skill, dependence, carry) are a novel risk framework not present in the repo's existing cost tracking. The repo has instrumentation pieces (token ledger, burn rate, health monitor) that a debt ledger would consume, adding a strategic risk layer on top of operational cost tracking.

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Authoritative pattern with ledger schema, exposure view, and mitigation decisions | `docs/canonical/deferred-ledger-agentic-work.md` | Done |
| Operational skill | Skill that classifies debt into three categories and produces exposure view | `.opencode/skills/deferred-ledger-agentic-work/SKILL.md` | Done |
| Level 4 exercise | Audit exercise: classify KODA's 14 features into skill/dependence/carry debt with exposure calculation | `curriculum/.../exercise-06-deferred-ledger-agentic-work.md` | Done |
| Token budget integration | Feed token ledger data into deferred ledger for carry cost estimation | Future: connect `explicit-token-budget-ledger.md` with debt ledger | Future |
| GC Day integration | Add debt ledger review as a quarterly section of GC Day | Future: `docs/canonical/garbage-collection-day-meta-loop.md` update | Future |

### P1: Value-Gated Agent Control Loop (Partial Coverage → Gap Fill)

**Why P1:** High impact, Medium effort. The repo has pre-execution infrastructure (alignment interview, routing gate, split-brain review) but lacks the build/experiment/defer/stop decision vocabulary wired into the control loop. The canonical doc formalizes this; the skill and exercise are still needed.

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Formalize the value gate as a control-loop component | `docs/canonical/value-gated-agent-control-loop.md` | Done |
| Operational skill | Skill that executes the value gate before agent dispatch | `.opencode/skills/value-gated-agent-control-loop/SKILL.md` | **Not created** |
| Level 4 exercise | Exercise wiring value gate into agent dispatch flow | `curriculum/.../exercise-07-value-gated-agent-control-loop.md` | **Not created** |
| Control-plane integration | Add value gate as an explicit gate in the control plane contract | Future: `docs/canonical/application-owned-agent-control-plane.md` update | Future |

### P1: Carry Debt Sunset Gate (Partial Coverage → Gap Fill)

**Why P1:** High impact, Medium effort. The repo has mature component lifecycle (BUILD/STABILIZE/SIMPLIFY/REMOVE) but scoped to harness components only. Extending the pattern to general agent-created artifacts addresses a core gap: "software que foi barato de criar se torna inventario permanente sem decisao explicita de sunset."

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Extend harness lifecycle to general agent-created artifacts with keep/retire/archive/promote vocabulary | `docs/canonical/carry-debt-sunset-gate.md` | Done |
| Operational skill | Skill that audits artifact inventory and produces retirement decisions | `.opencode/skills/carry-debt-sunset-gate/SKILL.md` | **Not created** |
| Level 4 exercise | Exercise auditing agent-created artifacts and making retirement decisions | `curriculum/.../exercise-08-carry-debt-sunset-gate.md` | **Not created** |
| GC Day integration | Add artifact inventory review as a monthly GC Day section | Future | Future |

### P1: Owner-of-No Role (Missing → Canonical + Skill; Exercise Missing)

**Why P1:** Medium impact, Low effort. The concept is more organizational than technical but fills a vacuum: "nenhum agente, skill, doc canonico ou material de curriculo define um papel cujo trabalho explicito e recusar trabalho de baixo valor."

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Define the Owner-of-No role with responsibilities, criteria, and escalation paths | `docs/canonical/owner-of-no-role-design.md` | Done |
| Operational skill | Skill that activates the Owner-of-No role in governance workflows | `.opencode/skills/owner-of-no-role/SKILL.md` | Done |
| Level 4 exercise | Exercise designing refusal ownership for a KODA team | `curriculum/.../exercise-09-owner-of-no-role.md` | **Not created** |
| Level 3 reframe | Add "Refusal Roles" to multi-agent-systems module (Core Concept 7) | Future | Future |

### P2: Continue Decision Checkpoint (Partial Coverage → Curriculum Reframe)

**Why P2:** Medium impact, Medium effort. The repo has loop controls and lifecycle decisions but lacks the experiment-boundary checkpoint with Continue/pivot/stop/archive vocabulary. The source's key insight -- "the verb that creates the problem is not Build -- it's Continue" -- is not formalized anywhere.

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Formalize the continue decision checkpoint pattern | `docs/canonical/continue-decision-checkpoint.md` | **Not created** |
| Level 3 reframe | Add "Experiment Boundary Decisions" to harness-evolution module | Future | Future |
| Level 4 exercise | Exercise defining stop criteria and making continue/pivot/stop decisions | `curriculum/.../exercise-03-continue-decision-checkpoint.md` | **Not created** |

### P2: Judgment Exercise Cadence (Partial Coverage → Ritual Integration)

**Why P2:** Medium impact, Medium effort. The repo has weekly and quarterly cadences (GC Day, harness lifecycle) but they focus on harness improvement, not on exercising human value judgment. The pattern's purpose -- keeping judgment muscle active through explicit build/don't-build tradeoff discussions -- could be added as a layer on existing cadences.

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Formalize the judgment exercise cadence pattern | `docs/canonical/judgment-exercise-cadence.md` | **Not created** |
| GC Day reframe | Add "Judgment Exercise" section to GC Day: one build/don't-build tradeoff per session | Future | Future |
| Level 4 exercise | Exercise running a judgment calibration session with KODA feature proposals | `curriculum/.../exercise-04-judgment-exercise-cadence.md` | **Not created** |

### P3: Accidental Brake Replacement (Missing → Canonical Only)

**Why P3:** Low impact for the repo itself. The concept of replacing external bureaucracy with intentional harness gates is relevant to enterprise adoption contexts but the repo is a curriculum and pattern library, not an enterprise organization. The canonical doc exists for enterprise curriculum use.

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Define the accidental brake replacement pattern | `docs/canonical/accidental-brake-replacement.md` | Done |
| Enterprise case study | Case study applying the pattern to a fictional enterprise adopting agentic workflows | Future: `curriculum/.../case-study-04-accidental-brake-replacement.md` | **Not created** |

---

## 6. Impact by Category

| Category | Artifacts Created | Highest-Value Gap Addressed |
|---|---|---|
| **New Canonical Docs** | 6 docs (4 new patterns, 2 gap fills) | Value-gating vocabulary (build/experiment/defer/stop) formalized for first time |
| **New Skills** | 3 skills (2 governance, 1 decision) | Manual Brake operationalized as a pre-build gate |
| **New Exercises (Level 4)** | 2 exercises (decision discipline + risk accounting) | Hands-on practice with brake questions and debt classification on real KODA scenarios |
| **Gap Analysis** | 8 remaining gaps documented | 2 canonical docs, 4 skills, 4 exercises still needed for full coverage |
| **Curriculum Cross-Reference** | 10 patterns mapped to 4 levels | Clear path for future curriculum integration of remaining patterns |

---

## 7. Precedence Alignment

Per `docs/system-of-record.md`:

- **Level 2 (canonical):** 6 new canonical docs in `docs/canonical/`. These now take precedence over analysis docs for their covered patterns.
- **Level 3 (evidence):** No new evidence artifacts. The exercises will produce evidence when completed by learners.
- **Level 4 (analysis):** This roadmap and the classification doc remain at analysis level -- they inform but don't override canonical docs.
- **Level 6 (READMEs):** `PROGRESS.md` tracks phase completion. No README changes needed.

### System-of-Record Updates Required

The following entries need to be added to `docs/system-of-record.md` under the canonical docs section:

- `manual-brake-question-gate.md` -- Gate de tres perguntas diagnosticas de valor antes de construir
- `deferred-ledger-agentic-work.md` -- Classificacao de divida agentica em skill, dependence e carry debt
- `owner-of-no-role-design.md` -- Papel organizacional cujo trabalho e recusar trabalho de baixo valor
- `value-gated-agent-control-loop.md` -- Gate de valor integrado ao loop de controle do agente
- `carry-debt-sunset-gate.md` -- Gate de sunset para artefatos criados por agentes
- `accidental-brake-replacement.md` -- Substituicao de burocracia acidental por gates intencionais

And under the skills section:

- `.opencode/skills/manual-brake-question-gate/SKILL.md` -- Aplica as tres perguntas do Manual Brake
- `.opencode/skills/deferred-ledger-agentic-work/SKILL.md` -- Mantem o Deferred Ledger de divida agentica
- `.opencode/skills/owner-of-no-role/SKILL.md` -- Define e operacionaliza o papel de Owner-of-No

This is tracked as part of the phase-5 Integration step.

---

## 8. Future ADR Candidates

From the pattern analysis, these decisions warrant formal ADRs:

1. **Value gate placement in the agent control loop** -- Should the value gate be a pre-execution phase (before Plan-Execute-Verify) or a concurrent check at each loop iteration? Tradeoffs: pre-execution blocks trivial builds early; concurrent catches scope creep during execution.
2. **Artifact lifecycle governance** -- Should Carry Debt Sunset Gate be a manual review (quarterly) or an automated gate (every N iterations)? Tradeoffs: manual catches edge cases; automated scales without attention cost.
3. **Debt ledger vs. token budget** -- Should the Deferred Ledger replace or complement the Explicit Token Budget Ledger? Tradeoffs: replacing simplifies the cost model; complementing preserves operational vs. strategic separation.

---

## 9. References

- `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification.md` -- full classification with evidence
- `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns.md` -- 10 pattern definitions with 6 fields each
- `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md` -- source knowledge extraction
- `docs/canonical/manual-brake-question-gate.md` -- canonical pattern doc
- `docs/canonical/deferred-ledger-agentic-work.md` -- canonical pattern doc
- `docs/canonical/owner-of-no-role-design.md` -- canonical pattern doc
- `docs/canonical/value-gated-agent-control-loop.md` -- canonical pattern doc
- `docs/canonical/carry-debt-sunset-gate.md` -- canonical pattern doc
- `docs/canonical/accidental-brake-replacement.md` -- canonical pattern doc
- `curriculum/README.md` -- curriculum overview with level descriptions
- `docs/system-of-record.md` -- documentation precedence and domain map

---

*Created: 2026-06-11 | From: SDD Trap Pattern Classification | Precedence: analysis*
