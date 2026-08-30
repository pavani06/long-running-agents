---
title: "Classification Batch 1: Kavak's Playbook for Rebuilding a Company Around AI (Patterns 1-8)"
type: classification
tags: ["agentes-orquestracao", "harness-engineering", "curriculo-conteudo", "governanca"]
date: 2026-08-30
aliases: ["kavak classification batch 1", "kavak playbook classification 1-8"]
relates-to: ["[[docs/system-of-record|System of Record]]", "2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml", "2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-mental-model.md"]
sources: ["2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml"]
---

# Classification Batch 1: Patterns 1-8 vs. long-running-agents

Precedence order applied per `docs/system-of-record.md:14-21`: decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs. Every classification cites file:line from the repo; `Missing` confirms NOT_FOUND with the locations searched.

---

## 1. Model-Agnostic Agent-VM Harness

**Classification: Partial Coverage**

**Justification:** The repo has strong, canonical-level alignment on the model-agnostic philosophy — a canonical doc specifies a model-agnostic selection layer with vendor adapters, another canonical doc treats model switching as a mechanical eval-gated process, and File-System Materialization provides the "universal tooling surface" analog to Kavak's CLI-exposing-everything. However, the repo's own canonical docs declare the concrete implementation NOT_FOUND, and the Kavak-specific packaging — one VM per agent with memory subsystem, per-agent eval suite, long-term goal slot, and a model-swap interface as a single compounding harness asset at fleet scale — exists nowhere as one pattern. What is present are the parts (context portability, switch-gating, universal file interface), not the assembled minimal-harness contract.

**Evidence:**
- `docs/canonical/neutral-selection-layer.md:28` — "A model-agnostic selection layer that sits between the model and the store, serving context through a uniform interface regardless of which model, vendor, or session requests it."
- `docs/canonical/neutral-selection-layer.md:53` — "NOT_FOUND across all 85 canonical docs. The repo has philosophical alignment with vendor independence" (implementation gap acknowledged at canonical level).
- `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:24` — "However, the concrete infrastructure to execute model switching — an enterprise eval dataset that tests model upgrades against domain-specific data, side-by-side comparison infrastructure, and a mechanical switching decision framework — does not exist."
- `docs/canonical/file-system-materialization.md:38` — "Materialize everything into files, git, and grep: Domain logic, agent specifications, configuration, knowledge bases — if a coding agent needs to interact with it, make it a file."
- `docs/canonical/invariant-compensation-split.md:25` — harness components "kept compensations that only made sense for an older model, turning the harness into bug surface, latency, token cost, complexity, and maintenance burden" (the harness-as-ceiling problem the Kavak harness avoids).

**Integration value: High** — A unifying "minimal model-agnostic harness" canonical doc would tie together neutral-selection-layer (spec-only), model-switching-architecture-enterprise-eval-gate (infrastructure-missing), and the eval-gate cluster into the repo's central compounding-asset thesis.

---

## 2. Alarm-Clock Agent Lifecycle

**Classification: Partial Coverage**

**Justification:** The repo covers the state side of wake/sleep extensively: Serializable Pause/Resume State exists precisely because "scheduled tasks" and async waits cannot complete in a synchronous call, and Versioned Durable Agent State covers surviving crashes, callbacks, and long pauses. The orchestrator skill selects the next task by priority. What is missing is the scheduling primitive itself: an alarm scheduler where the agent sets its own next-wake time, a wake trigger, and the wake-work-sleep fleet lifecycle as a named pattern. Searches for alarm/wake/sleep/scheduler/cron (EN) and agendamento/despertador/próxima tarefa (PT) across docs/canonical/, curriculum/, .opencode/skills/ return only the Kavak analysis files themselves and unrelated matches (token budgets, orchestration dashboards).

**Evidence:**
- `docs/canonical/serializable-pause-resume-state.md:22` — "Long-running tools (async API calls, human approval waits, scheduled tasks) cannot complete inside a single synchronous model call."
- `docs/canonical/serializable-pause-resume-state.md:33` — "Serialize the entire agent state (context window + execution state + business state) to persistent storage. On resume, deserialize and continue from exactly where the agent paused."
- `docs/canonical/versioned-durable-agent-state.md:23` — state loss on "crashes, restarts, payment events, callbacks, and long pauses" is the problem the durable-state contract solves.
- `docs/canonical/closed-loop-agent-operating-system.md:54` — "orchestrator skill lines 27-62 defines a dashboard and priority logic for choosing the next task" (priority-based selection, not time-based wake).

