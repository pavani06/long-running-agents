---
title: "Manual Brake Question Gate"
type: canonical
tags: ["governanca", "decision-discipline", "agentes-orquestracao", "spec-driven-development"]
aliases: ["manual brake", "brake questions", "three brake questions", "value gate questions", "cost-proxy gate"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
---

# Manual Brake Question Gate

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-trap-spec-driven-development-is-setting/
**Classification:** Missing, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

When the economic brake (production cost near zero) and the methodological brake (Spec-Driven Development collapsed under delivery pressure) are both removed simultaneously, nothing in the workflow forces anyone to ask "is this worth building?" before the agent starts coding. Cheap token-driven builds and the absence of enforced spec discipline create a vacuum where builds happen because nothing stops them. The result is feature inflation, carry debt from agent-created artifacts that never reach users, and an organization that has lost the institutional muscle of questioning value before constructing.

The source analysis names this as the two-brake failure: "a disciplina de perguntar 'vale a pena construir?' antes de construir perdeu simultaneamente dois mecanismos de enforcement" and "o colapso do SDD nao era o fundo; o fundo e a situacao resultante onde nem preco nem metodo forçam a pergunta de valor" ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:24-29).

## Solution

Introduce a manual brake -- a lightweight gate of three diagnostic questions that must be answered before any agent begins building. The questions artificially restore the economic and methodological brakes that the market removed.

**The three questions:**

1. **Who needs this, and what breaks for them if it never exists?** If the honest answer is "nobody," it is an experiment -- treat it as such with explicit success criteria and a stop date.
2. **Would we still build it if it cost a week of engineering time instead of an afternoon of tokens?** This is the cost-proxy question. It restores the economic gate by asking teams to price their own work in pre-agent terms. Most feature inflation does not survive this question.
3. **Who owns saying no to this?** A decision without an owner is a trap. Name the person whose job includes refusal. Their job also includes providing alternative intents when the original request is rejected.

The gate is a decision point, not a checklist. The answers must be challenged, not just recorded. The three questions together address the value dimension (who needs it), the cost dimension (the proxy), and the accountability dimension (who owns the refusal).

**Flow:**

1. A build candidate (feature, agent task, or continuation request) arrives.
2. The responsible owner or reviewer asks the three questions in sequence.
3. Answers are recorded with rationale.
4. Based on the answers, the candidate is classified: build, experiment (with stop criteria), defer, or stop.
5. The named refusal owner is recorded alongside the classification.
6. The classification and rationale travel with the task into downstream workflows.

**Integration with existing repo mechanisms:**

- The [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]] can incorporate the three questions into its one-question-at-a-time interview flow, using the decision/deferral ledger to record answers.
- The [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]] can consume the brake question answers as an additional routing dimension: tasks that fail the brake questions should not be routed as AFK-ready regardless of ambiguity/architecture scores.
- The [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] can use the brake question answers as a rubric for the product/destination reviewer.

## Implementation in this repo

### What already exists

- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-35 asks one-question-at-a-time to expose hidden constraints and record decisions -- structurally similar to the brake question gate, but its questions focus on architecture, scope, and product decisions rather than value, cost-proxy, and refusal ownership.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:32-37 classifies tasks on ambiguity, architecture, feedback-loop readiness, and product judgment -- a pre-execution filter without the value/cost/ownership dimensions.
- [[.opencode/skills/issue-start/SKILL|issue-start skill]]:111-147 creates an execution brief with objective, success criteria, scope, and out-of-scope -- a build contract without the cost/refusal dimension.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 reviews plans with dual rubrics but does not include cost-proxy or refusal-owner questions.

### What is missing from the pattern

The classification marks Manual Brake Question Gate as Missing because the three specific diagnostic questions are not present in any repo document, skill, or curriculum ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|classification]]:56-77).

Missing items:

1. The three brake questions themselves -- no canonical doc, skill, or curriculum lesson documents them.
2. A decision gate that produces build/experiment/defer/stop classification with rationale before execution.
3. A named refusal-owner field in task records or execution briefs.
4. Integration of the cost-proxy question into the pre-execution workflow alongside existing ambiguity and architecture checks.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Reintroduces a value and cost gate when real token prices do not force one | Consumes human attention at a step that currently costs zero time |
| Filters feature inflation before agents spend cycles implementing it | Can become a checkbox if answers are not challenged |
| Makes ownerless decisions visible instead of letting them drift forward | Relies on authority to enforce a no decision under delivery pressure |
| The cost-proxy question is simple and immediately usable without instrumentation | The proxy is approximate and should not replace real cost telemetry when available |
| Pairs naturally with existing alignment interview and routing gate infrastructure | Adds friction to trivial changes if applied without a bypass policy |

## Relationship to Other Patterns

- **[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]** -- the brake questions are the tactical implementation of the broader value-gating philosophy. The control loop defines the architectural placement; the brake questions define the specific decision vocabulary.
- **[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]** -- the third brake question ("Who owns saying no?") directly requires the Owner-of-No role. The role pattern designs the organizational structure; the brake question gate operationalizes it.
- **[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]** -- the brake questions prevent the three debts (skill, dependence, carry) from accumulating by stopping low-value builds before they create artifacts that enter the ledger.
- **[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]** -- the alignment interview can incorporate the brake questions into its question flow and record answers in the decision/deferral ledger.
- **[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]** -- tasks that fail the brake questions should not be routed as AFK-ready. The brake gate adds the value dimension to the routing gate's current four dimensions.
- **[[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]]** -- the brake gate prevents artifacts from entering the carry-debt pipeline; the sunset gate manages artifacts that were created despite the gate.

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]:62-70 -- source description of the Manual Brake and three diagnostic questions
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]:43-68 -- extracted pattern structure
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]:56-77 -- classification evidence and gap analysis
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:24-29 -- Two-Brake Failure model
