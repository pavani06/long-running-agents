---
title: "Presence-in-the-Loop Metric"
type: canonical
tags: ["governanca", "agentes-orquestracao", "decision-discipline", "harness-engineering"]
aliases: ["presence in the loop", "presence metric", "involvement metric", "stale presence warning", "absent owner detection", "presence timeline", "human-in-the-loop metric"]
last_updated: 2026-06-12
relates-to: ["[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-mental-model|IDSD Method Mental Model]]"]
sources: ["[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]"]
---

# Presence-in-the-Loop Metric

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-12-idsd-method/
**Classification:** Missing, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

When the human only appears at the end of an agentic workflow to approve a diff, that diff is already too large to meaningfully review. The human becomes a symbolic gate, not an active outcome owner. The agent has made hundreds of micro-decisions during execution -- decisions about what "correct" means, what constraints matter, and what tradeoffs to make -- and the human discovers these only after the work is done. At that point, rework is the dominant cost.

The source frames this as the central measurement inversion: "metrica central e presenca no loop, nao aprovacao no gate" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:100). The risk is not that teams are not ready -- "O risco e o dia em que um agente escreve dez mil linhas que parecem certas, e ninguem possui a parte que explica o que 'certo' significa" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:100).

The repo has pre-execution gates (Manual Brake, Grill-Me, AFK Routing) and post-execution gates (review, merge), but no mechanism measures or tracks human involvement during active agent work. All existing gates are at entry or exit points. The classification confirms this is Missing: "no document defines a presence metric, presence timeline, stale-presence warning, or involvement measurement" ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:175-176).

## Solution

Treat human presence during agent execution as a governance metric, not as an assumption. Measure when the outcome owner was involved, detect when they have been absent too long, and require intervention points before the loop continues.

**Presence timeline:**

A chronological record of human involvement during an agent work session. Each entry records:
- Timestamp of the human interaction (question, clarification, review checkpoint, or approval).
- The phase or iteration in which the interaction occurred.
- The specific decision or clarification produced.
- The delta between the current interaction and the previous one.

The timeline answers the question: "Was the human in the loop while decisions were being made, or only at the end?"

**Stale-presence warnings:**

When the time since the last human interaction exceeds a risk-tiered threshold, the system emits a warning. The warning does not stop the agent immediately -- it signals that the human has been absent and that decisions are accumulating without ownership input.

Risk-based thresholds:
- **Low-risk work** (well-defined, small scope, reversible): longer tolerance before warning.
- **Medium-risk work** (moderate scope, user-facing change, requires product judgment): moderate tolerance.
- **High-risk work** (large diff, security-sensitive, production-critical, expensive to revert): short tolerance; may escalate to blocking the agent.

**Required intervention points:**

Instead of waiting for the final gate, define specific points during execution where the human must provide input before the agent continues. These points are placed at natural decision boundaries:

1. **After intent clarification.** The agent has read the intent and identified ambiguities. Before filling gaps with assumptions, route the ambiguities to the outcome owner.
2. **After the first working output.** The agent has produced something that passes automated validation. Before proceeding to refinement, show the output to the owner for a directional check.
3. **Before large-scope execution.** If the agent's plan involves changes across multiple files or systems, confirm the scope with the owner before broad execution.
4. **When validation fails repeatedly.** Multiple retry cycles on the same expectation signal that either the expectation is wrong or the approach is wrong. The human should decide.

**Review confidence signal for the final gate:**

When the final review gate does arrive, it should not be blind. The presence timeline provides a confidence signal: a review of a diff where the owner was involved at three checkpoints has higher confidence than a review of a diff with zero human interaction during execution. The signal does not replace the review -- it informs the reviewer about how much ownership was exercised during construction.

**Integration with the ICE crafts:**

Presence is most critical for the crafts the human owns (Intent and Expectations). The five-part intent is written by the outcome owner; the expectations boundary is defined by the outcome owner. Presence-in-the-loop means the owner stays engaged as the agent interprets those artifacts, not just when they were written.

## Implementation in this repo

### What already exists

