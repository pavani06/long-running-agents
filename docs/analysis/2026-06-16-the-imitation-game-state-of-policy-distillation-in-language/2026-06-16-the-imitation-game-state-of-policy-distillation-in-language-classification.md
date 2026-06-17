---
title: "Classification: Policy Distillation Patterns against long-running-agents"
type: analysis
date: 2026-06-16
aliases: ["OPD classification", "policy distillation classification", "on-policy distillation classification"]
tags: ["agentes-orquestracao", "context-engineering", "evals", "error-handling", "harness-engineering"]
relates-to:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-mental-model|Policy Distillation Mental Model]]"
  - "[[docs/system-of-record|System of Record]]"
  - "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]"
  - "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]"
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]"
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]"
  - "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]"
  - "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]"
  - "[[docs/canonical/external-state-persistence|External State Persistence]]"
  - "[[docs/canonical/summary-buffer-continuity|Summary Buffer Continuity]]"
  - "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]"
  - "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]"
  - "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]"
  - "[[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification|12FA Classification]]"
  - "[[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification|Eval Maturity Classification]]"
sources: ["[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Patterns]]"]
---

# Classification: Policy Distillation Patterns against long-running-agents

Date: 2026-06-16
Source: [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]
Patterns classified: 8
Evidence precedence: ADRs (empty) < canonical < analysis < curriculum < READMEs

## 1. On-Policy Rollout Feedback Loop

- **Classification:** Partial Coverage
- **Integration Value:** High

### Justification

The repository has strong infrastructure for capturing and learning from production failures, but does not close the on-policy loop where the agent's own trajectory prefixes become the learning signal.

### What exists

- `Production-Grounded Eval Sampling` (`docs/canonical/production-grounded-eval-sampling.md:28-52`) captures production interactions, agent traces, tool results, and state snapshots for replay against baseline and candidate agent versions. This samples from the inference distribution, which is a core input of the on-policy loop.
- `Production Failure Regression Flywheel` (`docs/canonical/production-failure-regression-flywheel.md:28-40`) converts every production failure into a durable eval regression case with trace, labels, tier assignment, and deduplication. Failures feed back into eval cases, which is the learning-output side of the loop.
- `QA-to-Backlog Feedback Loop` (`docs/canonical/qa-to-backlog-feedback-loop.md:24`, `docs/canonical/qa-to-backlog-feedback-loop.md:50`) formalizes review findings as backlog inputs, converting observations into concrete issues.
- `Closed-Loop Agent Operating System` (`docs/canonical/closed-loop-agent-operating-system.md:32-45`) includes feedback writeback as an OS surface: "outcomes become trusted future memory."
- `Eval to Production Correlation Tracking` (`docs/canonical/eval-to-production-correlation-tracking.md:50-76`) ties eval scores to production outcomes, providing the directional signal for whether a change improved or degraded behavior.

### What is missing

None of these mechanisms runs the agent on production-like prompts, captures the agent's own prefixes (its actual decisions, not the ideal ones), scores those prefixes with a teacher/evaluator, and feeds the scored prefixes back as update targets (prompts, skills, evals, or training data). The repo captures failures and turns them into evals (regression side), but does not explicitly sample from the agent's on-policy distribution to close the exposure-bias gap between curated examples and runtime trajectories. The "rollout → score on own prefixes → update → re-run" loop is not present as a named pattern.

### Evidence

- `docs/canonical/production-grounded-eval-sampling.md:28-52` — production trace capture and replay
- `docs/canonical/production-failure-regression-flywheel.md:28-40` — failure → durable eval regression
- `docs/canonical/qa-to-backlog-feedback-loop.md:24,50` — review findings → backlog items
- `docs/canonical/closed-loop-agent-operating-system.md:32-45` — feedback writeback OS surface
- `docs/canonical/eval-to-production-correlation-tracking.md:50-76` — eval-to-outcome correlation
- NOT_FOUND: explicit "agent runs on own prefixes → scored by teacher → updates targets → re-runs" loop in any canonical doc, skill, or curriculum file.

---

## 2. Autonomy Curriculum Sampling

- **Classification:** Missing
- **Integration Value:** Medium

### Justification

