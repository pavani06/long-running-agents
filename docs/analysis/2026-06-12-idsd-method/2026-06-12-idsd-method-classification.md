---
title: "Comparative Classification: IDSD Method Patterns vs. long-running-agents Repo"
type: analysis
date: 2026-06-12
aliases: ["classificacao IDSD", "IDSD classification", "ICE pattern classification", "IDSD gap analysis", "mapeamento padroes IDSD"]
tags: ["agentes-orquestracao", "agentic-coding", "spec-driven-development", "harness-engineering", "context-engineering", "decision-discipline", "governanca"]
relates-to: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
sources: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]"]
---

# Comparative Classification: IDSD Method Patterns vs. long-running-agents Repo

**Date:** 2026-06-12
**Repo analyzed:** `pavani06/long-running-agents`
**Patterns source:** "IDSD Method" analysis (2026-06-12), 8 extracted agentic patterns
**Evidence basis:** `docs/canonical/`, `.opencode/skills/`, `.opencode/agents/`, `curriculum/`, `docs/system-of-record.md`, `AGENTS.md`
**Precedence order:** decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs

## Classification Legend

| Class | Meaning |
|---|---|
| Already Exists | Pattern is documented, implemented, or taught with equivalent depth |
| Partial Coverage | Elements exist but missing key mechanics, reframe, or formalization |
| Missing | Not present in any form (doc, code, or curriculum) |
| Better Implementation | Repo has a superior or more mature version of the same idea |

---

## 1. ICE Craft Separation

**Pattern:** Decomposing monolithic spec into Intent + Context + Expectations with distinct owners.

**Classification:** Partial Coverage

**Integration value:** High

**Why:**
The repo has extensive ownership separation across multiple canonical docs but does not formalize the Intent-Context-Expectations trichotomy as named crafts with explicit ownership assignment. The pieces exist -- intent collection, context engineering, expectations-as-rubrics -- but they are distributed across patterns rather than unified as the three ICE crafts.

**What exists:**

- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]:29-51 defines explicit ownership roles with refusal authority, a four-word decision vocabulary, and a decision record. This is the repo's strongest ownership mechanism -- but it governs a single gatekeeper role rather than assigning distinct owners to Intent, Context, and Expectations as separated crafts.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 runs a structured one-question-at-a-time interview to capture intent, expose hidden constraints, and record decisions. Separates intent capture from implementation, but does not formalize "Context" and "Expectations" as equivalent first-class crafts with their own owners.
- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:29-64 unifies prompt, context builder, dispatch, and loop policy as owned components. The Context Builder is explicitly an owned component (line 70-71: "Context is constructed, not appended"), but Context ownership is merged into the control plane rather than separated as an independent craft.
- [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]:73-78 attaches intent statements and scope constraints to build decisions. Separates intent from execution mechanics.
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:31-36 asks "Who owns saying no to this?" -- an explicit ownership question. But the question assigns one owner, not three distinct craft owners.
- [[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]]:30-48 formalizes the alignment output as a durable handoff artifact separating human judgment from agent interpretation -- closest to ICE intent/context separation.

**What is missing:**
The three named crafts (Intent, Context, Expectations) as a formal decomposition. The repo separates ownership conceptually (human vs. agent, planner vs. evaluator) but does not frame the work decomposition as the ICE triad. The `intent` is captured via Grill-Me; `context` is delivered via the resolver/hybrid-stack; `expectations` are encoded in rubrics and constraint-anchored evaluation. But no single canonical doc names "ICE Craft Separation" or assigns distinct owners to each craft as a deliberate architectural decision.

---

## 2. Intent as Five-Part Primitive

**Pattern:** Intent formalized as description + constraints + failure scenarios + success scenarios + connections.

**Classification:** Missing

**Integration value:** Medium

**Why:**
The five-part intent structure (description, constraints, failure scenarios, success scenarios, connections) is not present in any repo document, skill, or curriculum lesson. The repo captures intent through alignment interviews and manual brake questions, but does not formalize intent as a five-field primitive.

