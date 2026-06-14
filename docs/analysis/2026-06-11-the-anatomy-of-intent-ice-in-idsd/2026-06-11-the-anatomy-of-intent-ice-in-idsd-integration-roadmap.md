---
title: "Integration Roadmap: The Anatomy of Intent ICE in IDSD Patterns"
type: analysis
tags: ["agentes-orquestracao", "spec-driven-development", "decision-discipline", "evals", "harness-engineering", "curriculo-conteudo", "governanca"]
date: 2026-06-11
aliases: ["roadmap anatomy intent ice", "integracao anatomy intent", "ICE integration roadmap", "anatomy of intent integration plan", "mapeamento integracao ICE patterns", "integration roadmap intent ice"]
last_updated: 2026-06-14
relates-to: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-mental-model|Anatomy of Intent Mental Model]]", "[[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]]", "[[docs/canonical/goal-atomicity-split|Goal Atomicity Split]]", "[[docs/canonical/constraint-budget-gate|Constraint Budget Gate]]", "[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]", "[[docs/canonical/scenario-destination-split|Scenario Destination Split]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]", "[[curriculum/INDEX|Curriculum Index]]", "[[docs/system-of-record|System of Record]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-mental-model|Anatomy of Intent Mental Model]]", "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]", "[[docs/system-of-record|System of Record]]"]
---

# Integration Roadmap: The Anatomy of Intent ICE in IDSD Patterns

**Date:** 2026-06-11 (last updated 2026-06-14)
**Type:** Analysis
**Precedence:** Level 4 (`docs/system-of-record.md:19`)
**Source Patterns:** 9 agentic patterns from "The Anatomy of Intent — ICE in IDSD" (Kapil Viren Ahuja, 2026)
**Source Classification:** [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification.md]]
**Phase:** 4a-4c — canonical docs, skills, and exercises created for patterns classified as Missing or Partial Coverage.

---

## 1. Summary Matrix

Maps each of the 9 classified patterns to integration surfaces, prioritised by impact and implementation effort.

| # | Pattern | Classification | Impact | Effort | Priority | Integration Surface |
|---|---|---|---|---|---|---|
| 1 | ICE Ownership Boundary | Already Exists | None | None | — | No new integration needed. Covered at greater depth by [[docs/canonical/ice-craft-separation|ICE Craft Separation]], [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]], and [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]. |
| 2 | Three-Part Intent Contract | Partial Coverage | Medium | Low | P2 | [[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]] canonical doc. Missing skill and exercise. Complements [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]] as an alternative decomposition model. |
| 3 | Two-Implementations Goal Test | Missing | Medium | Low | P1 | [[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]] canonical, [[.opencode/skills/two-implementations-goal-test/SKILL|two-implementations-goal-test skill]], [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-two-implementations-goal-test|exercise (Level 2)]]. |
| 4 | Goal Atomicity Split | Missing | Medium | Low | P1 | [[docs/canonical/goal-atomicity-split|Goal Atomicity Split]] canonical, [[.opencode/skills/goal-atomicity-split/SKILL|goal-atomicity-split skill]], [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-goal-atomicity-split|exercise (Level 2)]]. |
| 5 | Constraint Budget Gate | Missing | Medium | Low | P1 | [[docs/canonical/constraint-budget-gate|Constraint Budget Gate]] canonical, [[.opencode/skills/constraint-budget-gate/SKILL|constraint-budget-gate skill]], [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-constraint-budget-gate|exercise (Level 3)]]. |
| 6 | Constraint-Failure Decision Rule | Missing | High | Low | **P0** | [[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]] canonical, [[.opencode/skills/constraint-failure-decision-rule/SKILL|constraint-failure-decision-rule skill]], [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-constraint-failure-decision-rule|exercise (Level 3)]]. Foundational heuristic that feeds into Patterns 5, 7, and 8. |
| 7 | Compartmented Evaluation Architecture | Partial Coverage | High | Medium | **P0** | [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] canonical doc. **HIGH** integration value per classification. Extends [[docs/canonical/generator-evaluator|Generator-Evaluator]] with sealed information surfaces. Missing skill and exercise. |
| 8 | Scenario Destination Split | Partial Coverage | Medium | Low | P2 | [[docs/canonical/scenario-destination-split|Scenario Destination Split]] canonical doc. Clarifies the routing rule between failure scenarios (Intent) and success scenarios (Expectations). Missing skill and exercise. |
| 9 | Harness-Owned Context Assembly | Already Exists | None | None | — | Repo exceeds pattern depth. Covered by [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]], [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]], [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]], and 6 additional canonical docs (see classification for full evidence). |

