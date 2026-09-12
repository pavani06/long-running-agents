#!/usr/bin/env python3
"""Extract pipeline for the X bookmarks corpus (lean per-tweet extract).

For every raw bookmark item without an extract, calls GLM once to distill a
lean extract (topic / summary / tags / entities / content_type / revisit) and
writes it as a Markdown note under extracts/x/bookmarks/. Factual links/media
are carried from the raw item, not the model. Stateless: the diff is
raw/x/bookmarks/items/ minus extracts/x/bookmarks/.

Modes:
  incremental  extract items that have no extract yet (default; capped)
  full         same, but no small cap — backfill the whole corpus (resumable)
  rebuild      re-extract every item (after an extract_version bump)

Environment:
  ZAI_API_KEY   GLM coding-plan key (distillation)   — required
  EXTRACT_CAP   override the per-run cap

Exit: 0 = success (incl. nothing-to-do, over-cap partial, 429 partial, skipped
items); 1 = red (missing/invalid key).
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

import glm  # noqa: E402
from glm import AuthError, ExtractError, RateLimited, fetch_extract  # noqa: E402
from render import BookmarkMeta, build_note  # noqa: E402
from store import ExtractStore  # noqa: E402
from taxonomy import build_vocabulary  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
TZ = ZoneInfo("America/Sao_Paulo")
EXTRACT_VERSION = 1
DEFAULT_CAP = 50
PACING_SECONDS = 1.5


def today() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def run(mode: str, cap: int, zai_key: str) -> int:
    store = ExtractStore(REPO_ROOT)
    pending = store.pending(rebuild=(mode == "rebuild"))
    if not pending:
        summary("nothing to extract")
        return 0

    vocab = build_vocabulary(REPO_ROOT)
    summary(f"{len(pending)} bookmarks pending; vocab={len(vocab)} tags")

    over_cap = len(pending) > cap
    targets = pending[:cap]
    if over_cap:
        summary(f"cap {cap}: extracting {len(targets)} now, {len(pending) - cap} left for next run")

    date = today()
    done = skipped = 0
    for i, (sid, ifile) in enumerate(targets, 1):
        item = store.read_item(ifile)
        text = item.get("text", "")
        handle = item.get("handle", "unknown")
        links = item.get("links", []) or []
        try:
            extract = fetch_extract(text, handle, links, zai_key, vocab)
        except AuthError as e:
            summary(f"RED: {e}")
            return 1
        except RateLimited:
            summary(f"WARNING: GLM rate-limited after {done} — leaving the rest for next run")
            break
        except ExtractError as e:
            skipped += 1
            summary(f"[{i}/{len(targets)}] {sid} — skip: {e}")
            time.sleep(PACING_SECONDS)
            continue

        meta = BookmarkMeta(
            status_id=sid,
            handle=handle,
            url=item.get("url", ""),
            created_at=item.get("created_at", ""),
            item_file=ifile,
            extracted=date,
            links=links,
            media=item.get("media", []) or [],
        )
        name = store.write_extract(ifile, build_note(meta, extract, vocab, EXTRACT_VERSION, glm.MODEL))
        done += 1
        summary(f"[{i}/{len(targets)}] {sid} — ok (revisit={extract.get('revisit')}) -> {name}")
        time.sleep(PACING_SECONDS)

    summary(f"done: {done} extracts written, {skipped} skipped, {len(pending) - done} still pending")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", nargs="?", default="incremental",
                    choices=["incremental", "full", "rebuild"])
    ap.add_argument("--cap", type=int, default=None)
    args = ap.parse_args()

    zai_key = os.environ.get("ZAI_API_KEY")
    if not zai_key:
        print("RED: ZAI_API_KEY not set", file=sys.stderr)
        return 1

    if args.cap is not None:
        cap = args.cap
    elif os.environ.get("EXTRACT_CAP"):
        cap = int(os.environ["EXTRACT_CAP"])
    else:
        cap = DEFAULT_CAP if args.mode == "incremental" else 10_000

    return run(args.mode, cap, zai_key)


if __name__ == "__main__":
    raise SystemExit(main())
