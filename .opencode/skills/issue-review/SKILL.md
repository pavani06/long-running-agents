---
name: issue-review
description: "Validate HoP issue work, open a draft PR against main, run a second-agent review, and stop for user confirmation before merge."
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: github
  priority: high
---

## What I Do

I sit between implementation and merge. I validate the worktree with HoP's real npm gates, create a draft PR targeting `main`, run a second-agent review on the diff, surface findings, and stop. Nothing merges until the user explicitly confirms.

## When to Use Me

Load this skill when:

- Implementation for a GitHub issue appears complete
- The user asks to open a PR or get ready for review
- You need CI-style validation and a second pass before merge

## Step-by-Step Workflow

### Step 1 - Identify context

You need:

- Issue number `N`
- Branch name, usually `issue/<N>-<slug>`
- Worktree path, usually `.worktrees/<N>-<slug>`

If any are unclear, ask the user or inspect with `git worktree list` and `gh issue view`.

---

## Required Gate

Run `/compact` before CI and PR creation on non-trivial work. Enter review with a clean context focused on the diff and validation output.

---

### Step 2 - Run validation in the worktree

Always run the relevant gates from `package.json`; do not invent commands.

Core review gates:

```bash
WORKTREE=".worktrees/N-SLUG"

npm --prefix "$WORKTREE" run test:regression:mock
npm --prefix "$WORKTREE" run ops:preflight
```

Add surface-specific gates when relevant:

Eval-sensitive changes include prompt, model, tool, context, memory, rubric, evaluator policy, agent-loop, sampling, corpus, or rollout-threshold changes. For those PRs, select validation from the eval tier registry documented in `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` and save the summary for the PR body's `Eval impact` section.

```bash
npm --prefix "$WORKTREE" run lint
npm --prefix "$WORKTREE" run test:unit
npm --prefix "$WORKTREE" run test:integration
npm --prefix "$WORKTREE" run dashboard:test
npm --prefix "$WORKTREE" run dashboard:build
npm --prefix "$WORKTREE" run test:fixture-parity
npm --prefix "$WORKTREE" run evidence:verify
npm --prefix "$WORKTREE" run test:ci-gates
npm --prefix "$WORKTREE" run ops:verify-branch-protection
```

`npm run smoke:live` requires live runtime/auth context and should be run only when the issue touches live runtime behavior and the user has approved the external interaction.

If a validation step fails, stop. Show the relevant error and fix before creating or updating the PR.

Save validation output summaries for the PR body.

For eval-sensitive PRs, also capture:

- Baseline and candidate versions for the affected prompt, model, tool, context, memory, rubric, or agent loop.
- Fast, medium, and deep tiers selected from the registry, plus skipped tiers and waiver rationale.
- Quality, latency, and cost deltas against explicit thresholds.
- Failing `case_id` or `trace_id` examples with expected behavior and current decision.
- Merge recommendation: pass, block, or waiver with owner and backfill date.

### Step 3 - Check HoP-specific gates

Before opening the PR, verify:

- Scope is limited to the issue.
- No unrelated cleanup or formatting churn.
- `.runtime/` and `artifacts/` changes, if any, respect `HOP_TENANT_ID` tenant isolation.
- Crossroad files are documented in the PR template if touched.
- Eval-sensitive changes include a completed `Eval impact` section in the PR body, not only generic test output.
- Any skipped eval tier has waiver rationale, owner, risk, and backfill date.
- Env var changes update `.env.example` and relevant docs.
- Dashboard/UI changes follow `DESIGN.md`.
- Behavior or architecture changes update relevant `docs/canonical/`, `docs/guides/`, `docs/evidence/`, or ADRs as appropriate.
- Accepted ADRs are not contradicted without a surfaced conflict.

### Step 4 - Create or update a draft PR

The PR targets `main` and should follow `.github/PULL_REQUEST_TEMPLATE.md`.

