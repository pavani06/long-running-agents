---
title: "Behavioral Eval Path Analysis"
type: canonical
aliases: ["behavioral eval", "path analysis", "tool call evaluation", "execution path scoring", "Layer 3 behavioral eval"]
tags: ["evals", "production", "tracing", "observability"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]"]
sources: []
---
# Behavioral Eval Path Analysis

**Type:** canonical
**Status:** active
**Source:** The Production AI Playbook (Bhaumik, Databricks)
**Classification:** Missing (P0, High)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

An agent can return the correct answer ("your balance is R$ 1.234,56") while executing a wasteful path: three redundant database calls (same query, identical parameters), two unnecessary external API calls to overlapping services, and a tool call loop that retried a non-idempotent operation three times before returning the cached result from attempt one. Semantic evaluation (Layer 2) gives this query a perfect score — the answer is correct. But at 20,000 queries per month, the behavioral waste multiplies into unsustainable infrastructure cost and latency.

This is the "right answer, wrong path" failure mode. It is invisible to:
- **Layer 1 (Deterministic):** The output format is valid.
- **Layer 2 (Semantic):** The answer is correct and well-grounded.
- **Logs and APM:** Latency is within SLO; no errors were thrown.
- **Demo evaluations:** Quick spot-check sets never surface path inefficiency at scale.

Without behavioral evaluation, the agent's per-query cost profile is a black box until the monthly infrastructure bill arrives — and by then, thousands of wasteful queries have already consumed budget.

## Solution

Behavioral Eval Path Analysis is **Layer 3** of the [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]. It evaluates HOW the agent arrived at the answer — the execution path — not just what the answer was. It consumes the full execution trace (ordered tool calls with timestamps, parameters, and costs) and produces behavioral scores that quantify path quality.

### Prerequisites

Before behavioral eval can operate, the tracing infrastructure must capture:

- Every tool call with: tool name, parameters (hashed or anonymized for privacy), timestamp, duration, success/failure
- Every external API call with: endpoint, parameters, cost (if known), duration
- Every LLM call with: model, tokens consumed, estimated cost
- The full ordered sequence of calls, preserving causal ordering

The repo's trace instrumentation (`docs/canonical/trace-instrumentation.md`) provides this data foundation via `tracer.ts`, `task-wrapper.sh`, and `telemetry.db`.

### Behavioral Scores

For each agent query execution, compute four behavioral scores from the execution trace:

#### 1. Redundancy Score

**What it measures:** How many unnecessary repeated calls the agent made to the same tool with semantically equivalent parameters.

**Algorithm:**
1. Group consecutive calls to the same tool.
2. Compare parameters: if the next call to the same tool has identical or semantically equivalent parameters (e.g., same SQL query with the same bind values, same API endpoint with the same request body), flag as redundant.
3. Score: `redundant_calls / total_calls`. A score of 0 means no redundant calls; a score of 0.5 means half the tool calls were unnecessary repeats.

**Example:** Agent calls `get_user_balance(user_id=42)` → receives balance → calls `get_user_balance(user_id=42)` again with identical parameters. Redundancy score increases. This commonly occurs when the agent "double-checks" a value it already retrieved.

#### 2. Loop Detection Flag

**What it measures:** Whether the tool call sequence forms a semantic cycle — the agent enters a loop where calls A → B → A (or longer cycles) with the same semantic intent.

**Algorithm:**
1. Build a directed graph of consecutive tool calls.
2. Detect cycles of length ≤ N (e.g., N=5 for practical detection).
3. For each detected cycle, check if the parameters are semantically equivalent between cycle iterations.
4. Flag as loop if a cycle repeats ≥ 3 times with equivalent intent.

**Example:** `search_knowledge_base("refund policy")` → `get_order_details(order_id)` → `search_knowledge_base("refund policy")` — the agent oscillates between search and order retrieval without making progress. This is a semantic loop: the same information-seeking intent repeats without resolution.

#### 3. Path Efficiency Ratio

**What it measures:** The ratio of necessary tool calls to total tool calls for the query category.

**Algorithm:**
1. Define an expected execution path template per query category. The template specifies the minimum necessary tool calls and their order. For example, a "check balance" query might expect: `authenticate_user → get_accounts → get_balance(account_id)` — 3 necessary calls.
2. Compare the actual execution path against the template.
3. Score: `expected_calls / actual_calls`. A score of 1.0 means the agent executed exactly the expected path. A score of 0.3 means the agent made 3x more calls than necessary.

