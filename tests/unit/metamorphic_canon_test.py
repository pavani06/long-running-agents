#!/usr/bin/env python3
"""Unit tests for the Concept Canon loader/validation (#288) — pure logic, plus a
load of the SHIPPED canon that also verifies its evidence resolves on disk."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import metamorphic_canon as mc  # noqa: E402

CANON_PATH = ROOT / "eval" / "truth" / "metamorphic_canon.yaml"


def _concept(**over):
    base = {
        "concept_id": "c1", "canonical_definition": "def",
        "aliases": ["a"], "positive_examples": ["p"], "negative_examples": ["n"],
        "variants": ["v1", "v2"], "expected_repo_state": {"exists": True},
        "expected_verdict": "Exists",
        "evidence": [{"file": "scripts/x.py", "quote": "q"}],
    }
    base.update(over)
    return base


# ── pure structural validation ──────────────────────────────────────────────
def test_valid_minimal_canon_has_no_problems():
    canon = {"version": 1, "concepts": [_concept()]}
    assert mc.validate_structure(canon) == []


def test_exists_true_requires_evidence():
    canon = {"concepts": [_concept(evidence=[])]}
    probs = mc.validate_structure(canon)
    assert any("evidence[] is empty" in p for p in probs)


def test_missing_concept_must_not_carry_evidence():
    canon = {"concepts": [_concept(expected_repo_state={"exists": False},
                                   expected_verdict="Missing")]}
    assert any("carries evidence" in p for p in mc.validate_structure(canon))


def test_verdict_must_agree_with_exists():
    canon = {"concepts": [_concept(expected_repo_state={"exists": False},
                                   expected_verdict="Exists", evidence=[])]}
    assert any("contradicts verdict" in p for p in mc.validate_structure(canon))


def test_duplicate_concept_id_flagged():
    canon = {"concepts": [_concept(), _concept()]}
    assert any("duplicate concept_id" in p for p in mc.validate_structure(canon))


def test_near_miss_pair_must_reference_known_ids():
    canon = {"concepts": [_concept()], "near_miss_pairs": [["c1", "ghost"]]}
    assert any("unknown concept_id 'ghost'" in p for p in mc.validate_structure(canon))


def test_reranker_sanity_shape_checked():
    canon = {"concepts": [_concept()], "reranker_sanity": [{"a": "x", "same": True}]}
    assert any("reranker_sanity[0]" in p for p in mc.validate_structure(canon))


# ── pure helpers ─────────────────────────────────────────────────────────────
def test_profile_text_joins_definition_aliases_positives_only():
    txt = mc.profile_text(_concept(canonical_definition="D", aliases=["A1"],
                                   positive_examples=["P1"], negative_examples=["NEG"]))
    assert "D" in txt and "A1" in txt and "P1" in txt and "NEG" not in txt


def test_all_variants_flattens_with_ground_truth():
    canon = {"concepts": [_concept(concept_id="c1", variants=["v1", "v2"])]}
    vs = mc.all_variants(canon)
    assert len(vs) == 2
    assert vs[0] == {"variant": "v1", "concept_id": "c1",
                     "expected_verdict": "Exists", "exists": True}


def test_evidence_substring_ok_is_whitespace_insensitive():
    assert mc.evidence_substring_ok("hello world", "xx  hello\n  world yy")
    assert not mc.evidence_substring_ok("absent", "nothing here")
    assert not mc.evidence_substring_ok("", "anything")


def test_check_evidence_on_disk_uses_injected_reader():
    canon = {"concepts": [_concept(evidence=[{"file": "a.py", "quote": "needle"}])]}
    ok = mc.check_evidence_on_disk(canon, ROOT, reader=lambda f: "has a needle inside")
    assert ok == []
    missing = mc.check_evidence_on_disk(canon, ROOT, reader=lambda f: None)
    assert any("file not found" in p for p in missing)
    badquote = mc.check_evidence_on_disk(canon, ROOT, reader=lambda f: "no match")
    assert any("quote not found" in p for p in badquote)


# ── the shipped canon must be valid AND its evidence must resolve on disk ─────
def test_shipped_canon_is_structurally_valid():
    canon = mc.load_canon(CANON_PATH)   # raises on any structural problem
    s = mc.summary(canon)
    assert s["concepts"] == 10 and s["variants"] == 50
    assert s["exists"] == 5 and s["missing"] == 3 and s["partial"] == 2


def test_shipped_canon_evidence_resolves_against_real_repo():
    canon = mc.load_canon(CANON_PATH)
    problems = mc.check_evidence_on_disk(canon, ROOT)
    assert problems == [], f"canon evidence must point at real repo content: {problems}"
