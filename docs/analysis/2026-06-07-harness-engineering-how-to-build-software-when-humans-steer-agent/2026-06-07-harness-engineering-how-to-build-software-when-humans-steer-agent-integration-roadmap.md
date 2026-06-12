---
title: "Integration Roadmap: Harness Engineering Patterns → long-running-agents"
type: analysis
date: 2026-06-11
aliases: ["harness engineering integration roadmap", "roadmap harness engineering", "integration plan harness"]
tags: ["agentes-orquestracao", "harness", "governanca", "evals", "context-engineering", "curriculo-conteudo"]
last_updated: 2026-06-11
relates-to: ["[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|Harness Engineering Classification]]", "[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]", "[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]", "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]", "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]", "[[docs/system-of-record|System of Record]]"]
sources: ["[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|Harness Engineering Classification]]", "[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]"]
---

# Integration Roadmap: Harness Engineering Patterns → long-running-agents

**Date:** 2026-06-11
**Type:** Analysis
**Precedence:** Level 4 (`[[docs/system-of-record|System of Record]]`:10)
**Source:** `[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification.md]]`
**Scope:** All 16 patterns from the Harness Engineering pattern catalog

---

## Objective

Map each of the 16 Harness Engineering patterns to concrete integration points in the long-running-agents repository: canonical docs, skills, curriculum exercises, and modules. Prioritize by impact and implementation effort. Identify what was created during Phase 4 and what remains uncovered.

---

## 1. Summary Matrix

| # | Pattern | Classification | Impact | Effort | Priority | Integration Surfaces | Artifacts Created (Phase 4) |
|---|---|---|---|---|---|---|---|
| 1 | Durable Non-Functional Requirements Memory | Better Implementation | Low | -- | -- | AGENTS.md + eslint + .editorconfig (already exceeds pattern) | None needed |
| 2 | Reviewer Agents as CI Gates | Already Exists | Low | -- | -- | `.opencode/skills/issue-review/` + PR-Gated Eval Enforcement (operational) | None needed |
| 3 | Garbage Collection Day Meta-Loop | Partial Coverage | High | Medium | P1 | Canonical doc, skill, curriculum exercise | Canonical doc: `garbage-collection-day-meta-loop.md` |
| 4 | Prompt Injection Taxonomy | Partial Coverage | Medium | Medium | P2 | Canonical doc (injection surface taxonomy), resolver metadata | None |
| 5 | Just-in-Time Context Surfacing | Partial Coverage | Medium | Low | P2 | Canonical doc (JIT strategy formalization), resolver trigger map | None |
| 6 | Deep Skills Strategy | Partial Coverage | Medium | Medium | P2 | Resolver metadata, trigger evals, smoke tests, storage schema | None (pipeline quality gates remain missing) |
| 7 | Codebase Uniformity as Agent Affordance | Partial Coverage | Medium | Medium | P2 | Refactoring playbook, agent-navigation rubric, follow-up issue pattern | None (canonical doc exists but playbook missing) |
| 8 | PR as Hub-and-Spoke Broadcast Domain | Already Exists | Low | -- | -- | `.opencode/skills/issue-review/` + PR template + `.opencode/skills/issue-finish/` (operational) | None needed |
| 9 | Micro-Harnesses Architecture | Partial Coverage | Medium | High | P3 | Structural ESLint rules (package privacy, dependency direction) | None (infra exists, structural rules missing) |
| 10 | QA Plan as Agent Contract | Already Exists | Low | -- | -- | Sprint Contract template + Level 2 module + 3 canonical docs (operational) | None needed |
| 11 | Token Budget Optimization | Better Implementation | Low | -- | -- | 4 canonical docs + Level 1 module (exceeds pattern) | None needed |
| 12 | Failure Pattern Classification Loop | Partial Coverage | High | Medium | P1 | Canonical doc, GC Day ritual integration, classification rubric in curriculum | Canonical doc: `failure-pattern-classification-loop.md` |
| 13 | LLM as Fuzzy Compiler | Missing | Medium | High | P0 | Canonical doc, skill, curriculum exercise | Canonical doc + skill + exercise (full stack) |
| 14 | Harness-as-Context-Manager | Better Implementation | Low | -- | -- | 7+ canonical docs (exceeds pattern) | None needed |
| 15 | Persona-Based Documentation | Missing | High | High | P0 | Canonical doc, skill, curriculum exercise, persona reviewer agents | Canonical doc + skill + exercise (full stack) |
| 16 | Harness Evolution Lifecycle | Better Implementation | Low | -- | -- | Measured lifecycle + invariant-compensation split + Level 3 module + Core Concept 6 (exceeds pattern) | None needed |

