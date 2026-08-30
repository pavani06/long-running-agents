# Classification — Kavak's Playbook for Rebuilding a Company Around AI (Batch 2 of 2: Patterns 9-14)

**Date:** 2026-08-30
**Type:** classification (batch 2)
**Target repository:** `long-running-agents` at `/mnt/c/Users/pavan/long-running-agents` (branch `main`)
**Input:** `2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml` (items 9-14)
**Precedence followed:** `docs/system-of-record.md:14-21` — decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs.

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

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 9 | Evals-as-Brakes | Partial Coverage | High |
| 10 | Eval-Investment Parity | Partial Coverage | Medium |
| 11 | Outcome-Level Eval Hierarchy | Partial Coverage | Medium |
| 12 | Mega-Expert Consolidation | Missing | Medium |
| 13 | Production-Contact Training Loop | Partial Coverage | Medium |
| 14 | Carve-Out Pilot with Hard P&L Target | Partial Coverage | High |
