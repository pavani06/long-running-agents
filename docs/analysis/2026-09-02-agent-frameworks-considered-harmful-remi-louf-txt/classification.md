---
title: "Classification: Agent Frameworks Considered Harmful (Remi Louf, .txt)"
type: analysis
date: 2026-09-02
tags: [agentes-orquestracao, harness-engineering, context-engineering, multi-agent, production, governanca]
aliases: ["remi louf classification", "agent frameworks considered harmful classification", "classificacao padroes remi louf"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns|Patterns]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-analysis|Analysis]]", "[[docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-mental-model|Mental Model]]"]
sources:
  - "docs/analysis/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt/2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.yaml"
---

# Classification: Patterns vs. long-running-agents

Consolidated from batches A (patterns 1-5) and B (patterns 6-9), executed in parallel by two classification agents. Precedence per `docs/system-of-record.md:14-21`: decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs. Batch evidence files: `classification-batch-a.md`, `classification-batch-b.md`.

# Classification Batch A: Patterns 1-5 vs. long-running-agents

Precedence order applied per `docs/system-of-record.md:14-21`: decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs. Every classification cites file:line from the repo; `Missing` confirms NOT_FOUND with the locations searched. Pattern names are used exactly as they appear in `2026-09-02-agent-frameworks-considered-harmful-remi-louf-txt-patterns.md`.

---

## 1. Typed Tool and Event Boundaries

**Classification: Partial Coverage**

**Justification:** The agent-tool frontier is covered at canonical depth and in implementation: structured output contracts with schema validation, post-generation constraint validation, and deterministic dispatch with typed tool inputs (Zod) exist as named patterns. The agent-agent frontier, however, exists only as an adjacent protocol (agent-parseable review comments), not as a general typed event boundary. What no doc, code, or curriculum material defines: per-agent declaration of which events it accepts and returns, and a kernel-level validator applied at BOTH frontiers that rejects non-conforming tool calls and events before they produce effect — the "make bad actions impossible, not improbable" reframe extended to inter-agent events.

**Evidence:**
- `docs/canonical/structured-generation-constraint-validation-circuit.md:29` — unified action-safety circuit: "output schema, generation prompt, domain constraint set, post-generation validator, repair or rejection policy, and audit log" (output-side boundary at canonical depth)
- `docs/canonical/structured-generation-constraint-validation-circuit.md:61-63` — shape validation (schema + fields) then domain constraint validation, with reject/repair/flag/fallback on failure (boundary rejects rather than corrects — same posture as the source pattern)
- `docs/canonical/deterministic-tool-dispatch.md:74` — "Every tool is a `DynamicStructuredTool` with Zod schema input and typed return" (mhc-backend implementation of the typed tool boundary)
- `docs/canonical/deterministic-tool-dispatch.md:107` — "Built on: Pattern 1 (Structured Output Contract)" (12FA structured-output contract already named in canon)
- `docs/canonical/agent-to-agent-review-comment-protocol.md:37` — agent-agent interface contract framing ("sem um formato agent-parseable... o loop fecha no humano em vez de fechar no próximo agente") — closest agent-agent analogue, but scoped to review comments, not event schemas
- NOT_FOUND: per-agent event schemas (accepted/returned events) and a validator applied at both agent-tool and agent-agent frontiers — searched `docs/canonical/`, `docs/decisions/`, `docs/evidence/`, `curriculum/`, `.opencode/` (grep for "typed event", "eventos tipados", "input schema", "output schema", "structured output"; matches cover model-output and tool-input validation only)

**Integration value: High** — The tool-side boundary is mature; the missing agent-agent event boundary is the substrate this source's patterns 3 and 4 assume, and the repo already owns the contract vocabulary (Structured Output Contract, Deterministic Tool Dispatch) to absorb it without a new pattern family.

---

## 2. Content-Addressed Prompt Graph

**Classification: Partial Coverage**

**Justification:** Prompt versioning, rollback, and audit exist at canonical depth (prompt-as-code with causal commits, git revert rollback, "what was the exact prompt text deployed"), and prompt versions are already required inside replay state. Addressable memory gives every omitted context piece a stable identifier, and graph-addressed placement keys knowledge to graph nodes. None of this is content addressing: no hash function over prompt components, no storage keyed by content hash (git/Nix style), no prompt represented as a graph of hashes before text rendering, no component-granularity diff between runs, and no compaction-as-graph-manipulation. The repo's replay patterns replay conversations and traces, not the exact rendered prompt reconstructed from hashes.

