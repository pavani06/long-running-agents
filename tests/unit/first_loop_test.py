#!/usr/bin/env python3
"""Unit tests for the First-Loop deterministic selection + PR-body assembly (#263 slice).
Pure parts only; no network, no GLM."""
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

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
        artifact=artifact, proposed_path="docs/canonical/b.md",   # canonical target on the branch
        gates={"citations_ok": True},
        evaluation={"mean": 3.5, "passed": True, "scores": {}, "rationale": "ok"},
        dup={"duplicate": False, "score": 0.4})
    assert "auto_merge=OFF" in body or "auto-merge OFF" in body
    assert "creation != promotion" in body
    assert "docs/canonical/b.md" in body                     # the canonical target file
    assert "PR é a quarentena" in body                       # PR-is-quarantine model
    assert "merge deste PR é a promoção" in body             # merge = promotion
    assert "O que o humano está sendo pedido a aprovar" in body
    assert "roda no CI" in body and "Check Obsidian Conventions" in body   # actual validate-obsidian contract


# ── run() exit semantics: no-op success vs error (#263 operational fix) ─────
def _patch_pipeline(monkeypatch, tmp_path, *, classifications, phase1_raises=None):
    """Drive run() offline: patch every collaborator + capture _emit_output. Returns the
    emitted (key,value) list."""
    monkeypatch.setenv("ZAI_API_KEY", "z")
    monkeypatch.setenv("OPENAI_API_KEY", "o")
    monkeypatch.setenv("PR_BODY_PATH", str(tmp_path / "pr-body.md"))
    monkeypatch.setattr(fl, "load_state", lambda: {"records": {"a": {"path": "docs/canonical/x.md"}}})
    monkeypatch.setattr(fl, "scan_pending", lambda d: [P("2026-09-11-real-source--vid.md")])
    tp = tmp_path / "t.txt"
    tp.write_text("transcript body", encoding="utf-8")
    monkeypatch.setattr(fl, "_transcript_for", lambda f: tp)
    monkeypatch.setattr(fl.retrieval, "make_pattern_retriever",
                        lambda *a, **k: (lambda need_more=None: "REPO-CTX"))

    def _p1(transcript, key):
        if phase1_raises:
            raise phase1_raises
        return {"thesis": "T", "video_id": "v"}

    monkeypatch.setattr(fl.phase1_extract, "run", _p1)
    monkeypatch.setattr(fl.phase2_patterns, "run",
                        lambda extraction, key: [{"name": "P", "problem": "pr",
                                                  "mechanism": "m", "tradeoffs": "t"}])
    monkeypatch.setattr(fl.phase3_classify, "run", lambda patterns, key, retriever: classifications)
    monkeypatch.setattr(fl.phase3_classify, "citations_of", lambda c: [])
    monkeypatch.setattr(fl.phase3_classify, "mark_verified", lambda c, v: c)
    monkeypatch.setattr(fl.phase3_classify, "mark_grounding", lambda c, v: c)
    monkeypatch.setattr(fl.grep_verify, "verify_all", lambda cits, root: [])
    monkeypatch.setattr(fl.grep_verify, "all_ok", lambda v: True)
    monkeypatch.setattr(fl.phase4_create, "create",
                        lambda pattern, **k: {"type": "canonical", "title": "T", "content": "B",
                                              "intended_destination": "docs/canonical/p.md"})
    monkeypatch.setattr(fl.phase4_create, "write_proposed",
                        lambda root, art, slug, pat: "docs/canonical/p.md")
    monkeypatch.setattr(fl.evaluator, "run",
                        lambda art, key: {"mean": 4.0, "passed": True, "scores": {}, "rationale": "ok"})
    monkeypatch.setattr(fl, "embed_texts", lambda texts, key: [[0.1]])
    monkeypatch.setattr(fl.dedup, "is_duplicate", lambda vec, idx: {"duplicate": False, "score": 0.5})
    emitted = []
    monkeypatch.setattr(fl, "_emit_output", lambda k, v: emitted.append((k, v)))
    return emitted


def test_run_no_eligible_missing_is_success_noop(monkeypatch, tmp_path):
    emitted = _patch_pipeline(monkeypatch, tmp_path,
                              classifications=[{"pattern": "P", "verdict": "Exists"}])
    rc = fl.run(source_arg=None, pattern_id=None)
    assert rc == 0                                              # successful no-op, not failure
    assert ("has_proposal", "false") in emitted
    assert not any(k == "proposed_path" for k, _ in emitted)    # no PR metadata
    assert not (tmp_path / "pr-body.md").exists()               # no artifact / PR body written


def test_run_eligible_missing_takes_f4_path(monkeypatch, tmp_path):
    emitted = _patch_pipeline(
        monkeypatch, tmp_path,
        classifications=[{"pattern": "P", "verdict": "Missing", "evidence": [], "rationale": "r"}])
    rc = fl.run(source_arg=None, pattern_id=None)
    assert rc == 0
    assert ("has_proposal", "true") in emitted
    assert ("proposed_path", "docs/canonical/p.md") in emitted   # normal F4 path + PR metadata


def test_run_actual_exception_still_fails(monkeypatch, tmp_path):
    _patch_pipeline(monkeypatch, tmp_path, classifications=[],
                    phase1_raises=RuntimeError("boom"))
    with pytest.raises(RuntimeError):                            # a real error is NOT swallowed
        fl.run(source_arg=None, pattern_id=None)
