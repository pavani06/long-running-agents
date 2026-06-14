---
title: "Integration Roadmap: IDSD Method Patterns → long-running-agents"
type: analysis
tags: ["agentes-orquestracao", "governanca", "spec-driven-development", "harness-engineering", "context-engineering", "decision-discipline", "agentic-coding", "curriculo-conteudo"]
date: 2026-06-12
aliases: ["roadmap IDSD", "plano integracao IDSD", "proximos passos IDSD", "integration roadmap IDSD", "IDSD integration plan", "mapeamento integracao IDSD", "ICE integration roadmap"]
relates-to: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]", "[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]", "[[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/system-of-record|System of Record]]"]
sources: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]"]
last_updated: 2026-06-12
---

> [!warning] Formato legado
> Este arquivo usa o formato histórico `integration-roadmap.md`.
> Sessões a partir de 2026-06-14 usam `<date>-<source-slug>-artifacts.{md,yaml}`.
> Preservado para rastreabilidade e estabilidade de wikilinks.

# Integration Roadmap: IDSD Method Patterns → long-running-agents

**Date:** 2026-06-12
**Type:** Analysis
**Precedence:** Level 4 (`docs/system-of-record.md:19`)
**Source Patterns:** 8 agentic patterns from "IDSD — Intent-Driven Software Development" (Kapil Viren Ahuja, 2026)
**Source Classification:** [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|2026-06-12-idsd-method-classification.md]]

---

## Objective

Map each of the 8 agentic patterns extracted from the IDSD Method to concrete integration points in the long-running-agents repository: canonical docs, skills, curriculum exercises, lessons, and future implementation work. Prioritize by impact, effort, and integration value from the [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]].

---

## 1. Summary Matrix

| #   | Pattern                           | Classification        | Impact | Effort | Priority | Integration Surface                                                   |
| --- | --------------------------------- | --------------------- | ------ | ------ | -------- | --------------------------------------------------------------------- |
| 1   | ICE Craft Separation              | Partial Coverage      | High   | Medium | **P0**   | Canonical doc, curriculum lesson (Nivel 2/3), skill (future)          |
| 2   | Intent as Five-Part Primitive     | Missing               | Medium | Low    | **P1**   | Canonical doc, skill, exercise (Nivel 2)                              |
| 3   | Human-Owned Expectations Boundary | Partial Coverage      | High   | Medium | **P0**   | Canonical doc, curriculum lesson (Nivel 2), skill (future)            |
| 4   | Harness-Owned Progressive Context | Better Implementation | Low    | —      | —        | Repo exceeds pattern — no integration needed                          |
| 5   | Agentic Loop with Validation Gate | Already Exists        | Low    | —      | —        | Already covered by Generator-Evaluator + Owned Control Loop           |
| 6   | Presence-in-the-Loop Metric       | Missing               | Medium | Low    | **P1**   | Canonical doc, skill, exercise (Nivel 3)                              |
| 7   | Symphony Trap Awareness           | Partial Coverage      | Medium | Low    | **P2**   | Canonical doc, skill (future), curriculum reframe                     |
| 8   | Token Economics of Gap-Filling    | Partial Coverage      | High   | Medium | **P0**   | Canonical doc, curriculum lesson (Nivel 1), skill + exercise (future) |

**Priority legend:**
- **P0** — High integration value, partial coverage needs completing with curriculum + skills
- **P1** — Missing patterns now covered with canonical doc + skill + exercise; additional curriculum integration remains
- **P2** — Medium integration value, canonical doc exists; skill and curriculum reframe are lower urgency

---

## 2. Artifacts Created During This Session (2026-06-12)

### 2.1 Canonical Docs (`docs/canonical/`)

6 new canonical docs created in this session:

| File | Pattern # | Classification | Status |
|---|---|---|---|
| [[docs/canonical/ice-craft-separation\|ice-craft-separation.md]] | 1 — ICE Craft Separation | Partial Coverage → Formalized | Done |
| [[docs/canonical/intent-five-part-primitive\|intent-five-part-primitive.md]] | 2 — Intent as Five-Part Primitive | Missing → Filled | Done |
| [[docs/canonical/human-owned-expectations-boundary\|human-owned-expectations-boundary.md]] | 3 — Human-Owned Expectations Boundary | Partial Coverage → Formalized | Done |
| [[docs/canonical/presence-in-the-loop-metric\|presence-in-the-loop-metric.md]] | 6 — Presence-in-the-Loop Metric | Missing → Filled | Done |
| [[docs/canonical/symphony-trap-awareness\|symphony-trap-awareness.md]] | 7 — Symphony Trap Awareness | Partial Coverage → Formalized | Done |
| [[docs/canonical/token-economics-gap-filling\|token-economics-gap-filling.md]] | 8 — Token Economics of Gap-Filling | Partial Coverage → Formalized | Done |

