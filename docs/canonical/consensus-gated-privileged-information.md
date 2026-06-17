---
title: "Consensus-Gated Privileged Information"
type: canonical
aliases: ["consensus gate", "gated PI", "GATES pattern", "privileged info gate", "consenso em informacao privilegiada", "gate de confianca"]
tags: ["agentes-orquestracao", "evals", "error-handling", "curriculo-conteudo"]
last_updated: 2026-06-16
relates-to:
  - "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]"
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]"
  - "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]"
  - "[[docs/canonical/privileged-context-self-distillation|Privileged Context Self-Distillation]]"
  - "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|OPD Classification]]"
sources:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]"
---

# Consensus-Gated Privileged Information

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]]
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

An agent receives privileged information from multiple sources — retrieved documents, sub-agent findings, generated plans, reference answers — and treats every signal as equally trustworthy. When one source is wrong (stale document, hallucinated sub-agent output, inaccurate plan), that error propagates into the agent's decisions, prompts, skills, or memory without any gate. A single wrong retrieved document can poison every subsequent turn of a 30-step agent session.

Concretely: a KODA agent handling an order modification retrieves the product return policy from the knowledge base. The retrieved document is from an outdated cache and states a 7-day return window when the actual policy is 30 days. The agent enforces the 7-day limit across 4 turns. The customer escalates. The root cause is not the agent's reasoning — it's that no mechanism validated the retrieved information before the agent acted on it.

The underlying mechanism mirrors the GATES method from On-Policy Distillation: privileged information is only trusted when multiple independent tutor rollouts agree above a threshold. The consensus gate prevents noisy privileged information from being promoted into prompts, skills, or memory. The repo's `Multi-Model Evaluation Council` applies this exact pattern to evaluation outputs, but does not generalize it to all privileged information.

## Solution

Generalize the consensus gate to apply to any privileged information candidate before it influences the agent. For each candidate (retrieved document, sub-agent finding, generated plan, reference answer), run multiple independent evaluator/tutor passes. Accept the information only when independent rollouts agree above a configurable trust threshold. Record the consensus evidence, dissenting outputs, and escalation path in an audit record.

```
Candidate PI:  [Retrieved Doc] [Sub-agent Finding] [Generated Plan] [Reference Answer]
                        |
            +-----------+-----------+
            |                       |
    [Evaluator Pass 1]     [Evaluator Pass 2]     ... [Evaluator Pass N]
            |                       |
            +-----------+-----------+
                        |
                  Agreement Metric
                  (exact match, rubric agreement, semantic consensus, conflict count)
                        |
            +-----------+-----------+
            |           |           |
      [ACCEPT]     [DEFER]     [REJECT]
      consensus    weak        no agreement
      > threshold  consensus   or conflict
            |           |           |
            v           v           v
      Trusted PI   Pending       Escalated to
      enters       re-eval       human review
      agent loop   or more       with audit
                   passes        record
```

**Core rules:**

| Component | Requirement |
|---|---|
| Evaluator diversity | Multiple independent passes with different evaluator configurations (models, rubrics, or perspectives) |
| Agreement metric | Exact answer match, rubric score agreement, semantic consensus, or conflict count |
| Trust threshold | Configurable minimum agreement level required to accept PI (e.g., 2 of 3 agree, or mean score > 0.8) |
| Audit record | Document accepted/rejected/deferred status per PI candidate, with rationale, dissenting outputs, and consensus evidence |
| Escalation path | When consensus is weak or conflicting, route to human review with the evidence bundle attached |
| PI categories | Retrieved documents, sub-agent findings, generated plans, reference answers, teacher traces, tool outputs |

The key generalization: the repo already gates evaluation outputs with model diversity and consensus thresholds (`Multi-Model Evaluation Council`). This pattern extends that gate to all privileged information — not just eval results, but any signal the agent would otherwise trust blindly.

## Implementation in this repo

### What already exists

