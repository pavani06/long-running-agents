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
import spine  # noqa: E402

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


def _destination_ok(repo_root, destination, text):
    return True


def _run(tmp_path, *, eval_client, classifications=CLS):
    return flow.run_fase4(
        tmp_path, PKG, classifications, PATTERNS, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=_fake_zai, eval_client=eval_client, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True, validate_destination_fn=_destination_ok,
        today="2026-09-15")


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
def _run_with_destination_gate(tmp_path, validate_destination_fn):
    return flow.run_fase4(
        tmp_path, PKG, CLS, PATTERNS, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=_fake_zai, eval_client=_pass_eval, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True,
        validate_destination_fn=validate_destination_fn, today="2026-09-15")


def test_run_fase4_validates_each_artifact_at_its_intended_destination(tmp_path):
    seen = []

    def spy(repo_root, destination, text):
        seen.append((destination, text))
        return True

    _run_with_destination_gate(tmp_path, spy)
    # the validator sees the destination path, not the quarantine path, and the
    # rendered content that would land there
    assert sorted(d for d, _ in seen) == sorted([
        "docs/canonical/x.md", ".opencode/skills/x/SKILL.md",
        "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-01-x.md"])
    assert all(not d.startswith("docs/analysis/") for d, _ in seen)
    assert all(t.startswith("---\n") for _, t in seen)


def test_run_fase4_holds_the_artifact_its_destination_validation_rejects(tmp_path):
    """The canonical-scoped checks only fire at docs/canonical/ — a doc they reject
    must be held, never promoted on the strength of the quarantine-path run."""
    result = _run_with_destination_gate(
        tmp_path, lambda root, dest, text: not dest.startswith("docs/canonical/"))
    assert "docs/canonical/x.md" not in result["promoted"]
    assert not (tmp_path / "docs" / "canonical").exists()
    [held] = [h for h in result["held"] if h["path"] == "docs/canonical/x.md"]
    assert "convenções obsidian no destino falharam" in held["reasons"]
    # the artifacts it accepts still promote
    assert ".opencode/skills/x/SKILL.md" in result["promoted"]


def test_run_fase4_blocks_promotion_when_the_validator_cannot_run(tmp_path):
    """Fail-closed: the default gate runs the real validator, which is absent from
    this bare tmp repo, so nothing may be promoted."""
    result = flow.run_fase4(
        tmp_path, PKG, CLS, PATTERNS, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=_fake_zai, eval_client=_pass_eval, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True, today="2026-09-15")
    assert result["promoted"] == []
    assert all("convenções obsidian no destino falharam" in h["reasons"]
               for h in result["held"])
    assert not (tmp_path / "docs" / "canonical").exists()


# ── the destination gate delegates to the real validator ───────────────────
VALIDATOR_AVAILABLE = (ROOT / "scripts" / "validate-obsidian.ts").is_file() and \
    (ROOT / "node_modules" / "@pavani_org" / "obsidian-eval").is_dir()


def test_validate_destination_ok_fails_closed_without_the_validator(tmp_path):
    assert spine.validate_destination_ok(
        tmp_path, "docs/canonical/x.md", "---\ntype: canonical\n---\n") is False


@pytest.mark.skipif(not VALIDATOR_AVAILABLE, reason="validate-obsidian.ts deps not installed")
@pytest.mark.parametrize("body,expected", [("apenas prosa.", True),
                                           ("veja [o doc](outro.md)", False)])
def test_validate_destination_ok_runs_the_real_validator(body, expected):
    """A raw markdown link is a violation only at docs/canonical/ (Check 5); the
    verdict must come from validate-obsidian.ts itself, not a Python copy of it."""
    import phase4_create
    art = {"type": "canonical", "pattern": "X", "phase3_verdict": "Missing",
           "title": "T", "content": body, "source": "s--v.md",
           "last_updated": "2026-09-15", "intended_destination": "docs/canonical/x.md"}
    assert spine.validate_destination_ok(
        ROOT, "docs/canonical/x.md", phase4_create.render(art)) is expected



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
        validate_fn=lambda root: True, validate_destination_fn=_destination_ok,
        today="2026-09-15")
    assert result["promoted"] == ["docs/canonical/sub-agents.md"]
    [held] = result["held"]
    assert held["path"] == "docs/canonical/sub-agents.md"
    assert any("colisão de destino" in r for r in held["reasons"])
    # the promoted file is the FIRST pattern's content, and nothing is left behind
    promoted_text = (tmp_path / "docs" / "canonical" / "sub-agents.md").read_text(encoding="utf-8")
    assert "corpo de Sub-Agents" in promoted_text and "corpo de Sub Agents" not in promoted_text
    assert list((tmp_path / "docs" / "analysis" / PKG / "proposed").rglob("*.md")) == []
    promoted_row, held_row = result["manifest"]["artifacts"]["canonical_docs"]
    assert [promoted_row["pattern"], held_row["pattern"]] == ["Sub-Agents", "Sub Agents"]
    # a hold with no quarantined copy must not claim one in the Fase-5 contract
    assert "quarantine_path" not in held_row
