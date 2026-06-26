---
title: "Model-Switch-Driven Eval Hardening"
type: canonical
status: draft
source: "LangChain Max Agency — Zack Reno Wedeen (Sierra)"
date: 2026-06-26
tags: ["evals", "agentes-orquestracao"]
aliases: ["model-switch eval hardening", "discovery-driven eval improvement", "provider-agnostic eval hardening", "switch-to-discover-eval-gaps"]
relates-to: ["[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]"]
---

# Model-Switch-Driven Eval Hardening

**Type:** canonical
**Status:** draft
**Source:** LangChain Max Agency — Zack Reno Wedeen (Sierra)
**Classification:** Partial Coverage (High)
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Eval suites designed against a single model provider develop blind spots — they test what the current model gets right but not what a different model might get wrong. If you build your eval suite by running GPT-5 on test cases and validating outputs, your evals encode the assumption that "GPT-5-like reasoning" is the correct answer. When you switch a task to Claude or Gemini, the new model might produce different outputs that are equally correct — or it might produce outputs that are wrong in ways your GPT-5-calibrated evals never anticipated.

The blind spot is structural, not operational: an eval suite validates outputs against expected behavior, but expected behavior is defined by observing a specific model's performance. The eval suite becomes a self-reinforcing loop — it tests what the current model does well and ignores what it does poorly because you never wrote tests for those failure modes.

Wedeen's insight is that switching models is the best way to expose these blind spots: "The first switch invariably reveals the eval wasn't as good as you thought." When you route a task to a new model provider, the eval suite catches some failures (the ones it was designed to catch) but misses others (the new provider's novel failure modes). Each switch reveals gaps that were invisible against the previous provider.

Rather than treating these gaps as switch failures, Sierra treats them as eval hardening opportunities. Each switch strengthens the eval suite, making future switches safer. Over time, the eval suite becomes genuinely model-agnostic — it catches failures regardless of which provider generated the output.

## Solution

Model-switch-driven eval hardening is a discovery-driven process: switch a task to a different model provider, observe where the eval suite fails to catch regressions, harden the eval suite to cover those gaps, and repeat. The process is iterative — each new provider exposes new gaps, and each gap closure improves the eval suite's model-agnostic coverage.

**Key components:**

1. **Model-agnostic eval infrastructure**: Evals must operate on the same input/output contract regardless of provider. The eval does not know or care which model generated the output — it only validates the output against expected behavior. This requires the neutral selection layer described in [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] — a provider-agnostic format where the eval expects the same structured output from any model.

2. **Switch as regression detection**: When a task is switched to a new provider, the existing eval suite runs on the new provider's outputs. Pass/fail results are compared against the previous provider's pass/fail rates. A significant increase in failures means the new provider is worse on those dimensions. But the real value is in the failures the eval *doesn't* catch — outputs that pass evals but are actually wrong in production.

3. **Gap discovery through production monitoring**: After a switch, [[docs/canonical/always-on-monitoring-human-triage|Always-On Production Monitoring]] catches failures the eval suite missed. Those failures are classified: was this a new failure mode the old provider never exhibited? If so, it becomes a new eval case. The eval suite grows monotonically — see [[docs/canonical/living-eval-dataset|Living Eval Dataset]].

4. **Hardening cycle: switch → discover gaps → harden eval → retry**: Each switch follows this cycle:
   - **Switch**: Route a task (or task subset) to a new provider.
   - **Discover gaps**: Production monitoring and side-by-side comparison reveal failures the eval missed.
   - **Harden eval**: Add new eval cases covering the discovered failure modes. The eval suite now catches this class of failure for any provider.
   - **Retry**: With the hardened eval suite, switching again is safer because the suite now covers the gaps the first switch exposed.

5. **Iterative strengthening**: The first switch exposes the most gaps — Wedeen says it "invariably reveals the eval wasn't as good as you thought." The second switch exposes fewer gaps because the eval suite has been hardened. The third switch exposes even fewer. Over time, the eval suite asymptotically approaches genuine model-agnosticism — it catches failures regardless of provider because it has been battle-tested against multiple providers' failure modes.

**How this differs from the existing Model-Switching Architecture:**

[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] describes a formal gate process: evaluate a new model against an eval dataset → decide Switch/Hold/Hybrid → migrate traffic. This is a *migration* pattern — it treats eval as a stable gate that models must pass. Model-switch-driven eval hardening treats eval as an evolving artifact that switches strengthen. The difference is philosophical: the existing pattern validates models against evals; the Sierra pattern improves evals through model switching.

