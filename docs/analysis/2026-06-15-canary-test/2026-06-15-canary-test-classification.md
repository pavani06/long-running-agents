---
title: "Comparative Classification: Canary Test Code Review Patterns vs. long-running-agents Repo"
type: analysis
date: 2026-06-15
domain: canary-test
aliases: ["classificacao canary test", "canary code review classification", "gap analysis canary review"]
tags: ["analise", "agentic-coding", "governanca", "evals", "classification"]
last_updated: 2026-06-15
relates-to: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-mental-model|Canary Test Mental Model]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"]
sources: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]"]
---

# Comparative Classification: Canary Test Code Review Patterns vs. long-running-agents Repo

**Date:** 2026-06-15
**Repo analyzed:** `long-running-agents`
**Patterns source:** Canary Test Code Review (extracted via analyze-and-improve pipeline)
**Evidence basis:** `docs/canonical/`, `docs/evidence/`, `docs/analysis/`, `curriculum/`, `.opencode/`, `docs/system-of-record.md`

**Precedence order:** `docs/decisions/` > `docs/canonical/` > `docs/evidence/` > `docs/analysis/` > `curriculum/` > READMEs/operational summaries.

---

## Classification Legend

| Class | Meaning |
|---|---|
| Already Exists | Pattern is documented, implemented, or taught with equivalent depth |
| Partial Coverage | Elements exist but missing key mechanics, reframe, or formalization |
| Missing | Not present in any form (doc, code, or curriculum) |
| Better Implementation | Repo has a superior or more mature version of the same idea |

---

## 1. Shadow Review Pipeline

**Classification:** Missing

**Why:**

The repo has a well-developed general concept of shadow tests and canary stages for production deployment safety. However, the Shadow Review Pipeline pattern is specifically about shadowing an AI-based code reviewer alongside human review, collecting agreement metrics (true positive, false positive, missed-by-human, missed-by-AI), and using shadow-period data to graduate specific AI checks to blocking status. This specific mechanism does not exist in any form.

**What the repo has (adjacent, not equivalent):**

- `docs/canonical/eval-to-production-correlation-tracking.md:113` — Mentions "staged shadow tests, canaries, production metrics, rollback, and observation" as a Better Implementation of external canary-gate patterns, but this is about production deployment canaries (comparing baseline vs. candidate agent behavior), not about shadowing an AI code review system.
- `docs/canonical/eval-tier-stratification.md:58` — References "staging shadow tests, and canary phases" in the harness playbook context; again about production deployment, not AI review trust-building.
- `docs/canonical/measured-harness-evolution-lifecycle.md:60` — Mentions "shadow tests" in quarterly harness cadence; deployment safety, not review trust.
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:64` — Discusses shadowing messy customer work to extract operator decisions and edge cases before automating workflows; operational shadowing, not AI review shadowing.

**What is missing (confirmed NOT_FOUND):**

1. No canonical doc, curriculum lesson, or skill that describes running an AI reviewer in non-blocking shadow mode alongside human reviewers.
2. No mechanism for collecting agreement metrics between AI and human review outcomes (true positive, false positive categories).
3. No concept of a shadow period with dashboard/log sink for AI review trust data.
4. No graduation process from shadow to blocking based on agreement-rate thresholds.
5. No agreement-category taxonomy (`true_positive`, `false_positive`, `missed_by_human`, `missed_by_AI`) for AI review findings.

**Locations searched:**
- `docs/canonical/` (all 55 canonical docs) — shadow references relate to production canary stages, not AI review shadowing.
- `curriculum/` — No AI review shadow pipeline lesson, exercise, or case study.
- `.opencode/skills/` — No skill for non-blocking shadow review with agreement metrics.
- `docs/evidence/` — No shadow review agreement data or dashboards.

**Integration value:** Medium

The repo's general canary/shadow infrastructure provides a conceptual foundation, but the specific AI review shadow pipeline with structured agreement metrics, non-blocking shadow period, and data-driven gating decisions is a novel contribution. It would complement the existing eval tier stratification by adding a trust-calibration phase before automated review gates become blocking.

---

## 2. Review Contract Checklist

**Classification:** Partial Coverage

**Why:**

The repo has rich evaluation infrastructure with structured rubrics, constraint-anchored checking, sprint contracts, and per-dimension evaluation matrices. However, these are primarily oriented toward evaluating agent output quality (product recommendations, generated code correctness) — not structured checklist contracts specifically for AI code review. The concept is present; the specific format and application to AI code review are missing.

**What already exists:**

- `docs/canonical/constraint-anchored-evaluation.md:31-49` — Formal verification-matrix format (`constraint → check → pass/fail → violation detail`) with an aggregate verdict that approves only when all constraints pass. This is the closest structural match to the Review Contract Checklist pattern.
- `docs/canonical/generator-evaluator.md:57-65` — Evaluator applies quality rubrics and business rules with access to `cliente_data` and rubrics, producing approve/reject with specific feedback.
- `docs/canonical/split-brain-planning-review.md:28-41` — Independent rubrics applied by separate engineering and destination reviewers, reconciled through explicit decisions.
- `docs/canonical/pr-gated-eval-enforcement.md:30-43` — Structured PR eval report with explicit fields: `change_scope`, `baseline_version`, `quality_delta`, `latency_delta`, `cost_delta`, `thresholds`, `failure_examples`, `merge_policy`.
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:72-131` — Teaches Sprint Contracts as a pre-agreed definition of "done" between Generator and Evaluator, with explicit acceptance criteria.
- `curriculum/08-tools-templates/evaluation-rubric-template.md` — Provides a template for structured evaluation rubrics with measurable criteria.
- `docs/canonical/repeatable-agent-spot-check-set.md:30-42` — Eval cases with `expected_outcome`, `acceptable_tool_behavior`, `baseline`, and `grading_notes`.

