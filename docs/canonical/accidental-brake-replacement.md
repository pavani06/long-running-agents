---
title: "Accidental Brake Replacement"
type: canonical
tags: ["governanca", "decision-discipline", "agentes-orquestracao", "harness-engineering"]
aliases: ["accidental brake", "bureaucracy replacement", "bureaucratic brake", "intentional governance gates", "brake migration"]
last_updated: 2026-06-11
relates-to: ["[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]", "[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]", "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
sources: ["[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]", "[[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]"]
---

# Accidental Brake Replacement

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-11-the-trap-spec-driven-development-is-setting/
**Classification:** Missing, Low integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

In organizations adopting agentic coding, the useful discipline of asking "is this worth building?" often survives only inside slow, bureaucratic processes that nobody respects: cautious procurement, dragged-out security reviews, gated AI rollouts. This bureaucracy is not designed to be a value brake -- it is designed for compliance, purchasing policy, and risk management. But it is the only brake still functioning, and it works by accident, not by design. The danger is that an executive mandate to "move faster" or "remove bureaucracy" can eliminate the last remaining mechanism that prevents unchecked agentic construction, without anyone realizing what function it was serving.

The source articulates this as an enterprise paradox: "a disciplina de valor nao sobreviveu nos melhores profissionais com tokens gratuitos. Sobreviveu na burocracia: procurement, security review, rollout gates. Isso funciona por acidente, nao por design, e nao sobrevivera ao primeiro executivo que decidir que lentidao e o inimigo" ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:116-118). The repo is not an enterprise organization with inherited bureaucracy, so this pattern has low direct integration value for this repo. However, it documents a structural risk relevant to organizations adopting the repo's agentic patterns and is suitable as curriculum content for enterprise adoption contexts.

## Solution

Audit existing organizational gates that slow down construction, identify which ones are serving an accidental value-brake function, and replace them with intentional harness gates before anyone removes them as "bureaucracy."

**The audit process:**

1. **Inventory existing gates.** Map every approval, review, sign-off, and wait-state in the current build-to-ship pipeline. Include procurement approval, security review, architecture board, change advisory board, compliance check, legal review, and any other process that adds delay between idea and deployment.

2. **Classify each gate by function.** For each gate, answer: what is the intended purpose? What does it actually prevent? Does it prevent low-value builds (accidental value brake), prevent compliance violations (regulatory brake), prevent security incidents (security brake), or just add process overhead (pure bureaucracy)?

3. **Identify accidental value brakes.** Gates classified as "prevents low-value builds" or "forces someone to justify the work before it proceeds" are accidental value brakes. They are performing a function nobody designed them for. Document what value they are accidentally preserving.

4. **Design intentional replacements.** For each accidental brake, design a harness gate that preserves the useful function while removing the accidental overhead. The replacement should be: faster than the bureaucratic gate, intentional rather than accidental, and integrated into the agent workflow rather than bolted on as process overhead.

5. **Replace before removing.** Never remove a bureaucratic gate until its intentional replacement is operational. The sequence is: deploy replacement gate, validate it catches the same class of problematic builds, then deprecate the bureaucratic gate.

6. **Audit trail.** Maintain a record mapping each removed bureaucratic gate to its intentional replacement, with rationale and validation evidence.

**Replacement examples:**

| Accidental brake | Useful function | Intentional replacement |
|---|---|---|
| Procurement approval (takes 2 weeks) | Forces cost justification before spend | [[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]: cost-proxy question asked in minutes, not weeks |
| Security review (takes 1 week) | Prevents vulnerable code from shipping | [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] + automated security scanning at PR time |
| Architecture board (monthly) | Prevents architectural drift and unowned decisions | [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] + [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]] |
| Change advisory board (weekly) | Forces explicit change justification and risk assessment | [[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]: build/experiment/defer/stop decisions with recorded rationale |

**Governance for the replacements:**

The intentional replacements must be hardened against the same pressure that created the accidental brakes in the first place. A [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] governs the replacement gates: they have ROI, they can be simplified, and they can be removed -- but only when the function they serve is no longer needed, not when they are perceived as slow.

## Implementation in this repo

### What already exists

- `docs/canonical/` -- 55 canonical patterns cover agent-internal harness engineering; none address external bureaucracy replacement.
- [[.github/PULL_REQUEST_TEMPLATE|PR template]], [[.github/CODEOWNERS]], [[.github/ISSUE_TEMPLATE/|issue templates]] -- these are intentional governance mechanisms, not inherited bureaucracy.
- [[.opencode/skills/issue-review/SKILL|issue-review skill]] -- validation gates (lint, test, eval) are designed intentionally, not inherited from bureaucracy.
- [[.opencode/skills/issue-start/SKILL|issue-start skill]] -- worktree setup and claim are internal workflow, not bureaucracy replacement.
- [[AGENTS]] -- rules are designed for agent behavior, not inherited from organizational bureaucracy.

### What is missing from the pattern

The classification marks Accidental Brake Replacement as Missing because the concept of auditing external bureaucracy and replacing it with intentional harness gates is not present in the repo ([[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|classification]]:200-220). The classification notes this makes structural sense: the repo is a curriculum and canonical pattern library, not an enterprise organization with inherited procurement, security review, or compliance gates. The repo's governance was designed intentionally from the start.

Missing items:

1. The audit methodology for classifying organizational gates as accidental value brakes.
2. A mapping pattern for replacing bureaucratic gates with intentional harness equivalents.
3. An audit trail format for tracking which intentional gate replaced which accidental one.
4. Curriculum content on this pattern (could live in Level 4: enterprise adoption contexts).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Preserves the useful brake function while removing unnecessary slowness | Requires executive support because it changes who may say yes or no |
| Makes governance robust against mandates to "just move faster" | Can overformalize exploration if every gate from bureaucracy is copied directly |
| Reduces hidden risk from private builder workflows outside enterprise gates | Informal autonomous workflows can still evade the replacement gate |
| Converts accidental discipline into designed, auditable governance | The audit itself consumes organizational attention before any improvement is delivered |
| Prevents removal of the last functioning brake without a replacement | Only relevant to organizations with inherited bureaucracy -- not applicable to greenfield agentic systems |

## Relationship to Other Patterns

- **[[docs/canonical/manual-brake-question-gate|Manual Brake Question Gate]]** -- the brake questions are the simplest intentional replacement for the value-gating function that accidental bureaucracy currently performs.
- **[[docs/canonical/value-gated-agent-control-loop|Value-Gated Agent Control Loop]]** -- the control loop is the architectural home for intentional value gates that replace accidental bureaucratic brakes.
- **[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]** -- an intentional replacement for the quality-gating function of slow review processes.
- **[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]** -- governs the intentional replacement gates over time, ensuring they can be simplified or removed when their function is no longer needed.
- **[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]** -- the control plane unifies prompt, context, dispatch, and gates -- the infrastructure that hosts the intentional replacements.

## References

- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|The Trap SDD Analysis]]:54-56 -- source description of the Accidental Brake Model
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-patterns|SDD Trap Patterns]]:205-230 -- extracted pattern structure
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-classification|SDD Trap Classification]]:200-220 -- classification evidence and gap analysis
- [[docs/analysis/2026-06-11-the-trap-spec-driven-development-is-setting/2026-06-11-the-trap-spec-driven-development-is-setting-analysis|analysis]]:116-118 -- bureaucracy as the only remaining brake
