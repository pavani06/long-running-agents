---
title: "Centralized Cross-Framework Tracing"
type: canonical
aliases: ["cross-framework tracing", "unified trace layer", "multi-framework tracing", "centralized trace"]
tags: ["tracing", "observability", "production"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/trace-instrumentation|Trace Instrumentation]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"]
sources: []
---
# Centralized Cross-Framework Tracing

**Type:** canonical
**Status:** active
**Source:** The Production AI Playbook (Bhaumik, Databricks)
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Enterprises deploying multiple agent frameworks (CrewAI for customer support, LangChain for internal tools, custom agents for domain-specific workflows) across multiple cloud environments create fragmented observability. Each framework has its own tracing format, its own storage, and its own debugging surface. When a production incident spans multiple agents built on different frameworks, diagnosing root cause requires context-switching between disconnected tools — and cross-framework performance comparison is impossible because the data is not comparable.

Regulatory compliance in regulated industries requires end-to-end traceability for every AI-generated output: which agent produced it, using which model, accessing which data, with which tool calls. Without a centralized trace layer, compliance evidence is scattered across framework-specific logs that auditors cannot reconcile.

## Solution

A centralized trace layer with a unified schema across all agent frameworks. Every agent — regardless of which framework built it, which model it uses, or which cloud it runs in — produces traces in a single, framework-independent format that flows into a centralized store.

### Unified Trace Schema

Define a canonical trace schema that every framework adapter must produce. The schema captures the minimum information required for debugging, evaluation, compliance, and cross-framework comparison:

| Field | Type | Description | Required |
|---|---|---|---|
| `trace_id` | UUID | Unique identifier for the full execution | Yes |
| `span_id` | UUID | Unique identifier for this operation | Yes |
| `parent_span_id` | UUID | Parent span (null for root) | Yes |
| `framework` | String | Originating framework (crewai, langchain, custom) | Yes |
| `agent_id` | String | Agent identifier within the framework | Yes |
| `agent_version` | String | Agent version at execution time | Yes |
| `model` | String | Model identifier and version | Yes |
| `session_id` | String | User session identifier | No |
| `query_text` | String | User input (sanitized for PII) | Yes |
| `operation` | String | Operation type: `tool_call`, `llm_call`, `retrieval`, `dispatch` | Yes |
| `tool_name` | String | Tool name (for tool_call operations) | No |
| `tool_params` | JSON | Tool parameters (sanitized/hashed) | No |
| `duration_ms` | Integer | Operation duration in milliseconds | Yes |
| `tokens_in` | Integer | Input tokens (for llm_call operations) | No |
| `tokens_out` | Integer | Output tokens (for llm_call operations) | No |
| `success` | Boolean | Whether the operation succeeded | Yes |
| `error_class` | String | Error classification if failed | No |
| `timestamp` | ISO 8601 | UTC timestamp | Yes |
| `deployment_region` | String | Cloud region or deployment zone | No |
| `metadata` | JSON | Framework-specific metadata (extensible) | No |

### Per-Framework Adapter Pattern

