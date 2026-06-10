# Pain-Signal Eval Progression Gate

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-eval-maturity-phases/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Agent teams often make eval investments at the wrong time. They may ship by feel after users are already reporting failures, or they may build expensive eval infrastructure before there is enough traffic, feedback, or team capacity to use it well.

The pattern solves the decision problem: when should the repository stay with its current eval capability, and when should it add the next minimum eval capability?

## Solution

Treat eval maturity as a gate driven by pain signals instead of a calendar roadmap. The gate asks whether current evidence shows that the next eval capability is now necessary.

Operational steps:

1. Inventory the current eval capability: manual checks, seed spot-checks, production-sampled replays, tiered suites, PR gates, canaries, and failure regressions.
2. Capture pain signals from users, developers, reviewers, and production operations.
3. Classify each signal into one or more trigger classes.
4. Map each trigger class to the next minimum eval investment.
5. Approve only the smallest eval capability that addresses the observed pain.
6. Record deferred eval investments with the reason they are not yet justified.
7. Re-run the gate after incidents, repeated manual bottlenecks, scoring drift, or release-risk changes.

Recommended trigger mapping:

| Pain signal | Minimum next capability |
|---|---|
| User complaints repeat for known workflows | Add or expand Repeatable Agent Spot-Check Set |
| Manual reviews block prompt, model, or tool changes | Add Eval Tier Stratification and PR-Gated Eval Enforcement |
| Hand-authored cases miss real behavior | Add Production-Grounded Eval Sampling |
| Scorecards disagree with reviewer or user feedback | Calibrate existing metricized rubrics, thresholds, and correlation checks |
| Escaped edge cases recur after fixes | Add Production Failure Regression Flywheel |
| Late-session or context failures recur | Add or expand Late-Failure Regression Suite |

The gate should produce a decision record with the observed pain, source evidence, current capability, chosen next step, owner, expected operating cost, and a review date.

## Implementation in this repo

### What already exists

The repo already has adjacent decision habits for harness evolution and rollback:

- The KODA harness-evolution framework asks which concrete failure a component prevents, how often it prevents that failure, what token, latency, and maintenance cost it adds, whether replay or A/B proves removal safe, and how quickly rollback can happen (`curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1490`).
- Harness-improvement proposals require evidence, rollback or config disablement, a technical owner, a review cadence, and metrics such as critical-fact loss or harness value (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:498`).
- The classification identifies this as an adjacent mechanic, not a formal eval-maturity gate (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:15`).

### What needs to be added

The missing implementation is a named eval progression gate that explicitly connects pain signals to the next minimum eval capability.

Add:

1. A canonical checklist for eval-maturity reviews.
2. A standard trigger taxonomy covering user complaints, manual eval bottlenecks, score-feedback mismatch, and escaped edge cases.
3. A decision template that records the current capability, selected next capability, deferred capabilities, and review cadence.
4. Integration with PR review and incident review so eval maturity changes are triggered by evidence, not by preference.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents premature eval-platform work | Requires honest collection of pain signals |
| Keeps eval investment tied to real reliability bottlenecks | Can underinvest when feedback collection is weak |
| Gives reviewers a common language for eval maturity decisions | Adds governance overhead to incidents and PRs |
| Makes deferred eval work explicit instead of forgotten | Requires periodic revisit or stale decisions persist |

## Relationship to Other Patterns

- **Triggers:** Repeatable Agent Spot-Check Set when known critical paths need a first repeatable safety net.
- **Triggers:** Production-Grounded Eval Sampling when hand-authored cases stop representing real traffic.
- **Triggers:** Eval Tier Stratification when one suite cannot satisfy local, PR, and release needs.
- **Triggers:** PR-Gated Eval Enforcement when eval results must become merge evidence.
- **Triggers:** Production Failure Regression Flywheel when escaped failures need durable regression cases.
- **Complements:** Existing harness evolution, rollback, and ownership practices in the curriculum.

## References

- `docs/analysis/2026-06-10-eval-maturity-phases/patterns.md:16` - extracted pattern definition.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:10` - Partial Coverage classification.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:19` - KODA harness-evolution evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/classification.md:20` - harness-improvement proposal evidence.
- `docs/analysis/2026-06-10-eval-maturity-phases/mental-model.md:16` - documentation precedence context.
- `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1490` - harness-evolution failure and cost questions.
- `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:498` - evidence, rollback, ownership, and metric requirements.

## Better Implementation Cross-References

Do not create separate canonical docs for Metricized Agent Eval Contract or Canary Eval Rollout Gate from this analysis. The classification says the repo already has better implementations: Sprint Contracts, KODA rubrics, and baseline/candidate score comparison exceed the metricized contract pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:37`), while staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern (`docs/analysis/2026-06-10-eval-maturity-phases/classification.md:108`).

---

*Created: 2026-06-10 | From: Eval Maturity pattern classification | Precedence: canonical*
