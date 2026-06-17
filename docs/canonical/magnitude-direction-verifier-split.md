---
title: "Magnitude-Direction Verifier Split"
type: canonical
aliases: ["RLSD split", "magnitude-direction", "verifier split", "magnitude direcao", "trust but verify", "confidence grounding"]
tags: ["agentes-orquestracao", "evals", "error-handling"]
last_updated: 2026-06-16
relates-to:
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]"
  - "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]"
  - "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"
  - "[[docs/canonical/two-implementations-goal-test|Two Implementations Goal Test]]"
  - "[[docs/canonical/privileged-context-self-distillation|Privileged Context Self-Distillation]]"
  - "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|OPD Classification]]"
sources:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]"
---

# Magnitude-Direction Verifier Split

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]]
**Classification:** Missing
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

An agent improvement loop faces a fundamental tension: the agent's internal signal tells you **where** change matters (which decisions the model is uncertain about, which steps carry high conviction), but the agent cannot tell you **whether** the change is correct. Self-distillation alone — updating based on the model's own confidence — produces information leakage: the agent learns to imitate the form of privileged outputs without the substance, and overconfidence compounds.

Concretely: a KODA agent's self-distillation loop identifies 12 decisions per day where the model's internal confidence delta is high — the agent "really believes" these decisions matter. The loop updates the agent's prompt rules and skills to reinforce those decisions. After 2 weeks, the agent becomes more confident on every decision, but the operations team discovers that 4 of those 12 per day are actively wrong — the agent is now more confidently making mistakes. The internal signal (magnitude) was strong, but the external signal (direction) was missing.

The underlying mechanism mirrors RLSD from On-Policy Distillation: self-distillation produces a dense per-token signal (magnitude — how much to push each token) but cannot validate the direction. A separate verifier (deterministic test, evaluator rubric, human review) provides the direction signal (positive/negative correction). The weight per update is `w_t = (P_T/P_S)^sign(A)` where the magnitude comes from self-distillation and the sign comes from the external verifier.

## Solution

Separate the agent improvement signal into two independent components: **magnitude** (where the agent believes change is important, extracted from internal confidence signals) and **direction** (whether the change should be positive reinforcement or negative correction, determined by an external verifier). Combine them into a weighted correction plan that spends effort where the agent's conviction is high and the verifier has grounded the direction. Escalate high-magnitude, uncertain-direction cases to human review.

```
Agent produces output
        |
        v
+------------------+     +------------------+
| MAGNITUDE Signal |     | DIRECTION Signal |
| (internal)        |     | (external)       |
+------------------+     +------------------+
| Where the agent   |     | Is it correct?   |
| believes change   |     |                  |
| matters:          |     | Deterministic    |
| - self-distill    |     |   test           |
|   delta           |     | Verifier rubric  |
| - log-ratio       |     | Evaluator score  |
| - attention       |     | Human review     |
|   hotspot         |     | User confirmation|
| - disagreement    |     |                  |
|   intensity       |     |                  |
+------------------+     +------------------+
        |                        |
        +-----------+------------+
                    |
                    v
    +-------------------------------+
    | Magnitude × Direction Matrix  |
    +-------------------------------+
    | Magnitude\Direction |   +1    |   -1    |   0 (uncertain) |
    |---------------------|---------|---------|----------------|
    | HIGH                | REINFORCE| CORRECT | ESCALATE       |
    | MEDIUM              | reinforce| correct | defer          |
    | LOW                 | ignore   | ignore  | ignore         |
    +-------------------------------+
                    |
                    v
+------------------+     +------------------+     +------------------+
| REINFORCE        |     | CORRECT          |     | ESCALATE         |
| Update prompts,  |     | Fix prompt rules,|     | Human reviews    |
| skills, evals    |     | add regression  |     | evidence bundle, |
| with positive    |     | case, retry with|     | decides direction |
| direction       |     | alternatives    |     |                  |
+------------------+     +------------------+     +------------------+
                    |                        |
                    v                        v
              Audit trail: magnitude evidence separated from direction evidence
```

**Core rules:**

| Component | Requirement |
|---|---|
| Magnitude extraction | Internal model signal: self-distillation delta, log-ratio, attention hotspot, disagreement intensity between sampled outputs |
| Direction signal | External verifier: deterministic test, evaluator rubric, human review, user confirmation, constraint validation |
| Weighted correction plan | Update weight = magnitude × direction; high magnitude + clear direction = strongest update |
| Escalation rule | High magnitude + uncertain direction -> human review with evidence bundle (magnitude evidence + direction ambiguity) |
| Audit trail | Separate records for confidence evidence (why the agent thought this mattered) and correctness evidence (why the verifier confirmed/rejected it) |
| Re-verification | After update, re-run the verifier to confirm the correction took effect in the intended direction |

The formalization is: **"trust but verify" as an architectural split rather than a slogan.** The agent is the best source of signal density (per-token confidence), but the worst source of correctness validation. The verifier is the best source of correctness validation, but provides sparse signal (binary or scalar, not per-token). Combining them gives dense, grounded improvement.

## Implementation in this repo

### What already exists

