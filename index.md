---
title: "Long-Running Agents — Knowledge Index"
type: index
aliases: ["index", "home", "mapa"]
tags: [index]
last_updated: 2026-06-10
---

## Canonical Patterns

- [[docs/canonical/addressable-memory-catalog.md|Addressable Memory Catalog]] — Defines stable IDs, locations, previews, scopes, and fetch handles for omitted context.
- [[docs/canonical/deterministic-tool-dispatch.md|Deterministic Tool Dispatch]] — Reframes tools as model-emitted JSON routed through deterministic, testable application code.
- [[docs/canonical/error-context-hygiene.md|Error Context Hygiene]] — Curates failed tool-call context through summaries, success clearing, and strict error-size control.
- [[docs/canonical/eval-tier-stratification.md|Eval Tier Stratification]] — Organizes eval suites into fast, medium, and deep tiers with explicit decision power.
- [[docs/canonical/eval-to-production-correlation-tracking.md|Eval-to-Production Correlation Tracking]] — Audits whether eval scores still predict production outcomes across releases and metric windows.
- [[docs/canonical/head-tail-context-truncation.md|Head-Tail Context Truncation with Recoverable Middle]] — Preserves durable head, current tail, stable prompt, and retrievable omitted middle context.
- [[docs/canonical/late-failure-regression-suite.md|Late-Failure Regression Suite]] — Turns late-session context failures into durable fixtures for regression testing and rollout gates.
- [[docs/canonical/n-plus-one-long-session-evals.md|N+1 Long-Session Evals]] — Tests turn N+1 after production context reduction to catch continuity and retrieval failures.
- [[docs/canonical/owned-agent-control-loop.md|Owned Agent Control Loop]] — Splits agent operation into owned prompt, context builder, dispatch, and loop components.
- [[docs/canonical/pain-signal-eval-progression-gate.md|Pain-Signal Eval Progression Gate]] — Advances eval maturity only when observed pain justifies the next minimum capability.
- [[docs/canonical/pr-gated-eval-enforcement.md|PR-Gated Eval Enforcement]] — Requires eval reports and merge policy for prompt, model, tool, context, and loop changes.
- [[docs/canonical/production-failure-regression-flywheel.md|Production Failure Regression Flywheel]] — Converts production failures, complaints, and scoring gaps into tiered regression eval cases.
- [[docs/canonical/production-grounded-eval-sampling.md|Production-Grounded Eval Sampling]] — Builds replayable eval datasets from representative production interactions with privacy and metadata controls.
- [[docs/canonical/repeatable-agent-spot-check-set.md|Repeatable Agent Spot-Check Set]] — Defines a small seed set of repeatable cases for critical agent workflow checks.
- [[docs/canonical/serializable-pause-resume-state.md|Serializable Pause/Resume State]] — Serializes context, execution, and business state so agents can pause and resume reliably.
- [[docs/canonical/stable-harness-prompt.md|Stable Harness Prompt During Context Reduction]] — Keeps harness instructions separate, versioned, and non-reducible during context compaction.

## System of Record

- [[docs/system-of-record.md|System of Record]] — Defines documentation precedence, canonical domains, active patterns, analyses, and current ADR status.

## Analyses

- [[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis.md|12-Factor Agents Analysis]] — Extracts the owned loop, deterministic dispatch, micro-agent, and scaffold patterns from 12-Factor Agents.
- [[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-patterns.md|12-Factor Agents Patterns]] — Lists extracted agentic patterns with reusable problem, mechanism, and tradeoff structures.
- [[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md|12-Factor Agents Classification]] — Compares extracted 12FA patterns against repository coverage and implementation gaps.
- [[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-integration-roadmap.md|12-Factor Agents Integration Roadmap]] — Plans how selected 12FA patterns should enter curriculum and canonical docs.
- [[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md|Context Management in Agents Analysis]] — Analyzes strategic context selection, recoverable memory, truncation, and long-session evals.
- [[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-patterns.md|Context Management Patterns]] — Extracts reusable context-management patterns for truncation, catalogs, and late-session validation.
- [[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md|Context Management Classification]] — Classifies context-management coverage across canonical docs, curriculum, evidence, and gaps.
- [[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-integration-roadmap.md|Context Management Integration Roadmap]] — Maps context-management gaps into canonical, curriculum, and evaluation work.
- [[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis.md|Eval Maturity Phases Analysis]] — Describes eval maturity from ad hoc testing to continuous eval-driven development.
- [[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-patterns.md|Eval Maturity Patterns]] — Captures production sampling, PR gates, eval tiers, and regression-flywheel operating patterns.
- [[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md|Eval Maturity Classification]] — Classifies repository coverage for eval-maturity phases and identifies missing formal mechanisms.
- [[docs/analysis/2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-integration-roadmap.md|Eval Maturity Integration Roadmap]] — Prioritizes how eval-maturity patterns should become canonical and operational guidance.
- [[docs/analysis/mhc-backend/2026-05-26-harness-diagnostic.md|MHC Backend Harness Diagnostic]] — Diagnoses KODA backend architecture against Level 1 harness patterns and state infrastructure.
- [[docs/analysis/mhc-backend/2026-05-26-nivel-2-diagnostic.md|MHC Backend Level 2 Diagnostic]] — Assesses practical pattern maturity for KODA workflows and validation behavior.
- [[docs/analysis/mhc-backend/2026-05-26-nivel-3-comparacao.md|MHC Backend Level 3 Comparison]] — Compares KODA architecture with advanced multi-agent and state-persistence expectations.
- [[docs/analysis/mhc-backend/2026-05-26-pedido-bling-agente.md|Pedido Bling Agent Failure Analysis]] — Investigates a paid-order notification failure across webhook, ERP, and agent flow.
- [[docs/analysis/mhc-backend/2026-05-28-janela-deslizante-contexto.md|Sliding Context Window Diagnostic]] — Reviews context windowing, summaries, metadata, and sliding-history behavior in the agent.
- [[docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence.md|Output Validation and State Persistence Diagnostic]] — Examines validation layers, structured outputs, and state persistence mechanisms.
- [[docs/analysis/mhc-backend/2026-05-28-output-validation-structured-generation.md|Structured Generation Diagnostic]] — Reviews Zod, LangChain, and structured-output validation practices in MHC backend flows.

