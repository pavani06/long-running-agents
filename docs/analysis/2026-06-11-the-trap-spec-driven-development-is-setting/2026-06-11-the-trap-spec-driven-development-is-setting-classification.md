---
title: "Comparative Classification: The Trap SDD Patterns vs. long-running-agents Repo"
type: analysis
date: 2026-06-11
aliases: ["classificacao SDD trap", "SDD gap analysis", "mapeamento padroes SDD", "trap classification"]
tags: ["agentes-orquestracao", "agentic-coding", "spec-driven-development", "decision-discipline", "harness-engineering", "governanca"]
relates-to: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|SDD Trap Analysis]]"]
---

# Comparative Classification: SDD Trap Patterns vs. long-running-agents Repo

**Date:** 2026-06-11
**Repo analyzed:** `pavani06/long-running-agents`
**Patterns source:** "The Trap Spec-Driven Development Is Setting" (2026-06-11)
**Evidence basis:** `docs/canonical/`, `.opencode/skills/`, `.opencode/agents/`, `curriculum/`, `docs/system-of-record.md`, `AGENTS.md`
**Precedence order:** decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs

---

## Classification Legend

| Class | Meaning |
|---|---|
| Already Exists | Pattern is documented, implemented, or taught with equivalent depth |
| Partial Coverage | Elements exist but missing key mechanics, reframe, or formalization |
| Missing | Not present in any form (doc, code, or curriculum) |
| Better Implementation | Repo has a superior or more mature version of the same idea |

---

## 1. Value-Gated Agent Control Loop

**Classification:** Partial Coverage

**Why:**
The repo governs HOW agents execute (context, dispatch, evaluation) but does not formalize a value gate that governs WHETHER the agent should build at all.

**What exists:**

- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 defines a structured pre-planning interview that asks value and scope questions before execution, with a decision/deferral ledger. This is the closest mechanism: it interrogates intent before building.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:30-52 classifies tasks on ambiguity, architecture, feedback-loop readiness, and product judgment before allowing autonomous execution. This creates a pre-execution filter.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75 defines loop intervention points: break, summarize, LM-as-judge, human approval gate, force terminate. These are execution-quality controls, not value decisions.
- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:29-64 unifies prompt, context, dispatch, and loop policy with gates, but all gates govern execution quality, not value judgment.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:28-37 connects state intake, priority synthesis, execution routing, and feedback writeback, but routes work rather than gating by value.

**What is missing:**
The specific decision vocabulary of the pattern -- build, experiment, defer, or stop -- attached to intent statements and scope constraints before execution. The Alignment Interview asks about intent but doesn't produce a build/experiment/defer/stop classification. The AFK Routing Gate classifies task readiness, not task value. No canonical doc formalizes a value-gating decision point in the agent control loop.

The source analysis itself names this gap: "O harness nao deve apenas governar COMO o agente constroi (contexto, dispatch, avaliacao) -- deve tambem governar SE o agente deve construir" (`2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:175`).

**Integration value:** High. The repo has the pre-execution infrastructure (alignment interview, routing gate) but lacks the value-decision vocabulary. Adding a value gate would close the loop named by the source analysis itself.

---

## 2. Manual Brake Question Gate

**Classification:** Missing

**Why:**
The three specific diagnostic questions ("Who needs this, and what breaks?", "Would we still build it if it cost a week of engineering time?", "Who owns saying no to this?") are not present in any repo document, skill, or curriculum.

**Searched locations (NOT_FOUND):**
- `docs/canonical/grill-me-alignment-interview.md` -- asks alignment questions but not these three brake questions; focuses on architecture, scope, and product decisions rather than cost proxies and refusal ownership
- `docs/canonical/human-afk-task-routing-gate.md` -- classifies by ambiguity/architecture/feedback/product, not by value/cost/ownership
- `docs/canonical/split-brain-planning-review.md` -- reviews plans with dual rubrics but doesn't include cost-proxy or refusal-owner questions
- `.opencode/skills/issue-start/SKILL.md` -- creates execution brief with objective, success criteria, scope, out-of-scope; related discipline but not the brake questions
- `.opencode/agents/` -- Hop agents (orchestrator, KODA init, live tester) have defined scopes but no refusal-owner role
- `curriculum/` -- no lesson on brake questions or cost-proxy evaluation; Core Concept 7 (Multi-Agent Coordination) covers decision ownership generically but not refusal ownership

