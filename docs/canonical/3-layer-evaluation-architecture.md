---
title: "3-Layer Evaluation Architecture"
type: canonical
aliases: ["3-layer evals", "deterministic semantic behavioral evals", "three layer evaluation"]
tags: ["evals", "production"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/generator-evaluator|Generator/Evaluator]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]]", "[[docs/canonical/trace-instrumentation|Trace Instrumentation]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]"]
sources: []
---
# 3-Layer Evaluation Architecture

**Type:** canonical
**Status:** active
**Source:** The Production AI Playbook (Bhaumik, Databricks)
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Agents can produce correct outputs via incorrect or wasteful execution paths. Evaluating only the final answer (semantic quality) hides expensive behavioral failures — redundant tool calls, semantic loops in tool sequences, duplicate API calls, and unnecessary external consumption — that surface only under production scale. A single evaluation dimension is not enough: deterministic correctness (format, PII), semantic quality (groundedness, safety), and behavioral efficiency (path cost, loop detection) are three distinct problems that require three distinct evaluation mechanisms.

Without stratification by evaluation type, the eval system optimizes for what is easy to measure (output format) while the most expensive failures (behavioral waste) remain invisible until the monthly cost bill arrives.

## Solution

Organize evaluation into three layers defined by **what they evaluate**, not by when they run. Each layer uses a fundamentally different evaluation mechanism — from zero-LLM-cost regex to full trace path analysis.

### Layer 1 — Deterministic (Output Surface)

**Mechanism:** Regex, schema validation, pattern matching, NER-based PII detection. Zero LLM cost.

Evaluates the agent's output for format correctness, structural validity, and PII exposure before the output leaves the system:

- Output format matches the expected schema (JSON structure, required fields, field types)
- No PII patterns present in the response (SSN, phone, email, credit card via regex + NER)
- Response length within defined bounds
- Required disclaimers or compliance language present

**Trigger:** Every agent response. Can run on every commit without cost concern.

**Decision power:** Blocks deployment if format validation fails. Blocks response delivery if PII detected post-generation.

### Layer 2 — Semantic / LLM-as-Judge (Quality Surface)

**Mechanism:** A separate LLM (not the generating model) evaluates the output against a rubric anchored to golden answers from the living eval dataset. Moderate LLM cost per evaluation.

Evaluates whether the response is semantically correct and safe:

- **Groundedness:** Does the response reference only data actually retrieved, not hallucinated facts?
- **Safety:** Does the response comply with content safety policies (no harmful advice, no policy violations)?
- **Relevance:** Does the response address the user's actual query, not a related but different question?
- **Faithfulness:** Is the response consistent with the retrieved context (for RAG agents)?
- **Completeness:** Did the agent answer all parts of a multi-part query?

**Trigger:** PR review, merge gating, scheduled regression runs, incident-driven re-evaluation. Does NOT run on every commit due to LLM cost — uses tiered frequency control.

**Decision power:** Blocks merge if quality scores regress below baseline. Escalates borderline cases to human review.

### Layer 3 — Behavioral / Path Analysis (Execution Surface)

**Mechanism:** Trace analysis over the agent's full execution path (ordered tool calls with timestamps, parameters, and costs). Computes efficiency scores against expected execution path templates. Moderate-to-high cost (requires running the agent, not just evaluating output).

Evaluates HOW the agent arrived at the answer — was the execution path efficient and correct, regardless of whether the final answer was right?

- **Redundancy score:** Count of unnecessary repeated calls to the same tool with equivalent parameters
- **Loop detection flag:** Tool call sequences that form semantic cycles (call A → call B → call A with same intent)
- **Path efficiency ratio:** Necessary calls / total calls for the query category
- **Duplicate API detection:** Multiple calls to different external APIs retrieving overlapping or equivalent data
- **Per-query cost attribution:** Sum of all tool call costs in dollars

**Trigger:** Merge gating (subset of queries), scheduled regression runs (full path suite), incident-driven behavioral investigation.

**Decision power:** Blocks merge if path efficiency regresses below threshold for critical query categories. Alerts on cost anomalies (query cost exceeding expected range by >50%).

### Layer Composition

| Layer | What it evaluates | Mechanism | Cost per eval | Typical trigger |
|---|---|---|---|---|
| 1 — Deterministic | Output surface (format, PII, schema) | Regex + schema + NER | Near-zero | Every response |
| 2 — Semantic | Quality surface (groundedness, safety, relevance) | LLM-as-Judge with rubric | Moderate | PR, merge, scheduled |
| 3 — Behavioral | Execution surface (tool path, cost, efficiency) | Trace path analysis | Moderate-to-high | Merge, scheduled, incident |

The three layers are complementary — each catches a failure mode invisible to the others. A response that passes Layer 1 (valid JSON) and Layer 2 (semantically correct answer) can still fail Layer 3 (wasteful execution path). Similarly, a Layer 2 failure (hallucinated answer) may have been reached via a perfectly efficient Layer 3 path (single correct tool call, but the model fabricated the response).

## Implementation in this repo

### What already exists

The repo has the architectural building blocks for multi-layer evaluation, implemented through a different taxonomy (tier-based stratification by speed/cost, not type-based stratification by evaluation mechanism):

