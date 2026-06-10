---
title: "Classification: Stanford CS153 AI Native Company Patterns"
type: analysis
tags: [agentes-orquestracao, evals, context-engineering, governanca]
date: 2026-06-10
sources:
  - "docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/patterns.md"
---
# Classification: Stanford CS153 AI Native Company Patterns

Scope: classify the 11 extracted patterns in `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/patterns.md` against `long-running-agents`, using the precedence order in `docs/system-of-record.md:14-21`. Search covered `docs/decisions/**/*.md`, `docs/canonical/*.md`, `docs/evidence/**/*.md`, `docs/analysis/**/*.md`, `curriculum/**/*.md`, and `.opencode/skills/*/SKILL.md`. `docs/decisions/**/*.md` and `docs/evidence/**/*.md` returned no Markdown files in this checkout.

## 1. Closed-Loop Agent Operating System

**Classification:** Partial Coverage.

**Justification:** The repo has a documented source-of-truth hierarchy, operational issue lifecycle, agent dashboard, and analysis pipeline, but it does not yet describe a single closed-loop operating system that continuously reads company/product artifacts, recommends next work, updates operational memory, and feeds outcomes back into prioritization. The equivalent mechanics are split across governance, HoP issue skills, and analysis workflows.

**Evidence:**
- `docs/system-of-record.md:14-21` defines the documentation precedence hierarchy used to keep operational knowledge from competing silently.
- `docs/system-of-record.md:25-46` maps the `.opencode` agent system, lifecycle skills, orchestrator, and analysis pipeline into the project domains.
- `.opencode/skills/orchestrator/SKILL.md:12-15` says the orchestrator fetches state, summarizes active work, suggests next issues, generates prompts, and cleans up sessions.
- `.opencode/skills/orchestrator/SKILL.md:27-62` defines a dashboard plus priority logic for choosing the next task.
- `.opencode/skills/analyze-and-improve/SKILL.md:46-56` defines a 7-phase pipeline from repository model through classification, improvements, integration, and curriculum deep integration.
- NOT_FOUND: exact pattern name `Closed-Loop Agent Operating System` had no matches in `docs/canonical/*.md`, `curriculum/**/*.md`, or `.opencode/skills/*/SKILL.md`; `docs/decisions/**/*.md` and `docs/evidence/**/*.md` contained no Markdown files.

**Integration value:** High. A canonical closed-loop OS frame would connect existing governance, orchestrator, issue workflow, and analysis-loop mechanics into one teachable operating model.

## 2. Agentic Software Factory Quality Gate

**Classification:** Better Implementation.

**Justification:** The extracted pattern asks for production validation and review loops around high-volume agent output. The repo goes beyond that with issue-review workflow, explicit validation gates, eval-sensitive PR reporting, eval tiering, baseline/candidate deltas, waiver metadata, and durable evidence expectations.

**Evidence:**
- `.opencode/skills/issue-review/SKILL.md:12-15` positions issue review between implementation and merge, with validation, draft PR creation, second-agent review, and no merge without user confirmation.
- `.opencode/skills/issue-review/SKILL.md:44-85` requires real package gates, surface-specific gates, eval impact data, baseline/candidate versions, tier selection, quality/latency/cost deltas, failing trace examples, and merge recommendation.
- `docs/canonical/pr-gated-eval-enforcement.md:28-53` requires eval-specific PR reports for prompt, model, tool, context, memory, scoring, and agent-loop changes, with blocking thresholds and preserved report links.
- `docs/canonical/eval-tier-stratification.md:28-49` defines fast/medium/deep tiers with runtime, cost, flakiness, trigger, threshold, reporting, owner, and escalation metadata.
- `docs/canonical/production-grounded-eval-sampling.md:28-50` adds production-sampled replay, privacy filters, coverage metadata, labels, baseline/candidate replay, and quality/latency/cost reporting.
- NOT_FOUND: exact pattern name `Agentic Software Factory Quality Gate` had no matches in `docs/canonical/*.md`, `curriculum/**/*.md`, or `.opencode/skills/*/SKILL.md`; the equivalent is distributed across issue review and canonical eval-gate docs.

**Integration value:** Low. The repo already has a stronger quality-gate system; the main value is adding the Stanford name as a cross-reference or summary frame.

## 3. Latent-Deterministic Boundary Enforcement

**Classification:** Already Exists.

**Justification:** The pattern's core rule, separate model-owned semantic judgment from code-owned exactness, is already taught and documented at equivalent depth through Deterministic Tool Dispatch and the multi-agent distinction between deterministic services and LLM agents.

