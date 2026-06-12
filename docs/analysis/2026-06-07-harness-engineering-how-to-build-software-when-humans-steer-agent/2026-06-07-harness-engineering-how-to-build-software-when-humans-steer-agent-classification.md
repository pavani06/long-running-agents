---
title: "Unified Classification — Harness Engineering Patterns vs. long-running-agents"
type: analysis
tags: ["agentes-orquestracao", "harness", "context-engineering", "evals", "governanca"]
date: 2026-06-11
aliases: ["harness engineering classification", "unified classification", "patterns classification", "batch 1 classification", "batch 2 classification"]
last_updated: 2026-06-11
relates-to: ["[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-mental-model|Harness Engineering Mental Model]]", "[[docs/system-of-record|System of Record]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]]", "[[docs/canonical/architecture-as-agent-affordance|Architecture-as-Agent-Affordance]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/burn-rate-runtime-forecast|Burn-Rate Runtime Forecast]]", "[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]", "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]"]
sources: ["[[docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[AGENTS|AGENTS.md]]"]
---

# Unified Classification — Harness Engineering Patterns vs. long-running-agents

**Source:** `docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns.md`
**Scope:** All 16 patterns from the Harness Engineering pattern catalog
**Method:** Evidence-based classification following `docs/system-of-record.md` precedence order: decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs

---

## 1. Durable Non-Functional Requirements Memory

**Classification: Better Implementation**

The repository's `AGENTS.md` is a mature, agent-loaded durable NFR document that the pattern's source describes as the target outcome. The repo has gone further than the pattern by combining three enforcement layers: a single loaded rules document, mechanical enforcement via ESLint, and format-level enforcement via `.editorconfig`.

**Evidence:**

- `AGENTS.md:1-238` — 16 rules governing agent behavior. Rule 6 (Commit and PR Style) at lines 43-51 defines naming, format, and traceability conventions. Rule 9 (Security Constraints) at lines 77-84 encodes no-secrets, no-type-suppressions, no-empty-catch, no-eslint-disable, and side-effect approval gates. Rule 10 (Code Standards) at lines 86-90 demands following existing module patterns, small explicit testable functions, and central config/client/logger helpers. Rule 16 (Obsidian Document Conventions) at lines 120-238 is a comprehensive standard for documentation authoring.
- `eslint.config.js:1-99` — Mechanical enforcement of code standards: `no-var`, `no-unused-vars`, `prefer-const`, `eqeqeq`, `no-await-in-loop`, `preserve-caught-error`, plus custom rules `no-catch-message` and `no-raw-console-in-scripts`.
- `.editorconfig:1-10` (inferred from SOR listing) — Format-level uniformity: UTF-8, LF, indent 2 spaces.

**Comparison to pattern:** The pattern describes durable NFR documents that agents load during work. The repo already has a versioned `AGENTS.md` loaded by every agent, plus mechanical enforcement layers that catch violations without human attention. The repo's implementation is more mature because NFRs are not only documented but mechanically enforced. The pattern mentions persona-specific NFRs (product, frontend, reliability, security, architecture owners); the repo's unified `AGENTS.md` serves as the universal NFR and the HoP orchestrator agent (`hop-orchestrator-rezek.md`) provides governance-persona coordination.

**Integration value: Low** — no integration needed; the repo already exceeds the pattern.

---

## 2. Reviewer Agents as CI Gates

**Classification: Already Exists**

The repository's issue-review workflow implements a second-agent review exactly as the pattern describes: automated review of PR diffs against standards, blocking vs. advisory findings, and CI-style quality gates that run before merge. The mechanism is operational, not aspirational.

**Evidence:**

