---
name: issue-start
description: "Claim a HoP GitHub issue, create an isolated worktree from main, and prepare a scoped execution brief before implementation."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: github
  priority: high
---

## What I Do

I handle the safe setup phase for HoP issue work: confirm the issue, claim it, create an isolated branch/worktree from `main`, read the project context, and produce a scoped execution brief before implementation begins.

## When to Use Me

Load this skill when:

- Starting work on any GitHub issue in HoP
- You need issue claim + branch + worktree setup
- You want a concise brief before editing code or docs

## Step-by-Step Workflow

Follow these steps in order. Do not write implementation code until setup is complete.

### Step 1 - Resolve the issue number

If the user gave an issue URL, extract the number. If they said "issue 42", use `42`.

```bash
gh issue view <N> --json number,title,body,assignees,labels,state
```

If the issue is missing or closed, stop and report.

### Step 2 - Check if already claimed

```bash
gh issue view <N> --json assignees,labels --jq '{assignees: [.assignees[].login], labels: [.labels[].name]}'
```

If `agent:working` exists or the issue is already assigned, stop and ask whether to proceed anyway. Do not steal active work silently.

### Step 3 - Claim the issue

```bash
gh label create "agent:working" --color "FFA500" --description "Agent session actively working on this issue" 2>/dev/null || true
gh issue edit <N> --add-assignee "@me" --add-label "agent:working"
gh issue comment <N> --body "Agent session started - $(date -u +%Y-%m-%dT%H:%M:%SZ)"
```

### Step 4 - Derive branch and worktree names

HoP issue branches use the observed convention:

```txt
issue/<N>-<slug>
```

Examples:

- Issue #123 "Fix tenant artifact paths" -> `issue/123-fix-tenant-artifact-paths`
- Issue #124 "Dashboard health panel regression" -> `issue/124-dashboard-health-panel-regression`
- Issue #125 "Crossroad logger parity" -> `issue/125-crossroad-logger-parity`

Use a short lowercase slug from the issue title. Keep it readable; do not encode implementation details.

```bash
BRANCH="issue/<N>-<slug>"
WORKTREE=".worktrees/<N>-<slug>"

echo "Branch:   $BRANCH"
echo "Worktree: $WORKTREE"
```

### Step 5 - Create the worktree

```bash
git fetch origin main
git worktree add -b "$BRANCH" "$WORKTREE" origin/main

echo "Worktree ready at: $WORKTREE"
echo "Branch: $BRANCH"
```

If the worktree or branch already exists, stop and inspect instead of deleting automatically. Only remove existing branches/worktrees with explicit user approval or when you created them in this session.

### Step 6 - Read HoP context

In the worktree, read the relevant context before implementation:

- `AGENTS.md`
- `docs/system-of-record.md`
- `agents/manifest.yaml`
- `README.md`
- Relevant `docs/canonical/`, `docs/decisions/`, `docs/guides/`, and `docs/evidence/`
- `DESIGN.md` for dashboard/UI work
- `.github/PULL_REQUEST_TEMPLATE.md`
- `docs/guides/crossroad-change-policy.md` if crossroad files may be touched

Also inspect adjacent code and tests for the specific surface:

- Operational scripts: `scripts/`
- Libraries/config/clients: `src/lib/`, `src/config/`, `src/clients/`, `src/persistence/`
- Runtime/test engine: `src/runner/`, `src/evaluator/`, `src/reporter/`, `src/orchestration/`
- Dashboard: `packages/dashboard/`
- Tests: `tests/`

### Step 7 - Generate an execution brief

Create a brief before implementation. Use a concise inline template. Save it only if the issue is non-trivial or the user wants an artifact. Prefer `docs/analysis/` for non-normative working notes unless the repo has an approved briefs directory.

Brief template:

```md
# Execution Brief - Issue #N: <title>

## Objective
<One sentence.>

## Success Criteria
- <Concrete, verifiable outcome>

## In Scope
- <Files/modules/behaviors included>

## Out of Scope
- <Explicit non-goals>

## Candidate Files
- <Likely files to modify>

## Sensitive Surfaces
- Tenant paths: <yes/no + details>
- Crossroad files: <yes/no + details>
- Env vars: <yes/no + details>
- Dashboard design: <yes/no + DESIGN.md relevance>
- Docs/ADR impact: <yes/no + docs>

## Implementation Strategy
<Steps and existing pattern to follow.>

## Validation Plan
- <npm script or manual QA command>
```

For trivial single-file fixes, a brief in the chat is enough.

### Step 8 - Report to the user

Report:

```txt
Issue #N claimed.
Branch:   issue/<N>-<slug>
Worktree: .worktrees/<N>-<slug>

Execution brief:
<brief summary>

Approve the brief to proceed, or request changes.
When implementation is complete, load the issue-review skill.
```

---

## Required Gate

Run `/compact` after setup and before implementation on non-trivial issues. The setup phase creates noisy context; implementation should start from the brief and relevant files.

## Safety Rules

- Never proceed silently if the issue is already claimed.
- Branch from `main`.
- Use `issue/<N>-<slug>` branch names.
- Do not delete existing worktrees/branches unless they were created by you in this session or the user approves.
- Do not modify `.runtime/` or `artifacts/` without considering `HOP_TENANT_ID` tenant isolation.
- Do not contradict accepted ADRs without surfacing the conflict.

## Quick Reference

```bash
gh issue edit N --add-assignee "@me" --add-label "agent:working"
gh issue comment N --body "Agent session started - $(date -u +%Y-%m-%dT%H:%M:%SZ)"
git fetch origin main
git worktree add -b "issue/N-short-slug" ".worktrees/N-short-slug" origin/main
```
