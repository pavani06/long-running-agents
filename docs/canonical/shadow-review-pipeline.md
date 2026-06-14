---
title: "Shadow Review Pipeline"
type: canonical
aliases: ["shadow review", "AI review shadow", "non-blocking AI review", "review shadow pipeline", "shadow period", "review agreement metrics"]
tags: ["evals", "agentic-coding", "governanca", "harness-engineering"]
last_updated: 2026-06-15
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/review-contract-checklist|Review Contract Checklist]]", "[[docs/canonical/contextual-severity-calibration|Contextual Severity Calibration]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]"]
sources: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]"]
---

# Shadow Review Pipeline

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]
**Classification:** Missing ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:35-67)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

AI-based code reviewers cannot be trusted as blocking gates before their agreement rate, false-positive rate, and missed-finding value are observed in the target workflow. Blocking merges with an untested AI reviewer generates resistance and distrust; bypass the gate entirely and no one learns whether the AI adds value. The adoption decision defaults to opinion instead of data.

The canary-test analysis reports that AI reviewers catching 30-40% of issues missed by humans is valuable, but 15-20% false-positive rate means that blocking merges on day one would alienate developers and produce the opposite of the intended effect ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:130-132, 210-218). The failure pattern documented is premature gating without data: developers encounter blocking false positives, lose trust in the tool, and find bypasses before the tool proves its value ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:341-351).

The repo already has a general concept of shadow tests and canary stages for production deployment safety, but these are about comparing baseline vs. candidate agent behavior in production, not about shadowing an AI code review system alongside human reviewers ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:40-48). No mechanism exists for running an AI reviewer in non-blocking shadow mode, collecting structured agreement metrics, or graduating specific AI checks to blocking status based on observed reliability data.

## Solution

Run the AI reviewer in parallel with human review for a defined shadow period (typically two weeks) without blocking any merges. AI review output is captured in a dashboard or log sink alongside human review outcomes. After the shadow period, agreement metrics determine which AI checks are reliable enough to graduate to blocking status.

The pipeline operates in four phases:

```
+--------------------+     +--------------------+     +--------------------+     +--------------------+
| 1. SHADOW          | --> | 2. COLLECT         | --> | 3. EVALUATE        | --> | 4. GRADUATE        |
| AI reviews every   |     | Agreement metrics  |     | Which checks are   |     | Selected checks    |
| PR, does not       |     | per check category |     | reliable enough?   |     | become blocking    |
| block merges       |     | stored in dashboard|     |                    |     | gates              |
+--------------------+     +--------------------+     +--------------------+     +--------------------+
```

**Inputs:**
- Open PRs or proposed changes.
- Human review outcomes (approve/reject with specific findings).
- AI reviewer outcomes captured without blocking merges.
- Agreement categories structured per finding.

**Agreement category taxonomy:**

| Category | Meaning |
|---|---|
| `true_positive` | AI flagged it, human agreed it is a real issue |
| `false_positive` | AI flagged it, human determined it is not an issue |
| `missed_by_AI` | Human caught it, AI did not flag |
| `missed_by_human` | AI caught it, human missed it during review |

This taxonomy is confirmed NOT_FOUND in the repo — no existing canonical doc, curriculum lesson, or skill defines agreement categories for AI review findings ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:56).

**Outputs:**
- Non-blocking AI review trace for each change during the shadow period.
- Agreement-rate and false-positive metrics by check category.
- Data-backed threshold decisions: which checks graduate to blocking, which remain advisory, which are retired.
- Trust evidence for developers and reviewers before workflow enforcement changes.

**Shadow period properties:**

The source document recommends a two-week shadow period sufficient to produce meaningful volume without delaying value capture ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:208). During this period, no developer workflow changes — the AI reviewer runs silently alongside existing review practices, producing output visible only to the team collecting metrics. This de-risks adoption because resistance to change is not triggered until data exists to justify it ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|patterns]]:30).

## Implementation in this repo

### What already exists (adjacent, not equivalent)

