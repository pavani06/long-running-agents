---
title: "Two-Implementations Goal Test"
type: canonical
tags: ["agentes-orquestracao", "spec-driven-development", "decision-discipline", "governanca"]
aliases: ["two-implementations test", "goal vs spec", "goal purity test", "two-impl heuristic", "goal classification test", "implementation freedom test"]
last_updated: 2026-06-14
relates-to: ["[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/goal-atomicity-split|Goal Atomicity Split]]", "[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
---

# Two-Implementations Goal Test

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/
**Classification:** Missing, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Humans often write implementation methods and call them goals, turning the agent into a typist instead of a decision-maker. A statement like "add a Redis cache layer with TTL of 300 seconds" looks like a goal but is an implementation specification. It tells the agent exactly how to achieve something, leaving no room for the agent's judgment about what architecture, tool, or approach best satisfies the outcome. The agent becomes a code generator executing a recipe rather than a decision-maker pursuing an outcome.

The source names this as the spec-disguised-as-goal problem: "Humans often write implementation methods and call them goals, turning the agent into a typist instead of a decision-maker" ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|patterns]]:62-63).

The repo has extensive material on intent composition and vertical-slice-issue-generation that produces observable behavior, but no lightweight pre-flight test that asks whether two different implementations could satisfy the same statement. The concept appears only in the source analysis, not in any repo artifact ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:94-101).

## Solution

Apply a single review question before the agent receives a goal: "Can two substantially different implementations both satisfy this statement?" Two implementations are substantially different if they make different architectural choices, use different tools, or organize work differently while still satisfying the stated outcome.

**The test:**

| If the answer is... | Then the statement is... | Action |
|---|---|---|
| Yes -- at least two different approaches could both satisfy it | A goal | Proceed. The statement describes an outcome, not a method. |
| No -- only one approach satisfies it, or the statement itself mandates a specific approach | A specification disguised as a goal | Reject from the goal slot. Extract the implementation details and route them to Context. Identify the underlying outcome and rewrite the goal in outcome language. |

**Examples:**

| Statement | Two implementations? | Classification | Rewrite |
|---|---|---|---|
| "Add a Redis cache layer with TTL of 300 seconds" | Only one approach -- mandates Redis, cache, TTL. No alternative satisfies the literal words. | Spec disguised as goal | Goal: "Reduce median query latency below 50ms for repeated reads." Context: "We use Redis for caching. Current TTL is unset." |
| "The checkout page must load in under 2 seconds" | Yes -- CDN, edge rendering, query optimization, precomputation, or architecture change could all satisfy it. | Goal | Keep as-is. This is an outcome, not a method. |
| "Migrate the payments module from Stripe v2 to Stripe v3" | Only one approach -- mandates Stripe v3 migration. | Spec disguised as goal | Goal: "Payment processing remains operational and passes the payment-gateway compliance audit by Q3." Context: "Stripe v2 is being deprecated. Stripe v3 is the migration target." |
| "Users can recover their account without contacting support" | Yes -- email reset, SMS code, OAuth recovery, security questions, or a combination could all satisfy it. | Goal | Keep as-is. The how is open; the what is clear. |

**What "substantially different" means:**

Two implementations are substantially different when a competent engineer reviewing both would say they made different architectural choices, not just different variable names or formatting. The test does not require formal proof of difference -- it asks for plausible, non-trivial alternatives that both satisfy the stated outcome.

**Goal versus constraint:**

