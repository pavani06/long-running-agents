---
title: "Autonomy Curriculum Sampling"
type: canonical
aliases: ["autonomy curriculum", "curriculo de autonomia", "autonomy mix", "teacher-mixed sampling", "lambda dial", "observe assist own"]
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness", "evals"]
last_updated: 2026-06-16
relates-to:
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]"
  - "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]"
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]"
  - "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|OPD Classification]]"
  - "[[curriculum/README|Curriculum Overview]]"
sources:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]"
---

# Autonomy Curriculum Sampling

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]]
**Classification:** Missing
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

An agent deployed in production jumps from zero autonomy to full autonomy in a single step. Either a human reviews every action (wasting time on routine tasks the agent handles well), or the agent operates unsupervised (producing unusable traces when its loop isn't stable for that task class). There is no middle ground — no gradual handover, no phase where the agent observes, then assists, then owns.

Concretely: a KODA agent handles 150 product inquiries per day. For the "view order status" task family, the agent achieves 98% accuracy after 3 weeks of human supervision. For the "modify multi-item order with conflicting constraints" task family, the agent achieves 34% accuracy. The operations team has no mechanism to grant autonomy for the first task family while keeping human-in-the-loop for the second. The result: either blanket supervision (costly) or blanket autonomy (risky).

The underlying mechanism mirrors Teacher-Mixed Sampling from On-Policy Distillation: pure student rollouts are low-quality early in training, so the training curriculum mixes teacher demonstrations with student-generated data, controlled by a single lambda parameter. As the student stabilizes, lambda shifts from teacher-heavy to student-heavy. The same concept applies to operational agent autonomy: start with human demonstrations, then progressively increase the agent's self-generated work using an explicit schedule with readiness gates per task class.

## Solution

Define an explicit autonomy curriculum that maps each task class or agent capability to an autonomy phase — observe, assist, or own — with a single lambda parameter controlling the mix of supervised vs. autonomous execution, and readiness gates that gate transitions with objective metrics.

```
Autonomy Lambda: 0.0 (full supervision)  ------------------->  1.0 (full autonomy)

Phase:          OBSERVE                  ASSIST                    OWN
Lambda range:   [0.0 -- 0.3]           [0.3 -- 0.7]            [0.7 -- 1.0]
Mechanic:       Human does,             Agent proposes,          Agent executes,
                agent watches            human approves           human monitors exceptions
```

**Core rules:**

| Component | Requirement |
|---|---|
| Lambda parameter | Single autonomy mix dial (0.0 = full human, 1.0 = full agent) per task class |
| Task class registry | Catalog of task families with current autonomy phase, lambda value, and metrics |
| Readiness gates | Per-phase metrics that must pass before advancing lambda: task success rate, repair rate, unsafe-action rate, evaluator confidence |
| Schedule policy | Rules for when to increase lambda: time-in-phase, metric thresholds, stability window |
| Phase progression | Observe (human does, agent watches) -> Assist (agent proposes, human approves) -> Own (agent executes, human monitors exceptions) |
| Regression trigger | Lambda rollback rule when metrics degrade: if success rate drops below threshold for N consecutive windows, reduce lambda to previous stable level |

The key insight from On-Policy Distillation literature: **autonomy should be a dial, not a switch**. The lambda parameter creates one visible control that replaces the implicit binary jump from "manual operation" to "full agent ownership." Each task class can have a different lambda, reflecting the reality that agents master some tasks faster than others.

## Implementation in this repo

### What already exists

- `Measured Harness Evolution Lifecycle` [[docs/canonical/measured-harness-evolution-lifecycle|measured-harness-evolution-lifecycle.md:29-62]] defines BUILD -> STABILIZE -> SIMPLIFY -> REMOVE stages for harness components. This is a progression from defense to removal, structurally similar to an autonomy progression but operating on harness components rather than agent autonomy.
- `Domain-Embedded Workflow Automation Wedge` [[docs/canonical/domain-embedded-workflow-automation-wedge|domain-embedded-workflow-automation-wedge.md:48-71]] requires validation before broad rollout, which is a readiness gate concept applied to deployment rather than agent autonomy.
- `Resolver-Based Context Progressive Disclosure` [[docs/canonical/resolver-based-context-progressive-disclosure|resolver-based-context-progressive-disclosure.md]] loads skills progressively by trigger, sharing the "progressive increase" structure.
- The curriculum itself [[curriculum/README|curriculum/README.md:192-247]] defines a 4-level progression (N1 fundamentals -> N4 production), which is a learning curriculum — adjacent in spirit but designed for human students, not operational agent autonomy.
- `Tested Degradation Ladder` [[docs/canonical/tested-degradation-ladder|tested-degradation-ladder.md:29-65]] classifies failure severity with retry, fallback, and escalation paths — relevant for the regression trigger when autonomy degrades.
- `Pain-Signal Eval Progression Gate` [[docs/canonical/pain-signal-eval-progression-gate|pain-signal-eval-progression-gate.md:51-60]] uses observed pain, evidence, and review dates to gate eval tooling progression — structurally analogous to readiness gates for autonomy.

### What is missing

1. No autonomy mix parameter (lambda) that controls the proportion of human-supervised vs. agent-owned execution per task class.
2. No readiness gates with objective metrics (success rate, repair rate, unsafe-action rate, evaluator confidence) that control when the agent can advance from observe to assist to own.
3. No schedule policy for increasing lambda based on time-in-phase and metric stability.
4. No regression trigger that rolls back lambda when post-transition metrics degrade.
5. The repo has "assist" operations (shadow review, human-in-the-loop gates) but does not map them to a graduated autonomy dial with explicit phases.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Replaces implicit binary jump with one visible autonomy dial per task class | Requires tuning the schedule per task class; too slow hides autonomy failures, too fast floods the loop with noise |
| Keeps the agent exposed to its own mistakes as soon as those mistakes become learnable | Demonstrations can overfit the agent to expert paths and reduce exploration |
| Reduces cold-start collapse by avoiding pure autonomous rollouts before the agent can recover from basic errors | Readiness metrics must be task-specific enough to avoid promoting brittle autonomy |
| Creates a shared language (observe/assist/own) that operations, engineering, and product teams can align on | Requires ongoing metric monitoring and regression detection infrastructure |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] for the evaluator that scores agent proposals in the Assist phase.
- **Depends on:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] for severity classification when autonomy regressions trigger lambda rollback.
- **Complements:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — harness components move through BUILD/STABILIZE/SIMPLIFY/REMOVE; agent autonomy moves through observe/assist/own. Both are graduated progressions with metrics and gates.
- **Complements:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] — the wedge validates before broad rollout; the autonomy curriculum gates each step of the handover.
- **Complements:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — both use observed metrics, evidence, and review dates to gate progression.
- **Cross-reference:** [[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]] — the feedback loop captures agent rollouts as learning data; the autonomy curriculum controls the mix of when those rollouts are supervised vs. autonomous.

