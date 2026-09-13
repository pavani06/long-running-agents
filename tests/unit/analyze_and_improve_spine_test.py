#!/usr/bin/env python3
"""Unit tests for Etapa 3 pure parts — cosine dedup, rubric parsing, quarantine
routing, and PR/Issue construction (the surface the DoD names), plus the spine
helpers and the shared retriever. No network."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import dedup  # noqa: E402
import evaluator  # noqa: E402
import landing  # noqa: E402
import quarantine  # noqa: E402
import retrieval  # noqa: E402
import spine  # noqa: E402
from glm import GLMError  # noqa: E402


# ── dedup (cosine duplication) ────────────────────────────────────────────
DUP_INDEX = {"records": {
    "a": {"path": "docs/canonical/a.md", "heading": "A", "vector": [1.0, 0.0]},
    "b": {"path": "docs/canonical/b.md", "heading": "B", "vector": [0.0, 1.0]},
}}


def test_is_duplicate_above_threshold():
    r = dedup.is_duplicate([1.0, 0.02], DUP_INDEX, 0.85)
    assert r["duplicate"] is True and r["nearest"]["id"] == "a"


def test_is_duplicate_below_threshold():
    r = dedup.is_duplicate([1.0, 1.0], DUP_INDEX, 0.85)   # ~0.707 to each
    assert r["duplicate"] is False


def test_is_duplicate_empty_index():
    r = dedup.is_duplicate([1.0, 0.0], {"records": {}}, 0.85)
    assert r == {"duplicate": False, "score": 0.0, "nearest": None}


# ── evaluator rubric parsing ──────────────────────────────────────────────
def test_build_messages_has_rubric_criteria():
    sys_msg = evaluator.build_messages({"x": 1})[0]["content"]
    for c in evaluator.CRITERIA:
        assert c in sys_msg


def test_parse_evaluation_pass():
    reply = {"scores": {"fidelity": 4, "evidence": 4, "non_duplication": 3, "format": 5},
             "rationale": "ok"}
    out = evaluator.parse_evaluation(reply, min_mean=3.0)
    assert out["passed"] is True and out["mean"] == 4.0


def test_parse_evaluation_fail_below_min():
    reply = {"scores": {"fidelity": 2, "evidence": 2, "non_duplication": 2, "format": 2}}
    assert evaluator.parse_evaluation(reply, min_mean=3.0)["passed"] is False


def test_parse_evaluation_missing_criterion():
    with pytest.raises(GLMError):
        evaluator.parse_evaluation({"scores": {"fidelity": 5}})


def test_parse_evaluation_out_of_range():
    with pytest.raises(GLMError):
        evaluator.parse_evaluation({"scores": {"fidelity": 9, "evidence": 3,
                                               "non_duplication": 3, "format": 3}})


def test_parse_evaluation_bool_rejected():
    with pytest.raises(GLMError):
        evaluator.parse_evaluation({"scores": {"fidelity": True, "evidence": 3,
                                               "non_duplication": 3, "format": 3}})


def test_run_evaluator_with_fake_client():
    reply = {"scores": {"fidelity": 5, "evidence": 5, "non_duplication": 5, "format": 5}}
    out = evaluator.run({"a": 1}, "KEY", client=lambda m, k: reply)
    assert out["passed"] is True and out["mean"] == 5.0


# ── quarantine routing ────────────────────────────────────────────────────
def test_decide_accepted_when_all_pass():
    report = quarantine.report_from_gates(validate_obsidian=True, citations_ok=True,
                                          duplicate=False, evaluation_passed=True)
    d = quarantine.decide(report)
    assert d == {"accepted": True, "reasons": []}
    assert quarantine.destination_subdir(True) == ""


def test_decide_quarantines_on_duplicate():
    report = quarantine.report_from_gates(validate_obsidian=True, citations_ok=True,
                                          duplicate=True, evaluation_passed=True)
    d = quarantine.decide(report)
    assert d["accepted"] is False
    assert any("duplica" in r.lower() for r in d["reasons"])
    assert quarantine.destination_subdir(False) == "proposed"


def test_decide_fail_closed_on_missing_gate():
    assert quarantine.decide({})["accepted"] is False        # missing gates → held


def test_decide_lists_all_failures():
    report = quarantine.report_from_gates(validate_obsidian=False, citations_ok=False,
                                          duplicate=True, evaluation_passed=False)
    assert len(quarantine.decide(report)["reasons"]) == 4


# ── landing library ───────────────────────────────────────────────────────
def test_landing_plan_describe():
    assert "auto-merge OFF" in landing.LandingPlan(auto_merge=False, dry_run=True).describe()
    assert landing.LandingPlan(auto_merge=True, dry_run=False).describe() == "auto-merge ON"


def test_pr_body_accepted():
    summary = {"slug": "s", "accepted": True, "reasons": [],
               "classifications": [{"verdict": "Missing"}, {"verdict": "Missing"},
                                   {"verdict": "Exists"}],
               "evaluation": {"mean": 4.0, "passed": True},
               "dedup": {"duplicate": False, "score": 0.3},
               "plan": landing.LandingPlan(auto_merge=False, dry_run=True)}
    body = landing.pr_body(summary)
    assert "`s`" in body and "aceito" in body
    assert "Missing: 2" in body and "Exists: 1" in body
    assert "auto-merge OFF" in body


def test_pr_body_quarantine_lists_reasons():
    summary = {"slug": "s", "accepted": False, "reasons": ["evaluator adversarial abaixo do corte"],
               "classifications": [], "evaluation": {"mean": 1.0, "passed": False},
               "dedup": {"duplicate": False, "score": 0.1}, "plan": None}
    body = landing.pr_body(summary)
    assert "quarentena" in body and "abaixo do corte" in body


def test_quarantine_digest_empty_and_items():
    assert "nada em quarentena" in landing.quarantine_digest([])
    d = landing.quarantine_digest([{"slug": "x", "reasons": ["r1"], "link": "http://pr/1"}])
    assert "`x`" in d and "r1" in d and "http://pr/1" in d


# ── spine helpers ─────────────────────────────────────────────────────────
def test_artifact_for_eval_shape():
    art = spine.artifact_for_eval(
        {"thesis": "T", "concepts": [], "claims": []},
        [{"name": "P", "problem": "prob", "mechanism": "m", "tradeoffs": "t"}],
        [{"pattern": "P", "verdict": "Missing", "verified": True, "evidence": []}])
    assert art["thesis"] == "T"
    assert art["patterns"] == [{"name": "P", "problem": "prob"}]
    assert art["classifications"] == [{"pattern": "P", "verdict": "Missing", "verified": True}]


def test_dedup_text_joins_thesis_and_patterns():
    txt = spine.dedup_text({"thesis": "Big idea"},
                           [{"name": "P1", "problem": "prob one"}])
    assert "Big idea" in txt and "P1: prob one" in txt


# ── shared retriever (make_pattern_retriever) ─────────────────────────────
def test_make_pattern_retriever_empty_need_more(tmp_path):
    calls = {"embed": 0}

    def fake_embed(texts, key):
        calls["embed"] += 1
        return [[1.0, 0.0]]

    r = retrieval.make_pattern_retriever([{"name": "P"}], DUP_INDEX, "KEY", tmp_path,
                                         embed_fn=fake_embed)
    ctx = r({"greps": [], "files": []})       # no dense, no grep → both empty
    assert ctx.count("_(nenhuma)_") == 2
    assert calls["embed"] == 0                # need_more path doesn't embed


def test_make_pattern_retriever_initial_embeds(tmp_path):
    calls = {"embed": 0}

    def fake_embed(texts, key):
        calls["embed"] += 1
        return [[1.0, 0.0]]

    r = retrieval.make_pattern_retriever([{"name": "P", "problem": "x", "mechanism": "y"}],
                                         DUP_INDEX, "KEY", tmp_path, embed_fn=fake_embed)
    ctx = r(None)                             # initial → embeds the query
    assert calls["embed"] == 1
    assert "dense retrieval" in ctx