**Searched locations (NOT_FOUND):**
- `docs/canonical/` -- 57 canonical docs searched; no document defines a five-part intent format. Searched for `five-part`, `five-field`, `intent completeness gate`, `description + constraints + failure + success + connections`. All returned NOT_FOUND.
- `docs/canonical/grill-me-alignment-interview.md` -- captures intent through questioning but records answers in a decision/deferral ledger without the five specific fields.
- `docs/canonical/manual-brake-question-gate.md` -- asks three diagnostic questions (who needs this, cost proxy, who says no) but these are value-gating questions, not intent structure fields.
- `docs/canonical/vertical-slice-issue-generation.md` -- generates issues with observable behavior but does not use the five-part intent format.
- `curriculum/08-tools-templates/` -- sprint contract templates define scope, success criteria, and constraints but not the five specific intent fields.
- `.opencode/skills/` -- issue-start and orchestrator skills capture objectives and success criteria but not the five-part primitive.

**What exists nearby:**
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:30-37 captures decisions, deferrals, and rationale in a ledger -- structurally similar to intent capture but without the five specific fields.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 anchors evaluation on explicit, verifiable constraint lists -- covers the "constraints" field of the five-part intent but as an evaluation input, not as an intent field.
- [[curriculum/05-core-concepts/04-sprint-contracts|Sprint Contracts]]:1-3412 formalizes scope, success criteria, and failure handling as a contract between human and agent. Covers success and failure scenarios but within a contract frame, not an intent frame.

**Why not higher integration value:**
The five-part format is a specific authoring convention. The repo already captures equivalent information through the alignment interview (decisions), constraint-anchored evaluation (constraints), sprint contracts (success/failure), and manual brake (who needs this). Formalizing intent as a five-field primitive would add precision but is more a reframing than a new capability.

---

## 3. Human-Owned Expectations Boundary

**Pattern:** Definition of done written by outcome-owner, not guessed by keyboard-holder.

**Classification:** Partial Coverage

**Integration value:** High

**Why:**
The repo separates evaluation from generation (Generator-Evaluator) and assigns explicit ownership roles (Owner-of-No), but does not formalize "Expectations" as a standalone artifact authored exclusively by the outcome owner and consumed by the harness for validation. The done boundary exists -- in sprint contracts, rubrics, and constraint lists -- but ownership is implicit rather than enforced as "the person who wants the outcome must define done."

**What exists:**

- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]:29-51 defines explicit ownership with refusal authority. The role can say no to low-value builds. This is ownership of the value decision, but not ownership of the definition of done for a specific outcome.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-73 separates generation from evaluation. The Evaluator checks output against rubrics and constraints. The rubrics serve as expectations, but their authorship (who defines the rubric) is not enforced as outcome-owner-owned.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 anchors evaluation on explicit, verifiable constraints from client state and business rules. Constraints define the done boundary, but the pattern focuses on constraint verification mechanics rather than constraint ownership.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 captures decisions and defers unresolved questions -- the interview output forms implicit expectations, but the output is a decision ledger, not an expectations artifact.
- [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]:73-78 attaches intent statements and scope constraints to build decisions. Scope constraints define done boundaries, but the pattern focuses on placement in the loop rather than ownership of the done definition.
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:33-35 asks "Who needs this, and what breaks for them if it never exists?" This forces the outcome-owner to define what success looks like, but as a diagnostic question rather than a formal expectations artifact.
- [[curriculum/05-core-concepts/04-sprint-contracts|Sprint Contracts]]:1-3412 formalizes explicit agreements with scope, success criteria, and failure handling. This is the repo's closest mechanism to an "expectations boundary" -- a contract defining what done means. However, the contract is presented as a negotiated agreement between human and agent, not as a boundary authored exclusively by the outcome owner.

**What is missing:**
The explicit concept of "Expectations" as a named artifact with a single named owner (the outcome-owner), separate from implementation instructions. The repo has contracts, rubrics, and constraints that serve the same function, but ownership is distributed (rubric author vs. interviewer vs. evaluator) rather than pinned to the outcome owner as a deliberate governance rule.

---

## 4. Harness-Owned Progressive Context

**Pattern:** Context fed progressively by harness, not dumped as single wall at start.

**Classification:** Better Implementation

**Integration value:** Low -- repo exceeds the pattern's maturity

**Why:**
The repo has formalized progressive context disclosure as a mature canonical pattern with resolver mechanics, trigger evals, capability directory, and thin base context -- a more sophisticated model than the IDSD pattern's "harness feeds context progressively." The repo's resolver-based model adds positive/negative triggers, deduplication policy, and trigger evals that the IDSD pattern does not describe.

