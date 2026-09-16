#!/usr/bin/env python3
"""Unit tests for the Fase 4 flow (#263): quarantine write, promotion, and the
governed generate→quarantine→gates→promote loop with every external call faked."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import phase4_flow as flow  # noqa: E402
import serialize  # noqa: E402

PATTERN = {"name": "X", "problem": "p", "mechanism": "m", "tradeoffs": "t"}
PKG = "2026-09-15-pkg"
INDEX = {"records": {"r1": {"path": "docs/canonical/existing.md", "vector": [1.0, 0.0]}}}


def _artifact(kind: str, dest: str) -> dict:
    base = {"type": kind, "pattern": "X", "phase3_verdict": "Missing", "priority": "P0",
            "title": "T", "content": "BODY", "source": "s--v.md",
            "last_updated": "2026-09-15", "intended_destination": dest}
    if kind == "skill":
        base.update(name="X", description="d")
    if kind == "exercise":
        base.update(level=3, level_dir="03-nivel-3-advanced-architecture", number=12)
    return base


# ── quarantine write ───────────────────────────────────────────────────────
@pytest.mark.parametrize("kind,dest", [
    ("canonical", "docs/canonical/x.md"),
    ("skill", ".opencode/skills/x/SKILL.md"),
    ("exercise", "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-12-x.md"),
])
def test_write_quarantined_writes_only_under_quarantine(tmp_path, kind, dest):
    art = _artifact(kind, dest)
    rel = flow.write_quarantined(tmp_path, PKG, art)
    assert rel == f"docs/analysis/{PKG}/proposed/{dest}"
    assert (tmp_path / rel).is_file()
    assert art["quarantine_path"] == rel
    # the authoritative layers are NEVER touched by the quarantine write
    assert not (tmp_path / "docs" / "canonical").exists()
    assert not (tmp_path / "curriculum").exists()
    assert not (tmp_path / ".opencode").exists()


def test_write_quarantined_rejects_escape(tmp_path):
    art = _artifact("canonical", "../../docs/canonical/x.md")
    with pytest.raises(ValueError):
        flow.write_quarantined(tmp_path, PKG, art)
    assert not (tmp_path / "docs").exists()


def test_quarantined_markdown_is_validator_compliant(tmp_path):
    """Every quarantined .md lives under docs/analysis/ → needs type/aliases/relates-to."""
    for kind, dest in [("canonical", "docs/canonical/x.md"),
                       ("skill", ".opencode/skills/x/SKILL.md"),
                       ("exercise", "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-12-x.md")]:
        art = _artifact(kind, dest)
        rel = flow.write_quarantined(tmp_path, PKG, art)
        fm, _ = serialize.split_frontmatter((tmp_path / rel).read_text(encoding="utf-8"))
        assert fm is not None, kind
        assert fm.get("type"), kind                     # Check 2: type present
        assert fm.get("aliases"), kind                  # Check 12: non-empty
        assert "relates-to" in fm, kind                 # Check 11: present


# ── promotion ──────────────────────────────────────────────────────────────
def test_promote_moves_accepted_artifact(tmp_path):
    art = _artifact("canonical", "docs/canonical/x.md")
    flow.write_quarantined(tmp_path, PKG, art)
    dest = flow.promote(tmp_path, PKG, art)
    assert dest == "docs/canonical/x.md"
    assert (tmp_path / dest).is_file()
    assert not (tmp_path / art["quarantine_path"]).exists()   # moved, not copied


def test_promote_refuses_occupied_destination(tmp_path):
    art = _artifact("canonical", "docs/canonical/x.md")
    flow.write_quarantined(tmp_path, PKG, art)
    dest = tmp_path / "docs" / "canonical" / "x.md"
    dest.parent.mkdir(parents=True)
    dest.write_text("authoritative", encoding="utf-8")
    with pytest.raises(ValueError):
        flow.promote(tmp_path, PKG, art)
    assert dest.read_text(encoding="utf-8") == "authoritative"   # untouched
    assert (tmp_path / art["quarantine_path"]).is_file()          # copy intact


def test_promote_refuses_missing_quarantine_copy(tmp_path):
    art = _artifact("skill", ".opencode/skills/x/SKILL.md")     # never quarantined
    with pytest.raises(ValueError):
        flow.promote(tmp_path, PKG, art)


# ── the governed loop (all externals faked) ────────────────────────────────
def _fake_zai(messages, key):
    system = messages[0]["content"]
    if "skill de implementação" in system:
        return {"name": "X", "description": "triggers", "body": "## What I Do\nB"}
    if "exercício hands-on" in system:
        return {"title": "Exercício X", "body": "prólogo + asserts"}
    return {"title": "Doc X", "body": "## Problema\nB"}


def _pass_eval(messages, key):
    return {"scores": {"fidelity": 5, "evidence": 5, "non_duplication": 5, "format": 5},
            "rationale": "ok"}


def _fail_eval(messages, key):
    return {"scores": {"fidelity": 0, "evidence": 0, "non_duplication": 0, "format": 0},
            "rationale": "invenção"}


def _embed_orthogonal(texts, key):
    return [[0.0, 1.0] for _ in texts]


CLS = [{"pattern": "X", "verdict": "Missing", "evidence": [], "verified": True},
       {"pattern": "E", "verdict": "Exists", "evidence": [{"file": "a.py", "line": 1}],
        "verified": True}]
PATTERNS = [PATTERN, {"name": "E", "problem": "pe", "mechanism": "me", "tradeoffs": "te"}]
EXTRACTION = {"thesis": "t", "video_id": "v"}


def _run(tmp_path, *, eval_client, classifications=CLS):
    return flow.run_fase4(
        tmp_path, PKG, classifications, PATTERNS, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=_fake_zai, eval_client=eval_client, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True, today="2026-09-15")


def test_run_fase4_generates_all_three_categories_and_promotes_on_pass(tmp_path):
    result = _run(tmp_path, eval_client=_pass_eval)
    # Missing = P0 → canonical + skill + exercise, all gates pass → promoted
    assert sorted(result["promoted"]) == sorted([
        "docs/canonical/x.md",
        ".opencode/skills/x/SKILL.md",
        "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-01-x.md",
    ])
    assert result["held"] == []
    for rel in result["promoted"]:
        assert (tmp_path / rel).is_file()
    # Exists generates nothing but is recorded as skipped in the manifest
    assert [s["pattern"] for s in result["manifest"]["skipped"]["already_exists"]] == ["E"]
    # the manifest files (Fase-5 contract) are written into the package dir
    pkg = tmp_path / "docs" / "analysis" / PKG
    assert (pkg / f"{PKG}-artifacts.yaml").is_file()
    assert (pkg / f"{PKG}-artifacts.md").is_file()
    assert result["manifest"]["gate"]["artifacts_count"] == {
        "canonical_docs": 1, "skills": 1, "exercises": 1}


def test_run_fase4_holds_failed_gate_in_quarantine_and_never_promotes(tmp_path):
    result = _run(tmp_path, eval_client=_fail_eval)
    assert result["promoted"] == []
    assert len(result["held"]) == 3
    assert all("evaluator adversarial abaixo do corte" in h["reasons"] for h in result["held"])
    # the authoritative layers stay untouched; the copies remain in quarantine
    assert not (tmp_path / "docs" / "canonical").exists()
    assert not (tmp_path / ".opencode").exists()
    assert not (tmp_path / "curriculum").exists()
    quarantine_root = tmp_path / "docs" / "analysis" / PKG / "proposed"
    assert len(list(quarantine_root.rglob("*.md"))) == 3
    [skill_row] = result["manifest"]["artifacts"]["skills"]
    assert skill_row["status"] == "quarantined" and skill_row["reasons"]


def test_run_fase4_citations_gate_fails_closed_without_verified_flag(tmp_path):
    cls = [{"pattern": "X", "verdict": "Missing", "evidence": []}]   # no `verified`
    result = _run(tmp_path, eval_client=_pass_eval, classifications=cls)
    assert result["promoted"] == []
    assert all("grep-verify de citações falhou" in h["reasons"] for h in result["held"])


def test_run_fase4_exercise_numbering_continues_existing(tmp_path):
    exercises = tmp_path / "curriculum" / "03-nivel-3-advanced-architecture" / "exercises"
    exercises.mkdir(parents=True)
    (exercises / "exercise-07.md").write_text("x", encoding="utf-8")
    result = _run(tmp_path, eval_client=_pass_eval)
    assert "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-08-x.md" \
        in result["promoted"]


def test_run_fase4_no_eligible_work_writes_empty_manifest(tmp_path):
    cls = [{"pattern": "E", "verdict": "Exists", "evidence": [], "verified": True}]
    result = _run(tmp_path, eval_client=_pass_eval, classifications=cls)
    assert result["promoted"] == [] and result["held"] == []
    assert result["manifest"]["gate"]["artifacts_count"]["canonical_docs"] == 0
    assert (tmp_path / "docs" / "analysis" / PKG / f"{PKG}-artifacts.yaml").is_file()


# ── destination-scoped validation runs BEFORE promotion ────────────────────
def _zai_with_canonical_body(body: str):
    def client(messages, key):
        system = messages[0]["content"]
        if "skill de implementação" in system:
            return {"name": "X", "description": "triggers", "body": "## What I Do\nB"}
        if "exercício hands-on" in system:
            return {"title": "Exercício X", "body": "prólogo + asserts"}
        return {"title": "Doc X", "body": body}
    return client


def _run_with(tmp_path, zai_client):
    return flow.run_fase4(
        tmp_path, PKG, CLS, PATTERNS, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=zai_client, eval_client=_pass_eval, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True, today="2026-09-15")


def test_run_fase4_holds_canonical_doc_that_violates_a_canonical_scoped_check(tmp_path):
    """A raw markdown link only violates validate-obsidian at docs/canonical/ — the
    quarantined copy never trips it, so the gate must run at the destination."""
    result = _run_with(tmp_path, _zai_with_canonical_body("veja [o doc](outro.md)"))
    assert "docs/canonical/x.md" not in result["promoted"]
    assert not (tmp_path / "docs" / "canonical").exists()
    [held] = [h for h in result["held"] if h["path"] == "docs/canonical/x.md"]
    assert "convenções obsidian no destino falharam" in held["reasons"]
    assert any("link markdown cru" in r for r in held["reasons"])
    # the clean skill/exercise from the same run still promote
    assert ".opencode/skills/x/SKILL.md" in result["promoted"]


def test_run_fase4_promotes_a_clean_canonical_doc(tmp_path):
    result = _run_with(tmp_path, _zai_with_canonical_body("apenas prosa mecanicista."))
    assert "docs/canonical/x.md" in result["promoted"]
    assert (tmp_path / "docs" / "canonical" / "x.md").is_file()


# ── fail-closed promotion refusals are contained ──────────────────────────
def test_run_fase4_occupied_destination_holds_only_that_artifact(tmp_path):
    canonical = tmp_path / "docs" / "canonical"
    canonical.mkdir(parents=True)
    (canonical / "x.md").write_text("authoritative", encoding="utf-8")
    result = _run(tmp_path, eval_client=_pass_eval)
    assert (canonical / "x.md").read_text(encoding="utf-8") == "authoritative"
    [held] = [h for h in result["held"] if h["path"] == "docs/canonical/x.md"]
    assert any("promotion refused" in r for r in held["reasons"])
    # the run still finishes: the other artifacts promote and the manifest is written
    assert ".opencode/skills/x/SKILL.md" in result["promoted"]
    assert (tmp_path / "docs" / "analysis" / PKG / f"{PKG}-artifacts.yaml").is_file()


# ── quarantine path collisions ────────────────────────────────────────────
def test_run_fase4_holds_the_later_artifact_on_a_destination_collision(tmp_path):
    """Two pattern names slugifying to the same destination must not overwrite each
    other's quarantined copy (which would promote the wrong content)."""
    cls = [{"pattern": "Sub-Agents", "verdict": "Partial", "value": "medium",
            "evidence": [], "verified": True},
           {"pattern": "Sub Agents", "verdict": "Partial", "value": "medium",
            "evidence": [], "verified": True}]
    patterns = [{"name": "Sub-Agents", "problem": "p", "mechanism": "m", "tradeoffs": "t"},
                {"name": "Sub Agents", "problem": "p2", "mechanism": "m2", "tradeoffs": "t2"}]


    def echoing_zai(messages, key):
        user = messages[1]["content"]
        name = "Sub-Agents" if "nome: Sub-Agents" in user else "Sub Agents"
        return {"title": f"Doc {name}", "body": f"corpo de {name}"}

    result = flow.run_fase4(
        tmp_path, PKG, cls, patterns, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=echoing_zai, eval_client=_pass_eval, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True, today="2026-09-15")
    assert result["promoted"] == ["docs/canonical/sub-agents.md"]
    [held] = result["held"]
    assert held["path"] == "docs/canonical/sub-agents.md"
    assert any("colisão de destino" in r for r in held["reasons"])
    # the promoted file is the FIRST pattern's content, and nothing is left behind
    promoted_text = (tmp_path / "docs" / "canonical" / "sub-agents.md").read_text(encoding="utf-8")
    assert "corpo de Sub-Agents" in promoted_text and "corpo de Sub Agents" not in promoted_text
    assert list((tmp_path / "docs" / "analysis" / PKG / "proposed").rglob("*.md")) == []
    assert [r["pattern"] for r in result["manifest"]["artifacts"]["canonical_docs"]] == \
        ["Sub-Agents", "Sub Agents"]