**Evidence:**
- `docs/canonical/prompt-as-code-causal-change-management.md:28` — "Treat prompts as first-class versioned artifacts in a git repository, with a mandatory causal commit discipline" (versioning at commit granularity, not content-addressed granularity)
- `docs/canonical/prompt-as-code-causal-change-management.md:80-85` — rollback infrastructure: git-revert per prompt change, per-component prompt files, deploy at a specific commit, rollback audit trail
- `docs/canonical/prompt-as-code-causal-change-management.md:100-105` — audit trail answers "what was the exact prompt text deployed" per point in time (via git history, not via hashes)
- `docs/canonical/stable-harness-prompt.md:52` — replay requires prompt, rubric, catalog, and schema versions (`curriculum/05-core-concepts/05-state-persistence.md:1414`); `:62` — prompt version metadata in replay artifacts
- `docs/canonical/addressable-memory-catalog.md:28-43` — stable `id`/`kind`/`location`/`preview`/`scope`/`tool`/`path` per omitted context piece (addressing by catalog ID, not by content hash)
- `docs/canonical/graph-addressed-context-placement.md:42-48` — placement of knowledge keyed to software-graph nodes, retrieval by traversal (graph addressing of context, not of prompt components)
- `docs/canonical/production-grounded-eval-sampling.md:28` — replay of representative real interactions (conversation-level replay, not exact-prompt reconstruction)
- NOT_FOUND: content hashing of prompt components (system/skill/tool/user), content-addressed storage, prompt-as-graph-of-hashes before rendering, per-component run diffs, compaction as graph manipulation, response-to-exact-prompt tracing via hashes — searched `docs/canonical/`, `docs/decisions/`, `curriculum/`, `.opencode/` (grep for "content-address", "hash", "replay": canonical `hash` matches are a mtime/hash gate artifact `docs/canonical/structural-guarantee-over-compliance.md:52` and sanitized tool params `docs/canonical/centralized-cross-framework-tracing.md:47`; "content-address" appears only in this source's own analysis package)

**Integration value: High** — Exact-input reconstruction is the mechanical substrate the repo's replay, regression, and model-swap patterns assume but never ground; it would connect prompt-as-code, addressable-memory-catalog, and production-grounded replay into one debug story. (Cost is admittedly the source's own "deep rabbit hole" — value is high, effort is too.)

---

## 3. Append-Only Causal Event Log

**Classification: Partial Coverage**

**Justification:** Append-only audit logs exist in curriculum (`audit_log.jsonl` defined as immutable, never overwritten, for post-mortem timelines; a `_log()` implementation appending JSONL events), trace stores are taught as immutable chronological logs that every agent writes to, and centralized tracing exists in implementation (`tracer.ts` → `trace-state.json` → `telemetry.db`) with a unified schema including `parent_span_id`. Missing are the two defining mechanics: event-level causal links captured at publish time (`caused_by`/`parent_event_id` between events — `parent_span_id` is span hierarchy, not event causality), and the single mandatory append-only destination for ALL agents and processes with the reframe "the log is the memory of the system; nothing is lost." No queryable failure-to-trigger reconstruction exists.