**Evidence that exceeds the pattern:**

- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]:28-53 defines a five-part resolver model: thin base context, capability directory, positive triggers, negative triggers, and trigger evals. This formalizes progressive context as a tested routing layer, not just "feed context in steps."
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:28-42 defines a layered context assembly policy with explicit budget ordering: prompt, memory, durable state, summaries, latest result, and recoverable handles. Each layer has a defined scope, budget, and freshness requirement.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:26-39 bounds active context to head, tail, and latest result while keeping the middle recoverable by handle -- implementing progressive context reduction, not just progressive disclosure.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-53 catalogs omitted context with `id`, `location`, `preview`, `scope`, and `fetch` -- making context recovery explicit rather than lost on reduction.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41 preserves invariant harness instructions separately from reducible context -- distinguishing what must never be removed from what can be progressively disclosed.
- [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]] formalizes the full pipeline from one-off workflow to resolver-routed, tested skill -- the broader context-routing infrastructure.
- [[.opencode/skills/issue-start/SKILL|issue-start skill]]:16-23 and [[.opencode/skills/issue-review/SKILL|issue-review skill]]:16-23 demonstrate load-on-demand skill triggers in production -- practical progressive disclosure in the agent lifecycle.
- [[curriculum/GLOSSARY|Glossary]]:110-113 defines "Context Progressive Disclosure" as a curriculum concept -- taught, not just documented.

**Why better:**
The IDSD pattern describes progressive context as a general approach. The repo formalizes it as a resolver-based architecture with trigger contracts, evals, deduplication, and a layered context stack that handles both disclosure and reduction. The repo also teaches this in the curriculum (Context Management core concept, Nivel 1 token budgeting) and implements it in operational skills (issue-start, issue-review, issue-finish loading only relevant context).

---

## 5. Agentic Loop with Validation Gate

**Pattern:** Harness codes, validates against expectations, retries until met.

**Classification:** Already Exists

**Integration value:** Low -- repo already implements at equivalent depth

**Why:**
The repo has multiple canonical patterns that together implement the code-validate-retry loop with richer mechanics than the IDSD pattern describes. Generator-Evaluator is the direct analog: Generator builds, Evaluator validates against constraints, rejects with feedback, and the loop retries. This is the same structure formalized with more detail.

**Evidence:**

- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-73 formalizes the two-agent loop: Generator produces candidate output, Evaluator checks against persisted client state and rubrics, returns approve or reject with feedback. The diagram at lines 34-73 shows the explicit retry loop when rejected output returns to Generator with feedback. This is functionally identical to the IDSD "codes, validates, retries until met" pattern.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:29-75 defines a 4-component loop (Prompt, Context Builder, Switch Statement, Loop) with intervention points including LM-as-judge, human approval gate, and force terminate. The loop is owned by application code, not a framework -- giving precise control over when to validate and retry.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-60 implements a three-phase separation with explicit verification phase and retry paths from failed verification back to execution. The verify phase validates against gates and routes failures back to execution with specific feedback.
- [[docs/canonical/structured-generation-constraint-validation-circuit|Structured Generation + Constraint Validation Circuit]] formalizes the generate-validate-repair-reject-audit cycle as a canonical pattern with repair attempts, rejection conditions, and audit trail.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 produces a verification matrix with pass/fail per constraint and an aggregate verdict -- the validation gate mechanics.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:28-45 connects state intake, execution routing, and feedback writeback as a continuous operating loop -- broader than the single-task code-validate-retry but same closed-loop philosophy.
- [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]:31-69 adds a pre-execution value gate with build/experiment/defer/stop decisions -- extending validation beyond quality to value.

**Coverage summary:**
The repo's Generator-Evaluator canonical doc explicitly describes the "build, validate, retry" loop. Owned Agent Control Loop provides the loop architecture. Plan-Execute-Verify provides the phase separation. Constraint-Anchored Evaluation provides the validation mechanics. Together, these provide a more mature and detailed implementation of the same concept.

---

## 6. Presence-in-the-Loop Operating Metric

**Pattern:** Measuring human involvement during work, not just approval at the end gate.

**Classification:** Missing

**Integration value:** Medium

