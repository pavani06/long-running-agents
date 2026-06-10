---
title: "Agentic Eval-Driven Development Patterns"
type: digest
date: 2026-06-10
sources_covered: 2
sources:
  - "docs/analysis/2026-06-10-eval-maturity-phases/analysis.md"
  - "docs/analysis/2026-06-10-eval-maturity-phases/analysis.yaml"
tags: [synthesis, ai, agents, evals, eval-driven-development]
---

# Agentic Eval-Driven Development Patterns

Scope: extracted from the phase 1 knowledge analysis of Phil Hetzel's "The maturity phases of running evals" talk. The five-phase maturity model itself is excluded; only operational mechanisms that can be implemented in agentic systems are kept.

## 1. Pain-Signal Eval Progression Gate

- **name:** Pain-Signal Eval Progression Gate
- **problem solved:** Agent teams either keep shipping by feel for too long or overbuild eval infrastructure before the team can use it.
- **inputs:**
  - Current eval practice and automation level.
  - Pain signals such as user complaints, manual eval bottlenecks, score-to-feedback mismatch, or escaped edge cases.
  - Existing eval artifacts, production feedback, and team capacity.
- **outputs:**
  - A decision to stay at the current eval capability or add the next minimum capability.
  - Explicit transition criteria tied to observed failure modes.
  - Deferred eval investments that are not yet justified by the current pain.
- **benefits:**
  - Turns eval maturity into an operational decision instead of a calendar goal.
  - Reduces premature platform work that the team will not use.
  - Keeps investment focused on the next reliability bottleneck in the agent workflow.
- **limitations:**
  - Requires honest signals from users, production, or development workflow pain.
  - Can underinvest when a system has little traffic or weak feedback collection.
  - Does not replace organizational commitment to act on eval results.

## 2. Repeatable Agent Spot-Check Set

- **name:** Repeatable Agent Spot-Check Set
- **problem solved:** Manual prompt trials cannot reliably detect regressions in multi-step agent behavior.
- **inputs:**
  - Known important agent workflows, prompts, tasks, and user intents.
  - Expected outcomes, acceptable tool calls, and relevant state or memory fixtures.
  - A lightweight runner such as a spreadsheet, script, or local harness.
- **outputs:**
  - A small repeatable eval set for critical agent paths.
  - Baseline results for the current prompt, model, or agent configuration.
  - A seed corpus that later eval infrastructure can automate.
- **benefits:**
  - Creates the first repeatable safety net without requiring production-scale infrastructure.
  - Makes obvious regressions visible before users find them.
  - Gives the team shared examples of what good agent behavior means.
- **limitations:**
  - Covers mostly known cases from team memory, not unknown unknowns.
  - Becomes a bottleneck as the set grows if execution stays manual.
  - Does not prove correlation with real production distribution.

## 3. Metricized Agent Eval Contract

- **name:** Metricized Agent Eval Contract
- **problem solved:** Teams cannot compare agent versions unless "good" is translated into measurable criteria.
- **inputs:**
  - Eval cases with expected behavior or scoring rubrics.
  - Quality dimensions such as task success, instruction following, tool-call correctness, latency, and cost.
  - Model, prompt, tool, and configuration versions under evaluation.
- **outputs:**
  - Eval scorecards with pass/fail thresholds and trendable metrics.
  - Regression, improvement, latency, and cost deltas between agent versions.
  - Candidate cases for deeper review when metrics and human judgment diverge.
- **benefits:**
  - Makes agent quality comparable across changes.
  - Enables CI, PR, or release systems to consume eval results.
  - Exposes tradeoffs between quality, latency, and cost instead of optimizing only for apparent accuracy.
- **limitations:**
  - Metrics can become false confidence if scoring criteria do not reflect user outcomes.
  - Rubrics and judges need calibration as the product changes.
  - Complex agent tasks may require expensive or partially subjective scoring.

## 4. Production-Grounded Eval Sampling

- **name:** Production-Grounded Eval Sampling
- **problem solved:** Hand-authored eval sets miss real user distributions and long-tail agent failures.
- **inputs:**
  - Production interactions, user requests, agent traces, tool results, and relevant state snapshots.
  - Privacy filters, retention rules, and sampling criteria.
  - Replay infrastructure that can run captured interactions against a candidate agent version.
- **outputs:**
  - A representative replayable eval set sampled from real usage.
  - Coverage information about which production segments are represented.
  - Refreshed eval cases as traffic and product behavior change.
- **benefits:**
  - Aligns eval distribution with the distribution the agent actually serves.
  - Finds failures that hand-written cases are unlikely to anticipate.
  - Grounds prompt, model, and tool changes in observed user behavior.
- **limitations:**
  - Requires enough production volume to sample meaningfully.
  - Needs capture, storage, replay, redaction, and labeling infrastructure.
  - Can still miss rare edge cases if sampling or traffic volume is weak.

## 5. Eval Tier Stratification

