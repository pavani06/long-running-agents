---
title: "Human-Owned Expectations Boundary"
type: canonical
tags: ["governanca", "decision-discipline", "agentes-orquestracao", "spec-driven-development", "evals"]
aliases: ["expectations boundary", "outcome-owned expectations", "done boundary", "definition of done ownership", "expectations artifact", "human-owned done", "outcome owner expectations"]
last_updated: 2026-06-12
relates-to: ["[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]"]
sources: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]"]
---

# Human-Owned Expectations Boundary

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-12-idsd-method/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

When the definition of done is not authored by the person who wanted the outcome, the agent decides "done" on its own. The agent looks at its output, sees that it compiled, that it passed a few tests, and that it looks reasonable -- and marks it complete. The person who actually needs the outcome has a different definition of done, but they never wrote it down as a separate, owned artifact. The drift is invisible until the outcome fails in use.

The source names this as "done definition drift": "o momento em que a definicao de done se afasta da pessoa que queria o outcome, o agente comeca a decidir 'done' por ela" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:86). The fix is not a better specification format -- it is removing the definition of done from the agent's discretion entirely.

The repo separates evaluation from generation (Generator-Evaluator), anchors evaluation on constraints (Constraint-Anchored Evaluation), and defines contracts with success criteria (Sprint Contracts). But ownership of the definition of done is distributed -- rubric author, interviewer, evaluator -- rather than pinned to the outcome owner as a deliberate governance rule. The classification confirms Partial Coverage: "ownership is implicit rather than enforced as 'the person who wants the outcome must define done'" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:93).

## Solution

Define Expectations as a standalone artifact authored exclusively by the outcome owner and consumed by the harness for validation. Expectations are not a specification, not implementation instructions, and not a checklist of technical completions. They are the boundary -- what "done" and "failed" mean in the language of the person who needs the outcome.

**The Expectations artifact:**

| Field | Purpose | Example (red sneaker purchase) |
|---|---|---|
| Done scenarios | What successful outcomes look like in user/outcome language | Buyer searches for red sneakers, filters under $90, sees only in-stock items in their size, adds to cart, completes checkout |
| Failed scenarios | What must cause the output to be rejected | Returns a sneaker over $90, returns an out-of-stock sneaker, returns a non-red sneaker, returns a sneaker in the wrong size |
| Limits | Boundaries the result must respect | Price ceiling $90, stock must be real-time, delivery must be to buyer's shipping address |
| Non-goals | Explicitly out of scope to prevent scope creep | Does not include price comparison across retailers, does not include coupon application, does not include wishlist functionality |
| Outcome owner | Named person responsible for this definition of done | The product manager for the search-and-purchase flow |

**Ownership rule:**

The same person who wrote the Intent writes the Expectations. This is not a negotiable rule -- it is a structural separation. The outcome owner defines what done means. The agent does not. The harness does not. The engineer does not. If the outcome owner cannot articulate what done means in outcome language, the work is not ready for the agent.

When the outcome is subjective (e.g., "the UI should feel clean"), the Expectations artifact includes examples, rubrics, or reference outputs that make the subjective boundary concrete enough for the harness to validate against.

**Validation mechanics:**

The Expectations artifact is consumed by the harness during the ICE Loop:

1. Harness reads Expectations before generation begins.
2. Generator produces output within the Intent and Context boundaries.
3. Evaluator ([[docs/canonical/generator-evaluator|Generator-Evaluator]]) checks output against each Expectations field: does this output satisfy the done scenarios? Does it avoid the failed scenarios? Does it respect the limits?
4. If the output fails any Expectations field, the Evaluator returns a rejection with specific feedback tied to the failed field.
5. The Generator retries with the specific feedback.
6. When all Expectations fields are met, the output is done.

**Stop, retry, escalate conditions:**

Ambiguous expectations can create retry loops. The Expectations artifact includes conditions for when to stop retrying and escalate to the outcome owner:

- **Retry limit exceeded**: after N retries on the same expectation without convergence, escalate to the outcome owner.
- **Conflicting expectations detected**: if two expectations appear to contradict each other (e.g., "fast" and "comprehensive"), escalate for clarification.
- **Expectation requires human judgment**: some expectations cannot be validated automatically (e.g., "the tone should be professional but warm"). These are flagged for human review during the loop, not deferred to the final gate.

**Separation from implementation instructions:**

Expectations are not a specification. A specification says "build a REST endpoint at /search with query parameters color, maxPrice, and size, using Elasticsearch for the query." Expectations say "a buyer can search for red sneakers under $90 and see only items they can actually buy." The specification tells the agent how; the Expectations artifact tells the agent what success looks like. The how belongs to the agent, within the boundaries the Expectations set.

## Implementation in this repo

### What already exists

- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-73 separates generation from evaluation. The Evaluator checks output against rubrics and constraints. The rubrics serve as expectations, but their authorship (who defines the rubric) is not enforced as outcome-owner-owned.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 anchors evaluation on explicit, verifiable constraints from client state and business rules. Constraints define the done boundary, but the pattern focuses on constraint verification mechanics rather than constraint ownership.
- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]:29-51 defines explicit ownership with refusal authority. Owns the value decision, not the definition of done for a specific outcome.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 captures decisions and defers unresolved questions. The interview output forms implicit expectations, but the output is a decision ledger, not an expectations artifact.
- [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]:73-78 attaches intent statements and scope constraints to build decisions. Scope constraints define done boundaries, but the pattern focuses on placement in the loop rather than ownership.
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:33-35 asks "Who needs this, and what breaks for them if it never exists?" Forces the outcome-owner to define what success looks like, but as a diagnostic question rather than a formal expectations artifact.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 reviews plans with dual rubrics. The product/destination reviewer evaluates against outcome expectations, but this is a review of a plan, not a standalone expectations artifact consumed during execution.
- [[curriculum/05-core-concepts/04-sprint-contracts|Sprint Contracts]]:1-3412 formalizes explicit agreements with scope, success criteria, and failure handling. Closest existing mechanism to an expectations boundary -- a contract defining what done means. However, the contract is presented as a negotiated agreement between human and agent, not as a boundary authored exclusively by the outcome owner.

### What is missing from the pattern

The classification marks Human-Owned Expectations Boundary as Partial Coverage because expectations exist in multiple forms (contracts, rubrics, constraints) but ownership is distributed rather than pinned to the outcome owner as a deliberate governance rule ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:92-107).

Missing items:

1. The Expectations artifact as a named, standalone document type with explicit fields (done scenarios, failed scenarios, limits, non-goals, outcome owner).
2. The ownership rule: the same person who wrote the Intent writes the Expectations. This is not currently enforced anywhere in the repo's workflows.
3. Stop, retry, escalate conditions tied to the Expectations artifact. The retry loop in Generator-Evaluator exists, but escalation conditions for ambiguous or conflicting expectations are not defined.
4. Integration of the Expectations artifact into the ICE Loop: the Evaluator consumes the Expectations artifact, checks output against each field, and returns field-specific rejection feedback.
5. The distinction between Expectations (outcome language, owned by outcome owner) and implementation instructions (technical language, owned by agent). The repo does not currently separate these.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps the definition of done out of the agent's discretion -- the agent cannot redefine what success means | Expectations are not an implementation spec and still need translation into tests, evals, or review checks |
| Lets the harness validate outputs against outcome language, not only code completion or test pass/fail | Subjective outcomes need rubrics or examples to become reliably enforceable by automated evaluation |
| Makes failed and successful outcomes visible before a large diff exists -- the boundary is defined upfront | The boundary can slow work if the outcome owner is unavailable when ambiguity appears during execution |
| Pairs naturally with constraint-anchored evaluation: the constraints field of the expectations feeds directly into the evaluator | Adding formal expectations for every task adds ceremony that small, reversible tasks may not need |
| Creates a clean handoff to the evaluator: "here is what done means, validate against this" instead of "figure out what done means" | Expectations quality depends on the outcome owner's ability to articulate outcomes in their own language |

## Relationship to Other Patterns

- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- the Expectations craft in the ICE trichotomy. ICE separates the three crafts; this pattern defines the structure, ownership, and validation mechanics of the Expectations craft specifically.
- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- Intent and Expectations are written by the same person (the outcome owner), but they are different crafts. Intent defines the desire; Expectations define the done boundary. The five-part intent's success/failure scenarios overlap with Expectations, but Expectations add the ownership rule, limits, non-goals, and escalation conditions.
- **[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]** -- when expectations are ambiguous during execution, the outcome owner must be present to clarify. Presence-in-the-loop ensures the owner is available for that clarification.
- **[[docs/canonical/generator-evaluator|Generator-Evaluator]]** -- the Evaluator consumes the Expectations artifact as its validation rubric. Without owned expectations, the Evaluator is checking output against criteria the outcome owner never explicitly defined.
- **[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]** -- constraints in the Expectations artifact feed directly into the constraint verification process. Constraints define the done boundary; constraint-anchored evaluation verifies it.
- **[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]** -- the pre-execution value gate should check whether the Expectations artifact exists and whether it was authored by the outcome owner. A missing or proxy-authored expectations artifact is a value-gate failure.
- **[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]** -- when expectations are ambiguous, the agent fills the gaps with tokens. Clear expectations reduce retries and prevent the agent from burning tokens exploring wrong definitions of done.
- **[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]** -- the Owner-of-No can refuse work. The Expectations artifact gives the Owner-of-No a concrete artifact to evaluate: "does this definition of done justify building this?"
- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake question "Who needs this, and what breaks for them if it never exists?" probes whether an outcome owner exists. The Expectations artifact is what that owner produces to define done.
- **[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]** -- the product/destination reviewer in the split-brain review evaluates the plan against the Expectations artifact. The Expectations artifact provides the rubric for that review.

## References

- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:27 -- Expectations como craft separavel: fronteira de done/failed/limites
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:84-88 -- done definition drift e Expectations como artefato separado do outcome owner
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:169 -- failure pattern: done definition drift quando Expectations nao sao craft separado com dono
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]:73-101 -- extracted pattern: Outcome-Owned Expectations Boundary
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]:84-107 -- classification evidence: Partial Coverage, High integration value
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:118-119 -- caso dos tres dias de retrabalho: o agente tinha uma spec boa mas derivou porque ninguem estava no loop para manter o done boundary
