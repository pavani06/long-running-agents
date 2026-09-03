---
title: "Agentic Patterns from The Prompting Playbook"
type: analysis
tags: ["agentes-orquestracao", "harness-engineering", "evals", "context-engineering", "production"]
date: 2026-09-02
aliases: ["prompting playbook patterns", "padrões prompting playbook", "generate evaluate repair", "eval gated model migration"]
last_updated: 2026-09-02
relates-to: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-analysis|The Prompting Playbook Analysis]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-mental-model|Mental Model: The Prompting Playbook]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/prompt-as-code-causal-change-management|Prompt as Code Causal Change Management]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]"]
sources: ["docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-analysis.md"]
---

# Agentic Patterns from The Prompting Playbook

Extraction mode: **FILE** — the single knowledge input was the analysis document `2026-09-02-the-prompting-playbook-analysis.md`, read in full. Transcription notes, talk context, and non-agentic advice were excluded; only patterns applicable to agentic systems (agent prompts, harnesses, evals, tool use, decomposition) were kept. Cross-cutting theme from the source synthesis: guarantees migrate from the prompt to the harness — format, correctness, and quality move from instruction text into stop sequences, tools, and architecture.

## 1. Eval-Gated Model Migration Diagnostic

- **name:** Eval-Gated Model Migration Diagnostic
- **problem solved:** When a prompt migrates to a new model and performance drops, teams cannot tell a fixable behavior difference from an unfixable capability gap, so they waste effort prompting around a capability deficit.
- **inputs:**
  - Production prompt being migrated to a new model.
  - An eval suite covering the prompt's behavior, run before and after migration.
  - Per-case pass/fail results plus a violation-count metric.
- **outputs:**
  - A per-failure diagnosis: behavior difference (remediable by prompt/harness tuning) vs. capability gap (no amount of prompting fixes it).
  - A regression-test signal for the migration decision.
- **benefits:**
  - Separates the only two possible causes of post-migration failure, each with a distinct remedy.
  - Doubles as a regression suite for every future migration.
  - Violation counts give directional signal (capability improving) even when pass/fail has not moved.
- **limitations:**
  - Requires the eval suite to exist before migration; without it, iteration is vibes.
  - Natural variance between runs can mimic regression; revalidate the specific case before concluding.
  - Only as representative as its case taxonomy (see pattern 2).

## 2. Control/Edge/Boundary Eval Taxonomy

- **name:** Control/Edge/Boundary Eval Taxonomy
- **problem solved:** Ad hoc eval suites do not systematically cover what a production agent must preserve: unambiguous baseline behavior, past failure modes locked by instruction, and the edge of its own competence.
- **inputs:**
  - The agent's task domain and known past failures.
  - Policy, tools, and handoff/refusal criteria.
- **outputs:**
  - A three-class suite: control cases (must always pass, unambiguous), edge cases (past failures locked by instruction so they do not regress), and capability-boundary cases (the agent must know when to hand off to a human or refuse).
- **benefits:**
  - Makes regression meaning class-specific: control regression is breakage; boundary regression is calibration loss.
  - Encodes institutional memory of past failures as permanent tests.
  - Tests the agent's self-knowledge of its limits, not just task skill.
- **limitations:**
  - Requires deliberate curation to map cases onto the three classes.
  - Boundary cases depend on correctly specifying when handoff or refusal is right.
  - Each new production failure grows the edge set, so the suite needs maintenance.

## 3. Structural Prompt Hygiene

- **name:** Structural Prompt Hygiene
- **problem solved:** Multi-owner production prompts mix policy, tone, process, data, and defensive patches in undifferentiated text; the model cannot tell them apart, and neither can maintainers.
- **inputs:**
  - A legacy prompt with mixed concerns, redundancy, pasted web copy, and false identity claims.
  - A structural scheme such as XML tags: role, guidelines, policy, tone of voice, data.
- **outputs:**
  - A prompt with logically separated, tagged sections and redundancy removed.
  - A measured eval uplift from hygiene alone, before any targeted failure fix.
- **benefits:**
  - Rule of thumb: if a human reader cannot tell guidelines from policy from data, the model cannot either; separation fixes both at once.
  - Reusable at any stage of prompt maintenance, especially as prompts grow more complex.
  - Cheap: in the source case it produced uplift before any targeted fix.
- **limitations:**
  - Bounded: hygiene does not fix specific failure modes, which need targeted work.
  - Requires an explicit owner to prevent rot from re-accumulating.
  - Post-hygiene evals still show per-case variance that must be revalidated case by case.

## 4. Defensive Patch Ledger