**Grouped by classification:**

- **Missing → Now documented:** Pattern #2 (Intent as Five-Part Primitive), Pattern #6 (Presence-in-the-Loop Metric)
- **Partial Coverage → Now formalized:** Pattern #1 (ICE Craft Separation), Pattern #3 (Human-Owned Expectations Boundary), Pattern #7 (Symphony Trap Awareness), Pattern #8 (Token Economics of Gap-Filling)
- **Already Exists / Better Implementation:** Pattern #4 (Harness-Owned Progressive Context), Pattern #5 (Agentic Loop with Validation Gate) — no new canonical docs needed

### 2.2 Skills (`.opencode/skills/`)

2 new skills created in this session:

| Directory | Pattern # | Pattern | Status |
|---|---|---|---|
| [[.opencode/skills/intent-five-part-primitive/SKILL\|intent-five-part-primitive/SKILL.md]] | 2 | Intent as Five-Part Primitive | Done |
| [[.opencode/skills/presence-in-the-loop-metric/SKILL\|presence-in-the-loop-metric/SKILL.md]] | 6 | Presence-in-the-Loop Metric | Done |

Both skills define YAML frontmatter with description, triggers, compatibility (`opencode`), metadata (audience, workflow, priority), and operational instructions. Each implements the corresponding pattern as a loadable agent capability.

### 2.3 Curriculum Exercises (`curriculum/`)

2 new exercises created in this session:

| File | Pattern # | Level | Status |
|---|---|---|---|
| [[curriculum/02-nivel-2-practical-patterns/exercises/exercise-05-intent-five-part-primitive\|exercise-05-intent-five-part-primitive.md]] | 2 — Intent as Five-Part Primitive | Nivel 2 | Done |
| [[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-06-presence-in-the-loop-metric\|exercise-06-presence-in-the-loop-metric.md]] | 6 — Presence-in-the-Loop Metric | Nivel 3 | Done |

Both exercises follow the curriculum exercise format: prolog (narrative scenario), objectives, prerequisites, implementation steps, and solution guide.

### 2.4 Analysis Docs (this session)

| File | Scope |
|---|---|
| [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model\|2026-06-12-idsd-method-mental-model.md]] + `.yaml` | Full repo mental model (Phase 0) |
| [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis\|2026-06-12-idsd-method-analysis.md]] | Knowledge extraction from IDSD source |
| [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns\|2026-06-12-idsd-method-patterns.md]] | 8 agentic patterns extracted |
| [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification\|2026-06-12-idsd-method-classification.md]] | Comparative classification vs. repo |
| `2026-06-12-idsd-method-integration-roadmap.md` (this file) | Integration roadmap |

---

## 3. Cross-Reference Table

### 3.1 Patterns → Curriculum Levels

| # | Pattern | Nivel 1 (Fundamentos) | Nivel 2 (Praticos) | Nivel 3 (Avancado) | Nivel 4 (KODA) |
|---|---|---|---|---|---|
| 1 | ICE Craft Separation | — | Owner-of-No, Grill-Me, Sprint Contracts | Generator-Evaluator, Multi-Agent | Governance patterns |
| 2 | Intent as Five-Part Primitive | — | **Exercise 05** (new), Sprint Contracts | — | — |
| 3 | Human-Owned Expectations Boundary | — | Generator-Evaluator, Sprint Contracts, Rubric Design | Constraint-Anchored Eval | Evaluation Rubrics |
| 4 | Harness-Owned Progressive Context | Token Budgeting, Context Windowing | — | Resolver-Based Context | Harness Improvements |
| 5 | Agentic Loop with Validation Gate | Basic Harness Patterns | Generator-Evaluator | Plan-Execute-Verify, Multi-Agent | — |
| 6 | Presence-in-the-Loop Metric | — | — | **Exercise 06** (new), Multi-Agent, Value-Gated Loop | Manual Brake, Deferred Ledger |
| 7 | Symphony Trap Awareness | — | — | LLM as Fuzzy Compiler, Harness Evolution | — |
| 8 | Token Economics of Gap-Filling | Token Budgeting, Burn Rate, Phase Monitor | Deferred Ledger | Budget-Aware Handoff | — |

