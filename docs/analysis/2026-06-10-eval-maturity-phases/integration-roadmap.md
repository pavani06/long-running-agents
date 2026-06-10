---
title: "Integration Roadmap: Eval Maturity Patterns -> long-running-agents"
type: analysis
date: 2026-06-10
domain: eval-maturity
aliases: []
tags: [analise, evals, maturity-model, roadmap]
last_updated: 2026-06-10
---

# Integration Roadmap: Eval Maturity Patterns -> long-running-agents

**Date:** 2026-06-10  
**Type:** Analysis  
**Precedence:** Level 4 (`docs/system-of-record.md:10`)  
**Source:** `docs/analysis/2026-06-10-eval-maturity-phases/classification.md`

---

## Objective

Map the 9 eval-maturity patterns extracted in this analysis package to concrete curriculum, canonical documentation, PR workflow, and harness-evolution integration points. The roadmap prioritizes Phase 6 curriculum integration, not runtime implementation.

**Classification note:** the task handoff says the classification produced 6 Partial Coverage patterns and 2 Better Implementation patterns. The source classification file currently lists 7 Partial Coverage patterns and 2 Better Implementation patterns: pattern 9, Eval-to-Production Correlation Tracking, is also marked Partial Coverage (`classification.md:122`, `classification.md:124`, `classification.md:148`). This roadmap follows the checked-in classification source and calls out the missing canonical artifact for pattern 9.

---

## Summary Matrix

| # | Pattern | Classification | Impact | Effort | Priority | Integration Surface |
|---|---|---|---|---|---|---|
| 4 | Production-Grounded Eval Sampling | Partial Coverage | High | Medium | P0 | `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`, future production-sampled eval corpus |
| 6 | PR-Gated Eval Enforcement | Partial Coverage | High | Medium | P0 | `.github/PULL_REQUEST_TEMPLATE.md`, `.opencode/skills/issue-review/SKILL.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`, future eval report template |
| 7 | Production Failure Regression Flywheel | Partial Coverage | High | Medium | P0 | `docs/canonical/late-failure-regression-suite.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`, `curriculum/08-tools-templates/evaluation-rubric-template.md`, incident-to-regression workflow |
| 9 | Eval-to-Production Correlation Tracking | Partial Coverage | High | Medium | P1 | `curriculum/05-core-concepts/08-evaluation-rubrics.md`, `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`, future correlation dashboard/report |
| 2 | Repeatable Agent Spot-Check Set | Partial Coverage | Medium | Low | P1 | `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`, `curriculum/02-nivel-2-practical-patterns/exercises/`, `curriculum/07-implementation-guides/05-trace-analysis-guide.md`, seed eval checklist |
| 5 | Eval Tier Stratification | Partial Coverage | Medium | Medium | P1 | `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`, `.opencode/skills/issue-review/SKILL.md`, `package.json`, future tier registry |
| 1 | Pain-Signal Eval Progression Gate | Partial Coverage | Medium | Low | P2 | `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`, `curriculum/05-core-concepts/06-harness-evolution.md`, eval maturity decision checklist |
| 3 | Metricized Agent Eval Contract | Better Implementation | Low | Low | Reference | Already stronger in Sprint Contracts, KODA rubrics, and baseline/candidate comparison |
| 8 | Canary Eval Rollout Gate | Better Implementation | Low | Low | Reference | Already stronger in harness-evolution rollout stages, production metrics, rollback, and observation |

Priority rationale: P0 patterns close high-impact operational gaps that affect whether eval evidence represents production, blocks risky PRs, and improves after incidents. P1 patterns organize the eval system into repeatable sets, tiers, and correlation checks. P2 makes maturity decisions explicit but depends on the lower-level surfaces becoming visible.

---

## Artifacts Created In This Analysis Package

### Analysis Artifacts - `docs/analysis/2026-06-10-eval-maturity-phases/`

