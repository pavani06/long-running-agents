---
title: "Constraint-Failure Decision Rule"
type: canonical
tags: ["agentes-orquestracao", "spec-driven-development", "decision-discipline", "evals"]
aliases: ["constraint vs failure condition", "would knowing this change", "builder guidance rule", "constraint classification rule", "failure condition rule", "constraint-or-failure heuristic", "builder-validator classification"]
last_updated: 2026-06-14
relates-to: ["[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/constraint-budget-gate|Constraint Budget Gate]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]", "[[docs/canonical/scenario-destination-split|Scenario Destination Split]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
---

# Constraint-Failure Decision Rule

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/
**Classification:** Missing, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Teams mix builder guidance with validator checks, which exposes eval targets to the agent and turns directional constraints into arbitrary pass/fail thresholds. A requirement like "the search response must be relevant" gets included in both the builder's prompt and the validator's rubric. The builder treats it as a hint (make the search look relevant), and the validator treats it as a check (is the search relevant?). The dual use means the validator is checking output against a criterion the builder already knew about, and the builder is optimizing for a criterion that was never precise enough to guide design.

The source names this as a classification failure: "Teams mix builder guidance with validator checks, which exposes eval targets to the agent and turns directional constraints into arbitrary pass/fail thresholds" ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|patterns]]:129-131).

The repo's five-part intent includes both constraints and failure scenarios as separate fields ([[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41), implying they are different, but provides no decision rule for classifying a candidate requirement into one field or the other. The classification is left to author judgment without a formal heuristic ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:180-185).

## Solution

Classify every candidate requirement using a single decision question: **"Would knowing this change how the builder writes code?"** If yes, the requirement is a constraint -- it guides the builder's design decisions and belongs on the builder surface. If no -- it can only be checked after output exists and the builder cannot meaningfully use it during generation -- it is a failure condition and belongs on the validator surface.

**The decision rule:**

| Question | Answer | Classification | Destination | Example |
|---|---|---|---|---|
| Would knowing this change how the builder writes code? | Yes | Constraint | Builder surface (Intent) | "The system must handle 10,000 concurrent users" -- knowing this changes architecture decisions, caching strategy, and queue design. |
| Would knowing this change how the builder writes code? | No | Failure condition | Validator surface (hidden from builder) | "Output must not return products priced above the user's stated budget" -- this can only be checked after output exists. Knowing it in advance does not change how the builder approaches the problem; it only changes what the validator checks. |

**Why the rule works:**

A constraint changes design. The builder uses it to make decisions: which architecture, what approach, where to spend complexity budget. A failure condition checks output. The builder cannot use it to make decisions because it only applies after the work is done. Telling the builder "the output must pass these 20 validation checks" does not produce better output -- it produces output that passes those 20 checks, regardless of whether it satisfies the underlying outcome. Telling the builder "the system must handle 10,000 concurrent users" changes how the builder thinks about the entire design.

**Borderline cases:**

Some requirements sit on the boundary. "The UI must be accessible" could change how the builder writes code (use semantic HTML, add ARIA labels, test with screen readers) -- constraint. It could also only be checked after output exists (run accessibility audit, check contrast ratios) -- failure condition. When a requirement naturally spans both categories, the stronger classification wins:

1. If the requirement can change design decisions (even if it also needs post-hoc verification), classify as constraint.
2. If the requirement can only be verified after output exists and provides no design guidance, classify as failure condition.
3. If the requirement needs both a builder-facing direction and a separate hidden eval, create two artifacts: a constraint for the builder and a hidden failure condition for the validator.

**Honest routing as a structural requirement:**

The rule depends on honest routing. If someone copies a failure condition into the builder prompt, the rule's benefit is lost and the builder can game the check. The compartmented evaluation architecture ([[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]) provides the structural enforcement that prevents this leakage. The decision rule decides the classification; compartmented evaluation enforces it.

**Simpler than it sounds:**

The rule is a single question applied to each candidate requirement. It does not require a framework, a methodology, or a formal process. It requires asking one question and routing accordingly. This makes it teachable in minutes and applicable at any scale, from a single intent review to a full constraint-audit of an existing system.

## Implementation in this repo

### What already exists

- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- defines constraints and failure scenarios as separate intent fields. The structure implies they are different, but no rule explains how to decide which classification applies to a given requirement.
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:35-41 -- defines failed scenarios and limits as expectations fields. Adjacent to failure conditions but does not define the constraint/failure boundary.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:77-83 -- the Generator builds, the Evaluator checks. The architecture implies different information surfaces, but no rule classifies what goes on which surface.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 -- anchors evaluation on explicit constraint lists. The constraints the evaluator uses should ideally be pre-classified by the decision rule, but the classification step does not exist.
- [[.opencode/skills/intent-five-part-primitive/SKILL|intent-five-part-primitive skill]]:19-23 -- checks field completeness but does not classify items into constraint versus failure condition using a decision rule.
- [[curriculum/05-core-concepts/04-sprint-contracts|Sprint Contracts]] -- separates scope from success criteria and failure handling using a contract negotiation frame, not a constraint-versus-failure heuristic.

### What is missing from the pattern

The classification marks Constraint-Failure Decision Rule as Missing because no canonical doc, skill, or curriculum lesson provides a decision rule for classifying requirements as constraints versus failure conditions ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:180-185).

Missing items:

1. The decision question itself -- "Would knowing this change how the builder writes code?" -- as a named, documented heuristic.
2. A classification gate embedded in the intent-five-part-primitive skill that classifies each requirement into constraints or failure conditions using the decision rule.
3. Integration with the three-part intent contract: the decision rule populates the constraints slot (builder surface) and failure conditions slot (validator surface) of the three-part contract.
4. Curriculum content teaching the classification rule with examples of requirements that change builder decisions versus requirements that only verify output.
5. A lightweight skill trigger that runs the decision rule against a candidate requirement and returns the classification with rationale.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents agents from gaming checks that should belong to the validator -- the builder cannot see failure conditions if they are correctly routed | Borderline cases still require human judgment -- the rule is not fully automatable |
| Gives reviewers a simple, teachable classification rule -- one question that applies consistently across domains | Some requirements may legitimately need both a builder-facing direction and a separate hidden eval |
| Enables encrypted or hidden evals because failure conditions are already separated from builder guidance | The rule depends on honest routing -- it fails if failure conditions are copied back into the builder prompt |
| Cleaner separation between generation guidance and evaluation criteria -- each surface gets only what it needs | Over-classification can create an artificial split where a requirement genuinely belongs on both surfaces |
| Pairs with Constraint Budget Gate and Compartmented Evaluation Architecture as a coordinated constraint-management stack | The rule cannot detect misclassification -- a constraint routed as a failure condition or vice versa produces wrong behavior silently |

## Relationship to Other Patterns

- **[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]** -- the validator's verification mechanics. The decision rule ensures the verification matrix only receives correctly classified failure conditions, not builder-facing constraints that would expose eval targets.
- **[[docs/canonical/constraint-budget-gate|Constraint Budget Gate]]** -- the budget gate limits the constraint list size. The decision rule ensures the items in the constraint list are genuinely constraints, not misclassified failure conditions that slipped through.
- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- the five-part intent provides separate slots for constraints and failure scenarios. The decision rule is the classification logic that decides which slot each requirement goes into.
- **[[docs/canonical/generator-evaluator|Generator-Evaluator]]** -- the Generator builds with constraints; the Evaluator checks with failure conditions. The decision rule ensures each agent receives the right type of requirement for its role.
- **[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]** -- compartmented evaluation depends on correct classification. If a failure condition is misclassified as a constraint and routed to the builder surface, the sealed surface is breached. The decision rule is the gate that prevents misclassification.
- **[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]** -- the contract's constraints slot receives builder-facing requirements; the failure conditions slot receives validator-facing requirements. The decision rule populates both slots correctly.
- **[[docs/canonical/scenario-destination-split|Scenario Destination Split]]** -- the same classification logic applied to scenarios specifically: failure scenarios become failure conditions (validator surface); success scenarios go to Expectations. The decision rule handles the general case; the destination split handles scenarios.
- **[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]** -- the Expectations artifact includes failed scenarios. The decision rule classifies which failed scenarios should stay as expectations (human-checkpointed) versus which should become hidden failure conditions (validator surface).
- **[[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]]** -- when a statement fails the two-implementations test (it is a specification, not a goal), the decision rule classifies it as constraint or failure condition and routes it accordingly.

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:127-149 -- extracted pattern: Constraint-Failure Decision Rule
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Classification]]:168-195 -- classification evidence: Missing, Medium integration value
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- constraints and failure scenarios as separate fields
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:35-41 -- failed scenarios as an expectations field
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:77-83 -- Generator and Evaluator with different responsibilities
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 -- verification matrix that consumes correctly classified constraints
