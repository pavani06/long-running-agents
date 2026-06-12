---
title: "Persona-Based Documentation"
type: canonical
tags: ["agentes-orquestracao", "harness", "governanca"]
aliases: ["persona-based NFRs", "persona documentation", "role-based documentation", "specialty-owner documents", "persona-specific NFR documents", "multi-persona documentation"]
last_updated: 2026-06-11
relates-to: ["[[AGENTS|AGENTS.md]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]", "[[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]", "[[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]]", "[[.opencode/agents/hop-orchestrator-rezek|orchestrator agent]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|Harness Engineering Classification]]"]
sources: ["[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|Harness Engineering Patterns]]", "[[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|Harness Engineering Classification]]"]
---

# Persona-Based Documentation

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/
**Classification:** Missing
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

A single universal instruction file creates a bottleneck: every quality dimension (front-end architecture, reliability, security, scalability, product behavior, accessibility) competes for space in one document. The document grows to cover everything, becomes hard to maintain, and forces every agent to load every constraint regardless of the task. When a team has specialists in different domains, their expertise is not systematically captured in durable documentation surfaces that agents can load.

The source describes this as the key insight behind persona-based documentation: "each team member documents their specialty (front-end architect, reliability engineer, security, product) as durable NFR documents, and reviewer agents load persona-specific rubrics" ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:45, 99). Without persona-specific documentation surfaces, quality criteria from the front-end architect, the reliability engineer, and the security specialist all end up in a single monolithic file or, worse, remain as tacit knowledge in individual engineers' heads.

The repository uses a single universal `AGENTS.md` with 16 rules loaded by every agent. There are no persona-specific documentation surfaces. The HoP agents have role-specific scopes but their instructions are agent-specific, not persona-based documentation surfaces that multiple agents inherit. The `review-work` skill performs second-agent review using generic quality criteria, not persona-specific rubrics. The `multi-model-evaluation-council.md` runs multiple evaluators with divergence policy, but evaluators are model-based, not persona-based ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:333-349).

## Solution

Create persona-specific documentation surfaces where each quality dimension owner writes durable NFR documents. Reviewer agents load persona-specific rubrics. Every agent inherits the full quality standard regardless of which persona's perspective is most relevant to the current task.

The mechanism has three layers:

```
+---------------------------------------------------+
| Persona owners (humans)                            |
| front-end | reliability | security | product       |
| write durable NFR documents for their dimension    |
+---------------------+-----------------------------+
                      |
                      v
+---------------------------------------------------+
| Persona-specific NFR documents (durable artifacts) |
| frontend-architecture.md  reliability.md           |
| security.md  product-behavior.md  accessibility.md |
+---------------------+-----------------------------+
                      |
                      v
+---------------------------------------------------+
| Persona-specific reviewer agents (CI gates)        |
| load persona rubric → review PR diff               |
| produce BLOCKING/ADVISORY findings per dimension   |
+---------------------------------------------------+
```

**Components:**

1. **Persona ownership.** Each quality dimension has a designated human owner who is responsible for writing and maintaining the persona-specific NFR document. The front-end architect owns UI component structure, state management patterns, CSS conventions, and accessibility requirements. The reliability engineer owns error handling, retry policies, degradation behavior, and observability contracts. The security specialist owns input validation, auth patterns, secret management, and dependency audit rules. The product owner owns behavioral acceptance criteria, user-facing contract definitions, and feature-completeness gates.

2. **Persona-specific NFR documents.** Each persona produces a durable, versioned document that encodes the non-functional requirements for their dimension. These documents follow the same conventions as `AGENTS.md`: they are markdown files with explicit rules, examples, and decision rubrics. They are stored in a known location where agents and reviewer agents load them during work. The documents are maintained independently: the front-end architect updates the front-end document without touching reliability rules, and vice versa.

3. **Persona-specific reviewer agents.** Each persona has a corresponding reviewer agent configured as a CI gate. The front-end reviewer loads the front-end NFR document and reviews the PR diff for UI component violations. The reliability reviewer loads the reliability NFR document and checks error handling, retry, and observability patterns. The security reviewer loads the security NFR document and audits for injection risks, exposed secrets, and unsafe patterns. Each reviewer produces BLOCKING or ADVISORY findings scoped to their dimension.

4. **Inheritance across agent sessions.** Every implementation agent loads the relevant persona-specific documents based on the task scope. A front-end task loads the front-end and accessibility documents. A backend task loads the reliability and security documents. A full-stack task loads all persona documents. The resolver-based disclosure system determines which persona documents to load based on task triggers.

**Interaction with universal AGENTS.md:**

The universal `AGENTS.md` remains as the base contract: operational rules (commit style, validation gates, security constraints, code standards) that apply to every agent regardless of persona. Persona-specific documents extend `AGENTS.md` with dimension-specific quality criteria. The universal document is the floor; persona documents raise the ceiling per dimension.