### 3.2 Patterns → Existing Canonical Docs

| # | Pattern | Primary Canonical Docs | Supporting Canonical Docs |
|---|---|---|---|
| 1 | ICE Craft Separation | [[docs/canonical/ice-craft-separation\|ICE Craft Separation]] (new) | [[docs/canonical/owner-of-no-role-design\|Owner-of-No Role Design]], [[docs/canonical/grill-me-alignment-interview\|Grill-Me Alignment Interview]], [[docs/canonical/application-owned-agent-control-plane\|Application-Owned Agent Control Plane]], [[docs/canonical/shared-design-concept-handoff\|Shared Design Concept Handoff]] |
| 2 | Intent as Five-Part Primitive | [[docs/canonical/intent-five-part-primitive\|Intent as Five-Part Primitive]] (new) | [[docs/canonical/ice-craft-separation\|ICE Craft Separation]], [[docs/canonical/grill-me-alignment-interview\|Grill-Me Alignment Interview]], [[docs/canonical/constraint-anchored-evaluation\|Constraint-Anchored Evaluation]] |
| 3 | Human-Owned Expectations Boundary | [[docs/canonical/human-owned-expectations-boundary\|Human-Owned Expectations Boundary]] (new) | [[docs/canonical/ice-craft-separation\|ICE Craft Separation]], [[docs/canonical/generator-evaluator\|Generator-Evaluator]], [[docs/canonical/owner-of-no-role-design\|Owner-of-No Role Design]], [[docs/canonical/constraint-anchored-evaluation\|Constraint-Anchored Evaluation]], [[docs/canonical/value-gated-agent-control-loop\|Value-Gated Agent Control Loop]] |
| 4 | Harness-Owned Progressive Context | [[docs/canonical/resolver-based-context-progressive-disclosure\|Resolver-Based Context Progressive Disclosure]] | [[docs/canonical/hybrid-context-stack\|Hybrid Context Stack]], [[docs/canonical/head-tail-context-truncation\|Head-Tail Context Truncation]], [[docs/canonical/addressable-memory-catalog\|Addressable Memory Catalog]], [[docs/canonical/stable-harness-prompt\|Stable Harness Prompt]], [[docs/canonical/skill-resolver-skillify-capability-pipeline\|Skill-Resolver-Skillify Pipeline]] |
| 5 | Agentic Loop with Validation Gate | [[docs/canonical/generator-evaluator\|Generator-Evaluator]] | [[docs/canonical/owned-agent-control-loop\|Owned Agent Control Loop]], [[docs/canonical/plan-execute-verify\|Plan-Execute-Verify]], [[docs/canonical/constraint-anchored-evaluation\|Constraint-Anchored Evaluation]], [[docs/canonical/value-gated-agent-control-loop\|Value-Gated Agent Control Loop]], [[docs/canonical/structured-generation-constraint-validation-circuit\|Structured Generation + Constraint Validation Circuit]] |
| 6 | Presence-in-the-Loop Metric | [[docs/canonical/presence-in-the-loop-metric\|Presence-in-the-Loop Metric]] (new) | [[docs/canonical/manual-brake-question-gate\|Manual Brake Question Gate]], [[docs/canonical/human-afk-task-routing-gate\|Human/AFK Task Routing Gate]], [[docs/canonical/grill-me-alignment-interview\|Grill-Me Alignment Interview]], [[docs/canonical/owner-of-no-role-design\|Owner-of-No Role Design]], [[docs/canonical/value-gated-agent-control-loop\|Value-Gated Agent Control Loop]] |
| 7 | Symphony Trap Awareness | [[docs/canonical/symphony-trap-awareness\|Symphony Trap Awareness]] (new) | [[docs/canonical/llm-as-fuzzy-compiler\|LLM as Fuzzy Compiler]], [[docs/canonical/production-grounded-eval-sampling\|Production-Grounded Eval Sampling]], [[docs/canonical/production-failure-regression-flywheel\|Production Failure Regression Flywheel]], [[docs/canonical/eval-to-production-correlation-tracking\|Eval-to-Production Correlation Tracking]] |
| 8 | Token Economics of Gap-Filling | [[docs/canonical/token-economics-gap-filling\|Token Economics of Gap-Filling]] (new) | [[docs/canonical/explicit-token-budget-ledger\|Explicit Token Budget Ledger]], [[docs/canonical/burn-rate-runtime-forecast\|Burn Rate Runtime Forecast]], [[docs/canonical/phase-gated-token-health-monitor\|Phase-Gated Token Health Monitor]], [[docs/canonical/deferred-ledger-agentic-work\|Deferred Ledger for Agentic Work]], [[docs/canonical/budget-aware-session-handoff\|Budget-Aware Session Handoff]], [[docs/canonical/manual-brake-question-gate\|Manual Brake Question Gate]] |

