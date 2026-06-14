---
title: "Scenario Destination Split"
type: canonical
tags: ["agentes-orquestracao", "spec-driven-development", "decision-discipline", "evals"]
aliases: ["scenario split", "scenario routing", "failure vs success split", "binary failure conditions", "scenario destination routing", "expectations split"]
last_updated: 2026-06-14
relates-to: ["[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
---

# Scenario Destination Split

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/
**Classification:** Partial Coverage, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Scenarios serve conflicting roles as both builder guidance and validator checks. When the same scenario appears in both the builder's prompt and the validator's rubric, the builder over-fits to the visible scenario and the validator loses independence. A success scenario that tells the builder "the output should look like X" also tells the builder "produce X and it will pass." A failure scenario that tells the builder "avoid Y" also tells the builder "just don't do Y and you're fine." The scenarios stop measuring whether the output satisfies the outcome and start measuring whether the builder followed the scenario.

The source names this as a role-conflict problem: "Scenarios serve conflicting roles as builder guidance and validator checks; sharing the same scenarios causes over-fitting and weakens independent validation" ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|patterns]]:175-176).

The repo's five-part intent includes both failure scenarios and success scenarios as fields of the Intent artifact ([[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:39-40). The Human-Owned Expectations Boundary also includes both done scenarios and failed scenarios as fields of the Expectations artifact ([[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:36-37). Both artifacts cover both types of scenarios, creating an intentional overlap rather than a destination split. The repo does not formalize a routing rule that sends failure scenarios exclusively to Intent and success scenarios exclusively to Expectations ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:247-254).

## Solution

Split scenarios by destination: failure scenarios become binary failure conditions in Intent, routed to the validator surface and hidden from the builder. Success scenarios move to Expectations, generated from intent plus context, with a mandatory human checkpoint before execution proceeds.

**The split rule:**

| Scenario type | Destination | Recipient | Format | Builder sees it? |
|---|---|---|---|---|
| Failure scenarios | Intent (failure conditions) | Validator surface | Binary pass/fail checks | No -- hidden from builder |
| Success scenarios | Expectations (done scenarios) | Expectations artifact | Outcome-language examples | Yes -- after human checkpoint |

**Why the split matters:**

Failure scenarios routed to the validator surface remain structurally independent. The builder does not see them, so it cannot optimize output to avoid specific failure checks. This makes failure conditions a true measure of output quality, not a measure of the builder's ability to pattern-match.

Success scenarios routed to Expectations serve a different purpose: they define what done looks like in outcome language, not in implementation language. They are reviewed by a human before execution, giving the outcome owner a checkpoint to confirm the expectations match the intent. The builder sees them only after human approval, and only as a definition of success -- not as hidden evaluation criteria.

**Failure conditions as binary checks:**

Failure scenarios converted to failure conditions must be binary: either the output satisfies the condition or it does not. "The output might be too expensive" is not binary. "The output includes a product priced over $90" is binary. This binary property makes failure conditions mechanically verifiable -- the validator can check each one without judgment.

**Expectations as generated from intent plus context:**

Success scenarios in the Expectations artifact are generated from the intent (what the outcome owner wants) plus context (what the technical environment enables). The generation is not purely human-authored -- the harness derives candidate success scenarios from the intent and context, and the human approves or rejects them. This reduces the authoring burden on the outcome owner while keeping human judgment at the checkpoint.

**Human checkpoint before execution:**

Before the builder receives the success scenarios from the Expectations artifact, a human checkpoint confirms:
1. The generated success scenarios accurately reflect the intended outcome.
2. No success scenario accidentally encodes a hidden failure condition.
3. The expectations are complete enough to judge done-ness.

The human checkpoint prevents generated expectations from introducing bias or drifting from the intent. It creates a deliberate pause where the outcome owner asserts ownership of the definition of done.

## Implementation in this repo

### What already exists

- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:39-40 -- failure scenarios and success scenarios are both fields of the five-part intent. Both types of scenarios live in the same artifact, with no routing rule sending them to different destinations.
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:36-37 -- done scenarios (success) and failed scenarios (failure) are both fields of the Expectations artifact. The Expectations artifact covers both scenario types, with no rule that failure scenarios should be in Intent and success scenarios in Expectations.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:35 -- the Intent includes "failure scenarios, success scenarios" as fields. The Expectations include "scenarios, limits, non-goals" ([[docs/canonical/ice-craft-separation|ICE Craft Separation]]:47).
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:110 -- acknowledges the overlap: "The five-part intent's success/failure scenarios overlap with Expectations, but Expectations add the ownership rule, limits, non-goals, and escalation conditions."
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-85 -- separates generation from evaluation. The evaluator checks output, but both failure and success scenarios are available to both sides, creating the role-conflict problem the split addresses.

### What is missing from the pattern

The classification marks Scenario Destination Split as Partial Coverage because scenarios exist in both Intent and Expectations but without an explicit routing rule ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:247-254).

Missing items:

1. An explicit routing rule: "failure scenarios belong to Intent as binary failure conditions; success scenarios belong to Expectations as done scenarios." The repo has both types in both places.
2. The human checkpoint for generated expectations -- the Expectations artifact is authored by the outcome owner, not generated from intent plus context with a human checkpoint. The pattern proposes expectations-as-generated-artifact with human approval; the repo treats them as directly authored.
3. The specific naming "scenario destination split" and the framing of the problem as scenarios serving conflicting roles that must be resolved by routing them to different destinations.
4. The explicit binary requirement for failure conditions: "binary" means mechanically verifiable without judgment. The repo's failure scenarios do not have a binary format requirement.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps validator-owned failure conditions independent from builder hints -- the builder cannot optimize for what it cannot see | Requires an expectations generation step and a human checkpoint, adding ceremony |
| Success criteria can include real context (from the harness) without the human hand-authoring every scenario from scratch | Poorly generated expectations can still bias downstream work even after human checkpoint |
| Gives curriculum a concrete exercise for separating examples, expectations, and evals | Teams may resist the split because shared scenarios feel simpler at first |
| Binary failure conditions enable automated verification without judgment calls | Some failure conditions resist binary formulation and require human judgment |
| Creates a clean pre-condition for compartmented evaluation: the scenarios already know their destinations | The split depends on honest routing -- if someone copies success scenarios into the builder prompt, the benefit is lost |

## Relationship to Other Patterns

- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- the five-part intent currently holds both scenario types. The destination split would restructure the five-part primitive: failure scenarios stay in intent as binary failure conditions; success scenarios move to Expectations.
- **[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]** -- the destination for success scenarios after the split. The Expectations artifact currently holds both scenario types; the split would make it the exclusive home of success scenarios.
- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- the split clarifies what each ICE craft owns for scenarios: Intent owns failure conditions (validator-facing); Expectations owns success scenarios (human-checkpointed). ICE motivates the split; the split makes ICE's scenario handling concrete.
- **[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]** -- the three-part contract provides the destination slots: failure conditions go to the failure conditions slot in the intent; success scenarios go out of intent entirely. The destination split is the routing logic that populates the three-part contract.
- **[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]** -- compartmented evaluation requires that the builder cannot see failure conditions. The destination split ensures failure conditions are routed to the validator surface, not the builder surface. Compartmented evaluation depends on the split being executed correctly.
- **[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]** -- the classification rule that determines whether a requirement is a constraint (builder-facing) or a failure condition (validator-facing). The destination split applies the same classification logic to scenarios specifically.
- **[[docs/canonical/generator-evaluator|Generator-Evaluator]]** -- the Generator builds; the Evaluator checks. The destination split ensures each receives the right scenarios for its role. Generator receives success scenarios (after checkpoint); Evaluator receives failure conditions (hidden).

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:173-195 -- extracted pattern: Scenario Destination Split
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Classification]]:229-254 -- classification evidence: Partial Coverage, Medium integration value
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:39-40 -- failure scenarios and success scenarios as intent fields
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:36-37 -- done scenarios and failed scenarios as expectations fields
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:110 -- acknowledgement of scenario overlap between intent and expectations
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:35, 47 -- scenarios in both intent and expectations
