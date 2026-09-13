"""Single definition of a 'thin' extract — the source of truth for downstream.

A bookmark is thin when there was no real substance to extract: the model
produced no key_points AND the extract was grounded only in the tweet (the
linked content was a bare link, a one-liner, or an ingest that failed/paywalled).
Thin extracts cluster on generic placeholder topics; downstream layers read this
flag to exclude them from the theme graph (Fase 4) and surface them as a
"to investigate" bucket instead of a junk theme (Fase 5).
"""
from __future__ import annotations


def is_thin(key_points, grounded_in: str) -> bool:
    return not (key_points or []) and grounded_in == "tweet"
