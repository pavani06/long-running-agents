#!/usr/bin/env python3
"""Unit tests for the stage-2 reranker pure parts (#288). No network: the OpenAI
call is stubbed with a fake client where a live path is exercised."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import metamorphic_rerank as rr  # noqa: E402
from glm import GLMError  # noqa: E402


# ── prompt assembly ─────────────────────────────────────────────────────────
def test_build_messages_carries_both_texts_and_rubric():
    msgs = rr.build_messages("alpha text", "beta text")
    assert msgs[0]["role"] == "system" and "granularity_relation" in msgs[0]["content"]
    assert "alpha text" in msgs[1]["content"] and "beta text" in msgs[1]["content"]


def test_concept_description_includes_definition_and_aliases():
    d = rr.concept_description({"canonical_definition": "the def", "aliases": ["x", "y"]})
    assert "the def" in d and "x, y" in d


# ── reply validation ────────────────────────────────────────────────────────
def test_parse_rerank_accepts_valid_reply():
    out = rr.parse_rerank({"same_concept": True, "confidence": 0.8,
                           "granularity_relation": "broader_than"})
    assert out == {"same_concept": True, "confidence": 0.8, "granularity_relation": "broader_than"}


@pytest.mark.parametrize("bad", [
    {"same_concept": "yes", "confidence": 0.5, "granularity_relation": "equivalent"},
    {"same_concept": True, "confidence": 1.5, "granularity_relation": "equivalent"},
    {"same_concept": True, "confidence": True, "granularity_relation": "equivalent"},  # bool≠number
    {"same_concept": True, "confidence": 0.5, "granularity_relation": "same-ish"},
    {"same_concept": True, "granularity_relation": "equivalent"},
])
def test_parse_rerank_rejects_malformed(bad):
    with pytest.raises(GLMError):
        rr.parse_rerank(bad)


# ── candidate reranking with a fake client ──────────────────────────────────
def test_rerank_candidates_attaches_stage1_score():
    concepts = {"A": {"canonical_definition": "da", "aliases": []},
                "B": {"canonical_definition": "db", "aliases": []}}
    fake = lambda messages, key: {"same_concept": True, "confidence": 0.9,
                                  "granularity_relation": "equivalent"}
    out = rr.rerank_candidates("v", [{"concept_id": "A", "score": 0.6}],
                               concepts, "k", client=fake)
    assert out[0]["concept_id"] == "A" and out[0]["stage1_score"] == 0.6
    assert out[0]["same_concept"] is True


# ── sanity mini-eval scoring ────────────────────────────────────────────────
def test_score_sanity_computes_accuracy_and_pass():
    pairs = [{"a": "1", "b": "1", "same": True}, {"a": "2", "b": "3", "same": False},
             {"a": "4", "b": "4", "same": True}]
    r = rr.score_sanity(pairs, [True, False, True], min_accuracy=0.8)
    assert r["accuracy"] == 1.0 and r["passed"] and r["mistakes"] == []


def test_score_sanity_flags_mistakes_and_fails_below_bar():
    pairs = [{"a": "1", "b": "1", "same": True}, {"a": "2", "b": "3", "same": False}]
    r = rr.score_sanity(pairs, [False, False], min_accuracy=0.8)
    assert r["accuracy"] == 0.5 and r["passed"] is False
    assert r["mistakes"] == [{"a": "1", "b": "1", "expected": True, "got": False}]


def test_score_sanity_empty_never_passes():
    assert rr.score_sanity([], [], min_accuracy=0.8)["passed"] is False