**Evidence:**
- `curriculum/06-knowledge-graphs/detailed-graphs/generator-evaluator-graphs.md:355` — `audit_log.jsonl` defined as append-only immutable JSONL, events never altered/removed; timeline for post-mortem (no causal links defined)
- `curriculum/05-core-concepts/07-multi-agent-coordination.md:2737-2738` — Trace store as immutable chronological log for debug, audit, replay; `:2776-2780` — checklist requires each agent to write `started`/`completed` entries
- `curriculum/02-nivel-2-practical-patterns/exercises/solutions/exercise-01-solution.md:1748-1759` — `_log()` implementation appending JSONL events (timestamp, type) in mode `"a"` (physical append, no immutability guarantee beyond file mode)
- `curriculum/06-knowledge-graphs/detailed-graphs/planning-execution-graphs.md:1096-1100` — write-ahead logging and append-only audit log required, never overwritten (no causal event schema)
- `docs/canonical/centralized-cross-framework-tracing.md:28-55` — centralized tracing layer with unified schema (`trace_id`, `span_id`, `parent_span_id`) for debugging and audit; `:123-130` — existing pipeline `tracer.ts` → `trace-state.json` → `collector.ts`/`telemetry.db`
- `docs/canonical/behavioral-eval-path-analysis.md:34-45` — full trace with timestamps, params, success/failure and "causal ordering" (execution-order preservation, not event-to-event causality)
- `docs/canonical/asymmetric-failure-correction-router.md:74-83` — two "immutable append-only" learning logs specified (imitate/correct), declared absent in the repo at `:98-103`
- NOT_FOUND: explicit causal links captured at event publish time (`caused_by`, `parent_event_id`, `causal_links`); a single append-only table/stream as mandatory destination for all agents; a common publish API; queryable reconstruction from failure back to trigger event; equivalent implementation in `.opencode/` or `scripts/` — searched `docs/canonical/`, `docs/decisions/`, `docs/evidence/` (no matches in evidence/), `curriculum/`, `.opencode/`, `scripts/`

**Integration value: High** — The repo already operates `telemetry.db` tracing and teaches `audit_log.jsonl` conventions; adding publish-time causality fields and the log-as-memory discipline is an incremental delta on existing infrastructure, and it is the prerequisite for the source's topology and unattended-operation claims.

---

## 4. Emergent Event Topology

**Classification: Partial Coverage**

**Justification:** The constituent ideas exist in curriculum: message-queue channels (Redis/RabbitMQ) taught alongside file-based coordination, workers that consume and publish events with `event_type` fields, fan-out/fan-in taught explicitly, and choreography named as an alternative paradigm; one canonical doc even shares the philosophical stance against declared workflow DAGs. Missing is the defining reframe and its mechanics: agents communicating ONLY through typed-event pub/sub with zero declared edges, topology existing solely in the event log, extension by dropping a new agent file that subscribes to known public event schemas, and free fan-in/fan-out from subscriptions. The repo's canonical multi-agent architecture leans the opposite way — orchestrators, declared A→B→C workflows with per-step contracts, and Saga rollback — and no pub/sub runtime, event schema registry, or subscription dispatch exists in code.