**Query category templates must be authored by domain experts** who know the correct path for each query type. Templates are maintained in the living eval dataset alongside golden answers.

#### 4. Duplicate API Detection

**What it measures:** Whether the agent called multiple external APIs that returned overlapping or equivalent data — a more subtle form of redundancy that crosses tool boundaries.

**Algorithm:**
1. Compare response payloads (or response fingerprints) across different API calls within the same execution.
2. If two different API calls return data sets with >80% overlap (e.g., `get_customer_info` and `get_customer_profile` return the same customer record), flag as duplicate.
3. Score: count of duplicate API pairs.

**Example:** Agent calls `stripe.get_customer(id)` AND `internal.get_customer_profile(id)` — both return email, name, and address. The second call was unnecessary.

#### 5. Per-Query Cost Attribution

**What it measures:** The total cost of the query in dollars, broken down by cost source.

**Algorithm:**
1. Sum LLM call costs (tokens × cost per token for the model used).
2. Sum external API costs (per-call pricing from the API provider).
3. Sum database query costs (estimated from query complexity and execution time).
4. Report total cost and cost breakdown per query.

**Required:** A cost model that maps each tool call to its dollar cost. The cost model must be maintained with real pricing data from providers; stale cost models mislead decisions.

### Behavioral Eval Pipeline

```
Agent Query → Full Execution Trace (spans)
    │
    ├──→ Redundancy Analyzer → redundancy_score
    ├──→ Loop Detector → loop_detected (bool) + loop_length
    ├──→ Path Efficiency Calculator → efficiency_ratio (expected/actual)
    ├──→ Duplicate API Detector → duplicate_api_count
    └──→ Cost Attributor → total_cost_usd + cost_breakdown
    │
    └──→ Behavioral Score Report
         ├── Pass/Fail per score against category-specific thresholds
         ├── Anomaly flag if any score exceeds 2σ from historical baseline
         └── Report stored in eval results, linked to trace_id
```

### Execution Frequency

Behavioral eval is more expensive than Layer 1 or Layer 2 because it requires running (or replaying) the agent, not just evaluating its output. Cost governance is essential:

| Trigger | Scope | Rationale |
|---|---|---|
| Stratified CI (every PR) | Sample of ~10 queries per category | Fast feedback on whether behavioral scores regress |
| Full merge suite | All non-archived cases in the living eval dataset | Complete behavioral coverage before merge to main |
| Scheduled regression (nightly/weekly) | Full dataset + deep/expensive cases | Long-running behavioral analysis that is too slow for PR gates |
| Incident investigation | Specific query category flagged by anomaly | Targeted deep dive into behavioral degradation |

### Anomaly Detection

Behavioral scores are continuous metrics — they degrade gradually, not fail catastrophically. Anomaly detection with historical baselines is essential:

1. **Establish baseline** per query category: expected redundancy score, expected efficiency ratio, expected cost range.
2. **Monitor drift:** When a query category's average efficiency ratio drops below 2σ of its historical baseline, trigger an alert.
3. **Cost anomaly:** When per-query cost exceeds 2x the category baseline, flag for investigation even if all other scores pass.

## Implementation in this repo

### What already exists

The repo has the trace collection infrastructure that a behavioral eval system would consume, but no behavioral evaluation logic:

- **trace-instrumentation** (`docs/canonical/trace-instrumentation.md:24`) provides the complete span collection pipeline: `tracer.ts` (state machine of spans, 10/10 testes), `trace-cli.ts` (CLI wrapper, 7/7 testes), `task-wrapper.sh` (bash wrapper with --start-only/--end-last/--wrap modes, 8/8 testes), `collect-session.sh` (bridge), `session-end-hook.sh` (post-session hook), `collector.ts` (SQLite persistence in `telemetry.db`). Every `task()` call is instrumented with span data including category, subagent type, skills, duration, tokens, success/failure, and trace_id.
- **deterministic-tool-dispatch** (`docs/canonical/deterministic-tool-dispatch.md:33`) defines tools as JSON + deterministic code — providing the data model for tool call sequences and parameters.
- **n-plus-one-long-session-evals** (`docs/canonical/n-plus-one-long-session-evals.md:28`) evaluates behavioral continuity after context reduction (loading N turns, testing turn N+1) but does not evaluate individual tool call paths.
- **The flywheel daemon** (60s loop, anomaly_score ≥ 80 → QI loop) provides the anomaly detection infrastructure that could consume behavioral scores.
- **The QI loop** (review-work → recommendation-writer → writing-plans → implement → re-verify) provides the correction mechanism for behavioral failures.

