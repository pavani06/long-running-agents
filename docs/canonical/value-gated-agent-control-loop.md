---
title: "Value-Gated Agent Control Loop"
type: canonical
tags: ["agentes-orquestracao", "governanca", "decision-discipline", "harness-engineering", "spec-driven-development"]
aliases: ["value gate", "value-gated loop", "build-or-not gate", "agent value gate", "value-decision gate", "value gating"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
---

# Value-Gated Agent Control Loop

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-trap-spec-driven-development-is-setting/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Agent harnesses govern how an agent builds -- context management, deterministic dispatch, state persistence, evaluation, and loop control -- but they do not govern whether the agent should build the requested artifact at all. The decision vocabulary for value (build, experiment, defer, stop) is absent from the control loop. The loop knows how to execute, pause, resume, break, and terminate, but the break/terminate decisions are about execution quality and safety, not about value judgment.

The source analysis names this gap directly: "O harness nao deve apenas governar COMO o agente constroi (contexto, dispatch, avaliacao) -- deve tambem governar SE o agente deve construir. A ausencia desse gate no harness e o equivalente arquitetonico da ausencia de um owner do 'nao' no time" ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:175).

The repo has extensive pre-execution infrastructure: the Alignment Interview asks value and scope questions, the AFK Routing Gate classifies task readiness, and the Split-Brain Review evaluates plans against dual rubrics. But none of these produce a build/experiment/defer/stop classification as an explicit decision point in the control loop. The repo's loop controls (break, terminate, human approval gate) are about execution safety; the value dimension is not wired into the loop architecture.

## Solution

Add a value-gating decision point to the agent control loop that produces an explicit classification -- build, experiment, defer, or stop -- before execution begins, and that links the classification to intent statements and scope constraints.

**The value gate decision vocabulary:**

| Decision | Meaning | Behavior |
|---|---|---|
| Build | The work has clear value, a named user, and justified cost. Proceed with full execution. | Agent enters the build loop with full scope. |
| Experiment | Value is uncertain but worth investigating. The build is an experiment with explicit stop criteria. | Agent builds with constrained scope, stop conditions, and a defined evaluation point. |
| Defer | Value may exist but the question cannot be answered now. Revisit at a defined date or trigger. | Task is parked with rationale and re-evaluation date. |
| Stop | No clear user, no value signal, or cost unjustified. Do not build. | Task is closed with refusal rationale. |

**Placement in the loop architecture:**

The value gate sits before the existing loop intervention points. While the current loop controls (break, summarize, LM-as-judge, human approval gate, force terminate) govern execution quality mid-loop, the value gate governs whether the loop should start at all.

```
  Task/Intent arrives
        │
        ▼
  +------------------+
  | Value Gate       |
  | build/experiment |
  | /defer/stop      |
  +------------------+
        │
  build │ experiment
        ▼
  +------------------+     +------------------+     +------------------+
  | Plan Phase       | --> | Execute Phase    | --> | Verify Phase     |
  | (scope + steps)  |     | (agent loop)     |     | (evals + user)   |
  +------------------+     +------------------+     +------------------+
                                  │                        │
                                  ▼                        ▼
                           Loop controls:           Verification gates:
                           break, summarize,        PR-gated evals,
                           LM-as-judge,             human approval,
                           human approval gate,     degradation ladder
                           force terminate
```

**Mechanics:**

1. **Intent statement** is captured before the value gate. The intent answers: what outcome do we want, and for whom? Derived from the [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] or explicit user declaration.

2. **Value gate evaluation** uses the [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]] or a functional equivalent to classify the intent as build, experiment, defer, or stop. The three brake questions are the evaluation rubric.

3. **Scope constraints** are attached to the build or experiment decision. For build: full scope with explicit acceptance criteria. For experiment: constrained scope with stop conditions and a re-evaluation date.

4. **Decision record** is persisted. The classification, rationale, intent statement, scope constraints, and named decision owner are recorded and carried through the execution pipeline.

5. **Downstream consumption.** The decision record feeds into the [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] pipeline, the [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] (stop/defer tasks never enter the AFK queue), and the [[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger]] (auditable answer to why the agent is or is not working).

