---
title: "Generator-Evaluator"
type: canonical
aliases: ["generator evaluator", "two-agent review", "avaliador externo", "evaluator pattern"]
tags: ["agentes-orquestracao", "evals"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]"]
sources: ["[[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]"]
---

# Generator-Evaluator

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]
**Classification:** Partial Coverage — 12+ eval infrastructure docs exist, no unified Generator-Evaluator architecture doc
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Agents evaluating their own output suffer from confirmation bias: they search for evidence confirming the answer they already generated instead of evidence that would refute it. In the KODA scenario, KODA recommends a whey protein product because the client asked about whey protein, the product has strong reviews, and it is cheap; when KODA self-evaluates, it checks those same confirming facts and marks the recommendation as acceptable [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:210-221.

The missed constraints are the real failure: the client said they are allergic to whey, asked for vegan options, and still wanted quality within budget [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:223-227. The structural root cause is that the same context and perspective that generated the response also evaluates it, creating a closed validation loop: KODA is invested in its own answer, searches for confirming evidence, and has no external perspective [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:229-232.

The quantified gap is large enough to be a production risk. The source frames a 15% real error rate, with self-evaluation detecting 3% and a human or external evaluator detecting 14%, leaving an 11% silent failure rate [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:237-243. The analysis generalizes this as self-evaluation detecting about 3% of real errors, external evaluation detecting about 14%, and a 10-12 percentage-point silent failure gap [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]:18.

## Solution

Separate generation from evaluation into two distinct agents. The Generator is creative and user-facing: it understands the user, works within a tight conversation-focused context window, and produces candidate responses. The Evaluator is impartial and constraint-facing: it receives the candidate output, reads persisted client state, applies quality rubrics and business rules, and returns an approve or reject verdict with specific feedback. The curriculum states the external evaluator is not invested in the generated answer and can therefore be critical [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:406-416.

```
┌──────────────────────────────────────────────────────────┐
│ CLIENTE entra em conversa com KODA                       │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────┐
        │ GENERATOR (KODA)         │
        │ ───────────────────────  │
        │ Tarefas:                 │
        │ • Entender cliente       │
        │ • Gerar recomendação     │
        │ • Processar pedido       │
        │                          │
        │ Constraints:             │
        │ • Janela pequena         │
        │ • Foco em criatividade   │
        └──────────────┬───────────┘
                       │
                       ▼ (resultado bruto)
        ┌──────────────────────────┐
        │ EVALUATOR (outro agente) │
        │ ───────────────────────  │
        │ Tarefas:                 │
        │ • Verificar qualidade    │
        │ • Checar constraints     │
        │ • Apontar problemas      │
        │                          │
        │ Recursos:                │
        │ • Acesso a cliente_data  │
        │ • Acesso a rubrics       │
        │ • Avaliação imparcial    │
        └──────────────┬───────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
         ✅ Aprovado         ❌ Rejeitado
         (envia cliente)    (volta para GENERATOR
                            com feedback)
```

The diagram is the curriculum preview of the Generator-Evaluator pattern: Generator produces the raw result, Evaluator verifies quality and constraints using `cliente_data`, rubrics, and impartial review, then either approves delivery or rejects back to the Generator with feedback [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:420-464.

| Dimension | Generator | Evaluator |
|---|---|---|
| Primary responsibility | Understand the client and generate the candidate response | Verify the candidate response against constraints, rubrics, and business rules |
| Context need | Tight window focused on the live conversation and task | Persisted client state, explicit constraints, rubrics, and the raw Generator output |
| Model characteristics | Fast, fluent, creative, good at synthesis | Rigorous, skeptical, consistent, good at finding violations |
| Success output | Candidate response or action plan | Approved verdict, or rejected verdict with concrete feedback |
| Failure mode | Creative but unsafe recommendation | False positive rejection, false negative approval, or under-specified rubric |

Without Generator-Evaluator, one agent tries to understand the user, recommend a product, evaluate quality, remember allergy constraints, and process the order in one blended pass; the curriculum's KODA story shows this leads to a wrong recommendation, missed allergy constraint, reprocessing, and lost trust [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:283-315. With Generator-Evaluator, KODA generates a candidate recommendation, the Evaluator checks it against `cliente_data.json`, verifies vegan, gluten-free, budget, quality, and prior purchase constraints, and only then approves the response to the client [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:487-505.

## Implementation in this repo

### What already exists

- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] provides model diversity as evaluator plurality: it requires evaluators from meaningfully different model families, shared rubrics, independent first passes, aggregation policy, disagreement policy, and calibration loops [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]:30-40.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] provides fast, medium, and deep evaluation tiers with runtime, cost, flakiness, trigger, threshold, reporting, owner, and escalation metadata [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-50.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] requires eval-specific reports for prompt, model, tool, context, memory, scoring, or agent-loop changes and defines baseline/candidate reporting fields plus merge policy [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:26-53.
- [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] anchors evaluation in representative production interactions, traces, tool results, and state snapshots with privacy, labeling, replay, and refresh mechanics [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]:26-52.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] separates reviewer concerns by having independent engineering and product-destination reviewers apply distinct rubrics before reconciliation [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:26-41.
- The system of record lists 24 active canonical patterns and includes the evaluation infrastructure docs, but does not list `generator-evaluator.md` among active canonical documents before this addition [[docs/system-of-record|System of Record]]:124-155.
- The classification for this analysis explicitly says 12+ canonical docs cover evaluation infrastructure, including multi-model evaluation, eval tiers, PR-gated enforcement, spot checks, production sampling, regression flywheels, long-session evals, late-failure suites, eval-to-production correlation, pain-signal progression, workflow automation, and skill promotion [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Classification]]:59-79.

### What is missing

1. No canonical doc that explicitly names and formalizes the Generator-Evaluator two-agent architecture; the classification identifies this as the first Generator-Evaluator gap [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Classification]]:80-83.
2. Existing eval docs focus on evaluation mechanics, not the generator↔evaluator loop with feedback; the classification states the mature eval docs explain how to evaluate rather than the architecture decision itself [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Classification]]:85-86.
3. No explicit contract for what the Generator produces versus what the Evaluator checks; the extracted pattern defines candidate response, binary verdict, and rejection feedback, but the classification says no canonical doc frames this two-agent architecture as a deliberate pattern [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Patterns]]:30-33 [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Classification]]:83.
4. No documented feedback loop mechanism in canonical form; the curriculum diagram shows rejected output returning to the Generator with feedback, while the classification says the generator↔evaluator loop with feedback is not anchored by one canonical doc [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:456-464 [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Classification]]:82.
5. No integration guide showing how state persistence, constraint-anchored evaluation, and generator-evaluator compose; the pattern analysis lists External State Persistence, Generator-Evaluator, and Constraint-Anchored Evaluation as separate extracted patterns, and the summary classifies all four extracted patterns as Partial Coverage candidates for canonicalization [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Patterns]]:8-42 [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Classification]]:114-123.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Impartial evaluation — Evaluator not invested in Generator's response | Minimum 2 LLM calls per turn (Generator + Evaluator) |
| Catches 10-12% more errors than self-evaluation | Additional latency from evaluation step |
| Generator can be creative/exploratory; Evaluator ensures safety | Evaluator can also err (false positives and false negatives) |
| Allows different models: fast/creative Generator, slow/rigorous Evaluator | Shared blind spots if both use same base model |
| Separation of concerns: Generator doesn't need to self-police | Requires explicit quality rubrics — not magic |
| Solves all 3 fundamental problems when combined with state persistence | Rejection loops add latency if Generator needs multiple revisions |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/external-state-persistence|External State Persistence]] (Evaluator reads persisted client constraints), [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] (Evaluator uses explicit constraints as verification criteria)
- **Validated by:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] (model diversity as evaluators), [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] (appropriate evaluation depth per use case), [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] (enforces evaluation in development workflow)
- **Complements:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] (Generator uses P-E-V internally), [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] (independent review before execution), [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] (real-world calibration of Evaluator)

## References

- [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:420-464 — Generator-Evaluator diagram and explanation
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]] — knowledge extraction with silent failure quantification
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Patterns]] — pattern definition
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Classification]] — classification evidence
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — model diversity evaluation
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — eval enforcement on merge
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] — independent review architecture
