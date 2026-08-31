---
title: "Classification Batch 1: GTM AI Agents — Lessons from Deploying to 6,000 Users (Patterns 1-8)"
type: classification
tags: ["agentes-orquestracao", "evals", "production", "governanca"]
date: 2026-08-30
aliases: ["gtm ai agents classification batch 1", "snowflake gtm classification 1-8", "gtm 6000 users classification batch 1"]
relates-to:
  - "[[docs/system-of-record|System of Record]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|GTM AI Agents Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-mental-model|GTM AI Agents Mental Model]]"
sources:
  - "docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.yaml"
---

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
