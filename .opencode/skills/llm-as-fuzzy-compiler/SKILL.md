---
name: llm-as-fuzzy-compiler
description: "Apply the LLM-as-Fuzzy-Compiler mental model when designing harness components, deciding what to preserve vs. regenerate, or planning model migrations. Treat the LLM as a fuzzy compiler backend, harness controls (lint rules, review agents, skills, tests, docs) as optimization passes, and generated code as a disposable build artifact. Use when designing new harness components, evaluating which assets to version-control, planning model upgrades, or explaining why guardrails matter more than generated code. Triggers: 'compiler model', 'fuzzy compiler', 'code as build artifact', 'disposable code', 'model migration planning', 'harness as compiler passes', 'what to preserve vs regenerate', 'compiler backend swap'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: design
  priority: medium
  source: "Harness Engineering (Ryan Lopopolo, OpenAI — AI Engineer 2026)"
---

## What I Do

I provide the mental model and concrete decision rules for treating LLM output as compilation, not authorship. I enforce three principles:

1. **LLM is a fuzzy compiler** — the model transforms prompts and constraints into code, with probabilistic variance
2. **Harness controls are optimization passes** — lint rules, review agents, tests, and skills are compiler passes that refine output toward correctness
3. **Code is a disposable build artifact** — the durable assets are prompts, guardrails, and documentation; generated code can be reproduced from them

This mental model changes what you version-control, what you invest in maintaining, and how you plan model migrations.

## When to Use Me

Load this skill when:

- Designing a new harness component (lint rule, review agent, skill, CI check) — frame it as a compiler pass
- Deciding whether to preserve generated code or regenerate it from upgraded guardrails
- Planning a model migration (e.g., GPT-4 → GPT-5, Claude 3 → 4) — treat it as a compiler backend swap
- Evaluating which artifacts deserve version control and which are rebuildable
- Explaining to stakeholders why harness investment compounds while generated code is ephemeral
- Auditing existing harness components to classify them as domain invariants or model-specific compensations (pair with [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]])

Do NOT use when:

- The task is a single trivial code change with no harness design implications
- You are editing human-authored handcrafted code (this pattern applies to agent-generated output)
- You need concrete implementation rules for a specific lint rule or test — load that specific skill instead

## The Anti-Pattern

```
ANTI-PATTERN: Treating generated code as precious, versioning everything,
and preserving code when the harness that produced it is lost.

Scenario:
  1. Agent generates 2000 lines of React components from a prompt
  2. Team commits all 2000 lines, reviews them line-by-line
  3. The prompt and guardrails that produced them are discarded (or never versioned)
  4. Six months later, model upgrades. The code still works, but nobody can reproduce
     or improve it systematically.

Consequence:
  - The durable knowledge (prompts, constraints, docs) is lost
  - The disposable artifact (generated code) is preserved
  - Model migrations become manual rewrites instead of recompilation
  - Harness never improves because nobody tracks what produced the code
```

## The Pattern

```
PATTERN: Treat the harness as the source of truth and code as build output.

Pipeline view:

  [NFR Docs + Prompts] ──┐
  [Lint Rules]          ──┤
  [Review Agents]       ──┼──► LLM (compiler backend) ──► Generated Code (build artifact)
  [Skills]              ──┤
  [Test Suites]         ──┘

Each harness component is an optimization pass:
  - Lint rules        = syntax-level constraints (no unsafe patterns)
  - Review agents     = semantic-level constraints (architecture, security, style)
  - Skills            = workflow constraints (correct tool dispatch, error handling)
  - Tests             = behavioral constraints (must pass before merge)
  - NFR docs          = specification constraints (what "good" means)

When the model improves:
  - Keep all harness components classified as domain invariants
  - Re-evaluate model-specific compensations (may become obsolete)
  - Regenerate code through the upgraded pipeline
```

### Concrete Decision Rules

**Rule 1: Classify before preserving**

Before version-controlling any agent output, ask:

| Question | If YES | If NO |
|---|---|---|
| Can this be reproduced from versioned harness assets? | Treat as build artifact; version the harness, not the output | Treat as handcrafted; version the output |
| Is this a prompt, guardrail, rule, skill, test, or NFR doc? | ALWAYS version — this is the harness | See above |
| Is this generated code that passed all gates? | Tag with source prompt/guardrail version; can regenerate | Fix the harness, not the code |

**Rule 2: Version the recipe, not the cake**