- `.opencode/skills/issue-review/SKILL.md:12-14` — "I sit between implementation and merge. I validate the worktree with HoP's real npm gates, create a draft PR targeting main, run a second-agent review on the diff, surface findings, and stop."
- `.opencode/skills/issue-review/SKILL.md:166-188` — Step 6: "Delegate a review subagent" with structured review scope covering correctness, minimal change, tests, tenant isolation, crossroad files, Supabase mock parity, logging, env vars, dashboard compliance, documentation precedence, eval-sensitive PR evidence, and security. Findings are reported as BLOCKING or ADVISORY.
- `.opencode/skills/issue-review/SKILL.md:57-85` — Eval-sensitive PR validation with baseline/candidate comparison, tier registry selection, quality/latency/cost deltas, thresholds, and merge recommendation.
- `docs/canonical/pr-gated-eval-enforcement.md:28-53` — Formalizes eval-specific PR gates: change-scope detection, required eval tiers, baseline-vs-candidate report, thresholds, waiver policy, and merge policy.
- `AGENTS.md:108-110` — Rule 13: "Significant implementation should receive a second-pass review before merge."

**Comparison to pattern:** The pattern asks for automated review findings focused on merge-blocking issues, pass/fail/acknowledge/defer/reject signals, and CI-visible quality gates. The repo's second-agent review covers all of these: structured review scope, BLOCKING/ADVISORY classification, CI validation gates, and explicit merge policy with waiver. The PR-Gated Eval Enforcement doc extends this further for eval-sensitive changes.

**Integration value: Low** — already fully implemented.

---

## 3. Garbage Collection Day Meta-Loop

**Classification: Partial Coverage**

The repository has strong mechanisms that align with parts of the pattern — converting review feedback into backlog items, evolving harness through measured lifecycle, and using pain signals to drive improvements. But the specific "weekly cadence where human review feedback gets systematically converted into automated harness guardrails (lint rules, skills, reviewer prompts, tests)" is not formalized as a recurring meta-loop.

**Evidence of existing pieces:**

- `docs/canonical/qa-to-backlog-feedback-loop.md:30-44` — Converts QA/review findings into backlog issues through capture, triage, convert, and return-to-board stages. This is the closest mechanism: findings become backlog work. But the output is issues, not automated harness guardrails.
- `docs/canonical/measured-harness-evolution-lifecycle.md:29-62` — BUILD → STABILIZE → SIMPLIFY → REMOVE lifecycle with quarterly cadence, ROI threshold, One In One Out rule. This is harness evolution, but the cadence is quarterly (not weekly) and the trigger is usage metrics, not review feedback.
- `docs/canonical/pain-signal-eval-progression-gate.md:28-51` — Maps pain signals (user complaints, manual review bottlenecks, escaped edge cases) to minimum eval investments. This converts observations into harness improvements, but is scoped to eval capability, not general harness guardrails.
- `docs/canonical/production-failure-regression-flywheel.md:28-40` (referenced by SOR) — Converts production failures into durable regression cases.
- `docs/canonical/invariant-compensation-split.md:31-50` — Classifies harness components before simplification or removal.

**What is missing:**

