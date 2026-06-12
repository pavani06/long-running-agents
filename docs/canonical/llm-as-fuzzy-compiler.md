---
title: "LLM as Fuzzy Compiler"
type: canonical
tags: ["agentes-orquestracao", "harness", "governanca", "context-engineering"]
aliases: ["LLM as compiler", "fuzzy compiler", "code as build artifact", "disposable code", "compiler mental model", "code generation backend"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|Harness Engineering Classification]]"]
sources: ["[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|Harness Engineering Classification]]"]
---

# LLM as Fuzzy Compiler

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/
**Classification:** Missing
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Teams building with AI agents default to treating model output as the durable asset. They version generated code, polish it in review, and preserve it indefinitely. When the model improves, they rewrite the code by hand or keep the old output. When the model regresses on a specific pattern, they add more guardrails without asking whether the code itself should be regenerated from updated constraints.

This mental model treats the LLM as an oracle whose output is precious. In reality, the LLM is a probabilistic transformer with no guarantees about consistency across model versions. Code produced by one model version may look different from code produced by another even when both satisfy the same acceptance constraints. The durable asset was never the code; it was always the constraints that define what acceptable code looks like.

The source identifies this as a fundamental reframe: "code is a disposable build artifact" and "what matters is preserving the prompts, guardrails, and documentation that produced the code, not the code itself" ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:61-63, 208). Without this reframe, teams waste maintenance effort on generated output while the reusable system knowledge — prompts, lint rules, NFR documents, reviewer rubrics, skills — receives no versioning, governance, or lifecycle management.

The repository currently has no canonical doc, curriculum lesson, or skill that frames the LLM as a compiler backend. Adjacent canonical docs cover related but distinct concepts: `invariant-compensation-split.md` classifies harness controls by domain risk vs. model weakness, and `measured-harness-evolution-lifecycle.md` governs component lifecycle, but neither frames the LLM as a compilation target nor code as a disposable artifact ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:297-309).

## Solution

Adopt the mental model: **the LLM is a fuzzy compiler, the harness is a set of optimization passes, and code is a disposable build artifact.**

The model works as follows:

```
         +---------------------------+
         | Harness assets (durable)  |
         | prompts, NFRs, lint rules |
         | reviewer rubrics, skills  |
         +-------------+-------------+
                       |
                       v
         +---------------------------+
         | LLM backend (fuzzy)       |
         | model as code-generation  |
         | compiler                   |
         +-------------+-------------+
                       |
                       v
         +---------------------------+
         | Code output (disposable)  |
         | generated and validated   |
         | against harness constraints|
         +---------------------------+
```

**Components:**

1. **Harness assets (source of truth).** Prompts, guardrails, lint rules, reviewer rubrics, NFR documents, and skills define what acceptable output looks like. These are versioned, governed, and treated as durable engineering artifacts. They survive model changes because they encode domain requirements, not model-specific behavior.

2. **LLM backend (fuzzy compiler).** The model is a code-generation backend — analogous to LLVM or Cranelift in traditional compilation. Different model versions produce different output, but the acceptance constraints (harness assets) produce valid output regardless of the generation process. Swapping models is like swapping compiler backends: the output changes, the constraints do not ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:61-62).

3. **Harness as optimization passes.** Each harness component functions as a compiler pass: lint rules catch syntax-level violations, reviewer rubrics enforce architectural constraints, skills encapsulate complex workflows, NFR documents encode domain requirements, and eval suites validate behavioral correctness. These passes run at different phases of the compilation pipeline and collectively ensure the generated code meets acceptance criteria.

4. **Code output (disposable artifact).** Generated code is treated as replaceable output. When a model improves, the code is regenerated from the same harness assets. When a model introduces a new failure pattern, the harness assets are updated and the code is regenerated. The code itself is not the durable investment; the harness that produces it is.

**Core rules:**

| Rule | Decision test | Default action |
|---|---|---|
| Version harness assets, not generated code | Can this artifact be regenerated from harness assets? | Version the harness; treat code as build output |
| Improve the harness before patching output | Does a code-level fix address a class of behavior or one instance? | Add a harness guardrail that eliminates the class |
| Model changes are backend swaps | When upgrading models, does the harness still produce acceptable output? | Regenerate; update harness only if acceptance criteria changed |
| Harness assets rot too | Do lint rules, NFRs, and reviewer rubrics still match current domain requirements? | Govern harness assets through measured lifecycle |

