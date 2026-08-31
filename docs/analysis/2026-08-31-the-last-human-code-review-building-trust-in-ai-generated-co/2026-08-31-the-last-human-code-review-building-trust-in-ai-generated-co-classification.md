---
title: "Classification: The Last Human Code Review — Building Trust in AI-Generated Code"
type: analysis
tags: [agentes-orquestracao, code-review, context-engineering, evals, governanca]
date: 2026-08-31
aliases: ["last human code review classification", "context engine patterns classification", "software graph review classification"]
relates-to:
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|Source Patterns]]"
  - "[[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-mental-model|Mental Model]]"
  - "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]"
  - "[[docs/canonical/relational-context-graph|Relational Context Graph]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]"
sources:
  - "docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns.md"
---

# Classification: The Last Human Code Review — Building Trust in AI-Generated Code

Evidence-based classification of the 7 extracted patterns against the `long-running-agents` repository. Pattern names are used exactly as they appear in [[docs/analysis/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co/2026-08-31-the-last-human-code-review-building-trust-in-ai-generated-co-patterns|the extracted patterns]] (canonical source). Precedence order applied per [[docs/system-of-record|System of Record]] `:14-21`: `docs/decisions/` > `docs/canonical/` > `docs/evidence/` > `docs/analysis/` > `curriculum/` > READMEs. Every classification cites `file:line` from files opened and read on 2026-08-31; `Missing` would require NOT_FOUND confirmation with the locations searched — no pattern fell to outright Missing, because the semantic-neighbor check (shadow review, staged automation, context graphs, evals-as-brakes, presence metric) surfaced real canonical anchors for all seven mechanisms. All searches executed 2026-08-31.

---

## 1. Dual-Interface Context Engine

**Classification: Partial Coverage**

**Justification:** Both consumption interfaces exist as canonical patterns and as the repo's operating model, but the unifying reframe — one governed codification layer rendered twice (verbose/structured for agents, wiki-style for humans) with auditability-by-link — is absent. The codification side is covered: Persona-Based Documentation prescribes capturing specialist knowledge as durable NFR documents that reviewer agents load (and its own gap section admits the surfaces do not exist yet); File-System Materialization supplies the single-representation principle (knowledge bases as files/git/grep — one materialization, both consumers); Resolver-Based Context Progressive Disclosure supplies the agent-facing structured interface; the Obsidian conventions (frontmatter, wikilinks, tags) supply the human-facing wiki style with machine-validatable metadata, and the `obsidian-eval` CLI makes the same vault agent-queryable. Cross-Context Knowledge Siloing documents the exact fragmentation pathology the "context lake" solves. Missing: the codify-once-render-twice principle as a stated rule, the dual renderer as a governed artifact, the self-learning ingestion pipeline (peer history, accepted/unaccepted changes, production-breaking cases as codification sources), and the review report that lists violated rules with a link to all rules applied.

