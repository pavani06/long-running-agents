---
title: "Skills and CLI as Native Agent Data Access"
type: canonical
aliases: ["skills cli data access", "acesso nativo a dados para agentes", "goal-level data work"]
tags: ["agentes-orquestracao", "data-platform", "harness-engineering"]
last_updated: 2026-08-31
relates-to: ["[[docs/canonical/file-system-materialization|File-System Materialization]]", "[[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]]", "[[docs/canonical/shadow-builds-separated-compute|Shadow Builds on Separated Compute]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]"]
sources: ["[[docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns|Clay Eval Stack Patterns]]"]
---
# Skills and CLI as Native Agent Data Access

**Type:** canonical
**Status:** active
**Source:** Inside Clay's Eval Stack (LangChain) — `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/`
**Classification:** Partial Coverage — Integration value: Medium (P2)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Agentes precisam acessar a plataforma de dados **nativamente** — sem adaptadores humanos no meio. Quando o único caminho até os dados passa por dashboards, exports e tickets, o agente vira um cliente de segunda classe da própria plataforma: cada tarefa de dados exige um humano intermediando, e trabalho de dados longo e iterativo (explorar, modelar, testar, refinar) torna-se impraticável para agentes.

O problema tem duas faces: (a) interface — como o agente consome a plataforma; (b) execução — onde roda o trabalho pesado que esse acesso dispara.

## Solution

Parear **skills agent-oriented + CLI dedicada** como camada de acesso à plataforma de dados:

1. **Skills agent-oriented** encapsulam o know-how de operação da plataforma (como consultar, como modelar, como não atirar no próprio pé) em unidades que o agente carrega.
2. **CLI dedicada** é a interface nativa: os mesmos comandos que um humano usaria, sem UI obrigatória no caminho. A CLI é o contrato estável entre agentes e plataforma.
3. **Delegação goal-level** — o input é um statement de objetivo ("here's this goal, I want this data model"), não um script passo-a-passo; o agente planeja os passos.
4. **Compute escalável para execuções longas** — execuções de 1-2 horas são cidadãs de primeira classe: budget management, retomada, monitoramento. O output da execução é um **novo data model**, não um relatório.
5. **Pareamento com shadow builds** — o artefato construído pela execução longa deploya no shadow target separado (ver [[docs/canonical/shadow-builds-separated-compute|Shadow Builds on Separated Compute]]).

## Implementation in this repo

### What already exists

O repo opera a mecânica no próprio metabolismo:

- **Biblioteca de skills como superfície operacional:** 35 skills agente-orientadas em `.opencode/skills/` (`docs/system-of-record.md:36-67`) — o repo é, ele mesmo, um sistema agêntico orientado a skills.
- **CLI dedicada de dados:** `obsidian-eval` (@pavani/obsidian-eval) para "scan, query, grafo e cross-vault wikilinks" do knowledge vault (`README.md:159`; `docs/system-of-record.md:127`) — acesso nativo de dados sem adaptador humano.
- **Substrato universal:** [[docs/canonical/file-system-materialization|File-System Materialization]] — "The file system is the universal interface that every coding model understands" (`docs/canonical/file-system-materialization.md:38,48`).
- **Delegação goal-level:** [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]] — hard goal + "full tool/API access and persistence across the task horizon" (`:37`); "agent survives across the whole horizon (own plan, own replans)" (`:54`).
- **Execução longa com estado persistente:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]] (`docs/system-of-record.md:180`); harness `harness.sh` + `PROGRESS.md` entre passos (`harness/GUIDE-analyze-and-improve.md`).

### What is missing

O pareamento específico com plataforma de dados:

1. Skills/CLI não são framing de acesso a uma **data platform** — o alvo do repo é o vault de conhecimento, não uma plataforma de dados de produto. NOT_FOUND: grep `dedicated CLI|goal-level|1-2 hours|long-running goal` em `*.md` → sem correspondência fora do pacote-fonte.
2. Execuções goal-level de **1-2 horas em compute escalável** com resultado = novo data model não existem como contrato.
3. O pareamento explícito com shadow builds (acesso nativo → build → deploy shadow) não está nomeado.

Add:

1. Encarar `obsidian-eval` + skills como camada de acesso a dados candidata a generalização (o mecanismo existe; falta o framing de plataforma).
2. Contrato de execução goal-level longa sobre dados: goal statement → budget → execução resumível → artefato versionado.
3. Ponte curricular explícita file-system-materialization → goal-driven-agents → shadow target de deploy.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Agentes têm a mesma ergonomia de acesso de humanos, em escala de máquina | Execução longa exige gestão de budget e compute |
| Delegação goal-level substitui scriptar passo-a-passo o trabalho de dados | Skills e CLI são superfície de manutenção contínua |
| Execuções de 1-2h destravam trabalho de dados que fragmentação tornava impraticável | Goals mal especificados queimam horas de compute antes de falhar |
| Pareia com shadow builds para execução segura | Exige a fundação de dados unificada como pré-requisito de valor pleno |

## Relationship to Other Patterns

- **Builds on:** [[docs/canonical/file-system-materialization|File-System Materialization]] — arquivos/git/grep como substrato; a CLI é a forma concreta desse substrato para dados.
- **Builds on:** [[docs/canonical/goal-driven-agents-over-workflows|Goal-Driven Agents over Workflows]] — a delegação é goal-level com persistência ao longo do horizonte.
- **Uses:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]] — execuções de horas só sobrevivem com estado serializável.
- **Pairs with:** [[docs/canonical/shadow-builds-separated-compute|Shadow Builds on Separated Compute]] — o output da execução (novo data model) deploya no shadow; o par acesso-nativo + deploy-shadow é a unidade de autonomia de dados.
- **Dispatch via:** [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] — a CLI como autoridade única de dispatch sobre a plataforma.

## References

- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-patterns.md:250` — definição original do padrão.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification.md` — §12, classificação Partial Coverage/Medium com evidência.
- `docs/analysis/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel/2026-08-31-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipel-classification-batch-2.md` — batch-fonte da classificação.
- `docs/system-of-record.md:36-67,127,180` — biblioteca de skills, `obsidian-eval`, serializable-pause-resume-state.
- `README.md:159` — CLI `obsidian-eval`.
- `docs/canonical/file-system-materialization.md:38,48` — interface universal de arquivos.
- `docs/canonical/goal-driven-agents-over-workflows.md:37,54` — delegação goal-level com persistência.

---

*Created: 2026-08-31 | From: Clay Eval Stack classification | Precedence: canonical*
