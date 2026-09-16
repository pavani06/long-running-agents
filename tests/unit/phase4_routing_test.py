#!/usr/bin/env python3
"""Unit tests for Fase 4 category routing + prioritization (#263). Pure parts; no network."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import phase4_routing as pr  # noqa: E402


def test_priority_for_verdicts():
    assert pr.priority_for("Missing") == "P0"
    assert pr.priority_for("Partial") == "P1"                    # default value = high
    assert pr.priority_for("Partial", "high") == "P1"
    assert pr.priority_for("Partial", "medium") == "P2"
    assert pr.priority_for("Exists") is None                     # no new artifacts
    assert pr.priority_for("Better") is None
    assert pr.priority_for("nonsense") is None


def test_categories_for_priorities():
    assert pr.categories_for("P0") == ["canonical", "skill", "exercise"]
    assert pr.categories_for("P1") == ["canonical", "exercise"]
    assert pr.categories_for("P2") == ["canonical"]
    assert pr.categories_for(None) == []


CLS = [
    {"pattern": "A", "verdict": "Missing"},
    {"pattern": "B", "verdict": "Partial"},                       # P1 (high)
    {"pattern": "C", "verdict": "Partial", "value": "medium"},    # P2
    {"pattern": "D", "verdict": "Exists"},
    {"pattern": "E", "verdict": "Better"},
]


def test_plan_of_work_category_order_is_canonical_skill_exercise():
    plan = pr.plan_of_work(CLS)
    categories = [item["category"] for item in plan]
    # v3 "Ordem de criacao": canonical docs first, then skills, then exercises.
    assert categories == ["canonical", "canonical", "canonical", "skill", "exercise", "exercise"]


def test_plan_of_work_routes_categories_per_priority():
    plan = pr.plan_of_work(CLS)
    by_pattern = {}
    for item in plan:
        by_pattern.setdefault(item["pattern"], []).append(item["category"])
    assert by_pattern["A"] == ["canonical", "skill", "exercise"]   # Missing = P0
    assert by_pattern["B"] == ["canonical", "exercise"]            # Partial high = P1
    assert by_pattern["C"] == ["canonical"]                        # Partial medium = P2
    assert "D" not in by_pattern                                    # Exists: nothing
    assert "E" not in by_pattern                                    # Better: nothing


def test_plan_of_work_orders_priority_ascending_within_category():
    plan = pr.plan_of_work(CLS)
    canonical = [item for item in plan if item["category"] == "canonical"]
    assert [item["pattern"] for item in canonical] == ["A", "B", "C"]   # P0, P1, P2
    assert [item["priority"] for item in canonical] == ["P0", "P1", "P2"]


def test_plan_of_work_is_stable_in_fase2_order():
    cls = [{"pattern": "X", "verdict": "Missing"}, {"pattern": "Y", "verdict": "Missing"}]
    plan = pr.plan_of_work(cls)
    exercises = [i for i in plan if i["category"] == "exercise"]
    assert [i["pattern"] for i in exercises] == ["X", "Y"]


def test_plan_of_work_empty_when_nothing_eligible():
    assert pr.plan_of_work([{"pattern": "D", "verdict": "Exists"}]) == []


def test_skip_reason_names_the_verdict_policy():
    assert "Already Exists" in pr.skip_reason("Exists")
    assert "Better Implementation" in pr.skip_reason("Better")
