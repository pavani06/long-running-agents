---
title: "Multi-Agent Fault Tolerance"
type: canonical
aliases: ["agent fault tolerance", "Saga pattern for agents", "circuit breaker for agents", "multi-agent resilience"]
tags: ["agentes-orquestracao", "error-handling", "production", "harness-engineering"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]"]
---

# Multi-Agent Fault Tolerance

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/
**Classification:** Partial Coverage (P1, High)
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Multi-agent workflows fail partially — one agent succeeds, another times out, a third returns stale data. Without fault tolerance at the orchestration layer, partial failures either go undetected (producing incorrect final results) or crash the entire workflow (losing the progress of successful agents).

The repo has strong single-agent fault tolerance: a tested degradation ladder (`tested-degradation-ladder.md`) defining failure classification → retry with repair → safe fallback → human escalation, exponential backoff retry with jitter (`harness/retry.py`), error context hygiene with bounded retry and summarized errors (`error-context-hygiene.md`), and explicit loop intervention points (`owned-agent-control-loop.md`). However, these mechanisms cover single-agent failure recovery — not multi-agent distributed transaction fault tolerance with Saga rollback and rate-threshold circuit breaking at the orchestration layer.

## Solution

Extend fault tolerance from single-agent recovery to multi-agent orchestration using three complementary mechanisms:

### 1. Saga Pattern (Compensating Transactions)

When a multi-step agent workflow fails at step N, execute compensating actions for steps 1..N-1 in reverse order, returning the system to its pre-workflow state. Each step in the workflow must declare its compensating action — the reverse operation that undoes the step's effect.

```
Workflow: Agent A → Agent B → Agent C
Failure: Agent C fails
Saga rollback: Compensate(B) → Compensate(A)
```

Not every operation has a clean undo (e.g., sending an email, posting a message). For irreversible operations, the compensating action is a notification or correction message, not a true undo. The Saga contract must classify each step as `reversible`, `compensatable` (correctable via notification), or `irreversible` (requires human intervention).

### 2. Circuit Breaker at Orchestration Layer

When an agent's failure rate exceeds a configured threshold over a rolling window, the circuit opens. Subsequent calls to that agent are redirected to a fallback — either a default response, a cached result, or a human escalation queue. The circuit transitions through three states:

| State | Behavior | Transition trigger |
|---|---|---|
| **Closed** | Normal operation — calls pass through to the agent | Failure rate > threshold → Open |
| **Open** | Calls redirected to fallback — agent not invoked | Timeout expires → Half-Open |
| **Half-Open** | Limited probing — a subset of calls pass through to test recovery | Probe succeeds → Closed; Probe fails → Open |

The threshold is per-agent, configurable, and measured over a rolling window. The fallback action is declared per agent in the orchestration contract.

### 3. Human Escalation with Full Context

When confidence is below threshold, the circuit is open, or an irreversible operation must be decided, route the query to a human operator with full context: what the agent attempted, why it failed, what compensating actions were applied, and what the human needs to decide.

### Orchestration Contract

Each multi-agent workflow step must declare:

| Field | Meaning |
|---|---|
| `agent_id` | Which agent executes this step |
| `compensating_action` | Reverse operation (or `NONE` for compensation-free steps) |
| `reversibility` | `reversible`, `compensatable`, or `irreversible` |
| `circuit_threshold` | Failure rate threshold for circuit breaker (per agent) |
| `fallback_action` | What to do when circuit is open |
| `escalation_policy` | Which failure classes require human judgment |
| `timeout` | Maximum execution time before the step is considered failed |

## Implementation in this repo

### What already exists

- **Tested Degradation Ladder** (`tested-degradation-ladder.md:29-63`) defines failure classification → retry with repair → safe fallback or hold → human escalation → outcome log + rung tests. Covers single-agent recovery comprehensively.
- **Exponential backoff retry** with jitter is implemented in `harness/retry.py:25` using stdlib asyncio.
- **Error Context Hygiene** (`error-context-hygiene.md:93`) provides bounded retry with one-line error summaries, context injection by attempt, success detection, and pending-error cleanup.
- **Owned Agent Control Loop** (`owned-agent-control-loop.md:68`) defines explicit intervention points: break, summarize, LM-as-judge, human approval gate, and force terminate.
- **Multi-Model Evaluation Council** (`multi-model-evaluation-council.md:30-47`) routes evaluation outcomes to retry, needs-human, or rubric-update.

### What is missing

1. **Saga pattern**: no compensating action design for multi-step agent workflows. No reverse-order rollback that undoes partial successes when a later step fails. No reversibility classification (`reversible`, `compensatable`, `irreversible`) per workflow step.
2. **Circuit Breaker at the agent orchestration layer**: no failure-rate-threshold-based tripping that stops cascading failures by routing to fallback. The Circuit Breaker referenced by codegraph exists in `Documents/Codex/`, not in this repo.
3. **Orchestration contract**: no per-step declaration of compensating action, circuit threshold, fallback action, escalation policy, and timeout for multi-agent workflows.
4. **Partial completion log**: no record of which steps succeeded and what compensating actions were applied when a workflow cannot complete.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents cascading failures: a slow external API does not degrade the entire multi-agent system | Compensating actions must be designed and tested for every step — not every operation has a clean undo |
| Maintains consistency: Saga ensures distributed transactions across agents are atomic — all succeed or all are compensated | Saga adds latency: each step must await confirmation, and rollback multiplies the number of operations |
| Graceful degradation: circuit breaker routes failing agents to fallback responses instead of returning errors to users | Circuit breaker thresholds require tuning; too sensitive degrades UX, too lenient allows cascading failures |
| Audit trail: every failure, rollback, and escalation is logged, enabling post-incident analysis | Human escalation introduces variable latency and requires operational staffing |

## Relationship to Other Patterns

- **Extends:** Tested Degradation Ladder — the ladder covers single-agent recovery; Saga + Circuit Breaker extend it to multi-agent orchestration.
- **Uses:** Error Context Hygiene — when escalating to human, the error summary and context cleanup rules apply.
- **Uses:** Owned Agent Control Loop — loop intervention points (break, human approval gate, force terminate) serve as the integration surface for circuit breaker actions.
- **Complements:** Multi-Model Evaluation Council — the council's routing (retry, needs-human, rubric-update) serves as one trigger for circuit breaker state transitions.
- **Enables:** Closed-Loop Agent Operating System — fault tolerance with audit trail closes the loop between failure detection and operational correction.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:263` — extracted pattern definition.
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:306` — Partial Coverage classification (P1, High).
- `docs/canonical/tested-degradation-ladder.md:29` — failure classification → retry → fallback → escalation ladder.
- `docs/canonical/tested-degradation-ladder.md:46` — human escalation rung.
- `docs/canonical/error-context-hygiene.md:93` — bounded retry with summarized errors.
- `docs/canonical/owned-agent-control-loop.md:68` — loop intervention points.
- `.opencode/skills/analyze-and-improve/harness/retry.py:25` — exponential backoff retry implementation.
- `docs/canonical/multi-model-evaluation-council.md:30` — council routing to retry, needs-human, rubric-update.

---

*Created: 2026-06-26 | From: Production AI Playbook classification (Batch B) | Precedence: canonical*
