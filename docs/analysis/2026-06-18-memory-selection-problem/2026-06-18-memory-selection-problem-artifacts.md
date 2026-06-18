---
title: "Artifacts Manifest: Memory Selection Problem"
type: analysis
date: 2026-06-18
aliases: ["manifesto memory-selection", "artifacts memory-selection"]
tags: ["analise", "agentes-orquestracao", "context-engineering"]
relates-to:
  - "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification|Classificação]]"
  - "[[docs/system-of-record|System of Record]]"
---

# Artifacts Manifest: Memory Selection Problem

Fonte: `raw-knowledge/sources/2026-06-17-your-ai-agents-don't-have-a-memory-problem.-they-have-a-sele.md`

## Summary

| # | Pattern | Classification | Priority | Artifacts Created |
|---|---|---|---|---|
| 1 | Tiered Context Storage with Promotion/Demotion | Missing | P0 | canonical, skill, exercise |
| 2 | Neutral Selection Layer | Missing | P0 | canonical, skill, exercise |
| 3 | Selection-Budgeted Retrieval | Missing | P0 | canonical, skill, exercise |
| 4 | Deliberate Forgetting | Partial Coverage | P1 | canonical |
| 5 | Smallest Sufficient Context | Partial Coverage | P1 | canonical |
| 6 | Relational Context Graph | Partial Coverage | P1 | canonical |
| 7 | Context Health Monitoring | Partial Coverage | P1 | canonical |
| 8 | Agent Degradation Loop Prevention | Partial Coverage | P1 | canonical |

**Total: 8 canonical docs + 3 skills + 3 exercises = 14 artifacts**

## Integration Map

| Artifact | Path | Updates |
|---|---|---|
| Tiered Context Storage canonical | `docs/canonical/tiered-context-storage.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Neutral Selection Layer canonical | `docs/canonical/neutral-selection-layer.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Selection-Budgeted Retrieval canonical | `docs/canonical/selection-budgeted-retrieval.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Deliberate Forgetting canonical | `docs/canonical/deliberate-forgetting.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Smallest Sufficient Context canonical | `docs/canonical/smallest-sufficient-context.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Relational Context Graph canonical | `docs/canonical/relational-context-graph.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Context Health Monitoring canonical | `docs/canonical/context-health-monitoring.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Agent Degradation Loop Prevention canonical | `docs/canonical/agent-degradation-loop-prevention.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Tiered Context Storage skill | `.opencode/skills/tiered-context-storage/SKILL.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Neutral Selection Layer skill | `.opencode/skills/neutral-selection-layer/SKILL.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Selection-Budgeted Retrieval skill | `.opencode/skills/selection-budgeted-retrieval/SKILL.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Tiered Context Storage exercise | `curriculum/05-core-concepts/exercises/exercise-tiered-context-storage.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| Neutral Selection Layer exercise | `curriculum/05-core-concepts/exercises/exercise-neutral-selection-layer.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| Selection-Budgeted Retrieval exercise | `curriculum/05-core-concepts/exercises/exercise-selection-budgeted-retrieval.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |

## Skipped

Nenhum — todos os 8 padrões requeriam artefatos (nenhum Already Exists ou Better Implementation).

## Notes

- system-of-record.md foi atualizado com as 8 novas entradas de canonical docs durante a Phase 4a
- Os 3 skills seguem o formato exato dos skills existentes (frontmatter, What I Do, Anti-Pattern, Pattern, Quality Gates)
- Os 3 exercises estão no nível N3 (Arquitetura Avançada) com skeleton code Python, acceptance criteria e rubrica
- Validação `validate-obsidian.ts` passou em todos os checks para os novos arquivos
