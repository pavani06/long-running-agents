"""Deterministic negative preflight for the metamorphic eval (#288 decontamination).

Proves, with no LLM, that the eval-truth sentinel is unreachable by any path the
classifier can use against the SUT-view, and refuses to run otherwise. Three
checks:

  1. grep      — `git grep -F <sentinel>` in the view returns nothing;
  2. index     — no dense-index record has a path under the eval-truth prefix
                 (the index carries paths, not text, so a path check is the
                 deterministic proxy for "truth content is not indexed");
  3. boundary  — the real eval-truth store does NOT resolve inside the view
                 (realpath / anti-traversal), so no symlink or `..` can reach it.

`sentinel_of`, `index_has_truth_paths` and `assess` are pure and unit-tested;
`grep_hits` and `assert_isolated` do the git/filesystem I/O. A non-empty failure
list means the caller must exit non-zero WITHOUT running the eval.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from sut_view import TRUTH_PREFIX, path_within


def sentinel_of(canon: dict) -> str | None:
    """The leak sentinel declared in the canon, if any. Pure."""
    s = canon.get("_leak_sentinel")
    return s if isinstance(s, str) and s.strip() else None


def index_has_truth_paths(index: dict, truth_prefix: str = TRUTH_PREFIX) -> list[str]:
    """Index record paths that fall under the eval-truth prefix (should be empty). Pure."""
    return sorted({rec.get("path", "") for rec in index.get("records", {}).values()
                   if (rec.get("path") or "").startswith(truth_prefix + "/")
                   or rec.get("path") == truth_prefix})


def grep_hits(view_root: Path, sentinel: str) -> int:
    """How many times the sentinel appears in the view via `git grep -F` (I/O)."""
    out = subprocess.run(["git", "-C", str(view_root), "grep", "-c", "-F", sentinel],
                         capture_output=True, text=True)
    # git grep exits 1 with no output when there are no matches.
    return sum(int(line.rsplit(":", 1)[-1]) for line in out.stdout.splitlines() if ":" in line)


def assess(*, grep_count: int, index_truth_paths: list[str],
           truth_within_view: bool) -> list[str]:
    """Turn the three raw signals into a list of failures (empty == isolated). Pure."""
    failures: list[str] = []
    if grep_count > 0:
        failures.append(f"sentinel grep-reachable in SUT-view ({grep_count} hit(s))")
    if index_truth_paths:
        failures.append(f"eval-truth path(s) present in dense index: {index_truth_paths}")
    if truth_within_view:
        failures.append("eval-truth store resolves inside the SUT-view (realpath boundary breached)")
    return failures


def assert_isolated(view_root: Path, index: dict, real_truth_path: Path,
                    sentinel: str, *, truth_prefix: str = TRUTH_PREFIX) -> list[str]:
    """Run all three checks against disk (I/O). Returns failures; empty == safe to run."""
    return assess(
        grep_count=grep_hits(view_root, sentinel),
        index_truth_paths=index_has_truth_paths(index, truth_prefix),
        truth_within_view=path_within(view_root, real_truth_path),
    )
