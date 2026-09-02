---
title: "Presence Interface Ladder"
type: canonical
tags: ["governanca", "agentes-orquestracao", "production", "decision-discipline"]
aliases: ["interface ladder", "escada de modos de interface", "SSH with vibes", "unattended as the product", "atencao exigida por interface"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]"
  - "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]"
  - "[[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]"
  - "[[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]]"
  - "[[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]]"
sources:
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Agent Frameworks Considered Harmful]]"
  - "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification|Classification: Agent Frameworks Considered Harmful]]"
---

# Presence Interface Ladder

**Type:** Canonical Pattern
**Status:** Active
**Source:** AI Engineer — Remi Louf (.txt), "Agent Frameworks Considered Harmful" (2026-08-22)
**Classification:** Partial Coverage (P2, Medium integration value)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problema

Medir maturidade de interface de agente por capacidade do modelo esconde o gargalo real: **quanta atencao humana a interface exige** (patterns.md:182). O sintoma diagnostico do fonte: pilotar agentes pelo celular durante uma caminhada, instruindo sem pensar claramente — "claramente transitório", absurdo como estado final (analysis.md:32-34).

O nome colide com [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]], mas a polaridade e o proposito diferem, e essa distincao e o conteudo deste doc. O canonical existente mede presenca como **metrica de governanca** para manter o owner engajado durante trabalho de risco (presenca desejada MAIOR em high-risk, `:23-27`, `:29-67`); este padrao mede atencao exigida pela interface como **metrica de maturidade de produto**, com direcao oposta: reduzir presenca humana a ~zero (classification.md:174).

## Solucao

A escada de modos de interface, classificados pela atencao que exigem do humano (analysis.md:26-30):

| Degrau | Interface | Analogia do fonte | Atencao exigida |
|---|---|---|---|
| Interativo | TUI no terminal | trator que voce dirige mesmo que "dirija sozinho" | total — voce fica "em cima" |
| Semi-remoto | app mobile | "SSH with vibes": controle remoto, corrige a trajetoria "de vez em quando" | parcial — nao esta ao lado, mas continua pilotando |
| Unattended | background agent | robo de corte autonomo, sem controle remoto | ~zero — trabalha o dia todo sozinho |

A escada produz uma decisao direcional de produto (analysis.md:32-35):

1. **O produto prometido e o modo unattended** — o agente como processo de fundo que produz o resultado sem ninguem apontar.
2. **O modo mobile e transitorio** — pilotar pelo celular e sintoma de interface imatura, nao feature.
3. **Presenca-no-loop vira a metrica de maturidade da interface**, independente do modelo: subir na escada nao e trocar o modelo, e remover atencao humana exigida.

Guarda-chuva de segurança: unattended reduz presenca a ~zero, nao a zero — falhas ainda escalam para humanos (patterns.md:198). O degrau unattended exige os demais padroes de runtime (log causal, fronteiras tipadas, replay) para ser seguro (patterns.md:196).

## Implementacao neste repositorio

### O que ja existe

- **A metrica, polaridade governanca:** [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]] — problema do humano que so aparece no fim para aprovar diff grande (`:23`); solution com presence timeline, stale-presence warnings, risk-tiered thresholds, intervention points (`:29-67`). A maquinaria de medicao ensinada em N3 (exercise-06, PresenceTracker completo; classification.md:180) mede a mesma grandeza que esta escada classifica.
- **Escada binaria de roteamento:** [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:30-37 — AFK-ready vs human-in-loop em quatro dimensoes (ambiguidade, arquitetura, feedback loop, julgamento de produto) por tarefa.
- **Escada de autonomia por task class:** [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]:41-63 — observe/assist/own com lambda 0.0→1.0; "autonomy should be a dial, not a switch" (`:63`).
- **Escada de valor (construto diferente):** [[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]]:36-52 — estagios de valor ao usuario com switching costs e wow-collapse; unico match de "maturity ladder" na busca do classification (classification.md:181).

### O que falta

(classification.md:181) — busca por `semi-remote|SSH with vibes|interface ladder|maturity ladder|unattended` em `docs/canonical/` nao encontra a escada de interface:

1. **A taxonomia de modos de interface** (interativo / semi-remoto / unattended) com atencao exigida por degrau.
2. **A decisao direcional de produto** — unattended como meta declarada; modo mobile como estado transitorio, nao destino.
3. **A ligacao explicita de polaridade** com o canonical de metrica: mesma maquinaria de medicao, uso direcional oposto (governanca quer presenca no risco; produto quer remove-la da interface).

## Tradeoffs

| Beneficio | Custo |
|---|---|
| Presenca-no-loop como metrica de maturidade de interface, independente do modelo | Taxonomia de produto, nao mecanismo: nao implementa nada por si |
| Identifica o celular como sintoma transitorio e evita investir nele como destino | O degrau unattended exige todos os demais padroes (log, fronteiras tipadas, replay) para ser seguro |
| Direciona investimento para remover o humano do loop, nao para aumentar capacidade do modelo | Unattended reduz presenca a ~zero, nao a zero: falhas ainda escalam para humanos |

## Relacao com outros padroes

- **Polaridade oposta de:** [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]] — governanca mede para MANTER presenca em trabalho de risco; produto mede para REDUZIR atencao exigida. Complementos, nao duplicatas: a mesma PresenceTracker serve aos dois usos.
- **Fronteira de granularidade com:** [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] — roteamento binario por tarefa vs escada por modo de interface da frota.
- **Eixo distinto de:** [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]] — dial de autonomia por task class (observe/assist/own) vs degraus de atencao exigida pela interface.
- **Construto distinto de:** [[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]] — estagios de valor/switching costs vs degraus de atencao humana.
- **Depende, no degrau unattended, de:** [[docs/canonical/append-only-causal-event-log|Append-Only Causal Event Log]] (e, pela limitacao do padrao, fronteiras tipadas e replay — ver [[docs/canonical/typed-event-boundaries|Typed Event Boundaries]]).

## Referencias

- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis.md:21-36` — taxonomia de modos de interacao humano-agente com atencao exigida por modo; decisao direcional.
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md:180-198` — padrao 9 extraido: inputs, outputs, beneficios, limitacoes (incluindo ~zero, nao zero).
- `docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/classification.md:170-183` — classificacao Partial Coverage (Medium), colisao de nome com o canonical de metrica, NOT_FOUND da escada de interface.
- [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]`:23-27, :29-67` — metrica na polaridade governanca.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]`:30-37` — escada binaria de roteamento por tarefa.
- [[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]`:41-63` — observe/assist/own com lambda dial.
- [[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]]`:36-52` — escada de valor, construto diferente.
