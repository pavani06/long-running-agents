---
title: "Classification: Harness Evolution and Construction Methods"
type: analysis
tags: ["agentes-orquestracao", "harness", "context-engineering", "evals"]
date: 2026-06-10
aliases: ["harness evolution classification", "construction methods classification"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/external-state-persistence|External State Persistence]]"]
sources: ["[[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Pattern Extraction: Harness Evolution and Construction Methods]]"]
---
# Classification: Harness Evolution and Construction Methods

## Exhaustive Canonical Scope

The classification uses `docs/system-of-record.md` as the canonical index. The system of record states that `docs/canonical/` has active canonical patterns at `docs/system-of-record.md:124` and lists the active canonical pattern table at `docs/system-of-record.md:128` through `docs/system-of-record.md:159`.

All existing canonical docs in `docs/canonical/` were read. The worktree contains 27 canonical markdown files. `docs/canonical/obsidian-document-conventions.md` is listed by the system of record at `docs/system-of-record.md:155`, but the file is absent in this worktree, so it could not be read as a canonical source.

## 1. Application-Owned Agent Control Plane

**Classification:** Partial Coverage

**Justification:** The repository already has a strong inner-loop canonical model and a broader closed-loop operating model, but the target pattern combines prompt versioning, context construction, structured action schema, deterministic dispatch, loop policy, persistent execution state, and intervention gates as one application-owned control plane. The canonical docs cover those pieces, but not as one unified control-plane contract.

**Evidence (file:line):**

- `docs/canonical/owned-agent-control-loop.md:29` introduces owning the control loop as the solution.
- `docs/canonical/owned-agent-control-loop.md:31` says to decompose the loop into four components with explicit intervention points.
- `docs/canonical/owned-agent-control-loop.md:33` through `docs/canonical/owned-agent-control-loop.md:51` names Prompt, Context Builder, Switch Statement, and Loop plus intervention points.
- `docs/canonical/owned-agent-control-loop.md:68` through `docs/canonical/owned-agent-control-loop.md:75` defines loop controls such as break, summarize, LM-as-judge, human approval, and force terminate.
- `docs/canonical/owned-agent-control-loop.md:96` through `docs/canonical/owned-agent-control-loop.md:107` states the repo still lacks full loop ownership because LangGraph owns internal iteration.
- `docs/canonical/closed-loop-agent-operating-system.md:28` through `docs/canonical/closed-loop-agent-operating-system.md:37` defines state intake, priority synthesis, execution routing, and feedback writeback as a broader operational loop.

**What's missing:** A single canonical control-plane pattern that integrates the owned loop with structured action schema, durable execution state, versioned prompt/tool contracts, and intervention gates as one application-owned runtime contract.

**Integration value:** High

## 2. Context Working Set with Recoverable Middle

**Classification:** Already Exists

**Justification:** The canonical `Head-Tail Context Truncation with Recoverable Middle` doc covers the same name-level concept, mechanism, and tradeoffs. Supporting canonical docs define the addressable catalog and stable harness prompt blocks that complete the working-set model.

**Evidence (file:line):**

- `docs/canonical/head-tail-context-truncation.md:20` through `docs/canonical/head-tail-context-truncation.md:24` defines the long-session context-loss problem.
- `docs/canonical/head-tail-context-truncation.md:26` through `docs/canonical/head-tail-context-truncation.md:39` defines the mechanism: stable prompt, head, tail, latest result, recoverable middle, memory store, IDs, location, and preview.
- `docs/canonical/head-tail-context-truncation.md:63` through `docs/canonical/head-tail-context-truncation.md:70` gives tradeoffs for boundary selection, storage, auditability, and eval cost.
- `docs/canonical/addressable-memory-catalog.md:26` through `docs/canonical/addressable-memory-catalog.md:43` defines the omitted-memory catalog with `id`, `kind`, `location`, `preview`, `scope`, and `fetch`.
- `docs/canonical/stable-harness-prompt.md:26` through `docs/canonical/stable-harness-prompt.md:41` defines stable harness prompt preservation during context reduction.

