#!/usr/bin/env python3
"""Unit tests for Fase 3 (classification) pure parts — hybrid assembly + citation
verification (the surface the Etapa 2 DoD names), plus the classify parsers, the
one 'ask for more' round, and classification serialization. No network."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import phase3_classify as p3  # noqa: E402
import retrieval  # noqa: E402
import serialize  # noqa: E402
from glm import GLMError  # noqa: E402
from grep_verify import all_ok, verify_all, verify_citation  # noqa: E402


# ── retrieval.rank_sections (dense ranking) ───────────────────────────────
INDEX = {"records": {
    "a#1-x": {"path": "docs/canonical/a.md", "heading": "X", "vector": [1.0, 0.0]},
    "b#1-y": {"path": "docs/canonical/b.md", "heading": "Y", "vector": [0.9, 0.1]},
    "c#1-z": {"path": "docs/canonical/c.md", "heading": "Z", "vector": [0.0, 1.0]},
    "d#1-w": {"path": "docs/canonical/d.md", "heading": "W", "vector": None},  # skipped
}}


def test_rank_sections_topk_order():
    ranked = retrieval.rank_sections([1.0, 0.0], INDEX, k=2)
    assert [r["id"] for r in ranked] == ["a#1-x", "b#1-y"]     # closest first
    assert ranked[0]["score"] >= ranked[1]["score"]


def test_rank_sections_floor_and_skips_vectorless():
    ranked = retrieval.rank_sections([1.0, 0.0], INDEX, k=10, floor=0.5)
    ids = {r["id"] for r in ranked}
    assert ids == {"a#1-x", "b#1-y"}          # c below floor, d has no vector


def test_rank_sections_empty_index():
    assert retrieval.rank_sections([1.0], {"records": {}}, k=5) == []


# ── retrieval.build_context (prompt assembly) ─────────────────────────────
def test_build_context_dense_and_grep():
    dense = [{"path": "docs/canonical/a.md", "heading": "X", "score": 0.91, "text": "alpha body"}]
    grep = [{"identifier": "Foo", "path": "src/x.py", "line": 12, "content": "class Foo:"}]
    ctx = retrieval.build_context(dense, grep)
    assert "docs/canonical/a.md :: X" in ctx and "alpha body" in ctx
    assert "src/x.py:12" in ctx and "`Foo`" in ctx


def test_build_context_caps_section_text():
    long_body = "z" * (retrieval.MAX_SECTION_CHARS + 4000)
    dense = [{"path": "docs/canonical/a.md", "heading": "X", "score": 0.9, "text": long_body}]
    ctx = retrieval.build_context(dense, [])
    assert ctx.count("z") == retrieval.MAX_SECTION_CHARS   # truncated, not full body


def test_build_context_empty():
    ctx = retrieval.build_context([], [])
    assert ctx.count("_(nenhuma)_") == 2


# ── grep_verify (citation verification) ───────────────────────────────────
FILE = "line one\nthe key claim is here\nline three\nline four\n"


def test_verify_citation_quote_found():
    assert verify_citation(FILE, 2, "key claim")["ok"] is True


def test_verify_citation_quote_found_within_window():
    assert verify_citation(FILE, 1, "key claim")["ok"] is True     # ±2 window reaches line 2


def test_verify_citation_quote_not_found():
    # "line four" is at line 4; the ±2 window around line 1 is lines 1-3 only.
    r = verify_citation(FILE, 1, "line four")
    assert r["ok"] is False


def test_verify_citation_line_out_of_range():
    assert verify_citation(FILE, 99, "x")["ok"] is False
    assert verify_citation(FILE, 0, "x")["ok"] is False


def test_verify_citation_no_quote_just_line():
    assert verify_citation(FILE, 3, "")["ok"] is True


def test_verify_citation_whitespace_normalized():
    assert verify_citation("a\n  the   key    claim  \nz\n", 2, "the key claim")["ok"] is True


def test_verify_all_and_all_ok(tmp_path):
    (tmp_path / "f.md").write_text(FILE, encoding="utf-8")
    cits = [{"file": "f.md", "line": 2, "quote": "key claim"},
            {"file": "missing.md", "line": 1, "quote": "x"}]
    verified = verify_all(cits, tmp_path)
    assert verified[0]["ok"] is True
    assert verified[1]["ok"] is False and "not found" in verified[1]["reason"]
    assert all_ok(verified) is False
    assert all_ok([]) is True


# ── phase3 parsers ────────────────────────────────────────────────────────
def test_build_messages_has_patterns_and_context():
    msgs = p3.build_messages([{"name": "P1"}], "CTX-HERE")
    assert '"name": "P1"' in msgs[1]["content"] and "CTX-HERE" in msgs[1]["content"]


def test_parse_ask_for_more_none_when_empty():
    assert p3.parse_ask_for_more({"need_more": {"greps": [], "files": []}}) is None
    assert p3.parse_ask_for_more({}) is None


def test_parse_ask_for_more_returns_spec():
    nm = p3.parse_ask_for_more({"need_more": {"greps": ["Foo", ""], "files": ["docs/x.md"]}})
    assert nm == {"greps": ["Foo"], "files": ["docs/x.md"]}


def test_parse_classification_ok():
    reply = {"classifications": [
        {"pattern": "P1", "verdict": "Missing", "evidence": [], "rationale": "r"},
        {"pattern": "P2", "verdict": "Exists", "evidence": [{"file": "a.md", "line": 3}]},
    ]}
    assert p3.parse_classification(reply) == reply["classifications"]


def test_parse_classification_bad_verdict():
    with pytest.raises(GLMError):
        p3.parse_classification({"classifications": [
            {"pattern": "P", "verdict": "Nope", "evidence": []}]})


def test_parse_classification_missing_pattern():
    with pytest.raises(GLMError):
        p3.parse_classification({"classifications": [
            {"verdict": "Missing", "evidence": []}]})


def test_parse_classification_evidence_not_list():
    with pytest.raises(GLMError):
        p3.parse_classification({"classifications": [
            {"pattern": "P", "verdict": "Missing", "evidence": "nope"}]})


def test_parse_classification_not_a_list():
    with pytest.raises(GLMError):
        p3.parse_classification({"classifications": {}})


def test_citations_of_flattens_evidence():
    cls = [{"pattern": "P1", "evidence": [{"file": "a.md", "line": 1, "quote": "q"}]},
           {"pattern": "P2", "evidence": [{"line": 2}]}]  # no file → skipped
    cits = p3.citations_of(cls)
    assert cits == [{"file": "a.md", "line": 1, "quote": "q", "pattern": "P1",
                     "source_type": "doc"}]   # G1 provenance tag (annotation only)


# ── mark_verified (verdict-aware policy) ──────────────────────────────────
def test_mark_verified_missing_needs_no_citation():
    cls = [{"pattern": "M", "verdict": "Missing", "evidence": []}]
    p3.mark_verified(cls, [])
    assert cls[0]["verified"] is True


def test_mark_verified_exists_needs_content_checked_citation():
    cls = [{"pattern": "E", "verdict": "Exists", "evidence": [{"file": "a.md", "line": 1, "quote": "q"}]}]
    p3.mark_verified(cls, [{"pattern": "E", "ok": True, "quote": "q"}])
    assert cls[0]["verified"] is True


def test_mark_verified_exists_empty_evidence_is_false():
    cls = [{"pattern": "E", "verdict": "Exists", "evidence": []}]
    p3.mark_verified(cls, [])
    assert cls[0]["verified"] is False        # bare existence claim, nothing verified


def test_mark_verified_exists_empty_quote_is_false():
    cls = [{"pattern": "E", "verdict": "Better", "evidence": [{"file": "a.md", "line": 1}]}]
    p3.mark_verified(cls, [{"pattern": "E", "ok": True, "quote": ""}])
    assert cls[0]["verified"] is False        # line exists but content never checked


def test_mark_verified_failing_citation_is_false():
    cls = [{"pattern": "E", "verdict": "Partial", "evidence": [{"file": "a.md", "line": 9, "quote": "q"}]}]
    p3.mark_verified(cls, [{"pattern": "E", "ok": False, "quote": "q"}])
    assert cls[0]["verified"] is False


# ── mark_grounding (#288 B′ — code_only_grounded derivation) ──────────────
# Cases mirror the observed behavior matrix: code-only Exists, doc-only Exists,
# mixed Exists, and Missing controls.
def _cit(pattern, source_type, ok=True, quote="q"):
    return {"pattern": pattern, "source_type": source_type, "ok": ok, "quote": quote}


def test_mark_grounding_code_only_existence_is_flagged():
    # cosine-dedup-gate style: docs+code → Exists grounded solely in verified code
    cls = [{"pattern": "cosine-dedup", "verdict": "Exists"}]
    p3.mark_grounding(cls, [_cit("cosine-dedup", "code"), _cit("cosine-dedup", "code")])
    assert cls[0]["grounding"] == {"code": 2, "doc": 0, "other": 0}
    assert cls[0]["code_only_grounded"] is True


def test_mark_grounding_mixed_is_not_flagged():
    # mixed evidence (code + doc) → has documentation backing → NOT code-only
    cls = [{"pattern": "P", "verdict": "Exists"}]
    p3.mark_grounding(cls, [_cit("P", "code"), _cit("P", "doc")])
    assert cls[0]["grounding"] == {"code": 1, "doc": 1, "other": 0}
    assert cls[0]["code_only_grounded"] is False


def test_mark_grounding_doc_only_is_not_flagged():
    cls = [{"pattern": "P", "verdict": "Exists"}]
    p3.mark_grounding(cls, [_cit("P", "doc")])
    assert cls[0]["code_only_grounded"] is False


def test_mark_grounding_missing_is_never_flagged():
    # a Missing control (k8s/DP) makes no existence claim → never code_only_grounded
    cls = [{"pattern": "k8s", "verdict": "Missing"}]
    p3.mark_grounding(cls, [_cit("k8s", "code")])   # even if a stray code cit exists
    assert cls[0]["code_only_grounded"] is False


def test_mark_grounding_unverified_code_does_not_ground():
    cls = [{"pattern": "P", "verdict": "Exists"}]
    p3.mark_grounding(cls, [_cit("P", "code", ok=False)])   # failed grep-verify
    assert cls[0]["grounding"] == {"code": 0, "doc": 0, "other": 0}
    assert cls[0]["code_only_grounded"] is False


def test_mark_grounding_empty_quote_code_does_not_ground():
    cls = [{"pattern": "P", "verdict": "Better"}]
    p3.mark_grounding(cls, [_cit("P", "code", quote="")])   # line but no content checked
    assert cls[0]["code_only_grounded"] is False


def test_mark_grounding_partial_existence_verdict_flagged():
    cls = [{"pattern": "P", "verdict": "Partial"}]
    p3.mark_grounding(cls, [_cit("P", "code")])
    assert cls[0]["code_only_grounded"] is True   # Partial is an existence verdict


def test_mark_grounding_does_not_touch_verdict_or_verified():
    # DERIVED-ONLY / NON-COUPLING: verdict and verified are byte-identical after.
    cls = [{"pattern": "P", "verdict": "Exists", "verified": True}]
    p3.mark_grounding(cls, [_cit("P", "code")])
    assert cls[0]["verdict"] == "Exists" and cls[0]["verified"] is True


# ── phase3.run — one 'ask for more' round ─────────────────────────────────
def test_run_no_ask_for_more():
    final = {"classifications": [{"pattern": "P", "verdict": "Exists", "evidence": []}]}
    calls = {"retriever": 0, "client": 0}

    def retriever(need_more):
        calls["retriever"] += 1
        return "ctx"

    def client(messages, key):
        calls["client"] += 1
        return final

    out = p3.run([{"name": "P"}], "KEY", retriever=retriever, client=client)
    assert out == final["classifications"]
    assert calls == {"retriever": 1, "client": 1}      # single round


def test_run_with_ask_for_more_round():
    replies = [
        {"classifications": [], "need_more": {"greps": ["Foo"], "files": []}},   # 1st: asks
        {"classifications": [{"pattern": "P", "verdict": "Better", "evidence": []}]},  # 2nd: final
    ]
    seen_need_more = []

    def retriever(need_more):
        seen_need_more.append(need_more)
        return "ctx-more" if need_more else "ctx-initial"

    def client(messages, key):
        return replies.pop(0)

    out = p3.run([{"name": "P"}], "KEY", retriever=retriever, client=client)
    assert out[0]["verdict"] == "Better"
    assert seen_need_more == [None, {"greps": ["Foo"], "files": []}]   # initial, then the ask


# ── classification serialization ──────────────────────────────────────────
def test_classification_md_verdict_evidence_badge():
    md = serialize.classification_md([
        {"pattern": "P1", "verdict": "Missing", "rationale": "r",
         "evidence": [{"file": "a.md", "line": 3, "quote": "q"}], "verified": True},
    ])
    assert "## P1 — **Missing**" in md and "a.md:3" in md and "✅" in md


def test_classification_md_unverified_badge():
    md = serialize.classification_md([
        {"pattern": "P", "verdict": "Exists", "evidence": [], "verified": False}])
    assert "⚠️" in md