**Priority legend:**
- **P0** — High integration value; foundational mechanics that feed other patterns. Demand skill + exercise next.
- **P1** — Missing patterns now fully addressed (canonical + skill + exercise). Integration complete at this phase.
- **P2** — Partial Coverage patterns improved with canonical docs. Skill and exercise remain as future work.

**Totals:** Already Exists: 2, Partial Coverage: 3 (improved with canonicals), Missing: 4 (now filled with canonicals + skills + exercises).

---

## 2. Artifacts Created During This Session (2026-06-14, Phase 4a-4c)

All artifacts map directly to patterns from the [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]].

### 2.1 Canonical Docs (`docs/canonical/`)

7 new canonical docs created. Three for Partial Coverage patterns (formalising what was implicit), four for Missing patterns (filling the gap).

| File | Pattern # | Classification Before | Status |
|---|---|---|---|
| [[docs/canonical/compartmented-evaluation-architecture|compartmented-evaluation-architecture.md]] | 7 — Compartmented Evaluation Architecture | Partial Coverage | Formalised |
| [[docs/canonical/three-part-intent-contract|three-part-intent-contract.md]] | 2 — Three-Part Intent Contract | Partial Coverage | Formalised |
| [[docs/canonical/scenario-destination-split|scenario-destination-split.md]] | 8 — Scenario Destination Split | Partial Coverage | Formalised |
| [[docs/canonical/two-implementations-goal-test|two-implementations-goal-test.md]] | 3 — Two-Implementations Goal Test | Missing → Filled | Done |
| [[docs/canonical/goal-atomicity-split|goal-atomicity-split.md]] | 4 — Goal Atomicity Split | Missing → Filled | Done |
| [[docs/canonical/constraint-budget-gate|constraint-budget-gate.md]] | 5 — Constraint Budget Gate | Missing → Filled | Done |
| [[docs/canonical/constraint-failure-decision-rule|constraint-failure-decision-rule.md]] | 6 — Constraint-Failure Decision Rule | Missing → Filled | Done |

**Grouped by classification:**
- **Missing → Now documented:** Pattern #3 (Two-Implementations Goal Test), Pattern #4 (Goal Atomicity Split), Pattern #5 (Constraint Budget Gate), Pattern #6 (Constraint-Failure Decision Rule)
- **Partial Coverage → Now formalised:** Pattern #2 (Three-Part Intent Contract), Pattern #7 (Compartmented Evaluation Architecture), Pattern #8 (Scenario Destination Split)
- **Already Exists — no new canonical needed:** Pattern #1 (ICE Ownership Boundary), Pattern #9 (Harness-Owned Context Assembly)

### 2.2 Skills (`.opencode/skills/`)

4 new skills created. All correspond to the four Missing patterns, providing operational gating mechanics.

| Directory | Pattern # | Pattern | Status |
|---|---|---|---|
| [[.opencode/skills/two-implementations-goal-test/SKILL|two-implementations-goal-test/]] | 3 | Two-Implementations Goal Test | Done |
| [[.opencode/skills/goal-atomicity-split/SKILL|goal-atomicity-split/]] | 4 | Goal Atomicity Split | Done |
| [[.opencode/skills/constraint-budget-gate/SKILL|constraint-budget-gate/]] | 5 | Constraint Budget Gate | Done |
| [[.opencode/skills/constraint-failure-decision-rule/SKILL|constraint-failure-decision-rule/]] | 6 | Constraint-Failure Decision Rule | Done |

