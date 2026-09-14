"""Disposable system-under-test view for the metamorphic eval (#288 decontamination).

The eval must not let the classifier retrieve/grep the eval-truth (the canon +
its labels), or it grades against its own answer key (the leak the E/R/V run
exposed: 20/83 citations pointed at the canon). Rather than teach the shared
retriever an `observable_root`, we hand it a **physically stripped root**: a
throwaway git worktree of HEAD with `eval/truth/` removed. Everything the
classifier can reach — dense index (built elsewhere), `git grep`, ask-for-more
file reads — is confined to this view because that is the `repo_root` it gets,
and the view simply does not contain the truth.

`path_within` (realpath containment / anti-traversal) is pure and unit-tested;
`build`/`teardown` are the git I/O, exercised by an integration test over a tmp
git repo. Nothing here touches production retrieval code.
"""
from __future__ import annotations

import contextlib
import os
import subprocess
import tempfile
from pathlib import Path

# The single prefix that holds eval-truth. Truth authored under it is invisible
# to the SUT by default (it is stripped from the view); truth authored anywhere
# else is a policy violation the preflight is meant to catch.
TRUTH_PREFIX = "eval/truth"


def path_within(root: str | Path, candidate: str | Path) -> bool:
    """True if `candidate` resolves inside `root` after realpath (symlink/`..` safe). Pure."""
    r = os.path.realpath(str(root))
    c = os.path.realpath(str(candidate))
    return c == r or c.startswith(r + os.sep)


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args],
                          check=True, capture_output=True, text=True)


def build(repo_root: Path, dest: Path, *, truth_prefix: str = TRUTH_PREFIX) -> Path:
    """Create a disposable worktree of HEAD at `dest`, with `truth_prefix` removed.

    The removal is `git rm` (index + working tree) so `git grep` in the view cannot
    reach the truth. `dest` must be outside `repo_root` so the view is not nested in
    the scanned repo. Returns the view root."""
    dest = Path(dest)
    _git(repo_root, "worktree", "add", "--detach", "--quiet", str(dest), "HEAD")
    if (dest / truth_prefix).exists():
        _git(dest, "rm", "-r", "-q", "--", truth_prefix)
    return dest


def teardown(repo_root: Path, dest: Path) -> None:
    """Remove the disposable worktree (best-effort; never raises)."""
    try:
        _git(repo_root, "worktree", "remove", "--force", str(dest))
    except subprocess.CalledProcessError:
        pass


@contextlib.contextmanager
def session(repo_root: Path, *, truth_prefix: str = TRUTH_PREFIX):
    """Yield a disposable SUT-view root (worktree of HEAD minus `truth_prefix`),
    torn down on exit. The view lives in a temp dir outside `repo_root`."""
    dest = Path(tempfile.mkdtemp(prefix="sut-view-")) / "repo"
    try:
        yield build(repo_root, dest, truth_prefix=truth_prefix)
    finally:
        teardown(repo_root, dest)
