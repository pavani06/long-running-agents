---
title: "Deferred Ledger for Agentic Work"
type: canonical
tags: ["agentes-orquestracao", "governanca", "decision-discipline", "production", "harness-engineering"]
aliases: ["deferred ledger", "agentic debt ledger", "three debts model", "skill debt", "dependence debt", "carry debt", "deferred cost ledger"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]", "[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
---

# Deferred Ledger for Agentic Work

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-trap-spec-driven-development-is-setting/
**Classification:** Missing, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Agentic workflows accumulate hidden structural debts while token prices and generation costs are artificially cheap. These debts do not appear in the current quarter's budget, and that is precisely why they are dangerous. The source identifies three categories of deferred debt: Skill Debt (judgment atrophy from never exercising build-or-dont-build decisions), Dependence Debt (workflows built on the assumption of free, correct generation that break silently when generation degrades or reprices), and Carry Debt (agent-created software that becomes permanent production inventory -- maintained, secured, and eventually repriced at true cost).

The repo tracks token costs extensively through the Explicit Token Budget Ledger, Burn Rate Runtime Forecast, and Phase-Gated Token Health Monitor, but cost tracking is operational, not strategic. It tells you how much you are spending; it does not tell you what structural risk you are accumulating. The source analysis frames this as a risk framework, not a bookkeeping exercise: "O Deferred Ledger e um framework de risco, nao de contabilidade -- as tres dividas nao sao itens de budget -- sao mudancas estruturais na organizacao que se tornam irreversiveis antes de serem visiveis" ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:173).

## Solution

Maintain a strategic ledger that classifies agentic debt into three categories and tracks exposure over time. The ledger sits above the operational cost tracking layer and provides a risk view that answers: what breaks when generation becomes expensive, degraded, or unavailable?

**The three debt categories:**

| Debt | What it is | What it costs when activated | Activation trigger |
|---|---|---|---|
| Skill Debt | Judgment not exercised does not survive. A team that spent a year without taking a hard build-or-dont-build decision cannot make one in the quarter it matters. The hard part -- deciding what is worth building -- is exactly the part being skipped. | Loss of institutional ability to evaluate value before construction; decisions become pattern-matching rather than judgment | Repricing forces cost-based prioritization; organization cannot triage effectively |
| Dependence Debt | Every workflow built on the premise that generation is free and correct stops working when generation is not. It is not a tool adoption; it is moving weight to a load-bearing dependency. Worse than an outage (which is visible): failure can be silent and subtle for weeks. | Silent degradation producing plausible but wrong outputs; teams shipping against a broken instrument | Model degradation, rate limiting, API changes, or repricing that throttles access |
| Carry Debt | Software built without need does not become free because it was cheap to make. It becomes inventory: maintained, secured, understood, and accounted for over its lifetime, repriced upward when access costs normalize. | Maintenance burden, security surface area, operational cost, and cognitive load from artifacts with no users | Artifact ages without ownership review; security vulnerability; dependency upgrade breaks unmaintained code |

**Ledger mechanics:**

1. **Classification on creation.** When an agent produces an artifact, a task, or a workflow dependency, classify what debt categories it contributes to: Is it building a skill gap (someone should have judged this)? Is it creating a dependence (workflow now assumes correct generation)? Is it creating carry (artifact enters production inventory)?

2. **Periodic exposure review.** On a defined cadence (weekly or per-iteration), review the ledger and ask: what is our exposure in each category? What changed since last review? What is the repricing sensitivity -- how much of our workflow breaks if generation cost doubles, quality degrades 20%, or the API changes?

3. **Mitigation decisions.** For each exposure, decide: stop (freeze building in high-exposure areas), simplify (reduce dependency surface), retire (archive artifacts with no users), rehearse judgment (explicit build/dont-build exercises to maintain skill), or monitor (continue with explicit thresholds).

4. **Integration with cost telemetry.** The ledger consumes data from the operational cost layer: token budgets from [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]], burn-rate projections from [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]], and health phases from [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]. These feed the exposure calculation; the ledger adds the risk classification on top.

