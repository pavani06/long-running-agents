---
name: persona-based-documentation
description: "Write persona-specific Non-Functional Requirement (NFR) documents and load them via reviewer agents keyed to quality dimensions. Each team member documents their specialty (front-end architecture, reliability, security, product, performance) as a durable NFR file. Reviewer agents load persona-specific rubrics at review time instead of using generic quality criteria. Every agent session inherits all persona knowledge without consuming upfront context. Use when writing team convention docs, designing reviewer agents, setting up quality gates per dimension, or migrating from a single universal AGENTS.md to persona-specific NFRs. Triggers: 'persona documentation', 'persona NFR', 'persona-based doc', 'NFR by role', 'specialty documentation', 'role-based standards', 'reviewer rubric by persona', 'front-end standards doc', 'reliability standards doc', 'security standards doc', 'product requirements doc', 'multi-persona review'."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: documentation
  priority: high
  source: "Harness Engineering (Ryan Lopopolo, OpenAI — AI Engineer 2026)"
---

## What I Do

I ensure quality standards are inheritable across all agent sessions by splitting a single universal rule file into persona-specific Non-Functional Requirement (NFR) documents. I enforce four principles:

1. **Each quality dimension has an owner** — front-end architecture, reliability, security, product, and performance each get a dedicated NFR document authored by the person who owns that dimension
2. **Reviewer agents load persona rubrics, not generic criteria** — instead of one reviewer checking "code quality," multiple reviewers each check their dimension against documented standards
3. **Persona NFRs are loaded on-demand** — agents inherit all persona knowledge without upfront context cost via [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]
4. **Every agent session inherits the full team's taste** — a front-end agent gets reliability standards at review time; a backend agent gets product requirements at planning time

## When to Use Me

Load this skill when:

- Writing or updating team convention documents — split by persona instead of one monolithic file
- Designing a reviewer agent — define the persona rubric it will enforce
- Setting up quality gates per dimension (e.g., security review must check specific OWASP items)
- Onboarding a new team member — they document their specialty as a persona NFR
- Migrating from a single `AGENTS.md` to persona-specific NFR documents
- The team keeps repeating the same domain-specific feedback in code review — encode it in a persona NFR
- Multiple agent sessions produce inconsistent quality because standards are in people's heads

Do NOT use when:

- The team has fewer than 2 people — universal AGENTS.md is sufficient for solo work
- The quality dimension has no owner who can maintain the document
- You are writing a skill or workflow — this is for NFR documentation, not operational procedures
- The standard is already mechanically enforceable (lint rule, test) — prefer mechanical enforcement over documented preference

## The Anti-Pattern

```
ANTI-PATTERN: Single monolithic AGENTS.md with all quality standards,
reviewer agents using generic "check code quality" criteria, domain
knowledge trapped in individual engineers' heads.

Scenario:
  Team of 5 engineers. AGENTS.md has 16 universal rules.
  Reviewer agent checks "correctness, minimal change, tests, security."
  Front-end architect silently fixes React anti-patterns in every PR.
  Reliability engineer catches missing retry logic post-merge.
  Security person reviews only when tagged — half the PRs skip security review.
  Product manager's acceptance criteria live in Notion, never seen by agents.

Consequence:
  - Generic review misses domain-specific issues
  - Domain expertise doesn't compound across sessions
  - Human review remains the bottleneck for specialized quality dimensions
  - Agents repeat the same mistakes across different domains
  - "Bus factor" for quality standards = 1 per dimension
```

## The Pattern

```
PATTERN: Persona-specific NFR docs authored by dimension owners,
loaded via resolver-based disclosure, enforced by persona-keyed reviewer agents.

Structure:

  personas/
    front-end-architecture.md    ← React patterns, component design, state management
    reliability-engineering.md   ← retry logic, degradation, observability, alerting
    security.md                  ← auth, data handling, dependency audit, threat model
    product.md                   ← acceptance criteria, user flows, edge cases, UX rules
    performance.md               ← bundle size, latency budgets, caching strategy

  Each persona doc is:
    1. Authored by the dimension owner
    2. Versioned and reviewed like code
    3. Loaded by reviewer agents at PR time
    4. Cross-referenced by implementation agents via resolver triggers

  Reviewer agents load specific rubrics:
    Front-end reviewer    → loads personas/front-end-architecture.md
    Reliability reviewer  → loads personas/reliability-engineering.md
    Security reviewer     → loads personas/security.md
    (Product review still involves human — but agents see the documented criteria)
```

### The Mechanism

