#!/usr/bin/env python3
"""Unit tests for the analyze-and-improve judgment plane (Fases 0-2), pure parts.

Covers what the Etapa 1 DoD names — prompt assembly and output parsing — plus
serialization and package writing. No network: the GLM client is never called;
`run()` receives an injected fake client returning canned JSON.
"""
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import analysis_package  # noqa: E402
import phase0_mental_model as p0  # noqa: E402
import phase1_extract as p1  # noqa: E402
import phase2_patterns as p2  # noqa: E402
import serialize  # noqa: E402
from glm import GLMError, extract_json  # noqa: E402


# ── glm.extract_json (output parsing) ─────────────────────────────────────
def test_extract_json_plain():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_extract_json_strips_code_fence():
    assert extract_json('```json\n{"a": 1}\n```') == {"a": 1}


def test_extract_json_embedded_in_prose():
    assert extract_json('Sure! Here:\n{"a": [1, 2]}\nDone.') == {"a": [1, 2]}


def test_extract_json_no_object_raises():
    with pytest.raises(GLMError):
        extract_json("no json here")


def test_extract_json_bad_json_raises():
    with pytest.raises(GLMError):
        extract_json('{"a": }')


# ── Fase 1 — extraction ───────────────────────────────────────────────────
def test_p1_build_messages_fences_full_transcript():
    transcript = "line one\n" * 5000  # large; must NOT be truncated
    msgs = p1.build_messages(transcript)
    assert msgs[0]["role"] == "system" and msgs[1]["role"] == "user"
    assert "<untrusted_source>" in msgs[1]["content"]
    assert "</untrusted_source>" in msgs[1]["content"]
    assert transcript in msgs[1]["content"]              # full fidelity, no cap
    assert "DADO" in msgs[0]["content"]                  # injection guard present


def test_p1_parse_extraction_ok():
    good = {"thesis": "t", "concepts": [{"name": "c", "summary": "s"}],
            "claims": [{"claim": "x", "evidence": "y"}]}
    assert p1.parse_extraction(good) is good


def test_p1_parse_extraction_missing_key():
    with pytest.raises(GLMError):
        p1.parse_extraction({"thesis": "t", "concepts": []})     # no claims


def test_p1_parse_extraction_concepts_not_list():
    with pytest.raises(GLMError):
        p1.parse_extraction({"thesis": "t", "concepts": "nope", "claims": []})


def test_p1_run_with_fake_client():
    canned = {"thesis": "t", "concepts": [], "claims": []}
    seen = {}

    def fake(messages, api_key):
        seen["messages"] = messages
        return canned

    out = p1.run("some transcript", "KEY", client=fake)
    assert out == canned
    assert "<untrusted_source>" in seen["messages"][1]["content"]


# ── Fase 0 — mental model ─────────────────────────────────────────────────
def test_p0_build_messages_with_prev_and_sections():
    prev = {"goals": ["g1"], "architecture": {"abstractions": []}, "patterns": []}
    sections = [{"path": "docs/canonical/x.md", "heading": "H", "text": "body"}]
    msgs = p0.build_messages(prev, sections)
    user = msgs[1]["content"]
    assert "docs/canonical/x.md" in user and "<repo_sections>" in user
    assert '"g1"' in user                                # prev model serialized in


def test_p0_build_messages_initial_build():
    msgs = p0.build_messages(None, [])
    assert "build inicial" in msgs[1]["content"]


def test_p0_parse_model_ok():
    good = {"goals": [], "architecture": {"abstractions": [{"name": "a", "role": "r"}]},
            "patterns": []}
    assert p0.parse_model(good) is good


def test_p0_parse_model_missing_section():
    with pytest.raises(GLMError):
        p0.parse_model({"goals": [], "patterns": []})            # no architecture


def test_p0_parse_model_architecture_without_abstractions():
    with pytest.raises(GLMError):
        p0.parse_model({"goals": [], "architecture": {}, "patterns": []})


