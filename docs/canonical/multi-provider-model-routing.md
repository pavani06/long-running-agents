---
title: "Multi-Provider Model Routing with Capacity Resilience"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["agentes-orquestracao", "evals"]
aliases: ["multi-provider routing", "provider fallback", "capacity resilience routing", "provider-agnostic task dispatch"]
relates-to: ["[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]", "[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]]"]
---

# Multi-Provider Model Routing with Capacity Resilience

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Missing (P0)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Single-provider model dependencies create catastrophic failure risk during traffic spikes (Black Friday, Cyber Monday) or provider outages. An agent system that routes every request to the same provider has no resilience — when that provider degrades or fails, the entire system degrades or fails. The failure is architectural, not operational: no amount of retry logic or queue depth can compensate for capacity that does not exist.

In Sierra's case, serving Fortune 20 enterprises with billions of conversations per year means provider availability is a business-continuity concern. A single-provider architecture puts the business at the mercy of one vendor's SLOs, rate limits, and capacity decisions. The solution is not to switch providers at the system level (migration) or the evaluation level (batch comparison), but to route individual tasks to different providers at the turn level — making provider selection a runtime decision, not an architecture decision.

## Solution

Multi-provider model routing operates at task granularity: within a single conversation turn, different subtasks (classification, retrieval, reasoning, response generation) can be dispatched to different providers based on per-task eligible model sets, provisioned capacity, and enterprise constraints. The key architectural insight is that the harness must be provider-agnostic — evals, prompt formats, and task definitions must work across providers so that switching is "pretty simple" (Wedeen's words).

**Key components:**

1. **Per-task eligible model sets**: Each task type maintains a list of models across providers that meet its quality and latency requirements. A classification task might be eligible on Haiku (Anthropic), Flash (Google), and an in-house classifier; a reasoning task might require Opus (Anthropic) or GPT-5 (OpenAI). These sets are maintained as model capabilities evolve.

2. **Provider-agnostic eval infrastructure**: Evals must produce the same pass/fail signal regardless of which provider generated the output. The eval suite is the stable interface — models can be swapped behind it without rewriting test logic. This is the same architecture described in [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] and [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]].

3. **Load simulation and capacity planning**: Sierra runs load simulations against billions of conversations per year to understand which provider capacity allocation survives extreme traffic events. The routing layer provisions capacity across providers based on these simulations, not static allocations.

4. **Per-customer cloud and vendor constraints**: Enterprise customers have cloud region restrictions (data must stay in EU, or must not use provider X). The routing layer respects these constraints at the customer level — a task for Customer A might only route to providers approved for that customer's compliance profile.

**Operational flow:**

1. A conversation turn arrives with multiple subtasks (intent classification, knowledge retrieval, structured data fetch, response generation).
2. For each subtask, the routing layer consults the eligible model set, current provider health, provisioned capacity, and customer-specific constraints.
3. Subtasks are dispatched in parallel to different providers. A classification task might go to Haiku (Anthropic) while a reasoning task goes to Opus (same provider) and a data fetch goes to a lightweight in-house model.
4. If a provider returns degraded results or times out, the routing layer falls back to the next eligible provider for that task type.
5. All subtask outputs are aggregated into the final response. The conversation consumer never sees which provider handled which task.

**Why this isn't just "model switching":** The existing [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] describes batch-level migration (evaluate a new model → decide switch/hold/hybrid → migrate all traffic). Multi-provider routing operates at task granularity within a single turn and is runtime, not migration. The difference is the same as choosing a compute instance per request vs. migrating your whole cluster to a new region.

## Implementation in this repo

### What already exists

- [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] lines 22-25, 62-70: Batch migration pattern for model switching based on eval data. Provider-agnostic eval format and Switch/Hold/Hybrid decision framework.
- [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] lines 28-48: Model-agnostic context format with vendor adapter. Foundational abstraction for provider-independence but no routing logic.

### What is missing

From the classification: "No multi-provider redundancy at task level. No provider fallback mechanism. No load simulation across providers. No per-customer cloud constraint routing."

1. **Task-level multi-provider routing**: No mechanism to dispatch individual subtasks to different providers within a turn.
2. **Provider fallback at task granularity**: [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] handles failure retry but not provider-level fallback.
3. **Per-customer constraint routing**: No concept of customer-specific cloud region or vendor approval lists in the routing layer.
4. **Load simulation across providers**: No infrastructure to simulate traffic allocation across multiple providers under spike conditions.

The repo's focus on coding-agent harnesses (single-session, single-model-per-task) means multi-provider routing has not been architecturally necessary. As the harness matures toward production agent deployment, this pattern becomes relevant when business continuity depends on provider diversity.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Eliminates single-provider lock-in for business continuity | Eval coverage must be comprehensive across all providers — the routing layer is only as reliable as the eval that validates each provider's outputs |
| Handles extreme traffic spikes through multi-provider redundancy at task level | Adds operational overhead: model-specific prompt tuning, rate limit management per provider, quota tracking across multiple vendors |
| Respects enterprise compliance constraints (cloud regions, approved vendors) | Requires customer-specific routing configuration that must be maintained as providers change |
| Model-agnostic harness makes provider switching a runtime decision, not a migration project | Benefits diminish if all providers share common infrastructure (single cloud backend); vendor diversity without infrastructure diversity is false resilience |

## Relationship to Other Patterns

- **Builds on:** [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] — extends batch migration to runtime task-level routing.
- **Requires:** [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] — provider-agnostic context format is prerequisite for task-level routing.
- **Requires:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — model-diverse evaluation validates that provider switching doesn't degrade quality.
- **Complements:** [[docs/canonical/task-routed-model-tiering|Task-Routed Model Tiering]] — model tiering decides *which capability level* per task; multi-provider routing decides *which vendor* for that capability level.
- **Extends:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] — adds provider-level fallback to the existing retry and escalation ladder.

## References

-  lines 46-71 — extracted pattern with inputs, outputs, benefits, limitations.
-  lines 52-61 — Missing classification with evidence of foundational-only coverage.
- [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] lines 22-25, 62-70 — existing batch-level model switching infrastructure.
- [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] lines 28-48 — provider-agnostic context format as foundational abstraction.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