**Distribution:** 4 Better Implementation, 3 Already Exists, 7 Partial Coverage, 2 Missing

---

## 2. Artifacts Created During Phase 4

### 2.1 Canonical Docs (4 new) -- `docs/canonical/`

| File | Pattern | Pattern # | Classification Before | Gap Closed |
|---|---|---|---|---|
| `llm-as-fuzzy-compiler.md` | LLM as Fuzzy Compiler | 13 | Missing → Canonical defined | Canonical doc: mental model, compiler passes, decision rules, tradeoffs. 131 lines. |
| `persona-based-documentation.md` | Persona-Based Documentation | 15 | Missing → Canonical defined | Canonical doc: persona ownership, NFR documents, reviewer agents, migration from universal AGENTS.md. 128 lines. |
| `garbage-collection-day-meta-loop.md` | Garbage Collection Day Meta-Loop | 3 | Partial Coverage → Strengthened | Canonical doc: weekly cadence, observation collection, categorization rubric, guardrail construction, cadence protection. 125 lines. |
| `failure-pattern-classification-loop.md` | Failure Pattern Classification Loop | 12 | Partial Coverage → Strengthened | Canonical doc: 4-stage loop (observe/classify/build/verify), root cause taxonomy (6 classes), guardrail surface mapping (7 surfaces). 137 lines. |

### 2.2 Skills (2 new) -- `.opencode/skills/`

| Directory | Pattern | Pattern # | What It Does |
|---|---|---|---|
| `llm-as-fuzzy-compiler/SKILL.md` | LLM as Fuzzy Compiler | 13 | Applies compiler mental model when designing harness components, deciding what to preserve vs. regenerate, planning model migrations. Includes compiler pass classification, decision rules (version the recipe, not the cake), model migration checklist, integration map to existing repo infrastructure. 197 lines. |
| `persona-based-documentation/SKILL.md` | Persona-Based Documentation | 15 | Guides writing persona-specific NFR documents with templates, persona identification rules, reviewer agent contracts, and 5-phase migration path from universal AGENTS.md to persona-based model. Includes anti-pattern documentation, quality gates, and integration with existing issue-review workflow. 289 lines. |

### 2.3 Curriculum Exercises (2 new) -- `curriculum/03-nivel-3-advanced-architecture/exercises/`

| File | Pattern | Pattern # | Format |
|---|---|---|---|
| `exercise-04-llm-as-fuzzy-compiler.md` | LLM as Fuzzy Compiler | 13 | Narrative-driven exercise: refactor a harness as a fuzzy compiler. Students implement `HarnessCompiler` class with `LegacyBackend` and `ModernBackend` (simulated LLMs), 3 optimization passes (LintPass, ConstraintPass, ReviewerPass), feedback loop, separation of `DomainInvariant` vs `ModelCompensation`. 7 validation scenarios with test code. ~1,186 lines. |
| `exercise-05-persona-based-documentation.md` | Persona-Based Documentation | 15 | Narrative-driven exercise: implement persona-based documentation system. Students build `PersonaRegistry`, `AgentContextBuilder`, `ReviewerDispatch`. 4 predefined personas (Frontend/Camila, Security/Roberta, UX/Guilherme, Product/PM). 9 validation scenarios with BLOCKING/ADVISORY severity, auto-dispatch by file type. ~1,625 lines. |