**Integration value:** Low

## 3. Error Hygiene Recovery Loop

**Classification:** Already Exists

**Justification:** The canonical `Error Context Hygiene` doc directly covers the target pattern's name, mechanism, retry-loop integration, recovery cleanup behavior, and tradeoffs.

**Evidence (file:line):**

- `docs/canonical/error-context-hygiene.md:20` through `docs/canonical/error-context-hygiene.md:27` defines context pollution, spiral-out, and stale error bias.
- `docs/canonical/error-context-hygiene.md:28` through `docs/canonical/error-context-hygiene.md:39` states the solution and core rules: summarize, clear on success, never blind-append, keep only what is needed.
- `docs/canonical/error-context-hygiene.md:41` through `docs/canonical/error-context-hygiene.md:58` shows the error summarizer and clear-pending-errors mechanism.
- `docs/canonical/error-context-hygiene.md:93` through `docs/canonical/error-context-hygiene.md:106` integrates the pattern into a bounded retry loop.
- `docs/canonical/error-context-hygiene.md:136` through `docs/canonical/error-context-hygiene.md:143` documents tradeoffs.

**Integration value:** Low

## 4. Structured Generation and Constraint Validation Circuit

**Classification:** Partial Coverage

**Justification:** The repository has canonical coverage for structured tool/action dispatch and separate canonical coverage for constraint-anchored evaluation, but no unified circuit that explicitly combines shape validation, domain-constraint validation, repair or rejection, and audit logging for generated actions or recommendations.

**Evidence (file:line):**

- `docs/canonical/deterministic-tool-dispatch.md:20` through `docs/canonical/deterministic-tool-dispatch.md:29` frames model output as JSON routed by application code.
- `docs/canonical/deterministic-tool-dispatch.md:31` through `docs/canonical/deterministic-tool-dispatch.md:36` states the reframe: tools are JSON plus deterministic code.
- `docs/canonical/deterministic-tool-dispatch.md:37` through `docs/canonical/deterministic-tool-dispatch.md:57` gives the structured-output-to-handler mechanism.
- `docs/canonical/constraint-anchored-evaluation.md:29` through `docs/canonical/constraint-anchored-evaluation.md:33` defines evaluation against explicit verifiable constraints and an aggregate verdict.
- `docs/canonical/constraint-anchored-evaluation.md:35` through `docs/canonical/constraint-anchored-evaluation.md:50` defines the verification matrix and approved-only-if-all-constraints-pass circuit.
- `docs/canonical/constraint-anchored-evaluation.md:80` through `docs/canonical/constraint-anchored-evaluation.md:89` documents tradeoffs.

**What's missing:** A single canonical doc that treats structured generation plus post-generation constraint validation as one action-safety circuit with repair, rejection, risk flags, and audit-ready evidence.

**Integration value:** High

## 5. Independent Generator-Evaluator Gate

**Classification:** Already Exists

**Justification:** The canonical `Generator-Evaluator` doc directly covers independent generation and evaluation, including distinct roles, context needs, verdicts, feedback loops, and tradeoffs. `Multi-Model Evaluation Council` further strengthens the independent-evaluator side for high-risk cases.

**Evidence (file:line):**

- `docs/canonical/generator-evaluator.md:21` through `docs/canonical/generator-evaluator.md:27` defines the self-evaluation confirmation-bias problem.
- `docs/canonical/generator-evaluator.md:29` through `docs/canonical/generator-evaluator.md:31` defines the two-agent solution: Generator produces candidates, Evaluator checks persisted state, rubrics, and business rules.
- `docs/canonical/generator-evaluator.md:33` through `docs/canonical/generator-evaluator.md:75` shows the approval and rejection feedback loop.
- `docs/canonical/generator-evaluator.md:77` through `docs/canonical/generator-evaluator.md:83` defines Generator and Evaluator responsibilities, context needs, model characteristics, outputs, and failure modes.
- `docs/canonical/generator-evaluator.md:107` through `docs/canonical/generator-evaluator.md:116` documents tradeoffs.
- `docs/canonical/multi-model-evaluation-council.md:28` through `docs/canonical/multi-model-evaluation-council.md:40` defines independent multi-model evaluator mechanics for high-risk decisions.

