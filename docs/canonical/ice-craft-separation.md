---
title: "ICE Craft Separation"
type: canonical
tags: ["governanca", "decision-discipline", "agentes-orquestracao", "spec-driven-development", "harness-engineering", "context-engineering"]
aliases: ["ICE framework", "ICE decomposition", "ICE crafts", "intent context expectations", "craft separation", "ICE trichotomy", "ICE ownership split"]
last_updated: 2026-06-12
relates-to: ["[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]", "[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]"]
sources: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]"]
---

# ICE Craft Separation

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-12-idsd-method/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

When a single specification document carries four distinct responsibilities -- intent (what we want), expectations (what done means), workflow (how we build it), and context (the technical environment) -- the gaps between these responsibilities are filled by the agent. The agent guesses what the human wanted, guesses what "done" means, fills in missing constraints, and produces output that looks correct but encodes decisions the human never explicitly made. The single document collapses under its own weight because it was never one thing.

The source names this as the single-document failure: "SDD colapsa porque pede que um documento carregue quatro responsabilidades distintas, e os gaps entre elas sao deixados para o agente preencher" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:40). The insight is not that specifications are bad -- it is that mixing distinct crafts with distinct owners into one artifact is the structural error.

The repo has extensive ownership separation (Owner-of-No, Generator-Evaluator, Grill-Me alignment) but does not formalize the Intent-Context-Expectations trichotomy as named crafts with explicit ownership assignment. The pieces exist distributed across multiple canonical docs, but no single document names "ICE Craft Separation" or assigns distinct owners to each craft as a deliberate architectural decision ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:38-52).

## Solution

Decompose the monolithic specification into three separated crafts, each with a distinct owner, purpose, and artifact. The crafts are Intent, Context, and Expectations (ICE). The separation of owners is the central architectural point: the human owns Intent and Expectations and never abandons them; the harness owns Context and the execution Loop and is never invited to invent what the human wanted.

**Intent -- owned by the outcome owner (human):**

What you want. A first-class primitive structured as five fields: description, constraints, failure scenarios, success scenarios, and connections to other intents. Intent answers "what should exist and what must not happen." The five-part structure ensures completeness: any missing field is a visible gap, not an invisible delegation to the agent. Formalized in [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]].

The outcome owner writes the Intent. No one else has the authority or the context to define what they want. The agent never invents intent.

**Context -- owned by the harness:**

The how: technology, existing system, codebase constraints, runtime state, tools. Context is not a wall of text dumped at the start -- it is fed progressively by the harness, on demand, as the agent needs it for the current step. The harness owns Context selection, freshness, and disclosure policy. Formalized in [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] and [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]].

The harness constructs Context from its inventory (docs, architecture decisions, state, tool results, constraints). The agent never decides what context it needs -- it receives context from the harness at the right time for the right step.

**Expectations -- owned by the outcome owner (human):**

The boundary: what "done" and "failed" look like, written in outcome language, not implementation language. Expectations are not a specification -- they are a craft of what "terminated successfully" means, separate from both Intent (the desire) and Context (the environment). Formalized in [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]].

The same person who wrote the Intent writes the Expectations. The moment the definition of done drifts away from the person who wanted the outcome, the agent starts deciding "done" on its own.

**The separation principle:**

| Craft | Owner | Purpose | Artifact | Agent can modify? |
|---|---|---|---|---|
| Intent | Outcome owner (human) | What we want | Five-part intent record | No |
| Context | Harness | Technical environment | Progressive context packets | No (reads only) |
| Expectations | Outcome owner (human) | What done/failed means | Expectations artifact with scenarios, limits, non-goals | No |
| Loop execution | Harness | Build, validate, retry | Owned Agent Control Loop | Yes (within ICE boundaries) |

**Gap list:**

When the three crafts are separated, gaps become visible. Any question the agent would have to answer to proceed -- "what constraint applies here?", "is this done?", "does this affect another system?" -- goes onto a gap list. The gap list is routed to the appropriate owner before execution continues. The agent never fills a gap silently.

**The method versus the harness:**

The source draws a sharp distinction: spec-kit, BMAD, Kiro, Tessl, and Agent OS are harnesses -- useful, but only harnesses. ICE is the method that decides what the work is before the harness touches it. Adopting the harness without the method produces the same failure mode the author experienced: three days of rework, ~$985 in tokens, building and then undoing work ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:58-59).

**The ICE Loop flow:**

1. Human provides Intent + Expectations.
2. Harness pulls Context for the current step.
3. Harness codes/executes.
4. Harness validates against Expectations.
5. If output does not meet Expectations, iterate with targeted feedback.
6. If output meets Expectations, merge/handoff.

The human owns steps 1 and the approval of step 6. The harness owns steps 2-5. The human never abandons Intent and Expectations; the harness never invents them.

## Implementation in this repo

### What already exists

- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]:29-51 defines explicit ownership roles with refusal authority and a four-word decision vocabulary. This is the repo's strongest ownership mechanism, but it governs a single gatekeeper role rather than assigning distinct owners to Intent, Context, and Expectations as separated crafts.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 runs a structured interview capturing decisions, deferrals, and rationale. Separates intent capture from implementation, but does not formalize Context and Expectations as equivalent first-class crafts with their own owners.
- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:29-64 unifies prompt, context builder, dispatch, and loop policy as owned components. The Context Builder is explicitly an owned component (line 70-71: "Context is constructed, not appended"), but Context ownership is merged into the control plane rather than separated as an independent craft.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 anchors evaluation on explicit constraint lists from client state and business rules. Covers the expectations-as-constraints dimension but focuses on verification mechanics rather than craft ownership.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-73 separates generation from evaluation with distinct agents and an explicit retry loop. This is the loop execution craft in ICE -- the Generator builds, the Evaluator validates against expectations, and the loop retries until expectations are met.
- [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]:73-78 attaches intent statements and scope constraints to build decisions at a pre-execution gate. Separates intent from execution mechanics.
- [[docs/canonical/shared-design-concept-handoff|Shared Design Concept Handoff]]:30-48 formalizes the alignment output as a durable handoff artifact separating human judgment from agent interpretation. Closest existing artifact to the ICE intent/context separation.
- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]:28-53 defines a five-part resolver model for progressive context delivery. This is the Context craft implemented with trigger contracts, evals, and deduplication.

### What is missing from the pattern

The classification marks ICE Craft Separation as Partial Coverage because the pieces exist distributed across multiple canonical docs but are not unified as the named ICE triad with explicit craft ownership ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:38-52).

Missing items:

1. A unified ICE craft decomposition document (this doc) that names Intent, Context, and Expectations as three distinct crafts with explicit owners.
2. The gap list mechanism: when the three crafts are separated, gaps between them become visible. The repo does not generate or route gap lists.
3. Formal assignment of craft ownership: Intent owned by outcome owner, Context owned by harness, Expectations owned by outcome owner. The repo has ownership concepts but not this specific trichotomy.
4. The ICE Loop flow as a named pattern: human provides Intent+Expectations, harness pulls Context, harness codes/validates/iterates, human approves merge.
5. The method-vs-harness distinction: the repo has extensive harness infrastructure (owned agent control loop, context builder, eval pipeline) but does not frame ICE as the method layer above the harness.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents a single document from carrying four incompatible responsibilities collapsed into one artifact | Adds ceremony for very small or reversible tasks that do not need craft separation |
| Makes human-owned outcomes distinct from harness-owned mechanics -- each craft has one clear owner | Requires a named human owner for Intent and Expectations; owner unavailability blocks work |
| Gap list makes agent discretion visible: every decision the agent would have filled silently becomes a routable question | Does not by itself prove that each craft is complete or testable |
| Gives long-running workflows clearer auditability -- when behavior drifts, the craft responsible is identifiable | Higher setup cost than dumping everything into one prompt |
| Enables the ICE Loop: harness codes, validates, retries within boundaries the human defined | Requires organizational maturity to respect craft boundaries under delivery pressure |

## Relationship to Other Patterns

- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- the five-part intent is the detailed structure of the Intent craft. ICE defines the separation; the five-part primitive defines the Intent craft's structure.
- **[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]** -- the Expectations craft in ICE. Defines the done boundary as an artifact owned by the outcome owner, separate from Intent and Context.
- **[[docs/canonical/presence-in-the-loop-metric|Presence-in-the-Loop Metric]]** -- ICE assigns Intent and Expectations to the human. Presence-in-the-loop measures whether the human stayed engaged while those crafts were being interpreted.
- **[[docs/canonical/token-economics-gap-filling|Token Economics of Gap-Filling]]** -- gaps between the ICE crafts are what agents fill with tokens. The gap-filling cost attribution model measures the cost of not separating the crafts.
- **[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]** -- the control plane is the harness infrastructure that owns Context and the Loop. ICE is the method layer above the control plane.
- **[[docs/canonical/generator-evaluator|Generator-Evaluator]]** -- the Generator-Evaluator loop is the execution engine for the ICE Loop. Generator builds within the ICE boundary; Evaluator validates against Expectations.
- **[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]** -- the resolver is the harness mechanism that owns Context delivery. ICE assigns Context ownership to the harness; the resolver implements it.
- **[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]** -- constraints are the verifiable dimension of Expectations. After ICE separates Expectations as a craft, constraint-anchored evaluation provides the verification mechanics.
- **[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]** -- the alignment interview is a practical mechanism for capturing Intent with the outcome owner. ICE defines what Intent is; the interview captures it.
- **[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]** -- the Owner-of-No is a role that can refuse low-value work. ICE craft ownership is a broader concept: it assigns ownership to every craft, not just the refusal decision.
- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake questions probe the value dimension at the Intent boundary. ICE separates Intent as a craft; the brake questions validate that the Intent is worth executing.

## References

- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:22-30 -- ICE framework: decomposicao em tres partes com donos distintos
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:30 -- separacao de donos como ponto arquitetonico central
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:38-42 -- modelo de colapso do SDD: single-document failure
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:57-59 -- distincao harness vs. method
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:102-106 -- ICE Loop: fluxo completo com ownership
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:177-179 -- insight unificador: falha de decomposicao, nao de formato
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]:15-42 -- extracted pattern: ICE Craft Ownership Split
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]:30-52 -- classification evidence: Partial Coverage, High integration value
