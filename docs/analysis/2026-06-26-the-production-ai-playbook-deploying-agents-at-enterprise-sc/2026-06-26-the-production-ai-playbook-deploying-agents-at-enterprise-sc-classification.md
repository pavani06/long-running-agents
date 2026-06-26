---
title: "Classification: Production AI Playbook Patterns vs ecossistema-pavan"
type: classification
date: 2026-06-26
aliases: ["classificação Bhaumik", "pattern classification enterprise agents"]
tags: [analise, classificacao, agentes-orquestracao, evals, production, governanca]
relates-to:
  - "[[docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns|Patterns]]"
  - "[[docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-analysis|Analysis]]"
---

# Classification: Production AI Playbook Patterns vs ecossistema-pavan

> **Source**: 13 patterns extracted from Sandipan Bhaumik's "The Production AI Playbook: Deploying Agents at Enterprise Scale"
> **Classified against**: ecossistema-pavan repository (canonical docs, ADRs, curriculum, runtime infrastructure)
> **Date**: 2026-06-26

## Summary

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | 3-Layer Evaluation Architecture | Partial Coverage | High |
| 2 | Eval-Driven Development Timeline | Partial Coverage | Medium |
| 3 | Living Eval Dataset | Partial Coverage | High |
| 4 | Production Incident to Eval Flywheel | Already Exists | Low |
| 5 | Behavioral Eval Path Analysis | Missing | High |
| 6 | Centralized Cross-Framework Tracing | Partial Coverage | Medium |
| 7 | Prompt-as-Code with Causal Change Management | Partial Coverage | Medium |
| 8 | Eval Dashboard as Primary Detection Surface | Partial Coverage | Medium |
| 9 | Multi-Agent Fault Tolerance | Partial Coverage | High |
| 10 | Agent-Specific Data Freshness Pipeline | Missing | Low |
| 11 | Governance Context Injection for PII Prevention | Missing | Low |
| 12 | Business-Outcome-First Eval Pipeline | Partial Coverage | Medium |
| 13 | Model-Switching Architecture with Enterprise Eval Gate | Partial Coverage | Medium |

**Totals**: 13 patterns — 1 Already Exists, 9 Partial Coverage, 3 Missing, 0 Better Implementation

---

## 1. 3-Layer Evaluation Architecture

**Classification**: Partial Coverage | **Integration Value**: High

**What exists**: eval-tier-stratification provides a 3-tier model (fast/medium/deep) with metadata contracts and decision power per tier; generator-evaluator separates role-based evaluation; constraint-anchored-evaluation defines explicit constraint-based checking; compartmented-evaluation-architecture seals builder from validator surfaces. The repo has the architectural building blocks for multi-layer evaluation.

**What is missing**: The specific 3-layer type taxonomy (Deterministic → Semantic → Behavioral) is not formalized. Layer 1 deterministic scanning (PII regex, schema validation, NER) is not named as a distinct layer. Layer 2 LLM-as-judge for semantic evaluation (groundedness, safety, faithfulness scores) is absent as a canonical pattern — NOT_FOUND in docs/canonical/ (searched: eval-tier-stratification, generator-evaluator, constraint-anchored-evaluation, compartmented-evaluation-architecture, repeatable-agent-spot-check-set). Layer 3 behavioral evaluation (tool call redundancy, loop detection, duplicate API calls, path efficiency) is NOT_FOUND in any canonical doc — trace-instrumentation.md covers span collection but not behavioral scoring.

**Evidence**:
- `long-running-agents/docs/canonical/eval-tier-stratification.md:32` — Organize evals into fast, medium, and deep tiers. Each tier must declare runtime, cost, flakiness tolerance, trigger, threshold, reporting format, owner, and escalation policy.
- `long-running-agents/docs/canonical/eval-tier-stratification.md:62` — The missing implementation is metadata and policy that make the tiers explicit.
- `long-running-agents/docs/canonical/generator-evaluator.md:31` — Separate generation from evaluation into two distinct agents. The Generator is creative and user-facing... The Evaluator is impartial and constraint-facing...
- `long-running-agents/docs/canonical/constraint-anchored-evaluation.md:31` — Anchor every evaluation to an explicit, verifiable constraint list.
- `long-running-agents/docs/canonical/compartmented-evaluation-architecture.md:31` — Extend the Generator-Evaluator separation with explicit information compartmentation.