| File | Purpose |
|---|---|
| `mental-model.md` | Repository model, curriculum structure, documentation precedence, and existing gaps |
| `mental-model.yaml` | Structured version of the repository model |
| `analysis.md` | Non-obvious knowledge extraction from the eval-maturity source |
| `analysis.yaml` | Structured extraction of frameworks, patterns, lessons, tradeoffs, and failure modes |
| `patterns.md` | 9 extracted operational eval patterns |
| `patterns.yaml` | Structured pattern inventory |
| `classification.md` | Pattern-by-pattern classification against the repo with evidence |
| `classification.yaml` | Structured classification evidence |
| `integration-roadmap.md` | This roadmap for Phase 6 integration |

### Canonical Docs Created - `docs/canonical/`

| File | Pattern | Classification |
|---|---|---|
| `pain-signal-eval-progression-gate.md` | Pain-Signal Eval Progression Gate | Partial Coverage |
| `repeatable-agent-spot-check-set.md` | Repeatable Agent Spot-Check Set | Partial Coverage |
| `production-grounded-eval-sampling.md` | Production-Grounded Eval Sampling | Partial Coverage |
| `eval-tier-stratification.md` | Eval Tier Stratification | Partial Coverage |
| `pr-gated-eval-enforcement.md` | PR-Gated Eval Enforcement | Partial Coverage |
| `production-failure-regression-flywheel.md` | Production Failure Regression Flywheel | Partial Coverage |

### Existing Better Implementations Reused

| Pattern | Existing stronger implementation |
|---|---|
| Metricized Agent Eval Contract | Sprint Contract KPIs, thresholds, measurement sources, reproducible metrics, KODA rubric IDs, approval thresholds, confidence and overall scores, and baseline/candidate metric gates (`classification.md:42`, `classification.md:46`, `classification.md:47`, `classification.md:49`, `classification.md:50`) |
| Canary Eval Rollout Gate | Staging, 5%, 25%, and 100% rollout stages with regression gates, N+1 gates, production metrics, trace sampling, rollback commands, and post-rollout observation (`classification.md:113`, `classification.md:117`, `classification.md:118`, `classification.md:119`, `classification.md:120`) |

### Artifact Gap

| Pattern | Gap |
|---|---|
| Eval-to-Production Correlation Tracking | Classified as Partial Coverage in `classification.md`, but no canonical doc was created in the Phase 4 list. Phase 6 should either create `docs/canonical/eval-to-production-correlation-tracking.md` or explicitly decide that this remains analysis-only until the dashboard/reporting surface exists. |

---

## Cross-Reference Table: Patterns To Curriculum Levels

| # | Pattern | Curriculum Levels To Teach It | Concrete Curriculum Files |
|---|---|---|---|
| 1 | Pain-Signal Eval Progression Gate | Level 3 for harness evolution decisions; Level 4 for KODA improvement governance; Core Concept 6 for maturity framing | `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`, `curriculum/05-core-concepts/06-harness-evolution.md` |
| 2 | Repeatable Agent Spot-Check Set | Level 2 for first repeatable trace-based evals; Level 4 for KODA critical workflows; implementation guide for trace analysis | `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`, `curriculum/02-nivel-2-practical-patterns/exercises/`, `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md`, `curriculum/07-implementation-guides/05-trace-analysis-guide.md` |
| 3 | Metricized Agent Eval Contract | Level 2 and Core Concepts already teach it; templates operationalize it | `curriculum/02-nivel-2-practical-patterns/02-sprint-contracts.md`, `curriculum/02-nivel-2-practical-patterns/03-rubric-design.md`, `curriculum/05-core-concepts/04-sprint-contracts.md`, `curriculum/05-core-concepts/08-evaluation-rubrics.md`, `curriculum/08-tools-templates/sprint-contract-template.md` |
| 4 | Production-Grounded Eval Sampling | Level 3 for architecture and replay; Level 4 for KODA production readiness; implementation guide for corpus/replay mechanics | `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`, `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` |
| 5 | Eval Tier Stratification | Level 2 introduces fast seed checks; Level 3 and guides teach medium/deep gates; operational skills enforce tiers | `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`, `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`, `.opencode/skills/issue-review/SKILL.md` |
| 6 | PR-Gated Eval Enforcement | Level 3/4 for risk-based change control; repo workflow for actual PR enforcement | `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`, `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.opencode/skills/issue-review/SKILL.md` |
| 7 | Production Failure Regression Flywheel | Level 2 trace reading for failure diagnosis; Level 3/4 for permanent regression creation; templates for rubric/evidence records | `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md`, `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md`, `curriculum/08-tools-templates/evaluation-rubric-template.md` |
| 8 | Canary Eval Rollout Gate | Level 3 and implementation guide already teach stronger rollout gates; Level 4 applies readiness to KODA features | `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md`, `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` |
| 9 | Eval-to-Production Correlation Tracking | Core Concept 8 for calibration theory; Level 4 and guides for production-readiness dashboards | `curriculum/05-core-concepts/08-evaluation-rubrics.md`, `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` |

