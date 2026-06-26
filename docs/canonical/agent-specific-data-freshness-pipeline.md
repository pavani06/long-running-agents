---
title: "Agent-Specific Data Freshness Pipeline"
type: canonical
aliases: ["data freshness pipeline", "agent data pipeline", "freshness guarantees", "staleness monitoring"]
tags: ["production", "knowledge-management", "context-engineering", "harness-engineering"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]", "[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
---

# Agent-Specific Data Freshness Pipeline

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/
**Classification:** Missing (P0, Low)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Data pipelines built for human consumption (dashboards, reports) tolerate staleness, ambiguity, and inconsistency because humans infer context and apply judgment. Agents treat every data point literally — stale embeddings, outdated policy documents, and contradictory records produce confident wrong answers that directly damage user trust.

The canonical example is the "stale RAG" failure mode: a bank changes interest rates, sends customer emails, but the agent keeps quoting old rates because the vector database was not updated. The failure is invisible to infrastructure monitoring (the agent is up, latencies are normal) but catastrophic to user trust.

The repo has zero coverage for agent-specific data freshness pipelines. The closest artifacts are an application-level freshness gate in the KODA e-commerce domain (`freshness.py`) that detects stale price/stock at send time, and epistemic drift detection in `obsidian-eval/src/ground-truth.ts` that compares candidate principles against ground truths. Neither addresses the infrastructure pattern of data pipelines designed for agent consumption with freshness guarantees, consistency checks, and staleness monitoring.

## Solution

Build a data pipeline designed for agent consumption — not for human dashboards — with three core guarantees:

### 1. Freshness Guarantees with SLAs

Every source document change triggers automatic re-ingestion and re-embedding within a defined SLA. The pipeline is event-driven (not periodic batch), reacting to source document changes in real time.

```
Source document change → Change event → Re-ingestion → Re-embedding → Agent knowledge base updated
```

The SLA defines maximum staleness per document class:
- **Hot documents** (policy documents, pricing): SLA < 5 minutes
- **Warm documents** (product catalogs, FAQs): SLA < 1 hour
- **Cold documents** (historical references): SLA < 24 hours

### 2. Consistency Checks

Before ingestion into the agent's knowledge base, contradictory records across documents are flagged. Two policy documents with conflicting interest rates must not both enter the vector database without a resolution. Consistency checks operate at ingestion time (gate) and at query time (warning).

| Check | Mechanism | Action on conflict |
|---|---|---|
| Numeric contradiction | Compare numeric fields (prices, rates, limits) across documents | Flag for human review; block ingestion until resolved |
| Semantic contradiction | LLM-based comparison of textual claims | Route to human with both document excerpts |
| Schema mismatch | Validate document structure against expected schema | Reject with structured error |

### 3. Staleness Monitoring in the Tracing Layer

The trace pipeline detects when agent responses reference outdated document versions. When an agent retrieves a document whose version is behind the source system, the trace span records a staleness flag. This flag feeds into the eval dashboard and triggers CSAT alerts when staleness exceeds thresholds.

### Pipeline Architecture

| Component | Responsibility | Trigger |
|---|---|---|
| **Change detector** | Monitor source systems for document changes | Webhook, polling, or filesystem watch |
| **Ingestion pipeline** | Parse, validate, and normalize changed documents | Change event |
| **Consistency gate** | Check for contradictions before ingestion | Before re-embedding |
| **Re-embedding engine** | Regenerate embeddings for changed documents | After consistency gate passes |
| **Staleness monitor** | Detect agent responses referencing outdated versions | Agent query → trace span |
| **Freshness dashboard** | Per-document-class freshness SLA compliance | Continuous |

## Implementation in this repo

### What already exists

**NOT_FOUND across all evidence sources.** No canonical doc, curriculum module, analysis, ADR, or plan addresses agent-specific data freshness pipeline architecture. The closest artifacts are:

- `agent-analysis/Programa-conhecimento-aplicado/projeto-koda/freshness.py:74` — application-level freshness gate in the KODA e-commerce domain that detects stale price/stock at send time. This is domain-specific business logic, not a data pipeline infrastructure pattern.
- `obsidian-eval/src/ground-truth.ts:133` — `checkDrift()` detects epistemic drift between candidate principles and ground truths. This is knowledge consistency validation, not data freshness.
- `epistemic-memory-graph.md` — grafo de memória com status epistêmico e proveniência. Tracks entity relationships and provenance but does not monitor source document freshness.

### What is missing

1. **No freshness guarantees with SLAs** for re-ingestion/re-embedding after source document changes.
2. **No consistency checks** flagging contradictory records before agent ingestion.
3. **No staleness monitoring** in the tracing layer that detects when agent responses reference outdated document versions.
4. **No event-driven update triggers** for source document changes — the repo has no source document integration infrastructure.
5. **No data pipelines designed for agent consumption** rather than human dashboard consumption. The existing data flows (knowledge pipeline, telemetry pipeline) serve internal operational needs, not agent-facing knowledge freshness.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents the "stale RAG" failure mode: agent quotes outdated information that contradicts current source documents | Requires integration with every source document system to detect changes — organizational data is often scattered across legacy systems without webhooks |
| Data quality becomes a first-class engineering concern — 60% of project time may need to be allocated to data foundation | Embedding regeneration latency is non-trivial; large knowledge bases may take minutes to re-embed, creating a freshness gap |
| Event-driven freshness eliminates the gap between "document changed" and "agent knows about the change" | Consistency checks require semantic comparison between documents, which may use LLM calls — adding cost |
| Staleness monitoring provides leading indicators of quality degradation before CSAT drops | The 60% time investment in data foundation must be justified against the business value of the agent |

## Relationship to Other Patterns

- **Informs:** Production Failure Regression Flywheel — staleness-caused failures become new regression cases in the eval dataset.
- **Depends on:** Trace Instrumentation — staleness monitoring requires trace spans that capture document version metadata.
- **Complements:** Neutral Selection Layer — the selection layer can factor document freshness into retrieval ranking, deprioritizing stale documents.
- **Complements:** Epistemic Memory Graph — the graph's provenance tracking provides the version lineage that staleness monitoring consumes.
- **Feeds:** Eval Tier Stratification — freshness-related eval cases can be assigned to the fast tier (deterministic version comparison) or medium tier (semantic consistency LLM-as-judge).

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:294` — extracted pattern definition.
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:347` — Missing classification (P0, Low).
- `agent-analysis/Programa-conhecimento-aplicado/projeto-koda/freshness.py:74` — closest artifact: application-level freshness gate in KODA.
- `obsidian-eval/src/ground-truth.ts:133` — closest artifact: epistemic drift detection.
- `docs/canonical/epistemic-memory-graph.md` — provenance tracking infrastructure.

---

*Created: 2026-06-26 | From: Production AI Playbook classification (Batch B) | Precedence: canonical*