---

## 2. Eval-Driven Development Timeline

**Classification**: Partial Coverage | **Integration Value**: Medium

**What exists**: pain-signal-eval-progression-gate captures the core principle: invest in eval infrastructure driven by real failure signals, not calendar planning. The trigger mapping table links specific pain signals to minimum eval capabilities (spot-check sets, tier stratification, production sampling, regression flywheel). The repo also has harness-evolution practices that ask 'which concrete failure does this prevent?' before investing.

**What is missing**: The specific 6-week infrastructure-first timeline (build eval weeks 1-6, select model weeks 7-8 based on dataset comparison) is not present. The repo's philosophy is pain-signal-driven, not calendar-driven — it rejects the calendar roadmap in favor of evidence-gated progression. The 'model selection last' principle with eval dataset comparison is NOT_FOUND as an explicit strategy.

**Evidence**:
- `long-running-agents/docs/canonical/pain-signal-eval-progression-gate.md:28` — Treat eval maturity as a gate driven by pain signals instead of a calendar roadmap.
- `long-running-agents/docs/canonical/pain-signal-eval-progression-gate.md:42` — Pain signal → Minimum next capability mapping (user complaints → spot-check set, manual review bottlenecks → tier stratification, escaped edge cases → regression flywheel).
- `long-running-agents/docs/canonical/pain-signal-eval-progression-gate.md:57` — The repo already has adjacent decision habits for harness evolution and rollback.
- `long-running-agents/docs/canonical/pain-signal-eval-progression-gate.md:65` — The missing implementation is a named eval progression gate that explicitly connects pain signals to the next minimum eval capability.

---

## 3. Living Eval Dataset

**Classification**: Partial Coverage | **Integration Value**: High

**What exists**: production-failure-regression-flywheel defines converting production failures into durable regression cases with deduplication and tier assignment. production-grounded-eval-sampling defines the data pipeline (capture, privacy filters, retention, coverage metadata, labeling, replay, refresh). repeatable-agent-spot-check-set provides a seed of repeatable cases. eval-tier-stratification provides fast/medium/deep tiers supporting partitioned execution.

**What is missing**: The explicit 'living eval dataset' concept with monotonic growth guarantee (~200 initial cases growing from every incident), per-category ownership and maintenance cycles (security, login, tool calls, knowledge retrieval, math/reasoning), and explicitly named partitioned execution plans (stratified CI subset vs. full merge suite) is not formalized as a single named artifact. The individual building blocks exist separately but the composition into a single growing, categorized, partitioned dataset is NOT_FOUND as a named entity.

**Evidence**:
- `long-running-agents/docs/canonical/production-failure-regression-flywheel.md:28` — Every production failure that reveals a behavioral gap should become a durable eval regression case unless it is explicitly rejected as duplicate, unactionable, or out of scope.
- `long-running-agents/docs/canonical/production-failure-regression-flywheel.md:71` — A failure intake process that accepts incidents, complaints, escaped edge cases, tool misuse, and scoring gaps.
- `long-running-agents/docs/canonical/production-grounded-eval-sampling.md:28` — Create an end-to-end production-sampled eval dataset that can replay representative real interactions against candidate agent versions.
- `long-running-agents/docs/canonical/production-grounded-eval-sampling.md:37` — Required dataset mechanics: Capture, Privacy filters, Retention policy, Sampling criteria, Coverage metadata, Expected-behavior labeling, Replay infrastructure, Refresh cadence.
- `long-running-agents/docs/canonical/eval-tier-stratification.md:36` — Fast: inner-loop confidence for known critical paths — seconds to minutes.

