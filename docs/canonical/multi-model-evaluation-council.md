---
title: "Multi-Model Evaluation Council"
type: canonical
tags: ["evals", "agentes-orquestracao"]
aliases: ["model-diverse evaluator council", "evaluation council", "multi-model judging"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]"]
sources: ["[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Agentic Patterns from Stanford CS153 AI Native Company]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Classification: Stanford CS153 AI Native Company Patterns]]"]
---
# Multi-Model Evaluation Council

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/
**Classification:** Partial Coverage, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

A single model judge can turn evaluation into a mirror of one model family's preferences and blind spots. Even when the rubric is strong, one evaluator can miss failure modes that another model would catch, over-reward outputs that match its own style, or under-report uncertainty.

High-risk agent outputs need evaluator plurality that is not only multiple calls to the same judge, but a council with model diversity, independent scoring, disagreement handling, and calibration against real outcomes.

## Solution

Use a model-diverse evaluation council for high-value decisions, risky agent behavior changes, ambiguous rubric cases, and production-impacting releases.

Council mechanics:

| Component | Requirement |
|---|---|
| Model diversity | Use evaluators from meaningfully different model families, sizes, or providers when available |
| Shared rubric | Every evaluator receives the same task, evidence bundle, scoring scale, and disallowed shortcuts |
| Independent first pass | Evaluators score before seeing each other's judgments |
| Aggregation policy | Convert independent scores into pass, fail, retry, needs-human, or needs-rubric-update |
| Disagreement policy | Escalate when score spread, blocker disagreement, or rationale conflict crosses a threshold |
| Calibration loop | Compare council outcomes to human review, production outcomes, incidents, and later regression data |

Recommended aggregation rules:

1. Use the strictest blocker result when any evaluator finds safety, correctness, or policy failure with evidence.
2. Use median or trimmed mean for scalar quality scores when no blocker is present.
3. Treat high variance as signal, not noise; route divergent cases to human review or rubric clarification.
4. Feed disagreement examples back into eval cases, rubric wording, and model-selection policy.
5. Reserve council mode for medium or deep eval tiers where latency and cost are justified.

## Implementation in this repo

### What already exists

The repo already teaches evaluator plurality and escalation:

- Evaluation coordination includes Dual/Ensemble Evaluator and Continuous Calibration Loop in [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]:156-164.
- Dual/Ensemble Evaluator means two or more evaluators apply the same rubric independently, compare scores, escalate divergence, and reserve ensemble evaluation for high-value decisions in [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]:162-166.
- The detailed graph documentation represents Dual/Ensemble Evaluator with independent evaluators, score comparison, high-value financial decisions, and divergence tolerance in [[curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs|Evaluation Rubrics Graphs]]:827.
- Human review calibrates rubrics, audits gray-zone cases, and reviews evaluator divergences in [[curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs|Evaluation Rubrics Graphs]]:1660.

### What is missing

The Partial Coverage gap is model diversity and council governance. The repo has multiple evaluator roles, but the classification found no formal Multi-Model Evaluation Council, no required evaluator model diversity, no model-specific blind-spot calibration, and no council aggregation policy outside the current Stanford pattern file in [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|classification]]:109-122.

Missing implementation details:

1. A model-selection policy for evaluator diversity.
2. Council aggregation rules for pass/fail, blocker handling, and score variance.
3. Disagreement thresholds that trigger retry, human review, or rubric updates.
4. Calibration records that tie model-specific judgments to production outcomes.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Reduces dependence on one evaluator model's preferences | Increases latency and model cost |
| Surfaces disagreement before risky outputs ship | Aggregation policy can become complex |
| Gives reviewers richer qualitative critique | Multiple models can still share benchmark blind spots |
| Creates calibration data about evaluator reliability | Requires outcome tracking to avoid eval theater |

## Relationship to Other Patterns

- **Uses:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] to decide when council mode is worth the cost.
- **Feeds:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] by attaching model-diverse council summaries to risky PRs.
- **Calibrated by:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]], because council quality must be measured against real outcomes.
- **Strengthened by:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]], which gives the council representative cases instead of synthetic examples only.
- **Builds on:** [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]] dual/ensemble evaluator guidance.
- **Comes from:** [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]]:140-159 and its Partial Coverage classification in [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|classification]]:109-122.

## References

- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|patterns]]:140-159 - extracted pattern definition.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|classification]]:109-122 - Partial Coverage classification and model-diversity gap.
- [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]:156-164 - existing evaluation coordination strategies.
- [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]]:162-166 - existing dual/ensemble evaluator guidance.
- [[curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs|Evaluation Rubrics Graphs]]:827 - graph evidence for independent evaluator comparison.
- [[curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs|Evaluation Rubrics Graphs]]:1660 - human calibration and divergence review.

---

*Created: 2026-06-10 | From: Stanford CS153 pattern classification | Precedence: canonical*