---

## Gap Analysis

### Remaining Partial Coverage Patterns

| Pattern | What Exists | What Is Still Missing |
|---|---|---|
| Pain-Signal Eval Progression Gate | Harness-evolution questions already ask what failure a component prevents, frequency, cost, A/B or replay proof, and rollback path (`classification.md:19`). Harness-improvement proposals already require evidence, rollback/config disablement, owner, cadence, and metrics (`classification.md:20`). | A named eval-maturity review gate that maps user complaints, manual eval bottlenecks, score-feedback mismatch, and escaped edge cases to the next minimum eval capability (`classification.md:15`, `docs/canonical/pain-signal-eval-progression-gate.md:56`). |
| Repeatable Agent Spot-Check Set | Trace-reading has four reconstructed KODA trace cases with trace JSON, manual analysis, script output, diagnosis, and lesson (`classification.md:32`). The same module says cases can support practice, training, CI/CD automation, and comparison (`classification.md:33`). | A small named seed eval set with stable case IDs, expected outcomes, acceptable tool behavior, state fixtures, saved baselines, ownership, and refresh rules (`classification.md:28`, `docs/canonical/repeatable-agent-spot-check-set.md:57`). |
| Production-Grounded Eval Sampling | KODA materials already require replay of real anonymized conversations before canary, shadow traffic samples, baseline/candidate comparison, metrics, manual trace review, and canary trace sampling (`classification.md:61`, `classification.md:62`, `classification.md:63`). | A first-class production-sampled eval corpus with privacy filters, retention policy, coverage metadata, labels, replay infrastructure, refresh cadence, and deletion process (`classification.md:57`, `docs/canonical/production-grounded-eval-sampling.md:57`). |
| Eval Tier Stratification | The repo already has local npm gates, component regression batteries, N+1 gates, staging shadow tests, canary stages, and issue-review gates (`classification.md:75`, `classification.md:76`). | Explicit fast/medium/deep tier taxonomy with runtime, cost, flakiness, trigger, threshold, reporting, owner, skipped-tier visibility, and quarantine policy (`classification.md:71`, `docs/canonical/eval-tier-stratification.md:55`). |
| PR-Gated Eval Enforcement | The issue-review skill validates worktrees, creates draft PRs, runs second-agent review, and stops before merge; the PR template requires test evidence and regression-suite verification (`classification.md:88`, `classification.md:89`). | Eval-specific PR reports for prompt/model/tool/context/rubric/loop changes with baseline/candidate deltas, eval tiers run, quality/latency/cost impact, thresholds, failure examples, and merge/waiver policy (`classification.md:84`, `docs/canonical/pr-gated-eval-enforcement.md:60`). |
| Production Failure Regression Flywheel | Late-Failure Regression Suite already turns late-session context failures into durable regression cases, and the harness playbook requires permanent regression cases for late context incidents (`classification.md:102`, `classification.md:103`, `classification.md:104`). | A general all-failure flywheel covering user complaints, escaped edge cases, tool misuse, state persistence failures, scoring gaps, deduplication, pruning, and backfill reporting (`classification.md:98`, `docs/canonical/production-failure-regression-flywheel.md:60`). |
| Eval-to-Production Correlation Tracking | Evaluation Rubrics already teaches continuous calibration by comparing production rubric scores with real outcomes; harness dashboards already compare baseline/candidate production metrics; KODA readiness requires calibrated rubrics, replayable traces, and canary metrics (`classification.md:131`, `classification.md:132`, `classification.md:133`). | A named correlation tracking system that audits whether eval scores predict production outcomes over time, with score-drift alerts, recalibration triggers, and a canonical/reporting surface (`classification.md:127`, `classification.md:134`). |

