---
title: "Plan-Execute-Verify"
type: canonical
aliases: ["planejar executar verificar", "separation of concerns", "separação de concerns", "planning execution separation"]
tags: ["agentes-orquestracao", "12-factor-agents"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]"]
sources: ["[[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]"]
---

# Plan-Execute-Verify

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md]]
**Classification:** Partial Coverage — 7 canonical docs cover component pieces, no unified three-phase doc
**Precedence:** Level 2 ([[docs/system-of-record|docs/system-of-record.md]])

---

## Problem

Planning-Execution Collapse happens when an agent tries to plan, execute, and verify inside the same pass. The source lesson describes this as doing everything in one context window and one call, like driving while reading a map, checking GPS, and deciding at the same time ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:115-122). The analysis extracts the same structural failure: quality collapses under task complexity because there is no explicit plan, no checkpoints, and planning information mixes with execution information ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]:16-17).

In the KODA order-processing scenario, KODA receives a 5-product order and tries to verify catalog existence, confirm stock in Sao Paulo, calculate shipping, apply a 20% coupon, process payment, and confirm same-day delivery in one run ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:123-140). While doing that, it loses track of the client's address, whether the client asked for a guarantee, and whether the promotion applies to the product ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:137-139). The result is confusion, errors, and retries ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:142-142).

The structural issue is not that KODA needs a better prompt. The lesson names five failure modes of a single pass: no explicit plan, no per-step checkpoint, chaotic context where planning and execution information mix, difficult debugging because the failure location is unknown, and no space to adjust once the plan is discovered to be wrong ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:144-152). In order processing, each validation can fail differently and one failure causes reprocessing and customer frustration ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:185-191).

## Solution

Decompose complex work into three distinct phases: Plan, Execute, Verify. The source curriculum states the solution as separation of concerns: planning asks what needs to be done, execution does each thing carefully, and verification checks whether everything worked ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:398-405). The extracted pattern makes the phase outputs explicit: Plan produces atomic steps with per-step success criteria, Execute isolates each step with checkpoint verification, and Verify validates that all steps produced the expected results ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:17-24).

```
Complex Task
     |
     v
+------------------------------+
| PLAN                         |
| atomic steps + success gates |
+------------------------------+
     |
     | plan accepted
     v
+------------------------------+
| EXECUTE                      |
| one step at a time           |
| checkpoint after each step   |
+------------------------------+
     |              ^
     | step failed  |
     +--------------+
     |
     | all steps complete
     v
+------------------------------+
| VERIFY                       |
| compare results to gates     |
+------------------------------+
     |              ^
     | verification |
     | fails        |
     +--------------+
     |
     v
Approved Outcome
```

| Phase | Produces | Needs in Context | Gate Before Proceeding |
|---|---|---|---|
| Plan | Ordered atomic steps and per-step success criteria | User goal, constraints, current system state | Every step has an observable success criterion and a clear dependency boundary |
| Execute | Step results and checkpoints | Current step, required inputs, relevant tools, prior checkpoint state | Step result matches its success criterion before the next step starts |
| Verify | Final verdict, failures, and retry target | Plan, all checkpoints, business constraints, expected outputs | All planned success criteria pass or the failed step is returned for re-execution |

The purpose is context separation. In a single-pass flow, planning tokens, tool results, partial decisions, retries, and verification notes all compete inside the same reasoning pass. In Plan-Execute-Verify, each phase receives only the context it needs and emits a bounded artifact for the next phase. The pattern extraction names the benefits as clean per-phase context, localizable failures, granular retry, and quality that remains flat as task complexity increases ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:21-24). The curriculum makes the same quality claim operationally: agents that separate planning from execution maintain quality on complex tasks, can reflect and adjust plans, and are easier to debug, while agents that mix everything fall quickly with complexity and produce cascading errors ([[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:175-183).

## Implementation in this repo

### What already exists

- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] decomposes an agent loop into Prompt, Context Builder, Switch Statement, and Loop, each with explicit intervention points ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:31-52). Its loop section names break, summarize, LM-as-judge, human approval, and force terminate as intervention points that can host phase gates ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75).
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] makes execution auditable by showing model JSON routed through a deterministic switch statement to handler code and returned context ([[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:39-57). It also frames dispatch as testable, auditable, circuit-breakable, and observable instead of framework magic ([[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:59-67).
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] defines a broader operating loop with state intake, priority synthesis, execution routing, and feedback writeback ([[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:28-37). Its minimum contract requires source precedence, readable state, ownership, validation before writeback, and durable memory updates ([[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:39-45).
- [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]] supplies the checkpoint substrate for phase boundaries by serializing context, execution state, and business state to persistent storage and resuming later from that state ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-57).
- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] keeps phase context narrow by loading task-specific instructions only when a resolver trigger matches, rather than putting every workflow into the base prompt ([[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]:20-40).
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] preserves the operating contract between phases by separating the stable harness prompt from reducible context payload and treating prompt changes as deliberate, versioned, and evaluated separately from compaction ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41).
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] covers an upstream planning-quality gate by separating engineering review from product or destination review before execution begins ([[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:26-41).

### What is missing

1. No canonical doc explicitly names the three phases Plan -> Execute -> Verify with documented intervention points; the classification lists this as the first missing item for the pattern ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:49-50).
2. No explicit contract defines what constitutes a valid plan, a valid execution phase, and a valid verification phase; the classification names this as a gap even though the source pattern defines the desired phase outputs ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:51-53; [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:21-24).
3. No formalized checkpoint mechanism is documented as the Plan-Execute-Verify boundary, even though the extracted pattern requires checkpoint verification during execution and the related canonical docs only cover checkpoint pieces separately ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:21-24; [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:40-48).
4. No canonical doc frames this as the direct solution to Planning-Execution Collapse; the classification says the curriculum teaches the pattern explicitly, but no canonical doc formalizes it ([[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:54-55).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Clean per-phase context (no cross-contamination) | Adds latency: 3 phases = potentially 3 model calls |
| Failures localizable to exact step | Overhead unjustified for simple single-step tasks |
| Granular retry (re-execute only the failed step) | Requires external orchestrator for phase transitions |
| Quality preserved under increasing task complexity | Plan may become stale if world changes between planning and execution |
| Explicit checkpoints enable auditing and debugging | Phase separation adds orchestration code complexity |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] for loop structure, [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] for auditable execution, and [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] for a stable contract between phases.
- **Validated by:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] for independent review before execution and [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]] for validating behavior after long-session context pressure.
- **Complements:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] because the Generator can use Plan-Execute-Verify internally, [[docs/canonical/external-state-persistence|External State Persistence]] because checkpoints can write to persisted task and business state, and [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] because the Verify phase checks explicit constraints.

## References

- [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:115-152 — problem description and KODA single-pass order-processing scenario.
- [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]:398-405 — three-phase separation of concerns solution.
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Knowledge Extraction]]:10-18 — three fundamental long-running-agent problems and Planning-Execution Collapse summary.
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]:17-24 — Plan-Execute-Verify pattern definition.
- [[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-classification|Agent Focus Classification]]:33-56 — Partial Coverage classification and missing unified canonical doc.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:31-75 — loop structure and intervention points.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:39-67 — auditable deterministic execution.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:26-41 — independent planning review before execution.

---

*Created: 2026-06-10 | From: Agent Focus Problems pattern classification | Precedence: canonical*