**Reframe from existing mechanisms:**

The repo has the structural pieces for this pattern but distributes the value-gating function across multiple mechanisms without an explicit decision point. The reframe is:

- The [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] asks value and scope questions but does not produce a build/experiment/defer/stop classification. Reframe: the alignment interview output feeds into the value gate, which produces the classification.
- The [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] classifies task readiness on four dimensions but does not include value as a dimension. Reframe: add the value gate classification as a fifth dimension -- tasks classified as stop or defer are not AFK-ready regardless of other scores.
- The [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75 has intervention points (break, terminate) but these are execution-quality controls. Reframe: add the value gate as a pre-loop decision point, distinct from the mid-loop and post-loop controls.

## Implementation in this repo

### What already exists

- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 runs a structured pre-planning interview with value and scope questions and a decision/deferral ledger. This is the closest mechanism: it interrogates intent before building.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:30-52 classifies tasks on ambiguity, architecture, feedback-loop readiness, and product judgment before allowing autonomous execution. Creates a pre-execution filter, but classifies task readiness, not task value.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75 defines loop intervention points: break, summarize, LM-as-judge, human approval gate, force terminate. These are execution-quality controls, not value decisions.
- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:29-64 unifies prompt, context, dispatch, and loop policy with gates. All gates govern execution quality, not value judgment.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:28-37 connects state intake, priority synthesis, execution routing, and feedback writeback. Routes work rather than gating by value.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-56 implements three-phase separation starting from a plan derived from intent.

### What is missing from the pattern

The classification marks Value-Gated Agent Control Loop as Partial Coverage because the specific decision vocabulary (build, experiment, defer, stop) attached to intent statements and scope constraints before execution is not formalized ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|classification]]:32-53).

Missing items:

1. The build/experiment/defer/stop decision vocabulary as an explicit classification in the control loop.
2. A value gate decision point placed before the execution loop begins, distinct from mid-loop execution-quality controls.
3. Integration of the value gate classification into the routing gate (as a fifth dimension) and the plan-execute-verify pipeline.
4. A decision record format linking intent, classification, rationale, scope constraints, and named decision owner.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Separates the agentic coding engine from the value brake that governs it | Requires human or business judgment that the harness cannot infer alone |
| Prevents build requests from self-approving just because generation is cheap | Adds friction to trivial changes if applied without a bypass policy |
| Gives long-running workflows an auditable answer to why the agent is or is not working | Low-quality intents can still approve low-value work |
| Closes the architectural gap named by the source analysis itself | The classification vocabulary adds a decision step that teams may resist |
| Integrates naturally with existing pre-execution infrastructure | Value judgment quality is hard to measure without delayed outcome tracking |

## Relationship to Other Patterns

- **[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]** -- the value gate is a new pre-loop decision point that complements the existing mid-loop and post-loop controls. The owned loop governs execution; the value gate governs whether execution should start.
- **[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]** -- the control plane unifies prompt, context, dispatch, and loop policy. The value gate is a new dimension of the control plane: governing whether dispatch should occur at all.
- **[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]** -- the OS routes work and writes back feedback. The value gate adds a pre-routing filter: work that fails the value gate does not enter the routing queue.
- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake questions are the tactical evaluation rubric for the value gate. The gate is the architectural placement; the brake questions are the decision framework.
- **[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]** -- the alignment interview captures intent and hidden constraints. The value gate consumes the interview output and produces the build/experiment/defer/stop classification.
- **[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]** -- the value gate classification should be a dimension of the routing decision. Tasks classified as stop or defer are not routable as AFK-ready.
- **[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]** -- every build or experiment that passes the value gate enters the deferred ledger. The ledger tracks structural debt; the value gate prevents unnecessary entries.
- **[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]** -- the value gate feeds the plan phase with the intent statement and scope constraints that shape the plan.

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]:41-48 -- source description of Engine vs. Brake model
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]:15-41 -- extracted pattern structure
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]:32-53 -- classification evidence and gap analysis
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:175 -- the harness must govern not just HOW but WHETHER the agent should build