All four skills are authored as review gates / pre-flight checks that run against candidate intent fields before the agent receives them. Each produces a binary verdict and actionable reclassification recommendations.

### 2.3 Exercises (`curriculum/`)

4 new exercises created. Two at Level 2 (goal purity heuristics), two at Level 3 (constraint engineering). All use Python dataclass-based exercises with input/output verification.

| File | Pattern # | Pattern | Level | Status |
|---|---|---|---|---|
| [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-two-implementations-goal-test|exercise-two-implementations-goal-test.md]] | 3 | Two-Implementations Goal Test | 2 | Done |
| [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-goal-atomicity-split|exercise-goal-atomicity-split.md]] | 4 | Goal Atomicity Split | 2 | Done |
| [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-constraint-budget-gate|exercise-constraint-budget-gate.md]] | 5 | Constraint Budget Gate | 3 | Done |
| [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-constraint-failure-decision-rule|exercise-constraint-failure-decision-rule.md]] | 6 | Constraint-Failure Decision Rule | 3 | Done |

### 2.4 Summary by Pattern

| Pattern # | Pattern | Canonical | Skill | Exercise |
|---|---|---|---|---|
| 1 | ICE Ownership Boundary | Existed before | Existed before | — |
| 2 | Three-Part Intent Contract | Done | **Missing** | **Missing** |
| 3 | Two-Implementations Goal Test | Done | Done | Done (Level 2) |
| 4 | Goal Atomicity Split | Done | Done | Done (Level 2) |
| 5 | Constraint Budget Gate | Done | Done | Done (Level 3) |
| 6 | Constraint-Failure Decision Rule | Done | Done | Done (Level 3) |
| 7 | Compartmented Evaluation Architecture | Done | **Missing** | **Missing** |
| 8 | Scenario Destination Split | Done | **Missing** | **Missing** |
| 9 | Harness-Owned Context Assembly | Existed before | Existed before | — |

---

## 3. Cross-Reference: Patterns → Curriculum Levels

Which curriculum level teaches which pattern, based on the [[curriculum/MASTER_PLAN|Curriculum Master Plan]] level structure.

| Level | Focus | Duration | Patterns Introduced | Exercises |
|---|---|---|---|---|
| **Level 1**: Conceitos Fundamentais | Why agents lose focus; token budgeting; basic harness patterns | 3-4h | None directly. Pattern #9 (Harness-Owned Context Assembly) already taught as [[curriculum/05-core-concepts/01-context-management|Context Management core concept]] with token budgeting. | — |
| **Level 2**: Padroes Praticos | Generator/Evaluator, sprint contracts, rubric design, trace reading | 6-8h | Pattern #3 (Two-Implementations Goal Test), Pattern #4 (Goal Atomicity Split). Both are lightweight heuristics that fit the Level 2 goal of "applying patterns that improve reliability." | [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-two-implementations-goal-test|exercise-two-implementations-goal-test]], [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-goal-atomicity-split|exercise-goal-atomicity-split]] |
| **Level 3**: Arquitetura Avancada | Multi-agent systems, state persistence, harness evolution | 8-10h | Pattern #5 (Constraint Budget Gate), Pattern #6 (Constraint-Failure Decision Rule). Constraint engineering requires understanding of Generator-Evaluator separation, which is taught in Level 2. Pattern #7 (Compartmented Evaluation Architecture) conceptually belongs here — it builds on Generator-Evaluator with sealed surfaces. | [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-constraint-budget-gate|exercise-constraint-budget-gate]], [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-constraint-failure-decision-rule|exercise-constraint-failure-decision-rule]] |
| **Level 4**: KODA-Especifico | Application to KODA: architecture, customer journeys, feature design | Continuous | All patterns applied in context. Pattern #7 (Compartmented Evaluation Architecture) would be applied to KODA's recommendation evaluation pipeline. Patterns #2 (Three-Part Intent), #8 (Scenario Destination Split) inform KODA's intent authoring discipline. | Future: KODA-specific exercises for Patterns 2, 7, 8 |

