---
title: "Contextual Severity Calibration"
type: canonical
aliases: ["severity calibration", "risk-based review", "module risk profile", "contextual severity", "risk-adjusted review", "risk-profile"]
tags: ["evals", "agentic-coding", "governanca", "harness-engineering"]
last_updated: 2026-06-15
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]]", "[[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]", "[[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]"]
sources: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]"]
---

# Contextual Severity Calibration

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]
**Classification:** Missing ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:130-163)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Applying uniform review depth and severity to all modules treats a help page change with the same scrutiny as a payment module change. This creates two simultaneous failures: low-risk modules receive excessive review, generating fatigue and false positives; high-risk modules receive insufficient review, leaving catastrophic failure paths unexamined. The repo's eval tier stratification selects tiers by change type (prompt, model, tool, loop), not by module risk level — a change to the payment integration and a change to the help page both trigger the same fast/medium/deep eval selection ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:143).

The source document captures this as the one-size-fits-all review depth failure pattern: uniform review generates fatigue on low-risk code and risk on critical code, and teams lose confidence in the process because effort is not proportional to impact ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:314-325). The repo has adjacent concepts — blast radius is mentioned in human-AFK task routing and architecture-as-agent-affordance — but no mechanism maps module-level risk to review depth ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:138-144).

The classification confirms this pattern has high integration value: it would add precision to eval tier stratification and PR-gated eval enforcement, making agentic review effort proportional to operational risk rather than uniform ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:161-163).

## Solution

Declare module-level risk profiles via a `risk-profile.yaml` file in each module directory. The AI reviewer reads this profile before analyzing the diff and adjusts review depth and severity labels proportionally to the declared risk level. Risk levels map to applicable check sets.

**Risk profile contract:**

```yaml
risk_level: critical | high | medium | low
checks:
  - style
  - correctness
  - security
  - performance
  - data_integrity
```

This format is defined in the extracted pattern specification ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:150-162) and is confirmed NOT_FOUND as a file or template anywhere in the repo — the only occurrences are within the canary-test analysis itself ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:148).

**Risk level to check set mapping:**

| Risk level | Checks applied | Example modules |
|---|---|---|
| Low | Style checks only | Help pages, documentation, static content |
| Medium | Style + basic correctness | Utility functions, internal tools, shared components without side effects |
| High | Style + correctness + security | API handlers, authentication, authorization, data access layers |
| Critical | Full security, performance, and data integrity checks | Payment processing, PII handling, database migrations, session management |

This mapping is defined in the analysis source ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:55-60).

**Calibration mechanics:**

1. **On change detection:** The AI reviewer identifies which modules were changed via `git diff` paths.
2. **Profile lookup:** For each changed module, the reviewer reads the nearest `risk-profile.yaml` (walking up the directory tree if no local profile exists, with a repository-level default of `medium`).
3. **Check selection:** The reviewer activates only the checks declared in the profile for the module's risk level.
4. **Severity labeling:** Findings are tagged with calibrated severity — the same finding type (e.g., missing error handling) carries higher severity when found in a `critical` module than in a `low` module.
5. **Feedback integration:** Per-module false-positive rates from the shadow review pipeline inform periodic recalibration of risk levels and check selections ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:390-393).

**Calibration feedback loop:**

```
+-------------------------+     +-------------------------+     +-------------------------+
| Shadow Review Pipeline  | --> | Module false-positive   | --> | risk-profile.yaml       |
| per-module agreement    |     | rates, missed issues    |     | risk level adjusted     |
| metrics                 |     | by risk level           |     | checks adjusted         |
+-------------------------+     +-------------------------+     +-------------------------+
```

## Implementation in this repo

### What already exists (adjacent, not equivalent)

The repo has concepts of blast radius and risk awareness in isolated contexts, but none applies to automated review severity calibration:

- [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]]:35 mentions system-wide blast radius as a criterion for routing tasks to human vs. agent — about task assignment, not review severity.
- [[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]]:38 discusses reduced coupling to minimize blast radius — about module design principles, not review calibration.
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29-60 classifies failures by severity into retryable/unsafe/hold rungs — severity classification by failure type, not by module risk profile.
- [[docs/system-of-record|System of Record]]:213 documents `crossroad-change-policy.md` as pending for high blast-radius file changes — governance policy, not automated severity calibration, and not yet created.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-49 selects eval tiers by change type (prompt, model, tool, loop), not by module risk level.

These provide partial awareness of risk as a concept but no mechanism for module-level risk profiles, risk-adjusted check selection, or calibrated severity labels ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:138-144).

### What is missing

1. `risk-profile.yaml` format: module-level risk metadata declaring risk level (`critical`, `high`, `medium`, `low`) and applicable check sets. NOT_FOUND as a file or template anywhere in the repo outside the canary-test analysis ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:148).
2. Risk-adjusted review depth: mechanism to select checks proportional to the blast radius and failure cost of the changed module. NOT_FOUND ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:149).
3. Calibrated severity labels: severity levels that adjust based on which module changed, rather than applying uniform severity to all findings. NOT_FOUND ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:150).
4. Module risk profile maintenance and ownership: no canonical doc or curriculum lesson covers maintaining module risk metadata or periodic re-evaluation of risk classifications ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:151).
5. Feedback loop from false-positive rates per module into severity calibration: the analysis proposes this as a dependency on the shadow review pipeline, but no such loop exists ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:152).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Reduces reviewer fatigue on low-risk changes — fewer false positives on trivial code | Requires maintained risk profiles and ownership of module metadata |
| Increases scrutiny where failures have high security, data, performance, or integrity cost | Misclassified modules can create either false confidence or unnecessary friction |
| Makes agentic review effort proportional to operational risk instead of uniform | Calibration needs periodic re-evaluation as product, architecture, and empirical review data change |
| Severity labels carry contextual weight — developers can trust that `critical` findings on `critical` modules matter | Risk profile maintenance overhead grows with module count; default-fallback policy is needed |
| Feeds and is fed by shadow review pipeline data — a self-improving calibration loop | The feedback loop adds latency between problem detection and risk profile correction |

## Relationship to Other Patterns

- **Fed by:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] because per-module false-positive rates and missed-issue data collected during the shadow period inform which severity levels are trustworthy for each module type. The analysis identifies this as the primary data input to the calibration feedback loop ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:390-393).
- **Feeds into:** [[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]] because the pre-commit gate uses calibrated severity to adjust prompt depth and check selection at pre-commit time.
- **Integrates with:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] by adding a module-risk dimension to the existing change-type dimension for tier selection.
- **Integrates with:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] by providing risk-weighted thresholds that affect merge policy decisions.
- **Complements:** [[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]] because modular design with reduced blast radius creates a natural boundary for risk profile assignment.
- **Context from:** [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]] because blast radius as a routing criterion is conceptually adjacent to blast radius as a review depth criterion.
- **Adjacent to:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] because both classify severity, but the degradation ladder classifies by failure type (retryable/unsafe/hold) while contextual severity calibrates by module risk profile.

## References

- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:45-60 — risk stratification model with risk-level table and check set mapping.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:147-169 — contextual severity calibration mechanics: risk-profile.yaml structure, check selection, severity adjustment.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:259-268 — tradeoff: revisao uniforme vs. calibrada por risco.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:314-325 — failure pattern: one-size-fits-all review depth.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:380-401 — synthesis: dependency chain shadow pipeline → severity calibration → continuous improvement.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|patterns]]:83-103 — extracted pattern definition with inputs, outputs, benefits, limitations.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:130-163 — Missing classification with NOT_FOUND evidence and high integration value.
- [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]]:35 — adjacent blast radius concept in task routing.
- [[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]]:38 — adjacent blast radius concept in module design.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-49 — existing tier selection by change type, not module risk.
- [[docs/system-of-record|System of Record]]:213 — pending `crossroad-change-policy.md` for high blast-radius file changes.

---

*Created: 2026-06-15 | From: Canary Test Code Review pattern classification | Precedence: canonical*