The repository contains adjacent concepts (curriculum levels, harness evolution stages, progressive disclosure) but no mechanism that controls the autonomy mix between supervised demonstrations and self-generated rollouts with an explicit schedule and readiness gates.

### What exists

- `Measured Harness Evolution Lifecycle` (`docs/canonical/measured-harness-evolution-lifecycle.md:29-62`) defines BUILD → STABILIZE → SIMPLIFY → REMOVE stages for harness components. This is a progression from defense to removal, similar in spirit to an autonomy progression, but it operates on harness components, not on agent autonomy.
- The curriculum itself (`curriculum/README.md:192-247`) defines a 4-level progression (N1 fundamentals → N4 production), which is a learning curriculum, not an operational autonomy schedule.
- `Resolver-Based Context Progressive Disclosure` (`docs/canonical/resolver-based-context-progressive-disclosure.md`) loads skills progressively by trigger rather than monolithically, sharing the "progressive increase" structure.
- `Domain-Embedded Workflow Automation Wedge` (`docs/canonical/domain-embedded-workflow-automation-wedge.md:48-71`) requires validation before broad rollout, which is a readiness gate concept but applied to deployment, not agent autonomy.

### What is missing

None of the above defines an explicit autonomy mix parameter (lambda), readiness thresholds, or a schedule policy that gradually increases self-generated work. The concept of "start teacher-heavy, gradually increase student rollouts, gate each step on success/safety metrics" has no representation in the repository. The repo has "assist" operations (shadow review, human-in-the-loop gates) but does not map them to a graduated autonomy dial.

### Evidence

- `docs/canonical/measured-harness-evolution-lifecycle.md:29-62` — harness component stages (adjacent but different domain)
- `curriculum/README.md:192-247` — learning curriculum levels (adjacent but learning, not operational)
- NOT_FOUND: autonomy mix parameter, readiness gate for agent autonomy, or explicit teacher/student rollout schedule in any canonical doc, skill, curriculum file, or ADR.
- Searched: `docs/canonical/`, `curriculum/`, `.opencode/skills/`

---

## 3. Privileged Context Self-Distillation

- **Classification:** Partial Coverage
- **Integration Value:** Medium

### Justification

The repository has extensive context-management infrastructure where design-time analysis produces compact runtime artifacts, but lacks the specific self-distillation mechanic where the same agent is compared under two context views and the useful delta is distilled into runtime-usable behavior.

### What exists

- `Hybrid Context Stack` (`docs/canonical/hybrid-context-stack.md:20-42`) assembles context from ordered layers (stable prompt, durable state, head/tail anchors, summaries, recoverable omitted middle). This is the architecture that would consume distilled rules.
- `External State Persistence` (`docs/canonical/external-state-persistence.md:31-57`) decouples agent memory from model memory: durable facts persist across sessions while active context is rebuilt. This is the surface where distilled knowledge would land as "compact rules."
- `Head-Tail Context Truncation` (`docs/canonical/head-tail-context-truncation.md:26-39`) keeps bounded active context with recoverable middle. The middle is like privileged information that cannot fit at runtime but can be fetched on demand.
- `Summary Buffer Continuity` (`docs/canonical/summary-buffer-continuity.md`) compresses older history into a portable buffer — analogous to the distillation target that converts full context into compact operating knowledge.
- `Budget-Aware Session Handoff` (`docs/canonical/budget-aware-session-handoff.md:62-75`) passes compressed state (summary buffer, durable facts, recoverable handles) between sessions, which is the runtime consumption of distilled knowledge.
- `Durable Fact Selective History` (`docs/canonical/durable-fact-selective-history.md`) extracts and preserves durable facts from history, similar to identifying which privileged information matters.

### What is missing

None of these patterns runs the same agent under two different context views (runtime vs. privileged), compares the output delta, and explicitly distills the useful difference into compact runtime rules. The repo has the "compact context at runtime" side, but not the "design-time self-distillation from privileged information" loop. The specific mechanic of "run task under restricted view and privileged view → identify where privileged context changed the decision → convert useful delta into prompt rule/skill/eval → calibrate under runtime view" is not present.

### Evidence

