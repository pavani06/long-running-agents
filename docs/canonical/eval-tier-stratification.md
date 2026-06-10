---
title: "Eval Tier Stratification"
type: canonical
aliases: ["eval tiers", "stratification"]
tags: ["evals"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"]
sources: ["[[docs/analysis/2026-06-10-eval-maturity-phases/analysis|Eval Maturity Analysis]]"]
---
# Eval Tier Stratification

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-eval-maturity-phases/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

A single eval suite cannot provide fast developer feedback, PR protection, release confidence, and deep regression coverage at the same time. If every eval runs on every edit, the inner loop becomes too slow. If only fast checks exist, expensive long-running failures escape.

The repo needs an explicit taxonomy that tells contributors which evals run when, how costly they are, how flaky they are allowed to be, and what decision each tier can block.

## Solution

Organize evals into fast, medium, and deep tiers. Each tier must declare runtime, cost, flakiness tolerance, trigger, threshold, reporting format, owner, and escalation policy.

Recommended taxonomy:

| Tier | Purpose | Typical trigger | Expected runtime | Decision power |
|---|---|---|---|---|
| Fast | Inner-loop confidence for known critical paths | Local change, pre-commit, small PR | Seconds to a few minutes | Blocks local readiness or PR if critical paths regress |
| Medium | PR-level evidence for prompt, model, tool, or loop changes | PR, draft review, merge readiness | Minutes to tens of minutes | Blocks merge unless waived with explicit rationale |
| Deep | Release, canary, scheduled, and incident regression confidence | Release candidate, nightly, incident fix, canary | Tens of minutes to hours | Blocks rollout or requires hold/rollback decision |

Each eval case or suite should carry metadata:

| Metadata | Meaning |
|---|---|
| `tier` | `fast`, `medium`, or `deep` |
| `runtime_budget` | Maximum acceptable wall-clock time |
| `cost_budget` | Token, model, infrastructure, or reviewer cost |
| `flakiness_policy` | Retry, quarantine, owner, and confidence rules |
| `trigger` | Local, PR, scheduled, release, canary, or incident |
| `threshold` | Pass/fail score, maximum regression delta, or escalation boundary |
| `reporting` | Summary, baseline delta, trace links, rubric output, or dashboard |
| `owner` | Maintainer responsible for health and updates |

## Implementation in this repo

### What already exists

The repo already has multiple validation layers:

- The issue-review skill defines core gates and optional surface-specific gates including lint, unit, integration, dashboard, fixture parity, evidence verification, CI gates, and branch-protection verification (`.opencode/skills/issue-review/SKILL.md:44`).
- The harness playbook separates lint/unit checks, component regression batteries, N+1 long-session gates, staging shadow tests, and canary phases (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`).
- `package.json` defines real local validation commands such as `npm run lint`, `npm run test:unit`, and `npm run test:integration` (`package.json:8`).
- The classification says the layers exist, but there is no explicit fast/medium/deep eval tier taxonomy (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:71`).

### What needs to be added

The missing implementation is metadata and policy that make the tiers explicit.

Add:

1. A tier registry that maps eval suites to `fast`, `medium`, or `deep`.
2. Runtime, cost, flakiness, trigger, threshold, reporting, and owner metadata per suite.
3. A rule for which tiers must run for prompt, model, tool, context, and agent-loop changes.
4. A reporting convention that makes skipped deep tiers visible instead of silent.
5. A quarantine process for flaky evals that preserves the gate's integrity.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps developer feedback fast while preserving deeper coverage | Adds operational complexity around ownership and scheduling |
| Makes expensive agent evals usable without blocking every edit | Deep failures may arrive after the developer has moved on |
| Lets reviewers match evidence depth to change risk | Poor tier boundaries can leave risky behavior uncovered |
| Gives flakiness and cost explicit governance | Requires periodic cleanup as suites evolve |

## Relationship to Other Patterns

- **Triggered by:** Pain-Signal Eval Progression Gate when manual bottlenecks or PR latency show one undifferentiated suite is not enough.
- **Uses:** Repeatable Agent Spot-Check Set as an initial fast tier.
- **Uses:** Production-Grounded Eval Sampling as medium or deep replay tiers depending on cost.
- **Enables:** PR-Gated Eval Enforcement by defining which tier evidence belongs on a PR.
- **Enables:** Production Failure Regression Flywheel by assigning each new regression case to the right tier.
- **Complements:** Existing issue-review gates, harness regression batteries, N+1 gates, shadow tests, and canary stages.

## References

- `docs/analysis/2026-06-10-eval-maturity-phases/patterns.md:100` - extracted pattern definition.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:66` - Partial Coverage classification.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:75` - issue-review validation layer evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:76` - harness playbook layered eval evidence.
- `.opencode/skills/issue-review/SKILL.md:44` - current review gate validation step.
- `.opencode/skills/issue-review/SKILL.md:57` - optional surface-specific gates.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741` - regression battery.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:783` - rollout staging and canary phases.

## Better Implementation Cross-References

Do not create separate canonical docs for Metricized Agent Eval Contract or Canary Eval Rollout Gate from this analysis. The classification says the repo already has better implementations: Sprint Contracts, KODA rubrics, and baseline/candidate score comparison exceed the metricized contract pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:37`), while staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:108`).

---

*Created: 2026-06-10 | From: Eval Maturity pattern classification | Precedence: canonical*