A statement that fails the two-implementations test may not be wrong -- it may be a constraint, not a goal. "Must use PostgreSQL" is not a goal, but it may be a valid constraint. The test distinguishes goals (open how) from specifications (closed how). The Constraint-Failure Decision Rule ([[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]) then classifies the specification as either a constraint (builder-facing guidance) or a failure condition (validator-facing check).

**Pre-flight, not post-hoc:**

The test is designed as a pre-flight gate -- applied before the agent receives the goal. It catches spec-disguised-as-goal statements at authoring time, not after the agent has already burned tokens executing a recipe that should have been an outcome. It is lightweight: one question, applied in seconds, not a formal review process.

## Implementation in this repo

### What already exists

- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- decomposes intent into structured fields including a description field. The description field is the natural home for a goal statement validated by the two-implementations test, but no test currently validates the description field's content against this heuristic.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 -- captures decisions through structured interview questions. None of the interview questions probe whether a candidate statement is a goal or a specification.
- [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] -- generates issues with observable behavior. Conceptually adjacent: vertical slices describe what the user sees, not how it is implemented, but the generation process does not apply a two-implementations test to distinguish goals from specs.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:31 -- "The separation of owners is the central architectural point: the human owns Intent and Expectations and never abandons them." The two-implementations test helps the human write better Intent by catching specifications that should be Context instead.

### What is missing from the pattern

The classification marks Two-Implementations Goal Test as Missing because no canonical doc, curriculum lesson, skill, or agent defines a "two-implementations test" or any equivalent heuristic for distinguishing goals from implementation specifications ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:94-101).

Missing items:

1. The two-implementations test itself as a named, documented heuristic. No repo artifact asks "can two different implementations both satisfy this?" as a goal-quality gate.
2. A pre-flight review gate that applies the test during intent authoring, before the agent receives the goal statement.
3. Integration with the intent-five-part-primitive skill: the description field of the five-part intent could be validated by the two-implementations test as a completeness sub-gate.
4. Curriculum content that teaches the distinction between goals and specifications with concrete examples and the two-implementations heuristic.
5. A lightweight skill trigger that runs the test as a one-question check against a candidate goal statement.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Preserves the agent's decision space where the harness actually wants model judgment | Needs reviewer judgment about what counts as "substantially different implementation" |
| Produces simpler, more portable task intents that describe outcomes, not methods | Can be misapplied to tasks where a tool choice is already an external constraint (e.g., "must use our approved payment provider") |
| Works well as a lightweight pre-flight skill or curriculum drill -- one question, seconds to apply | Does not guarantee the goal is atomic or valuable, only that it is not method-bound |
| Catches spec-disguised-as-goal at authoring time, before tokens are burned | Some domains have tightly constrained implementation spaces where "substantially different" is genuinely unavailable |
| Pairs naturally with Goal Atomicity Split and Constraint Budget Gate as a trio of intent-quality heuristics | Overly strict application could reject valid goals where only one approach is economically feasible |

## Relationship to Other Patterns

- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- the description field of the five-part intent is where the two-implementations test applies. The test validates that the description contains an outcome, not a specification.
- **[[docs/canonical/goal-atomicity-split|Goal Atomicity Split]]** -- goal atomicity (one sentence, no "and") and goal purity (not a spec in disguise) are complementary quality checks. Apply atomicity first, then the two-implementations test to each atomic goal.
- **[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]** -- the goal slot in the three-part contract should pass the two-implementations test. A goal that fails the test should be rewritten or routed to Context.
- **[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]** -- the alignment interview could include the two-implementations test as a diagnostic question during intent capture: "Here is the goal you stated. Can you name a completely different way to achieve it? If not, you may have written a specification."
- **[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]** -- when a statement fails the two-implementations test, the decision rule classifies it as either a constraint or a failure condition and routes it appropriately.
- **[[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]]** -- vertical slices describe observable behavior. The two-implementations test validates that the described behavior is an outcome (open how) rather than a specification (closed how).
- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- the test helps the human write Intent (what we want) and catch statements that should be Context (how we build it).

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:60-80 -- extracted pattern: Two-Implementations Goal Test
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Classification]]:85-110 -- classification evidence: Missing, Medium integration value
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- the description field where the test applies
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 -- structured interview as a potential home for the test
- [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] -- adjacent pattern: observable behavior generation