**Integration value: High** — The repo's thesis is agents running reliably for hours or days; a canonical alarm-clock lifecycle (agent-owned next-wake scheduling over durable state) is a core long-running primitive with no canonical, curriculum, or skill coverage.

---

## 3. Agent-Per-Customer with Persistent Cross-Channel Memory

**Classification: Partial Coverage**

**Justification:** Per-customer memory mechanics exist at canonical level: Auth-Coupled Memory Architecture defines identity-keyed memory with authentication-confidence gating (though its own implementation section is NOT_FOUND), Three-Tier Memory Persistence covers what to remember per customer and reports resolution-rate gains from customer recall, and the KODA curriculum explicitly targets long-term relationship and LTV. Missing are the pattern's distinctive claims: one persistent agent *instance* per customer on its own VM (KODA is a single agent with per-customer state, not agent-per-customer), complete cross-channel history ingestion spanning years, outcome ownership by the per-customer agent, and the portfolio constraint layer bounding per-customer optimization.

**Evidence:**
- `docs/canonical/auth-coupled-memory-architecture.md:24` — "Memory products treat storage and retrieval as independent of identity, but extracting the right memories requires knowing *who* the caller is."
- `docs/canonical/auth-coupled-memory-architecture.md:36` — "Identity resolution as memory key: Every memory item is stored with an identity key (phone number, account ID, session token, or device fingerprint)."
- `docs/canonical/auth-coupled-memory-architecture.md:61` — "NOT_FOUND across `docs/canonical/`, `curriculum/`, `system-of-record.md`, and `.opencode/skills/`" (identity-keyed memory implementation).
- `docs/canonical/three-tier-memory-persistence.md:51` — "three-tier memory 'measurably improved resolution rate' through concrete memory applications: greeting customers by name (Tier 1), recalling previous call topics (Tier 1 + Tier 2)".
- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md:719` — "OBJETIVO: Construir relacionamento de longo prazo." (KODA relationship goal; LTV tracked at `:1297`).

**Integration value: Medium** — Useful enrichment for the KODA N4 curriculum (agent-per-customer vs. task-agent topology, dormant-base activation economics); the memory and relationship-goal layers are already covered at depth.

---

## 4. Goal-Driven Agents over Scripted Workflows

**Classification: Partial Coverage**

**Justification:** Goal-driven execution at task level is deeply institutionalized: the karpathy-guidelines skill teaches Goal-Driven Execution with verifiable goals as the stop criterion, Value-Gated Agent Control Loop adds a build/experiment/defer/stop decision before execution, Intent-Five-Part-Primitive makes goal a specification primitive, Symphony Trap Awareness is explicitly anti-scripting (anti over-specification), and Business-Outcome-First Eval Pipeline anchors measurement in business outcomes. Missing is the strategic reframe: a hard, persistent business objective (2x profits, maximize LTV) *owned* by the agent over a multi-day-to-months horizon with agent-owned decomposition, measured on outcome attainment rather than step compliance, and the superhuman-performance bar as the architecture-selection criterion.

**Evidence:**
- `.opencode/skills/karpathy-guidelines/SKILL.md:148` — "## 4. Goal-Driven Execution — Metas Verificaveis".
- `docs/canonical/value-gated-agent-control-loop.md:31` — "Add a value-gating decision point to the agent control loop that produces an explicit classification -- build, experiment, defer, or stop -- before execution begins".
- `docs/canonical/symphony-trap-awareness.md:33` — "Replace 'write spec then build' with 'build then distill spec from what works then rebuild with the spec as a contract.'" (anti-scripted-workflow stance).
- `docs/system-of-record.md:234` — "`intent-five-part-primitive.md` | Intenção decomposta em cinco partes primitivas: goal, context, constraints, verification, handoff".
- `docs/system-of-record.md:283` — "`business-outcome-first-eval-pipeline.md` | Pipeline de eval ancorado em business outcomes: define success em termos de negócio → golden answers de domain experts → Python pipeline comparativo, deflection rate prediction".

**Integration value: Medium** — Goal specification and outcome-level eval mechanics exist at depth; the missing piece is the long-horizon outcome-ownership reframe, which would enrich rather than fill a hole.

---

## 5. Scaffold Deletion on Model Step-Change

**Classification: Better Implementation**

**Justification:** The repo's canonical treatment is a more mature, governed version of the same idea. Measured Harness Evolution Lifecycle defines BUILD → STABILIZE → SIMPLIFY → REMOVE with ROI-threshold removal governance, quarterly cycles whose week 1 explicitly reviews model changelogs, One In One Out, and reversible archived removal (the Budget Guard example: removed after a 200K-token model migration with feature-flag reactivation). Invariant-Compensation Split supplies the classification step the Kavak pattern lacks (domain invariants must survive; only model-specific compensations are deletion candidates), and Model-Switch-Driven Eval Hardening supplies the event trigger (every model switch revalidates the full eval dataset). The curriculum teaches the exact question ("when the model improves, what happens to the scaffolding?") with the cycle restarting "with less initial scaffolding". The only Kavak-specific delta is the organizational framing (deleting two years of profitable infrastructure as a willpower act on a step-change trigger) — a narrative framing, not a missing mechanism.

**Evidence:**
- `docs/canonical/measured-harness-evolution-lifecycle.md:29` — "Treat harness evolution as a measured lifecycle, not as one-time architecture. Every component moves through four states: BUILD defensively, STABILIZE with production evidence, SIMPLIFY layer by layer, and REMOVE through archived, reversible removal".
- `docs/canonical/measured-harness-evolution-lifecycle.md:50` — "REMOVE is allowed when a component has fulfilled its purpose and removal remains reversible. The Budget Guard had zero triggers for 180 days after the 200K-token model migration... a feature flag allowed reactivation in minutes".
- `docs/canonical/measured-harness-evolution-lifecycle.md:60` — "Govern cadence with a quarterly cycle: week 1 reviews model changelogs, metrics, and component classification... Apply One In, One Out".
- `docs/canonical/invariant-compensation-split.md:23` — "the original Context Loader existed because a 32K-token model lost attention after 40 minutes; after a newer model held 98% accuracy at 100K tokens, that same component still cost 450ms, 1200 tokens..." (the exact kept-scaffolding-after-model-step-change case).
- `docs/system-of-record.md:298` — "`model-switch-driven-eval-hardening.md` | Model-Switch-Driven Eval Hardening — hardening de evals dirigido por switch de modelo: cada troca de modelo dispara revalidação completa do dataset de eval (Sierra)".
- `curriculum/05-core-concepts/06-harness-evolution.md:156` — "Harness Evolution fecha o ciclo... 'E quando o modelo melhorar? O que acontece com todo esse scaffolding que construímos?'" (cycle restarts "com menos scaffolding inicial" at `:361`).

**Integration value: Low** — Mechanism, trigger, eval gating, and reversibility are all covered at equal or greater depth; at most a footnote on the radical whole-stack deletion case.

---

## 6. Shared Fleet Learning

**Classification: Partial Coverage**

**Justification:** The capture side exists: Production Failure Regression Flywheel turns every production failure into a durable regression case, Living Eval Dataset grows monotonically from incidents, and the Closed-Loop Agent OS defines feedback writeback as one of its four surfaces. Cross-Context Knowledge Siloing documents the exact pathology fleet-learning solves (knowledge invisible across agent contexts causes repeated mistakes) and its mitigations. Missing is the propagation channel: aggregating one agent's mistake into a fleet-level skill/memory/policy update distributed to all running instances by the next day. The repo's own canonical doc on continual learning declares this NOT_FOUND — the flywheel surfaces findings for human review and deploys nothing, and there is no Ghostwriter-equivalent auto-update mechanism.

**Evidence:**
- `docs/canonical/production-failure-regression-flywheel.md:28` — "Every production failure that reveals a behavioral gap should become a durable eval regression case unless it is explicitly rejected as duplicate, unactionable, or out of scope."
- `docs/canonical/cross-context-knowledge-siloing.md:46` — "Knowledge created in one agent context becomes invisible to agents operating in a different context, causing repeated investigation of already-solved problems."
- `docs/canonical/confidence-gated-continual-learning.md:59` — "NOT_FOUND across `docs/canonical/`, `curriculum/`, `system-of-record.md`, and `.opencode/skills/`" (fleet-wide auto-update deployment mechanics).
- `docs/canonical/confidence-gated-continual-learning.md:64` — "The flywheel daemon (`systemd`, 60s loop) processes triggers but deploys nothing — it surfaces findings for human review."
- `docs/canonical/closed-loop-agent-operating-system.md:35` — "Feedback writeback | Persist decisions, traces, failures, eval results, canonical docs, and issue outcomes | Updated memory for future agents".

**Integration value: Medium** — Capture, deduplication, and writeback surfaces exist; a canonical doc on fleet-level propagation (update distribution to all instances of a shared substrate) would connect the flywheel, siloing, and continual-learning docs, but substantial adjacent infrastructure already exists.

---

## 7. Closed-Loop Help API (Humans Serve Agents)

**Classification: Partial Coverage**

**Justification:** The escalation side is well covered: Tested Degradation Ladder escalates to a human with summarized context sufficient to continue the work, logs the outcome, and converts real failures into durable regression coverage; Operator-Channel Authority defines escalation as flowing to the operator's own channel; the multi-model evaluation council routes disagreements to needs-human. Missing is the inversion that defines the Kavak pattern: a help API the *agent calls* synchronously when stuck, the resolution flowing *back into the agent that asked* so it continues the task, and the organizational inversion of human teams serving agents. The repo's escalation is terminal (human takes over the case); no mechanism returns a resolution to the calling agent, and no doc frames the humans-serve-agents topology.

**Evidence:**
- `docs/canonical/tested-degradation-ladder.md:29` — "escalates to a human with summarized context when automated recovery is insufficient, logs the outcome, and tests each rung before production reliance".
- `docs/canonical/tested-degradation-ladder.md:65` — "The final rung must turn real failures into durable eval or regression coverage, because production failures should become regression cases" (training-data capture exists at the outcome-log level).
- `docs/canonical/operator-channel-authority.md:73-76` — "Genuine escalation still exists... but it flows *to* the operator's channel for a decision, not *between* peers as a substitute for one."
- `docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-classification.md:135` — "`docs/canonical/multi-model-evaluation-council.md:37` through `:45` defines retry, needs-human, disagreement escalation, and human review routing" (escalation routing, one-directional).

**Integration value: Medium** — Escalation-with-context and outcome logging exist; the resolution-return channel and the humans-serve-agents reframe would be a useful enrichment, partially overlapping the flywheel's training-data capture.

---

## 8. Sidekick Pattern at Physical Boundaries

**Classification: Missing**

**Justification:** NOT_FOUND. Searches across `docs/canonical/` (full directory listing reviewed; no candidate), `docs/decisions/`, `curriculum/`, `.opencode/skills/`, and `docs/system-of-record.md` for the concept name and mechanism keywords (`sidekick`, `co-pilot`, `copilot`, `ride along`, `mechanic`, `voice note`, `nota de voz`, `destreza`, `dexterity`, `physical work`, `trabalho físico`, `presença física`) return matches only in the Kavak analysis package itself. The nearest non-equivalents: `presence-in-the-loop-metric.md` and `human-afk-task-routing-gate.md` (per `docs/system-of-record.md:219`, `:235`) calibrate how much humans intervene in *agent* tasks — the inverse direction of service — and `curriculum/10-references/model-capability-timeline.md:919-921` mentions WhatsApp voice notes only as a client-facing latency feature, not worker telemetry feeding evals.

**Evidence:**
- `curriculum/10-references/model-capability-timeline.md:919-921` — "Real-time Voice... Latência de voz é importante para experiência do cliente (WhatsApp voice notes), mas o core do agente funciona sem isso." (nearest mention; client experience, not agent-guides-human telemetry; not equivalent).
- `docs/system-of-record.md:235` — "`presence-in-the-loop-metric.md` | Métrica de presença-no-loop: calibração do grau de intervenção humana necessária por tarefa" (adjacent, inverse direction).

**Integration value: Low** — The pattern's core value is at physical-world boundaries (mechanics, car keys), outside this repo's software-agent harness scope; only the telemetry-return-channel generalization (human progress signals feeding agent evals) is transferable.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Model-Agnostic Agent-VM Harness | Partial Coverage | High |
| 2 | Alarm-Clock Agent Lifecycle | Partial Coverage | High |
| 3 | Agent-Per-Customer with Persistent Cross-Channel Memory | Partial Coverage | Medium |
| 4 | Goal-Driven Agents over Scripted Workflows | Partial Coverage | Medium |
| 5 | Scaffold Deletion on Model Step-Change | Better Implementation | Low |
| 6 | Shared Fleet Learning | Partial Coverage | Medium |
| 7 | Closed-Loop Help API (Humans Serve Agents) | Partial Coverage | Medium |
| 8 | Sidekick Pattern at Physical Boundaries | Missing | Low |
