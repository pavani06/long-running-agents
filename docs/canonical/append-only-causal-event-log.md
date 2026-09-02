---
title: "Append-Only Causal Event Log"
type: canonical
tags: ["tracing", "observability", "agentes-orquestracao", "production", "error-handling", "multi-agent", "harness-engineering"]
aliases: ["causal event log", "log causal append-only", "event sourcing de agentes", "log as memory", "publish-time causality"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]]"
  - "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]"
  - "[[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]"
  - "[[docs/canonical/asymmetric-failure-correction-router|Asymmetric Failure Correction Router]]"
  - "[[docs/canonical/emergent-event-topology|Emergent Event Topology]]"
  - "[[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Append-Only Causal Event Log

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P1, High integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Trabalho perdido entre passos e debugging impossivel com multiplos agentes: "mesmo com 3-4 agentes voce ja tem major debugging headaches" (analysis.md:139-140). O caso concreto do fonte: uma nota de voz sumiu porque nada era persistido entre passos do pipeline (analysis.md:88, :206).

O repo ja opera tracing centralizado e ensina logs de auditoria append-only, mas sem as duas mecanicas que definem este padrao: **ligacoes causais no nivel do evento, capturadas no momento do publish**, e **um unico destino append-only obrigatorio para todos os agentes e processos**. O `parent_span_id` do schema de tracing do repo e hierarquia de span, nao causalidade evento-a-evento (classification.md:64, :74).

## Solucao

Uma unica tabela/stream append-only como **destino obrigatorio** de todos os eventos publicados por todos os agentes e processos, com uma API comum de publish e causalidade registrada no momento do evento (analysis.md:141-144):

```jsonl
{"id": "evt_91", "ts": "...", "agent": "transcritor", "type": "voice-note.processed",
 "caused_by": ["evt_88"], "payload_ref": "..."}
{"id": "evt_92", "ts": "...", "agent": "daily-brief", "type": "brief.generated",
 "caused_by": ["evt_91", "evt_20"], "payload_ref": "..."}
{"id": "evt_93", "ts": "...", "agent": "slack-poster", "type": "slack.message.post.failed",
 "caused_by": ["evt_92"], "error_class": "duplicate_delivery"}
```

Regras load-bearing:

1. **Append-only, sem remocao nem alteracao** — o log e a memoria do sistema: "nada e perdido, tudo e observado" (analysis.md:143).
2. **Causalidade capturada no publish** (`caused_by`/`parent_event_id` entre eventos) — reconstrucao posterior da causalidade nao e confiavel; se nao foi registrada quando o evento aconteceu, nao existe (classification.md:79).
3. **Cadeia causal navegavel de qualquer falha de volta ao gatilho** — e a cadeia que torna o debug de multi-agente viavel, nao a mera cronologia (analysis.md:144).

A distincao contra tracing de spans: span hierarchy responde "quem chamou quem dentro de uma execucao"; causal event chain responde "qual evento do sistema disparou este evento", atravessando agentes, filas e schedules.

## Implementacao neste repositorio

### O que ja existe

- **Tracing centralizado operacional:** [[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]] define schema unificado `trace_id`/`span_id`/`parent_span_id` (`:28-55`) e o pipeline existente `tracer.ts` → `trace-state.json` → `collector.ts`/`telemetry.db` (`:123-130`) — hierarquia de span, sem causalidade evento-a-evento.
- **Convencao de audit log append-only no curriculum:** `audit_log.jsonl` definido como JSONL imutavel, eventos nunca alterados/removidos, timeline para post-mortem (classification.md:67); trace store ensinado como log cronologico imutavel com `started`/`completed` por agente (classification.md:68); implementacao `_log()` appendedo JSONL em modo `"a"` (classification.md:69); write-ahead logging e append-only exigidos em planning-execution graphs (classification.md:70) — tudo sem schema de causalidade entre eventos.
- **Ordem causal preservada em traces:** [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] trabalha traces com timestamps, params e sucesso/falha com "causal ordering" — preservacao de ordem de execucao, nao ligacao evento-a-evento (classification.md:72).
- **Especificacao de logs append-only de aprendizado:** [[docs/canonical/asymmetric-failure-correction-router|Asymmetric Failure Correction Router]] especifica dois logs "immutable append-only" (imitate/correct), declarados ausentes na implementacao (classification.md:73).

### O que falta

(classification.md:74) — NOT_FOUND de campos causais e destino unico; busca em `docs/canonical/`, `docs/decisions/`, `docs/evidence/`, `curriculum/`, `.opencode/`, `scripts/`:

1. **Campos causais capturados no publish** (`caused_by`, `parent_event_id`, `causal_links`) — nenhuma implementacao ou especificacao existente.
2. **Tabela/stream append-only unico como destino obrigatorio** de todos os agentes e processos, com API comum de publish.
3. **Reconstrucao queryavel de falha para tras ate o evento gatilho** — nenhuma ferramenta navega a cadeia causal (que nem existe como dado).
4. **Equivalente em `.opencode/` ou `scripts/`** — o pipeline `telemetry.db` nao carrega causalidade de eventos.

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Elimina trabalho perdido: tudo salvo para sempre | Volume de armazenamento cresce sem remocao |
| Debug viavel: da falha de volta ao gatilho pela cadeia causal | Exige disciplina de publicacao: o valor do log depende de TODO evento ser publicado |
| Substrato para topologia emergente, auditoria e unattended operation | Causalidade precisa ser capturada no momento do evento; reconstrucao posterior nao e confiavel |

## Relacao com outros padroes

- **Estende:** [[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]] e [[docs/canonical/trace-instrumentation|Trace Instrumentation]] — o delta e incremental sobre infra existente: adicionar campos de causalidade no publish e a disciplina log-as-memory (classification.md:76).
- **Alimenta:** [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] — traces com causalidade real, nao apenas ordem.
- **Implementa a persistencia que:** [[docs/canonical/asymmetric-failure-correction-router|Asymmetric Failure Correction Router]] assume para seus logs de aprendizado.
- **E substrato de:** [[docs/canonical/emergent-event-topology|Emergent Event Topology]] (a topologia so existe no que o log diz que aconteceu) e pre-requisito para a operacao unattended em [[docs/canonical/presence-interface-ladder|Presence Interface Ladder]].
- **E o journal de:** [[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]] — journaling (log + definicao do agente) e uma das tres responsabilidades do kernel.

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:137-144` — log append-only com causalidade; o log e a memoria do sistema.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:86-90, :206` — falha "nota de voz sumiu" e a peca de runtime que nasceu dela.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:61-79` — padrao 3 extraido: inputs, outputs, beneficios, limitacoes.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:60-76` — classificacao Partial Coverage (High) com evidencia file:line e NOT_FOUND.
- [[docs/canonical/centralized-cross-framework-tracing|Centralized Cross-Framework Tracing]]`:28-55, :123-130` — schema unificado de tracing e pipeline telemetry.db existente.
