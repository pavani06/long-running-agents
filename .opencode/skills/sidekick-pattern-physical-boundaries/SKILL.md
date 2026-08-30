---
name: sidekick-pattern-physical-boundaries
description: "Run an agent as a sidekick that rides along guiding a human worker at physical boundaries: step-by-step inspection and repair procedures, tolerances, quality checks, tips, spoken or shown in the flow of physical work, while the worker's confirmations and voice notes return as telemetry that feeds agent state and the eval corpus. Inverts the default direction of service: instead of replacing the human (full physical automation) or handing off to a human queue and forgetting (open-loop escalation), the same fleet harness guides the human who executes with irreplaceable dexterity and senses. Use when designing agent guidance for field service, mechanics, inspection or repair procedures, warehouse or handover work where errors are expensive (warranty claims, rework), or when worker voice notes should become progress telemetry. Triggers: 'sidekick', 'sidekick pattern', 'ratatouille pattern', 'el mike', 'agent rides along', 'ride-along agent', 'agent guides human', 'agent guides mechanic', 'mechanic guidance', 'physical boundary', 'physical work agent', 'human-in-the-loop physical', 'telemetry from physical work', 'worker voice notes', 'voice notes as telemetry', 'inspection procedure agent', 'field service guidance', 'warranty reduction', 'warranty cost down', 'guide the human who executes'."
license: MIT
compatibility: opencode
metadata:
  version: 1.0.0
  audience: all-agents
  workflow: agent-architecture
  priority: low
  source: "Kavak's Playbook for Rebuilding a Company Around AI — analysis 2026-08-30 (pattern classified Missing, integration Low)"
---

## What I Do

I replace the two failing defaults at physical work boundaries — exclude agents entirely, or escalate to a human queue and forget — with an inversion: **the agent rides along guiding the human; the human's execution returns as telemetry** (`...-analysis.md:98-99` — "Same scaling harness, agent rides along guiding a human mechanic (inspection procedure, tips). Used where dexterity/senses are irreplaceable (~800 mechanics)").

The loop has four beats:

1. **Agent guides.** The sidekick agent drives the procedure: inspection steps, tolerances, tips, next best action — spoken or shown to the worker in the flow of work.
2. **Human executes.** The worker performs the physical work — the dexterity and senses software does not have (`...-analysis.md:99`).
3. **Telemetry returns.** Worker confirmations and voice notes come back as progress telemetry — the same channel the carve-out pilot uses ("daily plans pushed to every physical worker, voice notes returned as progress telemetry", `...-analysis.md:50`) — feeding agent state for this job and, through it, the eval corpus.
4. **Deployment stays at physical boundaries only.** Humans-in-the-loop is not a general fallback: humans remain only where physical presence is required ("96% of interactions and 95% of transactions fully agent-handled", `...-analysis.md:105-106`).

Reported outcome at Kavak: "inspection quality up, faster/cheaper repairs, warranty costs down ~20-26%, CSAT up" (`...-analysis.md:100`).

## When to Use Me

Load this skill when:

- The work is physical and the worker's dexterity/senses are irreplaceable — inspection, repair, field service, warehouse picks, key handover
- Errors at the physical boundary are expensive: warranty claims, rework, safety recalls
- A procedure exists (or should exist) in documentation: steps, tolerances, quality checks, tips
- Worker actions could return as signal: confirmations, voice notes, photos, measurements
- You want physical work to inherit fleet intelligence: same harness, same evals, compounding improvements

Do NOT use when:

- The human-in-the-loop need is **judgment escalation** on an agent's task (a human deciding/reviewing agent output) — that is the inverse direction of service; see [[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]] and [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]]. The sidekick pattern is the agent guiding the human's physical execution, not humans rescuing agent decisions.
- **No human is present** — attempting full physical automation with no worker to guide and no telemetry channel is the sensor/actuator fantasy, not this pattern.
- The work is pure knowledge work with no physical execution — a co-pilot for text is not a sidekick session; there is no embodied step to confirm.
- The "procedure" cannot be sourced from documentation — guidance invented by the agent at runtime is hallucination risk, not a procedure.

## The Anti-Pattern