**Evidence:**
- `docs/canonical/deterministic-tool-dispatch.md:22-35` states that the model emits JSON and ordinary application code parses, routes, validates, executes, and handles errors.
- `docs/canonical/deterministic-tool-dispatch.md:45-66` frames the switch statement as deterministic, testable without an LLM, auditable, observable, and circuit-breakable.
- `curriculum/05-core-concepts/07-multi-agent-coordination.md:129-146` explicitly distinguishes deterministic services for catalog, inventory, price, payment, and constraint validation from LLM agents used for judgment, language, ranking, recommendation, and evaluation.
- `curriculum/05-core-concepts/07-multi-agent-coordination.md:146-148` gives the practical boundary rule: use deterministic services for `if/else` or arithmetic, and LLM agents for judgment, natural language interpretation, or qualitative tradeoffs.
- NOT_FOUND: exact pattern name `Latent-Deterministic Boundary Enforcement` had no matches in `docs/canonical/*.md`, `curriculum/**/*.md`, or `.opencode/skills/*/SKILL.md`; the mechanism exists under different names.

**Integration value:** Low. A rename or alias could help, but the boundary is already covered.

## 4. Skill-Resolver-Skillify Capability Pipeline

**Classification:** Partial Coverage.

**Justification:** The repo has skills, skill creation targets, and an analysis-to-improvement pipeline, but it lacks the full skillify formalization from the pattern: resolver metadata, trigger evals, check-resolvable, smoke tests, storage schema, and an acceptance gate that proves a workflow became a routable capability rather than a macro.

**Evidence:**
- `docs/system-of-record.md:34-43` lists operational skills for issue lifecycle, orchestration, doc co-authoring, planning, error context hygiene, and analyze-and-improve.
- `.opencode/skills/analyze-and-improve/SKILL.md:46-56` includes improvement generation and integration phases after classification.
- `.opencode/skills/analyze-and-improve/SKILL.md:102-119` defines output slots for analysis artifacts and concrete artifacts such as canonical docs, skills, and exercises.
- `.opencode/skills/error-context-hygiene/SKILL.md:15-20` demonstrates an implemented operational skill with explicit rules for error context hygiene.
- `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/analysis.md:84` describes the missing Stanford mechanic: skillify plus unit tests, LLM evals, integration tests, resolver trigger, trigger eval, check-resolvable, smoke test, and storage schema.
- NOT_FOUND: outside the current Stanford analysis package, searches for `skillify`, `check-resolvable`, `trigger eval`, and `resolver metadata` found no canonical, curriculum, or `.opencode/skills` implementation of that full pipeline.

**Integration value:** High. This would turn the repo's existing skill library into a testable capability lifecycle.

## 5. Resolver-Based Context Progressive Disclosure

**Classification:** Partial Coverage.

**Justification:** The repo uses load-on-demand skills and compaction guidance, but it does not formalize resolver-based progressive disclosure with positive/negative triggers, trigger evals, resolver miss handling, or a replacement strategy for monolithic instruction growth.

**Evidence:**
- `.opencode/skills/issue-start/SKILL.md:16-23` defines when the issue-start skill should load, showing task-scoped skill disclosure.
- `.opencode/skills/issue-review/SKILL.md:16-23` defines when the issue-review skill should load for validation and second-pass review.
- `.opencode/skills/issue-review/SKILL.md:38-40` requires `/compact` before CI and PR creation so review context focuses on diff and validation output.
- `.opencode/skills/issue-finish/SKILL.md:25-46` narrows merge/cleanup to a separate mechanical context after approval.
- `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/analysis.md:150` identifies the anti-pattern of putting instructions into a global prompt instead of loading specific skills on demand.
- `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/analysis.md:197-200` documents token overflow, one-shot skillify, duplicate skills, and trigger-eval false confidence as failure modes not yet covered by current repo mechanics.
- NOT_FOUND: exact pattern name `Resolver-Based Context Progressive Disclosure` had no matches in `docs/canonical/*.md`, `curriculum/**/*.md`, or `.opencode/skills/*/SKILL.md`.

**Integration value:** High. The repo already has the ingredients, but formal resolver tests would reduce instruction bloat and missed skill loads.

## 6. Split-Brain Planning Review

**Classification:** Partial Coverage.

**Justification:** The repo strongly separates planning, execution, generation, and evaluation, and it requires second-agent review before merge. It does not yet split planning review into distinct engineering-quality and product/CEO-destination reviewers with separate rubrics and reconciliation rules.

