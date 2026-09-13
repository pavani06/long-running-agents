"""Build a symmetric top-K similarity graph from embeddings (pure, testable)."""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Edge:
    a: str  # video_id, a < b
    b: str
    weight: float


def _normalize(vec: list[float]) -> list[float]:
    n = math.sqrt(sum(x * x for x in vec))
    return [x / n for x in vec] if n else vec


def cosine_unit(a: list[float], b: list[float]) -> float:
    """Dot product of two already-unit-normalized vectors."""
    return sum(x * y for x, y in zip(a, b))


def build_edges(ids: list[str], vectors: list[list[float]], *, k: int = 6,
                floor: float | None = None) -> list[Edge]:
    """Symmetric top-K edges. Each node keeps its K nearest (>= floor); the edge
    set is the undirected union, so a link A->B also connects B->A."""
    units = [_normalize(v) for v in vectors]
    n = len(ids)
    sims = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            s = cosine_unit(units[i], units[j])
            sims[i][j] = sims[j][i] = s

    edge_w: dict[tuple[str, str], float] = {}
    for i in range(n):
        order = sorted((j for j in range(n) if j != i), key=lambda j: sims[i][j], reverse=True)
        kept = 0
        for j in order:
            if floor is not None and sims[i][j] < floor:
                break
            a, b = sorted((ids[i], ids[j]))
            edge_w[(a, b)] = sims[i][j]
            kept += 1
            if kept >= k:
                break
    return sorted((Edge(a, b, w) for (a, b), w in edge_w.items()),
                  key=lambda e: e.weight, reverse=True)


def neighbors(edges: list[Edge]) -> dict[str, list[tuple[str, float]]]:
    """video_id -> [(neighbor_id, weight)], sorted by weight desc."""
    out: dict[str, list[tuple[str, float]]] = {}
    for e in edges:
        out.setdefault(e.a, []).append((e.b, e.weight))
        out.setdefault(e.b, []).append((e.a, e.weight))
    for vid in out:
        out[vid].sort(key=lambda t: t[1], reverse=True)
    return out


def distribution(ids: list[str], vectors: list[list[float]]) -> dict:
    """Percentiles of all pairwise cosine similarities — to calibrate the floor."""
    units = [_normalize(v) for v in vectors]
    n = len(ids)
    sims = sorted(cosine_unit(units[i], units[j])
                  for i in range(n) for j in range(i + 1, n))
    if not sims:
        return {}
    def pct(p): return round(sims[min(len(sims) - 1, int(p / 100 * len(sims)))], 3)
    return {"pairs": len(sims), "min": round(sims[0], 3), "p50": pct(50),
            "p75": pct(75), "p90": pct(90), "p95": pct(95), "p99": pct(99),
            "max": round(sims[-1], 3)}
