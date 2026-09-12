"""Filename helpers for bookmark extracts.

An extract mirrors its raw item's stem with `.md` (`<stem>.json` <-> `<stem>.md`),
so the pair is obvious on disk. The numeric status id (the stable diff key) is
recovered from either — same `--<id>` rule as the raw layer.
"""
from __future__ import annotations

import re

STATUS_ID_RE = re.compile(r"^\d{5,25}$")


def status_id_from(filename: str) -> str | None:
    stem = filename.rsplit(".", 1)[0]
    candidate = stem.rsplit("--", 1)[-1] if "--" in stem else stem
    return candidate if STATUS_ID_RE.match(candidate) else None


def extract_name_for(item_filename: str) -> str:
    """`<date>-<handle>-<slug>--<id>.json` -> `<date>-<handle>-<slug>--<id>.md`."""
    return item_filename.rsplit(".", 1)[0] + ".md"