**Evidence:**
- `curriculum/05-core-concepts/02-planning-execution-separation.md:47-54` describes splitting KODA work into Planner and Executor phases to avoid planning/execution collapse.
- `curriculum/05-core-concepts/02-planning-execution-separation.md:60-72` connects Planner, Generator, and Evaluator as separate responsibilities in a reliable multi-agent system.
- `curriculum/05-core-concepts/03-generator-evaluator-pattern.md:151-153` states the core separation: one role creates and another judges so the system proves it is right.
- `.opencode/skills/refine-issue/SKILL.md:8-21` decomposes high-level issues into executable sub-issues with dependency relationships.
- `.opencode/skills/issue-review/SKILL.md:12-15` supplies validation and second-agent review before merge.
- NOT_FOUND: exact pattern name `Split-Brain Planning Review`, plus Stanford-specific `CEO-review` and `10x ambition` review mechanics, had no matches in `docs/canonical/*.md`, `curriculum/**/*.md`, or `.opencode/skills/*/SKILL.md` outside the current pattern file.

**Integration value:** Medium. Existing planning and review assets would benefit from an explicit dual-rubric planning review for high-impact roadmaps, not for routine changes.

## 7. Multi-Model Evaluation Council

**Classification:** Partial Coverage.

**Justification:** The repo teaches independent evaluator roles, dual/ensemble evaluator strategies, disagreement handling, and human escalation. It does not require evaluator model diversity, formal council aggregation, or calibration across model-specific blind spots.

**Evidence:**
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:156-164` lists evaluation coordination strategies, including Dual/Ensemble Evaluator and Continuous Calibration Loop.
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:162-166` says two or more Evaluators apply the same rubric independently, compare scores, escalate divergence, and reserve ensemble evaluation for high-value decisions.
- `curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs.md:827` documents Dual/Ensemble Evaluator with independent evaluators, score comparison, high-value financial decisions, and divergence tolerance.
- `curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs.md:1660` says human review is used to calibrate rubrics, audit gray-zone cases, and review divergences between Evaluators in Dual/Ensemble mode.
- NOT_FOUND: exact pattern name `Multi-Model Evaluation Council` and model-diversity/council aggregation language had no matches outside the current Stanford pattern file.

**Integration value:** Medium. The repo has evaluator plurality, but model diversity and aggregation policy would strengthen high-risk evals.

## 8. Trace-Eval-Replay Self-Healing Flywheel

**Classification:** Already Exists.

**Justification:** The repo already documents the same flywheel at canonical depth: capture production failures and traces, label expected behavior, replay baseline and candidate versions, attach cases to eval tiers, preserve links to incidents/PRs, and use failures to improve future gates.

**Evidence:**
- `docs/canonical/production-failure-regression-flywheel.md:22-24` states the problem: production failures repeat when they rely on human memory rather than permanent tests.
- `docs/canonical/production-failure-regression-flywheel.md:28-40` defines the flywheel: intake, capture interaction/trace/tool/state versions, privacy filters, labels, dedupe, eval tier assignment, baseline/candidate backfill, links to incident/PR/analysis, and pruning.
- `docs/canonical/production-failure-regression-flywheel.md:42-53` provides a taxonomy including prompt issue, tool misuse, context loss, state persistence, scoring gap, latency/cost regression, safety/policy issue, and late-session failure.
- `docs/canonical/production-grounded-eval-sampling.md:28-50` covers production-sampled replay datasets with traces, state snapshots, labels, baseline/candidate replay, and reporting.
- `curriculum/07-implementation-guides/05-trace-analysis-guide.md:73-101` defines trace anatomy with input, context, decision, reasoning, and evaluation sections for diagnosis.
- NOT_FOUND: exact pattern name `Trace-Eval-Replay Self-Healing Flywheel` had no matches in `docs/canonical/*.md`, `curriculum/**/*.md`, or `.opencode/skills/*/SKILL.md`; the equivalent exists as `Production Failure Regression Flywheel`.

**Integration value:** Low. Only naming alignment is needed.

## 9. Epistemic Memory Graph

**Classification:** Partial Coverage.

**Justification:** The repo has knowledge graphs, addressable memory catalogs, retrieval warnings, manifests, and Obsidian-style graph documentation. It does not provide epistemic labels such as hunch/person-specific belief/world knowledge, hybrid search/vector/backlink/graph fusion, or dynamic ontology governance for agent memory.

**Evidence:**
- `docs/canonical/addressable-memory-catalog.md:22-24` says external memory must expose enough compact information for the agent to choose what to retrieve without reloading all history.
- `docs/canonical/addressable-memory-catalog.md:28-43` defines stable IDs, kind, location, preview, scope, and fetch contract for omitted memory.
- `docs/canonical/addressable-memory-catalog.md:51-55` cites adjacent retrieval, privacy/scope filters, output refs, manifests, and prior analysis memory-store mechanics.
- `docs/canonical/addressable-memory-catalog.md:57-66` says the repo still lacks an explicit omitted-memory catalog implementation and observability for offered/fetched IDs.
- `curriculum/06-knowledge-graphs/01-concept-ecosystem.md:75-91` frames knowledge graphs as a connected ecosystem of concepts rather than isolated techniques.
- `curriculum/08-tools-templates/knowledge-graph-template.md:51-60` defines knowledge graphs as methodical diagrams for dependencies, operational order, and maturity timelines.
- NOT_FOUND: exact pattern name `Epistemic Memory Graph`, and searches for `epistemic`, `hunch`, `person-specific belief`, `world knowledge`, `reciprocal rank fusion`, and dynamic ontology mechanics found no matching repo implementation outside the current Stanford pattern file.

