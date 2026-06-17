---
title: "On-Policy Rollout Feedback Loop"
type: canonical
aliases: ["OPD loop", "on-policy loop", "rollout feedback", "loop de feedback on-policy", "exposure bias gap"]
tags: ["agentes-orquestracao", "evals", "production"]
last_updated: 2026-06-16
relates-to:
  - "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]"
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]"
  - "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]"
  - "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/asymmetric-failure-correction-router|Asymmetric Failure Correction Router]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|OPD Classification]]"
sources:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]"
---

# On-Policy Rollout Feedback Loop

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]]
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

An agent trained or evaluated only on curated scripts breaks when its own production trajectories contain early mistakes, strange tool outputs, or context drift that never appeared in the static data. This is the exposure-bias gap: the agent's inference distribution differs from the training distribution, and the gap compounds over long trajectories.

Concretely: a KODA agent receives a product inquiry. In production, it misidentifies the product category on step 2 due to an ambiguous user message. The remaining 8 steps operate on this wrong assumption, generating tool calls, context lookups, and conversation turns that no curated eval set anticipated. The agent's pass@1 on benchmark evals is 94%, but its production success rate on 10+ step workflows is 62% — because every real trajectory prefix is "off-distribution" after the first error.

The underlying mechanism mirrors On-Policy Distillation in ML: off-policy training uses teacher-generated prefixes that never contain errors, so the student never learns to recover. In agent systems, the same gap exists between hand-authored eval scripts and runtime agent trajectories. The failure compounds quadratically — O(eT^2) — because each wrong step pushes the next step further from anything the agent was evaluated against.

## Solution

Close the exposure-bias gap by making the agent's own production trajectories the learning signal. When an agent executes a task, capture the full trace — decisions, tool calls, tool results, context snapshots, and the final outcome. Score the agent's own prefixes using a teacher, evaluator, verifier, or human review signal. Feed those scored prefixes back as update targets: prompt rules, skills, eval cases, memory policy, or training data. Then re-run the task against the updated agent and measure whether performance improved.

```
+------------------+     +--------------------+     +--------------------+
| Production-like  | --> | Agent Rollout      | --> | Teacher/Evaluator  |
| prompt / task    |     | y ~ agent(x)       |     | scores agent's own |
+------------------+     +--------------------+     | prefixes           |
                                                     +--------+-----------+
                                                              |
                                    +-------------------------+
                                    v
+------------------+     +--------------------+     +--------------------+
| Re-run           | <-- | Update targets:    | <-- | Scored prefixes +  |
| verification     |     | prompts, skills,   |     | trajectory trace   |
| with updated     |     | evals, memory,     |     +--------------------+
| agent            |     | training data      |
+------------------+     +--------------------+
```

**Core rules:**

| Component | Requirement |
|---|---|
| Rollout capture | Full trajectory trace: agent decisions, tool calls, tool results, errors, context snapshots at each step |
| Scoring | Teacher, evaluator, verifier, or human review signal over the agent's own prefixes — not over an idealized trace |
| Update targets | Prompt rules, skills, eval cases, memory policy, or fine-tuning data derived from scored prefixes |
| Verification | Re-run the same task against the updated agent to confirm the feedback improved behavior |
| Privacy & safety | Filters for secrets, personal data, credentials before production traces become learning data |

The critical distinction from existing regression patterns: this loop **samples from the agent's on-policy distribution** — its actual decisions, not the ideal ones. The production-grounded eval sampling captures traces for replay comparison, and the regression flywheel converts failures into eval cases, but neither feeds the agent's own prefixes back as scored update targets with re-run verification.

## Implementation in this repo

### What already exists