**Sample ledger entry:**

| Artifact | Skill Debt | Dependence Debt | Carry Debt | Review Date | Mitigation |
|---|---|---|---|---|---|
| Agent-built dashboard for internal metrics | None (well-scoped value) | Low (reads from stable API) | Medium (needs maintenance, 2 users) | 2026-09-11 | Review adoption; retire if <5 users |
| Agent-generated helper library for async patterns | Low | High (used across 8 workflows) | Low | 2026-07-11 | Promote to canonical pattern or refactor out |
| Agent-built experiment parser (never shipped) | Medium (nobody evaluated whether needed) | None (not integrated) | Low (not in production) | 2026-06-25 | Archive or kill; was an experiment |

## Implementation in this repo

### What already exists

- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:29-62 maintains a per-call ledger with fixed cost, reducible cost, output reservation, safety buffer, and remaining budget -- operational cost accounting.
- [[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]:28-60 forecasts token consumption velocity and session runway -- consumption projection.
- [[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:32-55 converts budget to green/yellow/orange/red phases -- health monitoring.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:52-58 calculates ROI as (Errors Prevented * Average Error Cost) / Component Operating Cost -- component-level cost/benefit, related to carry cost but scoped to harness components.
- [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]:31-55 reviews agent misbehavior weekly -- slop cleanup, not debt classification.
- [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]:28-50 detects silent degradation by comparing eval scores against production outcomes -- detects dependence debt manifestation.

### What is missing from the pattern

The classification marks Deferred Ledger for Agentic Work as Missing because the three debt categories (skill, dependence, carry) are not present in any form -- no canonical doc, no curriculum material, not in the token-budgeting lessons ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|classification]]:150-170).

Missing items:

1. The three debt categories (skill, dependence, carry) as a named framework -- not found in `docs/canonical/`, `curriculum/`, or `.opencode/`.
2. A ledger format or tracking mechanism that classifies agent output into debt categories.
3. Periodic exposure review ritual that consumes the ledger and produces mitigation decisions.
4. Integration between the operational cost layer and the strategic debt layer.
5. Curriculum content on deferred debt as a concept (could live in Level 2 or Level 3).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Makes hidden structural risk visible before repricing or degradation exposes it | Debt estimates are approximate and need human review rather than blind automation |
| Connects cost, quality, dependency, and maintenance risk in one operating artifact | Can become bookkeeping overhead if not tied to stop or mitigation decisions |
| Treats future burden as a current workflow decision, not a budget surprise | Requires instrumentation across costs, outputs, owners, and evals |
| The repo already has the operational cost layer the ledger would consume | Classification judgment requires human attention on a recurring cadence |
| Provides a vocabulary for discussing risk that cost tracking alone cannot express | Skill debt is inherently fuzzy and resists precise quantification |

## Relationship to Other Patterns

- **[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]**, **[[docs/canonical/burn-rate-runtime-forecast|Burn Rate Runtime Forecast]]**, **[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]** -- the operational cost layer that feeds data into the deferred ledger. The ledger adds risk classification on top of cost tracking.
- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake questions prevent the debts from accumulating by stopping low-value builds before they create artifacts. The cost-proxy question ("would we still build it if it cost a week?") is a leading indicator of carry debt.
- **[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]** -- the value gate governs whether agents build; the deferred ledger tracks the structural consequences when the gate is absent or bypassed.
- **[[docs/canonical/carry-debt-sunset-gate|Carry Debt Sunset Gate]]** -- the sunset gate is the specific mechanism for managing carry debt (one of the three categories) at the artifact level with expiration dates and retirement decisions.
- **[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]** -- the quarterly lifecycle with ROI gating and removal decisions is the repo's closest existing mechanism to carry debt management, but scoped to harness components rather than general agent output.
- **[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]** -- detects dependence debt manifestation by correlating eval scores with production outcomes.

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]:31-39 -- source description of the three debts
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]:150-177 -- extracted pattern structure
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]:150-170 -- classification evidence and gap analysis
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:173 -- Deferred Ledger as risk framework, not bookkeeping
