---
title: 'Structured Generation and Constraint Validation Circuit'
type: canonical
aliases: ["structured generation circuit", "circuito geracao estruturada", "constraint validation circuit", "structured output validation"]
tags: ["agentes-orquestracao", "harness", "evals"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]"]
sources: ["[[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction: Harness Evolution]]"]
---

# Structured Generation and Constraint Validation Circuit

**Type:** Canonical Pattern
**Status:** Active
**Source:** docs/articles/harness-evolution-metodos-construcao.md
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Free-form model output cannot safely drive agent actions or customer-facing recommendations because the harness source says Structured Generation exists to force JSON fields such as `recommendation`, `reasoning`, `confidence`, and `risk_flags` before the response reaches the client [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:49-55. JSON shape alone is not enough because the same source names the classic failure: valid JSON can still recommend a product containing an ingredient to which the customer is allergic [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:55.

The concrete KODA failure is a recommendation that looks good on product category, reviews, and price while missing the customer's allergy and vegan constraints; [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] records this as a missed explicit-constraint failure, not a syntax failure [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:21-27. The analysis generalizes the same failure as JSON-only validation producing semantically wrong decisions and says the mitigation is business-rule validation after generation [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction: Harness Evolution]]:121-125.

## Solution

Use one action-safety circuit that treats generation, shape validation, domain-constraint validation, repair or rejection, risk flags, deterministic dispatch, and audit logging as one path rather than separate practices; the extracted pattern defines the components as output schema, generation prompt, domain constraint set, post-generation validator, repair or rejection policy, and audit log [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:128-140.

```text
Model output
  recommendation + reasoning + confidence + risk_flags
        |
        v
+------------------+
| Shape validation |
| schema + fields  |
+------------------+
        |
        v
+------------------------------+
| Domain constraint validation |
| allergy + budget + stock     |
| timing + safety + policy     |
+------------------------------+
        |
        +-------------------+
        |                   |
        v                   v
 Valid action        Invalid or risky action
        |                   |
        v                   v
Deterministic        repair request
dispatch             reject
        |            risk flag
        v            safe fallback
Audit log <----------+
```

Shape validation checks whether the model emitted the required structure, because the harness source defines Structured Generation as JSON with named fields and automatic field validation [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:49-55. Domain constraint validation checks whether the structured candidate is allowed by business, safety, budget, availability, and timing rules, because the extracted pattern lists those constraints as inputs and says they are validated outside the prompt after generation [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:111-119.

The circuit sends valid output to deterministic code because the extracted flow routes valid output after shape and domain validation [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:136-140. The circuit rejects, repairs, flags, or falls back when validation fails because the extracted outputs include rejection, repair request, risk flag, or safe next action when constraints fail [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:116-119.

## Implementation in this repo

### What already exists

- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] covers the JSON-to-handler side of the circuit: the model emits JSON, application code reads it, a switch statement or router dispatches to a deterministic handler, and the handler returns a result [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:20-29.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] also names auditability and circuit breaking as dispatch properties, including logging `{tool, args, handler, result}` and rejecting calls that exceed budget, time, or rate limits [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:59-66.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] covers the constraint side of the circuit: evaluations must use explicit constraints from persisted client state, business rules, and domain knowledge, and must produce a verification matrix plus an approval verdict only when all constraints pass [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-50.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]] covers the independent review role that can reject unsafe output with feedback, and it describes the Evaluator as reading persisted client state, applying rubrics and business rules, and returning approve or reject feedback [[docs/canonical/generator-evaluator|Generator-Evaluator]]:29-31.
- The harness analysis already identifies Structured Generation, Guardrails & Constraints, and Generator/Evaluator as separate patterns: structured JSON reduces ambiguous recommendation errors, constraints are validated in code after generation, and an Evaluator scores recommendations against a rubric before approval [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction: Harness Evolution]]:57-75.

### What is missing

- No active canonical doc listed in the system of record names this pattern as a single circuit that unifies shape validation, domain-constraint validation, repair or rejection policy, risk flags, and audit logging; the active list includes deterministic dispatch, generator-evaluator, and constraint-anchored evaluation as separate documents [[docs/system-of-record|System of Record]]:124-160.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] explains JSON plus deterministic code, but its missing-items section is about naming the dispatch reframe, testing dispatch handlers, and audit logging rather than validating domain constraints before action [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:78-86.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] explains verification matrices and constraint-level approval, but its missing-items section focuses on formalizing constraint anchoring, state-to-criteria mapping, matrix format, granularity, and evolution rather than the full structured-generation-to-dispatch action circuit [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:72-78.
- The extracted pattern requires audit-ready evidence that both shape and domain rules were checked, but no cited canonical document currently defines that evidence as the required output of one unified circuit [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:116-119.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Deterministic code can route model output without parsing prose because the pattern separates structured action schema from dispatch [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:111-123. | Schemas cannot capture every semantic failure mode, so validators and evaluators still need explicit domain rules [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:124-127. |
| Shape and domain checks are separated, which prevents valid JSON from being mistaken for a safe recommendation [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction: Harness Evolution]]:121-125. | Constraint lists must evolve as product rules and available tools evolve [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:124-127. |
| Guardrails become code-enforced after generation rather than prompt-only instructions [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:71-74. | Broad constraints can create false positives and block valid actions [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:124-127. |
| Audit evidence can show that both syntax and domain rules were checked before dispatch [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:116-119. | The circuit adds validation and logging work around each candidate action [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:128-140. |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] for the JSON-to-handler routing step, because that pattern defines tool use as model-emitted JSON followed by deterministic application dispatch [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:20-36.
- **Validated by:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] for the verification matrix and all-constraints-pass approval rule [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:31-50.
- **Complements:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] because an Evaluator can apply persisted client state, rubrics, and business rules before approval or rejection feedback returns to the Generator [[docs/canonical/generator-evaluator|Generator-Evaluator]]:29-31.

## References

- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:49-55 — Structured Generation fields and JSON-only business-rule failure.
- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:71-74 — constraints defined before generation and validated in code after generation.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction: Harness Evolution]]:57-75 — Structured Generation, Guardrails & Constraints, and Generator/Evaluator extraction.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction: Harness Evolution]]:121-128 — failure patterns for JSON-only validation, prompt-only guardrails, and self-evaluation bias.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Harness Evolution Patterns]]:109-140 — extracted Structured Generation and Constraint Validation Circuit definition.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:20-57 — structured JSON-to-handler routing mechanism.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-89 — explicit constraint validation, verification matrix, and tradeoffs.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:29-31 — independent evaluator role applying persisted state, rubrics, and business rules.
