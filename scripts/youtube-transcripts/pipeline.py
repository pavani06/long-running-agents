#!/usr/bin/env python3
"""Daily transcript pipeline for the "AI - Learning" playlist.

Enumerates the playlist (YouTube Data API v3), diffs against the corpus on disk
(stateless — the repo is the source of truth), fetches transcripts for the gap
(SerpApi), and regenerates index.json / missing.json.

Modes:
  daily          fetch videos not on disk and not already known-missing (default)
  retry-missing  daily + re-attempt the known-missing videos (weekly / on demand)
  full-rescan    re-attempt every video not on disk, ignoring the fetch cap
  migrate        one-off: rename legacy `<id>.txt` files to the new scheme

Environment:
  YOUTUBE_API_KEY    YouTube Data API v3 key (enumeration)   — always required
  SERPAPI_API_KEY    SerpApi key (transcripts)               — required except in migrate
  MAX_FETCH          override the per-run fetch cap (default 25)

Exit codes: 0 = success (incl. nothing-new and 429 partial); 1 = red (invalid
key, empty enumeration, or diff over the cap).
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from serpapi import AuthError, RateLimited, fetch_transcript
from store import Corpus, watch_url
from youtube import EnumerationError, enumerate_playlist

PLAYLIST_ID = "PLdJYvRCSB6rO2Mm_0wGnHgFfoy34OaC0S"
DATA_DIR = Path(__file__).resolve().parents[2] / "raw" / "youtube" / "ai-learning"
TZ = ZoneInfo("America/Sao_Paulo")
DEFAULT_MAX_FETCH = 25
PACING_SECONDS = 1.75
MIGRATION_DATE = "2026-09-11"  # real extraction date of the original 361-file corpus


def today() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def summary(line: str) -> None:
    """Print, and append to the GitHub Actions step summary when running in CI."""
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def run_migrate(corpus: Corpus, date: str, youtube_key: str) -> int:
    videos = enumerate_playlist(PLAYLIST_ID, youtube_key)
    if not videos:
        summary("RED: enumeration returned 0 videos")
        return 1
    id_to_title = {v.video_id: v.title for v in videos}
    renamed = corpus.rename_legacy(id_to_title, date)
    corpus.regenerate_index()
    summary(f"migrate: renamed {len(renamed)} legacy files; index regenerated")
    return 0


def run_fetch(corpus: Corpus, mode: str, max_fetch: int, youtube_key: str, serpapi_key: str) -> int:
    videos = enumerate_playlist(PLAYLIST_ID, youtube_key)
    if not videos:
        summary("RED: enumeration returned 0 videos (API/playlist problem)")
        return 1
    summary(f"enumerated {len(videos)} playlist videos")

    on_disk = set(corpus.scan_disk())
    missing = corpus.load_missing()
    skip = on_disk | set(missing) if mode == "daily" else on_disk
    targets = [v for v in videos if v.video_id not in skip]

    over_cap = False
    enforce_cap = mode != "full-rescan"
    if enforce_cap and len(targets) > max_fetch:
        over_cap = True
        summary(f"WARNING: {len(targets)} new videos exceeds cap {max_fetch} — fetching {max_fetch}, will exit red")
        targets = targets[:max_fetch]

    if not targets:
        summary("nothing new to fetch")
        corpus.regenerate_index()
        corpus.write_missing(missing)
        return 1 if over_cap else 0

    date = today()
    prior_meta = corpus._load_prior_meta()
    fetched = 0
    rate_limited = False
    for i, v in enumerate(targets, 1):
        try:
            tr = fetch_transcript(v.video_id, serpapi_key)
        except AuthError as e:
            summary(f"RED: {e}")
            corpus.regenerate_index(prior_meta)
            corpus.write_missing(missing)
            return 1
        except RateLimited:
            summary(f"WARNING: SerpApi rate-limited after {fetched} fetched — leaving the rest for next run")
            rate_limited = True
            break

        if tr is None:
            missing[v.video_id] = "sem transcript"
            summary(f"[{i}/{len(targets)}] {v.video_id} — no captions")
        else:
            fname = corpus.add_transcript(date, v.video_id, v.title, tr.text)
            prior_meta[v.video_id] = {"lang": tr.lang, "segments": tr.segments}
            missing.pop(v.video_id, None)
            fetched += 1
            summary(f"[{i}/{len(targets)}] {v.video_id} — ok ({len(tr.text)} chars) -> {fname}")
        time.sleep(PACING_SECONDS)

    corpus.regenerate_index(prior_meta)
    corpus.write_missing(missing)
    summary(f"done: {fetched} new transcripts, {len(missing)} still missing"
            + (" [partial: rate-limited]" if rate_limited else ""))
    return 1 if over_cap else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", nargs="?", default="daily",
                    choices=["daily", "retry-missing", "full-rescan", "migrate"])
    ap.add_argument("--max-fetch", type=int, default=int(os.environ.get("MAX_FETCH", DEFAULT_MAX_FETCH)))
    ap.add_argument("--date", default=MIGRATION_DATE, help="extraction date stamp for migrate mode")
    ap.add_argument("--data-dir", default=str(DATA_DIR))
    args = ap.parse_args()

    corpus = Corpus(Path(args.data_dir))

    youtube_key = os.environ.get("YOUTUBE_API_KEY")
    if not youtube_key:
        print("RED: YOUTUBE_API_KEY not set", file=sys.stderr)
        return 1

    try:
        if args.mode == "migrate":
            return run_migrate(corpus, args.date, youtube_key)

        serpapi_key = os.environ.get("SERPAPI_API_KEY")
        if not serpapi_key:
            print("RED: SERPAPI_API_KEY not set", file=sys.stderr)
            return 1
        return run_fetch(corpus, args.mode, args.max_fetch, youtube_key, serpapi_key)
    except EnumerationError as e:
        summary(f"RED: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
