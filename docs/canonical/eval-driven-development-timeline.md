---
title: "Eval-Driven Development Timeline (Model-Selection-Last)"
type: canonical
aliases: ["eval driven timeline", "model selection last", "eval first timeline", "6-week eval infrastructure"]
tags: ["evals", "production", "agentes-orquestracao"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]", "[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]"]
sources: []
---
# Eval-Driven Development Timeline (Model-Selection-Last)

**Type:** canonical
**Status:** active
**Source:** The Production AI Playbook (Bhaumik, Databricks)
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Model selection decisions made before evaluation infrastructure exists are based on intuition and public benchmarks (MMLU, HumanEval), not on domain-specific performance. This leads to weeks of subjective debate over which model is "better" — debates that have no empirical resolution because the evaluation machinery that could answer them does not yet exist. Teams commit to a model based on hype, then build eval infrastructure later to validate a decision already made.

The timeline order matters: build the evaluation system first, then use it to select the model. Inverting this sequence (model first, eval later) produces model lock-in without evidence and eval infrastructure that is accidentally tuned to the chosen model's quirks rather than to the domain's requirements.

## Solution

Invest 6 weeks in evaluation infrastructure before any model experimentation or selection. The timeline is deliberately inverted from conventional development: evaluation is the first thing built, not the last.

### Phase 1 — Evaluation Infrastructure (Weeks 1-6)

