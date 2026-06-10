---
title: "Padroes Reutilizaveis: Agent Focus Problems"
type: analysis
date: 2026-06-10
aliases: ["padroes foco agente", "agent focus patterns", "catalogo problemas atencao", "context amnesia patterns"]
tags: ["agentes-orquestracao", "context-engineering"]
relates-to: ["[[docs/analysis/2026-06-10-agent-focus-problems/analysis|Agent Focus Analysis]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Plot]]"]
---

# Reusable Patterns: Agent Focus Problems

**Source:** `docs/analysis/2026-06-10-agent-focus-problems/analysis.md`
**Date:** 2026-06-10

---

## Pattern 1: External State Persistence

- **Name:** External State Persistence
- **Problem solved:** Context Amnesia — agents forget critical information (allergies, preferences, constraints) when conversations exceed the effective context window
- **Inputs:** Client/session identifier, critical data extracted from conversation (preferences, restrictions, commitments), interaction history
- **Outputs:** State persisted in external storage (JSON file, database, cache) loaded every turn
- **Benefits:** Critical information survives any conversation length; independent of model's context window; enables cross-session conversation resumption; decouples "agent memory" from "model memory"
- **Limitations:** Requires extraction logic (what to persist vs. what is ephemeral); stale data needs invalidation mechanism; adds I/O latency per turn; schema must evolve without breaking existing conversations

## Pattern 2: Plan-Execute-Verify

- **Name:** Plan-Execute-Verify (Separation of Concerns)
- **Problem solved:** Planning-Execution Collapse — agents confuse themselves when trying to plan, execute, and verify in a single pass
- **Inputs:** Complex task with interdependent steps, business constraints, current system state
- **Outputs:** Phase 1 (Plan): explicit atomic steps with per-step success criteria; Phase 2 (Execute): each step isolated with checkpoint verification; Phase 3 (Verify): validation that all steps produced expected results
- **Benefits:** Clean context per phase (no cross-contamination); failures are localizable to exact step; enables granular retry; quality remains flat with task complexity
- **Limitations:** Adds latency (3 phases = potentially 3 model calls); overhead for simple tasks; requires external orchestrator for phase transitions; plan may become stale if world changes between planning and execution

## Pattern 3: Generator-Evaluator

- **Name:** Generator-Evaluator (Two-Agent Review)
- **Problem solved:** Self-Evaluation Collapse — agents cannot critically evaluate their own output due to confirmation bias. Also indirectly solves Context Amnesia (via state persistence) and Planning Collapse (via separation of responsibilities)
- **Inputs:** Generator: user request, conversation context, persisted client data; Evaluator: raw generator output, client constraints (from state persistence), quality rubrics, business rules
- **Outputs:** Generator: candidate response; Evaluator: binary verdict (approve/reject) + specific feedback on rejection; Loop: rejected outputs return to Generator with feedback
- **Benefits:** Impartial evaluator (did not generate the response); catches 10-12% more errors than self-evaluation; Generator can be creative, Evaluator ensures safety; allows different models (fast/creative Generator, slow/rigorous Evaluator)
- **Limitations:** Minimum 2 LLM calls per turn; additional evaluation latency; Evaluator can also err (false positives/negatives); requires explicit quality rubrics; shared model blind spots if same base model

## Pattern 4: Constraint-Anchored Evaluation

- **Name:** Constraint-Anchored Evaluation
- **Problem solved:** Vague evaluations ("is this good?") miss real errors. Evaluators need concrete, verifiable constraints to be effective
- **Inputs:** Constraint list from state persistence (e.g., `allergies: [gluten]`, `budget_max: 150`, `preference: vegan`), Generator output, business rules (e.g., "never recommend a product the client returned")
- **Outputs:** Verification matrix: each constraint checked against output with binary result (pass/fail); aggregate verdict: approved only if ALL constraints pass; on failure: precise identification of which constraint was violated
- **Benefits:** Transforms subjective evaluation into objective verification; actionable feedback (Generator knows exactly what to fix); reduces Evaluator false positives; auditable (every decision traceable to a constraint)
- **Limitations:** Only catches explicitly modeled constraints; implicit/common-sense constraints missed; requires maintenance as business rules evolve; can be overly rigid (technical constraint violation may be contextually acceptable)