1. **Write persona NFRs** — each dimension owner documents what "good" looks like for their domain
2. **Register in resolver** — persona NFRs get trigger phrases so agents load them when relevant
3. **Create persona reviewer agents** — each reviewer loads ONE persona rubric and checks ONLY that dimension
4. **Run reviewers in parallel** — all persona reviewers run on every PR; each has narrow scope, reducing noise
5. **Human confirms** — the human sees a summary across all dimensions, not a wall of undifferentiated feedback

## Persona NFR Document Template

Each persona NFR document follows this structure:

```markdown
---
title: "Front-End Architecture NFR"
type: persona-nfr
persona: front-end-architecture
owner: <name>
tags: ["agentes-orquestracao", "governanca"]
last_updated: YYYY-MM-DD
relates-to: ["[[AGENTS]]", "[[docs/canonical/architecture-as-agent-affordance|Architecture as Agent Affordance]]"]
---

# Front-End Architecture NFR

## Scope

What this persona covers and does NOT cover.

## Mandatory Patterns

### Pattern: <Name>

- **Rule:** <concrete, checkable statement>
- **Why:** <one sentence on impact>
- **Example (correct):**
  ```typescript
  // DO: Component is small, stateless where possible, single responsibility
  ```
- **Example (incorrect):**
  ```typescript
  // DON'T: 400-line component handling rendering, state, API, and validation
  ```
- **How to verify:** <what a reviewer agent or lint rule checks>

## Conditional Patterns

Patterns that apply only in specific contexts (e.g., "when using React Query," "for dashboard pages").

## Prohibited Patterns

Things that should never appear in code this persona reviews.

## Interaction with Other Personas

How this persona's rules interact with or defer to other personas.
```

### Persona Identification Rules

Start with these canonical personas and add project-specific ones:

| Persona | Covers | Example rule topics |
|---|---|---|
| `front-end-architecture` | Component design, state management, rendering patterns, a11y, bundle size | Component size limits, state colocation, CSS methodology, React patterns |
| `reliability-engineering` | Error handling, retry logic, degradation, observability, alerting | Retry with backoff, circuit breakers, structured logging, graceful degradation |
| `security` | Auth, data handling, dependency audit, threat surface, secrets | Input validation, output encoding, dependency pinning, no secrets in logs |
| `product` | Acceptance criteria, user flows, edge cases, UX consistency | Happy path + 2 error states, mobile-first, loading/empty/error states |
| `performance` | Latency budgets, bundle size, caching, database queries | N+1 prevention, memoization rules, lazy loading thresholds |

Add project-specific personas when a dimension has a dedicated owner and > 5 rules:

| Trigger to add persona | Example persona |
|---|---|
| One person consistently catches the same class of issues in review | `api-design` — REST conventions, pagination, versioning |
| A domain has external compliance requirements | `data-privacy` — GDPR, data retention, PII handling |
| The stack has framework-specific conventions | `nextjs-patterns` — SSR vs. client, routing, middleware |

### Persona NFR Anti-Patterns

| Don't | Do instead |
|---|---|
| Write vague preferences ("code should be clean") | Write checkable rules ("no component over 200 lines; split into sub-components with explicit props") |
| Duplicate rules across personas | Cross-reference: "For auth patterns, see [[personas/security|Security NFR]]" |
| Overlap reviewer scopes (two reviewers checking the same thing) | Each reviewer checks exactly one persona dimension |
| Let persona docs go stale | Assign an owner; review quarterly via [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] |
| Write 50 rules per persona | Start with 5-10 highest-impact rules; add as review patterns emerge |

## Integration with Existing Repo Infrastructure

This skill connects to existing repo mechanisms:

| Existing | How persona docs integrate |
|---|---|
| [[AGENTS]] | Universal rules stay in AGENTS.md (commit style, security constraints, tool conventions). Persona NFRs are the domain-specific layer ON TOP of universal rules. |
| `.opencode/skills/issue-review/SKILL.md` | The review scope (Step 6) currently uses generic quality criteria. Replace with: "For each active persona, load the persona NFR and check ONLY that dimension. Report findings grouped by persona." |
| [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] | Register each persona NFR with triggers (e.g., "front-end change," "UI component," "React" → loads front-end NFR). Implementation agents get relevant standards; reviewers get all active personas. |
| [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] | Extend from model-based evaluators to persona-based evaluators: each council member represents a quality dimension with a dedicated rubric. |
| [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] | Persona reviewers become eval gates: each persona reviewer produces a pass/block/waiver signal for their dimension. |
| [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] | When a persona reviewer catches a recurring issue, the feedback loop creates a backlog item to strengthen that persona's NFR. |
| `.opencode/skills/analyze-and-improve/SKILL.md` | When extracting patterns from external sources, classify which persona should own each new pattern. |