**What is missing:**

1. The `review-contract.yaml` format: a structured checklist attached to each change with explicit review dimensions (security surface, migrations, API compatibility, error handling, test coverage). NOT_FOUND as a file or template anywhere outside the canary-test analysis itself.
2. Per-item status of `pass`, `fail`, or `not-applicable` specifically for code review dimensions — the existing verification matrix is for agent output constraints, not code review items.
3. Review dimensions as an explicit named concept for AI code review — existing dimensions are about eval quality (quality, latency, cost), not code review dimensions (security, migrations, API compatibility).
4. Contract attachment to the change itself — sprint contracts exist in the curriculum, but they define work scope, not review scope per change.

**Integration value:** Medium

The repo's constraint-anchored evaluation and sprint contract mechanisms provide the structural foundation. Formalizing a `review-contract.yaml` format for AI code review with explicit review dimensions and per-item status would extend these patterns into the code review domain, making AI review output comparable and auditable — a direct input to the Shadow Review Pipeline's agreement metrics.

---

## 3. Pre-Commit AI Review Gate

**Classification:** Partial Coverage

**Why:**

The repo has the conceptual framework for gating checks at different lifecycle stages (pre-commit, PR, release, canary) via eval tier stratification. Standard pre-commit hooks for mechanical lint/formatting exist in the curriculum setup guide. However, the specific pattern of running an AI-based review as a local pre-commit hook — receiving a diff as input and checking for bugs, project-style violations, and security concerns before push — is not documented, implemented, or taught.

**What already exists:**

- `docs/canonical/eval-tier-stratification.md:34` — Fast eval tier explicitly lists "pre-commit" as a trigger: "Local change, pre-commit, small PR" with decision power to "block local readiness or PR if critical paths regress."
- `docs/canonical/eval-tier-stratification.md:30-49` — Comprehensive metadata per tier including `runtime_budget`, `cost_budget`, `flakiness_policy`, `trigger`, `threshold`, `reporting`, and `owner`.
- `docs/canonical/failure-pattern-classification-loop.md:67-69` — Lint rules as "commit time" guardrail surface with low token cost and instant latency — establishes the concept of pre-commit mechanical checks.
- `curriculum/07-implementation-guides/01-setup-guide.md:2452-2487` — Standard pre-commit hooks for lint/ruff formatting (mechanical, not AI-based).
- `docs/canonical/pr-gated-eval-enforcement.md:30-53` — PR-level eval enforcement with structured reports, but operates after push (PR time), not pre-commit.

**What is missing:**

1. An AI reviewer prompt designed to be invoked at pre-commit time, receiving a local `git diff` and checking for bugs, project convention violations, and security concerns. NOT_FOUND in any canonical doc, skill, or curriculum lesson.
2. A pass/block policy for local AI pre-commit results — the existing pre-commit hooks block on lint failure, but there is no equivalent AI-review block policy.
3. Integration between AI pre-commit findings and the eval tier stratification: the fast tier mentions pre-commit as a trigger, but does not describe an AI reviewer as the mechanism.
4. Project-specific convention awareness in an AI pre-commit prompt — the canonical docs emphasize project conventions (AGENTS.md rules, canonical patterns), but none describes injecting these into a pre-commit AI review prompt.

**Integration value:** Medium

The eval tier stratification's fast tier and pre-commit trigger provide a natural slot for this pattern. Adding an AI pre-commit review gate would operationalize the fast tier for code review, giving developers immediate AI feedback before shared resources (CI, human reviewers) are engaged. The repo's project convention documentation (AGENTS.md rules, canonical patterns, Obsidian conventions) would serve as rich input to the AI reviewer prompt.

