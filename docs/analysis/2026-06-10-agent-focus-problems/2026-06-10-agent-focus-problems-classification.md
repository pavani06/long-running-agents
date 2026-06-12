---
title: "Classificacao: Agent Focus Problems vs Repositorio"
type: analysis
date: 2026-06-10
aliases: ["classificacao foco agente", "gap agent focus", "cobertura problemas atencao"]
tags: ["agentes-orquestracao", "context-engineering"]
relates-to: ["[[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-analysis|Agent Focus Analysis]]", "[[docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns|Agent Focus Patterns]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]"]
---

# Classification: Agent Focus Problems Patterns vs. Repository

**Source:** `docs/analysis/2026-06-10-agent-focus-problems/2026-06-10-agent-focus-problems-patterns.md`
**Date:** 2026-06-10

---

## Pattern 1: External State Persistence

**Classification:** Partial Coverage
**Integration Value:** High

### Evidence

**What exists (6 canonical docs cover pieces):**
- `addressable-memory-catalog.md` — catalog of omitted memory with `id`, `location`, `preview`, `fetch`
- `head-tail-context-truncation.md` — preserves head+tail, stores omitted middle externally with retrieval handles
- `serializable-pause-resume-state.md` — full state serialization for pause/resume
- `stable-harness-prompt.md` — separation of stable instructions from reducible payload
- `epistemic-memory-graph.md` — epistemic labels, provenance, validity scope
- `closed-loop-agent-operating-system.md` — state writeback in operational loop

**What is missing:**
1. No unified canonical doc that connects catalog, exact recovery, pause/resume, and writeback as a cohesive "external memory" strategy
2. No explicit naming of the pattern as "External State Persistence"
3. No tradeoff analysis across the 6 component pieces as a unified strategy

### Justification
The repo has all the mechanical pieces for external state persistence, distributed across 6 canonical docs. Each doc solves a sub-problem (cataloging, truncation, serialization, harness stability, epistemic labeling, loop integration). What is missing is the umbrella pattern that names and unifies these pieces as a deliberate architectural choice: "external state persistence" as a strategy, not an accident of having those 6 docs.

---

## Pattern 2: Plan-Execute-Verify

**Classification:** Partial Coverage
**Integration Value:** High

### Evidence

**What exists (7 canonical docs cover pieces):**
- `owned-agent-control-loop.md` — decomposes loop into Prompt → Context Builder → Switch → Loop with intervention points
- `deterministic-tool-dispatch.md` — deterministic dispatch via switch statement, testable and auditable
- `closed-loop-agent-operating-system.md` — state intake → priority synthesis → execution routing → feedback writeback
- `serializable-pause-resume-state.md` — checkpoints between phases
- `resolver-based-context-progressive-disclosure.md` — load-on-demand with trigger evals
- `stable-harness-prompt.md` — stable operating contract between phases
- `split-brain-planning-review.md` — independent rubric review before execution

**What is missing:**
1. No canonical doc that explicitly names the three-phase loop (Plan → Execute → Verify) with documented intervention points
2. `owned-agent-control-loop.md` is the closest but uses different terminology and doesn't frame it as plan-execute-verify
3. No explicit contract for what constitutes a valid "plan" vs. "execution" vs. "verification" phase

### Justification
The repo has extensive coverage of controlled execution loops, deterministic dispatch, and split-brain review. These are pieces of plan-execute-verify but not named or unified as such. The curriculum teaches this pattern explicitly (in 01-why-agents-lose-plot.md) but no canonical doc formalizes it.

---

## Pattern 3: Generator-Evaluator

**Classification:** Partial Coverage
**Integration Value:** High

### Evidence

**What exists (12+ canonical docs cover evaluation infrastructure):**
- `multi-model-evaluation-council.md` — model diversity as independent evaluators
- `eval-tier-stratification.md` — fast/medium/deep eval tiers
- `pr-gated-eval-enforcement.md` — eval enforcement on PR merge
- `repeatable-agent-spot-check-set.md` — named seed set with fixtures and baselines
- `production-grounded-eval-sampling.md` — production-anchored eval sampling
- `production-failure-regression-flywheel.md` — production incidents as regression cases
- `n-plus-one-long-session-evals.md` — N+1 follow-up grading after truncation
- `late-failure-regression-suite.md` — late-session failure regression
- `eval-to-production-correlation-tracking.md` — eval-to-production correlation
- `pain-signal-eval-progression-gate.md` — pain-signal-driven eval progression
- `domain-embedded-workflow-automation-wedge.md` — eval-gated workflow automation
- `skill-resolver-skillify-capability-pipeline.md` — eval-gated capability promotion

**What is missing:**
1. No single canonical doc that anchors the Generator-Evaluator pattern as the unified architecture
2. The existing eval docs focus on evaluation mechanics and infrastructure, not the generator↔evaluator loop with feedback
3. No explicit framing of the two-agent architecture (Generator + Evaluator) as a deliberate architectural pattern

### Justification
The repo has arguably the most mature evaluation infrastructure among its canonical docs. But these docs focus on "how to evaluate" (tiers, sampling, regression, gates), not "the Generator-Evaluator pattern as an architectural decision." The curriculum teaches this pattern as the unified solution to all three problems, but no canonical doc formalizes it.

---

## Pattern 4: Constraint-Anchored Evaluation

**Classification:** Partial Coverage
**Integration Value:** High

### Evidence

**What exists (same eval docs as Generator-Evaluator cover constraint mechanics):**
- `repeatable-agent-spot-check-set.md` — expected outcomes with tool constraints and baselines
- `pr-gated-eval-enforcement.md` — threshold-based enforcement
- `eval-tier-stratification.md` — tier-specific thresholds
- `split-brain-planning-review.md` — independent rubrics with reconciliation rules
- `skill-resolver-skillify-capability-pipeline.md` — compliance tests and trigger evals

**What is missing:**
1. No canonical doc that places constraints, thresholds, negatives, and acceptance criteria as the spine of evaluation
2. Existing docs mention thresholds and criteria but not as "constraint anchoring" — the idea that evaluation is objective because it is anchored to explicit, verifiable constraints
3. No explicit mapping from state persistence constraints to evaluation criteria

### Justification
The evaluation infrastructure implicitly uses constraint-based checking (thresholds, expected outcomes, baselines, compliance tests). But "Constraint-Anchored Evaluation" as a named pattern — the idea that evaluation quality depends on having explicit, objective, verifiable constraints rather than subjective judgment — is not formalized in any single canonical doc.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | External State Persistence | Partial Coverage | High |
| 2 | Plan-Execute-Verify | Partial Coverage | High |
| 3 | Generator-Evaluator | Partial Coverage | High |
| 4 | Constraint-Anchored Evaluation | Partial Coverage | High |

**All patterns classified as Partial Coverage with High integration value — all 4 are candidates for canonical doc creation (P1 priority).**
