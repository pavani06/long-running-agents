---
title: "Artifacts Manifest: Production AI Playbook"
type: analysis
date: 2026-06-26
aliases: ["manifesto production AI playbook", "artifacts Bhaumik"]
tags: ["analise", "roadmap", "agentes-orquestracao", "evals", "production", "governanca"]
relates-to:
  - "[[docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification|Classificação]]"
---

# Artifacts Manifest: Production AI Playbook

> **Source**: 13 patterns from Sandipan Bhaumik's "The Production AI Playbook: Deploying Agents at Enterprise Scale"
> **Date**: 2026-06-26

## Summary

| # | Pattern | Classification | Priority | Artifacts Created |
|---|---|---|---|---|
| 1 | 3-Layer Evaluation Architecture | Partial Coverage | P1 | canonical doc |
| 2 | Eval-Driven Development Timeline | Partial Coverage | P2 | canonical doc |
| 3 | Living Eval Dataset | Partial Coverage | P1 | canonical doc |
| 4 | Behavioral Eval Path Analysis | Missing | P0 | canonical doc |
| 5 | Centralized Cross-Framework Tracing | Partial Coverage | P2 | canonical doc |
| 6 | Prompt-as-Code with Causal Change Management | Partial Coverage | P2 | canonical doc |
| 7 | Eval Dashboard as Primary Detection Surface | Partial Coverage | P2 | canonical doc |
| 8 | Multi-Agent Fault Tolerance | Partial Coverage | P1 | canonical doc |
| 9 | Agent-Specific Data Freshness Pipeline | Missing | P0 | canonical doc |
| 10 | Governance Context Injection for PII Prevention | Missing | P0 | canonical doc |
| 11 | Business-Outcome-First Eval Pipeline | Partial Coverage | P2 | canonical doc |
| 12 | Model-Switching Architecture with Enterprise Eval Gate | Partial Coverage | P2 | canonical doc |
| 13 | Behavioral Eval Path Analysis | Missing | P0 | canonical + skill + exercise |

**Totals**: 12 canonical docs, 1 skill(s), 1 exercise(s)

## Integration Map

| Artifact | Path | Updates |
|---|---|---|
| 3-Layer Evaluation Architecture canonical doc | `long-running-agents/docs/canonical/3-layer-evaluation-architecture.md` | `system-of-record.md` → domínio correspondente |
| Eval-Driven Development Timeline canonical doc | `long-running-agents/docs/canonical/eval-driven-development-timeline.md` | `system-of-record.md` → domínio correspondente |
| Living Eval Dataset canonical doc | `long-running-agents/docs/canonical/living-eval-dataset.md` | `system-of-record.md` → domínio correspondente |
| Behavioral Eval Path Analysis canonical doc | `long-running-agents/docs/canonical/behavioral-eval-path-analysis.md` | `system-of-record.md` → domínio correspondente |
| Centralized Cross-Framework Tracing canonical doc | `long-running-agents/docs/canonical/centralized-cross-framework-tracing.md` | `system-of-record.md` → domínio correspondente |
| Prompt-as-Code with Causal Change Management canonical doc | `long-running-agents/docs/canonical/prompt-as-code-causal-change-management.md` | `system-of-record.md` → domínio correspondente |
| Eval Dashboard as Primary Detection Surface canonical doc | `long-running-agents/docs/canonical/eval-dashboard-primary-detection-surface.md` | `system-of-record.md` → domínio correspondente |
| Multi-Agent Fault Tolerance canonical doc | `long-running-agents/docs/canonical/multi-agent-fault-tolerance.md` | `system-of-record.md` → domínio correspondente |
| Agent-Specific Data Freshness Pipeline canonical doc | `long-running-agents/docs/canonical/agent-specific-data-freshness-pipeline.md` | `system-of-record.md` → domínio correspondente |
| Governance Context Injection for PII Prevention canonical doc | `long-running-agents/docs/canonical/governance-context-injection-pii-prevention.md` | `system-of-record.md` → domínio correspondente |
| Business-Outcome-First Eval Pipeline canonical doc | `long-running-agents/docs/canonical/business-outcome-first-eval-pipeline.md` | `system-of-record.md` → domínio correspondente |
| Model-Switching Architecture with Enterprise Eval Gate canonical doc | `long-running-agents/docs/canonical/model-switching-architecture-enterprise-eval-gate.md` | `system-of-record.md` → domínio correspondente |
| Behavioral Eval Path Analysis skill | `.opencode/skills/behavioral-eval-path-analysis/SKILL.md` | `system-of-record.md` → agentes e orquestração |
| Behavioral Eval Path Analysis exercise | `long-running-agents/curriculum/04-nivel-3-engenharia-avancada/exercises/exercise-behavioral-eval-path-analysis.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |

## Skipped

| Pattern | Reason |
|---|---|
| Production Incident to Eval Flywheel | Already Exists — repo has production-failure-regression-flywheel canonical doc + flywheel daemon implementation |

## Canonical Docs Created

- [[docs/canonical/3-layer-evaluation-architecture.md|3-Layer Evaluation Architecture]] — Partial Coverage (P1)
- [[docs/canonical/eval-driven-development-timeline.md|Eval-Driven Development Timeline]] — Partial Coverage (P2)
- [[docs/canonical/living-eval-dataset.md|Living Eval Dataset]] — Partial Coverage (P1)
- [[docs/canonical/behavioral-eval-path-analysis.md|Behavioral Eval Path Analysis]] — Missing (P0)
- [[docs/canonical/centralized-cross-framework-tracing.md|Centralized Cross-Framework Tracing]] — Partial Coverage (P2)
- [[docs/canonical/prompt-as-code-causal-change-management.md|Prompt-as-Code with Causal Change Management]] — Partial Coverage (P2)
- [[docs/canonical/eval-dashboard-primary-detection-surface.md|Eval Dashboard as Primary Detection Surface]] — Partial Coverage (P2)
- [[docs/canonical/multi-agent-fault-tolerance.md|Multi-Agent Fault Tolerance]] — Partial Coverage (P1)
- [[docs/canonical/agent-specific-data-freshness-pipeline.md|Agent-Specific Data Freshness Pipeline]] — Missing (P0)
- [[docs/canonical/governance-context-injection-pii-prevention.md|Governance Context Injection for PII Prevention]] — Missing (P0)
- [[docs/canonical/business-outcome-first-eval-pipeline.md|Business-Outcome-First Eval Pipeline]] — Partial Coverage (P2)
- [[docs/canonical/model-switching-architecture-enterprise-eval-gate.md|Model-Switching Architecture with Enterprise Eval Gate]] — Partial Coverage (P2)

## Skills Created

- `.opencode/skills/behavioral-eval-path-analysis/SKILL.md` — Behavioral Eval Path Analysis (Missing)

## Exercises Created

- `curriculum/04-nivel-3-engenharia-avancada/exercises/exercise-behavioral-eval-path-analysis.md` — Behavioral Eval Path Analysis (Missing)
