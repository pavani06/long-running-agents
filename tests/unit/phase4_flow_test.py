#!/usr/bin/env python3
"""Unit tests for the Fase 4 flow (#263): quarantine write, promotion, and the
governed generate→quarantine→gates→promote loop with every external call faked."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from markdown_frontmatter import split_frontmatter  # noqa: E402

import phase4_flow as flow  # noqa: E402
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
        fm, _ = split_frontmatter((tmp_path / rel).read_text(encoding="utf-8"))
        assert fm is not None, kind
        assert fm.get("type"), kind                     # Check 2: type present
        assert fm.get("aliases"), kind                  # Check 12: non-empty
        assert "relates-to" in fm, kind                 # Check 11: present


# ── promotion ──────────────────────────────────────────────────────────────
def test_promote_moves_accepted_artifact(tmp_path):
    art = _artifact("canonical", "docs/canonical/x.md")
    flow.write_quarantined(tmp_path, PKG, art)
    assert flow.promote(tmp_path, PKG, art) is None           # a plain move, no qualifier
    assert (tmp_path / "docs/canonical/x.md").is_file()
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


def test_promote_is_idempotent_when_the_destination_holds_the_same_content(tmp_path):
    """A re-run over a source a prior run already promoted is the same landing, not
    a refusal — the manifest must not call a live file quarantined."""
    art = _artifact("canonical", "docs/canonical/x.md")
    flow.write_quarantined(tmp_path, PKG, art)
    flow.promote(tmp_path, PKG, art)
    again = _artifact("canonical", "docs/canonical/x.md")
    flow.write_quarantined(tmp_path, PKG, again)
    assert flow.promote(tmp_path, PKG, again) == flow.ALREADY_AT_DESTINATION
    assert (tmp_path / "docs/canonical/x.md").is_file()
    assert not (tmp_path / again["quarantine_path"]).exists()


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
    return {"available": True, "violations": []}


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
        return {"available": True, "violations": []}

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
    must be held, never promoted on the strength of the quarantine-path run, and the
    validator's own violation text must reach the manifest."""
    violation = "docs/canonical/x.md:9 — raw markdown link (raw-links)"
    result = _run_with_destination_gate(tmp_path, lambda root, dest, text: {
        "available": True,
        "violations": [violation] if dest.startswith("docs/canonical/") else []})
    assert "docs/canonical/x.md" not in result["promoted"]
    assert not (tmp_path / "docs" / "canonical").exists()
    [held] = [h for h in result["held"] if h["path"] == "docs/canonical/x.md"]
    assert "convenções obsidian no destino falharam" in held["reasons"]
    assert violation in held["reasons"]
    [row] = result["manifest"]["artifacts"]["canonical_docs"]
    assert row["status"] == "quarantined" and violation in row["reasons"]
    # the artifacts it accepts still promote
    assert ".opencode/skills/x/SKILL.md" in result["promoted"]


def test_run_fase4_unavailable_validator_is_not_reported_as_a_content_violation(tmp_path):
    """Fail-closed, but the manifest must not claim the content breaks conventions
    when the toolchain simply could not run."""
    result = _run_with_destination_gate(
        tmp_path, lambda root, dest, text: {"available": False, "violations": []})
    assert result["promoted"] == []
    for held in result["held"]:
        assert "validador de destino indisponível — conteúdo não verificado" in held["reasons"]
        assert "convenções obsidian no destino falharam" not in held["reasons"]
    assert not (tmp_path / "docs" / "canonical").exists()


def test_run_fase4_blocks_promotion_when_the_real_validator_cannot_run(tmp_path):
    """The default gate shells out to the real validator, absent from this bare tmp
    repo, so nothing may be promoted."""
    result = flow.run_fase4(
        tmp_path, PKG, CLS, PATTERNS, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=_fake_zai, eval_client=_pass_eval, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True, today="2026-09-15")
    assert result["promoted"] == []
    assert all("validador de destino indisponível — conteúdo não verificado" in h["reasons"]
               for h in result["held"])
    assert not (tmp_path / "docs" / "canonical").exists()
    assert list(tmp_path.glob(".validate-destination-*")) == []   # root cleaned up


# ── the destination gate delegates to the real validator ───────────────────
VALIDATOR_AVAILABLE = (ROOT / "scripts" / "validate-obsidian.ts").is_file() and \
    (ROOT / "node_modules" / "@pavani_org" / "obsidian-eval").is_dir()


