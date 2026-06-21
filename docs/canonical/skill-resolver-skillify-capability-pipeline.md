---
title: "Skill-Resolver-Skillify Capability Pipeline"
type: canonical
tags: ["agentes-orquestracao", "context-engineering", "evals", "governanca"]
aliases: ["skillify pipeline", "skill resolver pipeline", "capability pipeline", "routable skill lifecycle"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]"]
sources: ["[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]]"]
---
# Skill-Resolver-Skillify Capability Pipeline

**Type:** canonical
**Status:** active
**Source:** Stanford CS153 AI Native Company analysis
**Classification:** Partial Coverage, High integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

Successful agent workflows stay fragile when they remain one-off prompts, private operator habits, macros, or accumulated global instructions. The workflow may have worked once, but future agents cannot reliably discover it, load it, test it, or know when not to use it.

The pattern solves the gap between a demonstrated workflow and a durable agent capability.

## Solution

Promote repeated agent work through a capability pipeline. A workflow is accepted as a real capability only after it becomes a routable skill with resolver metadata, tests, evals, storage expectations, and smoke evidence.

Pipeline stages:

| Stage | Question | Required artifact |
|---|---|---|
| Workflow capture | What input/output behavior worked in practice? | Example task, expected result, failure notes |
| Skill authoring | What instructions and deterministic helpers make the workflow repeatable? | `SKILL.md`, scripts, templates, or supporting code |
| Resolver registration | When should the agent load this capability? | Positive triggers, negative triggers, aliases, metadata |
| Compliance tests | Does the skill work beyond the original example? | Unit tests, integration tests, LLM evals, trigger evals |
| Resolvability check | Can the resolver find the skill at the right time and avoid duplicates? | `check-resolvable` evidence and overlap review |
| Smoke execution | Can a fresh agent use it end to end? | Smoke result with command, prompt, or fixture |
| Storage schema | Where does durable output or state live? | Output path, metadata schema, retention or precedence rule |

The key rule is that skill text alone is not enough. The resolver and acceptance gates are part of the capability. A skill that exists but fails trigger evals behaves as unavailable in practice.

## Implementation in this repo

### What already exists

- [[docs/system-of-record|System of Record]] lines 34-43 lists operational skills for issue lifecycle, orchestration, doc co-authoring, planning, error-context hygiene, and analyze-and-improve.
- [[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve skill]] lines 46-56 includes improvement generation and integration after classification.
- [[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve skill]] lines 102-119 defines concrete artifact slots such as canonical docs, skills, exercises, and artifacts manifest outputs.
- [[.opencode/skills/error-context-hygiene/SKILL.md|error-context-hygiene skill]] lines 15-20 demonstrates a focused operational skill with explicit behavioral rules.
- [[.opencode/skills/issue-review/SKILL.md|issue-review skill]] lines 57-85 already requires eval-sensitive changes to preserve baseline/candidate, tier, delta, failure example, and merge recommendation evidence.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] documents how eval-sensitive changes should be represented at review time.

### What is missing from the pattern

The classification found Partial Coverage because the repo has skills and a knowledge-to-improvement pipeline, but not the full skillify lifecycle.

Missing pieces:

1. Resolver metadata schema for every reusable skill: positive triggers, negative triggers, audience, workflow, priority, aliases, and overlap constraints.
2. Trigger evals that test whether realistic tasks load the right skill and avoid false positives.
3. A `check-resolvable` gate that verifies discoverability, deduplication, and conflict with existing skills before accepting a new capability.
4. Smoke tests that prove a fresh session can use the skill without hidden author context.
5. A storage schema for skill outputs, evidence, fixtures, or runtime state.
6. An acceptance rule that distinguishes a durable skill from a one-shot macro.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Turns successful workflows into reusable agent capabilities | Most work is compliance, routing, and testing rather than writing the skill text |
| Keeps capability growth auditable and deduplicated | Requires owners to maintain resolver metadata and trigger fixtures |
| Prevents global prompt bloat by moving behavior into loadable skills | Resolver misses can make a valid skill invisible |
| Makes skill quality measurable through evals and smoke tests | Trigger evals can give false confidence if examples are narrow |

## Relationship to Other Patterns

- **Requires:** [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]], because skills only reduce context when the resolver loads them at the right time.
- **Feeds:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]], because durable capabilities are what the operating system can route to.
- **Uses:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] for PR review of skill, resolver, prompt, context, or eval changes.
- **Uses:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] to choose fast trigger checks, medium integration checks, and deep capability regression tests.
- **Can start from:** [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] when repeated manual checks reveal a workflow worth skillifying.
- **Example of existing skill shape:** [[docs/canonical/error-context-hygiene|Error Context Hygiene]], which has focused triggers and explicit rules but would still need resolver eval and smoke evidence under this pipeline.
- **Grounded by:** [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]] pattern 4.

## References

- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]] lines 77-97 - extracted capability pipeline pattern.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]] lines 60-74 - Partial Coverage classification and High integration value.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]] lines 80-86 - skillify mechanism and compliance-heavy insight.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]] lines 152-155 - operational lesson that skillify without tests is incomplete.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis|Stanford CS153 Analysis]] lines 197-200 - one-shot macro, duplicate skill, and trigger-eval false confidence failure modes.
- [[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve skill]] lines 46-56 and 102-119 - current analysis-to-artifact pipeline.
- [[.opencode/skills/error-context-hygiene/SKILL.md|error-context-hygiene skill]] lines 15-20 - focused operational skill example.

---

*Created: 2026-06-10 | From: Stanford CS153 pattern classification | Precedence: canonical*