---

## 4. Production Incident to Eval Flywheel

**Classification**: Already Exists | **Integration Value**: Low

**Evidence**:
- `long-running-agents/docs/canonical/production-failure-regression-flywheel.md:18` — Every production failure that reveals a behavioral gap should become a durable eval regression case.
- `long-running-agents/docs/canonical/production-failure-regression-flywheel.md:31` — Flywheel steps: 1. Intake a production failure... 2. Capture the interaction, trace, tool results, state snapshot... 3. Apply privacy filters... 4. Label expected behavior... 5. Deduplicate... 6. Add to eval tier... 7. Backfill baseline... 8. Link to incident... 9. Periodically prune.
- `long-running-agents/docs/canonical/production-failure-regression-flywheel.md:42` — Failure taxonomy: prompt issue, tool misuse, context loss, state persistence, scoring gap, latency/cost regression, safety/policy issue, late-session failure.
- `long-running-agents/docs/canonical/trace-instrumentation.md:28` — Components: tracer.ts (state machine of spans), trace-cli.ts (CLI wrapper), task-wrapper.sh (bash wrapper), collect-session.sh (bridge), session-end-hook.sh (post-session hook), collector.ts (SQLite persistence).
- `long-running-agents/docs/canonical/trace-instrumentation.md:76` — Enforcement (4 Camadas): Template Injection, Auto-verificação pré-delegação, Warning pós-sessão, Health check cross-session.

---

## 5. Behavioral Eval Path Analysis

**Classification**: Missing | **Integration Value**: High

**Search locations**: trace-instrumentation.md provides the span collection infrastructure that could power behavioral eval. deterministic-tool-dispatch.md defines tool calls as structured JSON dispatch, providing the data model. n-plus-one-long-session-evals.md evaluates behavioral continuity after context reduction but does not evaluate tool call paths. NOT_FOUND: redundancy score, loop detection flag, path efficiency score, duplicate API detection, per-query cost attribution in the canonical docs or curriculum.

**Note**: No formalization of behavioral path analysis as an evaluation layer. Missing: redundancy scoring of repeated tool calls, loop detection for semantic cycles in tool sequences, path efficiency ratio (necessary/total calls), duplicate API detection across endpoints, per-query cost attribution in dollars, and expected execution path templates per query category. The trace infrastructure exists but no evaluation logic consumes it for behavioral scoring.

**Evidence**:
- `NOT_FOUND:0` — Searched long-running-agents/docs/canonical/ (106 entries) for behavioral eval, path analysis, tool call evaluation, loop detection, redundancy score. No canonical doc defines behavioral evaluation of agent execution paths.
- `long-running-agents/docs/canonical/trace-instrumentation.md:24` — Padrão canônico para instrumentar toda chamada task() no runtime Sisyphus com spans de trace.
- `long-running-agents/docs/canonical/deterministic-tool-dispatch.md:33` — Tools are not magical. Tools are JSON + deterministic code.
- `long-running-agents/docs/canonical/n-plus-one-long-session-evals.md:28` — Evaluate the production context strategy by loading N turns, applying the same context-building... then testing turn N+1.

---

## 6. Centralized Cross-Framework Tracing

**Classification**: Partial Coverage | **Integration Value**: Medium

**What exists**: trace-instrumentation.md defines a complete centralized trace pipeline for the Sisyphus/OpenCode runtime: task-wrapper.sh (instrumentation) → trace-state.json (tmpfs state) → collect-session.sh (dump) → collector.ts (SQLite persistence in telemetry.db). Multiple consumers exist: daily-summary.ts, budget-slo-check.sh, reflection-trace-analyze.sh, flywheel-daemon.service. The collector supports session-level dedup (PRIMARY KEY on session ID). scavenge-sessions.sh provides a safety net for orphaned artifacts (systemd timer every 15min).