def test_validate_destination_reports_unavailable_without_the_validator(tmp_path):
    assert spine.validate_destination(
        tmp_path, "docs/canonical/x.md", "---\ntype: canonical\n---\n") == {
            "available": False, "violations": []}


def _canonical_markdown(body: str) -> str:
    import phase4_create
    return phase4_create.render({
        "type": "canonical", "pattern": "X", "phase3_verdict": "Missing",
        "title": "T", "content": body, "source": "s--v.md",
        "last_updated": "2026-09-15", "intended_destination": "docs/canonical/x.md"})


@pytest.mark.validator_integration
@pytest.mark.skipif(not VALIDATOR_AVAILABLE, reason="validate-obsidian.ts deps not installed")
def test_validate_destination_accepts_clean_generated_prose():
    assert spine.validate_destination(
        ROOT, "docs/canonical/x.md", _canonical_markdown("apenas prosa.")) == {
            "available": True, "violations": []}


@pytest.mark.validator_integration
@pytest.mark.skipif(not VALIDATOR_AVAILABLE, reason="validate-obsidian.ts deps not installed")
@pytest.mark.parametrize("body,check", [("veja [o doc](outro.md)", "raw-links"),
                                        ("veja [[agent-loop]]", "broken-wikilinks")])
def test_validate_destination_rejects_links_in_generated_canonical_bodies(body, check):
    """Raw links and wikilinks are violations only at docs/canonical/ (Checks 5/6).
    The wikilink verdict is deliberately stricter than the repo-wide run: the root
    carries no vault context, and generated pre-review content must not link at all."""
    outcome = spine.validate_destination(ROOT, "docs/canonical/x.md", _canonical_markdown(body))
    assert outcome["available"] is True
    assert any(check in v for v in outcome["violations"]), outcome["violations"]



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


# ── partial failure and retry (the manifest never lies about a landing) ─────
def _run_with_eval(tmp_path, eval_client, classifications=CLS, patterns=PATTERNS,
                   today="2026-09-15"):
    return flow.run_fase4(
        tmp_path, PKG, classifications, patterns, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=_fake_zai, eval_client=eval_client, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True, validate_destination_fn=_destination_ok,
        today=today)


def test_run_fase4_contains_a_provider_failure_and_still_writes_the_manifest(tmp_path):
    """A transient provider error on one artifact must not abandon the run: that
    artifact is held with the error, the rest land, and the manifest says the
    phase did not complete."""
    def flaky_eval(messages, key):
        if "Exercício X" in str(messages):
            raise RuntimeError("openai: connection reset")
        return _pass_eval(messages, key)

    result = _run_with_eval(tmp_path, flaky_eval)
    assert "docs/canonical/x.md" in result["promoted"]
    assert ".opencode/skills/x/SKILL.md" in result["promoted"]
    exercise = "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-01-x.md"
    [held] = [h for h in result["held"] if h["path"] == exercise]
    assert any("connection reset" in r for r in held["reasons"])
    assert result["manifest"]["gate"]["phase4_complete"] is False
    assert (tmp_path / "docs" / "analysis" / PKG / f"{PKG}-artifacts.yaml").is_file()
    [row] = result["manifest"]["artifacts"]["exercises"]
    assert row["status"] == "quarantined" and row["reasons"]


EXERCISES = "curriculum/03-nivel-3-advanced-architecture/exercises"


def test_run_fase4_rerun_over_already_promoted_content_records_it_promoted(tmp_path):
    """The regression: run 1 promotes, run 2 regenerates the same content and must
    NOT record the live file as quarantined for Fase 5 to skip."""
    first = _run_with_eval(tmp_path, _pass_eval)
    assert "docs/canonical/x.md" in first["promoted"]
    second = _run_with_eval(tmp_path, _pass_eval)
    assert "docs/canonical/x.md" in second["promoted"]
    assert second["held"] == []
    assert second["manifest"]["gate"]["phase4_complete"] is True
    for key in ("canonical_docs", "skills", "exercises"):
        [row] = second["manifest"]["artifacts"][key]
        assert row["status"] == "promoted", key
        assert flow.ALREADY_AT_DESTINATION in row["reasons"], key