### 3.3 Patterns → Skills

| # | Pattern | Existing Skills | New Skills (this session) | Missing Skills |
|---|---|---|---|---|
| 1 | ICE Craft Separation | `analyze-and-improve`, `owner-of-no-role`, `manual-brake-question-gate`, `grill-me-alignment-interview` | — | `ice-craft-separation` (P0 future) |
| 2 | Intent as Five-Part Primitive | — | [[.opencode/skills/intent-five-part-primitive/SKILL\|intent-five-part-primitive]] | — |
| 3 | Human-Owned Expectations Boundary | `generator-evaluator`, `owner-of-no-role` | — | `human-owned-expectations-boundary` (P0 future) |
| 4 | Harness-Owned Progressive Context | `issue-start`, `issue-review`, `issue-finish` (resolver loading), `skillify` | — | — |
| 5 | Agentic Loop with Validation Gate | `orchestrator`, `issue-review` (validation gates) | — | — |
| 6 | Presence-in-the-Loop Metric | — | [[.opencode/skills/presence-in-the-loop-metric/SKILL\|presence-in-the-loop-metric]] | — |
| 7 | Symphony Trap Awareness | `llm-as-fuzzy-compiler` | — | `symphony-trap-awareness` (P2 future) |
| 8 | Token Economics of Gap-Filling | `deferred-ledger-agentic-work`, `manual-brake-question-gate` | — | `token-economics-gap-filling` (P0 future) |

---

## 4. Gap Analysis

### 4.1 Gaps Closed in This Session

| What Was Missing | What Was Created | Classification Transition |
|---|---|---|
| Intent as Five-Part Primitive — no canonical doc, skill, or curriculum exercise existed | Canonical doc, skill, exercise (Nivel 2) | Missing → Documented + Operational |
| Presence-in-the-Loop Metric — no canonical doc, skill, or curriculum exercise existed | Canonical doc, skill, exercise (Nivel 3) | Missing → Documented + Operational |
| ICE Craft Separation — no canonical doc formalized the ICE trichotomy | Canonical doc with explicit craft ownership and relation mapping | Partial Coverage → Formalized |
| Human-Owned Expectations Boundary — expectations ownership was implicit | Canonical doc formalizing "expectations as named artifact owned by outcome-owner" | Partial Coverage → Formalized |
| Symphony Trap Awareness — reverse-engineering ritual not formalized as named practice | Canonical doc formalizing running-system spec distillation | Partial Coverage → Formalized |
| Token Economics of Gap-Filling — gap-cost attribution model did not exist | Canonical doc formalizing gap-cost reports and ICE field gap attribution | Partial Coverage → Formalized |

### 4.2 Gaps Still Open (Remaining Work)

These are concrete, actionable gaps that remain after this session. Ordered by priority.

