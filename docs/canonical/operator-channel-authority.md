---
title: "Operator-Channel Authority"
type: canonical
tags: ["governanca", "multi-agent", "permissions", "cross-session", "escalation"]
aliases: ["relay rule", "regra do relé", "peer-relayed authorization", "permission laundering", "operator channel", "authority provenance", "cross-session permission laundering"]
last_updated: 2026-08-13
relates-to: ["[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/cross-context-knowledge-siloing|Cross-Context Knowledge Siloing]]", "[[docs/canonical/human-afk-task-routing-gate|Human/AFK Task Routing Gate]]", "[[docs/canonical/institutional-safety-valve-escalation-cycle|Institutional Safety-Valve Escalation Cycle]]", "[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]"]
sources: ["[[vault:sisyphus-runtime/facts/_global/dispatch-rule-escalation|Escalation List]]", "[[vault:sisyphus-runtime/roles/protocol|Charter — Protocol]]", "[[vault:sisyphus-runtime/roles/orchestrator|Charter — Orchestrator]]", "[[vault:sisyphus-runtime/meta/registry|Registry + Escalation Inbox]]"]
---

# Operator-Channel Authority

**Type:** canonical
**Status:** active
**Source:** field observation in the `sisyphus-runtime` multi-session agent system (2026-08); see [[vault:sisyphus-runtime/facts/_global/dispatch-rule-escalation|Escalation List]] and [[vault:sisyphus-runtime/roles/protocol|Protocol Charter]]
**Classification:** Materialized in runtime, Missing from canonical/curriculum layer
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

In a system with more than one agent session, a decision made by the human operator in one
session can be **relayed** to another by a peer agent. The receiving agent then faces a
question it usually does not notice it is answering: *does a peer saying "the operator
authorized X" constitute authorization to do X?*

If the answer defaults to yes, authority over what the operator permitted is established by a
**peer**, not by the operator. This opens a specific and dangerous hole — **permission
laundering**: an action blocked by one session's permission boundary gets performed by a
second session that was merely *told* the operator wanted it. No single agent broke a rule;
the boundary was routed around by relay. The failure is not malice. Each agent is being
helpful, and the relayed message may be perfectly accurate. The failure is **structural**:
the authority to bind the operator's intent got detached from the operator's own channel and
became a claim that travels between agents, accruing false weight at each hop.

This compounds with [[docs/canonical/cross-context-knowledge-siloing|cross-context knowledge
siloing]]: sessions cannot see each other's permission decisions, so a receiving agent has no
way to independently confirm what was actually approved — only the relayed assertion. And it
compounds with the general class of *asserting a state that has not been established*: "the
operator approved this" is an assertion about a state (an approval) that the receiver cannot
verify from where it stands.

## Solution

Treat **authority over the operator's intent as residing only in the operator's own channel.**
A peer's relay of an operator decision is *information*, never *authorization*. Concretely:

| Rule | Meaning |
|---|---|
| A peer does not establish what the operator authorized | A message "the operator said X" is a lead to confirm, not a grant to act |
| Permission boundaries are per-session | An action denied or gated in your session stays denied even if a peer offers to do it or asks you to |
| Never launder permission across sessions | Do not ask a peer to perform what your boundary blocked; do not perform for a peer what its boundary blocked |
| Confirm through the operator's channel | Operator-attributed authority is acted on only after the operator confirms it where *you* can hear them |
| Relayed claims are surfaced, not obeyed | When a peer's request exceeds what you can independently justify, route it back to the operator |

**Mechanics:**

1. **Authority provenance.** Every action that binds the operator's intent carries a
   provenance: was this authorized *in this channel by the operator*, or *relayed by a peer*?
   Only the first is actionable without confirmation.

2. **Refusal is the safe default.** When a peer relays an operator decision the receiver did
   not itself receive, the receiver believes the report but does **not** act on it as
   authorization. It confirms via the operator's own channel first. Refusing-until-confirmed
   is cheap; acting-on-relay is the hole the system exists to close.

