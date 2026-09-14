#!/usr/bin/env python3
"""Unit tests for the PoC runner's fault-tolerance helper (#288).

The live loop makes ~50 GLM/OpenAI calls; a single unparseable reply must degrade
one variant, not abort the run (regression: run 34840697159 crashed on one bad
GLM JSON reply)."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import metamorphic_poc as poc  # noqa: E402
from glm import AuthError, GLMError, RateLimited  # noqa: E402


def test_safe_call_passes_through_success():
    result, err = poc.safe_call(lambda: {"verdict": "Exists"}, {"verdict": None})
    assert result == {"verdict": "Exists"} and err is None


def test_safe_call_swallows_glm_error_and_returns_default():
    def boom():
        raise GLMError("unparseable JSON in GLM reply")
    result, err = poc.safe_call(boom, {"verdict": None})
    assert result == {"verdict": None} and "unparseable JSON" in err


def test_safe_call_swallows_rate_limited():
    def boom():
        raise RateLimited("429 after retries")
    result, err = poc.safe_call(boom, {"concept_id": None})
    assert result == {"concept_id": None} and "429" in err


def test_safe_call_does_not_swallow_auth_error():
    # a bad key is fatal for every variant — it must propagate, not degrade silently
    def boom():
        raise AuthError("invalid key")
    with pytest.raises(AuthError):
        poc.safe_call(boom, {"verdict": None})


def test_report_notes_degraded_variants():
    import metamorphic_canon as mc
    canon = mc.load_canon(ROOT / "scripts" / "analyze-and-improve" / "metamorphic_canon.yaml")
    t1 = {"recall": 1.0, "precision": 1.0, "false_merge": 0, "false_merge_rate": 0.0, "total": 50}
    t2 = {"agreement": 0.9, "considered": 45, "dispersion_flags": [], "correctness_flags": []}
    t3 = {"same_pairs": 100, "tp": 90, "tp_rate": 0.9, "diff_pairs": 1, "fp": 0, "fp_rate": 0.0}
    t4 = {"considered": 35, "false_merge": 0, "false_merge_rate": 0.0, "offenders": []}
    import metamorphic_metrics as met
    ga, gb, gc = met.gate_a(t1), met.gate_b(t2), met.gate_c([])
    dec = met.poc_decision(ga, gb, gc, {"passed": True})
    rep = poc._report(canon, 50, {"correct": 6, "total": 6, "accuracy": 1.0, "passed": True},
                      t1, t2, t3, t4, ga, gb, gc, dec, errors=3)
    assert "3 variante(s) com erro de LLM" in rep
