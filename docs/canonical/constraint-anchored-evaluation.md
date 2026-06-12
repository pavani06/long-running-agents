---
title: "Constraint-Anchored Evaluation"
type: canonical
aliases: ["avaliação ancorada em constraints", "constraint-based evaluation", "objective evaluation", "verifiable evaluation"]
tags: ["evals", "agentes-orquestracao"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill Capability Pipeline]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]"]
sources: ["[[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]"]
---

# Constraint-Anchored Evaluation

**Type:** Canonical Pattern
**Status:** Active
**Source:** curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md
**Classification:** Partial Coverage — constraint-based checking exists implicitly in eval docs, not formalized as named pattern
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Evaluation without explicit constraints is subjective and unreliable. An evaluator asked only "is this good?" applies inconsistent, implicit criteria, favoring what feels plausible over what can be verified. In the KODA product-recommendation scenario, KODA self-evaluates a recommendation by checking that it is whey protein, has good reviews, and is cheap, but misses that the client said they are allergic to whey and asked for vegan because those constraints were not encoded in the evaluation checklist ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:208-227).

The failure compounds because every implicit constraint is a potential silent failure. The same source quantifies that self-evaluation detects 3% of real errors while a human or external evaluator detects 14%, leaving an 11% silent failure gap ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:234-246). The knowledge extraction summarizes the same gap as 10-12 percentage points and identifies the external evaluator's role as verifying output against constraints with access to client data and rubrics ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]:18, [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]:26-31).

External evaluation improves the situation, but it is only as strong as the criteria it receives. A vague evaluator can still approve an unsafe recommendation if the allergy, diet, budget, return-policy, or compatibility constraint was never made explicit.

## Solution

Anchor every evaluation to an explicit, verifiable constraint list. Constraints come from persisted client state such as allergies, preferences, budget, and dietary restrictions; business rules such as return policies, promotion eligibility, and shipping restrictions; and domain knowledge such as product compatibility or legal requirements. The extracted pattern defines those inputs as client constraints, generator output, and business rules, and defines the output as a verification matrix plus an aggregate verdict that approves only when all constraints pass ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:35-42).

The evaluator produces one row per constraint: the constraint, the check performed, the binary pass/fail result, and the violation detail when it fails. The aggregate verdict is `approved` only if every row passes. If any constraint fails, the evaluator reports exactly which constraint was violated and how.

```text
Constraint Store
  client state + business rules + domain knowledge
        |
        v
Evaluator
  candidate output + explicit constraint list
        |
        v
Verification Matrix
  constraint -> check -> pass/fail -> violation detail
        |
        v
Aggregate Verdict
  approved only if all constraints pass
```

| Subjective evaluation | Constraint-anchored evaluation |
|---|---|
| Asks whether the output seems good | Checks each named constraint directly |
| Uses implicit reviewer judgment | Uses explicit pass/fail criteria |
| Produces inconsistent decisions across reviewers | Produces repeatable decisions for the same constraint set |
| Hides why an output was approved | Records the constraint-level reason for approval or rejection |
| Gives vague feedback to the generator | Identifies the exact violated constraint |
| Cannot be audited without rereading the whole case | Leaves a verification matrix that can be inspected later |

## Implementation in this repo

### What already exists

- [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] defines eval cases with `expected_outcome`, `acceptable_tool_behavior`, `baseline`, and `grading_notes`, which already creates concrete criteria instead of free-form judgment ([[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]:30-42).
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] requires PR eval reports to include `thresholds`, `failure_examples`, and `merge_policy`, and its operating steps block merge when thresholds fail unless a waiver is recorded ([[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:30-43, [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:45-53).
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] requires every eval tier to declare threshold, reporting, owner, runtime, cost, flakiness policy, and trigger metadata, making pass/fail policy part of the eval contract ([[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-49).
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] separates engineering and destination reviewers, has each reviewer apply its own rubric independently, and reconciles the outputs through explicit decisions ([[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41).
- [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]] requires compliance tests, trigger evals, smoke evidence, and acceptance gates before a workflow becomes a durable capability ([[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]]:28-42, [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]]:55-66).
- The classification for agent focus problems explicitly identifies these same docs as existing constraint mechanics for expected outcomes, thresholds, independent rubrics, compliance tests, and trigger evals ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:90-110).

### What is missing

1. No canonical doc explicitly names and formalizes Constraint-Anchored Evaluation as the pattern; the classification says existing eval docs mention thresholds and criteria but do not formalize constraint anchoring as the reason evaluation becomes objective ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:104-110).
2. No explicit mapping from External State Persistence constraints to evaluation criteria; the classification calls this out directly, while the pattern source lists persisted constraints such as allergies, budget, and preference as evaluator inputs ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:107, [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:37-40).
3. No formal verification matrix format of `constraint -> check -> pass/fail -> violation detail`; the extracted pattern defines the matrix as an output, but the classification says the repo has not made constraints and acceptance criteria the spine of evaluation ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:39-40, [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:104-110).
4. No guidance on constraint granularity, such as what deserves a hard constraint versus what should remain reviewer judgment; this is part of the missing formalization of constraints, thresholds, negatives, and acceptance criteria as the evaluation spine ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:104-110).
5. No mechanism for constraint evolution as business rules change; the pattern source warns that constraint lists require maintenance as business rules evolve, but the classification does not identify a current canonical mechanism for that evolution ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:41-42, [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:104-110).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Objective verification instead of subjective judgment | Only catches explicitly modeled constraints |
| Actionable feedback: Generator knows exactly what to fix | Implicit/common-sense constraints are missed |
| Auditable: every decision traceable to a specific constraint | Requires ongoing maintenance as business rules evolve |
| Reduces Evaluator false positives through clear pass/fail criteria | Can be overly rigid when a technical violation is contextually acceptable |
| Composable: constraints can come from state persistence, business rules, and domain knowledge | Constraint list can grow large, adding evaluation latency |
| Enables automated evaluation without human judgment per check | Initial constraint modeling requires domain expertise |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/external-state-persistence|External State Persistence]] for constraints stored in persisted client state, and [[docs/canonical/generator-evaluator|Generator-Evaluator]] for the evaluator role that applies constraint-anchored checking.
- **Validated by:** [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] when constraints become expected outcomes, [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] when violations block merge, and [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] when constraint complexity determines eval tier.
- **Complements:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] because independent rubrics are constraint sets, and [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]] because compliance tests are constraint checks.
- **Explains:** [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]] by turning the KODA allergy failure into a missing-constraint failure mode rather than a vague quality issue.

## References

- [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:208-227 — self-evaluation collapse scenario showing implicit constraint failure.
- [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:234-246 — self-evaluation versus external evaluator detection gap.
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]:26-31 — Generator-Evaluator with evaluator verification against constraints.
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:35-42 — extracted Constraint-Anchored Evaluation pattern definition.
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:90-110 — Partial Coverage evidence and missing constraint anchoring.
- [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]:30-42 — expected outcomes, tool constraints, baselines, and grading notes.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:30-53 — PR thresholds, failure examples, merge policy, and blocking behavior.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-49 — tier metadata including thresholds and reporting.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 — independent rubrics and reconciliation rules.
- [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]]:28-42 — compliance tests, trigger evals, smoke execution, and acceptance gates.

---

*Created: 2026-06-10 | From: Agent Focus Problems pattern classification | Precedence: canonical*
