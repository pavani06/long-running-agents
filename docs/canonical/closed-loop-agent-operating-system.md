---
title: "Closed-Loop Agent Operating System"
type: canonical
tags: ["agentes-orquestracao", "context-engineering", "governanca"]
aliases: ["closed-loop agent OS", "agent operating system", "operational agent loop"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]"]
sources: ["[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]]"]
---
# Closed-Loop Agent Operating System

**Type:** canonical
**Status:** active
**Source:** Stanford CS153 AI Native Company analysis
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Long-running agent operations drift when decisions, failures, priorities, and ownership live in human heads, private messages, issue comments, or incomplete notes. In that state, agents can read isolated artifacts, but they cannot turn the current operating state into a durable next-action loop.

The pattern solves open-loop company drift: each execution produces local output, but the system does not consistently feed outcomes back into memory, prioritization, issue selection, and future agent behavior.

## Solution

Build a closed-loop operating system around the agent fleet. The operating system continuously connects four surfaces:

| Surface | Mechanism | Output |
|---|---|---|
| State intake | Read company, product, repo, issue, PR, chat, trace, and memory artifacts with clear source precedence | Current operational picture |
| Priority synthesis | Compare state against ownership, blockers, labels, failures, and roadmap context | Suggested next work and escalation targets |
| Execution routing | Start the right skill, issue lifecycle, sub-agent, or review path for the selected work | Scoped agent execution with an accountable owner |
| Feedback writeback | Persist decisions, traces, failures, eval results, canonical docs, and issue outcomes | Updated memory for future agents |

The loop is not a chatbot that answers questions about the repo. It is an operational control loop: observe state, decide what should happen next, route execution, validate the outcome, and update the records that future agents will trust.

Minimum operating contract:

1. **Source precedence:** agents resolve conflicts through [[docs/system-of-record|System of Record]] before acting.
2. **Readable state:** issues, PRs, worktrees, canonical docs, analysis artifacts, and skills expose enough metadata for an agent to choose next work.
3. **Ownership:** every recommended action has an issue, DRI, label, worktree, PR, or explicit owner boundary.
4. **Validation:** completion includes tests, review, eval evidence, or documented waiver before state is written back as authoritative.
5. **Memory update:** important outcomes become canonical docs, evidence, issue comments, eval cases, or analysis artifacts rather than staying in session transcript only.

## Implementation in this repo

### What already exists

- [[docs/system-of-record|System of Record]] lines 14-21 defines the documentation precedence hierarchy used when operational knowledge conflicts.
- [[docs/system-of-record|System of Record]] lines 25-46 maps the `.opencode` agent system, lifecycle skills, orchestrator, and analysis pipeline into project domains.
- [[.opencode/skills/orchestrator/SKILL|orchestrator skill]] lines 12-15 fetches state, summarizes active work, suggests next issues, generates prompts, and cleans up sessions.
- [[.opencode/skills/orchestrator/SKILL|orchestrator skill]] lines 27-62 defines a dashboard and priority logic for choosing the next task.
- [[.opencode/skills/analyze-and-improve/SKILL|analyze-and-improve skill]] lines 46-56 defines a pipeline from repository model through extraction, classification, improvements, integration, and curriculum integration.
- [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] provides the inner-loop harness frame for an individual agent.
- [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] defines how failures become durable regression knowledge.

### What is missing from the pattern

The classification found Partial Coverage because the mechanics are split across governance, HoP issue skills, orchestrator workflow, and analysis workflow rather than named as one operating system.

Missing pieces:

1. A single canonical closed-loop OS model that connects state intake, task recommendation, execution routing, validation, and memory writeback.
2. A required feedback-writeback policy for agent outcomes: what becomes canonical, what becomes evidence, what stays analysis, and what remains ephemeral.
3. Operational observability for loop health: recommendations made, accepted, rejected, executed, blocked, and converted into durable memory.
4. A mapping from product/company artifacts such as customer traces, bugs, meetings, and decisions into the same loop used for repo issues and docs.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Converts scattered agent workflows into a teachable operating model | Requires disciplined artifact hygiene across issues, docs, traces, and reviews |
| Reduces information loss between sessions and agents | Noisy or stale source artifacts can produce noisy recommendations |
| Makes next-work selection explicit and auditable | Needs ownership metadata and conflict resolution before automation is safe |
| Feeds execution outcomes back into future prioritization | Adds writeback work after each meaningful agent run |

## Relationship to Other Patterns

- **Contains:** [[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]] as the inner loop for an individual agent run.
- **Requires:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]] when the operating loop spans multiple sessions or waits for human approval.
- **Uses:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] to make omitted or historical state discoverable without loading all memory.
- **Feeds:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] when failures discovered by operations become replayable tests.
- **Depends on:** [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]] and [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] so the operating system can route work to durable capabilities without global prompt bloat.
- **Grounded by:** [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]] pattern 1.

## References

- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]] lines 14-33 - extracted problem, inputs, outputs, benefits, and limitations.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]] lines 13-28 - Partial Coverage classification and High integration value.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]] lines 201-214 - open-loop company drift and capability-as-operating-system synthesis.
- [[docs/system-of-record|System of Record]] lines 14-46 - precedence and agent domain map.
- [[.opencode/skills/orchestrator/SKILL|orchestrator skill]] lines 12-62 - current dashboard and task-selection mechanics.
- [[.opencode/skills/analyze-and-improve/SKILL|analyze-and-improve skill]] lines 46-56 - current knowledge-to-improvement loop.

---

*Created: 2026-06-10 | From: Stanford CS153 pattern classification | Precedence: canonical*