```
ANTI-PATTERN: Full physical automation fantasy + open-loop ticket escalation.

Two wrong answers to "the agent cannot do physical work":

  1. PRETEND IT CAN: schedule a robot inspection. The harness has no
     actuators, no hands, no senses — the "execution" is a stub.

  2. FORGET IT EXISTS: open a ticket for the human maintenance queue
     and return. The learning signal dies with the handoff —
     "Open-loop escalation: agent hands off to a human queue and
     forgets → no improvement data → system plateaus"
     (...-analysis.md:164).

Consequence (source: ...-analysis.md:164, :100):
  - Inspection quality, repair cost, warranty spend stay unmeasured
    and unimproved by software intelligence
  - The 800 mechanics get NO guidance: every worker improvises, tribal
    knowledge never compounds, anomalies never become eval cases
  - The org reads "agents can't do physical work" as a boundary
    condition instead of an interface condition
```

Wrong code — full automation attempt with an open-loop fallback:

```python
from dataclasses import dataclass, field

# WRONG: the agent pretends to execute physically, and "delegates" by
# opening a ticket that no one ever reads back.

@dataclass
class RobotInspection:
    """Assumes actuators that do not exist."""
    findings: list[str] = field(default_factory=list)

    def inspect(self, vehicle_id: str) -> list[str]:
        # no hands, no senses: fabrication dressed as execution
        return [f"{vehicle_id}: looks fine"]


@dataclass
class ForgetfulTicketBot:
    queue: list[str] = field(default_factory=list)

    def handle_physical_task(self, task: str) -> str:
        self.queue.append(task)          # ticket opened...
        return f"ticket #{len(self.queue)} created"  # ...and forgotten
        # no guidance reaches the worker; nothing returns:
        # open loop, no improvement data (...-analysis.md:164)

# Failure mode: warranty costs keep climbing because defects the
# procedure would catch are only discovered by the customer.
```

## The Pattern

```
                 SAME FLEET HARNESS (no parallel assistant stack)
     ┌──────────────────────────────────────────────────────────┐
     │                SIDEKICK AGENT (guide channel)            │
     │  procedure steps + tolerances + tips + next best action  │
     └───────────────┬───────────────────────────▲──────────────┘
        guide (voice/screen) │                   │ telemetry
                     ┌──────▼──────┐    ┌────────┴─────────┐
                     │    HUMAN    │    │  TelemetryEvent   │
                     │   WORKER    │───>│ confirmations,    │
                     │ dexterity + │    │ voice notes,      │
                     │   senses    │    │ anomalies         │
                     └─────────────┘    └────────┬─────────┘
                                                 │ closed loop
                     ┌───────────────────────────▼─────────────┐
                     │  agent state (this job) → eval corpus   │
                     │  anomalies → regression cases           │
                     │  metrics: inspection quality, warranty  │
                     │  cost (~20-26% down), CSAT, rework      │
                     └─────────────────────────────────────────┘
```

Correct code — procedure from documentation, human confirms critical steps, telemetry flows back, anomalies feed evals, business metrics captured:

