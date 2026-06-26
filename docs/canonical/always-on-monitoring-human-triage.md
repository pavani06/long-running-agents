---
title: "Always-On Production Monitoring with Human Triage"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["evals", "agentes-orquestracao", "production"]
aliases: ["always-on monitoring", "human triage monitoring", "production quality monitoring", "monitor-driven triage", "compression ratio monitoring"]
relates-to: ["[[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/business-outcome-first-eval-pipeline|Business Outcome First Eval Pipeline]]"]
---

# Always-On Production Monitoring with Human Triage

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Partial Coverage (High)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Exhaustive human review of every agent conversation is impossible at production scale. Sierra handles billions of conversations per year — reviewing even 1% would require thousands of reviewers. Random sampling is the intuitive alternative: review a random subset and assume it is representative. But random sampling misses rare but critical failure modes — the one conversation in ten thousand where the agent gave dangerously wrong information or handled a sensitive situation incompetently.

The failure mode is statistical: a random sample of 100 conversations from a pool of 100,000 has a ~63% chance of missing a failure that occurs in 1% of conversations. If the failure occurs in 0.1% of conversations, a random sample of 100 has only a ~10% chance of catching it. At production scale, failures that affect 0.01% of conversations still represent thousands of individual failures — and random sampling will almost certainly miss them.

The solution is not to review more — it is to review smarter. Replace random sampling with monitor-driven triage: define evaluators (monitors) that score every conversation on key quality dimensions and flag only the subset where the monitors detect potential issues. Humans then review the flagged subset, confident that monitors have filtered out the 99.9% of conversations that are fine.

Wedeen describes Sierra's compression ratio: from 10,000 conversations, monitors flag ~5 for human review. The remaining 9,995 are not reviewed by humans at all — the monitors certified them as acceptable. This shifts human attention from defensive (review everything) to offensive (improve resolution rate and satisfaction based on what flagged conversations reveal).

## Solution

An always-on production monitoring system where monitors continuously evaluate every agent conversation against defined quality dimensions, flag a small subset for human review, and feed insights from reviews back into monitor refinement and agent improvement. The system is complementary to pre-release evaluations, not a replacement — pre-release evals validate before deployment; production monitors validate during operation.

**Key components:**

1. **Monitor definitions for quality dimensions**: Each monitor is an evaluator specification for a specific quality dimension — greeting quality, empathy appropriateness, policy compliance, information accuracy, resolution effectiveness. Monitors can be deterministic (regex checks, schema validation), semantic (LLM-as-judge scoring), or behavioral (trace path analysis). They run on every conversation in real time.

2. **Compression ratio engineering**: The monitor system achieves a massive compression ratio (10,000 → 5 in Sierra's case) by tuning monitors to be highly specific — they flag only when they are confident something is wrong. High specificity means some failures may be missed (false negatives), but this is acceptable because the alternative (random sampling) misses far more failures. The compression ratio is a tunable parameter: tighten monitors = less compression, fewer missed failures, more human work; loosen monitors = more compression, more missed failures, less human work.

3. **Human triage of flagged conversations**: Flagged conversations enter a human review queue. Reviewers examine what the monitor flagged and why, confirm or dismiss the flag, and document findings. The review output is structured: was the flag correct? What category of failure occurred? What would have prevented it? This structured output feeds into the improvement flywheel.

4. **Monitor refinement loop**: When humans dismiss a flag as a false positive, the monitor is adjusted to reduce that class of flag. When humans identify failure modes the monitors missed (discovered through other channels — customer complaints, executive escalations), new monitors are added. The monitor suite tightens over time.

5. **Separation of monitors from evals**: Monitors and evals are distinct infrastructure with different purposes. Pre-release evals gate deployment — "does this agent version meet the quality bar?" Production monitors track ongoing quality — "is the deployed agent performing acceptably right now?" Monitors do not replace evals; they complement them at a different stage of the lifecycle.

**The production monitoring workflow in practice (Sierra's use case):**

1. Every conversation flows through the monitor pipeline in real time. Multiple monitors evaluate different quality dimensions simultaneously.
2. 99.95% of conversations pass all monitors — no flags raised, no human review needed.
3. The remaining 0.05% (5 conversations per 10,000) are flagged on one or more dimensions — the agent greeted a frustrated customer with excessive cheerfulness, provided incorrect policy information, or used language inconsistent with the brand voice.
4. Flagged conversations enter the human review queue. Reviewers examine each flag, classify the failure, and document findings.
5. Review findings feed into the improvement flywheel: failure patterns are classified, regression cases are added to evals, and agent specifications are updated (via [[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]]).
6. Monitors receive periodic refinement: false positive patterns are suppressed, and new monitors are added for failure modes discovered through other channels.

## Implementation in this repo

### What already exists

From the classification:

- [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]] lines 20-44: Always-on quality dashboard as primary detection surface. Detection-vs-diagnosis distinction.
- Flywheel daemon (systemd, 60s loop): Operational monitoring via `flywheel-health.sh` — processes triggers and surfaces findings.
- SLO checker (`budget-slo-check.sh`): Burn rate alerts every 6h — monitoring for operational health, not conversation quality.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] lines 28-40: Converts production incidents into regression cases (batch/post-hoc).