## Failure modes

- **Brittle autonomy promotion:** Readiness gates pass during a quiet period but fail under real load. Mitigation: require stability over a minimum observation window (e.g., 14 days with consistent traffic) before advancing lambda.
- **Schedule overfitting:** A single lambda schedule applied uniformly across all task classes promotes some too fast and others too slow. Mitigation: per-task-class lambda with independent readiness gates.
- **Expert overfitting:** Heavy teacher demonstrations in the Observe phase cause the agent to mimic expert paths without learning recovery strategies. Mitigation: introduce controlled failure scenarios in the Assist phase where the agent must recover from known errors.
- **Metric divergence:** Success rate in the Assist phase (where a human approves proposals) may not predict success rate in the Own phase (where the agent acts without approval). Mitigation: use shadow mode — run the agent autonomously in parallel during Assist and compare outcomes.

## Verification / eval hooks

- Add at least one regression or eval case before relying on this pattern in production.
- Capture the input trace, expected decision, observed decision, and evaluator/verifier output.
- Record which existing canonical pattern this one complements and which failure mode it is meant to reduce.
- Re-run the relevant eval tier after changing prompts, skills, memory policy, or harness routing.

## References

- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:90-96` — teacher-mixed sampling as bridge between off-policy and on-policy.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns.md:40-64` — extracted pattern with inputs, outputs, benefits, limitations.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification.md:71-98` — Missing classification with evidence.
- `docs/canonical/measured-harness-evolution-lifecycle.md:29-62` — adjacent progression stages for harness components.
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:48-71` — validation before broad rollout.
- `curriculum/README.md:192-247` — 4-level learning curriculum progression.