- [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]:31-36 forces a human checkpoint before execution with three diagnostic questions. A pre-execution gate -- human is present at the start, not during work.
- [[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]:30-52 classifies tasks as AFK-ready or human-in-loop at routing time based on ambiguity, architecture, feedback-loop readiness, and product judgment. A classification decision, not an ongoing presence metric.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 requires human answers to structured questions before the agent proceeds. Human present before planning, not during execution.
- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]:29-51 defines explicit ownership roles with refusal authority. Assigns owners but does not measure owner presence or involvement during execution.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-73 separates generation from evaluation with an explicit retry loop. The Evaluator validates against rubrics and constraints, but the rubrics are evaluated at the end of each iteration -- after the agent has already produced output.

### What is missing from the pattern

The classification marks Presence-in-the-Loop as Missing because no repo document, skill, or curriculum defines presence measurement, involvement tracking, or stale-owner detection ([[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|classification]]:171-191).

Missing items:

1. A presence timeline data structure that records human interactions during agent execution with timestamps, phases, and decisions.
2. Stale-presence detection: configurable thresholds that emit warnings or escalate when the owner has been absent too long for the risk tier.
3. Required intervention points: specific checkpoints during execution where the agent pauses and routes questions to the owner.
4. Review confidence signal: when the final gate arrives, the presence timeline informs the reviewer about ownership involvement during construction.
5. Risk-tiered thresholds: low-risk work tolerates longer absence; high-risk work requires more frequent presence.
6. Integration with the issue lifecycle workflow: where in claim -> worktree -> implement -> review does presence measurement fit?

## Tradeoffs

| Benefit | Cost |
|---|---|
| Measures human ownership during work, not symbolic approval after the work | Can become surveillance if treated as attention monitoring instead of outcome ownership |
| Catches expectation drift earlier, when repair is cheaper than after a large diff | Adds human attention cost and should be risk-tiered, not uniformly applied |
| Makes large autonomous diffs visible as a governance failure, not just a review burden | Presence does not guarantee good judgment -- checkpoints must be structured and outcome-aware |
| Provides data for calibrating how much human involvement different task types actually need | Instrumentation overhead: requires tracking interactions and computing presence deltas |
| Pairs naturally with the ICE crafts (the owner stays engaged while their Intent and Expectations are interpreted) | Requires organizational buy-in to treat presence as a metric, not just attendance |

## Relationship to Other Patterns

- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- ICE assigns Intent and Expectations to the human owner. Presence-in-the-loop measures whether the owner stayed engaged while those crafts were being interpreted by the agent. The crafts define what the human owns; presence measures whether they exercised it.
- **[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]** -- the expectations boundary defines done from the outcome owner's perspective. Presence-in-the-loop ensures the owner is available to clarify that boundary when the agent encounters ambiguity.
- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake questions are a pre-execution checkpoint. Presence-in-the-loop extends this from a single gate to an ongoing metric, measuring involvement across the full execution timeline.
- **[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]** -- tasks classified as human-in-loop by the routing gate should be monitored for presence during execution. Tasks classified as AFK-ready should tolerate longer absence.
- **[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]** -- the alignment interview is a pre-planning presence event. The presence timeline would record this as an interaction point and track the delta to the next interaction.
- **[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]** -- the Owner-of-No has refusal authority. Presence-in-the-loop means the Owner-of-No is actually present to exercise that authority, not just named on a document.
- **[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]** -- the value gate is a decision point in the agent architecture. Presence-in-the-loop ensures the human is available at that decision point, not just notified after the decision was made.
- **[[docs/canonical/generator-evaluator|Generator-Evaluator]]** -- the Evaluator checks output against rubrics. But if the rubrics are ambiguous, the Evaluator needs the owner to clarify. Presence-in-the-loop provides that clarification channel.

## References

- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|IDSD Method Analysis]]:53-55 -- drift e ausencia: o agente preencheu partes que o humano nao pensou porque o humano saiu do loop
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:96-100 -- metrica central e presenca no loop, nao aprovacao no gate
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:132-134 -- resposta genuina ao problema: estar envolvido em cada passo
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-patterns|IDSD Method Patterns]]:161-188 -- extracted pattern: Presence-in-the-Loop Operating Metric
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]:163-191 -- classification evidence: Missing, Medium integration value
- [[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-analysis|analysis]]:117-119 -- caso dos tres dias de retrabalho: $985 em tokens para criar e desfazer porque ninguem estava no loop