**Why:**
The concept of measuring human presence/involvement as a governance metric -- a presence timeline, stale-presence warnings, required intervention points -- is not formalized in any repo document, skill, or curriculum. The repo has pre-execution and post-execution human gates but does not track or measure human involvement during active agent work.

**Searched locations (NOT_FOUND):**
- `docs/canonical/` -- 57 canonical docs searched; no document defines a presence metric, presence timeline, stale-presence warning, or involvement measurement. Searched for `presence timeline`, `stale presence`, `absent owner`, `involvement metric`, `presence during execution`. All returned NOT_FOUND.
- `docs/canonical/manual-brake-question-gate.md` -- gates at pre-execution with three diagnostic questions. These are a pre-execution human checkpoint, not ongoing presence measurement.
- `docs/canonical/human-afk-task-routing-gate.md` -- classifies tasks as AFK-ready or human-in-loop at routing time. This is a classification decision, not a presence metric.
- `docs/canonical/grill-me-alignment-interview.md` -- runs pre-planning interview. Human is present before work starts, not measured during work.
- `docs/canonical/split-brain-planning-review.md` -- dual-rubric review during planning. Human judgment during a planning phase, not ongoing presence measurement.
- `docs/canonical/owner-of-no-role-design.md` -- assigns ownership but does not measure owner presence or involvement during execution.
- `.opencode/skills/` -- issue-start, issue-review, issue-finish, orchestrator skills manage workflow transitions but do not track human presence or involvement metrics during agent execution.
- `curriculum/` -- no lesson on presence measurement, involvement metrics, or stale-owner detection.

**What exists nearby:**
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:31-36 forces a human checkpoint before execution.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:30-52 routes tasks to human-in-loop when ambiguity or product judgment is needed.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 requires human answers to structured questions before the agent proceeds.
- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]:29-51 defines explicit ownership roles.

**What is missing:**
All existing gates are at entry points (before execution) or exit points (review, merge). None measure or track human involvement during active agent work. The specific concepts from the IDSD pattern -- presence timeline, stale-presence warnings, required intervention points before the loop continues, review confidence signal for the final gate -- do not exist in any form.

---

## 7. Symphony Trap Awareness

**Pattern:** Specs that work are reverse-engineered from running systems, not written upfront.

**Classification:** Partial Coverage

**Integration value:** Medium

**Why:**
The repo's philosophy is explicitly anti-upfront-spec. The "The Trap Spec-Driven Development Is Setting" analysis (2026-06-11) names this trap directly. Intent-first, production-grounded, code-as-disposable -- the repo's architecture embodies the Symphony Trap awareness. However, the specific ritual of reverse-engineering specs from running systems (ambiguity probes, multi-implementation shaking, behavior distillation) is not formalized as a named practice.

**What exists:**

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]:1-280 is a complete analysis of the upfront-spec trap. Its classification labels the repo's Intent-First Spec Loop as Better Implementation (lines 82-98) -- the repo's intent-first pipeline exceeds upfront spec approaches.
- [[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]:27-28 frames code as "a disposable build artifact" and states that "what matters is preserving the prompts, guardrails, and documentation that produced the code, not the code itself." This is the repo's strongest anti-upfront-spec statement: the durable asset is the harness, not the spec.
- [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]:26-52 anchors evaluation in representative production interactions, traces, tool results, and state snapshots. Grounds validation in real behavior rather than upfront expectations -- implementing the principle that ground truth comes from running systems.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]:28-60 converts production failures into durable regression knowledge. Failures observed in running systems become the spec for future behavior.
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]:28-50 tracks correlation between eval scores and production outcomes. If eval scores diverge from production behavior, the evals -- not the running system -- are updated.

**What is missing:**
The specific ritual of reverse-engineering: running prototype -> ambiguity probes (independent rebuilds) -> observed behavior extraction -> reference behavior set. The repo grounds validation in production but does not describe the practice of running a system to observe what it actually does, then deriving the spec from observation. The repo's approach is "build, validate, learn" rather than "observe running system, distill spec from behavior."

---

## 8. Token Economics of Gap-Filling

**Pattern:** Agents filling intent/context/expectations gaps burn exponentially more tokens per finished outcome.

**Classification:** Partial Coverage

**Integration value:** High

