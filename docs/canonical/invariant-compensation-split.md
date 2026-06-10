---
title: 'Invariant-Compensation Split'
type: canonical
aliases: ["invariant compensation", "compensacao invariante", "separacao invariante-compensacao", "invariant split"]
tags: ["agentes-orquestracao", "harness", "governanca"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]"]
sources: ["[[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction: Harness Evolution]]"]
---

# Invariant-Compensation Split

**Type:** Canonical Pattern
**Status:** Active
**Source:** docs/articles/harness-evolution-metodos-construcao.md
**Classification:** Missing
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Harness components often enter during BUILD because the current model has a concrete weakness. In the source case, the original Context Loader existed because a 32K-token model lost attention after 40 minutes; after a newer model held 98% accuracy at 100K tokens, that same component still cost 450ms, 1200 tokens, and 3 maintenance hours per month while preventing only 12 errors in 145K turns [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:15-17.

Without this pattern, teams make one of two opposite mistakes. They remove safeguards that are permanent domain controls, such as customer-safety validation, irreversible-decision checkpoints, availability fallback, external evaluation, or state persistence [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:161-171. Or they keep compensations that only made sense for an older model, turning the harness into bug surface, latency, token cost, complexity, and maintenance burden [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:117-125.

The concrete failure is governance by intuition: "the model improved" becomes a reason to delete controls that should never depend on model quality, while "the harness works" becomes a reason to keep obsolete compensations that no longer change outcomes.

## Solution

Classify every harness control as either a **domain invariant** or a **model-specific compensation** before simplification or removal. The extracted pattern defines the input as a component inventory, the failure each component prevents, domain risk classes, current model capability, incident history, and cost/false-positive metrics; its output is a keep, simplify, measure, or removal-candidate decision with explicit rationale [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:171-191.

```
                 +----------------------------+
                 | Harness component inventory |
                 +--------------+-------------+
                                |
                                v
                 +----------------------------+
                 | What failure does it stop? |
                 +--------------+-------------+
                                |
                  +-------------+-------------+
                  |                           |
                  v                           v
      +----------------------+     +--------------------------+
      | Permanent domain risk |     | Model/runtime weakness   |
      | safety, irreversible  |     | context, budget, latency |
      | availability, eval,   |     | older capability gap     |
      | state persistence     |     +------------+-------------+
      +----------+-----------+                  |
                 |                              v
                 v                +----------------------------+
          KEEP AS INVARIANT       | Measure marginal value     |
                                  | cost, false positives, ROI |
                                  +-------------+--------------+
                                                |
                                                v
                                      SIMPLIFY / REMOVE
```

Core rules:

| Rule | Decision test | Default action |
|---|---|---|
| Name the prevented failure | If nobody can state the failure, the component cannot be defended | Measure or remove after validation |
| Separate domain risk from model weakness | If the failure still exists with a better model, it is an invariant candidate | Keep and test as a permanent control |
| Count false positives as cost | If the component blocks valid work more than it prevents real failures, it may be compensation drag | Simplify or shadow-test removal |
| Use evidence before removal | If impact is uncertain, isolate one component with shadow/canary evidence | Measure before changing multiple controls |
| Record the rationale | If future maintainers cannot tell why it exists, governance has failed | Add decision log or archive note |

Before/after:

| Before | After |
|---|---|
| "The new model is better, so remove guards." | "Remove only controls classified as low-value compensations; keep domain invariants." |
| "This component works, so keep it." | "Keep it only if it prevents a current domain risk or shows positive measured value." |
| "Simplification is cleanup." | "Simplification is a governed decision with evidence, rollback, and rationale." |

## Implementation in this repo

### What already exists

- [[docs/system-of-record|System of Record]] gives canonical documentation precedence: accepted ADRs first, then active canonical docs, then validated evidence, then analysis and archive material [[docs/system-of-record|System of Record]]:14-21.
- [[docs/system-of-record|System of Record]] lists the active canonical pattern table that the classification used as the canonical review scope [[docs/system-of-record|System of Record]]:124-159.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] contains adjacent harness-evolution questions about what failure a component prevents, how often it prevents that failure, its token, latency, and maintenance cost, replay/A-B proof, and rollback speed [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:57-60.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] already protects stable harness instructions during context reduction by separating reducible payload from the role, policy, tool contracts, safety boundaries, response format, and evaluation behavior [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:20-41.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] already decomposes an agent loop into Prompt, Context Builder, Switch Statement, and Loop with explicit intervention points [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:29-75.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]] already treats external evaluation as an independent gate rather than self-approval by the generator [[docs/canonical/generator-evaluator|Generator-Evaluator]]:21-31.
- [[docs/canonical/external-state-persistence|External State Persistence]] already classifies durable facts such as allergies, preferences, constraints, commitments, and critical history as state that should survive context limits [[docs/canonical/external-state-persistence|External State Persistence]]:59-65.

### What is missing

1. No active canonical doc classifies harness controls as permanent domain invariants versus temporary model-specific compensations; the classification marks Invariant-Compensation Split as Missing after reading the system of record and all 27 existing canonical docs [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/classification|Classification]]:143-158.
2. Adjacent canonical docs cover cost, removal safety, stable prompts, and eval metadata, but the classification says those are non-equivalent because they do not define invariant/compensation classification [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/classification|Classification]]:149-156.
3. The repository lacked a canonical component-inventory contract with failure-prevention rationale, domain-invariant criteria, compensation criteria, false-positive/cost metrics, and keep/simplify/measure/remove decisions [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/classification|Classification]]:156-158.
4. The source analysis names permanent invariants and quarterly review behavior, but before this document that distinction lived in analysis/article material rather than Level 2 canonical documentation [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction]]:47-49 [[docs/system-of-record|System of Record]]:14-21.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents essential domain controls from being removed merely because model capability improved | Requires product and domain judgment, not only telemetry |
| Makes obsolete compensation weight visible as latency, token, false-positive, and maintenance cost | Early systems may not have enough incident history to classify confidently |
| Turns simplification into a governed keep/simplify/measure/remove decision | Adds review work to harness evolution cycles |
| Preserves institutional rationale for why a control is permanent or temporary | Misclassification can create high-severity regressions if an invariant is treated as compensation |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]], because the component inventory is only actionable when Prompt, Context Builder, Switch Statement, and Loop controls are visible intervention points [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:29-75.
- **Validated by:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]], because harness evolution decisions need observed pain, evidence, current capability, selected next step, owner, operating cost, and review date [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:51-60.
- **Complements:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]], because stable prompt preservation is one example of an invariant-like harness contract that must not be removed by generic context reduction [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41.
- **Complements:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] and [[docs/canonical/external-state-persistence|External State Persistence]], because the source analysis identifies external evaluation and state persistence as permanent invariants rather than temporary model compensations [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction]]:47-49.

## References

- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:15-17 - Context Loader cost and model-capability change scenario.
- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:117-125 - harness ossification as bug surface, latency, token cost, complexity, and maintenance.
- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:161-171 - permanent architectural invariants and quarterly-review boundary.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction]]:47-49 - permanent-invariant model extracted from the source article.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction]]:134-140 - synthesis: smallest measured harness that preserves invariants.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:171-191 - Invariant-Compensation Split definition, inputs, outputs, benefits, and limitations.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns.yaml|Pattern Extraction YAML]]:242-273 - structured component list and flow for this pattern.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/classification|Classification]]:143-158 - Missing classification and NOT_FOUND confirmation.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/classification.yaml|Classification YAML]]:197-217 - structured Missing classification and nearest adjacent evidence.
- [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]:57-60 - adjacent harness-evolution and rollback questions.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41 - adjacent stable prompt preservation during context reduction.