### 2.4 Artifacts NOT created (deliberately)

| Pattern | What was NOT created | Rationale |
|---|---|---|
| Garbage Collection Day Meta-Loop (Pattern 3) | Skill + curriculum exercise | Canonical doc establishes the mechanic. Skill/exercise require the weekly cadence ritual to be operationalized — a team-level commitment, not a doc artifact. |
| Failure Pattern Classification Loop (Pattern 12) | Skill + curriculum exercise | Classification rubric is defined in the canonical doc. Separate skill would duplicate the GC Day skill (both execute together). Exercise would be GC Day + classification combined. |
| Prompt Injection Taxonomy (Pattern 4) | Canonical doc | Resolver-based disclosure and hybrid context stack already do the heavy lifting. Taxonomy adds formalization value but lower urgency than Missing patterns. |
| Just-in-Time Context Surfacing (Pattern 5) | Canonical doc | Mechanics exist operationally. Formalization as named pattern adds narrative value but patterns 13 and 15 were higher priority (Missing). |
| Deep Skills Strategy (Pattern 6) | Resolver metadata, trigger evals, smoke tests | Quality gates are implementation work (resolver schema, test infrastructure), not documentation. Requires code changes. |
| Micro-Harnesses Architecture (Pattern 9) | Structural ESLint rules | ESLint infrastructure exists but the repo has minimal source code, limiting immediate applicability. Deferred until codebase grows. |
| Codebase Uniformity (Pattern 7) | Refactoring playbook, agent-navigation rubric | Canonical doc exists (architecture-as-agent-affordance.md). Playbook and rubric are actionable complements but not among the highest-priority gaps. |

---

## 3. Cross-Reference: Patterns → Curriculum Levels

### 3.1 By Pattern

| Pattern # | Pattern | Curriculum Level | Module / Exercise | Status |
|---|---|---|---|---|
| 1 | Durable NFR Memory | Nivel 1 | 03-basic-harness-patterns (concept) | Already covered |
| 2 | Reviewer Agents as CI Gates | Nivel 2 | 01-generator-evaluator-pattern (concept) + `.opencode/skills/issue-review/` (operational) | Already covered |
| 3 | GC Day Meta-Loop | Nivel 3 | 05-harness-evolution (concept) | Canonical doc created. Exercise pending. |
| 4 | Prompt Injection Taxonomy | Nivel 3 | 04-server-side-compaction / 05-harness-evolution (concept) | Not yet integrated |
| 5 | JIT Context Surfacing | Nivel 1 / Nivel 3 | 03-basic-harness-patterns (concept) + 04-server-side-compaction | Not yet formalized |
| 6 | Deep Skills Strategy | Nivel 3 | 01-multi-agent-systems (concept) | Canonical doc exists. Quality gates pending. |
| 7 | Codebase Uniformity as Affordance | Nivel 2 / Nivel 3 | 03-file-based-coordination (concept) | Canonical doc exists. Playbook pending. |
| 8 | PR as Hub-and-Spoke | Nivel 2 | 01-generator-evaluator-pattern (concept) + `.opencode/skills/issue-review/` (operational) | Already covered |
| 9 | Micro-Harnesses Architecture | Nivel 3 | 05-harness-evolution (concept) + ESLint infra | Infra exists. Structural rules pending. |
| 10 | QA Plan as Agent Contract | Nivel 2 | 02-sprint-contracts (full module) + template | Already covered |
| 11 | Token Budget Optimization | Nivel 1 | 02-token-budgeting (full module) | Already covered (exceeds pattern) |
| 12 | Failure Pattern Classification Loop | Nivel 3 | 05-harness-evolution (concept) | Canonical doc created. Exercise pending. |
| 13 | LLM as Fuzzy Compiler | Nivel 3 | 05-harness-evolution + **Exercise 04** (NEW) | Full stack created: canonical doc + skill + exercise |
| 14 | Harness-as-Context-Manager | Nivel 1 / Nivel 3 | 03-basic-harness-patterns + 04-server-side-compaction | Already covered (exceeds pattern) |
| 15 | Persona-Based Documentation | Nivel 3 | 01-multi-agent-systems + **Exercise 05** (NEW) | Full stack created: canonical doc + skill + exercise |
| 16 | Harness Evolution Lifecycle | Nivel 3 | 05-harness-evolution (full module) + Core Concept 6 | Already covered (exceeds pattern) |