**What exists nearby:**
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-35 asks one-question-at-a-time to expose hidden constraints and record decisions -- structurally similar, different questions.
- [[.opencode/skills/issue-start/SKILL.md|issue-start skill]]:111-147 creates an execution brief with "objective, success criteria, scope, out-of-scope" -- a build contract without the cost/refusal dimension.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:32-37 routes tasks to AFK or human-in-loop -- classification without the brake questions.

**Integration value:** High. These three questions are lightweight, immediately usable, and address the gap the source analysis names: no mechanism forces the value question before building.

---

## 3. Intent-First Spec Loop

**Classification:** Better Implementation

**Why:**
The repo has a fully documented, multi-layer intent-first pipeline that exceeds the pattern's description. The alignment interview collects intents, the shared concept preserves them as the primary asset, and downstream PRDs/issues are derived from intents rather than the other way around.

**Evidence:**

- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 runs a structured one-question-at-a-time interview to expose hidden constraints, architectural assumptions, and product decisions before any planning or coding. Produces a decision/deferral ledger with rationale.
- [[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]]:30-48 formalizes the alignment output as a durable handoff artifact: "The shared concept is the primary asset; the PRD is a downstream summarization. This reverses the common spec-driven instinct: the workflow trusts the PRD because alignment happened before it" (`shared-design-concept-handoff.md:40`).
- The handoff contract captures human product judgment, agent interpretation, decision trail, assumption summary (confirmed vs. deferred), and downstream PRD/issue generation rules (`shared-design-concept-handoff.md:32-38`).
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-56 implements the three-phase separation starting from a plan derived from intent: "Plan produces atomic steps with per-step success criteria" before execution and verification begin.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:30-52 consumes the alignment output to determine whether tasks are AFK-ready: "the handoff clarity determines whether tasks are ready for AFK execution" (`human-afk-task-routing-gate.md:91`).
- The entire flow runs Grill-Me → Shared Design Concept → PRD/Issue → Plan → Execute → Verify, with each stage preserving intent traceability.

**Why Better Implementation:**
The source analysis mentions IDSD (Intent-Driven Software Development) as a brief framework reference (`2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:50-52`) with the sequence "Gather Intents → Create Specs → Let the framework do the rest." The repo not only implements this sequence but formalizes each stage as a canonical pattern with documented components, flow, tradeoffs, and integration points. The repo's version adds the decision/deferral ledger, assumption classification (confirmed vs. deferred), and trust boundaries that downstream artifacts must not override -- elements the source analysis doesn't describe.

**Integration value:** Low -- repo already exceeds the pattern's maturity.

---

## 4. Continue Decision Checkpoint

**Classification:** Partial Coverage

**Why:**
The repo has loop controls and lifecycle decisions but does not formalize the experiment-boundary checkpoint where the dangerous verb is Continue rather than Build.

**What exists:**

- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75 defines explicit loop intervention points: break (stop iteration after N steps or when confidence is low), summarize, LM-as-judge, human approval gate, and force terminate. These are execution-quality controls at the loop level.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:29-62 defines a quarterly lifecycle with BUILD/STABILIZE/SIMPLIFY/REMOVE states, ROI thresholds, and the rule "A component with ROI below 1x for two consecutive quarters becomes a removal candidate" (`measured-harness-evolution-lifecycle.md:58`). This is a continue/remove checkpoint for harness components.
- [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]:31-55 has a weekly cadence for reviewing observations and building guardrails -- a regular review checkpoint, not an experiment-boundary decision.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:32-35 includes feedback writeback for decisions, and the orchestrator routes execution.

**What is missing:**
The specific experiment-boundary checkpoint: stop criteria defined before the experiment continues, with Continue/pivot/stop/archive as the explicit decision vocabulary at iteration boundaries. The source's key insight is that "the verb that creates the problem is not Build -- it's Continue" (`2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:76`). The repo's loop controls (break, terminate) are about execution safety, not about the experiment-continuation decision. The harness evolution lifecycle has removal decisions but operates on a quarterly cadence for components, not on experiment iterations.

**Integration value:** Medium. The repo has all the structural pieces (loop controls, lifecycle decisions, review cadences) but lacks the specific decision vocabulary and placement at the experiment boundary. Adding a Continue Decision Checkpoint would close the gap between execution safety and experiment economics.

---

## 5. Owner-of-No Role

**Classification:** Missing

**Why:**
No agent, skill, canonical doc, or curriculum material defines a named role whose explicit job is to refuse low-value work.

