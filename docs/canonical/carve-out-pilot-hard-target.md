---
title: "Carve-Out Pilot with Hard P&L Target"
type: canonical
tags: ["governanca", "decision-discipline", "production", "evals"]
aliases: ["carve-out pilot", "hard pnl target", "ai ceo pilot", "contained operating unit"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]"
  - "[[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]]"
  - "[[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]]"
  - "[[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]]"
  - "[[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]]"
  - "[[docs/canonical/sidekick-pattern-physical-boundaries|Sidekick Pattern at Physical Boundaries]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
---

# Carve-Out Pilot with Hard P&L Target

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage, High integration value
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Agent pilots fail two ways at once: unbounded scope and soft readouts.

**Unbounded scope:** a pilot that crosses the org ("everyone try an agent in your process") diffuses into a hackathon. The source names this failure directly: "Hackathon/use-case-sponsorship transformation: diffuse bottom-up effort with no target org design" (analysis:166), and "bottom-up cannot generate the taste/strategy for what to build ... Hackathons + sponsored use cases don't work" (analysis:135).

**Soft readouts:** a pilot graded on "impressive model behavior" rather than a hard, pre-registered financial outcome. The repo's own guidance already warns: "Prefer slices with clear before/after outcome evidence, not merely impressive model behavior" (docs/canonical/domain-embedded-workflow-automation-wedge.md:44). Without a hard target, the pilot cannot fail — and a pilot that cannot fail cannot decide anything.

Concrete scenario: a company wants proof that agents can run operations. Option A: a demo where an agent summarizes support tickets — proves nothing about running a business. Option B: hand one support team an agent — blast radius unclear, success metric negotiable after the fact. Root cause in both: containment and financial accountability were never designed as the two axes of the pilot.

## Solution

Carve out one contained operating unit, install an agent in the standard harness as its operator (the "AI CEO"), and make a hard P&L number the eval readout.

The Kavak instance: "Isolate one city as a contained experiment; install an agent in the standard harness as its CEO, with a hard P&L target (goal: 2x profits in month one; got 1.5x in six weeks)" (analysis:49). The value mechanism is depth, not altitude: "enumerate every number and customer, forecast perfectly, micromanage daily execution against plan" (analysis:132). Daily execution runs through a telemetry loop: "daily plans pushed to every physical worker, voice notes returned as progress telemetry. All KPIs moved (CSAT, inventory quality, rotation, financing penetration)" (analysis:50).

The mechanism in prose — four load-bearing properties:

1. **Containment by org boundary, not by tool scope.** A city is a full P&L with clean edges; blast radius is the unit itself. This is containment at business-unit granularity, one level above the module-level blast-radius rows in [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]] ("The change fits within existing module boundaries with a clear public interface", docs/canonical/human-afk-task-routing-gate.md:35).
2. **The standard harness, unmodified.** The pilot agent runs the same harness as the future fleet — otherwise the pilot proves nothing about the fleet.
3. **Hard financial readout.** The P&L target is the eval: pre-registered, numeric, and owned by the agent.
4. **Daily plan-push/telemetry-return loop.** The agent pushes daily plans to human workers; humans return voice notes as progress telemetry (analysis:50) — the loop that makes daily micromanagement possible.

Concrete example — pilot charter:

```yaml
# pilot-charter.yaml
unit: city-of-quito-operations          # contained operating unit
operator: agent in standard-harness-v1  # same harness as fleet target
readout:
  metric: profit
  target: 2.0x baseline_month   # pre-registered hard P&L target
  horizon: month one            # measured: 1.5x in six weeks
telemetry:
  plan_push: daily, per physical worker
  return_channel: voice notes from workers
  kpis_watched: [csat, inventory-quality, rotation, financing-penetration]
exit: [scale-to-next-city, iterate-harness, kill]
```

## Implementation in this repo

### What already exists

- **Containment and outcome-anchored first slices:** the automation wedge is defined as a "Small workflow slice with high pain, bounded scope, available data, clear owner, and testable outcome" (docs/canonical/domain-embedded-workflow-automation-wedge.md:38), with the explicit preference for before/after outcome evidence over impressive model behavior (docs/canonical/domain-embedded-workflow-automation-wedge.md:44).
- **Blast-radius containment at task/module level:** the AFK routing gate's architecture row (docs/canonical/human-afk-task-routing-gate.md:35); the classification additionally records module-design containment at architecture-as-agent-affordance.md:38 and review calibration at contextual-severity-calibration.md:25 (classification.yaml:401-403).
- **Hard-goal machinery:** [[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]] and [[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]] supply verifiable-goal specification (classification.yaml:397-398).
- **Business-anchored eval readouts:** [[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]] defines success in business terms before technical pipelines.

### What is missing

1. **Agent-as-operator of a contained unit.** No doc covers "an agent running a contained business unit against a profit target" (classification.yaml:403-404). Existing containment stops at workflow slices and module boundaries.
2. **Hard financial P&L target as the eval readout.** The wedge's "testable outcome" never commits to a financial number owned by the agent (classification.yaml:399-400).
3. **The daily plan-push/voice-note telemetry loop.** No pattern describes the operator-to-physical-worker plan channel and its return telemetry (classification.yaml:400). Repo audit: "searched docs/canonical/ with 'pilot|carve|P&L|blast radius|isolated'" — matches are module design and review calibration only (classification.yaml:401-403).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Readout is unfakeable: profit moves or it does not (analysis:49) | A city-scale unit is expensive to isolate; most orgs must start smaller than Kavak |
| Pilot runs the standard harness, so results transfer to the fleet | Agent failure is publicly material: a missed P&L is a real business event, not a sandbox |
| Daily telemetry loop gives operator-grade visibility cheaply (voice notes, not dashboards) | Micromanagement-by-agent requires human workers to accept daily plan-push; organizational change cost |
| Clear exit rule: scale, iterate, or kill — decided by the hard number | Six weeks to 1.5x (analysis:49) sets a patient horizon many pilots will not be granted |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] (slice selection discipline), [[docs/canonical/intent-five-part-primitive|Intent Five-Part Primitive]] and [[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]] (the hard goal must be well-specified), [[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]] (business terms define the readout).
- **Validated by:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] (pilot KPIs must predict the outcomes being claimed), [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]] (which human-in-loop work the unit still requires).
- **Complements:** [[docs/canonical/sidekick-pattern-physical-boundaries|Sidekick Pattern at Physical Boundaries]] (the plan-push/voice-note channel is the operator-side twin of the mechanic sidekick loop), [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] (the "standard harness" the pilot must not modify), [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] (the P&L gate is the hardest brake).

## References

- Analysis: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:48-50 (carve-out city pilot), :132 (AI-CEO value from depth), :135-136 (top-down vs hackathon), :166 (hackathon failure pattern)
- Classification evidence: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:379-404 (pattern entry, evidence quotes, integration value High, NOT_FOUND searches)
- Cited canonical docs (quotes as recorded in the classification YAML): docs/canonical/domain-embedded-workflow-automation-wedge.md:38, :44; docs/canonical/human-afk-task-routing-gate.md:35
- Source: Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md (a16z, video_id n34CIw3gk1k, 2026-08-10)