**The hardening cycle in practice (Sierra's use case):**

1. Sierra routes a task type (e.g., intent classification) to a new model from a different provider.
2. The existing eval suite runs on the new model's outputs. 95% pass rate — comparable to the previous provider's 96%. The eval says the switch is safe.
3. Production monitoring catches failures the eval missed: the new model classifies "I'd like to return this" as a billing inquiry 2% of the time (a failure mode the previous provider never exhibited). The eval suite had no test for this because the previous provider never got it wrong.
4. Sierra adds eval cases specifically testing return-vs-billing disambiguation. The hardened eval now catches this failure for any provider.
5. When Sierra later switches a different task to this provider, the eval suite already covers the return-vs-billing edge case — because it was hardened by the first switch.

## Implementation in this repo

### What already exists

From the classification:

- [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]: Full design for model-switching eval gate (Switch/Hold/Hybrid decision). Provider-agnostic eval format and side-by-side comparison infrastructure.
- [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]]: Provider-agnostic eval format — the foundation for model-agnostic eval infrastructure.
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]: Model-diverse evaluation — runs evals against multiple models but does not formalize the discovery-driven hardening cycle.

### What is missing

From the classification: "The specific insight that 'switching models is the best way to expose gaps in your eval suite' is not articulated. The repo's approach is a formal gate process, not the iterative, discovery-driven hardening Wedeen describes. No documented process of 'switch → discover eval gap → harden eval → try again.'"

1. **Discovery-driven hardening philosophy**: The repo treats evals as a stable gate; Sierra treats evals as an evolving artifact improved by switching. The repo documents "how to validate a model switch" but not "how model switches improve evals."
2. **Hardening cycle documentation**: No explicit switch → discover → harden → retry loop with evidence of gaps discovered through switching.
3. **Iterative strengthening trajectory**: No concept that the first switch exposes the most gaps and subsequent switches expose fewer as the eval suite asymptotically approaches model-agnosticism.
4. **Integration with living eval dataset**: [[docs/canonical/living-eval-dataset|Living Eval Dataset]] describes monotonic growth from production incidents but does not connect growth specifically to model switches as a gap-discovery mechanism.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Turns model switching from a migration risk into an eval hardening mechanism — each switch makes the harness stronger | Initial switches surface more gaps than expected — requires investment to close them before the switch can be completed |
| Continuous strengthening: each switch improves evals, making future switches safer — the eval suite asymptotically approaches model-agnosticism | Eval hardening is iterative — each new provider exposes new gaps that must be closed; the process never fully converges |
| Treats the eval suite as the stable interface, not model affinity — evals, not models, are the architecture's anchor | Not beneficial if you never intend to switch models — the hardening value comes from exposure to diverse failure modes |
| Complements formal gate processes with discovery-driven improvement — both perspectives are valid and necessary | Requires eval infrastructure that works across providers (same inputs/outputs semantics) — the neutral selection layer is prerequisite |

## Relationship to Other Patterns

- **Extends:** [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] — adds the discovery-driven hardening philosophy to the existing formal gate process.
- **Requires:** [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] — provider-agnostic eval format is prerequisite for running evals across providers.
- **Uses:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — model-diverse evaluation provides the multi-provider comparison needed to discover gaps.
- **Requires:** [[docs/canonical/always-on-monitoring-human-triage|Always-On Production Monitoring with Human Triage]] — production monitoring catches the failures the eval suite misses post-switch.
- **Feeds:** [[docs/canonical/living-eval-dataset|Living Eval Dataset]] — discovered gaps become permanent eval cases, growing the dataset monotonically.
- **Uses:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — gaps are classified by layer (deterministic, semantic, behavioral) for targeted hardening.

## References

-  lines 290-315 — extracted pattern with hardening cycle, iterative strengthening, model-agnostic confidence.
-  lines 173-183 — Partial Coverage classification with evidence of formal gate but missing discovery-driven philosophy.
- [[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]] lines 48-52, 98 — existing Switch/Hold/Hybrid gate process.
- [[docs/canonical/neutral-selection-layer|Neutral Selection Layer]] — existing provider-agnostic eval format.
- Sierra transcript: "The first switch invariably reveals the eval wasn't as good as you thought." — Wedeen on the gap discovery mechanism.
- Sierra transcript: "We switch models not to switch models — we switch models to discover what our evals are missing." — Wedeen on the philosophy.

---

*Created: 2026-06-26 | From: Sierra pattern classification | Precedence: canonical*
