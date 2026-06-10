---
title: "Eval Maturity Pattern Classification"
type: analysis
date: 2026-06-10
domain: eval-maturity
aliases: []
tags: [analise, evals, maturity-model, classification]
last_updated: 2026-06-10
---

# Eval Maturity Pattern Classification

**Date:** 2026-06-10  
**Repository:** `long-running-agents`  
**Scope:** Classify operational eval-maturity mechanisms from `patterns.md` / `patterns.yaml` against the target repository.  
**Precedence used:** `docs/decisions/` -> `docs/canonical/` -> `docs/evidence/` -> `docs/analysis/` -> `curriculum/` -> READMEs / operational summaries, per `docs/system-of-record.md:5`, `docs/system-of-record.md:7`, `docs/system-of-record.md:8`, `docs/system-of-record.md:9`, `docs/system-of-record.md:10`, `docs/system-of-record.md:11`, `docs/system-of-record.md:12`.

Search note: `docs/decisions/` and `docs/evidence/` contain only `.gitkeep` files in this checkout, so no accepted ADR or validated evidence source supersedes the canonical/curriculum evidence below.

## 1. Pain-Signal Eval Progression Gate

**Classification:** Partial Coverage  
**Integration value:** Medium

The repo has an adjacent harness-evolution decision habit based on observed failures, cost, risk, rollback, and evidence. It does not formalize eval maturity as a progression gate where user complaints, manual-eval bottlenecks, score/feedback mismatch, and escaped edge cases decide the next minimum eval capability.

**Evidence:**