### Better Implementation Patterns

| Pattern | Roadmap Treatment |
|---|---|
| Metricized Agent Eval Contract | Do not create a new canonical pattern. Add cross-references from Phase 6 curriculum edits to the existing Sprint Contract, Evaluation Rubric, KODA rubric, and baseline/candidate gate surfaces. |
| Canary Eval Rollout Gate | Do not create a new canonical pattern. Use it as supporting context when editing harness evolution and KODA readiness material, because the repo already exceeds the extracted pattern. |

---

## Integration Recommendations For Phase 6

### P0. Add Eval Evidence To PR Workflow

| Target | Add |
|---|---|
| `.github/PULL_REQUEST_TEMPLATE.md` | Add an optional `Eval impact` section for prompt, model, tool, context, memory, rubric, and agent-loop changes. Include baseline version, candidate version, eval tiers run, quality delta, latency delta, cost delta, threshold result, skipped tiers, and waiver rationale. |
| `.opencode/skills/issue-review/SKILL.md` | Extend surface-specific gates so eval-sensitive changes require an eval report summary before draft PR review completes. Map the report to PR body evidence instead of relying only on generic test output. |
| `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Add a reusable PR eval report example near the existing baseline/candidate metric comparison, so contributors learn the exact evidence shape before merge. |

Rationale: the repo already has PR validation and draft-review discipline, but no eval-specific merge evidence for agent behavior changes (`classification.md:84`, `classification.md:88`, `classification.md:89`).

### P0. Formalize Production-Sampled Eval Corpus

| Target | Add |
|---|---|
| `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Add a `Production-sampled eval corpus` subsection after shadow testing: eligible surfaces, redaction, retention, metadata, labels, replay command shape, refresh cadence, and deletion rules. |
| `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md` | Upgrade the repeated "replay de conversas reais anonimizadas antes de canary" cards into a named eval-corpus pattern with metadata and labeling requirements. |
| `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` | Add production-sampled eval corpus requirements to proposals that rely on shadow tests or canaries. |

Rationale: production replay and trace sampling already exist as adjacent mechanics, but not as a governed corpus with privacy, retention, coverage, labels, replay, and refresh (`classification.md:57`, `docs/canonical/production-grounded-eval-sampling.md:61`).

### P0. Generalize Incident-To-Regression Flywheel

| Target | Add |
|---|---|
| `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Expand the existing Late-Failure Regression Suite into an all-failure regression flywheel section with intake, taxonomy, fixture fields, tier assignment, deduplication, and backfill proof. |
| `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` | Add a follow-up exercise: convert one diagnosed trace failure into a durable regression eval case with expected behavior and failure class. |
| `curriculum/08-tools-templates/evaluation-rubric-template.md` | Add a regression-case template that links incident output, rubric label, expected behavior, suite tier, and owner. |

Rationale: the late-session version is already strong, but the repo lacks a generalized flywheel across production failures, complaints, tool misuse, scoring gaps, and suite deduplication (`classification.md:98`, `docs/canonical/production-failure-regression-flywheel.md:64`).

### P1. Create Eval Tier Registry And Seed Spot-Check Set

| Target | Add |
|---|---|
| `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` | Name the four reconstructed KODA traces as the first `fast` spot-check seed set, with `case_id`, expected outcome, acceptable tool behavior, state fixture, baseline, owner, and refresh trigger. |
| `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Add a fast/medium/deep registry table mapping local checks, spot checks, component regression, N+1 fixtures, production-sampled replays, shadow tests, and canaries to triggers and decision power. |
| `.opencode/skills/issue-review/SKILL.md` | Reference the tier registry when selecting required validation for eval-sensitive PRs. |

Rationale: repeatable cases and layered gates already exist, but the missing contracts are naming, metadata, tier assignment, and trigger policy (`classification.md:28`, `classification.md:71`).

### P1. Add Correlation Tracking As A First-Class Concept

