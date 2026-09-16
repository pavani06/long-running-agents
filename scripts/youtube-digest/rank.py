"""'Watch in this order' ranking — deterministic, by tier then recency.

Not chronological: ranks by deep_dive tier (the extract's own high/medium/low
triage), then by extracted date, then video_id for stability. Thin extracts are
excluded (youtube extracts are never thin today, but the guard stays for parity).
"""
from __future__ import annotations

from corpus import Extract

REVISIT_W = {"high": 3, "medium": 2, "low": 1}


def read_order(extracts: list[Extract], *, n: int) -> list[Extract]:
    ranked = sorted(
        (e for e in extracts if not e.thin),
        key=lambda e: (REVISIT_W.get(e.revisit, 1), e.extracted, e.video_id),
        reverse=True,
    )
    return ranked[:n]
