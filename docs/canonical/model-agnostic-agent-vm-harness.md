---
title: "Model-Agnostic Agent-VM Harness"
type: canonical
tags: ["harness-engineering", "agentes-orquestracao", "production", "agentic-coding"]
aliases: ["agent vm harness", "model swap interface", "model-agnostic harness", "fleet vm harness"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]"
  - "[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]"
  - "[[docs/canonical/file-system-materialization|File-System Materialization]]"
  - "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]"
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
---

# Model-Agnostic Agent-VM Harness

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage, High integration value
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

A harness built around a specific model's weaknesses becomes the fleet's ceiling the day a step-change model lands. Kavak observed this directly: the trigger was Opus 4.5, and the response was deleting two years of working, profitable multi-agent infrastructure rather than let tuned scaffolding cap the smarter model (analysis:149, analysis:167). The root cause is compensation entanglement: components that existed only to compensate for an older model's limits keep running after the limit disappears, turning the harness into "bug surface, latency, token cost, complexity, and maintenance burden" (docs/canonical/invariant-compensation-split.md:25).

The concrete failure scenario, before/after:

- **Before:** an orchestration graph tuned to the current model's attention span and tool reliability. A new model arrives (monthly cadence). Every compensation component is now wrong in a different way. Options: rewrite the graph per model (weeks of work, fleet-wide), or cap adoption of the new model (leaving capability on the table). Kavak chose a third option: delete and rebuild.
- **After (rebuilt harness):** each agent runs in a virtual machine with memory, evals, and a CLI exposing every tool/API in the company; hundreds of thousands instantiated daily, each with a long-term goal (e.g., maximize lifetime value). Design constraint: the harness must absorb smarter models arriving monthly without rewrites (analysis:84-86). The harness is valuable precisely because it is dumb — model-agnostic by construction, it converts each model improvement into company value without rewrites (analysis:174).

The compounding framing matters: the harness is simultaneously the depreciating asset (scaffolding rots as models improve) and the compounding asset (the rebuilt VM + memory + evals layer absorbs each new model) (analysis:174).

## Solution

Package the harness as five slots, one of which is the model itself — swappable through an interface, gated by evals:

1. **Per-agent VM** — each agent instance gets an isolated execution environment with a CLI exposing every company tool/API (analysis:84-86).
2. **Persistent memory** — durable state that survives the model call and the model swap.
3. **Per-agent evals** — the acceptance test the next model must pass before it inherits the fleet.
4. **Goal slot** — the long-term objective (e.g., maximize LTV), declared independently of which model pursues it.
5. **Model-swap interface** — the model is a slot behind a uniform interface, not a woven-in assumption.

The mechanism in prose: nothing in slots 1-4 may reference a model-specific weakness. Compensations that are model-specific live in a clearly marked layer and are candidates for deletion on every model step-change, per [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] and [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]].

Concrete example — harness spec with a gated model slot:

```yaml
# agent-vm.yaml — one per agent role, model-agnostic by construction
vm:
  image: agent-base-vm        # slot 1: execution environment
  tools: full-company-cli     # every internal API exposed as CLI
memory:
  store: durable-state-v3     # slot 2: versioned durable state
  identity: per-agent-key
evals:
  suite: agent-role.evalset   # slot 3: acceptance test for any model
  threshold: 0.92
goal:
  type: maximize-ltv          # slot 4: objective, model-independent
model:                        # slot 5: swappable
  interface: uniform-chat-completion   # no model-specific params above this line
  primary: provider-a/model-x
  candidates:
    - provider-b/model-y
swap_policy:
  trigger: monthly model changelog review
  gate: candidate must pass evals.suite >= threshold on side-by-side run
  action: [switch, hold, hybrid]
```

The swap sequence: candidate model runs the eval suite side-by-side with the incumbent against the domain dataset; the mechanical switch/hold/hybrid decision follows the gate; the fleet swaps by config change, not by rewrite.

