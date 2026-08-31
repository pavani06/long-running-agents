---
title: "Classification: GTM AI Agents — Lessons from Deploying to 6,000 Users"
type: analysis
date: 2026-08-30
aliases: ["gtm agents classification", "snowflake gtm pattern classification", "6000 users classification"]
tags: [agentes-orquestracao, evals, production, governanca]
relates-to: ["[[docs/canonical/evals-as-brakes|Evals as Brakes]]", "[[docs/canonical/production-contact-training-loop|Production Contact Training Loop]]", "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|Source Patterns]]"]
sources: ["docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.md"]
---

# Classification: GTM AI Agents — Lessons from Deploying to 6,000 Users

Evidence-based classification of the 13 extracted patterns against the target repository.
Produced in 2 parallel batches (8 + 5 patterns) and consolidated by the orchestrator.

# Classification Batch 1: Patterns 1-8 vs. long-running-agents

Precedence order applied per `docs/system-of-record.md:14-21`: decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs. Every classification cites file:line from the repo; `Missing` confirms NOT_FOUND with the locations searched. Pattern names are used exactly as they appear in `2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.yaml` (canonical source).

---

## 1. Workflow-Derived Golden Question Set

**Classification: Partial Coverage**

**Justification:** The repo has the eval-anchoring machinery at canonical depth, but sourced from the opposite direction. Business-Outcome-First Eval Pipeline prescribes golden answers authored by domain experts and a go/no-go launch gate on the predicted deflection rate; the automation wedge formalizes "domain eval seeds" derived from observed work; the spot-check set prescribes seeding from highest-value workflows. What none of them do is author the question set from a workflow artifact *before the system exists*: the repo's golden answers are sourced from real production query logs (which requires a running system), while the GTM pattern's load mechanic is ~150 questions written up front from the extracted sales workflow, independent of what data is connected — catching a 50% accuracy baseline pre-launch. The pre-build authoring pass, the workflow-extraction artifact as question source, and the recorded first-run baseline ritual are the missing mechanics.

**Evidence:**
- `docs/canonical/business-outcome-first-eval-pipeline.md:28` — "Invert the eval pipeline construction sequence: define business success first, then create golden answers from domain experts, then build the technical pipeline to compare agent outputs against business-aligned metrics."
- `docs/canonical/business-outcome-first-eval-pipeline.md:55` — "Source ~200 real production queries from human agent logs (not synthetic queries). For each query, have a human domain expert author the expected correct response — the 'golden answer.'" (production-sourced, not pre-launch workflow-sourced)
- `docs/canonical/business-outcome-first-eval-pipeline.md:75` — "This enables evidence-based go/no-go deployment decisions: deploy when predicted deflection rate exceeds the business target, hold when it does not." (launch gate exists)
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:39` — "Domain eval seeds | Cases derived from observed work, including successful paths and exception paths" (workflow-derived eval seeds exist, without the pre-build question-authoring pass)
- `docs/canonical/repeatable-agent-spot-check-set.md:46` — "Choose 5-15 cases that cover the highest-value and highest-risk workflows."
- `docs/canonical/eval-driven-development-timeline.md:37` — "Golden answers: domain experts author correct responses for the initial ~200 queries; build the living eval dataset with categorization taxonomy" (again production-captured queries, weeks 3-4 of a running pipeline)

**Integration value: Medium** — A "pre-launch golden question set from the workflow artifact" mechanic would slot into Business-Outcome-First Eval Pipeline as its missing Step 0 and into the N4/KODA production curriculum; the surrounding golden-answer and gate infrastructure already exists, so the delta is one authoring-sequence mechanic, not a new pattern family.

---

## 2. Quality-Over-Coverage Trust Scoping

**Classification: Partial Coverage**

**Justification:** The repo gates *shipping* on quality (Evals-as-Brakes: velocity as a function of eval capacity) and cuts *first slices* narrow (automation wedge rules 1-2; carve-out pilot containment), which are the two halves of quality-over-coverage. Missing is the specific reframe: scoping the *user-facing launch surface* by accuracy zone — 50 questions at 95% instead of 100 at 70 — plus the trust-asymmetry framing (first ~5 questions decide return; 10x recovery cost), the post-launch coverage roadmap, and the demand-signal monitor ("Can I get more of that?") as the expansion trigger. A case-insensitive grep for `trust` across `docs/canonical/` returns zero matches: no canonical doc frames trust as the unit of account for scoping exposure.

**Evidence:**
- `docs/canonical/evals-as-brakes.md:32` — "Organizations respond to AI risk with the wrong dial: they slow down. ... Companies that go slow do so because they lack brakes (evals), not because slowness is safe" (quality gates velocity; not scope)
- `docs/canonical/evals-as-brakes.md:34` — "shipping velocity and safety are treated as independent dials" (the coupling the GTM pattern extends to launch scope)
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:43` — "Choose a workflow slice that operators already perform repeatedly and painfully." (narrow-first scope discipline, at workflow level)
- `docs/canonical/carve-out-pilot-hard-target.md:41` — "Carve out one contained operating unit, install an agent in the standard harness as its operator (the 'AI CEO'), and make a hard P&L number the eval readout." (containment + hard readout; org-unit level, not question-space level)
- NOT_FOUND: `trust` (case-insensitive) in `docs/canonical/` — zero matches (grep 2026-08-30; matches exist only in `docs/analysis/` packages and `docs/articles/`). NOT_FOUND for accuracy-zone mapping, launch-scope cut, or coverage roadmap in `docs/canonical/`, `curriculum/`, `.opencode/skills/`.