**Integration value:** Low

## 6. Versioned Durable Agent State

**Classification:** Partial Coverage

**Justification:** The repository has durable external state, pause/resume state, and prompt/catalog/schema version references, but no canonical doc unifies versioned agent-state schema, migration policy, writeback policy, reload policy, and audit trail as one durable-state contract.

**Evidence (file:line):**

- `docs/canonical/external-state-persistence.md:29` through `docs/canonical/external-state-persistence.md:57` defines extracting critical data, writing to an external store, loading it on the next turn, and merging it with current context.
- `docs/canonical/external-state-persistence.md:57` states that this decouples agent memory from model memory and persists critical facts outside the context window.
- `docs/canonical/external-state-persistence.md:59` through `docs/canonical/external-state-persistence.md:65` distinguishes durable state from ephemeral content.
- `docs/canonical/serializable-pause-resume-state.md:31` through `docs/canonical/serializable-pause-resume-state.md:57` defines serializing context, execution state, and business state for pause/resume.
- `docs/canonical/serializable-pause-resume-state.md:78` through `docs/canonical/serializable-pause-resume-state.md:89` compares serialized state with repo state rebuild tradeoffs.
- `docs/canonical/stable-harness-prompt.md:41` states prompt changes should be deliberate, versioned, and evaluated separately from context compaction.

**What's missing:** Explicit versioned state schema, migration rules, writeback and reload contracts, and audit-trail requirements for durable agent state as one canonical pattern.

**Integration value:** High

## 7. Tested Degradation Ladder

**Classification:** Partial Coverage

**Justification:** The canonical docs cover rungs that a degradation ladder would need: error summarization and retry hygiene, loop intervention points, human approval gates, escalation, regression tests, eval tiers, canary/shadow evidence, and production failure flywheels. They do not define one tested ladder from failure classification to retry, fallback or hold, human escalation, and production-like fallback tests.

**Evidence (file:line):**

- `docs/canonical/error-context-hygiene.md:93` through `docs/canonical/error-context-hygiene.md:106` defines bounded retry-loop integration.
- `docs/canonical/error-context-hygiene.md:120` through `docs/canonical/error-context-hygiene.md:125` identifies existing fallback mechanisms and the context-layer addition.
- `docs/canonical/owned-agent-control-loop.md:68` through `docs/canonical/owned-agent-control-loop.md:75` names break, summarize, LM-as-judge, human approval, and force terminate as loop controls.
- `docs/canonical/multi-model-evaluation-council.md:37` through `docs/canonical/multi-model-evaluation-council.md:45` defines retry, needs-human, disagreement escalation, and human review routing.
- `docs/canonical/eval-tier-stratification.md:26` through `docs/canonical/eval-tier-stratification.md:50` defines eval tiers with runtime, cost, trigger, threshold, reporting, owner, and escalation metadata.
- `docs/canonical/production-failure-regression-flywheel.md:28` through `docs/canonical/production-failure-regression-flywheel.md:40` requires production failures to become durable eval regression cases.

**What's missing:** A named degradation ladder with ordered rungs, failure classifier, retry eligibility, fallback/hold policy, human escalation route, outcome logging, and tests for each rung before production reliance.

**Integration value:** High

## 8. Invariant-Compensation Split

**Classification:** Missing

**Justification:** NOT_FOUND after reading the system of record and all 27 existing canonical docs in `docs/canonical/`. The repository has adjacent cost, removal, prompt-stability, and harness-evolution references, but no canonical pattern that classifies harness controls as permanent domain invariants versus temporary model-specific compensations.

**Evidence (file:line):**

