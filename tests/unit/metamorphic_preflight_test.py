#!/usr/bin/env python3
"""Tests for the deterministic decontamination preflight (#288)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import metamorphic_preflight as pf  # noqa: E402


def test_sentinel_of():
    assert pf.sentinel_of({"_leak_sentinel": "EVALTRUTH-SENTINEL-x"}) == "EVALTRUTH-SENTINEL-x"
    assert pf.sentinel_of({}) is None
    assert pf.sentinel_of({"_leak_sentinel": "  "}) is None


def test_index_has_truth_paths_flags_only_truth_prefix():
    index = {"records": {
        "a": {"path": "scripts/analyze-and-improve/dedup.py"},
        "b": {"path": "eval/truth/metamorphic_canon.yaml"},
        "c": {"path": "docs/canonical/x.md"},
    }}
    assert pf.index_has_truth_paths(index) == ["eval/truth/metamorphic_canon.yaml"]
    assert pf.index_has_truth_paths({"records": {}}) == []


def test_assess_passes_when_clean():
    assert pf.assess(grep_count=0, index_truth_paths=[], truth_within_view=False) == []


def test_assess_reports_each_breach():
    fails = pf.assess(grep_count=2, index_truth_paths=["eval/truth/c.yaml"],
                      truth_within_view=True)
    assert len(fails) == 3
    assert any("grep-reachable" in f for f in fails)
    assert any("dense index" in f for f in fails)
    assert any("realpath boundary" in f for f in fails)


def test_assess_single_breach():
    fails = pf.assess(grep_count=1, index_truth_paths=[], truth_within_view=False)
    assert fails == ["sentinel grep-reachable in SUT-view (1 hit(s))"]
