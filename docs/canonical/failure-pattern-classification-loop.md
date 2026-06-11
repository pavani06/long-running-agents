---
title: "Failure Pattern Classification Loop"
type: canonical
tags: ["agentes-orquestracao", "harness", "governanca", "evals"]
aliases: ["failure classification loop", "slop classification loop", "failure class categorization", "agent misbehavior classification", "recurring failure categorization", "slop pattern classification"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[AGENTS|AGENTS.md]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|Harness Engineering Classification]]"]
sources: ["[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/patterns|Harness Engineering Patterns]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|Harness Engineering Classification]]"]
---

# Failure Pattern Classification Loop

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

When agents produce recurring misbehavior, teams fix individual instances without asking: what class of failure does this represent, and can we eliminate the class rather than the instance? The degradation ladder catches the failure, the flywheel preserves it as a regression case, and the feedback loop converts it to a backlog item. But none of these mechanisms classify the failure into a root cause class that can be systematically eliminated through a harness guardrail.

The source captures this as the distinction between instance-level fixes and class-level elimination: "Figure out why we're spending time on it. Devise a solution to systematically eliminate this class of misbehavior" ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|analysis]]:55-57). The key mechanic is the classification rubric that converts observations into identified failure classes, each with a corresponding guardrail surface.

The repository has the mechanical infrastructure for classifying failures and converting them into durable guardrails: the [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] classifies failures by severity into retryable/unsafe/hold rungs, the [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] converts review findings to issues, the [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] turns production incidents into eval cases, and the [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] includes feedback writeback. But the classification rubric that maps an observed failure to a root cause class and then to a specific guardrail surface is missing from every component ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|classification]]:276-291).

## Solution

Classify every observed agent failure into a root cause class and map each class to the smallest guardrail surface that eliminates the class. The loop converts observation → classification → guardrail → verification, where the classification step is the critical bridge between seeing a problem and solving it systematically.

The classification loop operates in four stages:

```
+------------------+     +------------------+     +------------------+     +------------------+
| 1. OBSERVE       | --> | 2. CLASSIFY      | --> | 3. BUILD         | --> | 4. VERIFY        |
| Capture failure  |     | Root cause class |     | Guardrail at     |     | Does guardrail   |
| with context     |     | + guardrail      |     | minimum viable   |     | eliminate the    |
|                  |     | surface mapping  |     | surface          |     | class?           |
+------------------+     +------------------+     +------------------+     +------------------+
```

**Components:**

1. **Observe.** Every agent failure is captured with sufficient context to enable classification: what the agent did, what the expected behavior was, which surface caught it (review, lint, test, production), and how many instances were observed. The observation format is lightweight — a sentence or two with a link to the PR, issue, or incident — not a multi-page incident report. The degradation ladder provides the severity classification; this loop adds the root cause dimension.

2. **Classify.** Each observation is classified along two axes: root cause class and guardrail surface. The root cause class identifies why the failure occurred — is it a model weakness (the agent does not know to do X), a missing harness constraint (no rule says to do X), a local coherence violation (the agent optimized for the local file at the expense of the global architecture), or a prompt ambiguity (the instruction was unclear)? The guardrail surface identifies where the fix should live — lint rule, reviewer prompt, skill update, NFR document, test, eval case, or structural micro-harness.

3. **Build.** A guardrail is constructed at the mapped surface. The guardrail is the minimum viable change that eliminates the class of failure — not the most comprehensive possible fix, but the smallest one that prevents recurrence. A lint rule that catches the pattern before commit. A reviewer prompt amendment that flags the issue during review. An eval case that asserts the correct behavior in CI.

4. **Verify.** After deployment, the guardrail is verified against new agent output. Does the guardrail catch the failure class in subsequent PRs? Does it produce false positives that need tuning? Is the guardrail itself worth the token cost, latency, and maintenance overhead? If verification shows the guardrail is effective, it enters the measured harness evolution lifecycle. If it is ineffective, it is tuned or removed.

**Root cause classification taxonomy:**

| Root cause class | Description | Example | Typical guardrail surface |
|---|---|---|---|
| **Model ignorance** | Agent does not know the correct pattern; the constraint is not documented | Agent uses `any` because no type constraint is visible | NFR document + lint rule |
| **Missing harness** | The constraint exists as human knowledge but has no mechanical enforcement | Team convention is "no raw console.log" but no lint rule exists | Lint rule or structural check |
| **Local coherence** | Agent optimizes for the local file or package, ignoring global architecture | Agent duplicates a utility that exists in another package | Micro-harness: dependency direction or canonical helper check |
| **Prompt ambiguity** | The instruction exists but is too vague for the agent to follow consistently | "Handle errors properly" without specifying retry policy or degradation behavior | NFR document update with concrete rules + reviewer rubric |
| **Context loss** | Agent had the constraint earlier but lost it through compaction or session boundary | Agent forgets a constraint from earlier in a long session | Durable state persistence + just-in-time context surfacing |
| **Model regression** | A model upgrade changed behavior on a previously reliable pattern | Model previously handled async patterns correctly, now produces callback-based code | Eval case regression + invariant check |

**Guardrail surface mapping:**

