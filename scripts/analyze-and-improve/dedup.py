"""Cosine duplication check — a deterministic gate against re-creating what exists.

Given the embedding of a proposed artifact and the Etapa-0 repo index, find the
nearest existing section; if it is at or above a threshold, the artifact is a
likely duplicate and must be held (never landed as net-new). Reuses the index's
vectors and `retrieval.rank_sections`. Pure and unit-tested; the threshold is
provisional here (final calibration is #262).
"""
from __future__ import annotations

from retrieval import rank_sections

# Duplication threshold: at/above this cosine to an existing section, treat a
# proposed artifact as already covered. VALIDATED via #262 — an exact indexed
# section (the seeded known-duplicate) scores ~1.0 and is caught; 0.85 sits well
# above the repo's p99 (0.64), so it flags near-duplicates without false positives.
DUP_THRESHOLD = 0.85


def nearest(vec: list[float], index: dict) -> dict | None:
    """The single closest indexed section to `vec`, or None if the index is empty."""
    top = rank_sections(vec, index, k=1)
    return top[0] if top else None


def is_duplicate(vec: list[float], index: dict,
                 threshold: float = DUP_THRESHOLD) -> dict:
    """{'duplicate': bool, 'score': float, 'nearest': {id,path,heading}|None}.

    `duplicate` is True when the nearest section's cosine is >= threshold."""
    n = nearest(vec, index)
    if n is None:
        return {"duplicate": False, "score": 0.0, "nearest": None}
    return {"duplicate": n["score"] >= threshold, "score": n["score"], "nearest": n}