- Existing adjacent mechanic: the KODA harness-evolution framework asks what concrete failure a component prevents, how often it prevented that failure, its token/latency/maintenance cost, whether A/B or replay proves removal safe, and rollback time (`curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1490`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1491`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1492`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1493`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1497`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1498`).
- Existing adjacent mechanic: the harness-improvement proposals require evidence, rollback/config disablement, technical owner, review cadence, and metrics such as critical-fact loss or harness value (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:498`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:502`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:504`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:505`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:506`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:559`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:563`).
- NOT_FOUND for the formal eval-maturity trigger: searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/skills/`, and prior `docs/analysis/` for `Pain-Signal`, `pain signal`, `manual eval bottleneck`, `score-to-feedback`, and `next eval capability`; matches outside the source extraction were absent.

## 2. Repeatable Agent Spot-Check Set

**Classification:** Partial Coverage  
**Integration value:** Medium

The repo has repeatable trace cases, regression batteries, and practical guidance to turn cases into CI tests. It does not define a small named spot-check eval set with critical workflows, expected outcomes, acceptable tool behavior, state fixtures, and saved baselines as a first maturity step.

**Evidence:**

- Existing adjacent mechanic: the trace-reading curriculum gives four reconstructed real KODA trace cases with trace JSON, manual analysis, script output, diagnosis, and lesson (`curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3876`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3880`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3881`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3882`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3883`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3884`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:3885`).
- Existing adjacent mechanic: the same module says those cases can be used for practice, training, CI/CD automation, and comparison with new traces (`curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:4580`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:4582`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:4583`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:4584`, `curriculum/02-nivel-2-practical-patterns/04-trace-reading.md:4585`).
- Existing adjacent mechanic: the harness-evolution playbook includes a component-specific regression battery with concrete long-context and context-limit cases (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:748`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:752`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:756`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:760`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:764`).
- NOT_FOUND for the named seed-set formalization: searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/skills/`, and prior `docs/analysis/` for `Repeatable Agent Spot-Check Set`, `spot-check eval set`, `baseline results`, and `acceptable tool behavior`; no equivalent named pattern was found outside the source extraction.

## 3. Metricized Agent Eval Contract

**Classification:** Better Implementation  
**Integration value:** Low

The repo has a more mature version than the extracted pattern: Sprint Contracts define KPIs, thresholds, measurement sources, sign-off, and versioned agreement; KODA rubrics define rubric IDs, approval thresholds, confidence/overall scores, blockers, and auditability; the harness playbook compares baseline vs candidate metrics with explicit pass gates.

**Evidence:**

- Contract-level metricization: Sprint Contracts define KPIs, thresholds, measurement sources, and evaluator validation (`curriculum/08-tools-templates/sprint-contract-template.md:166`, `curriculum/08-tools-templates/sprint-contract-template.md:168`, `curriculum/08-tools-templates/sprint-contract-template.md:172`, `curriculum/08-tools-templates/sprint-contract-template.md:173`, `curriculum/08-tools-templates/sprint-contract-template.md:174`).
- Contract-level reproducibility: thresholds must be specific enough for another agent to reproduce the decision, and the JSON blueprint includes `approval_rate`, `constraint_accuracy`, `fit_score`, `token_cost`, and `latency_seconds` with thresholds and measurement artifacts (`curriculum/08-tools-templates/sprint-contract-template.md:181`, `curriculum/08-tools-templates/sprint-contract-template.md:308`, `curriculum/08-tools-templates/sprint-contract-template.md:309`, `curriculum/08-tools-templates/sprint-contract-template.md:310`, `curriculum/08-tools-templates/sprint-contract-template.md:311`).
- Rubric-level metricization: core rubrics teach dimensions, weights, scoring levels, thresholds, anchors, evidence rules, and decision policy (`curriculum/05-core-concepts/08-evaluation-rubrics.md:75`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:77`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:78`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:79`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:80`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:81`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:82`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:83`).
- KODA-specific operational metricization: KODA rubrics use `rubric_id`, `approval_threshold`, `confidence_score`, `overall_score`, and `generation_id`, then turn evaluator output into approve/reject/escalate decisions (`curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:7`, `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:10`, `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:42`, `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:45`, `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:46`, `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:111`, `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:116`).
- Baseline/candidate score comparison: the harness playbook records baseline, candidate, delta, and gate status for incomplete-response rate, token budget, latency, and CSAT proxy (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1643`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1646`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1654`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1655`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1656`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1657`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1658`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1659`).

## 4. Production-Grounded Eval Sampling

**Classification:** Partial Coverage  
**Integration value:** High

The repo teaches replay of real anonymized conversations, shadow traffic samples, sampled trace review, and canary investigation. It does not define an end-to-end production-sampled eval dataset with privacy filters, retention policy, coverage metadata, expected-behavior labeling, and replay infrastructure as a first-class eval artifact.

**Evidence:**

- Existing adjacent mechanic: KODA harness evolution repeatedly requires replay of real anonymized conversations before canary (`curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1552`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1554`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1568`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1570`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1584`, `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1586`).
- Existing adjacent mechanic: the playbook configures shadow tests with `traffic_sample_percentage`, baseline/candidate comparison, metrics, and manual review of sampled traces (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:710`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:712`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:715`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:719`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:722`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:725`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:738`).
- Existing adjacent mechanic: canary investigation samples traces by flag, metric, window, and limit (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1669`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1672`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1673`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1674`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1675`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1676`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1679`).
- Missing formalization: no accepted ADR, canonical doc, evidence artifact, curriculum module, or `.opencode/skills/` workflow defines a production-sampled eval corpus with redaction/retention, representativeness coverage, labels, and refresh cadence. Searches covered `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/skills/`, and prior `docs/analysis/` for `production-grounded eval`, `representative replayable eval set`, `redaction`, `retention`, and `coverage information`.

## 5. Eval Tier Stratification

**Classification:** Partial Coverage  
**Integration value:** Medium

The repo has multiple validation layers: local npm gates, component regression batteries, N+1 long-session context gates, staging shadow tests, canary stages, and issue-review surface-specific gates. It does not organize evals into an explicit fast/medium/deep tier taxonomy with runtime, cost, flakiness, trigger, threshold, and reporting metadata.

**Evidence:**

- Existing adjacent mechanic: the issue-review skill has core gates and optional surface-specific gates including lint, unit, integration, dashboard, fixture parity, evidence verification, CI gates, and branch protection verification (`.opencode/skills/issue-review/SKILL.md:44`, `.opencode/skills/issue-review/SKILL.md:46`, `.opencode/skills/issue-review/SKILL.md:48`, `.opencode/skills/issue-review/SKILL.md:53`, `.opencode/skills/issue-review/SKILL.md:54`, `.opencode/skills/issue-review/SKILL.md:57`, `.opencode/skills/issue-review/SKILL.md:60`, `.opencode/skills/issue-review/SKILL.md:67`, `.opencode/skills/issue-review/SKILL.md:68`).
- Existing adjacent mechanic: the harness playbook separates lint/unit, component regression battery, N+1 long-session gate, staging shadow, and canary phases (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:743`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:748`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:776`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:783`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:787`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:788`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:789`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:790`).
- Missing formalization: searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/skills/`, and prior `docs/analysis/` for `Eval Tier Stratification`, `fast eval tier`, `medium eval tier`, `deep eval tier`, `cost-aware eval schedule`, and `flakiness`; no equivalent tier taxonomy was found outside the extracted pattern source.

## 6. PR-Gated Eval Enforcement

**Classification:** Partial Coverage  
**Integration value:** High

The repo has strong PR validation and review workflow, but it gates PRs mostly through generic test/regression commands, PR-template checklists, and second-agent review. It does not require eval-specific reports showing baseline deltas, thresholds, quality/latency/cost impact, and merge policy for prompt, model, tool, or agent-loop changes.

**Evidence:**

- Existing adjacent mechanic: issue-review validates the worktree, creates a draft PR, runs second-agent review, and stops before merge (`.opencode/skills/issue-review/SKILL.md:12`, `.opencode/skills/issue-review/SKILL.md:14`, `.opencode/skills/issue-review/SKILL.md:44`, `.opencode/skills/issue-review/SKILL.md:73`, `.opencode/skills/issue-review/SKILL.md:90`, `.opencode/skills/issue-review/SKILL.md:150`, `.opencode/skills/issue-review/SKILL.md:183`, `.opencode/skills/issue-review/SKILL.md:209`).
- Existing adjacent mechanic: the PR template requires test evidence and regression-suite verification for crossroad files (`.github/PULL_REQUEST_TEMPLATE.md:11`, `.github/PULL_REQUEST_TEMPLATE.md:13`, `.github/PULL_REQUEST_TEMPLATE.md:15`, `.github/PULL_REQUEST_TEMPLATE.md:16`, `.github/PULL_REQUEST_TEMPLATE.md:40`, `.github/PULL_REQUEST_TEMPLATE.md:44`).
- Existing adjacent mechanic: issue-review says behavior or architecture changes should update relevant canonical docs, guides, evidence, or ADRs and should not contradict accepted ADRs (`.opencode/skills/issue-review/SKILL.md:77`, `.opencode/skills/issue-review/SKILL.md:87`, `.opencode/skills/issue-review/SKILL.md:88`).
- Missing eval-specific PR gate: searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/skills/`, `.github/`, and prior `docs/analysis/` for `PR-Gated Eval Enforcement`, `eval results attached to the PR`, `baseline comparator`, `quality latency cost impact`, and `prompt/model/tool change eval`; no first-class eval report attachment or merge threshold policy was found.

## 7. Production Failure Regression Flywheel

**Classification:** Partial Coverage  
**Integration value:** High

The repo has a strong late-session context version of this flywheel and rubric guidance to use old incidents as regression examples. It is not generalized across all production failures, complaints, escaped edge cases, tool misuse, scoring gaps, and suite deduplication as a broad eval flywheel.

**Evidence:**

- Canonical context-specific version: Late-Failure Regression Suite says every observed late-session context failure becomes a durable regression case with session shape, context strategy, expected N+1 behavior, and root-cause category (`docs/canonical/late-failure-regression-suite.md:17`, `docs/canonical/late-failure-regression-suite.md:19`, `docs/canonical/late-failure-regression-suite.md:21`, `docs/canonical/late-failure-regression-suite.md:25`, `docs/canonical/late-failure-regression-suite.md:26`, `docs/canonical/late-failure-regression-suite.md:27`, `docs/canonical/late-failure-regression-suite.md:28`, `docs/canonical/late-failure-regression-suite.md:29`, `docs/canonical/late-failure-regression-suite.md:30`, `docs/canonical/late-failure-regression-suite.md:31`).
- Canonical gate: the suite should run before context-strategy changes ship, during harness canaries, and after incident fixes (`docs/canonical/late-failure-regression-suite.md:33`).
- Curriculum implementation: the playbook says every late context incident generates a permanent regression case with fixture, metadata, gate, and ownership (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1118`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1120`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1122`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1123`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1124`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1125`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1126`).
- Rubric implementation: the rubric template requires applying rubrics to old incident outputs and includes N+1 long-session fixtures in the regression set (`curriculum/08-tools-templates/evaluation-rubric-template.md:812`, `curriculum/08-tools-templates/evaluation-rubric-template.md:813`, `curriculum/08-tools-templates/evaluation-rubric-template.md:814`).
- Missing generalization: searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/skills/`, and prior `docs/analysis/` for `Production Failure Regression Flywheel`, `failure intake`, `suite deduplication`, `production failure becomes eval case`, and `escaped edge case`; the generalized all-failure flywheel was not found.

## 8. Canary Eval Rollout Gate

**Classification:** Better Implementation  
**Integration value:** Low

The repo has a detailed, production-like rollout gate that exceeds the extracted pattern: it combines shadow tests, regression batteries, N+1 gates, staged canary percentages, production metrics, trace sampling, rollback commands, and post-rollout observation.

**Evidence:**

- Staged canary policy: the harness playbook defines staging, 5%, 25%, and 100% rollout stages with duration, observed metrics, and advance/rollback decisions (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:783`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:785`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:787`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:788`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:789`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:790`).
- Eval gates before rollout: the same playbook requires regression tests and N+1 long-session fixtures before canary, with any regression aborting rollout (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:748`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:776`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:777`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:778`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:779`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:780`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:781`).
- Production metric gate: canary reports compare baseline and candidate on incomplete-response rate, token budget, latency, evaluator rejection rate, support tickets, and CSAT proxy (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1621`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1623`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1625`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1626`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1627`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1628`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1629`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1654`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1659`).
- Rollback gate: when canary alert fires, the rule is rollback first, then investigation, with flag rollback, alert acknowledgement, and evidence export commands (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:2434`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:2436`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:2438`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:2441`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:2442`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:2443`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:2444`).

