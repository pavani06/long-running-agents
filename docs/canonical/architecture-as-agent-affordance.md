---
title: "Architecture-as-Agent-Affordance Refactoring"
type: canonical
tags: ["agentes-orquestracao", "arquitetura", "governanca"]
aliases: ["deep module refactoring", "agent affordance architecture", "architecture for agents", "agent-navigable architecture"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Matt Pocock Classification]]", "[[.opencode/skills/writing-plans/SKILL|writing-plans skill]]"]
sources: ["[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Workflow Patterns]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|Matt Pocock Classification]]", "[[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Workflow Analysis]]"]
---
# Architecture-as-Agent-Affordance Refactoring

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Agents navigate codebases through surface-level structure: file names, import graphs, function signatures, and inline patterns. A shallow, highly coupled module structure forces the agent to read more files to understand a single behavior, track tangled dependencies, and guess at boundaries that are not encoded in the architecture. The source analysis frames this directly: a shallow, highly coupled codebase is not just ugly; it is hostile terrain for an agent ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|Matt Pocock Analysis]]:72).

The repository values clear interfaces and boundaries. The writing-plans skill maps files, responsibilities, boundaries, and interfaces before defining tasks. The split-brain planning review evaluates scope, dependencies, and risk. AGENTS.md demands small, explicit, and testable scripts and functions. But none of these rules name architecture as a deliberate input to agent performance. They treat boundaries as design hygiene, not as runtime affordances that reduce navigation cost, error rate, and cognitive load for the next agent session ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:232-236).

The consequence is missed leverage: each improvement cycle produces completion evidence but does not leave the codebase more navigable for the next agent. The next session inherits the same coupling, the same cost of understanding, and the same risk of breaking distant behavior.

## Solution

Architecture decisions should be evaluated as affordances for future agent sessions. A deep module with a simple public interface and behavior-level boundary tests is not only better human design; it is more navigable terrain for the next agent.

The pattern from the source identifies three architectural moves as agent affordances:

1. **Deep modules with simple public interfaces.** A deep module encapsulates complex behavior behind a small, explicit surface. An agent that encounters `paymentService.capture(orderId, amount)` does not need to read the internal validation, gateway routing, retry logic, audit logging, and state machine transitions. It trusts the interface and can work at the behavior level. A shallow module exposes all of that internal complexity through multiple public functions, leaked dependency objects, and implicit state, forcing the agent to read and understand everything before making safe changes.

2. **Boundary tests at behavior-level targets.** Tests that exercise module boundaries through the public interface produce more useful agent feedback than tests coupled to internal implementation. When an agent changes behavior inside `paymentService`, a boundary test that passes `capture(orderId, amount)` and asserts the payment gateway was called with the correct arguments survives the change. A test that imports internal helper functions and asserts local variable values breaks. Boundary tests reduce false-positive failures and give the agent actionable evidence about behavior correctness.

3. **Reduced coupling to reduce blast radius.** Coupled modules create cascading agent errors: a change to the order model unintentionally breaks invoice generation because both share a common utility that was not clearly owned. Deep modules with clear ownership boundaries limit the blast radius of any single change and reduce the number of files an agent must read to understand the consequences of its work.

The pattern flow: inspect dependency clusters and coupled behavior, identify boundaries where a deeper module can own behavior behind a simple interface, define tests around the behavior boundary, refactor or create issues for the architectural change, and use the improved boundary as a future agent affordance ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|patterns]]:407-411).

Critical distinction: this is architecture work, not formatting cleanup. Renaming files, reordering imports, or wrapping multiple functions in a class is not architecture-as-affordance. Deep modules hide complexity while exposing behavior; shallow reorganizations hide neither.

## Implementation in this repo

### What already exists

- [[.opencode/skills/writing-plans/SKILL|writing-plans skill]] lines 22-29 maps files, responsibilities, boundaries, and interfaces before defining implementation tasks. It requires clear-boundary design units, smaller focused files, and following established patterns.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] lines 30-41 evaluates scope, dependencies, tests, and risk during planning review, and records tradeoffs and deferred ambition for future agents.
- [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] lines 43-48 separates deterministic system integration from model-owned judgment and chooses slices with evidence before expanding automation surface.
- [[AGENTS]] lines 86-90 demands following existing module patterns, keeping scripts and functions small, explicit, and testable.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] provides the inner-loop frame that would benefit from improved module navigation.

### What is missing from the pattern

The Partial Coverage gap is that the repository treats architecture as code quality but not as a deliberate agent affordance. The classification found no canonical doc, curriculum material, or skill that names deep modules, boundary tests, or coupling reduction as explicit agent-performance inputs ([[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:234-236).

Missing pieces:

1. A canonical refactoring playbook that identifies dependency clusters and coupled behavior as agent-navigation costs.
2. A rubric for evaluating module boundaries through the lens of future agent sessions: surface area, coupling depth, test stability, and navigation cost.
3. A pattern for creating architecture-follow-up issues that persist on the backlog until the boundary is improved, not treated as one-off cleanup.
4. A rule that couples architecture improvement to feature work only when the coupling actively blocks the task, preventing scope-creep refactoring.
5. A definition of "deep module" and "simple public interface" as concrete, measurable properties rather than subjective design preferences.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Reduces agent cognitive load and error rate in future sessions | Requires real architecture judgment, not surface-level cleanup |
| Makes tests more meaningful by targeting behavior boundaries instead of internal implementation | Can be expensive and risky without strong test coverage before refactoring |
| Lets humans own interfaces while agents fill internals safely | Should not be mixed into unrelated feature work unless coupling blocks the task |
| Improves both human and agent maintainability in the same move | Deep modules take deliberate design time that defers feature completion |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] because the engineering reviewer should flag shallow, coupled modules that increase agent burden and recommend architecture issues.
- **Complements:** [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]] because architectural refactoring should itself follow plan-execute-verify to avoid destabilizing working behavior.
- **Enables:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] because boundary tests at the public interface level survive internal refactors, keeping the evaluator useful across architecture changes.
- **Feeds:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] by reducing navigation time and error rate inside the loop's exploration phase.
- **Relates to:** [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] because wedge selection benefits from clean boundaries between deterministic integration and model judgment.
- **Comes from:** [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|Matt Pocock Patterns]]:381-411 and its Partial Coverage classification in [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:220-237.

## References

- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns|patterns]]:381-411 - extracted pattern definition with dependency clusters, deep modules, boundary tests, and architecture follow-up backlog.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification|classification]]:220-237 - Partial Coverage classification and gap analysis for Architecture-as-Agent-Affordance.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|analysis]]:68-72 - deep modules as agent architecture and hostile terrain for agents.
- [[docs/analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis|analysis]]:140-146 - improve-codebase-architecture skill pattern description.
- [[.opencode/skills/writing-plans/SKILL|writing-plans skill]]:22-29 - file mapping, boundaries, and interfaces before task definition.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:30-41 - existing planning-review evaluation of scope, dependencies, and risk.
- [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]]:43-48 - deterministic vs model-judgment boundary separation.
- [[AGENTS]]:86-90 - existing code standards for small, explicit, testable scripts.

---

*Created: 2026-06-11 | From: Matt Pocock workflow pattern classification | Precedence: canonical*
