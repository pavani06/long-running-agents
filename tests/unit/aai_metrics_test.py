#!/usr/bin/env python3
"""Unit tests for AAI_METRICS Stage-A telemetry (#288). Pure parts only; no network."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import aai_metrics as m  # noqa: E402


# ── scope_label ──────────────────────────────────────────────────────────
def test_scope_label(monkeypatch):
    monkeypatch.delenv("INDEX_EXTS", raising=False)
    assert m.scope_label() == "docs"
    monkeypatch.setenv("INDEX_EXTS", ".md")
    assert m.scope_label() == "docs"
    monkeypatch.setenv("INDEX_EXTS", ".md,.py")
    assert m.scope_label() == "docs+code"


# ── chunk_breakdown ──────────────────────────────────────────────────────
def test_chunk_breakdown_by_source_type():
    records = {
        "a": {"path": "docs/canonical/x.md"},
        "b": {"path": "scripts/analyze-and-improve/dedup.py"},
        "c": {"path": "scripts/analyze-and-improve/floor.py"},
        "d": {"path": "data/x.yaml"},
    }
    bd = m.chunk_breakdown(records)
    assert bd == {"chunks_total": 4, "chunks_doc": 1, "chunks_code": 2, "chunks_other": 1}


def test_chunk_breakdown_empty():
    assert m.chunk_breakdown({})["chunks_total"] == 0


# ── embed_cost_usd (proxy) ───────────────────────────────────────────────
def test_embed_cost_zero_and_monotonic():
    assert m.embed_cost_usd(0) == 0.0
    assert m.embed_cost_usd(4_000_000) > m.embed_cost_usd(1_000_000)
    # 4M chars ≈ 1M tokens → ~$0.13
    assert abs(m.embed_cost_usd(4_000_000) - 0.13) < 1e-6


# ── classify_fields (reuses the merged guard) ─────────────────────────────
def test_classify_fields_drift_and_guard_signals():
    cls = [
        {"verdict": "Exists", "code_only_grounded": True,
         "grounding": {"code": 5, "doc": 0, "other": 0}},   # coverage claim, uncovered (gap)
        {"verdict": "Exists", "code_only_grounded": False,
         "grounding": {"code": 0, "doc": 2, "other": 0}},   # coverage, covered
        {"verdict": "Missing"},
        {"verdict": "Partial", "grounding": {"code": 0, "doc": 1, "other": 0}},
    ]
    f = m.classify_fields(cls)
    assert f["patterns"] == 4
    assert f["exists_total"] == 2 and f["exists_covered"] == 1 and f["exists_uncovered"] == 1
    assert f["code_only_grounded"] == 1
    assert f["doc_gaps"] == 1               # only the code-only Exists
    assert '"Exists":2' in f["verdicts"] and '"Missing":1' in f["verdicts"]


def test_classify_fields_empty():
    f = m.classify_fields([])
    assert f["patterns"] == 0 and f["exists_total"] == 0 and f["doc_gaps"] == 0


# ── format_line / emit ────────────────────────────────────────────────────
def test_format_line_is_greppable():
    line = m.format_line("index", {"scope": "docs+code", "chunks_total": 13600})
    assert line == "AAI_METRICS index scope=docs+code chunks_total=13600"


def test_emit_prints_and_writes_summary(tmp_path, capsys, monkeypatch):
    sp = tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(sp))
    line = m.emit("classify", {"scope": "docs", "patterns": 3})
    assert line == "AAI_METRICS classify scope=docs patterns=3"
    assert line in capsys.readouterr().out
    assert line in sp.read_text(encoding="utf-8")


def test_emit_survives_unwritable_summary(monkeypatch, capsys):
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", "/nonexistent-dir/summary.md")
    line = m.emit("index", {"scope": "docs"})   # must not raise
    assert "AAI_METRICS index" in capsys.readouterr().out
