---
title: "Full Walkthrough: Workflow for AI Coding - Matt Pocock Analysis"
type: analysis
tags: [ai, agents, coding-workflow, harness-engineering, context-management, software-architecture]
date: 2026-06-07
aliases: ["matt pocock workflow analysis", "ai coding workflow walkthrough", "full walkthrough analysis", "matt pocock ai coding talk"]
relates-to: ["[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]]", "[[docs/canonical/vertical-slice-issue-generation|Vertical-Slice Issue Generation]]", "[[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/summary-buffer-continuity|Summary Buffer Continuity]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Progressive Disclosure]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis|Context Management Analysis]]"]
---

# Full Walkthrough: Workflow for AI Coding - Matt Pocock Analysis

Source: Matt Pocock talk "Full Walkthrough: Workflow for AI Coding" (AI Engineer World's Fair, 2025). This analysis extracts workflow knowledge, design models, architectural patterns, operating lessons, tradeoffs, and failure modes. It ignores workshop banter, marketing, tool preference anecdotes, and generic "AI changes everything" claims.

## Frameworks & Models

### Software engineering fundamentals as the AI coding substrate

The talk's deepest model is that AI coding does not replace software engineering discipline; it increases the payoff of old disciplines. [[concepts/vertical-slices]], [[concepts/deep-modules]], TDD, code review, issue decomposition, and feedback loops become control surfaces for agents. The model treats agents as faster implementers inside the same engineering system, not as a new system that can bypass architecture and verification.

Non-obvious implication: the scarce resource is no longer keystrokes. The scarce resources are task framing, module boundaries, feedback quality, and review attention. AI makes poor architecture and weak tests more expensive because it can generate bad code faster.

### Smart zone / dumb zone

[[concepts/smart-zone-dumb-zone]] is a context-quality model, not just a token-count warning. The working assumption is that useful reasoning degrades well before the nominal context window is full, around the practical smart-zone ceiling discussed in the source. The workflow therefore optimizes for predictable reasoning quality rather than maximum context retention.

Operational shape:

- Keep system prompts and always-loaded instructions small.
- Size implementation tasks so one agent session can finish inside the smart zone.
- Use sub-agents for expensive exploration so the main working context receives only summaries.
- Prefer clearing context to repeated compaction when predictability matters.
- Use fresh contexts for review so the reviewer is not operating after the implementation context has degraded.

### Shared design concept before plans

The [[concepts/grill-me-skill]] is a planning model where the goal is not a perfect plan artifact. The goal is a [[concepts/shared-design-concept]] between human and agent. The agent interviews the human aggressively, one question at a time, to expose hidden constraints, unresolved product calls, architectural assumptions, and domain unknowns.

The resulting conversation is the real planning asset. The PRD is downstream summarization, not the source of truth by itself. This reverses a common spec-driven instinct: the workflow trusts the PRD because alignment happened before it, not because the PRD is detailed enough to remove judgment.

### PRD as destination, not executable spec

[[concepts/prd-as-destination]] frames the PRD as a navigational artifact. It says where the system is going and what matters, but it is not treated as a literal code-generation contract. It is useful enough to generate issues, define scope, and keep agents oriented. It is not a permanent repository bible.

The important boundary is temporal: a PRD is valuable during planning and issue generation, but can become [[concepts/doc-rot]] after implementation if it remains in the repo as apparently-current context.

### Human-in-loop versus AFK classification

[[concepts/human-in-loop-vs-afk]] is the task-routing model. Planning, ambiguity resolution, architectural judgment, prototype interpretation, QA, and final review require human presence. Bounded implementation issues can run AFK only after they have clear scope, dependencies, feedback loops, and module boundaries.

The model is not "automate everything." It is "move implementation into bounded queues while keeping judgment at the boundaries."

### Architecture as agent affordance

[[concepts/deep-modules]] are presented as both human architecture and agent architecture. Deep modules give agents larger behavioral surfaces with simple public interfaces. They reduce navigation burden, make tests more meaningful, and let humans own the interface while agents fill internals.

This reframes architecture as an input to agent performance. A shallow, highly coupled codebase is not just ugly; it is hostile terrain for an agent.

## Patterns & Architectures

### Grill-me skill

Problem: initial prompts hide assumptions and produce premature plans.

Pattern: clear the context, invoke a short skill that forces the agent to interview the human relentlessly, answer one question at a time, and continue until unresolved branches of the decision tree are closed or explicitly deferred. The agent should offer recommended answers, so the human edits judgment rather than inventing every answer from scratch.

Architecture role: creates shared design context before any PRD, plan, or issue backlog exists.

### Destination PRD

Problem: detailed plans can become brittle pseudo-specifications and still miss the real design intent.

Pattern: summarize the grilling conversation into a PRD containing problem, solution, user stories, implementation decisions, testing expectations, and out-of-scope boundaries. Use it to generate work and keep direction, not to avoid reading or reviewing code.

Architecture role: bridges high-level intent to issue decomposition.

### Vertical-slice issue generation

Problem: agents tend to implement horizontally, such as all database changes, then all API changes, then all UI changes, which delays integration feedback.

Pattern: generate issues as [[concepts/vertical-slices]] that cross layers and produce observable behavior. Each issue should be small enough for one AFK session but complete enough to test a real path. Represent dependencies as blockers rather than as a single linear phase list.

Architecture role: turns planning into an integration-feedback graph.

### Agent Kanban

Problem: sequential plans waste parallel agent capacity and hide which tasks are actually independent.

Pattern: maintain a board of independently grabbable issues with AFK/human classification and blocking relationships. Agents pick ready AFK work; humans handle blocked, ambiguous, or judgment-heavy work. QA creates more issues instead of ending the workflow.

Architecture role: the board is a concurrency control layer for agent work.

### Ralph loop / AFK implementation loop

Problem: an agent needs a repeatable operating loop after work has been decomposed.

Pattern: an implementation loop loads ready issues, explores enough repo context, chooses a task, writes failing tests when applicable, implements, runs tests/types/linters, records status, and stops or takes the next ready issue. The loop is useful only after planning has produced bounded tasks.

Architecture role: converts a backlog into repeated implementation attempts with feedback.

### Fresh-context review

Problem: the implementer often reaches review after spending a large context budget and inheriting its own assumptions.

Pattern: review in a separate context, or clear context before review. The review pass reads the diff and standards fresh, runs checks, and evaluates behavior without the sediment of the implementation conversation.

Architecture role: separates builder context from evaluator context.

### Sandboxed parallel agents

Problem: parallel agents interfere when they share a working tree, branch, or runtime environment.

Pattern: run each issue in an isolated worktree and container, review each branch separately, then hand accepted branches to a merge/integration step that resolves conflicts and reruns checks.

Architecture role: maps Kanban parallelism onto safe filesystem and git isolation.

### Sub-agent exploration

Problem: repository exploration is token-expensive and can push the primary agent into degraded context before implementation starts.

Pattern: delegate exploration to isolated sub-agents that can spend large token budgets and return condensed findings. The main agent consumes summaries, not raw exploration traces.

Architecture role: keeps discovery costs out of the primary working context.

### Improve-codebase-architecture skill

Problem: agents inherit and amplify shallow module structures.

Pattern: use a skill to inspect dependency clusters, identify coupled behavior, propose deeper module boundaries, and define tests around those boundaries. This is architecture work, not formatting cleanup.

Architecture role: makes the codebase more navigable and testable for future agent sessions.

## Operational Lessons

- AI coding quality is bounded by feedback-loop quality. Tests, types, linters, runtime checks, and manual QA are the ceiling, not optional polish.
- TDD functions as steering for agents. Red-green-refactor gives the model immediate evidence and narrows its search space.
- Token visibility is operational telemetry. Without knowing session size, the human cannot know when to clear context, delegate exploration, or stop reviewing.
- Planning remains human-in-loop because it encodes taste, domain judgment, scope, and tradeoffs. AFK is appropriate only after those are converted into bounded tasks.
- PRD review has diminishing returns after a strong grilling session. The high-value review target becomes issue decomposition and implementation behavior, not the prose artifact alone.
- QA creates more work rather than closing the loop permanently. A healthy agent workflow treats QA findings as backlog inputs.
- Doc hygiene matters more for agents than for humans. Stale docs are not harmless clutter; they become misleading retrieval targets.
- Owning the workflow matters. Opaque planning tools reduce the team's ability to see why the agent failed and where to change the process.
- Parallel agents amplify backlog quality. Good vertical slices become throughput; bad decomposition becomes parallel chaos.
- Architecture improvement is part of the AI workflow. Deep modules reduce agent cognitive load and increase the usefulness of tests.

## Tradeoffs

| Decision | Benefit | Cost |
|---|---|---|
| Clear context instead of compacting | Predictable reset into a known smart-zone state | Loses conversational continuity and requires durable artifacts |
| Grill before planning | Exposes hidden assumptions and creates alignment | Consumes substantial human time and can feel excessive |
| PRD as destination, not spec | Avoids brittle spec-to-code thinking | Requires humans to keep reviewing code and behavior |
| Vertical slices over horizontal layers | Produces integration feedback early | Requires careful issue design and dependency mapping |
| Kanban over linear plan | Enables parallelism and dynamic backlog growth | Requires blocker metadata and active curation |
| Human QA at boundaries | Preserves taste, intent, and product judgment | Moves human labor from implementation to review and QA |
| Deep modules over shallow modules | Improves navigability and behavioral testability | Requires deliberate architecture work before or during implementation |
| Close/remove stale PRDs | Reduces doc-rot poisoning | Loses convenient local historical context unless tracked elsewhere |
| Fresh-context review | Improves reviewer reasoning and independence | Adds orchestration and model/token cost |
| Sandboxed worktrees | Enables safe parallel implementation | Adds Docker/worktree/merge infrastructure |
| Sub-agent exploration | Preserves main-context quality | Requires trusting and verifying summaries |

## Failure Patterns

### Premature planning

Cause: the agent writes a plan before interrogating assumptions.

Failure mode: hidden decisions surface during implementation as rework, incoherent architecture, or wrong scope.

Counterpattern: grill first, then summarize.

### Spec-to-code drift

Cause: humans treat the PRD as the only control surface and stop engaging with code.

Failure mode: the prose artifact looks aligned while the actual system drifts in architecture, behavior, or tests.

Counterpattern: use the PRD to generate issues, then review modules, tests, runtime behavior, and QA findings.

### Dumb-zone continuation

Cause: long sessions, repeated compaction, large prompts, or raw exploration traces fill the context.

Failure mode: the agent makes worse decisions, forgets constraints, or reviews its own work with degraded reasoning.

Counterpattern: size tasks, clear context, use sub-agents, and review fresh.

### Horizontal implementation

Cause: the agent decomposes by layer instead of by end-to-end behavior.

Failure mode: integration feedback arrives late, cross-layer defects accumulate, and AFK progress looks larger than it is.

Counterpattern: generate vertical-slice issues with observable outputs.

### Shallow-module sprawl

Cause: agents create many tiny files/functions without a human-owned module design.

Failure mode: dependency graphs become hard to navigate and tests verify fragments rather than behavior.

Counterpattern: design deep modules with simple interfaces and test at meaningful boundaries.

### Blind coding

Cause: insufficient tests, types, linters, runtime checks, or manual verification.

Failure mode: the agent has no reliable signal and optimizes for plausible code instead of working behavior.

Counterpattern: make feedback loops mandatory in every AFK issue.

### Rotten-document poisoning

Cause: completed PRDs and stale plans remain discoverable as if current.

Failure mode: future agents retrieve old intent and implement against obsolete context.

Counterpattern: close issues, remove stale docs from active context, and preserve history only with clear status.

### Parallel chaos

Cause: multiple agents work from poorly sliced issues or shared branches.

Failure mode: conflicts, duplicated work, incompatible assumptions, and difficult integration.

Counterpattern: require blocker-aware Kanban, isolated worktrees, and a merge/review step.

### Taste collapse from over-automation

Cause: planning, research interpretation, QA, and final judgment are delegated as if they were implementation.

Failure mode: outputs may pass mechanical checks while missing product intent or design quality.

Counterpattern: keep humans in judgment-heavy loops and reserve AFK for bounded execution.

## Synthesis

> [!inference]
> The talk describes an agentic coding control system, not a prompting recipe. The control system has six main levers: alignment interviews reduce ambiguity, PRDs preserve direction, vertical-slice Kanban exposes safe work, feedback loops steer implementation, context resets preserve reasoning quality, and human QA injects taste and judgment back into the queue.

> [!inference]
> The workflow's most important architectural claim is that agents make codebase structure more important, not less. Deep modules, clear interfaces, and executable feedback loops are how humans project intent into many future AFK sessions.

> [!inference]
> Documentation is phase-scoped operational state. The same PRD can be highly valuable before implementation and dangerous afterward if it remains retrievable as current truth.

> [!inference]
> Parallelization is a second-order capability. The first-order capability is decomposition into independently verifiable vertical slices; only then do Sandcastle-style worktrees and multiple agents become useful.

> [!inference]
> Human work shifts from typing code to designing constraints, queues, interfaces, and verification. The role is closer to systems operator and architect than prompt writer.
