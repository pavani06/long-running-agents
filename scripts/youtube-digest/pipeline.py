#!/usr/bin/env python3
"""Digest generator for the YouTube "AI - Learning" corpus.

Groups in-scope extracts by their theme (youtube-themes), synthesizes each theme
with GLM (concrete argument + non-obvious + project-anchored actions), ranks a
"watch in this order" list, and writes a Markdown digest. Derives everything
from committed artifacts (extracts + themes.json + connections.json).

Modes:
  bootstrap   the whole acervo, organized by theme (one-time)
  daily       only videos extracted today (default)

Environment:
  ZAI_API_KEY   GLM key for synthesis (optional; deterministic fallback if absent)

Exit: 0 = success (incl. empty day, GLM-absent/fallback); 1 = red (invalid ZAI key).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

from corpus import (Extract, load_connection_neighbors, load_extracts,  # noqa: E402
                    load_themes)
from glm import AuthError, synthesize  # noqa: E402
from rank import read_order  # noqa: E402
import render  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACTS_DIR = REPO_ROOT / "extracts" / "youtube" / "ai-learning"
DIGESTS_DIR = REPO_ROOT / "digests" / "youtube"
PROJECTS_MD = REPO_ROOT / "digests" / "x" / "projects.md"
TZ = ZoneInfo("America/Sao_Paulo")


def today() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def scope_for(extracts: list[Extract], mode: str, date: str) -> list[Extract]:
    """bootstrap = all; daily = extracts written today (`extracted` field)."""
    if mode == "bootstrap":
        return list(extracts)
    return [e for e in extracts if e.extracted == date]


def _chips(members: list[Extract], neighbors: dict[str, list[str]],
           by_id: dict[str, Extract], *, limit: int = 5) -> list[Extract]:
    """Connection neighbors of a theme's members that sit in OTHER themes."""
    member_ids = {e.video_id for e in members}
    theme = members[0].theme if members else ""
    out: list[Extract] = []
    seen: set[str] = set()
    for e in members:
        for nid in neighbors.get(e.video_id, []):
            n = by_id.get(nid)
            if n and nid not in member_ids and nid not in seen and not n.thin and n.theme != theme:
                seen.add(nid)
                out.append(n)
                if len(out) >= limit:
                    return out
    return out


def run(mode: str, zai_key: str | None) -> int:
    by_id = load_extracts(EXTRACTS_DIR)
    themes = load_themes(EXTRACTS_DIR / "themes.json")
    neighbors = load_connection_neighbors(EXTRACTS_DIR / "connections.json")
    projects = []
    if PROJECTS_MD.exists():
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "x-digest"))
        from projects import parse_projects, projects_brief  # noqa: E402
        projects = parse_projects(PROJECTS_MD.read_text(encoding="utf-8"))
    pbrief = projects_brief(projects)
    date = today()

    scope = scope_for(list(by_id.values()), mode, date)

    thin = [e for e in scope if e.thin]
    live = [e for e in scope if not e.thin]
    summary(f"{mode}: {len(scope)} in scope ({len(live)} themed, {len(thin)} thin)")

    # group by theme, ordered by themes.json (largest-first)
    theme_order = [t["name"] for t in themes]
    by_theme: dict[str, list[Extract]] = {}
    for e in live:
        by_theme.setdefault(e.theme or "Sem tema", []).append(e)
    ordered_names = [n for n in theme_order if n in by_theme] + \
                    [n for n in by_theme if n not in theme_order]

    n_read = 5 if mode == "bootstrap" else 3
    order = read_order(live, n=n_read)

    theme_blocks = []
    bad_key = False
    polished = 0
    for name in ordered_names:
        members = by_theme[name]
        synth = None
        if zai_key and not bad_key:
            try:
                synth = synthesize(name, render.material_for(members), pbrief, zai_key)
            except AuthError as e:
                summary(f"WARNING: {e} — deterministic synthesis for remaining themes")
                bad_key = True
            if synth:
                polished += 1
        theme_blocks.append({"name": name, "synth": synth, "members": members,
                             "chips": _chips(members, neighbors, by_id)})

    md = render.build_digest(date=date, mode=mode, order=order,
                             theme_blocks=theme_blocks, thin=thin, total=len(scope))
    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIGESTS_DIR / (f"bootstrap-{date}.md" if mode == "bootstrap" else f"{date}.md")
    out_path.write_text(md, encoding="utf-8")
    summary(f"wrote {out_path.relative_to(REPO_ROOT)} ({len(theme_blocks)} themes, "
            f"{polished} GLM-synthesized, {len(thin)} thin)")
    return 1 if bad_key else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", nargs="?", default="daily", choices=["daily", "bootstrap"])
    args = ap.parse_args()
    return run(args.mode, os.environ.get("ZAI_API_KEY"))


if __name__ == "__main__":
    raise SystemExit(main())