```bash
ISSUE_TITLE=$(gh issue view N --json title --jq '.title')
BRANCH="issue/N-slug"
WORKTREE=".worktrees/N-slug"

DIFF_STAT=$(git -C "$WORKTREE" diff --stat origin/main...HEAD)
COMMITS=$(git -C "$WORKTREE" log origin/main...HEAD --oneline)

PR_BODY=$(cat <<'PR_EOF'
## Resumo

<1-3 frases explicando o que mudou e por que.>

Closes #N

## Mudanças

- <Mudança principal>

## Testes

- [ ] `npm run test:regression:mock` passou
- [ ] `npm run ops:preflight` passou
- [ ] Nenhum teste novo quebrou

---

## Eval impact

N/A

## Crossroad-file impact

N/A
PR_EOF
)

git -C "$WORKTREE" push -u origin "$BRANCH"

gh pr create \
  --title "$ISSUE_TITLE" \
  --body "$PR_BODY" \
  --base main \
  --head "$BRANCH" \
  --draft
```

Fill the PR template accurately. If the diff touches prompt, model, tool, context, memory, rubric, or agent-loop behavior, replace `Eval impact` N/A with the eval report summary from Step 2. If any crossroad file changed, replace `N/A` with the full crossroad section: affected files, change type, migration/consumer impact, regression proof, mock parity if relevant, and code-owner approval expectation.

### Step 5 - Gather review context

```bash
WORKTREE=".worktrees/N-SLUG"

git -C "$WORKTREE" diff origin/main...HEAD
git -C "$WORKTREE" diff --stat origin/main...HEAD
git -C "$WORKTREE" log origin/main...HEAD --oneline
gh issue view N --json title,body --jq '"# " + .title + "\n\n" + .body'
```

### Step 6 - Run second-agent review

Delegate a review subagent with this scope:

```txt
TASK: Review the HoP diff for issue #N.

Review for:
- Correctness against issue scope and acceptance criteria
- Minimal change; no unrelated cleanup
- Tests and validation coverage for the changed surface
- Tenant isolation for `.runtime/` and `artifacts/`
- Crossroad file policy and PR template completeness
- Supabase client/mock parity if persistence files changed
- pino logging and redaction safety
- Config/env var documentation (`.env.example` and docs)
- Dashboard compliance with `DESIGN.md` if UI changed
- Documentation precedence and ADR conflicts
- Eval-sensitive PR evidence: tier registry selection, baseline/candidate versions, quality/latency/cost delta, threshold result, skipped-tier waiver, and failure examples
- Security: no secrets, no type suppressions, no unsafe external side effects

Report findings as BLOCKING or ADVISORY. Do not rewrite code.
```

Collect findings before proceeding.

---

## Required Gate

Run `/compact` after receiving review findings and before presenting the final review summary to the user.

---

### Step 7 - Surface findings and stop

Report:

```txt
## Review Complete - Issue #N: <title>

What we had to do:
<issue summary>

What changed:
<commit list and diff stat>

Validation:
- <commands run and outcomes>

Second-agent review:
- BLOCKING: <items or none>
- ADVISORY: <items or none>

PR: <draft PR URL>

To proceed, confirm "ship it" and I will load issue-finish.
To fix findings, update the worktree and rerun issue-review.
```

Do not merge. Wait for explicit user confirmation.

## Safety Rules

- Never merge without explicit user confirmation.
- Create draft PRs until the user approves merge readiness.
- Target `main`.
- Do not skip validation.
- Surface blocking findings before asking for merge confirmation.
- If CI or local gates fail, fix and rerun review.

## Quick Reference

```bash
npm --prefix .worktrees/N-slug run test:regression:mock
npm --prefix .worktrees/N-slug run ops:preflight
git -C .worktrees/N-slug push -u origin issue/N-slug
gh pr create --base main --head issue/N-slug --draft
git -C .worktrees/N-slug diff origin/main...HEAD
```
