---
title: 'Application-Owned Agent Control Plane'
type: canonical
aliases: ["owned control plane", "plano de controle owned", "agent control plane", "control plane"]
tags: ["agentes-orquestracao", "harness", "arquitetura"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]"]
sources: ["[[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction: Harness Evolution]]"]
---

# Application-Owned Agent Control Plane

**Type:** Canonical Pattern
**Status:** Active
**Source:** docs/articles/harness-evolution-metodos-construcao.md
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Opaque agent runtimes make long-running behavior hard to inspect, pause, validate, or terminate because the runtime hides the loop boundaries where application code would otherwise summarize context, validate quality, require approval, or stop execution ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:7-26; [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:20-28). In production harnesses, this opacity compounds the three structural long-running failures named by the source article: context loss, fragile planning, and blind self-evaluation ([[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:27-35).

The concrete failure mode is a workflow that keeps iterating after context has degraded, tool output has drifted, or a high-risk step needs approval, while the application can only observe the framework's outer result rather than the prompt, context, action, dispatch, state writeback, and loop decision for each turn ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:22-28; [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:96-107).

## Solution

Own the agent control plane as application code. The control plane is the contract that joins the four owned loop components from [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] with the wider harness requirements extracted in the harness-evolution pattern: versioned prompt contracts, deliberate context construction, structured action schema, deterministic dispatch, loop policy, persistent execution state, and intervention gates ([[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:129-142; [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:7-40).

```
                    APPLICATION-OWNED AGENT CONTROL PLANE

  persistent state + durable facts
              |
              v
  +----------------------+     +-----------------------+
  | 1. Versioned Prompt  | --> | 2. Context Builder    |
  | prompt/tool contract |     | state, memory, tools  |
  +----------------------+     +-----------------------+
              |                            |
              +-------------+--------------+
                            v
                 model emits structured action
                            |
                            v
  +----------------------+     +-----------------------+
  | 3. Switch Dispatch   | --> | deterministic handler |
  | JSON -> handler      |     | result + trace        |
  +----------------------+     +-----------------------+
                            |
                            v
  +----------------------------------------------------+
  | 4. Loop Controller                                 |
  | persist result -> decide next control action        |
  |                                                    |
  | Gates: break | summarize | judge | human approval  |
  |        pause/resume | handoff | force terminate    |
  +----------------------------------------------------+
                            |
                            v
              continue, summarize, judge, pause,
              approve, hand off, or terminate
```

Core rules:

| Rule | Contract | Evidence |
|---|---|---|
| Prompt is owned and versioned | Treat the harness prompt and tool contract as code, with deliberate version changes and evals rather than incidental context compaction | [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:133-135; [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41 |
| Context is constructed, not appended | Build each model call from approved state, history, memory, tool results, and business facts, choosing every token deliberately | [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:135-136; [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction]]:41-45 |
| Actions are structured | Require the model to emit a structured action schema before application code routes behavior | [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:49-55; [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:9-14 |
| Dispatch is deterministic | Map action JSON to ordinary handler code through a switch/router that can be tested and audited without treating tools as magic | [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:20-36; [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:37-57 |
| Loop policy is explicit | Decide iteration count, exit conditions, summarization, LM-as-judge, approval, pause, handoff, and termination in code | [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:137-142; [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75 |
| State survives the loop | Persist execution state, durable facts, handler results, and traces so debugging, recovery, and audit do not depend on the current context window | [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:57-64; [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:169; [[docs/canonical/external-state-persistence|External State Persistence]]:29-57 |

Before and after:

| Before: framework-owned runtime | After: application-owned control plane |
|---|---|
| Framework appends messages and tool results until a configured stop condition | Application builds prompt and context blocks deliberately for each turn ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:77-85; [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:30-41) |
| Tool calls look like agent magic hidden behind framework internals | Model output is JSON routed through deterministic application code ([[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:20-36) |
| Pause, approval, summarization, and termination are unavailable or config-only | Loop gates are explicit application decisions at known boundaries ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75) |
| Debugging starts from the final trace after drift has already happened | Debugging can inspect prompt version, context input, action JSON, handler result, state writeback, and loop decision for each turn ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:15-22) |

## Implementation in this repo

### What already exists

- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] already names the inner-loop solution: own the control loop and decompose it into four components with explicit intervention points ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:29-31).
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] already defines the four components as Prompt, Context Builder, Switch Statement, and Loop, including prompt variants, summarization, circuit breaking, audit logging, human approval, and force termination as intervention points ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:33-51).
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] already defines loop controls such as break, summarize, LM-as-judge, human approval gate, and force terminate ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75).
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] already covers the broader operating loop: state intake, priority synthesis, execution routing, and feedback writeback ([[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]:28-37).
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] already requires source precedence, readable state, ownership, validation, and memory update as a minimum operating contract ([[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]:39-45).
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] already defines model output as JSON routed by application code and reframes tools as JSON plus deterministic code ([[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:20-36).
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] already shows the structured-output-to-switch-statement mechanism and its testability, auditability, circuit-breaking, and observability properties ([[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:37-67).

### What is missing

1. A single canonical contract that names the application-owned control plane rather than leaving prompt, context, dispatch, loop policy, persistent state, and gates split across adjacent docs ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/classification|Classification]]:18-33).
2. An explicit bridge from the four-component loop to the pattern inputs extracted from the source analysis: versioned prompt/tool contracts, context-builder inputs, structured action schema, deterministic handlers, loop policies, persistent state, and intervention gates ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:9-14; [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:27-40).
3. A control-plane view of persistent execution state as part of the loop contract, rather than only as a separate state-persistence or pause/resume pattern ([[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:57-64; [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-57; [[docs/canonical/external-state-persistence|External State Persistence]]:29-57).
4. A unified intervention-gate vocabulary that includes continue, summarize, judge, human approval, pause, handoff, and termination decisions as first-class control-plane outputs ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:15-18; [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Makes long-running agent behavior debuggable and testable as ordinary application control flow ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:19-22) | Requires engineering ownership of loop code instead of relying only on framework defaults ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:23-26) |
| Creates precise intervention points before drift, excessive runtime, or high-risk actions continue ([[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:137-142) | Adds application surface area that must be tested and maintained ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:23-26) |
| Makes dispatch, state writeback, and loop decisions auditable at each turn ([[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:59-67; [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]:39-45) | Each gate becomes a critical path where a bad policy can block valid work or allow unsafe continuation ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:117-124) |
| Lets the harness evolve independently of opaque framework loop behavior ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:77-85) | May be unnecessary for single-shot or very low-risk model calls ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:23-26) |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] for the four inner-loop components and intervention points ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:29-51), [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] for JSON-to-handler routing ([[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:20-57), and [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] for preserving and versioning the prompt contract separately from reducible context ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41).
- **Validated by:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] when control-plane outcomes are written back as durable operational state ([[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]:39-45), and by eval or review gates such as LM-as-judge and human approval inside the loop ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:68-75).
- **Complements:** [[docs/canonical/external-state-persistence|External State Persistence]] for durable facts outside the context window ([[docs/canonical/external-state-persistence|External State Persistence]]:29-57), [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]] for pause/resume mechanics ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-57), and [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]] for the harness-evolution framing that treats harnesses as structures for reliability, traceability, and auditability ([[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:23-35).

## References

- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:23-35 - harnesses transform nondeterministic models into reliable, traceable, auditable products and address context loss, fragile planning, and blind self-evaluation.
- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:129-142 - four owned loop components and intervention points.
- [[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]:145-158 - context engineering framing and stable prompt, memory catalog, and error hygiene mechanisms.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/analysis|Knowledge Extraction]]:35-40 - extracted four-component owned control loop.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/patterns|Pattern Extraction]]:7-40 - extracted Application-Owned Agent Control Plane problem, inputs, outputs, components, and flow.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/classification|Classification]]:18-35 - Partial Coverage classification and missing unified control-plane contract.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:29-75 - existing owned-loop solution, components, and loop controls.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:96-107 - current gap where full loop ownership remains incomplete under framework-managed iteration.
- [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]:28-45 - broader operating loop and minimum operating contract.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]:20-67 - JSON-to-deterministic-code dispatch mechanism and properties.