### What is missing

Behavioral evaluation of agent execution paths is NOT_FOUND as a named entity. The trace data exists but no evaluation logic consumes it for path analysis:

1. **Redundancy score:** NOT_FOUND. No algorithm detects repeated calls to the same tool with equivalent parameters.
2. **Loop detection flag:** NOT_FOUND. No algorithm detects semantic cycles in tool call sequences.
3. **Path efficiency ratio:** NOT_FOUND. No expected execution path templates exist per query category.
4. **Duplicate API detection:** NOT_FOUND. No cross-tool response comparison for overlapping data.
5. **Per-query cost attribution in dollars:** NOT_FOUND. Token counts are collected but not converted to dollar costs per query.
6. **Layer 3 evaluation logic that consumes trace spans:** NOT_FOUND. The trace pipeline collects spans into `telemetry.db` but no behavioral scoring pipeline reads them.

Add:

1. A behavioral eval pipeline (this doc) that defines the five scores and their algorithms.
2. Redundancy analyzer: a module that consumes trace spans and detects repeated tool calls with equivalent parameters.
3. Loop detector: a module that builds a tool-call graph and detects semantic cycles.
4. Path efficiency calculator: a module that compares actual paths against expected templates.
5. Duplicate API detector: a module that cross-references API response payloads.
6. Per-query cost attributor: a module that maps tool calls to dollar costs using a maintained cost model.
7. Expected execution path templates per query category, maintained as part of the living eval dataset.
8. Integration with eval-tier-stratification: behavioral eval runs at deep tier (merge + scheduled), with stratified sampling for CI.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Reveals the "wrong path, right answer" failure mode that demo evaluations never expose | Requires full trace instrumentation of every tool call — adding tracing to existing agents retroactively is high effort |
| Quantifies the per-query cost profile, enabling cost prediction at scale | Defining the "correct" path template per query category requires expert knowledge of the agent's design intent |
| Path efficiency scores provide a leading indicator of production cost before CSAT drops | Cost model accuracy depends on real pricing data from providers; stale cost models mislead decisions |
| Loop detection catches infinite or near-infinite tool call cycles before they consume budgets or crash the system | Path analysis is expensive to run on every query; requires sampling or cost-tiered execution |
| Behavioral anomaly detection catches gradual degradation (increasing redundancy over weeks) that binary alerts miss | Behavioral scores are sensitive to query category — a high redundancy score for a "multi-step reasoning" query may be normal |

## Relationship to Other Patterns

- **Is Layer 3 of:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — the behavioral evaluation layer.
- **Consumes data from:** [[docs/canonical/trace-instrumentation|Trace Instrumentation]] — the span collection pipeline that provides execution traces.
- **Uses data model from:** [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] — tools as structured JSON dispatch.
- **Detected by:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — behavioral failures become eval regression cases.
- **Scheduled by:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — behavioral eval runs at deep tier with stratified CI sampling.
- **Anchored in:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] — expected execution path templates maintained alongside golden answers.
- **Complements:** [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]] — N+1 evals test behavioral continuity after context reduction, not individual tool call efficiency.
- **Integrated with:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] — behavioral failures feed into the flywheel daemon → QI loop → correction.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:140` — original pattern definition (Bhaumik).
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:157` — Missing classification with evidence of NOT_FOUND across all canonical docs.
- `docs/canonical/trace-instrumentation.md:24` — span collection infrastructure.
- `docs/canonical/deterministic-tool-dispatch.md:33` — tool call data model.
- `docs/canonical/n-plus-one-long-session-evals.md:28` — behavioral continuity evaluation.
- `docs/canonical/trace-instrumentation.md:28` — full component list and enforcement layers.

---

*Created: 2026-06-26 | From: Production AI Playbook classification | Precedence: canonical*
