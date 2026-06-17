---
title: "Privileged Context Self-Distillation"
type: canonical
aliases: ["self-distillation", "OPSD", "privileged self-distillation", "destilacao auto-supervisionada", "contexto privilegiado", "PI distillation"]
tags: ["agentes-orquestracao", "context-engineering", "evals"]
last_updated: 2026-06-16
relates-to:
  - "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]"
  - "[[docs/canonical/external-state-persistence|External State Persistence]]"
  - "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]"
  - "[[docs/canonical/summary-buffer-continuity|Summary Buffer Continuity]]"
  - "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]"
  - "[[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]"
  - "[[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|OPD Classification]]"
sources:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]"
---

# Privileged Context Self-Distillation

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]]
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

A long-running agent needs access to full session logs, complete source documents, architecture diagrams, and troubleshooting playbooks during execution — information that cannot fit in the runtime context window. The agent either omits this information entirely (operating blind on complex decisions) or pays the full context cost every time (loading 40K tokens of documentation for a 2K-token decision).

Concretely: a KODA agent handling a disputed order needs access to the full conversation history (200+ messages), the product catalog entry with all variants, the payment gateway error trace, and the warehouse inventory snapshot. Loading all of this into the context window costs 28K tokens and 3.2 seconds. The agent does this for every dispute — even the 70% that resolve in 3 steps. The ops team knows which information matters because they've handled 500 disputes, but that knowledge is trapped in human experience, not in the agent's operating knowledge.

The underlying mechanism mirrors On-Policy Self-Distillation from ML: the same model is run under two different context views — a privileged teacher view with full information, and a restricted student view with runtime context. The per-token log-ratio between the two views reveals which privileged information changed the agent's decisions. Those deltas are distilled into compact runtime rules that the agent can use without loading the full privileged source.

## Solution

Run the same agent under two different context views on the same task: a teacher view with full privileged information (complete logs, documents, reference answers) and a student view with only runtime-available context. Compare the outputs to identify where privileged context changed the decision, confidence, or reasoning. Distill the useful deltas — the specific facts that made a difference — into compact runtime artifacts: prompt rules, skills, memory writebacks, or eval cases. Calibrate the distilled agent under the runtime view to confirm the knowledge transferred without the privileged source.

```
+------------------+     +--------------------+     +--------------------+
| Same task prompt | --> | Teacher View       | --> | Delta extraction:  |
|                  |     | agent(x, PI)       |     | where did PI       |
|                  |     | full logs, docs,   |     | change the output? |
+------------------+     | reference answers  |     +--------+-----------+
                          +--------------------+              |
                          +--------------------+              |
                          | Student View       |              |
                          | agent(x)           |              |
                          | runtime context    |              |
                          +--------------------+              |
                                                              v
+------------------+     +--------------------+     +--------------------+
| Calibrate under  | <-- | Distill deltas     | <-- | Useful PI deltas   |
| runtime view     |     | into compact       |     | (facts that changed|
| (no PI)          |     | runtime artifacts  |     | decisions)         |
+------------------+     +--------------------+     +--------------------+
```

**Core rules:**

| Component | Requirement |
|---|---|
| Dual-view execution | Same agent, same task, two context views: teacher (privileged) and student (runtime) |
| Delta identification | Compare outputs to identify where privileged information changed the decision, confidence, or reasoning |
| Distillation target | Compact runtime artifacts: prompt rules, skill instructions, memory writebacks, durable facts, eval cases |
| Calibration | Verify that the distilled agent performs equivalently under the runtime view (no privileged information) |
| Privileged information types | Full session logs, stack traces, reference solutions, architecture diagrams, complete source documents, troubleshooting playbooks |
| Safety | Secrets and private data must not be distilled into reusable artifacts |

The power of this pattern is that it does not require a larger teacher model — the same agent serves as both teacher and student, with the only difference being the information available at decision time. This converts expensive design-time analysis into reusable operating knowledge that reduces token cost at runtime.

## Implementation in this repo

### What already exists

