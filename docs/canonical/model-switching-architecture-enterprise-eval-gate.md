---
title: "Model-Switching Architecture with Enterprise Eval Gate"
type: canonical
aliases: ["model switching architecture", "enterprise eval gate", "model comparison infrastructure", "vendor-independent model selection"]
tags: ["agentes-orquestracao", "evals", "production", "harness-engineering"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]", "[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"]
---

# Model-Switching Architecture with Enterprise Eval Gate

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/
**Classification:** Partial Coverage (P2, Medium)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Committing to a single model provider creates vendor lock-in. When the provider updates their model, performance may degrade silently because the organization has no way to test the new model against their specific domain before customers are affected. Model selection decisions become subjective debates based on public benchmarks (MMLU, HumanEval) rather than domain-specific performance data.

The repo has strong philosophical alignment for model independence. `neutral-selection-layer.md` defines a model-agnostic context format with vendor adapter and cross-model portability. `llm-as-fuzzy-compiler.md` treats models as swappable compiler backends and generated code as disposable. `multi-model-evaluation-council.md` uses model diversity for evaluation. The codebase practices multi-model operation (DeepSeek for orchestrator, Anthropic for momus). However, the concrete infrastructure to execute model switching — an enterprise eval dataset that tests model upgrades against domain-specific data, side-by-side comparison infrastructure, and a mechanical switching decision framework — does not exist. The philosophical alignment exists but the infrastructure does not.

## Solution

Build concrete infrastructure that makes model switching a mechanical, data-driven process rather than a subjective debate. The infrastructure has four components:

### 1. Enterprise Eval Dataset

Maintain an eval dataset that is independent of any specific model provider. This dataset:
- Contains domain-specific test cases (real queries, not public benchmarks)
- Has golden answers authored by domain experts (not model-generated)
- Covers all three eval layers (deterministic, semantic, behavioral)
- Is the same dataset used for regression testing, CI gates, and model selection
- Grows monotonically from production incidents via the regression flywheel

The dataset is the **enterprise eval gate** — it is what determines whether a model upgrade is safe, not provider claims or public benchmark scores.

### 2. Side-by-Side Model Comparison Infrastructure

When a candidate model becomes available (new version, new provider, or fine-tuned variant), run it against the enterprise eval dataset and compare results to the current model baseline:

```
Candidate model → Enterprise eval dataset → Candidate scores
Current model  → Enterprise eval dataset → Baseline scores
                            ↓
                   Comparison report
                            ↓
              Switch / Hold / Hybrid decision
```

The comparison report includes:
- Overall pass rate comparison per eval layer
- Per-category breakdown (security, login, tool calls, knowledge retrieval, math/reasoning)
- Regression cases: specific test cases where candidate performs worse than current
- Improvement cases: specific test cases where candidate performs better
- Cost comparison: tokens per query, latency per query

### 3. Model-Switching Decision Framework

The comparison data drives a structured decision tree, not a subjective debate:

| Comparison result | Decision | Action |
|---|---|---|
| Candidate ≥ current on all layers, no regressions | **Switch** | Deploy candidate, archive current |
| Candidate ≥ current overall, but N specific regressions | **Hybrid** | Use candidate for categories where it wins, current for categories with regressions |
| Candidate < current on any critical layer (deterministic PII, safety) | **Hold** | Keep current; file regression report with provider |
| Candidate < current overall but better on specific categories | **Evaluate** | Assess whether category-specific improvement justifies regression risk |

### 4. Continuous Eval Monitoring

Model behavior can change without provider announcement. After switching, continuous eval monitoring runs the enterprise eval dataset at a scheduled cadence:

- **Daily**: Fast tier (deterministic) on all active models
- **Weekly**: Medium tier (semantic) on all active models
- **Per-release**: Deep tier (behavioral) on candidate models before deployment

If a provider silently updates their model and pass rates degrade, the monitoring catches it within 24 hours.

## Implementation in this repo

### What already exists

- **Neutral Selection Layer** (`neutral-selection-layer.md:28`) defines model-agnostic context format, vendor adapter, and cross-model portability. Three properties: Neutral (not coupled to a single model), Horizontal (cross-agent, cross-session, cross-model), Structured (relational).
- **LLM as Fuzzy Compiler** (`llm-as-fuzzy-compiler.md`) treats models as swappable compiler backends and generated code as disposable artifacts.
- **Multi-Model Evaluation Council** (`multi-model-evaluation-council.md:28`) uses model diversity for evaluation and routes outcomes to retry, needs-human, or rubric-update.
- **Practical multi-model operation**: the codebase uses DeepSeek for orchestrator and Anthropic for momus, demonstrating operational multi-model capability.
- **Neutral Selection Layer in curriculum** (`curriculum/GLOSSARY.md:530`) — taught at N3 level with exercises.

### What is missing

1. **No enterprise eval dataset** maintained independently of any model provider. The evolving eval cases from `production-failure-regression-flywheel.md` are the closest artifact, but they are not packaged as a model-evaluation dataset.
2. **No side-by-side model comparison infrastructure**: no mechanical process to run candidate model against eval dataset and compare to current baseline with structured reporting.
3. **No model-switching decision framework**: no switch/hold/hybrid decision tree based on eval comparison data.
4. **No provider-upgrade testing against domain-specific data**: when a model provider releases a new version, there is no automated process to test it against the enterprise eval dataset.
5. **No mechanical model comparison process** that replaces subjective debate with data-driven reports. The repo has the philosophical framework (neutral selection layer, fuzzy compiler) but not the concrete infrastructure.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Vendor independence: model selection is governed by domain-specific performance data, not by provider relationships | Multi-model architecture adds complexity: prompting strategies, tool call formats, and output parsing may differ between models |
| Provider updates become testable: run candidate against eval dataset to decide if the update is safe | Running the full eval suite against multiple models adds cost (LLM calls for Layer 2-3 multiplied by number of candidates) |
| No single point of model failure: if one model degrades, switch to another already tested against the eval dataset | Model behavior can change without provider announcement — continuous eval monitoring is required, not just point-in-time comparison |
| The eval dataset that selected the model also serves as the continuous validation suite for every subsequent change | The eval dataset itself may have model-specific biases if golden answers were authored with one model's typical output style in mind |

## Relationship to Other Patterns

- **Depends on:** Neutral Selection Layer — the model-agnostic context format is the prerequisite for being able to swap models without changing the rest of the system.
- **Consumes from:** Multi-Model Evaluation Council — the council's model diversity provides candidate models for comparison.
- **Uses:** Eval Tier Stratification — the enterprise eval dataset is stratified into fast/medium/deep tiers, and comparison runs respect tier cost governance.
- **Feeds into:** Production Failure Regression Flywheel — model-switching incidents (provider update breaks production) become new regression cases.
- **Aligns with:** LLM as Fuzzy Compiler — the compiler-backend mental model justifies treating models as swappable and code as disposable.
- **Informs:** Measured Harness Evolution Lifecycle — model switching is a BUILD-phase activity: add comparison infrastructure, measure ROI, stabilize or simplify.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:384` — extracted pattern definition.
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:456` — Partial Coverage classification (P2, Medium).
- `docs/canonical/neutral-selection-layer.md:28` — model-agnostic context format, vendor adapter, cross-model portability.
- `docs/canonical/neutral-selection-layer.md:71` — context survives model migrations.
- `docs/canonical/neutral-selection-layer.md:73` — vendor independence.
- `docs/canonical/llm-as-fuzzy-compiler.md` — LLM as swappable compiler backend.
- `docs/canonical/multi-model-evaluation-council.md:28` — model-diverse evaluation council.
- `long-running-agents/curriculum/GLOSSARY.md:530` — Neutral Selection Layer definition.

---

*Created: 2026-06-26 | From: Production AI Playbook classification (Batch B) | Precedence: canonical*
