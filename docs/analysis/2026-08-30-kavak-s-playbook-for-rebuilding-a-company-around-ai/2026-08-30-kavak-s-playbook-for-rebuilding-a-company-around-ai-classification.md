---
title: "Classification: Kavak's Playbook for Rebuilding a Company Around AI"
type: analysis
tags: [agentes-orquestracao, evals, harness-engineering]
date: 2026-08-30
aliases: ["classificacao kavak playbook", "kavak playbook classification"]
relates-to:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Knowledge Extraction]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns|Patterns]]"
sources:
  - "Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md"
---

# Classification: Kavak's Playbook for Rebuilding a Company Around AI

Consolidated from 2 parallel batches (8 + 6 patterns). Evidence follows the precedence of `docs/system-of-record.md`.

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

---

## 9. Evals-as-Brakes

**Classification:** Partial Coverage

**Justification:** The repo has the "brakes" half at canonical depth — evals as merge/deployment gates (PR-Gated Eval Enforcement) and an organizational brakes vocabulary (Manual Brake Question Gate, Accidental Brake Replacement, which even maps slow bureaucratic brakes to eval-based intentional replacements). The velocity/safety tension is explicitly named in the Sierra-derived Confidence-Gated Continual Learning pattern. What is missing is the specific coupling rule of the Kavak pattern: permitted shipping velocity set as a function of eval quality/coverage — "maximum speed becomes a function of eval quality rather than risk appetite" — and the corresponding response-to-risk reframe (on failure, improve the brakes rather than permanently slow down). Grepping `velocity|shipping speed|go faster|go slow` across `docs/canonical/` returns only token-burn velocity (`burn-rate-runtime-forecast.md`) and the confidence-gate tension; no doc ties deployment speed limits to eval coverage.

**Evidence:**
- `docs/canonical/pr-gated-eval-enforcement.md:28` — "Require eval-specific reports on PRs that touch prompt, model, tool, context, memory, scoring, or agent-loop behavior."
- `docs/canonical/pr-gated-eval-enforcement.md:51` — "Block merge when thresholds fail unless an explicit waiver is recorded."
- `docs/canonical/accidental-brake-replacement.md:23` — "The danger is that an executive mandate to 'move faster' or 'remove bureaucracy' can eliminate the last remaining mechanism that prevents unchecked agentic construction, without anyone realizing what function it was serving."
- `docs/canonical/accidental-brake-replacement.md:50` — "Security review (takes 1 week) | Prevents vulnerable code from shipping | PR-Gated Eval Enforcement + automated security scanning at PR time" (evals positioned as the intentional brake replacing slow gates).
- `docs/canonical/confidence-gated-continual-learning.md:24` — "Agent improvement cycles face a tension between velocity and safety."
- NOT_FOUND (coupling rule "velocity as a function of eval quality"): searched `docs/canonical/` and `docs/system-of-record.md` with `velocity|shipping speed|go faster|go slow` — only `burn-rate-runtime-forecast.md:31,49` (token consumption velocity) and `confidence-gated-continual-learning.md:24` (tension without an eval-quality coupling rule).

**Integration Value:** High — the repo's evals cluster is its largest canonical cluster (system-of-record.md:200-204, 279-299); a unifying governance principle that names eval quality as the determinant of permitted shipping speed would sit atop that cluster and directly extend the repo thesis that harness/eval engineering unlocks agent autonomy.

---

## 10. Eval-Investment Parity

**Classification:** Partial Coverage

**Justification:** The repo strongly documents evals as first-class artifacts built before or alongside agents (Eval-Driven Development Timeline prescribes 6 weeks of eval infrastructure before any model work; Living Eval Dataset, Eval Tier Stratification, and the full evals cluster formalize evals as durable products). However, the parity rule itself — a ~50/50 split of engineering time, tokens, and money between agents and their evals — is absent. Notably, the repo's own investment philosophy is deliberately different: the Pain-Signal Eval Progression Gate mandates the *smallest* eval capability that addresses observed pain, explicitly rejecting proportional or calendar-driven allocation. So the "co-designed, first-class evals" mechanics exist; the fixed parity budget rule and its capacity-halving leadership trade-off are neither documented nor endorsed.