| Guardrail surface | Best for | Cost | Latency |
|---|---|---|---|
| Lint rule | Syntax-level violations, canonical helper enforcement, import restrictions | Low token cost, runs at commit time | Instant (pre-commit) |
| Reviewer prompt | Architectural judgment, nuanced patterns that require code-level understanding | Medium token cost, runs at PR time | Minutes (CI) |
| NFR document update | Standards that inform multiple surfaces (lint, review, skills) | Writing cost only, no runtime cost | N/A (documentation) |
| Skill update | Complex workflows where the agent needs procedural guidance | Maintenance cost, loaded on demand | Variable (loaded per task) |
| Eval case | Behavioral correctness, regression prevention | Token cost per eval run | Minutes to hours (CI) |
| Structural micro-harness | Package privacy, dependency direction, schema ownership | Development cost, runs at test time | Seconds to minutes |
| Test | Specific behavioral invariants that should never regress | Development cost, runs in CI | Seconds to minutes |

## Implementation in this repo

### What already exists

- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] lines 29-65 classifies failures into retryable, unsafe, and hold rungs with retry, safe fallback, human escalation, outcome logging, and rung tests. This is severity classification; the missing piece is root cause classification and guardrail surface mapping.
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] lines 30-44 formalizes QA/review findings as backlog inputs with capture, triage, conversion, and return-to-board stages. This captures findings but classifies by severity and blocker status, not by root cause class.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] lines 28-40 transforms production failures into durable regression cases with trace, labels, tier assignment, and deduplication. This preserves failures as eval cases but does not classify root cause classes.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] lines 32-45 includes feedback writeback as an operating system surface with ownership, validation, and memory update.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] lines 40-51 maps observed pain signals to next eval capabilities. This is the closest existing mechanic to "observe failure → build capability" but is scoped to eval capability, not root cause classification.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] lines 31-60 classifies harness controls as domain invariants vs. model-specific compensations. This classification happens at the harness component level, not at the individual failure level.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] lines 29-62 provides the lifecycle for guardrails once built: BUILD/STABILIZE/SIMPLIFY/REMOVE with ROI measurement and archive contract.

### What is missing from the pattern

The classification marks Failure Pattern Classification Loop as Partial Coverage because the repo has all the mechanical infrastructure for converting failures into guardrails but lacks the explicit classification rubric that connects a root cause class to a guardrail surface ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|classification]]:276-291).

Missing pieces:

1. No root cause taxonomy maps observed failures to root cause classes (model ignorance, missing harness, local coherence, prompt ambiguity, context loss, model regression). The degradation ladder classifies by severity; no mechanism classifies by root cause.
2. No guardrail surface mapping connects root cause classes to the appropriate guardrail surface (lint rule, reviewer prompt, NFR doc, skill, eval case, micro-harness). The existing components each handle one surface but there is no systematic mapping from failure class to surface.
3. No minimum viable guardrail principle guides construction: the existing patterns produce comprehensive fixes (full flywheels, full lifecycle governance) but the classification loop requires the smallest fix that eliminates the class.
4. The weekly GC Day ritual ([[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]) provides the cadence for running the classification loop, but the GC Day pattern is itself missing from the repo. The classification loop is the mechanic that GC Day executes; both are needed together.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Attacks classes of failure instead of instances — each guardrail prevents every future occurrence of the class | Poor classification can create narrow rules that catch one symptom but miss the underlying class |
| Makes guardrail construction systematic: root cause class → surface → minimum viable guardrail | Adds classification overhead before guardrail construction |
| Connects all existing mechanical infrastructure into a coherent pipeline: observe → classify → build → verify | Requires discipline to classify before building, resisting the instinct to jump to a fix |
| Feeds the harness evolution lifecycle with classified, justified guardrails rather than ad hoc additions | Misclassification can route a failure to the wrong surface, creating ineffective or costly guardrails |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] because the weekly GC Day cadence is the ritual where the classification loop runs. Without GC Day, the classification loop has no scheduled execution.
- **Consumes:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] because the degradation ladder provides the severity classification (retryable/unsafe/hold) that adds the severity dimension to the root cause classification.
- **Feeds from:** [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] and [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] because both produce observations that feed the classification loop.
- **Uses:** [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] because once a guardrail is built, it must be classified as domain invariant or model-specific compensation before entering the harness evolution lifecycle.
- **Feeds into:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] because classified and justified guardrails enter the BUILD state with known root cause and expected impact.
- **Validated by:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] because recurring failures that survive the classification loop are pain signals that justify investing in new eval capabilities.
- **Integrated with:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] because the classification loop is the feedback-writeback mechanism that closes the operating system loop.
- **Comes from:** [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|Harness Engineering Analysis]]:47-57, 193 and its Partial Coverage classification in [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|classification]]:276-291.

## References

- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|analysis]]:47-57 — Garbage Collection Day meta-loop: categorize slop patterns, build systematic solutions to eliminate classes of misbehavior.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|analysis]]:193 — slop accumulating weekly as a failure pattern; GC Day as the mitigation.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|analysis]]:201-210 — synthesis: the harness is a system that learns; GC Day is the meta-loop.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/patterns|patterns]]:137-159 — Weekly Harness Garbage Collection Loop pattern: categorized failure classes, new or updated guardrails, reduced need for synchronous correction.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|classification]]:276-291 — Partial Coverage classification with NOT_FOUND evidence for weekly cadence, categorization rubric, and documented slop-to-guardrail pipeline.
- [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29-65 — failure classification into retryable/unsafe/hold rungs.
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]:30-44 — capture, triage, convert, return-to-board pipeline.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40 — production failure to durable regression case conversion.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:40-51 — pain signal to eval capability mapping.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:31-60 — domain invariant vs. model compensation classification.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:32-45 — feedback writeback surface.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:29-62 — BUILD/STABILIZE/SIMPLIFY/REMOVE lifecycle.

---

*Created: 2026-06-11 | From: Harness Engineering pattern classification | Precedence: canonical*
