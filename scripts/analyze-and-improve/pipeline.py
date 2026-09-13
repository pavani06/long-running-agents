#!/usr/bin/env python3
"""Control plane for analyze-and-improve v4 (Etapa 0) — no LLM, read-only.

Two deterministic jobs, no model judgment (that lands in Etapa 1+):

  queue    List the `deep_dive: high` sources still needing an analysis package
           (stateless diff over the `analyzed:` marker). No network, no writes.

  index    Build/refresh the repo's per-section semantic index. `--full` embeds
           every target section; otherwise a git delta scan from the stored
           commit re-embeds only the chunks that changed. `--distribution`
           embeds and prints the pairwise-cosine distribution (to calibrate the
           floor, #262) without writing the index.

Environment:
  OPENAI_API_KEY   embeddings for `index` (not needed for `queue`)   — required there

Exit: 0 = success (incl. nothing-to-do); 1 = red (missing/invalid key, git failure).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import deltascan  # noqa: E402
from embed import AuthError, EmbedError, embed_texts  # noqa: E402
from floor import PROVISIONAL_FLOOR, distribution  # noqa: E402
from index_store import (index_vectors, merge_index, records_for,  # noqa: E402
                         select_to_embed)
from analysis_queue import scan_pending  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACTS_DIR = REPO_ROOT / "extracts" / "youtube" / "ai-learning"
STATE_PATH = REPO_ROOT / ".runtime" / "analyze-and-improve" / "index.json"


def summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"version": 1, "base_sha": None, "records": {}}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def run_queue() -> int:
    pending = scan_pending(EXTRACTS_DIR)
    summary(f"queue: {len(pending)} deep_dive:high source(s) pending analysis")
    for p in pending:
        print(f"  - {p.file}")
    return 0


def _collect_records(paths: list[str]) -> dict[str, list]:
    out: dict[str, list] = {}
    for rel in paths:
        fp = REPO_ROOT / rel
        if fp.exists():
            out[rel] = records_for(rel, fp.read_text(encoding="utf-8"))
    return out


def run_index(full: bool, dist_only: bool) -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        summary("index: OPENAI_API_KEY not set")
        return 1

    state = load_state()
    if full or not state.get("base_sha"):
        paths, deleted = deltascan.full_scan(REPO_ROOT), []
    else:
        paths = deltascan.changed_files(REPO_ROOT, state["base_sha"])
        deleted = deltascan.deleted_files(REPO_ROOT, state["base_sha"])

    changed = _collect_records(paths)
    to_embed = [r for recs in changed.values() for r in select_to_embed(state, recs)]
    summary(f"index: {len(paths)} file(s) in scope, {len(to_embed)} chunk(s) to embed, "
            f"{len(deleted)} deleted; provisional floor={PROVISIONAL_FLOOR}")

    vectors: dict[str, list[float]] = {}
    if to_embed:
        try:
            embedded = embed_texts([r.text for r in to_embed], api_key)
        except AuthError as e:
            summary(f"index: {e}")
            return 1
        except EmbedError as e:
            summary(f"index: {e}")
            return 1
        vectors = {r.id: v for r, v in zip(to_embed, embedded)}

    merged = merge_index(state, changed, deleted, vectors)
    dist = distribution(index_vectors(merged))
    summary(f"index: distribution {json.dumps(dist)}")

    if dist_only:
        summary("index: --distribution set, not writing state")
        return 0

    merged["base_sha"] = deltascan.head_sha(REPO_ROOT)
    save_state(merged)
    summary(f"index: {len(merged['records'])} record(s) written to {STATE_PATH.relative_to(REPO_ROOT)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="analyze-and-improve control plane (Etapa 0)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("queue", help="list deep_dive:high sources pending analysis")
    pi = sub.add_parser("index", help="build/refresh the repo semantic index")
    pi.add_argument("--full", action="store_true", help="embed every target section")
    pi.add_argument("--distribution", action="store_true",
                    help="embed + print cosine distribution, write nothing")
    args = ap.parse_args(argv)

    if args.cmd == "queue":
        return run_queue()
    return run_index(args.full, args.distribution)


if __name__ == "__main__":
    raise SystemExit(main())