**Integration value:** Medium. It would extend existing graph and memory work from structural retrieval into belief-status-aware memory.

## 10. Taste-to-Domain-Eval Ownership Loop

**Classification:** Better Implementation.

**Justification:** The extracted pattern asks for human product taste and domain rules to become labeled eval rubrics and release gates. The repo has a richer KODA-specific domain-eval system with weighted rubrics, blockers, decision logic, audit fields, Generator/Evaluator loops, state files, human review, continuous calibration, production outcomes, and eval-to-production correlation tracking.

**Evidence:**
- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:22-45` grounds evaluation in real KODA commercial, relational, and safety risk rather than generic benchmark quality.
- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:50-58` teaches rubrics for KODA-critical families, criteria, weights, blockers, decision logic, feedback loops, audit IDs, calibration, and evidence-based approve/reject decisions.
- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:85-126` defines a Generator/Evaluator architecture where the Evaluator applies the rubric, produces score, feedback, and decision, and blocks customer output when needed.
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:152-166` connects rubric scores to hard-rule pre-gates, loops, human sampling, ensemble evaluation, threshold routing, and continuous calibration.
- `docs/canonical/eval-to-production-correlation-tracking.md:28-50` adds correlation tracking between eval score history and production outcomes, with recalibration triggers and durable reports.
- NOT_FOUND: exact pattern name `Taste-to-Domain-Eval Ownership Loop` had no matches in `docs/canonical/*.md`, `curriculum/**/*.md`, or `.opencode/skills/*/SKILL.md`; the repo implementation is more mature under KODA rubrics and eval-correlation docs.

**Integration value:** Low. The repo already covers this deeply; a short alias could connect Stanford terminology to the existing KODA rubric system.

## 11. Domain-Embedded Workflow Automation Wedge

**Classification:** Partial Coverage.

**Justification:** The repo deeply embeds KODA workflows, customer journeys, order-processing steps, and domain-specific evals. It does not yet formalize the discovery wedge itself: shadowing messy customer work, extracting operator decisions and edge cases, and deciding which workflow slices to automate first from observed operations.

**Evidence:**
- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md:36-46` models KODA's Awareness state with trigger, goal, guard, and output.
- `curriculum/04-nivel-4-koda-specific/02-customer-journey-flows.md:76-110` decomposes Consideration into discovery, filtering, comparison, validation, and guard conditions based on customer constraints.
- `curriculum/09-case-studies/04-koda-order-processing.md:18-28` describes a real multi-step order-processing pain with six dependent stages and costly errors from a single agent.
- `curriculum/09-case-studies/04-koda-order-processing.md:31-45` turns each processing step into sprint contracts with Generator/Evaluator responsibilities, tests, and approval criteria.
- `curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda.md:24-45` ties workflow quality to WhatsApp history, preferences, restrictions, budget, tone, commercial pressure, and business validation.
- NOT_FOUND: exact pattern name `Domain-Embedded Workflow Automation Wedge`, plus explicit `shadowing notes` and `automation wedge` mechanics, had no matches in `docs/canonical/*.md`, `curriculum/**/*.md`, or `.opencode/skills/*/SKILL.md` outside the current Stanford pattern file.

**Integration value:** Medium. The repo has the domain workflows; adding the wedge would improve how new domains are discovered before automation.

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Closed-Loop Agent Operating System | Partial Coverage | High |
| 2 | Agentic Software Factory Quality Gate | Better Implementation | Low |
| 3 | Latent-Deterministic Boundary Enforcement | Already Exists | Low |
| 4 | Skill-Resolver-Skillify Capability Pipeline | Partial Coverage | High |
| 5 | Resolver-Based Context Progressive Disclosure | Partial Coverage | High |
| 6 | Split-Brain Planning Review | Partial Coverage | Medium |
| 7 | Multi-Model Evaluation Council | Partial Coverage | Medium |
| 8 | Trace-Eval-Replay Self-Healing Flywheel | Already Exists | Low |
| 9 | Epistemic Memory Graph | Partial Coverage | Medium |
| 10 | Taste-to-Domain-Eval Ownership Loop | Better Implementation | Low |
| 11 | Domain-Embedded Workflow Automation Wedge | Partial Coverage | Medium |
