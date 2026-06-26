---
title: "Eval Dashboard as Primary Detection Surface"
type: canonical
aliases: ["eval dashboard", "quality detection surface", "primary detection surface"]
tags: ["evals", "production", "observability", "monitoramento"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]"]
---

# Eval Dashboard as Primary Detection Surface

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/
**Classification:** Partial Coverage (P2, Medium)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Traditional production monitoring (logs, APM, infrastructure dashboards) surfaces latency, error rates, and resource consumption — but does not surface agent quality regressions. Increasing hallucination rates, response degradation, and drift in answer accuracy are invisible to infrastructure monitoring. They only become visible days or weeks later through CSAT surveys and user complaints, by which point damage has accumulated.

The repo detects operational failures through trace anomalies (the flywheel daemon processes anomaly_score ≥ 80 triggers) and SLO burn rate alerts. However, quality regressions across eval layers are not surfaced as the first place the team looks during an incident. Eval quality dashboards — pass/fail rates per layer, per category, per agent — are absent as a detection surface.

## Solution

Make the eval dashboard the **primary detection surface** for agent quality incidents. Instead of discovering quality degradation through CSAT surveys or infrastructure alerts, surface it through a real-time quality dashboard that is the first screen the team opens during any incident.

The dashboard should consume streaming eval results from all three layers (deterministic, semantic, behavioral) across all agents and queries, and provide:

1. **Real-time pass/fail rates** per eval layer, per category (security, login, tool calls, knowledge retrieval, math/reasoning), per agent — updated continuously.
2. **Anomaly alerts** keyed to eval quality regression thresholds: when pass rates drop below baseline for any category, alert — not just when traces show operational anomalies.
3. **Trend visualization**: quality trajectory over time, enabling detection of slow degradation (e.g., embeddings gradually going stale) that binary alerts miss.
4. **Drill-down capability**: from aggregate quality score → specific failing eval category → individual failing queries → full trace for rapid diagnosis.
5. **CSAT correlation overlay**: lagging human-feedback signal (CSAT) plotted alongside leading eval signal to validate the dashboard's predictive power.

The dashboard answers the question "is the agent still good?" before anyone asks it. It transforms eval from a development-time CI gate into an always-on production quality monitor.

### Detection vs. Diagnosis

The dashboard is a **detection surface**, not a diagnosis surface. It tells you quality dropped on which layer for which category. You still need traces for root cause analysis. The dashboard's role is to reduce time-to-detect from weeks (CSAT) to minutes (eval pass rate drop).

## Implementation in this repo

### What already exists

- **Production Failure Regression Flywheel** (`production-failure-regression-flywheel.md:28-40`) converts incidents into eval regression cases with deduplication and tier assignment.
- **Eval Tier Stratification** (`eval-tier-stratification.md:28-50`) defines fast/medium/deep tiers with runtime, cost, flakiness, trigger, threshold, reporting, owner, and escalation policy metadata.
- **Pain-Signal Eval Progression Gate** (`pain-signal-eval-progression-gate.md:28-50`) drives eval investment from real failure signals.
- **Flywheel daemon** (systemd, 60s loop) detects trace anomalies and triggers QI loop when `anomaly_score ≥ 80`.
- **FLYWHEEL_ALERT gate** in `AGENTS.md:343` injects findings into session context on next run.
- **SLO checker** with burn rate alerts provides operational health monitoring.

### What is missing

1. **No real-time eval quality dashboard**: no pass/fail rates per eval layer/category/agent surfaced as an always-on monitoring surface. The flywheel detects trace anomalies and operational failures — not eval quality regressions.
2. **No streaming eval results** feeding an always-on display. Eval results exist as batch computations in the flywheel loop, not as a continuous stream.
3. **No anomaly alerts keyed to eval quality regression thresholds**. Existing alerts are trace-anomaly-based (anomaly_score ≥ 80), not pass-rate-based (Layer 2 groundedness pass rate dropped from 92% to 81%).
4. **No drill-down from dashboard to individual trace**. The trace pipeline (`trace-instrumentation.md`) collects spans but no dashboard connects eval results to the traces that produced them.
5. **No CSAT correlation overlay** to validate that eval pass rate trends predict production satisfaction trends.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Quality regressions detected in minutes (via eval) instead of weeks (via CSAT) | Requires eval infrastructure to be always-on, not batch; streaming eval results adds infrastructure cost |
| The eval dashboard becomes the first place the team looks during an incident — not logs, not APM | Eval dashboard is only as good as the eval dataset feeding it — gaps in test coverage are gaps in visibility |
| Trend visibility catches slow degradation (e.g., embeddings gradually going stale) that binary alerts miss | High false-positive rate from Layer 2 (LLM-as-Judge) can create alert fatigue if thresholds are not calibrated |
| Drill-down from dashboard to individual trace enables rapid diagnosis without context-switching tools | Dashboard is a detection surface, not a diagnosis surface — it tells you quality dropped, but you still need traces to find why |

## Relationship to Other Patterns

- **Consumes from:** Eval Tier Stratification — each layer (fast/medium/deep) provides the pass/fail rates displayed on the dashboard.
- **Consumes from:** Production Failure Regression Flywheel — each new regression case added to the eval dataset becomes a new data point on the dashboard.
- **Validated by:** Eval-to-Production Correlation Tracking — the dashboard's CSAT overlay validates that eval pass rates predict production outcomes.
- **Enables:** Pain-Signal Eval Progression Gate — the dashboard makes pain signals visible (eval quality drops) that trigger eval infrastructure investment.
- **Depends on:** Trace Instrumentation — drill-down from dashboard pass/fail rate to individual query trace requires full trace coverage.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:233` — extracted pattern definition.
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:266` — Partial Coverage classification (P2, Medium).
- `scripts/telemetry/flywheel-health.sh:1` — flywheel health check with PASS/FAIL per component.
- `AGENTS.md:343` — FLYWHEEL_ALERT detection gate.
- `docs/canonical/eval-tier-stratification.md:28` — fast/medium/deep tier taxonomy with metadata contracts.
- `docs/canonical/production-failure-regression-flywheel.md:28` — failure-to-eval conversion.
- `docs/canonical/pain-signal-eval-progression-gate.md:28` — pain-signal-driven eval investment.
- `docs/canonical/trace-instrumentation.md:28` — trace pipeline components.

---

*Created: 2026-06-26 | From: Production AI Playbook classification (Batch B) | Precedence: canonical*
