#!/usr/bin/env python3
"""Unit tests for the E/R/V dataset capture pure signals (#288 follow-up)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import metamorphic_evrv as ev  # noqa: E402


def test_source_type():
    assert ev.source_type("scripts/analyze-and-improve/dedup.py") == "code"
    assert ev.source_type("docs/canonical/x.md") == "doc"
    assert ev.source_type("some/data.yaml") == "other"


def test_quote_anywhere_whitespace_insensitive():
    assert ev.quote_anywhere("hello world", "aa hello\n  world bb")
    assert not ev.quote_anywhere("absent", "nothing here")
    assert not ev.quote_anywhere("", "anything")


# ── citation_signals: the four automatable auto-axis labels ─────────────────
def test_citation_signal_verified():
    cit = {"file": "a.py", "line": 3, "quote": "DUP_THRESHOLD"}
    sig = ev.citation_signals(cit, "x\ny\nDUP_THRESHOLD = 0.85\n", {"ok": True, "reason": "ok"})
    assert sig["auto_axis"] == "V1_verified" and sig["source_type"] == "code"
    assert sig["quote_at_line"] and sig["file_exists"]


def test_citation_signal_wrong_location():
    # quote is in the file but grep_verify's ±2 window rejected it → R1
    cit = {"file": "a.md", "line": 99, "quote": "the needle"}
    sig = ev.citation_signals(cit, "line1\nthe needle\nline3\n",
                              {"ok": False, "reason": "quote not found near cited line"})
    assert sig["auto_axis"] == "R1_wrong_location" and sig["quote_anywhere"]


def test_citation_signal_quote_absent():
    cit = {"file": "a.md", "line": 1, "quote": "not present"}
    sig = ev.citation_signals(cit, "totally different text",
                              {"ok": False, "reason": "quote not found near cited line"})
    assert sig["auto_axis"] == "R0E_quote_absent" and not sig["quote_anywhere"]


def test_citation_signal_file_missing():
    cit = {"file": "ghost.py", "line": 1, "quote": "q"}
    sig = ev.citation_signals(cit, None, {"ok": False, "reason": "file not found: ghost.py"})
    assert sig["auto_axis"] == "R0_file_missing" and not sig["file_exists"]


def test_citation_signal_leaves_E_for_offline():
    sig = ev.citation_signals({"file": "a.py", "line": 1, "quote": "q"},
                              "q here", {"ok": True})
    assert sig["E_evidence_correct"] is None


# ── report renders and honours the STOP ─────────────────────────────────────
def test_report_counts_and_states_stop():
    records = [
        {"concept_id": "c1", "verdict": "Exists", "error": None,
         "citations": [{"auto_axis": "V1_verified", "source_type": "code"},
                       {"auto_axis": "R1_wrong_location", "source_type": "code"}]},
        {"concept_id": "c2", "verdict": "Missing", "error": None, "citations": []},
    ]
    rep = ev._report(records, "evrv-dataset.json")
    assert "V1_verified` (verificou): **1**" in rep
    assert "R1_wrong_location" in rep and "code / V1_verified: 1" in rep
    assert "STOP obrigatório" in rep and "Nenhuma correção" in rep
