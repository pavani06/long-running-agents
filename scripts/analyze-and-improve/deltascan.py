"""Git delta scan: which index-target files changed since the last indexed commit.

The semantic index is rebuilt only for the files the delta scan flags, so the
job stays cheap on incremental runs. The git call is I/O; the path-selection
logic (`under_targets`) is pure and unit-tested.

Targets are the repo's authoritative knowledge layers — the surfaces the
classifier (Fase 3) retrieves against.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

DEFAULT_TARGETS: tuple[str, ...] = (
    "docs/canonical/",
    "docs/decisions/",
    "curriculum/",
    ".opencode/skills/",
)


def under_targets(paths, targets: tuple[str, ...] = DEFAULT_TARGETS) -> list[str]:
    """Keep only `.md` paths under one of the target prefixes, sorted, deduped."""
    keep = {
        p for p in paths
        if p.endswith(".md") and any(p.startswith(t) for t in targets)
    }
    return sorted(keep)


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo_root), *args],
                          check=True, capture_output=True, text=True)


def changed_files(repo_root: Path, base: str, head: str = "HEAD",
                  targets: tuple[str, ...] = DEFAULT_TARGETS) -> list[str]:
    """Target `.md` files that changed between `base` and `head` (added/modified)."""
    out = _git(repo_root, "diff", "--name-only", "--diff-filter=d", base, head).stdout
    return under_targets(out.splitlines(), targets)


def deleted_files(repo_root: Path, base: str, head: str = "HEAD",
                  targets: tuple[str, ...] = DEFAULT_TARGETS) -> list[str]:
    """Target `.md` files deleted between `base` and `head`."""
    out = _git(repo_root, "diff", "--name-only", "--diff-filter=D", base, head).stdout
    return under_targets(out.splitlines(), targets)


def full_scan(repo_root: Path, targets: tuple[str, ...] = DEFAULT_TARGETS) -> list[str]:
    """Every tracked target `.md` file — the input for the initial full index."""
    out = _git(repo_root, "ls-files", "-z", *targets).stdout
    paths = [p for p in out.split("\0") if p]
    return under_targets(paths, targets)


def head_sha(repo_root: Path) -> str:
    """Current HEAD commit — stored in the index so the next run can delta from it."""
    return _git(repo_root, "rev-parse", "HEAD").stdout.strip()