**Integration value: Medium** — The trust-scoped-launch reframe connects Evals-as-Brakes and the wedge rules to the user-facing rollout moment, which is exactly the KODA N4/production curriculum surface; it supplies the "why narrow" argument the repo's containment patterns imply but never state in trust-economics terms.

---

## 3. Retention-Gated Phased Rollout

**Classification: Partial Coverage**

**Justification:** Staged rollout machinery exists in depth for *infrastructure* (shadow tests, canaries, production metrics, rollback — the repo's own canonical declares it exceeds the canary-gate pattern) and for *pilots* (carve-out with hard readout and exit rule; autonomy curriculum with readiness gates per phase). Missing is the *user-population* axis: pilot cohort of AI-native early adopters → 10% beta → GA, gated on a weekly-active retention threshold (>70%) plus request-concentration clustering to define must-have data. All canonical `retention` matches refer to memory/data retention policies or list retention as one production outcome metric; none gates rollout on user retention.

**Evidence:**
- `docs/canonical/production-grounded-eval-sampling.md:107` — "staged shadow tests, canaries, production metrics, rollback, and observation exceed the canary gate pattern" (staged rollout exists, infrastructure-facing)
- `docs/canonical/carve-out-pilot-hard-target.md:41` — pilot containment with pre-registered readout; `:66` — "exit: [scale-to-next-city, iterate-harness, kill]" (explicit gate/exit discipline at pilot level)
- `docs/canonical/autonomy-curriculum-sampling.md:58` — "Readiness gates | Per-phase metrics that must pass before advancing lambda: task success rate, repair rate, unsafe-action rate, evaluator confidence" (phase gates on metrics exist; none is user retention)
- `docs/canonical/eval-to-production-correlation-tracking.md:35` — "Production outcomes | Task success, complaints, escalations, support tickets, CSAT proxy, latency, cost, retention, or domain-specific success metrics" (retention appears only as a trackable outcome, never as a rollout gate)
- NOT_FOUND: `weekly-active`, `beta cohort`, retention-gated GA, or request clustering in `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `docs/system-of-record.md` (canonical `retention` matches are memory/data retention: `docs/canonical/semantic-topic-bucketing.md:23`, `:27`; telemetry data retention in `docs/plans/2026-06-18-obs-fase5-runtime-integration.md:1448-1504`).

**Integration value: Medium** — The repo teaches deployment to business users (KODA) and already owns pilot/containment and readiness-gate vocabulary; adding the user-population phasing with a retention gate would complete the rollout story at the N4/production level without new infrastructure concepts.

---

## 4. Trial-Retention Attribution Split

**Classification: Missing**

**Justification:** NOT_FOUND. The core mechanism — per-user trial flag crossed with return/retention telemetry, producing a two-branch attribution rule (tried-and-did-not-return → product problem; never-tried → change-management problem) with ownership routing — exists in no doc, code, or curriculum material. The repo's attribution patterns attribute *token cost* (gap-cost attribution) and *trace cost* (behavioral eval path analysis), not usage telemetry; its misattribution discipline runs eval-score-vs-production-outcome, not trial-vs-return. The routing adjacency (findings triaged for ownership and converted into work) exists in QA-to-Backlog, but it routes review findings, not activation diagnostics.

**Evidence:**
- NOT_FOUND searches (2026-08-30): `attribution` in `docs/canonical/` matches only `docs/canonical/token-economics-gap-filling.md:33` ("Build a gap-cost attribution layer ... measure which tokens were spent filling gaps") and behavioral-eval-path-analysis cost attribution (`docs/system-of-record.md:202`) — different axes. `activation|adoption|trial` across `docs/canonical/`, `curriculum/`, `.opencode/skills/`, `docs/system-of-record.md` returns only harness-adoption de-risking (`docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis.md:144`), HoP role activation (`.opencode/agents/` references), and feature-activation log fields (`curriculum/06-knowledge-graphs/02-koda-feature-dependencies.md:1973`) — none equivalent.
- `docs/canonical/eval-to-production-correlation-tracking.md:22` — "Eval scores become false safety signals when they stop predicting user outcomes." (nearest analogue: misattribution discipline in the eval domain)
- `docs/canonical/qa-to-backlog-feedback-loop.md:32` — "capture QA and review findings as structured observations, triage each finding for severity, blocker status, and ownership, convert actionable findings into vertical-slice issues or regression cases" (ownership-routing adjacency)

**Integration value: Medium** — A cheap, mechanism-like diagnostic (two flags, two branches, two owners) that would feed Retention-Gated Phased Rollout and the activation side of deployment; fits the KODA N4/production curriculum where "low usage ≠ product failure" is a teachable rule. No repo surface needs to change to absorb it.

---

## 5. Owner-Led Activation Blitz

**Classification: Missing**

**Justification:** NOT_FOUND. No doc, skill, or curriculum material describes an owner-funded adoption program: 60-70% of the product owner's time in live demos, per-team adoption dashboards, publicized team rankings, or sales-leader sponsorship channels. Grep for `live demo|demo program|adoption dashboard|per-team|sponsorship` matches only the GTM source package itself and the Kavak carve-out canonical — which mentions sponsorship only to *reject* diffuse sponsored-use-case transformation, the opposite mechanism. The repo has a documented self-awareness that this class of pattern falls outside its shape: "The repo is a curriculum and canonical pattern library, not an enterprise organization."

**Evidence:**
- NOT_FOUND searches (2026-08-30): `live demo|demo program|adoption dashboard|per-team|sponsorship` across the repo — matches only in `docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/` (the source package) and `docs/canonical/carve-out-pilot-hard-target.md:33` (sponsorship named as a *failure* mode: "Hackathon/use-case-sponsorship transformation: diffuse bottom-up effort with no target org design").
- `docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification.md:218` — "The repo is a curriculum and canonical pattern library, not an enterprise organization with inherited procurement, security review, or compliance gates." (precedent for org-change patterns being out of structural scope)
- `docs/canonical/owner-of-no-role-design.md` (`docs/system-of-record.md:231`) — nearest name match: single-owner artifact accountability, not owner-led adoption campaigns (not equivalent).

**Integration value: Low** — Pure organizational change management with no agentic mechanism; its only durable hook in this repo is as a N4 case-study sidebar on the never-tried branch of the Trial-Retention Attribution Split. The Kavak canonical already covers the org-mobilization terrain it overlaps (top-down ownership) via the carve-out pilot.

---

## 6. Centralized Data Plane with Inherited RBAC

**Classification: Partial Coverage**

**Justification:** The repo has two Sierra canonicals covering agent data *governance* — Auth-Coupled Memory (access keyed by identity with confidence-gated tiers) and Regulated Data Boundary (structural isolation tier) — plus Governance Context Injection's data-catalog PII tagging and an adjacent no-code analysis (Journeys layer). Missing is the consolidation-and-inheritance architecture: all first- and third-party data unified in one platform, RBAC defined once at the data plane, and every agent deployed on it automatically inheriting access controls with zero code. `RBAC`, `data plane`, and `zero-code` appear nowhere in `docs/canonical/` outside the GTM source package; the only `role-based` canonical match is persona-based *documentation* (a different concept), and the repo has zero MCP mentions, so the per-integration-governance problem the pattern solves is unnamed.

**Evidence:**
- `docs/canonical/auth-coupled-memory-architecture.md:32` — "An auth-coupled memory architecture where memory storage, retrieval, and sensitivity gating are all keyed by identity." (access control coupled to identity — inheritance in spirit, memory-scoped)
- `docs/canonical/auth-coupled-memory-architecture.md:36` — "Identity resolution as memory key: Every memory item is stored with an identity key (phone number, account ID, session token, or device fingerprint)."
- `docs/canonical/regulated-data-boundary.md:32` — "A regulated data boundary is an architectural isolation pattern: a separate infrastructure tier handling regulated operations that is physically isolated from LLM compute." (governance as architecture, isolation-scoped)
- `docs/canonical/governance-context-injection-pii-prevention.md:22` — "Agents access enterprise data catalogs containing PII (SSN, phone, address, credit card numbers, customer names) but the model has no awareness of which fields are sensitive." (data-catalog governance surface)
- `docs/analysis/2026-06-26-the-best-ai-agents-are-simpler-than-you-think-analysis.md:186` — "The platform's no-code layer, deterministic compilation, and Ghostwriter all serve this persona shift" (adjacent zero-code agent-building, analysis level only)
- NOT_FOUND: `RBAC|role-based|data plane|zero-code` in `docs/canonical/` — matches only in the GTM source package, `docs/canonical/persona-based-documentation.md:5` (aliases for role-based *documentation*; not equivalent), and the simpler-than-you-think analysis. `MCP` — zero matches in `docs/canonical/` (grep 2026-08-30).

**Integration value: Medium** — A "define governance once at the plane, agents inherit it" canonical would unify the three existing governance canonicals (identity-keyed access, regulated boundary, PII catalog) under one architecture and name the fleet-consistency argument; the GTM source supplies the consolidation/inheritance mechanics they lack.

---

## 7. Skill Library as Instruction-Overflow Valve

**Classification: Already Exists**

**Justification:** The valve mechanism is documented at canonical depth and is the repo's own operating model. Resolver-Based Context Progressive Disclosure states the exact problem ("instruction bloat", "context overflow" from monolithic instruction files) and the exact solution (move rarely-universal instructions out of the base prompt into skills loaded on trigger); Skill-Resolver-Skillify covers the extraction procedure (workflow → routable, tested skill); Explicit Token Budget Ledger instruments the size pressure; and the implementation is live — `.opencode/skills/` runs 33 skill directories listed in the System of Record. The repo's version is in respects deeper than the source account (trigger contracts, negative triggers, skillify compliance stages, curation via garbage-collection-day). The only GTM deltas with no counterpart are contextual, not mechanical: hard instruction-window limits as the extraction trigger (the repo frames pressure as token cost, not a hard limit) and MCP orchestration-rule overflow (the repo has zero MCP usage).

**Evidence:**
- `docs/canonical/resolver-based-context-progressive-disclosure.md:22` — "Monolithic instruction files degrade long-running agents. Every correction, preference, workflow, and domain rule gets loaded into every task, even when most of it is irrelevant. The result is token pressure, prompt interference, stale guidance, and context overflow."
- `docs/canonical/resolver-based-context-progressive-disclosure.md:24` — "The pattern solves instruction bloat by replacing always-on global context with resolver-driven, task-specific disclosure."
- `docs/canonical/resolver-based-context-progressive-disclosure.md:28` — "Move rarely universal instructions out of the base prompt and into skills or documents that the resolver loads only when the task matches their trigger contract."
- `docs/canonical/skill-resolver-skillify-capability-pipeline.md:28` — "Promote repeated agent work through a capability pipeline. A workflow is accepted as a real capability only after it becomes a routable skill with resolver metadata, tests, evals, storage expectations, and smoke evidence."
- `docs/system-of-record.md:33-65` — skills table; `.opencode/skills/` directory listing 2026-08-30 = 33 entries (implemented library, not just documentation).
- `docs/system-of-record.md:186` — "Ledger explícito para calcular custo de prompt, reservas e saldo de tokens por passo" (size-pressure instrumentation).
- NOT_FOUND: `MCP` in `docs/canonical/` — zero matches; no doc frames a hard instruction-size limit as the skill-extraction trigger.

**Integration value: Low** — Nothing to integrate at pattern level; the marginal enrichment is narrative (the Snowflake 9-pages-to-skill-library trajectory as a concrete production anecdote, and the instruction-limit-as-trigger framing) for the resolver/skillify canonicals' motivation sections.

---

## 8. Human-Review Staged Workflow Automation

**Classification: Partial Coverage**

**Justification:** The human-review gate and graduated autonomy are covered at canonical depth: the autonomy curriculum's Assist phase is exactly "agent proposes, human approves" progressing to Own; the wedge requires preserving operator review where automation is unsafe; the AFK routing gate classifies what may run autonomously; the degradation ladder escalates to a human with context. Missing is the *value-staging* reframe: using the reviewed-draft workflow (monitor channels → draft into Gmail → human reviews → human sends) as the deliberate second rung of agent value beyond data Q&A — automation of external-facing *actions* where the human owns the irreversible send, adopted by the users themselves as a trust-building stage. No repo doc stages automation by action irreversibility with a human-owned send step; the repo's review gates protect code/merge decisions, not outbound external actions (and the repo has no channel monitors or MCP connections).

**Evidence:**
- `docs/canonical/autonomy-curriculum-sampling.md:60` — "Phase progression | Observe (human does, agent watches) -> Assist (agent proposes, human approves) -> Own (agent executes, human monitors exceptions)" (the draft→review stage exists as a phase)
- `docs/canonical/domain-embedded-workflow-automation-wedge.md:47` — "Preserve operator review for cases where authority, risk, or missing data makes full automation unsafe."
- `docs/canonical/human-afk-task-routing-gate.md:30` — "The gate classifies every task as AFK-ready (safe for autonomous agent execution) or human-in-loop (requires human judgment before, during, or after execution)."
- `docs/canonical/tested-degradation-ladder.md:29` — "escalates to a human with summarized context when automated recovery is insufficient, logs the outcome, and tests each rung before production reliance"
- NOT_FOUND: staged automation of external actions with a human-owned irreversible send (monitor→draft→review→send), channel monitors, or value-stage framing ("insight → action") in `docs/canonical/`, `curriculum/`, `.opencode/skills/` (searched `draft|send|inbox|Slack|channel monitor` in canonical; `MCP` — zero matches in `docs/canonical/`).

**Integration value: Medium** — The insight→action staging with human-owned send is the deployment narrative that connects the autonomy curriculum, AFK gate, and degradation ladder into a user-facing rollout story for the KODA N4 curriculum; mechanics exist, the staging reframe does not.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Workflow-Derived Golden Question Set | Partial Coverage | Medium |
| 2 | Quality-Over-Coverage Trust Scoping | Partial Coverage | Medium |
| 3 | Retention-Gated Phased Rollout | Partial Coverage | Medium |
| 4 | Trial-Retention Attribution Split | Missing | Medium |
| 5 | Owner-Led Activation Blitz | Missing | Low |
| 6 | Centralized Data Plane with Inherited RBAC | Partial Coverage | Medium |
| 7 | Skill Library as Instruction-Overflow Valve | Already Exists | Low |
| 8 | Human-Review Staged Workflow Automation | Partial Coverage | Medium |

---

# Classification Batch 2: GTM AI Agents — Lessons from Deploying to 6,000 Users

Scope: evidence-based classification of patterns 9-13 from [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|the extracted patterns]] against the `long-running-agents` repository. Batch 2 of 2. Precedence order per [[docs/system-of-record|System of Record]]: `docs/decisions/` > `docs/canonical/` > `docs/evidence/` > `docs/analysis/` > `curriculum/` > READMEs. All searches executed 2026-08-30.

## 1. Pull-Based Infrastructure on Pain

**Classification: Partial Coverage**

The core investment philosophy (build capability only when observed pain pulls it) exists at canonical depth, but scoped to eval capability and harness governance, not to the full infrastructure stack. `pain-signal-eval-progression-gate.md:28` states the exact pull principle ("Treat eval maturity as a gate driven by pain signals instead of a calendar roadmap") and `:36` adds the smallest-sufficient mandate ("Approve only the smallest eval capability that addresses the observed pain"), with the trigger mapping table and decision record at `:40-51`. The measured harness lifecycle applies the same evidence-gated logic to harness components (`measured-harness-evolution-lifecycle.md:29`, ROI threshold and quarterly cadence at `:52-62`), and `symphony-trap-awareness.md:27` names the push-based failure mode the source pattern warns against (demanding upfront "a precision that usually exists only after the system has run"), with the build-then-distill inversion at `:33`. `eval-investment-parity.md:58` even reconciles the two regimes (pain-signal gating for *which* capability, parity for aggregate allocation).

What is missing: the generalization from evals/harness to the whole infrastructure stack (CI/CD for instructions, skills, progressive disclosure, memory, interfaces beyond chat) and the launch-strategy sequencing (minimal viable launch stack, then reactive hardening in the order constraints bind). The repo's canonical depth covers the decision gate for one asset class, not the launch-minimal strategy with its explicit re-architecture-tax trade-off. NOT_FOUND for a minimal-launch-stack or reactive-hardening-sequence pattern: searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `docs/analysis/`, `curriculum/`, and `.opencode/skills/` for `pull-based`, `on pain`, `minimal launch`, `reactive hardening` (2026-08-30); matches outside the source package were scoped to eval/harness as cited above.

**Evidence:**
- `docs/canonical/pain-signal-eval-progression-gate.md:28` — pull principle: eval maturity gated by pain signals, not calendar roadmap.
- `docs/canonical/pain-signal-eval-progression-gate.md:36` — "Approve only the smallest eval capability that addresses the observed pain".
- `docs/canonical/pain-signal-eval-progression-gate.md:40-51` — pain-signal-to-minimum-capability trigger table plus decision record.
- `docs/canonical/eval-investment-parity.md:58` — stated reconciliation: pain-signal gating governs which capability to build next.
- `docs/canonical/measured-harness-evolution-lifecycle.md:29` — harness as measured lifecycle, not one-time architecture; `:52-62` — ROI threshold, quarterly cadence, One In One Out.
- `docs/canonical/symphony-trap-awareness.md:27` — anti-upfront-spec stance (push-based failure mode named); `:33` — build then distill.
- `docs/system-of-record.md:198` — Pain-Signal Eval Progression Gate as active canonical (Level 2 precedence).
- NOT_FOUND — full-stack pull-based infrastructure pattern and minimal-launch sequencing (locations searched listed above).

**Integration value: Medium** — mostly a generalization of an existing repo philosophy from evals to all infrastructure; the new surface is the launch-strategy framing and the explicit pairing with the re-architecture tax, a natural fit for [[curriculum/05-core-concepts/06-harness-evolution|Harness Evolution]] and KODA N4.

## 2. Continuous Re-Architecture Budget

**Classification: Partial Coverage**

Standing capacity-allocation rules exist, but for a different track, and the repo's documented answer to technology churn is to *avoid* rewrites rather than budget for them. `eval-investment-parity.md:43-53` defines a structurally analogous standing budget: an explicit, accepted sprint allocation (agents 50% / evals 50% across time, tokens, money) sustained every sprint, with `:56` naming the acceptance of halved builder capacity as an explicit decision. Re-architecture governance exists as cadence: `measured-harness-evolution-lifecycle.md:60` (quarterly cycle plus One In One Out) and `garbage-collection-day-meta-loop.md:48`, `:54` (weekly, non-negotiable, time-boxed re-investment protected from feature pressure). Deferred rework is tracked by `deferred-ledger-agentic-work.md` and `carry-debt-sunset-gate.md` (indexed at `docs/system-of-record.md:230`, `:234`). On churn absorption specifically, the repo canonized the Kavak alternative: `model-agnostic-agent-vm-harness.md:36-37` (harness must absorb smarter models arriving monthly without rewrites) and `:79` ("the fleet swaps by config change, not by rewrite").

What is missing: the feature-vs-re-architecture portfolio split itself (60-70/30-40), the technology-wave watchlist, and the PRD/core-design drift audit with the 80%-persistence claim. NOT_FOUND by direct search: `60-70`, `30-40`, `portfolio split`, `wave watchlist`, `watchlist`, `PRD drift`, `drift audit` across `docs/`, `curriculum/`, `.opencode/`, and READMEs returned matches only inside this source package (2026-08-30).

**Evidence:**
- `docs/canonical/eval-investment-parity.md:43-53` — standing parity allocation as explicit accepted sprint budget (analogous standing-allocation rule, different target track).
- `docs/canonical/eval-investment-parity.md:56` — halved builder capacity accepted as an explicit decision.
- `docs/canonical/measured-harness-evolution-lifecycle.md:60` — quarterly review cycle and One In One Out rule governing harness re-architecture.
- `docs/canonical/garbage-collection-day-meta-loop.md:48` — weekly GC Day working session; `:54` — cadence non-negotiable under feature pressure, time-boxed.
- `docs/canonical/model-agnostic-agent-vm-harness.md:36-37` — design constraint: absorb model waves without rewrites; `:79` — fleet swaps by config change, not rewrite.
- `docs/system-of-record.md:230`, `:234` — Deferred-Ledger Agentic Work and Carry-Debt Sunset Gate as active canonicals for deferred rework.
- NOT_FOUND — 60-70/30-40 split, technology-wave watchlist, PRD-drift audit (searched `docs/`, `curriculum/`, `.opencode/`, READMEs; only the source package matches).

**Integration value: Medium** — names a budget discipline the repo lacks for the mechanics-churn track (skills, MCP, progressive disclosure); complements parity (which covers the eval track) and would give the KODA harness-improvements curriculum a portfolio-level allocation rule.

## 3. LLM-Classified Log Taxonomy

**Classification: Partial Coverage**

The classification mechanics exist as canonical, but every existing instrument classifies agent behavior or failures; the reframe (production question logs as a demand-side instrument) is absent. Layer 2 of `3-layer-evaluation-architecture.md:45` runs LLM-as-Judge with rubric dimensions (`:82`), and `failure-pattern-classification-loop.md:31-33` defines an observe-classify-build-verify loop with a 6-class root cause taxonomy (`:54-63`), both LLM- or rubric-driven classification at production scale. The detection surface exists: `eval-dashboard-primary-detection-surface.md:50` and `:77` surface pain signals and anomalies in near-real time. Production log harvesting exists for eval grounding (`production-contact-training-loop.md:64-66`, citing production-grounded sampling and the monotonically growing dataset), and `semantic-topic-bucketing.md` (indexed at `docs/system-of-record.md:191`) does semantic topic grouping, but for context retention, not logs. The `analyze-and-improve` skill (`docs/system-of-record.md:46`) is a working LLM classification pipeline over source content, proving the tooling.

What is missing: classification of user *questions* into a hierarchical topic taxonomy (category, subcategory, example questions), the feature-gap radar over unanswered or poorly answered demand concentrations, and the cost-engineering constraint at scale. All existing consumers classify what the agent did wrong, not what users ask for. NOT_FOUND: `log taxonomy`, `question log`, `battle card`, and demand-side taxonomy searches across `docs/canonical/`, `docs/analysis/`, `curriculum/`, and `.opencode/` returned matches only inside this source package (2026-08-30).

**Evidence:**
- `docs/canonical/3-layer-evaluation-architecture.md:45` — Layer 2 Semantic/LLM-as-Judge defined; `:82` — LLM-as-Judge with rubric as the quality-surface mechanism.
- `docs/canonical/failure-pattern-classification-loop.md:31-33` — observe-classify-build-verify classification loop; `:54-63` — root cause taxonomy with class-to-surface mapping.
- `docs/canonical/eval-dashboard-primary-detection-surface.md:50` — dashboard makes pain signals visible; `:77` — anomaly alerts calibrated per layer.
- `docs/canonical/production-contact-training-loop.md:64-66` — harvesting real production interactions into the growing corpus (data source precedent).
- `docs/system-of-record.md:191` — semantic-topic-bucketing (topic grouping for context retention; different object).
- `docs/system-of-record.md:46` — analyze-and-improve skill: LLM extraction/classification pipeline with model tiering (tooling precedent).
- NOT_FOUND — hierarchical demand taxonomy over user question logs and feature-gap radar (locations searched listed above).

**Integration value: High** — fills a genuine hole: the repo has no demand-side analytics instrument. It would supply evidence to the pain-signal gate (which currently relies on complaint heuristics, `pain-signal-eval-progression-gate.md:44`), feed production-grounded eval sampling with demand-shaped cases, and give the KODA GTM curriculum a measurable coverage roadmap input.

## 4. Gap-to-Content Feedback Circuit

**Classification: Partial Coverage**

Several gap-to-improvement feedback circuits exist as canonical, but the update artifacts are eval cases, policies, or backlog items, never generated knowledge content. `on-policy-rollout-feedback-loop.md:41` feeds scored production prefixes back as update targets (prompt rules, skills, eval cases, memory policy), and `production-contact-training-loop.md:37` closes the expose-harvest-update-redeploy loop (daily cadence at `:39-54`), while explicitly listing its own missing pieces at `:69-75`. `confidence-gated-continual-learning.md:32` is the closest structural analog: a four-stage detect-suggest-review-deploy loop for knowledge fixes with confidence gating. `production-failure-regression-flywheel.md:28` converts failures into durable regression content, and `qa-to-backlog-feedback-loop.md:30-44` converts findings into backlog issues (its own partial gap declared at `:57-59`). The `analyze-and-improve` skill (`docs/system-of-record.md:46`) is a working gap-to-content circuit for the repository's own knowledge base.

What is missing: the demand-side trigger (emerging or unanswered topics from classified logs, pattern 3 upstream), the content-generation step (battle cards and enablement docs auto-generated from internal sources), the feed-back channel into the agent's knowledge, and gap-closure confirmation in subsequent logs. NOT_FOUND: `battle card`, `enablement`, `gap-to-content`, `feedback circuit` across `docs/`, `curriculum/`, and `.opencode/` matched only this source package (2026-08-30).

**Evidence:**
- `docs/canonical/on-policy-rollout-feedback-loop.md:41` — scored prefixes fed back as update targets (prompt rules, skills, eval cases, memory policy).
- `docs/canonical/production-contact-training-loop.md:37` — expose, harvest, feed back as updates, redeploy, repeat; `:39-54` — the assembled daily loop; `:69-75` — declared missing pieces.
- `docs/canonical/confidence-gated-continual-learning.md:32` — four-stage detect-suggest-review-deploy loop, confidence-gated (closest structural analog).
- `docs/canonical/production-failure-regression-flywheel.md:28` — production failures become durable eval regression cases.
- `docs/canonical/qa-to-backlog-feedback-loop.md:30-44` — capture, triage, convert, return-to-board; `:57-59` — structured-conversion gap declared.
- `docs/system-of-record.md:46` — analyze-and-improve: automated knowledge-to-content pipeline for the repo itself.
- NOT_FOUND — enablement-content generation fed back as agent knowledge and closure confirmation (locations searched listed above).

**Integration value: Medium** — the repo's loops already close gaps with eval cases and policy updates; the delta is the generated-content artifact and the demand-side trigger. Directly applicable to KODA N4 (sales knowledge gaps becoming generated agent knowledge).

## 5. Agent Value Maturity Ladder

**Classification: Missing**

NOT_FOUND in any form (doc, code, or curriculum): agent-product value stages, a switching-cost or lock-in ladder, habituation or wow-collapse signals, and a staged capability roadmap as adoption strategy. Searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `docs/analysis/`, `curriculum/`, `.opencode/`, and READMEs for `maturity ladder`, `value ladder`, `value stage`, `switching cost`, `four-stage`, `hyper-personaliz`, `wow`, `habitua` (2026-08-30). All matches are either inside this source package or in different domains: `energy-value-chain-spread-analysis.md:90` discusses switching costs in energy-market analysis, and `confidence-gated-continual-learning.md:32` has a four-stage repair loop (not value stages).

Nearest non-equivalent coverage, all progressions of *other objects*: `autonomy-curriculum-sampling.md:41` and `:60` (observe-assist-own ladder for agent autonomy with readiness gates), `measured-harness-evolution-lifecycle.md:29` (BUILD-STABILIZE-SIMPLIFY-REMOVE for harness components), the 4-level learner curriculum (`curriculum/README.md:192-247`, cited as adjacent-in-spirit at `autonomy-curriculum-sampling.md:72`), and the eval maturity phases analysis (`docs/system-of-record.md:351-359`). None models user-perceived value stages of an agent product or the lock-in economics between them. The dimension is genuinely uncovered even though the audience would receive it: `README.md:34` targets business people building agent systems.

**Evidence:**
- NOT_FOUND — value-stage model, switching-cost ladder, habituation listener, staged capability roadmap; searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `docs/analysis/`, `curriculum/`, `.opencode/`, READMEs (greps listed above; only source-package or cross-domain matches).
- `docs/canonical/autonomy-curriculum-sampling.md:41`, `:60` — nearest ladder, wrong object (agent autonomy phases, not product value stages).
- `docs/canonical/measured-harness-evolution-lifecycle.md:29` — component lifecycle progression (different object).
- `docs/system-of-record.md:351-359` — eval maturity phases analysis (maturity of evals, not agent product value).
- `README.md:34` — audience (business people) confirms the GTM/value dimension has a home but no content.

**Integration value: Medium** — opens the product-value and adoption dimension the repo does not treat; natural fit as a KODA N4 roadmap concept (staged value delivery for the WhatsApp sales agent) and as the strategic counterpoint to the reliability-centric curriculum.

## Summary

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Pull-Based Infrastructure on Pain | Partial Coverage | Medium |
| 2 | Continuous Re-Architecture Budget | Partial Coverage | Medium |
| 3 | LLM-Classified Log Taxonomy | Partial Coverage | High |
| 4 | Gap-to-Content Feedback Circuit | Partial Coverage | Medium |
| 5 | Agent Value Maturity Ladder | Missing | Medium |

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Workflow-Derived Golden Question Set | Partial Coverage | Medium |
| 2 | Quality-Over-Coverage Trust Scoping | Partial Coverage | Medium |
| 3 | Retention-Gated Phased Rollout | Partial Coverage | Medium |
| 4 | Trial-Retention Attribution Split | Missing | Medium |
| 5 | Owner-Led Activation Blitz | Missing | Low |
| 6 | Centralized Data Plane with Inherited RBAC | Partial Coverage | Medium |
| 7 | Skill Library as Instruction-Overflow Valve | Already Exists | Low |
| 8 | Human-Review Staged Workflow Automation | Partial Coverage | Medium |
| 9 | Pull-Based Infrastructure on Pain | Partial Coverage | Medium |
| 10 | Continuous Re-Architecture Budget | Partial Coverage | Medium |
| 11 | LLM-Classified Log Taxonomy | Partial Coverage | High |
| 12 | Gap-to-Content Feedback Circuit | Partial Coverage | Medium |
| 13 | Agent Value Maturity Ladder | Missing | Medium |