## 9. Eval-to-Production Correlation Tracking

**Classification:** Partial Coverage  
**Integration value:** High

The repo tracks baseline/candidate production metrics, teaches continuous calibration with real outcomes, and uses dashboards during rollout. It does not define a named correlation system that audits whether eval scores predict production outcomes over time, with alerts or recalibration triggers when correlation decays.

**Evidence:**

- Existing adjacent mechanic: Evaluation Rubrics describes Continuous Calibration Loop, where rubric scores in production are compared with outcomes such as returns, complaints, and repeat purchase, and weights/thresholds are periodically adjusted (`curriculum/05-core-concepts/08-evaluation-rubrics.md:153`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:155`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:156`, `curriculum/05-core-concepts/08-evaluation-rubrics.md:158`).
- Existing adjacent mechanic: harness dashboards compare baseline vs candidate metrics such as incomplete-response rate, token budget, latency, evaluator rejection rate, and CSAT proxy (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1596`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1600`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1602`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1604`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1605`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1606`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1607`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1654`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1659`).
- Existing adjacent mechanic: feature readiness requires calibrated rubrics, replayable traces, and canary metrics with no trust regression (`curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md:1193`, `curriculum/04-nivel-4-koda-specific/03-feature-design-patterns.md:1194`).
- Missing formalization: searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/skills/`, and prior `docs/analysis/` for `Eval-to-Production Correlation Tracking`, `correlation dashboard`, `score no longer predicts`, `eval scores predict`, and `score drift`; no named correlation-tracking pattern was found outside the source extraction.

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Pain-Signal Eval Progression Gate | Partial Coverage | Medium |
| 2 | Repeatable Agent Spot-Check Set | Partial Coverage | Medium |
| 3 | Metricized Agent Eval Contract | Better Implementation | Low |
| 4 | Production-Grounded Eval Sampling | Partial Coverage | High |
| 5 | Eval Tier Stratification | Partial Coverage | Medium |
| 6 | PR-Gated Eval Enforcement | Partial Coverage | High |
| 7 | Production Failure Regression Flywheel | Partial Coverage | High |
| 8 | Canary Eval Rollout Gate | Better Implementation | Low |
| 9 | Eval-to-Production Correlation Tracking | Partial Coverage | High |
