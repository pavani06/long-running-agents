---
title: "Closed-Loop Help API (Humans Serve Agents)"
type: canonical
aliases: ["help API", "humans serve agents", "closed-loop escalation", "agent help endpoint"]
tags: ["agentes-orquestracao", "production", "harness-engineering"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]"
  - "[[docs/canonical/operator-channel-authority|Operator Channel Authority]]"
  - "[[docs/canonical/shared-fleet-learning|Shared Fleet Learning]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
---

# Closed-Loop Help API (Humans Serve Agents)

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

The standard escalation pattern (agent stuck → hand off to a tier-2 human queue → case forgotten) never closes the loop and generates no training data, so the system plateaus (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:186`).

Concrete scenario: a financing agent hits an ambiguous income-verification case, packages context, and escalates to the tier-2 queue. A human resolves it — by taking over the case. The customer is served, but: the resolution never returns to the agent that asked (so the same blocker recurs tomorrow), and the resolution is never captured as training data (so the fleet never learns it). The failure is named in the repository's own failure-pattern vocabulary as open-loop escalation: "agent hands off to a human queue and forgets → no improvement data → system plateaus" (`docs/analysis/...-analysis.md:164`).

Root cause: escalation is **terminal** — ownership transfers to the human and the loop ends there. The repository's canonical escalation has exactly this shape: the ladder "escalates to a human with summarized context when automated recovery is insufficient, logs the outcome" (`docs/canonical/tested-degradation-ladder.md:29`), but nothing returns a resolution to the calling agent. Kavak's inversion: the stuck agent calls a help API; a human answers on the other side; the resolution flows back into the agent that asked (`docs/analysis/...-analysis.md:96`). In org-chart terms, human teams that serve an agent outperform the reverse arrangement (`docs/analysis/...-analysis.md:96`).

## Solution

Expose a **help API the agent calls when stuck**, staff the other side with humans, and make the contract triadic: the resolution returns to the calling agent (which continues the task), the interaction is recorded as training data, and the fix may propagate fleet-wide (`docs/analysis/...-patterns.yaml:208-214`).

Concrete example — the API contract:

```yaml
# Agent side: the blocker becomes a synchronous question, not a handoff
- POST /v1/help
  body:
    agent_id: "customer-agent/MX-198.244.11"
    task_digest: "close financing, day 12 of 45"
    blocker: "income verification: two employers, non-matching payslips"
    attempted: ["ocr_recheck", "bureau_lookup", "conservative_pricing"]
  response:
    ticket_id: "help-8841"
    eta: "00:04:00"          # humans on the agent's schedule, not a batch queue

# Human side: resolve WITH the agent, not INSTEAD of it
- PATCH /v1/help/help-8841
  body:
    resolution_note: "employers merge confirmed; use payslip B + letter"
    corrected_next_action: "proceed_underwriting(payslip=B, letter=attached)"
    reusable: true            # routes to fleet propagation
  effect:
    - resolution injected into the calling agent -> task continues
    - interaction logged as training data (eval case + on-policy trace)
    - if reusable: fleet-level skill/policy update by next day
```

Two load-bearing details: humans must be "available on the agent's schedule, not a batch queue" (`docs/analysis/...-patterns.yaml:201`), and the pattern is only worth it "where the returned resolution can actually be captured as data" (`docs/analysis/...-patterns.yaml:202`).

## Implementation in this repo

### What already exists

- `docs/canonical/tested-degradation-ladder.md:29` — escalation rung exists: "escalates to a human with summarized context when automated recovery is insufficient, logs the outcome, and tests each rung before production reliance."
- `docs/canonical/tested-degradation-ladder.md:65` — "The final rung must turn real failures into durable eval or regression coverage, because production failures should become regression cases" — the failure-to-training-data conversion half exists.
- `docs/canonical/operator-channel-authority.md:73` — "Genuine escalation still exists ... but it flows *to* the operator's channel for a decision" — escalation as a decision request, the closest repository analogue of the help call.
- `docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-classification.md:135` — "`docs/canonical/multi-model-evaluation-council.md:37` through `docs/canonical/multi-model-evaluation-council.md:45` defines retry, needs-human, disagreement escalation, and human review routing" — needs-human routing already exists in the council.

### What is missing

From the classification justification (`docs/analysis/...-classification.yaml:210-216`), the inversion that defines the pattern:

1. **A help API the agent calls when stuck** — the repository's escalation is a rung inside a degradation ladder, not an on-demand endpoint the agent invokes mid-task.
2. **The resolution flowing back into the agent that asked so it continues the task** — no mechanism returns a resolution to the calling agent; the repo's escalation is terminal (human takes over the case).
3. **The humans-serve-agents organizational topology** — human teams structured around agent demand (agent's schedule, not batch queue) rather than agents structured around human queues.

Useful enrichment overlapping the flywheel's training-data capture (`docs/analysis/...-classification.yaml:216`).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Closes the loop that open-loop escalation leaves open (`docs/analysis/...-patterns.yaml:196`) | Restructures human work around agent demand (`docs/analysis/...-patterns.yaml:200`) |
| Every stuck moment becomes a learning signal (`docs/analysis/...-patterns.yaml:197`) | Requires humans available on the agent's schedule, not a batch queue (`docs/analysis/...-patterns.yaml:201`) |
| Human teams serving agents outperform the reverse arrangement (`docs/analysis/...-patterns.yaml:198`; `docs/analysis/...-analysis.md:151`) | Only worth it where the returned resolution can actually be captured as data (`docs/analysis/...-patterns.yaml:202`) |
| Tier-2 escalation loses the learning signal; the help-API inversion generates closed-loop data (`docs/analysis/...-analysis.md:151`) | The org-chart inversion is a management change, not just an API |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]] — the escalation rung supplies the transport (summarized context, outcome logging, tested rungs) the help API rides on.
- **Validated by:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — every recorded resolution must land as a regression case or the loop silently reopens.
- **Complements:** [[docs/canonical/shared-fleet-learning|Shared Fleet Learning]] — reusable resolutions propagate fleet-wide by the next day; the help API is a first-class capture source.
- **Complements:** [[docs/canonical/operator-channel-authority|Operator Channel Authority]] — both keep escalation flowing *to* a decision-maker; this pattern adds the return path the operator channel lacks.
- **Contrasts:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — needs-human routing among model reviewers; here the caller is the production agent itself.

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:94-96` — closed-loop human-in-the-loop pattern, the "I need help" API inversion.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:151,164` — escalation-vs-service tradeoff; open-loop escalation failure pattern.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:176` — synthesis: the inversion pattern (humans serve agents) as a cross-cutting theme.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:185-214` — components/flow/limitations.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:191-216` — Partial Coverage (Medium) classification with the evidence cited above.
- Source: a16z interview, channel and video_id per `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md:5-8`.