```python
from dataclasses import dataclass, field

# ---- Guidance: procedure sourced from documentation, never invented ----

@dataclass(frozen=True)
class GuidanceStep:
    step_id: str
    instruction: str          # what to do (from the documented procedure)
    tip: str                  # tolerance/trick: "103 Nm ±4", "min 3 mm"
    requires_confirmation: bool = False  # critical step: human must confirm


@dataclass
class TelemetryEvent:
    """One worker action returning through the guide channel."""
    step_id: str
    worker_id: str
    confirmed: bool = False   # human confirmed execution of the step
    voice_note: str = ""      # transcribed worker voice note (PII stripped)
    anomaly: bool = False     # deviation from the expected result


@dataclass
class RegressionCase:
    """A physical-world anomaly promoted to the eval corpus."""
    case_id: str
    procedure_id: str
    step_id: str
    anomaly_note: str


@dataclass
class OutcomeMetrics:
    """Business outcomes, not activity counts (...-analysis.md:100)."""
    inspection_quality: float   # 0.0-1.0
    warranty_cost_delta: float  # negative = reduction; Kavak saw ~-0.20..-0.26
    csat: float                 # 0.0-1.0
    rework_rate: float          # 0.0-1.0


@dataclass
class SidekickSession:
    """Agent rides along; human executes; telemetry returns.

    agent_id runs the SAME harness as the fleet (...-analysis.md:98):
    improvements compound fleet-wide instead of in a parallel
    assistant app.
    """
    session_id: str
    agent_id: str
    human_worker_id: str        # dexterity/senses are irreplaceable
    procedure: list[GuidanceStep] = field(default_factory=list)
    telemetry: list[TelemetryEvent] = field(default_factory=list)

    # 1. GUIDE: next unconfirmed step, with its tip
    def guide_next(self) -> GuidanceStep | None:
        done = {e.step_id for e in self.telemetry if e.confirmed}
        return next(
            (s for s in self.procedure if s.step_id not in done), None
        )

    # 2+3. OBSERVE → RECORD: worker action returns as a TelemetryEvent
    def record(self, event: TelemetryEvent) -> None:
        known = {s.step_id for s in self.procedure}
        if event.step_id not in known:
            raise ValueError(f"telemetry for unknown step: {event.step_id}")
        self.telemetry.append(event)

    # 4. FEED EVALS: recurring anomalies become regression cases
    def regression_cases(
        self, fleet_anomaly_counts: dict[str, int], min_occurrences: int = 2
    ) -> list[RegressionCase]:
        cases = []
        for e in self.telemetry:
            if e.anomaly and fleet_anomaly_counts.get(e.step_id, 0) >= min_occurrences:
                cases.append(RegressionCase(
                    case_id=f"REG-{self.session_id}-{e.step_id}",
                    procedure_id=self.session_id,
                    step_id=e.step_id,
                    anomaly_note=e.voice_note,
                ))
        return cases

    # Critical steps need explicit human confirmation before close-out
    def critical_confirmed(self) -> bool:
        critical = {s.step_id for s in self.procedure
                    if s.requires_confirmation}
        done = {e.step_id for e in self.telemetry if e.confirmed}
        return critical <= done

    def progress(self) -> float:
        if not self.procedure:
            return 0.0
        done = {e.step_id for e in self.telemetry if e.confirmed}
        return len(done) / len(self.procedure)


# Contract: guide → human executes → record → feed evals. The session
# never closes with critical_confirmed() False, and no executed step may
# lack a TelemetryEvent — an unconfirmed execution is an open loop.
```

## Implementation Rules

**Harness rules**

1. The sidekick agent runs the **same standard harness as the fleet** (`...-analysis.md:98`) — no parallel assistant stack, no separate eval pipeline. This is what makes the pattern scale with the fleet rather than beside it.
2. The sidekick is deployed **only at genuine physical boundaries** (`...-analysis.md:105-106`). Humans-as-general-fallback is the anti-pattern; the boundary classification ("is this physical?") is an explicit policy decision that drifts as robot capability grows — review it, don't hardcode it.

**Procedure rules**

3. Steps come from the documented procedure (inspection manual, repair guide) — instruction, tolerance/tip, expected result. Runtime-invented guidance is hallucination, not procedure.
4. Step granularity: one step = one confirmable action. If a step cannot be confirmed by a worker ("done, measured X"), it is too coarse or not physical.
5. Critical steps (safety, warranty-relevant) require explicit human confirmation before the session can close.

**Telemetry rules**

6. Every executed step returns a `TelemetryEvent`: confirmation, optional voice note, anomaly flag. Voice notes are transcribed and structured before they are signal (canonical tradeoff).
7. Worker voice notes are **worker PII**: strip personal content before anything enters the eval corpus; telemetry is procedure data, not surveillance data.
8. Recurring anomalies (seen ≥ N times across the fleet) become `RegressionCase`s in the eval corpus — the physical world's failure modes enter the same evals the software fleet uses.

**Metric rules**

9. Capture business outcomes per session and aggregate: inspection quality, repair time/cost, warranty cost delta, CSAT, rework rate (`...-analysis.md:100`). Activity counts (tickets opened, minutes guided) are superficial KPIs — signal without truth.

## Integration With This Repo

This pattern was classified **Missing** with **integration_value: Low** — "NOT_FOUND. Searched: docs/canonical/ ... via greps for sidekick|co-pilot|copilot|ride.along|mechanic|voice note ... — matches only inside the Kavak analysis package itself" (`...-classification.yaml:217-229`, entry "Sidekick Pattern at Physical Boundaries"). The canonical doc [[docs/canonical/sidekick-pattern-physical-boundaries|Sidekick Pattern at Physical Boundaries]] is the pattern of record; this skill plus the exercise below are the first artifacts covering it. Connection points:

