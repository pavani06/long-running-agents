---
title: "Adaptive Style Compression Teacher"
type: canonical
aliases: ["CRISP compression", "adaptive compression", "style compression", "compressao adaptativa", "compressao por dificuldade", "uncertainty preservation"]
tags: ["agentes-orquestracao", "context-engineering", "evals"]
last_updated: 2026-06-16
relates-to:
  - "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]"
  - "[[docs/canonical/summary-buffer-continuity|Summary Buffer Continuity]]"
  - "[[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]"
  - "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]"
  - "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]"
  - "[[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]]"
  - "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification|OPD Classification]]"
sources:
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|Policy Distillation Analysis]]"
  - "[[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns|Policy Distillation Patterns]]"
---

# Adaptive Style Compression Teacher

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis|OPD Analysis]]
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Context compression strategies apply fixed rules to every task regardless of difficulty. An easy product lookup gets the same head+tail truncation as a multi-step order dispute with conflicting constraints, payment gateway errors, and inventory exceptions. The compression either keeps too much context on easy tasks (wasting tokens) or cuts too aggressively on hard tasks (removing critical deliberation).

Worse: fixed compression strategies disproportionately suppress hedging phrases, uncertainty markers, and open decisions — the tokens of highest entropy that a privileged teacher view would drop. The resulting compressed context is shorter but transmits false confidence, inducing downstream agents to treat uncertain information as certain.

Concretely: a KODA agent compresses its session history for handoff. The compression policy keeps the last 3 turns + summary of earlier turns. For a simple "check order status" task (3 turns total), this is fine. For a complex "resolve disputed multi-item order with warehouse exception" task (22 turns), the summary of turns 1-19 strips the agent's explicit hedging from turn 8 ("I'm not sure about the warehouse availability — let me check") and turn 14 ("the inventory system returned an unexpected status — this may be a data issue"). The receiving agent sees a confident summary that says "warehouse checked, inventory confirmed" and proceeds with false certainty, generating a wrong resolution.

The underlying mechanism mirrors CRISP from On-Policy Distillation: a style instruction ("be concise") conditions the teacher to produce compressed outputs, and reverse KL makes the student mode-seek toward dense tokens. The natural behavior: compression is stronger on easy problems (where deliberation is unnecessary) and weaker on hard problems (where the conciseness instruction competes with the need for reasoning). For agents, this means compression should adapt to task difficulty, not apply a fixed policy.

## Solution

Condition compression on task difficulty signals: verifier uncertainty, unresolved constraint count, failed attempts, dependency depth, and outcome ambiguity. On easy tasks, compress aggressively (terse summaries, minimal context). On hard tasks, preserve deliberation, uncertainty markers, and open decisions. Validate compressed context through downstream task evals that compare task success and calibration using compressed vs. full context.

```
Task enters agent loop
        |
        v
+---------------------------+
| Task Difficulty Assessment |
+---------------------------+
| Signals:                  |
| - Verifier uncertainty    |
| - Unresolved constraints  |
| - Failed attempt count    |
| - Dependency depth        |
| - Outcome ambiguity       |
+---------------------------+
        |
   +----+----+
   |         |
[EASY]    [HARD]
   |         |
   v         v
+--------+  +--------+
|Aggres- |  |Preserve|
|sive    |  |deliber-|
|compres-|  |ation,  |
|sion    |  |uncer-  |
|        |  |tainty, |
|Terse   |  |open    |
|summary |  |decisions|
+--------+  +--------+
   |         |
   +----+----+
        |
        v
+---------------------------+
| Downstream Task Eval      |
| Compare:                  |
| - Task success (compressed|
|   vs. full context)       |
| - Calibration (confidence |
|   accuracy)               |
| - Uncertainty preservation|
|   (hedging retention)     |
+---------------------------+
```

**Core rules:**

| Component | Requirement |
|---|---|
| Difficulty signal extraction | Verifier uncertainty, unresolved constraints, failed attempts, dependency depth, outcome ambiguity |
| Compression policy | Map difficulty to compression strength: easy -> aggressive, hard -> preserve deliberation |
| Uncertainty preservation | Explicitly retain hedging phrases, confidence qualifiers, open decisions, and unresolved items in compressed output |
| Downstream eval | Compare task success rates and calibration between runs with compressed context and runs with full context |
| Compression audit | Log what was compressed, what was preserved, and the difficulty signal that drove the decision |
| Re-compression trigger | When downstream eval shows degradation, re-compress with adjusted policy and re-validate |

The key deviation from fixed-rule compression: the difficulty signal controls *how much* to compress and *what* to preserve. An easy task that resolves in 3 deterministic steps gets a 2-sentence summary. A hard task with 5 unresolved constraints and 3 failed attempts preserves the agent's deliberation traces, hedging, and open decisions even if it costs extra tokens.

## Implementation in this repo

### What already exists