**What is missing**: This is single-framework tracing (Sisyphus runtime only). Missing: per-framework adapter pattern for CrewAI, LangChain, or custom agents; OpenTelemetry integration; unified trace schema spanning multiple frameworks; text-to-SQL ad-hoc query interface over traces; cross-framework performance comparison capability; trace sampling at enterprise scale. The repo only has one agent framework to instrument, so cross-framework unification is not applicable — the infrastructure architecture is correct for the scale.

**Evidence**:
- `long-running-agents/docs/canonical/trace-instrumentation.md:24` — Padrão canônico para instrumentar toda chamada task() no runtime Sisyphus com spans de trace, garantindo que cada delegação produza um trace_id no telemetry.db.
- `long-running-agents/docs/canonical/trace-instrumentation.md:28` — Componentes: tracer.ts, trace-cli.ts, task-wrapper.sh, collect-session.sh, session-end-hook.sh, collector.ts.
- `long-running-agents/docs/canonical/trace-instrumentation.md:76` — 4 camadas de enforcement + scavenger safety net (scavenge-sessions.sh, systemd timer 15min).
- `NOT_FOUND:0` — Searched long-running-agents/docs/canonical/ for adapter pattern, OpenTelemetry, multi-framework trace unification, cross-framework schema. No canonical doc addresses collecting traces from multiple agent frameworks into a unified store.

---

## 7. Prompt-as-Code with Causal Change Management

**Classification**: Partial Coverage | **Integration Value**: Medium

**What exists**: stable-harness-prompt.md defines the separation of harness prompt from reducible context and requires deliberate, versioned prompt changes evaluated separately from compaction. application-owned-agent-control-plane.md defines versioned prompt contracts as part of the owned control plane. llm-as-fuzzy-compiler.md treats prompts as first-class durable assets alongside guardrails and docs. The repo explicitly identifies prompt versioning as a gap in owned-agent-control-loop.md:102.

**What is missing**: The specific 3-question causal commit discipline (why changed, what failure caused it, what failure it corrects) is NOT_FOUND as a formal requirement. No explicit prompt rollback infrastructure documented — concept exists (stable-harness-prompt implies rollback should be possible) but no operational procedure. No audit trail linking prompt changes to specific incidents or eval regressions. The concept of 'prompt-as-code with git versioning' exists partially (prompts are treated as durable assets and versioning is prescribed) but the causal change management discipline with 3 mandatory commit questions is not formalized.

**Evidence**:
- `long-running-agents/docs/canonical/stable-harness-prompt.md:28` — Separate the stable harness prompt from reducible context payload... it must preserve the active harness prompt as a first-class input with its own budget and version.
- `long-running-agents/docs/canonical/stable-harness-prompt.md:41` — This pattern does not require a prompt to be immutable forever. It requires prompt changes to be deliberate, versioned, and evaluated separately from context compaction.
- `long-running-agents/docs/canonical/application-owned-agent-control-plane.md:29` — The control plane is the contract... versioned prompt contracts, deliberate context construction, structured action schema, deterministic dispatch, loop policy, persistent execution state, and intervention gates.
- `long-running-agents/docs/canonical/owned-agent-control-loop.md:102` — Prompt: Yes — system prompt is hand-authored (1800+ lines). Not versioned or eval'd as a separate component.
- `long-running-agents/docs/canonical/llm-as-fuzzy-compiler.md:27` — Code is a disposable build artifact and what matters is preserving the prompts, guardrails, and documentation that produced the code.

---

## 8. Eval Dashboard as Primary Detection Surface

**Classification**: Partial Coverage | **Integration Value**: Medium

**What exists**: The repo has a production failure regression flywheel that converts incidents into eval regression cases (production-failure-regression-flywheel.md:28-40), eval tier stratification with fast/medium/deep tiers (eval-tier-stratification.md:28-50), pain-signal-driven eval investment (pain-signal-eval-progression-gate.md:28-50), a flywheel daemon with anomaly detection (60s loop, anomaly_score >= 80 triggers QI loop), SLO checker with burn rate alerts, and the FLYWHEEL_ALERT gate that injects findings into session context.

