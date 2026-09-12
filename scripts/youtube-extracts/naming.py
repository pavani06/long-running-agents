"""Filename helpers for extracts.

An extract mirrors its transcript's stem with a `.md` extension, so the pair is
obvious on disk (`<stem>.txt` <-> `<stem>.md`). The video id (the stable diff
key) is recovered from either, handling ids that contain "--" via the 11-char
tail — same rule as the transcripts layer.
"""
from __future__ import annotations

import re

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def video_id_from(filename: str) -> str | None:
    stem = filename.rsplit(".", 1)[0]
    candidate = stem.rsplit("--", 1)[-1] if "--" in stem else stem
    if VIDEO_ID_RE.match(candidate):
        return candidate
    tail = stem[-11:]
    return tail if VIDEO_ID_RE.match(tail) else None


def extract_name_for(transcript_filename: str) -> str:
    """`<date>-<slug>--<id>.txt` -> `<date>-<slug>--<id>.md`."""
    return transcript_filename.rsplit(".", 1)[0] + ".md"


def title_from_transcript_name(transcript_filename: str) -> str:
    """Fallback title when the video is no longer in the playlist enumeration.

    `2026-09-11-lets-build-gpt--kCc8FmEb1nY.txt` -> `Lets Build Gpt`.
    """
    stem = transcript_filename.rsplit(".", 1)[0]
    slug = stem.rsplit("--", 1)[0]  # drop the id
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)  # drop the date prefix
    return slug.replace("-", " ").strip().title() or "Untitled"
