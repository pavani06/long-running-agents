---
title: "Reusable Agentic Patterns from Matt Pocock's AI Coding Workflow"
type: analysis
tags: ["agentes-orquestracao", "context-engineering", "harness", "evals"]
date: 2026-06-07
aliases: ["Matt Pocock AI coding patterns", "workflow for AI coding patterns", "agentic coding workflow patterns"]
relates-to: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Workflow Analysis]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/generator-evaluator|Generator Evaluator]]", "[[docs/canonical/plan-execute-verify|Plan Execute Verify]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Workflow Analysis]]"]
---

# Reusable Agentic Patterns from Matt Pocock's AI Coding Workflow

Scope: extracted from the workflow analysis of Matt Pocock's AI coding workshop. Only patterns that can be reused in agentic AI coding systems are kept; generic productivity advice, tool preference, and non-agentic delivery advice are excluded.

## 1. Smart-Zone Context Management

- **name:** Smart-Zone Context Management
- **problem_solved:** Long agent sessions can enter a degraded reasoning zone before the nominal context window is full.
- **inputs:**
  - Current token budget and context size.
  - Always-loaded instructions, task scope, conversation history, and raw exploration traces.
  - Reset, compaction, delegation, and review thresholds.
- **outputs:**
  - Bounded task sizing decisions.
  - Clear-context or fresh-session handoffs.
  - Condensed summaries from delegated exploration.
  - Review contexts that start below the practical reasoning ceiling.
- **benefits:**
  - Preserves predictable reasoning quality.
  - Prevents raw discovery work from crowding out implementation judgment.
  - Makes review less dependent on an exhausted implementation context.
- **limitations:**
  - Requires token visibility and operational discipline.
  - Context resets lose conversational continuity unless durable artifacts exist.
  - Over-resetting can fragment work when task boundaries are weak.

## 2. Grill-Me Alignment Interview

- **name:** Grill-Me Alignment Interview
- **problem_solved:** Initial prompts hide assumptions and push agents into premature plans.
- **inputs:**
  - Human intent, product goals, constraints, and unresolved requirements.
  - A short interviewing skill or prompt.
  - Agent-generated recommended answers for the human to accept, edit, or reject.
- **outputs:**
  - Answered design questions.
  - Explicitly deferred decisions.
  - A decision trail that exposes scope, domain, product, and architecture assumptions.
- **benefits:**
  - Converts hidden ambiguity into explicit choices before implementation.
  - Lets the human edit suggested judgments instead of inventing every answer from scratch.
  - Reduces rework caused by discovering major decisions during coding.
- **limitations:**
  - Consumes meaningful human attention before any code is written.
  - Can feel excessive for small or already-obvious changes.
  - Works poorly when the human cannot supply the needed product or domain judgment.

## 3. Shared Design Concept Handoff

- **name:** Shared Design Concept Handoff
- **problem_solved:** A written plan cannot carry all tacit product and architecture judgment by itself.
- **inputs:**
  - The grilling conversation.
  - Human decisions, agent interpretations, tradeoffs, and deferred branches.
  - Current codebase constraints and product intent.
- **outputs:**
  - A shared human-agent mental model of the destination.
  - Assumptions that downstream PRDs, issues, and reviews must preserve.
  - A trust boundary for what the later PRD is summarizing.
- **benefits:**
  - Makes the PRD useful because alignment happened before it.
  - Keeps planning focused on mutual understanding instead of artifact completeness.
  - Gives reviewers a basis for checking intent, not just prose compliance.
- **limitations:**
  - The richest alignment may remain partly conversational and hard to serialize.
  - It decays if later agents receive only a shallow summary.
  - It does not replace code reading, testing, or final behavior review.

## 4. Destination PRD

- **name:** Destination PRD
- **problem_solved:** Detailed plans can become brittle pseudo-specifications while still missing the real design intent.
- **inputs:**
  - Shared design context from the alignment interview.
  - Problem statement, solution shape, user stories, implementation decisions, test expectations, and out-of-scope boundaries.
  - Known dependencies and non-goals.
- **outputs:**
  - A navigational PRD that points toward the target state.
  - Source material for issue decomposition.
  - Explicit scope and exclusion boundaries.
- **benefits:**
  - Preserves direction without pretending the document can generate correct code by itself.
  - Makes backlog creation easier and more consistent.
  - Reduces overfitting to detailed prose when code and behavior still need review.
- **limitations:**
  - It is not an executable spec and cannot replace implementation judgment.
  - It can become stale or harmful if left discoverable as current truth after implementation.
  - Its value depends on the quality of the prior alignment conversation.

## 5. Human/AFK Task Routing Gate

- **name:** Human/AFK Task Routing Gate
- **problem_solved:** Treating every task as autonomous implementation delegates judgment-heavy decisions to agents.
- **inputs:**
  - Backlog items, blockers, dependencies, and acceptance criteria.
  - Ambiguity level, module boundaries, and available feedback loops.
  - Human judgment points for planning, architecture, QA, and final review.
