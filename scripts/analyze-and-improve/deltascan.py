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
# The index covers prose by default. A caller can widen the extensions (e.g. to
# include code) so the classifier can retrieve against code mechanisms too — the
# #288 diagnostic showed a docs-only index can't surface a concept implemented in
# `scripts/*.py`. The production default stays `.md`-only.
DEFAULT_EXTS: tuple[str, ...] = (".md",)


def under_targets(paths, targets: tuple[str, ...] = DEFAULT_TARGETS,
                  exts: tuple[str, ...] = DEFAULT_EXTS) -> list[str]:
    """Keep only paths with a wanted extension under a target prefix, sorted, deduped."""
    keep = {
        p for p in paths
        if p.endswith(tuple(exts)) and any(p.startswith(t) for t in targets)
    }
    return sorted(keep)


def _git(repo_root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo_root), *args],
                          check=True, capture_output=True, text=True)


def changed_files(repo_root: Path, base: str, head: str = "HEAD",
                  targets: tuple[str, ...] = DEFAULT_TARGETS,
                  exts: tuple[str, ...] = DEFAULT_EXTS) -> list[str]:
    """Target files that changed between `base` and `head` (added/modified).

    `--no-renames` decomposes a rename into add + delete, so a renamed doc's old
    path shows up in `deleted_files` and its stale index records self-heal
    (otherwise a rename leaves orphan records until a `--full` rebuild).
    """
    out = _git(repo_root, "diff", "--name-only", "--no-renames",
               "--diff-filter=d", base, head).stdout
    return under_targets(out.splitlines(), targets, exts)


def deleted_files(repo_root: Path, base: str, head: str = "HEAD",
                  targets: tuple[str, ...] = DEFAULT_TARGETS,
                  exts: tuple[str, ...] = DEFAULT_EXTS) -> list[str]:
    """Target files deleted between `base` and `head` (renames included)."""
    out = _git(repo_root, "diff", "--name-only", "--no-renames",
               "--diff-filter=D", base, head).stdout
    return under_targets(out.splitlines(), targets, exts)


def full_scan(repo_root: Path, targets: tuple[str, ...] = DEFAULT_TARGETS,
              exts: tuple[str, ...] = DEFAULT_EXTS) -> list[str]:
    """Every tracked target file — the input for the initial full index."""
    out = _git(repo_root, "ls-files", "-z", *targets).stdout
    paths = [p for p in out.split("\0") if p]
    return under_targets(paths, targets, exts)


def head_sha(repo_root: Path) -> str:
    """Current HEAD commit — stored in the index so the next run can delta from it."""
    return _git(repo_root, "rev-parse", "HEAD").stdout.strip()