- `docs/canonical/hybrid-context-stack.md:20-42` — layered context assembly
- `docs/canonical/external-state-persistence.md:31-57` — durable state for compact runtime knowledge
- `docs/canonical/head-tail-context-truncation.md:26-39` — recoverable privileged-like middle
- `docs/canonical/summary-buffer-continuity.md` — compressed history buffer
- `docs/canonical/budget-aware-session-handoff.md:62-75` — compressed state transfer
- `docs/canonical/durable-fact-selective-history.md` — selective fact extraction
- NOT_FOUND: explicit self-distillation from teacher (privileged) view to student (runtime) view in any canonical doc, skill, or curriculum file.

---

## 4. Consensus-Gated Privileged Information

- **Classification:** Partial Coverage
- **Integration Value:** Medium

### Justification

The repository has a mature Multi-Model Evaluation Council that gates evaluation results with model diversity, independent scoring, and aggregation thresholds, but does not generalize this consensus gate to all privileged information (retrieved documents, sub-agent findings, plans, reference answers) before they influence the agent.

### What exists

- `Multi-Model Evaluation Council` (`docs/canonical/multi-model-evaluation-council.md:24-40`) gates evaluation outputs with model diversity, independent first passes, aggregation policy (pass/fail/retry/needs-human), disagreement thresholds, and calibration against real outcomes. This is structurally identical to consensus-gated privileged information but scoped to evaluation results.
- `Generator-Evaluator` (`docs/canonical/generator-evaluator.md:31-85`) separates generation from evaluation and routes rejected output back with feedback. This is a two-agent consensus on output quality.
- `Shadow Review Pipeline` (`docs/canonical/shadow-review-pipeline.md:27-31`) runs AI review in parallel with human review, collecting agreement metrics before graduating AI checks to blocking status. This gates AI review signals through human agreement.
- `Dual/Ensemble Evaluator` in the curriculum (`curriculum/05-core-concepts/08-evaluation-rubrics.md:156-164`) requires two or more independent evaluators, score comparison, divergence escalation, and ensemble evaluation reserved for high-value decisions.
- `Split-Brain Planning Review` (`docs/canonical/split-brain-planning-review.md:26-41`) separates engineering and product-destination reviews with independent rubrics before reconciliation.

### What is missing

All existing consensus mechanisms gate *evaluation outputs* or *review decisions*, not the broader class of *privileged information* (retrieved documents, generated plans, sub-agent findings, reference answers). The repo does not have a general pattern for running multiple evaluator/tutor passes over any candidate privileged information and only accepting it when independent rollouts agree above threshold with an explicit trust gate, audit record, and escalation path for weak consensus.

### Evidence

