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


# ── documentation-coverage guard matrix (#288 — the live-proof helper) ──────
def test_grounding_class_buckets():
    assert ev._grounding_class({"code": 0, "doc": 2, "other": 0}) == "doc_grounded"
    assert ev._grounding_class({"code": 3, "doc": 1, "other": 0}) == "doc_grounded"   # mixed → doc
    assert ev._grounding_class({"code": 3, "doc": 0, "other": 0}) == "code_only"
    assert ev._grounding_class({"code": 0, "doc": 0, "other": 2}) == "other_only"
    assert ev._grounding_class({"code": 0, "doc": 0, "other": 0}) == "zero"
    assert ev._grounding_class(None) == "zero"


def test_guard_matrix_assertions_pass_on_correct_data():
    # the three cases that DEFINE 'proven'
    records = [
        {"verdict": "Exists", "grounding": {"code": 5, "doc": 0, "other": 0},
         "documentation_covered": False, "error": None},        # code-only → gap
        {"verdict": "Exists", "grounding": {"code": 0, "doc": 2, "other": 0},
         "documentation_covered": True, "error": None},         # doc-backed → covered
        {"verdict": "Partial", "grounding": {"code": 0, "doc": 1, "other": 0},
         "documentation_covered": False, "error": None},        # Partial → gap
        {"verdict": "Missing", "grounding": None,
         "documentation_covered": False, "error": None},        # Missing → gap
    ]
    gm = ev.guard_matrix(records)
    assert gm["assertions"]["code_only_exists_is_gap"] == (1, True)
    assert gm["assertions"]["doc_backed_coverage_is_covered"] == (1, True)
    assert gm["assertions"]["missing_partial_is_gap"] == (2, True)
    assert gm["cells"][("Exists", "code_only", "gap")] == 1
    assert gm["cells"][("Exists", "doc_grounded", "covered")] == 1


def test_guard_matrix_flags_violation():
    # a code-only Exists wrongly marked covered must FAIL the assertion
    records = [{"verdict": "Exists", "grounding": {"code": 5, "doc": 0, "other": 0},
                "documentation_covered": True, "error": None}]
    gm = ev.guard_matrix(records)
    assert gm["assertions"]["code_only_exists_is_gap"] == (1, False)


def test_guard_matrix_skips_errored_records():
    records = [{"verdict": None, "grounding": None, "documentation_covered": False,
                "error": "GLM 500"}]
    gm = ev.guard_matrix(records)
    assert gm["assertions"]["code_only_exists_is_gap"] == (0, True)   # nothing to violate


def test_report_includes_guard_matrix():
    records = [{"concept_id": "c1", "verdict": "Exists",
                "grounding": {"code": 5, "doc": 0, "other": 0},
                "documentation_covered": False, "error": None, "citations": []}]
    rep = ev._report(records, "evrv-dataset.json")
    assert "Guardrail de cobertura de documentação" in rep
    assert "code-only Exists/Better NÃO suprime a lacuna" in rep
    assert "✅ PASS" in rep
