---
title: "Agent Kernel Runtime"
type: canonical
tags: ["agentes-orquestracao", "harness-engineering", "production", "agent-loop", "12-factor-agents"]
aliases: ["agent kernel", "kernel de agentes", "agent as process", "agente como processo", "scheduling isolation journaling"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]"
  - "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]"
  - "[[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]"
  - "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]"
  - "[[docs/canonical/typed-event-boundaries|Typed Event Boundaries]]"
  - "[[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]]"
  - "[[docs/canonical/agent-as-declarative-file|Agent as Declarative File]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Agent Kernel Runtime

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P1, High integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Frameworks invertem a relacao de posse: "frameworks just call code — your agents live inside their abstractions" (analysis.md:46-48). O agente deixa de ser um processo isolado do sistema do usuario e passa a ser um plugin dentro das abstracoes de terceiro.

O repo documenta essa inversao com forca: [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] descreve o loop de framework como black box sem intervention points (`:22-27`) e canonicaliza a tabela Framework-Owned vs Developer-Owned (`:77-85`). Porem a implementacao de referencia (mhc-backend/KODA) **delega o loop ao LangGraph** — "LangGraph owns the loop... the iteration inside the graph is framework-managed" (`:107`) — exatamente o estado que o padrao denuncia. O que falta e a unificacao: as tres responsabilidades existem, cada uma como canonical independente; nenhuma as amarra como um runtime unico (classification.md:127, :135).

## Solucao

Nomear o runtime como **kernel** que reutiliza as responsabilidades classicas de sistema operacional, com o agente como **processo de primeira classe do sistema do usuario** (analysis.md:40-45):

| Responsabilidade do kernel | O que faz | Canonical que ja cobre a peca |
|---|---|---|
| **Agendamento** (scheduler de processos) | Decide quando cada processo-agente roda (cron, wake triggers) | [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]] |
| **Isolamento** (processo por agente) | Cada agente executa em ambiente isolado; falha nao contamina vizinhos | [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] (slot 1, per-agent VM) |
| **Journaling** (log + definicao do agente) | Registra o que aconteceu e qual definicao rodou | [[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]] |

Tres propriedades definem o modelo:

1. **Ao kernel nao importa o que o agente faz** — o agente e um processo; o kernel agenda, isola e registra, sem conhecer sua semantica interna (analysis.md:42-43).
2. **O agente e um processo de primeiro classe do sistema do usuario** — nao um plugin hospedado nas abstracoes de um framework (analysis.md:44-48).
3. **O frontend de definicao e trocavel** — a definicao vive na userland (arquivo declarativo); o kernel a consome sem depender do formato (analysis.md:44-45).

O principio de design do kernel: tornar acoes ruins impossiveis, nao apenas improvaveis, via fronteiras tipadas em tool calls e eventos (analysis.md:50-51) — ver [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]].

**Contraste de granularidade:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] e OS no nivel das **operacoes da frota** (state intake, priority synthesis, execution routing, feedback writeback, `:28-37`); este padrao e kernel no nivel de **processos individuais** (scheduler + isolamento + journal). Sao camadas distintas, nao sinonimos.

## Implementacao neste repositorio

### O que ja existe

As tres responsabilidades existem como canonicos independentes:

- **Inversao de posse (problema) documentada:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:22-27 (loop de framework como black box), tabela `:77-85`, e o reconhecimento de que "LangGraph owns the loop" `:107`.
- **Isolamento por processo:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] — slot 1 "Per-agent VM: each agent instance gets an isolated execution environment" (`:45`), com o before/after da reconstrucao Kavak (`:36-37`).
- **Agendamento:** [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]:44-48 — wake → work → sleep com self-scheduling e durable wake trigger; o proprio canonical registra que faltava scheduler no repo (`:85`).
- **Journaling/OS operacional:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]`:28-37` — quatro superficies, mas em nivel de operacoes da frota; o doc se declara Partial porque a mecanica esta espalhada (`:61-68`).

### O que falta

(classification.md:135) — busca por `first-class process|agent as process|supervisor|daemon|process isolation|own runtime` em `docs/canonical/` e `docs/decisions/` retorna apenas ruido operacional (daemon systemd do flywheel); nenhum doc une scheduler + isolamento + journal como runtime unico:

1. **O modelo nomeado do kernel** — agendamento + isolamento + journaling como UM runtime, reutilizando responsabilidades classicas de SO em vez de reinventa-las dentro de um framework.
2. **O agente como processo de primeira classe** — o framing de posse: processos do sistema do usuario, nao plugins de terceiro.
3. **A agnosticidade semantica do kernel** — "ao kernel nao importa o que o agente faz" como regra de design que separa kernel de userland.

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Inverte a relacao do framework: as abstracoes de terceiro nao possuem o agente | Manutencao do runtime proprio (tradeoff build vs buy com infra de agentes ainda indefinida) |
| Reutiliza responsabilidades classicas de SO em vez de reinventa-las | O kernel so e completo com as demais pecas: log causal, content addressing, fila com dedup |
| Permite trocar o frontend de definicao sem trocar o kernel | Menor velocidade inicial que adotar framework pronto |

## Relacao com outros padroes

- **Unifica:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] (loop interno do processo), [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] (isolamento), [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]] (agendamento) — o kernel e o frame que amarra as pecas num modelo unico ensinavel.
- **Tem como journal:** [[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]] — journaling e registro do que aconteceu + definicao do agente.
- **Enforca na fronteira:** [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]] — o validador de tool calls e eventos e mecanismo do kernel.
- **Carrega como userland:** [[docs/canonical/agent-as-declarative-file|Agent as Declarative File]] — definicoes declarativas sao o frontend trocavel.
- **Camada distinta de:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] — OS de operacoes da frota vs kernel de processos individuais.
- **Pecas justificadas falha a falha em:** [[docs/canonical/failure-accrued-runtime-growth|Failure-Accrued Runtime Growth]].

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:38-51` — kernel vs framework: agente como processo, userland, principio de design do kernel.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:120-138` — padrao 6 extraido: inputs, outputs, beneficios, limitacoes.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:123-137` — classificacao Partial Coverage (High) com evidencia file:line e NOT_FOUND da unificacao.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]`:22-27, :77-85, :107` — inversao de posse documentada; LangGraph owns the loop.
- [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]`:36-37, :45` — slot 1 per-agent VM.
- [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]`:44-48, :85` — wake-work-sleep; scheduler faltante registrado.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]`:28-37, :61-68` — quatro superficies em nivel frota; mecanica espalhada.