### 3.2 By Curriculum Level (what Phase 4 added)

| Level | Existing Coverage | Phase 4 Additions | Gaps Remaining |
|---|---|---|---|
| **Nivel 1** (Fundamentals) | Token Budgeting (Pattern 11), Context Manager concepts (Pattern 14), Basic Harness (Patterns 1, 5) | None (Level 1 already well-covered) | JIT Context Surfacing as formal lesson |
| **Nivel 2** (Practical Patterns) | Sprint Contracts (Pattern 10), Generator/Evaluator (Patterns 2, 8), Rubric Design | None (Level 2 well-covered) | Deep Skills Strategy as exercise |
| **Nivel 3** (Advanced Architecture) | Multi-Agent Systems, State Persistence, File Coordination, Server-Side Compaction, Harness Evolution (Pattern 16) | Exercise 04 (LLM as Fuzzy Compiler, Pattern 13), Exercise 05 (Persona-Based Documentation, Pattern 15) | GC Day exercise, Failure Classification exercise, Prompt Injection Taxonomy lesson, Codebase Uniformity playbook |
| **Nivel 4** (KODA-specific) | 01-koda-architecture, customer journey flows | Persona-based documentation applied to KODA domains (via skill) | GC Day ritual for KODA team, Persona reviewer agents configured for KODA codebase |

---

## 4. Gap Analysis

### 4.1 What Phase 4 closed

Phase 4 targeted the two **Missing** patterns (13, 15) and the two **Partial Coverage with High integration value** patterns (3, 12). Results:

- **Pattern 13 (LLM as Fuzzy Compiler):** Closed from Missing to canonically defined with full vertical integration (canonical doc + skill + curriculum exercise). The mental model is now available to agents via skill loading, taught in the curriculum, and referenced by 8 related canonical docs.

- **Pattern 15 (Persona-Based Documentation):** Closed from Missing to canonically defined with full vertical integration. The persona model, reviewer agent contracts, migration path, and integration with existing issue-review workflow are all documented and operational via skill loading.

- **Pattern 3 (Garbage Collection Day Meta-Loop):** Strengthened from Partial Coverage to canonically defined. The canonical doc connects the existing component mechanisms (QA-to-backlog, harness evolution lifecycle, pain-signal progression, production flywheel) into a coherent weekly ritual with categorization rubric and cadence protection rules. Still missing: operational skill to execute the ritual, curriculum exercise to teach it.

- **Pattern 12 (Failure Pattern Classification Loop):** Strengthened from Partial Coverage to canonically defined. The canonical doc provides the 4-stage loop, root cause taxonomy (6 classes), and guardrail surface mapping (7 surfaces) that were missing from every existing component. Still missing: skill integration with GC Day ritual, curriculum exercise.

### 4.2 What remains uncovered

