#!/usr/bin/env bash
#
# repo-housekeeping.sh — READ-ONLY audit of what's safe to clean up.
#
# It NEVER deletes, switches, fetches, rebases, or moves anything. It inspects
# local state and prints the exact commands you can run by hand. This repo uses
# squash merges (so `git branch --merged` is unreliable) and a worktree-based
# issue flow, so the checks below decide "truly merged" by content diff, and
# they refuse to recommend removing any branch still tracking a live remote.
#
# Usage:  bash scripts/repo-housekeeping.sh
#
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

DEFAULT_BRANCH="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"
CURRENT="$(git branch --show-current || echo '(detached)')"

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
note() { printf '  %s\n' "$1"; }

bold "== Repo housekeeping audit (read-only) =="
note "default branch : $DEFAULT_BRANCH"
note "current branch : $CURRENT"
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
bold "Stale remote-tracking refs (remote branch deleted)"
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
SAFE=()
while IFS= read -r br; do
  [ "$br" = "$DEFAULT_BRANCH" ] && { note "$br  (default — keep)"; continue; }

  # gone upstream?  (its tracking ref no longer resolves)
  up_gone="no"
  if ! git rev-parse --verify --quiet "$br@{upstream}" >/dev/null 2>&1; then
    # either no upstream ever, or the upstream is gone
    if git config --get "branch.$br.remote" >/dev/null 2>&1; then
      up_gone="yes"
    fi
  fi

  # content fully contained in default branch?
  diffstat="$(git diff --stat "$DEFAULT_BRANCH" "$br" 2>/dev/null || echo 'diff-error')"

  if [ "$up_gone" = "yes" ] && [ -z "$diffstat" ]; then
    note "$br  ✅ MERGED + upstream gone — safe to delete"
    SAFE+=("$br")
  elif [ -z "$diffstat" ]; then
    note "$br  ~ content in $DEFAULT_BRANCH but upstream still live — LEAVE (running session?)"
  else
    note "$br  ✗ has unmerged content — LEAVE"
  fi
done < <(git for-each-ref --format='%(refname:short)' refs/heads/)
echo

# ── 5. Worktrees ────────────────────────────────────────────────────────────
bold "Worktrees"
git worktree list | sed 's/^/    /'
STALE_WT="$(git worktree list --porcelain | awk '/^worktree /{p=$2} /^prunable/{print p}')"
[ -n "$STALE_WT" ] && note "-> git worktree prune   (removes stale entries above)"
echo

# ── 6. Suggested commands (never executed here) ─────────────────────────────
if [ "${#SAFE[@]}" -gt 0 ]; then
  bold "Suggested deletions (run by hand — guardrail will ask you to authorize)"
  for br in "${SAFE[@]}"; do
    echo "    git branch -D $br"
  done
else
  bold "Nothing safe to delete. Repo is tidy."
fi
