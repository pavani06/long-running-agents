---
title: Trace Instrumentation
type: canonical
tags:
  - tracing
  - telemetry
  - observability
  - runtime
aliases:
  - Trace Instrumentation
  - tracer wiring
  - task-wrapper
  - trace-cli
relates-to:
  - "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]"
  - "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]"
---

# Trace Instrumentation

## Propósito

Padrão canônico para instrumentar toda chamada `task()` no runtime Sisyphus com spans de trace, garantindo que cada delegação produza um `trace_id` no `telemetry.db`. Resolve o problema de adesão comportamental do orquestrador: spans só existem se o agente executar `task-wrapper.sh` antes e depois de cada `task()`.

## Componentes

| Componente | Path | Responsabilidade |
|---|---|---|
| `tracer.ts` | `~/scripts/telemetry/tracer.ts` | Core: state machine de spans (start/end/dump/clear). 352 linhas, 10/10 testes. |
| `trace-cli.ts` | `~/scripts/telemetry/trace-cli.ts` | CLI wrapper para `tracer.ts`. Persiste estado em `/tmp/trace-state.json`. 7/7 testes. |
| `task-wrapper.sh` | `~/scripts/telemetry/task-wrapper.sh` | Wrapper bash que encapsula `trace-cli.ts`. 3 modos: `--start-only`, `--end-last`, `--wrap`. 8/8 testes. |
| `collect-session.sh` | `~/scripts/telemetry/collect-session.sh` | Bridge: dump de spans → merge no session JSON → collector.ts. |
| `session-end-hook.sh` | `~/scripts/telemetry/session-end-hook.sh` | Hook pós-sessão: coleta + trace coverage check. |
| `collector.ts` | `~/scripts/telemetry/collector.ts` | Persistência em SQLite (`telemetry.db`). |

## Modos de Uso

### Modo Preciso (start antes, end depois — recomendado)

```bash
# ANTES da task()
SPAN_ID=$(bash ~/scripts/telemetry/task-wrapper.sh --start-only \
  --category "deep" \
  --subagent-type "explore" \
  --skills "review-work,debugging" \
  --description "Review auth module")
START_MS=$(date +%s%3N)

# ... executa task() ...

# DEPOIS da task()
END_MS=$(date +%s%3N)
bash ~/scripts/telemetry/task-wrapper.sh --end-last \
  --success true \
  --duration-ms $((END_MS - START_MS)) \
  --tokens 5000 \
  --model "deepseek-v4-pro"
```

### Modo Wrap (chamada única após task — conveniência)

```bash
# DEPOIS da task()
bash ~/scripts/telemetry/task-wrapper.sh --wrap \
  --category "deep" \
  --subagent-type "explore" \
  --description "Review auth module" \
  --success true \
  --duration-ms 1500 \
  --tokens 5000
```

## Enforcement (3 Camadas)

1. **Instrução**: `AGENTS.md` → `## Trace Instrumentation Gate` (junto aos gates de pré-delegação)
2. **Warning pós-sessão**: `session-end-hook.sh` → trace coverage check no `telemetry.db`
3. **Health check cross-session**: `canonical-context` → `## Trace Health Check` consulta últimas 5 sessões

## Limitação Conhecida (W5)

O trace coverage check em `session-end-hook.sh` consulta `task_calls` no banco. Na arquitetura atual, `collector.ts` popula `task_calls` exclusivamente de `trace_spans`, portanto toda `task_call` tem `trace_id`. O warning `TRACED=0 && TOTAL!=0` só dispara se outra fonte popular `task_calls` sem `trace_id` (ex: metadados de sessão do OpenCode).

## Testes

```bash
cd ~/scripts/telemetry && node --import tsx --test test/task-wrapper.test.ts   # 8 testes
cd ~/scripts/telemetry && node --import tsx --test test/trace-cli.test.ts      # 7 testes
cd ~/scripts/telemetry && node --import tsx --test test/tracer.test.ts         # 10 testes
```

## Ver também

- `AGENTS.md` → `## Trace Instrumentation Gate`
- `budget-monitor/SKILL.md` → `## Trace Instrumentation`
- `canonical-context/SKILL.md` → `## Trace Health Check`
- Plano: `.omo/plans/2026-06-19-trace-auto-instrumentation.md`
- Plano: `.omo/plans/2026-06-19-gap9-tracer-wiring.md`