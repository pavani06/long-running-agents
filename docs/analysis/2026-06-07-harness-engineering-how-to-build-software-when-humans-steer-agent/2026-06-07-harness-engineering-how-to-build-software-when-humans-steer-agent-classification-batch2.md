---
title: "Classification Batch 2: Patterns 9-16 from Harness Engineering vs. long-running-agents"
type: analysis
tags: ["agentes-orquestracao", "harness", "context-engineering", "evals", "governanca"]
date: 2026-06-11
aliases: ["classification batch 2", "harness engineering classification batch 2", "patterns 9-16 classification"]
relates-to: ["[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-mental-model|Harness Engineering Mental Model]]", "[[docs/system-of-record|System of Record]]"]
sources: ["[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]"]
---

# Classification Batch 2: Patterns 9-16

Evidence-based classification of patterns 9 through 16 extracted from the Harness Engineering analysis, compared against the `long-running-agents` repository. Precedence order follows [[docs/system-of-record|System of Record]]: decisions > canonical > evidence > analysis > curriculum > READMEs.

## Pattern 9: Micro-Harnesses Architecture

**Source:** [[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md:134-139]]

**Classification: Partial Coverage**

**Justification:** The repository has the foundation for structural checks via custom ESLint rules, but these operate at syntax/behavior level, not at the architectural structure level the source describes. The source defines micro-harnesses as structural checks that assert code organization (package privacy, dependency direction, schema ownership, canonical helpers) rather than user behavior. The repo's closest equivalents are its two custom ESLint rules, but neither enforces package privacy or dependency edges between layers. The `architecture-as-agent-affordance.md` canonical doc covers the general principle of architecture as navigable terrain but does not define executable structural checks.

**Evidence:**
- `eslint-rules/no-catch-message.js:1-172` — custom ESLint rule that prevents `.message` access on catch-bound errors; this is a syntax-level guard, not an architectural structure check
- `eslint-rules/no-raw-console-in-scripts.js:1-133` — custom ESLint rule that enforces use of safe-console helpers; this enforces a canonical helper pattern, which is the closest existing mechanic to "canonical implementation guard" from the source
- `eslint.config.js:12-13` — imports and applies both custom rules, but contains no `import/no-restricted-paths`, `import/no-internal-modules`, or dependency-direction rules
- `docs/canonical/architecture-as-agent-affordance.md:29-38` — defines deep modules, boundary tests, and reduced coupling as agent affordances, but this is architectural guidance, not executable structural checks
- NOT_FOUND for dependency-edge checks, package-privacy enforcement, or schema-ownership assertions in `eslint.config.js`, `eslint-rules/`, `scripts/`, or `package.json`
- NOT_FOUND for any test that asserts code organization against architectural rules in `tests/`

**Integration Value: Medium.** The ESLint infrastructure exists and could host structural rules. The repo currently has minimal source code, limiting immediate applicability, but as the codebase grows, package-privacy and dependency-edge checks would prevent agent-local coherence drift.

---

## Pattern 10: QA Plan as Agent Contract

**Source:** [[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md:95-104, 163-165]]

**Classification: Already Exists**

**Justification:** The Sprint Contract pattern is one of the repository's 8 core concepts. It formalizes the agreement between Generator and Evaluator with explicit inputs, success criteria, constraints, metrics, and failure handling — exceeding the source's framing of "QA plan as agent contract." The curriculum teaches this across three levels, a 2875-line operational template exists, and the concept is reinforced by `generator-evaluator.md`, `constraint-anchored-evaluation.md`, and `plan-execute-verify.md`. The repo's version is more formalized, measurable, and reusable than the source's description.

