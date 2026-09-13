"""'Read in this order' ranking — deterministic, by density then recency.

Not chronological: ranks by revisit tier (the extract's own high/medium/low
triage), then by tweet recency, then status_id for stability. Thin extracts are
excluded (they go to the 'to investigate' bucket, not the reading list).
"""
from __future__ import annotations

from corpus import Extract

REVISIT_W = {"high": 3, "medium": 2, "low": 1}


def read_order(extracts: list[Extract], *, n: int) -> list[Extract]:
    ranked = sorted(
        (e for e in extracts if not e.thin),
        key=lambda e: (REVISIT_W.get(e.revisit, 1), e.created_at, e.status_id),
        reverse=True,
    )
    return ranked[:n]
