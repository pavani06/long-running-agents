---
title: "Mega-Expert Consolidation"
type: canonical
tags: ["agentes-orquestracao", "harness-engineering", "evals", "agentic-coding"]
aliases: ["mega expert", "specialist agent fusion", "superhuman specialist benchmark", "best-human bar"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/persona-based-documentation|Persona-Based Documentation]]"
  - "[[docs/canonical/goal-atomicity-split|Goal-Atomicity Split]]"
  - "[[docs/canonical/multi-agent-fault-tolerance|Multi-Agent Fault Tolerance]]"
  - "[[docs/canonical/generator-evaluator|Generator-Evaluator]]"
  - "[[docs/canonical/evals-as-brakes|Evals-as-Brakes]]"
  - "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
---

# Mega-Expert Consolidation

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Missing (integration value: Medium)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

A specialty-siloed organization hands the customer across teams: "The old org required ~15 specialists in 15 teams (financing, car advisory, buying, insurance, trade-in quoting)" (analysis:88). Each handoff drops context, and no one owns the whole outcome.

When such an org "adopts agents," the default build mirrors the org chart: one deflection bot per department, each held to a "good enough" bar on easy problems. The source frames this as the wrong bar entirely: the bet is on "superhuman agents — the bar is outperforming the best human ever hired on every dimension that matters" (analysis:27), and the tradeoff is explicit — "targeting 'better than the best human ever hired' on hard problems, rather than 'good enough' on easy problems, changes what architectures you build (mega-expert vs. deflection bot)" (analysis:148).

Root cause: the org never (a) held any single specialty to a best-individual-human benchmark, nor (b) designed the fusion step that turns per-specialty superiority into one customer-facing expert. Without (b), even excellent specialist agents reproduce the handoff problem in software.

## Solution

Two-phase consolidation, each phase gated by a benchmark:

**Phase 1 — one agent per specialty, benchmarked against the best individual human.** "First build an agent that beats each individual expert" (analysis:89). The benchmark population is the top performer in that specialty, not the median: financing-agent vs. the best underwriter ever hired; advisory-agent vs. the best car advisor. Each specialty agent is validated on its own eval suite constructed around that bar. This is where [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] and [[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]] supply the gate.

**Phase 2 — fuse the specialists into a single customer-facing mega expert.** "Then fuse them into a single 'mega expert' that faces the customer" (analysis:89). Fusion is not an ensemble vote and not a router between chatbots: one persistent agent holds the customer relationship and invokes the validated specialists as internal capabilities, so the customer experiences one expert with all fifteen competencies and complete context.

Concrete example — fusion config:

```yaml
# mega-expert.yaml — one customer-facing agent, specialists as capabilities
customer_facing:
  name: kavak-mega-expert
  owns: [relationship, complete-context, outcome]
  benchmark: "best human ever hired, every dimension that matters"
capabilities:            # phase-1 specialists, each already beating its best human
  - financing-underwriting
  - car-advisory
  - buying-negotiation
  - insurance-quoting
  - trade-in-valuation
invocation: internal-tool-call    # specialists are tools behind the mega-expert,
                                  # never customer-facing handoffs
context: shared-per-customer-memory
upgrade_path:
  per_specialty: re-benchmark when specialty evals or models change
  fusion: re-benchmark the mega-expert on end-to-end outcome metrics
```

The key distinction from a dense mega-prompt: the repo already rejects scaling by monolithic prompting — "Scales agent work by decomposition instead of by dense mega-prompts -- one outcome per intent" (docs/canonical/goal-atomicity-split.md:92). Here decomposition happens inside the fusion: specialties remain separate evaluable units; consolidation happens at the customer interface, not in the prompt.

## Implementation in this repo

### What already exists

Only adjacent-but-different surfaces; the pattern itself is NOT_FOUND:

- **Specialist knowledge capture as documentation:** "When a team has specialists in different domains, their expertise is not systematically captured in durable documentation surfaces that agents can load" (docs/canonical/persona-based-documentation.md:23). This captures specialist knowledge as docs — it does not build nor fuse specialist agents.
- **Anti-mega-prompt decomposition:** goal decomposition as the scaling axis (docs/canonical/goal-atomicity-split.md:92) — fusion must respect this boundary (consolidate at the interface, not in the prompt).

### What is missing

This doc fills the following numbered gaps — the classification records the pattern as NOT_FOUND in any form (doc, code, skill, or curriculum; classification.yaml:326-327):

1. **The best-individual-human benchmark as a build gate.** No canonical doc sets "one agent per specialty benchmarked against the best individual human" as the acceptance bar. Searches for `mega|specialist|superhuman|best human|deflection bot|fusion|consolidat|generalist` matched only the Kavak source package, the anti-pattern "dense mega-prompts" in goal-atomicity-split.md:92, and persona-based-documentation.md:23 (classification.yaml:328-331).
2. **The fusion mechanism.** No doc describes merging validated specialist agents into a single customer-facing agent. The active-canonical table has no consolidation/fusion entry (docs/system-of-record.md:172-299, per classification.yaml:331-332); curriculum has no mega-expert or specialist-fusion content (classification.yaml:332-333).
3. **The superhuman-bar-as-architecture-selector rule.** The explicit claim that the benchmark bar (best human vs. good enough) determines the architecture (mega-expert vs. deflection bot; analysis:148) is source-side only.

Adjacent-but-different concepts confirmed distinct: [[docs/canonical/multi-agent-fault-tolerance|Multi-Agent Fault Tolerance]] is orchestration reliability, not fusion; [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] is separate rubrics, not specialist consolidation (classification.yaml:334-335).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Customer experiences one expert with total context; handoff drops eliminated (analysis:88-89) | Phase 1 must clear a best-human bar per specialty — the most expensive benchmark in the org |
| Bar changes the architecture: mega-expert instead of deflection bot (analysis:148) | Fusion re-benchmarking on every model or eval change compounds phase-1 costs |
| Specialists stay separately evaluable and swappable behind the interface | One customer-facing agent becomes a single point of behavioral failure — needs multi-agent fault tolerance behind it |
| Decomposition discipline preserved (docs/canonical/goal-atomicity-split.md:92) | Fusion agent's context must host fifteen competencies without mega-prompt collapse |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/business-outcome-first-eval-pipeline|Business-Outcome-First Eval Pipeline]] and [[docs/canonical/evals-as-brakes|Evals-as-Brakes]] (the best-human benchmark is the eval gate), [[docs/canonical/persona-based-documentation|Persona-Based Documentation]] (specialist expertise must be captured before it can be exceeded), [[docs/canonical/auth-coupled-memory-architecture|Auth-Coupled Memory Architecture]] (the mega-expert's per-customer context).
- **Validated by:** [[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]] (the bar is only provable against real customer trajectories, per analysis:125), [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] (divergence policy when specialty evals disagree).
- **Complements:** [[docs/canonical/multi-agent-fault-tolerance|Multi-Agent Fault Tolerance]] (reliability layer behind the fused interface), [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] (specialists swap models without rewriting the fusion), [[docs/canonical/generator-evaluator|Generator-Evaluator]] (evaluation separation per specialty).

## References

- Analysis: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:88-89 (mega-expert consolidation), :26-28 (superhuman bet), :125 (production contact as the teacher), :148 (superhuman bar vs incremental automation)
- Classification evidence: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:315-335 (pattern entry: Missing, integration value Medium; NOT_FOUND searches; adjacent-but-different concepts)
- Cited canonical docs (quotes as recorded in the classification YAML): docs/canonical/persona-based-documentation.md:23; docs/canonical/goal-atomicity-split.md:92
- Source: Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md (a16z, video_id n34CIw3gk1k, 2026-08-10)