**What is missing**: Missing the eval dashboard as PRIMARY detection surface: no real-time quality dashboard showing pass/fail rates per eval layer/category/agent, no streaming eval results feeding an always-on monitoring surface, no anomaly alerts keyed to eval quality regression thresholds (as opposed to operational/trace anomaly alerts). The flywheel detects trace anomalies and operational failures — not eval quality regressions surfaced as the first place to look during incidents. The repo detects failures post-hoc via traces, not pre-emptively via eval quality dashboards.

**Evidence**:
- `long-running-agents/docs/canonical/production-failure-regression-flywheel.md:28` — Every production failure that reveals a behavioral gap should become a durable eval regression case
- `long-running-agents/docs/canonical/eval-tier-stratification.md:28` — Organize evals into fast, medium, and deep tiers. Each tier must declare runtime, cost, flakiness tolerance, trigger, threshold, reporting format, owner, and escalation policy.
- `long-running-agents/docs/canonical/pain-signal-eval-progression-gate.md:28` — Treat eval maturity as a gate driven by pain signals instead of a calendar roadmap.
- `scripts/telemetry/flywheel-health.sh:1` — Verificacao completa do pipeline flywheel — relatorio de saude com PASS/FAIL por componente
- `AGENTS.md:343` — FLYWHEEL_ALERT:N detection gate: 'N flywheel finding(s) requerem atencao (severity P1 ou score >= 60)'

---

## 9. Multi-Agent Fault Tolerance

**Classification**: Partial Coverage | **Integration Value**: High

**What exists**: The repo has a tested degradation ladder pattern (tested-degradation-ladder.md:29-63) that defines failure classification → retry with repair → safe fallback or hold → human escalation → outcome log + rung tests. Exponential backoff retry with jitter is implemented in harness/retry.py. Error context hygiene provides bounded retry with summarized errors and cleanup. Owned agent control loop defines explicit intervention points including break, human approval gate, and force terminate. Multi-model evaluation council routes to retry, needs-human, or rubric-update (multi-model-evaluation-council.md:30-47).

**What is missing**: Missing Saga pattern (compensating transactions across distributed agents — no compensating action design or reverse-order rollback for multi-step agent workflows). Missing Circuit Breaker at the agent orchestration layer (no failure-rate-threshold-based tripping that stops cascading failures by routing to fallback — the HoP circuit-breaker.js referenced by codegraph is in Documents/Codex/, not in this repo). The degradation ladder covers single-agent failure recovery, not multi-agent distributed transaction fault tolerance with Saga rollback and rate-threshold circuit breaking.

**Evidence**:
- `long-running-agents/docs/canonical/tested-degradation-ladder.md:29` — Define a tested degradation ladder: an ordered contract that starts at failure classification, allows bounded repair only when recovery is plausible, falls back to a conservative safe action or hold when automation is unsafe, escalates to a human with summarized context when automated recovery is insufficient, logs the outcome, and tests each rung before production reliance
- `long-running-agents/docs/canonical/tested-degradation-ladder.md:46` — [4. Human escalation / context to continue work]
- `long-running-agents/docs/canonical/error-context-hygiene.md:93` — bounded retry integration with max_retries, one-line error summaries, context injection by attempt, success detection, and pending-error cleanup
- `long-running-agents/docs/canonical/owned-agent-control-loop.md:68` — loop intervention points: break, summarize, LM-as-judge, human approval gate, and force terminate
- `.opencode/skills/analyze-and-improve/harness/retry.py:25` — Exponential backoff retry logic — stdlib only (asyncio, random, time, typing)

---

## 10. Agent-Specific Data Freshness Pipeline

**Classification**: Missing | **Integration Value**: Low

