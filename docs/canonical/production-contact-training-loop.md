---
title: "Production-Contact Training Loop"
type: canonical
aliases: ["production contact loop", "agents taught by exposure", "real-customer training", "on-policy production convergence"]
tags: ["evals", "agentes-orquestracao", "production", "harness-engineering"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]]"
  - "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]"
  - "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]"
  - "[[docs/canonical/shared-fleet-learning|Shared Fleet Learning]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis (2026-08-30)]]"
---

# Production-Contact Training Loop

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Lab-only agents do not converge; synthetic or historical data cannot substitute for real interaction distributions (`docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:351`).

Concrete scenario: a team perfects an agent offline — curated scripts, historical transcripts, golden dialogues. It ships to production and immediately wobbles: real customers interrupt, change language mid-sentence, ask two things at once, and hit tool states that never appeared in the static data. The repository states the mechanism precisely: "An agent trained and evaluated only on curated scripts breaks when its own production trajectories contain early mistakes, strange tool outputs, or context drift that never appeared in the static data" (`docs/canonical/on-policy-rollout-feedback-loop.md:33`), and "Hand-authored eval sets miss real user distributions and long-tail agent failures" (`docs/canonical/production-grounded-eval-sampling.md:22`). The curriculum teaches the same distinction as the lab-vs-production gap: "É a diferença entre um agente que **funciona no laboratório** e um agente que **funciona em produção, com clientes reais**, por horas a fio" (`curriculum/02-nivel-2-practical-patterns/exercises/solutions/exercise-03-solution.md:2477`).

Root cause: the agent's inference distribution diverges from anything available offline. Kavak's operational stance: the only way to make agents work is putting them in front of real customers, harvesting the interaction data and evals, and training on that loop — lab-only agents don't converge (`docs/analysis/...-analysis.md:125`).

## Solution

Make **real-customer contact the training mechanism itself**: expose the agent to production, harvest interactions and eval signals, feed them back as updates, redeploy, repeat (`docs/analysis/...-patterns.yaml:372-377`). The identity claim: the harvested data and feedback loops are not groundwork for the agents — they ARE the agents (`docs/analysis/...-patterns.yaml:358`; `docs/analysis/...-analysis.md:178`).

Concrete example — the daily loop assembled from repository primitives:

```bash
# production-contact-loop (daily cadence)
1. expose    : agent serves real customers
               (target: 96% of interactions fully agent-handled)
2. harvest   : traces + outcomes -> production_sampled_eval_corpus
               (nivel-3-koda.md:1625 — named artifact, replay de conversas
                reais anonimizadas, privacidade e labels explícitos)
3. eval      : score the agent's own prefixes on-policy
               (on-policy-rollout-feedback-loop:41 — teacher/verifier/human signal)
4. update    : scored prefixes -> prompt rules, skills, eval cases, memory policy
5. propagate : updates reach the fleet on next instantiation
               (shared-fleet-learning: fleet learns by the next day)
6. redeploy  : loop repeats; failure modes encountered become the curriculum
```

Every production interaction becomes training material (`docs/analysis/...-patterns.yaml:362`); the loop, not the lab, is where convergence happens.

## Implementation in this repo

### What already exists

- `docs/canonical/on-policy-rollout-feedback-loop.md:33` — the exposure-bias gap named: curated scripts break against real trajectories.
- `docs/canonical/on-policy-rollout-feedback-loop.md:41` — the exact loop prescribed: "Close the exposure-bias gap by making the agent's own production trajectories the learning signal. ... Feed those scored prefixes back as update targets: prompt rules, skills, eval cases, memory policy, or training data. Then re-run the task against the updated agent and measure whether performance improved."
- `docs/canonical/production-grounded-eval-sampling.md:22` — the harvesting argument: hand-authored sets miss real distributions and long-tail failures.
- `docs/canonical/production-failure-regression-flywheel.md:28` — "Every production failure that reveals a behavioral gap should become a durable eval regression case" — failures feed the corpus.
- `docs/canonical/living-eval-dataset.md:28` — "A **monotonically growing** eval dataset: every production incident, every escaped edge case, every new feature specification becomes a permanent addition" — the corpus that grows from contact.
- `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:1625` — "O replay de conversas reais anonimizadas ... vira um artefato nomeado: `production_sampled_eval_corpus`" — the named harvesting artifact, bridging harness evolution and production.

### What is missing

From the classification justification (`docs/analysis/...-classification.yaml:369-378`):

1. **The organizational stance that real-customer contact is the precondition for agents working at all** — the on-policy doc still allows teacher-mixed/lab-side sampling for cold start, treating production contact as one option rather than the precondition.
2. **The identity reframe that the harvested data and feedback loops ARE the agents** — the repo treats harvesting as supporting infrastructure for agents; the pattern asserts the feedback loops constitute the agents themselves.
3. **An explicit exposure-risk ordering** — putting unproven agents in front of real customers requires evals-as-brakes first (`docs/analysis/...-patterns.yaml:364`); the repo has no rule sequencing brake-building before exposure.

## Tradeoffs

| Benefit | Cost |
|---|---|
| The only mechanism observed to make agents work at all (`docs/analysis/...-patterns.yaml:360`) | Real-customer exposure carries risk; requires evals as brakes first (`docs/analysis/...-patterns.yaml:364`) |
| Convergence to real customer behavior instead of lab assumptions (`docs/analysis/...-patterns.yaml:361`) | Requires data harvesting and eval infrastructure before scale (`docs/analysis/...-patterns.yaml:365`) |
| Every production interaction becomes training material (`docs/analysis/...-patterns.yaml:362`) | Failure modes encountered in production become the curriculum — customers absorb early mistakes |
| Feedback loops compound: the architecture is inseparable from its data loops (`docs/analysis/...-analysis.md:178`) | Privacy handling of real conversations is a hard prerequisite (anonymization, labels — `nivel-3-koda.md:1625`) |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/on-policy-rollout-feedback-loop|On-Policy Rollout Feedback Loop]] — supplies the convergence mechanism (scored production prefixes as update targets).
- **Depends on:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] — supplies the harvesting discipline (real distributions over hand-authored sets).
- **Validated by:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] — the monotonically growing corpus is the durable proof the loop ran.
- **Validated by:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — verifies the loop's updates actually move production outcomes.
- **Complements:** [[docs/canonical/shared-fleet-learning|Shared Fleet Learning]] — propagation distributes what this loop harvests to the whole fleet.
- **Complements:** [[docs/canonical/closed-loop-help-api|Closed-Loop Help API]] — human resolutions during production contact are a first-class capture source for the loop.

## References

- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:125` — agents are taught by exposure; lab-only agents don't converge.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:178` — synthesis: all learning requires production contact; the feedback loops are the agents.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-patterns.yaml:350-377` — components/flow/limitations.
- `docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:336-378` — Partial Coverage (Medium) classification with the evidence cited above.
- Source: a16z interview, channel and video_id per `/mnt/c/Users/pavan/Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md:5-8`.
