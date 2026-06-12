---
title: 'Tested Degradation Ladder'
type: canonical
aliases: ["degradation ladder", "escada de degradacao", "fallback ladder", "resilience ladder"]
tags: ["agentes-orquestracao", "harness", "production"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]"]
sources: ["[[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction: Harness Evolution]]"]
---

# Tested Degradation Ladder

**Type:** Canonical Pattern
**Status:** Active
**Source:** docs/articles/harness-evolution-metodos-construcao.md
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

A runtime failure should not turn a long-running agent into a dead session or an automatic manual ticket. The source article defines the failure mode directly: without a fallback strategy, every error becomes a manual ticket, and a fallback that is never tested in production is broken when it is needed [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:65-69. The extracted pattern names the same problem as runtime failures becoming dead sessions or manual tickets when retry, safe fallback, and human escalation are not designed and exercised [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:208-219.

A concrete scenario is a tool call that fails, leaves raw error context behind, and gives the agent no ordered next step. [[docs/canonical/error-context-hygiene|Error Context Hygiene]] describes how raw errors and stack traces pollute context, bias the model toward error loops, and keep stale failure state visible after later progress [[docs/canonical/error-context-hygiene|Error Context Hygiene]]:20-27. Without a ladder, the session either retries blindly, emits an unsafe answer, dies, or creates a human ticket without enough summarized context to continue the workflow [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:208-240.

## Solution

Define a tested degradation ladder: an ordered contract that starts at failure classification, allows bounded repair only when recovery is plausible, falls back to a conservative safe action or hold when automation is unsafe, escalates to a human with summarized context when automated recovery is insufficient, logs the outcome, and tests each rung before production reliance [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:229-240.

```text
[Runtime failure observed]
          |
          v
+-------------------------------+
| 1. Classify failure           |
|    retryable / unsafe / hold  |
+-------------------------------+
          |
          v
+-------------------------------+
| 2. Retry with repair          |
|    bounded, summarized error  |
+-------------------------------+
          |
          v
+-------------------------------+
| 3. Safe fallback or hold      |
|    conservative action only   |
+-------------------------------+
          |
          v
+-------------------------------+
| 4. Human escalation           |
|    context to continue work   |
+-------------------------------+
          |
          v
+-------------------------------+
| 5. Outcome log + rung tests   |
|    regression evidence        |
+-------------------------------+
```

The retry rung should use the existing error-hygiene shape: summarize the failed call into one actionable line, inject the hint with attempt count and retry limit, clear pending errors on success, and stop at the retry bound [[docs/canonical/error-context-hygiene|Error Context Hygiene]]:93-106. The fallback and escalation rungs should be explicit loop outcomes, because an owned loop already names `break`, `summarize`, `LM-as-judge`, `human approval gate`, and `force terminate` as intervention points [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75. The final rung must turn real failures into durable eval or regression coverage, because production failures should become regression cases with trace, state, expected behavior, failure class, tier assignment, and links back to the incident or PR [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40.

## Implementation in this repo

### What already exists

- [[docs/canonical/error-context-hygiene|Error Context Hygiene]] already defines bounded retry integration with `max_retries`, one-line error summaries, context injection by attempt, success detection, and pending-error cleanup [[docs/canonical/error-context-hygiene|Error Context Hygiene]]:93-106.
- [[docs/canonical/error-context-hygiene|Error Context Hygiene]] also records that the repo already has infrastructure-level fallback mechanisms such as `try/catch`, fail-open behavior, Redis-to-DB fallback, and non-blocking `.catch()` behavior [[docs/canonical/error-context-hygiene|Error Context Hygiene]]:118-125.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] already names the loop intervention points that a degradation ladder needs: break, summarize, LM-as-judge, human approval gate, and force terminate [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75.
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] already defines aggregation outcomes that include pass, fail, retry, needs-human, and needs-rubric-update, and it routes high-variance cases to human review or rubric clarification [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]:30-47.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] already defines fast, medium, and deep eval tiers with runtime, cost, flakiness, trigger, threshold, reporting, owner, and escalation metadata [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-50.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] already makes production failures durable regression cases and assigns them to the correct eval tier [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40.
- The source analysis already captures the domain rule that retry with a new prompt, safe recommendation fallback, and human escalation are the expected escalation strategy, and that untested fallback is a classic failure [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction: Harness Evolution]]:65-67.

### What is missing

- A named ladder contract that orders the rungs from failure classification through retry, safe fallback or hold, human escalation, outcome logging, and rung tests; the extracted pattern lists these components and flow, but they are not yet represented as a single canonical contract [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:208-240.
- A failure classifier that decides retry eligibility before automation acts; the current retry coverage shows a loop with `max_retries`, but it does not define a classifier for retryable, unsafe, hold, or escalate outcomes [[docs/canonical/error-context-hygiene|Error Context Hygiene]]:93-106.
- A fallback or hold policy that specifies which conservative action is safe when retry is unsafe or exhausted; the article names safe recommendation fallback and human escalation, but it does not define the ordered ladder contract [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:65-69.
- An outcome log schema for the ladder itself; the production flywheel captures failures into regression cases, but the ladder still needs a per-rung record of classification, attempted repair, fallback or hold decision, escalation route, and final outcome [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:32-40.
- A test requirement for each rung before relying on it in production; eval tiers define where tests can run, and the extracted ladder flow explicitly requires testing each rung before production reliance [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-50 [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:235-240.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Keeps agent workflows operational when tools or model calls fail [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:220-223 | Can hide root causes if fallback success is treated as full recovery [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:224-227 |
| Reduces manual tickets for recoverable failures [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:65-69 | Human escalation adds latency and operational dependency [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:224-227 |
| Prevents untested fallback logic from failing when needed [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:65-69 | Safe fallbacks must be domain-specific to avoid misleading users [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:224-227 |
| Converts ladder failures into future regression evidence [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40 | Adds eval-tier ownership, runtime, cost, and reporting metadata for each rung test [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:38-50 |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/error-context-hygiene|Error Context Hygiene]], because retry with repair needs summarized failures, retry bounds, success detection, and error cleanup [[docs/canonical/error-context-hygiene|Error Context Hygiene]]:93-106.
- **Depends on:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]], because degradation requires explicit loop intervention points for break, summarize, human approval, and force termination [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75.
- **Validated by:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]], because each rung test needs a declared tier, trigger, threshold, reporting format, owner, and escalation policy [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-50.
- **Validated by:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]], because escaped ladder failures should become durable regression cases with trace, expected behavior, failure class, and tier assignment [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40.
- **Complements:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]], because council aggregation can route ambiguous eval outcomes to retry, needs-human, or rubric clarification [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]:30-47.

## References

- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:65-69 - source fallback and retry rule, including retry with new prompt, safe fallback, human escalation, and the untested-fallback failure.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction: Harness Evolution]]:65-67 - extracted fallback and retry mechanism from the source article.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:208-240 - extracted Tested Degradation Ladder problem, components, benefits, limitations, and flow.
- [[docs/canonical/error-context-hygiene|Error Context Hygiene]]:93-106 - bounded retry loop integration with summarized errors and cleanup on success.
- [[docs/canonical/error-context-hygiene|Error Context Hygiene]]:118-125 - existing infrastructure fallback mechanisms and context-layer gap.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75 - loop controls for break, summarize, LM-as-judge, human approval gate, and force terminate.
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]:30-47 - evaluation aggregation outcomes including retry and needs-human routing.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:26-50 - eval tier metadata and escalation policy requirements.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-40 - durable regression flywheel for production failures.
