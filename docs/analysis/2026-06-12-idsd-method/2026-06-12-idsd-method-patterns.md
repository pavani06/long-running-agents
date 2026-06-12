---
title: "Reusable Agentic Patterns from IDSD Method"
type: analysis
date: 2026-06-12
aliases: ["IDSD patterns", "ICE agentic patterns", "intent driven agent patterns", "agentic ICE framework"]
tags: ["agentes-orquestracao", "agentic-coding", "spec-driven-development", "harness-engineering", "context-engineering", "decision-discipline", "governanca"]
relates-to: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]"]
sources: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]"]
---

# Reusable Agentic Patterns from IDSD Method

Scope: extracted from `docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md`. Only patterns that can be reused inside agentic systems, harness design, long-running agent governance, or agent execution loops are included. Broad methodology commentary is kept only where it becomes an operational pattern for agents.

## 1. ICE Craft Ownership Split

- **name:** ICE Craft Ownership Split
- **problem solved:** Monolithic specs collapse because they mix intent, done boundary, workflow, and context, leaving agents to fill the gaps between them.
- **inputs:**
  - Outcome request or candidate agent task.
  - Human-authored intent draft.
  - Human-authored expectations draft.
  - Harness-owned context sources such as repository docs, codebase constraints, runtime state, and tools.
  - Ownership map for who controls intent, expectations, context, and loop execution.
- **outputs:**
  - Three separated crafts: Intent, Expectations, and Context.
  - Explicit owner assignment for each craft.
  - Gap list showing where the agent would otherwise have to infer missing decisions.
  - Agent task contract that passes only the right craft to the right execution phase.
- **benefits:**
  - Prevents a harness from treating one document as both user intent and implementation context.
  - Makes human-owned outcomes distinct from harness-owned mechanics.
  - Gives long-running workflows clearer auditability when behavior drifts.
- **limitations:**
  - Adds ceremony for very small or reversible tasks.
  - Requires a named human owner for intent and expectations.
  - Does not by itself prove that each craft is complete or testable.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:22
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:24
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:30
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:38

## 2. Five-Part Intent Completeness Gate

- **name:** Five-Part Intent Completeness Gate
- **problem solved:** Under-specified intent forces agents to invent constraints, failure cases, success cases, or impact boundaries during execution.
- **inputs:**
  - Intent description.
  - Constraints that bound acceptable work.
  - Failure scenarios that define wrong outputs.
  - Success scenarios that define the desired outcome.
  - Connections to other intents, systems, workflows, or decisions affected by this work.
- **outputs:**
  - Pass, fail, or clarify decision before the agent starts implementation.
  - Missing-field questions routed back to the outcome owner.
  - Normalized intent record attached to the agent task.
  - Impact links that downstream validation and change review can inspect.
- **benefits:**
  - Reduces token burn caused by the agent exploring unstated assumptions.
  - Turns intent into a first-class primitive instead of a vague prose request.
  - Creates traceability from a proposed change to affected downstream work.
- **limitations:**
  - Requires the outcome owner to understand enough of the domain to name failures and connections.
  - Can become bloated if every exploratory spike is forced through full precision.
  - Connections become stale unless the harness or owner maintains them as the system changes.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:26
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:65
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:69
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:76

## 3. Outcome-Owned Expectations Boundary

- **name:** Outcome-Owned Expectations Boundary
- **problem solved:** Agents start deciding what counts as done when expectations are not owned separately by the person who wanted the outcome.
- **inputs:**
  - Approved intent.
  - Done scenarios written in user or outcome language.
  - Failed scenarios that should reject the output.
  - Limits, non-goals, and constraints the result must respect.
  - Named outcome owner responsible for the definition of done.
- **outputs:**
  - Expectations artifact separate from implementation instructions.
  - Validation checklist, rubric, or eval targets derived from the outcome boundary.
  - Stop, retry, or escalate conditions for the agentic loop.
  - Questions for the owner when the boundary is incomplete.
- **benefits:**
  - Keeps the definition of done out of the implementation agent's discretion.
  - Lets the harness validate outputs against outcome language, not only code completion.
  - Makes failed and successful outcomes visible before a large diff exists.
- **limitations:**
  - Expectations are not an implementation spec and still need translation into tests, evals, or review checks.
  - Subjective outcomes need rubrics or examples to become reliably enforceable.
  - The boundary can slow work if the owner is unavailable when ambiguity appears.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:27
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:84
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:86
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:169

## 4. Harness Progressive Context Disclosure

- **name:** Harness Progressive Context Disclosure
- **problem solved:** Dumping all context at the start overloads the agent with irrelevant material and weakens the constraints that matter for the current step.
- **inputs:**
  - Context inventory such as codebase docs, architecture decisions, state, tool results, and operational constraints.
  - Current intent and expectations.
  - Current loop step and agent question.
  - Resolver, retrieval, or context-builder policy.
  - Token budget and context freshness requirements.
- **outputs:**
  - Step-scoped context packets supplied by the harness.
  - Retrieval handles or resolver paths for additional context.
  - Audit trail of what context was provided and why.
  - Omitted-context catalog when material is intentionally withheld from active context.
- **benefits:**
  - Reduces noise and token pressure in long-running agent loops.
  - Keeps context ownership in the harness instead of asking the agent to guess what it needs.
  - Makes context supply adaptable to the current step rather than frozen upfront.