- `Hybrid Context Stack` [[docs/canonical/hybrid-context-stack|hybrid-context-stack.md:20-42]] assembles context from ordered layers (stable prompt, durable state, head/tail anchors, summaries, recoverable omitted middle). This is the architecture that would consume distilled rules.
- `External State Persistence` [[docs/canonical/external-state-persistence|external-state-persistence.md:31-57]] decouples agent memory from model memory: durable facts persist across sessions while active context is rebuilt. This is the surface where distilled knowledge would land as compact rules.
- `Head-Tail Context Truncation` [[docs/canonical/head-tail-context-truncation|head-tail-context-truncation.md:26-39]] keeps bounded active context with recoverable middle — the middle is analogous to privileged information that cannot fit at runtime but can be fetched on demand.
- `Summary Buffer Continuity` [[docs/canonical/summary-buffer-continuity|summary-buffer-continuity.md]] compresses older history into a portable buffer — analogous to the distillation target that converts full context into compact operating knowledge.
- `Budget-Aware Session Handoff` [[docs/canonical/budget-aware-session-handoff|budget-aware-session-handoff.md:62-75]] passes compressed state (summary buffer, durable facts, recoverable handles) between sessions — the runtime consumption of distilled knowledge.
- `Durable Fact Selective History` [[docs/canonical/durable-fact-selective-history|durable-fact-selective-history.md]] extracts and preserves durable facts from history, which is structurally similar to identifying which privileged information matters.

### What is missing

1. No explicit teacher-view (privileged) vs. student-view (runtime) comparison using the same agent on the same task.
2. No delta extraction: where did privileged context change the agent's decision, confidence, or reasoning?
3. No distillation from teacher-view delta to compact runtime rules with calibration under the runtime view.
4. The repo has the "compact context at runtime" side (Hybrid Context Stack, External State Persistence) but not the "design-time self-distillation from privileged information" loop.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Converts expensive full-context analysis into reusable operating knowledge | Privileged information can leak into outputs as false confidence or unreachable assumptions |
| Does not require a larger teacher model — the same agent can be compared under different context views | Secrets or private data must not be distilled into reusable artifacts |
| Supports context-management systems where the training/review phase sees more than production can carry | Calibration must be measured under the runtime view, not under the privileged teacher view |
| Reduces token cost and latency by replacing full-context loads with compact distilled rules | The dual-view comparison adds design-time compute cost for each distillation cycle |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] as the target architecture that consumes distilled rules.
- **Depends on:** [[docs/canonical/external-state-persistence|External State Persistence]] as the surface where distilled knowledge lands as durable facts.
- **Complements:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] — the middle is the privileged information that self-distillation converts to runtime-accessible knowledge.
- **Complements:** [[docs/canonical/summary-buffer-continuity|Summary Buffer Continuity]] — the summary buffer is the output format; self-distillation is the production process.
- **Complements:** [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]] — selective extraction of facts is the distillation target; self-distillation provides the delta signal that identifies which facts matter.
- **Validated by:** [[docs/canonical/magnitude-direction-verifier-split|Magnitude-Direction Verifier Split]] — the verifier split provides the external grounding that prevents the self-distillation from reinforcing overconfidence.
- **Feeds:** [[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]] — distilled rules reduce the context payload that must be handed off between sessions.

## Failure modes

- **Information leakage:** The student learns to imitate the form of teacher outputs (confidence, structure, vocabulary) without the underlying privileged reasoning, producing outputs that "sound right" but are incorrect. Mitigation: calibrate exclusively under the runtime view; the teacher view is only for delta identification, never for performance measurement.
- **PI overconfidence:** The teacher under privileged information produces higher-confidence outputs. Distilling that confidence as a target gives the student unjustified certainty. Mitigation: separate confidence calibration from knowledge distillation; measure calibration separately under the runtime view.
- **Secrets in artifacts:** Privileged information containing secrets, credentials, or private data gets distilled into reusable rules and leaks. Mitigation: privacy filter before distillation; rules must reference information categories, not specific data values.
- **Stale distillation:** The distilled rules become outdated as the privileged information changes (new product catalog, updated playbook, revised architecture). Mitigation: version the distilled artifacts with source timestamps; trigger re-distillation when privileged sources change.

## Verification / eval hooks

- Add at least one regression or eval case before relying on this pattern in production.
- Capture the input trace, expected decision, observed decision, and evaluator/verifier output.
- Record which existing canonical pattern this one complements and which failure mode it is meant to reduce.
- Re-run the relevant eval tier after changing prompts, skills, memory policy, or harness routing.

## References

- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:60-70` — self-distillation as dissociation between professor and external model.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:98-108` — log-ratio as advantage without reward model.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns.md:65-89` — extracted pattern with inputs, outputs, benefits, limitations.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification.md:100-131` — Partial Coverage classification with evidence.
- `docs/canonical/hybrid-context-stack.md:20-42` — layered context assembly.
- `docs/canonical/external-state-persistence.md:31-57` — durable state for compact runtime knowledge.
- `docs/canonical/head-tail-context-truncation.md:26-39` — recoverable privileged-like middle.
