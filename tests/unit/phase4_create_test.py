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


def test_intended_destination_is_the_canonical_write_target():
    # This is now WHERE F4 writes on the proposal branch (promotion = human merge).
    assert f4.intended_destination(PATTERN) == "docs/canonical/idempotent-diff-pipeline.md"


def _artifact(**over):
    base = dict(slug="s", source_file="s--v.md", video_id="v", pattern=PATTERN,
                verdict="Missing", evidence=[], creation={"title": "X", "body": "B"},
                last_updated="2026-09-15")
    base.update(over)
    return f4.proposed_artifact(**base)


def test_proposed_artifact_is_canonical_type_with_provenance():
    art = _artifact(evidence=[{"file": "x", "line": 1, "quote": "q"}],
                    creation={"title": "Proposed X", "body": "## Problema\n..."})
    for k in ("source", "slug", "video_id", "pattern", "phase3_verdict", "evidence",
              "intended_destination", "title", "content", "problem", "mechanism", "last_updated"):
        assert k in art
    assert art["type"] == "canonical"                      # the file IS the canonical artifact
    assert art["phase3_verdict"] == "Missing"
    assert art["intended_destination"] == "docs/canonical/idempotent-diff-pipeline.md"


def test_render_markdown_is_a_valid_canonical_doc():
    art = _artifact(creation={"title": "X", "body": "BODY-CONTENT"})
    md = f4.render_markdown(art)
    assert md.startswith("---\n")
    assert "type: canonical" in md                         # Check 1: type present
    assert "aliases:" in md and "- idempotent diff pipeline" in md   # Check 12: non-empty
    assert "relates-to: []" in md                          # Check 11: present (empty, uncurated)
    assert "last_updated: '2026-09-15'" in md or "last_updated: 2026-09-15" in md
    assert "sources:" in md
    assert "**Status:**" not in md                         # no transient lifecycle state — Git represents it
    assert "BODY-CONTENT" in md


def test_render_markdown_body_is_link_free():
    # docs/canonical/ CI flags raw md links (Check 5) and broken wikilinks (Check 6);
    # the template must not introduce either around the model body.
    art = _artifact(creation={"title": "T", "body": "prose only"})
    md = f4.render_markdown(art)
    assert "](" not in md.split("BODY", 1)[0]              # no markdown links in our scaffold
    assert "[[" not in md                                   # no wikilinks in our scaffold


def test_destination_path_is_the_canonical_target(tmp_path):
    p = f4.destination_path(tmp_path, PATTERN)
    rel = p.resolve().relative_to(tmp_path.resolve()).as_posix()
    assert rel == "docs/canonical/idempotent-diff-pipeline.md"


def test_assert_canonical_target_rejects_non_canonical():
    with pytest.raises(ValueError):
        f4._assert_canonical_target(Path("/repo/docs/analysis/s/x.md"), Path("/repo"),
                                    "docs/analysis/s/x.md")


def test_write_proposed_writes_the_canonical_target(tmp_path):
    art = _artifact()
    rel = f4.write_proposed(tmp_path, art, "s", PATTERN)
    # creation writes the canonical artifact at its destination (on the branch); promotion
    # to main is the human PR merge, not this write.
    assert rel == "docs/canonical/idempotent-diff-pipeline.md"
    assert (tmp_path / rel).is_file()
    assert not (tmp_path / "docs" / "analysis").exists()   # no leftover proposed/ path