**Evidence:**
- `docs/canonical/persona-based-documentation.md:23` — "When a team has specialists in different domains, their expertise is not systematically captured in durable documentation surfaces that agents can load." (tribal-knowledge codification problem named)
- `docs/canonical/persona-based-documentation.md:25` — "each team member documents their specialty (front-end architect, reliability engineer, security, product) as durable NFR documents, and reviewer agents load persona-specific rubrics"; the same line names the alternative: knowledge that "remain[s] as tacit knowledge in individual engineers' heads."
- `docs/canonical/persona-based-documentation.md:88` — "No persona-specific NFR documents exist. `AGENTS.md` is a single universal file with no persona-specific sections or role-based loading rules." (the repo's own declared implementation gap)
- `docs/canonical/file-system-materialization.md:38` — "Materialize everything into files, git, and grep: Domain logic, agent specifications, configuration, knowledge bases — if a coding agent needs to interact with it, make it a file. The file system is the universal interface that every coding model understands."
- `docs/canonical/file-system-materialization.md:42` — "the agent's changes become diffs that can be reviewed, reverted, and branched — the same workflow humans use for code." (one representation serving both consumers)
- `docs/canonical/resolver-based-context-progressive-disclosure.md:28` — "Move rarely universal instructions out of the base prompt and into skills or documents that the resolver loads only when the task matches their trigger contract." (agent-facing interface)
- `docs/canonical/quarto-publishing-architecture.md:85` — "`AGENTS.md` lines 136-154 defines Obsidian document conventions as a kind of documentation contract: mandatory frontmatter with `type` and `tags`, wikilinks for cross-references, and tag taxonomy derived from system-of-record domains." (human-facing wiki style + machine-validatable)
- `docs/system-of-record.md:127` — "Runtime da CLI `obsidian-eval`: scan, query, graph, write, manifest, epistemic graph" (the same doc vault is agent-queryable).
- `docs/canonical/cross-context-knowledge-siloing.md:46` — "Knowledge created in one agent context becomes invisible to agents operating in a different context, causing repeated investigation of already-solved problems." (the fragmentation pathology)
- NOT_FOUND: `context lake` and `tribal knowledge` in `docs/canonical/` — zero matches (grep 2026-08-31). No doc states a codify-once/dual-render principle, a governed dual renderer, self-learning codification from outage/acceptance history, or a review-report artifact listing violated rules with links to the applied rule set.

**Integration value: Medium** — The unifying canonical would connect Persona-Based Documentation (spec-only), File-System Materialization, the resolver pattern, and the Obsidian conventions into one "context engine" thesis and add the missing self-learning ingestion sources; substantial adjacent infrastructure already exists, so the delta is the reframe plus the report artifact, not a new pattern family.

---

## 2. Software Graph Review Substrate

**Classification: Partial Coverage**

**Justification:** The repo has graph-substrate vocabulary at canonical depth — but for context units, not for software artifacts under review. Relational Context Graph defines nodes as tool results/decisions/state snapshots with four typed edge classes and traversal-as-query; the Epistemic Memory Graph is even implemented in `obsidian-eval`. What no doc does is make the reviewed software itself the graph: repos/services as nodes, inter-service contracts as edges carrying discussion history, in-flight PRs overlaid as bubbles, cross-PR contract-collision detection, and the review unit shifted from diff to graph. The nearest software-structure mechanic is the GC Day rubric row prescribing a structural test that asserts package dependency edges; the nearest philosophy is Architecture-as-Agent-Affordance (structure as terrain for the next agent). Relational Context Graph's own gap section declares even its context-graph components (Edge Classifier, Supersession Updater, Node Ingestor, Traversal Engine) unimplemented — the substrate is spec-level.

**Evidence:**
- `docs/canonical/relational-context-graph.md:22` — "The structural error: treating relevance as proximity in embedding space rather than as a graph property." (the graph-property reframe exists)
- `docs/canonical/relational-context-graph.md:28` — "Build a context graph where nodes represent context units (tool results, decisions, state snapshots, progress notes) and edges carry typed semantic relationships." (nodes are context units, not software/services)
- `docs/canonical/relational-context-graph.md:30-37` — the four formal edge types (Dependency, Provenance, Supersession, Causation).
- `docs/canonical/relational-context-graph.md:67-74` — the repo's own gap: "**Edge Classifier**: No component classifies relationships into the four formal edge types"; Supersession Updater, Node Ingestor, and Traversal Engine likewise declared missing.
- `docs/canonical/garbage-collection-day-meta-loop.md:64` — "| Agent repeats the same architectural dependency violation across PRs | Structural drift; no micro-harness checking dependency edges | Structural test: assert package dependency edges |" (nearest software-graph mechanic: dependency-edge assertion)
- `docs/canonical/architecture-as-agent-affordance.md:30` — "A deep module with a simple public interface and behavior-level boundary tests is not only better human design; it is more navigable terrain for the next agent."
- NOT_FOUND: `microservice|cross-PR|in-flight|collision|software graph|service graph|repo graph` in `docs/canonical/` — only `docs/canonical/budget-aware-session-handoff.md:103` and `:117`, both about handoff filename collisions (different concept). No contract-edge graph between services, no cross-PR collision detection, no review-unit shift from diff to graph anywhere in `docs/canonical/`, `curriculum/`, `.opencode/skills/`.

**Integration value: High** — The review-over-software-graph reframe (architecture-level knowledge and cross-PR contract collision entering review) is a genuine hole: the repo's graphs address memory and context, never the reviewed artifact. A canonical here would reuse the typed-edge vocabulary the repo already owns and point it at a new object.

---

## 3. Graph-Addressed Context Placement

**Classification: Partial Coverage**

**Justification:** The retrieval half is canonical: the Addressable Memory Catalog places omitted context at stable addresses (`id`, `location`, `preview`, `scope`, `tool`, `path`) for on-demand fetch; Smallest Sufficient Context prescribes retrieving the minimal token set by relational graph traversal instead of whole-dump loading; Relational Context Graph supplies the traversal primitive. Cross-Context Knowledge Siloing names the exact source failure mode — knowledge exists but the metadata that makes it retrievable is decoupled from the content — and prescribes a promotion pipeline as mitigation. Missing: the placement discipline keyed to the software graph (the source presupposes pattern 2's addressing structure — every codification act places knowledge at the node/edge where it applies), and the implementation itself: the Addressable Memory Catalog's own section declares the catalog schema and retrieval contract missing, and Smallest Sufficient Context declares retrieval handle/topic-based rather than traversal-based. The repo addresses memory units and file paths, not codified standards placed on software-structure addresses.

**Evidence:**
- `docs/canonical/addressable-memory-catalog.md:28` — "Represent omitted context as an addressable catalog. Each omitted message, tool call, span, prompt fragment, trace segment, or intermediate result receives a stable identifier plus enough metadata for the agent to choose what to fetch."
- `docs/canonical/addressable-memory-catalog.md:36-41` — catalog fields `location`, `preview`, `scope`, `tool`, `path` (workspace path validated against allowlist) — placement-plus-address contract.
- `docs/canonical/addressable-memory-catalog.md:61` — "The classification found no explicit pattern for an omitted-memory catalog with `id + location + preview` in the canonical docs, curriculum, evidence, decisions, or operational skills." (implementation declared absent)
- `docs/canonical/smallest-sufficient-context.md:28` — "determine the minimal token set the agent needs to reason correctly about the current step, retrieve only those tokens through relational graph traversal, and assemble them in their original temporal order."
- `docs/canonical/smallest-sufficient-context.md:63` — "**Relational Traversal Engine**: Retrieval is by handle or topic, not by dependency/provenance traversal. Addressable Memory Catalog provides handle-based access but does not traverse typed edges to collect connected context."
- `docs/canonical/relational-context-graph.md:39` — "traversing the graph by typed relationships converts retrieval (returning what is near) into selection (returning what is relevant)."
- `docs/canonical/cross-context-knowledge-siloing.md:53` — "the metadata that makes knowledge *retrievable* (frontmatter tags, repo namespace, memory_handles) is decoupled from the content that makes knowledge *valuable*." (the "context dumped into files is not agent-retrievable" failure mode, in repo terms)
- NOT_FOUND: placement of codified rules/standards at software-structure addresses — the software-graph terms grepped for pattern 2 (`microservice|cross-PR|in-flight|collision|software graph|service graph|repo graph`) return zero relevant matches in `docs/canonical/`; existing addressing surfaces (catalog paths, skill triggers, frontmatter tags) locate memory and instructions, never rules keyed to code nodes/edges.

**Integration value: Medium** — The traversal-retrieval principle is already canonical; the delta is the placement discipline for codified knowledge (where a rule lives is determined by the software element it governs), which would bridge the context cluster to the review surface once pattern 2's addressing structure exists.

---

## 4. Agent-to-Agent Review Comment Protocol

**Classification: Partial Coverage**

**Justification:** The ingredients exist at canonical depth, but the protocol itself — a review comment structured as agent-parseable state addressed to the next agent on the PR, plus a background fix task producing a closed fix-PR for cherry-picking — exists nowhere. Adjacent: Generator-Evaluator formalizes one agent returning an approve/reject verdict with specific feedback to the generating agent (same-iteration loop, not cross-session PR state); QA-to-Backlog converts findings into Agent-Kanban issues that agents claim (the next agent receives the finding as claimable work, not as a comment contract); Shadow Review produces structured per-check findings with graduation decisions; the issue-review skill runs second-agent review and stops before merge. The endgame inversion — human review reduced to cherry-picking pre-verified fixes — is entirely absent.

**Evidence:**
- `docs/canonical/generator-evaluator.md:31` — "The Evaluator is impartial and constraint-facing: it receives the candidate output, reads persisted client state, applies quality rubrics and business rules, and returns an approve or reject verdict with specific feedback."
- `docs/canonical/qa-to-backlog-feedback-loop.md:42` — "The new issues enter the Agent Kanban with severity labels, QA-intake metadata (source PR, finding ID, reviewer), and blocker relationships. Agents claim them through the normal ready-queue flow." (findings reach the next agent as work items)
- `docs/canonical/shadow-review-pipeline.md:62-65` — outputs include "Non-blocking AI review trace for each change" and "Data-backed threshold decisions: which checks graduate to blocking, which remain advisory, which are retired." (structured findings exist; addressed to humans/dashboard)
- `docs/canonical/pr-gated-eval-enforcement.md:61` — "The issue-review skill validates the worktree, creates a draft PR, runs second-agent review, and stops before merge." (review-to-human, not review-to-next-agent)
- NOT_FOUND: `cherry-pick|cherry pick` across `docs/` — matches only inside this source package (4 files, all under `docs/analysis/2026-08-31-the-last-human-code-review.../`). `dear agent|agent-to-agent|agent-parseable|background fix|fix task` in `docs/canonical/` — only `docs/canonical/architecture-as-agent-affordance.md:24`, `:26`, `:30`, where "next agent" means codebase navigability, not a review-comment contract. No comment format carries review state to the next PR-touching agent; no background-fix-task artifact exists.

**Integration value: Medium** — The delta is one interface artifact (the agent-addressed comment contract) plus the fix-PR handoff, composing existing pieces (Generator-Evaluator findings, QA-to-Backlog routing, shadow structured output); it would complete the repo's review loop from human-facing findings to agent-consumable state.

---

## 5. Semantic-Rule-Gated Auto Approve/Block

**Classification: Partial Coverage**

**Justification:** The graduated rule-gated gating stack exists at canonical depth and is in places more instrumented than the source account. Evals-as-Brakes defines an explicit `auto-merge` velocity tier — auto-approve machinery — gated on eval coverage (>= 0.9 of changed behaviors), PR eval report, merge threshold, and eval-to-production correlation; PR-Gated Eval Enforcement blocks merges on threshold failure with recorded waivers; the Shadow Review Pipeline graduates individual checks from advisory to blocking based on observed agreement metrics (the "adding more rules for blocking over time" mechanic, data-driven); the Pre-Commit AI Review Gate defines a confidence-tiered pass/block policy keyed to documented rules. What is missing is the source's decision substrate: approve/block driven only by codified *semantic rules* over the governed context layer — the repo's gates key on eval metrics and confidence tiers, not on an expanding set of codified review rules accumulated as auditable context; and the staged-automation philosophy deliberately keeps the human on irreversible actions (Human-Review Staged Workflow Automation) rather than codifying the approve side as rule expansion.

**Evidence:**
- `docs/canonical/evals-as-brakes.md:51` — "| Full suite green + production-correlation tracked | Auto-merge; deploy on merge |" (auto-approve tier in the velocity/coverage coupling table).
- `docs/canonical/evals-as-brakes.md:59-63` — `velocity_tiers` YAML: `- name: auto-merge` requiring `eval_coverage: ">= 0.9 of changed behaviors"`, `gates: [pr-eval-report, merge-threshold]`, `correlation: "eval score predicts production outcome"`.
- `docs/canonical/pr-gated-eval-enforcement.md:51` — "Block merge when thresholds fail unless an explicit waiver is recorded."
- `docs/canonical/shadow-review-pipeline.md:31` — "After the shadow period, agreement metrics determine which AI checks are reliable enough to graduate to blocking status."
- `docs/canonical/pre-commit-ai-review-gate.md:75` — "The gate operates with an explicit policy: block when any finding category produces a `fail` result for a high-confidence issue; allow when findings are advisory or low-confidence."; `:79` — "| High: unambiguous violation of a documented rule | Block: must fix before push |".
- `docs/canonical/human-review-staged-workflow-automation.md:58` — "**O envio irreversível permanece humano.**" — the repo's counter-philosophy: irreversible actions stay human-owned.
- NOT_FOUND: `auto-approve|auto approve|automatically approv|automerge|auto-merge` in `docs/canonical/` — only `docs/canonical/evals-as-brakes.md:59` (the velocity tier above). No doc frames approve/block decisions driven by an expanding set of codified semantic rules accumulated as auditable context; existing gates are eval-threshold/confidence driven (as cited).

**Integration value: High** — The missing semantic-rule substrate is the bridge between the repo's context cluster and its brakes cluster: rules-as-context that gate decisions would connect the context-engine patterns (1, 3) to Evals-as-Brakes and the shadow-graduation machinery — the load-bearing integration of this source.

---

## 6. Rule Lifecycle Analytics

**Classification: Partial Coverage**

**Justification:** Lifecycle analytics exist for harness components and eval categories, with real per-component catch telemetry — the STABILIZE example counts 59 real preventions in 145K turns against 340 false positives, and ROI (errors prevented x error cost / operating cost) with a below-1x-two-quarters removal rule governs update/retire/keep decisions on a quarterly cadence; GC Day reviews observations weekly and produces updated lint rules, skills, and reviewer prompts; the Eval Dashboard prescribes continuous pass/fail rates per layer/category/agent; the Failure Pattern Classification Loop records which surface caught each failure and how many instances were observed. Missing: the per-rule and per-skill dimension of the source's telemetry — how many times each codified rule caught an issue during review runs, and usage of each rule, standard, and skill during the review process — plus maintenance decisions (update/retire/keep) applied to the rules/standards/skills triad rather than to harness components. The repo measures components and evals, not the codified rule set consumed by review.

**Evidence:**
- `docs/canonical/measured-harness-evolution-lifecycle.md:46` — "The Context Loader example showed 59 real preventions in 145K turns, 340 false positives, and only 0.4% accuracy difference in a 50% shadow test with and without the component." (per-component catch/false-positive telemetry)
- `docs/canonical/measured-harness-evolution-lifecycle.md:55` — "ROI = (Erros Prevenidos × Custo Médio do Erro) / (Custo Operacional do Componente)"; `:58` — "A component with ROI below 1x for two consecutive quarters becomes a removal candidate." (data-driven retire/keep)
- `docs/canonical/measured-harness-evolution-lifecycle.md:60` — "Govern cadence with a quarterly cycle: week 1 reviews model changelogs, metrics, and component classification... Apply One In, One Out."
- `docs/canonical/garbage-collection-day-meta-loop.md:48` — "the team holds a dedicated session to review collected observations... The session produces concrete outputs: updated lint rules, new or amended skills, revised reviewer prompts, expanded eval cases, or updated NFR documents."
- `docs/canonical/eval-dashboard-primary-detection-surface.md:32` — "**Real-time pass/fail rates** per eval layer, per category (security, login, tool calls, knowledge retrieval, math/reasoning), per agent — updated continuously."
- `docs/canonical/failure-pattern-classification-loop.md:46` — "which surface caught it (review, lint, test, production), and how many instances were observed."
- NOT_FOUND: per-rule catch counters and per-skill usage telemetry — greps `catch rate|caught|per-rule|rule usage|how many times` in `docs/canonical/` return only the shadow agreement categories (`docs/canonical/shadow-review-pipeline.md:56-57`) and the failure-observation format (`docs/canonical/failure-pattern-classification-loop.md:46`); no doc counts catches or usage per codified rule/standard/skill across review runs.

**Integration value: Medium** — A per-rule/per-skill telemetry dimension would slot into the existing surfaces (Eval Dashboard, GC Day, lifecycle ROI) rather than create new infrastructure; the delta is the rule/skill object set and continuous review-run instrumentation.

---

## 7. Comment-Decay Readiness Signal

**Classification: Partial Coverage**

**Justification:** Human-involvement measurement and graduation machinery both exist, but the specific readiness signal — volume and trend of human comments per PR decaying toward zero, with an accumulated count of PRs passing without human review (~100) as the explicit automation-graduation criterion, decoupled from model benchmarks — is absent. Presence-in-the-Loop Metric treats human involvement as a governance metric (presence timeline, stale-presence warnings, review confidence signal) but with the opposite goal: keeping the owner engaged during execution, not certifying their exit. The Shadow Review Pipeline graduates checks to blocking on agreement metrics (AI-vs-human agreement, not human comment decay). Evals-as-Brakes gates its auto-merge tier on eval coverage/correlation (eval-based readiness, not behavioral comment trends). The autonomy curriculum's phase progression (Observe→Assist→Own) stages human withdrawal without an observable per-PR decay criterion. No doc measures human comments per PR, and no accumulated PRs-without-human-review counter or graduation threshold exists.

**Evidence:**
- `docs/canonical/presence-in-the-loop-metric.md:31` — "Treat human presence during agent execution as a governance metric, not as an assumption. Measure when the outcome owner was involved, detect when they have been absent too long, and require intervention points before the loop continues."
- `docs/canonical/presence-in-the-loop-metric.md:63` — "The signal does not replace the review -- it informs the reviewer about how much ownership was exercised during construction." (presence as review-confidence input, not exit criterion)
- `docs/canonical/shadow-review-pipeline.md:31` — "After the shadow period, agreement metrics determine which AI checks are reliable enough to graduate to blocking status." (graduation criterion exists; signal is agreement, not comment decay)
- `docs/canonical/evals-as-brakes.md:59-63` — the auto-merge tier's requirements (eval coverage, correlation) constitute the repo's automation-readiness criteria — eval-based, not behavioral.
- `docs/canonical/human-review-staged-workflow-automation.md:67` — quotes the phase progression: "Observe (human does, agent watches) -> Assist (agent proposes, human approves) -> Own (agent executes, human monitors exceptions)" (`docs/canonical/autonomy-curriculum-sampling.md:60`).
- NOT_FOUND: `human comments|comment volume|comments per PR|without human review` in `docs/canonical/` — zero matches (grep 2026-08-31; the only `benchmark` hits are unrelated: benchmark selection in `docs/canonical/institutional-layer-amplification.md:51-52` and best-human benchmarking in `docs/canonical/mega-expert-consolidation.md:41`). No ~100-PR threshold, no accumulated pass-without-review counter, no decoupling of review-readiness from model benchmarks.

**Integration value: Medium** — The behavioral graduation criterion would fill the decision slot atop existing anchors (presence metric, shadow graduation, auto-merge tier) — one observable trend metric plus a threshold, natural KODA N4/production content; it is the trigger the source's entire staged-automation stack (patterns 5-6) aims at.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Dual-Interface Context Engine | Partial Coverage | Medium |
| 2 | Software Graph Review Substrate | Partial Coverage | High |
| 3 | Graph-Addressed Context Placement | Partial Coverage | Medium |
| 4 | Agent-to-Agent Review Comment Protocol | Partial Coverage | Medium |
| 5 | Semantic-Rule-Gated Auto Approve/Block | Partial Coverage | High |
| 6 | Rule Lifecycle Analytics | Partial Coverage | Medium |
| 7 | Comment-Decay Readiness Signal | Partial Coverage | Medium |

**Distribuição:** 7 Partial Coverage (2 High, 5 Medium) · 0 Missing · 0 Already Exists · 0 Better Implementation. Nenhum padrão caiu em Missing: a checagem anti-falso-Missing contra os vizinhos semânticos ([[docs/canonical/human-review-staged-workflow-automation|staged automation]], [[docs/canonical/shadow-review-pipeline|shadow review]], [[docs/canonical/pre-commit-ai-review-gate|pre-commit gate]], [[docs/canonical/relational-context-graph|relational graph]], [[docs/canonical/addressable-memory-catalog|addressable catalog]], [[docs/canonical/evals-as-brakes|evals-as-brakes]], [[docs/canonical/presence-in-the-loop-metric|presence metric]]) encontrou âncoras canônicas reais para os sete mecanismos; os greps de mecânica confirmam o que falta em cada caso. PC High → P1; PC Medium → P2.
