"""Filename scheme for the "AI - Learning" transcript corpus.

Convention (follows the repo's `<date>-<slug>` precedent used by docs/analysis/):

    <YYYY-MM-DD>-<title-slug>--<video_id>.txt

- ``<YYYY-MM-DD>``  extraction date (America/Sao_Paulo), stamped when the
  transcript is fetched; immutable thereafter.
- ``<title-slug>``  kebab-case, ASCII-folded slug of the video title.
- ``--<video_id>``  the 11-char YouTube id, the stable key the stateless diff
  reads back from disk. The double dash is the only ``--`` in the name (slugs
  never contain consecutive dashes), so it is an unambiguous separator.

All functions here are pure so they can be unit-tested without network or disk.
"""
from __future__ import annotations

import re
import unicodedata

# YouTube video ids are always exactly 11 chars of [A-Za-z0-9_-].
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
_SLUG_MAX = 80


def slugify(title: str) -> str:
    """kebab-case, ASCII-only slug. Empty/degenerate titles -> 'untitled'."""
    folded = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", folded).lower().strip("-")
    slug = slug[:_SLUG_MAX].rstrip("-")
    return slug or "untitled"


def build_filename(extraction_date: str, title: str, video_id: str) -> str:
    """`<date>-<slug>--<id>.txt`. `extraction_date` must be 'YYYY-MM-DD'."""
    if not VIDEO_ID_RE.match(video_id):
        raise ValueError(f"invalid youtube video id: {video_id!r}")
    return f"{extraction_date}-{slugify(title)}--{video_id}.txt"


def parse_video_id(filename: str) -> str | None:
    """Recover the video id from a transcript filename.

    Handles both the current scheme (`...--<id>.txt`) and the legacy
    `<id>.txt` files that predate the migration. Returns None if no valid
    11-char id can be recovered.
    """
    stem = filename[:-4] if filename.endswith(".txt") else filename
    candidate = stem.rsplit("--", 1)[-1] if "--" in stem else stem
    if VIDEO_ID_RE.match(candidate):
        return candidate
    # Fallback: ids are exactly 11 chars, so try the tail.
    tail = stem[-11:]
    return tail if VIDEO_ID_RE.match(tail) else None
