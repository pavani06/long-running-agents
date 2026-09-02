---
title: "Cron plus Typed Events Orchestration Surface"
type: canonical
tags: ["agentes-orquestracao", "harness-engineering", "production", "multi-agent"]
aliases: ["cron plus typed events", "quando e porque", "two-axis orchestration", "superficie de orquestracao declarativa", "schedules plus events"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]"
  - "[[docs/canonical/typed-event-boundaries|Typed Event Boundaries]]"
  - "[[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]"
  - "[[docs/canonical/agent-as-declarative-file|Agent as Declarative File]]"
  - "[[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]]"
  - "[[docs/canonical/emergent-event-topology|Emergent Event Topology]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Cron plus Typed Events Orchestration Surface

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Camadas adicionais de orquestracao — grafos de agentes em codigo, workflows de framework — existem para expressar duas coisas simples: **quando** um agente roda e **porque** ele rodou (patterns.md:142).

O repo ensina os dois eixos separados: o eixo "quando" tem canonical proprio (alarm-clock) e scheduler nativo na arquitetura de referencia KODA; o eixo "porque" e ensinado como choreography/event-driven pub/sub no curriculum. O que nao existe e a **composicao como superficie completa**: a claim de que cron + eventos tipados substituem a camada inteira de orquestracao — "isso e a interface — voce nao escreve codigo, e esse e o produto inteiro" (analysis.md:65-66) — com agentes declarativos assinando schedules e assinaturas de eventos (classification.md:143, :150).

## Solucao

Duas primitivas baratas como a superficie declarativa completa de orquestracao (analysis.md:53-66):

| Eixo | Primitiva | Cobre | Exemplos |
|---|---|---|---|
| Quando | Cron (schedule) | Pontos no tempo | market watch todo dia de manha |
| Porque | Eventos tipados | Reatividade a mudanca do mundo | nova nota de voz, novo email, entrada no CRM, PR aberto/mergeado |

Regras da composicao:

1. **Nenhuma camada de orquestracao alem das duas primitivas.** O sistema de agentes inteiro do fonte foi descrito como `arquivo markdown por agente + cron (quando) + eventos tipados (por que)` — "nao ha camada de orquestracao adicional" (analysis.md:57-66).
2. **Cron isolado e explicitamente insuficiente**: e so um ponto no tempo, nao reatividade (analysis.md:63-64; patterns.md:156). A composicao dos dois eixos e o que cobre o espaco.
3. **A assinatura vive no arquivo declarativo do agente** — schedules e assinaturas de evento como campos (ver [[docs/canonical/agent-as-declarative-file|Agent as Declarative File]]).
4. **"Good old software orchestration"**: nada novo sob o sol — filas e eventos classicos de orquestracao de software (analysis.md:93-94; patterns.md:153).

A dependencia explicita: a composicao so funciona com eventos tipados (schemas), senao vira spaghetti de payloads (patterns.md:157) — por isso este padrao depende de [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]].

## Implementacao neste repositorio

### O que ja existe

- **Eixo "quando" canonizado:** [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]:30-38 — as opcoes quebradas, incluindo "External orchestrator polls" como anti-pattern; `:44` — "This is the scheduling primitive for the fleet".
- **Scheduler nativo na arquitetura de referencia:** o KODA tem scheduler proprio — "E por que tem um cron job? O KODA ja tem um scheduler..." (classification.md:147); o exercicio de presence marca cron job como "REDUNDANTE (deveria usar scheduler KODA)" (classification.md:147).
- **Eixo "porque" ensinado:** choreography com eventos de dominio disparando reacoes assincronas e Event Bus pub/sub no curriculum (classification.md:148).
- **Stance anti-grafo vizinha:** [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]] rejeita workflow DAG como unidade de especificacao (`:27-33`) e sustenta "goals age better than orchestration graphs" (`:88`) — conclusao vizinha por argumento diferente (goals, nao eventos).

### O que falta

(classification.md:150) — buscas por `cron|schedule|typed events|orchestration surface` retornam so os ingredientes; o alarm-clock canonical registra que o scheduler como primitiva propria sequer existia antes dele (doc-level only, sem codigo):

1. **A composicao dos dois eixos como superficie declarativa completa** — a formalizacao de que cron + eventos tipados substituem a camada de orquestracao, com agentes declarativos assinando ambos.
2. **A limitacao explicita do cron isolado** como regra de design (ponto no tempo, nao reatividade).
3. **A claim de completude de produto** ("voce nao escreve codigo, e esse e o produto inteiro") como posicao ensinavel, com a dependencia de eventos tipados nomeada.

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Duas primitivas baratas substituem a camada de framework inteira | Cron isolado e explicitamente insuficiente: so um ponto no tempo |
| "Good old software orchestration": filas e eventos classicos, nada novo | A composicao depende de eventos tipados (schema) para nao virar spaghetti de payloads |
| Interface declarativa (schedules + assinaturas) em vez de codigo de orquestracao | Sem visao declarada do conjunto: o que existe so aparece no log |
| Reatividade a mudancas do mundo externo, nao apenas a pontos no tempo | Subscribes espalhados por arquivos: nenhum grafo consultavel da frota |

## Relacao com outros padroes

- **Compoe:** [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]] (eixo quando) + [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]] (eixo porque) — este padrao e a composicao dos dois como superficie unica.
- **Declarada em:** [[docs/canonical/agent-as-declarative-file|Agent as Declarative File]] — schedule e assinaturas de evento sao os campos que materializam esta superficie.
- **E a superficie de:** [[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]] — o scheduler do kernel dispara os cron; as fronteiras tipadas validam os eventos.
- **Conclusao vizinha de:** [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]] — ambos eliminam a camada de grafo de orquestracao; um por goals persistentes, outro por schedules + eventos.
- **Topologia de:** [[docs/canonical/emergent-event-topology|Emergent Event Topology]] — eventos tipados sao o mesmo eixo "porque"; a topologia emergente e o que esta superficie produz quando nao ha orquestrador.

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:53-66` — sistema de agentes = schedules + eventos (+ nada mais); cron insuficiente isolado.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:93-94` — "good old software orchestration".
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:140-158` — padrao 7 extraido: inputs, outputs, beneficios, limitacoes.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:139-152` — classificacao Partial Coverage (Medium) com evidencia file:line e NOT_FOUND da composicao.
- [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]`:30-38, :44` — anti-patterns de scheduling e a primitiva da frota.
- [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]`:27-33, :88` — stance anti-DAG vizinha por argumento de goals.
