---
title: "Shared Fleet Learning"
type: canonical
aliases: ["fleet learning", "shared fleet learning", "fleet-wide propagation", "one mistake fleet learns"]
tags: ["agentes-orquestracao", "evals", "knowledge-management", "production", "agentic-coding"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]"
  - "[[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]]"
  - "[[docs/canonical/cross-context-knowledge-siloing|Cross-Context Knowledge Siloing]]"
  - "[[docs/canonical/closed-loop-help-api|Closed-Loop Help API]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
---

# Shared Fleet Learning

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Per-agent learning means the same mistake is repeated across ~200,000 instances; individual agents cannot benefit from each other's errors (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:158`).

Concrete scenario: agent #41,207 misprices a trade-in because it misread a VIN-region edge case. The failure becomes a regression case; the eval dataset grows. But the 199,999 sibling agents instantiated tomorrow still carry the old skill/policy and make the identical mistake — one per customer — until someone manually rewrites the shared prompt and ships it. Learning happened *about* the fleet, not *in* the fleet. The repository documents the same pathology in its own terms: "Knowledge created in one agent context becomes invisible to agents operating in a different context, causing repeated investigation of already-solved problems" (`docs/canonical/cross-context-knowledge-siloing.md:46`).

Root cause: the feedback path from a single agent's error to a **fleet-level update distributed to all running instances** does not exist. Capture is not propagation. Kavak's mechanism: when one agent makes a mistake, the entire fleet (~200k agents) learns from it by the next day — feedback propagates across instances, not per-agent (`docs/analysis/...-analysis.md:92`).

## Solution

Close the loop from **one agent's error** to **all agents' behavior** with a propagation channel: error capture at the agent level → feedback aggregation into a fleet-level skill/memory/policy update → fleet-wide distribution through the shared substrate → next-day propagation (`docs/analysis/...-patterns.yaml:174-184`).

Concrete example — a daily fleet-propagation pipeline composed from existing repository primitives plus the missing distribution step:

```bash
# fleet-propagation.service (daily, 60s-loop daemon upgrades from "surface" to "ship")
1. capture    : yesterday's production traces -> new regression cases
                (production-failure-regression-flywheel: every failure a case)
2. aggregate  : cluster cases -> fleet-level patch
                (skill edit | memory policy update | prompt rule | eval case)
3. gate       : confidence gate / human review before incorporation
                (confidence-gated-continual-learning: deploy nothing ungated)
4. distribute : ship patch to the SHARED substrate, not the instance --
                all agents pick it up on next instantiation/wake
5. verify     : re-run the triggering scenario fleet-wide; eval delta must be >= 0
```

The load-bearing property is step 4: agents run a common substrate so updates apply uniformly (`docs/analysis/...-patterns.yaml:173`); a fleet of bespoke per-agent harnesses cannot propagate anything.

## Implementation in this repo

### What already exists

- `docs/canonical/production-failure-regression-flywheel.md:28` — "Every production failure that reveals a behavioral gap should become a durable eval regression case unless it is explicitly rejected as duplicate, unactionable, or out of scope." The capture side.
- `docs/canonical/closed-loop-agent-operating-system.md:35` — "Feedback writeback | Persist decisions, traces, failures, eval results, canonical docs, and issue outcomes | Updated memory for future agents" — feedback writeback exists as an OS surface.
- `docs/canonical/confidence-gated-continual-learning.md:59` — the repo's own continual-learning canonical records that auto-update deployment is "NOT_FOUND across `docs/canonical/`, `curriculum/`, `system-of-record.md`, and `.opencode/skills/`."
- `docs/canonical/confidence-gated-continual-learning.md:64` — "The flywheel daemon (`systemd`, 60s loop) processes triggers but deploys nothing — it surfaces findings for human review." Capture without deployment, stated verbatim.
- `docs/canonical/cross-context-knowledge-siloing.md:46` — the pathology this pattern treats, already documented.

### What is missing

From the classification justification (`docs/analysis/...-classification.yaml:183-190`), the propagation channel:

1. **Aggregation into fleet-level updates** — converting one agent's mistake into a skill/memory/policy update scoped to the whole fleet, not a per-context artifact.
2. **Fleet-wide distribution to all running instances by the next day** — no mechanism ships an update to every instance; the repo's flywheel "deploys nothing" and its continual-learning canonical declares auto-update NOT_FOUND.
3. **The named propagation SLA** — "the entire fleet learns by the next day" as an explicit contract; the repository has no propagation-timing concept at all.

Substantial adjacent infrastructure already exists; a fleet-propagation doc connects existing patterns (`docs/analysis/...-classification.yaml:189-190`).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Each mistake costs the fleet only once (`docs/analysis/...-patterns.yaml:167`) | Requires a centralized feedback pipeline shared by all instances (`docs/analysis/...-patterns.yaml:171`) |
| Improvement compounds at fleet scale with every error (`docs/analysis/...-patterns.yaml:168`) | Propagation lag up to one day (`docs/analysis/...-patterns.yaml:172`) |
| Turns production failures into a training asset (`docs/analysis/...-patterns.yaml:169`) | Depends on all agents running a common substrate so updates apply uniformly (`docs/analysis/...-patterns.yaml:173`) |
| Treats cross-context siloing at the fleet level rather than per-context discovery | Ungated propagation would auto-deploy errors fleet-wide — the confidence gate is not optional |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — supplies the capture side: every failure a durable regression case.
- **Depends on:** [[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]] — supplies the incorporation gate that makes fleet-wide deployment safe.
- **Validated by:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] — the monotonically growing dataset is the audit trail proving the fleet actually learned each propagated case.
- **Complements:** [[docs/canonical/cross-context-knowledge-siloing|Cross-Context Knowledge Siloing]] — names the pathology; this pattern is the fleet-scale cure.
- **Complements:** [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]] — human resolutions captured through the help API become fleet-level updates here.

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:92` — fleet learns from one mistake by the next day.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:178` — synthesis: all learning requires production contact; fleet learning propagates per-mistake across ~200k instances.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:157-184` — components/flow/limitations.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:161-190` — Partial Coverage (Medium) classification with the evidence cited above.
- Source: a16z interview, channel and video_id per `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md:5-8`.
