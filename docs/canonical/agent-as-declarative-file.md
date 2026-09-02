---
title: "Agent as Declarative File"
type: canonical
tags: ["agentes-orquestracao", "harness-engineering", "multi-agent", "production"]
aliases: ["agent as file", "agente como arquivo declarativo", "declarative agent definition", "drop-in agent onboarding", "folder-scan agent discovery"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/file-system-materialization|File-System Materialization for Agent Tooling]]"
  - "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]"
  - "[[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]"
  - "[[docs/canonical/typed-event-boundaries|Typed Event Boundaries]]"
  - "[[docs/canonical/cron-plus-typed-events-orchestration|Cron plus Typed Events Orchestration]]"
  - "[[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Agent as Declarative File

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Editar o prompt do agente dentro do codigo de framework — "passei todo o tempo editando o prompt dentro do codigo" (analysis.md:163-164) — e restringir a criacao de agentes a engenheiros, porque toda extensao do sistema passa por codigo de orquestracao.

O repo **ja opera** a mecanica central: `.opencode/agents/` guarda definicoes declarativas carregadas pelo runtime. O que este doc formaliza e o **delta de formato e de historia**: assinaturas de evento e schedule como campos do arquivo declarativo, o onboarding por folder-scan ("o agente magicamente aparece") e a contribuicao por nao-codificadores como resultado mensuravel — 20 agentes em producao em um mes, "contribuidos nao apenas por gente tecnica" (analysis.md:168-169).

## Solucao

A definicao do agente e um arquivo markdown/YAML solto numa pasta; o runtime escaneia a pasta e carrega as definicoes (analysis.md:165-167). O formato deste padrao estende o formato que o repo ja usa com dois campos:

```yaml
# agents/daily-brief.md — arquivo declarativo completo
description: "Gera o daily brief a partir de notas duraveis"
mode: subagent
temperature: 0.2
tools:
  read: true
  write: true
events:                      # delta 1: assinaturas de eventos
  accepts:
    - { schema: voice-note.processed, version: 1 }
  returns:
    - { schema: brief.generated, version: 1 }
schedule:                    # delta 2: schedule declarativo
  cron: "0 7 * * *"
  timezone: America/Sao_Paulo
```

Propriedades resultantes:

1. **Onboarding de agente = drop de arquivo.** O agente "magicamente aparece" no proximo scan da pasta (analysis.md:166-167).
2. **Versionavel no git, diffavel, reviewavel em PR** — mesmo workflow de codigo, sem ser codigo.
3. **Contribuicao por nao-codificadores**: conhecer os eventos existentes e escrever um arquivo basta; o efeito organizacional medido no fonte foi 20 agentes em producao em um mes (analysis.md:168-169).
4. **O formato e da userland, nao do kernel**: um frontend alternativo de definicao poderia nem usar markdown (analysis.md:44-45; patterns.md:114).

## Implementacao neste repositorio

### O que ja existe

- **Formato declarativo operacional:** [[.opencode/agents/hop-orchestrator-rezek.md]]:1-19 — frontmatter com description, mode, temperature, tool allowlist e permissions, carregado pelo runtime OpenCode da pasta `agents/` (irmaos: `hop-live-whatsapp-tester.md`, `koda-hop-init-basic.md`); o README promove o sistema `.opencode/` (3 agentes, 36 skills) como template reutilizavel (classification.md:105-106).
- **Espec declarativo ensinado como canon:** [[docs/canonical/file-system-materialization|File-System Materialization for Agent Tooling]] — "A declarative agent specification stored as a YAML file in a Git repository is more agent-accessible than the same specification in a database or a custom UI" (`:38`); Ghostwriter le/edita/commita specs YAML de agentes via Git (`:52-58`).
- **Spec por papel de agente:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] — `agent-vm.yaml` declarativo por papel (vm, tools, memory, evals, goal, model slots) (`:55-70`).
- **Scheduling como comportamento de runtime:** [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]] — wake → work → sleep com self-scheduling e wake trigger duravel (`:32-48`), porem como padrao de runtime, nao como campo do arquivo do agente.

### O que falta

(classification.md:111) — scheduling aparece em `alarm-clock-agent-lifecycle.md` e skills de orquestracao, nunca como campo de arquivo declarativo; eventos aceitos/retornados nao aparecem em nenhum formato:

1. **Campo `events` (aceita/retorna) no formato do arquivo de agente** — hoje nenhuma definicao declara contratos de evento.
2. **Campo `schedule` no formato** — o alarm-clock existe como lifecycle canonico; o delta e trazer o schedule para dentro do arquivo declarativo.
3. **A historia de onboarding folder-scan** ("drop a file and the agent magically appears") e o **reframe de contribuicao nao-tecnica** como padrao ensinado.

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Onboarding de agente = drop de arquivo versionavel, diffavel, reviewavel em PR | YAML/markdown e menos expressivo que codigo ("YAML e odiado") |
| Contribuicao por nao-codificadores (20 agentes/mes no fonte) | Dependencia do runtime que consome o formato |
| Frontend de definicao trocavel: o formato pertence a userland | Capacidade dos agentes limitada ao que o declarativo expressa |

## Relacao com outros padroes

- **Estende:** [[docs/canonical/file-system-materialization|File-System Materialization for Agent Tooling]] — o arquivo de agente e o caso mais puro de spec declarativa materializada em arquivo.
- **Empacota:** [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]] — o schedule declarativo ganha casa no formato de arquivo.
- **Carrega:** [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]] — assinaturas de evento no arquivo sao como o contrato tipado se torna consultavel por agente.
- **E a userland de:** [[docs/canonical/agent-kernel-runtime|Agent Kernel Runtime]] — o kernel carrega definicoes; o arquivo e o frontend trocavel de definicao.
- **Composicao completa em:** [[docs/canonical/cron-plus-typed-events-orchestration|Cron plus Typed Events Orchestration]] — schedules + assinaturas de evento no arquivo sao a superficie declarativa daquela orquestracao.
- **Espec vizinha:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] — `agent-vm.yaml` cobre vm/tools/memory/evals/goal/model; faltam events e schedule.

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:161-169` — agente-como-arquivo: mecanismo, versionamento, efeito organizacional.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:44-45` — kernel vs userland: o frontend de definicao e da userland.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:101-118` — padrao 5 extraido: inputs, outputs, beneficios, limitacoes.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:98-113` — classificacao Partial Coverage (Medium) com evidencia file:line e NOT_FOUND.
- [[.opencode/agents/hop-orchestrator-rezek.md]]:1-19 — formato declarativo existente: description, mode, temperature, tools, permissions.
- [[docs/canonical/file-system-materialization|File-System Materialization for Agent Tooling]]`:38, :52-58` — spec declarativa em Git; Ghostwriter.
- [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]`:32-48` — self-scheduling como runtime, nao como campo.
