#!/usr/bin/env python3
"""Unit tests for the Gate-B dispersion diagnostic pure logic (#288 follow-up)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import metamorphic_diagnose as dg  # noqa: E402


# ── disagreement ────────────────────────────────────────────────────────────
def test_disagreement_zero_when_invariant():
    assert dg.disagreement(["Exists"] * 5) == 0.0


def test_disagreement_counts_minority():
    assert dg.disagreement(["Exists", "Exists", "Exists", "Exists", "Missing"]) == 0.2
    assert dg.disagreement(["Missing", "Partial", "Exists"]) == round(1 - 1 / 3, 3)


def test_disagreement_empty_is_zero():
    assert dg.disagreement([]) == 0.0


# ── jaccard / retrieval stability ───────────────────────────────────────────
def test_jaccard_identical_sets_is_one():
    assert dg.jaccard([{1, 2, 3}, {1, 2, 3}]) == 1.0


def test_jaccard_disjoint_is_zero():
    assert dg.jaccard([{1, 2}, {3, 4}]) == 0.0


def test_jaccard_single_set_is_one():
    assert dg.jaccard([{1, 2}]) == 1.0


def test_retrieval_stability_reports_common_and_union():
    s = dg.retrieval_stability([{"a", "b"}, {"a", "c"}, {"a", "d"}])
    assert s["common"] == 1 and s["union"] == 4 and 0 < s["mean_jaccard"] < 1


def test_evidence_recall_fraction_of_variants_surfacing_evidence():
    topk = [{"dedup.py", "x.py"}, {"y.py"}, {"dedup.py"}]
    assert dg.evidence_recall(topk, {"dedup.py"}) == round(2 / 3, 3)
    assert dg.evidence_recall(topk, set()) == 0.0


# ── attribution ─────────────────────────────────────────────────────────────
def test_attribute_invariant_when_no_variable_dispersion():
    assert dg.attribute(["Exists"] * 5, ["Exists"] * 5)["label"] == "invariant"


def test_attribute_retrieval_driven_when_fixing_context_converges():
    # variable dispersed, fixed context makes them agree → retrieval was the cause
    a = dg.attribute(["Exists", "Missing", "Partial", "Exists", "Missing"], ["Exists"] * 5)
    assert a["label"] == "retrieval-driven"


def test_attribute_classifier_driven_when_fixing_context_does_not_help():
    # identical context, still dispersed → the classifier flips on wording alone
    a = dg.attribute(["Exists", "Missing", "Exists", "Missing", "Exists"],
                     ["Exists", "Missing", "Partial", "Missing", "Exists"])
    assert a["label"] == "classifier-driven"


def test_attribute_mixed_when_fixing_reduces_but_not_eliminates():
    a = dg.attribute(["Exists", "Missing", "Partial", "Missing", "Exists"],  # var 0.6
                     ["Exists", "Exists", "Exists", "Missing", "Partial"])   # fix 0.4
    assert a["label"] == "mixed"


# ── aggregate ───────────────────────────────────────────────────────────────
def test_aggregate_picks_dominant_driver_and_counts():
    per = [
        {"attribution": {"label": "classifier-driven"}},
        {"attribution": {"label": "classifier-driven"}},
        {"attribution": {"label": "retrieval-driven"}},
        {"attribution": {"label": "invariant"}},
    ]
    agg = dg.aggregate(per)
    assert agg["dominant_driver"] == "classifier"
    assert agg["dispersed_concepts"] == 3
    assert agg["labels"]["classifier-driven"] == 2
