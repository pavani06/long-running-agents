"""Fase 4 — priorização por classificação e roteamento de categoria. Puro.

Mapping from the Fase-3 verdict (Missing/Partial/Exists/Better) to the creation
priority and the artifact categories to generate, following the v3 skill's
prioritization table (analyze-and-improve SKILL.md, "Priorizacao por impacto"):

    Missing            -> P0 -> canonical + skill + exercise
    Partial (high)     -> P1 -> canonical + exercise
    Partial (medium)   -> P2 -> canonical
    Exists / Better    -> no new artifacts (skip; recorded in the manifest)

The Fase-3 classifier of v4 emits no High/Medium axis, so `Partial` defaults to
"high" (P1); a classification carrying an explicit `value` key ("high"/"medium")
is honored. `plan_of_work` orders the work items in the v3 "Ordem de criacao":
canonical docs first, then skills, then exercises — within a category, P0 before
P1 before P2, stable in Fase-2 pattern order. Everything here is pure.
"""
from __future__ import annotations

CATEGORIES = ("canonical", "skill", "exercise")

# Creation order (v3 "Ordem de criacao"): canonical docs establish the truth
# before skills and exercises reference them; skills only for Missing; exercises
# for Missing (P0) and Partial High (P1).
_CATEGORIES_FOR_PRIORITY = {
    "P0": ["canonical", "skill", "exercise"],
    "P1": ["canonical", "exercise"],
    "P2": ["canonical"],
}
_PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2}


def priority_for(verdict: str, value: str = "high") -> str | None:
    """Missing=P0; Partial high=P1, medium=P2; Exists/Better=None (skip). Pure."""
    if verdict == "Missing":
        return "P0"
    if verdict == "Partial":
        return "P1" if value == "high" else "P2"
    return None   # Exists / Better: no new artifacts (cross-reference only)


def categories_for(priority: str | None) -> list[str]:
    """The artifact categories to generate for a priority. Pure."""
    return list(_CATEGORIES_FOR_PRIORITY.get(priority, []))


def skip_reason(verdict: str) -> str:
    """The manifest `skipped` reason for a verdict that generates nothing. Pure."""
    if verdict == "Exists":
        return "Already Exists — já coberto no repo; apenas cross-reference, sem artefatos novos"
    if verdict == "Better":
        return "Better Implementation — documentar a superioridade, não duplicar"
    return f"verdict {verdict!r} não gera artefatos"


def plan_of_work(classifications: list[dict]) -> list[dict]:
    """The ordered work items for Fase 4 generation. Pure.

    Each item: {category, pattern, verdict, priority}. Ordered by the v3 creation
    order (canonical, then skill, then exercise), priority ascending within a
    category (P0 first), stable in Fase-2 pattern order. Verdicts with no
    categories (Exists/Better) produce no items — they are recorded as skipped
    by the manifest, not planned here. A classification may carry `value`
    ("high"/"medium") to refine Partial; absent defaults to "high".
    """
    def _priority(c: dict):
        return _PRIORITY_ORDER.get(priority_for(c.get("verdict", ""),
                                                c.get("value", "high")), 99)

    planned: list[dict] = []
    for category in CATEGORIES:
        eligible = [c for c in classifications
                    if category in categories_for(
                        priority_for(c.get("verdict", ""), c.get("value", "high")))]
        for c in sorted(eligible, key=_priority):
            planned.append({"category": category, "pattern": c.get("pattern", ""),
                            "verdict": c.get("verdict", ""),
                            "priority": priority_for(c.get("verdict", ""),
                                                     c.get("value", "high"))})
    return planned
