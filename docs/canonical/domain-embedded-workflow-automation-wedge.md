---
title: "Domain-Embedded Workflow Automation Wedge"
type: canonical
tags: ["agentes-orquestracao", "evals", "curriculo-conteudo"]
aliases: ["automation wedge", "embedded workflow discovery", "domain workflow wedge"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]", "[[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|KODA Customer Journey Flows]]"]
sources: ["[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Agentic Patterns from Stanford CS153 AI Native Company]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Classification: Stanford CS153 AI Native Company Patterns]]"]
---
# Domain-Embedded Workflow Automation Wedge

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/
**Classification:** Partial Coverage, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Agent teams often automate the visible surface of a workflow instead of the messy operational work underneath it. A demo can follow the happy path while real operators handle exceptions through phone calls, email, spreadsheets, system-of-record lookups, informal judgment, and hidden handoffs.

A domain-embedded wedge prevents shallow automation. It starts from observed work, identifies the narrow slice where automation can create real leverage, and turns operator decisions and edge cases into agent capabilities, deterministic integrations, and eval cases.

## Solution

Use embedded workflow discovery before choosing the first automation slice.

Discovery artifacts:

| Artifact | Requirement |
|---|---|
| Shadowing notes | Observed operator actions, tools, handoffs, delays, exceptions, and workarounds |
| Decision inventory | Judgment calls, deterministic checks, escalation rules, and owner approvals |
| System map | Systems of record, APIs, spreadsheets, inboxes, chat channels, and manual copy-paste paths |
| Edge-case catalog | Rare but costly failures, ambiguous customer states, missing data, policy exceptions, and recovery steps |
| Automation wedge | Small workflow slice with high pain, bounded scope, available data, clear owner, and testable outcome |
| Domain eval seeds | Cases derived from observed work, including successful paths and exception paths |

Wedge selection rules:

1. Choose a workflow slice that operators already perform repeatedly and painfully.
2. Prefer slices with clear before/after outcome evidence, not merely impressive model behavior.
3. Separate deterministic system integration from model-owned judgment before automation.
4. Convert observed edge cases into eval fixtures before expanding the automation surface.
5. Preserve operator review for cases where authority, risk, or missing data makes full automation unsafe.
6. Revisit the wedge after deployment using production traces, operator feedback, and customer outcomes.

## Implementation in this repo

### What already exists

The repo already contains strong domain workflow and eval material:

- KODA Awareness state is modeled with trigger, goal, guard, and output in [[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|KODA Customer Journey Flows]]:36-46.
- KODA Consideration is decomposed into discovery, filtering, comparison, validation, and guard conditions based on customer constraints in [[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|KODA Customer Journey Flows]]:76-110.
- The KODA order-processing case study describes a real multi-step order-processing pain with six dependent stages and costly errors from a single agent in [[curriculum/09-case-studies/04-koda-order-processing|KODA Order Processing Case Study]]:18-28.
- The same case study turns each processing step into sprint contracts with Generator/Evaluator responsibilities, tests, and approval criteria in [[curriculum/09-case-studies/04-koda-order-processing|KODA Order Processing Case Study]]:31-45.
- KODA evaluation rubrics tie workflow quality to WhatsApp history, preferences, restrictions, budget, tone, commercial pressure, and business validation in [[curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda|KODA Evaluation Rubrics]]:24-45.

### What is missing

The Partial Coverage gap is the discovery wedge itself. The repo has domain workflows and KODA-specific evals, but the classification found no formal pattern for shadowing messy customer work, extracting operator decisions and edge cases, or deciding which workflow slice to automate first from observed operations outside the current Stanford pattern file in [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|classification]]:173-187.

Missing implementation details:

1. A shadowing-note template for observed customer or operator work.
2. A decision-inventory format that separates judgment, deterministic checks, and escalation authority.
3. A wedge-selection rubric for first automation slices.
4. A requirement that observed edge cases become domain eval seeds before broad rollout.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Grounds agent automation in real operational work | Requires discovery time before implementation |
| Reveals hidden handoffs and failure modes before automation | Can overfit to one operator or customer process |
| Produces better eval cases because they come from observed edge cases | Shadowing notes need privacy and consent discipline |
| Helps choose a narrow, high-leverage automation wedge | The first wedge may be less impressive than a broad demo |

## Relationship to Other Patterns

- **Feeds:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] by turning observed work and later production traces into representative eval cases.
- **Feeds:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] when edge cases or failed automations become permanent regression cases.
- **Uses:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] when wedge selection needs both engineering feasibility and product-destination pressure.
- **Builds on:** [[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|KODA Customer Journey Flows]] and [[curriculum/09-case-studies/04-koda-order-processing|KODA Order Processing Case Study]] for existing domain workflow decomposition.
- **Comes from:** [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]]:224-243 and its Partial Coverage classification in [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|classification]]:173-187.

## References

- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|patterns]]:224-243 - extracted pattern definition.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|classification]]:173-187 - Partial Coverage classification and missing shadowing/wedge mechanics.
- [[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|KODA Customer Journey Flows]]:36-46 - existing Awareness workflow modeling.
- [[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|KODA Customer Journey Flows]]:76-110 - existing Consideration workflow decomposition.
- [[curriculum/09-case-studies/04-koda-order-processing|KODA Order Processing Case Study]]:18-28 - existing multi-step operational pain.
- [[curriculum/09-case-studies/04-koda-order-processing|KODA Order Processing Case Study]]:31-45 - existing sprint contracts from workflow steps.
- [[curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda|KODA Evaluation Rubrics]]:24-45 - existing domain-specific eval criteria.

---

*Created: 2026-06-10 | From: Stanford CS153 pattern classification | Precedence: canonical*