| Target | Add |
|---|---|
| `docs/canonical/eval-to-production-correlation-tracking.md` | Create the missing canonical doc if Phase 6 is allowed to update canonical docs; otherwise record it as a deferred canonical artifact. |
| `curriculum/05-core-concepts/08-evaluation-rubrics.md` | Extend Continuous Calibration Loop with score-to-production correlation reports, score drift, recalibration triggers, and examples of misleading scores. |
| `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Add a dashboard/report shape that compares eval score distributions with incomplete-response rate, evaluator rejection rate, support tickets, CSAT proxy, latency, and cost. |

Rationale: correlation is classified as Partial Coverage and high value, but it is the only partial pattern from `classification.md` without a newly created canonical doc (`classification.md:124`, `classification.md:127`, `classification.md:134`).

### P2. Add Pain-Signal Maturity Gate

| Target | Add |
|---|---|
| `curriculum/05-core-concepts/06-harness-evolution.md` | Add a short eval-maturity gate that asks which pain signal justifies the next eval capability. |
| `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` | Add a proposal field: `eval_maturity_trigger`, with allowed values such as user complaint, manual bottleneck, score-feedback mismatch, escaped edge case, and release-risk increase. |
| `curriculum/08-tools-templates/architecture-decision-record-template.md` | Add optional fields for current eval capability, chosen next capability, deferred capabilities, owner, operating cost, and review date. |

Rationale: harness governance already has evidence and rollback discipline, so this is a low-effort naming and decision-template addition (`classification.md:15`, `docs/canonical/pain-signal-eval-progression-gate.md:42`).

---

## Suggested Phase 6 Edit Order

1. Update `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` first, because it is the common integration surface for production sampling, tiers, PR eval reports, canary evidence, and failure regression.
2. Update `.github/PULL_REQUEST_TEMPLATE.md` and `.opencode/skills/issue-review/SKILL.md` together, so the contributor-facing PR shape and agent review workflow agree.
3. Update `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md` to turn existing trace cases into the seed spot-check set and regression-case exercise.
4. Update `curriculum/05-core-concepts/08-evaluation-rubrics.md` to teach correlation tracking and calibration drift.
5. Update `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` and `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md` to connect KODA-specific improvement proposals to production-sampled evals, pain-signal triggers, and incident regressions.
6. Decide whether Phase 6 should create `docs/canonical/eval-to-production-correlation-tracking.md`; if not, leave an explicit TODO in the Phase 6 summary.

---

## Precedence Alignment

- `docs/canonical/` now has authoritative docs for 6 eval-maturity partial patterns and should guide curriculum edits before analysis docs.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md` remains the evidence-backed source for the full 9-pattern inventory and identifies pattern 9 as a remaining partial gap.
- `docs/system-of-record.md` says canonical docs outrank analysis docs, while analysis docs outrank READMEs and operational summaries (`docs/system-of-record.md:7`, `docs/system-of-record.md:8`, `docs/system-of-record.md:10`, `docs/system-of-record.md:12`).
- No ADR supersedes this roadmap because `docs/decisions/` is empty in this checkout (`docs/system-of-record.md:105`, `docs/system-of-record.md:107`).

---

## References

- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md` - classification and evidence for all 9 patterns.
- `docs/analysis/2026-06-10-eval-maturity-phases/patterns.md` - extracted pattern definitions.
- `docs/analysis/2026-06-10-eval-maturity-phases/analysis.md` - source knowledge extraction and eval maturity framework.
- `docs/canonical/pain-signal-eval-progression-gate.md` - canonical partial pattern.
- `docs/canonical/repeatable-agent-spot-check-set.md` - canonical partial pattern.
- `docs/canonical/production-grounded-eval-sampling.md` - canonical partial pattern.
- `docs/canonical/eval-tier-stratification.md` - canonical partial pattern.
- `docs/canonical/pr-gated-eval-enforcement.md` - canonical partial pattern.
- `docs/canonical/production-failure-regression-flywheel.md` - canonical partial pattern.
- `docs/system-of-record.md` - documentation precedence and curriculum source map.

---

*Created: 2026-06-10 | From: Eval maturity pattern classification | Precedence: analysis*