```
Version-control these (harness assets — durable):
  docs/canonical/           — authoritative patterns and constraints
  .opencode/skills/         — reusable capability wrappers
  AGENTS.md                 — universal non-functional requirements
  eslint.config.js          — mechanical constraint enforcement
  eslint-rules/             — custom constraint rules
  prompts/                  — source prompts for generation
  tests/                    — behavioral correctness constraints

Treat as build artifacts (disposable — reproducible):
  Generated components from a known prompt + harness version
  Boilerplate that a skill can regenerate
  Migration output where the migration script is versioned
```

**Rule 3: Model migration = compiler backend swap**

When upgrading models:

1. Freeze the harness (prompts, rules, skills, tests).
2. Re-run the same harness through the new model.
3. Compare output: what changed? Did quality improve or regress?
4. If regression: adjust harness constraints (optimization passes), not hand-patched code.
5. If improvement: consider simplifying model-specific compensations via [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]].

```
Migration checklist:
  [ ] Harness assets are versioned and tagged before migration
  [ ] Same prompts/constraints run through both old and new model
  [ ] Diff between old and new generated output is reviewed for regressions
  [ ] Model-specific compensations are re-evaluated (may be obsolete)
  [ ] Domain invariants are preserved regardless of model change
  [ ] Migration results recorded for future reference
```

## Compiler Pass Classification

When designing or auditing harness components, classify each by what kind of pass it performs:

| Pass Type | Examples in this repo | What it constrains |
|---|---|---|
| **Lexical/Syntax** | `eslint.config.js`, `eslint-rules/no-catch-message.js` | Code shape: no unsafe patterns, consistent style |
| **Structural** | (not yet implemented — see [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|classification]] Pattern 9) | Package privacy, dependency direction, schema ownership |
| **Semantic** | `.opencode/skills/issue-review/SKILL.md` (review scope) | Architecture decisions, security, correctness |
| **Behavioral** | `npm run test:unit`, `npm run test:regression:mock` | Runtime behavior, acceptance criteria |
| **Workflow** | `.opencode/skills/error-context-hygiene/SKILL.md` | Tool dispatch, error recovery, context hygiene |
| **Specification** | `AGENTS.md`, `docs/canonical/` docs | What "good" means across all dimensions |

Each pass runs at a different phase of the agent trajectory. Design passes so they surface at the moment they become actionable (see [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]).

## Integration with Existing Repo Infrastructure

This mental model connects existing repo infrastructure into a coherent narrative:

| Existing | Role in compiler model |
|---|---|
| [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] | Classifies harness passes as domain invariants (permanent) vs. model compensations (may simplify) |
| [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] | Governs when passes are BUILD, STABILIZE, SIMPLIFY, or REMOVE as models improve |
| [[AGENTS]] (Rule 16 rules) | Specification-level constraints loaded on every compilation |
| `eslint.config.js` + custom rules | Lexical/syntax passes that run automatically |
| `.opencode/skills/issue-review/SKILL.md` | Semantic pass that runs before merge |
| [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] | Controls which passes load at which phase |
| [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] | Budgets context across passes to avoid over-consumption |
| [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] | Validates that the compilation pipeline produces correct output |

### What this model adds

The repo already has classification (invariant-compensation), lifecycle (BUILD/STABILIZE/SIMPLIFY/REMOVE), and context delivery (hybrid stack, resolver disclosure). This skill adds:

- **A unified frame**: all these mechanisms are compiler passes working together on the same pipeline
- **The preservation rule**: prompts, rules, and docs are source code; generated output is build artifact
- **The migration pattern**: model upgrade = backend swap; recompile through the same harness, compare, adjust

## Quality Gates

Before declaring harness design work complete, verify:

- [ ] Every harness component can be classified as a domain invariant or model-specific compensation
- [ ] Prompts, guardrails, and NFR docs are version-controlled before generated code is committed
- [ ] Generated code committed to the repo is tagged with the harness version that produced it
- [ ] The model migration checklist is followed when upgrading model backends
- [ ] No harness component exists without a documented "what failure does this prevent" rationale
- [ ] Components classified as model-specific compensations have a removal or simplification plan tracked via [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]

## References

- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|Harness Engineering Analysis]]:59-63 — "LLM as fuzzy compiler, harness as optimization passes, code as disposable build artifact"
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/patterns|Harness Engineering Patterns]]:357-381 — Pattern 15: Durable Harness Asset Preservation
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|Harness Engineering Classification]]:295-309 — Classification as Missing
- [[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]] — classify harness controls as domain invariants vs. model compensations
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — BUILD/STABILIZE/SIMPLIFY/REMOVE lifecycle for harness components
- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] — load passes at the right phase
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]] — budget context across compiler passes

---

*Created: 2026-06-11 | Source: Harness Engineering pattern classification (Pattern 13 — Missing)*
