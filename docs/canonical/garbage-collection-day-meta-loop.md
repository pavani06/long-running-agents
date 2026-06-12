---
title: "Garbage Collection Day Meta-Loop"
type: canonical
tags: ["agentes-orquestracao", "harness", "governanca"]
aliases: ["GC day", "garbage collection day", "weekly harness cleanup", "weekly slop review", "harness garbage collection", "weekly guardrail cadence", "Friday harness ritual"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]", "[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|Harness Engineering Classification]]"]
sources: ["[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|Harness Engineering Classification]]"]
---

# Garbage Collection Day Meta-Loop

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Teams review agent-generated code, catch recurring slop patterns, and write the same feedback week after week. The feedback addresses individual patches but never becomes automated harness behavior. Reviewers spend synchronous human time on problems that should have been eliminated systematically after their first observation.

The source describes this as the core failure mode that Garbage Collection Day addresses: "teams keep paying for the same agent slop when recurring review feedback never becomes automated harness behavior" ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|patterns]]:140-141). Without a dedicated cadence for converting observations into guardrails, the review bottleneck compounds as agent throughput grows — more PRs per day means more instances of the same failure patterns, and the human reviewers become the permanent cost of every class of misbehavior.

The repository has strong component mechanisms that align with parts of the pattern: the [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] converts review findings into backlog items, the [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] governs harness component lifecycle, the [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] maps observed pain to eval investments, and the [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] converts production incidents into regression cases. But the specific weekly cadence where human review feedback gets systematically converted into automated harness guardrails (lint rules, skills, reviewer prompts, tests) is not formalized as a recurring meta-loop ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:58-81).

## Solution

Establish a weekly ritual where the team reviews observations from the past work cycle, categorizes recurring agent misbehavior into failure classes, and systematically builds automated guardrails that eliminate each class — not each instance.

The meta-loop operates on a weekly cadence:

```
+------------------+      +------------------+      +------------------+
| Week of agent    | ---> | Friday GC Day    | ---> | Next week:       |
| work produces    |      | review +         |      | agents protected |
| review feedback  |      | categorize +     |      | by new guardrails|
| + failure traces |      | build guardrails |      |                  |
+------------------+      +------------------+      +------------------+
```

**Components:**

1. **Observation collection.** Throughout the work week, human reviewers collect observations of recurring agent misbehavior: repeated lint violations, duplicated utilities, inconsistent error handling, architectural boundary violations, avoidable PR feedback loops. These are captured in a lightweight format — a running list, a shared document, or a backlog lane — not elaborate incident reports. The goal is to surface patterns, not to document every instance.

2. **Weekly GC Day session.** Every Friday (or the team's chosen cadence day), the team holds a dedicated session to review collected observations. This is not a status meeting or a planning session; it is a working session where observations become automated guardrails. The session produces concrete outputs: updated lint rules, new or amended skills, revised reviewer prompts, expanded eval cases, or updated NFR documents.

3. **Failure class categorization.** Each observed pattern is categorized using a rubric that asks: what class of misbehavior does this represent? Can a guardrail eliminate the class rather than patching the instance? Which surface should the guardrail live in (lint rule, skill, reviewer prompt, NFR document, test, eval case)?

4. **Guardrail construction.** The team builds, tests, and deploys guardrails during the session. A lint rule that catches duplicated async helpers. A reviewer prompt amendment that flags missing error boundaries. An eval case that asserts architectural dependency direction. The guardrails are deployed immediately so the following week's agents benefit from the previous week's observations.

5. **Cadence protection.** The weekly cadence is non-negotiable. Feature pressure, release deadlines, and incident response do not cancel GC Day — they make it more important because agent throughput continues regardless of whether guardrails improve. The session is time-boxed (e.g., 2 hours), ensuring it remains a recurring investment rather than an open-ended cleanup project.

**Categorization rubric:**

| Observed pattern | Root cause class | Guardrail surface |
|---|---|---|
| Agent duplicates a utility function that already exists in a shared module | Local coherence optimization; agent does not search for existing implementations | Lint rule: `no-internal-duplication` or structural check for canonical helpers |
| Agent uses bare `console.log` instead of safe-console helpers | Missing enforcement of code standards at generation time | Lint rule: `no-raw-console-in-scripts` (already exists in repo) |
| Agent ignores error boundaries in React components | NFR not surfaced at implementation time | Reviewer prompt: flag missing error boundaries; add to front-end persona NFR doc |
| Agent produces inconsistent async patterns (callbacks vs. async/await) | No canonical async pattern documented | NFR document: define the one canonical async pattern; lint rule enforces it |
| Agent repeats the same architectural dependency violation across PRs | Structural drift; no micro-harness checking dependency direction | Structural test: assert package dependency edges |

## Implementation in this repo

### What already exists

- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] lines 30-44 converts QA/review findings into backlog issues through capture, triage, convert, and return-to-board stages. This is the closest existing mechanism: findings become backlog work. But the output is issues, not automated harness guardrails. The canonical itself notes this gap: findings become backlog items, not automated harness behavior (`docs/canonical/qa-to-backlog-feedback-loop.md:57-59`).
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] lines 29-62 defines BUILD, STABILIZE, SIMPLIFY, REMOVE lifecycle with quarterly cadence, ROI threshold, and One In One Out rule. This is harness evolution, but the cadence is quarterly (not weekly) and the trigger is usage metrics, not review feedback.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] lines 40-51 maps pain signals (user complaints, manual review bottlenecks, escaped edge cases) to minimum eval investments. This converts observations into harness improvements, but is scoped to eval capability, not general harness guardrails.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] lines 28-40 converts production failures into durable regression cases with trace, labels, tier assignment, and deduplication.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] lines 31-60 classifies harness controls as domain invariants vs. model-specific compensations, providing the decision framework for what guardrails to build vs. remove.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] lines 32-45 includes feedback writeback as an operating system surface.
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] lines 29-65 classifies failures into retryable, unsafe, and hold rungs with retry, fallback, escalation, and logging per rung.