def test_p0_run_injects_meta():
    model = {"goals": [], "architecture": {"abstractions": []}, "patterns": []}
    out = p0.run(None, [], "KEY", meta={"base_commit": "abc"},
                 client=lambda m, k: model)
    assert out["meta"] == {"base_commit": "abc"}
    assert out["goals"] == []


# ── Fase 2 — patterns ─────────────────────────────────────────────────────
def test_p2_build_messages_includes_extraction():
    extraction = {"thesis": "T", "concepts": [], "claims": []}
    msgs = p2.build_messages(extraction)
    assert '"thesis": "T"' in msgs[1]["content"]


def test_p2_parse_patterns_ok():
    reply = {"patterns": [{"name": "n", "problem": "p", "mechanism": "m", "tradeoffs": "t"}]}
    assert p2.parse_patterns(reply) == reply["patterns"]


def test_p2_parse_patterns_empty_ok():
    assert p2.parse_patterns({"patterns": []}) == []


def test_p2_parse_patterns_not_list():
    with pytest.raises(GLMError):
        p2.parse_patterns({"patterns": {}})


def test_p2_parse_patterns_missing_field():
    with pytest.raises(GLMError):
        p2.parse_patterns({"patterns": [{"name": "n", "problem": "p"}]})   # no mechanism/tradeoffs


def test_p2_run_with_fake_client():
    reply = {"patterns": []}
    assert p2.run({"thesis": "t", "concepts": [], "claims": []}, "KEY",
                  client=lambda m, k: reply) == []


# ── serialization ─────────────────────────────────────────────────────────
def test_to_yaml_roundtrips():
    obj = {"meta": {"date": "2026-09-13"}, "goals": ["a", "b"]}
    assert yaml.safe_load(serialize.to_yaml(obj)) == obj


def test_mental_model_md_has_sections():
    model = {"meta": {"title": "T", "repo": "r", "base_commit": "c"},
             "goals": ["g1"], "architecture": {"abstractions": [{"name": "A", "role": "R"}]},
             "patterns": [{"name": "P", "where_defined": "x", "maturity": "stable"}],
             "gaps": []}
    md = serialize.mental_model_md(model)
    assert "# Mental Model: T" in md and "## Goals" in md and "g1" in md and "**A**" in md


def test_extraction_md_has_thesis():
    md = serialize.extraction_md({"thesis": "The thesis", "concepts": [], "claims": []})
    assert "## Tese" in md and "The thesis" in md


def test_patterns_md_empty_and_nonempty():
    assert "nenhum" in serialize.patterns_md([])
    md = serialize.patterns_md([{"name": "N", "problem": "p", "mechanism": "m", "tradeoffs": "t"}])
    assert "## N" in md and "Mecanismo" in md


# ── package writing (I/O, tmp) ────────────────────────────────────────────
def test_write_package_writes_expected_files(tmp_path):
    slug = "2026-09-13-example"
    written = analysis_package.write_package(
        tmp_path, slug,
        mental_model={"goals": [], "architecture": {"abstractions": []}, "patterns": []},
        extraction={"thesis": "t", "concepts": [], "claims": []},
        patterns=[],
    )
    names = {Path(w).name for w in written}
    assert names == {
        f"{slug}-mental-model.yaml", f"{slug}-mental-model.md",
        f"{slug}-analysis.yaml", f"{slug}-analysis.md",
        f"{slug}-patterns.yaml", f"{slug}-patterns.md",
    }
    pkg = tmp_path / "docs" / "analysis" / slug
    assert (pkg / f"{slug}-patterns.yaml").exists()
    assert yaml.safe_load((pkg / f"{slug}-patterns.yaml").read_text()) == {"patterns": []}


def test_write_package_partial(tmp_path):
    written = analysis_package.write_package(tmp_path, "s", extraction={"thesis": "t", "concepts": [], "claims": []})
    assert {Path(w).name for w in written} == {"s-analysis.yaml", "s-analysis.md"}
