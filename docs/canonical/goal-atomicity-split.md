---
title: "Goal Atomicity Split"
type: canonical
tags: ["agentes-orquestracao", "spec-driven-development", "decision-discipline", "governanca"]
aliases: ["goal atomicity", "one goal one sentence", "goal splitting", "no and in goals", "atomic goals", "goal decomposition", "conjunction split"]
last_updated: 2026-06-14
relates-to: ["[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]]", "[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]", "[[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]]", "[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]", "[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Anatomy of Intent Classification]]"]
---

# Goal Atomicity Split

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/
**Classification:** Missing, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Multi-goal intents hide coordination complexity behind a single sentence, causing agents to optimize for one part while silently dropping another. A goal like "Add dark mode and improve accessibility" asks the agent to pursue two distinct outcomes -- visual theme support and accessible interaction patterns -- but presents them as one. The agent will likely do a good job on one and a shallow job on the other, or do both poorly. The hidden coordination (which depends on which, whether they interact, which should be validated first) is left for the agent to resolve silently.

The source names this as a hidden coordination problem: "Multi-goal intents hide coordination complexity behind a single sentence, causing agents to optimize for one part while silently dropping another" ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|patterns]]:84-85).

The repo decomposes work through vertical-slice-issue-generation and plan-execute-verify, but has no rule that enforces goal atomicity through conjunction scanning. No canonical doc, skill, or curriculum lesson teaches "if the goal needs 'and,' it's two goals" ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:122-129).

## Solution

Enforce goal atomicity through a simple linguistic rule: one goal equals one sentence with one outcome. When a conjunction ("and," "or," "then," "while," "also") appears in a goal sentence, split it into separate goals. Each resulting goal describes exactly one outcome. Dependency ordering between split goals is recorded separately in the orchestration layer.

**The split rule:**

| Signal | Action | Example |
|---|---|---|
| "and" connecting two verbs or outcomes | Split into two goals | "Add dark mode and improve accessibility" → Goal 1: "The app supports a dark color theme." Goal 2: "Interactive elements meet WCAG 2.1 AA contrast ratios." |
| "then" indicating sequential steps | Split into sequential goals with dependency | "Validate the payment then confirm the order" → Goal 1: "Payment validation returns success or specific failure reason." Goal 2: "Confirmed orders update inventory and trigger fulfillment." Depends on: Goal 1. |
| "or" indicating alternatives | The goal may be ambiguous about what the outcome is | "Send email or push notification" → Clarify with the outcome owner: which outcome is primary? Split if both are valid separate outcomes. |
| "while" indicating concurrent outcomes | Split into parallel goals | "Resize images while maintaining metadata" → Goal 1: "Uploaded images are resized to the configured dimensions." Goal 2: "Image metadata (EXIF, copyright, geotag) is preserved through resize." |

**Dependency tracking after split:**

When a multi-goal sentence is split, the relationships between the resulting goals must be made explicit:

1. **Independent goals.** The split goals do not depend on each other. They can be executed in parallel or in any order.
2. **Sequential goals.** Goal B depends on Goal A completing successfully. The dependency is recorded as `Goal B depends on Goal A`.
3. **Interacting goals.** The split goals share a dependency (e.g., both modify the same component). The shared dependency is recorded, and the goals are sequenced or coordinated to avoid conflicts.

The orchestration layer -- not the intent -- handles dependency ordering. The intent contains atomic goals; the orchestration layer holds the dependency graph between them.

**Why atomic goals scale better:**

Atomic goals help orchestration systems route, parallelize, or sequence work safely. When each intent has one outcome, the orchestrator can:
- Assign goals to different agents in parallel.
- Sequence goals by explicit dependency, not implicit sentence order.
- Validate each outcome independently -- a failure in one goal does not invalidate other goals.
- Track completion per outcome, not per sentence.

Non-atomic goals collapse all of this into one opaque unit. The orchestrator cannot see inside the sentence to schedule or validate the parts.

**Limits of the rule:**

Applied mechanically, the conjunction rule can create too many tiny tasks. Judgment is required: does the conjunction actually encode two distinct outcomes, or is it a natural-language idiom? "The API is fast and reliable" is not two goals -- it is one quality statement whose atomicity is not broken by the "and." The rule applies to outcome verbs, not to adjectives or qualifiers.

