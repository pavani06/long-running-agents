---
title: "Agent Lifecycle"
type: canonical
tags: ["agentes-orquestracao", "governanca", "harness-engineering"]
aliases: ["issue lifecycle", "agent issue lifecycle", "issue claim protocol", "claim worktree review merge cleanup", "HoP issue lifecycle"]
last_updated: 2026-09-02
relates-to: ["[[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/skill-testing-conventions|Skill Testing Conventions]]"]
sources: ["[[.opencode/skills/orchestrator/SKILL.md|orchestrator skill]]", "[[.opencode/skills/issue-start/SKILL.md|issue-start skill]]", "[[.opencode/skills/issue-review/SKILL.md|issue-review skill]]", "[[.opencode/skills/issue-finish/SKILL.md|issue-finish skill]]", "[[.opencode/skills/issue-workflow/SKILL.md|issue-workflow skill]]"]
---

# Agent Lifecycle

**Type:** canonical
**Status:** active
**Source:** repository mechanics — `.opencode/skills/` issue lifecycle skills
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

The HoP issue lifecycle existed in practice, but it was split across five skills with no single named model, and the claim contract had drifted: `issue-workflow` claimed issues with an `in-progress` label and a divergent comment scheme, while `orchestrator`, `issue-start`, and `issue-finish` operate on the `agent:working` label. An agent loading the wrong skill broke the claim protocol that the orchestrator dashboard and the finish cleanup expect: active-issue detection reads `agent:working` (`.opencode/skills/orchestrator/SKILL.md:49`), and release paths remove `agent:working` (`.opencode/skills/issue-finish/SKILL.md:150`, `.opencode/skills/orchestrator/SKILL.md:134,143`), so an `in-progress` claim was invisible to both.

