#!/usr/bin/env python3
"""Unit tests for the two-stage matcher pure parts (#288)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import metamorphic_match as mm  # noqa: E402


# ── stage 1: cosine ranking ─────────────────────────────────────────────────
def test_rank_candidates_orders_by_cosine_and_caps_k():
    q = [1.0, 0.0]
    vecs = {"same": [1.0, 0.0], "near": [0.9, 0.1], "orth": [0.0, 1.0]}
    ranked = mm.rank_candidates(q, vecs, k=2)
    assert [r["concept_id"] for r in ranked] == ["same", "near"]
    assert ranked[0]["score"] > ranked[1]["score"]


def test_rank_candidates_floor_drops_weak_matches():
    q = [1.0, 0.0]
    vecs = {"same": [1.0, 0.0], "orth": [0.0, 1.0]}
    ranked = mm.rank_candidates(q, vecs, k=5, floor=0.5)
    assert [r["concept_id"] for r in ranked] == ["same"]


def test_rank_candidates_skips_empty_vectors():
    ranked = mm.rank_candidates([1.0, 0.0], {"a": [], "b": [1.0, 0.0]}, k=5)
    assert [r["concept_id"] for r in ranked] == ["b"]


# ── stage 2: decision ───────────────────────────────────────────────────────
def test_decide_match_picks_highest_confidence_same_concept():
    results = [
        {"concept_id": "A", "same_concept": True, "confidence": 0.7,
         "granularity_relation": "equivalent", "stage1_score": 0.6},
        {"concept_id": "B", "same_concept": True, "confidence": 0.9,
         "granularity_relation": "broader_than", "stage1_score": 0.5},
    ]
    d = mm.decide_match(results)
    assert d["matched"] and d["concept_id"] == "B" and d["confidence"] == 0.9


def test_decide_match_unmatched_when_none_same_concept():
    results = [{"concept_id": "A", "same_concept": False, "confidence": 0.9,
                "granularity_relation": "related_but_distinct", "stage1_score": 0.6}]
    d = mm.decide_match(results)
    assert d["matched"] is False and d["concept_id"] is None


def test_decide_match_respects_min_confidence():
    results = [{"concept_id": "A", "same_concept": True, "confidence": 0.3,
                "granularity_relation": "equivalent", "stage1_score": 0.6}]
    assert mm.decide_match(results, min_confidence=0.5)["matched"] is False


def test_decide_match_tie_breaks_on_stage1_score():
    results = [
        {"concept_id": "A", "same_concept": True, "confidence": 0.8,
         "granularity_relation": "equivalent", "stage1_score": 0.4},
        {"concept_id": "B", "same_concept": True, "confidence": 0.8,
         "granularity_relation": "equivalent", "stage1_score": 0.7},
    ]
    assert mm.decide_match(results)["concept_id"] == "B"


def test_decide_match_empty_is_unmatched():
    assert mm.decide_match([]) == {"concept_id": None, "matched": False,
                                   "confidence": 0.0, "granularity_relation": None}
