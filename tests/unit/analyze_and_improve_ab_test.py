#!/usr/bin/env python3
"""Unit tests for the A/B validation harness (Etapa 4, #262) — pure comparison and
report logic. No network: the live run() is exercised only in the Actions job."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import ab_validate as ab  # noqa: E402


# ── label normalization ───────────────────────────────────────────────────
def test_canonical_verdict_maps_historical_and_fresh():
    assert ab.canonical_verdict("Already Exists") == "Exists"
    assert ab.canonical_verdict("Partial Coverage") == "Partial"
    assert ab.canonical_verdict("Better Implementation") == "Better"
    assert ab.canonical_verdict("Missing") == "Missing"
    assert ab.canonical_verdict("Exists") == "Exists"     # fresh label
    assert ab.canonical_verdict("nonsense") is None
    assert ab.canonical_verdict("") is None


def test_normalize_name():
    assert ab.normalize_name("Structured Output Contract") == "structured output contract"
    assert ab.normalize_name("Error-Context  Hygiene!") == "error context hygiene"


def test_historical_from_yaml():
    data = {"patterns": [
        {"id": 1, "name": "A", "classification": "Already Exists"},
        {"id": 2, "name": "B", "classification": "Partial Coverage"},
        {"id": 3, "name": "C", "classification": "junk"},   # unmapped → dropped
        {"id": 4, "classification": "Missing"},              # no name → dropped
    ]}
    assert ab.historical_from_yaml(data) == [
        {"name": "A", "verdict": "Exists"}, {"name": "B", "verdict": "Partial"}]


def test_fresh_from_classifications():
    cls = [{"pattern": "A", "verdict": "Exists"}, {"pattern": "B", "verdict": "Nope"},
           {"verdict": "Missing"}]
    assert ab.fresh_from_classifications(cls) == [{"name": "A", "verdict": "Exists"}]


# ── agreement ─────────────────────────────────────────────────────────────
def test_label_agreement_full():
    fresh = [{"name": "Structured Output", "verdict": "Exists"},
             {"name": "Error Context", "verdict": "Missing"}]
    hist = [{"name": "structured output", "verdict": "Exists"},
            {"name": "Error Context", "verdict": "Missing"},
            {"name": "Unshared", "verdict": "Partial"}]
    a = ab.label_agreement(fresh, hist)
    assert a["shared"] == 2 and a["matched"] == 2 and a["agreement"] == 1.0
    assert a["mismatches"] == []


def test_label_agreement_partial_with_mismatch():
    fresh = [{"name": "P1", "verdict": "Exists"}, {"name": "P2", "verdict": "Missing"}]
    hist = [{"name": "P1", "verdict": "Partial"}, {"name": "P2", "verdict": "Missing"}]
    a = ab.label_agreement(fresh, hist)
    assert a["shared"] == 2 and a["matched"] == 1 and a["agreement"] == 0.5
    assert a["mismatches"] == [{"name": "p1", "fresh": "Exists", "historical": "Partial"}]


def test_label_agreement_no_overlap_is_zero():
    a = ab.label_agreement([{"name": "X", "verdict": "Exists"}],
                           [{"name": "Y", "verdict": "Exists"}])
    assert a["shared"] == 0 and a["agreement"] == 0.0    # no false confidence


def test_label_agreement_fuzzy_matches_near_names():
    # curated "Structured Output Contract" vs GLM "Structured Output" — no exact
    # match, but the default fuzzy matcher pairs them.
    fresh = [{"name": "Structured Output", "verdict": "Exists"}]
    hist = [{"name": "Structured Output Contract", "verdict": "Exists"}]
    a = ab.label_agreement(fresh, hist)
    assert a["shared"] == 1 and a["matched"] == 1 and a["agreement"] == 1.0


def test_fuzzy_matcher_greedy_unique():
    m = ab.fuzzy_matcher(threshold=0.6)
    pairs = m(["error context hygiene", "structured output"],
              ["error context", "structured output contract"])
    assert pairs["error context"] == "error context hygiene"
    assert pairs["structured output contract"] == "structured output"


# ── decision ──────────────────────────────────────────────────────────────
def test_decide_ab_pass():
    d = ab.decide_ab({"agreement": 0.85, "shared": 10}, True)
    assert d["passed"] is True and d["criteria"] == {"label_agreement": True,
                                                     "seeded_duplicate_caught": True}


def test_decide_ab_fail_on_low_agreement():
    d = ab.decide_ab({"agreement": 0.5, "shared": 10}, True)
    assert d["passed"] is False and d["criteria"]["label_agreement"] is False


def test_decide_ab_fail_on_missed_duplicate():
    d = ab.decide_ab({"agreement": 0.95, "shared": 10}, False)
    assert d["passed"] is False and d["criteria"]["seeded_duplicate_caught"] is False


def test_decide_ab_fail_on_tiny_shared_sample():
    # high agreement but only 1 shared pattern → criterion 1 must NOT pass
    d = ab.decide_ab({"agreement": 1.0, "shared": 1}, True, min_shared=5)
    assert d["passed"] is False and d["criteria"]["label_agreement"] is False


# ── floor suggestion + report ─────────────────────────────────────────────
def test_suggest_floor_from_p90():
    assert ab.suggest_floor({"p90": 0.42, "p50": 0.2}) == 0.42
    assert ab.suggest_floor({}) == 0.0


def test_ab_report_pass_and_fail():
    agreement = {"agreement": 0.9, "matched": 9, "shared": 10, "mismatches": []}
    dup = {"duplicate": True, "score": 0.99}
    dec = ab.decide_ab(agreement, True)
    rep = ab.ab_report(agreement, dup, {"p90": 0.4}, 4.0, dec,
                       suggested_floor=0.4, suggested_cut=4.0)
    assert "PROSSEGUIR PRO TIER B" in rep and "90%" in rep and "Floor sugerido" in rep

    dec_fail = ab.decide_ab({"agreement": 0.3, "matched": 3, "shared": 10, "mismatches": [
        {"name": "p", "fresh": "Missing", "historical": "Exists"}]}, False)
    rep2 = ab.ab_report({"agreement": 0.3, "matched": 3, "shared": 10, "mismatches": [
        {"name": "p", "fresh": "Missing", "historical": "Exists"}]},
        {"duplicate": False, "score": 0.1}, {}, 1.0, dec_fail,
        suggested_floor=0.0, suggested_cut=1.0)
    assert "ITERAR" in rep2 and "fresh=**Missing**" in rep2