| Gap | Patterns Affected | Why It Matters | Effort Estimate |
|---|---|---|---|
| **GC Day operational skill** | 3, 12 | Canonical docs define the ritual; a skill would make it executable by agents. Without it, the weekly cadence remains a human-only process. | Medium (new skill, ~250 lines) |
| **GC Day + Classification curriculum exercise** | 3, 12 | Both patterns are High integration value but have no curriculum exercise. Exercise 06 at Nivel 3 could combine both: simulate a week of agent work, categorize failures, build guardrails during a GC Day session. | High (new exercise, ~800 lines) |
| **Prompt Injection Taxonomy canonical doc** | 4 | The repo has all injection surfaces (AGENTS.md, lint rules, test failures, review comments, skills, resolvers) but no taxonomy classifying them with placement guidance. Medium integration value. | Medium (canonical doc, ~100 lines) |
| **JIT Context Surfacing formalization** | 5 | Mechanics exist operationally but are unnamed. Formalizing as a named strategy would prevent future prompt bloat and make the design intent explicit. Medium integration value, low effort. | Low (canonical doc + AGENTS.md amendment, ~80 lines) |
| **Deep Skills Strategy quality gates** | 6 | The skillify pipeline canonical doc is comprehensive but the quality gates (resolver metadata schema, trigger evals, smoke tests, storage schema) remain unimplemented. These are code/infra work, not documentation. | High (implementation work across resolver, test infra, storage schema) |
| **Architecture-as-Affordance playbook + rubric** | 7 | The canonical doc defines the concept but the playbook, module-boundary rubric, and follow-up issue pattern are missing. These would make architecture-as-affordance actionable. | Medium (new canonical doc or playbook, ~150 lines) |
| **Micro-Harnesses structural ESLint rules** | 9 | ESLint infrastructure exists (custom rules directory, config). No package-privacy, dependency-direction, or schema-ownership rules exist. Deferred until codebase grows. | High (ESLint rule development, test coverage, ~400 lines) |

### 4.3 Gap severity summary

| Severity | Count | Patterns |
|---|---|---|
| **Closed** (fully addressed) | 10 | 1, 2, 8, 10, 11, 13, 14, 15, 16 (+ 3, 12 partially) |
| **Canonical doc exists, skill/exercise missing** | 2 | 3 (GC Day), 12 (Failure Classification) |
| **Canonical doc exists, playbook/quality gates missing** | 2 | 6 (Deep Skills), 7 (Codebase Uniformity) |
| **No Phase 4 artifacts** | 4 | 4 (Prompt Injection Taxonomy), 5 (JIT Context), 9 (Micro-Harnesses) |

---

## 5. Recommended Next Steps

### P0: Already completed in Phase 4

- **Pattern 13 (LLM as Fuzzy Compiler):** Canonical doc + skill + exercise created. Ready for curriculum integration and agent use.
- **Pattern 15 (Persona-Based Documentation):** Canonical doc + skill + exercise created. Ready for curriculum integration and agent use.

### P1: Highest remaining leverage (Patterns 3 + 12 combined)

**Create GC Day operational skill and curriculum exercise.** These two patterns are the single highest-leverage gap remaining (both marked High integration value). They share the same execution context (the GC Day ritual) and would be implemented together.

