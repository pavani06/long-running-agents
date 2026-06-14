---
title: "Reusable Agentic Patterns from Canary Test Code Review"
type: analysis
tags: ["agentic-coding", "governanca", "decision-discipline", "harness-engineering", "evals", "spec-driven-development"]
date: 2026-06-15
aliases: ["canary test patterns", "AI review agentic patterns", "code review agent patterns"]
relates-to: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]"]
sources: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]"]
---

# Reusable Agentic Patterns from Canary Test Code Review

Scope: extracted from `docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis.md`. Only reusable patterns applicable to agentic review systems, agentic governance, or agent-operated validation loops are included. Repository classification is intentionally out of scope.

## 1. Shadow Review Pipeline

- **name:** Shadow Review Pipeline
- **problem solved:** Agentic reviewers are hard to trust as blocking gates before their agreement rate, false positives, and missed-find value are observed in the target workflow.
- **inputs:**
  - Open PRs or proposed changes.
  - Human review outcomes.
  - AI reviewer outcomes captured without blocking merges.
  - Agreement categories such as true positive, false positive, missed-by-human, and missed-by-AI.
  - Shadow-period duration and dashboard or log sink.
- **outputs:**
  - Non-blocking AI review trace for each change.
  - Agreement and false-positive metrics by check category.
  - Data-backed decision about which checks can graduate to blocking status.
  - Trust evidence for developers and reviewers before workflow enforcement changes.
- **benefits:**
  - De-risks adoption because human workflow does not change during measurement.
  - Turns gating decisions from opinion into observed reliability data.
  - Reveals which AI review categories add value and which create noise.
- **limitations:**
  - Provides no blocking protection during the shadow period.
  - Requires enough review volume to produce useful agreement data.
  - Metrics are only actionable if AI findings are structured enough to compare with human outcomes.

## 2. Review Contract Checklist

- **name:** Review Contract Checklist
- **problem solved:** Freeform agent review produces ambiguous comments that are hard to verify, compare, or turn into repeatable gates.
- **inputs:**
  - A `review-contract.yaml` or equivalent checklist attached to the change.
  - Explicit review dimensions such as security surface, migrations, API compatibility, error handling, and test coverage.
  - The code diff or artifact under review.
  - Project conventions and applicability rules for each checklist item.
- **outputs:**
  - Per-item status such as `pass`, `fail`, or `not-applicable`.
  - Structured findings tied to specific review dimensions.
  - A review artifact that humans, dashboards, and later gates can inspect consistently.
- **benefits:**
  - Gives the agent independent, bounded checks instead of an open-ended instruction to comment.
  - Makes review output actionable without forcing humans to reinterpret freeform prose.
  - Creates comparable data for shadow pipelines and future gate decisions.
- **limitations:**
  - A weak or incomplete contract can omit important risks.
  - Checklist maintenance costs grow as the system and review policy evolve.
  - It does not replace human architectural judgment when dimensions require tradeoff evaluation.

## 3. Pre-Commit AI Review Gate

- **name:** Pre-Commit AI Review Gate
- **problem solved:** Agentic review that runs only after push creates slow feedback loops and lets trivial issues reach shared CI or PR review surfaces.
- **inputs:**
  - Local `git diff` or staged diff.
  - AI reviewer prompt constrained to potential bugs, project-style violations, and security concerns.
  - Project-specific conventions rather than generic best-practice defaults.
  - Pass/block policy for local gate results.
- **outputs:**
  - Early pass or block decision before push.
  - Focused finding list for bugs, project convention violations, and security concerns.
  - Local remediation loop before shared pipeline resources are used.
- **benefits:**
  - Shortens feedback latency for mechanical and policy-level issues.
  - Keeps CI and human review focused on higher-value checks.
  - Reduces noise when the prompt enforces the team's actual rules.
- **limitations:**
  - Local hooks can be bypassed unless paired with server-side or PR gates.
  - The agent remains a fast, shallow first pass and should not own architecture or design approval.
  - Poor prompt tuning can produce noisy output that developers learn to ignore.

## 4. Contextual Severity Calibration

- **name:** Contextual Severity Calibration
- **problem solved:** One-size-fits-all agent review over-reviews low-risk modules while under-reviewing critical paths.
- **inputs:**
  - Module-level `risk-profile.yaml` or equivalent risk metadata.
  - Risk level such as `critical`, `high`, `medium`, or `low`.
  - Applicable check set such as style, correctness, security, performance, and data integrity.
  - Changed file paths or module ownership metadata.
  - Historical false-positive and agreement metrics when available.
- **outputs:**
  - Risk-adjusted review depth for the changed module.
  - Calibrated severity labels for findings.
  - Check selection proportional to the blast radius and failure cost of the change.
- **benefits:**
  - Reduces reviewer fatigue on low-risk changes.
  - Increases scrutiny where failures have high security, data, performance, or integrity cost.
  - Makes agentic review effort proportional to operational risk instead of uniform across the codebase.
- **limitations:**
  - Requires maintained risk profiles and ownership of module metadata.
  - Misclassified modules can create either false confidence or unnecessary friction.
  - Calibration needs periodic re-evaluation as the product, architecture, and empirical review data change.
