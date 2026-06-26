---
title: "Business-Outcome-First Eval Pipeline"
type: canonical
aliases: ["business outcome eval", "deflection rate eval", "golden answers eval", "bottom-up eval pipeline"]
tags: ["evals", "production", "governanca"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]"]
---

# Business-Outcome-First Eval Pipeline

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/
**Classification:** Partial Coverage (P2, Medium)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Engineering teams build evaluation pipelines starting with technical metrics (latency, throughput, accuracy) instead of business outcomes (deflection rate, CSAT, revenue impact). This creates a misalignment where the technical eval passes but the business outcome fails — the agent is technically correct but business-irrelevant.

The repo ties eval investments to business-visible pain signals (user complaints, manual bottlenecks, escaped edge cases) via `pain-signal-eval-progression-gate.md`. Production-grounded eval sampling uses real queries. Eval-to-production correlation tracking measures eval score vs. production outcomes. However, eval investment starts from **technical pain** (incidents, regressions, manual bottlenecks), not from **business outcome definition** (deflection rate target, CSAT threshold, revenue impact). The dependency chain is missing: business success definition → golden answers → Python eval pipeline — with technical infrastructure built after, not before, the business alignment.

## Solution

Invert the eval pipeline construction sequence: define business success first, then create golden answers from domain experts, then build the technical pipeline to compare agent outputs against business-aligned metrics.

### Construction Sequence

The pattern prescribes a specific construction order that is the opposite of most engineering-first approaches:

```
Step 1: Define business success → Step 2: Create golden answers → Step 3: Build eval pipeline
```

This is faster than the engineering-first approach ("build eval infrastructure → figure out what to measure") because it starts from what matters.

#### Step 1: Define Success in Business Terms

Before any technical infrastructure, define the business outcome the agent is intended to improve. This must be a measurable metric with a target threshold:

| Business outcome | Metric | Example target |
|---|---|---|
| Deflection | % of queries resolved without human intervention | 60% deflection rate |
| Resolution time | Mean time to resolve customer query | < 3 minutes |
| CSAT | Customer satisfaction score | ≥ 4.2 / 5 |
| Revenue protection | % of cart abandonments recovered | 15% recovery rate |

The business outcome definition is authored by the outcome owner (product manager, business stakeholder), not by the engineering team. It is the eval's north star.

#### Step 2: Create Golden Answers from Domain Experts

Source ~200 real production queries from human agent logs (not synthetic queries). For each query, have a human domain expert author the expected correct response — the "golden answer."

Key properties of golden answers:
- **Authored by humans**, not by models — prevents training the eval against model-generated hallucinations.
- **Derived from real production queries** — represents actual user intent, not idealized scenarios.
- **Scored against the business outcome** — each golden answer is rated by how well it achieves the business metric (e.g., "this response would have deflected the customer").
- **Categorized** by query type (simple lookup, multi-step reasoning, transactional) for stratified analysis.

#### Step 3: Build the Python Evaluation Pipeline

After golden answers exist, build a Python pipeline that compares agent outputs against golden answers using metrics correlated with the business outcome:

```
Agent output → Compare against golden answer → Business-aligned score → Aggregate by category
```

The evaluation metric is not generic "accuracy" — it is "how well does this agent response achieve the business outcome compared to the human-authored golden answer?"

### Deflection Rate Prediction

The eval pass rate predicts production deflection rate. If 85% of agent responses match or exceed golden answers in the eval dataset, the predicted deflection rate is ~85%. This enables evidence-based go/no-go deployment decisions: deploy when predicted deflection rate exceeds the business target, hold when it does not.

## Implementation in this repo

### What already exists

- **Pain-Signal Eval Progression Gate** (`pain-signal-eval-progression-gate.md:28-50`) ties eval investments to business-visible pain signals: user complaints → expand spot-check set, manual bottlenecks → tier stratification, escaped edge cases → regression flywheel.
- **Production-Grounded Eval Sampling** (`production-grounded-eval-sampling.md:28-37`) uses real production queries (not synthetic) with capture, privacy filters, retention, sampling, coverage, labeling, and replay infrastructure.
- **Eval-to-Production Correlation Tracking** (`eval-to-production-correlation-tracking.md`) measures eval score vs. production outcomes with correlation tracking.
- **KODA domain** has business-specific eval rubrics and sprint contracts with human-escalation outcomes.

### What is missing

1. **Business-outcome-FIRST sequence**: the repo's eval investment starts from technical pain (incidents, regressions), not from business outcome definition. The sequence "define success in business terms → create golden answers → build pipeline" is not formalized.
2. **No golden answers authored by human domain experts** as the eval foundation. The repo has repeatable spot-check sets (`repeatable-agent-spot-check-set.md`) but these are agent-authored, not expert-authored.
3. **No deflection rate prediction** from eval scores. The repo tracks eval-to-production correlation (`eval-to-production-correlation-tracking.md`) but does not predict production metrics from eval pass rates.
4. **No Python evaluation pipeline** that compares agent outputs against business-outcome-aligned golden answers as the FIRST step before building technical eval infrastructure.
5. **No business outcome definition as eval north star** — the repo evaluates technical quality but does not anchor evaluation to a specific business metric target.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents the "technically correct, business irrelevant" trap: the eval measures what matters to the business, not what is easy to measure | Requires access to real production queries and domain experts to author golden answers — not feasible for pre-product agents |
| Golden answers authored by domain experts, not models, ensure the eval represents real customer expectations | Manual golden answer authoring does not scale; beyond ~200 cases, LLM-assisted authoring is required, introducing quality risk |
| Starting with business outcomes is faster than starting with engineering — "define success → create golden answers → build pipeline" | Business metric correlation with eval scores must be validated empirically; initial correlation may not hold as the domain evolves |
| Deflection rate prediction from eval scores enables evidence-based deployment decisions | The pipeline requires maintenance as business outcomes change; a deflection-rate-optimized eval may not measure quality for a new business goal |

## Relationship to Other Patterns

- **Informs:** Pain-Signal Eval Progression Gate — business outcome definition provides the north star against which pain signals are prioritized. A CSAT drop is more urgent if the target is 4.2/5 and current is 3.8.
- **Consumes from:** Production-Grounded Eval Sampling — the 200 golden answers are sourced from real production queries captured by the sampling pipeline.
- **Validated by:** Eval-to-Production Correlation Tracking — the correlation between business-outcome eval scores and actual production outcomes validates the pipeline's predictive power.
- **Feeds into:** Eval Tier Stratification — golden answer comparison can be assigned to the medium tier (LLM-as-judge comparison against goldens), while the business metric target defines the pass/fail threshold.
- **Extends:** Repeatable Agent Spot-Check Set — golden answers become the authoritative seed for the spot-check set.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:354` — extracted pattern definition.
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:421` — Partial Coverage classification (P2, Medium).
- `docs/canonical/pain-signal-eval-progression-gate.md:28` — pain-signal-driven eval investment.
- `docs/canonical/pain-signal-eval-progression-gate.md:44` — user complaints → expand spot-check set mapping.
- `docs/canonical/eval-to-production-correlation-tracking.md` — eval score vs. production outcome correlation.
- `docs/canonical/production-grounded-eval-sampling.md:28` — production-sampled eval dataset with capture, privacy, replay.

---

*Created: 2026-06-26 | From: Production AI Playbook classification (Batch B) | Precedence: canonical*
