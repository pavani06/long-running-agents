#!/usr/bin/env python3
"""G1 (#288) — evidence provenance (source_type) with a NON-COUPLING regression
invariant: code evidence may improve detection/retrieval, but `source_type == "code"`
must NOT, by itself, determine `Exists` or add any verdict rule. The verdict contract
(build_context, mark_verified, parse_classification) must ignore source_type."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import retrieval  # noqa: E402
import phase3_classify as p3  # noqa: E402


# ── provenance is recorded ───────────────────────────────────────────────────
def test_source_type():
    assert retrieval.source_type("scripts/analyze-and-improve/dedup.py") == "code"
    assert retrieval.source_type("docs/canonical/x.md") == "doc"
    assert retrieval.source_type("data/x.yaml") == "other"


def test_rank_sections_annotates_source_type():
    index = {"records": {
        "a": {"path": "scripts/analyze-and-improve/dedup.py", "heading": "h", "vector": [1.0, 0.0]},
        "b": {"path": "docs/canonical/x.md", "heading": "h", "vector": [0.9, 0.1]},
    }}
    ranked = retrieval.rank_sections([1.0, 0.0], index, k=2)
    by = {r["path"]: r["source_type"] for r in ranked}
    assert by["scripts/analyze-and-improve/dedup.py"] == "code"
    assert by["docs/canonical/x.md"] == "doc"


def test_citations_of_annotates_source_type():
    cls = [{"pattern": "P", "evidence": [
        {"file": "scripts/analyze-and-improve/dedup.py", "line": 1, "quote": "q"},
        {"file": "docs/canonical/x.md", "line": 2, "quote": "q2"}]}]
    cits = p3.citations_of(cls)
    assert [c["source_type"] for c in cits] == ["code", "doc"]


# ── NON-COUPLING: build_context ignores source_type (prompt doesn't couple) ──
def test_build_context_ignores_source_type():
    base = {"path": "same/path.md", "heading": "H", "score": 0.5, "text": "body"}
    as_code = dict(base, source_type="code")
    as_doc = dict(base, source_type="doc")
    # only the source_type field differs → the assembled prompt must be identical
    assert retrieval.build_context([as_code], []) == retrieval.build_context([as_doc], [])


# ── NON-COUPLING: verified depends on ok/quote, never on source_type ─────────
def test_mark_verified_ignores_source_type():
    cls = [{"pattern": "P", "verdict": "Exists", "evidence": [{"file": "f", "line": 1, "quote": "q"}]}]
    # a CODE citation that FAILED grep-verify must NOT be treated as verified
    code_fail = [{"pattern": "P", "quote": "q", "ok": False, "source_type": "code"}]
    p3.mark_verified(cls, code_fail)
    assert cls[0]["verified"] is False   # source_type=code does not rescue a failed citation

    cls2 = [{"pattern": "P", "verdict": "Exists", "evidence": [{"file": "f", "line": 1, "quote": "q"}]}]
    # the SAME (ok, quote) with source_type doc vs code → identical verified
    for st in ("code", "doc"):
        c = [dict(cls2[0])]
        p3.mark_verified(c, [{"pattern": "P", "quote": "q", "ok": True, "source_type": st}])
        assert c[0]["verified"] is True   # verified by the same rule regardless of provenance


def test_parse_classification_unaffected_by_source_type():
    reply = {"classifications": [{"pattern": "P", "verdict": "Exists",
             "evidence": [{"file": "x.py", "line": 1, "quote": "q", "source_type": "code"}]}]}
    out = p3.parse_classification(reply)   # must parse identically; source_type is inert
    assert out[0]["verdict"] == "Exists" and out[0]["pattern"] == "P"