**Evidence:**
- `curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md` — Level 2 lesson teaching the contract between Generator and Evaluator with explicit criteria and negotiation
- `curriculum/08-tools-templates/sprint-contract-template.md:1-80` — 2875-line canonical template with Input Specification, Success Criteria, Constraints, Metrics, Failure Handling, and sign-off mechanics
- `curriculum/05-core-concepts/04-sprint-contracts.md` — core concept definition as one of 8 foundational ideas
- `curriculum/MASTER_PLAN.md:345` — Sprint Contracts listed as Core Concept 4
- `docs/canonical/constraint-anchored-evaluation.md:31` — evaluation anchored in explicit, verifiable constraints from persisted state
- `docs/canonical/generator-evaluator.md:31` — Generator/Evaluator architecture with explicit contract between the two roles
- `docs/canonical/plan-execute-verify.md:31` — three-phase separation with checkpoints and per-phase contracts
- `curriculum/GLOSSARY.md:117-118` — defines Sprint Contract as "acordo previo entre generator e evaluator sobre o que pronto significa"

**Integration Value: Low.** The repo already has a more mature implementation. The Sprint Contract concept is foundational to the curriculum and reinforced by multiple canonical docs. No integration needed beyond noting the alignment.

---

## Pattern 11: Token Budget Optimization

**Source:** [[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md:159-161]]

**Classification: Better Implementation**

**Justification:** The source presents a rough heuristic ("~1/3 planning, ~1/3 implementation, ~1/3 CI"). The repo has formalized token budgeting into a multi-layered canonical architecture with explicit ledger schema, runtime burn-rate forecasting, phase-gated health monitoring, and budget-aware session handoff. Four canonical docs plus the Level 1 curriculum lesson exceed the source's maturity by providing measurable, auditable, and proactive token governance rather than a post-hoc allocation guideline.

**Evidence:**
- `docs/canonical/explicit-token-budget-ledger.md:30-59` — per-call ledger with 9 canonical fields: model context window, fixed prompt cost, tool schema cost, durable state cost, accumulated context cost, planned input cost, response buffer, safety buffer, remaining budget, and budget percentage
- `docs/canonical/burn-rate-runtime-forecast.md:31-56` — runtime token consumption forecasting with velocity, acceleration, runway estimation, and intervention mapping
- `docs/canonical/phase-gated-token-health-monitor.md:31-60` — operational health phases (green/yellow/orange/red) driven by remaining budget percentage and burn-rate acceleration
- `docs/canonical/budget-aware-session-handoff.md:26-45` — session handoff triggered by token health with fresh-session payload construction
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:34-62` — foundation lesson defining token budgeting as planning, allocating, and controlling token use; includes budget equation, burn-rate formula, and viability calculator
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:428-566` — conversation viability calculator with reserves, remaining budget estimation, remaining messages, and KODA phase scenarios

**Integration Value: Low.** The repo's token budget architecture is significantly more mature than the source. No integration needed; the source's "rule of thirds" could be referenced as a practical rule of thumb in the curriculum.

---

## Pattern 12: Failure Pattern Classification Loop

**Source:** [[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md:47-57, 185-193]]

**Classification: Partial Coverage**

**Justification:** The repo has the mechanical infrastructure for classifying failures and converting them into durable guardrails: the QA-to-Backlog Feedback Loop converts review findings to issues, the Tested Degradation Ladder classifies failures into rungs, the Production Failure Regression Flywheel turns production incidents into eval cases, and the Closed-Loop Agent OS includes feedback writeback. However, the WEEKLY CADENCE and ritual aspect ("Garbage Collection Day" as a Friday meta-loop) is absent. The source's key mechanic — a recurring weekly review where humans categorize slop patterns and systematically eliminate behavior classes — has no equivalent cadenced ritual in the repo's skills, curriculum, or canonical docs.

