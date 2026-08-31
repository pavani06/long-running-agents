---
title: "Artifacts Manifest: GTM AI Agents — Lessons from Deploying to 6,000 Users"
type: analysis
date: 2026-08-30
aliases: ["manifesto gtm-ai-agents-lessons-from-deploying-to-6000-users", "artifacts gtm-ai-agents-lessons-from-deploying-to-6000-users"]
tags: ["agentes-orquestracao", "evals", "production", "governanca"]
relates-to: ["[[docs/canonical/llm-classified-log-taxonomy|LLM-Classified Log Taxonomy]]", "[[docs/canonical/trial-retention-attribution-split|Trial-Retention Attribution Split]]"]
---

# Artifacts Manifest: GTM AI Agents — Lessons from Deploying to 6,000 Users

## Summary

| # | Pattern | Classification | Priority | Artifacts Created |
|---|---|---|---|---|
| 1 | LLM-Classified Log Taxonomy | Partial Coverage | P1 | canonical |
| 2 | Trial-Retention Attribution Split | Missing | P0 | canonical, skill, exercise |
| 3 | Agent Value Maturity Ladder | Missing | P0 | canonical, skill, exercise |
| 4 | Workflow-Derived Golden Question Set | Partial Coverage | P2 | canonical |
| 5 | Quality-Over-Coverage Trust Scoping | Partial Coverage | P2 | canonical |
| 6 | Retention-Gated Phased Rollout | Partial Coverage | P2 | canonical |
| 7 | Centralized Data Plane with Inherited RBAC | Partial Coverage | P2 | canonical |
| 8 | Human-Review Staged Workflow Automation | Partial Coverage | P2 | canonical |
| 9 | Pull-Based Infrastructure on Pain | Partial Coverage | P2 | canonical |
| 10 | Continuous Re-Architecture Budget | Partial Coverage | P2 | canonical |
| 11 | Gap-to-Content Feedback Circuit | Partial Coverage | P2 | canonical |
| 12 | Owner-Led Activation Blitz | Missing | P0 | canonical |

## Integration Map

| Artifact | Path | Updates |
|---|---|---|
| 12 canonical docs | `docs/canonical/*.md` (ver artifacts.yaml) | `system-of-record.md` -> tabelas dos dominios + contagem de padroes |
| trial-retention-attribution-split skill | `.opencode/skills/trial-retention-attribution-split/SKILL.md` | `system-of-record.md` -> tabela de skills |
| agent-value-maturity-ladder skill | `.opencode/skills/agent-value-maturity-ladder/SKILL.md` | `system-of-record.md` -> tabela de skills |
| exercise-09 trial-retention | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-09-trial-retention-attribution-split.md` | `curriculum/INDEX.md`, `curriculum/README.md`, `curriculum/MASTER_PLAN.md` |
| exercise-10 value ladder | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-10-agent-value-maturity-ladder.md` | `curriculum/INDEX.md`, `curriculum/README.md`, `curriculum/MASTER_PLAN.md` |

## Skipped

| Pattern | Reason |
|---|---|
| `Skill Library as Instruction-Overflow Valve` | Already Exists — [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] + biblioteca de 33 skills do proprio repo |
