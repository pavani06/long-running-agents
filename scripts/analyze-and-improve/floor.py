"""Cosine floor + pairwise-similarity distribution for the repo's own sections.

The *floor* is the cosine threshold below which two sections are treated as
unrelated during retrieval. The repo's section-embedding distribution differs
from the videos' (denser shared vocabulary), so the floor must be calibrated to
the repo — this module ships a documented **provisional** starting value and the
`distribution` tool to calibrate it. Final calibration is Etapa 4 (#262).

`distribution` mirrors the connections layer's pairwise-cosine summary
(`scripts/youtube-connections/graph.py`), pure math, no numpy.
"""
from __future__ import annotations

import math

# Provisional starting floor. Anchored to the connections layer's cross-video
# floor (~0.38); the repo's true floor is calibrated in #262 from the empirical
# distribution emitted by `pipeline.py --distribution` on the first indexed run.
PROVISIONAL_FLOOR = 0.38


def _normalize(vec: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in vec))
    return [x / n for x in vec] if n else vec


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two vectors (normalizes internally)."""
    ua, ub = _normalize(a), _normalize(b)
    return sum(x * y for x, y in zip(ua, ub))


def distribution(vectors: list[list[float]]) -> dict:
    """Percentiles of all pairwise cosine similarities — to calibrate the floor."""
    units = [_normalize(v) for v in vectors]
    n = len(units)
    sims = sorted(
        sum(x * y for x, y in zip(units[i], units[j]))
        for i in range(n) for j in range(i + 1, n)
    )
    if not sims:
        return {}

    def pct(p: float) -> float:
        return round(sims[min(len(sims) - 1, int(p / 100 * len(sims)))], 3)

    return {"pairs": len(sims), "min": round(sims[0], 3), "p50": pct(50),
            "p75": pct(75), "p90": pct(90), "p95": pct(95), "p99": pct(99),
            "max": round(sims[-1], 3)}
