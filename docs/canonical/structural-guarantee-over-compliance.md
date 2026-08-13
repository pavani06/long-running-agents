---
title: "Structural Guarantee over Compliance"
type: canonical
tags: ["governanca", "gate-design", "verification", "process", "decision-discipline"]
aliases: ["garantia estrutural vence obediência", "structural guarantee", "guarantee over compliance", "put the rule in the gate", "compliance fails under load", "knowing is not preventing"]
last_updated: 2026-08-13
relates-to: ["[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/operator-channel-authority|Operator-Channel Authority]]"]
sources: ["[[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Dispatch Rule — Post-Exec Gate]]", "[[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Dispatch Rule — Amendment Provenance]]", "[[vault:sisyphus-runtime/facts/_global/gate-mtime-provenance|Gate — Mtime Provenance]]", "[[vault:sisyphus-runtime/meta/registry|Registry + Escalation Inbox]]"]
---

# Structural Guarantee over Compliance

**Type:** canonical
**Status:** active
**Source:** field observation in the `sisyphus-runtime` multi-session agent system (2026-08); see [[vault:sisyphus-runtime/meta/registry|Registry]] and [[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Post-Exec Gate Rule]]
**Classification:** Materialized in runtime, Missing from canonical/curriculum layer
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

A rule that depends on an agent **remembering it and choosing to follow it** fails precisely
when it matters most: under load, mid-task, with the rule formulated and in plain sight.
Knowing a rule does not prevent violating it. The knowledge and the moment of violation live
in different places — one in the agent's stated principles, the other in the split-second of
concluding something without checking whether the evidence supports it.

The `sisyphus-runtime` produced a sharp field observation of this. On a single day, two
distinct roles — each with the relevant rule formulated and visible — independently committed
the *same* failure: asserting a state that had not been established ("I already sent X", "the
review is done") when it had not been. One did so **minutes after critiquing the other's
instance of the very same failure**. Across the day, the same class recurred several times; in
most cases the contradicting evidence was already on disk *and had been read* by the agent
before it asserted the opposite. The lesson the system drew and recorded was blunt: *"I know
this" did not prevent anything.* A rule of this class, if it is to exist, **cannot depend on
anyone remembering it.**

This is the general form behind several narrower patterns: gates that read a promise instead
of measuring the disk, reviews declared rather than performed, baselines asserted rather than
captured. In each, a *compliance* mechanism (follow the rule) was standing in for a
*structural* one (make the violation impossible or caught by construction).

## Solution

Move the guarantee from **compliance** to **structure**. Do not rely on an agent choosing to
follow the rule; build a mechanism that enforces it regardless of whether anyone remembers.

| Compliance (fragile) | Structural guarantee (robust) |
|---|---|
| "The reviewer should check the diff" | The gate mechanically diffs named writes; there is no pass without it |
| "State that a review was done" | The gate measures the review artifact on disk by hash/mtime |
| "Agents should not self-approve" | A separate head must sign off ([[docs/canonical/split-brain-planning-review|split-brain]]) |
| "Remember to confirm relayed authority" | A gate flags any action justified only by a relayed claim |
| "Don't assert an unverified baseline" | The runner re-captures the baseline; the assertion is not trusted |

**Design tests for turning a rule structural:**

1. **The forgetting test.** If every agent forgot this rule tomorrow, would the violation
   still be caught? If yes, the guarantee is structural. If the only thing standing between
   the system and the failure is that someone remembers, it is compliance, and it will fail.

2. **Measurement by a third party.** The strongest structural form is a check performed by
   something *other than the actor asserting the state* — a separate session, a mechanical
   diff, a runner that re-measures. An actor cannot be the sole verifier of its own claim;
   the failure mode is exactly the actor not asking whether the evidence weighs against its
   own conclusion. (See the companion assertion-provenance discipline.)

3. **The rule lives in the gate, not the memory.** Write the rule where enforcement happens —
   in the gate, the tool dispatch, the schema — not only in a charter that an agent is
   trusted to recall. A charter documents; a gate guarantees.

Structural guarantees are not free and not always warranted: some rules are low-stakes enough
that a documented convention suffices. The pattern's claim is narrower and firmer — **when a
class of failure has recurred despite the rule being known, stop strengthening the reminder
and move the rule into structure.** Recurrence-despite-knowledge is the signal.

## Implementation in the runtime

### What already exists

- [[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Post-Exec Gate]] — a
  two-layer exit gate whose first layer is an *always-on mechanical diff* of named writes: no
  approval phrase can dispense with the measurement.
- [[vault:sisyphus-runtime/facts/_global/gate-mtime-provenance|Mtime Provenance Gate]] and the
  "gates are text-base" discipline — a gate measures the disk, it does not read the artifact's
  claim about itself.
- [[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Amendment
  Provenance]] — the rule that crystallized from an approval phrase asserting a review that
  had not happened.
- [[vault:sisyphus-runtime/meta/registry|Registry]] — notably, the meta-layer recorded its
  *own* instance of the failure rather than hiding it, which is what made the recurrence
  visible as evidence.

### What is missing from the pattern

1. A reusable **forgetting-test checklist** applied to every new rule before it is accepted as
   a mere convention.
2. Curriculum material framing this as the meta-rule behind the specific gates (it is the
   organizing idea of the runtime reimplementation course, Level 3).
3. Tooling that makes the third-party-measurement form the path of least resistance, so that
   the structural option is easier than the compliance one.

## Tradeoffs

| Benefit | Cost |
|---|---|
| The guarantee survives forgetting, fatigue, and load | Building a gate costs more up front than writing a rule |
| Failure is caught by construction, not by luck of recall | Over-applied, it bureaucratizes low-stakes decisions |
| Recurrence-despite-knowledge becomes an actionable signal | Requires honest recording of one's own violations to see the signal |
| Third-party measurement removes the actor's self-verification blind spot | Adds a second party (session, runner) to the critical path |

## Relationship to Other Patterns

- **[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]** — the
  canonical structural guarantee: separate the head that builds from the head that judges, so
  approval cannot be self-granted. This pattern is its generalization.
- **[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]** —
  anchoring evaluation to a verifiable constraint (not an assertion) is a structural guarantee
  applied to judgment.
- **[[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]]** — putting the
  rule in the dispatch mechanism rather than in a prompt is this pattern applied to tool use.
- **[[docs/canonical/operator-channel-authority|Operator-Channel Authority]]** — a relay rule
  held only by discipline is fragile; this pattern argues for moving it into a gate. The two
  were promoted together from the same field observation.
- **[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]** — designing a refusal
  as a role rather than an act of courage is structure-over-compliance at the organizational
  level.

## References

- [[vault:sisyphus-runtime/meta/registry|Registry + Escalation Inbox]] — the recorded day of recurring assertion-without-verification, including the meta-layer's own instance
- [[vault:sisyphus-runtime/facts/_global/dispatch-rule-post-exec-gate|Post-Exec Gate]] — always-on mechanical diff as structural guarantee
- [[vault:sisyphus-runtime/facts/_global/gate-mtime-provenance|Mtime Provenance Gate]] — gates measure the disk, not the promise
- [[vault:sisyphus-runtime/facts/_global/dispatch-rule-amendment-provenance|Amendment Provenance]] — the rule born from an approval phrase that asserted an unperformed review