Build the three-layer evaluation architecture ([[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]) and the living eval dataset ([[docs/canonical/living-eval-dataset|Living Eval Dataset]]) before touching model selection:

| Week | Activity | Output |
|---|---|---|
| 1-2 | Data foundation: centralized tracing across all agent frameworks, capture of real production queries with human agent responses | Trace pipeline operational; initial ~200 queries captured |
| 3-4 | Golden answers: domain experts author correct responses for the initial ~200 queries; build the living eval dataset with categorization taxonomy | Golden answer dataset with per-category ownership |
| 5 | Layer 1 (Deterministic): regex, schema, PII detection evaluation pipeline | Layer 1 operational on every PR |
| 6 | Layer 2 (Semantic): LLM-as-Judge evaluation pipeline with rubric dimensions (groundedness, safety, faithfulness, relevance) | Layer 2 operational on merge; baseline scores established |

### Phase 2 — Model Selection (Weeks 7-8)

Only after the eval infrastructure exists and the baseline dataset is ready:

1. **Run candidate models against the eval dataset.** Every candidate model (any provider, any version) is evaluated against the same domain-specific dataset with the same rubric.
2. **Produce a data-driven comparison report.** Ranking all candidates by Layer 1 pass rate, Layer 2 quality scores, and (when Layer 3 is operational) per-query cost profile.
3. **Select based on domain performance, not public benchmarks.** The model that performs best on your data, your domain, your failure patterns wins — not the model with the highest MMLU score.

### Phase 3 — Continuous Validation (Ongoing)

The eval dataset that selected the model also serves as the regression suite for every subsequent change:

- **Prompt changes:** Run the eval dataset before deploy; quantify the impact on quality.
- **Model provider updates:** When a provider releases a new model version, re-run the comparison. The update is safe to adopt only if it maintains or improves scores.
- **Model switching:** Architecture should support switching models mechanically — run new model against eval dataset, compare scores, decide (switch/hold/hybrid).

### Model-Selection-Last Principle

The core reversal: model selection is the **last** decision in the build sequence, not the first. This eliminates subjective model debates (“GPT-5 vs. Claude 5 vs. Gemini 3”) and replaces them with hours of data-driven comparison. The same eval dataset that answers “which model?” also answers “is this prompt change safe?” and “should we adopt the model provider's update?”

## Implementation in this repo

### What already exists

The repo has the philosophical foundation for evidence-driven progression, though implemented through a pain-signal-driven gate rather than a calendar-driven timeline:

- **pain-signal-eval-progression-gate** (`docs/canonical/pain-signal-eval-progression-gate.md:28`) captures the core principle: invest in eval infrastructure driven by real failure signals, not calendar planning. The trigger mapping table links specific pain signals (user complaints, manual review bottlenecks, escaped edge cases) to minimum eval capabilities (spot-check sets, tier stratification, production sampling, regression flywheel).
- **Harness evolution practices** (`docs/canonical/measured-harness-evolution-lifecycle.md`) ask "which concrete failure does this prevent?" before investing in any harness component — the same evidence-first philosophy.
- **production-grounded-eval-sampling** (`docs/canonical/production-grounded-eval-sampling.md:28`) defines the data pipeline for capturing real production interactions, applying privacy filters, labeling expected behavior, and maintaining replay infrastructure — covering the data foundation weeks (1-2) of the timeline.
- **repeatable-agent-spot-check-set** (`docs/canonical/repeatable-agent-spot-check-set.md`) provides a seed of repeatable cases that can bootstrap the living eval dataset.
- **neutral-selection-layer** (`docs/canonical/neutral-selection-layer.md:28`) defines model-agnostic context format and vendor adapter — the architectural foundation for model switching.
- **llm-as-fuzzy-compiler** (`docs/canonical/llm-as-fuzzy-compiler.md:27`) treats models as swappable compiler backends and generated code as disposable — the philosophical alignment with model-selection-last.
- **Multi-model operation** is demonstrated in practice: the runtime uses DeepSeek for the orchestrator, Anthropic for momus/adversarial review, demonstrating practical multi-model architecture.

### What is missing

The specific 6-week infrastructure-first timeline with model-selection-last as an explicit named strategy is not formalized:

1. **The calendar-driven 6-week timeline is rejected by the repo's philosophy.** The repo's pain-signal-eval-progression-gate explicitly rejects calendar roadmaps in favor of evidence-gated progression — "treat eval maturity as a gate driven by pain signals instead of a calendar roadmap." The repo would not adopt a fixed 6-week schedule but would endorse the sequence (eval infrastructure before model selection) when the pain signals justify it.

2. **"Model selection last" is not named as an explicit strategy.** The concept exists implicitly: neutral-selection-layer enables model switching, llm-as-fuzzy-compiler treats models as disposable, multi-model-council uses model diversity. But "select the model last, after the eval dataset proves which model performs best on your domain" is NOT_FOUND as an explicit decision principle.

3. **No side-by-side model comparison infrastructure.** The repo can run multiple models but has no mechanical process for comparing candidate model performance against a baseline on the same eval dataset and producing a ranked comparison report.

Add:

1. An explicit "model-selection-last" principle that names the sequence: build eval infrastructure → create domain dataset → select model based on evidence.
2. Side-by-side model comparison capability: run candidate model against enterprise eval dataset, compare to current baseline, produce ranked report.
3. The decision rule: when a model provider updates, re-run the comparison before adopting. The eval dataset is the gate, not the provider's changelog.
4. Integration with pain-signal-eval-progression-gate: the pain signal that triggers this timeline is "subjective model debates consuming engineering time without evidence."

## Tradeoffs

| Benefit | Cost |
|---|---|
| Eliminates subjective model debates: weeks of debate replaced by hours of data-driven comparison | Requires organizational discipline to invest 6 weeks in evaluation infrastructure before any model experimentation |
| Model is chosen based on domain-specific performance, not public benchmarks irrelevant to the use case | The initial ~200 golden answers must come from human domain experts, creating a bootstrapping dependency |
| The same eval dataset that selected the model also serves as the regression suite for every subsequent change | If the domain evolves rapidly, an eval dataset built on historical queries may not represent emerging query patterns |
| Model switching becomes mechanical: run new model against eval dataset, compare scores, decide | The timeline assumes a greenfield project; retrofitting into an existing agent system requires different phasing |
| Provider updates become testable before adoption, not after customer exposure | Multi-model architecture adds complexity: prompting strategies, tool call formats, and output parsing may differ between models |

## Relationship to Other Patterns

- **Triggered by:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] when subjective model debates consume engineering time without evidence.
- **Depends on:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] for the evaluation infrastructure built in weeks 1-6.
- **Depends on:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] for the domain-specific golden answer dataset that drives model comparison.
- **Uses:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] for capturing real queries and building the initial dataset.
- **Enables:** [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] by providing the evaluation evidence that makes model switching safe.
- **Complements:** [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]] by treating models as swappable compiler backends validated by the eval dataset.
- **Feeds:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] by making the eval dataset the gate for model, prompt, and tool changes.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:48` — original pattern definition (Bhaumik).
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:50` — Partial Coverage classification with evidence.
- `docs/canonical/pain-signal-eval-progression-gate.md:28` — pain-signal-driven eval investment gate.
- `docs/canonical/production-grounded-eval-sampling.md:28` — production-anchored eval data pipeline.
- `docs/canonical/repeatable-agent-spot-check-set.md` — seed set of repeatable eval cases.
- `docs/canonical/neutral-selection-layer.md:28` — model-agnostic selection layer.
- `docs/canonical/llm-as-fuzzy-compiler.md:27` — model output as disposable artifact.
- `docs/canonical/measured-harness-evolution-lifecycle.md` — evidence-gated harness investment.

---

*Created: 2026-06-26 | From: Production AI Playbook classification | Precedence: canonical*
