#!/usr/bin/env python3
"""Unit tests for the artifacts manifest (#263) — the Fase-5 contract. Pure; no network."""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import artifact_manifest as am  # noqa: E402

PROMOTED_CANONICAL = {"type": "canonical", "pattern": "X", "phase3_verdict": "Missing",
                      "priority": "P0", "intended_destination": "docs/canonical/x.md"}
HELD_SKILL = {"type": "skill", "pattern": "X", "phase3_verdict": "Missing",
              "priority": "P0", "intended_destination": ".opencode/skills/x/SKILL.md",
              "quarantine_path": "docs/analysis/pkg/proposed/.opencode/skills/x/SKILL.md"}
PROMOTED_EXERCISE = {"type": "exercise", "pattern": "X", "phase3_verdict": "Missing",
                     "priority": "P0", "level": 3,
                     "intended_destination":
                         "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-12-x.md"}

OUTCOMES = [
    {"category": "canonical", "artifact": PROMOTED_CANONICAL, "accepted": True, "reasons": []},
    {"category": "skill", "artifact": HELD_SKILL, "accepted": False,
     "reasons": ["evaluator adversarial abaixo do corte"]},
    {"category": "exercise", "artifact": PROMOTED_EXERCISE, "accepted": True, "reasons": []},
]
CLS = [
    {"pattern": "X", "verdict": "Missing",
     "evidence": [{"file": "docs/canonical/y.md", "line": 3, "quote": "q"}]},
    {"pattern": "E1", "verdict": "Exists", "evidence": [{"file": "a.py", "line": 1}]},
    {"pattern": "B1", "verdict": "Better"},
]


def _manifest():
    return am.build_manifest("pkg", "2026-09-15", CLS, OUTCOMES,
                             planned_categories={"canonical", "skill", "exercise"})


def test_build_manifest_schema_and_counts():
    m = _manifest()
    assert m["meta"] == {"type": "artifact-manifest", "date": "2026-09-15", "source_slug": "pkg",
                         "classification_file": "docs/analysis/pkg/pkg-classification.yaml"}
    assert m["gate"]["artifacts_count"] == {"canonical_docs": 1, "skills": 1,
                                            "exercises": 1, "examples": 0}
    assert m["gate"]["phase4_complete"] is True


def test_build_manifest_records_status_and_hold_reasons():
    m = _manifest()
    [canonical] = m["artifacts"]["canonical_docs"]
    assert canonical["status"] == am.STATUS_PROMOTED and canonical["priority"] == "P0"
    [skill] = m["artifacts"]["skills"]
    assert skill["status"] == am.STATUS_QUARANTINED
    assert skill["quarantine_path"].startswith("docs/analysis/pkg/proposed/")
    assert skill["reasons"] == ["evaluator adversarial abaixo do corte"]
    [exercise] = m["artifacts"]["exercises"]
    assert exercise["status"] == am.STATUS_PROMOTED


def test_build_manifest_skipped_rows_from_verdicts():
    m = _manifest()
    [exists_row] = m["skipped"]["already_exists"]
    assert exists_row["pattern"] == "E1" and "a.py:1" in exists_row["evidence"]
    [better_row] = m["skipped"]["better_implementation"]
    assert better_row["pattern"] == "B1" and "Better Implementation" in better_row["reason"]


def test_not_applicable_rows_when_categories_unplanned():
    rows = am.not_applicable_rows(set())
    assert {r["artifact_type"] for r in rows} == {"skills", "exercises"}
    assert am.not_applicable_rows({"canonical", "skill", "exercise"}) == []


def test_manifest_yaml_round_trips():
    m = _manifest()
    assert yaml.safe_load(am.manifest_yaml(m)) == m


def test_manifest_md_frontmatter_is_analysis_compliant():
    md = am.manifest_md(_manifest())
    assert md.startswith("---\n")
    assert "type: analysis" in md
    assert "date: '2026-09-15'" in md or "date: 2026-09-15" in md
    assert "aliases:" in md and "relates-to:" in md


def test_manifest_md_carries_summary_and_integration_map():
    md = am.manifest_md(_manifest())
    assert "## Summary" in md and "## Integration Map" in md and "## Skipped" in md
    assert "docs/canonical/x.md" in md
    assert "quarentena" in md                      # the held artifact is flagged for review
    assert "E1" in md and "B1" in md               # skipped patterns surface in the .md


def test_manifest_md_empty_skipped_is_graceful():
    m = am.build_manifest("pkg", "2026-09-15", [{"pattern": "X", "verdict": "Missing"}],
                          OUTCOMES[:1], planned_categories={"canonical", "skill", "exercise"})
    md = am.manifest_md(m)
    assert "_(nenhum padrão ignorado)_" in md
