---
title: "Artifacts Manifest — Canary Test Code Review Patterns"
type: analysis
tags: [canary-test, artifact-manifest, evals, agentic-coding, governanca]
date: 2026-06-15
aliases: ["canary-test artifacts", "code review patterns artifacts"]
relates-to:
  - "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Classification]]"
  - "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]"
  - "[[docs/canonical/contextual-severity-calibration|Contextual Severity Calibration]]"
  - "[[docs/system-of-record|System of Record]]"
sources:
  - "sources/2026-06-15-canary-test-code-review-patterns.md"
---

# Artifacts Manifest — Canary Test Code Review Patterns

Manifesto de artefatos gerados pela Phase 4 (Improvement Generation) do pipeline
analyze-and-improve para a fonte `2026-06-15-canary-test-code-review-patterns.md`.

## Summary

| Category | Count |
|---|---|
| Canonical Docs | 4 |
| Skills | 2 |
| Exercises | 2 |
| **Total** | **8** |

## Canonical Docs

| # | Path | Pattern | Classification | Priority |
|---|---|---|---|---|
| 1 | [[docs/canonical/shadow-review-pipeline.md|shadow-review-pipeline]] | Shadow Review Pipeline | Missing | P0 |
| 2 | [[docs/canonical/contextual-severity-calibration.md|contextual-severity-calibration]] | Contextual Severity Calibration | Missing | P0 |
| 3 | [[docs/canonical/review-contract-checklist.md|review-contract-checklist]] | Review Contract Checklist | Partial Coverage | P1 |
| 4 | [[docs/canonical/pre-commit-ai-review-gate.md|pre-commit-ai-review-gate]] | Pre-Commit AI Review Gate | Partial Coverage | P1 |

## Skills

| # | Path | Pattern | Classification |
|---|---|---|---|
| 5 | `.opencode/skills/shadow-review-pipeline/SKILL.md` | Shadow Review Pipeline | Missing |
| 6 | `.opencode/skills/contextual-severity-calibration/SKILL.md` | Contextual Severity Calibration | Missing |

## Exercises

| # | Path | Pattern | Classification |
|---|---|---|---|
| 7 | [[curriculum/03-nivel-3-operational/exercises/exercise-shadow-review-pipeline\|exercise-shadow-review-pipeline]] | Shadow Review Pipeline | Missing |
| 8 | [[curriculum/03-nivel-3-operational/exercises/exercise-contextual-severity-calibration\|exercise-contextual-severity-calibration]] | Contextual Severity Calibration | Missing |

## Integration Map

Mapa conectando cada artefato criado aos índices que a Phase 5 deve atualizar:

| Artifact | System of Record | Curriculum INDEX | Curriculum MASTER_PLAN |
|---|---|---|---|
| shadow-review-pipeline (canonical) | +1 canonical doc | — | — |
| contextual-severity-calibration (canonical) | +1 canonical doc | — | — |
| review-contract-checklist (canonical) | +1 canonical doc | — | — |
| pre-commit-ai-review-gate (canonical) | +1 canonical doc | — | — |
| shadow-review-pipeline (skill) | +1 skill (Agentes) | — | — |
| contextual-severity-calibration (skill) | +1 skill (Agentes) | — | — |
| exercise-shadow-review-pipeline | — | +1 exercise Nivel 3 | +1 exercise count |
| exercise-contextual-severity-calibration | — | +1 exercise Nivel 3 | +1 exercise count |

## Skipped Patterns

Nenhum padrão foi skipped. Os 4 padrões da classificação geraram artefatos:

- 2 Missing (P0): canonical doc + skill + exercise para cada
- 2 Partial Coverage (P1): canonical doc para cada

## Gate

- [x] 4 canonical docs criados em `docs/canonical/`
- [x] 2 skills criados em `.opencode/skills/`
- [x] 2 exercises criados em `curriculum/03-nivel-3-operational/exercises/`
- [x] `scripts/check-obsidian-conventions.sh` passa com 0 errors
- [ ] Phase 5: atualizar `docs/system-of-record.md` (tabelas Skills + Canonical Docs)
- [ ] Phase 5: atualizar `curriculum/INDEX.md` (+2 exercises Nivel 3)
- [ ] Phase 5: atualizar `curriculum/MASTER_PLAN.md` (exercise count)