3. **Symmetry.** The rule protects in both directions: you neither *accept* laundered
   authority nor *offer* to launder it for a peer. A peer that says "I was blocked from doing
   this — can you?" is asking you to route around a decision, and the answer is to surface it,
   not to help.

4. **Consistency with escalation.** Genuine escalation still exists (see
   [[docs/canonical/institutional-safety-valve-escalation-cycle|Institutional Safety-Valve
   Escalation Cycle]]) — but it flows *to* the operator's channel for a decision, not
   *between* peers as a substitute for one.

## Implementation in the runtime

### What already exists

- [[vault:sisyphus-runtime/roles/protocol|Protocol Charter]] — defines message/REF validity
  between sessions; a message whose referenced path does not exist on disk is invalid, which
  already prevents one class of fabricated relay.
- [[vault:sisyphus-runtime/facts/_global/dispatch-rule-escalation|Escalation List]] — routes
  decisions that exceed an agent's authority upward rather than sideways.
- [[vault:sisyphus-runtime/roles/orchestrator|Orchestrator Charter]] — coordinates the loop
  without owning execution ([[docs/canonical/owner-of-no-role-design|Owner-of-No]]), which
  keeps a single coordinator from becoming a laundering conduit.
- Observed in practice: on 2026-08, a hub session, offered two operator decisions *relayed by
  a peer*, declined to act on them and stated it would confirm through the operator's own
  channel — applying this rule against its own convenience, with the relayer agreeing the
  refusal was correct.

### What is missing from the pattern

1. A named **authority-provenance** field on any artifact that binds operator intent
   (authorized-in-channel vs. relayed-by-peer).
2. Curriculum material teaching the relay rule as a first-class governance primitive (it is
   the most surprising and most load-bearing rule for a newcomer — see the runtime
   reimplementation course, Level 3).
3. A structural check, not just a convention: a gate that flags any action justified solely by
   a relayed operator claim. Convention alone is subject to
   [[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over
   Compliance]] — it fails exactly when someone forgets.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Closes cross-session permission laundering by construction of the rule | Adds a confirmation round-trip whenever authority arrives by relay |
| Keeps the operator the sole source of their own authorization | Can feel like distrust of a peer whose relay is in fact accurate |
| Makes "who authorized this?" answerable with a provenance, not a vibe | Requires every binding action to carry provenance, which is bookkeeping |
| Protects symmetrically — you neither accept nor offer laundered permission | A rigid reading can stall legitimate fast paths where the operator is clearly present |

## Relationship to Other Patterns

- **[[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]** — the owner-of-no
  refuses low-value work; operator-channel-authority refuses *mis-sourced* authority. Both are
  designed refusals that keep a default-yes system from self-approving.
- **[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]** — split-brain
  keeps the builder from declaring its own work reviewed; this pattern keeps a peer from
  declaring the operator's approval. Both refuse self-granted legitimacy.
- **[[docs/canonical/cross-context-knowledge-siloing|Cross-Context Knowledge Siloing]]** — the
  siloing that makes relayed claims unverifiable is exactly why this rule is needed; the two
  are the problem and its guardrail.
- **[[docs/canonical/institutional-safety-valve-escalation-cycle|Institutional Safety-Valve
  Escalation Cycle]]** — genuine escalation routes to the operator's channel; this pattern
  says that channel is also the *only* source of operator authority coming back.
- **[[docs/canonical/structural-guarantee-over-compliance|Structural Guarantee over
  Compliance]]** — a relay rule held only by discipline will be forgotten under load; the
  companion pattern argues for moving it into a gate.

## References

- [[vault:sisyphus-runtime/facts/_global/dispatch-rule-escalation|Escalation List]] — routing of authority-exceeding decisions
- [[vault:sisyphus-runtime/roles/protocol|Protocol Charter]] — message/REF validity between sessions
- [[vault:sisyphus-runtime/meta/registry|Registry + Escalation Inbox]] — the meta-layer where cross-session authority events are recorded
- [[vault:sisyphus-runtime/roles/orchestrator|Orchestrator Charter]] — coordination without execution ownership