---

## 4. Contextual Severity Calibration

**Classification:** Missing

**Why:**

The repo has no mechanism for adjusting automated review depth or severity by module risk profile. The concept of blast radius and high-risk vs. low-risk code paths exists in isolated contexts (architecture-as-agent-affordance mentions blast radius for module design, crossroad-change-policy is planned but not yet created), but there is no `risk-profile.yaml` format, no module-level risk metadata, no risk-adjusted check selection, and no calibrated severity labels anywhere in the repo.

**What the repo has (adjacent, not equivalent):**

- `docs/canonical/human-afk-task-routing-gate.md:35` — Architecture dimension mentions "system-wide blast radius" as a criterion for routing tasks to human vs. agent — not about automated review severity calibration.
- `docs/canonical/architecture-as-agent-affordance.md:38` — "Reduced coupling to reduce blast radius" — about module design principles, not review severity.
- `docs/canonical/tested-degradation-ladder.md:29-60` — Classifies failures by type (retryable/unsafe/hold) with ordered escalation, not by module risk profile.
- `docs/system-of-record.md:213` — `crossroad-change-policy.md` documented as pending for high blast-radius file changes — governance policy, not automated severity calibration, and not yet created.
- `docs/canonical/eval-tier-stratification.md:26-49` — Tier-based eval selection by change type (prompt, model, tool, loop), not by module risk level.

**What is missing (confirmed NOT_FOUND):**

1. `risk-profile.yaml` format: Module-level risk metadata declaring risk level (`critical`, `high`, `medium`, `low`) and applicable check sets (style, correctness, security, performance, data integrity). NOT_FOUND as a file or template anywhere in the repo — the only occurrences are in the canary-test analysis itself (source document and extracted patterns).
2. Risk-adjusted review depth: Mechanism to select checks proportional to the blast radius and failure cost of the changed module. NOT_FOUND.
3. Calibrated severity labels: Severity levels that adjust based on which module changed, rather than applying uniform severity to all findings. NOT_FOUND.
4. Module risk profile maintenance and ownership: No canonical doc or curriculum lesson covers maintaining module risk metadata or periodic re-evaluation of risk classifications.
5. Feedback loop from false-positive rates per module into severity calibration: The canary-test analysis proposes this as a dependency, but no such loop exists in the repo.

**Locations searched:**
- `docs/canonical/` (all 55 canonical docs) — No `risk-profile.yaml` or module-level risk calibration.
- `curriculum/` — No lesson, exercise, or case study on module risk profiles for review calibration.
- `.opencode/skills/` — No skill for risk-based review depth adjustment.
- `docs/evidence/` — No risk profile data.
- `docs/decisions/` — Empty, no ADRs on risk calibration.

**Integration value:** High

This is a genuinely new concept for the repo that would add precision to the eval tier stratification and PR-gated eval enforcement. Currently, all eval tiers apply uniformly regardless of which module changed — a change to a help page receives the same review depth as a change to the payment module. Module-level risk profiles would make agentic review effort proportional to operational risk, reducing fatigue on low-risk changes and increasing scrutiny where failures have high cost. This pattern would feed into and be fed by both the Shadow Review Pipeline (false-positive data per module) and the Pre-Commit AI Review Gate (risk-adjusted prompt depth at pre-commit time).

---

## Summary

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Shadow Review Pipeline | Missing | Medium |
| 2 | Review Contract Checklist | Partial Coverage | Medium |
| 3 | Pre-Commit AI Review Gate | Partial Coverage | Medium |
| 4 | Contextual Severity Calibration | Missing | High |

**Key insight:** The long-running-agents repo has a mature eval infrastructure (tier stratification, constraint-anchored evaluation, PR-gated enforcement, generator-evaluator) that covers the *structural* dimensions of agentic evaluation. It is weaker on the *operational* dimensions specific to AI code review: building trust through shadow pipelines, structuring review output through dimensioned contracts, catching issues at pre-commit time with AI, and calibrating review depth by module risk. Two patterns (Shadow Review Pipeline, Contextual Severity Calibration) are fully novel contributions; two patterns (Review Contract Checklist, Pre-Commit AI Review Gate) extend existing concepts into the AI code review domain.

**Dependency chain among these patterns:** The canary-test analysis identifies a sequential dependency: Review Contract Checklist enables Shadow Review Pipeline (structured findings needed for agreement metrics); Shadow Review Pipeline generates efficacy data that feeds Contextual Severity Calibration (false-positive rates per module); Contextual Severity Calibration informs Pre-Commit AI Review Gate (risk-adjusted prompt depth). All four patterns together form a continuous improvement loop for AI code review trust and precision.

---

*Created: 2026-06-15 | From: Canary Test Code Review pattern classification | Precedence: analysis*
