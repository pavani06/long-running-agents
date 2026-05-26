---
name: orchestrator
description: "Manage parallel HoP GitHub issue agents: show work status, suggest next issues, generate prompts, and clean idle sessions."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: github
  priority: high
---

## What I Do

I coordinate parallel HoP agent sessions across GitHub issues. I do not implement product/code changes. I fetch state, summarize active work, suggest the next issue, generate prompts for worker sessions, and clean up idle or completed sessions.

Agents are tracked by issue number. For example, "Agent #123" means the session working on GitHub issue #123.

## When to Use Me

Load this skill when:

- You want a dashboard of open issues, PRs, and worktrees
- You need to assign an issue to a new agent session
- An agent reports idle or abandoned work
- You want to know what issue should be picked up next

## Phase 1 - Dashboard

Gather these in parallel when possible:

```bash
gh issue list --state open --json number,title,labels,assignees --limit 100
gh pr list --state open --json number,title,headRefName,isDraft,url --limit 50
git worktree list --porcelain
gh label list --limit 200
```

Present a compact table:

```txt
## Dashboard

| # | Issue Title | Labels | Assignee | PR | Worktree | Status |
|---|-------------|--------|----------|----|----------|--------|
| 123 | Fix tenant artifact paths | priority:P1 | bot | #130 draft | .worktrees/123-... | active |
| 124 | Dashboard health panel regression | - | - | - | - | ready |
```

Mark issues with `agent:working` as active. Put `blocked` issues at the bottom. If the repo has no `blocked` label, treat only explicit issue labels/status as blockers.

## Phase 2 - Suggest Next Task

Do not assume historical label systems. Discover labels first with `gh label list`.

Priority order:

1. Skip issues with `agent:working`.
2. Skip issues with `blocked` if that label exists.
3. Honor priority labels if present, in order `priority:P0` -> `priority:P4`.
4. Prefer unassigned issues over assigned issues.
5. If no priority signal exists, suggest the lowest-numbered open unblocked issue.
6. If an issue body says `blocked by #N`, check that blocker is closed before suggesting it.

```bash
gh issue view <BLOCKER_N> --json state --jq '.state'
```

Output:

```txt
Suggested next: #123 "Fix tenant artifact paths" (priority:P1, unassigned, no open blockers)
```

## Phase 3 - Assign Issue and Generate Worker Prompt

When the user says "assign #N", generate a prompt for a new worker session.

```txt
Work on HoP issue #N: "<title>".

Load skill `issue-start` and claim issue #N.

After setup, implement the issue in the created worktree. Follow:
- `AGENTS.md`
- `docs/system-of-record.md`
- `agents/manifest.yaml`
- `README.md`
- Relevant `docs/canonical/`, `docs/decisions/`, `docs/guides/`, and `docs/evidence/`
- `DESIGN.md` for dashboard/UI work

Use the minimum viable change. Respect tenant isolation for `.runtime/` and `artifacts/`. If crossroad files are touched, follow `.github/PULL_REQUEST_TEMPLATE.md`, `.github/CODEOWNERS`, and `docs/guides/crossroad-change-policy.md`.

When implementation is complete, load skill `issue-review`. Fix blocking findings and rerun review.

When review passes and the user explicitly confirms merge, load skill `issue-finish`.
```

Do not add extra implementation instructions unless the issue requires them.

## Phase 4 - Agent Idle or Completed

When the user reports "Agent #N idle", inspect before cleanup.

### Step 1 - Check issue and PR state

```bash
N=<issue_number>

gh issue view "$N" --json state,title,labels,assignees
gh pr list --state all --search "#$N" --json number,state,mergedAt,headRefName,url --limit 20
git worktree list --porcelain
```

### Step 2 - If issue is closed or PR is merged

Clean up only that issue's worktree/branch.

```bash
N=<issue_number>
WORKTREE=$(git worktree list --porcelain | awk -v n="/$N-" '/^worktree / {path=$2} path ~ n {print path; exit}')

if [ -n "$WORKTREE" ] && [ -d "$WORKTREE" ]; then
  if [ -n "$(git -C "$WORKTREE" status --porcelain)" ]; then
    echo "Worktree has uncommitted changes; cleanup skipped: $WORKTREE"
  else
    BRANCH=$(git -C "$WORKTREE" rev-parse --abbrev-ref HEAD 2>/dev/null || true)
    git worktree remove "$WORKTREE"
    if [ -n "$BRANCH" ] && git show-ref --verify --quiet "refs/heads/$BRANCH"; then
      git branch -D "$BRANCH"
    fi
  fi
fi

gh issue edit "$N" --remove-label "agent:working" 2>/dev/null || true
git remote prune origin
```

### Step 3 - If issue is not done and the agent stopped

Release the claim so another session can continue.

```bash
gh issue edit "$N" --remove-label "agent:working" 2>/dev/null || true
gh issue edit "$N" --remove-assignee "@me" 2>/dev/null || true
gh issue comment "$N" --body "Agent session ended without completion - $(date -u +%Y-%m-%dT%H:%M:%SZ). Issue returned to queue."
```

Do not delete a worktree containing uncommitted work unless the user explicitly approves. Report its path for manual inspection.

### Step 4 - Suggest next

Run Phase 2 and present the next suggestion.

```txt
## Agent #N - Cleaned Up

Issue #N: <closed | returned to queue | needs manual inspection>
Worktree: <removed | retained at path>
Branch: <deleted | retained>
Label: agent:working released

Suggested next: #M "Next issue title" (<labels/status>)
```

## Phase 5 - Blocker Handling

If a worker cannot resolve blocking findings after three materially different attempts:

1. Ensure the attempts and current blocker are documented.
2. Add `blocked` if the label exists, otherwise add a comment only and surface that the label is missing.
3. Release `agent:working` unless the user wants the issue retained by that agent.
4. Suggest the next unblocked issue.

```bash
if gh label list --limit 200 --json name --jq '.[].name' | grep -qx "blocked"; then
  gh issue edit N --add-label "blocked"
fi
gh issue comment N --body "Blocked: <brief reason>. Needs manual intervention."
```

## Safety Rules

- Do not write implementation code in orchestrator mode.
- Do not merge or close issues directly; `issue-finish` handles merge/close after confirmation.
- Do not assign an issue with `agent:working` without user confirmation.
- Verify blocker state before suggesting dependent issues.
- Do not delete worktrees with uncommitted work without approval.
- Always release stale `agent:working` labels when an agent stops and the issue is returned to the queue.

## Quick Reference

```bash
gh issue list --state open --json number,title,labels,assignees --limit 100
gh pr list --state open --json number,title,headRefName,isDraft,url --limit 50
git worktree list --porcelain
gh label list --limit 200
gh issue edit N --remove-label "agent:working"
```
