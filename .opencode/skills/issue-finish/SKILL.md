---
name: issue-finish
description: "After explicit user approval, merge a reviewed HoP PR into main and clean up the issue branch, worktree, and agent labels."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: github
  priority: high
---

## What I Do

I handle the final merge and cleanup after the user says "ship it": verify PR state, confirm required checks and approvals, merge into `main`, close the issue with a summary, remove the issue worktree/branch, and release `agent:working`.

## When to Use Me

Load this skill only when:

- `issue-review` has run
- Blocking findings are resolved or explicitly accepted by the user
- A draft/open PR exists
- The user explicitly confirmed merge, e.g. "ship it" or "merge it"

## Step-by-Step Workflow

### Step 1 - Confirm context

You need:

- Issue number `N`
- Branch name, usually `issue/<N>-<slug>`
- Worktree path, usually `.worktrees/<N>-<slug>`
- PR number or URL

```bash
gh pr view "$BRANCH" --json number,state,isDraft,mergeStateStatus,statusCheckRollup,reviewDecision,url,baseRefName,headRefName
```

If the PR is not open, check whether it was already merged. If not merged, stop and report.

---

## Required Gate

Run `/compact` before merge and cleanup. The finish sequence is mechanical and should not carry noisy implementation context.

---

### Step 2 - Verify merge readiness

Check:

- Base branch is `main`.
- Required checks are green or clearly not applicable.
- Required approval and code-owner review are present when needed.
- PR is ready for review, or will be marked ready immediately before merge.
- Crossroad file section is complete if crossroad files changed.
- Docs/ADR/design impact was handled or explicitly accepted.

Recommended commands:

```bash
gh pr view "$BRANCH" --json number,title,isDraft,baseRefName,reviewDecision,statusCheckRollup,files,url
git -C "$WORKTREE" diff --name-only origin/main...HEAD
```

If checks are red, approvals are missing, or blocking review findings remain, stop and report.

### Step 3 - Verify HoP documentation and risk surfaces

Inspect changed files against HoP rules:

| If PR touches... | Verify... |
|---|---|
| `.runtime/` or `artifacts/` paths | Tenant isolation via `HOP_TENANT_ID` or path helpers |
| Crossroad files | PR has crossroad impact, migration/consumer notes, regression proof, code-owner path |
| `.env.example` or config | README/docs explain env behavior when needed |
| Supabase persistence | Mock parity and relevant migration/check command |
| Dashboard/UI | `DESIGN.md` constraints are respected |
| Canonical behavior or architecture | Relevant canonical doc, guide, evidence, or ADR impact is addressed |
| GitHub workflows or branch protection | CI gate docs and branch protection drift are considered |

Surface missing documentation or unresolved risk before merging. Block only when it affects acceptance criteria, required review, CI, security, tenant isolation, or crossroad policy.

### Step 4 - Mark ready and merge

```bash
BRANCH="issue/N-slug"
PR_URL=$(gh pr view "$BRANCH" --json url --jq '.url')
PR_NUMBER=$(gh pr view "$BRANCH" --json number --jq '.number')
PR_TITLE=$(gh pr view "$BRANCH" --json title --jq '.title')

gh pr ready "$BRANCH" 2>/dev/null || true

gh pr merge "$BRANCH" \
  --squash \
  --subject "${PR_TITLE} (#${PR_NUMBER})" \
  --delete-branch
```

If merge fails due to conflicts or failing checks, stop. Fix in the worktree and rerun `issue-review`.

### Step 5 - Close the issue with a summary

```bash
gh issue close N --comment "Completed by ${PR_URL}

Merged into main via squash."
```

If the issue is already closed, treat it as success and continue cleanup.

### Step 6 - Remove the worktree and local branch

Clean only the current issue branch/worktree unless the user explicitly asked for broader pruning.

```bash
WORKTREE=".worktrees/N-slug"
BRANCH="issue/N-slug"

if [ -d "$WORKTREE" ]; then
  if [ -n "$(git -C "$WORKTREE" status --porcelain)" ]; then
    echo "Worktree has uncommitted changes; cleanup skipped: $WORKTREE"
    exit 1
  fi
  git worktree remove "$WORKTREE"
fi

if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git branch -D "$BRANCH"
fi

if [ -d "$WORKTREE" ]; then
  echo "Worktree still exists after cleanup: $WORKTREE"
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  echo "Local branch still exists after cleanup: $BRANCH"
  exit 1
fi

git remote prune origin
```

### Step 7 - Release the issue claim

```bash
gh issue edit N --remove-label "agent:working" 2>/dev/null || true
```

If cleanup fails mid-way, release `agent:working` first and comment with the remaining manual cleanup.

### Step 8 - Final status report

Report only what actually completed. If cleanup was partial, report the remaining manual steps instead of marking them done.

```txt
## Done - Issue #N

PR merged: <PR_URL>
Issue closed: #N
Remote branch deleted: issue/N-slug
Worktree removed: .worktrees/N-slug
Label released: agent:working

Pull main to get the merged changes:
  git pull origin main
```

## Failure Handling

| Problem | What to do |
|---|---|
| PR has conflicts | Stop, report, fix in worktree, rerun issue-review |
| CI/checks are red | Stop, report, fix, rerun issue-review |
| Approval missing | Stop and request review/approval |
| PR already merged | Continue issue/worktree/label cleanup |
| Issue already closed | Continue worktree/label cleanup |
| Worktree already removed | Skip worktree removal and continue |

## Safety Rules

- Never run without prior review and explicit user confirmation.
- Never force-merge.
- Merge into `main` only.
- Use squash merge for traceability.
- Clean only the current issue branch/worktree unless asked otherwise.
- Always release `agent:working`, even after partial cleanup failures.

## Quick Reference

```bash
gh pr ready issue/N-slug 2>/dev/null || true
gh pr merge issue/N-slug --squash --delete-branch
gh issue close N --comment "Completed by <PR_URL>"
git worktree remove .worktrees/N-slug
git branch -D issue/N-slug
gh issue edit N --remove-label "agent:working"
```
