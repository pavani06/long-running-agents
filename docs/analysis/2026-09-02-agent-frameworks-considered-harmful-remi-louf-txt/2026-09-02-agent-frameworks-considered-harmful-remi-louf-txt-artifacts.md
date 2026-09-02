---
title: "Artifacts Manifest: Agent Frameworks Considered Harmful (Remi Louf, .txt)"
type: analysis
date: 2026-09-02
aliases: ["manifesto agent frameworks considered harmful", "artifacts remi louf 2026-09-02"]
tags: ["agentes-orquestracao", "harness-engineering", "curriculo-conteudo"]
relates-to: ["[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns|Patterns]]", "[[docs/system-of-record|System of Record]]"]
---

# Artifacts Manifest: Agent Frameworks Considered Harmful (Remi Louf, .txt)

## Summary

| # | Pattern | Classification | Priority | Artifacts Created |
|---|---|---|---|---|
| 1 | Typed Tool and Event Boundaries | Partial Coverage | P1 | canonical + exercise |
| 2 | Content-Addressed Prompt Graph | Partial Coverage | P1 | canonical + exercise |
| 3 | Append-Only Causal Event Log | Partial Coverage | P1 | canonical + exercise |
| 4 | Emergent Event Topology | Partial Coverage | P2 | canonical |
| 5 | Agent as Declarative File | Partial Coverage | P2 | canonical |
| 6 | Agent Kernel Runtime | Partial Coverage | P1 | canonical + exercise |
| 7 | Cron plus Typed Events Orchestration Surface | Partial Coverage | P2 | canonical |
| 8 | Failure-Accrued Runtime Growth | Partial Coverage | P2 | canonical |
| 9 | Presence-in-the-Loop Interface Ladder | Partial Coverage | P2 | canonical |

## Integration Map

| Artifact | Path | Updates |
|---|---|---|
| `typed-event-boundaries` canonical | `docs/canonical/typed-event-boundaries.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| `content-addressed-prompt-graph` canonical | `docs/canonical/content-addressed-prompt-graph.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| `append-only-causal-event-log` canonical | `docs/canonical/append-only-causal-event-log.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| `emergent-event-topology` canonical | `docs/canonical/emergent-event-topology.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| `agent-as-declarative-file` canonical | `docs/canonical/agent-as-declarative-file.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| `agent-kernel-runtime` canonical | `docs/canonical/agent-kernel-runtime.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| `cron-plus-typed-events-orchestration` canonical | `docs/canonical/cron-plus-typed-events-orchestration.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| `failure-accrued-runtime-growth` canonical | `docs/canonical/failure-accrued-runtime-growth.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| `presence-interface-ladder` canonical | `docs/canonical/presence-interface-ladder.md` | `system-of-record.md` → domínio `agentes-orquestracao` |
| Exercise 18 | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-18-typed-event-boundaries.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| Exercise 19 | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-19-content-addressed-prompt-graph.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| Exercise 20 | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-20-causal-event-log.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |
| Exercise 21 | `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-21-agent-kernel-runtime.md` | `INDEX.md`, `README.md`, `MASTER_PLAN.md` |

## Skipped

| Pattern/Artifact | Reason |
|---|---|
| skills (todos os padrões) | 0 padrões Missing — skills são artefatos exclusivos de Missing (P0) |
| exercises para P2 (4, 5, 7, 8, 9) | P2 recebe canonical doc; exercise é opcional e não foi criado |
| Already Exists / Better Implementation | Nenhum padrão nessas categorias nesta fonte |
