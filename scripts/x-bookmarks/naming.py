"""Filename scheme for the X bookmarks corpus.

Convention (mirrors the youtube corpus `<date>-<slug>--<id>` precedent):

    <YYYY-MM-DD>-<handle>-<title-slug>--<status_id>.json

- ``<YYYY-MM-DD>``  collection date (America/Sao_Paulo), stamped when the
  bookmark is first written; immutable thereafter.
- ``<handle>``      the author's screen name, ASCII-folded, no leading '@'.
- ``<title-slug>``  kebab-case, ASCII-folded slug of the tweet text.
- ``--<status_id>`` the numeric tweet id — the stable key the stateless diff
  reads back from disk. Handles and slugs never contain ``--``, so the double
  dash is an unambiguous separator (unlike the youtube 11-char id, the X id is
  numeric and variable length, so we key on the ``--`` split, not a fixed len).

All functions here are pure so they can be unit-tested without network or disk.
"""
from __future__ import annotations

import re
import unicodedata

# Tweet ids are numeric, currently ~19 digits; allow a generous range.
STATUS_ID_RE = re.compile(r"^\d{5,25}$")
_SLUG_MAX = 60
_HANDLE_MAX = 20


def _fold(text: str) -> str:
    return unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")


def slugify(text: str, limit: int = _SLUG_MAX) -> str:
    """kebab-case, ASCII-only slug. Empty/degenerate -> 'untitled'."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", _fold(text)).lower().strip("-")
    slug = slug[:limit].rstrip("-")
    return slug or "untitled"


def clean_handle(handle: str) -> str:
    """ASCII handle without a leading '@'. Empty -> 'unknown'."""
    h = re.sub(r"[^a-zA-Z0-9_]+", "", _fold(handle).lstrip("@")).lower()
    return (h[:_HANDLE_MAX] or "unknown")


def build_filename(collection_date: str, handle: str, text: str, status_id: str) -> str:
    """`<date>-<handle>-<slug>--<status_id>.json`. Date must be 'YYYY-MM-DD'."""
    if not STATUS_ID_RE.match(status_id):
        raise ValueError(f"invalid tweet status id: {status_id!r}")
    return f"{collection_date}-{clean_handle(handle)}-{slugify(text)}--{status_id}.json"


def parse_status_id(filename: str) -> str | None:
    """Recover the numeric status id from a bookmark filename, or None."""
    stem = filename[:-5] if filename.endswith(".json") else filename
    candidate = stem.rsplit("--", 1)[-1] if "--" in stem else stem
    return candidate if STATUS_ID_RE.match(candidate) else None