## Curriculum

- [[curriculum/INDEX.md|Curriculum Index]] — Provides quick navigation paths by learner profile, content type, and lookup need.
- [[curriculum/MASTER_PLAN.md|Curriculum Master Plan]] — Maps the complete 12-week program, levels, concepts, exercises, and KODA integration.
- [[curriculum/README.md|Curriculum README]] — Introduces the 12-week program for reliable long-running agents applied to KODA.
- [[curriculum/QUICK_START.md|Curriculum Quick Start]] — Onboards learners in 45 minutes with paths for beginners, LLM users, architects, and KODA work.
- [[curriculum/EXECUTION_PLAN.md|Curriculum Execution Plan]] — Breaks the 12-week rollout into weekly phases, activities, owners, and learning outcomes.
- [[curriculum/GLOSSARY.md|Curriculum Glossary]] — Defines core long-running-agent terms, KODA examples, levels, and cross-references.
- [[curriculum/FAQ.md|Curriculum FAQ]] — Answers participant, mentor, and technical questions about learning and applying the curriculum.
- [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md|01-nivel-1-fundamentals/]] — Covers fundamental failure modes: context amnesia, planning collapse, and weak harnesses.
- [[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md|02-nivel-2-practical-patterns/]] — Teaches practical reliability patterns such as Generator/Evaluator, sprint contracts, rubrics, and trace reading.
- [[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems.md|03-nivel-3-advanced-architecture/]] — Explains advanced multi-agent systems, state persistence, file coordination, and server-side compaction.
- [[curriculum/04-nivel-4-koda-specific/01-koda-architecture.md|04-nivel-4-koda-specific/]] — Applies curriculum patterns directly to KODA architecture, journeys, features, evals, and harness improvements.
- [[curriculum/05-core-concepts/01-context-management.md|05-core-concepts/]] — Expands eight core concepts behind long-running-agent context, state, coordination, and evaluation.
- [[curriculum/06-knowledge-graphs/01-concept-ecosystem.md|06-knowledge-graphs/]] — Visualizes concept ecosystems, learning progression, dependencies, and problem-solution relationships.
- [[curriculum/07-implementation-guides/01-setup-guide.md|07-implementation-guides/]] — Provides setup, team progression, harness design, trace analysis, and evolution playbooks.
- [[curriculum/08-tools-templates/architecture-decision-record-template.md|08-tools-templates/]] — Supplies reusable ADR, rubric, sprint contract, tracker, and knowledge-graph templates.
- [[curriculum/09-case-studies/00-all-case-studies.md|09-case-studies/]] — Demonstrates five long-running-agent case studies, including generic systems and KODA workflows.
- [[curriculum/10-references/additional-resources.md|10-references/]] — Curates papers, posts, videos, repositories, tools, and model capability references.

## Architecture Decisions

- [[docs/system-of-record.md|Architecture Decisions Status]] — Records that `docs/decisions/` is currently empty and no accepted ADRs exist.
- [[curriculum/08-tools-templates/architecture-decision-record-template.md|Architecture Decision Record Template]] — Provides the ADR structure intended for future entries in `docs/decisions/`.

## Plans

- [[docs/plans/2026-05-26-curriculum-completion-strategy.md|Curriculum Completion Strategy]] — Plans GitHub Issues, milestones, dependencies, priorities, and automation for completing curriculum files.

## Project Docs

- [[README.md|Repository README]] — Introduces long-running-agents, quick start commands, project structure, and Node requirement.
- [[AGENTS.md|Agent Working Rules]] — Defines mandatory agent rules, repository context, validation gates, precedence, and security constraints.
