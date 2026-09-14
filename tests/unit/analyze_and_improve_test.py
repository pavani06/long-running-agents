#!/usr/bin/env python3
"""Unit tests for the analyze-and-improve control plane's pure logic (no network).

Covers the functions the Etapa 0 DoD names — frontmatter parsing / marker,
stateless diff (queue), git-target selection (delta scan), section chunking, the
floor distribution, and the incremental index merge.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

from analysis_queue import Pending, is_pending, pending_from_texts  # noqa: E402
from chunking import Section, split_sections, strip_frontmatter  # noqa: E402
from deltascan import DEFAULT_TARGETS, under_targets  # noqa: E402
from embed import MAX_INPUT_CHARS, cap_input  # noqa: E402
from floor import REPO_FLOOR, cosine, distribution  # noqa: E402
from frontmatter import (mark_analyzed, parse_frontmatter,  # noqa: E402
                         read_analyzed, set_analyzed)
from index_store import (Record, merge_index, records_for,  # noqa: E402
                         select_to_embed, text_hash)

HIGH = (
    '---\n'
    'title: "A Great Talk"\n'
    'video_id: "vid123"\n'
    'deep_dive: "high"\n'
    'tags: ["evals"]\n'
    '---\n'
    '\n# Body\ntext\n'
)
HIGH_ANALYZED = (
    '---\n'
    'title: "Done"\n'
    'video_id: "vid999"\n'
    'deep_dive: "high"\n'
    'analyzed: "docs/analysis/2026-01-01-done/"\n'
    '---\n'
)
LOW = '---\ntitle: "Meh"\nvideo_id: "vidlow"\ndeep_dive: "low"\n---\n'


# ── frontmatter parsing + analyzed marker ─────────────────────────────────
def test_parse_frontmatter_json_values():
    fm = parse_frontmatter(HIGH)
    assert fm["deep_dive"] == "high"
    assert fm["video_id"] == "vid123"
    assert fm["tags"] == ["evals"]


def test_parse_frontmatter_no_block():
    assert parse_frontmatter("no frontmatter here") == {}


def test_read_analyzed():
    assert read_analyzed(HIGH) is None
    assert read_analyzed(HIGH_ANALYZED) == "docs/analysis/2026-01-01-done/"


def test_set_analyzed_inserts_before_close():
    out = set_analyzed(HIGH, "docs/analysis/2026-02-02-slug/")
    assert 'analyzed: "docs/analysis/2026-02-02-slug/"' in out
    assert read_analyzed(out) == "docs/analysis/2026-02-02-slug/"
    # body preserved, exactly one closing --- consumed, marker inside the block
    assert out.count("\n---") == 1
    assert "# Body" in out and "text" in out


def test_set_analyzed_replaces_existing():
    out = set_analyzed(HIGH_ANALYZED, "docs/analysis/new/")
    assert read_analyzed(out) == "docs/analysis/new/"
    assert out.count("analyzed:") == 1


def test_set_analyzed_noop_without_frontmatter():
    assert set_analyzed("plain text", "x") == "plain text"


def test_mark_analyzed_writes_and_is_idempotent(tmp_path):
    f = tmp_path / "e.md"
    f.write_text(HIGH, encoding="utf-8")
    assert mark_analyzed(f, "docs/analysis/s/") is True
    assert mark_analyzed(f, "docs/analysis/s/") is False  # no change second time
    assert read_analyzed(f.read_text(encoding="utf-8")) == "docs/analysis/s/"


# ── stateless queue diff ──────────────────────────────────────────────────
def test_is_pending():
    assert is_pending(parse_frontmatter(HIGH)) is True
    assert is_pending(parse_frontmatter(HIGH_ANALYZED)) is False   # analyzed
    assert is_pending(parse_frontmatter(LOW)) is False             # not high


def test_pending_from_texts_filters_and_sorts():
    items = [("b.md", HIGH), ("a.md", HIGH), ("c.md", HIGH_ANALYZED), ("d.md", LOW)]
    pending = pending_from_texts(items)
    assert [p.file for p in pending] == ["a.md", "b.md"]      # sorted, only pending
    assert pending[0] == Pending(file="a.md", video_id="vid123", title="A Great Talk")


# ── git delta-scan target selection ───────────────────────────────────────
def test_under_targets_keeps_only_target_md():
    paths = [
        "docs/canonical/x.md",
        "docs/decisions/0001-y.md",
        "curriculum/01-intro/lesson.md",
        ".opencode/skills/foo/SKILL.md",
        "docs/canonical/z.txt",      # not md
        "scripts/other.py",          # not a target dir
        "README.md",                 # root, not a target dir
    ]
    got = under_targets(paths)
    assert got == [
        ".opencode/skills/foo/SKILL.md",
        "curriculum/01-intro/lesson.md",
        "docs/canonical/x.md",
        "docs/decisions/0001-y.md",
    ]


def test_under_targets_dedupes():
    assert under_targets(["docs/canonical/a.md", "docs/canonical/a.md"]) == ["docs/canonical/a.md"]


def test_default_targets_shape():
    assert "docs/canonical/" in DEFAULT_TARGETS
    assert ".opencode/skills/" in DEFAULT_TARGETS


# ── embed input cap (guards the 8192-token embedding limit) ───────────────
def test_cap_input_truncates_long_and_keeps_short():
    assert cap_input("short") == "short"
    long = "x" * (MAX_INPUT_CHARS + 5000)
    assert len(cap_input(long)) == MAX_INPUT_CHARS
    assert cap_input(long) == long[:MAX_INPUT_CHARS]


# ── chunking by heading ───────────────────────────────────────────────────
DOC = (
    "---\ntitle: t\ntags: []\n---\n"
    "Intro preamble.\n\n"
    "# One\nalpha\n\n"
    "## Two\nbeta\n\n"
    "# Three\ngamma\n"
)


def test_strip_frontmatter():
    assert strip_frontmatter(DOC).startswith("Intro preamble.")
    assert "title: t" not in strip_frontmatter(DOC)
    assert strip_frontmatter("no fm") == "no fm"


def test_split_sections_headings_and_preamble():
    secs = split_sections(DOC)
    assert [s.heading for s in secs] == ["", "One", "Two", "Three"]
    assert [s.level for s in secs] == [0, 1, 2, 1]
    assert secs[0].text == "Intro preamble."
    assert secs[1].text == "# One\nalpha"


def test_split_sections_ignores_headings_in_code_fence():
    text = "# Real\ncode below\n\n```python\n# not a heading\nx = 1\n```\nafter\n"
    secs = split_sections(text)
    assert [s.heading for s in secs] == ["Real"]         # only one section
    assert "# not a heading" in secs[0].text             # fenced line preserved


def test_split_sections_empty():
    assert split_sections("---\ntitle: t\n---\n") == []


# ── floor distribution (pure math) ────────────────────────────────────────
def test_cosine_bounds():
    assert abs(cosine([1.0, 0.0], [1.0, 0.0]) - 1.0) < 1e-9
    assert abs(cosine([1.0, 0.0], [0.0, 1.0])) < 1e-9
    assert abs(cosine([1.0, 0.0], [2.0, 0.0]) - 1.0) < 1e-9   # scale-invariant


def test_distribution_shape_and_order():
    vecs = [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]]
    d = distribution(vecs)
    assert d["pairs"] == 3
    assert d["min"] <= d["p50"] <= d["max"]


def test_distribution_empty():
    assert distribution([[1.0, 0.0]]) == {}                   # no pairs
    assert 0.0 < REPO_FLOOR < 1.0


# ── incremental index merge ───────────────────────────────────────────────
FILE_A = "# H1\naaa\n\n## H2\nbbb\n"


def test_records_for_ids_stable_and_hashed():
    recs = records_for("docs/canonical/a.md", FILE_A)
    assert [r.id for r in recs] == ["docs/canonical/a.md#1-h1", "docs/canonical/a.md#2-h2"]
    assert all(r.hash == text_hash(r.text) for r in recs)


def test_records_for_duplicate_headings_get_ordinals():
    recs = records_for("p.md", "# Dup\nx\n\n# Dup\ny\n")
    assert [r.id for r in recs] == ["p.md#1-dup", "p.md#1-dup-1"]


def test_select_to_embed_new_and_changed_only():
    recs = records_for("docs/canonical/a.md", FILE_A)
    empty: dict = {"records": {}}
    assert select_to_embed(empty, recs) == recs               # all new
    # index already has the first record with the same hash -> only second selected
    idx = {"records": {recs[0].id: {"hash": recs[0].hash, "vector": [1.0]}}}
    assert select_to_embed(idx, recs) == [recs[1]]


def test_merge_index_reuses_unchanged_vectors_and_drops_deleted():
    recs = records_for("docs/canonical/a.md", FILE_A)
    # start: both records embedded
    base = merge_index({"records": {}}, {"docs/canonical/a.md": recs}, [],
                       {recs[0].id: [1.0], recs[1].id: [2.0]})
    assert base["records"][recs[0].id]["vector"] == [1.0]

    # re-run: same file, only re-embed the first record; second reuses stored vector
    again = merge_index(base, {"docs/canonical/a.md": recs}, [], {recs[0].id: [9.0]})
    assert again["records"][recs[0].id]["vector"] == [9.0]     # refreshed
    assert again["records"][recs[1].id]["vector"] == [2.0]     # reused, not lost


def test_merge_index_keeps_untouched_files():
    other = {"records": {"other.md#1-x": {"path": "docs/canonical/other.md",
                                          "heading": "x", "level": 1,
                                          "hash": "h", "vector": [7.0]}}}
    recs = records_for("docs/canonical/a.md", FILE_A)
    merged = merge_index(other, {"docs/canonical/a.md": recs}, [],
                         {recs[0].id: [1.0], recs[1].id: [2.0]})
    assert "other.md#1-x" in merged["records"]                 # untouched file survives


def test_merge_index_drops_deleted_path():
    other = {"records": {"gone.md#1-x": {"path": "docs/canonical/gone.md",
                                         "heading": "x", "level": 1,
                                         "hash": "h", "vector": [7.0]}}}
    merged = merge_index(other, {}, ["docs/canonical/gone.md"], {})
    assert merged["records"] == {}