| Action | Artifact | Effort |
|---|---|---|
| Create GC Day operational skill | `.opencode/skills/garbage-collection-day/SKILL.md` | Medium |
| Create combined Nivel 3 exercise | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-06-garbage-collection-day.md` | High |
| Register GC Day in resolver | Resolver metadata for trigger-based loading | Low |
| Add to system-of-record | `[[docs/system-of-record|SOR]]` canonical docs section | Low |

### P2: Formalization debt (Patterns 4, 5)

**Create Prompt Injection Taxonomy and JIT Context Surfacing canonical docs.** Both are Medium integration value, low-to-medium effort. They would formalize existing operational mechanics into named, teachable patterns.

| Action | Artifact | Effort |
|---|---|---|
| Injection Surface Taxonomy canonical doc | `docs/canonical/injection-surface-taxonomy.md` | Medium |
| JIT Context Surfacing canonical doc | `docs/canonical/jit-context-surfacing.md` | Low |
| AGENTS.md amendment (JIT loading policy) | Rule addition to `[[AGENTS|AGENTS.md]]` | Low |

### P3: Deferred until codebase grows or quality gate infrastructure exists

| Action | Artifact | Precondition |
|---|---|---|
| Architecture-as-Affordance playbook | `docs/canonical/architecture-as-affordance-playbook.md` | Module boundaries to evaluate exist in codebase |
| Deep Skills quality gates | Resolver metadata, trigger evals, smoke tests | Test infrastructure for resolver evals exists |
| Micro-Harnesses structural rules | ESLint rules for package privacy, dependency direction | Source code with packages/modules exists |
| Persona reviewer agent implementations | `.opencode/agents/reviewer-frontend.md` etc. | Persona NFR documents operationalized |

---

## 6. Precedence Alignment

Per `[[docs/system-of-record|System of Record]]`:

- **Level 2 (canonical):** 4 new canonical docs added to `docs/canonical/`. These now take precedence over analysis docs and READMEs for their respective patterns. The system-of-record should be updated to include them in the canonical docs table (currently listing 51 docs).
- **Level 4 (analysis):** This roadmap, the classification doc, and the analysis remain at analysis level — they inform but do not override canonical docs.
- **Level 3 (evidence):** No new evidence artifacts were created. The classification doc provides file:line evidence for existing repo coverage.
- **Level 1 (ADRs):** `docs/decisions/` remains empty. The Persona-Based Documentation migration (universal AGENTS.md → persona model) is the strongest ADR candidate from this work.

---

## 7. Integration Summary

Phase 4 transformed 4 patterns from theoretical concepts to operational artifacts:

```
BEFORE Phase 4:
  - 2 patterns classified as Missing (13, 15) — zero repo artifacts
  - 2 patterns classified as Partial Coverage (3, 12) — components exist, ritual missing

AFTER Phase 4:
  + 4 canonical docs (521 total lines of authoritative documentation)
  + 2 operational skills (486 total lines, loaded by agents via resolver triggers)
  + 2 curriculum exercises (2,811 total lines, Nivel 3 advanced architecture)
  + 2 patterns closed from Missing to canonical + skill + exercise (13, 15)
  + 2 patterns strengthened with canonical docs (3, 12)

REMAINING:
  - 2 patterns need skill + exercise (3, 12) — P1
  - 2 patterns need canonical docs (4, 5) — P2
  - 3 patterns need implementation work (6, 7, 9) — P3
  - 7 patterns require no further action (1, 2, 8, 10, 11, 14, 16)
```

Phase 4 prioritized the two Missing conceptual patterns (LLM as Fuzzy Compiler, Persona-Based Documentation) because they required only documentation and curriculum — no code or infrastructure — yet significantly amplify the repository's pedagogical value by reframing the agent workflow and multiplying quality standards across all agent sessions.

---

## References

- `[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification.md]]` — full classification with evidence for all 16 patterns
- `[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|patterns.md]]` — 16 pattern definitions with 6 fields each
- `[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md]]` — non-obvious knowledge extraction
- `[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]` — canonical doc (Pattern 13)
- `[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]` — canonical doc (Pattern 15)
- `[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]` — canonical doc (Pattern 3)
- `[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]` — canonical doc (Pattern 12)
- `.opencode/skills/llm-as-fuzzy-compiler/SKILL.md` — operational skill (Pattern 13)
- `.opencode/skills/persona-based-documentation/SKILL.md` — operational skill (Pattern 15)
- `[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-04-llm-as-fuzzy-compiler|Exercise 04: LLM as Fuzzy Compiler]]` — curriculum exercise (Pattern 13)
- `[[curriculum/03-nivel-3-advanced-architecture/exercises/exercise-05-persona-based-documentation|Exercise 05: Persona-Based Documentation]]` — curriculum exercise (Pattern 15)
- `[[docs/system-of-record|System of Record]]` — documentation precedence and canonical doc registry

---

*Created: 2026-06-11 | From: Harness Engineering Phase 4 artifacts | Precedence: analysis*
