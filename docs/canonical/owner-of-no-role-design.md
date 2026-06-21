---
title: "Owner-of-No Role Design"
type: canonical
tags: ["governanca", "decision-discipline", "agentes-orquestracao"]
aliases: ["owner of no", "refusal role", "designated skeptic", "no-owner", "refusal ownership", "value gatekeeper"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
---

# Owner-of-No Role Design

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-trap-spec-driven-development-is-setting/
**Classification:** Missing, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Builder-heavy agent teams naturally drift toward construction. The gravitational pull is toward building, not toward questioning whether the build is necessary. When no person or role is explicitly responsible for refusing low-value work, build decisions self-approve one iteration at a time. The source describes this as builder gravity: "em times de builders, a gravidade natural puxa para construir. Sem uma pessoa cujo unico trabalho e perguntar 'alguem precisa disso?', o time inevitavelmente entra na armadilha" ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:92). The failure is not that builders cannot recognize low-value work; it is that nobody is paid to say no, and without that role, the default answer is always yes.

The repo's agent system has roles defined by scope and function: the orchestrator coordinates, the KODA init initializes, the live tester tests, and the issue reviewer validates. None of these roles has refusal authority over whether work should proceed at all. The absence is structural: the system knows how to build and review, but not how to refuse.

## Solution

Design a named role or accountability point whose explicit job is to refuse low-value work, demand intent clarity, and provide alternative intents when the original request is rejected. The role is not a blocker -- it is an accelerator of valuable work by eliminating non-valuable work before it consumes agent cycles.

**Role definition:**

| Attribute | Description |
|---|---|
| Primary responsibility | Say no to build requests that lack clear value, user need, or cost justification |
| Secondary responsibility | Provide better intents: when rejecting a request, supply an alternative that is worth building |
| Decision vocabulary | Approve, refuse, defer (needs more information), experiment (build with stop criteria) |
| Authority | Can stop or redirect any agent build request before execution; decision is binding unless escalated |
| Accountability | Answerable for both false positives (approved low-value work) and false negatives (rejected high-value work) over time |

**Role mechanics:**

1. **Pre-execution gate.** The Owner-of-No is consulted before any significant agent build begins. The Manual Brake questions provide the decision framework; the Owner-of-No provides the person who answers them with authority.

2. **Refusal with alternatives.** Saying no is not enough. The role must pair each refusal with a constructive alternative: a narrower experiment, a different approach, or an explicit statement of what would make the work worth approving.

3. **Distributed ownership.** One person cannot gate all work for a team of any size. The role should be domain-scoped: a domain expert owns the refusal decision for work in their domain. Multiple Owners-of-No cover different surfaces.

4. **Escalation path.** When the Owner-of-No refuses and the builder disagrees, there is an explicit escalation path to a higher-authority decision. The default should be that refusal stands until escalated and overturned.

5. **Decision record.** Every decision (approve, refuse, defer, experiment) is recorded with rationale, date, and the alternative intent provided for refused requests. This record feeds the [[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger]] and enables calibration of refusal quality over time.

**Organizational integration:**

The Owner-of-No role works best when embedded in existing workflows:

- During the [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]], the Owner-of-No is the person who answers the brake questions and whose approval gates the transition from interview to plan.
- In the [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]], tasks refused by the Owner-of-No never reach the AFK-ready queue.
- In the [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]], the product/destination reviewer can serve as the Owner-of-No for that review instance.

## Implementation in this repo

### What already exists

- [[.opencode/agents/hop-orchestrator-rezek|hop-orchestrator-rezek]]: coordinates governance and role activation -- does not have refusal authority.
- [[.opencode/skills/orchestrator/SKILL.md|orchestrator skill]]: suggests next tasks and priorities -- routes work, does not refuse it.
- [[.opencode/skills/issue-review/SKILL.md|issue-review skill]]:14-15 validates and gates before merge with explicit user confirmation -- a stop-before-merge gate focused on quality, not value.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 reviews plans with dual rubrics -- approval, not refusal ownership.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:32-37 routes tasks as AFK-ready or human-in-loop -- classification, not refusal ownership.

### What is missing from the pattern

The classification marks Owner-of-No Role as Missing because no agent, skill, canonical doc, or curriculum material defines a named role whose explicit job is to refuse low-value work ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|classification]]:124-147).

Missing items:

1. A named role definition with refusal authority as its primary responsibility.
2. A decision vocabulary (approve, refuse, defer, experiment) with recorded rationale.
3. An escalation path for disputes between the Owner-of-No and builders.
4. Curriculum content on refusal ownership as a role design pattern (could live in Level 3 or 4).
5. Integration of the role into the existing agent workflow (where in the issue lifecycle does the Owner-of-No intervene?).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Turns saying no into a designed role instead of an accidental act of courage | Creates cultural tension when the team identifies speed with value |
| Gives the harness a concrete decision point before autonomous execution | Can be bypassed if builders keep private token workflows outside the gate |
| Makes refusal constructive by pairing no with better intents | Becomes a bottleneck if ownership is not distributed across domains |
| Prevents self-approving builds that drift forward without explicit approval | Requires organizational maturity to respect the role without undermining it |
| Provides accountability for both approval and refusal decisions over time | Decision quality is hard to measure without delayed outcome tracking |

## Relationship to Other Patterns

- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake questions are the tactical tool the Owner-of-No uses. The third question ("Who owns saying no to this?") directly names this role. The brake gate provides the decision framework; the Owner-of-No provides the accountable person.
- **[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]** -- the control loop defines where in the agent architecture the value decision lives; the Owner-of-No is the human component of that architectural decision point.
- **[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]** -- the product/destination reviewer in the split-brain review can serve as the Owner-of-No for the specific plan under review.
- **[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]** -- tasks where the Owner-of-No has deferred or refused should not be routable as AFK-ready regardless of other dimension scores.
- **[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]** -- skill debt accumulates when the Owner-of-No role is absent and nobody exercises the judgment muscle. The role directly prevents skill debt.

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]:90-94 -- source description of Ownership-of-No as role design
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]:124-148 -- extracted pattern structure
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]:124-147 -- classification evidence and gap analysis
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:159 -- builder gravity in teams without a designated skeptic