The repo has a well-developed general concept of shadow tests and canaries for production deployment safety, but these address a different domain:

- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]:113 mentions staged shadow tests, canaries, production metrics, rollback, and observation — but this is about production deployment canaries comparing baseline vs. candidate agent behavior, not AI review shadowing.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:58 references staging shadow tests and canary phases in the harness playbook context — again about production deployment safety.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:60 mentions shadow tests in the quarterly harness cadence — deployment safety context.
- [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]:64 discusses shadowing messy customer work to extract operator decisions and edge cases — operational shadowing, not AI review shadowing.

These provide a conceptual foundation for the idea of shadowing, but none addresses an AI code review pipeline with structured agreement metrics, non-blocking shadow period, and data-driven gating decisions ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:40-48).

### What is missing

1. No canonical doc, curriculum lesson, or skill that describes running an AI reviewer in non-blocking shadow mode alongside human reviewers ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:52).
2. No mechanism for collecting agreement metrics between AI and human review outcomes across the four agreement categories (`true_positive`, `false_positive`, `missed_by_human`, `missed_by_AI`) ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:53).
3. No concept of a shadow period with a dashboard or log sink for AI review trust data ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:54).
4. No graduation process from shadow to blocking based on agreement-rate thresholds per check category ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:55).
5. No agreement-category taxonomy for AI review findings ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:56).

## Tradeoffs

| Benefit | Cost |
|---|---|
| De-risks adoption: no workflow changes until data proves value | Provides no blocking protection during the shadow period |
| Turns gating decisions from opinion into observed reliability data | Requires enough review volume to produce statistically useful agreement data |
| Reveals which AI review categories add value and which create noise | Metrics are only actionable if AI findings are structured enough to compare with human outcomes |
| Developers can ignore AI output without penalty during tuning phase | Dashboard and log sink infrastructure must be built and maintained |
| Data from shadow period feeds severity calibration for later risk adjustment | Two-week shadow period delays time-to-value for the blocking gate |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/review-contract-checklist|Review Contract Checklist]] because structured, per-dimension AI findings are required to compute agreement metrics that are comparable with human review outcomes. The classification identifies this as the primary dependency: without structured contracts, shadow period agreement data would be ambiguous and non-actionable ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:382-384).
- **Uses:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] as the verification structure that makes AI findings comparable to human findings per check item.
- **Uses:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] as the architectural model for separating the AI reviewer (evaluator) from the code author (generator).
- **Feeds into:** [[docs/canonical/contextual-severity-calibration|Contextual Severity Calibration]] because per-module false-positive rates collected during the shadow period inform which severity levels are trustworthy for each module type.
- **Feeds into:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] because checks that graduate from shadow to blocking become PR-gated enforcement rules.
- **Complements:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] because the shadow pipeline adds a trust-calibration phase before automated review gates become blocking — a natural extension of the fast tier's pre-commit and PR triggers.
- **Context from:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] because the repo's existing shadow/canary infrastructure for production deployment provides a conceptual foundation for the review shadow pipeline, even though the domains differ.

## References

- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:124-145 — Shadow Review Pipeline mechanics: parallel AI+human review, dashboard, two-week period, gating decision.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:208 — recommended two-week shadow period duration.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:210-218 — failure pattern: AI output ignored due to noise from untuned prompts.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:341-351 — failure pattern: premature gating without data leads to rejection.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:249-258 — tradeoff: bloqueio imediato vs. adocao gradual com shadow pipeline.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:380-401 — dependency chain: shadow pipeline → severity calibration → continuous improvement cycle.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|patterns]]:15-37 — extracted pattern definition with inputs, outputs, benefits, limitations.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:35-67 — Missing classification with NOT_FOUND evidence.
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]:113 — adjacent shadow test infrastructure (production deployment canaries, not AI review).
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:58 — adjacent shadow references in harness playbook context.

---

*Created: 2026-06-15 | From: Canary Test Code Review pattern classification | Precedence: canonical*