**Searched locations (NOT_FOUND):**
- `.opencode/agents/hop-orchestrator-rezek.md` -- coordinates governance and role activation; does not have refusal authority
- `.opencode/agents/koda-hop-init-basic.md` -- subagente de inicial guiada; no refusal role
- `.opencode/agents/hop-live-whatsapp-tester.md` -- tester agent; no refusal role
- `.opencode/skills/orchestrator/SKILL.md` -- suggests next tasks and priorities; routes work, does not refuse it
- `.opencode/skills/issue-review/SKILL.md` -- validates and gates before merge (explicit approval required), but this is validation, not value refusal
- `docs/canonical/split-brain-planning-review.md` -- dual reviewers approve plans; approval, not refusal
- `docs/canonical/human-afk-task-routing-gate.md` -- routes tasks as AFK-ready or human-in-loop; classification, not refusal ownership
- `docs/system-of-record.md:25-46` -- maps agent system and domains; no refusal-owner role
- `curriculum/` -- no lesson on refusal-ownership as a designed role; Core Concept 7 (Multi-Agent Coordination) covers agent specialization but not refusal roles

**What exists nearby:**
- [[.opencode/skills/issue-review/SKILL.md|issue-review skill]]:14-15 "Nothing merges until the user explicitly confirms" -- a stop-before-merge gate but focused on quality, not value.
- The issue lifecycle skills (start, review, finish) gate work at quality checkpoints, not value checkpoints.

**Integration value:** Medium. The pattern is more organizational than technical. The repo's domain is curriculum and canonical patterns, not team role design. The concept could be valuable as curriculum content (Level 3 or 4) about harness governance.

---

## 6. Deferred Ledger for Agentic Work

**Classification:** Missing

**Why:**
The repo tracks token costs extensively but does not classify debt into the three categories (skill, dependence, carry) described by the pattern.

