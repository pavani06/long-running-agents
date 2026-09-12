#!/usr/bin/env python3
"""Connections layer for the "AI - Learning" extract corpus.

Embeds every extract (title+thesis+concepts+claims) with OpenAI, builds a
symmetric top-K cosine graph, writes `relates-to` into each extract's
frontmatter (the Obsidian graph) and a weighted `connections.json` (programmatic
use / future theme clustering). Batch job: recomputes the whole graph each run.

Environment:
  OPENAI_API_KEY  embeddings key                       — required
  CONN_K          neighbors per node (default 6)
  CONN_FLOOR      cosine floor, e.g. 0.38 (default: none — pure top-K)
  CONN_DRY_RUN    "1" to embed + log distribution only, writing nothing

Exit: 0 = success (incl. nothing-to-do); 1 = red (missing/invalid key, API error).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

from embed import AuthError, EmbedError, MODEL, embed_texts  # noqa: E402
from extracts_io import embed_text, load_all  # noqa: E402
from frontmatter_io import update_file, wikilink  # noqa: E402
from graph import build_edges, distribution, neighbors  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACTS_DIR = REPO_ROOT / "extracts" / "youtube" / "ai-learning"
CONNECTIONS_JSON = EXTRACTS_DIR / "connections.json"
TZ = ZoneInfo("America/Sao_Paulo")
DEFAULT_K = 6


def summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def run(api_key: str, k: int, floor: float | None, dry_run: bool) -> int:
    extracts = load_all(EXTRACTS_DIR)
    if len(extracts) < 2:
        summary(f"only {len(extracts)} extracts — nothing to connect")
        return 0

    ids = [e.video_id for e in extracts]
    by_id = {e.video_id: e for e in extracts}
    try:
        vectors = embed_texts([embed_text(e) for e in extracts], api_key)
    except AuthError as e:
        summary(f"RED: {e}")
        return 1
    except EmbedError as e:
        summary(f"RED: {e}")
        return 1

    dist = distribution(ids, vectors)
    summary(f"embedded {len(ids)} extracts ({MODEL}); similarity {dist}")

    edges = build_edges(ids, vectors, k=k, floor=floor)
    nbrs = neighbors(edges)
    summary(f"graph: {len(edges)} edges, k={k}, floor={floor}; "
            f"avg degree {round(2 * len(edges) / len(ids), 1)}")

    if dry_run:
        summary("dry-run: not writing relates-to or connections.json")
        return 0

    changed = 0
    for e in extracts:
        links = [wikilink(by_id[nid].file, by_id[nid].title) for nid, _w in nbrs.get(e.video_id, [])]
        if update_file(EXTRACTS_DIR / e.file, links):
            changed += 1

    payload = {
        "model": MODEL,
        "generated": datetime.now(TZ).strftime("%Y-%m-%d"),
        "k": k,
        "floor": floor,
        "nodes": len(ids),
        "distribution": dist,
        "edges": [
            {"a": e.a, "b": e.b, "weight": round(e.weight, 4),
             "a_title": by_id[e.a].title, "b_title": by_id[e.b].title}
            for e in edges
        ],
    }
    CONNECTIONS_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary(f"wrote relates-to to {changed} extracts + connections.json ({len(edges)} edges)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--k", type=int, default=int(os.environ.get("CONN_K", DEFAULT_K)))
    ap.add_argument("--floor", type=float,
                    default=(float(os.environ["CONN_FLOOR"]) if os.environ.get("CONN_FLOOR") else None))
    ap.add_argument("--dry-run", action="store_true", default=os.environ.get("CONN_DRY_RUN") == "1")
    args = ap.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("RED: OPENAI_API_KEY not set", file=sys.stderr)
        return 1
    return run(api_key, args.k, args.floor, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
