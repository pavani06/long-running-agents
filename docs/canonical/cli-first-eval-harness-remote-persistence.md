---
title: "CLI-First Eval Harness with Remote Persistence"
type: canonical
aliases: ["cli-first evals", "harness com persistência remota", "eval history backend"]
tags: ["evals", "harness-engineering", "production", "harness", "agent-loop", "observability", "agentes-orquestracao"]
last_updated: 2026-08-31
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]]", "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]", "[[docs/canonical/agent-specific-data-freshness-pipeline|Agent-Specific Data Freshness Pipeline]]"]
sources: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]"]
---
# CLI-First Eval Harness with Remote Persistence

**Type:** canonical
**Status:** active
**Source:** Inside Clay's Eval Stack (LangChain; backend LangSmith na fonte, generalizado) — `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage — Integration value: Medium (P2)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Suites de eval que exigem provisioning em UI de plataforma — criar experimento, provisionar managed agent, configurar run — criam fricção que mata o uso. O desenvolvedor está no terminal; cada salto para uma UI para registrar um resultado é um ponto de abandono. O resultado prático: evals rodam menos do que deveriam, e quando rodam os resultados ficam espalhados em artefatos locais sem histórico comparável.

O problema tem duas metades: (a) ergonomia — o eval precisa rodar onde o dev já está; (b) durabilidade — todo resultado precisa parar num store central, versionado e consultável, ou não existe história contra a qual comparar.

## Solution

Combinar as duas metades numa arquitetura só:

1. **Suite de eval local, command-line first.** O ponto de entrada é um comando no terminal (`eval run`, `shadow-tests start`), não um wizard de plataforma. Sem provisioning em UI.
2. **Backend de persistência remota.** Todo resultado — inclusive de runs locais — é escrito automaticamente no store remoto ao final da execução; o write-out não é opcional nem manual.
3. **Versionamento no store.** Resultados carregam metadados (prompt version, harness version, suite, dataset) que permitem comparação across runs, prompts e desenvolvedores.
4. **Histórico consultável.** O store responde "como este prompt performou contra o baseline na semana passada?" sem re-run.

O contrato: o comando local retorna o resultado imediatamente (ergonomia local) E o registro é durável no backend (centralidade). Nenhuma das duas metades é negociável — só-local perde história, só-remoto perde o desenvolvedor.

## Implementation in this repo

### What already exists

O repo tem a primeira metade (CLI-first local) real e madura:

- `harness.sh` roda o loop de fases com contrato default-FAIL: "`test-results.json` — contrato default-FAIL; harness.sh só avança se evaluator der PASS" (`harness/GUIDE-analyze-and-improve.md:42`); `PROGRESS.md` mantém estado persistente com retomada automática (`:39,43`), loop em `:50-53`.
- O currículo ensina eval disparado por CLI sem UI: `koda shadow-tests start budget_guard_removal --env staging --duration 48h --sample 100` (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:1823`).
- Persistência local existe: artefatos de resultado em arquivos (`test-results.json`, `PROGRESS.md`) e telemetria SQLite local (`telemetry.db`, `docs/system-of-record.md:128`).

### What is missing

A segunda metade do padrão não existe em forma alguma:

1. Nenhum backend de persistência remota com write-out automático de todo resultado. NOT_FOUND: grep `LangSmith|remote persist|CLI-first|cli first` em `docs/` → apenas os arquivos do próprio pacote-fonte Clay.
2. Nenhum histórico versionado e comparável de runs de eval. O próprio repo documenta a ausência: [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] lista "Eval history | Eval run IDs, score distributions, suite/tier, rubric version..." como componente a ser adicionado (`docs/canonical/eval-to-production-correlation-tracking.md:34`), e a seção "What needs to be added" confirma que o sistema não existe (`:65-76`).

Add:

1. Um write path do harness para um store central (a telemetria SQLite local é o candidato natural de export).
2. Schema de run de eval versionado (run ID, prompt/harness version, suite, tier, scores, timestamps).
3. Comando de comparação contra histórico (baseline delta por run ID) no próprio CLI.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Remove fricção de provisioning em UI; eval roda onde o dev já está | Exige write path e conectividade com o store remoto |
| Combina ergonomia local com durabilidade e versionamento centrais numa só arquitetura | Riqueza local é menor que os recursos completos da plataforma |
| Histórico comparável across runs, prompts e desenvolvedores | O store remoto vira dependência para história e comparação |
| Habilita correlação eval↔produção com run IDs estáveis | Duplicação momentânea entre artefatos locais e store central precisa de política de verdade única |

## Relationship to Other Patterns

- **Prerequisite for:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — o "Eval history" com run IDs e distribuições é exatamente o componente listado como faltante.
- **Composes with:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — cada run carrega `tier` no metadata persistido.
- **Composes with:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]] — `PROGRESS.md` é o estado local; o store remoto é a memória de longo prazo.
- **Uses:** [[docs/canonical/trace-instrumentation|Trace Instrumentation]] — `telemetry.db` é a base local que o write-out exportaria.
- **Feeds:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — evolução medida do harness exige história de runs para comparar.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:80` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md` — §4, classificação Partial Coverage/Medium com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification-batch-1.md` — batch-fonte da classificação.
- `harness/GUIDE-analyze-and-improve.md:39,42,43,50-53` — contrato default-FAIL, estado persistente, loop do harness.
- `docs/canonical/eval-to-production-correlation-tracking.md:34,65-76` — Eval history como componente a ser adicionado.
- `docs/system-of-record.md:128` — telemetria SQLite local (não store remoto).

---

*Created: 2026-08-31 | From: Clay Eval Stack classification | Precedence: canonical*