### What is missing from the pattern

The classification marks Garbage Collection Day Meta-Loop as Partial Coverage because the repo has all the component mechanisms but lacks the connecting meta-loop that turns recurring review observations into automated guardrails on a weekly cadence ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:60-81).

Missing pieces:

1. No explicit weekly cadence for converting review feedback into automated guardrails. The `measured-harness-evolution-lifecycle.md` has a quarterly cadence; the `qa-to-backlog-feedback-loop.md` converts findings to issues, not guardrails. No skill, curriculum module, or agent definition schedules a weekly harness improvement ritual.
2. No categorization rubric for slop patterns observed during review. The pattern's specific mechanic — classifying each observation by root cause class and guardrail surface — has no documented rubric in `docs/canonical/`, `curriculum/`, or `.opencode/skills/`.
3. No documented pipeline from "human reviewer noticed recurring pattern X" to "new lint rule, skill update, or reviewer-prompt amendment was deployed." The `qa-to-backlog-feedback-loop.md` produces backlog issues; the gap is the step from backlog issue to deployed guardrail.
4. The `remove-ai-slops` built-in skill is the closest operational tool but is a reactive, one-shot tool, not a recurring meta-loop.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Converts human observations into accumulating harness leverage — each week, the harness improves and review cost decreases | Requires recurring time allocation even under feature pressure |
| Attacks classes of behavior instead of patching one instance at a time | Poor categorization can create narrow rules that miss the real failure class |
| Creates a predictable rhythm for harness learning and cleanup | New guardrails can add false positives, latency, or token cost if not measured |
| Reduces synchronous human review time as automated guardrails take over | Weekly cadence may be too fast for some teams or too slow for high-throughput teams |

## Relationship to Other Patterns

- **Feeds from:** [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] because the feedback loop captures review findings that GC Day categorizes and converts into guardrails.
- **Uses:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] because the classification rubric (root cause class, guardrail surface) is the mechanic that converts observations into systematic improvements during GC Day.
- **Governed by:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] because new guardrails enter the BUILD state and follow the full lifecycle through STABILIZE, SIMPLIFY, and REMOVE.
- **Validated by:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] because GC Day observations are pain signals that justify investment in new eval capabilities.
- **Uses:** [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] because each candidate guardrail must be classified as a domain invariant or model-specific compensation before construction.
- **Feeds from:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] and [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] because production failures and degradation rung data provide additional observation sources for GC Day.
- **Integrated with:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] because GC Day is the feedback-writeback surface that closes the loop between observation and automation.
- **Extends:** [[docs/canonical/persona-based-documentation|Persona-Based Documentation]] because persona-specific observations during GC Day update persona-specific NFR documents and reviewer rubrics.
- **Comes from:** [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]:137-159 and its Partial Coverage classification in [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:58-81.

## References

- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:47-57 — Garbage Collection Day as Friday meta-loop: human review feedback → documentation → automated prompt injection → self-healing agents.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:193 — slop accumulating weekly as a failure pattern when no GC Day cadence exists.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|patterns]]:137-159 — Weekly Harness Garbage Collection Loop pattern definition with inputs, outputs, benefits, and limitations.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:58-81 — Partial Coverage classification with evidence of existing component mechanisms and gap analysis.
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]:30-44 — capture, triage, convert, return-to-board pipeline for review findings.
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]:57-59 — explicit note that findings become backlog items, not automated harness behavior.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:29-62 — BUILD/STABILIZE/SIMPLIFY/REMOVE lifecycle with quarterly cadence and ROI measurement.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:40-51 — pain signal to eval capability mapping.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40 — production failure to regression case conversion.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:31-60 — classification of harness controls before simplification or removal.

---

*Created: 2026-06-11 | From: Harness Engineering pattern classification | Precedence: canonical*