- **name:** Defensive Patch Ledger
- **problem solved:** Prompts accumulate defensive patches written for previous models; newer, more instruction-following models overfit those patches, and nobody knows which patch to remove because the why was never recorded.
- **inputs:**
  - A version-controlled prompt.
  - A rationale recorded for every defensive change (why added, which failure it addressed).
- **outputs:**
  - An auditable history mapping each defensive instruction to the model-era failure that justified it.
  - The ability to backtrack or neutralize patches during model migration.
- **benefits:**
  - Turns patch debt from an invisible liability into a depreciable inventory.
  - Makes model migration trigger a patch audit, not just an eval re-run.
  - Operationalizes the invariant-compensation split: model compensations decay across generations; domain invariants survive.
- **limitations:**
  - Discipline cost: the rationale must be recorded at write time or never.
  - Does not by itself decide which patches are obsolete; audit judgment is still required.
  - Depends on prompt-as-code infrastructure (version control).

## 5. Two-Sided Trade-off Instruction

- **name:** Two-Sided Trade-off Instruction
- **problem solved:** Instructions that state only the cost of an action (for example, escalation costs $8) make the agent over-optize the single stated objective and never escalate, even when escalating is correct.
- **inputs:**
  - The action whose frequency the prompt should control (escalate, refund, hand off).
  - The cost side of the action (money, team metrics).
  - The counter-cost of wrongly avoiding it (refund exposure, customer trust).
  - The behavior the eval suite expects.
- **outputs:**
  - A balanced instruction declaring both sides of the trade-off, letting the model make the judgment per case.
- **benefits:**
  - As models improve at making trade-offs, stating both sides lets them exercise that judgment.
  - Eliminates single-objective overfit such as under-escalation.
  - Resolves prompt-vs-eval conflict when both describe the desired behavior consistently.
- **limitations:**
  - Requires knowing both sides well enough to state them.
  - Converts a hard rule into a judgment; behavior becomes less deterministic.
  - The framing must stay aligned with what the eval defines as correct.

## 6. Capability Escalation Ladder

- **name:** Capability Escalation Ladder
- **problem solved:** When an agent fails a hard task, teams guess which lever to pull (bigger model, more thinking, better prompt, decomposition); ad hoc ordering wastes spend and hides the economic winner.
- **inputs:**
  - A failing task with an eval suite and violation counts.
  - Four escalation rungs: larger model, reasoning budget (adaptive thinking), improved instructions, architectural decomposition.
  - Cost and latency measurements per rung.
- **outputs:**
  - An ordered exploration: capability, then budget, then instruction, then architecture.
  - A cost/quality comparison across the routes that pass; the economic winner is typically the last rung (decomposition).
- **benefits:**
  - Each rung is cheap to test relative to the next, and violation counts give directional signal along the way.
  - Prevents shipping routes that pass evals but fail economics (triple tokens and latency).
  - In the source case the decomposition rung passed everything at the lowest cost.
- **limitations:**
  - Later rungs cost more engineering (three prompts to maintain instead of one).
  - Early rungs can pass evals at unacceptable cost; pass/fail alone does not decide.
  - Meaningless without eval infrastructure to compare rungs.

## 7. Hard/Soft Constraint Grader Split

- **name:** Hard/Soft Constraint Grader Split
- **problem solved:** Grading agent outputs that mix binary rules with fuzzy preferences through a single judge yields either non-deterministic hard-rule grading or ossified soft preferences.
- **inputs:**
  - Task constraints partitioned into hard (binary, countable) and soft (preferences).
  - A deterministic checker function for the hard rules.
  - An LLM evaluator prompt carrying the soft constraints.
  - A trial count (for example, five runs per candidate).
- **outputs:**
  - Violation counts per hard rule per trial, deterministic and cheap.
  - Soft-constraint judgment from the evaluator, adjustable at runtime without backend changes.
- **benefits:**
  - Hard rules graded programmatically instead of by a non-deterministic LLM judge.
  - Soft constraints become runtime-tunable prompt content rather than code deploys.
  - Count-based reporting detects directional improvement even when binary pass/fail does not move.
- **limitations:**
  - Requires a clean partition; ambiguous constraints force a choice of side.
  - The LLM evaluator keeps non-determinism and cost for the soft portion.
  - Multi-trial reporting multiplies eval runtime.

## 8. Two-Layer Output Contract

- **name:** Two-Layer Output Contract
- **problem solved:** Relying on prompt text alone for output-format consistency produces drift; machine consumers of structured output cannot tolerate it.
- **inputs:**
  - A prompt-level format definition, such as XML tags wrapping the answer.
  - Harness enforcement mechanisms: a stop sequence that detects the closing tag, and structured outputs for nested JSON schemas.
  - A classification of the output type: conversational vs. structured.
- **outputs:**
  - Format consistency enforced programmatically: generation stops at the contract boundary; schemas constrain structure.