| # | Gap | Pattern | What Is Missing | Recommended Action | Priority |
|---|---|---|---|---|---|
| 1 | ICE Craft Separation skill | #1 | No `.opencode/skill` that executes the ICE decomposition as an agent workflow | Create `ice-craft-separation` skill that takes an incoming task and decomposes it into Intent, Context, and Expectations artifacts before the agent loop starts | P0 |
| 2 | ICE Craft Separation exercise | #1 | No curriculum exercise that teaches students to decompose a real task into ICE crafts | Create exercise at Nivel 2 or 3: decompose a KODA feature into Intent, Context, and Expectations with explicit owner assignments | P0 |
| 3 | Human-Owned Expectations Boundary skill | #3 | No skill that validates whether expectations are authored by the outcome-owner | Create `human-owned-expectations-boundary` skill that checks expectation authorship and rejects agent-authored done definitions | P0 |
| 4 | Token Economics of Gap-Filling skill | #8 | No skill that produces gap-cost reports from session traces | Create `token-economics-gap-filling` skill that analyzes session traces and attributes token cost to specific ICE field gaps | P0 |
| 5 | Token Economics of Gap-Filling exercise | #8 | No curriculum exercise on gap-cost attribution | Create exercise at Nivel 1 or 2: analyze a real session trace and attribute token burn to missing intent, context, or expectations fields | P0 |
| 6 | Human-Owned Expectations Boundary exercise | #3 | No curriculum exercise on outcome-owner authored expectations | Create exercise at Nivel 2: write an expectations artifact in outcome-owner language, validate against Generator-Evaluator loop | P0 |
| 7 | Symphony Trap Awareness skill | #7 | No skill that guides the running-system spec distillation ritual | Create `symphony-trap-awareness` skill: observe running system → ambiguity probes → behavior extraction → reference spec | P2 |
| 8 | Curriculum lesson: Token Economics of Gap-Filling | #8 | `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md` does not cover gap-cost attribution | Add section to Token Budgeting lesson explaining exponential gap-filling penalty and linking to `token-economics-gap-filling` canonical doc | P1 |
| 9 | Curriculum lesson: ICE Craft Separation | #1 | No dedicated lesson on ICE decomposition | Add lesson at Nivel 2 or 3 covering ICE trichotomy, craft ownership, and the gap-list that prevents agents from inventing missing decisions | P1 |
| 10 | Symphony Trap Awareness curriculum reframe | #7 | `llm-as-fuzzy-compiler.md` (lesson) and `production-grounded-eval-sampling.md` (canonical) cover adjacent concepts but do not teach the running-system spec distillation ritual | Add sidebar or section to Nivel 3 lessons linking to `symphony-trap-awareness.md` canonical doc | P2 |
| 11 | `docs/system-of-record.md` update | All | System of Record still declares 55 canonical patterns; repo now has 63 `docs/canonical/` files | Update the System of Record canonical patterns table to include the 6 new canonical docs from this session | P1 |

### 4.3 Patterns Requiring No Further Integration

| # | Pattern | Reason |
|---|---|---|
| 4 | Harness-Owned Progressive Context | Repo exceeds the pattern's maturity with 8+ canonical docs (Resolver-Based Context, Hybrid Context Stack, Head-Tail Truncation, Addressable Memory Catalog, Stable Harness Prompt, Skill Pipeline), 3+ operational skills, and a curriculum lesson. Classification: Better Implementation. |
| 5 | Agentic Loop with Validation Gate | Already fully covered by Generator-Evaluator (functionally identical loop), Owned Agent Control Loop (loop architecture), Plan-Execute-Verify (phase separation), Constraint-Anchored Evaluation (validation mechanics), and Value-Gated Agent Control Loop (value extension). Classification: Already Exists. |

### 4.4 Summary of Remaining Work

| Priority | Count | Effort Estimate |
|---|---|---|
| P0 (skills + exercises for High-value patterns) | 6 gaps | ~4-6 sessions |
| P1 (curriculum lessons + system-of-record update) | 3 gaps | ~2-3 sessions |
| P2 (Symphony Trap awareness — lower urgency) | 2 gaps | ~1-2 sessions |
| **Total remaining** | **11 gaps** | **~7-11 sessions** |

**Critical path:** The three P0 patterns — ICE Craft Separation (#1), Human-Owned Expectations Boundary (#3), and Token Economics of Gap-Filling (#8) — all share the same structural concern (the intent-to-execution boundary). Completing the skills and exercises for these three would close the integration value loop: separation (ICE) → ownership (Expectations) → cost measurement (Gap-Filling).

---

## References

- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]] — full classification of all 8 patterns with file:line evidence
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]] — complete pattern catalog with inputs, outputs, benefits, limitations
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]] — non-obvious knowledge extraction from source
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]] — repository mental model (Phase 0)
- [[docs/system-of-record|System of Record]] — governance index and documentation precedence

---

*This roadmap was generated by the analyze-and-improve pipeline (Phase 3: Integration Planning) on 2026-06-12. Patterns #2 and #6 were classified as Missing and now have full coverage (canonical + skill + exercise). Patterns #1, #3, #7, #8 were classified as Partial Coverage and now have canonical docs, with skills and exercises remaining as future work. Patterns #4 and #5 are already covered or exceeded by the repo.*