Consequences before unification (resolved by epic #208 / issue #209, commit `7f8f325`, 2026-09-02):

1. An issue claimed via `issue-workflow` did not appear as active in the orchestrator dashboard.
2. Completion via `issue-workflow` removed a label nobody else consumed, leaving the real label semantics to the other skills.
3. The [[docs/system-of-record|System of Record]] carried `agent-lifecycle.md` as a pending canonical doc, and [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] listed "a single canonical closed-loop OS model" as missing piece number 1 of its Partial Coverage classification (`docs/canonical/closed-loop-agent-operating-system.md:65`).

## Solution

One issue-driven work lifecycle with five operational components and one claim contract.

### The five components

| # | Component | Skill | Contract |
|---|---|---|---|
| 1 | Selection / orchestration | `orchestrator` | Dashboard of issues/PRs/worktrees/labels; skip `agent:working` then `blocked`, honor priority labels, prefer unassigned, else lowest-numbered open issue; generate worker prompts; clean idle sessions. Never writes implementation code. |
| 2 | Claim + isolation | `issue-start` | Resolve issue number; refuse to steal active work (`agent:working` present or assigned, `.opencode/skills/issue-start/SKILL.md:38-44`); claim with assignee `@me` + label `agent:working` + "Agent session started" comment (`:46-52`); derive branch `issue/<N>-<slug>` and worktree `.worktrees/<N>-<slug>` from `origin/main` (`:54-88`); read context and produce an execution brief before implementation (`:90-149`). |
| 3 | Implementation + tracking | `issue-workflow` | Session start adds `agent:working` and posts the work plan (`.opencode/skills/issue-workflow/SKILL.md:12-16`, label at `:15`); acceptance-criteria checkboxes are updated as work completes (`:18-20`); progress comments are optional (`:116-134`); a handoff comment is mandatory at session end (`:143-164`). Also owns issue creation templates for epics and sub-issues (`:35-82`). |
| 4 | Review | `issue-review` | Run the real npm gates from `package.json` in the worktree (`.opencode/skills/issue-review/SKILL.md:44-77`); check scope, tenant isolation, crossroad, and docs impact (`:87-101`); open a draft PR against `main` with the PR template (`:102-153`); run a second-agent review surfacing BLOCKING/ADVISORY findings (`:155-190`); stop — nothing merges without explicit human confirmation (`:226-236`). |
| 5 | Finish + cleanup | `issue-finish` | Only after explicit user approval: verify merge readiness (`:50-68`), squash merge with traceable subject (`:86-100`), close the issue with a summary (`:104-112`), remove worktree and branch (`:114-145`), and always release `agent:working` — even after partial cleanup failures (`:147-153,190`). |

### Invariants

1. **One claim label.** `agent:working` is the single marker of an active issue. The orchestrator uses it to detect active work and to release stale claims; every other lifecycle skill must claim and release exactly this label.
2. **Isolation per issue.** Branch from `main`, name `issue/<N>-<slug>`, work in `.worktrees/<N>-<slug>`. Never reuse another issue's worktree.
3. **Review gate.** Merge happens only through `issue-review` (draft PR + second-agent findings resolved) followed by `issue-finish` (explicit approval). The orchestrator never merges or closes.
4. **Claim is always released.** Normal finish, orchestrator idle cleanup, and blocker handling all end with `--remove-label "agent:working"`, so a failed session never leaves a phantom active issue.
5. **Handoff over memory.** Session state leaves the transcript in the issue: claim comment in, handoff comment out; checkboxes carry acceptance-criteria truth.

## Implementation in this repo

- `.opencode/skills/orchestrator/SKILL.md` — dashboard `:27-49`, priority order `:51-66`, worker prompt generation `:74-98`, idle/completed cleanup with label release `:100-163`, blocker handling `:165-179`, safety rules `:181-188`.
- `.opencode/skills/issue-start/SKILL.md` — claim-check `:38-44`, claim `:46-52`, branch/worktree derivation `:54-88`, context reading `:90-109`, execution brief `:111-149`.
- `.opencode/skills/issue-workflow/SKILL.md` — mandatory behaviors `:10-31`, issue creation `:35-82`, session checklist with `agent:working` `:96-115`, handoff `:143-164`, completion with label release `:168-201`, labels reference `:205-210`.
- `.opencode/skills/issue-review/SKILL.md` — gates `:44-77`, HoP checks `:87-101`, draft PR `:102-153`, second-agent review `:155-190`.
- `.opencode/skills/issue-finish/SKILL.md` — merge `:86-102`, close with summary `:104-112`, worktree/branch cleanup `:114-145`, claim release `:147-153`.
- [[docs/system-of-record|System of Record]] — the "Agentes e orquestração" domain table maps all five skills into the project's agent system.

The 2026-09-02 unification (epic #208, issue #209, commit `7f8f325`) migrated `.opencode/skills/issue-workflow/SKILL.md` from `in-progress` to `agent:working` (8 occurrences: original lines `:15, :29, :102, :103, :198, :210, :226, :237`), demoted progress comments to optional, and confirmed zero GitHub issues carried the legacy label in any state. Mentions of `in-progress` in `docs/analysis/` are historical records and are intentionally not rewritten.

## Tradeoffs

| Benefit | Cost |
|---|---|
| One label makes active work machine-readable for any agent or dashboard | Any skill that drifts from the label silently breaks active-issue detection — the exact failure this doc closes |
| Per-issue worktrees allow safe parallel agent sessions | `.worktrees/` accumulates; cleanup is a mandatory extra step with guards against deleting uncommitted work |
| Mandatory handoff makes any issue resumable by a fresh session with zero conversational context | Every session pays a structured writeback cost at start and end |
| Human confirmation gates merge and close | Adds approval latency at the end of each issue; blockers need an explicit escalation path (orchestrator blocker handling) |

## Relationship to Other Patterns

- **Distinct from:** [[docs/canonical/alarm-clock-agent-lifecycle|Alarm-Clock Agent Lifecycle]]. The term "agent lifecycle" is used by two canonical docs with different meanings: alarm-clock is the fleet scheduling primitive (self-set wake → work → sleep for long-running agents across hours or days); this doc is the repository's issue-driven work lifecycle (claim → worktree → implement → review → merge → cleanup). They share no mechanism.
- **Materializes:** [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] — this lifecycle is the concrete execution-routing, ownership, and validation surface of the closed-loop OS (`docs/canonical/closed-loop-agent-operating-system.md:30-45`), and closes the "single canonical closed-loop OS model" gap for the issue-workflow slice.
- **Feeds:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — failures of the lifecycle itself (divergent claim labels, blind telemetry) become durable regression cases in `docs/evidence/`.
- **Tested by:** [[docs/canonical/skill-testing-conventions|Skill Testing Conventions]] — changes to lifecycle skills are validated with the repo's real npm gates, not invented commands.

## References

- `.opencode/skills/orchestrator/SKILL.md:27-66,100-163,165-179` — selection, cleanup, and blocker mechanics.
- `.opencode/skills/issue-start/SKILL.md:38-88,111-149` — claim, worktree isolation, execution brief.
- `.opencode/skills/issue-workflow/SKILL.md:10-31,96-115,143-164,168-201` — tracking contract post-unification.
- `.opencode/skills/issue-review/SKILL.md:44-190` — validation, draft PR, second-agent review.
- `.opencode/skills/issue-finish/SKILL.md:86-153` — merge, close, cleanup, claim release.
- [[docs/system-of-record|System of Record]] — documentation precedence and agent domain map.
- `docs/analysis/2026-09-01-adversarial-review-cl-epic-3-territory.md` — territory diagnosis that grounded the unification decision (F-A6: `in-progress` had zero GitHub consumers).

---

*Created: 2026-09-02 | From: epic #208 (CL-EPIC 3) lifecycle unification | Precedence: canonical*