- Exhaustive canonical scope came from `docs/system-of-record.md:124` through `docs/system-of-record.md:159`, which lists the active canonical pattern set.
- Nearest non-equivalent coverage: `docs/canonical/pain-signal-eval-progression-gate.md:57` through `docs/canonical/pain-signal-eval-progression-gate.md:60` references adjacent harness-evolution questions about what failure a component prevents, cost, and whether removal is safe.
- Nearest non-equivalent coverage: `docs/canonical/stable-harness-prompt.md:26` through `docs/canonical/stable-harness-prompt.md:41` protects stable harness instructions during context reduction, but does not classify controls as domain invariants or model-specific compensations.
- Nearest non-equivalent coverage: `docs/canonical/eval-tier-stratification.md:38` through `docs/canonical/eval-tier-stratification.md:50` defines eval metadata such as runtime, cost, flakiness, trigger, threshold, reporting, and owner, but not invariant/compensation classification.

**NOT_FOUND confirmation:** The exact pattern concept was not found in the canonical set or `docs/system-of-record.md`: no canonical doc defines a harness component inventory with failure-prevention rationale, domain-invariant criteria, compensation criteria, false-positive/cost metrics, and keep/simplify/measure/remove decisions.

**Integration value:** High

## 9. Measured Harness Evolution Lifecycle

**Classification:** Partial Coverage

**Justification:** Canonical docs cover measurement, shadow/canary rollout, eval tiers, PR gates, production correlation, and failure regression, but no canonical doc defines the BUILD, STABILIZE, SIMPLIFY, REMOVE lifecycle with component archive, ROI calculation, reversible removal, and reactivation path.

**Evidence (file:line):**

- `docs/canonical/pain-signal-eval-progression-gate.md:51` requires a decision record with observed pain, source evidence, current capability, chosen next step, owner, expected operating cost, and review date.
- `docs/canonical/pain-signal-eval-progression-gate.md:57` through `docs/canonical/pain-signal-eval-progression-gate.md:60` captures adjacent harness-evolution and rollback questions about prevented failures, frequency, cost, replay/A-B proof, and rollback speed.
- `docs/canonical/production-grounded-eval-sampling.md:28` through `docs/canonical/production-grounded-eval-sampling.md:52` defines production-sampled replay, baseline/candidate comparison, and reporting of quality, latency, cost, and failure-class deltas.
- `docs/canonical/eval-to-production-correlation-tracking.md:28` through `docs/canonical/eval-to-production-correlation-tracking.md:50` defines correlation tracking between eval scores, production outcomes, releases, and recalibration triggers.
- `docs/canonical/late-failure-regression-suite.md:50` through `docs/canonical/late-failure-regression-suite.md:53` references regression before canary, staged rollout, shadow diffs, canary metrics, rollback decisions, and observation windows.
- `docs/canonical/pr-gated-eval-enforcement.md:30` through `docs/canonical/pr-gated-eval-enforcement.md:43` defines baseline/candidate PR eval reports including quality, latency, cost, thresholds, failure examples, and merge policy.

**What's missing:** A canonical lifecycle that explicitly assigns every harness component to BUILD, STABILIZE, SIMPLIFY, or REMOVE, then archives removed components with reason, metrics, validation results, rollback path, and reactivation path.

**Integration value:** High

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Application-Owned Agent Control Plane | Partial Coverage | High |
| 2 | Context Working Set with Recoverable Middle | Already Exists | Low |
| 3 | Error Hygiene Recovery Loop | Already Exists | Low |
| 4 | Structured Generation and Constraint Validation Circuit | Partial Coverage | High |
| 5 | Independent Generator-Evaluator Gate | Already Exists | Low |
| 6 | Versioned Durable Agent State | Partial Coverage | High |
| 7 | Tested Degradation Ladder | Partial Coverage | High |
| 8 | Invariant-Compensation Split | Missing | High |
| 9 | Measured Harness Evolution Lifecycle | Partial Coverage | High |