**Search locations**: NOT_FOUND across all evidence sources for a data pipeline architecture pattern. The closest artifacts are: (1) freshness.py in agent-analysis — application-level freshness gate in the KODA e-commerce domain that detects stale price/stock at send time, not a data pipeline infrastructure pattern; (2) checkDrift in obsidian-eval — epistemic drift detection between candidate principles and ground truths, not data freshness. Searched paths: long-running-agents/docs/canonical/ (all 85+ files), long-running-agents/docs/decisions/, long-running-agents/docs/analysis/, long-running-agents/curriculum/, plans/adr/, .omo/plans/, obsidian-eval/src/.

**Note**: No agent-specific data pipeline architecture: no freshness guarantees with SLAs for re-ingestion/re-embedding after source document changes, no consistency checks flagging contradictory records before agent ingestion, no staleness monitoring in the tracing layer that detects when agent responses reference outdated document versions, no event-driven update triggers for source document changes, no data pipelines designed for agent consumption rather than human dashboard consumption.

**Evidence**:
- `NOT_FOUND: long-running-agents/docs/canonical/ (all 85+ files):0` — No canonical doc for agent-specific data freshness pipeline, freshness guarantees, or staleness monitoring
- `NOT_FOUND: long-running-agents/curriculum/ and long-running-agents/docs/analysis/:0` — No curriculum module or analysis covering data pipelines designed for agent consumption
- `NOT_FOUND: plans/adr/ and .omo/plans/:0` — No ADRs or plans addressing agent-specific data freshness pipeline architecture
- `agent-analysis/Programa-conhecimento-aplicado/projeto-koda/freshness.py:74` — Closest artifact: application-level freshness gate in KODA e-commerce domain — detects stale price/stock at send time, NOT a data pipeline infrastructure pattern
- `obsidian-eval/src/ground-truth.ts:133` — Closest artifact: epistemic drift detection between candidate principles and ground truths, NOT data freshness

---

## 11. Governance Context Injection for PII Prevention

**Classification**: Missing | **Integration Value**: Low

**Search locations**: NOT_FOUND across all evidence sources. ZERO PII-related canonical docs, curriculum materials, analysis documents, ADRs, or skill implementations. ZERO references to data catalog PII tagging, governance context injection, pre-generation deterministic PII detection, or compliance audit records for sensitive data. The KODA domain (e-commerce) operates in a PII-rich environment (customer names, addresses, payment info) but the repo addresses PII concerns only indirectly through general-purpose constraint-anchored evaluation and compartmented evaluation — never as a domain-specific governance injection pattern.

**Note**: No PII tagging in any data catalog, no governance metadata injection into agent prompts (informing the model which fields are sensitive), no pre-generation deterministic PII detection via NER or regex, no post-generation PII scan as safety net, no audit record of governance context per query. The pattern's core mechanic (Unity Catalog → prompt injection → model awareness of PII fields) is entirely absent.

**Evidence**:
- `NOT_FOUND: long-running-agents/docs/canonical/ (all 85+ files):0` — No PII, governance context, data catalog, or sensitive data detection canonical docs found
- `NOT_FOUND: long-running-agents/curriculum/ (all levels N1-N4):0` — No PII or governance injection modules in any curriculum level
- `NOT_FOUND: long-running-agents/docs/analysis/:0` — No PII-related analysis documents found
- `NOT_FOUND: plans/adr/ and .omo/plans/:0` — No ADRs or plans mentioning PII, governance injection, or data catalog tagging
- `NOT_FOUND: ~/.config/opencode/skills/:0` — No skill implementing PII detection, governance context injection, or compliance audit

---

## 12. Business-Outcome-First Eval Pipeline

**Classification**: Partial Coverage | **Integration Value**: Medium

**What exists**: The repo ties eval investments to business-visible pain signals (user complaints, manual bottlenecks, escaped edge cases) via pain-signal-eval-progression-gate.md:28-50. Production-grounded eval sampling uses real production queries (not synthetic). Eval-to-production correlation tracking measures eval score vs. production outcomes. The KODA domain has business-specific eval rubrics and sprint contracts with human-escalation outcomes.