**Evidence:**
- `docs/canonical/tested-degradation-ladder.md:29-65` — ordered failure classification into retryable/unsafe/hold, with retry, safe fallback, human escalation, outcome logging, and rung tests
- `docs/canonical/qa-to-backlog-feedback-loop.md:30-44` — formalizes QA/review findings as backlog inputs with capture, triage, conversion, and return-to-board stages
- `docs/canonical/production-failure-regression-flywheel.md:28-40` — transforms production failures into durable regression cases with trace, labels, tier assignment, and deduplication
- `docs/canonical/closed-loop-agent-operating-system.md:32-45` — includes feedback writeback as operating system surface with ownership, validation, and memory update
- `docs/canonical/pain-signal-eval-progression-gate.md:40-51` — maps observed pain signals to next eval capabilities, closest mechanic to "observe failure → build capability"
- NOT_FOUND for a weekly cadence or ritual in `.opencode/skills/`, `docs/canonical/`, `curriculum/07-implementation-guides/`, or `scripts/`. The orchestrator skill handles blocker triage but not a weekly classification cycle
- NOT_FOUND for a "harness garbage collection" or "weekly slop review" mechanism that categorizes failure classes and systematically builds guardrails from them

**Integration Value: High.** Adding a weekly GC ritual as a curriculum exercise or skill would close the loop between the existing mechanical infrastructure (degradation ladder, flywheel, QA-to-backlog) and the human observation-to-automation cycle. This is the highest-leverage missing piece in batch 2.

---

## Pattern 13: LLM as Fuzzy Compiler

**Source:** [[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md:59-63, 201-210]]

**Classification: Missing**

**Justification:** The concept of "LLM as fuzzy compiler, harness as optimization passes, code as disposable build artifact" does not exist in any canonical doc, curriculum lesson, or skill in the repository. The mental model appears only in the Harness Engineering analysis documents themselves. Adjacent canonical docs cover related but distinct concepts: `invariant-compensation-split.md` classifies harness controls by domain risk vs. model weakness (not compiler passes), and `measured-harness-evolution-lifecycle.md` governs component lifecycle (not code-as-artifact). The patterns.md pattern "Durable Harness Asset Preservation" captures the "preserve prompts/guardrails, not code" idea but has no corresponding canonical doc.

**Evidence:**
- `docs/canonical/invariant-compensation-split.md:31-60` — classifies harness controls as domain invariants vs. model-specific compensations; this is the closest canonical doc but addresses harness component governance, not the LLM-as-compiler mental model
- `docs/canonical/measured-harness-evolution-lifecycle.md:29-62` — governs component lifecycle through BUILD/STABILIZE/SIMPLIFY/REMOVE; related to model improvement triggering harness changes, but does not frame the LLM as a compiler backend
- NOT_FOUND for "LLM as compiler," "fuzzy compiler," "compilation target," or "code as build artifact" in `docs/canonical/`, `curriculum/`, `docs/decisions/`, `.opencode/skills/`, or `.opencode/agents/`
- NOT_FOUND for "code is disposable," "replaceable output," or "generated code as artifact" in `docs/canonical/`, `curriculum/05-core-concepts/`, or `curriculum/README.md`
- The concept exists in analysis documents only: `2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns.md:367` and `2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis.md:61-63, 208` — these are the source material being classified, not evidence of repo coverage

**Integration Value: Medium.** The LLM-as-compiler mental model is a powerful reframe that would add pedagogical value to the curriculum and connect the existing `invariant-compensation-split.md` and `measured-harness-evolution-lifecycle.md` into a coherent narrative. It does not require new code or infrastructure — it is a conceptual lens.

---

## Pattern 14: Harness-as-Context-Manager

**Source:** [[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md:35-39, 201-210]]

**Classification: Better Implementation**

**Justification:** The source defines harness engineering as "give the model text at the right time." The repo has formalized this into a complete context-engineering architecture with 7+ canonical docs that define ordered context layers, token budgets, decision traces, progressive disclosure, stable prompt preservation, recoverable omitted content, and durable state injection. The repo's `hybrid-context-stack.md` is a direct, formalized implementation of the source's core thesis. The repo's architecture exceeds the source by providing explicit layer ordering, budget enforcement, decision traceability, and integration between context management and eval validation.

