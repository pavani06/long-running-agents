#!/usr/bin/env python3
"""Unit tests for the x-connections pipeline's pure logic (no network)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "x-connections"))

# Issue #269: sibling pipelines ship same-basename modules (naming, store,
# glm, ...); in a single pytest process the first import wins in sys.modules.
# Purge pipeline-local names so the imports below resolve from this file's dir.
for _mod in ("annotate_thin", "bookmarks", "cluster", "corpus", "embed",
             "extracts_io", "fetch", "fm", "frontmatter_io", "gitio", "glm",
             "graph", "label", "moc", "naming", "oauth", "pipeline", "projects",
             "rank", "render", "serpapi", "store", "taxonomy", "thin", "youtube"):
    sys.modules.pop(_mod, None)

from extracts_io import Extract, embed_text, parse_frontmatter  # noqa: E402
from frontmatter_io import set_relates_to, wikilink  # noqa: E402
from graph import build_edges, cosine_unit, distribution, neighbors  # noqa: E402

IDS = ["A", "B", "C"]
VECS = [[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]]  # A~B, C apart


# ── graph (generic, mirrors youtube-connections) ──────────────────────────
def test_cosine_unit():
    assert abs(cosine_unit([1.0, 0.0], [1.0, 0.0]) - 1.0) < 1e-9
    assert abs(cosine_unit([1.0, 0.0], [0.0, 1.0])) < 1e-9


def test_build_edges_topk_symmetric():
    edges = build_edges(IDS, VECS, k=1)
    pairs = {(e.a, e.b) for e in edges}
    assert ("A", "B") in pairs and ("B", "C") in pairs and ("A", "C") not in pairs
    assert edges[0].weight >= edges[-1].weight


def test_build_edges_floor_drops_weak():
    pairs = {(e.a, e.b) for e in build_edges(IDS, VECS, k=2, floor=0.5)}
    assert ("A", "B") in pairs
    assert all(p != ("B", "C") for p in pairs)


def test_neighbors_symmetric():
    nb = neighbors(build_edges(IDS, VECS, k=1))
    assert "B" in [n for n, _ in nb["A"]] and "A" in [n for n, _ in nb["B"]]


def test_distribution_shape():
    d = distribution(IDS, VECS)
    assert d["pairs"] == 3 and d["min"] <= d["p50"] <= d["max"]


# ── frontmatter surgery ───────────────────────────────────────────────────
EXTRACT = (
    '---\n'
    'title: "T"\n'
    'status_id: "1798557144580735156"\n'
    'topic: "Tema"\n'
    'summary: "Resumo aqui"\n'
    'key_points: ["ponto um", "ponto dois"]\n'
    'tags: ["evals"]\n'
    '---\n'
    '\n'
    '# T\n\nbody stays\n'
)


def test_set_relates_to_inserts_and_preserves():
    out = set_relates_to(EXTRACT, ["[[extracts/x/bookmarks/x|X]]"])
    assert 'relates-to: ["[[extracts/x/bookmarks/x|X]]"]' in out
    assert 'title: "T"' in out and 'status_id: "1798557144580735156"' in out
    assert "# T\n\nbody stays" in out


def test_set_relates_to_replaces_existing():
    twice = set_relates_to(set_relates_to(EXTRACT, ["[[a|A]]"]), ["[[b|B]]"])
    assert twice.count("relates-to:") == 1
    assert "[[b|B]]" in twice and "[[a|A]]" not in twice


def test_wikilink_format():
    assert wikilink("2026-09-12-h-x--1798557144580735156.md", "My Title") == \
        "[[extracts/x/bookmarks/2026-09-12-h-x--1798557144580735156|My Title]]"


# ── extracts io ───────────────────────────────────────────────────────────
def test_parse_frontmatter_json_values():
    fm = parse_frontmatter(EXTRACT)
    assert fm["topic"] == "Tema" and fm["key_points"] == ["ponto um", "ponto dois"]


def test_embed_text_composition():
    e = Extract(status_id="1", title="Title", file="f.md", topic="Tema",
                summary="Resumo denso", key_points=["p1", "p2"], tags=["evals"])
    t = embed_text(e)
    assert "Tema" in t and "Resumo denso" in t and "p1" in t and "evals" in t


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
