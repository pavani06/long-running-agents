---
title: "Split-Brain Planning Review"
type: canonical
tags: ["agentes-orquestracao", "evals", "governanca"]
aliases: ["dual-rubric planning review", "engineering and CEO review", "split-brain review"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/classification|Stanford CS153 Classification]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/patterns|Stanford CS153 Patterns]]"]
sources: ["[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/patterns|Agentic Patterns from Stanford CS153 AI Native Company]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/classification|Classification: Stanford CS153 AI Native Company Patterns]]"]
---
# Split-Brain Planning Review

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/
**Classification:** Partial Coverage, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

A single planning reviewer can collapse two different questions into one blended judgment: "is this plan technically sound?" and "is this plan pointed at the strongest destination?" When those questions share one reviewer role, engineering caution can flatten ambition, while product ambition can ignore maintainability, validation, or production risk.

Long-running agent work needs both checks. Plans must be shippable enough for agents to execute safely, but high-impact roadmaps also need strategic pressure toward a better target state than the first workable implementation.

## Solution

Run planning review as two deliberately separate reviewer roles before execution begins.

| Reviewer | Primary question | Review surface | Output |
|---|---|---|---|
| Engineering reviewer | Can this be implemented, validated, maintained, and rolled back safely? | Scope, dependencies, tests, eval tiers, migration risk, observability, failure modes | Engineering blockers, required gates, simplifications, risk controls |
| Product or CEO-destination reviewer | Is this the right destination and is the ambition high enough? | User outcome, 10x target state, strategic sequencing, wedge choice, roadmap leverage | Directional objections, stronger target state, staged roadmap, ambition upgrades |

The two reviews should not negotiate with each other during first pass. Each reviewer applies its own rubric independently. The planner or orchestrator then reconciles the outputs into a revised plan with explicit decisions:

1. Accept engineering blockers before execution when they affect safety, correctness, or reversibility.
2. Preserve product-destination feedback as roadmap pressure instead of letting it silently disappear into scope cuts.
3. Split execution into stages when the 10x destination is correct but the first step needs a smaller validated wedge.
4. Record disagreements, accepted tradeoffs, and deferred ambition so later agents understand why the plan took its shape.
5. Use this review only for high-impact roadmaps, ambiguous product bets, or major agent-system changes, not routine issue execution.

## Implementation in this repo

### What already exists

The repo already separates planning, execution, generation, and evaluation:

- Planning/execution separation is taught as Planner and Executor phases to avoid collapse between strategy and implementation in [[curriculum/05-core-concepts/02-planning-execution-separation|Planning Execution Separation]]:47-54.
- Planner, Generator, and Evaluator are presented as separate responsibilities in reliable multi-agent systems in [[curriculum/05-core-concepts/02-planning-execution-separation|Planning Execution Separation]]:60-72.
- Generator/Evaluator separation states that one role creates and another judges so the system proves it is right in [[curriculum/05-core-concepts/03-generator-evaluator-pattern|Generator Evaluator Pattern]]:151-153.
- The issue refinement skill decomposes high-level issues into executable sub-issues with dependency relationships in [[.opencode/skills/refine-issue/SKILL|refine-issue skill]]:8-21.
- The issue review skill provides validation and second-agent review before merge in [[.opencode/skills/issue-review/SKILL|issue-review skill]]:12-15.

### What is missing

The Partial Coverage gap is the explicit split between engineering-quality review and product or CEO-destination review. The classification found no canonical doc, curriculum material, or skill that names Split-Brain Planning Review or defines Stanford-specific CEO-review and 10x-ambition mechanics outside the current analysis in [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/classification|classification]]:93-107.

Missing implementation details:

1. Separate planning-review rubrics for engineering quality and product destination.
2. A reconciliation rule for conflicting reviewer output.
3. A trigger policy that reserves the extra review cost for high-impact roadmaps.
4. A durable record of accepted ambition, deferred ambition, and engineering blockers.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps implementation review from suppressing strategic ambition | Adds reviewer latency before execution |
| Keeps product ambition from bypassing validation and production risk | Requires an orchestrator or human to reconcile conflicting feedback |
| Produces clearer plans because each reviewer has one job | Rubrics must stay distinct or the split becomes theater |
| Helps long-running agents preserve roadmap intent across handoffs | Too heavy for routine bug fixes or mechanical documentation updates |

## Relationship to Other Patterns

- **Builds on:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]], because planning review is an intervention point before the loop spends execution budget.
- **Complements:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]], which reviews eval-sensitive changes at PR time while this pattern reviews the plan before execution.
- **Uses:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] when the engineering reviewer decides which evidence tier the plan must produce.
- **Depends on:** [[curriculum/05-core-concepts/02-planning-execution-separation|Planning Execution Separation]] for the base separation between planner and executor.
- **Comes from:** [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/patterns|Stanford CS153 Patterns]]:119-138 and its Partial Coverage classification in [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/classification|classification]]:93-107.

## References

- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/patterns|patterns]]:119-138 - extracted pattern definition.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/classification|classification]]:93-107 - Partial Coverage classification and missing CEO-review mechanics.
- [[curriculum/05-core-concepts/02-planning-execution-separation|Planning Execution Separation]]:47-54 - existing Planner and Executor separation.
- [[curriculum/05-core-concepts/02-planning-execution-separation|Planning Execution Separation]]:60-72 - Planner, Generator, and Evaluator responsibility split.
- [[curriculum/05-core-concepts/03-generator-evaluator-pattern|Generator Evaluator Pattern]]:151-153 - creator/judge separation.
- [[.opencode/skills/refine-issue/SKILL|refine-issue skill]]:8-21 - existing issue decomposition workflow.
- [[.opencode/skills/issue-review/SKILL|issue-review skill]]:12-15 - existing second-agent review gate.

---

*Created: 2026-06-10 | From: Stanford CS153 pattern classification | Precedence: canonical*
