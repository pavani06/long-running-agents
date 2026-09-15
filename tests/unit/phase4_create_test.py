#!/usr/bin/env python3
"""Unit tests for Fase 4 creation (#263 slice). Pure parts + the never-canonical
invariant; no network."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import phase4_create as f4  # noqa: E402
from glm import GLMError  # noqa: E402

PATTERN = {"name": "Idempotent Diff Pipeline", "problem": "reprocessing wastes cost",
           "mechanism": "hash-gated re-embed", "tradeoffs": "staleness window"}


def test_slugify():
    assert f4.slugify("Idempotent Diff Pipeline") == "idempotent-diff-pipeline"
    assert f4.slugify("  A/B  test!! ") == "a-b-test"
    assert f4.slugify("") == "proposta"


def test_build_messages_carries_pattern_and_context():
    msgs = f4.build_messages(PATTERN, "SRC-CONTEXT")
    assert msgs[0]["role"] == "system" and "AUSENTE" in msgs[0]["content"]
    u = msgs[1]["content"]
    assert "Idempotent Diff Pipeline" in u and "hash-gated re-embed" in u and "SRC-CONTEXT" in u


def test_parse_creation_ok():
    assert f4.parse_creation({"title": "T", "body": "B"}) == {"title": "T", "body": "B"}


def test_parse_creation_rejects_empty():
    for bad in ({"title": "", "body": "B"}, {"title": "T", "body": ""}, {"title": "T"}, {}):
        with pytest.raises(GLMError):
            f4.parse_creation(bad)


def test_intended_destination_is_canonical_path_recorded_only():
    assert f4.intended_destination(PATTERN) == "docs/canonical/idempotent-diff-pipeline.md"


def test_proposed_artifact_retains_review_provenance():
    art = f4.proposed_artifact(
        slug="2026-09-11-some-talk", source_file="2026-09-11-some-talk--vid.md",
        video_id="vid", pattern=PATTERN, verdict="Missing",
        evidence=[{"file": "x", "line": 1, "quote": "q"}],
        creation={"title": "Proposed X", "body": "## Problema\n..."})
    # every human-review provenance field present
    for k in ("source", "slug", "video_id", "pattern", "phase3_verdict", "evidence",
              "intended_destination", "title", "content", "problem", "mechanism"):
        assert k in art
    assert art["type"] == "proposed-canonical-doc" and art["status"] == "proposed"
    assert art["phase3_verdict"] == "Missing"
    assert art["intended_destination"].startswith("docs/canonical/")


def test_render_markdown_is_a_proposal_not_canonical():
    art = f4.proposed_artifact(slug="s", source_file="s--v.md", video_id="v", pattern=PATTERN,
                               verdict="Missing", evidence=[],
                               creation={"title": "X", "body": "BODY-CONTENT"})
    md = f4.render_markdown(art)
    assert md.startswith("---\n")
    assert "type: proposed-canonical-doc" in md          # NOT a canonical/analysis type
    assert "PROPOSTA" in md and "não promovida" in md     # explicit non-promotion
    assert "docs/canonical/idempotent-diff-pipeline.md" in md   # intended dest recorded
    assert "BODY-CONTENT" in md


def test_render_markdown_satisfies_monitored_dir_frontmatter():
    # docs/analysis/ is a validate-obsidian MONITORED dir: aliases (present+non-empty,
    # Check 12) and relates-to (present, Check 11) are required even in quarantine.
    art = f4.proposed_artifact(slug="s", source_file="s--v.md", video_id="v", pattern=PATTERN,
                               verdict="Missing", evidence=[], creation={"title": "X", "body": "B"})
    md = f4.render_markdown(art)
    assert "aliases:" in md and "- idempotent diff pipeline" in md   # non-empty alias
    assert "relates-to: []" in md                                    # present, empty (uncurated)


def test_quarantine_path_is_under_proposed(tmp_path):
    p = f4.quarantine_path(tmp_path, "2026-09-11-talk", PATTERN)
    rel = p.resolve().relative_to(tmp_path.resolve()).as_posix()
    assert rel == "docs/analysis/2026-09-11-talk/proposed/idempotent-diff-pipeline.md"


def test_never_canonical_invariant():
    # the guard must refuse any authoritative-layer path
    with pytest.raises(ValueError):
        f4._assert_never_canonical(Path("/repo/docs/canonical/x.md"), Path("/repo"))
    with pytest.raises(ValueError):
        f4._assert_never_canonical(Path("/repo/curriculum/x.md"), Path("/repo"))
    # a path outside proposed/ is also refused
    with pytest.raises(ValueError):
        f4._assert_never_canonical(Path("/repo/docs/analysis/s/x.md"), Path("/repo"))


def test_write_proposed_writes_quarantine_only(tmp_path):
    art = f4.proposed_artifact(slug="s", source_file="s--v.md", video_id="v", pattern=PATTERN,
                               verdict="Missing", evidence=[], creation={"title": "X", "body": "B"})
    rel = f4.write_proposed(tmp_path, art, "s", PATTERN)
    assert rel == "docs/analysis/s/proposed/idempotent-diff-pipeline.md"
    assert (tmp_path / rel).is_file()
    assert not (tmp_path / "docs" / "canonical").exists()   # nothing written to canonical