## Implementation in this repo

### What already exists

- [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] -- generates single-purpose vertical slices with observable behavior. Conceptually adjacent to atomic goals but uses a different decomposition method (cross-layer behavior) rather than conjunction-based splitting of goal statements.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-60 -- separates work into three explicit phases. Adjacent to work decomposition but at the plan phase level, not the goal atomicity level.
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- the description field is where the atomicity rule applies. A completeness gate could check whether the description field contains one sentence with one outcome.
- [[.opencode/skills/refine-issue/SKILL|refine-issue skill]] -- decomposes issues into sub-issues with dependencies. Structurally adjacent to goal splitting but uses issue decomposition logic, not goal-language heuristics.
- [[.opencode/skills/issue-start/SKILL|issue-start skill]] -- creates isolated worktrees for individual issues. Atomic goals would create cleaner, more focused issues for this workflow.

### What is missing from the pattern

The classification marks Goal Atomicity Split as Missing because no rule, heuristic, or gate enforces goal atomicity through conjunction scanning ([[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|classification]]:122-129).

Missing items:

1. The conjunction-scanning rule itself as a named, documented heuristic. No repo artifact states "one goal equals one sentence, no 'and' -- split on conjunction."
2. A pre-flight gate that scans goal statements for conjunctions during intent authoring, applied by the intent-five-part-primitive skill or the Grill-Me alignment interview.
3. Dependency tracking for split goals: when a conjunction triggers a split, the resulting goals need explicit dependency ordering recorded in the orchestration layer.
4. Curriculum content teaching atomic goal decomposition as a concrete discipline, with before/after examples showing multi-goal sentences versus atomic goals.
5. Integration with the intent-five-part-primitive skill: the description field completeness gate could include an atomicity check alongside the non-empty check.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Scales agent work by decomposition instead of by dense mega-prompts -- one outcome per intent | Can create too many tiny tasks if applied mechanically without judgment |
| Makes validation sharper because each output has one primary outcome to check | Requires dependency tracking once one overloaded goal becomes several tasks |
| Helps orchestration systems route, parallelize, or sequence work safely with explicit dependencies | Does not solve ambiguous constraints or weak evals on the resulting goals |
| Makes completion tracking precise: an atomic goal is either done or not done | The overhead of creating separate intents may not be worth it for trivial, naturally co-dependent goals |
| Pairs with Two-Implementations Goal Test and Constraint Budget Gate as a trio of lightweight intent-quality heuristics | Ambiguous conjunctions in natural language require human judgment about what counts as a separate outcome |

## Relationship to Other Patterns

- **[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]** -- the description field is where the atomicity rule applies. The completeness gate for the description field should include an atomicity check: does the description contain exactly one outcome?
- **[[docs/canonical/two-implementations-goal-test|Two-Implementations Goal Test]]** -- atomicity and purity are complementary quality checks. Apply atomicity first (split on conjunctions), then the two-implementations test to each atomic goal (is it an outcome, not a spec?).
- **[[docs/canonical/three-part-intent-contract|Three-Part Intent Contract]]** -- the goal slot in the three-part contract should be atomic. A multi-goal sentence violates the contract because it smuggles multiple outcomes into one slot.
- **[[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]]** -- atomic goals generate cleaner vertical slices because each slice maps to one observable outcome. A multi-goal sentence generates a muddy slice that tries to show multiple things at once.
- **[[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]** -- atomic goals produce tighter plans because each plan addresses exactly one outcome. Non-atomic goals produce sprawling plans that try to solve multiple problems in one pass.
- **[[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]** -- the interview can apply the conjunction scan as a diagnostic question: "Your goal says 'and.' Are these two separate outcomes? Should they be separate intents?"
- **[[docs/canonical/ice-craft-separation|ICE Craft Separation]]** -- atomic intents make the Intent craft more precise: each intent is one outcome, not an overloaded wishlist.

## References

- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]:82-102 -- extracted pattern: Goal Atomicity Split
- [[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-classification|Classification]]:112-138 -- classification evidence: Missing, Medium integration value
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- the description field where the atomicity rule applies
- [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] -- adjacent pattern: cross-layer behavior decomposition
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-60 -- phase-gated execution that benefits from atomic goals