- **outputs:**
  - AFK-ready tasks.
  - Human-in-loop tasks.
  - Escalations, blockers, and clarification requests.
- **benefits:**
  - Keeps bounded execution autonomous while preserving human taste and accountability at the boundaries.
  - Prevents agents from continuing through unresolved product or architecture calls.
  - Makes queue ownership explicit.
- **limitations:**
  - Requires active backlog curation.
  - Misclassification can send ambiguous work into unsafe automation.
  - Human availability becomes a throughput constraint for judgment-heavy work.

## 6. Vertical-Slice Issue Generation

- **name:** Vertical-Slice Issue Generation
- **problem_solved:** Horizontal layer-by-layer implementation delays integration feedback and makes AFK progress look larger than it is.
- **inputs:**
  - PRD goals, user paths, behavior boundaries, and acceptance checks.
  - Relevant database, API, UI, testing, and documentation surfaces.
  - Dependency and blocker relationships.
- **outputs:**
  - Small issues that cut through layers to observable behavior.
  - A blocker-aware issue graph.
  - Testable and reviewable slices for one agent session.
- **benefits:**
  - Produces integration feedback early.
  - Makes independent work safer for parallel agents.
  - Gives reviewers a real behavior path instead of disconnected layer changes.
- **limitations:**
  - Requires careful issue design and dependency mapping.
  - Some infrastructure or architecture work does not split cleanly into user-visible slices.
  - Slices that are too small can create coordination overhead and fragmented intent.

## 7. Agent Kanban

- **name:** Agent Kanban
- **problem_solved:** Sequential plans waste parallel agent capacity and hide which work is actually independent.
- **inputs:**
  - Vertical-slice issues, AFK/human labels, blockers, status, and ownership metadata.
  - QA findings and newly discovered work.
  - Agent capacity and isolation boundaries.
- **outputs:**
  - A ready queue for autonomous agents.
  - Visible blocked, active, review, and done states.
  - New issues created from QA or implementation discoveries.
- **benefits:**
  - Turns decomposition into a concurrency-control layer.
  - Allows multiple agents to pull safe work without central micromanagement.
  - Keeps the workflow dynamic as QA and review uncover more tasks.
- **limitations:**
  - Board metadata can rot without active maintenance.
  - Bad slices become parallel chaos faster than in a linear plan.
  - Requires agreement on status, blockers, and ownership semantics.

## 8. Ralph/AFK Implementation Loop

- **name:** Ralph/AFK Implementation Loop
- **problem_solved:** Agents need a repeatable operating loop after planning has produced bounded work.
- **inputs:**
  - Ready AFK issue, repository context, scoped brief, and known dependencies.
  - Tests, type checks, linters, runtime checks, and status reporting surface.
  - Policy for continuing to the next issue or stopping for review.
- **outputs:**
  - Reviewable code changes.
  - Test and validation results.
  - Updated task status and optional next-task selection.
- **benefits:**
  - Converts a prepared backlog into repeated implementation attempts with feedback.
  - Gives agents a predictable red-green-verify cadence.
  - Supports unattended progress when issue boundaries and checks are strong.
- **limitations:**
  - Useful only after planning has produced clear, bounded tasks.
  - Weak feedback loops let plausible but broken code accumulate.
  - Long unattended runs can compound mistakes if review cadence is too loose.

## 9. Feedback-Loop-Gated Implementation

- **name:** Feedback-Loop-Gated Implementation
- **problem_solved:** Without executable feedback, agents optimize for plausible code rather than working behavior.
- **inputs:**
  - Acceptance criteria and expected behavior.
  - Failing tests, TDD checkpoints, types, linters, runtime checks, and manual QA criteria.
  - Tool outputs and observed failures from each implementation attempt.
- **outputs:**
  - Pass/fail evidence for the change.
  - Regression tests or updated checks where appropriate.
  - Implementation corrections driven by observed feedback.
- **benefits:**
  - Steers the agent with evidence instead of vibes.
  - Narrows the search space during implementation.
  - Raises confidence that AFK work is correct before human review.
- **limitations:**
  - Feedback quality is the ceiling; weak checks still produce weak assurance.
  - Building or running checks can be costly for small tasks.
  - Manual QA remains necessary for taste, integration, and product judgment.

## 10. Fresh-Context Review

- **name:** Fresh-Context Review
- **problem_solved:** Implementers often review after spending a large context budget and inheriting their own assumptions.
- **inputs:**
  - Diff, changed files, standards, acceptance criteria, and verification commands.
  - A new reviewer context or cleared session.
  - Evidence produced by the implementation loop.
- **outputs:**
  - Independent review findings.
  - Pass/fail or follow-up decisions.
  - Additional issues when QA or review finds new work.
- **benefits:**
  - Separates builder context from evaluator context.
  - Reduces confirmation bias from the implementation conversation.
  - Preserves reasoning quality for review.