## Implementation in this repo

### What already exists

- [[AGENTS|AGENTS.md]] lines 1-238 provides a single universal instruction file with 16 rules governing agent behavior. This is the base contract that persona-specific documents would extend.
- [[.opencode/agents/hop-orchestrator-rezek|orchestrator agent]] provides governance-persona coordination as the HoP orchestrator, demonstrating role-specific agent scopes.
- [[.opencode/skills/review-work/SKILL|review-work skill]] performs second-agent review with structured quality criteria, but uses generic quality dimensions rather than persona-specific rubrics.
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] lines 30-47 runs multiple evaluators with divergence policy. This is the closest existing mechanic to persona-specific evaluation, but evaluators are model-based (different models), not persona-based (different quality dimensions).
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] lines 30-44 converts QA findings into backlog issues with capture, triage, convert, and return-to-board stages. Persona-specific reviewer findings would feed into this loop.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] defines merge-policy gates. Persona-specific reviewer findings would add dimension-specific merge criteria.

### What is missing from the pattern

The classification marks Persona-Based Documentation as Missing after searching all canonical docs, curriculum lessons, core concepts, skills, and agent definitions. The concept appears only in the source analysis documents, not in any repo artifact ([[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:333-349).

Missing pieces:

1. No persona-specific NFR documents exist. `AGENTS.md` is a single universal file with no persona-specific sections or role-based loading rules.
2. No persona-specific reviewer agents are defined. The `review-work` skill and `multi-model-evaluation-council` use generic or model-based criteria, not dimension-specific rubrics keyed to front-end architecture, reliability, security, or product behavior.
3. No documentation ownership model assigns quality dimensions to human specialists. The orchestrator agent coordinates workflow but does not route quality decisions to persona owners.
4. No curriculum lesson teaches persona-based NFR writing. The curriculum covers NFR concepts through Sprint Contracts and Evaluation Rubrics but does not teach persona-specific documentation ownership.
5. No resolver integration loads persona documents based on task scope. The `resolver-based-context-progressive-disclosure.md` loads skills on demand but does not route persona documents per task dimension.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Multiplies quality standards across all agent sessions — every agent inherits every specialist's knowledge | Requires human specialists to externalize and maintain their persona documents |
| Persona-specific reviewer agents scale review capacity per quality dimension | Each persona reviewer adds CI latency and token cost per PR |
| Independent maintenance: front-end changes do not touch reliability rules | Persona documents can drift or contradict each other without cross-persona governance |
| Makes hiring and onboarding systematic: new team members contribute to their persona document | Requires cultural commitment to writing durable documentation, not just sharing knowledge in chat |

## Relationship to Other Patterns

- **Extends:** [[AGENTS|AGENTS.md]] because persona documents add dimension-specific quality criteria on top of the universal agent contract.
- **Feeds:** [[docs/canonical/generator-evaluator|Reviewer Agents as CI Gates]] because each persona-specific reviewer agent loads its persona document and produces BLOCKING/ADVISORY findings for its quality dimension.
- **Consumed by:** [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] because the council's evaluators can be extended from model-based to persona-based evaluation with per-dimension divergence policy.
- **Feeds into:** [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] because persona-specific review findings become structured backlog items with dimension metadata.
- **Governed by:** [[docs/canonical/garbage-collection-day-meta-loop|Garbage Collection Day Meta-Loop]] because the weekly cadence converts persona-specific observations into updated persona documents and reviewer rubrics.
- **Depends on:** [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] because persona documents should be loaded on demand based on task scope, not front-loaded into every agent session.
- **Comes from:** [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|Harness Engineering Analysis]]:41-45, 95-103 and its Missing classification in [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:333-349.

## References

- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:41-45 — NFR documentation as durable asset; persona-based documentation model where each specialist documents their quality dimension.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:95-103 — reviewer agents as CI gates with persona-specific rubrics (front-end architect, reliability engineer, scalability).
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-analysis|analysis]]:124-130 — implementation agent autonomy to acknowledge/defer/reject persona-specific feedback.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-patterns|patterns]]:17-37 — Durable Non-Functional Requirements Memory pattern: persona-specific quality knowledge as input, reusable quality criteria as output.
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent-classification|classification]]:333-349 — Missing classification with NOT_FOUND evidence across canonical docs, curriculum, core concepts, skills, and agents.
- [[AGENTS|AGENTS.md]]:1-238 — universal agent instructions without persona-specific sections.
- [[.opencode/agents/hop-orchestrator-rezek|orchestrator agent]] — governance-persona coordination agent.
- [[.opencode/skills/review-work/SKILL|review-work skill]] — second-agent review with generic quality criteria.
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]]:30-47 — model-based evaluators with divergence policy.
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]]:30-44 — capture, triage, convert, return-to-board pipeline for review findings.

---

*Created: 2026-06-11 | From: Harness Engineering pattern classification | Precedence: canonical*
