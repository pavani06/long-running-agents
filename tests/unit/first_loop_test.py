#!/usr/bin/env python3
"""Unit tests for the First-Loop deterministic selection + PR-body assembly (#263 slice).
Pure parts only; no network, no GLM."""
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import first_loop as fl  # noqa: E402


@dataclass(frozen=True)
class P:
    file: str
    video_id: str = "v"
    title: str = "t"


# ── source selection (deterministic, excludes the benchmark) ──────────────
def test_select_source_excludes_benchmark_and_takes_first():
    pending = [
        P("2026-09-11-12-factor-agents-patterns--8kMaTybvDUw.md"),   # benchmark → excluded
        P("2026-09-11-75m-founder-reveals--QBfXiWvM0qc.md"),
        P("2026-09-11-agentic-explained--FU5_kpTAVDo.md"),
    ]
    f, rule = fl.select_source(pending, None)
    assert f == "2026-09-11-75m-founder-reveals--QBfXiWvM0qc.md"
    assert "excluding the 12-factor benchmark" in rule


def test_select_source_explicit_overrides():
    f, rule = fl.select_source([P("a.md")], "chosen.md")
    assert f == "chosen.md" and rule == "explicit --source"


def test_select_source_none_when_only_benchmark():
    f, rule = fl.select_source([P("x-12-factor-agents-y.md")], None)
    assert f is None and "no eligible" in rule


# ── Missing selection (explicit pattern_id, else first eligible) ──────────
CLS = [
    {"pattern": "A", "verdict": "Exists"},
    {"pattern": "B", "verdict": "Missing", "rationale": "b"},
    {"pattern": "C", "verdict": "Missing", "rationale": "c"},
]


def test_select_missing_first_eligible_in_order():
    m, rule = fl.select_missing(CLS, None)
    assert m["pattern"] == "B" and "first eligible Missing" in rule


def test_select_missing_explicit_pattern_id():
    m, rule = fl.select_missing(CLS, "C")
    assert m["pattern"] == "C" and "explicit --pattern-id=C" in rule


def test_select_missing_pattern_id_not_missing():
    m, rule = fl.select_missing(CLS, "A")     # A is Exists, not an eligible Missing
    assert m is None and "not an eligible Missing" in rule


def test_select_missing_none_available():
    m, rule = fl.select_missing([{"pattern": "A", "verdict": "Exists"}], None)
    assert m is None and "no eligible Missing" in rule


# ── transcript mapping ────────────────────────────────────────────────────
def test_transcript_for_maps_extract_md_to_transcript_txt():
    p = fl._transcript_for("2026-09-11-talk--vid.md")
    assert p.name == "2026-09-11-talk--vid.txt"
    assert p.parent.as_posix().endswith("raw/youtube/ai-learning/transcripts")


# ── PR body carries what the human must review ────────────────────────────
def test_pr_body_states_human_decision_and_gates():
    missing = {"pattern": "B", "verdict": "Missing", "rationale": "why", "evidence": []}
    pattern = {"name": "B", "problem": "prob", "mechanism": "mech", "tradeoffs": "to"}
    artifact = {"intended_destination": "docs/canonical/b.md"}
    body = fl._pr_body(
        slug="s", source_file="s--v.md", source_rule="deterministic rule",
        missing=missing, missing_rule="first eligible Missing", pattern=pattern,
        artifact=artifact, proposed_path="docs/analysis/s/proposed/b.md",
        gates={"citations_ok": True},
        evaluation={"mean": 3.5, "passed": True, "scores": {}, "rationale": "ok"},
        dup={"duplicate": False, "score": 0.4})
    assert "auto_merge=OFF" in body or "auto-merge OFF" in body
    assert "creation != promotion" in body
    assert "docs/analysis/s/proposed/b.md" in body
    assert "docs/canonical/b.md" in body                     # intended destination
    assert "O que o humano está sendo pedido a aprovar" in body
    assert "não promove automaticamente" in body
    assert "roda no CI" in body and "Check Obsidian Conventions" in body   # actual validate-obsidian contract