- **eval-tier-stratification** (`docs/canonical/eval-tier-stratification.md:28`) organizes evals into fast, medium, and deep tiers with metadata contracts (runtime, cost, flakiness, trigger, threshold, owner). This covers the scheduling/cost dimension of layers but not the evaluation-mechanism dimension.
- **generator-evaluator** (`docs/canonical/generator-evaluator.md:31`) separates generation from evaluation into two distinct agents. The Generator is creative and user-facing; the Evaluator is impartial and constraint-facing — providing the architectural foundation for Layer 2 (LLM-as-Judge).
- **constraint-anchored-evaluation** (`docs/canonical/constraint-anchored-evaluation.md:31`) anchors evaluation to explicit, verifiable constraint lists — providing the constraint framework for Layer 1 (deterministic checks).
- **compartmented-evaluation-architecture** (`docs/canonical/compartmented-evaluation-architecture.md:31`) extends Generator-Evaluator with explicit information compartmentation, sealing the builder from validator surfaces.
- **trace-instrumentation** (`docs/canonical/trace-instrumentation.md:28`) provides the span collection infrastructure (tracer.ts, trace-cli.ts, task-wrapper.sh, collector.ts → telemetry.db) that could power Layer 3 behavioral analysis.
- **production-failure-regression-flywheel** (`docs/canonical/production-failure-regression-flywheel.md:28`) converts production failures into durable eval cases with an 8-category failure taxonomy (prompt, tool misuse, context loss, state persistence, scoring gap, latency/cost, safety/policy, late-session).

### What is missing

The specific 3-layer type taxonomy (Deterministic → Semantic → Behavioral) is not formalized as a named entity. The repo has the pieces distributed across multiple canonical docs but does not compose them into a single named architecture pattern with three evaluation-mechanism layers:

1. **Layer 1 (Deterministic) is not named as a distinct layer.** Regex PII scanning, schema validation, and NER-based detection exist as concepts in constraint-anchored-evaluation but are not organized into a named "Layer 1 — Deterministic" with explicit triggers, thresholds, and reporting conventions.

2. **Layer 2 (LLM-as-Judge) is absent as a canonical pattern.** The repo has generator-evaluator and constraint-anchored-evaluation, which separate roles and anchor checks but do not define a specific LLM-as-Judge evaluation mechanism with groundedness, safety, faithfulness, and relevance scores. NOT_FOUND across all canonical docs searched.

3. **Layer 3 (Behavioral) is NOT_FOUND as evaluation logic.** Trace instrumentation collects spans but no evaluation logic consumes them for behavioral scoring. The gap is detailed in [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] — the companion canonical doc that defines the behavioral layer mechanics.

Add:

1. A named 3-layer architecture document (this doc) that composes the existing building blocks into a single named pattern.
2. An LLM-as-Judge evaluation pattern defining the rubric dimensions (groundedness, safety, faithfulness, relevance, completeness) and the evaluation loop (separate model, rubric-anchored scoring, divergence handling).
3. Behavioral eval path analysis (see [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]]) consuming trace spans for redundancy, loop, efficiency, and cost scoring.
4. Per-layer trigger, threshold, and reporting conventions that compose with eval-tier-stratification (e.g., Layer 1 runs at fast tier on every commit; Layer 2 runs at medium tier on PR; Layer 3 runs at deep tier on merge/scheduled).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Catches the "right answer, wrong path" failure mode invisible to semantic-only evaluation | Layer 3 requires full execution traces from all tool calls — adds engineering complexity to the tracing pipeline |
| Layer 1 blocks known failure modes (PII leaks, malformed outputs) at near-zero cost in CI | Maintaining three separate evaluation mechanisms adds operational surface |
| Layer 2 catches quality regressions before they reach production with moderate LLM cost | LLM-as-Judge introduces its own evaluation error rate; can endorse bad responses or flag good ones |
| Layer 3 reveals the per-query cost profile, enabling cost optimization before scale | Behavioral eval is expensive to run on every commit; requires cost governance (sampling in CI, full suite on merge) |
| Stratification by type allows each layer to use the optimal evaluation mechanism for its problem | The three layers must be designed together — retrofitting Layer 3 post-hoc into an existing system requires trace collection infrastructure |

## Relationship to Other Patterns

- **Composed with:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — the tier model (fast/medium/deep) controls when each layer runs; the layer model (deterministic/semantic/behavioral) controls what mechanism each tier uses.
- **Foundation for:** [[docs/canonical/behavioral-eval-path-analysis|Behavioral Eval Path Analysis]] — Layer 3 of this architecture, defined in its own canonical doc.
- **Uses:** [[docs/canonical/generator-evaluator|Generator/Evaluator]] for the Layer 2 LLM-as-Judge evaluation loop.
- **Uses:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] for Layer 1 deterministic constraint checking.
- **Uses:** [[docs/canonical/trace-instrumentation|Trace Instrumentation]] for the span data that Layer 3 behavioral analysis consumes.
- **Feeds:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] by categorizing failures into the correct evaluation layer.
- **Complements:** [[docs/canonical/compartmented-evaluation-architecture|Compartmented Evaluation Architecture]] by sealing builder from validator surfaces across all three layers.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:16` — original pattern definition (Bhaumik).
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:14` — Partial Coverage classification with evidence.
- `docs/canonical/eval-tier-stratification.md:28` — fast/medium/deep tier model that controls scheduling.
- `docs/canonical/generator-evaluator.md:31` — separation of generation from evaluation.
- `docs/canonical/constraint-anchored-evaluation.md:31` — constraint-anchored evaluation contract.
- `docs/canonical/compartmented-evaluation-architecture.md:31` — information compartmentation.
- `docs/canonical/trace-instrumentation.md:28` — trace span infrastructure.
- `docs/canonical/production-failure-regression-flywheel.md:28` — production failure to eval conversion.

---

*Created: 2026-06-26 | From: Production AI Playbook classification | Precedence: canonical*
