#!/usr/bin/env python3
"""Unit tests for the T1–T4 metrics + Gates A/B/C (#288) — all pure."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import metamorphic_metrics as met  # noqa: E402


# ── T1 identification ───────────────────────────────────────────────────────
def test_t1_perfect():
    cases = [{"true": "A", "predicted": "A"}, {"true": "A", "predicted": "A"}]
    t1 = met.t1_identification(cases)
    assert t1["recall"] == 1.0 and t1["precision"] == 1.0 and t1["false_merge_rate"] == 0.0


def test_t1_distinguishes_unmatched_from_false_merge():
    cases = [{"true": "A", "predicted": "A"},   # correct
             {"true": "A", "predicted": None},  # unmatched (miss, not merge)
             {"true": "A", "predicted": "B"}]   # false merge
    t1 = met.t1_identification(cases)
    assert t1["correct"] == 1 and t1["matched"] == 2 and t1["false_merge"] == 1
    assert round(t1["recall"], 3) == 0.333 and t1["false_merge_rate"] == 0.333
    assert t1["precision"] == 0.5


# ── T2 invariance ───────────────────────────────────────────────────────────
def test_t2_only_counts_correctly_mapped_and_measures_agreement():
    cases = [
        {"true": "A", "predicted": "A", "verdict": "Exists"},
        {"true": "A", "predicted": "A", "verdict": "Exists"},
        {"true": "A", "predicted": "A", "verdict": "Partial"},
        {"true": "A", "predicted": "B", "verdict": "Missing"},  # misrouted → ignored
    ]
    t2 = met.t2_invariance(cases)
    assert t2["considered"] == 3
    assert t2["agreement"] == round(2 / 3, 3)   # modal verdict Exists (2 of 3)


def test_t2_flags_exists_missing_dispersion():
    cases = [{"true": "A", "predicted": "A", "verdict": "Exists"},
             {"true": "A", "predicted": "A", "verdict": "Missing"}]
    t2 = met.t2_invariance(cases)
    assert t2["dispersion_flags"] and t2["dispersion_flags"][0]["concept_id"] == "A"


# ── T3 dedup invariance ─────────────────────────────────────────────────────
def test_t3_tp_on_same_concept_fp_on_distinct():
    items = [
        {"concept_id": "A", "vec": [1.0, 0.0]},
        {"concept_id": "A", "vec": [0.99, 0.01]},   # near-identical → TP
        {"concept_id": "B", "vec": [0.0, 1.0]},     # orthogonal → no FP
    ]
    t3 = met.t3_dedup_invariance(items, threshold=0.85)
    assert t3["same_pairs"] == 1 and t3["tp"] == 1 and t3["tp_rate"] == 1.0
    assert t3["diff_pairs"] == 2 and t3["fp"] == 0 and t3["fp_rate"] == 0.0


# ── T4 novelty discrimination ───────────────────────────────────────────────
def test_t4_counts_cross_boundary_merges_only():
    cases = [
        {"true": "A", "predicted": "B"},   # A→B is a near-miss boundary → offender
        {"true": "A", "predicted": "A"},   # correct
        {"true": "B", "predicted": "B"},   # correct
        {"true": "C", "predicted": "D"},   # C not in a near-miss pair → not considered
    ]
    t4 = met.t4_novelty(cases, [["A", "B"]])
    assert t4["considered"] == 3 and t4["false_merge"] == 1
    assert t4["false_merge_rate"] == round(1 / 3, 3)


# ── Gates ───────────────────────────────────────────────────────────────────
def test_gate_a_needs_recall_and_low_false_merge():
    assert met.gate_a({"recall": 0.92, "false_merge_rate": 0.04})["passed"]
    assert not met.gate_a({"recall": 0.92, "false_merge_rate": 0.06})["passed"]
    assert not met.gate_a({"recall": 0.80, "false_merge_rate": 0.0})["passed"]


def test_gate_b_needs_agreement_and_no_dispersion():
    assert met.gate_b({"agreement": 0.95, "dispersion_flags": []})["passed"]
    assert not met.gate_b({"agreement": 0.95, "dispersion_flags": [{"concept_id": "A"}]})["passed"]
    assert not met.gate_b({"agreement": 0.5, "dispersion_flags": []})["passed"]


def test_gate_c_requires_every_existence_verdict_verified():
    ok = met.gate_c([{"concept_id": "A", "verdict": "Exists", "verified": True}])
    assert ok["passed"] and ok["verified"] == 1
    bad = met.gate_c([{"concept_id": "A", "verdict": "Exists", "verified": False}])
    assert not bad["passed"] and bad["unverified"][0]["concept_id"] == "A"


def test_poc_decision_requires_all_gates_and_sanity():
    g = {"passed": True}
    assert met.poc_decision(g, g, g, {"passed": True})["passed"]
    assert not met.poc_decision(g, g, g, {"passed": False})["passed"]
    assert not met.poc_decision(g, {"passed": False}, g, {"passed": True})["passed"]
