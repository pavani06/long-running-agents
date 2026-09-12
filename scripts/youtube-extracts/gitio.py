"""Incremental commit+push of the extracts directory, for resilient backfills.

A long `full` backfill would otherwise write hundreds of files and commit only
at the end — one crash/timeout and everything is lost. Committing in batches
persists progress as it goes; a re-dispatch then resumes from the stateless diff.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

EXTRACTS_SUBDIR = "extracts/youtube/ai-learning"


def _git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo_root), *args], check=check,
                          capture_output=True, text=True)


def commit_push(repo_root: Path, message: str) -> bool:
    """Stage extracts/, commit, and push. Returns False when nothing was staged.

    On a non-fast-forward push (something else advanced the branch), rebase once
    and retry — so incremental pushes survive a concurrent commit.
    """
    _git(repo_root, "add", EXTRACTS_SUBDIR)
    if _git(repo_root, "diff", "--cached", "--quiet", check=False).returncode == 0:
        return False
    _git(repo_root, "commit", "-m", message)
    if _git(repo_root, "push", check=False).returncode != 0:
        _git(repo_root, "pull", "--rebase")
        _git(repo_root, "push")
    return True
