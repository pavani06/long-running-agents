---
title: "Artifacts Manifest: The Prompting Playbook"
type: analysis
date: 2026-09-02
aliases: ["manifesto the prompting playbook", "artifacts the prompting playbook"]
tags: ["agentes-orquestracao", "harness-engineering", "evals", "curriculo-conteudo"]
relates-to: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-classification|Classification: The Prompting Playbook]]", "[[docs/system-of-record|System of Record]]"]
last_updated: 2026-09-02
---

# Artifacts Manifest: The Prompting Playbook

## Summary

| # | Pattern | Classification | Priority | Artifacts Created |
|---|---|---|---|---|
| 1 | Eval-Gated Model Migration Diagnostic | Partial Coverage | P2 | canonical |
| 2 | Control/Edge/Boundary Eval Taxonomy | Partial Coverage | P2 | canonical |
| 3 | Structural Prompt Hygiene | Partial Coverage | P2 | canonical |
| 4 | Defensive Patch Ledger | Partial Coverage (High) | P1 | canonical, exercise |
| 5 | Two-Sided Trade-off Instruction | Missing | P0 | canonical, skill, exercise |
| 6 | Capability Escalation Ladder | Missing | P0 | canonical, skill, exercise |
| 7 | Hard/Soft Constraint Grader Split | Partial Coverage | P2 | canonical |
| 8 | Two-Layer Output Contract | Partial Coverage | P2 | canonical |
| 9 | Tool Integration Triad | Partial Coverage (Low) | — | skipped (cross-reference only) |
| 10 | Generate-Evaluate-Repair Loop | Partial Coverage | P2 | canonical |
| 11 | Ban-to-Source-of-Truth Rebalancing | Partial Coverage | P2 | canonical |
| 12 | Self-Check Reasoning Instruction | Better Implementation | — | skipped (repo superior) |

Totals: 10 canonical docs, 2 skills, 3 exercises, 0 examples.

## Integration Map

| Artifact | Path | Updates |
|---|---|---|
| 10 canonical docs | `docs/canonical/*.md` (see .yaml manifest) | `system-of-record.md` → domínio "Agentes e orquestração" (tabela de padrões canônicos ativos + contagem 185 → 195) |
| `two-sided-trade-off-instruction` skill | `.opencode/skills/two-sided-trade-off-instruction/SKILL.md` | `system-of-record.md` → skill inventory (36 → 38) |
| `capability-escalation-ladder` skill | `.opencode/skills/capability-escalation-ladder/SKILL.md` | `system-of-record.md` → skill inventory (36 → 38) |
| `exercise-08-defensive-patch-ledger` | `curriculum/02-nivel-2-practical-patterns/exercises/` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| `exercise-09-two-sided-trade-off-instruction` | `curriculum/02-nivel-2-practical-patterns/exercises/` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| `exercise-22-capability-escalation-ladder` | `curriculum/03-nivel-3-advanced-architecture/exercises/` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |

## Skipped

| Pattern | Reason |
|---|---|
| `Self-Check Reasoning Instruction` | Better Implementation — repo externaliza verificação via Generator-Evaluator (self-eval detecta ~3% dos erros) e o próprio source mostra o rung de instrução estagnar em 2/5 antes de migrar para o loop; diagnóstico de truncation (budget failure) já coberto pelo currículo de token budgeting |
| `Tool Integration Triad` | Partial Coverage com Integration Value Low — pernas schema + implementação determinística já cobertas por `deterministic-tool-dispatch` (construído sobre o structured output contract); cross-reference apenas |
