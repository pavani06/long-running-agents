---
title: "Classificacao Batch B: Agent Frameworks Considered Harmful (Remi Louf, .txt)"
type: analysis
date: 2026-09-02
tags: [agentes-orquestracao, harness-engineering, production, governanca]
aliases: ["classificacao batch B Remi Louf", "patterns 6-9 classification", "kernel cron eventos presenca classificacao"]
relates-to: ["[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns|Padroes Remi Louf .txt]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analise Remi Louf .txt]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-mental-model|Mental Model do Pipeline]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]", "[[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]", "[[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]]", "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]", "[[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/autonomy-curriculum-sampling|Autonomy Curriculum Sampling]]", "[[docs/canonical/agent-value-maturity-ladder|Agent Value Maturity Ladder]]"]
---

# Classificacao Batch B: Agent Frameworks Considered Harmful (Remi Louf, .txt)

Classificacao dos padroes 6-9 de [[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns|patterns.md]] contra o repositorio, com evidencia `file:line`. Precedencia seguida: `docs/decisions/` > `docs/canonical/` > `docs/evidence/` > `docs/analysis/` > `curriculum/` > READMEs ([[docs/system-of-record|system-of-record.md]]). Os dois ADRs aceitos (`docs/decisions/2026-09-01-vault-federation-consultable-registry.md`, `docs/decisions/2026-06-24-skill-canons-bridge-implementation.md`) nao tocam em nenhum dos quatro padroes; a evidencia relevante vive toda no nivel canonical e curriculum.

## 6. Agent Kernel Runtime

**Classificacao: Partial Coverage**

**Justificativa:** as tres responsabilidades do kernel existem, cada uma como canonical independente, mas a unificacao — um runtime que agenda processos, isola execucao e registra journal, com o agente como processo de primeiro classe do sistema do usuario e frontend de definicao trocavel — nao existe como modelo nomeado. A inversao de posse (o argumento central contra frameworks) esta documentada com forca no [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]], porem a implementacao de referencia do repo (mhc-backend/KODA) delega o loop ao LangGraph, ou seja, o exato estado que o padrao denuncia. Faltam: o framing de responsabilidades classicas de SO reutilizadas (agendamento + isolamento + journaling como um kernel), o agente como processo de primeiro classe, e a nocao de que o kernel nao sabe o que o agente faz.

**Evidencia:**
- Inversao de posse (problema): `docs/canonical/owned-agent-control-loop.md:22-27` — loop de framework e black box, sem intervention points; tabela Framework-Owned vs Developer-Owned em `:77-85`.
- Implementacao de referencia delega ao framework: `docs/canonical/owned-agent-control-loop.md:107` — "LangGraph owns the loop... the iteration inside the graph is framework-managed".
- Isolamento por processo: `docs/canonical/model-agnostic-agent-vm-harness.md:45` — slot 1 "Per-agent VM: each agent instance gets an isolated execution environment"; before/after da reconstrucao Kavak em `:36-37`.
- Agendamento: `docs/canonical/alarm-clock-agent-lifecycle.md:44-48` — wake-work-sleep com self-scheduling e durable wake trigger; o proprio canonical registra que faltava scheduler no repo (`:85`).
- Journaling/OS operacional: `docs/canonical/closed-loop-agent-operating-system.md:28-37` — quatro superficies (state intake, priority synthesis, execution routing, feedback writeback); mas e OS no nivel de operacoes da frota, nao kernel de processos, e o proprio doc se declara Partial porque a mecanica esta espalhada (`:61-68`).
- NOT_FOUND (unificacao kernel): busca por `first-class process|agent as process|supervisor|daemon|process isolation|own runtime|frameworks just call` em `docs/canonical/` e `docs/decisions/` — unicos matches sao ruido operacional do flywheel daemon systemd (`docs/canonical/eval-dashboard-primary-detection-surface.md:51`, `docs/canonical/always-on-monitoring-human-triage.md:64`); nenhum doc une scheduler + isolamento + journal como runtime unico.

**Valor de integracao: High** — e o frame que falta ao conjunto: owned-loop (inner), VM harness (isolamento), alarm-clock (schedule) e o log causal do mesmo fonte ja existem como pecas; o kernel-named-pattern os amarraria num unico modelo ensinavel, territorio central da tese do repo.