**Evidence:**
- `docs/canonical/eval-driven-development-timeline.md:28` — "Invest 6 weeks in evaluation infrastructure before any model experimentation or selection. The timeline is deliberately inverted from conventional development: evaluation is the first thing built, not the last."
- `docs/canonical/pain-signal-eval-progression-gate.md:28` — "Treat eval maturity as a gate driven by pain signals instead of a calendar roadmap."
- `docs/canonical/pain-signal-eval-progression-gate.md:36` — "Approve only the smallest eval capability that addresses the observed pain." (the repo's alternative to a parity allocation)
- NOT_FOUND (parity rule): searched `docs/` with `parity|50/50|50%` — matches are only fixture parity (`docs/canonical/eval-tier-stratification.md:57`) and Supabase mock parity in the issue-review skill, i.e., test-environment parity, unrelated to budget allocation between agents and evals.

**Integration Value:** Medium — useful as an organizational budget heuristic and as a teaching counterpoint to the repo's pain-signal gate (when does pain-gating underinvest relative to a fleet-scale ambition?), but the repo already has a rich, deliberate eval-investment philosophy, so this enriches rather than fills a hole.

---

## 11. Outcome-Level Eval Hierarchy

**Classification:** Partial Coverage

**Justification:** The core reframe — anchor first-order evaluation on business results, not technical metrics — exists at canonical depth: Business-Outcome-First Eval Pipeline prescribes defining business success (deflection rate, CSAT, revenue protection) before golden answers and before the technical pipeline, and names the exact Kavak failure mode ("technically correct but business-irrelevant"). Eval-to-Production Correlation Tracking covers outcome metrics (CSAT proxy, retention, task success) and the false-safety problem ("eval scores become false safety signals"). What is missing: (a) the explicit hierarchy ordering — measure the business outcome, then optimize the agentic architecture, then add skills where outcomes reveal gaps — as a single loop; and (b) the named rejection of vanity/proxy KPIs (call counts, minutes on call) as a distinct failure class. Grepping `vanity|proxy KPI` finds nothing outside the Kavak source package.

**Evidence:**
- `docs/canonical/business-outcome-first-eval-pipeline.md:28` — "Invert the eval pipeline construction sequence: define business success first, then create golden answers from domain experts, then build the technical pipeline to compare agent outputs against business-aligned metrics."
- `docs/canonical/business-outcome-first-eval-pipeline.md:46` — "Deflection | % of queries resolved without human intervention | 60% deflection rate" (business-result metrics as eval north star).
- `docs/canonical/business-outcome-first-eval-pipeline.md:22` — "the technical eval passes but the business outcome fails — the agent is technically correct but business-irrelevant."
- `docs/canonical/eval-to-production-correlation-tracking.md:22` — "Eval scores become false safety signals when they stop predicting user outcomes."
- `docs/canonical/eval-to-production-correlation-tracking.md:35` — "Production outcomes | Task success, complaints, escalations, support tickets, CSAT proxy, latency, cost, retention, or domain-specific success metrics."
- NOT_FOUND (vanity-metric rejection and architecture→skill ordering): searched repo `*.md` with `vanity|proxy KPI|superficial` — matches are unrelated (reward-hacking prevention via blind rubrics, `curriculum/GLOSSARY.md:98`); no doc names call-count/minutes-on-call vanity KPIs or orders architecture optimizations and skill additions by outcome impact.

**Integration Value:** Medium — the business-outcome anchor is already canonical; the additions (outcome→architecture→skill hierarchy as one loop, vanity-KPI taxonomy) are incremental enrichment to existing docs rather than a new capability.

---

## 12. Mega-Expert Consolidation

**Classification:** Missing

**Justification:** NOT_FOUND in any form. The pattern's mechanism — build one agent per specialty domain, benchmark each against the best individual human expert, then fuse the proven-superhuman specialists into a single customer-facing mega expert — has no canonical doc, skill, curriculum lesson, or analysis treatment. Searched: `docs/canonical/` with `mega|specialist|superhuman|best human|deflection bot|fusion|consolidat|generalist` (matches are only the Kavak source package, the anti-pattern "dense mega-prompts" in `goal-atomicity-split.md:92`, and persona documentation for human specialists in `persona-based-documentation.md:23` — knowledge capture, not agent consolidation); the active canonical pattern table in `docs/system-of-record.md:172-299` (no entry covers agent consolidation or fusion); `curriculum/` (no mega-expert or specialist-fusion content); `.opencode/skills/` (per system-of-record skills table, `docs/system-of-record.md:33-65` — no consolidation skill). Adjacent-but-different concepts confirmed during search: multi-agent-fault-tolerance (orchestration reliability, not fusion), persona-based-documentation (specialist knowledge as docs), split-brain-planning-review (separate rubrics, not unified agents).

**Evidence (adjacent concepts inspected, mechanism itself NOT_FOUND):**
- `docs/canonical/persona-based-documentation.md:23` — "When a team has specialists in different domains, their expertise is not systematically captured in durable documentation surfaces that agents can load." (specialists as documentation sources, not as agents to fuse)
- `docs/canonical/goal-atomicity-split.md:92` — "Scales agent work by decomposition instead of by dense mega-prompts -- one outcome per intent" (only "mega" usage in canonical/, an anti-pattern reference)
- Searched locations with no match for the pattern: `docs/canonical/` (grep as above), `docs/system-of-record.md:172-299` (canonical table), `curriculum/` (grep mega-expert/specialist fusion), `docs/analysis/` (only the Kavak source package itself), `.opencode/skills/` (skills table at `docs/system-of-record.md:33-65`).

**Integration Value:** Medium — relevant to the KODA case (a single customer-facing agent spanning the full sales journey) and to Level 4 / multi-agent coordination content as a design rationale (unified expert vs. specialist fragmentation with handoffs), but the org-consolidation framing sits at the periphery of the repo's harness-engineering core.

---

## 13. Production-Contact Training Loop

**Classification:** Partial Coverage

**Justification:** The mechanism is documented at considerable depth. The On-Policy Rollout Feedback Loop states the Kavak convergence claim in different words (exposure-bias gap: agents trained/evaluated only on curated scripts break on their own production trajectories) and prescribes the exact loop — capture production traces, score them, feed back as update targets (prompts, skills, eval cases, memory policy, training data), re-run and verify. Production-Grounded Eval Sampling supplies the harvesting infrastructure ("hand-authored eval sets miss real user distributions"), the Production Failure Regression Flywheel and Living Eval Dataset convert production contact into permanent assets, and the curriculum teaches the lab-vs-production distinction explicitly. Missing: (a) the organizational stance that real-customer contact is the *precondition* for agents working at all (the Kavak pattern makes it the only observed convergence mechanism, not one option among several — the repo's on-policy doc still allows teacher-mixed/lab-side sampling for cold start); and (b) the identity reframe that the harvested data and feedback loops *are* the agents rather than groundwork for them.

**Evidence:**
- `docs/canonical/on-policy-rollout-feedback-loop.md:33` — "An agent trained or evaluated only on curated scripts breaks when its own production trajectories contain early mistakes, strange tool outputs, or context drift that never appeared in the static data."
- `docs/canonical/on-policy-rollout-feedback-loop.md:41` — "Close the exposure-bias gap by making the agent's own production trajectories the learning signal. ... Feed those scored prefixes back as update targets: prompt rules, skills, eval cases, memory policy, or training data. Then re-run the task against the updated agent and measure whether performance improved."
- `docs/canonical/production-grounded-eval-sampling.md:22` — "Hand-authored eval sets miss real user distributions and long-tail agent failures."
- `docs/canonical/production-failure-regression-flywheel.md:28` — "Every production failure that reveals a behavioral gap should become a durable eval regression case unless it is explicitly rejected as duplicate, unactionable, or out of scope."
- `docs/canonical/living-eval-dataset.md:28` — "A **monotonically growing** eval dataset: every production incident, every escaped edge case, every new feature specification becomes a permanent addition to the dataset."
- `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1625` — "O replay de conversas reais anonimizadas deixa de ser uma atividade genérica e vira um artefato nomeado: `production_sampled_eval_corpus`."
- `curriculum/02-nivel-2-practical-patterns/exercises/solutions/exercise-03-solution.md:2477` — "É a diferença entre um agente que **funciona no laboratório** e um agente que **funciona em produção, com clientes reais**, por horas a fio."

**Integration Value:** Medium — the harvesting/eval/update mechanics exist across four canonical docs; what would be added is the convergence-first sequencing principle (production contact as precondition, gated by evals-as-brakes) and the "agents are the feedback loops" identity claim — a reframe enriching the existing cluster rather than a new mechanism.

---

## 14. Carve-Out Pilot with Hard P&L Target

**Classification:** Partial Coverage

**Justification:** Elements of containment and outcome-anchored first slices exist. The Domain-Embedded Workflow Automation Wedge selects a first automation slice with "bounded scope ... and testable outcome" and prefers "clear before/after outcome evidence"; blast-radius containment exists at task/module level (Human-AFK Task Routing Gate, Architecture-as-Agent-Affordance); and technical canary/shadow staging provides contained rollout with real-metric readout. The repo also has generic hard-goal machinery (Two-Implementations Goal Test, Intent Five-Part Primitive's goal slot). Missing key mechanics: an agent installed as the operator/CEO of a contained operating unit; a hard financial P&L target as the eval readout (e.g., 2x profits); and the plan-push/telemetry loop with human workers. Grepping `pilot|carve|P&L` over `docs/canonical/` returns no match — all "blast radius"/"isolated" hits are module-coupling, review-severity, or worktree contexts, not business-unit experiments.

**Evidence:**
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:38` — "Automation wedge | Small workflow slice with high pain, bounded scope, available data, clear owner, and testable outcome"
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:44` — "Prefer slices with clear before/after outcome evidence, not merely impressive model behavior."
- `docs/canonical/human-afk-task-routing-gate.md:35` — "The change crosses module boundaries, introduces new abstractions, or has system-wide blast radius" (blast-radius containment exists at task-routing level, not business-unit level).
- NOT_FOUND (agent-run operating unit / hard P&L target): searched `docs/canonical/` with `pilot|carve|P&L|blast radius|isolated` — blast-radius matches are module design (`architecture-as-agent-affordance.md:38`), review calibration (`contextual-severity-calibration.md:25`), and task routing; no document covers an agent running a contained business unit against a profit target.

**Integration Value:** High — the repo's audience is business people building agent systems around a revenue-generating sales agent (KODA); a pattern bridging technical canary containment and business-level proof (isolated unit, hard financial target as the eval) fills the gap between the repo's wedge/canary mechanics and org-level adoption, and slots naturally into Level 4 / production curriculum.

---

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
| 9 | Evals-as-Brakes | Partial Coverage | High |
| 10 | Eval-Investment Parity | Partial Coverage | Medium |
| 11 | Outcome-Level Eval Hierarchy | Partial Coverage | Medium |
| 12 | Mega-Expert Consolidation | Missing | Medium |
| 13 | Production-Contact Training Loop | Partial Coverage | Medium |
| 14 | Carve-Out Pilot with Hard P&L Target | Partial Coverage | High |

**Distribuição:** 2 Missing (Mega-Expert Consolidation, Sidekick Pattern) · 9 Partial Coverage (4 High, 5 Medium) · 1 Better Implementation (Scaffold Deletion) · 2 Missing patterns → P0; PC High → P1; PC Medium → P2.
