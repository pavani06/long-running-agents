---
title: "Asymmetric Failure Correction Router"
type: canonical
aliases: ["AOPD router", "asymmetric correction", "failure router", "roteador assimetrico", "sucesso vs falha", "correction channel"]
tags: ["agentes-orquestracao", "error-handling", "production"]
last_updated: 2026-06-16
relates-to:
  - "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]"
  - "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]"
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]"
  - "[[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|OPD Classification]]"
sources:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]"
---

# Asymmetric Failure Correction Router

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]]
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

An agent improvement loop treats success and failure feedback symmetrically — routing both through the same path with the same mechanics. But successes and failures have fundamentally different properties: failures have heavy-tailed gradient distributions, extreme variance, and stagnation near zero when the agent's error rate is high. Routing them through the same correction machinery either over-corrects failures (flooding the loop with noise) or under-reinforces successes (losing signal from good trajectories).

Concretely: a KODA agent handles 200 conversations per day. 75 succeed (the agent correctly identifies the issue, applies the right resolution, and the customer confirms). 25 fail (wrong product identified, incorrect policy applied, or the agent gets stuck in a retry loop). The current feedback loop sends all 100 traces through the same QA review pipeline. The 25 failure traces dominate the review queue because they generate more discussion. The 75 success traces are skimmed and discarded. After 3 months, the ops team has a rich taxonomy of failure patterns but zero systematized knowledge of what the agent does well.

The underlying mechanism mirrors AOPD from On-Policy Distillation: tokens with negative advantage exhibit heavy-tailed gradients, extreme variance, and qualitative behaviors different from positive-advantage tokens. The solution is to separate the loss into two channels — forward KL top-K for negative tokens (stable correction) and standard OPD for positive tokens (reinforcement). The same structural split applies to agent feedback: failures need repair, root-cause analysis, and regression creation; successes need exemplar capture, confidence calibration, and reduced supervision.

## Solution

Route agent performance feedback through two asymmetric channels with different mechanics: a **correction channel** for failures (repair, regression, root-cause analysis, escalation) and a **reinforcement channel** for successes (exemplars, demonstrations, confidence calibration, reduced supervision). Maintain separate learning logs for "what to correct" and "what to imitate."

```
Agent Trace + Outcome
        |
        v
[Success/Failure Classifier]
        |
   +----+----+
   |         |
[SUCCESS]  [FAILURE]
   |         |
   v         v
+--------+  +--------+
|Reinforce|  |Correct |
|Channel  |  |Channel |
+--------+  +--------+
   |         |
   v         v
Exemplars   Root Cause
Demos       Classification
Confidence  Regression Case
Calibration Repair/Retry
Reduced     Escalation
Supervision Human Review

+--------+  +--------+
|What to |  |What to |
|Imitate |  |Correct |
|Log     |  |Log     |
+--------+  +--------+
```

**Core rules:**

| Component | Requirement |
|---|---|
| Success/failure classifier | Deterministic classification: verifier rejection, constraint failure, repeated retry, confidence drop -> failure. Task completion, verifier approval, user confirmation -> success |
| Correction channel | Failure -> root cause classification, targeted repair, top-K alternatives, regression case creation, human review escalation |
| Reinforcement channel | Success -> exemplar capture, demonstration generation, confidence calibration, eligibility for reduced supervision |
| Separate learning logs | Immutable append-only logs: one for "what to imitate" (success patterns), one for "what to correct" (failure patterns with mechanisms) |
| Asymmetric mechanics | Failures never flow through the reinforcement channel; successes never trigger regression case creation. Each channel has its own processing rules |
| Severity-aware routing | Within the correction channel, severity classification (from Tested Degradation Ladder) determines retry vs. fallback vs. escalation path |

The key insight: treating failure feedback as a mirror image of success reinforcement is the root cause of improvement loop stagnation. Failures need stabilization before repair; successes need reinforcement before they're forgotten. Separate channels let each operate with its optimal mechanics.

## Implementation in this repo

### What already exists

