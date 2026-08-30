---
title: "Goal-Driven Agents over Workflows"
type: canonical
aliases: ["goal-driven agents", "agents over workflows", "outcome ownership vs step compliance", "hard goal agents"]
tags: ["agentes-orquestracao", "agentic-coding", "harness-engineering"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]"
  - "[[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]]"
  - "[[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]]"
  - "[[docs/canonical/outcome-level-eval-hierarchy|Outcome-Level Eval Hierarchy]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
---

# Goal-Driven Agents over Workflows

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

The prevailing multi-agent expert/workflow pattern scripts agent behavior, producing deflection bots and no outcome ownership; agents never persist toward anything (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:102`).

Concrete scenario: a team builds a customer-service "agent" as a workflow DAG — classify intent → retrieve FAQ → draft reply → escalate if confidence low. Every step is compliant, every diagram is green, and the system is structurally incapable of doing the one thing that matters: converting a 3–4 month car-plus-loan decision cycle into a sale. The workflow answers calls; it cannot hold a multi-week objective, cannot replan when the customer's situation changes, and nobody in the system owns "this customer converts."

Root cause: the **workflow**, not the goal, is the unit of specification. Step compliance replaces outcome attainment as the measure, which caps the architecture at deflection-bot altitude. Kavak's explicit architectural bet against this: agents hold hard goals (not scripted workflows) and persist toward them (`docs/analysis/...-analysis.md:78-79`). The superhuman bar — outperform the best human ever hired on conversion, LTV, customer experience, deployed against the hardest problems (`docs/analysis/...-analysis.md:27`) — is what selects this architecture: you build a mega-expert, not a deflection bot (`docs/analysis/...-analysis.md:148`).

## Solution

Assign each agent a **hard, measurable goal** plus full tool/API access and persistence across the task horizon. The agent decomposes the goal into its own plan, persists toward it, and is measured on **outcome attainment, not step compliance** (`docs/analysis/...-patterns.yaml:123-127`).

Concrete example — the same business objective specified two ways:

```yaml
# Workflow specification (rejected): steps are the contract
workflow: handle_financing_inquiry
steps: [classify_intent, retrieve_offers, present_three_options, handoff_to_finance_desk]
success: each step executed, SLA 30s

# Goal specification (this pattern): the outcome is the contract
intent:
  goal: "customer closes financing within 45 days, portfolio-safe pricing"
  context: full cross-channel customer history, current inventory, rate sheet
  constraints: [portfolio_risk_ceiling, regulatory_disclosure]
  verification: funded-loan readout at day 45 (outcome-level eval)
  handoff: physical handover only at key handoff
persistence: agent survives across the whole horizon (own plan, own replans)
success: outcome attained; the plan is the agent's business, not the contract
```

The goal specification exploits the structural advantages agents have in complex sales — infinite patience, complete customer history, long-horizon planning, no fatigue (`docs/analysis/...-analysis.md:127`) — none of which a workflow DAG can express.

## Implementation in this repo

### What already exists

- `.opencode/skills/karpathy-guidelines/SKILL.md:148` — "## 4. Goal-Driven Execution — Metas Verificaveis": verifiable goals as the stop criterion, institutionalized at task level.
- `docs/canonical/value-gated-agent-control-loop.md:31` — "Add a value-gating decision point to the agent control loop that produces an explicit classification -- build, experiment, defer, or stop -- before execution begins": goal-directed value gating inside the loop.
- `docs/canonical/symphony-trap-awareness.md:33` — "Replace 'write spec then build' with 'build then distill spec from what works then rebuild with the spec as a contract.'": the anti-over-specification stance that keeps workflows from becoming the ceiling.
- `docs/system-of-record.md:234` — `intent-five-part-primitive.md`: "Intenção decomposta em cinco partes primitivas: goal, context, constraints, verification, handoff" — goal already exists as a specification primitive.
- `docs/system-of-record.md:283` — `business-outcome-first-eval-pipeline.md`: eval pipeline anchored in business outcomes — the measurement half of outcome-over-steps.

### What is missing

From the classification justification (`docs/analysis/...-classification.yaml:116-122`), the strategic reframe beyond the existing task-level depth:

1. **A hard persistent business objective owned by the agent over multi-week horizons** — repository goal machinery is task-scoped; no agent owns a 45-day or multi-month business objective.
2. **Agent-owned decomposition** — the repository decomposes goals upstream (humans/specs split goals into atomic units); the agent planning its own decomposition toward a persistent objective is absent.
3. **Outcome-attainment measurement instead of step compliance** — no canonical rule that the eval readout for a goal-driven agent is the business outcome, not per-step verification.
4. **The superhuman bar as architecture selector** — "better than the best human ever hired on hard problems" as the explicit criterion that chooses goal-driven architecture over workflow automation.

This is enrichment over existing depth, not a gap fill (`docs/analysis/...-classification.yaml:121-122`).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Exploits agent structural advantages: infinite patience, complete history, long-horizon planning, no fatigue (`docs/analysis/...-patterns.yaml:111`) | Goal compliance is harder to verify than workflow compliance; requires outcome-level evals (`docs/analysis/...-patterns.yaml:115`) |
| Changes what architecture you build — mega-expert vs. deflection bot (`docs/analysis/...-patterns.yaml:112`) | Presupposes the superhuman bar; incremental good-enough targets pull back toward workflows (`docs/analysis/...-patterns.yaml:117`) |
| Superhuman performance on hardest problems: 2.1x conversion vs. human team, tripled NPS/CSAT (`docs/analysis/...-patterns.yaml:113`) | Task-scoped agents remain simpler for narrowly scoped work (`docs/analysis/...-patterns.yaml:116`) |
| Smarter the model, the less scaffolding it wants — goals age better than orchestration graphs (`docs/analysis/...-analysis.md:149`) | Full tool/API access plus persistence layer per agent is a heavier substrate than a workflow runtime (`docs/analysis/...-patterns.yaml:119-121`) |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]] — goal, context, constraints, verification, handoff is the specification shape a hard goal takes.
- **Depends on:** [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]] — the in-loop value gate is how a goal-pursuing agent decides build/experiment/defer/stop without a script.
- **Validated by:** [[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]] — proves the goal is correctly specified precisely because two different plans can attain it.
- **Validated by:** [[docs/canonical/outcome-level-eval-hierarchy|Outcome-Level Eval Hierarchy]] — outcome attainment (never step compliance) is the measurement contract this pattern requires.
- **Complements:** [[docs/canonical/symphony-trap-awareness|Symphony Trap Awareness]] — both reject upfront scripting; the symphony trap names the failure when specification hardens into a workflow ceiling.

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:78-79` — explicit bet against multi-agent expert/workflow pattern; hard goals.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:27,127,148,149` — superhuman bar, structural advantages in complex sales, architecture selection, scaffolding-vs-intelligence.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:101-127` — pattern components/flow.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:93-122` — Partial Coverage (Medium) classification with the evidence cited above.
- Source: a16z interview, channel and video_id per `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md:5-8`.