### Migration Path from Universal AGENTS.md

Current state: single `AGENTS.md` with 16 universal rules.
Target state: `AGENTS.md` for universal rules + `personas/` for domain-specific NFRs.

```
Phase 1: Identify persona dimensions
  - List quality dimensions that have an owner on the team
  - For each, catalog the implicit rules that owner applies during review

Phase 2: Extract domain rules from AGENTS.md
  - Rules that are domain-specific move to persona NFRs
  - Rules that are universal (commit style, no secrets, search-before-code) stay in AGENTS.md
  - Rule 16 (Obsidian conventions) stays — it's universal

Phase 3: Write initial persona NFRs
  - Each owner writes 5-10 concrete, checkable rules for their dimension
  - Use the template above
  - Review as a team before activating

Phase 4: Create persona reviewer agents
  - One reviewer per active persona
  - Each loads exactly one persona NFR
  - Run in parallel on every PR
  - Report BLOCKING/ADVISORY grouped by persona

Phase 5: Iterate via Garbage Collection Day
  - Weekly: review which persona rules caught real issues
  - Strengthen rules that prevented bugs; relax rules that produced false positives
  - Add new rules when review reveals a recurring pattern
```

## Reviewer Agent Template

Each persona reviewer agent follows this contract:

```markdown
---
name: reviewer-<persona-slug>
description: "Persona reviewer for <persona-name>. Loads [[personas/<persona-slug>|<Persona Name> NFR]] and checks ONLY that dimension. Reports BLOCKING or ADVISORY findings."
---

## What I Do

I load the [[personas/<persona-slug>|<Persona Name> NFR]] and check the PR diff
against every mandatory and conditional rule in that document. I do NOT check
other dimensions — other persona reviewers handle those.

## Review Scope

ONLY check rules defined in [[personas/<persona-slug>|<Persona Name> NFR]].
For rules that cross-reference other personas, note the cross-reference
but do not evaluate it — let that persona's reviewer handle it.

## Output

Report findings as:

| Rule | Finding | Severity (BLOCKING/ADVISORY) | Location (file:line) |
|---|---|---|---|
| <rule name> | <what violates the rule> | BLOCKING | path/to/file.ts:42 |

Summary: X BLOCKING, Y ADVISORY.
```

## Quality Gates

Before declaring persona-based documentation complete, verify:

- [ ] Every active persona has a documented NFR file with an assigned owner
- [ ] Each persona NFR contains 5-10 concrete, checkable rules (not vague preferences)
- [ ] Persona NFRs do not duplicate rules — cross-reference instead
- [ ] Reviewer agents exist for each active persona and load exactly one NFR
- [ ] Persona NFRs are registered in the resolver with trigger phrases
- [ ] Universal rules remain in AGENTS.md; only domain-specific rules moved to personas
- [ ] The issue-review workflow loads all active persona reviewers in parallel
- [ ] Persona NFRs have a review cadence (quarterly, aligned with [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]])
- [ ] Garbage Collection Day includes a step: "which persona NFR rules caught real issues this week? which missed something?"

## References

- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|Harness Engineering Analysis]]:45 — "documentacao baseada em personas multiplica o efeito: cada membro do time documenta sua especialidade"
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/analysis|Harness Engineering Analysis]]:97-99 — Persona-based reviewer agents (front-end architect, reliability engineer, security)
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/patterns|Harness Engineering Patterns]]:15-37 — Pattern 1: Durable Non-Functional Requirements Memory
- [[docs/analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent.md/classification|Harness Engineering Classification]]:333-349 — Classification as Missing
- [[AGENTS]] — Current universal agent rules; domain-specific rules move to persona NFRs
- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] — Load persona NFRs on-demand by trigger
- [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] — Model for multi-evaluator architecture (extend to persona-based)
- [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] — Govern persona NFR lifecycle (review quarterly, simplify stale rules)
- [[docs/canonical/qa-to-backlog-feedback-loop|QA-to-Backlog Feedback Loop]] — Persona reviewer findings become backlog inputs
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — Persona reviewers as eval gates
- `.opencode/skills/issue-review/SKILL.md` — Current review workflow to extend with persona-based reviewers

---

*Created: 2026-06-11 | Source: Harness Engineering pattern classification (Pattern 15 — Missing)*
