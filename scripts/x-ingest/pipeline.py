#!/usr/bin/env python3
"""Ingest the content bookmarks link to, into ingest/x/.

For every external link across raw/x/bookmarks/items/ without ingested content,
fetch it (Jina Reader → trafilatura fallback) and store the cleaned text plus
provenance (fetch_status). Stateless: the diff is raw links minus ingest/x/.

Modes:
  incremental  fetch links not yet ingested (default; capped)
  retry        also re-fetch links previously marked `failed`
  full         re-fetch every link (no small cap)

Environment:
  INGEST_CAP   override the per-run cap

No API key required (Jina Reader anonymous). Exit: 0 = success (incl.
nothing-to-do, over-cap partial, per-link failures recorded as status);
1 = red (unexpected error).
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

from fetch import fetch_content  # noqa: E402
from store import IngestStore  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
TZ = ZoneInfo("America/Sao_Paulo")
DEFAULT_CAP = 40
PACING_SECONDS = 3.0  # Jina anonymous rate-limits; pace defensively


def today() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def run(mode: str, cap: int) -> int:
    store = IngestStore(REPO_ROOT)
    links = store.collect_links()
    pending = store.pending(links, mode=mode)
    summary(f"{len(links)} external links total; {len(pending)} pending ({mode})")
    if not pending:
        summary("nothing to ingest")
        store.regenerate_index()
        return 0

    over_cap = len(pending) > cap
    targets = pending[:cap]
    if over_cap:
        summary(f"cap {cap}: ingesting {len(targets)} now, {len(pending) - cap} left for next run")

    date = today()
    counts: dict[str, int] = {}
    for i, url in enumerate(targets, 1):
        result = fetch_content(url)
        st = result["status"]
        counts[st] = counts.get(st, 0) + 1
        store.write_entry(url, result, date)
        summary(f"[{i}/{len(targets)}] {st:11s} {result.get('method',''):11s} {url[:80]}")
        time.sleep(PACING_SECONDS)

    total = store.regenerate_index()
    summary(f"done: this run {counts}; corpus status {total}")
    if counts.get("failed", 0) == len(targets) and targets:
        summary("WARNING: every fetch failed this run (possible rate-limit) — retry next run")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", nargs="?", default="incremental",
                    choices=["incremental", "retry", "full"])
    args = ap.parse_args()
    if args.mode == "full":
        cap = int(os.environ.get("INGEST_CAP") or 10_000)
    else:
        cap = int(os.environ.get("INGEST_CAP") or DEFAULT_CAP)
    return run(args.mode, cap)


if __name__ == "__main__":
    raise SystemExit(main())