### 3.1 Pattern-to-Level Mapping

| Pattern # | Pattern | Curriculum Level | Rationale |
|---|---|---|---|
| 3 | Two-Implementations Goal Test | Level 2 | Lightweight heuristic. Requires understanding of intents but not multi-agent systems. Pairs naturally with sprint contracts and Generator-Evaluator. |
| 4 | Goal Atomicity Split | Level 2 | Lightweight rule. Same rationale as P3. Both are pre-flight checks on intent quality. |
| 5 | Constraint Budget Gate | Level 3 | Requires understanding of constraint-anchored evaluation, ICE separation, and how constraints affect agent design freedom. |
| 6 | Constraint-Failure Decision Rule | Level 3 | Foundational classification heuristic. Requires understanding of Generator-Evaluator separation (Level 2) and the builder/validator information boundary. |
| 7 | Compartmented Evaluation Architecture | Level 3 (conceptual) / Level 4 (applied) | Builds on Generator-Evaluator and Constraint-Anchored Evaluation (Level 2-3). Applied to KODA in Level 4. |
| 2 | Three-Part Intent Contract | Level 2-3 | Structural model for intent decomposition. Complements intent-five-part-primitive (Level 2). Could be introduced as an alternative decomposition in Level 2 or as a comparison exercise in Level 3. |
| 8 | Scenario Destination Split | Level 3 | Routing rule that depends on understanding the intent/expectations boundary (Level 2) and constraint classification (Level 3). |

---

## 4. Gap Analysis

What remains uncovered after Phase 4a-4c. Cross-referencing the classification's 9 patterns against the three artifact types (canonical doc, skill, exercise).

### 4.1 Patterns Without Skills

Three patterns have canonical docs but no operational skills:

| Pattern # | Pattern | Integration Value | Gap |
|---|---|---|---|
| 2 | Three-Part Intent Contract | Medium | No skill. Would benefit from a skill that validates the three-slot completeness gate (analogous to [[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive]] for the five-part model). |
| 7 | Compartmented Evaluation Architecture | **High** | **Critical gap.** This is the only High-value pattern without a skill. A compartmentation audit skill could verify that failure conditions are not leaked to the builder prompt, validate sealed information surfaces, and detect reward-hacking vectors. |
| 8 | Scenario Destination Split | Medium | No skill. A routing skill could classify scenario statements into Intent (failure) vs Expectations (success) destinations and flag scenarios that appear in both. |

### 4.2 Patterns Without Exercises

Three patterns have canonical docs but no curriculum exercises:

| Pattern # | Pattern | Integration Value | Gap |
|---|---|---|---|
| 2 | Three-Part Intent Contract | Medium | No exercise. Could be a Level 2 comparison exercise: "Given the same requirement, decompose using the three-part contract vs the five-part primitive. Which decomposition exposes more ambiguity?" |
| 7 | Compartmented Evaluation Architecture | **High** | **Critical gap.** No exercise at any level. A Level 3 exercise could simulate information leakage: "Given a builder prompt, identify which statements should have been withheld. Rewrite the prompt with sealed compartments." A Level 4 KODA exercise could apply compartmentation to KODA's product recommendation pipeline. |
| 8 | Scenario Destination Split | Medium | No exercise. A Level 3 exercise could present mixed scenario lists and ask students to route each to the correct destination, then verify against the Constraint-Failure Decision Rule. |

### 4.3 Patterns Fully Covered

Four patterns have the complete set (canonical doc + skill + exercise):

| Pattern # | Pattern | Prior Classification | Artifacts |
|---|---|---|---|
| 3 | Two-Implementations Goal Test | Missing | Canonical + skill + exercise (Level 2) |
| 4 | Goal Atomicity Split | Missing | Canonical + skill + exercise (Level 2) |
| 5 | Constraint Budget Gate | Missing | Canonical + skill + exercise (Level 3) |
| 6 | Constraint-Failure Decision Rule | Missing | Canonical + skill + exercise (Level 3) |