- **limitations:**
  - Adds orchestration, model, and token cost.
  - Reviewers can miss intent when upstream artifacts are thin.
  - Requires reproducible checks and readable diffs to be effective.

## 11. Sandboxed Parallel Agents

- **name:** Sandboxed Parallel Agents
- **problem_solved:** Parallel agents interfere when they share a working tree, branch, or runtime environment.
- **inputs:**
  - Independent issues, branches, worktree roots, containers, and runtime configuration.
  - Review, merge, conflict-resolution, and validation policies.
  - Agent assignment and status metadata.
- **outputs:**
  - Isolated implementation branches.
  - Separately reviewable agent outputs.
  - Integrated accepted changes with rerun checks.
- **benefits:**
  - Maps Kanban parallelism onto safe filesystem and git isolation.
  - Contains conflicts and bad experiments to one branch or environment.
  - Enables real parallel throughput when decomposition is good.
- **limitations:**
  - Requires worktree, container, and merge infrastructure.
  - Integration conflicts still need human or dedicated merge handling.
  - Isolation overhead is not worth it for tiny or strongly coupled tasks.

## 12. Sub-Agent Exploration Compression

- **name:** Sub-Agent Exploration Compression
- **problem_solved:** Repository exploration can consume enough tokens to degrade the primary implementation context before coding starts.
- **inputs:**
  - Specific exploration questions.
  - Repository files, history, tests, and conventions.
  - A sub-agent context with permission to spend a larger discovery budget.
- **outputs:**
  - Condensed findings for the main agent.
  - Relevant files, risks, and uncertainty notes.
  - A smaller main-context payload for implementation.
- **benefits:**
  - Keeps discovery costs out of the primary working context.
  - Parallelizes expensive codebase reading.
  - Lets the main agent start implementation with a compressed map.
- **limitations:**
  - Summaries can omit details that matter.
  - The main agent must verify findings against actual files before editing.
  - More agents increase orchestration and review overhead.

## 13. Architecture-as-Agent-Affordance Refactoring

- **name:** Architecture-as-Agent-Affordance Refactoring
- **problem_solved:** Shallow, coupled module structures make agents navigate poorly and amplify code sprawl.
- **inputs:**
  - Dependency clusters, coupled behavior, public interfaces, and existing tests.
  - Desired deep module boundaries and behavior-level test targets.
  - Architecture-improvement skill or review process.
- **outputs:**
  - Proposed or implemented deeper modules.
  - Simpler public interfaces.
  - Boundary-focused tests and architecture follow-up issues.
- **benefits:**
  - Reduces agent cognitive load in future sessions.
  - Makes tests more meaningful by targeting behavior boundaries.
  - Lets humans own interfaces while agents can fill internals.
- **limitations:**
  - Requires real architecture judgment, not formatting cleanup.
  - Can be expensive and risky without strong tests.
  - Should not be mixed into unrelated feature work unless the coupling blocks the task.

## 14. Phase-Scoped Documentation Hygiene

- **name:** Phase-Scoped Documentation Hygiene
- **problem_solved:** Stale PRDs and plans poison future agent retrieval when they remain discoverable as current truth.
- **inputs:**
  - PRDs, plans, issues, implementation status, and documentation precedence rules.
  - Current source-of-truth documents and archived historical context.
  - Signals that a document's phase is complete or obsolete.
- **outputs:**
  - Closed, archived, removed, or clearly status-labeled planning documents.
  - Reduced active-context surface for future agents.
  - Historical context preserved with explicit freshness status.
- **benefits:**
  - Prevents agents from implementing against obsolete intent.
  - Treats documentation as operational state rather than harmless clutter.
  - Keeps retrieval focused on current sources of truth.
- **limitations:**
  - Requires lifecycle discipline after implementation.
  - Can remove convenient local context unless history is preserved elsewhere.
  - Documentation governance overhead rises with the number of artifacts.

## 15. QA-to-Backlog Feedback Loop

- **name:** QA-to-Backlog Feedback Loop
- **problem_solved:** QA findings are often treated as terminal pass/fail events instead of inputs for the next bounded agent tasks.
- **inputs:**
  - Human QA observations, reviewer findings, failed checks, and runtime behavior gaps.
  - Existing Kanban board, severity, blockers, and acceptance criteria.
  - Regression-case or follow-up issue templates.
- **outputs:**
  - New backlog issues or vertical slices.
  - Updated blockers and task priorities.
  - Regression checks for defects that should not recur.
- **benefits:**
  - Turns review and QA into a closed improvement loop.
  - Keeps agent work adaptive as real behavior is observed.
  - Prevents discovered defects from remaining as informal memory.
- **limitations:**
  - Can expand scope if findings are not triaged.
  - Low-quality QA creates noisy or duplicate backlog items.
  - Requires human judgment to distinguish defects from new feature ideas.
