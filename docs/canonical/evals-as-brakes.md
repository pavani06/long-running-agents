---
title: "Evals-as-Brakes"
type: canonical
tags: ["evals", "governanca", "testes-qa", "decision-discipline"]
aliases: ["evals as brakes", "velocity eval coupling", "brakes not slower", "eval-gated speed"]
last_updated: 2026-08-30
relates-to:
  - "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]"
  - "[[docs/canonical/accidental-brake-replacement|Accidental Brake Replacement]]"
  - "[[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]]"
  - "[[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]]"
  - "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"
  - "[[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]]"
  - "[[docs/canonical/mega-expert-consolidation|Mega-Expert Consolidation]]"
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
sources:
  - "[[docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis|Kavak Playbook Analysis]]"
---

# Evals-as-Brakes

**Type:** Canonical Pattern
**Status:** Active
**Source:** a16z Kavak interview (video_id n34CIw3gk1k)
**Classification:** Partial Coverage, High integration value
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Organizations respond to AI risk with the wrong dial: they slow down. "Treating AI risk by throttling velocity instead of building eval capacity — the wrong inversion of the speed/brakes relationship" (analysis:161). Companies that go slow do so because they lack brakes (evals), not because slowness is safe (analysis:145).

The complementary failure is brake removal without replacement. "The danger is that an executive mandate to 'move faster' or 'remove bureaucracy' can eliminate the last remaining mechanism that prevents unchecked agentic construction, without anyone realizing what function it was serving" (docs/canonical/accidental-brake-replacement.md:23). Both failures share one root cause: **shipping velocity and safety are treated as independent dials**, so the only visible way to buy safety is to pay in speed — permanently.

Concrete scenario, before/after:

- **Before:** an agent team ships behind a manual review queue. After an incident, leadership mandates a 2-week cooling period per agent change. Velocity halves. Quality does not measurably improve — the queue was never instrumented to catch the failure class that caused the incident. The tension is named but unresolved: "Agent improvement cycles face a tension between velocity and safety" (docs/canonical/confidence-gated-continual-learning.md:24).
- **After:** the cooling period is replaced by an eval-coverage rule. Speed becomes an output of brake quality, not a bargaining chip.

## Solution

Make the coupling explicit: **permitted shipping velocity is a function of eval quality and coverage.** The governing maxim from the source: "You only hit the gas if you have the right brakes" — and the correct response to AI risk is building better brakes (evals), not going slower (analysis:34-35).

The mechanism in prose: define discrete velocity tiers and discrete eval-coverage tiers, and bind them in policy. Raising shipping speed is then only possible by investing in evals — the investment is the unlock, and the risk response is always "improve the brakes," never "permanently slow down."

Concrete example — velocity/coverage coupling table plus policy snippet:

| Eval state (brakes) | Permitted velocity (gas) |
|---|---|
| Full suite green + production-correlation tracked | Auto-merge; deploy on merge |
| Stratified CI subset green; full suite on schedule | Daily deploy batch |
| New surface with thin eval coverage | Manual gate per change |
| Eval failing or eval-to-production correlation broken | Stop; fix brakes first |

```yaml
# velocity-policy.yaml — speed as a function of brake quality
velocity_tiers:
  - name: auto-merge
    requires:
      eval_coverage: ">= 0.9 of changed behaviors"
      gates: [pr-eval-report, merge-threshold]
      correlation: "eval score predicts production outcome"
  - name: daily-batch
    requires:
      eval_coverage: ">= 0.6"
      gates: [stratified-ci]
  - name: manual-gate
    requires: {}          # default floor: nothing ships without a human
risk_response:
  on_incident: "add eval case + raise coverage"   # improve brakes
  never: "reduce velocity tier permanently without eval justification"
```

The enforcement hooks already exist as patterns: require eval-specific reports on PRs touching agent behavior — "prompt, model, tool, context, memory, scoring, or agent-loop behavior" (docs/canonical/pr-gated-eval-enforcement.md:28) — and "Block merge when thresholds fail unless an explicit waiver is recorded" (docs/canonical/pr-gated-eval-enforcement.md:51). The same evals can be intentional replacements for removed bureaucratic brakes: "Security review (takes 1 week) | Prevents vulnerable code from shipping | PR-Gated Eval Enforcement + automated security scanning at PR time" (docs/canonical/accidental-brake-replacement.md:50).

