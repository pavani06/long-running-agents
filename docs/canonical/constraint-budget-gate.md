---
title: "Constraint Budget Gate"
type: canonical
tags: ["agentes-orquestracao", "spec-driven-development", "decision-discipline", "evals"]
aliases: ["constraint budget", "constraint limit", "5 to 7 constraints", "directional constraints", "business language constraints", "constraint count gate", "constraint budget heuristic"]
last_updated: 2026-06-14
relates-to: ["[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
---

# Constraint Budget Gate

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/
**Classification:** Missing, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Constraint lists grow until they become hidden implementation specs. What starts as "the output must respect budget limits" expands into "the output must respect budget limits, use PostgreSQL, implement the repository pattern, expose a REST API, use JWT auth, log to CloudWatch, deploy to ECS, and run the integration suite before merge." Each addition removes a degree of freedom from the agent. The constraint list drifts from bounding unacceptable outcomes to specifying acceptable implementation, and the workflow drifts back toward the spec-driven development the harrow was designed to replace.

The source names this as constraint-list drift: "Constraint lists grow until they become hidden implementation specs, removing degrees of freedom from the agent and drifting the workflow back toward spec-driven development" ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|patterns]]:107-108).

The repo's Constraint-Anchored Evaluation pattern anchors evaluation on explicit, verifiable constraint lists but does not impose a numeric budget or a classification gate on those constraints. The canonical doc explicitly notes constraint list growth as a cost: "Constraint list can grow large, adding evaluation latency" ([[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:89). The repo treats this as a risk to manage, not as a hard gate. No mechanism limits constraints to 5-7, filters out implementation-level constraints, or routes them to Context or Expectations instead ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:152-157).

## Solution

Impose a hard budget of five to seven constraints per intent. Every candidate constraint must be directional (it tells the builder which way to go, not exactly what to build), unconditional (it does not depend on runtime state), and written in business language (it describes what the outcome owner cares about, not what the engineer would name as a requirement). Constraints that fail this classification are rejected from the constraint list and routed to their correct destination.

**The budget gate:**

| Constraint count | Action |
|---|---|
| 0-4 | Acceptable. Low constraint surface leaves more builder freedom. |
| 5-7 | Optimal. Enough constraints to bound unacceptable outcomes without specifying implementation. |
| 8+ | Budget exceeded. Review every constraint. Classify and route excess to Context, Expectations, or failure conditions. |

**Classification rules for excess constraints:**

When the budget is exceeded, each excess constraint is classified and routed:

| If the constraint... | Then it is... | Route it to... |
|---|---|---|
| Chooses a tool, names a pattern, or describes implementation | Implementation guidance | Context (the harness's inventory of technical standards) |
| Measures output quality and can only be checked after output exists | A failure condition | Expectations or the validator's failure conditions |
| Describes a desired outcome or user-facing behavior | A success scenario | Expectations (as a done scenario) |
| Is genuinely a boundary on acceptable output | A constraint | Keep in the constraint list, and remove a less-important constraint to stay within budget |

**What directional means:**

A directional constraint tells the builder which way to go without specifying the path. "The system must handle 10,000 concurrent users" is directional -- it specifies a boundary but leaves architecture, caching, queueing, and scaling decisions to the builder. "The system must use Redis for caching" is not directional -- it specifies a tool, not a boundary. The test: can the builder choose among multiple valid approaches and still satisfy this constraint? If yes, it is directional.

**What business language means:**

A business-language constraint describes what the outcome owner cares about in the outcome owner's terms. "Buyers must see only items in stock" is business language. "The `/inventory` endpoint must use an `IN_STOCK` filter with `excludeReserved=true`" is not business language -- it is an API specification. Business language belongs to the outcome owner; technical language belongs to the engineering team or the harness's Context inventory.

**What unconditional means:**

An unconditional constraint applies regardless of runtime state. "The system must handle 10,000 concurrent users" is unconditional -- it is always true. "If the load balancer is under 50% capacity, route to the primary cluster" is conditional on runtime state and belongs to the harness's orchestration logic, not to the intent's constraint list.

**The budget is a heuristic, not proof:**

The 5-7 number is a practical discipline informed by the source author's experience, not a mathematical derivation. Some regulated or high-risk domains may legitimately need more constraints. The budget serves as a forcing function: it asks the intent author to prioritize which boundaries truly matter, rather than listing every boundary they can think of.

## Implementation in this repo

### What already exists

- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 -- anchors evaluation on explicit, verifiable constraint lists from client state and business rules. Provides the evaluation mechanics for constraints but imposes no numeric budget or classification gate on which items qualify as constraints.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:89 -- explicitly notes constraint list growth as a cost: "Constraint list can grow large, adding evaluation latency." The repo acknowledges the risk but has not yet imposed a budget as a countermeasure.
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- the constraints field of the five-part intent is where the budget gate applies. The field currently has no numeric limit or business-language filter.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:62 -- gap list mechanism surfaces gaps between crafts, which could surface overgrown constraint lists. Does not gate them at a numeric budget, but provides the visibility that could trigger budget enforcement.

### What is missing from the pattern

The classification marks Constraint Budget Gate as Missing because no mechanism limits constraints to 5-7 or filters out implementation-level constraints ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:152-157).