## Implementation in this repo

### What already exists

- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] lines 31-60 classifies harness controls as domain invariants vs. model-specific compensations. This is the closest existing canonical doc to the compiler-mental-model because it separates what must survive model changes (invariants) from what should be simplified or removed when models improve (compensations).
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] lines 29-62 governs component lifecycle through BUILD, STABILIZE, SIMPLIFY, and REMOVE states with ROI measurement, quarterly cadence, and archive contract. This is the governance mechanism for harness assets as first-class artifacts.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] lines 26-41 separates stable harness instructions from reducible context payload. This treats harness instructions as durable assets that survive context reduction, directly implementing the "preserve harness, not code" principle.
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] lines 30-42 defines a layered context assembly policy with explicit budget ordering. This is the context-delivery mechanism that the compiler-mental-model depends on.
- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] lines 28-53 loads context on demand via resolvers, implementing "give the model text at the right time" — the harness as context manager.

### What is missing from the pattern

The classification marks LLM as Fuzzy Compiler as Missing after searching all canonical docs, curriculum lessons, decisions, skills, and agent definitions. The concept appears only in the Harness Engineering analysis documents themselves, not in any repo artifact ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:297-309).

Missing pieces:

1. No canonical doc frames the LLM as a compiler backend rather than an oracle. The closest doc (`invariant-compensation-split.md`) addresses harness component governance but does not adopt the compiler mental model.
2. No curriculum lesson or core concept teaches the compiler-mental-model as a pedagogical frame. The curriculum teaches harness evolution (Core Concept 6) and constraint-anchored evaluation but does not teach code-as-disposable-artifact.
3. No explicit policy distinguishes durable harness assets (versioned, governed) from disposable code output (regenerated, not maintained). The `measured-harness-evolution-lifecycle.md` governs harness components but does not classify code output as the product of a compilation process.
4. The source's `Durable Harness Asset Preservation` pattern ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|patterns]]:367) captures "generated code treated as replaceable output" but has no corresponding canonical doc or curriculum integration.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Makes model upgrades less disruptive because acceptance constraints remain stable | Requires upfront investment in harness assets before code generation is reliable |
| Focuses maintenance on structures that improve every future run, not one codebase snapshot | Teams may underinvest in generated code quality if "disposable" is interpreted as "unimportant" |
| Enables systematic improvement: fix the harness, regenerate code, verify against evals | Regeneration still requires test and review infrastructure to validate new output |
| Creates a coherent pedagogical narrative connecting harness components to compilation passes | The compiler metaphor abstracts away the probabilistic nature of LLMs, which can mislead about determinism |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] because separating domain invariants from model compensations is the prerequisite for treating model output as disposable.
- **Governed by:** [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] because harness assets need the full BUILD/STABILIZE/SIMPLIFY/REMOVE lifecycle with ROI measurement and archive contract.
- **Implemented through:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] because preserving harness instructions during context reduction is how the compiler constraints survive.
- **Delivered by:** [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] and [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] because layered context assembly and on-demand loading are the delivery mechanism for compiler passes.
- **Complements:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent OS]] because feedback writeback updates harness assets based on observed behavior, closing the compilation-improvement loop.
- **Feeds:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] because the weekly cadence of converting review feedback into automated guardrails is how harness assets improve systematically.
- **Comes from:** [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]:357-381 and its Missing classification in [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:295-309.

## References

- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:59-63 — LLM as fuzzy compiler, harness as optimization passes, model swap as backend swap.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:201-210 — synthesis: harness as context operating system, unit of value shifts from code to prompt+guardrails.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|patterns]]:357-381 — Durable Harness Asset Preservation pattern: version harness assets, treat generated code as replaceable output.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:295-309 — Missing classification with NOT_FOUND evidence across canonical docs, curriculum, decisions, skills, and agents.
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]:31-60 — classification of harness controls as domain invariants vs. model compensations.
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]:29-62 — BUILD/STABILIZE/SIMPLIFY/REMOVE lifecycle with ROI, archive, and reactivation.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41 — stable harness prompt preservation during context reduction.
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:30-42 — layered context assembly policy.

---

*Created: 2026-06-11 | From: Harness Engineering pattern classification | Precedence: canonical*
