---
title: "Resolver-Based Context Progressive Disclosure"
type: canonical
tags: ["context-engineering", "agentes-orquestracao", "evals"]
aliases: ["resolver progressive disclosure", "skill context disclosure", "load-on-demand skills", "context progressive disclosure"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]"]
sources: ["[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]]"]
---
# Resolver-Based Context Progressive Disclosure

**Type:** canonical
**Status:** active
**Source:** Stanford CS153 AI Native Company analysis
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Monolithic instruction files degrade long-running agents. Every correction, preference, workflow, and domain rule gets loaded into every task, even when most of it is irrelevant. The result is token pressure, prompt interference, stale guidance, and context overflow.

The pattern solves instruction bloat by replacing always-on global context with resolver-driven, task-specific disclosure.

## Solution

Move rarely universal instructions out of the base prompt and into skills or documents that the resolver loads only when the task matches their trigger contract.

Resolver-based disclosure has five parts:

| Part | Purpose |
|---|---|
| Thin base context | Keep only universal operating rules, safety constraints, and source-of-truth precedence always loaded |
| Capability directory | Store workflow, domain, and implementation guidance as individually loadable skills or docs |
| Positive triggers | Define when a task should load the capability |
| Negative triggers | Define when similar tasks should not load the capability |
| Trigger evals | Test whether realistic tasks load the right capability and avoid the wrong one |

The resolver becomes the context router. It does not merely save tokens; it defines which operational memory is allowed to influence a task. Good progressive disclosure therefore needs both recall and precision. A resolver that misses required guidance creates silent failure, while a resolver that loads too much recreates the monolithic prompt.

## Implementation in this repo

### What already exists

- [[.opencode/skills/issue-start/SKILL|issue-start skill]] lines 16-23 defines a narrow task-scoped load condition for starting issue work.
- [[.opencode/skills/issue-review/SKILL|issue-review skill]] lines 16-23 defines a separate load condition for validation, PR preparation, and second-agent review.
- [[.opencode/skills/issue-review/SKILL|issue-review skill]] lines 38-40 requires context compaction before CI and PR creation.
- [[.opencode/skills/issue-finish/SKILL|issue-finish skill]] lines 18-24 narrows merge and cleanup to a separate mechanical context after explicit approval.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]] keeps invariant harness instructions stable while other context is reduced.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] and [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] address context recovery once old context has been omitted.

### What is missing from the pattern

The classification found Partial Coverage because the repo uses load-on-demand skills and compaction guidance, but does not formalize the resolver as a tested progressive-disclosure layer.

Missing pieces:

1. Positive and negative trigger examples for each operational skill.
2. Trigger evals that measure whether skill loading works on realistic task prompts.
3. Resolver miss handling: what an agent should do when a required skill was not loaded, or when two skills overlap.
4. A replacement strategy for monolithic instruction growth: when a new global rule must stay global, and when it must become a skill.
5. Observability for loaded, skipped, and incorrectly loaded capabilities.
6. Deduplication policy for overlapping skills and stale triggers.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Reduces token pressure and prompt interference | Requires taxonomy and trigger maintenance |
| Lets the instruction library grow without charging every task the full context cost | Resolver misses can silently remove needed guidance |
| Makes context architecture explicit and testable | Trigger evals can be misleading if they are too synthetic |
| Encourages focused skills instead of global prompt patches | Duplicate or overlapping skills need governance |

## Relationship to Other Patterns

- **Enables:** [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]], because a skill is only a capability if it can be resolved at the right time.
- **Feeds:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]], because the operating system routes work through resolver-visible capabilities.
- **Complements:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]], which protects universal harness instructions while progressive disclosure keeps non-universal guidance out of base context.
- **Complements:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] and [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]], which recover omitted session state rather than routing capability instructions.
- **Should be evaluated by:** [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]] when resolver behavior must survive long sessions and compaction.
- **Grounded by:** [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]] pattern 5.

## References

- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]] lines 98-118 - extracted resolver progressive disclosure pattern.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]] lines 76-91 - Partial Coverage classification and High integration value.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]] lines 88-92 - resolver mechanics for loading task-specific skills.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]] lines 148-150 - Claude.md growth as context architecture smell.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]] lines 197-200 - token overflow, duplicate skill, and trigger-eval failure modes.
- [[.opencode/skills/issue-start/SKILL|issue-start skill]] lines 16-23 - current load-on-demand issue setup skill.
- [[.opencode/skills/issue-review/SKILL|issue-review skill]] lines 16-23 and 38-40 - current review skill trigger and compaction gate.
- [[.opencode/skills/issue-finish/SKILL|issue-finish skill]] lines 18-24 - current finish skill trigger.

---

*Created: 2026-06-10 | From: Stanford CS153 pattern classification | Precedence: canonical*