Each agent framework requires an adapter that intercepts framework-native events and translates them into the unified schema:

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   CrewAI     │  │  LangChain   │  │   Custom     │
│   Adapter    │  │   Adapter    │  │   Adapter    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
               ┌──────────▼──────────┐
               │  Unified Trace      │
               │  Layer (SQLite /    │
               │  OLAP / OTEL)       │
               └──────────┬──────────┘
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
┌──────▼──────┐  ┌────────▼───────┐  ┌───────▼──────┐
│ Dashboards  │  │  LLM Judges   │  │  Compliance  │
│ & Alerts    │  │  & Evals      │  │  Reports     │
└─────────────┘  └───────────────┘  └──────────────┘
```

**Adapter responsibilities:**
1. Intercept framework-native events (tool calls, LLM calls, retrieval operations).
2. Normalize to the unified schema (map framework-specific fields to canonical fields).
3. Forward to the centralized trace store (via OpenTelemetry collector or direct write).
4. Handle framework-specific edge cases (e.g., LangChain's callback system, CrewAI's task delegation).

### OpenTelemetry Integration

For frameworks that natively support OpenTelemetry (or can be wrapped with OTel instrumentation), the adapter becomes an OTel exporter: framework emits OTel spans → OTel collector → unified schema transformer → centralized store. This leverages existing instrumentation and reduces per-framework adapter development.

For frameworks without OTel support, the adapter must hook into the framework's event/callback system directly.

### Consumers of the Unified Trace Layer

Once traces from all frameworks flow into a single store with a unified schema, multiple consumers operate on the same data:

- **Single-pane debugging dashboard:** Trace any query from any agent in any framework from one surface. Drill from query → span tree → individual tool call → parameter inspection.
- **Text-to-SQL ad-hoc query interface:** Business users and operators query trace data without knowing the schema: "show me all queries that took >5 tool calls last week", "which agents had >10% failure rate yesterday", "compare average latency between CrewAI and custom agents for checkout queries."
- **LLM judge reports:** Automated quality evaluation consumes the unified trace stream and produces per-agent, per-framework quality scores without knowing which framework produced each trace.
- **Compliance auditor reports:** Regulated industries can demonstrate that every query is traceable end-to-end: which agent, which model, which data accessed, which tool calls, what response was given.
- **Real-time anomaly detection:** Online monitoring detects anomalies (latency spikes, failure rate increases, tool call pattern shifts) across all frameworks from a single alerting surface.
- **Cross-framework performance comparison:** Measure relative performance of CrewAI vs. LangChain vs. custom agents on identical query categories — enabling data-driven framework selection.

### Trace Sampling at Scale

At enterprise scale (thousands of agents, millions of queries per day), storing and processing every trace is economically infeasible. Trace sampling strategies:

| Strategy | When to use | Tradeoff |
|---|---|---|
| **Head sampling** (probabilistic at trace start) | High-throughput, low-risk query categories | May miss rare failure patterns |
| **Tail sampling** (keep all errors + sample successes) | When failures are rare but critical | Requires buffering; adds latency |
| **Category-based sampling** | Different rates per query risk profile | Requires query categorization |
| **Adaptive sampling** (increase rate during anomalies) | Production incident response | Complex to implement |

The sampling strategy must be documented and auditable: compliance auditors need to know what percentage of queries are traced and whether the sampling is biased.

## Implementation in this repo

### What already exists

The repo has a complete centralized trace pipeline for the Sisyphus/OpenCode runtime — single-framework tracing with strong operational discipline:

- **trace-instrumentation** (`docs/canonical/trace-instrumentation.md:24`) defines the full pipeline for the Sisyphus runtime: `task-wrapper.sh` (instrumentation) → `trace-state.json` (tmpfs state) → `collect-session.sh` (dump) → `collector.ts` (SQLite persistence in `telemetry.db`). 25 total tests across tracer.ts, trace-cli.ts, and task-wrapper.sh.
- **Multiple consumers** operate on the trace data: `daily-summary.ts`, `budget-slo-check.sh`, `reflection-trace-analyze.sh`, `flywheel-daemon.service` (60s loop).
- **Session-level dedup:** `collector.ts` uses PRIMARY KEY on session ID for `INSERT OR IGNORE`.
- **4 enforcement layers:** Template injection in AGENTS.md, auto-verification pre-delegation, warning post-session, health check cross-session (`docs/canonical/trace-instrumentation.md:76`).
- **Safety net:** `scavenge-sessions.sh` (systemd timer, 15min) detects orphaned artifacts.
- **Structured span data:** Each span includes category, subagent_type, skills, description, duration_ms, tokens, success/failure, trace_id, model.

### What is missing

This is single-framework tracing: the repo only instruments one agent runtime (Sisyphus/OpenCode), so cross-framework unification is not applicable at this scale. The infrastructure is architecturally correct for single-framework operation:

1. **Per-framework adapter pattern:** NOT_FOUND. The repo has no adapter architecture because it operates a single framework. The adapter concept (interface that normalizes framework-specific traces into a unified schema) would become relevant only if the repo instrumented multiple agent frameworks.

2. **OpenTelemetry integration:** NOT_FOUND. The trace pipeline uses a custom state machine (`tracer.ts` → `/tmp/trace-state.json`) rather than OTel spans. This is appropriate for the repo's scale (single runtime, single machine) but would not scale to multi-framework enterprise deployments.

3. **Unified trace schema spanning multiple frameworks:** NOT_FOUND as a separate concern. The existing schema (`tracer.ts` span format) serves the single-framework case.

4. **Text-to-SQL query interface over traces:** NOT_FOUND. Queries over `telemetry.db` are done via TypeScript modules (`daily-summary.ts`, `budget-slo-check.sh`), not via an ad-hoc natural language interface.

5. **Cross-framework performance comparison:** NOT_FOUND. Not applicable at single-framework scale.

6. **Trace sampling at enterprise scale:** NOT_FOUND. The repo traces every `task()` call — no sampling is needed at single-session scale.

Add (when the repo expands to multiple agent frameworks or when the pattern is taught as architecture):

1. A unified trace schema specification (this doc) that defines the canonical fields.
2. Per-framework adapter interface: a contract that any framework adapter must implement.
3. OpenTelemetry exporter configuration for frameworks that support OTel.
4. Text-to-SQL query interface over the trace store.
5. Cross-framework comparison dashboard metrics.
6. Trace sampling strategy for enterprise-scale deployment.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Single debugging surface: trace any query from any agent in any framework from one tool | Requires per-framework adapter development; each framework's trace format is different |
| Regulatory compliance: centralized trace layer satisfies audit requirements for end-to-end traceability | Trace volume at enterprise scale (thousands of agents, millions of queries) demands significant storage and processing infrastructure |
| Framework-independent evaluation: LLM judges and dashboards consume the same trace format regardless of which framework produced it | Schema evolution management: if a framework adds new trace fields, the centralized layer must accommodate without breaking consumers |
| Enables cross-framework comparisons: measure relative performance of different frameworks on identical queries | Adds latency: trace collection and forwarding is an additional network hop per tool call |
| Single alerting surface: anomaly detection across all frameworks from one monitoring tool | Trace sampling at scale may miss rare failure patterns; compliance requires auditable sampling strategy |

## Relationship to Other Patterns

- **Foundation for:** [[docs/canonical/trace-instrumentation|Trace Instrumentation]] — the single-framework implementation that serves as the first adapter in a multi-framework deployment.
- **Data source for:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — all three evaluation layers consume the unified trace layer.
- **Data source for:** [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] — Layer 3 behavioral scoring consumes execution traces.
- **Detection surface for:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — incidents detected via trace anomalies become eval regression cases.
- **Monitoring for:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] — the flywheel daemon consumes trace data for anomaly detection.
- **Complements:** [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] — cross-framework tracing enables comparing models across frameworks.
- **Validates:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — trace data provides the production outcomes that correlate with eval scores.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:171` — original pattern definition (Bhaumik).
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:190` — Partial Coverage classification with evidence.
- `docs/canonical/trace-instrumentation.md:24` — single-framework trace pipeline for Sisyphus runtime.
- `docs/canonical/trace-instrumentation.md:28` — full component list: tracer.ts, trace-cli.ts, task-wrapper.sh, collect-session.sh, session-end-hook.sh, collector.ts.
- `docs/canonical/trace-instrumentation.md:76` — 4 enforcement layers + scavenger safety net.

---

*Created: 2026-06-26 | From: Production AI Playbook classification | Precedence: canonical*