### What is missing

From the classification: "No human triage mechanism — no monitor definitions for quality dimensions, no flagged conversation subset, no compression ratio (10,000→5). The flywheel is fully automated without the Sierra pattern's human-in-the-loop triage step."

1. **Human triage mechanism**: The flywheel surfaces findings automatically, but there is no structured human review step where flagged conversations are examined, classified, and fed back into improvement.
2. **Monitor definitions for quality dimensions**: No evaluator specifications for production quality monitoring — no greeting quality monitor, empathy appropriateness monitor, policy compliance monitor, etc.
3. **Compression ratio**: No engineered compression from "all conversations" to "human-reviewable subset." The flywheel processes all triggers algorithmically without human filtering.
4. **Monitor-vs-eval separation**: The repo treats evaluation as primarily a pre-release concern (gating deployment). The distinction between pre-release evals and production monitors is not formalized.

The repo's flywheel is operationally sophisticated — systemd daemon, 60s loop, SLO checks, burn rate alerts — but it is automated end-to-end without the human triage step that Sierra considers essential. This is partly architectural (coding-agent harness vs. conversational agent in production) and partly a missing pattern that should be formalized.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Catches rare failure modes (0.01% occurrence) that random sampling would almost certainly miss | Monitor quality determines triage accuracy — poorly designed monitors miss failures or flood humans with false positives |
| Shifts human attention from defensive (review everything) to offensive (improve quality based on flagged patterns) | Human reviewers may develop alert fatigue if false positive rate is high — the compression ratio must balance sensitivity against human bandwidth |
| Treats evaluation as ongoing operational concern, not just a pre-release gate | Requires investment in monitor development and maintenance — each quality dimension needs a defined evaluator |
| Compression ratio is tunable per domain and per budget — tighten for higher safety, loosen for lower cost | Does not replace pre-release evals — production monitoring is complementary, not substitutive |

## Relationship to Other Patterns

- **Builds on:** [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]] — adds human triage and compression ratio to the existing dashboard and anomaly detection infrastructure.
- **Extends:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — adds monitor-driven detection and human triage to the existing batch/post-hoc regression pipeline.
- **Uses:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] — the classification taxonomy is used by human reviewers to categorize flagged conversations.
- **Uses:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — monitors use the same three-layer architecture (deterministic, semantic, behavioral) as pre-release evals.
- **Feeds:** [[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]] — human triage findings become inputs to the Ghostwriter improvement loop.
- **Complements:** [[docs/canonical/business-outcome-first-eval-pipeline|Business Outcome First Eval Pipeline]] — pre-release evals validate before deployment; production monitors validate during operation.

## References

-  lines 264-289 — extracted pattern with monitor definitions, compression ratio (10,000→5), human triage workflow.
-  lines 159-170 — Partial Coverage classification with evidence of monitoring infrastructure but missing human triage.
- [[docs/canonical/eval-dashboard-primary-detection-surface|Eval Dashboard Primary Detection Surface]] lines 20-44 — existing detection-vs-diagnosis distinction.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] lines 28-40 — existing regression pipeline.
- Sierra transcript: "From 10,000 conversations, monitors flag ~5 for human review." — Wedeen on the compression ratio.
- Sierra transcript: "Monitors are separate infrastructure from eval pipelines — both coexist." — Wedeen on the monitor-vs-eval distinction.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