- **name:** Eval Tier Stratification
- **problem solved:** A single eval suite cannot provide fast developer feedback, PR protection, and deep regression coverage at the same time.
- **inputs:**
  - Eval inventory with runtime, cost, flakiness, and coverage metadata.
  - Development events such as commits, PRs, releases, and scheduled runs.
  - Risk areas in the agent workflow, including tools, memory, handoffs, and long-running state.
- **outputs:**
  - Fast, medium, and deep eval suites with distinct triggers.
  - Different thresholds and reporting expectations per tier.
  - A cost-aware eval schedule that matches feedback latency to risk.
- **benefits:**
  - Keeps the inner development loop quick while preserving deeper coverage.
  - Makes expensive agent evals usable without blocking every edit.
  - Gives reviewers and operators confidence at the right level of depth for each decision.
- **limitations:**
  - Adds operational complexity around suite ownership, thresholds, and scheduling.
  - Deep failures may arrive after the developer has moved on.
  - Poor tier design can create gaps where no suite covers a risky behavior.

## 6. PR-Gated Eval Enforcement

- **name:** PR-Gated Eval Enforcement
- **problem solved:** Prompt, tool, model, or agent-loop changes can merge without visible evidence of quality impact.
- **inputs:**
  - A code, prompt, config, model, or tool change under review.
  - Relevant eval tiers, baseline metrics, and merge thresholds.
  - Reviewer policy for blocking, accepting, or escalating eval regressions.
- **outputs:**
  - Eval results attached to the PR.
  - A pass, fail, or needs-review signal for the change.
  - Reviewer-ready deltas showing quality, latency, and cost impact.
- **benefits:**
  - Moves eval from a separate activity into the daily development workflow.
  - Makes "do not ship without evals" enforceable and auditable.
  - Gives reviewers concrete evidence beyond prompt diffs and intuition.
- **limitations:**
  - Gates are only reliable when evals correlate with production outcomes.
  - Expensive or flaky evals can slow delivery if tiers are not designed well.
  - Teams can still bypass the gate without leadership and process support.

## 7. Production Failure Regression Flywheel

- **name:** Production Failure Regression Flywheel
- **problem solved:** Production failures repeat when they depend on human memory to become permanent tests.
- **inputs:**
  - A production failure, user complaint, incident, or escaped edge case.
  - The captured interaction, tool trace, state snapshot, and expected behavior label.
  - Failure classification such as prompt issue, tool misuse, context loss, or scoring gap.
- **outputs:**
  - A new regression eval case added to the appropriate suite.
  - Backfilled pass/fail results for the current and candidate agent versions.
  - Updated coverage that preserves the incident as institutional memory.
- **benefits:**
  - Makes the eval suite self-improving as the agent encounters real failures.
  - Reduces recurrence of known failures in long-running workflows.
  - Converts production incidents into durable development assets.
- **limitations:**
  - Can add noise when expected behavior is unclear or the incident is misclassified.
  - Requires reliable trace capture, redaction, and replay.
  - Needs triage to avoid bloating suites with duplicate or low-value cases.

## 8. Canary Eval Rollout Gate

- **name:** Canary Eval Rollout Gate
- **problem solved:** Full rollout amplifies bad agent changes before the team can observe real impact.
- **inputs:**
  - Candidate agent release, prompt version, model change, or tool integration.
  - Canary population, rollout policy, eval thresholds, and rollback criteria.
  - Production metrics and user feedback from the canary segment.
- **outputs:**
  - A promote, hold, or rollback action for the rollout.
  - Canary reports combining eval gates with production signals.
  - Reduced blast radius for regressions in agent behavior.
- **benefits:**
  - Tests agent changes against real traffic before broad exposure.
  - Connects offline eval confidence with live operational evidence.
  - Limits user impact when prompts, tools, or models regress.
- **limitations:**
  - Requires traffic routing, observability, and rollback infrastructure.
  - Rare workflows may not appear during the canary window.
  - Promotion decisions remain risky if eval gates and production metrics are poorly calibrated.

## 9. Eval-to-Production Correlation Tracking

- **name:** Eval-to-Production Correlation Tracking
- **problem solved:** Eval scores become false safety signals when they stop predicting user outcomes.
- **inputs:**
  - Eval run history, score distributions, and version metadata.
  - Production metrics such as task success, user complaints, escalations, latency, cost, or retention.
  - Release, model, prompt, and tool-change markers.
- **outputs:**
  - Dashboards or reports showing correlation between eval scores and production outcomes.
  - Alerts or review triggers when the score no longer predicts user feedback.
  - Calibration decisions for rubrics, thresholds, sampling, or eval suite composition.
- **benefits:**
  - Audits whether the eval system is measuring useful agent quality.
  - Detects metric theater before it becomes a shipping habit.
  - Improves trust in eval gates by tying them to real-world outcomes.
- **limitations:**
  - Requires enough production data and stable instrumentation.
  - Correlation can be confounded by traffic mix, releases, or external events.
  - Low-volume agents may need qualitative review alongside quantitative tracking.