- `Production-Grounded Eval Sampling` [[docs/canonical/production-grounded-eval-sampling|production-grounded-eval-sampling.md:28-52]] captures production interactions, agent traces, tool results, and state snapshots for replay against baseline and candidate versions. This provides the sampling infrastructure.
- `Production Failure Regression Flywheel` [[docs/canonical/production-failure-regression-flywheel|production-failure-regression-flywheel.md:28-40]] converts every production failure into a durable eval regression case with trace, labels, tier assignment, and deduplication. This handles the regression output.
- `QA-to-Backlog Feedback Loop` [[docs/canonical/qa-to-backlog-feedback-loop|qa-to-backlog-feedback-loop.md:24,50]] formalizes review findings as backlog inputs, converting observations into concrete issues.
- `Closed-Loop Agent OS` [[docs/canonical/closed-loop-agent-operating-system|closed-loop-agent-operating-system.md:32-45]] includes feedback writeback as an OS surface: outcomes become trusted future memory.
- `Eval to Production Correlation Tracking` [[docs/canonical/eval-to-production-correlation-tracking|eval-to-production-correlation-tracking.md:50-76]] ties eval scores to production outcomes, providing the directional signal.
- `Generator-Evaluator` [[docs/canonical/generator-evaluator|generator-evaluator.md:31-85]] separates generation from evaluation with feedback loop — the teacher/evaluator role.

### What is missing

1. No mechanism runs the agent on production-like prompts, captures the agent's own prefixes (its actual decisions, not the ideal ones), scores those prefixes with a teacher/evaluator, and feeds the scored prefixes back as update targets.
2. No explicit "rollout -> score on own prefixes -> update targets -> re-run verification" loop bridges the gap between the sampling infrastructure and the regression flywheel.
3. No distinction between curated eval examples and on-policy trajectories as qualitatively different learning signals with different update strategies.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Closes the exposure-bias gap between curated examples and messy runtime trajectories | Rollouts are expensive and can be low quality early in the agent lifecycle |
| Turns production drift, failed tool calls, and late-session context errors into high-value learning data | Requires privacy, safety, and sampling controls before production traces become learning data |
| Makes compounding errors visible before they become silent cascades in long workflows | Needs a reliable evaluator; otherwise the loop converts runtime noise into training noise |
| Produces update targets that reflect the agent's actual inference distribution, not an idealized one | Updating prompts, skills, or evals from on-policy traces can introduce regressions if not verified |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] for trace capture and replay infrastructure.
- **Depends on:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] for the teacher/evaluator that scores agent prefixes.
- **Feeds:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] by converting on-policy failure prefixes into durable eval cases.
- **Feeds:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] by providing outcome-labeled trajectory data for correlation analysis.
- **Complements:** [[docs/canonical/asymmetric-failure-correction-router|Asymmetric Failure Correction Router]] by separating the success-routing and failure-routing paths that the on-policy loop produces.
- **Complements:** [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] by providing scored trajectory evidence for backlog item generation.
- **Cross-reference:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] covers the related but distinct problem of classifying failures by root cause mechanism. The on-policy loop addresses the upstream problem: ensuring the agent sees its own failures as learning data, not just an idealized curriculum.

## Failure modes

- **Cold-start collapse:** Early agent rollouts produce unusable traces. Mitigation: start with teacher-mixed sampling (alpha * teacher + (1-alpha) * student) and gradually increase student proportion as the agent stabilizes.
- **Prefix drift:** An early error pushes the trajectory outside the evaluator's support, and all subsequent scoring becomes noise. Mitigation: detect prefix drift early and re-anchor to a known-good prefix before scoring.
- **Information leakage:** The teacher/evaluator's scoring signal leaks privileged information (full logs, reference answers) that won't be available in production. Mitigation: calibrate under the runtime view, not the teacher view.
- **Proxy metric divergence:** Per-step scores may diverge from trajectory-level success, especially in long workflows. Mitigation: score at the trajectory level, not per-step; use trajectory-level success as the primary metric.

## Verification / eval hooks

- Add at least one regression or eval case before relying on this pattern in production.
- Capture the input trace, expected decision, observed decision, and evaluator/verifier output.
- Record which existing canonical pattern this one complements and which failure mode it is meant to reduce.
- Re-run the relevant eval tier after changing prompts, skills, memory policy, or harness routing.

## References

- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:33-53` — on-policy loop definition and exposure bias gap.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns.md:15-39` — extracted pattern with inputs, outputs, benefits, limitations.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification.md:39-69` — Partial Coverage classification with evidence.
- `docs/canonical/production-grounded-eval-sampling.md:28-52` — production trace capture and replay.
- `docs/canonical/production-failure-regression-flywheel.md:28-40` — failure to durable eval regression.
- `docs/canonical/generator-evaluator.md:31-85` — generator/evaluator separation with feedback loop.
