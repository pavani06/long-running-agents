---
title: "Task-Routed Model Tiering"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["agentes-orquestracao", "evals"]
aliases: ["task-routed model selection", "per-task model dispatch", "model tier routing", "tiered model dispatch"]
relates-to: ["[[docs/canonical/multi-provider-model-routing|Multi-Provider Model Routing with Capacity Resilience]]", "[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]", "[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]"]
---

# Task-Routed Model Tiering

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Partial Coverage (High)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Using a single frontier model for every subtask within an agent turn wastes cost and latency on tasks that do not need frontier-level reasoning. An agent turn typically contains multiple subtasks: intent classification (requires pattern matching), knowledge retrieval (requires search), structured data lookups (requires deterministic logic), reasoning (requires frontier intelligence), and response generation (requires fluency). Running all of these through a frontier model like Opus or GPT-5 means paying frontier prices for classification and retrieval work that a lightweight model could handle at a fraction of the cost and latency.

The problem compounds in production at scale: Sierra's platform handles billions of conversations per year. The cost difference between routing all classification tasks to a frontier model vs. a lightweight classifier is measured in millions of dollars annually. And because lightweight models have lower latency, routing simple tasks to them also reduces end-to-end turn time — the user gets a response faster because classification didn't wait for frontier inference.

The deeper problem is architectural coupling: when model selection is embedded in orchestration logic, switching models requires rewriting agent code. A task-routed architecture decouples model selection from orchestration — the routing layer decides which model handles which task, and the harness adapts without code changes.

## Solution

Task-routed model tiering dispatches each subtask within an agent turn to the appropriate model tier based on the task's quality requirements, latency budget, and cost profile. The routing layer maintains per-task eligible model sets and dispatches subtasks in parallel to maximize throughput.

**Key components:**

1. **Per-task eligible model sets**: Each task type defines the models that meet its quality bar. Intent classification might be eligible on Haiku (Anthropic), Flash (Google), and a custom in-house classifier. Reasoning tasks might require Opus (Anthropic) or a comparable frontier model. Response generation requires fluency and empathy — frontier models for complex responses, mid-tier for simple acknowledgments. These sets evolve as model capabilities change.

2. **Parallel dispatch of subtasks**: Within a single turn, subtasks are dispatched to their respective model tiers in parallel. The classification task runs on a lightweight model while the reasoning task runs on a frontier model simultaneously — the overall turn latency is bound by the slowest subtask, not the sum of all subtasks.

3. **Composition rule of thumb**: Wedeen describes Sierra's model composition as "roughly one-third frontier, one-third in-house fine-tuned, one-third third-party." This is not a static allocation — it is an emergent property of the routing layer making per-task decisions. Over time, the distribution converges to this ratio because that is where the quality/cost tradeoff settles.

4. **Decoupled orchestration and model selection**: The agent's orchestration logic (what to do next) is separate from the routing layer's model selection (which model to use). Changing model assignments for a task type does not require changes to agent code — only to the routing configuration.

**How parallel dispatch works in practice:**

1. A conversation turn arrives. The harness decomposes it into subtasks: classify intent, retrieve knowledge, fetch customer data, generate response.
2. The routing layer evaluates each subtask against eligible model sets: classify → Haiku (lightweight, fast), retrieve → in-house search (deterministic), fetch data → internal API (deterministic), generate response → Opus (frontier, needs fluency).
3. Subtasks are dispatched in parallel. Classification returns in 200ms via Haiku. Data fetch returns in 50ms via internal API. Search returns in 300ms. The harness waits for all parallel tasks.
4. The response generator receives the aggregated context (intent, knowledge, customer data) and generates the final response via Opus.
5. The user experiences the latency of the slowest subtask plus the generation pass — significantly faster than running everything sequentially through Opus.

**Distinction from multi-provider routing:** Task-routed model tiering decides *which tier of model* (frontier, mid, lightweight) per task. [[docs/canonical/multi-provider-model-routing|Multi-Provider Model Routing]] decides *which vendor* for that tier. Together they form a two-dimensional routing matrix: capability tier × provider.

## Implementation in this repo

### What already exists

From the classification:

- `~/.opencode/skills/analyze-and-improve/SKILL.md:67`: `model_tier.py` routes pipeline phases (3, 4, 6) to lighter model via `export AI_LIGHT_CATEGORY=quick`. Phase-level tiering, not task-level routing within a turn.
- `long-running-agents/curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:845-858`: KODA assigns Opus to Generator and Sonnet to Evaluator. Agent-level model assignment, not within-turn routing.
- `long-running-agents/curriculum/10-references/model-capability-timeline.md:2312`: Industry reference: "Haiku/Flash for 80%, Opus for 15%" documented as FAQ, not formalized pattern.

### What is missing

1. **Task-level routing within a turn**: The repo routes at the agent level (Generator gets Opus, Evaluator gets Sonnet) and at the pipeline phase level (`model_tier.py` routes phases). Neither is task-level routing where individual subtasks within a turn can be dispatched to different models in parallel.
2. **Parallel dispatch mechanism**: No infrastructure for orchestrating parallel model calls to different tiers within a single agent turn.
3. **Per-task eligible model sets**: No formalized concept of which models are eligible for which task types, maintained as model capabilities evolve.
4. **Decoupled model selection from orchestration**: Model assignments are embedded in agent definitions and pipeline code, not in a separate routing layer.

The repo's single-session coding-agent architecture means within-turn multi-model dispatch has not been architecturally necessary — coding agents typically use one model for the entire session. This pattern becomes relevant when the harness evolves toward production agent deployment with multi-task turns.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Reduces per-turn cost by routing simple tasks to lightweight models — material at production scale | Incorrect task classification routes simple tasks to expensive models (waste) or complex tasks to weak models (quality degradation) |
| Decreases end-to-end latency through parallel task dispatch | Parallel dispatch adds coordination complexity — if one subtask times out, the harness must decide: wait, retry with a different model, or proceed with partial results |
| Decouples model selection from orchestration — switch models without rewriting agent code | Per-task eligible model sets must be maintained as model capabilities evolve — a new model release can obsolete yesterday's routing decisions |
| Composition ratio (one-third frontier, one-third in-house, one-third third-party) emerges naturally from per-task decisions | Not beneficial when all subtasks genuinely require frontier reasoning — tiering adds overhead without benefit when every task needs the best model |

## Relationship to Other Patterns

- **Complements:** [[docs/canonical/multi-provider-model-routing|Multi-Provider Model Routing with Capacity Resilience]] — model tiering decides capability level; multi-provider routing decides vendor. Together they form a complete routing matrix.
- **Builds on:** [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] — the eval infrastructure that validates model-agnostic correctness across tiers.
- **Requires:** [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] — model-agnostic context format so that outputs from different tiers can be aggregated without format translation.
- **Requires:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — model-diverse evaluation to validate that lightweight models meet quality bars for their assigned tasks.
- **Contrasts with:** Agent-level model assignment (KODA's Generator=Opus, Evaluator=Sonnet) — task-routed tiering operates within a turn, not across agent roles.

## References

-  lines 19-45 — extracted pattern with parallel dispatch, one-third composition ratio, decoupled orchestration.
-  lines 39-49 — Partial Coverage classification with evidence of phase-level and agent-level tiering only.
- `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:845-858` — KODA agent-level model assignment.
- `curriculum/10-references/model-capability-timeline.md:2312` — industry reference on model tier composition ratios.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
