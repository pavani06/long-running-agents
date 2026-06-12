---
title: "Classification Batch 1 — Harness Engineering Patterns vs. long-running-agents"
type: analysis
tags: ["agentes-orquestracao", "harness", "context-engineering", "evals", "governanca"]
date: 2026-06-11
aliases: ["harness engineering classification batch 1", "batch 1 classification"]
last_updated: 2026-06-11
relates-to: ["[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-mental-model|Harness Engineering Mental Model]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/system-of-record|System of Record]]"]
sources: ["[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[AGENTS|AGENTS.md]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]]", "[[docs/canonical/architecture-as-agent-affordance|Architecture-as-Agent-Affordance]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"]
---

# Classification Batch 1 — Harness Engineering Patterns vs. long-running-agents

**Source:** `docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns.md`
**Scope:** Patterns 1-8 from the 16-pattern catalog
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

## Summary Table

| # | Pattern | Classification | Integration Value | Key Evidence |
|---|---|---|---|---|
| 1 | Durable Non-Functional Requirements Memory | Better Implementation | Low | `AGENTS.md:1-238`, `eslint.config.js:1-99`, `.editorconfig` |
| 2 | Reviewer Agents as CI Gates | Already Exists | Low | `.opencode/skills/issue-review/SKILL.md:166-188`, `pr-gated-eval-enforcement.md:28-53` |
| 3 | Garbage Collection Day Meta-Loop | Partial Coverage | High | `qa-to-backlog-feedback-loop.md:30-44`, `measured-harness-evolution-lifecycle.md:29-62`, `pain-signal-eval-progression-gate.md:28-51` |
| 4 | Prompt Injection Taxonomy | Partial Coverage | Medium | `resolver-based-context-progressive-disclosure.md:28-39`, `hybrid-context-stack.md:30-43` |
| 5 | Just-in-Time Context Surfacing | Partial Coverage | Medium | `resolver-based-context-progressive-disclosure.md:28-39`, `.opencode/skills/issue-review/SKILL.md:38-40` |
| 6 | Deep Skills Strategy | Partial Coverage | Medium | `skill-resolver-skillify-capability-pipeline.md:28-41`, `.opencode/skills/` directory |
| 7 | Codebase Uniformity as Agent Affordance | Partial Coverage | Medium | `architecture-as-agent-affordance.md:30-42`, `AGENTS.md:86-90` |
| 8 | PR as Hub-and-Spoke Broadcast Domain | Already Exists | Low | `.opencode/skills/issue-review/SKILL.md:102-226`, `.github/PULL_REQUEST_TEMPLATE.md:1-89` |

---

## Distribution

- **Better Implementation:** 1 (Pattern 1)
- **Already Exists:** 3 (Patterns 2, 8)
- **Partial Coverage:** 5 (Patterns 3, 4, 5, 6, 7)
- **Missing:** 0
- **Total:** 8

The repo has strong coverage of the operational patterns (NFR memory, reviewer gates, PR hub) and has partially covered the systemic patterns (GC loop, injection taxonomy, JIT surfacing, deep skills, codebase uniformity) through canonical docs that define the concepts but leave quality gates and formal pipelines as remaining work.
