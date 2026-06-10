# Late-Failure Regression Suite

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-09-how-we-solved-context-management-in-agents/
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Late-session context failures are easy to treat as one-off incidents: a user asks a follow-up after many turns, the agent forgets a constraint, a retrieval handle is missing, or a context strategy that once worked degrades after real sessions become longer.

If those failures are only fixed ad hoc, they can recur when truncation thresholds, summaries, retrieval, prompts, or sub-agent boundaries change. The system needs a named regression suite specifically for failures that appear late in long sessions.

## Solution

Turn every observed late-session context failure into a durable regression case. The suite should preserve the session shape, the context strategy used, the expected N+1 behavior, and the root-cause category.

Recommended case fields:

| Field | Purpose |
|---|---|
| `case_id` | Stable regression identifier |
| `session_fixture` | N-turn history or trace needed to reproduce the late failure |
| `next_turn` | N+1 prompt that exposed the failure |
| `expected_behavior` | Continuity, reference resolution, retrieval, or task outcome required |
| `context_strategy` | Prompt version, truncation policy, catalog version, memory policy, delegation policy |
| `failure_class` | Over-truncation, missing catalog item, wrong retrieval, stale summary, prompt mutation, sub-agent loss |
| `evidence` | Links to incident, analysis, trace, or eval output |

The suite should run before context-strategy changes ship, during harness canaries, and after any incident fix. Its purpose is narrower than a general harness regression battery: it protects against late-session context degradation.

## Implementation in this repo

### What already exists

The repo already has mature regression and rollout practices that this suite can build on:

- The evaluation rubric template requires applying rubrics to old incident outputs as a regression set and using real problem outputs as regression examples (`curriculum/08-tools-templates/evaluation-rubric-template.md:812`).
- The harness evolution playbook requires regression tests before canary, staged rollout with shadow diffs, canary metrics, rollback decisions, and 14-day observation (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`).
- Harness Improvements defines comparison-controlled shadow testing, rollback or disablement, technical ownership, and review cadence as acceptance criteria (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:480`).
- The source analysis identifies late-session forgetting and N+1 evals as the mechanism for turning context degradation into a reproducible bug (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:50`).

### What is missing

The classification found no named late-session context regression suite in the canonical docs, curriculum, evidence, decisions, or operational skills (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/classification.md:95`). Existing suites are broader harness and rubric regressions rather than a first-class family for late context failures.

The missing implementation details are:

1. A suite name and ownership model for late-session context regressions.
2. A fixture convention that stores enough prior session context to reproduce failures.
3. A failure taxonomy tied to context strategy components.
4. A gate that runs this suite before changing truncation, retrieval, prompt, memory, or delegation policies.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Prevents fixed late-session failures from recurring | Requires curation of realistic long-session fixtures |
| Gives context-strategy changes a focused regression gate | Test runs can be slower and more expensive than unit tests |
| Turns user or eval incidents into durable engineering evidence | Requires root-cause labeling discipline |
| Complements canary and shadow testing with targeted historical failures | Can overfit if the suite is not refreshed with new usage patterns |

## Relationship to Other Patterns

- **Consumes:** N+1 Long-Session Evals, because failing N+1 cases are natural regression seeds.
- **Validates:** Head-Tail Context Truncation with Recoverable Middle after thresholds or payload structures change.
- **Validates:** Addressable Memory Catalog by locking in cases where catalog handles or previews previously failed.
- **Protects:** Stable Harness Prompt During Context Reduction by detecting prompt mutation as a late-session failure class.
- **Complements:** Harness evolution canaries, rollback policy, and rubric regression practices already present in the curriculum.

## References

- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:50` — context quality as observable through long-session evals.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md:221` — late-session forgetting failure pattern.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/classification.md:84` — Partial Coverage classification and gap.
- `curriculum/08-tools-templates/evaluation-rubric-template.md:812` — old incident outputs as regression examples.
- `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741` — regression tests before canary rollout.
- `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:480` — shadow testing, rollback, ownership, and review cadence.

---

*Created: 2026-06-10 | From: Context Management pattern classification | Precedence: canonical*
