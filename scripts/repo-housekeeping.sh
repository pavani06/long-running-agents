#!/usr/bin/env bash
#
# repo-housekeeping.sh — READ-ONLY audit of what's safe to clean up.
#
# It NEVER deletes, switches, fetches, or rebases. It inspects local + remote
# state and prints the exact commands you can run by hand.
#
# Merge detection: the PR state on GitHub is the authority (`gh pr list --head`).
# A squash merge rewrites SHAs, so `git branch --merged` is unreliable; and once
# `main` advances past a branch, `git diff --stat main <branch>` reports a huge
# false "divergence" (all the work main gained AFTER the merge). So we ask GitHub
# whether the branch's PR is MERGED, and fall back to the content diff only when
# `gh` is unavailable.
#
# Usage:  bash scripts/repo-housekeeping.sh
#
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

DEFAULT_BRANCH="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"
CURRENT="$(git branch --show-current || echo '(detached)')"

GH_OK="no"
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then GH_OK="yes"; fi

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
note() { printf '  %s\n' "$1"; }

# PR state for a branch head: MERGED | OPEN | CLOSED | none | unknown
pr_state() {
  [ "$GH_OK" = "yes" ] || { echo "unknown"; return; }
  gh pr list --head "$1" --state all --limit 1 --json state \
    --jq '.[0].state // "none"' 2>/dev/null || echo "unknown"
}

# Branches checked out in ANY worktree — never deletable, and likely a live
# session even if their PR already merged. `git branch --show-current` only sees
# this worktree, so ask git for all of them.
WT_BRANCHES="$(git worktree list --porcelain | sed -n 's#^branch refs/heads/##p')"
is_checked_out() { printf '%s\n' "$WT_BRANCHES" | grep -qxF "$1"; }

bold "== Repo housekeeping audit (read-only) =="
note "default branch : $DEFAULT_BRANCH"
note "current branch : $CURRENT"
note "gh available   : $GH_OK  ($([ "$GH_OK" = yes ] && echo 'PR state is authoritative' || echo 'falling back to content diff'))"
echo

# ── 1. Working tree ─────────────────────────────────────────────────────────
bold "Working tree"
if [ -n "$(git status --porcelain)" ]; then
  note "DIRTY — commit or stash before cleaning:"
  git status --short | sed 's/^/    /'
else
  note "clean"
fi
echo

# ── 2. Default branch vs its remote ─────────────────────────────────────────
bold "$DEFAULT_BRANCH sync"
if git rev-parse --verify --quiet "$DEFAULT_BRANCH" >/dev/null; then
  UP="$(git rev-parse --abbrev-ref "$DEFAULT_BRANCH@{upstream}" 2>/dev/null || echo '')"
  if [ -n "$UP" ]; then
    BEHIND="$(git rev-list --count "$DEFAULT_BRANCH..$UP" 2>/dev/null || echo 0)"
    AHEAD="$(git rev-list --count "$UP..$DEFAULT_BRANCH" 2>/dev/null || echo 0)"
    note "behind $UP by $BEHIND, ahead by $AHEAD"
    [ "$BEHIND" -gt 0 ] && note "-> git checkout $DEFAULT_BRANCH && git pull --ff-only origin $DEFAULT_BRANCH"
  else
    note "no upstream configured"
  fi
else
  note "no local $DEFAULT_BRANCH branch"
fi
echo

# ── 3. Stale remote-tracking refs ───────────────────────────────────────────
bold "Stale remote-tracking refs (remote branch already deleted)"
STALE="$(git remote prune origin --dry-run 2>/dev/null | sed -n 's/.*\[would prune\] //p' || true)"
if [ -n "$STALE" ]; then
  echo "$STALE" | sed 's/^/    /'
  note "-> git remote prune origin   (safe, reversible)"
else
  note "none"
fi
echo

# ── 4. Local branches: safe to delete? ──────────────────────────────────────
bold "Local branches"
SAFE_LOCAL=()
while IFS= read -r br; do
  [ "$br" = "$DEFAULT_BRANCH" ] && { note "$br  (default — keep)"; continue; }
  is_checked_out "$br"          && { note "$br  (checked out in a worktree — keep)"; continue; }

  state="$(pr_state "$br")"
  diffstat="$(git diff --stat "$DEFAULT_BRANCH" "$br" 2>/dev/null || echo 'diff-error')"

  if [ "$state" = "MERGED" ]; then
    note "$br  ✅ PR MERGED — safe to delete"
    SAFE_LOCAL+=("$br")
  elif [ "$state" = "unknown" ] && [ -z "$diffstat" ]; then
    note "$br  ✅ content contained in $DEFAULT_BRANCH (no gh) — safe to delete"
    SAFE_LOCAL+=("$br")
  elif [ "$state" = "OPEN" ]; then
    note "$br  ~ PR OPEN — LEAVE (in review)"
  else
    note "$br  ✗ PR ${state} — LEAVE (unmerged / running session)"
  fi
done < <(git for-each-ref --format='%(refname:short)' refs/heads/)
echo

# ── 5. Remote leftover branches (merged PR, branch never deleted) ───────────
bold "Remote branches with a MERGED PR (leftovers on GitHub)"
SAFE_REMOTE=()
if [ "$GH_OK" = "yes" ]; then
  while IFS= read -r rb; do
    case "$rb" in
      "$DEFAULT_BRANCH"|HEAD|dependabot/*) continue ;;
    esac
    if [ "$(pr_state "$rb")" = "MERGED" ]; then
      note "origin/$rb  ✅ MERGED — safe to delete on remote"
      SAFE_REMOTE+=("$rb")
    fi
  done < <(git ls-remote --heads origin 2>/dev/null | sed 's#.*refs/heads/##')
  [ "${#SAFE_REMOTE[@]}" -eq 0 ] && note "none"
else
  note "skipped (needs gh)"
fi
echo

# ── 6. Worktrees ────────────────────────────────────────────────────────────
bold "Worktrees"
git worktree list | sed 's/^/    /'
STALE_WT="$(git worktree list --porcelain | awk '/^worktree /{p=$2} /^prunable/{print p}')"
[ -n "$STALE_WT" ] && note "-> git worktree prune   (removes stale entries above)"
echo

# ── 7. Suggested commands (never executed here) ─────────────────────────────
if [ "${#SAFE_LOCAL[@]}" -gt 0 ] || [ "${#SAFE_REMOTE[@]}" -gt 0 ]; then
  bold "Suggested cleanup (run by hand — guardrail will ask you to authorize -D)"
  for br in "${SAFE_LOCAL[@]:-}";  do [ -n "$br" ] && echo "    git branch -D $br"; done
  [ "${#SAFE_REMOTE[@]}" -gt 0 ] && echo "    git push origin --delete ${SAFE_REMOTE[*]}"
  echo "    git remote prune origin   # tidy tracking refs afterward"
else
  bold "Nothing safe to delete. Repo is tidy."
fi
