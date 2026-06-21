---
title: "Three-Part Intent Contract"
type: canonical
tags: ["agentes-orquestracao", "spec-driven-development", "decision-discipline", "governanca"]
aliases: ["three-part intent", "three-slot intent", "goal-constraints-failure intent", "three-field intent", "intent contract", "intent decomposition three-part"]
last_updated: 2026-06-14
relates-to: ["[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/scenario-destination-split|Scenario Destination Split]]", "[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/canonical/constraint-budget-gate|Constraint Budget Gate]]", "[[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]]", "[[docs/canonical/goal-atomicity-split|Goal Atomicity Split]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
---

# Three-Part Intent Contract

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/
**Classification:** Partial Coverage, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Agents receive task prompts that mix outcome, implementation, evaluation, and contextual facts, making it hard to know what should guide generation and what should be checked after output exists. When a single intent artifact carries goal statements, non-functional constraints, failure conditions, success expectations, and implementation context, the agent cannot distinguish between "build toward this" and "verify this after building." The mixed signal produces a mixed result: the builder tries to satisfy everything at once, and the validator has no independent criteria.

The source names this as a slot confusion problem: when every requirement lives in one undifferentiated block of prose, the builder and validator both read the same text, and neither has a clear contract for their role ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|patterns]]:39-40).

The repo formalizes intent as a five-part primitive (description, constraints, failure scenarios, success scenarios, connections) in [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]. The three-part contract is a simpler decomposition that the five-part primitive subsumes but does not exactly match. The core structural difference is that the five-part primitive treats success scenarios as an intent field, while the three-part contract routes success scenarios out of intent entirely and into Expectations ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:65-76).

## Solution

Decompose the intent artifact into exactly three slots: goal, constraints, and failure conditions. Each slot has a distinct purpose and a distinct destination. No other content belongs in the intent -- implementation details belong to Context, success expectations belong to Expectations, and connections belong to orchestration.

**The three slots:**

| Slot | Purpose | Destination | Example |
|---|---|---|---|
| Goal | What the outcome owner wants, in outcome language | Builder surface | A red sneaker the buyer can buy for under $90 |
| Constraints | Boundaries that guide the builder's decisions during generation | Builder surface | Buyer's size, in stock, deliverable to buyer's location |
| Failure conditions | What wrong output looks like, expressed as binary checks | Validator surface | Returns a $140 sneaker, returns an out-of-stock sneaker, returns a non-red sneaker |

**Routing rule:**

- Goal and constraints go to the builder surface. They guide generation by telling the builder what to pursue and what boundaries to respect.
- Failure conditions go to the validator surface. They define what the evaluator checks against the builder's output. The builder does not see them.