- `Tested Degradation Ladder` [[docs/canonical/tested-degradation-ladder|tested-degradation-ladder.md:29-65]] classifies failures by severity into retryable, unsafe, and hold rungs with retry, safe fallback, human escalation, and outcome logging. This handles the correction side but does not separate success routing.
- `Failure Pattern Classification Loop` [[docs/canonical/failure-pattern-classification-loop|failure-pattern-classification-loop.md:27-45]] classifies failures into root cause classes (model ignorance, missing harness, local coherence, prompt ambiguity, context loss, model regression) and maps them to guardrail surfaces. This covers the "classify and route" aspect for failures.
- `Production Failure Regression Flywheel` [[docs/canonical/production-failure-regression-flywheel|production-failure-regression-flywheel.md:28-40]] converts production failures into eval cases — the regression creation channel for failures.
- `QA-to-Backlog Feedback Loop` [[docs/canonical/qa-to-backlog-feedback-loop|qa-to-backlog-feedback-loop.md:30-44]] routes review findings to backlog with capture, triage, conversion, and return-to-board stages.
- `Generator-Evaluator` [[docs/canonical/generator-evaluator|generator-evaluator.md:31-85]] separates Generator (creative) from Evaluator (critical), producing a binary verdict — but the evaluator does not route to asymmetric channels.
- `Constraint-Failure Decision Rule` [[docs/canonical/constraint-failure-decision-rule|constraint-failure-decision-rule.md:25-58]] classifies requirements as constraints (builder surface) vs. failure conditions (validator surface). This applies an asymmetric split to requirement types, not to agent performance feedback routing.

### What is missing

1. No explicit success-routing channel: exemplars, demonstrations, confidence calibration, reduced supervision.
2. No explicit separation between the correction channel for failures and the reinforcement channel for successes with different mechanics per channel.
3. No separate learning logs for "what to imitate" vs. "what to correct."
4. The repo has mature failure-processing infrastructure but no success-routing machinery, and no pattern that treats these as asymmetric paths.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents failure feedback from being treated as a mirror image of success reinforcement | Depends on reliable failure classification; false positives can over-route normal exploration into heavy review |
| Gives severe or high-variance failures a stabilizing path instead of repeatedly asking the same agent to self-correct | The correction channel must be tested, or it becomes another unverified fallback |
| Produces cleaner eval and backlog artifacts because every failure has a correction route | Low-risk tasks may not justify separate success and failure machinery |
| Creates institutional knowledge of both what the agent does well and what it does poorly | Maintaining two separate learning logs adds documentation surface |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] for severity classification within the correction channel.
- **Depends on:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] for root cause classification of failures before routing to specific correction surfaces.
- **Complements:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — failures enter the regression flywheel through the correction channel.
- **Complements:** [[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]] — the on-policy loop produces scored trajectories; the asymmetric router separates them into correction and reinforcement paths.
- **Complements:** [[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]] — applies the same asymmetric split philosophy (different mechanics for different signal types) at the requirement specification level.
- **Complements:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] — the evaluator provides the success/failure verdict; the router determines what happens next.
- **Feeds:** [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] — correction channel outputs become backlog items with classification metadata.

## Failure modes

- **False-positive classification:** Normal exploration or edge-case behavior is classified as failure and routed to heavy correction, wasting review cycles. Mitigation: require at least two independent failure signals (verifier rejection + confidence drop, or evaluator rejection + constraint failure) before routing through the correction channel.
- **Success blindness:** The reinforcement channel is neglected because failures are more salient. Success patterns accumulate unexamined. Mitigation: scheduled review of the "what to imitate" log; flag task classes where the success log has grown but no confidence calibration or supervision reduction has occurred.
- **Correction channel stagnation:** The correction channel becomes a dumping ground for all ambiguous outcomes, creating a growing backlog of "maybe-failures" that are never resolved. Mitigation: timeout and auto-escalation for deferred correction items; periodic review of correction channel throughput.
- **Channel crossover:** A corrected failure trace later succeeds at the same task, but the correction record is lost because the channels are separate. Mitigation: link correction and reinforcement entries by task class; track "failure -> correction -> re-test -> success" as a closed loop.

## Verification / eval hooks

- Add at least one regression or eval case before relying on this pattern in production.
- Capture the input trace, expected decision, observed decision, and evaluator/verifier output.
- Record which existing canonical pattern this one complements and which failure mode it is meant to reduce.
- Re-run the relevant eval tier after changing prompts, skills, memory policy, or harness routing.

## References

- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:110-116` — AOPD asymmetric separation between positive and negative tokens.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns.md:115-139` — extracted pattern with inputs, outputs, benefits, limitations.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification.md:165-197` — Partial Coverage classification with evidence.
- `docs/canonical/tested-degradation-ladder.md:29-65` — severity-based failure classification.
- `docs/canonical/failure-pattern-classification-loop.md:27-45` — root cause to guardrail surface mapping.
- `docs/canonical/production-failure-regression-flywheel.md:28-40` — failure to regression eval.
- `docs/canonical/constraint-failure-decision-rule.md:25-58` — asymmetric requirement classification.
