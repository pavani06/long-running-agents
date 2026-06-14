---
title: "Compartmented Evaluation Architecture"
type: canonical
tags: ["agentes-orquestracao", "evals", "spec-driven-development", "harness-engineering", "decision-discipline"]
aliases: ["compartmented evaluation", "sealed information surfaces", "hidden evals", "encrypted evals", "reward-hacking prevention", "information compartmentation", "evaluation compartment", "builder-validator separation"]
last_updated: 2026-06-14
relates-to: ["[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/scenario-destination-split|Scenario Destination Split]]", "[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
---

# Compartmented Evaluation Architecture

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

LLM builders reward-hack visible tests, scenarios, and rubrics, producing outputs that pass checks without satisfying the intended outcome. When the same failure conditions that the validator uses to judge output are visible to the builder during generation, the builder optimizes for the check rather than the outcome. The result is output that looks correct on paper -- all tests pass, all scenarios are satisfied -- but fails the underlying goal because the builder learned to game the visible evaluation criteria.

The source names this as a loss-of-signal problem: when the builder sees the validator's checks, those checks stop measuring the outcome and start measuring the builder's ability to satisfy the visible pattern. "LLM builders reward-hack visible tests, scenarios, and rubrics, producing outputs that pass checks without satisfying the intended outcome" ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|patterns]]:153-154).

The repo's Generator-Evaluator architecture structurally separates the Generator (builder) from the Evaluator (validator) with distinct information contexts ([[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-85). The ICE Craft Separation further separates crafts with explicit owners ([[docs/canonical/ice-craft-separation|ICE Craft Separation]]:53-58). However, the repo does not explicitly formalize "sealed information surfaces" -- there is no mechanism that prevents the Generator from accessing the Evaluator's rubrics, no concept of "encrypted evals," and no audit trail of which information each participant could see ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:206-221).

## Solution

Extend the Generator-Evaluator separation with explicit information compartmentation. The builder receives only goal and constraints -- the instruction surface needed to generate output. The validator receives failure conditions -- the evaluation surface needed to verify correctness. These surfaces are sealed: the builder cannot see the validator's rubrics, failure scenarios, or evaluation checks. The validator cannot influence the builder's generation beyond the explicit constraint set.

**The two sealed surfaces:**

| Surface | Recipient | Content | Purpose | Can the other side see it? |
|---|---|---|---|---|
| Builder surface | Generator agent | Goal statement, directional constraints | Guide generation toward the intended outcome | Validator can read (to confirm constraints were respected) |
| Validator surface | Evaluator agent | Failure conditions, evals, rubrics | Independently verify output against outcome criteria | Builder cannot read (prevents reward-hacking) |

**Compartmentation mechanics:**

1. **Information boundary enforcement.** The harness maintains an explicit list of what the builder received versus what the validator received. Any attempt to copy validator content into the builder prompt is a compartmentation violation.

2. **Encrypted or hidden evals.** Failure conditions are compiled into evals that the builder cannot access. The builder sees "validate output against expectations" but never sees the specific failure conditions, example scenarios, or pass/fail thresholds. This makes the evals structurally independent -- the builder cannot optimize for what it cannot see.

3. **Audit trail of information visibility.** The harness records which information each participant (builder, validator, human reviewer) could see at each step. This creates verifiable proof that the builder did not have access to validator criteria at generation time.

4. **Leakage prevention.** Explicit rules prevent a human from copying failure conditions into the builder prompt. The harness flags any content that appears on the validator surface but leaks onto the builder surface.

5. **Named design intent.** The architecture explicitly names "reward-hacking prevention" as its design intent. The separation is not an incidental property of using two agents -- it is the reason two agents exist.

**Relationship to Generator-Evaluator:**

The Generator-Evaluator architecture separates the roles; Compartmented Evaluation Architecture makes the separation structural. Generator-Evaluator says "generate with one agent, evaluate with another." Compartmented Evaluation says "the generating agent must not see the evaluation criteria -- and the harness must prove it." The difference is in the enforcement: Generator-Evaluator is a pattern; Compartmented Evaluation Architecture is a property the pattern can have or fail to have.

**Structural defense versus prompt defense:**

Prompt-level defenses ("do not game the tests," "focus on the goal, not the checks") ask the model to resist its own optimization incentives. Compartmented evaluation removes the optimization target: the builder cannot game what it cannot see. This is a structural defense, not a prompt-engineering defense, and structural defenses are more reliable because they do not depend on model cooperation.

## Implementation in this repo

### What already exists

- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-85 -- separates Generator from Evaluator with distinct information contexts. Generator receives conversation context and produces candidate output; Evaluator receives persisted client state, rubrics, and constraints to validate. The dimension table ([[docs/canonical/generator-evaluator|Generator-Evaluator]]:77-83) shows different primary responsibilities, context needs, model characteristics, success outputs, and failure modes for each role.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:77-83 -- dimension table showing Generator and Evaluator have different primary responsibilities, context needs, model characteristics, success outputs, and failure modes.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:53-58 -- ownership table separating Intent (human), Context (harness), Expectations (human), and Loop execution (harness). Creates craft boundaries but does not seal information between Generator and Evaluator within the Loop.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 -- the Evaluator's verification matrix checks output against explicit constraints, providing independent validation mechanics. The evaluator applies constraint checks without the generator's knowledge, but no mechanism prevents the generator from being told the constraints in advance.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-60 -- separates planning from execution from verification with explicit phase boundaries. Each phase has distinct information, but phases are sequential steps within one agent, not sealed compartments across agents.

### What is missing from the pattern

The classification marks Compartmented Evaluation Architecture as Partial Coverage because the repo has the Generator-Evaluator separation but does not formalize sealed information surfaces ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:206-221).

Missing items:

1. Formal "sealed information surfaces" as a named architectural property. The Generator-Evaluator separation is documented, but the docs do not frame it as compartmentation that prevents information leakage between builder and validator.
2. "Encrypted evals" or hidden failure conditions -- the pattern proposes that failure conditions are compiled into evals the builder cannot see. The repo has no equivalent mechanic.
3. Audit trail of information visibility -- no mechanism records which information each participant in the Generator-Evaluator loop could see at each step.
4. Leakage prevention -- no explicit rule or mechanism prevents a human from copying failure conditions into the builder prompt.
5. The structural defense against reward-hacking as a named concept. The repo's architecture creates the separation but does not name "reward-hacking prevention" as the design intent behind it.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Structural defense against reward-hacking -- builder cannot game what it cannot see | Adds infrastructure complexity: information boundaries, sealed surfaces, audit trails |
| Makes generator and evaluator roles more independent by removing shared visibility of evaluation criteria | Hidden evals can become stale, incomplete, or misaligned with the real outcome |
| Audit trail provides verifiable proof that the builder did not see validator criteria | Validator may miss design intent if failure conditions are too narrow or poorly written |
| Supports future implementation as skills, PR gates, eval harnesses, or exercises about information boundaries | The structure depends on honest routing -- it fails if failure conditions are copied back into the builder prompt |
| Enables more aggressive evaluator specificity -- the validator can use more detailed checks knowing the builder cannot see them | More complex debugging: when the builder fails validation, the human must inspect both surfaces separately |

## Relationship to Other Patterns

- **[[docs/canonical/generator-evaluator|Generator-Evaluator]]** -- the architectural foundation. Generator-Evaluator separates the roles; Compartmented Evaluation Architecture seals the information between them. Without Generator-Evaluator, there is nothing to compartment.
- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- ICE defines craft ownership boundaries; compartmented evaluation defines information boundaries within the Loop execution craft. Both are separation patterns at different layers.
- **[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]** -- the validator's verification mechanics. Compartmented evaluation ensures the builder never sees the constraint verification matrix. Constraint-anchored evaluation defines what the matrix contains.
- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- the five-part intent provides the fields that populate both surfaces: description and constraints go to the builder surface; failure scenarios go to the validator surface. Compartmented evaluation enforces that the split is honored.
- **[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]** -- the Expectations artifact feeds the validator surface. Compartmented evaluation ensures the builder never sees the Expectations that will be used to judge its output.
- **[[docs/canonical/scenario-destination-split|Scenario Destination Split]]** -- the routing rule that sends failure scenarios to the validator surface and success scenarios to Expectations. Compartmented evaluation provides the architectural motivation for the split.
- **[[docs/canonical/constraint-failure-decision-rule|Constraint-Failure Decision Rule]]** -- the classification heuristic that decides what goes on the builder surface versus the validator surface. Compartmented evaluation depends on this classification being correct.
- **[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]** -- phase-gated execution within one agent. Compartmented evaluation extends the phase concept across agents with information boundaries enforced by the harness.

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:150-171 -- extracted pattern: Compartmented Evaluation Architecture
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Classification]]:197-226 -- classification evidence: Partial Coverage, High integration value
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-85 -- Generator-Evaluator architecture with separate information contexts
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:77-83 -- dimension table: different responsibilities, context needs, and failure modes per role
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:53-58 -- craft ownership table with distinct owners per craft
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 -- verification matrix and independent validation mechanics
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-60 -- phase separation with explicit boundaries
