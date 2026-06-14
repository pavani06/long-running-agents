---
title: "Pre-Commit AI Review Gate"
type: canonical
aliases: ["pre-commit review", "AI pre-commit", "local AI gate", "pre-push AI review", "pre-commit AI hook"]
tags: ["evals", "agentic-coding", "governanca", "harness-engineering"]
last_updated: 2026-06-15
relates-to: ["[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]", "[[docs/canonical/review-contract-checklist|Review Contract Checklist]]", "[[docs/canonical/contextual-severity-calibration|Contextual Severity Calibration]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]"]
sources: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]"]
---

# Pre-Commit AI Review Gate

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]
**Classification:** Partial Coverage ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:101-127)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

AI-based code review that runs only after push — at PR time or in CI — creates slow feedback loops and lets trivial issues reach shared resources (CI pipelines, human reviewers). The developer pushes, waits for CI to start, sees an AI comment about a missing type annotation, fixes it locally, pushes again, and repeats. This cycle wastes CI minutes, human attention, and the developer's context window.

The repo has the conceptual framework for gating checks at different lifecycle stages via eval tier stratification — the fast tier explicitly lists pre-commit as a trigger with the power to "block local readiness or PR if critical paths regress" ([[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:34). Standard pre-commit hooks for mechanical lint/formatting exist in the curriculum setup guide ([[curriculum/07-implementation-guides/01-setup-guide|curriculum/07-implementation-guides/01-setup-guide.md]]:2452-2487). But the slot between "mechanical lint hooks" and "PR-level AI eval" is empty — no AI reviewer prompt is designed to run at pre-commit time with a local diff and project-specific conventions as input ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:107-109).

The classification identifies this as Partial Coverage because the structural framework (fast tier, pre-commit trigger) exists, but the specific AI reviewer mechanism, prompt design, convention injection, and block policy for pre-commit AI review are missing ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:105-109).

## Solution

Run an AI reviewer as a local pre-commit hook that receives the staged diff, checks it against project-specific conventions across three triage axes, and returns a pass/block decision before the developer pushes. The AI reviewer acts as the fast tier's pre-commit mechanism — a shallow-first pass that catches bugs, convention violations, and security concerns before any shared resource is engaged.

**Flow:**

```
git diff (staged)
      |
      v
AI Reviewer (pre-commit hook)
  prompt: bugs + project conventions + security concerns
  input: local diff + project convention documents
      |
      v
Gate: pass/block
  pass → allow commit/push
  block → findings list with location and rationale
```

This flow is defined in the pattern specification ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:77-84).

**Prompt design — three-question triage:**

The AI reviewer prompt must request three specific categories, not an open-ended review:

1. **Potential bugs:** Logic errors, null handling gaps, race conditions, incorrect assumptions visible in the diff.
2. **Style violations against the project's own conventions:** Rules from `AGENTS.md`, team ESLint config, canonical doc patterns, coding standards — not generic industry best practices.
3. **Security concerns:** Input validation gaps, hardcoded secrets, unsafe deserialization, missing authorization checks visible in the diff.

This triage model is the core prompt design principle: narrow, specific categories produce focused, actionable output; broad prompts produce noise that developers ignore ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:36-43, 176-180).

**Project convention injection:**

The prompt must include the project's actual conventions, not generic defaults. The source analysis identifies this as the critical tuning step: when the prompt uses generic industry rules, output is so noisy that developers ignore it entirely; when the prompt enforces the team's real rules, the signal-to-noise ratio is high enough for sustained use ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:177-180, 212-218).

Relevant convention sources in this repo:
- [[AGENTS|AGENTS.md]] — operational rules for agents (Rule 9: security constraints, Rule 10: code standards).
- [[docs/canonical/error-context-hygiene|Error Context Hygiene]] — canonical error handling rules.
- [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]] — tool usage conventions.
- Project-specific lint rules (`eslint-rules/no-catch-message.js`, `eslint-rules/no-raw-console-in-scripts.js`).

The classification notes that no canonical doc or skill currently describes injecting these conventions into a pre-commit AI review prompt ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:122).

**Pass/block policy:**

The gate operates with an explicit policy: block when any finding category produces a `fail` result for a high-confidence issue; allow when findings are advisory or low-confidence. The policy must be documented and understood by developers before enforcement begins — an undocumented block policy leads to confusion and bypass attempts.

| Finding confidence | Policy |
|---|---|
| High: unambiguous violation of a documented rule | Block: must fix before push |
| Medium: likely issue, requires human judgment | Advisory: warn, do not block |
| Low: style preference or suggestion | Informational: log only |

**Integration with eval tier stratification:**

The pre-commit AI review gate maps directly to the fast tier's pre-commit trigger slot. The fast tier already declares that it "blocks local readiness or PR if critical paths regress" with runtime budget of seconds to minutes ([[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:30-36). The AI pre-commit gate would operationalize this slot with an actual AI reviewer mechanism, filling the gap between mechanical lint hooks and PR-level eval enforcement.

## Implementation in this repo

### What already exists

The repo has the structural framework for pre-commit gating:

- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:34 — fast eval tier explicitly lists "pre-commit" as a trigger with decision power to block local readiness or PR if critical paths regress.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:30-49 — comprehensive per-tier metadata including `runtime_budget`, `cost_budget`, `flakiness_policy`, `trigger`, `threshold`, `reporting`, and `owner`.
- [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]:67-69 — lint rules as "commit time" guardrail surface with low token cost and instant latency, establishing the concept of pre-commit mechanical checks.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:30-53 — PR-level eval enforcement with structured reports, but operates after push (PR time), not pre-commit.
- [[curriculum/07-implementation-guides/01-setup-guide|curriculum/07-implementation-guides/01-setup-guide.md]]:2452-2487 — standard pre-commit hooks for lint/ruff formatting (mechanical, not AI-based).

These provide the slot and the adjacent infrastructure but not the AI reviewer mechanism that would fill the slot ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:110-115).

### What is missing

1. An AI reviewer prompt designed to be invoked at pre-commit time, receiving a local `git diff` and checking for bugs, project convention violations, and security concerns. NOT_FOUND in any canonical doc, skill, or curriculum lesson ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:119).
2. A pass/block policy for local AI pre-commit results — existing pre-commit hooks block on lint failure, but there is no equivalent AI-review block policy ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:120).
3. Integration between AI pre-commit findings and eval tier stratification: the fast tier mentions pre-commit as a trigger but does not describe an AI reviewer as the mechanism ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:121).
4. Project-specific convention awareness in an AI pre-commit prompt — canonical docs emphasize project conventions but none describes injecting them into a pre-commit AI review prompt ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:122).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Shortens feedback latency for mechanical and policy-level issues — feedback arrives before push, not after CI | Local hooks can be bypassed unless paired with server-side or PR gates |
| Keeps CI and human review focused on higher-value checks — AI catches trivial issues locally | The AI reviewer remains a fast, shallow first pass — architecture and design review still belongs to humans |
| Reduces noise when the prompt enforces the team's actual rules instead of generic best practices | Poor prompt tuning produces noisy output that developers learn to ignore — the most common failure mode |
| Project convention injection ensures relevance — the AI enforces YOUR rules, not industry defaults | Maintaining convention documents and prompt templates adds documentation overhead |
| Operates within the fast tier's runtime budget (seconds to minutes) — does not slow the inner dev loop | Token cost per commit adds up; fast models keep cost low but may miss issues deeper models would catch |

## Relationship to Other Patterns

- **Slots into:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] which explicitly reserves the "pre-commit" trigger in the fast tier. The pre-commit AI review gate operationalizes this slot with a specific AI reviewer mechanism.
- **Uses:** [[docs/canonical/review-contract-checklist|Review Contract Checklist]] because review contract dimensions provide the structured checklist the AI reviewer validates at pre-commit time, replacing an open-ended review prompt with bounded, verifiable checks.
- **Uses:** [[docs/canonical/contextual-severity-calibration|Contextual Severity Calibration]] because module risk profiles determine review depth and block thresholds at pre-commit time — a change to a `critical` module triggers stricter checks and lower block thresholds than a change to a `low` module.
- **Complements:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] because pre-commit catches shallow issues locally, leaving PR-level enforcement to handle deeper eval evidence (baseline deltas, latency/cost regression, long-session behavior).
- **Complements:** [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]] because pre-commit findings that are false positives or consistently ignored become classified pain signals that feed guardrail evolution.
- **Uses:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] because the three-axis triage (bugs, conventions, security) is a constraint-anchored check — each axis is a constraint category with explicit pass/fail criteria.
- **Adjacent to:** [[curriculum/07-implementation-guides/01-setup-guide|curriculum/07-implementation-guides/01-setup-guide.md]] which covers standard pre-commit hooks for mechanical linting, providing the hook infrastructure the AI gate would extend.

## References

- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:26-35 — AI reviewer capability model: fast but shallow, complement not replacement.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:36-43 — review triage model: three-question prompt (bugs, conventions, security).
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:76-91 — Pre-Commit Gate pattern mechanics, flow diagram, and structural properties.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:176-180 — prompt tuning against project-specific conventions as success factor.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:210-218 — failure pattern: AI output ignored due to noise from generic prompts.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:224-234 — tradeoff: velocidade vs. profundidade na revisao.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:236-247 — tradeoff: cobertura vs. relacao sinal-ruido.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|patterns]]:61-81 — extracted pattern definition with inputs, outputs, benefits, limitations.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:101-127 — Partial Coverage classification with what exists and what is missing.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:34 — fast tier pre-commit trigger.
- [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]:30-49 — per-tier metadata including runtime, cost, flakiness, trigger.
- [[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]:67-69 — lint rules as commit-time guardrail surface.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:30-53 — PR-level eval enforcement operating after push.
- [[curriculum/07-implementation-guides/01-setup-guide|curriculum/07-implementation-guides/01-setup-guide.md]]:2452-2487 — standard pre-commit hooks for mechanical linting.

---

*Created: 2026-06-15 | From: Canary Test Code Review pattern classification | Precedence: canonical*
