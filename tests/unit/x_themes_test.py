#!/usr/bin/env python3
"""Unit tests for the x-themes pipeline's pure logic (needs networkx, no network)."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "x-themes"))

import cluster  # noqa: E402
from corpus import ExtractMeta, load_extracts, parse_frontmatter  # noqa: E402
from fm import set_theme  # noqa: E402
from glm import _parse  # noqa: E402
from label import auto_label, slug  # noqa: E402
from moc import build_moc  # noqa: E402

EXTRACTS = {
    "1": ExtractMeta("1", "Alpha", "2026-01-01-a-x--1.md", tags=["harness-engineering", "evals"], key_points=["k1"], summary="S a"),
    "2": ExtractMeta("2", "Beta", "2026-01-01-b-x--2.md", tags=["harness-engineering"], key_points=["k1", "k2"], summary="S b"),
    "3": ExtractMeta("3", "Gamma", "2026-01-01-c-x--3.md", tags=["harness-engineering", "evals"], key_points=["k1"], summary="S c"),
    "4": ExtractMeta("4", "Delta", "2026-01-01-d-x--4.md", tags=["financas"], key_points=["k3"], summary="S d"),
    "5": ExtractMeta("5", "Epsilon", "2026-01-01-e-x--5.md", tags=["financas"], key_points=["k3"], summary="S e"),
    "6": ExtractMeta("6", "Zeta", "2026-01-01-f-x--6.md", tags=["financas"], key_points=["k3", "k4"], summary="S f"),
}
EDGES = [("1", "2", 0.9), ("2", "3", 0.9), ("1", "3", 0.9),
         ("4", "5", 0.9), ("5", "6", 0.9), ("4", "6", 0.9),
         ("3", "4", 0.2)]


# ── clustering ───────────────────────────────────────────────────────────
def test_two_communities():
    comms = cluster.communities(sorted(EXTRACTS), EDGES, resolution=1.0)
    groups = [set(c) for c in comms]
    assert len(comms) == 2
    assert {"1", "2", "3"} in groups and {"4", "5", "6"} in groups


def test_communities_deterministic():
    assert cluster.communities(sorted(EXTRACTS), EDGES) == cluster.communities(sorted(EXTRACTS), EDGES)


# ── labels ────────────────────────────────────────────────────────────────
def test_auto_label_top_tags():
    lab = auto_label(["1", "2", "3"], EXTRACTS)
    assert lab["top_tags"][0] == "harness-engineering" and "evals" in lab["top_tags"]


def test_slug():
    assert slug("Harness & Context: Engineering!") == "harness-context-engineering"
    assert slug("日本語") == "tema"


# ── frontmatter surgery ───────────────────────────────────────────────────
FM = '---\ntitle: "T"\nstatus_id: "1798557144580735156"\nrelates-to: ["[[x|X]]"]\nthin: false\n---\n\n# T\n\nbody\n'


def test_set_theme_inserts_and_preserves():
    out = set_theme(FM, "Harness Engineering")
    assert 'theme: "Harness Engineering"' in out
    assert 'relates-to: ["[[x|X]]"]' in out and 'thin: false' in out
    assert "# T\n\nbody" in out


def test_set_theme_replaces():
    twice = set_theme(set_theme(FM, "One"), "Two")
    assert twice.count("theme:") == 1 and "Two" in twice and '"One"' not in twice


# ── MOC ────────────────────────────────────────────────────────────────────
def test_build_moc_lists_members():
    theme = {"label_auto": "financas", "label_llm": "Mercado & Finanças",
             "description": "Leitura de mercado.", "top_tags": ["financas"]}
    md = build_moc(theme, ["4", "5", "6"], EXTRACTS)
    assert "# Tema: Mercado & Finanças" in md and "Leitura de mercado." in md
    assert "[[extracts/x/bookmarks/2026-01-01-d-x--4|Delta]]" in md
    assert "## Bookmarks (3)" in md


# ── glm parse + frontmatter parse ─────────────────────────────────────────
def test_glm_parse_fenced():
    body = {"choices": [{"message": {"content": '```json\n{"name":"X","description":"d"}\n```'}}]}
    assert _parse(body) == {"name": "X", "description": "d"}


def test_glm_parse_no_name_returns_none():
    assert _parse({"choices": [{"message": {"content": '{"description":"d"}'}}]}) is None


# ── thin exclusion (corpus reads thin; pipeline filters on it) ──────────────
def test_load_extracts_reads_thin_flag():
    with tempfile.TemporaryDirectory() as d:
        ed = Path(d)
        (ed / "2026-01-01-a-x--1.md").write_text(
            '---\nstatus_id: "1"\ntitle: "A"\nkey_points: ["k"]\ngrounded_in: "article"\nthin: false\n---\n\nx',
            encoding="utf-8")
        (ed / "2026-01-01-b-x--2.md").write_text(
            '---\nstatus_id: "2"\ntitle: "B"\nkey_points: []\ngrounded_in: "tweet"\nthin: true\n---\n\ny',
            encoding="utf-8")
        got = load_extracts(ed)
        assert got["1"].thin is False and got["2"].thin is True
        # this is exactly what pipeline filters on:
        clusterable = sorted(sid for sid, e in got.items() if not e.thin)
        assert clusterable == ["1"]


def _run_all():
    fns = [g for name, g in sorted(globals().items()) if name.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
