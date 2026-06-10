---
title: "Agentic Patterns from Stanford CS153 AI Native Company"
type: analysis
date: 2026-06-10
sources:
  - "docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/analysis.md"
tags: [agentes-orquestracao, evals, context-engineering]
---

# Agentic Patterns from Stanford CS153 AI Native Company

Scope: extracted from [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/analysis|analysis.md]]. Only patterns applicable to agentic systems, agent engineering, or long-running agent operations are kept. General company-role advice, market commentary, and strategy without an agentic operating mechanism are excluded.

## 1. Closed-Loop Agent Operating System

- **name:** Closed-Loop Agent Operating System
- **problem solved:** Long-running agents drift when decisions, failures, and next actions live in human heads, private messages, and incomplete notes.
- **inputs:**
  - Company or product state such as code, issues, chat, meetings, customer artifacts, and shared memory.
  - Agent-accessible operational artifacts and ownership metadata.
  - Feedback signals from bugs, decisions, customer outcomes, and unfinished work.
- **outputs:**
  - Suggested next work, bug fixes, and decision updates from the agentic controller.
  - Updated operational memory that future agents can read.
  - A tighter feedback loop between observed state and execution priorities.
- **benefits:**
  - Reduces information loss between humans, artifacts, and agents.
  - Makes long-running operations self-correcting instead of dependent on recall.
  - Turns agent read access into an operational control loop rather than a chatbot interface.
- **limitations:**
  - Requires broad, well-governed read access to real operational artifacts.
  - Produces noisy recommendations if ownership, memory, or source quality is weak.
  - Does not work as a one-off prompt; it needs persistent artifact hygiene and feedback intake.

## 2. Agentic Software Factory Quality Gate

- **name:** Agentic Software Factory Quality Gate
- **problem solved:** High-volume agent code generation becomes AI slop when it lacks production validation and review loops.
- **inputs:**
  - Agent-generated code, plans, tests, and review traces.
  - Quality gates such as engineering review, coverage thresholds, and production readiness checks.
  - Operator and customer evidence that the product actually works.
- **outputs:**
  - Code that has passed review, tests, and usage-oriented validation.
  - Coverage and quality evidence attached to the agent-produced change.
  - Rejected or reworked outputs when generated volume does not meet the gate.
- **benefits:**
  - Shifts the metric from code volume to usable software.
  - Converts abundant generation into maintainable production output.
  - Creates an anti-slop boundary before agent work reaches users.
- **limitations:**
  - Coverage targets can become theater if they do not represent real behavior.
  - Review and test infrastructure add cost before the factory becomes reliable.
  - The pattern is too heavy for throwaway experiments that will never ship.

## 3. Latent-Deterministic Boundary Enforcement

- **name:** Latent-Deterministic Boundary Enforcement
- **problem solved:** Agents hallucinate or become brittle when exact facts are left to latent judgment or open-ended judgment is hardcoded into deterministic code.
- **inputs:**
  - Candidate task requirements, including which parts require semantic judgment and which require exactness.
  - Deterministic tools for time, calendar, routing, tests, state, and formal invariants.
  - Prompt or skill instructions for ambiguous semantic work.
- **outputs:**
  - A boundary map between model-owned judgment and code-owned exactness.
  - Tested deterministic context injected into the agent as facts.
  - Cleaner prompts and tools that each own the work they are suited for.
- **benefits:**
  - Prevents failures such as timezone hallucination and markdown-only invariants.
  - Makes exact context testable with normal software techniques.
  - Keeps the model focused on ambiguity, synthesis, and semantic decisions.
- **limitations:**
  - Requires design effort to classify work correctly at the boundary.
  - Over-coding judgment can make the system rigid and domain-blind.
  - Over-prompting exactness leaves correctness to an unreliable latent process.

## 4. Skill-Resolver-Skillify Capability Pipeline

- **name:** Skill-Resolver-Skillify Capability Pipeline
- **problem solved:** Successful agent workflows stay fragile when they remain as ad hoc prompts, one-off macros, or accumulated global instructions.
- **inputs:**
  - A workflow that has worked at least once with known input and output behavior.
  - Skill content, supporting deterministic code, tests, evals, resolver triggers, and storage schema.
  - Audit checks such as trigger evals, integration tests, smoke tests, and check-resolvable.