- `docs/canonical/multi-model-evaluation-council.md:24-40` — council mechanics (model diversity, independent scoring, aggregation, disagreement)
- `docs/canonical/generator-evaluator.md:31-85` — generator↔evaluator rejection loop
- `docs/canonical/shadow-review-pipeline.md:27-31` — shadow period with agreement metrics
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:156-164` — dual/ensemble evaluator
- `docs/canonical/split-brain-planning-review.md:26-41` — independent review before reconciliation
- NOT_FOUND: consensus gate for privileged information (retrieved docs, plans, sub-agent findings) rather than evaluation results, with explicit trust thresholds, audit records, and escalation policies. Searched: `docs/canonical/`, `curriculum/`, `.opencode/skills/`

---

## 5. Asymmetric Failure Correction Router

- **Classification:** Partial Coverage
- **Integration Value:** Medium

### Justification

The repository has mature failure handling infrastructure (degradation ladder, regression flywheel, QA feedback loop), but does not separate positive and negative feedback into asymmetric routing paths where success goes to exemplars/reinforcement and failure goes to repair/root-cause analysis.

### What exists

- `Tested Degradation Ladder` (`docs/canonical/tested-degradation-ladder.md:29-65`) classifies failures by severity into retryable, unsafe, and hold rungs with retry, safe fallback, human escalation, and outcome logging. This handles the correction side but does not separate success routing.
- `Failure Pattern Classification Loop` (`docs/canonical/failure-pattern-classification-loop.md:27-45`) classifies failures into root cause classes (model ignorance, missing harness, local coherence, prompt ambiguity, context loss, model regression) and maps them to guardrail surfaces. This covers the "classify and route" aspect for failures.
- `Production Failure Regression Flywheel` (`docs/canonical/production-failure-regression-flywheel.md:28-40`) converts production failures into eval cases, which is the regression creation channel for failures.
- `QA-to-Backlog Feedback Loop` (`docs/canonical/qa-to-backlog-feedback-loop.md:30-44`) routes review findings to backlog with capture, triage, conversion, and return-to-board stages. This routes failures to actionable items.
- `Generator-Evaluator` (`docs/canonical/generator-evaluator.md:31-85`) separates Generator (creative) from Evaluator (critical), but the evaluator produces a binary verdict — not an asymmetric routing decision separating success reinforcement from failure correction.
- `Constraint-Failure Decision Rule` (`docs/canonical/constraint-failure-decision-rule.md:25-58`) classifies requirements as constraints (builder surface) vs. failure conditions (validator surface). This is an asymmetric split of requirement types, but applies to intent specification, not to routing agent performance feedback.

### What is missing

None of these mechanisms explicitly routes *successes* to exemplars, demonstrations, confidence calibration, or reduced supervision, while routing *failures* to repair, regression, root-cause, or escalation through a separate correction channel. The repo has the failure-processing infrastructure but no explicit success-routing machinery, and more importantly, no pattern that treats these as asymmetric paths with different mechanics and separate learning logs.

### Evidence

- `docs/canonical/tested-degradation-ladder.md:29-65` — severity-based failure classification
- `docs/canonical/failure-pattern-classification-loop.md:27-45` — root cause → guardrail mapping
- `docs/canonical/production-failure-regression-flywheel.md:28-40` — failure → regression eval
- `docs/canonical/qa-to-backlog-feedback-loop.md:30-44` — review findings → backlog
- `docs/canonical/generator-evaluator.md:31-85` — generator/evaluator separation
- `docs/canonical/constraint-failure-decision-rule.md:25-58` — asymmetric requirement classification
- NOT_FOUND: explicit success-routing channel (exemplars, demonstrations, reduced supervision) separated from failure-routing channel (repair, regression, escalation) with different mechanics and separate learning logs. Searched: `docs/canonical/`, `curriculum/05-core-concepts/`

---

## 6. Magnitude-Direction Verifier Split

- **Classification:** Missing
- **Integration Value:** High

### Justification

The repository has strong evaluator and verification infrastructure, but no mechanism that takes the agent's internal confidence (magnitude) as a separate signal, combines it with an external verifier's direction, and produces a weighted correction plan.

### What exists

- `Generator-Evaluator` (`docs/canonical/generator-evaluator.md:31-85`) separates generation from evaluation, with the Evaluator providing an external correctness signal (direction). The Generator produces the output (where the agent "believes" change matters), but internal confidence is not explicitly captured as a magnitude signal.
- `Constraint-Anchored Evaluation` (`docs/canonical/constraint-anchored-evaluation.md:29-56`) anchors evaluation on explicit constraint lists, providing the external verification direction.
- `Compartmented Evaluation Architecture` (`docs/canonical/compartmented-evaluation-architecture.md:64`) enforces separation between builder and validator surfaces, ensuring the builder does not see eval targets. This is direction enforcement, not magnitude+direction combination.
- `Two-Implementations Goal Test` (`docs/canonical/two-implementations-goal-test.md`) validates goal specification by testing whether different implementations of the same goal converge — an external verification mechanism.
- `Eval Tier Stratification` (`docs/canonical/eval-tier-stratification.md:26-50`) provides fast/medium/deep tiers for verification at appropriate levels.

### What is missing

None of these patterns:
1. Captures the agent's internal confidence as a magnitude signal (self-distillation delta, log-ratio, attention hotspot, disagreement intensity).
2. Combines that magnitude with an external direction signal to produce a weighted correction plan.
3. Escalates high-magnitude, uncertain-direction cases to human review.
4. Maintains an audit trail separating confidence evidence from correctness evidence.

The missing mechanism is the formal "the agent is confident here (magnitude), the verifier says this is correct/incorrect (direction), therefore spend correction effort here with this weight."

### Evidence

- `docs/canonical/generator-evaluator.md:31-85` — generator (internal) vs. evaluator (external)
- `docs/canonical/constraint-anchored-evaluation.md:29-56` — external constraint verification
- `docs/canonical/compartmented-evaluation-architecture.md:64` — builder/validator separation
- `docs/canonical/eval-tier-stratification.md:26-50` — verification tiers
- NOT_FOUND: explicit magnitude signal extraction from internal model confidence combined with external verifier direction to produce weighted corrections, with escalation rules for high-magnitude/unclear-direction cases. Searched: `docs/canonical/`, `curriculum/`, `.opencode/skills/`

---

## 7. Adaptive Style Compression Teacher

- **Classification:** Partial Coverage
- **Integration Value:** Medium

### Justification

The repository has extensive context compression infrastructure, but compression strategies operate on fixed rules rather than adapting to task difficulty, and none explicitly preserves uncertainty markers or conditions compression strength on task signals.

### What exists

- `Head-Tail Context Truncation` (`docs/canonical/head-tail-context-truncation.md:26-39`) keeps bounded active context with head, tail, latest result, and recoverable middle. This is a compression strategy, but operates on fixed rules (always keep head + tail + latest result), not adaptive to task difficulty.
- `Summary Buffer Continuity` (`docs/canonical/summary-buffer-continuity.md`) compresses older history into a portable, incrementally updated buffer. This compresses continuous context but does not adapt strength to task signals.
- `Durable Fact Selective History` (`docs/canonical/durable-fact-selective-history.md`) selects and preserves durable facts from history. This is selective about what to keep, but the selection is by fact type (durable vs. transient), not by task difficulty.
- `Budget-Aware Session Handoff` (`docs/canonical/budget-aware-session-handoff.md:27-62`) triggers handoff based on budget thresholds, not task difficulty signals. The compression trigger is budget-driven, not difficulty-driven.
- `Semantic Topic Bucketing` (`docs/canonical/semantic-topic-bucketing.md`) groups context by topic, which is a structuring strategy rather than a difficulty-adaptive one.
- `Hybrid Context Stack` (`docs/canonical/hybrid-context-stack.md:20-42`) assembles context from ordered layers — this defines what goes into context, not how compression adapts to difficulty.

### What is missing

None of these patterns:
1. Conditions compression strength on task difficulty signals (verifier uncertainty, unresolved constraints, failed attempts, dependency depth).
2. Preserves uncertainty markers and hedging in compressed output (adaptive style that is terse on easy tasks but preserves deliberation on hard tasks).
3. Uses downstream eval to validate that compressed context preserves task success and calibration.
4. Defines a compression policy that varies by task rather than applying a fixed rule everywhere.

The repo compresses context, but always with the same strategy regardless of whether the task is simple or complex — an easy product lookup gets the same truncation rules as a multi-step order with conflicting constraints.

### Evidence

- `docs/canonical/head-tail-context-truncation.md:26-39` — fixed-rule head+tail truncation
- `docs/canonical/summary-buffer-continuity.md` — continuous summary compression
- `docs/canonical/durable-fact-selective-history.md` — selective fact retention
- `docs/canonical/budget-aware-session-handoff.md:27-62` — budget-driven handoff trigger
- `docs/canonical/hybrid-context-stack.md:20-42` — layered context assembly
- NOT_FOUND: adaptive compression strength conditioned on task difficulty, uncertainty marker preservation, or downstream calibration via task-specific eval on compressed context. Searched: `docs/canonical/`, `curriculum/05-core-concepts/01-context-management.md`

---

## 8. Trajectory Failure Pattern Classifier

- **Classification:** Already Exists
- **Integration Value:** Low

### Justification

The repository has `Failure Pattern Classification Loop`, a mature canonical doc that covers the same core mechanism: classify agent failures by root cause mechanism rather than generic labels, then route each class to the appropriate mitigation surface. The taxonomy differs (policy-distillation failure classes vs. harness-engineering root causes), but the mechanism and architectural role are equivalent.

### Evidence

- `Failure Pattern Classification Loop` (`docs/canonical/failure-pattern-classification-loop.md:23-65`) defines a 4-stage observe → classify → build → verify loop where failures are classified into root cause classes (model ignorance, missing harness, local coherence, prompt ambiguity, context loss, model regression) and mapped to guardrail surfaces (lint rule, reviewer prompt, NFR doc, skill, eval case, micro-harness, test).
- The classification loop explicitly addresses the same problem: "When agents produce recurring misbehavior, teams fix individual instances without asking: what class of failure does this represent, and can we eliminate the class rather than the instance?" (`docs/canonical/failure-pattern-classification-loop.md:23`).
- `Tested Degradation Ladder` (`docs/canonical/tested-degradation-ladder.md:29-65`) provides severity classification on top of root cause classification.
- `Production Failure Regression Flywheel` (`docs/canonical/production-failure-regression-flywheel.md:42-54`) defines a failure taxonomy (prompt issue, tool misuse, context loss, state persistence, scoring gap, latency/cost, safety, late-session failure) and recommends every failure become a durable regression case with mechanism named.
- `Garbage Collection Day Meta-Loop` (`docs/canonical/garbage-collection-day-meta-loop.md:101`) uses the FPCL rubric as its execution mechanic.
- The curriculum embeds this at the checklist level: `curriculum/07-implementation-guides/03-harness-design-checklist.md:976` requires failures to be classified by taxonomy and converted to regression cases.

### Difference in taxonomy, not mechanism

The `Trajectory Failure Pattern Classifier` uses a taxonomy from on-policy distillation (proxy metric drift, early-prefix drift, supervision expiry, diversity collapse, PI leakage, calibration gap, epistemic suppression). The repo's FPCL uses a taxonomy from harness engineering (model ignorance, missing harness, local coherence, prompt ambiguity, context loss, model regression). These taxonomies serve different sources but the architectural role (classify failures by mechanism → route to specific mitigation → write regression artifact) is the same.

The repo's implementation is more mature: it includes a guardrail surface mapping table (`docs/canonical/failure-pattern-classification-loop.md:67-75`), integrates with the degradation ladder for severity stacking, feeds into the measured harness evolution lifecycle, and connects to GC Day as its scheduled execution surface.

### Recommendation

Cross-reference in any artifacts generated for other patterns. No new canonical doc, skill, or exercise is needed. The repo's `Failure Pattern Classification Loop` already covers this pattern's terrain at a deeper level of integration with the rest of the harness ecosystem.

### Evidence references

- `docs/canonical/failure-pattern-classification-loop.md:23-65` — observe → classify → build → verify loop with root cause taxonomy
- `docs/canonical/failure-pattern-classification-loop.md:67-75` — guardrail surface mapping table
- `docs/canonical/production-failure-regression-flywheel.md:42-54` — failure taxonomy and regression conversion
- `docs/canonical/tested-degradation-ladder.md:29-65` — severity classification
- `docs/canonical/garbage-collection-day-meta-loop.md:101` — FPCL as GC Day execution mechanic
- `curriculum/07-implementation-guides/03-harness-design-checklist.md:976` — classified failure → regression case

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | On-Policy Rollout Feedback Loop | Partial Coverage | High |
| 2 | Autonomy Curriculum Sampling | Missing | Medium |
| 3 | Privileged Context Self-Distillation | Partial Coverage | Medium |
| 4 | Consensus-Gated Privileged Information | Partial Coverage | Medium |
| 5 | Asymmetric Failure Correction Router | Partial Coverage | Medium |
| 6 | Magnitude-Direction Verifier Split | Missing | High |
| 7 | Adaptive Style Compression Teacher | Partial Coverage | Medium |
| 8 | Trajectory Failure Pattern Classifier | Already Exists | Low |

### Classification Distribution

| Classification | Count |
|---|---|
| Already Exists | 1 |
| Partial Coverage | 5 |
| Missing | 2 |
| Better Implementation | 0 |

### Precedence Sources Consulted

All classifications follow `docs/system-of-record.md:14-21` precedence:
1. `docs/decisions/` — empty (`.gitkeep` only, confirmed by mental model `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-mental-model.md:164`)
2. `docs/canonical/` — 65 active canonical patterns; all searched
3. `docs/evidence/` — empty (`.gitkeep` only)
4. `docs/analysis/` — all prior classification analyses reviewed
5. `curriculum/` — core concepts, exercises, implementation guides, glossary searched
6. READMEs and operational summaries — checked for pattern mentions