**Evidence:**
- `curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md:616-637` — three communication channels taught (file-based, Redis/RabbitMQ, APIs); `:731-759` — workers consuming/publishing events with `event_type` and `reply_to`, but an Evaluator awaits all results (declared coordination, not emergent topology)
- `curriculum/05-core-concepts/07-multi-agent-coordination.md:201-221` — fan-out/fan-in taught as explicit division and recombination by an orchestrator; `:538` — choreography mentioned (a gate as "um evento escutado por vários agentes") as one alternative among paradigms
- `docs/canonical/goal-driven-agents-over-workflows.md:27-58` — critique of declared workflow DAGs in favor of goal-driven agents (philosophical alignment with "no orchestration graph", without proposing typed events as the mechanism)
- `docs/canonical/agent-specific-data-freshness-pipeline.md:30-38` — event-driven pipeline (document change → re-ingest → re-embed) with typed triggers; declared NOT implemented at `:70-86`
- Counter-evidence (repo's declared-edge canon): `docs/canonical/multi-agent-fault-tolerance.md:20-40` — explicit `Agent A → Agent B → Agent C` workflows, Saga rollback, per-step contracts; `.opencode/skills/orchestrator/SKILL.md:12-29` — central orchestrator coordination via GitHub issues and dashboards
- NOT_FOUND: an architecture with zero declared edges whose topology is reconstructed from the log; extension by dropping an agent file that subscribes to existing public event schemas; an event schema registry; any pub/sub broker or subscription-dispatch runtime in code — searched `docs/canonical/`, `docs/decisions/`, `curriculum/`, `.opencode/`, `README.md` (event bus appears only as trace-collection middleware `curriculum/07-implementation-guides/05-trace-analysis-guide.md:1390` and a future "adaptive mesh" idea `curriculum/08-tools-templates/knowledge-graph-template.md:1283`)

**Integration value: Medium** — Valuable as a taught alternative at N3 (the no-edges reframe completes the repo's orchestration-vs-choreography spectrum and grounds its own DAG critique), but it tensions with the orchestrator-first canon; the repo would integrate it as curriculum contrast, not as replacement architecture.

---

## 5. Agent as Declarative File

**Classification: Partial Coverage**

**Justification:** The core mechanics already run in this repo: `.opencode/agents/` holds agent definitions as markdown files with declarative frontmatter (description, mode, temperature, tools, permissions) that the OpenCode runtime loads from the folder — versioned in git, diffable, reviewable in PRs — and README markets exactly this as a reusable template. Canonical docs teach declarative agent specs as files in Git (file-system-materialization; Sierra's Ghostwriter editing YAML agent specs) and a per-agent-role declarative harness spec (`agent-vm.yaml`). Missing: event subscriptions (accepted/returned events) and schedules as fields of the declarative file format, the folder-scan "drop a file and the agent magically appears" onboarding story, and the non-coder contribution reframe ("20 agents in a month, contributed not only by technical people") — scheduling exists as a separate canonical (self-scheduling agents) but not inside the file format.

**Evidence:**
- `.opencode/agents/hop-orchestrator-rezek.md:1-19` — declarative agent file: frontmatter with description, mode, temperature, tool allowlist, permissions; loaded by the OpenCode runtime from the agents folder (siblings: `hop-live-whatsapp-tester.md`, `koda-hop-init-basic.md`)
- `README.md:136-140` — operate the harness and adapt the `.opencode/` system (3 agents, 36 skills) as a template (the declarative-file agent system is a first-class repo deliverable)
- `docs/canonical/file-system-materialization.md:38` — "A declarative agent specification stored as a YAML file in a Git repository is more agent-accessible than the same specification in a database or a custom UI"; `:52-58` — Ghostwriter reads/edits/commits declarative YAML agent specs via Git
- `docs/canonical/model-agnostic-agent-vm-harness.md:55-70` — `agent-vm.yaml` declarative per-agent-role spec (vm, tools, memory, evals, goal, model slots)
- `docs/canonical/file-system-materialization.md:66` — file-based coordination lesson covering materialization of domain logic into file-system structures (curriculum coverage of the adjacent practice)
- `docs/canonical/alarm-clock-agent-lifecycle.md:32-48` — self-scheduling agents (wake → work → sleep) exist as a canonical pattern, but as runtime behavior, not as a schedule field in a declarative agent file
- NOT_FOUND: events accepted/returned declared in the agent file; schedule declaration in the `.opencode/` agent format; folder-scan auto-discovery ("agent magically appears") and non-coder contribution as a taught pattern — searched `.opencode/agents/`, `.opencode/skills/`, `docs/canonical/`, `docs/decisions/`, `curriculum/` (grep for "declarative", "agente.*arquivo", "schedule", "cron"; scheduling appears in `alarm-clock-agent-lifecycle.md` and orchestration skills, never as declarative-file fields)

**Integration value: Medium** — The repo already operates declarative agent files; the delta is enriching the format (event subscriptions, schedule) and teaching the drop-in onboarding story — an extension of an owned mechanism, not a new capability.

---

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

## Summary

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Typed Tool and Event Boundaries | Partial Coverage | High |
| 2 | Content-Addressed Prompt Graph | Partial Coverage | High |
| 3 | Append-Only Causal Event Log | Partial Coverage | High |
| 4 | Emergent Event Topology | Partial Coverage | Medium |
| 5 | Agent as Declarative File | Partial Coverage | Medium |
| 6 | Agent Kernel Runtime | Partial Coverage | High |
| 7 | Cron plus Typed Events Orchestration Surface | Partial Coverage | Medium |
| 8 | Failure-Accrued Runtime Growth | Partial Coverage | Medium |
| 9 | Presence-in-the-Loop Interface Ladder | Partial Coverage | Medium |

Result: 0 Already Exists, 9 Partial Coverage, 0 Missing, 0 Better Implementation. Integration value: 4 High (patterns 1, 2, 3, 6), 5 Medium (4, 5, 7, 8, 9).
