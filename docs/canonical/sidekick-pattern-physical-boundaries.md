---
title: "Sidekick Pattern at Physical Boundaries"
type: canonical
tags: ["agentes-orquestracao", "production", "evals", "harness-engineering"]
aliases: ["sidekick pattern", "ratatouille pattern", "agent rides along", "physical boundary human loop"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]"
  - "[[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]]"
  - "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]"
  - "[[docs/canonical/carve-out-pilot-hard-target|Carve-Out Pilot with Hard P&L Target]]"
  - "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
---

# Sidekick Pattern at Physical Boundaries

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Missing (integration value: Low)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Some work is physical: dexterity, senses, hands on the car. "Used where dexterity/senses are irreplaceable (~800 mechanics)" (analysis:99). The default designs both fail:

- **Exclude agents from physical processes:** inspection quality, repair cost, and warranty spend stay unmeasured and unimproved by software intelligence.
- **Escalate to humans as fallback:** the agent hands the task to a human when it cannot proceed, and the learning signal dies with the handoff — the open-loop failure: "Open-loop escalation: agent hands off to a human queue and forgets → no improvement data → system plateaus" (analysis:164).

Both defaults share a directional error: the human serves as a crutch for the agent (or is absent), and no telemetry flows back from the physical world into the agents or their evals.

Root cause: the org treats "agent cannot do physical work" as a boundary condition for the agent fleet, instead of an interface condition — a boundary where agent intelligence and human embodiment meet and can compound.

## Solution

Invert the direction: the agent rides along and guides the human; the human's execution returns as telemetry. The Kavak name for this is the "Ratatouille" / El Mike pattern: "Same scaling harness, agent rides along guiding a human mechanic (inspection procedure, tips)" (analysis:98-99). It is the same harness the fleet uses — not a special assistant app — which is what makes it scale with the fleet rather than beside it.

The mechanism in prose:

1. **Agent guides.** The sidekick agent drives the procedure: inspection steps, tolerances, tips, next best action, spoken or shown to the mechanic in the flow of work.
2. **Human executes.** The mechanic performs the physical work — the irreplaceable dexterity and senses (analysis:99).
3. **Telemetry returns.** The mechanic's voice notes come back as progress telemetry — the same channel the carve-out pilot uses for its daily plan-push loop (analysis:50) — feeding the agent's picture of physical execution and, through it, the eval corpus.
4. **Deployment stays at physical boundaries only.** Humans-in-the-loop is not a general fallback: "96% of interactions and 95% of transactions fully agent-handled; humans remain only where physical presence is required (handing over car keys)" (analysis:105-106).

This is one face of the broader inversion — "The help API, the three-role topology, the sidekick/Ratatouille pattern, and skill-building humans all reverse the default direction of service" (analysis:176) — here applied to embodied work rather than to decision help.

Concrete example — inspection run loop:

```yaml
# sidekick-session.yaml — one mechanic, one shift
human: mechanic-142 (physical execution: dexterity, senses)
agent: inspection-sidekick (same standard harness as the fleet)
guide_channel:
  to_human: step-by-step inspection procedure + tips (audio/wearable)
  return: voice notes per step (progress telemetry)
close_loop:
  telemetry -> agent state for this vehicle
  anomalies -> eval corpus as regression cases
measured: [inspection quality, repair time, repair cost,
           warranty cost, CSAT]
```

Reported outcomes at Kavak: "inspection quality up, faster/cheaper repairs, warranty costs down ~20-26%, CSAT up" (analysis:100).

## Implementation in this repo

### What already exists

Nothing covers the pattern; the classification evidence list is empty and the pattern is recorded NOT_FOUND (classification.yaml:217-229). The nearest non-equivalents, which calibrate the **inverse** direction of service (humans intervening in agent tasks, not agents guiding human work):

- [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]] and [[docs/canonical/human-afk-task-routing-gate|Human-AFK Task Routing Gate]] — calibrate human intervention in agent tasks (docs/system-of-record.md:219, :235, per classification.yaml:225-226).
- Voice notes appear once in curriculum, but only as a client-facing latency feature, not worker telemetry feeding evals: curriculum/10-references/model-capability-timeline.md:919-921 (classification.yaml:226-228).

### What is missing

1. **The agent-guides-human direction.** No canonical doc describes an agent riding along guiding a human worker. Searches for `sidekick|co-pilot|copilot|ride.along|mechanic|voice note|nota de voz` and `destreza|dexterity|physical work|trabalho fisico|presenca fisica` matched only the Kavak analysis package itself (classification.yaml:221-225).
2. **The telemetry-return channel as a generalization.** Worker voice notes flowing back into agent state and the eval corpus — the loop that distinguishes this from open-loop escalation (analysis:164) — exists in no canonical doc.
3. **The physical-boundary scoping rule.** Humans-in-the-loop reserved strictly for where physical presence is required (analysis:105-106), as opposed to a general fallback — unstated in the repo.

Integration value is Low for this repo because the pattern's core value sits at physical-world boundaries outside a software-agent harness scope; the transferable part is the telemetry-return-channel generalization (classification.yaml:228-229).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Physical work inherits fleet intelligence: warranty costs down ~20-26%, CSAT up (analysis:100) | Requires workers to accept agent guidance in the flow of physical work — organizational change |
| Same harness as the fleet, so improvements compound fleet-wide (analysis:98) | Sensor/actuator gap remains: the agent sees only what telemetry humans return |
| Telemetry closes the loop that open-loop escalation loses (analysis:164) | Voice-note telemetry needs transcription, structuring, and eval plumbing before it is signal |
| Human-in-the-loop stays scoped to true physical boundaries, not diffuse fallback (analysis:105-106) | Boundary classification ("physical?") is a policy decision that drifts as robot capability grows |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] (the sidekick runs the same standard harness as the fleet, analysis:98), [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] (what happens when the sidekick itself degrades mid-shift).
- **Validated by:** [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]] (measures the human's role from the other side of the interface), [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] (returned telemetry only counts if it feeds a representative eval corpus).
- **Complements:** [[docs/canonical/carve-out-pilot-hard-target|Carve-Out Pilot with Hard P&L Target]] (the operator's daily plan-push/voice-note loop, analysis:50, is the same channel viewed from above), [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] (physical-world anomalies become regression cases), [[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]] (telemetry as on-policy signal from the environment).

## References

- Analysis: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:98-100 (sidekick/Ratatouille pattern and outcomes), :105-106 (humans only at physical boundaries), :50 (voice notes as telemetry channel), :164 (open-loop escalation failure), :176 (inversion synthesis)
- Classification evidence: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:217-229 (pattern entry: Missing, evidence empty, integration value Low, NOT_FOUND searches, nearest non-equivalents)
- Cited files (as recorded in the classification YAML): docs/system-of-record.md:219, :235; curriculum/10-references/model-capability-timeline.md:919-921
- Source: Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md (a16z, video_id n34CIw3gk1k, 2026-08-10)