- `Multi-Model Evaluation Council` [[docs/canonical/multi-model-evaluation-council|multi-model-evaluation-council.md:24-40]] gates evaluation outputs with model diversity, independent first passes, aggregation policy (pass/fail/retry/needs-human), disagreement thresholds, and calibration against real outcomes. This is structurally identical to consensus-gated PI but scoped to evaluation results.
- `Generator-Evaluator` [[docs/canonical/generator-evaluator|generator-evaluator.md:31-85]] separates generation from evaluation and routes rejected output back with feedback — a two-agent consensus on output quality.
- `Shadow Review Pipeline` [[docs/canonical/shadow-review-pipeline|shadow-review-pipeline.md:27-31]] runs AI review in parallel with human review, collecting agreement metrics before graduating AI checks to blocking status.
- `Split-Brain Planning Review` [[docs/canonical/split-brain-planning-review|split-brain-planning-review.md:26-41]] separates engineering and product-destination reviews with independent rubrics before reconciliation — independent consensus passes on planning.
- `Dual/Ensemble Evaluator` in the curriculum [[curriculum/05-core-concepts/08-evaluation-rubrics|evaluation-rubrics.md:156-164]] requires two or more independent evaluators, score comparison, divergence escalation.

### What is missing

1. The consensus gate is scoped only to evaluation outputs, not to the broader class of privileged information (retrieved documents, generated plans, sub-agent findings, reference answers).
2. No trust threshold for accepting candidate privileged information into prompts, skills, or memory.
3. No audit record of dissenting outputs with accepted/rejected/deferred classifications for PI candidates.
4. No escalation path when consensus is weak on privileged information specifically (as opposed to evaluation results).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Filters noisy retrieved context before it is promoted into prompts, skills, plans, or memory | Adds latency and token cost through repeated evaluator or tutor calls |
| Maps naturally to multi-agent review councils where agreement is a gate, not a decoration | Correlated agents or evaluators can agree on the same wrong answer |
| Makes trust in privileged information explicit and inspectable via audit records | High-value minority dissent may be lost if the consensus rule is too strict |
| Reuses the same council mechanics already proven for evaluation outputs | Each PI category may need different agreement metrics (semantic consensus for docs, exact match for reference answers) |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] for the council mechanics (model diversity, independent scoring, aggregation, disagreement policy).
- **Depends on:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] for the separate-generation-from-evaluation foundation.
- **Complements:** [[docs/canonical/privileged-context-self-distillation|Privileged Context Self-Distillation]] — the consensus gate validates privileged information before self-distillation converts it to runtime knowledge.
- **Complements:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] — shadow agreement metrics are the calibration mechanism for consensus thresholds.
- **Complements:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] — independent review passes on planning outputs are a specific application of consensus-gated PI.
- **Feeds:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — consensus gate failures on PI should be classified by root cause mechanism.

## Failure modes

- **Correlated evaluators:** Two evaluators using the same model with different prompts may agree on the same wrong answer. Mitigation: enforce evaluator diversity — different models, different rubrics, or different perspectives.
- **Consensus too strict:** Setting the trust threshold too high rejects valid information that happens to produce varied but correct outputs. Mitigation: calibrate thresholds per PI category; retrieved documents may need looser semantic consensus than reference answers.
- **Consensus too loose:** Setting the threshold too low accepts information that evaluators agree on superficially but that contains subtle errors. Mitigation: require at least one evaluator pass that explicitly checks for factual accuracy, not just agreement.
- **Audit blind spot:** Dissenting outputs are recorded but never reviewed, so systematic evaluator biases accumulate undetected. Mitigation: scheduled review of audit records; flag PI categories with high defer/reject rates for root-cause analysis.

## Verification / eval hooks

- Add at least one regression or eval case before relying on this pattern in production.
- Capture the input trace, expected decision, observed decision, and evaluator/verifier output.
- Record which existing canonical pattern this one complements and which failure mode it is meant to reduce.
- Re-run the relevant eval tier after changing prompts, skills, memory policy, or harness routing.

## References

- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:72-85` — PI taxonomy as confidence spectrum and GATES consensus mechanism.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns.md:90-114` — extracted pattern with inputs, outputs, benefits, limitations.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification.md:133-163` — Partial Coverage classification with evidence.
- `docs/canonical/multi-model-evaluation-council.md:24-40` — council mechanics with model diversity, independent scoring, aggregation, disagreement.
- `docs/canonical/generator-evaluator.md:31-85` — generator/evaluator rejection loop.
- `docs/canonical/shadow-review-pipeline.md:27-31` — shadow period with agreement metrics.
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:156-164` — dual/ensemble evaluator.