Missing items:

1. A numeric budget gate that rejects intent when the constraint list exceeds 5-7 items and requires reclassification of excess items.
2. The classification rules for excess constraints: implementation guidance to Context, output checks to failure conditions, outcome behaviors to Expectations.
3. The dimensional, unconditional, business-language filter as a named quality standard for what qualifies as a constraint.
4. Integration with the intent-five-part-primitive skill: the constraints field completeness gate could add a budget check alongside the non-empty check.
5. A lightweight skill that runs the budget gate against candidate intent constraints before the agent receives them.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps constraints legible enough for humans and agents to use -- a short list is reviewable; a long list is ignored | The numeric budget (5-7) is a heuristic, not proof that every remaining constraint is valid |
| Protects the model's useful design latitude while still bounding unacceptable outcomes | Some regulated or high-risk tasks may legitimately need a larger external policy surface |
| Gives a concrete review gate for issue briefs, skills, and exercises | Requires a separate context system so removed implementation details are not simply lost |
| Prevents constraint-list drift -- the constraint list stays about outcomes, not implementations | Overzealous application could strip genuinely necessary constraints to meet the budget |
| Pairs naturally with the Constraint-Failure Decision Rule and Goal Atomicity Split as intent-quality heuristics | The budget needs calibration per domain -- a medical device intent may need more constraints than a UI tweak |

## Relationship to Other Patterns

- **[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]** -- constraint-anchored evaluation provides the verification mechanics that consume the constraints. The budget gate ensures the constraint list the evaluator receives is bounded and well-classified. Without the budget gate, the evaluator's verification matrix grows unbounded.
- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- the constraints field of the five-part intent is where the budget gate applies. The completeness gate should include a budget check: not just "is the field non-empty?" but "are there 5-7 well-classified constraints?"
- **[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]** -- the decision rule classifies individual requirements as constraints or failure conditions. The budget gate applies after classification: if the constraint list is too long, reclassify the weakest constraints and route them elsewhere.
- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- when the budget gate routes implementation constraints to Context, it is enforcing ICE craft separation: Intent says what; Context says how. The budget gate prevents Context from leaking into Intent through the constraint field.
- **[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]** -- the constraints slot in the three-part contract carries the budget-limited list. The budget gate ensures the slot does not grow into a specification.
- **[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]** -- the budget gate keeps the builder surface clean by removing implementation guidance that could constrain the builder's decision space unnecessarily.
- **[[docs/canonical/goal-atomicity-split|Goal Atomicity Split]]** -- atomic goals per intent. When each intent has one outcome, the constraint list naturally stays smaller because it only needs to bound that one outcome, not multiple.

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:104-125 -- extracted pattern: Constraint Budget Gate
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Classification]]:140-166 -- classification evidence: Missing, Medium integration value
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 -- constraint verification mechanics that the budget gate feeds
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:89 -- acknowledgement of constraint list growth as a cost
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- the constraints field of the five-part intent
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:62 -- gap list mechanism for surfacing craft boundary violations