## Implementation in this repo

### What already exists

- **Model-agnostic selection layer spec:** "A model-agnostic selection layer that sits between the model and the store, serving context through a uniform interface regardless of which model, vendor, or session requests it" (docs/canonical/neutral-selection-layer.md:28).
- **Eval-gated model switching spec:** the switching decision framework is specified, but the doc itself records that "the concrete infrastructure to execute model switching — an enterprise eval dataset that tests model upgrades against domain-specific data, side-by-side comparison infrastructure, and a mechanical switching decision framework — does not exist" (docs/canonical/model-switching-architecture-enterprise-eval-gate.md:24).
- **Universal tooling substrate:** "Materialize everything into files, git, and grep: Domain logic, agent specifications, configuration, knowledge bases — if a coding agent needs to interact with it, make it a file" (docs/canonical/file-system-materialization.md:38).
- **Rot-prevention classification:** compensations that outlive their model become "bug surface, latency, token cost, complexity, and maintenance burden" (docs/canonical/invariant-compensation-split.md:25).

### What is missing

1. **A unifying canonical packaging.** The repo's own audit records vendor-independence infrastructure as "NOT_FOUND across all 85 canonical docs. The repo has philosophical alignment with vendor independence" (docs/canonical/neutral-selection-layer.md:53). No single doc binds selection layer + eval gate + file substrate + compensation hygiene into one compounding harness thesis (classification.yaml:35-40).
2. **The concrete swap infrastructure.** Eval dataset, side-by-side comparison infra, and mechanical switching framework are declared absent (docs/canonical/model-switching-architecture-enterprise-eval-gate.md:24).
3. **The goal slot as a fleet primitive.** A persistent, model-independent objective per agent role, so the model is provably the only slot that changes on a swap.
4. **Fleet-scale instantiation framing.** Hundreds of thousands of daily instantiations as the scale test the harness interface must survive (analysis:85).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Each monthly model improvement converts to company value without rewrites (analysis:86, analysis:174) | Harness is "dumb" by design: no exploitation of the current model's specific strengths |
| No harness lock-in when a step-change model lands (failure pattern documented at analysis:167) | Compensations must be classified and continually re-justified (docs/canonical/invariant-compensation-split.md:25) |
| Fleet swaps by config change, not rewrite | Per-agent VM + memory + evals multiplies infrastructure cost vs shared harness (analysis:150) |
| Evals double as the model-swap gate and the safety brake | Eval suites must exist before any swap — eval investment fronts the schedule |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] (uniform model interface), [[docs/canonical/file-system-materialization|File-System Materialization]] (universal tool substrate), [[docs/canonical/versioned-durable-agent-state|Versioned Durable Agent State]] (memory slot).
- **Validated by:** [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] (the swap gate), [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] and [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] (rot prevention and removal governance), [[docs/canonical/model-switch-driven-eval-hardening|Model-Switch-Driven Eval Hardening]] (revalidation on every switch).
- **Complements:** [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]] (the scheduling primitive inside the same VM harness), [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] (per-agent evals double as the velocity brake), [[docs/canonical/multi-provider-model-routing|Multi-Provider Model Routing]] (resilience across providers behind the same slot).

## References

- Analysis: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:84-86 (agent-VM harness), :149 (orchestration vs minimal harness tradeoff), :167 (harness lock-in failure), :174 (depreciating and compounding asset synthesis)
- Classification evidence: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:11-40 (pattern entry, evidence quotes, integration value High)
- Cited canonical docs (quotes as recorded in the classification YAML): docs/canonical/neutral-selection-layer.md:28, :53; docs/canonical/model-switching-architecture-enterprise-eval-gate.md:24; docs/canonical/file-system-materialization.md:38; docs/canonical/invariant-compensation-split.md:25
- Source: Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md (a16z, video_id n34CIw3gk1k, 2026-08-10)
