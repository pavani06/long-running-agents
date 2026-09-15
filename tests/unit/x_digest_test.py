#!/usr/bin/env python3
"""Unit tests for the x-digest pipeline's pure logic (no network)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "x-digest"))

# Issue #269: sibling pipelines ship same-basename modules (naming, store,
# glm, ...); in a single pytest process the first import wins in sys.modules.
# Purge pipeline-local names so the imports below resolve from this file's dir.
for _mod in ("annotate_thin", "bookmarks", "cluster", "corpus", "embed",
             "extracts_io", "fetch", "fm", "frontmatter_io", "gitio", "glm",
             "graph", "label", "moc", "naming", "oauth", "pipeline", "projects",
             "rank", "render", "serpapi", "store", "taxonomy", "thin", "youtube"):
    sys.modules.pop(_mod, None)

from corpus import Extract, parse_frontmatter  # noqa: E402
from projects import parse_projects, projects_brief  # noqa: E402
from rank import read_order  # noqa: E402
from pipeline import scope_for, _chips  # noqa: E402
import render  # noqa: E402


def _e(sid, **kw):
    return Extract(status_id=sid, title=kw.pop("title", f"T{sid}"), file=f"f-{sid}.md", **kw)


# ── projects ──────────────────────────────────────────────────────────────
PROJECTS_MD = (
    "# projects\n\n## Tier 1\n"
    "- **long-running-agents** — Currículo + pipelines.\n"
    "- **chatshop-io/commerce** — Serviço. _[refinar: 1 linha]_\n"
    "## Tier 2\n- **obsidian-eval** — CLI do vault.\n"
    "## Teses / temas não-repo\n- **Ciclismo / performance** — treino.\n"
)


def test_parse_projects_tiers_and_theses():
    p = parse_projects(PROJECTS_MD)
    by = {x["name"]: x for x in p}
    assert by["long-running-agents"]["tier"] == 1
    assert by["obsidian-eval"]["tier"] == 2
    assert by["Ciclismo / performance"]["tier"] is None      # tese
    assert by["chatshop-io/commerce"]["desc"] == "Serviço."   # _[refinar]_ stripped


def test_projects_brief_tier_ordered():
    brief = projects_brief(parse_projects(PROJECTS_MD))
    assert brief.index("long-running-agents") < brief.index("obsidian-eval")
    assert "Ciclismo" in brief


# ── rank ────────────────────────────────────────────────────────────────
def test_read_order_by_revisit_then_recency_excludes_thin():
    items = [
        _e("1", revisit="low", created_at="2026-09-13T00:00:00Z"),
        _e("2", revisit="high", created_at="2026-09-01T00:00:00Z"),
        _e("3", revisit="high", created_at="2026-09-10T00:00:00Z"),
        _e("4", revisit="high", created_at="2026-09-12T00:00:00Z", thin=True),  # excluded
    ]
    order = read_order(items, n=5)
    assert [e.status_id for e in order] == ["3", "2", "1"]   # high(recent) > high(old) > low; thin gone


# ── render ────────────────────────────────────────────────────────────────
def test_build_digest_empty_day():
    md = render.build_digest(date="2026-09-13", mode="daily", order=[], theme_blocks=[], thin=[], total=0)
    assert "Nenhum bookmark novo" in md and "## Leia nesta ordem" not in md


def test_render_theme_with_synth_and_fallback():
    m = [_e("1", title="A", summary="resumo a"), _e("2", title="B", summary="resumo b")]
    synth = {"synthesis": "O argumento central.", "non_obvious": "O ponto não-óbvio.",
             "actions": ["Ação no projeto X"]}
    out = "\n".join(render.render_theme("Tema Z", synth, m, chips=[]))
    assert "## Tema Z  (2)" in out and "O argumento central." in out
    assert "> **Não-óbvio:** O ponto não-óbvio." in out and "Ações:" in out
    # fallback when no synth
    fb = "\n".join(render.render_theme("Tema Z", None, m, chips=[]))
    assert "Itens:" in fb and "resumo a" in fb


def test_render_thin_bucket():
    thin = [_e("9", title="Link X", handle="h", links=["https://ex.com/a"], url="https://x.com/h/status/9", thin=True)]
    out = "\n".join(render.render_thin(thin))
    assert "## A investigar (1)" in out and "https://ex.com/a" in out and "[tweet](https://x.com/h/status/9)" in out


def test_build_digest_full_shape():
    m = [_e("1", title="A", summary="ra", revisit="high", created_at="2026-09-12T00:00:00Z", theme="Tz")]
    thin = [_e("2", title="L", handle="h", url="u", thin=True)]
    blocks = [{"name": "Tz", "synth": {"synthesis": "arg", "non_obvious": "", "actions": []},
               "members": m, "chips": []}]
    md = render.build_digest(date="2026-09-13", mode="bootstrap", order=m,
                             theme_blocks=blocks, thin=thin, total=2)
    assert "bootstrap do acervo" in md and "## Leia nesta ordem" in md
    assert "## Tz  (1)" in md and "## A investigar (1)" in md


# ── scope (guards the daily/extracted bug) + chips ─────────────────────────
def test_scope_for_daily_uses_extracted():
    items = [_e("1", extracted="2026-09-13"), _e("2", extracted="2026-09-12"), _e("3", extracted="")]
    daily = scope_for(items, "daily", "2026-09-13")
    assert [e.status_id for e in daily] == ["1"]                 # only today's extract
    assert len(scope_for(items, "bootstrap", "2026-09-13")) == 3  # all


def test_chips_cross_theme_nonthin_dedup():
    a = _e("1", theme="Tx"); b = _e("2", theme="Tx")
    x = _e("10", theme="Ty"); y = _e("11", theme="Tz"); z = _e("12", theme="Tx")  # same theme, excluded
    t = _e("13", theme="Ty", thin=True)                                            # thin, excluded
    by_id = {e.status_id: e for e in (a, b, x, y, z, t)}
    neighbors = {"1": ["10", "12", "13"], "2": ["10", "11"]}       # 10 dup across members
    chips = _chips([a, b], neighbors, by_id, limit=5)
    ids = [c.status_id for c in chips]
    assert ids == ["10", "11"]        # 10 (dedup), 11; 12 same-theme out, 13 thin out


# ── corpus ──────────────────────────────────────────────────────────────
def test_parse_frontmatter():
    fm = parse_frontmatter('---\nstatus_id: "1"\nthin: false\ntags: ["a"]\n---\nbody')
    assert fm["status_id"] == "1" and fm["thin"] is False and fm["tags"] == ["a"]


def _run_all():
    fns = [g for n, g in sorted(globals().items()) if n.startswith("test_") and callable(g)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} passed")


if __name__ == "__main__":
    _run_all()