## 7. Cron plus Typed Events Orchestration Surface

**Classificacao: Partial Coverage**

**Justificativa:** os dois eixos existem separados. O eixo "quando" tem canonical proprio (alarm-clock) e aparece na arquitetura de referencia KODA como scheduler nativo. O eixo "porque" (eventos) e ensinado no curriculum como choreography/event-driven pub/sub. O que nao existe e a composicao como superficie completa de orquestracao: a claim de que cron + eventos tipados substituem a camada inteira de framework ("voce nao escreve codigo, e esse e o produto inteiro"), com agentes declarativos assinando schedules e assinaturas de eventos. O anti-orchestration-graph do repo (`goal-driven-agents-over-workflows`) chega a conclusao vizinha por argumento diferente (goals, nao eventos).

**Evidencia:**
- Eixo "quando": `docs/canonical/alarm-clock-agent-lifecycle.md:30-38` (as opcoes quebradas, incluindo "External orchestrator polls" como anti-pattern) e `:44` ("This is the scheduling primitive for the fleet").
- Scheduler nativo na arquitetura de referencia: `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md:1660` — "E por que tem um cron job? O KODA ja tem um scheduler..."; `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-06-presence-in-the-loop-metric.md:43,51,66` — cron job marcado "REDUNDANTE (deveria usar scheduler KODA)".
- Eixo "porque" (eventos): `curriculum/05-core-concepts/07-multi-agent-coordination.md:296,309` — choreography com eventos de dominio disparando reacoes assincronas; `curriculum/06-knowledge-graphs/04-problem-solution-mapping.md:1057` — Event Bus pub/sub; `curriculum/04-nivel-4-koda-specific/real-world-exercises/exercise-02.md:255` — coordinacao Event-Driven (Pub/Sub).
- Stance anti-grafo vizinha: `docs/canonical/goal-driven-agents-over-workflows.md:27-33` — workflow DAG rejeitado como unidade de especificacao; `:88` — "goals age better than orchestration graphs".
- NOT_FOUND (composicao): nenhum doc canonical ou de curriculum declara cron+eventos como a superficie de orquestracao completa/declarativa; buscas por `cron|schedule|typed events|orchestration surface` em `docs/canonical/`, `docs/decisions/` e `curriculum/` retornam so os ingredientes acima; o alarm-clock canonical registra em `:85-86` que o scheduler como primitiva propria sequer existia antes dele (doc-level only, sem codigo).

**Valor de integracao: Medium** — os ingredientes estao ensinados; o delta e a formalizacao da composicao de dois eixos como substituto declarativo da camada de orquestracao, incluindo a limitacao explicita (cron isolado e so ponto no tempo).

## 8. Failure-Accrued Runtime Growth

**Classificacao: Partial Coverage**

**Justificativa:** o principio — nada especulativo, cada peca justificada por dor/falha observada em producao, sequenciamento descoberto — ja esta documentado a profundidade canonical em [[docs/canonical/pull-based-infrastructure-on-pain|Pull-Based Infrastructure on Pain]] e seus vizinhos. O que falta e a instancia especifica deste fonte: o mapa 1:1 falha-producao → primitiva-de-runtime (nota de voz sumiu → log append-only; brief duplicado no Slack → fila com retry+dedup; regressao irreproduzivel → prompts content-addressed), o framing "runtime como sedimento das falhas" e o contraponto explicito ao design upfront de "agent operating systems". O proprio pull-on-pain registra que o principio no repo estava escopado a capacidade de eval e governanca de harness.