- **outputs:**
  - A registered, testable, routable skill that agents can load on demand.
  - Resolver metadata that makes the capability discoverable at the right moment.
  - Compliance evidence that the skill is not a one-shot macro.
- **benefits:**
  - Turns repeated manual work into durable agent capability.
  - Keeps agent capability growth auditable and deduplicated.
  - Preserves working knowledge without bloating the global prompt.
- **limitations:**
  - Most of the work is testing, routing, and compliance rather than writing the skill text.
  - Duplicate skills can appear without strong resolver hygiene.
  - A skill that exists but fails trigger evals still behaves as unavailable in practice.

## 5. Resolver-Based Context Progressive Disclosure

- **name:** Resolver-Based Context Progressive Disclosure
- **problem solved:** Monolithic instruction files pollute every agent context with rarely relevant guidance until the context window overflows or behavior degrades.
- **inputs:**
  - Global instructions, workflow runbooks, domain rules, and accumulated corrections.
  - Resolver rules that map task situations to specific skills or documents.
  - Trigger examples and negative examples for when a skill should not load.
- **outputs:**
  - Smaller base context with task-specific skills loaded only when relevant.
  - A directory of capabilities instead of one giant prompt file.
  - Trigger eval results that measure whether the resolver loads the right capability.
- **benefits:**
  - Reduces token pressure and prompt interference in long sessions.
  - Makes context architecture explicit and testable.
  - Lets agent instructions grow without making every task pay the full context cost.
- **limitations:**
  - Requires taxonomy, trigger design, and ongoing deduplication.
  - Resolver misses can silently remove needed instructions from the agent context.
  - Trigger evals can give false confidence if they do not cover realistic tasks.

## 6. Split-Brain Planning Review

- **name:** Split-Brain Planning Review
- **problem solved:** A single planning agent can conflate implementation quality with product direction and optimize neither well.
- **inputs:**
  - Current plan, implementation constraints, product goals, and desired outcome.
  - Engineering-review criteria such as coverage, maintainability, and production risk.
  - CEO-review criteria such as 10x ambition, ideal target state, and staged roadmap.
- **outputs:**
  - Engineering feedback on quality, tests, and production readiness.
  - Product-direction feedback on the stronger destination and path from current state.
  - A revised plan that separates build correctness from strategic direction.
- **benefits:**
  - Prevents quality review from flattening ambition and ambition review from ignoring operability.
  - Gives agents clearer reviewer roles with different rubrics.
  - Improves long-running plans by separating near-term execution gates from target-state design.
- **limitations:**
  - Adds reviewer overhead and may slow small changes.
  - Conflicting feedback still needs a human or orchestrator to reconcile priorities.
  - The split is only useful if each reviewer has distinct criteria and authority.

## 7. Multi-Model Evaluation Council

- **name:** Multi-Model Evaluation Council
- **problem solved:** A single model judge can reinforce its own blind spots and miss quality dimensions in agent outputs.
- **inputs:**
  - Candidate inputs, outputs, traces, and scoring rubrics.
  - Multiple evaluator models with different strengths and failure modes.
  - Aggregation rules for ratings, disagreements, and retry feedback.
- **outputs:**
  - Multi-perspective scores and qualitative critiques.
  - Disagreement signals that identify cases needing retry or human review.
  - Feedback that can be returned to planner, generator, or sub-agent loops.
- **benefits:**
  - Reduces dependence on one evaluator's preferences.
  - Surfaces more dimensions of quality before changes ship.
  - Supports planner-generator-evaluator architectures with model diversity.
- **limitations:**
  - Increases latency, cost, and aggregation complexity.
  - Multiple judges can still share benchmark or training-data blind spots.
  - Requires calibration against real outcomes to avoid sophisticated benchmark theater.

## 8. Trace-Eval-Replay Self-Healing Flywheel

