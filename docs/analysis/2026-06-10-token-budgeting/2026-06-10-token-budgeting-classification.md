---
title: "Token Budgeting Pattern Classification"
type: analysis
date: 2026-06-10
tags: ["agentes-orquestracao", "curriculo-conteudo", "context-engineering"]
aliases: ["token budgeting classification", "classificacao token budgeting", "token budget coverage"]
relates-to: ["[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/external-state-persistence|External State Persistence]]"]
sources: ["[[docs/system-of-record|System of Record]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Patterns]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]"]
---
# Token Budgeting Pattern Classification

Scope: classification of the 10 extracted patterns in `docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns.md` against the target repository's canonical documentation. I read `docs/system-of-record.md` first, then all Markdown files present under `docs/canonical/` before classifying. The titles below follow the actual `patterns.md`; several names differ from the task's abbreviated list.

## 1. Explicit Token Budget Ledger

**Classification:** Partial Coverage

**Justification:** Canonical docs cover deliberate context construction, block separation, stable prompt budget boundaries, and context-reduction policies, but no canonical doc defines a ledger that calculates fixed prompt/tool-schema cost, accumulated context cost, reserved response buffer, safety buffer, remaining budget, and budget percentage for each next step.

**Evidence:** `docs/canonical/owned-agent-control-loop.md:60` says the context builder assembles history, memory, tool results, and business state, and `docs/canonical/owned-agent-control-loop.md:61` requires constructing every token deliberately. `docs/canonical/stable-harness-prompt.md:28` separates the stable harness prompt from reducible payload, and `docs/canonical/stable-harness-prompt.md:30`-`docs/canonical/stable-harness-prompt.md:40` defines context blocks and reduction policy. `docs/canonical/head-tail-context-truncation.md:28`-`docs/canonical/head-tail-context-truncation.md:39` covers bounded context under a policy-defined budget with recoverable omitted middle. NOT_FOUND for a canonical ledger schema with response reserve, safety reserve, remaining-budget percentage, and per-call budget breakdown.

**Integration value:** High

## 2. Burn-Rate Runtime Forecast

**Classification:** Missing

**Justification:** No canonical doc covers a runtime forecast based on timestamped token usage, consumption velocity, acceleration, and estimated remaining messages/minutes. Existing docs discuss context reduction, token cost, eval runtime, latency, or harness component ROI, but not a live token burn-rate runway model.

**Evidence:** NOT_FOUND after reading `docs/system-of-record.md` and all Markdown files present in `docs/canonical/`. The closest canonical context-budget docs are static or structural: `docs/canonical/head-tail-context-truncation.md:28`-`docs/canonical/head-tail-context-truncation.md:39` defines bounded active context and recoverable omitted middle, and `docs/canonical/stable-harness-prompt.md:30`-`docs/canonical/stable-harness-prompt.md:40` defines context blocks and reduction policy. The closest metric docs are not equivalent: `docs/canonical/measured-harness-evolution-lifecycle.md:52`-`docs/canonical/measured-harness-evolution-lifecycle.md:60` uses ROI, false positives, latency, token cost, and maintenance cost for harness component lifecycle, while `docs/canonical/eval-tier-stratification.md:38`-`docs/canonical/eval-tier-stratification.md:49` defines eval runtime and cost metadata. None defines tokens-per-minute, tokens-per-iteration, acceleration, or estimated remaining session runway.

**Integration value:** High

## 3. Phase-Gated Token Health Monitor

**Classification:** Partial Coverage

**Justification:** Canonical docs already have loop intervention points, degradation rungs, context reduction, and eval progression gates, but no unified token-health monitor that converts remaining budget plus burn-rate forecast into green/yellow/orange/red phases and deterministic actions such as continue, monitor, compress, summarize, or new session.

**Evidence:** `docs/canonical/owned-agent-control-loop.md:68`-`docs/canonical/owned-agent-control-loop.md:75` defines loop controls including break, summarize, judge, human approval, and force terminate. `docs/canonical/tested-degradation-ladder.md:29`-`docs/canonical/tested-degradation-ladder.md:65` defines an ordered degradation ladder from failure classification through retry, fallback, escalation, and logging. `docs/canonical/pain-signal-eval-progression-gate.md:40`-`docs/canonical/pain-signal-eval-progression-gate.md:51` maps observed pain signals to next eval capabilities. NOT_FOUND for token-specific health phases driven by remaining-budget percentage and burn-rate acceleration.

