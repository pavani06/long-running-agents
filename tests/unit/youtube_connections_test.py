#!/usr/bin/env python3
"""Unit tests for the youtube-connections pipeline's pure logic (no network)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "youtube-connections"))

from extracts_io import Extract, embed_text, parse_frontmatter  # noqa: E402
from frontmatter_io import set_relates_to, wikilink  # noqa: E402
from graph import build_edges, cosine_unit, distribution, neighbors  # noqa: E402

# 3 vectors: A and B nearly identical, C orthogonal-ish.
IDS = ["A", "B", "C"]
VECS = [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]]


# ── graph ───────────────────────────────────────────────────────────────
def test_cosine_unit():
    assert abs(cosine_unit([1.0, 0.0], [1.0, 0.0]) - 1.0) < 1e-9
    assert abs(cosine_unit([1.0, 0.0], [0.0, 1.0])) < 1e-9


def test_build_edges_topk_symmetric():
    edges = build_edges(IDS, VECS, k=1)
    pairs = {(e.a, e.b) for e in edges}
    assert ("A", "B") in pairs        # A and B are mutual nearest
    assert ("B", "C") in pairs        # C's nearest is B
    assert ("A", "C") not in pairs
    # weights sorted desc
    assert edges[0].weight >= edges[-1].weight


def test_build_edges_floor_drops_weak():
    edges = build_edges(IDS, VECS, k=2, floor=0.5)
    pairs = {(e.a, e.b) for e in edges}
    assert ("A", "B") in pairs         # ~0.996 kept
    assert all(p != ("B", "C") for p in pairs)  # weak link dropped by floor


def test_neighbors_symmetric():
    nb = neighbors(build_edges(IDS, VECS, k=1))
    assert "B" in [n for n, _ in nb["A"]]
    assert "A" in [n for n, _ in nb["B"]]


def test_distribution_shape():
    d = distribution(IDS, VECS)
    assert d["pairs"] == 3
    assert d["min"] <= d["p50"] <= d["max"]


# ── frontmatter surgery ───────────────────────────────────────────────────
EXTRACT = (
    '---\n'
    'title: "T"\n'
    'video_id: "kCc8FmEb1nY"\n'
    'tags: ["evals"]\n'
    '---\n'
    '\n'
    '# T\n\nbody stays\n'
)


def test_set_relates_to_inserts_and_preserves():
    out = set_relates_to(EXTRACT, ["[[extracts/youtube/ai-learning/x|X]]"])
    assert 'relates-to: ["[[extracts/youtube/ai-learning/x|X]]"]' in out
    assert 'title: "T"' in out and 'video_id: "kCc8FmEb1nY"' in out
    assert "# T\n\nbody stays" in out  # body untouched


def test_set_relates_to_replaces_existing():
    once = set_relates_to(EXTRACT, ["[[a|A]]"])
    twice = set_relates_to(once, ["[[b|B]]"])
    assert twice.count("relates-to:") == 1
    assert "[[b|B]]" in twice and "[[a|A]]" not in twice


def test_wikilink_format():
    assert wikilink("2026-09-11-x--kCc8FmEb1nY.md", "My Title") == \
        "[[extracts/youtube/ai-learning/2026-09-11-x--kCc8FmEb1nY|My Title]]"


# ── extracts io ───────────────────────────────────────────────────────────
def test_parse_frontmatter_json_values():
    fm = parse_frontmatter(EXTRACT)
    assert fm["title"] == "T"
    assert fm["tags"] == ["evals"]


def test_embed_text_composition():
    e = Extract(video_id="v", title="Title", file="f.md", thesis="Thesis here",
                concepts=["c1", "c2"], claims=["do x"])
    t = embed_text(e)
    assert "Title" in t and "Thesis here" in t and "c1" in t and "do x" in t


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