**Evidence:**
- `docs/canonical/hybrid-context-stack.md:30-42` — layered context assembly policy with 7 ordered steps: reserve non-negotiable budget, inject durable state, preserve head/tail anchors, add summaries after pinned state, expose omitted middle via catalog, emit decision trace, reduce optional layers first when over budget
- `docs/canonical/stable-harness-prompt.md:26-41` — separates stable harness prompt from reducible context payload; harness instructions survive context reduction as a first-class input with its own budget and version
- `docs/canonical/resolver-based-context-progressive-disclosure.md:28-53` — loads context on demand via resolvers rather than front-loading all instructions; directly implements "give text at the right time"
- `docs/canonical/head-tail-context-truncation.md:28-39` — preserves head and tail anchors while making middle content recoverable by handle
- `docs/canonical/addressable-memory-catalog.md:30-43` — retrieval metadata for omitted content with id, location, preview, scope, and fetch
- `docs/canonical/external-state-persistence.md:31-57` — extracts critical data to external store, loads on next turn, merges with current context
- `docs/canonical/budget-aware-session-handoff.md:26-45` — fresh-session handoff with selected anchors and recoverable omitted content

**Integration Value: Low.** The repo's context-engineering architecture is the most mature cluster in the canonical doc library. The source's framing can serve as an entry-level narrative for the curriculum but adds no new mechanics.

---

## Pattern 15: Persona-Based Documentation

**Source:** [[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md:41-45, 99-101]]

**Classification: Missing**

**Justification:** The source describes a model where each team member documents their specialty (front-end architect, reliability engineer, security, product) as durable NFR documents, and reviewer agents load persona-specific rubrics. The repository has no persona-based documentation model. AGENTS.md is a single universal instruction file. The HoP agents have role-specific scopes but no persona-specific documentation surfaces. No reviewer agents are defined per persona dimension. The curriculum teaches NFR concepts through Sprint Contracts and Evaluation Rubrics but does not teach persona-specific documentation ownership.

**Evidence:**
- `AGENTS.md:1-50` — universal agent instructions with no persona-specific sections or role-based loading rules
- `.opencode/agents/` — HoP agents (rezek, koda-hop-init-basic, hop-live-whatsapp-tester) are role-specific but their instructions are agent-specific, not persona-based documentation surfaces that multiple agents inherit
- `.opencode/skills/review-work/SKILL.md` — review skill does second-agent review but uses generic quality criteria, not persona-specific rubrics
- `docs/canonical/multi-model-evaluation-council.md:30-47` — multiple evaluators with divergence policy, but evaluators are model-based, not persona-based (front-end, reliability, security, etc.)
- NOT_FOUND for "persona-based," "persona-specific," "role-based documentation," "NFR by persona," or "specialty owner" in `docs/canonical/`, `curriculum/05-core-concepts/`, `curriculum/02-nivel-2-practical-patterns/`, `.opencode/skills/`, or `.opencode/agents/`
- NOT_FOUND for any reviewer agent definition keyed to a specific quality dimension (front-end architecture, reliability, security, scalability) in `.opencode/`
- The concept appears only in the source analysis: `2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis.md:45` and `2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis.md:99` — not in any repo artifact

**Integration Value: High.** Persona-based documentation would multiply the repo's impact by making quality standards inheritable across all agent sessions. A canonical doc defining persona ownership, persona-specific reviewer agents, and a curriculum module on persona-based NFR writing would fill a gap that no existing pattern addresses.

---

## Pattern 16: Harness Evolution Lifecycle

**Source:** [[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis.md:203-210]]

**Classification: Better Implementation**

**Justification:** The source frames harness evolution as a general principle: harness components should be simplified or removed as models improve. The repo has formalized this into a measured lifecycle with four explicit states (BUILD, STABILIZE, SIMPLIFY, REMOVE), quarterly governance cadence, ROI measurement with concrete cost metrics (false positives, latency, token cost, infrastructure cost, maintenance hours, user outcomes), archive contract with ADR and reactivation path, and the invariant-compensation split to guide removal decisions. The repo's version is operational, measurable, and governable rather than aspirational.

