---
title: "Eval-Investment Parity"
type: canonical
aliases: ["eval parity", "50/50 eval budget", "evals first-class artifact", "equal eval investment"]
tags: ["evals", "harness-engineering", "governanca"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]]"
  - "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"
  - "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]"
  - "[[docs/canonical/outcome-level-eval-hierarchy|Outcome-Level Eval Hierarchy]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
---

# Eval-Investment Parity

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Evals treated as an afterthought cap the scale and speed an agent fleet can safely reach (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:272`).

Concrete scenario: a team of ten engineers spends a quarter building agent capabilities; eval work is squeezed into the last sprint, hand-picked, and manual. The fleet grows to dozens of agents and every deployment becomes a leap of faith — rollback cycles lengthen, velocity drops, and eventually the organization "goes slow" out of fear. The repository names the terminal form of this: "Evals as afterthought: getting to scale requires evals designed with the agent, not bolted on post-deployment; deferring them caps achievable speed" (`docs/analysis/...-analysis.md:162`). At Kavak's scale — 100,000–200,000 agents instantiated daily (`docs/analysis/...-analysis.md:73`) — post-hoc evals are arithmetically impossible.

Root cause: **budget allocation treats evals as overhead** rather than as a co-equal build track. The Kavak rule: roughly equal engineering time, tokens, and money spent building evals as building the agents themselves — evals as a first-class artifact, not an afterthought (`docs/analysis/...-analysis.md:108-109`).

## Solution

Run two parallel build tracks — agent build and eval build — under a **parity budget rule** across engineering time, tokens, and money, with deployment gated on eval results (`docs/analysis/...-patterns.yaml:286-295`).

Concrete example — sprint allocation under the parity rule:

```yaml
# sprint-budget.yaml — the parity rule as an explicit, accepted allocation
parity_rule: "eval_track ~= agent_track"        # time, tokens, AND money
allocation:
  engineering_time: { agents: 50%, evals: 50% }
  tokens:            { agents: 50%, evals: 50% }
  money:             { agents: "~50%", evals: "~50%" }
tracks:
  agent_build: [harness, skills, memory, deployment]
  eval_build:  [cases, judges, regression suite, dashboards]  # co-designed, same sprints
gate:
  deploy: only when eval track passes            # parity without the gate is theater
cadence: sustained every sprint, not a one-time allocation
```

The parity rule is the capacity decision that makes the gas/brakes coupling enforceable: "you only hit the gas if you have the right brakes" (`docs/analysis/...-analysis.md:34`), and accepting parity means accepting that effective builder capacity is halved — as an explicit decision rather than silent neglect (`docs/analysis/...-patterns.yaml:282`).

**Tension with this repository's philosophy (stated, not hidden):** the repo's eval investment is deliberately gated by pain signals, not by proportion — "Treat eval maturity as a gate driven by pain signals instead of a calendar roadmap" (`docs/canonical/pain-signal-eval-progression-gate.md:28`) and "Approve only the smallest eval capability that addresses the observed pain" (`docs/canonical/pain-signal-eval-progression-gate.md:36`). Parity is a fleet-scale rule (100k+ agents); pain-signal gating is a pre-scale rule. The reconciliation: pain-signal gating governs *which* eval capability to build next; parity governs *aggregate allocation* once contact with production is the norm.

## Implementation in this repo

### What already exists

- `docs/canonical/eval-driven-development-timeline.md:28` — "Invest 6 weeks in evaluation infrastructure before any model experimentation or selection. The timeline is deliberately inverted from conventional development: evaluation is the first thing built, not the last." Evals as first-class build artifact, sequenced first.
- `docs/canonical/pain-signal-eval-progression-gate.md:28` — eval maturity driven by pain signals instead of a calendar roadmap: the repository's own investment philosophy for eval capability.
- `docs/canonical/pain-signal-eval-progression-gate.md:36` — "Approve only the smallest eval capability that addresses the observed pain": the deliberate counter-rule to proportional allocation.
- Classification evidence additionally records the surrounding depth: Living Eval Dataset, Eval Tier Stratification, and the full evals cluster as co-designed artifacts (`docs/analysis/...-classification.yaml:276-277`).

### What is missing

From the classification justification (`docs/analysis/...-classification.yaml:276-283`):

1. **The parity rule itself** — a ~50/50 split of time/tokens/money between agents and evals appears nowhere; NOT_FOUND by the classification's own search (`parity|50/50|50%` matched only fixture parity in `eval-tier-stratification.md:57` and unrelated mock parity).
2. **A budget-level allocation mechanism** — no canonical doc treats eval investment as a *capacity allocation decision* (engineering time, tokens, money) rather than a capability-progression decision.
3. **The explicit reconciliation with pain-signal gating** — the two rules coexist unresolved; a doc must state when proportional parity applies versus smallest-sufficient capability.

## Tradeoffs

| Benefit | Cost |
|--- |--- |
| Unlocks scale: getting to hundreds of thousands of agents requires evals designed with the agent (`docs/analysis/...-patterns.yaml:280`) | Halves effective builder capacity; leadership must accept 50% non-product spend (`docs/analysis/...-patterns.yaml:284`) |
| Makes speed safe — feeds the gas/brakes coupling (`docs/analysis/...-patterns.yaml:281`) | Requires sustained discipline, not a one-time allocation (`docs/analysis/...-patterns.yaml:285`) |
| Parity as explicit decision rather than silent neglect (`docs/analysis/...-patterns.yaml:282`) | Conflicts with pain-signal gating's smallest-sufficient mandate unless scoped to fleet scale |
| Evals co-designed catch failures post-hoc evals structurally miss (`docs/analysis/...-analysis.md:162`) | Half the team experiences "no shipped features" on the eval track — morale cost the org must absorb |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]] — parity presupposes the eval-first sequence; a team that builds evals last cannot allocate parity sprints.
- **Validated by:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — the merge gate is what converts parity spend into enforced safety; without it the eval track is instrumentation without consequence.
- **Complements:** [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] — governs *what* to build next within the eval track; parity governs the *size* of the track (tension stated above).
- **Complements:** [[docs/canonical/outcome-level-eval-hierarchy|Outcome-Level Eval Hierarchy]] — anchors what the parity-funded evals measure, so the budget buys truth rather than volume.
- **Complements:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — the fast/medium/deep suites are what the eval track's 50% actually constructs.

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:108-109` — the parity rule: roughly equal time, tokens, money on evals as on agents.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:34,145,162` — gas/brakes coupling, halved builder capacity, evals-as-afterthought failure.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:271-295` — components/flow/limitations.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:261-283` — Partial Coverage (Medium) classification with the evidence cited above.
- Source: a16z interview, channel and video_id per `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md:5-8`.