**What is missing**: Missing the business-outcome-FIRST sequence: 'Define success in business terms → create golden answers from domain experts → build Python pipeline to compare AI outputs against business-outcome metrics.' The repo's eval investment starts from technical pain (incidents, regressions, manual bottlenecks), not from business outcome definition (deflection rate target, CSAT threshold, revenue impact). No golden answers authored by human domain experts as the eval foundation (200+ queries with human-authored expectations). No deflection rate prediction from eval scores. No Python evaluation pipeline that compares agent outputs against business-outcome-aligned golden answers as the FIRST step before building technical eval infrastructure.

**Evidence**:
- `long-running-agents/docs/canonical/pain-signal-eval-progression-gate.md:28` — Treat eval maturity as a gate driven by pain signals instead of a calendar roadmap. The gate asks whether current evidence shows that the next eval capability is now necessary.
- `long-running-agents/docs/canonical/pain-signal-eval-progression-gate.md:44` — User complaints repeat for known workflows → Add or expand Repeatable Agent Spot-Check Set
- `long-running-agents/docs/canonical/eval-to-production-correlation-tracking.md:1` — Eval-to-Production Correlation Tracking
- `long-running-agents/docs/canonical/production-grounded-eval-sampling.md:1` — Production-Grounded Eval Sampling

---

## 13. Model-Switching Architecture with Enterprise Eval Gate

**Classification**: Partial Coverage | **Integration Value**: Medium

**What exists**: The repo has strong philosophical foundation for model independence: neutral-selection-layer.md defines model-agnostic context format, vendor adapter, and cross-model portability. LLM-as-fuzzy-compiler treats models as swappable compiler backends and generated code as disposable. Multi-model-evaluation-council uses model diversity for evaluation. Neutral selection layer is taught in the curriculum (N3 exercises). The codebase uses multiple LLM providers (DeepSeek for orchestrator, Anthropic for momus, etc.) demonstrating practical multi-model operation.

**What is missing**: The neutral-selection-layer is classified as 'Missing (P0)' — it's a documented pattern, not an implementation. Missing: an enterprise eval dataset that is maintained independently of any specific model provider (the dataset that tests model upgrades against domain-specific data before adoption), side-by-side model comparison infrastructure (run candidate model against enterprise eval dataset, compare to current baseline), a model-switching decision framework (switch/hold/hybrid based on eval comparison), provider-upgrade testing against enterprise-specific data (not public benchmarks), and a mechanical process for model comparison that replaces subjective debate with data-driven reports. The philosophical alignment exists but the concrete infrastructure does not.

**Evidence**:
- `long-running-agents/docs/canonical/neutral-selection-layer.md:28` — A model-agnostic selection layer that sits between the model and the store, serving context through a uniform interface regardless of which model, vendor, or session requests it. Three properties define the layer: Neutral (not coupled to a single model), Horizontal (cross-agent, cross-session, cross-model), Structured (relational, not merely storage).
- `long-running-agents/docs/canonical/neutral-selection-layer.md:71` — Context survives model migrations — same structured record serves any model
- `long-running-agents/docs/canonical/neutral-selection-layer.md:73` — Vendor independence: the organization's most durable asset is not locked in
- `long-running-agents/docs/canonical/llm-as-fuzzy-compiler.md:1` — LLM as Fuzzy Compiler — model output as disposable artifact, constraints as durable
- `long-running-agents/docs/canonical/multi-model-evaluation-council.md:28` — Use a model-diverse evaluation council for high-value decisions, risky agent behavior changes, ambiguous rubric cases, and production-impacting releases.
- `long-running-agents/docs/canonical/neutral-selection-layer.md:53` — NOT_FOUND across all 85 canonical docs
- `long-running-agents/curriculum/GLOSSARY.md:530` — Neutral Selection Layer: Camada de selecao model-agnostic e vendor-independent

---

