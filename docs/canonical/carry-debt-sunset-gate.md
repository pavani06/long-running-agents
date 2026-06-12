---
title: "Carry Debt Sunset Gate"
type: canonical
tags: ["governanca", "agentes-orquestracao", "production", "harness-engineering"]
aliases: ["carry debt gate", "sunset gate", "artifact retirement", "artifact lifecycle", "agent output retirement", "prototype retirement gate"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]", "[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
---

# Carry Debt Sunset Gate

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-trap-spec-driven-development-is-setting/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Software that was cheap for an agent to create does not become free because it was cheap to make. It becomes inventory: maintained, secured, understood, and accounted for over its entire lifetime. Agent-created artifacts -- features, utilities, dashboards, helpers, experiments -- accumulate without anyone tracking what exists, who uses it, what it costs to maintain, or whether it still justifies that cost. The source identifies this as carry debt: "software construido sem necessidade nao se torna gratuito porque foi barato de fazer. Torna-se inventario: mantido, securitizado e contabilizado durante toda sua vida, e reprecificado para cima no momento em que o acesso e seu" ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:37).

The repo has a mature component lifecycle for harness infrastructure -- the [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] governs harness components with BUILD/STABILIZE/SIMPLIFY/REMOVE states, ROI thresholds, archiving, and One In One Out rules. But this lifecycle is scoped to harness engineering. Agent-created application artifacts (features, utilities, experiments, generated code) have no equivalent lifecycle. They enter production without a maintenance owner, an expiration date, or a retirement decision point.

## Solution

Extend the harness component lifecycle pattern to general agent-created artifacts. Install a sunset gate that maintains an inventory of what agents created, schedules periodic review of each artifact, and produces explicit keep/retire/archive/promote decisions with named maintenance owners.

**Artifact lifecycle states:**

| State | Meaning | Action |
|---|---|---|
| Active | Artifact is in production use with a named owner and clear value | Maintain, monitor, schedule next review |
| Watch | Artifact exists but adoption or value is uncertain. Observation window. | Monitor usage, set re-evaluation date |
| Retire | Artifact no longer justifies its carry cost | Archive with documentation, remove from active codebase |
| Archive | Retired artifact preserved for reference or possible reactivation | Stored with rationale for removal, reactivation path documented |
| Promote | Artifact graduated from experiment/watch to permanent feature | Transferred to team ownership, added to maintenance rotation |

**The sunset gate mechanics:**

1. **Artifact inventory.** Maintain a registry of agent-created artifacts with: artifact ID, what the agent created, for whom (user or use case), creation date, value hypothesis at creation time, current usage (if measurable), and current maintenance burden. The inventory is the source of truth for what agents have produced.

2. **Expiration dates.** Every agent-created artifact gets an expiration date or review trigger at creation time. Prototypes and experiments get short windows (e.g., 30 days). Features with clear value get longer windows (e.g., 90 days). The expiration date is not a hard delete -- it is a mandatory review trigger.

3. **Named maintenance owner.** Every artifact in the Active or Watch state has a named person responsible for it. The owner answers the keep/retire/archive/promote question at each review. If no owner can be named, the artifact defaults to Watch with a short expiration.

4. **Periodic review cadence.** At each review trigger, the owner evaluates: Is the artifact used? Does it deliver the value hypothesized at creation? What is its maintenance, security, and operational cost? Based on the answers, move the artifact to the appropriate state.

5. **Retirement execution.** When an artifact is marked Retire: archive the code with documentation explaining why it existed, why it is being retired, and what replaced it (if anything). Remove from the active codebase. If the artifact is in production, schedule staged removal with monitoring.

6. **Promotion path.** When an artifact demonstrates sustained value beyond the Watch window, it is promoted. Promotion means: transfer to team ownership (not an individual), entry into the standard maintenance rotation, removal from the special agent-artifact inventory, and treatment as a normal production feature.

**Reframe from existing mechanisms:**

The [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] already implements this pattern for harness components with BUILD/STABILIZE/SIMPLIFY/REMOVE states, quarterly cadence, ROI gating, archive with reactivation path, and One In One Out rules. The reframe is:

