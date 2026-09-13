#!/usr/bin/env python3
"""Themes/clusters layer for the X bookmarks corpus.

Detects communities in the semantic graph (connections.json), labels each
(deterministic top-tags + optional GLM polish), and writes:
  - themes.json (canonical clusters),
  - a `theme` field into each extract's frontmatter (Obsidian filter/color),
  - one MOC note per theme (extracts/x/bookmarks/themes/<slug>.md).
Derives everything from committed artifacts — never re-embeds.

`thin` extracts (no substance: no key_points + tweet-grounded) are EXCLUDED from
the graph so they don't collapse into a junk theme; they surface separately in
the digest (Fase 5) as a "to investigate" bucket.

Environment:
  ZAI_API_KEY        GLM key for label polish (optional; auto labels if absent)
  THEME_RESOLUTION   greedy-modularity resolution (default 1.0)
  THEME_DRY_RUN      "1" to log community count/sizes only, writing nothing

Exit: 0 = success (incl. dry-run, GLM-absent, per-cluster GLM fallback);
      1 = red (missing connections.json, networkx failure, invalid ZAI key).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cluster  # noqa: E402
from corpus import load_edges, load_extracts  # noqa: E402
from fm import update_theme  # noqa: E402
from glm import AuthError, polish_label  # noqa: E402
from label import auto_label, slug  # noqa: E402
from moc import build_moc  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACTS_DIR = REPO_ROOT / "extracts" / "x" / "bookmarks"
CONNECTIONS_JSON = EXTRACTS_DIR / "connections.json"
THEMES_JSON = EXTRACTS_DIR / "themes.json"
MOC_DIR = EXTRACTS_DIR / "themes"
DEFAULT_RESOLUTION = 1.0


def summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def run(resolution: float, dry_run: bool, zai_key: str | None) -> int:
    if not CONNECTIONS_JSON.exists():
        summary(f"RED: {CONNECTIONS_JSON} not found (run connections first)")
        return 1

    extracts = load_extracts(EXTRACTS_DIR)
    # Exclude thin extracts from the graph (they'd form a junk theme).
    nodes = sorted(sid for sid, e in extracts.items() if not e.thin)
    thin_n = len(extracts) - len(nodes)
    nodeset = set(nodes)
    edges = [(a, b, w) for a, b, w in load_edges(CONNECTIONS_JSON)
             if a in nodeset and b in nodeset]
    summary(f"{len(nodes)} clusterable extracts (excluded {thin_n} thin); {len(edges)} edges")
    if len(nodes) < 2:
        summary("fewer than 2 clusterable extracts — nothing to cluster")
        return 0

    try:
        comms = cluster.communities(nodes, edges, resolution=resolution)
    except Exception as e:  # networkx failure
        summary(f"RED: clustering failed: {e}")
        return 1

    summary(f"{len(comms)} communities @resolution={resolution}; sizes={cluster.sizes(comms)}")
    if dry_run:
        summary("dry-run: not writing themes.json / frontmatter / MOCs")
        return 0

    themes = []
    bad_key = False
    polished = 0
    for i, members in enumerate(comms, 1):
        auto = auto_label(members, extracts)
        theme = {"id": f"t{i:02d}", "size": len(members), "members": members, **auto,
                 "label_llm": None, "description": ""}
        if zai_key and not bad_key:
            titles = [extracts[m].title for m in members if m in extracts]
            summaries = [extracts[m].summary for m in members if m in extracts]
            try:
                pol = polish_label(titles, summaries, auto["label_auto"], zai_key)
            except AuthError as e:
                summary(f"WARNING: {e} — falling back to auto labels")
                bad_key = True
                pol = None
            if pol:
                theme["label_llm"] = pol["name"]
                theme["description"] = pol["description"]
                polished += 1
        themes.append(theme)

    used: dict[str, int] = {}
    for t in themes:
        name = t["label_llm"] or t["label_auto"]
        base = slug(name)
        used[base] = used.get(base, 0) + 1
        t["slug"] = base if used[base] == 1 else f"{base}-{used[base]}"
        t["name"] = name

    changed = 0
    for t in themes:
        for sid in t["members"]:
            e = extracts.get(sid)
            if e and update_theme(EXTRACTS_DIR / e.file, t["name"]):
                changed += 1

    MOC_DIR.mkdir(parents=True, exist_ok=True)
    for old in MOC_DIR.glob("*.md"):
        old.unlink()
    for t in themes:
        (MOC_DIR / f"{t['slug']}.md").write_text(build_moc(t, t["members"], extracts), encoding="utf-8")

    THEMES_JSON.write_text(json.dumps(
        {"resolution": resolution, "count": len(themes), "excluded_thin": thin_n, "themes": themes},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary(f"wrote {len(themes)} themes ({polished} GLM-polished), "
            f"theme on {changed} extracts, {len(themes)} MOC notes")
    return 1 if bad_key else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--resolution", type=float,
                    default=float(os.environ.get("THEME_RESOLUTION", DEFAULT_RESOLUTION)))
    ap.add_argument("--dry-run", action="store_true", default=os.environ.get("THEME_DRY_RUN") == "1")
    args = ap.parse_args()
    return run(args.resolution, args.dry_run, os.environ.get("ZAI_API_KEY"))


if __name__ == "__main__":
    raise SystemExit(main())