- `Head-Tail Context Truncation` [[docs/canonical/head-tail-context-truncation|head-tail-context-truncation.md:26-39]] keeps bounded active context with head, tail, latest result, and recoverable middle. This is a compression strategy, but operates on fixed rules (always keep head + tail + latest result), not adaptive to task difficulty.
- `Summary Buffer Continuity` [[docs/canonical/summary-buffer-continuity|summary-buffer-continuity.md]] compresses older history into a portable, incrementally updated buffer without adapting strength to task signals.
- `Durable Fact Selective History` [[docs/canonical/durable-fact-selective-history|durable-fact-selective-history.md]] selects and preserves durable facts from history — selective by fact type (durable vs. transient), not by task difficulty.
- `Budget-Aware Session Handoff` [[docs/canonical/budget-aware-session-handoff|budget-aware-session-handoff.md:27-62]] triggers handoff based on budget thresholds, not task difficulty signals. The compression trigger is budget-driven, not difficulty-driven.
- `Hybrid Context Stack` [[docs/canonical/hybrid-context-stack|hybrid-context-stack.md:20-42]] assembles context from ordered layers — defines what goes into context, not how compression adapts to difficulty.
- `Semantic Topic Bucketing` [[docs/canonical/semantic-topic-bucketing|semantic-topic-bucketing.md]] groups context by topic — a structuring strategy rather than difficulty-adaptive compression.
- `Eval to Production Correlation Tracking` [[docs/canonical/eval-to-production-correlation-tracking|eval-to-production-correlation-tracking.md:50-76]] ties eval scores to production outcomes — can validate whether compressed context degrades real outcomes.

### What is missing

1. No adaptive compression strength conditioned on task difficulty signals (verifier uncertainty, unresolved constraints, failed attempts, dependency depth).
2. No explicit preservation of uncertainty markers, hedging, and open decisions in compressed output.
3. No downstream eval validating that compressed context preserves task success and calibration compared to full context.
4. All current strategies apply fixed rules regardless of whether the task is simple or complex.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Saves tokens on easy tasks without reducing context management to a fixed truncation rule | Style compression can still suppress important hedging if not explicitly evaluated |
| Aligns summary length with task difficulty rather than with a static budget alone | A single style instruction may conflict with domain requirements for auditability or legal precision |
| Protects downstream agents from epistemic suppression caused by overconfident summaries | Requires downstream evals; shorter traces are not automatically better traces |
| Adapts naturally: as tasks become harder, compression eases off without manual policy changes | Difficulty signal extraction adds per-task overhead before compression begins |

## Relationship to Other Patterns

- **Extends:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] by adding task-difficulty-conditioned compression strength to the existing head+tail+recoverable-middle architecture.
- **Extends:** [[docs/canonical/summary-buffer-continuity|Summary Buffer Continuity]] by conditioning summary compression on task difficulty and preserving uncertainty markers.
- **Complements:** [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]] — the adaptive compression decides *how much* to compress; selective history decides *what* to keep.
- **Complements:** [[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]] — the budget trigger determines *when* to compress; adaptive compression determines *how aggressively*.
- **Validated by:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — downstream evals validate that compressed context doesn't degrade production outcomes.
- **Complements:** [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] — the stack defines the context layers; adaptive compression controls how each layer is compressed based on task difficulty.

## Failure modes

- **Epistemic suppression:** Compression removes uncertainty markers and hedging, producing outputs that are shorter but more confidently wrong. Mitigation: explicit preservation rules for hedging phrases, confidence qualifiers, and open decisions; downstream eval specifically checks calibration, not just task success.
- **Difficulty signal noise:** Task difficulty signals (verifier uncertainty, constraint count) fluctuate with model temperature and prompt variation, causing compression to oscillate between aggressive and preservation modes on the same task class. Mitigation: smooth difficulty signals over a window; use hysteresis to prevent oscillation.
- **Compression asymmetry:** Easy tasks are compressed aggressively, creating a feedback loop where downstream agents never see the detailed reasoning that hard tasks preserve, and therefore never learn to handle compressed context. Mitigation: periodically run easy tasks with preservation-mode compression to validate that the agent can handle both modes.
- **Style override:** A global "be concise" instruction conflicts with domain-specific requirements for audit trails, legal precision, or regulatory compliance that demand verbatim preservation. Mitigation: per-domain compression policies; some domains (legal, financial) may use a fixed preservation policy regardless of difficulty.

## Verification / eval hooks

- Add at least one regression or eval case before relying on this pattern in production.
- Capture the input trace, expected decision, observed decision, and evaluator/verifier output.
- Record which existing canonical pattern this one complements and which failure mode it is meant to reduce.
- Re-run the relevant eval tier after changing prompts, skills, memory policy, or harness routing.

## References

- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:118-124` — CRISP style instruction for automatic difficulty-adaptive compression.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-analysis.md:170-174` — epistemic suppression: compression removes uncertainty markers.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-patterns.md:165-189` — extracted pattern with inputs, outputs, benefits, limitations.
- `docs/analysis/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language/2026-06-16-the-imitation-game-state-of-policy-distillation-in-language-classification.md:237-273` — Partial Coverage classification with evidence.
- `docs/canonical/head-tail-context-truncation.md:26-39` — fixed-rule head+tail context reduction.
- `docs/canonical/summary-buffer-continuity.md` — continuous compressed summary buffer.
- `docs/canonical/durable-fact-selective-history.md` — selective fact retention.
- `docs/canonical/budget-aware-session-handoff.md:27-62` — budget-driven compression trigger.
