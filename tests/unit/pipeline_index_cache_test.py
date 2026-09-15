#!/usr/bin/env python3
"""load_state fallback safety for the First-Loop index cache (#263 operational fix).

A restored .runtime index is an optimization, never authoritative: a missing OR
corrupt state must fall back to the empty state (base_sha None → run_index full-rebuild
path), not crash. No network."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import pipeline  # noqa: E402

EMPTY = {"version": 1, "base_sha": None, "records": {}}


def test_load_state_missing_returns_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(pipeline, "STATE_PATH", tmp_path / "index.json")
    assert pipeline.load_state() == EMPTY          # cache miss → full-rebuild path


def test_load_state_valid_is_used(monkeypatch, tmp_path):
    sp = tmp_path / "index.json"
    sp.write_text('{"version": 1, "base_sha": "abc123", "records": {"x": {}}}', encoding="utf-8")
    monkeypatch.setattr(pipeline, "STATE_PATH", sp)
    state = pipeline.load_state()
    assert state["base_sha"] == "abc123" and "x" in state["records"]   # restored → incremental path


def test_load_state_corrupt_json_falls_back(monkeypatch, tmp_path):
    sp = tmp_path / "index.json"
    sp.write_text("{not valid json,,,", encoding="utf-8")
    monkeypatch.setattr(pipeline, "STATE_PATH", sp)
    assert pipeline.load_state() == EMPTY          # corruption → rebuild, no crash


def test_load_state_non_dict_falls_back(monkeypatch, tmp_path):
    sp = tmp_path / "index.json"
    sp.write_text('["not", "a", "dict"]', encoding="utf-8")
    monkeypatch.setattr(pipeline, "STATE_PATH", sp)
    assert pipeline.load_state() == EMPTY          # wrong shape → rebuild fallback
