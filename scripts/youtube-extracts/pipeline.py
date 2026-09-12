#!/usr/bin/env python3
"""Extract pipeline for the "AI - Learning" corpus (triage + implicit graph).

For every transcript without an extract, calls GLM once to distill a structured
extract (thesis / concepts / tools / people / claims + controlled tags + a
deep-dive tier), and writes it as a Markdown note under extracts/. Stateless:
the diff is transcripts/ minus extracts/.

Modes:
  incremental  extract transcripts that have no extract yet (default; capped)
  full         same, but no small cap — backfill the whole corpus (resumable)
  rebuild      re-extract every transcript (after an extract_version bump)

Environment:
  YOUTUBE_API_KEY  playlist enumeration (titles/channels)   — required
  ZAI_API_KEY      GLM coding-plan key (distillation)        — required
  EXTRACT_CAP      override the per-run cap

Exit: 0 = success (incl. nothing-to-do, over-cap partial, 429 partial, skipped
items); 1 = red (missing key, invalid key, or enumeration failure).
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# This package's dir goes to the FRONT so its naming/store win any name clash;
# the transcripts package (which has sibling naming.py/store.py) goes to the
# BACK, only to resolve `youtube` (unique to it).
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "youtube-transcripts"))

import glm  # noqa: E402
from glm import AuthError, ExtractError, RateLimited, fetch_extract  # noqa: E402
from render import VideoMeta, build_note  # noqa: E402
from store import ExtractStore  # noqa: E402
from taxonomy import build_vocabulary  # noqa: E402
from youtube import EnumerationError, enumerate_playlist  # noqa: E402

PLAYLIST_ID = "PLdJYvRCSB6rO2Mm_0wGnHgFfoy34OaC0S"
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


def watch_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def run(mode: str, cap: int, youtube_key: str, zai_key: str) -> int:
    store = ExtractStore(REPO_ROOT)
    pending = store.pending(rebuild=(mode == "rebuild"))
    if not pending:
        summary("nothing to extract")
        return 0

    try:
        videos = enumerate_playlist(PLAYLIST_ID, youtube_key)
    except EnumerationError as e:
        summary(f"RED: {e}")
        return 1
    meta_map = {v.video_id: v for v in videos}
    vocab = build_vocabulary(REPO_ROOT)
    summary(f"{len(pending)} transcripts pending; vocab={len(vocab)} tags; enumerated {len(videos)}")

    over_cap = len(pending) > cap
    targets = pending[:cap]
    if over_cap:
        summary(f"cap {cap}: extracting {len(targets)} now, {len(pending) - cap} left for next run")

    date = today()
    done = skipped = 0
    for i, (vid, tfile) in enumerate(targets, 1):
        text = store.read_transcript(tfile)
        try:
            extract = fetch_extract(text, zai_key, vocab)
        except AuthError as e:
            summary(f"RED: {e}")
            return 1
        except RateLimited:
            summary(f"WARNING: GLM rate-limited after {done} — leaving the rest for next run")
            break
        except ExtractError as e:
            skipped += 1
            summary(f"[{i}/{len(targets)}] {vid} — skip: {e}")
            time.sleep(PACING_SECONDS)
            continue

        pv = meta_map.get(vid)
        meta = VideoMeta(
            title=(pv.title if pv and pv.title else _fallback_title(tfile)),
            video_id=vid,
            url=watch_url(vid),
            channel=(pv.channel if pv else ""),
            transcript_file=tfile,
            extracted=date,
        )
        name = store.write_extract(tfile, build_note(meta, extract, vocab, EXTRACT_VERSION, glm.MODEL))
        done += 1
        summary(f"[{i}/{len(targets)}] {vid} — ok (deep_dive={extract.get('deep_dive')}) -> {name}")
        time.sleep(PACING_SECONDS)

    summary(f"done: {done} extracts written, {skipped} skipped, {len(pending) - done} still pending")
    return 0


def _fallback_title(transcript_filename: str) -> str:
    from naming import title_from_transcript_name
    return title_from_transcript_name(transcript_filename)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", nargs="?", default="incremental",
                    choices=["incremental", "full", "rebuild"])
    ap.add_argument("--cap", type=int, default=None)
    args = ap.parse_args()

    youtube_key = os.environ.get("YOUTUBE_API_KEY")
    zai_key = os.environ.get("ZAI_API_KEY")
    if not youtube_key:
        print("RED: YOUTUBE_API_KEY not set", file=sys.stderr)
        return 1
    if not zai_key:
        print("RED: ZAI_API_KEY not set", file=sys.stderr)
        return 1

    if args.cap is not None:
        cap = args.cap
    elif os.environ.get("EXTRACT_CAP"):
        cap = int(os.environ["EXTRACT_CAP"])
    else:
        cap = DEFAULT_CAP if args.mode == "incremental" else 10_000

    return run(args.mode, cap, youtube_key, zai_key)


if __name__ == "__main__":
    raise SystemExit(main())
