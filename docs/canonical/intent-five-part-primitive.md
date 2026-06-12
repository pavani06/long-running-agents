---
title: "Intent as Five-Part Primitive"
type: canonical
tags: ["governanca", "decision-discipline", "agentes-orquestracao", "spec-driven-development", "harness-engineering"]
aliases: ["five-part intent", "intent completeness gate", "intent primitive", "five-field intent", "intent format", "intent structure", "intent completeness"]
last_updated: 2026-06-12
relates-to: ["[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]"]
sources: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]"]
---

# Intent as Five-Part Primitive

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-12-idsd-method/
**Classification:** Missing, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

When a human asks an agent to build something, the request arrives as prose -- a paragraph or two of what the person wants. The agent processes it, notices gaps (things the human did not specify), fills them with assumptions, and produces output that looks correct but encodes decisions the human never explicitly made. The failure is not that the agent built wrong -- it is that the human's request was not structured as an inspectable primitive. Missing fields become agent discretion.

The source names this as the gap-filling problem: "Faltar qualquer um dos cinco devolve o controle ao agente para preencher a lacuna" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:26). The five-part structure is designed so that every unfilled field is a visible gap, not an invisible delegation.

The repo captures intent through alignment interviews ([[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]) and constraint-anchored evaluation ([[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]), but does not formalize intent as a five-field primitive with a completeness gate before execution. The classification confirms this is Missing: "no document defines a five-part intent format" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:66-67).

## Solution

Formalize intent as a five-field primitive that must pass a completeness gate before the agent begins implementation. Each field has a distinct purpose. If any field is empty or ambiguous, the intent is incomplete and the agent should not proceed -- the gap should be routed back to the outcome owner.

**The five fields:**

| Field | Purpose | Example (red sneaker purchase) |
|---|---|---|
| Description | What the outcome owner wants, in outcome language | A red sneaker the buyer can buy for under $90 |
| Constraints | Boundaries that bound acceptable work | Buyer's size, in stock, deliverable to buyer's location |
| Failure scenarios | What wrong output looks like | Returns a $140 sneaker, an out-of-stock sneaker, or a non-red sneaker |
| Success scenarios | What the desired outcome looks like | Buyer adds an affordable red sneaker to cart and checks out |
| Connections | Other intents, systems, or workflows affected by this work | Anything touching price, inventory, or checkout -- a change here changes those |

**Completeness gate mechanics:**

1. **Pre-execution check.** Before the agent receives the intent, a gate validates that all five fields contain non-trivial, non-ambiguous content. Empty fields are gaps, not defaults.
2. **Missing-field routing.** Any empty or ambiguous field generates a specific question routed back to the outcome owner. The question names which field is missing and what kind of information is needed.
3. **Normalized intent record.** Once all five fields are populated, the intent is recorded as a normalized artifact attached to the agent task. This record travels with the task through planning, execution, review, and merge.
4. **Impact traceability.** The connections field creates explicit links between intents. When an intent changes, the connections field shows which other intents, systems, or workflows may be affected. This enables impact analysis before code is written.

**Concrete first move -- the one-hour practical start:**

The source recommends against a full methodological rollout. Instead: take one real outcome shipping this week. Write the five parts for it. Hand it to someone who was not in your head and ask where the agent would still have to guess. Each place they point to is a gap you were about to leave for the agent to fill. Close those gaps -- not the whole system. Cost: one hour ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:82).

## Implementation in this repo

### What already exists

- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:30-37 captures decisions, deferrals, and rationale in a ledger through structured one-question-at-a-time interviewing. Structurally similar to intent capture but records decisions without the five specific fields.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 anchors evaluation on explicit, verifiable constraint lists pulled from persisted client state and business rules. Covers the constraints field as an evaluation input, not as an intent field.
- [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]:73-78 attaches intent statements and scope constraints to build decisions at the pre-execution gate. Separates intent from execution but does not decompose intent into five fields.
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:31-36 asks three diagnostic questions (who needs this, cost proxy, who says no) that force the outcome owner to clarify value and ownership before execution. The diagnostic questions probe intent quality but do not decompose intent into the five-part structure.
- [[curriculum/05-core-concepts/04-sprint-contracts|Sprint Contracts]]:1-3412 formalizes scope, success criteria, and failure handling as a negotiated agreement. Covers success and failure scenarios but within a contract frame, not an intent frame.

### What is missing from the pattern

The classification marks Intent as Five-Part Primitive as Missing because the five-field structure (description, constraints, failure scenarios, success scenarios, connections) is not present in any repo document, skill, or curriculum lesson ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:63-73).

Missing items:

1. The five-field intent schema itself -- description, constraints, failure scenarios, success scenarios, connections -- as a formal primitive.
2. A pre-execution completeness gate that blocks the agent when any of the five fields is missing or ambiguous.
3. Missing-field question routing: when a field is empty, generate a targeted question for the outcome owner, not a generic prompt.
4. Impact traceability via the connections field: when one intent changes, what else might be affected?
5. Integration with the Grill-Me Alignment Interview: the interview questions could be structured to populate all five fields systematically.
6. Curriculum content on intent as a first-class primitive with completeness criteria (could live in Level 2 or 3).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Turns intent from prose into an inspectable, gateable artifact with explicit fields | Adds upfront precision cost for every outcome request |
| Missing fields become visible gaps routed to the owner, not invisible delegations to the agent | Requires the outcome owner to understand the domain well enough to name failure cases and connections |
| Connections field creates impact traceability -- a change to one intent is traceable to downstream effects | Connections become stale unless maintained as the system changes |
| Reduces token burn caused by the agent exploring unstated assumptions during execution | Can become bureaucratic if applied to exploratory spikes that need freedom, not precision |
| Pairs naturally with constraint-anchored evaluation (constraints already exist there) and sprint contracts | Does not by itself prove that each field is correct or complete -- only that it is non-empty |

## Relationship to Other Patterns

- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- the five-part intent is the Intent craft in the ICE decomposition. ICE separates the three crafts; the five-part primitive defines the structure of the Intent craft specifically.
- **[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]** -- the alignment interview's one-question-at-a-time structure can be organized to populate all five intent fields systematically. The interview captures decisions; the five-part primitive provides the fields those decisions populate.
- **[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]** -- the constraints field of the five-part intent feeds directly into the constraint verification during evaluation. The constraints in the intent define what the evaluation should check.
- **[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]** -- missing intent fields are the root cause of gap-filling token burn. When the five-part primitive is complete, the agent spends fewer tokens guessing. The five-part primitive is the preventive measure; gap-filling cost attribution is the diagnostic that proves it works.
- **[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]** -- the five-part completeness gate is a pre-execution gate within the value-gated loop. If the intent is incomplete, the build should not proceed.
- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake questions probe the value dimension of an intent (who needs it, cost proxy). The five-part primitive probes the structural completeness dimension (are all five fields populated?). The two gates address different facets of intent quality.

## References

- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:26 -- intent as five-component primitivo de primeira classe
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:69-76 -- mecanica concreta dos cinco campos com exemplo do tenis vermelho
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:82 -- practical first move: uma hora, nao um rollout metodologico
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]:44-71 -- extracted pattern: Five-Part Intent Completeness Gate
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]:55-81 -- classification evidence: Missing, Medium integration value
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:118-119 -- caso dos tres dias de retrabalho causado por gaps no intent
