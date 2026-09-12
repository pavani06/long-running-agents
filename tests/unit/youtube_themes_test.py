#!/usr/bin/env python3
"""Unit tests for the youtube-themes pipeline's pure logic (needs networkx, no network)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "youtube-themes"))

import cluster  # noqa: E402
from corpus import ExtractMeta, parse_frontmatter  # noqa: E402
from fm import set_theme  # noqa: E402
from glm import _parse  # noqa: E402
from label import auto_label, slug  # noqa: E402
from moc import build_moc  # noqa: E402

EXTRACTS = {
    "a": ExtractMeta("a", "Alpha talk", "2026-01-01-alpha--aaaaaaaaaaa.md", tags=["harness-engineering", "evals"], concepts=["c1"], thesis="Th a"),
    "b": ExtractMeta("b", "Beta talk", "2026-01-01-beta--bbbbbbbbbbb.md", tags=["harness-engineering"], concepts=["c1", "c2"], thesis="Th b"),
    "c": ExtractMeta("c", "Gamma talk", "2026-01-01-gamma--ccccccccccc.md", tags=["harness-engineering", "evals"], concepts=["c1"], thesis="Th c"),
    "d": ExtractMeta("d", "Delta talk", "2026-01-01-delta--ddddddddddd.md", tags=["governanca"], concepts=["c3"], thesis="Th d"),
    "e": ExtractMeta("e", "Epsilon talk", "2026-01-01-eps--eeeeeeeeeee.md", tags=["governanca"], concepts=["c3"], thesis="Th e"),
    "f": ExtractMeta("f", "Zeta talk", "2026-01-01-zeta--fffffffffff.md", tags=["governanca"], concepts=["c3", "c4"], thesis="Th f"),
}
# two strong triangles + one weak bridge
EDGES = [("a", "b", 0.9), ("b", "c", 0.9), ("a", "c", 0.9),
         ("d", "e", 0.9), ("e", "f", 0.9), ("d", "f", 0.9),
         ("c", "d", 0.2)]


# ── clustering ───────────────────────────────────────────────────────────
def test_two_communities():
    comms = cluster.communities(sorted(EXTRACTS), EDGES, resolution=1.0)
    assert len(comms) == 2
    groups = [set(c) for c in comms]
    assert {"a", "b", "c"} in groups
    assert {"d", "e", "f"} in groups


def test_communities_deterministic():
    a = cluster.communities(sorted(EXTRACTS), EDGES)
    b = cluster.communities(sorted(EXTRACTS), EDGES)
    assert a == b  # stable ordering


# ── labels ────────────────────────────────────────────────────────────────
def test_auto_label_top_tags():
    lab = auto_label(["a", "b", "c"], EXTRACTS)
    assert lab["top_tags"][0] == "harness-engineering"  # 3x
    assert "evals" in lab["top_tags"]                     # 2x
    assert "harness-engineering" in lab["label_auto"]


def test_slug():
    assert slug("Harness & Context: Engineering!") == "harness-context-engineering"
    assert slug("日本語") == "tema"


# ── frontmatter surgery ───────────────────────────────────────────────────
FM = '---\ntitle: "T"\nvideo_id: "aaaaaaaaaaa"\nrelates-to: ["[[x|X]]"]\n---\n\n# T\n\nbody\n'


def test_set_theme_inserts_and_preserves():
    out = set_theme(FM, "Harness Engineering")
    assert 'theme: "Harness Engineering"' in out
    assert 'relates-to: ["[[x|X]]"]' in out and 'title: "T"' in out
    assert "# T\n\nbody" in out


def test_set_theme_replaces():
    once = set_theme(FM, "One")
    twice = set_theme(once, "Two")
    assert twice.count("theme:") == 1 and "Two" in twice and '"One"' not in twice


# ── MOC ────────────────────────────────────────────────────────────────────
def test_build_moc_lists_members():
    theme = {"label_auto": "governanca", "label_llm": "Governança de Agentes",
             "description": "Como governar agentes.", "top_tags": ["governanca"]}
    md = build_moc(theme, ["d", "e", "f"], EXTRACTS)
    assert "# Tema: Governança de Agentes" in md
    assert "Como governar agentes." in md
    assert "[[extracts/youtube/ai-learning/2026-01-01-delta--ddddddddddd|Delta talk]]" in md
    assert "## Vídeos (3)" in md


# ── glm parse + frontmatter parse ─────────────────────────────────────────
def test_glm_parse_fenced():
    body = {"choices": [{"message": {"content": '```json\n{"name":"X","description":"d"}\n```'}}]}
    assert _parse(body) == {"name": "X", "description": "d"}


def test_glm_parse_no_name_returns_none():
    body = {"choices": [{"message": {"content": '{"description":"d"}'}}]}
    assert _parse(body) is None


def test_parse_frontmatter():
    fm = parse_frontmatter(FM)
    assert fm["title"] == "T" and fm["relates-to"] == ["[[x|X]]"]


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