**Searched locations (NOT_FOUND):**
- `docs/canonical/explicit-token-budget-ledger.md` -- tracks per-call token costs, fixed vs. reducible blocks, remaining budget percentage -- cost accounting, not debt classification
- `docs/canonical/burn-rate-runtime-forecast.md` -- forecasts token consumption velocity and session runway -- consumption projection, not debt risk
- `docs/canonical/phase-gated-token-health-monitor.md` -- converts budget to green/yellow/orange/red phases -- health monitoring, not debt categories
- `docs/canonical/measured-harness-evolution-lifecycle.md` -- uses ROI (errors prevented vs. operating cost) for removal decisions -- component-level cost/benefit, not organizational debt
- `docs/canonical/garbage-collection-day-meta-loop.md` -- reviews agent misbehavior weekly -- slop cleanup, not debt ledger
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md` -- teaches token budgeting and burn rate -- cost awareness, not debt classification
- Searched for "skill debt", "dependence debt", "carry debt" across `docs/canonical/`, `curriculum/`, `.opencode/` -- NOT_FOUND

**What exists nearby:**
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:29-62 maintains a per-call ledger with fixed cost, reducible cost, output reservation, safety buffer, and remaining budget. This is a cost ledger, not a debt ledger.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:52-58 calculates ROI as `(Errors Prevented * Average Error Cost) / Component Operating Cost`. Related to carry cost but scoped to component-level cost/benefit, not organizational debt.

**Integration value:** High. The three debt categories (skill, dependence, carry) are a novel risk framework not present in the repo's existing cost tracking. The repo already has the instrumentation pieces (token ledger, burn rate, health monitor) that a debt ledger would consume. This would add a strategic risk layer on top of the operational cost layer.

---

## 7. Silent Degradation Sentinel Evals

**Classification:** Better Implementation

**Why:**
The repo has 15+ canonical docs covering eval infrastructure that together form a more comprehensive degradation-detection system than a single sentinel check. The repo's eval system is the most mature domain in the project.

**Evidence:**

- [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]:28-49 defines 5-15 seed cases with `case_id`, `workflow`, `input`, `state_fixture`, `expected_outcome`, `acceptable_tool_behavior`, `baseline`, `grading_notes`, and `owner`. This directly implements golden tasks with baselines -- the sentinel pattern's core mechanic.
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]:28-50 compares eval scores against production outcomes over time and defines decay thresholds: "Alert or require review when eval scores improve but production outcomes degrade" (`eval-to-production-correlation-tracking.md:48`). This detects exactly the silent degradation scenario the pattern describes.
- [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]:28-52 samples real production replays with baseline/candidate comparison and quality, latency, cost, and failure-class deltas.
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29-65 classifies failures into retryable/unsafe/hold rungs with retry, safe fallback, escalation, and rung tests -- operationalizes the fallback/escalation trigger the pattern describes.
- [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]:50-53 includes regression tests, staged rollout, shadow diffs, canary metrics, rollback decisions, and 14-day observation windows.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-50 defines fast/medium/deep tiers with runtime, cost, flakiness, trigger, threshold, reporting, and owner metadata -- production-ready eval infrastructure.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:40-51 maps pain signals (user complaints, manual review bottlenecks, escaped edge cases) to minimum eval investments.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40 converts production failures into durable regression cases.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:28-53 enforces eval checks at the PR gate with baseline/candidate comparison and merge policy.
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]:30-47 routes ambiguous eval outcomes to retry, needs-human, or rubric clarification using multiple models.

**Why Better Implementation:**
The source pattern describes a single sentinel check: golden tasks + baselines + independent evaluator. The repo has a full eval ecosystem: spot-check sets (golden tasks), production-grounded sampling (real behavior baselines), correlation tracking (detects when evals stop predicting outcomes -- the degradation signal), degradation ladder (operational response to detected degradation), tier stratification (cost-aware deployment), PR gates (enforcement), and failure regression flywheel (continuous improvement). The repo's eval system addresses not just detection but the full detect-classify-respond-improve lifecycle.

**Integration value:** Low -- repo already exceeds the pattern's maturity.

---

## 8. Accidental Brake Replacement

**Classification:** Missing

**Why:**
The concept of auditing external bureaucracy and replacing it with intentional harness gates is not present in the repo. The repo created its own governance infrastructure from scratch and does not model or interact with external bureaucratic gates.

**Searched locations (NOT_FOUND):**
- `docs/canonical/` -- 55 canonical patterns cover agent-internal harness engineering; none address external bureaucracy replacement
- `.github/` -- PR template, CODEOWNERS, issue templates, dependabot config; this is intentional governance, not replacement of accidental bureaucracy
- `.opencode/skills/issue-review/SKILL.md` -- validation gates (lint, test, eval) are designed intentionally, not inherited from bureaucracy
- `.opencode/skills/issue-start/SKILL.md` -- worktree setup and claim are internal workflow, not bureaucracy replacement
- `AGENTS.md` -- rules are designed for agent behavior, not inherited from organizational bureaucracy
- `docs/system-of-record.md:104-115` -- governance section covers PR templates, CODEOWNERS, issue templates; all intentional design
- `curriculum/` -- no lesson on bureaucracy replacement or accidental gate mapping

**Why this makes sense:**
The repo is a curriculum and canonical pattern library, not an enterprise organization with inherited procurement, security review, or compliance gates. The concept of replacing accidental bureaucracy with intentional harness gates is relevant to enterprise adoption contexts but not applicable to this repo's structure. The repo's governance was designed intentionally from the start.

**Integration value:** Low for the repo itself. The concept could be valuable as curriculum content for enterprise teams adopting agentic workflows.

---

## 9. Judgment Exercise Cadence

**Classification:** Partial Coverage

**Why:**
The repo has established review cadences but they focus on harness improvement and eval progression, not on exercising human value judgment for build/don't-build decisions.

**What exists:**

- [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]:31-55 defines a weekly cadence for reviewing agent misbehavior observations and converting them into automated guardrails. This is a recurring review ritual with a non-negotiable weekly cadence: "Feature pressure, release deadlines, and incident response do not cancel GC Day" (`garbage-collection-day-meta-loop.md:54`).
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:59-61 governs harness components with a quarterly cycle: "week 1 reviews model changelogs, metrics, and component classification; weeks 2-3 implement feature flags, shadow tests, and documented removals; weeks 4-12 observe without stacking new harness changes."
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:28-38 uses observed pain signals to trigger eval investments -- a decision gate driven by evidence, not calendar.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 reviews plans with dual rubrics (engineering and product/destination) and records deferred ambitions -- a review ritual but focused on plan quality, not value judgment.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 asks value questions one-at-a-time -- individual decisions, not a recurring cadence.

**What is missing:**
The specific purpose of exercising judgment muscle. The repo's cadences review harness quality, agent misbehavior, and eval capability -- all about the agent's output. The pattern's cadence is about keeping the human's value-decision skill active through explicit build/don't-build tradeoff discussions with recorded rationales, calibration examples, and refusal practice. The repo has the ritual infrastructure (weekly, quarterly cadences) but not this specific purpose.

**Integration value:** Medium. The repo has the structural pattern (recurring cadences, evidence-driven decisions) but lacks the specific content (build/don't-build tradeoff practice, judgment calibration, refusal muscle). This could be added as a layer on top of existing cadences or as a new exercise/ritual in the curriculum.

---

## 10. Carry Debt Sunset Gate

**Classification:** Partial Coverage

**Why:**
The repo has a mature component lifecycle with archiving and removal but applies it to harness components, not to general agent-created artifacts. The artifact-level keep/retire/archive/promote decision with expiration dates and named maintenance owners is missing.

**What exists:**

- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:50 defines the REMOVE phase: "REMOVE is allowed when a component has fulfilled its purpose and removal remains reversible." It archives code under `archive/components/<name>/` with a README explaining why it existed, why it was removed, and which model justified removal, while a feature flag allows reactivation in minutes (`measured-harness-evolution-lifecycle.md:50`).
- The lifecycle includes explicit removal-governance: ROI below 1x for two consecutive quarters triggers removal investigation (`measured-harness-evolution-lifecycle.md:58`), and "One In, One Out" requires each new component to mark an existing component for removal (`measured-harness-evolution-lifecycle.md:60`).
- [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]:46-54 builds guardrails during weekly sessions and deploys them immediately -- a creation cadence but focused on building, not retiring.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:29-60 classifies components as domain invariants or model-specific compensations before simplification or removal -- a pre-retirement classification.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:35 includes feedback writeback as an operating system surface -- outcomes become durable state but without artifact-specific retirement.

**What is missing:**
- Artifact-level inventory (not just harness components): what agents created, for whom, with what value hypothesis.
- Expiration dates or review triggers per artifact: when should each artifact be re-evaluated?
- Named maintenance owners: who is responsible for keeping, retiring, or promoting each artifact?
- The specific decision vocabulary: keep, retire, archive, promote -- applied to general agent output, not just harness components.

The measured-harness-evolution-lifecycle is the repo's closest implementation and covers the structural pattern (lifecycle states, archive, reactivation, ROI gating) but scoped to harness engineering rather than general artifact management.

**Integration value:** High. The repo already has the lifecycle mechanics for harness components; extending the same pattern to agent-created artifacts would add a novel capability. This addresses a gap that the source analysis names as "carry debt" -- agent-created software becoming permanent production burden without explicit sunset decisions.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Value-Gated Agent Control Loop | Partial Coverage | High |
| 2 | Manual Brake Question Gate | Missing | High |
| 3 | Intent-First Spec Loop | Better Implementation | Low |
| 4 | Continue Decision Checkpoint | Partial Coverage | Medium |
| 5 | Owner-of-No Role | Missing | Medium |
| 6 | Deferred Ledger for Agentic Work | Missing | High |
| 7 | Silent Degradation Sentinel Evals | Better Implementation | Low |
| 8 | Accidental Brake Replacement | Missing | Low |
| 9 | Judgment Exercise Cadence | Partial Coverage | Medium |
| 10 | Carry Debt Sunset Gate | Partial Coverage | High |

**Key insight:** The long-running-agents repo is strong in HOW agents execute (eval infrastructure, context management, loop control) but gap-heavy in WHETHER agents should execute (value gates, brake questions, debt tracking, refusal roles, artifact retirement). The two Better Implementations (Intent-First Spec Loop and Sentinel Evals) represent areas where the repo's existing investment naturally exceeds the source material. The four Missing classifications all concern value decision-making, organizational risk accounting, and governance that the repo's engineering-focused architecture doesn't address. This aligns with the source analysis's conclusion that "a arquitetura da decisao e mais importante que a arquitetura do codigo na era agentica" (`2026-06-11-the-trap-spec-driven-development-is-setting-analysis.md:171`).

## Evidence Summary

| Classification | Count | Patterns |
|---|---|---|
| Better Implementation | 2 | #3 Intent-First Spec Loop, #7 Silent Degradation Sentinel Evals |
| Already Exists | 0 | -- |
| Partial Coverage | 4 | #1 Value-Gated Agent Control Loop, #4 Continue Decision Checkpoint, #9 Judgment Exercise Cadence, #10 Carry Debt Sunset Gate |
| Missing | 4 | #2 Manual Brake Question Gate, #5 Owner-of-No Role, #6 Deferred Ledger for Agentic Work, #8 Accidental Brake Replacement |