**Integration value:** High

## 4. Durable Fact Selective History

**Classification:** Partial Coverage

**Justification:** Canonical docs cover durable state extraction, external persistence, freshness-aware injection, and recoverable memory handles. They do not unify those pieces into a selective-history policy that combines recent conversational texture with structured critical facts, updates durable memory when new facts appear, and explicitly drops transient turns.

**Evidence:** `docs/canonical/external-state-persistence.md:31`-`docs/canonical/external-state-persistence.md:57` defines extracting critical data, writing it to an external store, loading it on the next turn, and merging it with current context. `docs/canonical/external-state-persistence.md:59`-`docs/canonical/external-state-persistence.md:65` distinguishes durable facts from content that should not be persisted. `docs/canonical/stable-harness-prompt.md:30`-`docs/canonical/stable-harness-prompt.md:40` includes durable state as a separately injected context block. `docs/canonical/addressable-memory-catalog.md:28`-`docs/canonical/addressable-memory-catalog.md:43` defines stable handles and previews for omitted content. NOT_FOUND for one canonical selective-history contract combining recent turns plus structured durable facts plus update/freshness/provenance rules.

**Integration value:** High

## 5. Windowed Recent History

**Classification:** Better Implementation

**Justification:** The extracted pattern is a simple recent-window strategy. The canonical docs define a stronger version: preserve stable prompt, head, tail, latest result, and exact recoverable middle instead of only keeping the last N turns. This is superior because it bounds active context while retaining original anchors and recoverability.

**Evidence:** `docs/canonical/head-tail-context-truncation.md:20`-`docs/canonical/head-tail-context-truncation.md:24` explains why keeping only the beginning or only the end loses either latest state or original constraints. `docs/canonical/head-tail-context-truncation.md:28`-`docs/canonical/head-tail-context-truncation.md:39` defines active context as stable prompt, head, tail, latest result, plus externally recoverable middle. `docs/canonical/head-tail-context-truncation.md:63`-`docs/canonical/head-tail-context-truncation.md:70` records the tradeoff: more deliberate boundary selection and storage cost in exchange for bounded active context, auditability, and follow-up handling.

**Integration value:** Medium

## 6. Summary Buffer Continuity

**Classification:** Partial Coverage

**Justification:** Canonical docs mention summarization and structured old-history summaries as context-reduction tools, but no canonical doc defines an explicit rolling summary buffer with freshness metadata, update rules, target budget, quality checks, and portability as a handoff artifact.

**Evidence:** `docs/canonical/owned-agent-control-loop.md:60`-`docs/canonical/owned-agent-control-loop.md:63` names summarization and compression as context-builder interventions. `docs/canonical/stable-harness-prompt.md:28`-`docs/canonical/stable-harness-prompt.md:41` permits summarizing, truncating, externalizing, or retrieving reducible history and tool bulk while preserving the harness prompt. `docs/canonical/head-tail-context-truncation.md:24` warns that opaque summarization can remove exact details without auditable recovery, and `docs/canonical/head-tail-context-truncation.md:59` requires exact recoverability rather than only summaries. NOT_FOUND for a canonical summary-buffer lifecycle.

**Integration value:** High

## 7. Targeted Semantic Compression

**Classification:** Partial Coverage

**Justification:** Canonical docs include compression as an intervention and include specific one-line error summarization, but they do not define selective semantic compression for arbitrary verbose messages, tool results, or trace chunks under fidelity criteria and target token budgets.

**Evidence:** `docs/canonical/owned-agent-control-loop.md:42`-`docs/canonical/owned-agent-control-loop.md:63` names the context builder and interventions to summarize, compress, and inject context. `docs/canonical/stable-harness-prompt.md:37`-`docs/canonical/stable-harness-prompt.md:39` allows tool or trace bulk to be summarized, externalized, or delegated. `docs/canonical/error-context-hygiene.md:30`-`docs/canonical/error-context-hygiene.md:39` defines a narrower compression mechanism for failures: summarize errors, never blind-append, and keep only what is needed. NOT_FOUND for a general-purpose semantic compression contract with required facts, fidelity criteria, target budget, and omission notes.