## Implementation in this repo

### What already exists

- **The brakes half, at canonical depth:** eval-gated merges (docs/canonical/pr-gated-eval-enforcement.md:28, :51).
- **Organizational brakes vocabulary:** accidental-brake replacement mapping (docs/canonical/accidental-brake-replacement.md:23, :50) — slow bureaucratic brakes mapped to eval-based intentional replacements.
- **The named tension:** "Agent improvement cycles face a tension between velocity and safety" (docs/canonical/confidence-gated-continual-learning.md:24).
- **Sequencing discipline:** evals built first, not last — "Invest 6 weeks in evaluation infrastructure before any model experimentation or selection" (docs/canonical/eval-driven-development-timeline.md:28); eval capability approved only against observed pain (docs/canonical/pain-signal-eval-progression-gate.md:28).

### What is missing

1. **The coupling rule.** Nothing in the repo states that permitted shipping velocity is set as a function of eval quality/coverage. Repo audit: "NOT_FOUND for the coupling rule: searched docs/canonical/ and docs/system-of-record.md with 'velocity|shipping speed|go faster|go slow' — only token-burn velocity (burn-rate-runtime-forecast.md:31,49) and the confidence-gate tension (confidence-gated-continual-learning.md:24)" (classification.yaml:257-260).
2. **The response-to-risk reframe.** The rule that an incident's correct response is "improve the brakes" rather than a permanent velocity reduction. The failure pattern "slowing down as risk response" is absent as a named anti-pattern (analysis:161 is source-side only).
3. **A velocity-tier ladder artifact.** No doc binds eval-coverage tiers to deployment-velocity tiers as a single policy object.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Speed is purchased with eval investment, a compounding asset, instead of traded against safety | Eval parity roughly halves effective builder capacity (analysis:145) |
| Risk response always strengthens the system (new eval cases) instead of taxing it (cooling periods) | The coupling must be enforced; an org can decouple it by decree, recreating analysis:161 |
| Composes with existing gates — PR eval reports and merge blocking are already specified (docs/canonical/pr-gated-eval-enforcement.md:28, :51) | Velocity tiers add a policy surface that itself needs governance against brake removal (docs/canonical/accidental-brake-replacement.md:23) |
| Evals serve double duty as model-swap gates in the harness, so brake investment compounds | Coverage measurement over "changed behaviors" is approximate; a bad coverage metric becomes a false green light |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] (the mechanical brake), [[docs/canonical/living-eval-dataset|Living Eval Dataset]] and [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] (brake quality must be proven, not assumed).
- **Validated by:** [[docs/canonical/eval-driven-development-timeline|Eval-Driven Development Timeline]] (brakes exist before the gas), [[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]] (brake investment sized by observed pain).
- **Complements:** [[docs/canonical/accidental-brake-replacement|Accidental Brake Replacement]] (bureaucratic brakes replaced by these intentional ones), [[docs/canonical/confidence-gated-continual-learning|Confidence-Gated Continual Learning]] (the velocity/safety tension this pattern resolves), [[docs/canonical/model-agnostic-agent-vm-harness|Model-Agnostic Agent-VM Harness]] (per-agent evals double as swap gates and brakes), [[docs/canonical/mega-expert-consolidation|Mega-Expert Consolidation]] (benchmarking against the best human requires the eval brakes to be trustworthy).

## References

- Analysis: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-analysis.md:33-35 (evals-as-brakes model), :145 (speed vs safety tradeoff), :161-162 (slowing-down and afterthought failure patterns), :175 (evals as the currency converting capability into velocity)
- Classification evidence: docs/analysis/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai-classification.yaml:230-260 (pattern entry, evidence quotes, integration value High, NOT_FOUND searches)
- Cited canonical docs (quotes as recorded in the classification YAML): docs/canonical/pr-gated-eval-enforcement.md:28, :51; docs/canonical/accidental-brake-replacement.md:23, :50; docs/canonical/confidence-gated-continual-learning.md:24
- Source: Raw-Knowledge/sources/2026-08-30-kavak-s-playbook-for-rebuilding-a-company-around-ai.md (a16z, video_id n34CIw3gk1k, 2026-08-10)