- Extend the lifecycle from harness components to general agent-created artifacts. The states map naturally: Active = STABILIZE, Watch = BUILD (early), Retire = REMOVE, Archive = archived, Promote = transition to team-maintained.
- Add artifact-level metadata (created by agent, for whom, value hypothesis) that harness components do not need.
- Add shorter cadences for prototypes and experiments (the harness lifecycle is quarterly; agent artifacts may need 30-day reviews).
- Add the named maintenance owner field, which the harness lifecycle does not require (harness components are team-owned by default).

The [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] provides the weekly review cadence and the mechanism for converting observations into actions. The sunset gate would feed GC Day with artifact retirement candidates. The [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] provides the classification framework for deciding whether an artifact is a domain invariant (promote) or a model-specific compensation (retire when the model improves).

## Implementation in this repo

### What already exists

- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:50-61 defines REMOVE phase with archive, reactivation, ROI gating (below 1x for two quarters triggers removal), and One In One Out rule. Covers the structural pattern but scoped to harness components.
- [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]:31-55 provides weekly cadence for reviewing observations and building guardrails -- the cadence infrastructure a sunset gate would consume.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]:35 includes feedback writeback as an operating system surface -- outcomes become durable state, but without artifact-specific retirement.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:29-60 classifies components as domain invariants or model-specific compensations before simplification or removal -- pre-retirement classification logic.
- [[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]] defines carry debt as one of three debt categories -- the sunset gate is the specific mechanism for managing carry debt at the artifact level.

### What is missing from the pattern

The classification marks Carry Debt Sunset Gate as Partial Coverage because the repo has the lifecycle mechanics for harness components but lacks artifact-level inventory with expiration dates, named maintenance owners, and the keep/retire/archive/promote decision vocabulary applied to general agent output ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|classification]]:246-269).

Missing items:

1. Artifact-level inventory (not just harness components): what agents created, for whom, with what value hypothesis.
2. Expiration dates or review triggers per artifact: when should each artifact be re-evaluated?
3. Named maintenance owners: who is responsible for keeping, retiring, or promoting each artifact?
4. The keep/retire/archive/promote decision vocabulary applied to general agent output.
5. Shorter review cadences for prototypes and experiments (30-day) alongside the quarterly harness lifecycle.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents cheap prototypes from quietly becoming permanent production burden | Requires an accurate inventory of what agents created or changed |
| Keeps long-running agent output aligned with owned, maintained assets | Retirement can be politically difficult after stakeholders become attached |
| Makes deletion and archival normal parts of the agentic workflow | Some artifacts reveal value only after a longer observation window |
| Reuses the proven lifecycle mechanics from harness component governance | Adding artifact metadata (owner, value hypothesis, expiration) is manual overhead |
| Provides an explicit promotion path for agent-created artifacts that earn sustained value | The inventory itself must be maintained, creating a meta-carry-debt risk |

## Relationship to Other Patterns

- **[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]** -- the pattern this sunset gate extends from harness components to general agent artifacts. The lifecycle states, ROI gating, archive mechanism, and One In One Out rule are directly reused.
- **[[docs/canonical/deferred-ledger-agentic-work|Deferred Ledger for Agentic Work]]** -- carry debt is one of the three debt categories in the deferred ledger. The sunset gate is the operational mechanism for tracking and resolving carry debt at the artifact level.
- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake gate prevents artifacts from entering the carry-debt pipeline by stopping low-value builds before creation. The sunset gate manages artifacts that were created despite the gate.
- **[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]** -- the value gate's experiment classification is the entry point to the sunset gate. Experiments enter the artifact inventory with a short expiration and explicit stop criteria.
- **[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]** -- the weekly GC Day cadence is the natural home for artifact review. Sunset gate candidates are reviewed during GC Day sessions.
- **[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]** -- classifies artifacts before retirement: invariants should be promoted; compensations should be retired when the model improves.
- **[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]]** -- the OS feedback writeback surface is where artifact state changes (created, promoted, retired) are recorded as durable operating system events.

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]:37 -- source description of carry debt
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]:259-283 -- extracted pattern structure
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]:246-269 -- classification evidence and gap analysis
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:106 -- cheap today is not cheap forever