def test_run_fase4_rerun_does_not_duplicate_an_exercise_into_the_curriculum(tmp_path):
    """Exercise filenames carry an allocated number, so a re-run would otherwise take
    the next free number and write a byte-identical second copy into curriculum/."""
    first = _run_with_eval(tmp_path, _pass_eval)
    assert f"{EXERCISES}/exercise-01-x.md" in first["promoted"]
    second = _run_with_eval(tmp_path, _pass_eval)
    # the authoritative layer still holds exactly one exercise, the original one
    assert [p.name for p in sorted((tmp_path / EXERCISES).glob("*.md"))] == \
        ["exercise-01-x.md"]
    assert second["promoted"].count(f"{EXERCISES}/exercise-01-x.md") == 1
    assert not any("exercise-02" in path for path in second["promoted"])
    [row] = second["manifest"]["artifacts"]["exercises"]
    assert row["path"] == f"{EXERCISES}/exercise-01-x.md"
    assert row["status"] == "promoted"
    assert flow.ALREADY_AT_DESTINATION in row["reasons"]


def test_run_fase4_rerun_on_a_later_day_still_recognises_its_own_landing(tmp_path):
    """Only the canonical renderer stamps `last_updated: <today>`, so a re-run on any
    later day differs from its own promoted file by exactly that line. It is the same
    landing, and the Fase-5 contract must not call a live authoritative file held."""
    _run_with_eval(tmp_path, _pass_eval, today="2026-09-15")
    live = tmp_path / "docs" / "canonical" / "x.md"
    day_one = live.read_text(encoding="utf-8")
    assert "last_updated: '2026-09-15'" in day_one

    later = _run_with_eval(tmp_path, _pass_eval, today="2026-09-20")
    assert later["held"] == []
    for key in ("canonical_docs", "skills", "exercises"):
        [row] = later["manifest"]["artifacts"][key]
        assert row["status"] == "promoted", key
        assert flow.ALREADY_AT_DESTINATION in row["reasons"], key
        assert "quarantine_path" not in row, key
    # the authoritative file is left exactly as day one wrote it — no rewrite
    assert live.read_text(encoding="utf-8") == day_one
    assert sorted(p.name for p in (tmp_path / EXERCISES).glob("*.md")) == ["exercise-01-x.md"]
    assert list((tmp_path / "docs" / "analysis" / PKG / "proposed").rglob("*.md")) == []


def test_run_fase4_rerun_with_a_changed_body_is_still_refused(tmp_path):
    """Normalising the date must not blunt the gate: a real content change at an
    occupied destination is still a fail-closed refusal."""
    _run_with_eval(tmp_path, _pass_eval, today="2026-09-15")

    def different_zai(messages, key):
        reply = _fake_zai(messages, key)
        if "body" in reply and "Problema" in reply["body"]:
            reply["body"] = "## Problema\nCORPO DIFERENTE"
        return reply

    later = flow.run_fase4(
        tmp_path, PKG, CLS, PATTERNS, EXTRACTION, INDEX,
        openai_key="O", zai_key="Z", source_file="s--v.md",
        zai_client=different_zai, eval_client=_pass_eval, embed_fn=_embed_orthogonal,
        validate_fn=lambda root: True, validate_destination_fn=_destination_ok,
        today="2026-09-20")
    [held] = [h for h in later["held"] if h["path"] == "docs/canonical/x.md"]
    assert any("promotion refused" in r for r in held["reasons"])
    assert "CORPO DIFERENTE" not in (tmp_path / "docs/canonical/x.md").read_text(encoding="utf-8")


def test_run_fase4_numbers_a_genuinely_new_exercise_after_the_existing_ones(tmp_path):
    """Content matching must not stop a DIFFERENT exercise from getting its own slot."""
    exercises = tmp_path / EXERCISES
    exercises.mkdir(parents=True)
    (exercises / "exercise-01-other.md").write_text("outro exercício", encoding="utf-8")
    result = _run_with_eval(tmp_path, _pass_eval)
    assert f"{EXERCISES}/exercise-02-x.md" in result["promoted"]
    assert (exercises / "exercise-01-other.md").read_text(encoding="utf-8") == "outro exercício"


def test_run_fase4_rerun_with_different_content_at_the_destination_stays_held(tmp_path):
    """A destination occupied by DIFFERENT content is still a fail-closed refusal."""
    canonical = tmp_path / "docs" / "canonical"
    canonical.mkdir(parents=True)
    (canonical / "x.md").write_text("authoritative", encoding="utf-8")
    result = _run_with_eval(tmp_path, _pass_eval)
    assert (canonical / "x.md").read_text(encoding="utf-8") == "authoritative"
    [held] = [h for h in result["held"] if h["path"] == "docs/canonical/x.md"]
    assert any("promotion refused" in r for r in held["reasons"])
    assert result["manifest"]["gate"]["phase4_complete"] is True   # a refusal is terminal
