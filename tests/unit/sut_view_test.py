#!/usr/bin/env python3
"""Tests for the disposable SUT-view (#288 decontamination).

`path_within` is pure; the worktree build is exercised against a throwaway git
repo so the isolation property (eval-truth absent + not grep-reachable) is proven
without touching the real repo."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import sut_view  # noqa: E402


# ── pure: realpath containment / anti-traversal ─────────────────────────────
def test_path_within_true_for_child(tmp_path):
    assert sut_view.path_within(tmp_path, tmp_path / "a" / "b")


def test_path_within_false_for_escape(tmp_path):
    assert not sut_view.path_within(tmp_path / "root", tmp_path / "root" / ".." / "sibling")


def test_path_within_false_for_unrelated(tmp_path):
    assert not sut_view.path_within(tmp_path / "a", tmp_path / "b")


# ── integration: build a view of a tmp git repo, prove eval/truth is gone ───
def _git(cwd, *args):
    subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True)


def _make_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "eval" / "truth").mkdir(parents=True)
    (repo / "eval" / "truth" / "canon.yaml").write_text("_leak_sentinel: SENT-XYZ\n", encoding="utf-8")
    (repo / "code.py").write_text("# a real module\nX = 1\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    return repo


def test_build_view_strips_eval_truth_and_hides_sentinel(tmp_path):
    repo = _make_repo(tmp_path)
    dest = tmp_path / "view"
    try:
        view = sut_view.build(repo, dest)
        # the view has the real code but not the eval-truth store
        assert (view / "code.py").exists()
        assert not (view / "eval" / "truth" / "canon.yaml").exists()
        # and git grep in the view cannot find the sentinel
        out = subprocess.run(["git", "-C", str(view), "grep", "-F", "SENT-XYZ"],
                             capture_output=True, text=True)
        assert out.returncode != 0 and out.stdout == ""
    finally:
        sut_view.teardown(repo, dest)
    # teardown removed the worktree
    assert not dest.exists()