- **limitations:**
  - Requires a capable context builder, resolver, or retrieval layer.
  - Bad disclosure policy can omit critical constraints and cause hidden failure.
  - Higher setup cost than a single prompt dump for short one-shot tasks.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:28
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:90
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:94
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:171

## 5. Expectation-Validated Agentic Loop

- **name:** Expectation-Validated Agentic Loop
- **problem solved:** Agent loops can keep iterating on generated progress instead of proving that the output satisfies the human-owned expectations.
- **inputs:**
  - Approved intent.
  - Outcome-owned expectations.
  - Harness-owned context disclosure mechanism.
  - Agent-generated code, documents, decisions, or actions.
  - Validation harness, tests, evals, or review checks.
  - Retry and escalation policy.
- **outputs:**
  - Built artifact or completed action.
  - Validation result against expectations.
  - Retry instructions focused on unmet expectations.
  - Merge, handoff, stop, or escalate decision.
- **benefits:**
  - Converts the agentic loop into a closed control system rather than open-ended generation.
  - Makes retries purposeful because each retry is tied to a failed expectation.
  - Preserves the human-owned definition of done while letting the harness run execution.
- **limitations:**
  - Ambiguous expectations can create retry loops with no clear path to success.
  - The loop is only as reliable as the tests, evals, and review checks used as validators.
  - High-risk changes can still require direct human approval even after validation passes.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:36
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:102
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:104
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:106

## 6. Presence-in-the-Loop Operating Metric

- **name:** Presence-in-the-Loop Operating Metric
- **problem solved:** Final approval gates arrive too late for a human to own correctness when an agent has already produced a large, plausible diff.
- **inputs:**
  - Agent work trace and iteration timeline.
  - Human checkpoints, comments, clarifications, and interventions.
  - Questions or uncertainty raised during execution.
  - Risk level, diff size, and validation status.
  - Named owner availability for the active work.
- **outputs:**
  - Presence timeline showing when the owner was involved during execution.
  - Stale-presence or absent-owner warnings.
  - Required intervention points before the loop continues.
  - Review confidence signal for the final gate.
- **benefits:**
  - Measures human ownership during the work rather than symbolic approval after the work.
  - Catches expectation drift earlier, when repair is cheaper.
  - Makes large autonomous diffs visible as a governance failure, not only a review burden.
- **limitations:**
  - Can become surveillance if treated as attention monitoring instead of outcome ownership.
  - Adds human attention cost and should be risk-tiered.
  - Presence does not guarantee good judgment unless checkpoints are structured and outcome-aware.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:53
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:96
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:100
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:132

## 7. Running-System Spec Distillation

- **name:** Running-System Spec Distillation
- **problem solved:** Treating polished retrospective specs as upfront inputs leads teams to demand a precision that usually exists only after the system has run.
- **inputs:**
  - Running prototype, product slice, or internal system.
  - Execution traces, passing behaviors, and failure cases.
  - Owner decisions and implementation constraints discovered during build.
  - Ambiguity probes such as independent rebuilds, alternate implementations, or evaluator reviews.
  - Stable examples that represent desired behavior.
- **outputs:**
  - Reverse-engineered spec grounded in observed behavior.
  - Ambiguity list discovered by attempting independent implementations.
  - Reference behavior set for future agents.
  - Tests, evals, or rebuild prompts derived from the running system.
- **benefits:**
  - Grounds specs in software that has already encountered real constraints.
  - Avoids the Symphony trap of mistaking a final artifact for the method that produced it.
  - Creates stronger regression material for future agent runs than speculative upfront prose.
- **limitations:**
  - Requires something real enough to observe, so it cannot replace minimal upfront intent and safety constraints.
  - Multi-implementation ambiguity shaking is expensive.
  - Retrospective specs can encode accidental behavior unless owners separate desired behavior from incidental implementation.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:45
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:49
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:51
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:185

## 8. Gap-Filling Token Burn Control

- **name:** Gap-Filling Token Burn Control
- **problem solved:** Agents left to fill intent, expectation, or context gaps can burn large token volumes while confidently producing the wrong outcome.
- **inputs:**
  - Token usage and burn rate per run, retry, and finished outcome.
  - Missing ICE fields or unresolved owner questions.
  - Validation failures and retry reasons.
  - Context fetch history and prompt size.
  - Outcome completion status.
- **outputs:**
  - Gap-cost report tied to finished outcomes, not raw generation speed.
  - Stop, clarify, retry, or continue decision when token burn rises.
  - Owner question or missing-context request that closes the actual gap.
  - Budget guardrail for future agent loops.
- **benefits:**
  - Shifts optimization from cheaper tokens to fewer wrong turns per completed outcome.
  - Makes hidden cost from gap-filling visible before it becomes multi-day rework.
  - Encourages intent and expectations hygiene because missing fields become measurable cost drivers.
- **limitations:**
  - Requires instrumentation across token use, validation failures, retries, and outcomes.
  - Token cost is a proxy and cannot replace quality or value measurement.
  - Strict burn gates can interrupt legitimate exploration unless the work is explicitly framed as an experiment.
- **source_reference:**
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:118
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:124
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:126
  - /mnt/c/Users/pavan/long-running-agents/docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis.md:173