- **benefits:**
  - Harness enforcement guarantees consistency to a higher degree than text instructions.
  - Right-sizes effort: conversational bots carry a light contract; structured outputs carry heavy enforcement.
  - Survives model migration better than prompt-text format pleading.
- **limitations:**
  - Stop sequences require knowing the terminal token of the format.
  - Structured outputs couple the schema to the API surface; schema changes become API changes.
  - Overkill for outputs with no downstream machine consumer.

## 9. Tool Integration Triad

- **name:** Tool Integration Triad
- **problem solved:** Instructing the model that a calculation is critical does not make it capable: it does mental math and returns a vague answer instead of a concrete one.
- **inputs:**
  - A capability gap: deterministic computation the model can reason about but not execute reliably.
  - A prompt instruction saying when the tool must be used.
  - A tool schema in the API describing what the tool does and when to use it.
  - A deterministic implementation of the operation.
- **outputs:**
  - Concrete, computed answers executed by the tool, with the model retaining the reasoning and when-to-call judgment.
- **benefits:**
  - Instructions do not add capability; the tool reliably executes what the model only reasons about.
  - Frees the model to reason over harder problems while tools execute them reliably.
  - The implementation is deterministic, testable, ordinary code.
- **limitations:**
  - All three integration points must be present; instruction alone or schema alone fails.
  - Adds API surface and maintenance burden.
  - Wrong-time-to-call remains a behavioral risk that evals must cover.

## 10. Generate-Evaluate-Repair Loop

- **name:** Generate-Evaluate-Repair Loop
- **problem solved:** A single mega-prompt that generates, verifies, and corrects in one context burns tokens and cannot finish within the output limit; soft requirements frozen into code also resist change.
- **inputs:**
  - A task specification with hard and soft constraints.
  - Three independent simple prompts: generator (first draft), evaluator (checks every rule with evidence of every violation), repairer (targeted fixes from the violations).
  - Soft constraints injected into the evaluator prompt at runtime.
- **outputs:**
  - A corrected artifact that passes constraints at lower token cost and latency than model-upsizing or limit-inflating routes.
  - A structured violation report with evidence per rule.
- **benefits:**
  - Passed all source cases with fewer tokens and lower latency than the bigger-model and bigger-limit routes.
  - Soft constraints become runtime-adjustable evaluator content with no backend change.
  - Each prompt stays simple and independently maintainable and testable.
- **limitations:**
  - Three prompts to maintain instead of one, and the loop itself still admits optimization.
  - The evaluator is an LLM: cost and non-determinism for soft judgments.
  - Repairer quality bounds the loop; pathological cases may need more iterations.

## 11. Ban-to-Source-of-Truth Rebalancing

- **name:** Ban-to-Source-of-Truth Rebalancing
- **problem solved:** Defensive bans (never give plan details, point to the URL) make newer, more instruction-following models withhold information they actually have in context — the inverse failure of hallucination.
- **inputs:**
  - A prohibition instruction introduced for a past model's failure.
  - The authoritative data available in context, such as a customer record with grandfathered allowances.
  - Observed withholding behavior.
- **outputs:**
  - A balanced instruction designating the in-context data as the accurate source of truth, replacing the ban list.
- **benefits:**
  - Fixes information withholding with the same move that fixes hallucination: designate the source of truth instead of prohibiting output.
  - Shortens the prompt by removing long ban lists.
  - Stops new models from over-complying old prohibitions.
- **limitations:**
  - Requires trustworthy in-context data; bad context gets confidently served.
  - Judging which bans are still load-bearing needs the patch ledger (pattern 4).
  - Softening a ban can re-expose the original failure it fixed, so the case must be eval'd.

## 12. Self-Check Reasoning Instruction

- **name:** Self-Check Reasoning Instruction
- **problem solved:** A smaller model reasons about a problem but submits unverified work; it fails not because it cannot reason but because it does not check.
- **inputs:**
  - Prompt guidance on how to reason through the problem.
  - An explicit instruction to check its work before outputting.
  - The output-limit budget.
- **outputs:**
  - A measured partial improvement (0/5 to 2/5 in the source case).
  - A new, distinct failure surface: truncation when enriched reasoning exceeds the output limit.
- **benefits:**
  - A cheap, prompt-only lever that lifts weaker models without upsizing.
  - Shifts the error class from rule violations to budget exhaustion, which is diagnosable.
  - Serves as the instruction rung of the escalation ladder (pattern 6).
- **limitations:**
  - Bounded improvement; may not reach passing on its own.
  - Longer reasoning collides with fixed output limits; truncation is a budget failure, not a quality failure.
  - Fixing it by raising max tokens passes the eval but destroys token and latency economics.