- `Generator-Evaluator` [[docs/canonical/generator-evaluator|generator-evaluator.md:31-85]] separates generation (where the agent "creates") from evaluation (external correctness signal). The Evaluator provides the direction signal; what's missing is the Generator's internal confidence as a magnitude signal.
- `Constraint-Anchored Evaluation` [[docs/canonical/constraint-anchored-evaluation|constraint-anchored-evaluation.md:29-56]] anchors evaluation on explicit constraint lists — external verification direction against deterministic checks.
- `Compartmented Evaluation Architecture` [[docs/canonical/compartmented-evaluation-architecture|compartmented-evaluation-architecture.md:64]] enforces separation between builder and validator surfaces — direction enforcement through architectural isolation.
- `Two Implementations Goal Test` [[docs/canonical/two-implementations-goal-test|two-implementations-goal-test.md]] validates goal specification by testing whether different implementations converge — an external verification mechanism.
- `Eval Tier Stratification` [[docs/canonical/eval-tier-stratification|eval-tier-stratification.md:26-50]] provides fast/medium/deep tiers for verification at appropriate levels.
- `Multi-Model Evaluation Council` [[docs/canonical/multi-model-evaluation-council|multi-model-evaluation-council.md:24-40]] provides diverse external direction signals through model diversity.

### What is missing

1. No extraction of internal model confidence as a magnitude signal (self-distillation delta, log-ratio, attention hotspot, disagreement intensity).
2. No combination of magnitude (where agent thinks change matters) with direction (verifier says correct/incorrect) to produce weighted correction plans.
3. No escalation rule when magnitude is high but direction is uncertain.
4. No audit trail separating confidence evidence from correctness evidence.
5. The missing mechanism is the formal "the agent is confident here (magnitude), the verifier says this is correct/incorrect (direction), therefore spend correction effort here with this weight."

## Tradeoffs

| Benefit | Cost |
|---|---|
| Formalizes "trust but verify" as an architectural split with measurable components | The verifier becomes a bottleneck; bad tests or rubrics can point confidently in the wrong direction |
| Preserves dense model signal without letting the model be the sole judge of correctness | Extra verification adds latency and operational cost per update |
| Reduces information-leakage and overconfidence risks from pure self-distillation | Conflicting magnitude and direction signals need explicit tie-breaking or human escalation |
| Creates an inspectable audit trail separating "the agent thought this mattered" from "the verifier confirmed this was correct" | Magnitude extraction methods (log-ratio, attention hotspots) are model-internal and may not be accessible in all deployment scenarios |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] for the external direction signal (the evaluator provides the +/- sign).
- **Depends on:** [[docs/canonical/privileged-context-self-distillation|Privileged Context Self-Distillation]] for the internal magnitude signal (the self-distillation delta provides the weight).
- **Validated by:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] — deterministic constraints provide the strongest direction signal.
- **Validated by:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — model diversity reduces correlated errors in the direction signal.
- **Complements:** [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] — the architectural separation enforces that magnitude and direction cannot be conflated.
- **Complements:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — fast/medium/deep tiers provide direction signals at appropriate cost levels.
- **Complements:** [[docs/canonical/two-implementations-goal-test|Two Implementations Goal Test]] — convergence of independent implementations provides high-confidence direction.

## Failure modes

- **Direction dominance:** The verifier overrides all magnitude signals, turning the weighted correction plan into a binary "verifier says pass/fail." The dense agent signal is lost. Mitigation: weight the magnitude signal even when direction is clear; high-magnitude updates should receive more scrutiny, not less.
- **Magnitude leakage:** The agent learns to inflate its internal confidence signal (gaming the magnitude) to receive more correction weight, without actually improving. Mitigation: cross-validate magnitude against out-of-distribution task performance; decaying magnitude on tasks that show no actual improvement.
- **Verifier bottleneck:** All updates queue behind the verifier, which becomes the rate-limiter for the entire improvement loop. Mitigation: tiered verification (fast tier for low-magnitude updates, deep tier for high-magnitude updates); batch verification for related changes.
- **Escalation queue overflow:** High-magnitude, uncertain-direction cases accumulate faster than humans can review them. Mitigation: timeout and auto-defer for cases where direction uncertainty persists beyond N review cycles; flag the task class, not the individual case.

## Verification / eval hooks

- Add at least one regression or eval case before relying on this pattern in production.
- Capture the input trace, expected decision, observed decision, and evaluator/verifier output.
- Record which existing canonical pattern this one complements and which failure mode it is meant to reduce.
- Re-run the relevant eval tier after changing prompts, skills, memory policy, or harness routing.

## References

- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:126-132` — RLSD split between magnitude and direction.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns.md:140-164` — extracted pattern with inputs, outputs, benefits, limitations.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification.md:200-234` — Missing classification with evidence.
- `docs/canonical/generator-evaluator.md:31-85` — external evaluation direction via separate agent.
- `docs/canonical/constraint-anchored-evaluation.md:29-56` — external constraint verification.
- `docs/canonical/compartmented-evaluation-architecture.md:64` — builder/validator surface separation.
- `docs/canonical/eval-tier-stratification.md:26-50` — verification at appropriate tiers.