The three-part contract creates the preconditions for compartmented evaluation ([[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]): because each field already has a destination, the harness can route information correctly before the builder and validator begin work.

**Comparison with the five-part primitive:**

The five-part primitive ([[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]) decomposes intent into five fields: description, constraints, failure scenarios, success scenarios, and connections. The three-part contract uses three fields: goal, constraints, failure conditions. The comparison:

| Element | Three-Part Contract | Five-Part Primitive |
|---|---|---|
| Goal / Description | In intent | In intent |
| Constraints | In intent | In intent |
| Failure conditions / scenarios | In intent | In intent |
| Success scenarios | In Expectations (not intent) | In intent |
| Connections | In orchestration (not intent) | In intent |

The models are compatible, not contradictory. The three-part contract is a simpler decomposition that routes success scenarios and connections out of intent. The five-part primitive is a richer decomposition that keeps more structure within the intent artifact. Which model to choose depends on whether the team treats success scenarios as part of intent (five-part model) or as part of Expectations (three-part model). The source author's position is that success scenarios belong to Expectations because they create shared visibility that enables reward-hacking ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|analysis]]:150-162).

**Discipline over format:**

The three-part contract is not a template -- it is a discipline. The value is not in having three boxes to fill; it is in the constraint that nothing else goes in intent. Implementation details are rejected from intent and routed to Context. Success expectations are rejected from intent and routed to Expectations. The contract enforces purity: intent describes what outcome we want and what failure looks like, and nothing else.

## Implementation in this repo

### What already exists

- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- five-field intent schema with description, constraints, failure scenarios, success scenarios, and connections. The constraints and failure scenarios fields map directly to two of the three slots; the description field maps to the goal slot.
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:43-48 -- completeness gate mechanics blocking agent execution when fields are missing. A completeness gate for the three-part contract would be simpler: three fields instead of five.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:35 -- "The five-part structure ensures completeness: any missing field is a visible gap, not an invisible delegation to the agent." The same principle applies to the three-part structure with fewer fields.
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:35-41 -- the Expectations artifact with done scenarios, failed scenarios, limits, non-goals, and outcome owner. In the three-part model, success scenarios would move from intent to this Expectations artifact.
- [[.opencode/skills/intent-five-part-primitive/SKILL.md|intent-five-part-primitive skill]]:19-23 -- operational skill enforcing the five-field completeness gate. A three-part variant could enforce a simpler gate.

### What is missing from the pattern

The classification marks Three-Part Intent Contract as Partial Coverage because the repo has a five-field decomposition but not the specific three-slot contract as a named alternative ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:65-76).

Missing items:

1. The three-slot decomposition (goal, constraints, failure conditions) as a named contract. The repo documents the five-part primitive but not the simpler three-part alternative.
2. The explicit routing of success scenarios out of intent and into Expectations. The five-part primitive includes success scenarios as an intent field; the three-part contract treats them as external to intent.
3. The routing of connections out of intent and into orchestration. The five-part primitive includes connections as an intent field; the three-part contract leaves them to the orchestration layer.
4. A skill or gate that enforces the three-part contract as a simpler alternative to the five-part completeness gate for contexts where the full five-part decomposition is overkill.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Simpler intent model with fewer fields -- three slots are easier to populate and validate than five | Loses the granularity of the five-part model: success scenarios and connections are no longer in the intent artifact |
| Creates a clear pre-condition for compartmented evaluation: each slot already has a known destination | Does not decide context or success expectations by itself -- other crafts must handle those responsibilities |
| Makes the intent artifact more portable because it carries less content | Requires disciplined review because bad fields can still be written inside the right slot |
| Pairs naturally with the Constraint-Failure Decision Rule and Scenario Destination Split | Teams already using the five-part primitive may resist adopting a simpler model that moves fields to other artifacts |
| Reduces the risk of success scenarios leaking into the builder surface | Loses impact traceability that the connections field provides in the five-part model |

## Relationship to Other Patterns

- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- the five-part primitive is the richer, more comprehensive intent decomposition in this repo. The three-part contract is a simpler alternative that moves two fields (success scenarios, connections) out of intent. Both models share the core triad of goal/constraints/failure.
- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- the three-part contract defines the structure of the Intent craft within ICE. ICE separates the crafts; the three-part contract defines what the Intent craft specifically contains.
- **[[docs/canonical/scenario-destination-split|Scenario Destination Split]]** -- the routing rule that sends success scenarios to Expectations and failure conditions to Intent. The three-part contract is the destination artifact for failure conditions; Scenario Destination Split is the routing logic that decides what goes where.
- **[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]** -- compartmented evaluation requires that the builder and validator receive different information. The three-part contract creates the fields that populate those two surfaces: goal and constraints for the builder; failure conditions for the validator.
- **[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]** -- the classification heuristic that decides whether a requirement belongs in constraints (builder surface) or failure conditions (validator surface). The three-part contract provides the slots; the decision rule classifies each requirement into the correct slot.
- **[[docs/canonical/constraint-budget-gate|Constraint Budget Gate]]** -- the numeric budget on the constraints slot. The three-part contract defines the constraints field; the budget gate limits how many constraints can populate it.
- **[[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]]** -- validates that the goal slot contains an outcome, not a method. The three-part contract defines the goal slot; the two-implementations test validates its content.
- **[[docs/canonical/goal-atomicity-split|Goal Atomicity Split]]** -- ensures the goal slot contains one sentence with one outcome. The three-part contract defines the goal slot; atomicity split ensures it does not hide multiple goals behind one sentence.

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:37-58 -- extracted pattern: Three-Part Intent Contract
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Classification]]:56-82 -- classification evidence: Partial Coverage, Medium integration value
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- five-field intent schema for comparison with three-slot model
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:43-48 -- completeness gate mechanics applicable to both models
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:35 -- five-part structure as completeness guarantee
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:35-41 -- Expectations artifact where success scenarios live in the three-part model
