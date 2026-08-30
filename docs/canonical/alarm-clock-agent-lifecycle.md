---
title: "Alarm-Clock Agent Lifecycle"
type: canonical
tags: ["agentes-orquestracao", "harness-engineering", "production", "12-factor-agents"]
aliases: ["alarm clock lifecycle", "wake work sleep", "agent self-scheduling", "next-wake trigger"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]]"
  - "[[docs/canonical/versioned-durable-agent-state|Versioned Durable Agent State]]"
  - "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]"
  - "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]"
  - "[[docs/canonical/temporal-context-injection|Temporal Context Injection]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
---

# Alarm-Clock Agent Lifecycle

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage, High integration value
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

An agent fleet meant to run for hours or days cannot live inside a synchronous model call. "Long-running tools (async API calls, human approval waits, scheduled tasks) cannot complete inside a single synchronous model call" (docs/canonical/serializable-pause-resume-state.md:22). If the agent's only continuity is the context window, every gap between work bursts becomes amnesia: "state that lives only in the context window and turns failures or payment events into amnesia" (docs/canonical/versioned-durable-agent-state.md:23).

The concrete scenario: a customer-facing agent finishes a work burst at 14:00 and its next useful action is tomorrow at 09:00 (customer's local morning). Without a scheduling primitive, the options are all broken:

- **Keep the session alive** — burns tokens and context for 19 idle hours, and the context window degrades.
- **External orchestrator polls** — a central scheduler decides wake times for thousands of agents, becoming a bottleneck and a single point of failure, and it cannot know each agent's local reasoning about when work should resume.
- **Kill and re-instantiate fresh** — the new instance has no memory of why it was waiting; the long-term goal (e.g., a 3-month purchase cycle) resets on every gap.

Root cause: pause/resume machinery exists, but it is passive — something else must decide when to resume. The agent has no way to set its own next-wake.

## Solution

Give the agent an alarm clock and make the fleet lifecycle explicit: **wake → work → sleep**, where the agent itself sets the alarm before sleeping.

The mechanism in prose, per the Kavak fleet: "Agents wake, work for durations ranging from 3 minutes to 3 days, set an alarm for their next task, and sleep. This is the scheduling primitive for the fleet" (analysis:82-83). Three properties are load-bearing:

1. **Self-scheduling.** The wake time is decided by the agent's own reasoning about its goal ("customer decided in 3-4 months; check back after the weekend"), not by a central poller.
2. **Durable wake trigger.** The alarm lives outside the agent process — in persistent storage — so the sleep can outlive any session, VM, or model call.
3. **State continuity across sleep.** On wake, the agent deserializes and continues from exactly where it paused: "Serialize the entire agent state (context window + execution state + business state) to persistent storage. On resume, deserialize and continue from exactly where the agent paused" (docs/canonical/serializable-pause-resume-state.md:33).

Concrete example — alarm record in durable state plus a scheduler unit:

```yaml
# durable-state/alarm.yaml — written by the agent before sleeping
alarm:
  agent_id: customer-8812-agent
  wake_at: 2026-09-01T09:00:00-06:00        # customer-local morning
  wake_reason: "resume financing-offer follow-up; customer said 'next week'"
  task_pointer: tasks/financing-followup.md   # where to pick up
  state_ref: durable-state/v3/snapshot-4471   # what to deserialize
```

```ini
# /etc/systemd/system/agent-alarm@.service — wake trigger, one unit per agent VM
[Service]
Type=oneshot
# scheduler fires only alarms whose wake_at has passed
ExecStart=/usr/local/bin/agent-wake %i
# agent-wake: read alarm.yaml -> restore VM snapshot -> deserialize state_ref
#             -> inject wake_reason as first user message -> agent runs burst
```

The burst loop inside one wake cycle: deserialize state → work (minutes to days, per alarm:82) → write state back → write the next alarm → sleep. Choosing the next task after wake can reuse dashboard/priority logic where it exists: "orchestrator skill lines 27-62 defines a dashboard and priority logic for choosing the next task" (docs/canonical/closed-loop-agent-operating-system.md:54).

## Implementation in this repo

### What already exists

- **Pause/resume state contract:** serialize everything, resume exactly where paused (docs/canonical/serializable-pause-resume-state.md:22, :33).
- **Durable state with versioning:** the amnesia failure mode is already named, and a versioned durable-state contract answers it (docs/canonical/versioned-durable-agent-state.md:23).
- **Next-task selection:** dashboard and priority logic for choosing the next task exists in the orchestrator skill (docs/canonical/closed-loop-agent-operating-system.md:54).
- **Time awareness for prompts:** [[docs/canonical/temporal-context-injection|Temporal Context Injection]] supplies timestamps so a woken agent knows when it is.

### What is missing

1. **The alarm scheduler primitive.** No component where the agent sets its own next-wake and a scheduler fires it. Repo audit: "no alarm scheduler where the agent sets its own next-wake, no wake trigger, no wake-work-sleep fleet lifecycle as a named pattern" (classification.yaml:61-62).
2. **The named lifecycle.** Wake-work-sleep as the fleet-level lifecycle pattern appears nowhere outside the Kavak analysis files; searches for `alarm|wake|sleep|scheduler|cron` and `agendamento|despertador|proxima tarefa` across docs/canonical/, curriculum/, and .opencode/skills/ matched only the Kavak analysis package (classification.yaml:63-65).
3. **Burst-duration semantics.** Work bursts "from 3 minutes to 3 days" (analysis:82) as an explicit design input: the state contract must survive multi-day bursts, not just request-scoped pauses.

This doc fills gaps 1-3 at the canonical level; it does not introduce scheduler code.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Agents persist toward goals across hours and days without burning tokens while idle | Scheduler is new infrastructure with its own failure modes (missed alarms = missed customer moments) |
| Wake decisions use the agent's local goal reasoning, not a central poller's guess | Self-scheduling agents can set bad wake times; policy on wake-time choice becomes harness surface |
| Fleet scales: 100,000-200,000 instantiations/day implies sleep is the default state, wake is the exception (analysis:73) | Every alarm requires a durable-state snapshot; storage grows with wake frequency |
| Composes with model swaps: alarms live outside the model call, so the model is swappable between wakes | Clock skew and timezone handling (customer-local mornings) must be correct per-region |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]] and [[docs/canonical/versioned-durable-agent-state|Versioned Durable Agent State]] (state must survive sleep), [[docs/canonical/temporal-context-injection|Temporal Context Injection]] (woken agent needs to know now).
- **Validated by:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] (next-task selection on wake), [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]] (continuity across sleep must be evaluable, not assumed).
- **Complements:** [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] (the VM is what sleeps and wakes; the alarm is part of the harness, not the model), [[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]] (sleep as the maximal context reset, with durable state as the carrier).

## References

- Analysis: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:81-83 (alarm-clock lifecycle), :73 (daily instantiation scale), :150 (task- vs customer-scoped tradeoff)
- Classification evidence: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:41-65 (pattern entry, evidence quotes, integration value High, NOT_FOUND searches)
- Cited canonical docs (quotes as recorded in the classification YAML): docs/canonical/serializable-pause-resume-state.md:22, :33; docs/canonical/versioned-durable-agent-state.md:23; docs/canonical/closed-loop-agent-operating-system.md:54
- Source: Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md (a16z, video_id n34CIw3gk1k, 2026-08-10)
