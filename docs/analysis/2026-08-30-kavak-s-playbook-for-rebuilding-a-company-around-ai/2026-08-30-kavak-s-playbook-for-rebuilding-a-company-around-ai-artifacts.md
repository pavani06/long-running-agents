---
title: "Artifacts Manifest: Kavak's Playbook for Rebuilding a Company Around AI"
type: analysis
date: 2026-08-30
aliases: ["manifesto kavak playbook", "artifacts kavak playbook"]
tags: [agentes-orquestracao, harness-engineering]
relates-to:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification|Classificação]]"
---

# Artifacts Manifest: Kavak's Playbook for Rebuilding a Company Around AI

## Summary

| # | Pattern | Classification | Priority | Artifacts Created |
|---|---|---|---|---|
| 1 | model-agnostic-agent-vm-harness | Partial Coverage | P1 | canonical doc |
| 2 | alarm-clock-agent-lifecycle | Partial Coverage | P1 | canonical doc |
| 3 | evals-as-brakes | Partial Coverage | P1 | canonical doc |
| 4 | carve-out-pilot-hard-target | Partial Coverage | P1 | canonical doc |
| 5 | mega-expert-consolidation | Missing | P0 | canonical doc |
| 6 | sidekick-pattern-physical-boundaries | Missing | P0 | canonical doc |
| 7 | agent-per-customer-outcome-ownership | Partial Coverage | P2 | canonical doc |
| 8 | goal-driven-agents-over-workflows | Partial Coverage | P2 | canonical doc |
| 9 | shared-fleet-learning | Partial Coverage | P2 | canonical doc |
| 10 | closed-loop-help-api | Partial Coverage | P2 | canonical doc |
| 11 | eval-investment-parity | Partial Coverage | P2 | canonical doc |
| 12 | outcome-level-eval-hierarchy | Partial Coverage | P2 | canonical doc |
| 13 | production-contact-training-loop | Partial Coverage | P2 | canonical doc |
| 15 | Mega-Expert Consolidation | Missing | P0 | skill + exercise |

## Integration Map

| Artifact | Path | Updates |
|---|---|---|
| 13 canonical docs | `docs/canonical/<slug>.md` | `docs/system-of-record.md` → tabela "Padrões canônicos ativos" |
| `mega-expert-consolidation` skill | `.opencode/skills/mega-expert-consolidation/SKILL.md` | `docs/system-of-record.md` → domínio agentes-orquestracao |
| `exercise-07-mega-expert-consolidation` exercise | `curriculum/03-nivel-3-advanced-architecture/exercises/` | `curriculum/INDEX.md`, `curriculum/README.md`, `curriculum/MASTER_PLAN.md` |

## Skipped

| Pattern | Reason |
|---|---|
| `Scaffold Deletion on Model Step-Change` | Better Implementation — repo tem measured-harness-evolution-lifecycle + model-switch-driven-eval-hardening (versão mais governada) |