### 4.4 Patterns With No New Artifacts

Two patterns needed no new artifacts because the repo already covers them:

| Pattern # | Pattern | Classification | Existing Coverage |
|---|---|---|---|
| 1 | ICE Ownership Boundary | Already Exists | [[docs/canonical/ice-craft-separation|ICE Craft Separation]], [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]], [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]] |
| 9 | Harness-Owned Context Assembly | Already Exists | 8+ canonical docs including [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]], [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]], [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]. Already taught in [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Level 1 token budgeting]] and [[curriculum/05-core-concepts/01-context-management|Context Management core concept]]. |

### 4.5 Gap Summary

| Category | Count | Highest Priority |
|---|---|---|
| Complete (canonical + skill + exercise) | 4 patterns | P3-P6 |
| Canonical only (missing skill + exercise) | 3 patterns | **P7 (HIGH integration value)** |
| No new artifacts needed (Already Exists) | 2 patterns | P1, P9 |
| **Total patterns** | **9** | |

**Recommended next phase priority:** Pattern #7 (Compartmented Evaluation Architecture) should receive a skill and exercise before Patterns #2 or #8. It carries the highest integration value in the classification and the architectural concept (sealed information surfaces) is the most novel contribution from the Anatomy of Intent analysis.

---

## 5. Dependency Graph

Which patterns depend on which others, forming a layered dependency structure. A pattern that depends on another should be integrated after its dependency is stable.

### 5.1 Dependency Layers

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 0: Existing Repo Foundation (pre-existing, stable)        │
│                                                                 │
│ Generator-Evaluator  ICE Craft Separation  Constraint-Anchored  │
│                                            Evaluation           │
│ Human-Owned Expectations Boundary  Intent as Five-Part          │
│                                    Primitive                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌──────────────────┐
│ Layer 1:      │  │ Layer 1:      │  │ Layer 1:         │
│ Goal Purity   │  │ Classification│  │ Structural Model │
│               │  │               │  │                  │
│ P3 Two-Impl   │  │ P6 Constr-    │  │ P2 Three-Part    │
│ Goal Test  ◄──┼──┤ Failure       │  │ Intent Contract  │
│               │  │ Decision Rule │  │                  │
│ P4 Goal       │  │               │  └────────┬─────────┘
│ Atomicity     │  └───────┬───────┘           │
│ Split         │          │                   │
└───────────────┘          │                   │
        │                  │                   │
        │    ┌─────────────┼───────┐           │
        │    │             │       │           │
        ▼    ▼             ▼       ▼           ▼
┌───────────────┐  ┌───────────────┐  ┌──────────────────┐
│ Layer 2:      │  │ Layer 2:      │  │ Layer 2:         │
│ Constraint    │  │ Scenario      │  │ (fed by Layer 1) │
│ Engineering   │  │ Routing       │  │                  │
│               │  │               │  │                  │
│ P5 Constr     │  │ P8 Scenario   │  │                  │
│ Budget Gate ◄─┼──┤ Destination   │  │                  │
│               │  │ Split         │  │                  │
└───────┬───────┘  └───────┬───────┘  └──────────────────┘
        │                  │
        └────────┬─────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: Evaluation Architecture (top of pyramid)                │
│                                                                 │
│ P7 Compartmented Evaluation Architecture                        │
│                                                                 │
│ Depends on:                                                     │
│  - P6: knows what goes to builder vs validator                  │
│  - P8: scenario routing ensures correct compartment assignment  │
│  - Layer 0: Generator-Evaluator provides the two-agent split    │
│            ICE Craft Separation provides ownership boundary     │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Dependency Matrix