**Integration value:** Medium

## 8. Semantic Topic Bucketing

**Classification:** Missing

**Justification:** No canonical doc covers grouping conversation messages, tool outputs, or trace events into semantic topic buckets with per-topic summaries, retention policies, and source-span mappings. Existing memory docs provide handles, kinds, scopes, epistemic labels, and graph retrieval, but not topic-bucketed retention or summarization.

**Evidence:** NOT_FOUND after reading `docs/system-of-record.md` and all Markdown files present in `docs/canonical/`. The closest memory docs are adjacent but not equivalent: `docs/canonical/addressable-memory-catalog.md:28`-`docs/canonical/addressable-memory-catalog.md:43` defines omitted-memory fields such as `id`, `kind`, `location`, `preview`, `scope`, and `fetch`; `docs/canonical/epistemic-memory-graph.md:28`-`docs/canonical/epistemic-memory-graph.md:50` adds epistemic labels, provenance, graph edges, and retrieval fusion; `docs/canonical/external-state-persistence.md:59`-`docs/canonical/external-state-persistence.md:65` defines durable categories, not semantic topic buckets. None defines a topic taxonomy, per-topic summary policy, or mapping from bucket summaries back to source spans.

**Integration value:** Medium

## 9. Hybrid Context Stack

**Classification:** Partial Coverage

**Justification:** Canonical docs already define most layers in the stack: stable harness prompt, head/tail, omitted recoverable middle, durable state, addressable memory, and external persistence. What is missing is a unified canonical context-stack policy that assembles all layers under a known token budget and emits a decision trace explaining what was kept, summarized, compressed, or omitted.

**Evidence:** `docs/canonical/stable-harness-prompt.md:30`-`docs/canonical/stable-harness-prompt.md:40` defines the context-builder blocks: stable prompt, head, tail, omitted middle, tool/trace bulk, and durable state. `docs/canonical/head-tail-context-truncation.md:28`-`docs/canonical/head-tail-context-truncation.md:39` defines the bounded active context plus recoverable middle. `docs/canonical/addressable-memory-catalog.md:30`-`docs/canonical/addressable-memory-catalog.md:43` defines retrieval metadata for omitted content. `docs/canonical/external-state-persistence.md:31`-`docs/canonical/external-state-persistence.md:57` defines external durable-state loading and merge. NOT_FOUND for a single hybrid context stack with budgeted inclusion order and context-builder decision trace.

**Integration value:** High

## 10. Budget-Aware Session Handoff

**Classification:** Partial Coverage

**Justification:** Canonical docs cover pause/resume, handoff as a loop/control-plane outcome, durable state, and recoverable memory, but no canonical doc makes handoff budget-aware through red-phase token health, fresh-session payload construction, and explicit reset of active context budget.

**Evidence:** `docs/canonical/serializable-pause-resume-state.md:31`-`docs/canonical/serializable-pause-resume-state.md:57` covers serializing context window, execution state, and business state for pause/resume. `docs/canonical/application-owned-agent-control-plane.md:53`-`docs/canonical/application-owned-agent-control-plane.md:64` includes handoff as an explicit loop-controller output. `docs/canonical/external-state-persistence.md:95`-`docs/canonical/external-state-persistence.md:100` connects external state, pause/resume, long-session evals, and feedback writeback. `docs/canonical/addressable-memory-catalog.md:28`-`docs/canonical/addressable-memory-catalog.md:43` supplies recoverable memory handles needed by a handoff payload. NOT_FOUND for a handoff trigger tied to token red phase, burn-rate forecast, or active-budget reset.

**Integration value:** High

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Explicit Token Budget Ledger | Partial Coverage | High |
| 2 | Burn-Rate Runtime Forecast | Missing | High |
| 3 | Phase-Gated Token Health Monitor | Partial Coverage | High |
| 4 | Durable Fact Selective History | Partial Coverage | High |
| 5 | Windowed Recent History | Better Implementation | Medium |
| 6 | Summary Buffer Continuity | Partial Coverage | High |
| 7 | Targeted Semantic Compression | Partial Coverage | Medium |
| 8 | Semantic Topic Bucketing | Missing | Medium |
| 9 | Hybrid Context Stack | Partial Coverage | High |
| 10 | Budget-Aware Session Handoff | Partial Coverage | High |