- No explicit weekly cadence for converting review feedback into automated guardrails.
- No categorization rubric for slop patterns observed during review (the pattern's specific mechanic).
- No documented pipeline from "human reviewer noticed recurring pattern X" to "new lint rule, skill update, or reviewer-prompt amendment was deployed."
- The `qa-to-backlog-feedback-loop.md` itself notes this gap: findings become backlog issues, not automated harness behavior (`docs/canonical/qa-to-backlog-feedback-loop.md:57-59`).

**Searched:** `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `AGENTS.md` — no weekly harness cleanup meta-loop found. The `remove-ai-slops` built-in skill is closest but is a reactive tool, not a recurring meta-loop.

**Integration value: High** — the repo has all the component mechanisms (QA-to-backlog, harness evolution, pain-signal progression, production flywheel) but lacks the connecting meta-loop that turns recurring review observations into automated guardrails on a weekly cadence.

---

## 4. Prompt Injection Taxonomy

**Classification: Partial Coverage**

The repository has extensive context-delivery surfaces (skills with triggers, lint rules, test failures, review comments, AGENTS.md) and a formal resolver-based disclosure system. But it lacks an explicit taxonomy or map that classifies these surfaces and provides placement guidance for new instructions.

**Evidence of existing pieces:**

- `docs/canonical/resolver-based-context-progressive-disclosure.md:28-39` — Defines thin base context, capability directory, positive triggers, negative triggers, and trigger evals. This is a resolver-driven surface map, but focused on skill loading, not a complete injection surface taxonomy.
- `docs/canonical/hybrid-context-stack.md:30-43` — Defines a 7-layer context assembly policy with budgeted inclusion order. This is a structured surface for context injection, but within a single model call, not across the full agent trajectory.
- `.opencode/skills/issue-review/SKILL.md:166-188` — Review as an injection surface: the second-agent review injects blocking/advisory findings that the implementer must address.
- `eslint.config.js:1-99` — Lint as an injection surface: mechanical rules inject corrective feedback during validation.
- `AGENTS.md:1-238` — Base prompt as injection surface: 16 rules loaded on every agent session.
- `.opencode/skills/` directory — Skills as injection surfaces: each skill has triggers that determine when guidance is loaded.

**What is missing:**

- No explicit taxonomy classifying all injection surfaces (initial prompt, AGENTS.md, lint rules, test failures, review comments, skills, rules files, CI gates) with their phase of appearance and guidance placement rules.
- No documented decision framework for "this new rule belongs in AGENTS.md vs. a lint rule vs. a skill vs. review scope."
- No surface coordination rule to prevent instruction contradictions across surfaces.

**Searched:** `docs/canonical/`, `docs/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis/`, `curriculum/`, `.opencode/` — no explicit "injection surface map" or "instruction surface taxonomy" found. The closest is `resolver-based-context-progressive-disclosure.md` which handles skill-level routing but not cross-surface taxonomy.

**Integration value: Medium** — the repo has all the surfaces; the taxonomy would make placement decisions systematic rather than ad hoc. The resolver-based disclosure and hybrid context stack already do the heavy lifting.

---

## 5. Just-in-Time Context Surfacing

**Classification: Partial Coverage**

The repository implements skill-level JIT context loading through resolver-based progressive disclosure, and the issue-review skill injects context at validation/review time rather than upfront. But the pattern's full mechanic — surfacing guidance at lint, test, review, and repair time as a deliberate strategy to conserve initial context — is not formalized as a named pattern.

**Evidence of existing pieces:**

- `docs/canonical/resolver-based-context-progressive-disclosure.md:28-39` — Skills are loaded on-demand based on task triggers, not front-loaded. This is the core JIT mechanic at the skill level.
- `.opencode/skills/issue-review/SKILL.md:38-40` — Context compaction is required before CI/PR creation: "Run `/compact` before CI and PR creation on non-trivial work. Enter review with a clean context focused on the diff and validation output."
- `.opencode/skills/issue-review/SKILL.md:57-85` — Eval-sensitive surface guidance is injected at review time, not during implementation. The implementer builds first; the reviewer surfaces quality constraints afterward.
- `eslint.config.js:1-99` — Lint failures inject corrective guidance at the moment of violation, not in the initial prompt.
- `AGENTS.md:96-106` — Rule 12 (Search Before You Code) tells agents to read docs before editing, deferring context loading to when it is needed.

**What is missing:**

- No explicit "Just-in-Time Context Surfacing" as a named strategy or canonical doc.
- No formal trigger mapping: "this constraint surfaces at lint time, that one at review time."
- No policy for which guidance should be front-loaded vs. JIT-surfaced.
- The resolver disclosure is skill-level; the lint/test/review surface as context delivery is not formalized as part of the JIT strategy.

**Searched:** `docs/canonical/`, `AGENTS.md`, `.opencode/skills/` — no named JIT context surfacing pattern found. The resolver disclosure and issue-review compaction are the operational implementations.

**Integration value: Medium** — the mechanics exist operationally (resolver loading, review-time injection, lint-as-feedback) but formalizing them as a deliberate JIT strategy would make the design intent explicit and prevent future prompt bloat.

---

## 6. Deep Skills Strategy

**Classification: Partial Coverage**

The repository has a comprehensive canonical definition of the skillify pipeline, operational skills for the full issue lifecycle, and a knowledge-to-improvement pipeline via `analyze-and-improve`. But the canonical itself classifies the implementation as Partial Coverage, and the resolver metadata, trigger evals, smoke tests, and storage schema are documented as missing.

**Evidence of existing pieces:**

- `docs/canonical/skill-resolver-skillify-capability-pipeline.md:28-41` — Defines the full 7-stage pipeline: workflow capture, skill authoring, resolver registration, compliance tests, resolvability check, smoke execution, and storage schema.
- `.opencode/skills/` directory — Operational skills: `issue-start`, `issue-review`, `issue-finish`, `issue-workflow`, `refine-issue`, `orchestrator`, `doc-coauthoring`, `writing-plans`, `error-context-hygiene`, `analyze-and-improve`. These are deep skills that hide complex workflows behind stable interfaces.
- `.opencode/skills/error-context-hygiene/SKILL.md:15-20` — Example of a focused operational skill with explicit behavioral rules.
- `.opencode/skills/analyze-and-improve/SKILL.md:46-56` — Knowledge-to-improvement pipeline with concrete artifact slots.
- `docs/canonical/resolver-based-context-progressive-disclosure.md:28-39` — Provides the resolver contract that deep skills depend on.

**What is missing (per the canonical's own classification):**

- Resolver metadata schema for every reusable skill (`docs/canonical/skill-resolver-skillify-capability-pipeline.md:61`).
- Trigger evals that test whether realistic tasks load the right skill (`docs/canonical/skill-resolver-skillify-capability-pipeline.md:62`).
- A `check-resolvable` gate for discoverability and deduplication (`docs/canonical/skill-resolver-skillify-capability-pipeline.md:63`).
- Smoke tests proving fresh sessions can use skills without hidden author context (`docs/canonical/skill-resolver-skillify-capability-pipeline.md:64`).
- Storage schema for skill outputs and runtime state (`docs/canonical/skill-resolver-skillify-capability-pipeline.md:65`).

**Comparison to pattern:** The pattern describes 5-10 deep skills that hide infrastructure complexity behind stable interfaces. The repo has more than 10 operational skills, and the canonical pipeline already defines the formal promotion path from workflow to routable skill. The gap is in the pipeline's quality gates (trigger evals, smoke tests, dedup), not in the strategy or skill count.

**Integration value: Medium** — the strategy and skills exist; the missing pieces are quality gates that would make the pipeline auditable.

---

## 7. Codebase Uniformity as Agent Affordance

**Classification: Partial Coverage**

The repository has a dedicated canonical doc that explicitly names architecture as agent affordance, plus AGENTS.md rules and planning-review mechanics that enforce uniformity. But the canonical itself is classified as Partial Coverage because it lacks a concrete playbook, rubric, and follow-up issue pattern for architecture-as-affordance work.

**Evidence of existing pieces:**

- `docs/canonical/architecture-as-agent-affordance.md:30-42` — Defines three architectural moves as agent affordances: deep modules with simple interfaces, boundary tests at behavior-level targets, and reduced coupling to limit blast radius. Explicitly states: "A deep module with a simple public interface and behavior-level boundary tests is not only better human design; it is more navigable terrain for the next agent."
- `AGENTS.md:86-90` — Rule 10: "Follow existing module patterns before introducing new ones. Keep scripts and library functions small, explicit, and testable. Use central config/client/logger helpers instead of scattering direct environment or logging behavior."
- `.opencode/skills/writing-plans/SKILL.md:22-29` (referenced in canonical) — Maps files, responsibilities, boundaries, and interfaces before defining implementation tasks.
- `docs/canonical/split-brain-planning-review.md:30-41` (referenced in canonical) — Evaluates scope, dependencies, and risk during planning review.
- `eslint.config.js:1-99` — Enforces some uniformity mechanically: `no-var`, `prefer-const`, `eqeqeq`, consistent module patterns.

**What is missing (per the canonical's own classification):**

- No canonical refactoring playbook that identifies dependency clusters as agent-navigation costs (`docs/canonical/architecture-as-agent-affordance.md:60`).
- No rubric for evaluating module boundaries through the lens of future agent sessions (`docs/canonical/architecture-as-agent-affordance.md:61`).
- No pattern for architecture-follow-up issues that persist on the backlog (`docs/canonical/architecture-as-agent-affordance.md:62`).
- No concrete definition of "deep module" and "simple public interface" as measurable properties (`docs/canonical/architecture-as-agent-affordance.md:64`).

**Comparison to pattern:** The repo has the concept fully defined and partially implemented. The pattern asks for "one canonical way to perform common operations" and "predictable file, package, dependency, and helper patterns." The repo achieves this through AGENTS.md rules, eslint enforcement, and planning-review mechanics, but the canonical itself acknowledges that the refactoring playbook and agent-navigation rubric are missing.

**Integration value: Medium** — the canonical doc exists and the mechanics are partially in place; the missing pieces would make architecture-as-affordance actionable rather than aspirational.

---

## 8. PR as Hub-and-Spoke Broadcast Domain

**Classification: Already Exists**

The repository's issue lifecycle is built around the PR as the central collaboration surface. The issue-review workflow creates a draft PR that collects validation output, second-agent review findings, eval-impact evidence, and crossroad-file impact in one place. The human confirms on the PR. Multiple spokes (implementer, reviewer, CI, human) converge on the same surface.

**Evidence:**

- `.opencode/skills/issue-review/SKILL.md:12-14` — "I sit between implementation and merge. I validate the worktree, create a draft PR targeting main, run a second-agent review on the diff, surface findings, and stop."
- `.opencode/skills/issue-review/SKILL.md:102-153` — Step 4: Creates a draft PR with PR body template including summary, changes, tests, Eval impact section, and Crossroad-file impact section. The PR body is the structured broadcast surface.
- `.opencode/skills/issue-review/SKILL.md:166-188` — Step 6: Second-agent review findings are attached to the PR via the review subagent.
- `.opencode/skills/issue-review/SKILL.md:200-226` — Step 7: All findings (BLOCKING/ADVISORY) are surfaced on the PR. Human confirmation is required before merge. "Do not merge. Wait for explicit user confirmation."
- `.github/PULL_REQUEST_TEMPLATE.md:1-89` — Structured PR body with Eval impact section (baseline/candidate versions, tier execution, quality/latency/cost deltas, failures, waiver) and Crossroad-file impact section (affected files, change type, migration note, reviewer checklist).
- `.opencode/skills/issue-workflow/SKILL.md:12-32` — Issue-level progress updates, handoff comments, and completion comments create durable collaboration records on the issue.
- `.opencode/skills/issue-finish/SKILL.md:12-14` — Merge and cleanup only after explicit approval on the PR.

**Comparison to pattern:** The pattern describes "a shared collaboration surface for implementers, reviewers, CI, and humans" with "visible decisions and feedback threads tied to the code change." The repo's PR workflow implements exactly this: the PR is the hub where the implementer's diff, CI validation output, second-agent review findings, eval-impact evidence, crossroad-file impact, and human merge decision all converge. The pattern also mentions "merge or follow-up decisions without requiring synchronous review from every participant" — the repo's draft PR + second-agent review + human confirmation flow achieves this asynchronous convergence.

**Integration value: Low** — already fully implemented.

---

## 9. Micro-Harnesses Architecture

**Classification: Partial Coverage**

**Justification:** The repository has the foundation for structural checks via custom ESLint rules, but these operate at syntax/behavior level, not at the architectural structure level the source describes. The source defines micro-harnesses as structural checks that assert code organization (package privacy, dependency direction, schema ownership, canonical helpers) rather than user behavior. The repo's closest equivalents are its two custom ESLint rules, but neither enforces package privacy or dependency edges between layers. The `architecture-as-agent-affordance.md` canonical doc covers the general principle of architecture as navigable terrain but does not define executable structural checks.

**Evidence:**

- `eslint-rules/no-catch-message.js:1-172` — custom ESLint rule that prevents `.message` access on catch-bound errors; this is a syntax-level guard, not an architectural structure check
- `eslint-rules/no-raw-console-in-scripts.js:1-133` — custom ESLint rule that enforces use of safe-console helpers; this enforces a canonical helper pattern, which is the closest existing mechanic to "canonical implementation guard" from the source
- `eslint.config.js:12-13` — imports and applies both custom rules, but contains no `import/no-restricted-paths`, `import/no-internal-modules`, or dependency-direction rules
- `docs/canonical/architecture-as-agent-affordance.md:29-38` — defines deep modules, boundary tests, and reduced coupling as agent affordances, but this is architectural guidance, not executable structural checks
- NOT_FOUND for dependency-edge checks, package-privacy enforcement, or schema-ownership assertions in `eslint.config.js`, `eslint-rules/`, `scripts/`, or `package.json`
- NOT_FOUND for any test that asserts code organization against architectural rules in `tests/`

**Integration value: Medium.** The ESLint infrastructure exists and could host structural rules. The repo currently has minimal source code, limiting immediate applicability, but as the codebase grows, package-privacy and dependency-edge checks would prevent agent-local coherence drift.

---

## 10. QA Plan as Agent Contract

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

**Integration value: Low.** The repo already has a more mature implementation. The Sprint Contract concept is foundational to the curriculum and reinforced by multiple canonical docs. No integration needed beyond noting the alignment.

---

## 11. Token Budget Optimization

**Classification: Better Implementation**

**Justification:** The source presents a rough heuristic ("~1/3 planning, ~1/3 implementation, ~1/3 CI"). The repo has formalized token budgeting into a multi-layered canonical architecture with explicit ledger schema, runtime burn-rate forecasting, phase-gated health monitoring, and budget-aware session handoff. Four canonical docs plus the Level 1 curriculum lesson exceed the source's maturity by providing measurable, auditable, and proactive token governance rather than a post-hoc allocation guideline.

**Evidence:**

- `docs/canonical/explicit-token-budget-ledger.md:30-59` — per-call ledger with 9 canonical fields: model context window, fixed prompt cost, tool schema cost, durable state cost, accumulated context cost, planned input cost, response buffer, safety buffer, remaining budget, and budget percentage
- `docs/canonical/burn-rate-runtime-forecast.md:31-56` — runtime token consumption forecasting with velocity, acceleration, runway estimation, and intervention mapping
- `docs/canonical/phase-gated-token-health-monitor.md:31-60` — operational health phases (green/yellow/orange/red) driven by remaining budget percentage and burn-rate acceleration
- `docs/canonical/budget-aware-session-handoff.md:26-45` — session handoff triggered by token health with fresh-session payload construction
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:34-62` — foundation lesson defining token budgeting as planning, allocating, and controlling token use; includes budget equation, burn-rate formula, and viability calculator
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:428-566` — conversation viability calculator with reserves, remaining budget estimation, remaining messages, and KODA phase scenarios

**Integration value: Low.** The repo's token budget architecture is significantly more mature than the source. No integration needed; the source's "rule of thirds" could be referenced as a practical rule of thumb in the curriculum.

---

## 12. Failure Pattern Classification Loop

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

**Integration value: High.** Adding a weekly GC ritual as a curriculum exercise or skill would close the loop between the existing mechanical infrastructure (degradation ladder, flywheel, QA-to-backlog) and the human observation-to-automation cycle. This is the highest-leverage missing piece in batch 2.

---

## 13. LLM as Fuzzy Compiler

**Classification: Missing**

**Justification:** The concept of "LLM as fuzzy compiler, harness as optimization passes, code as disposable build artifact" does not exist in any canonical doc, curriculum lesson, or skill in the repository. The mental model appears only in the Harness Engineering analysis documents themselves. Adjacent canonical docs cover related but distinct concepts: `invariant-compensation-split.md` classifies harness controls by domain risk vs. model weakness (not compiler passes), and `measured-harness-evolution-lifecycle.md` governs component lifecycle (not code-as-artifact). The patterns.md pattern "Durable Harness Asset Preservation" captures the "preserve prompts/guardrails, not code" idea but has no corresponding canonical doc.

**Evidence:**

- `docs/canonical/invariant-compensation-split.md:31-60` — classifies harness controls as domain invariants vs. model-specific compensations; this is the closest canonical doc but addresses harness component governance, not the LLM-as-compiler mental model
- `docs/canonical/measured-harness-evolution-lifecycle.md:29-62` — governs component lifecycle through BUILD/STABILIZE/SIMPLIFY/REMOVE; related to model improvement triggering harness changes, but does not frame the LLM as a compiler backend
- NOT_FOUND for "LLM as compiler," "fuzzy compiler," "compilation target," or "code as build artifact" in `docs/canonical/`, `curriculum/`, `docs/decisions/`, `.opencode/skills/`, or `.opencode/agents/`
- NOT_FOUND for "code is disposable," "replaceable output," or "generated code as artifact" in `docs/canonical/`, `curriculum/05-core-concepts/`, or `curriculum/README.md`
- The concept exists in analysis documents only: `2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns.md:367` and `2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis.md:61-63, 208` — these are the source material being classified, not evidence of repo coverage

**Integration value: Medium.** The LLM-as-compiler mental model is a powerful reframe that would add pedagogical value to the curriculum and connect the existing `invariant-compensation-split.md` and `measured-harness-evolution-lifecycle.md` into a coherent narrative. It does not require new code or infrastructure — it is a conceptual lens.

---

## 14. Harness-as-Context-Manager

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

**Integration value: Low.** The repo's context-engineering architecture is the most mature cluster in the canonical doc library. The source's framing can serve as an entry-level narrative for the curriculum but adds no new mechanics.

---

## 15. Persona-Based Documentation

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

**Integration value: High.** Persona-based documentation would multiply the repo's impact by making quality standards inheritable across all agent sessions. A canonical doc defining persona ownership, persona-specific reviewer agents, and a curriculum module on persona-based NFR writing would fill a gap that no existing pattern addresses.

---

## 16. Harness Evolution Lifecycle

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

**Integration value: Low.** The repo already has a more formalized, measured, and governable lifecycle. The source's framing can reinforce the curriculum narrative but adds no new mechanics beyond what already exists.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Durable Non-Functional Requirements Memory | Better Implementation | Low |
| 2 | Reviewer Agents as CI Gates | Already Exists | Low |
| 3 | Garbage Collection Day Meta-Loop | Partial Coverage | High |
| 4 | Prompt Injection Taxonomy | Partial Coverage | Medium |
| 5 | Just-in-Time Context Surfacing | Partial Coverage | Medium |
| 6 | Deep Skills Strategy | Partial Coverage | Medium |
| 7 | Codebase Uniformity as Agent Affordance | Partial Coverage | Medium |
| 8 | PR as Hub-and-Spoke Broadcast Domain | Already Exists | Low |
| 9 | Micro-Harnesses Architecture | Partial Coverage | Medium |
| 10 | QA Plan as Agent Contract | Already Exists | Low |
| 11 | Token Budget Optimization | Better Implementation | Low |
| 12 | Failure Pattern Classification Loop | Partial Coverage | High |
| 13 | LLM as Fuzzy Compiler | Missing | Medium |
| 14 | Harness-as-Context-Manager | Better Implementation | Low |
| 15 | Persona-Based Documentation | Missing | High |
| 16 | Harness Evolution Lifecycle | Better Implementation | Low |

---

## Distribution

- **Better Implementation:** 4 (Patterns 1, 11, 14, 16)
- **Already Exists:** 3 (Patterns 2, 8, 10)
- **Partial Coverage:** 7 (Patterns 3, 4, 5, 6, 7, 9, 12)
- **Missing:** 2 (Patterns 13, 15)
- **Total:** 16

---

## Synthesis: Cross-Batch Patterns Observed

### 1. Operational patterns consistently exceed the source

The repo's strengths cluster in three domains where it has already built more mature implementations than the Harness Engineering source describes:

- **Context engineering** (Patterns 4, 5, 14): The hybrid context stack, resolver-based disclosure, stable harness prompts, head-tail truncation, addressable memory catalog, external state persistence, and budget-aware session handoff form a comprehensive architecture that directly implements the source's core thesis of "give the model text at the right time."
- **Governance and lifecycle** (Patterns 1, 11, 16): AGENTS.md with mechanical enforcement (ESLint, .editorconfig), the token budget ledger with burn-rate forecasting and phase-gated health monitoring, and the measured harness evolution lifecycle with BUILD/STABILIZE/SIMPLIFY/REMOVE states all exceed the source's maturity by providing measurable, auditable, and mechanically enforced governance.
- **Collaboration surfaces** (Patterns 2, 8, 10): The PR-as-hub workflow with second-agent review, eval-gated enforcement, and the Sprint Contract as formal Generator-Evaluator agreement are operational and foundational to the repo's issue lifecycle.

### 2. The weekly cadence gap is the single most impactful missing piece

Two patterns from different batches point to the identical missing mechanism:

- Pattern 3 (Garbage Collection Day Meta-Loop) and Pattern 12 (Failure Pattern Classification Loop) both describe a weekly ritual where human observations of recurring failure patterns are systematically converted into automated harness guardrails.

The repo has all the mechanical infrastructure for this — QA-to-backlog feedback loop, tested degradation ladder, production failure regression flywheel, pain-signal eval progression gate — but lacks the weekly cadenced ritual that connects human observation to harness automation. Closing this gap would be the highest-leverage single improvement (both marked "High" integration value).

### 3. Conceptual patterns are the repo's blind spot

Patterns 13 (LLM as Fuzzy Compiler) and 15 (Persona-Based Documentation) are classified as Missing. Both are conceptual models rather than mechanical implementations:

- **LLM as Fuzzy Compiler** reframes the entire agent workflow as compilation passes, which would connect the existing `invariant-compensation-split.md` and `measured-harness-evolution-lifecycle.md` into a coherent pedagogical narrative. It requires no new infrastructure.
- **Persona-Based Documentation** would extend the repo's single universal AGENTS.md into persona-specific NFR documents with role-based reviewer agents, multiplying the leverage of quality standards across all agent sessions.

These conceptual patterns are lower cost to integrate (they require documentation and curriculum, not code) but would significantly amplify the repo's pedagogical value.

### 4. Partial Coverage patterns share a common theme: formalization debt

Seven patterns (3, 4, 5, 6, 7, 9, 12) are classified as Partial Coverage. They share a common characteristic: the repo has the operational mechanics but lacks explicit formalization:

- Mechanics exist but are unnamed (Patterns 3, 5, 12)
- Concepts are defined but quality gates are missing (Patterns 6, 7)
- Surfaces exist but taxonomy is absent (Pattern 4)
- Infrastructure exists but structural rules are missing (Pattern 9)

In every case, the gap is not in capability but in formalization — naming the pattern, defining the quality gates, building the taxonomy, or adding the structural rules that would make the existing mechanics systematic rather than emergent.

### 5. The repo's context-engineering architecture is its strongest differentiated asset

Directly or indirectly, 8 of 16 patterns connect to context engineering: Durable NFR Memory (1), Prompt Injection Taxonomy (4), JIT Context Surfacing (5), Deep Skills Strategy (6), LLM as Fuzzy Compiler (13), Harness-as-Context-Manager (14), plus the token budget patterns that govern context allocation (11), and the harness evolution lifecycle that governs context component lifecycle (16). This cluster is the repo's most mature and distinctive contribution — it has formalized context delivery, budget enforcement, and lifecycle governance into a coherent, layered architecture with 7+ canonical docs that work together.