**Evidence:**
- `docs/canonical/measured-harness-evolution-lifecycle.md:29-62` — full lifecycle: BUILD defensively, STABILIZE with production evidence, SIMPLIFY layer by layer, REMOVE through archived reversible removal; quarterly cadence with week 1 review, weeks 2-3 implementation, weeks 4-12 observation; One In One Out policy; per-component feature flags, 14+ day shadow tests, 5-100% canary rollouts
- `docs/canonical/measured-harness-evolution-lifecycle.md:58-60` — ROI measurement: components with ROI below 1x for two consecutive quarters become removal candidates; costs include false positives, latency, token cost, infrastructure cost, maintenance hours, and user outcomes
- `docs/canonical/measured-harness-evolution-lifecycle.md:62` — removal with causal attribution: one removal at a time, independent feature flag, shadow test, canary, 14-day observation between removals; archive with ADR, decision date, metrics, validation, post-removal result, and code under `archive/components/<nome>/`
- `docs/canonical/invariant-compensation-split.md:31-71` — complementary classification: every harness control classified as domain invariant or model-specific compensation before simplification, with decision rules and evidence requirements
- `docs/canonical/pain-signal-eval-progression-gate.md:57-60` — adjacent harness-evolution questions: what failure a component prevents, frequency, cost, replay/A-B proof, rollback speed
- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md` — Level 3 lesson covering harness evolution as models improve
- `curriculum/05-core-concepts/06-harness-evolution.md` — Core Concept 6, one of 8 foundational ideas

**Integration Value: Low.** The repo already has a more formalized, measured, and governable lifecycle. The source's framing can reinforce the curriculum narrative but adds no new mechanics beyond what already exists.

---

## Summary Table

| # | Pattern | Classification | Integration Value | Key Evidence |
|---|---|---|---|---|
| 9 | Micro-Harnesses Architecture | Partial Coverage | Medium | Custom ESLint rules exist (`eslint-rules/`) but no package-privacy or dependency-edge checks; `architecture-as-agent-affordance.md` covers principle but not executable structural checks |
| 10 | QA Plan as Agent Contract | Already Exists | Low | Sprint Contracts are Core Concept 4 with 2875-line template; reinforced by `generator-evaluator.md`, `constraint-anchored-evaluation.md`, `plan-execute-verify.md` |
| 11 | Token Budget Optimization | Better Implementation | Low | 4 canonical docs (`explicit-token-budget-ledger.md`, `burn-rate-runtime-forecast.md`, `phase-gated-token-health-monitor.md`, `budget-aware-session-handoff.md`) plus Level 1 curriculum exceed source's rule-of-thirds heuristic |
| 12 | Failure Pattern Classification Loop | Partial Coverage | High | Mechanics exist (`tested-degradation-ladder.md`, `qa-to-backlog-feedback-loop.md`, `production-failure-regression-flywheel.md`) but WEEKLY CADENCE/RITUAL is missing; no Garbage Collection Day equivalent |
| 13 | LLM as Fuzzy Compiler | Missing | Medium | Concept exists only in analysis documents; no canonical doc captures LLM-as-compiler mental model; `invariant-compensation-split.md` is adjacent but distinct |
| 14 | Harness-as-Context-Manager | Better Implementation | Low | 7+ canonical docs (`hybrid-context-stack.md`, `stable-harness-prompt.md`, `resolver-based-context-progressive-disclosure.md`, etc.) formalize layered context delivery with decision traces and budget enforcement |
| 15 | Persona-Based Documentation | Missing | High | No persona-specific documentation model; AGENTS.md is universal; no reviewer agents per quality dimension; concept exists only in source analysis |
| 16 | Harness Evolution Lifecycle | Better Implementation | Low | Full BUILD/STABILIZE/SIMPLIFY/REMOVE lifecycle with quarterly cadence, ROI measurement, archive contract, and invariant-compensation classification in `measured-harness-evolution-lifecycle.md` |