**Evidencia:**
- Principio equivalente: `docs/canonical/pull-based-infrastructure-on-pain.md:43` — "Adicionar infraestrutura reativamente, na sequencia em que sua ausencia vira o binding constraint"; tabela 1:1 infra ← dor que a puxa em `:45-52`; regras "Cada investimento responde a uma restricao sentida, nao a especulacao" e "O sequenciamento e descoberto, nao planejado" em `:56-59`.
- Gate por dor (escopo eval): `docs/canonical/pain-signal-eval-progression-gate.md:28,36` — maturidade gateada por pain signals, "smallest eval capability that addresses the observed pain"; trigger table `:40-51`.
- Anti-upstream: `docs/canonical/symphony-trap-awareness.md:27,33` — especificacoes emergem de sistemas rodando; "build then distill".
- Falha → ativo duravel (output eval, nao runtime): `docs/canonical/production-failure-regression-flywheel.md:26-40`.
- Gap declarado pelo proprio repo: `docs/canonical/pull-based-infrastructure-on-pain.md:77-81` — NOT_FOUND para a generalizacao full-stack e o sequenciamento minimal-launch; principio aplicado so a eval e harness governance.
- NOT_FOUND (mapa runtime): nenhum doc mapeia incidentes nomeados a primitivas de runtime interno (journal/queue/content-addressing) na ordem de aparecimento da falha; buscado em `docs/canonical/`, `docs/analysis/` (exceto o proprio fonte Remi Louf), `curriculum/`.

**Valor de integracao: Medium** — a filosofia ja existe em profundidade; o delta e o instantiate runtime (pecas de kernel justificadas falha a falha) que fortaleceria o cross-reference entre pull-on-pain e os padroes 1-6 deste fonte.

## 9. Presence-in-the-Loop Interface Ladder

**Classificacao: Partial Coverage**

**Justificativa:** o nome do padrao colide com um canonical ativo forte ([[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]), mas a polaridade e o proposito diferem. O canonical do repo mede presenca como metrica de governanca para MANTER o owner engajado durante execucao de risco (presenca desejada maior em trabalho high-risk); o padrao de Louf mede atencao exigida pela INTERFACE como metrica de maturidade de produto, com direcao oposta (reduzir presenca humana a ~zero; modo unattended e o produto; pilotar pelo celular e sintoma de interface transitoria). Elementos adjacentes existem: o routing binario AFK/human, o curriculum de autonomia observe/assist/own (lambda dial), e a maquinaria completa da metrica ensinada em N3. Faltam: a taxonomia de modos de interface (interativo / semi-remoto / unattended) com atencao exigida por degrau, e a decisao direcional de produto que a escada produz.

**Evidencia:**
- Metrica-core existente (polaridade governanca): `docs/canonical/presence-in-the-loop-metric.md:23-27` — problema e o humano aparecer so no fim para aprovar diff grande; solution `:29-67` (presence timeline, stale-presence warnings, risk-tiered thresholds, intervention points).
- Escada binaria de roteamento de tarefas: `docs/canonical/human-afk-task-routing-gate.md:30-37` — AFK-ready vs human-in-loop em quatro dimensoes.
- Escada de autonomia mais proxima (por task class, nao por interface): `docs/canonical/autonomy-curriculum-sampling.md:41-63` — observe/assist/own com lambda 0.0→1.0; "autonomy should be a dial, not a switch" (`:63`).
- Ensino e implementacao: `curriculum/GLOSSARY.md:650-662`; `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-06-presence-in-the-loop-metric.md` (PresenceTracker completo); `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md:1667-1684`.
- NOT_FOUND (a escada de interface): busca por `semi-remote|SSH with vibes|interface ladder|maturity ladder|unattended` em `docs/canonical/` — unico match de "maturity ladder" e o alias de `docs/canonical/agent-value-maturity-ladder.md:10`, que e escada de valor/switching costs (estagios de valor ao usuario, wow-collapse; `:36-52`), construto diferente; nenhum doc classifica modos de interface por atencao exigida nem declara unattended como meta de produto.

**Valor de integracao: Medium** — complementa o canonical existente com a dimensao produto/interface (mesma metrica, uso direcional oposto); a maquinaria de medicao ja existe, o que falta e a taxonomia de modos e a decisao direcional.

## Tabela Resumo

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 6 | Agent Kernel Runtime | Partial Coverage | High |
| 7 | Cron plus Typed Events Orchestration Surface | Partial Coverage | Medium |
| 8 | Failure-Accrued Runtime Growth | Partial Coverage | Medium |
| 9 | Presence-in-the-Loop Interface Ladder | Partial Coverage | Medium |
