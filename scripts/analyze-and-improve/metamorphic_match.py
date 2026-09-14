"""Two-stage concept matcher — pure parts (#288).

Stage 1 (here, pure): embed the variant, cosine-rank it against each concept's
profile embedding, keep the top-k candidates. Fixes the "arbitrary threshold"
problem by handing several candidates to a semantic judge instead of cutting on
one number.

Stage 2 decision (here, pure): given the reranker's per-candidate verdicts
(`same_concept`, `confidence`, `granularity_relation`), pick the matched
concept_id. The reranker CALL itself is network and lives in metamorphic_rerank.

Identity (does this paraphrase name concept X?) is `same_concept`; granularity
(equivalent / broader / narrower) is recorded but does NOT gate identity — a
broader or narrower phrasing of the same concept is still the same concept.
`related_but_distinct` / `unrelated` are NOT a match (that is the T4 boundary).
"""
from __future__ import annotations

from floor import cosine

# Granularity relations that still count as "the same concept" for T1 identity.
SAME_CONCEPT_GRANULARITIES = {"equivalent", "broader_than", "narrower_than"}


def rank_candidates(variant_vec: list[float], concept_vecs: dict[str, list[float]],
                    *, k: int = 3, floor: float | None = None) -> list[dict]:
    """Top-k concepts by cosine of the variant to each concept's profile vector. Pure.

    Returns [{concept_id, score}] sorted desc. `floor` drops weak candidates so a
    variant that matches nothing well yields fewer (or zero) candidates to rerank."""
    scored = [{"concept_id": cid, "score": cosine(variant_vec, vec)}
              for cid, vec in concept_vecs.items() if vec]
    if floor is not None:
        scored = [s for s in scored if s["score"] >= floor]
    scored.sort(key=lambda d: d["score"], reverse=True)
    return scored[:k]


def decide_match(rerank_results: list[dict], *, min_confidence: float = 0.0) -> dict:
    """Pick the matched concept from stage-2 verdicts. Pure.

    `rerank_results`: [{concept_id, same_concept, confidence, granularity_relation,
    stage1_score}] for the reranked candidates. A candidate is eligible when the
    reranker says `same_concept` is true AND its confidence clears `min_confidence`.
    Among eligible candidates the highest confidence wins (ties broken by the
    stage-1 cosine). No eligible candidate -> unmatched (concept_id None)."""
    eligible = [r for r in rerank_results
                if r.get("same_concept") and (r.get("confidence") or 0.0) >= min_confidence]
    if not eligible:
        return {"concept_id": None, "matched": False, "confidence": 0.0,
                "granularity_relation": None}
    best = max(eligible, key=lambda r: (r.get("confidence") or 0.0, r.get("stage1_score") or 0.0))
    return {"concept_id": best["concept_id"], "matched": True,
            "confidence": best.get("confidence") or 0.0,
            "granularity_relation": best.get("granularity_relation")}
