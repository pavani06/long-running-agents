---
title: "N+1 Long-Session Evals"
type: canonical
aliases: ["n+1 evals", "long session evals"]
tags: ["evals", "context-engineering"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]", "[[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]", "[[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics Concept]]"]
sources: ["[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis|Context Management Analysis]]"]
---
# N+1 Long-Session Evals

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-09-how-we-solved-context-management-in-agents/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Context bugs often appear only after many turns. A context strategy can pass single-turn tests, short conversations, and token-budget checks while still failing when a user asks a follow-up after the active window has been compacted.

The failure mode is behavioral: the agent forgets a prior constraint, treats a follow-up as a new conversation, retrieves the wrong omitted item, or loses the latest state after a long session. Testing prompt size alone does not catch this.

## Solution

Evaluate the production context strategy by loading N turns, applying the same context-building, truncation, memory, and delegation logic used in production, then testing turn N+1.

```
1. Load a realistic N-turn conversation fixture.
2. Apply the production context strategy.
3. Ask the next-turn prompt that depends on earlier context.
4. Grade continuity, reference resolution, and task correctness.
5. Fail the eval when the answer behaves as if required context was unavailable.
```

The N+1 turn should force the context strategy to prove that the right information survived or can be recovered. Good fixtures include follow-ups that refer to earlier products, decisions, constraints, tool outputs, user preferences, trace spans, or unresolved work.

The eval result is not merely "within token budget". The pass condition is that the agent behaves correctly after the full production context policy has run.

## Implementation in this repo

### What already exists

The repo already has the evaluation vocabulary and adjacent long-session practices:

- The source analysis defines the target mechanic as loading 10 turns, applying the normal context and memory strategy, and testing the 11th turn (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:98`).
- Harness Improvements proposes a sample of 50 long conversations for compaction shadow tests (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:570`).
- Harness Improvements also prescribes measuring critical-fact retention in long, noisy conversations after shadow compaction (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:1030`).
- The harness evolution playbook includes a regression battery for long conversations, incomplete responses, and context limits (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`).

### What is missing

The classification found no named `N+1` long-session eval in the canonical docs, curriculum, evidence, decisions, or operational skills outside this analysis output (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md:64`). Existing tests are broader long-conversation or harness-evolution checks; this pattern names the precise fixture shape.

The missing implementation details are:

1. A fixture format for N-turn histories plus expected N+1 behavior.
2. A runner that applies the production context strategy before grading the N+1 prompt.
3. Rubrics for continuity, reference resolution, retrieval correctness, and task correctness.
4. A reporting convention that ties failures to truncation, catalog, memory, or prompt-stability causes.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Converts late-session forgetting into a reproducible regression | Requires realistic multi-turn fixtures and maintenance |
| Tests behavior after production context reduction, not just prompt size | Covers only the regimes represented by fixtures |
| Catches over-truncation, lossy summaries, and wrong retrieval | More expensive than single-turn unit tests |
| Creates evidence for context-strategy changes before rollout | Grading can require a rubric or judge model for nuanced answers |

## Relationship to Other Patterns

- **Validates:** Head-Tail Context Truncation with Recoverable Middle by proving follow-ups still work after the middle is omitted.
- **Validates:** Addressable Memory Catalog by exposing whether the agent can select and fetch the right ID.
- **Depends on:** Stable Harness Prompt During Context Reduction, because the eval should test context strategy, not accidental prompt mutation.
- **Feeds:** Late-Failure Regression Suite, because any observed N+1 failure should become a durable regression case.
- **Complements:** Harness shadow testing and canary rollout practices already present in the curriculum.

## References

- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:98` — source N+1 eval mechanism.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-patterns.md:106` — extracted long-session N+1 pattern.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md:52` — Partial Coverage classification and gap.
- `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:570` — long-conversation compaction shadow tests.
- `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:1030` — critical-fact retention in long noisy conversations.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741` — regression battery for long conversations and context limits.

---

*Created: 2026-06-10 | From: Context Management pattern classification | Precedence: canonical*