| Dependent Pattern | Depends On | Relationship |
|---|---|---|
| P3 Two-Implementations Goal Test | P2 Three-Part Intent Contract | P3 validates goal statements that populate P2's goal slot. |
| P4 Goal Atomicity Split | P2 Three-Part Intent Contract | P4 splits multi-goal statements into atomic goals, each filling one P2 contract. |
| P4 Goal Atomicity Split | P3 Two-Implementations Goal Test | P3 asks "is this a goal?" P4 asks "is there only one goal here?" Applied sequentially: P3 first, then P4. |
| P5 Constraint Budget Gate | P6 Constraint-Failure Decision Rule | P5 cannot budget constraints until P6 has classified which requirements ARE constraints. The budget gate depends on the decision rule's classification output. |
| P8 Scenario Destination Split | P6 Constraint-Failure Decision Rule | P8 routes scenarios based on constraint/failure classification. Needs P6's "would knowing this change how the builder writes code?" heuristic. |
| P8 Scenario Destination Split | P2 Three-Part Intent Contract | P8 maps scenarios onto P2's three slots: goals, constraints, failure conditions. |
| P7 Compartmented Evaluation Architecture | P6 Constraint-Failure Decision Rule | P7 seals information surfaces based on constraint vs failure classification. P6 determines which information goes to which compartment. |
| P7 Compartmented Evaluation Architecture | P8 Scenario Destination Split | P8's routing rule ensures scenarios arrive at the correct compartment. P7 then seals them. |
| P7 Compartmented Evaluation Architecture | Generator-Evaluator (Layer 0) | P7 extends the Generator-Evaluator's two-agent split with explicit sealed surfaces and leakage prevention. |
| P7 Compartmented Evaluation Architecture | ICE Craft Separation (Layer 0) | P7 inherits the ownership boundary from ICE separation: the human owns Intent and Expectations, the harness enforces compartment discipline. |

### 5.3 Recommended Integration Sequence

| Phase | Layer | Patterns | What to Build | Done When |
|---|---|---|---|---|
| 1. Classification foundation | Layer 1 | P6 Constraint-Failure Decision Rule | Already complete (canonical + skill + exercise). This is the foundational heuristic. | Done in this session. |
| 2. Goal quality gates | Layer 1 | P3 Two-Implementations Goal Test, P4 Goal Atomicity Split | Already complete (canonical + skill + exercise for both). Pair of pre-flight goal-quality heuristics. | Done in this session. |
| 3. Constraint management | Layer 2 | P5 Constraint Budget Gate | Already complete (canonical + skill + exercise). Depends on P6 for constraint classification. | Done in this session. |
| 4. Structural and routing models | Layers 1-2 | P2 Three-Part Intent Contract, P8 Scenario Destination Split | Canonical docs exist. Next: create skills for both, and exercises for both (Level 2 for P2, Level 3 for P8). | Skills and exercises created. |
| 5. Sealed evaluation architecture | Layer 3 | P7 Compartmented Evaluation Architecture | Canonical doc exists. **HIGHEST priority next work:** create compartmentation audit skill and a Level 3 exercise. | Skill verifies sealed surfaces; exercise teaches information leakage prevention. |

**Note:** Phases 1-3 are complete in this session. Phases 4-5 represent future work — the canonical docs exist for P2, P7, and P8, but their skills and exercises remain to be built. P7 should be prioritised first due to its High integration value.

---

## Observations

1. **Canonical docs for P1 and P9 were not created because they were Already Exists.** The repo's `ice-craft-separation`, `owner-of-no-role-design`, and `human-owned-expectations-boundary` cover P1; the extensive context assembly infrastructure (8+ canonical docs) covers P9. No new artifacts were warranted.

2. **The Constraint-Failure Decision Rule (P6) is the most connected pattern in the dependency graph.** It feeds into three other patterns (P5, P7, P8) and provides the classification heuristic that makes the constraint budget gate and compartmented evaluation architecture coherent. Its placement as P0 is justified by this connective role, not just its own impact.

3. **Patterns 2, 7, and 8 each have canonical docs but no skills or exercises.** These three represent the next phase of integration work. P7 is the highest priority among them.

4. **The curriculum exercise placement mirrors the dependency graph.** Level 2 exercises (P3, P4) teach goal-quality heuristics that students need before Level 3 constraint engineering exercises (P5, P6). This matches the recommended integration sequence where Layer 1 precedes Layer 2.