**Why:**
The repo has extensive token economics infrastructure -- per-call ledgers, burn-rate forecasting, health monitoring, strategic debt tracking -- but does not formalize the specific concept of gap-filling cost. The repo tracks how much you spend and at what rate, but cannot attribute token costs to specific information gaps or measure the exponential penalty of filling ICE gaps during execution.

**What exists:**

- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:29-62 maintains a per-call ledger with fixed cost, reducible cost, output reservation, safety buffer, remaining budget, and budget percentage. The ledger separates non-reducible blocks (fixed prompt, tool schemas, durable state) from reducible blocks (history, summaries) at line 34-45. This provides the instrumentation foundation that gap-filling measurement would consume.
- [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]:28-60 tracks consumption velocity, acceleration, and remaining runway in messages and minutes. Forecasts when token pressure will hit rather than detecting it after degradation.
- [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:32-55 converts budget and burn rate to green/yellow/orange/red health phases with corresponding actions (continue, monitor, compress, new session).
- [[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]:29-56 tracks three categories of strategic debt (skill, dependence, carry) with exposure review and mitigation decisions. The dependence debt category (line 36) captures "workflows built on assumption of free, correct generation" -- the closest concept to gap-filling cost, but framed as structural risk rather than token-efficiency optimization.
- [[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]:28-53 implements session handoff with explicit budget consideration and context reset.
- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:33-34 asks the cost-proxy question: "Would we still build it if it cost a week of engineering time instead of an afternoon of tokens?" This is a gap-filling cost proxy -- it estimates the true cost of building something that tokens make seem cheap. But it is a human judgment question, not an automated gap-cost measurement.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:34-566 teaches token budgeting as a full curriculum lesson with calculator, dashboard, burn rate, and phase scenarios.

**What is missing:**
The gap-cost attribution model. The repo can tell you how many tokens a session consumed, at what burn rate, and whether it hit the safety buffer. But it cannot tell you that "40% of tokens were spent filling the missing 'who needs this' gap" or "retries 3-7 were caused by an ambiguous constraint that should have been in the intent." The gap-cost report tied to finished outcomes and the missing-context request that closes the actual gap -- these specific mechanisms are NOT_FOUND:

- `docs/canonical/` searched for `gap cost report`, `gap fill token`, `missing ice field`, `fill gap burn`. All returned NOT_FOUND.
- No canonical doc maps token cost to specific ICE field gaps.
- No mechanism identifies that a retry was caused by missing intent, missing context, or missing expectations.

**What makes this High integration value:**
The repo has the cost instrumentation layer. Adding gap-filling cost attribution would close the measurement loop: pre-execution gates (Manual Brake, Grill-Me) prevent gaps, the token ledger tracks cost, and gap-attribution explains why cost exceeded budget. This would make the cost-proxy question in Manual Brake measurable rather than intuitive.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | ICE Craft Separation | Partial Coverage | High |
| 2 | Intent as Five-Part Primitive | Missing | Medium |
| 3 | Human-Owned Expectations Boundary | Partial Coverage | High |
| 4 | Harness-Owned Progressive Context | Better Implementation | Low |
| 5 | Agentic Loop with Validation Gate | Already Exists | Low |
| 6 | Presence-in-the-Loop Operating Metric | Missing | Medium |
| 7 | Symphony Trap Awareness | Partial Coverage | Medium |
| 8 | Token Economics of Gap-Filling | Partial Coverage | High |

**Totals:** Already Exists: 1, Better Implementation: 1, Partial Coverage: 4, Missing: 2

**Highest integration priorities:** ICE Craft Separation (High), Human-Owned Expectations Boundary (High), Token Economics of Gap-Filling (High). These three patterns address the same structural gap from different angles: the separation, ownership, and cost of the intent-to-execution boundary.

**Repo strengths in this classification:** The repo's progressive context engineering and validation loop infrastructure are more mature than the IDSD patterns describe. Harness-Owned Progressive Context (Better Implementation) and Agentic Loop with Validation Gate (Already Exists) require no integration -- the repo already exceeds these patterns.

**Related prior classifications:** The "The Trap SDD" classification (2026-06-11) found similar gaps around value gating and ownership, and classified Intent-First Spec Loop as Better Implementation. The IDSD patterns add the ICE craft decomposition and gap-filling token economics as new dimensions not covered by prior analyses.
