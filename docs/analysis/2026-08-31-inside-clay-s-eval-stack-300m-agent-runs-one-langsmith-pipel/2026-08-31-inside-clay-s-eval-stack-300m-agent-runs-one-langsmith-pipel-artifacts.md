---
title: "Artifacts Manifest: Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline"
type: analysis
date: 2026-08-31
aliases: ["manifesto clay eval stack", "artifacts clay eval stack"]
tags: ["analise", "evals", "roadmap"]
relates-to: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification|Classificacao]]"]
---

# Artifacts Manifest: Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline

## Summary

| #   | Pattern                                          | Classification   | Priority | Artifacts Created          |
| --- | ------------------------------------------------ | ---------------- | -------- | -------------------------- |
| 1   | perceived-eval                                   | Missing          | P0       | canonical, skill, exercise |
| 2   | eval-coverage-matrix                             | Partial Coverage | P1       | canonical, exercise        |
| 3   | production-to-offline-feedback-loop              | Partial Coverage | P1       | canonical, exercise        |
| 4   | unified-tool-surface-flywheel                    | Partial Coverage | P1       | canonical, exercise        |
| 5   | agent-first-data-foundation                      | Partial Coverage | P1       | canonical, exercise        |
| 6   | bulk-in-context-trace-analysis                   | Partial Coverage | P1       | canonical, exercise        |
| 7   | self-iterating-agent-loop                        | Partial Coverage | P1       | canonical, exercise        |
| 8   | environment-tiered-eval-fidelity                 | Partial Coverage | P2       | canonical                  |
| 9   | cli-first-eval-harness-remote-persistence        | Partial Coverage | P2       | canonical                  |
| 10  | plug-and-play-eval-harness-byo-evaluators        | Partial Coverage | P2       | canonical                  |
| 11  | structured-partial-checks-exact-goldens          | Partial Coverage | P2       | canonical                  |
| 12  | deterministic-multi-turn-scripts-simulated-users | Partial Coverage | P2       | canonical                  |
| 13  | shadow-builds-separated-compute                  | Partial Coverage | P2       | canonical                  |
| 14  | skills-cli-native-agent-data-access              | Partial Coverage | P2       | canonical                  |
| 15  | observability-threshold-eval-trigger             | Partial Coverage | P2       | canonical                  |
| 16  | eval-gated-autonomy                              | Already Exists   | -        | nenhum (skip)              |

## Integration Map

| Artifact | Path | Updates |
|---|---|---|
| `perceived-eval` canonical | `docs/canonical/perceived-eval.md` | `system-of-record.md` -> dominio `evals` |
| `eval-coverage-matrix` canonical | `docs/canonical/eval-coverage-matrix.md` | `system-of-record.md` -> dominio `evals` |
| `production-to-offline-feedback-loop` canonical | `docs/canonical/production-to-offline-feedback-loop.md` | `system-of-record.md` -> dominio `evals` |
| `unified-tool-surface-flywheel` canonical | `docs/canonical/unified-tool-surface-flywheel.md` | `system-of-record.md` -> dominio `evals` |
| `agent-first-data-foundation` canonical | `docs/canonical/agent-first-data-foundation.md` | `system-of-record.md` -> dominio `evals` |
| `bulk-in-context-trace-analysis` canonical | `docs/canonical/bulk-in-context-trace-analysis.md` | `system-of-record.md` -> dominio `evals` |
| `self-iterating-agent-loop` canonical | `docs/canonical/self-iterating-agent-loop.md` | `system-of-record.md` -> dominio `evals` |
| `environment-tiered-eval-fidelity` canonical | `docs/canonical/environment-tiered-eval-fidelity.md` | `system-of-record.md` -> dominio `evals` |
| `cli-first-eval-harness-remote-persistence` canonical | `docs/canonical/cli-first-eval-harness-remote-persistence.md` | `system-of-record.md` -> dominio `evals` |
| `plug-and-play-eval-harness-byo-evaluators` canonical | `docs/canonical/plug-and-play-eval-harness-byo-evaluators.md` | `system-of-record.md` -> dominio `evals` |
| `structured-partial-checks-exact-goldens` canonical | `docs/canonical/structured-partial-checks-exact-goldens.md` | `system-of-record.md` -> dominio `evals` |
| `deterministic-multi-turn-scripts-simulated-users` canonical | `docs/canonical/deterministic-multi-turn-scripts-simulated-users.md` | `system-of-record.md` -> dominio `evals` |
| `shadow-builds-separated-compute` canonical | `docs/canonical/shadow-builds-separated-compute.md` | `system-of-record.md` -> dominio `evals` |
| `skills-cli-native-agent-data-access` canonical | `docs/canonical/skills-cli-native-agent-data-access.md` | `system-of-record.md` -> dominio `evals` |
| `observability-threshold-eval-trigger` canonical | `docs/canonical/observability-threshold-eval-trigger.md` | `system-of-record.md` -> dominio `evals` |
| `perceived-eval` skill | `.opencode/skills/perceived-eval/SKILL.md` | `system-of-record.md` -> skills |
| `perceived-eval` exercise | `curriculum/02-nivel-2-practical-patterns/exercises/exercise-06-perceived-eval.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| `eval-coverage-matrix` exercise | `curriculum/02-nivel-2-practical-patterns/exercises/exercise-07-eval-coverage-matrix.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| `production-to-offline-feedback-loop` exercise | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-13-production-offline-drift-taxonomy.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| `unified-tool-surface-flywheel` exercise | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-14-unified-tool-surface-flywheel.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| `agent-first-data-foundation` exercise | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-15-agent-first-data-foundation.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| `bulk-in-context-trace-analysis` exercise | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-16-bulk-in-context-trace-analysis.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| `self-iterating-agent-loop` exercise | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-17-self-iterating-agent-loop.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |

## Skipped

| Pattern | Reason |
|---|---|
| `eval-gated-autonomy` | Already Exists, Integration Value Low — o repo ja documenta e ensina eval-gated delegation com profundidade equivalente |