- **`docs/canonical/sidekick-pattern-physical-boundaries.md:39-68`** — solution mechanics, the `sidekick-session.yaml` example, and the reported outcomes (warranty ~20-26% down, CSAT up); **`:87-94`** — tradeoffs (sensor/actuator gap, voice-note plumbing, boundary drift).
- **`curriculum/05-core-concepts/07-multi-agent-coordination.md:749-773`** — Pattern 13 ("Sidekick Pattern at Physical Boundaries — o Agente Guia, o Humano Executa") already cross-links the canonical doc; the exercise below is its hands-on counterpart.
- **`curriculum/03-nivel-3-advanced-architecture/exercises/exercise-08-sidekick-pattern.md`** — the companion exercise (session, telemetry, closed-loop pipeline with warranty/CSAT gates).
- **Inverse-direction neighbors** (do not conflate): `docs/canonical/presence-in-the-loop-metric.md` and `docs/canonical/human-afk-task-routing-gate.md` calibrate humans intervening in agent tasks (`docs/system-of-record.md:219`, `:235`, per `...-classification.yaml:225-226`); [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]] is the same inversion applied to decision help, not embodied work (`...-analysis.md:176`).
- **Nearest non-equivalent voice-note usage**: `curriculum/10-references/model-capability-timeline.md:919-921` covers WhatsApp voice notes as a client-facing latency feature — not worker telemetry feeding evals (`...-classification.yaml:226-228`).

## Quality Gates

- [ ] Telemetry closes the loop: every executed step produced a `TelemetryEvent`; recurring anomalies became `RegressionCase`s in the eval corpus — grep the session close-out for steps without telemetry, must return zero
- [ ] Procedure sourced from canonical/documentation (manual, repair guide) — no runtime-invented steps; each step carries instruction + tip + expected result
- [ ] Human confirms critical steps: `critical_confirmed()` is True before any session closes; an unconfirmed critical step blocks close-out
- [ ] Same harness as the fleet: the sidekick `agent_id` runs the standard fleet harness — no parallel assistant app or separate eval pipeline
- [ ] Voice-note privacy: worker PII stripped before eval-corpus entry; telemetry schema is procedure data (step, confirmation, anomaly), not surveillance
- [ ] Boundary scoping: deployment list of sidekick sessions contains only genuinely physical tasks; the boundary policy is written down and reviewable
- [ ] Business metrics captured and gated: inspection quality, warranty cost delta (target ~-20%), CSAT, rework rate — reported per session and aggregated; no activity-count success metrics

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:98-100` — the pattern: same scaling harness, agent rides along guiding a human mechanic; dexterity/senses irreplaceable (~800 mechanics); results (inspection quality up, warranty costs down ~20-26%, CSAT up)
- `...-analysis.md:105-106` — humans-in-the-loop only at physical boundaries: 96% of interactions and 95% of transactions fully agent-handled
- `...-analysis.md:50` — voice notes returned as progress telemetry (the carve-out pilot channel this pattern generalizes)
- `...-analysis.md:164` — open-loop escalation failure: agent hands off to a human queue and forgets → no improvement data → system plateaus
- `...-analysis.md:176` — the inversion synthesis: help API, three-role topology, sidekick/Ratatouille, and skill-building humans all reverse the default direction of service
- `...-classification.yaml:217-229` — entry "Sidekick Pattern at Physical Boundaries": classification Missing, evidence empty, integration_value Low, NOT_FOUND justification with searched locations and nearest non-equivalents
- `docs/canonical/sidekick-pattern-physical-boundaries.md` — the canonical pattern of record (problem, solution, `sidekick-session.yaml` example, tradeoffs, relationship to other patterns)
- `curriculum/05-core-concepts/07-multi-agent-coordination.md:749-773` — Pattern 13 with the scoping rule (humans only at genuine physical boundaries)
- `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-08-sidekick-pattern.md` — companion exercise
- Source: Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md (a16z, video_id n34CIw3gk1k, 2026-08-10)