- **name:** Trace-Eval-Replay Self-Healing Flywheel
- **problem solved:** Domain-specific agent failures repeat when traces are not converted into durable evals and replayed.
- **inputs:**
  - Product traces, tool calls, user outcomes, state snapshots, and failure labels.
  - Domain-specific rubrics and expected behavior for each failure case.
  - Replay infrastructure for candidate prompts, tools, skills, or model versions.
- **outputs:**
  - New eval cases derived from real failures.
  - Replay results that show whether the system still fails or has improved.
  - Prompt, skill, tool, or policy updates driven by production evidence.
- **benefits:**
  - Converts agent failures into institutional memory.
  - Improves reliability on the product's real distribution instead of generic benchmarks.
  - Creates a feedback loop for long-running agents to self-heal over time.
- **limitations:**
  - Requires trace capture, redaction, labeling, and replay infrastructure.
  - Low-quality labels can teach the system the wrong lesson.
  - Eval suites can bloat without deduplication and triage.

## 9. Epistemic Memory Graph

- **name:** Epistemic Memory Graph
- **problem solved:** Grep-only knowledge stores fail when agent memory grows across many artifacts, sources, and belief types.
- **inputs:**
  - Notes, source artifacts, backlinks, embeddings, graph relationships, and retrieval metadata.
  - Epistemic labels such as hunch, person-specific belief, and world knowledge.
  - User or workflow ontology needs that change by domain.
- **outputs:**
  - Hybrid retrieval results from search, vectors, reciprocal rank fusion, backlinks, and graph traversal.
  - Memory entries with explicit epistemic status.
  - Dynamic ontology updates that make memory useful for different agent workflows.
- **benefits:**
  - Improves retrieval quality as memory volume grows.
  - Helps agents distinguish facts, beliefs, and hypotheses before acting.
  - Supports long-running operations that need accumulated context without flattening all knowledge.
- **limitations:**
  - Adds storage, schema, and governance complexity.
  - Dynamic ontology can fragment unless ownership and migration rules exist.
  - Retrieval fusion does not fix inaccurate or stale source material by itself.

## 10. Taste-to-Domain-Eval Ownership Loop

- **name:** Taste-to-Domain-Eval Ownership Loop
- **problem solved:** Generic benchmarks do not tell whether an agent preserved trust, followed domain rules, or achieved the product goal.
- **inputs:**
  - Human product judgment, domain rules, business goals, and user trust criteria.
  - Agent traces and examples of right and wrong behavior.
  - Labels, rubrics, and scoring criteria owned by the product or domain expert.
- **outputs:**
  - Domain-specific eval rubrics and labeled cases.
  - Clear pass/fail or scored criteria for agent behavior.
  - Updates to prompts, skills, and release gates when traces reveal failures.
- **benefits:**
  - Turns taste from subjective opinion into operational quality infrastructure.
  - Aligns agent evaluation with product outcomes instead of public benchmark scores.
  - Keeps humans focused on high-leverage judgment and labeling rather than repetitive execution.
- **limitations:**
  - Requires scarce domain experts to read traces and label failures.
  - Rubrics can lag behind product changes unless maintained continuously.
  - Subjective criteria need calibration to avoid inconsistent labels.

## 11. Domain-Embedded Workflow Automation Wedge

- **name:** Domain-Embedded Workflow Automation Wedge
- **problem solved:** Agents automate shallow surfaces when builders do not understand the messy workflow behind the task.
- **inputs:**
  - A painful customer workflow with repetitive phone, email, spreadsheet, or system-of-record work.
  - Shadowing notes, operator decisions, edge cases, and integration constraints.
  - Candidate agent tasks and deterministic system integrations.
- **outputs:**
  - A grounded workflow map of what the agent should and should not automate.
  - Agent capabilities integrated into the customer's real systems.
  - Domain eval cases based on observed messy work rather than imagined demos.
- **benefits:**
  - Produces agents that match real operational work instead of surface process descriptions.
  - Reveals hidden constraints, handoffs, and failure modes before automation.
  - Creates better inputs for skills, evals, memory, and tool integrations.
- **limitations:**
  - Costs more discovery time than building from a generic workflow description.
  - Does not scale until the embedded workflow is distilled into reusable artifacts.
  - Can overfit to one customer's process without cross-customer validation.
