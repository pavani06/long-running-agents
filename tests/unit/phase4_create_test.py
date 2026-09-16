#!/usr/bin/env python3
"""Unit tests for Fase 4 creation (#263 slice). Pure parts + the never-canonical
invariant; no network."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import phase4_create as f4  # noqa: E402
import serialize  # noqa: E402
from glm import GLMError  # noqa: E402

PATTERN = {"name": "Idempotent Diff Pipeline", "problem": "reprocessing wastes cost",
           "mechanism": "hash-gated re-embed", "tradeoffs": "staleness window"}


def test_slugify():
    assert f4.slugify("Idempotent Diff Pipeline") == "idempotent-diff-pipeline"
    assert f4.slugify("  A/B  test!! ") == "a-b-test"
    assert f4.slugify("") == "proposta"


def test_build_messages_carries_pattern_and_context():
    msgs = f4.build_messages(PATTERN, "SRC-CONTEXT")
    assert msgs[0]["role"] == "system" and "AUSENTE" in msgs[0]["content"]
    u = msgs[1]["content"]
    assert "Idempotent Diff Pipeline" in u and "hash-gated re-embed" in u and "SRC-CONTEXT" in u


def test_build_messages_represents_repo_context_and_grounding_instruction():
    msgs = f4.build_messages(PATTERN, "SRC", repo_context="REPO-SECTION-AGENTS.md-marker")
    u = msgs[1]["content"]
    assert "CONTEXTO DO REPO" in u                        # the repo-context block is present
    assert "REPO-SECTION-AGENTS.md-marker" in u           # the retrieved context is threaded in
    assert "Como se aplicaria aqui" in u and "ancore em arquivos/mecanismos REAIS" in u


def test_build_messages_empty_repo_context_tells_model_to_say_so():
    u = f4.build_messages(PATTERN, "SRC", repo_context="")[1]["content"]
    assert "(nenhum contexto de repo recuperado)" in u    # graceful empty
    assert "diga isso explicitamente" in u                # instructed to admit no anchor, not invent


def test_create_threads_repo_context_into_the_prompt():
    seen = {}

    def fake_client(messages, key):
        seen["messages"] = messages
        return {"title": "T", "body": "B"}

    art = f4.create(PATTERN, slug="s", source_file="s--v.md", video_id="v", evidence=[],
                    source_context="SRC", repo_context="GROUNDING-FROM-RETRIEVER",
                    zai_key="KEY", client=fake_client, today="2026-09-15")
    assert art["type"] == "canonical"
    joined = seen["messages"][1]["content"]
    assert "GROUNDING-FROM-RETRIEVER" in joined           # repo_context reached the GLM prompt


def test_create_preserves_behavior_when_repo_context_empty():
    seen = {}

    def fake_client(messages, key):
        seen["messages"] = messages
        return {"title": "T", "body": "B"}

    art = f4.create(PATTERN, slug="s", source_file="s--v.md", video_id="v", evidence=[],
                    source_context="SRC", zai_key="KEY", client=fake_client, today="2026-09-15")
    assert art["type"] == "canonical" and art["title"] == "T"   # unchanged creation behavior
    assert "(nenhum contexto de repo recuperado)" in seen["messages"][1]["content"]


def test_parse_creation_ok():
    assert f4.parse_creation({"title": "T", "body": "B"}) == {"title": "T", "body": "B"}


def test_parse_creation_rejects_empty():
    for bad in ({"title": "", "body": "B"}, {"title": "T", "body": ""}, {"title": "T"}, {}):
        with pytest.raises(GLMError):
            f4.parse_creation(bad)


def test_intended_destination_is_the_canonical_write_target():
    # This is now WHERE F4 writes on the proposal branch (promotion = human merge).
    assert f4.intended_destination(PATTERN) == "docs/canonical/idempotent-diff-pipeline.md"


def _artifact(**over):
    base = dict(slug="s", source_file="s--v.md", video_id="v", pattern=PATTERN,
                verdict="Missing", evidence=[], creation={"title": "X", "body": "B"},
                last_updated="2026-09-15")
    base.update(over)
    return f4.proposed_artifact(**base)


def test_proposed_artifact_is_canonical_type_with_provenance():
    art = _artifact(evidence=[{"file": "x", "line": 1, "quote": "q"}],
                    creation={"title": "Proposed X", "body": "## Problema\n..."})
    for k in ("source", "slug", "video_id", "pattern", "phase3_verdict", "evidence",
              "intended_destination", "title", "content", "problem", "mechanism", "last_updated"):
        assert k in art
    assert art["type"] == "canonical"                      # the file IS the canonical artifact
    assert art["phase3_verdict"] == "Missing"
    assert art["intended_destination"] == "docs/canonical/idempotent-diff-pipeline.md"


def test_render_markdown_is_a_valid_canonical_doc():
    art = _artifact(creation={"title": "X", "body": "BODY-CONTENT"})
    md = f4.render_markdown(art)
    fm, _ = serialize.split_frontmatter(md)
    assert fm["type"] == "canonical"                       # Check 1: type present
    assert fm["aliases"] == ["idempotent diff pipeline"]   # Check 12: non-empty
    assert fm["relates-to"] == []                          # Check 11: present (empty, uncurated)
    assert str(fm["last_updated"]) == "2026-09-15"
    assert fm["sources"] == ["s--v.md"]
    assert "**Status:**" not in md                         # no transient lifecycle state — Git represents it
    assert "BODY-CONTENT" in md


def test_render_markdown_body_is_link_free():
    # docs/canonical/ CI flags raw md links (Check 5) and broken wikilinks (Check 6);
    # the template must not introduce either around the model body.
    art = _artifact(creation={"title": "T", "body": "prose only"})
    md = f4.render_markdown(art)
    assert "](" not in md.split("BODY", 1)[0]              # no markdown links in our scaffold
    assert "[[" not in md                                   # no wikilinks in our scaffold


def test_destination_path_is_the_canonical_target(tmp_path):
    p = f4.destination_path(tmp_path, PATTERN)
    rel = p.resolve().relative_to(tmp_path.resolve()).as_posix()
    assert rel == "docs/canonical/idempotent-diff-pipeline.md"


def test_assert_canonical_target_rejects_non_canonical():
    with pytest.raises(ValueError):
        f4._assert_canonical_target(Path("/repo/docs/analysis/s/x.md"), Path("/repo"),
                                    "docs/analysis/s/x.md")


def test_write_proposed_writes_the_canonical_target(tmp_path):
    art = _artifact()
    rel = f4.write_proposed(tmp_path, art, "s", PATTERN)
    # creation writes the canonical artifact at its destination (on the branch); promotion
    # to main is the human PR merge, not this write.
    assert rel == "docs/canonical/idempotent-diff-pipeline.md"
    assert (tmp_path / rel).is_file()
    assert not (tmp_path / "docs" / "analysis").exists()   # no leftover proposed/ path


# ── verdict-aware canonical path (P1/P2 = Partial → reframe/naming) ───────
def test_build_messages_partial_verdict_reframes_header():
    u = f4.build_messages(PATTERN, "SRC", verdict="Partial")[1]["content"]
    assert "PARCIALMENTE COBERTO" in u and "veredito Fase 3 = Partial" in u
    assert "PADRÃO AUSENTE" not in u


def test_build_messages_missing_verdict_is_byte_identical_to_default():
    assert (f4.build_messages(PATTERN, "SRC", verdict="Missing")
            == f4.build_messages(PATTERN, "SRC"))


def test_create_stamps_the_verdict():
    art = f4.create(PATTERN, slug="s", source_file="s--v.md", video_id="v", evidence=[],
                    source_context="SRC", zai_key="KEY", client=lambda m, k: {"title": "T", "body": "B"},
                    today="2026-09-15", verdict="Partial")
    assert art["phase3_verdict"] == "Partial"


def test_render_markdown_classification_is_verdict_aware():
    art = _artifact()
    art["phase3_verdict"] = "Partial"
    md = f4.render_markdown(art)
    assert "cobertura parcial no repo; proposta de reframe/naming" in md
    assert f4.render_markdown(_artifact()).count("Missing — ausente no repo") == 1


# ── skill generation (#263 remainder) ──────────────────────────────────────
def test_build_skill_messages_carries_pattern_and_grounding_rule():
    msgs = f4.build_skill_messages(PATTERN, "SRC-CTX", repo_context="REPO-ANCHOR")
    assert "skill de implementação" in msgs[0]["content"]
    u = msgs[1]["content"]
    assert "Idempotent Diff Pipeline" in u and "SRC-CTX" in u and "REPO-ANCHOR" in u
    assert "Implementation Rules" in u and "não invente arquivos" in u


def test_parse_skill_ok_and_rejects_missing_fields():
    ok = {"name": "N", "description": "D", "body": "B"}
    assert f4.parse_skill(ok) == ok
    for bad in ({"name": "", "description": "D", "body": "B"},
                {"name": "N", "description": "", "body": "B"},
                {"name": "N", "description": "D", "body": ""}, {"name": "N"}):
        with pytest.raises(GLMError):
            f4.parse_skill(bad)


def test_skill_destination_is_the_skills_layer():
    assert f4.skill_destination(PATTERN) == ".opencode/skills/idempotent-diff-pipeline/SKILL.md"


def _skill_artifact(**over):
    base = dict(slug="s", source_file="s--v.md", video_id="v", pattern=PATTERN,
                verdict="Missing", evidence=[], last_updated="2026-09-15",
                creation={"name": "Idempotent Diff Pipeline", "description": "triggers", "body": "## What I Do\nB"})
    base.update(over)
    return f4.proposed_skill_artifact(**base)


def test_render_skill_markdown_frontmatter_and_body():
    md = f4.render_skill_markdown(_skill_artifact())
    fm, body = serialize.split_frontmatter(md)
    # the layer's dominant schema (34/38 siblings): name/description/license/compatibility
    assert fm["name"] == "idempotent-diff-pipeline"     # byte-equal to the skill directory
    assert fm["name"] == f4.skill_destination(PATTERN).split("/")[-2]
    assert fm["description"] == "triggers"
    assert fm["license"] == "MIT" and fm["compatibility"] == "opencode"
    assert fm["metadata"]["title"] == "Idempotent Diff Pipeline"   # model's name kept as title
    # quarantine-compliance keys (the copy lives under docs/analysis/)
    assert fm["type"] == "skill" and fm["aliases"] and fm["relates-to"] == []
    assert "## What I Do" in body
    assert "[[" not in md and "](" not in md           # link-free scaffold


def test_create_skill_uses_the_injected_client():
    seen = {}

    def fake_client(messages, key):
        seen["m"] = messages
        return {"name": "N", "description": "D", "body": "B"}

    art = f4.create_skill(PATTERN, slug="s", source_file="s--v.md", video_id="v", evidence=[],
                          source_context="SRC", repo_context="GROUND", zai_key="KEY",
                          client=fake_client, today="2026-09-15")
    assert art["type"] == "skill" and art["title"] == "N" and art["description"] == "D"
    assert art["intended_destination"] == ".opencode/skills/idempotent-diff-pipeline/SKILL.md"
    assert "GROUND" in seen["m"][1]["content"]


# ── exercise generation (#263 remainder) ───────────────────────────────────
def test_build_exercise_messages_carries_format_and_assert_rules():
    msgs = f4.build_exercise_messages(PATTERN, "SRC", repo_context="REPO-ANCHOR")
    assert "exercício hands-on" in msgs[0]["content"]
    u = msgs[1]["content"]
    assert "Idempotent Diff Pipeline" in u and "REPO-ANCHOR" in u
    assert "asserts" in u and "falhar antes da implementação" in u


def test_parse_exercise_ok_and_rejects_missing_fields():
    assert f4.parse_exercise({"title": "T", "body": "B"}) == {"title": "T", "body": "B"}
    for bad in ({"title": "", "body": "B"}, {"title": "T", "body": ""}, {}):
        with pytest.raises(GLMError):
            f4.parse_exercise(bad)


def test_next_exercise_number_deterministic():
    assert f4.next_exercise_number([]) == 1
    assert f4.next_exercise_number(["exercise-01.md", "exercise-11-x.md", "solutions"]) == 12
    assert f4.next_exercise_number(["README.md"]) == 1


def test_exercise_destination_shape():
    assert (f4.exercise_destination(PATTERN, "03-nivel-3-advanced-architecture", 12)
            == "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-12-idempotent-diff-pipeline.md")


def _exercise_artifact(**over):
    base = dict(slug="s", source_file="s--v.md", video_id="v", pattern=PATTERN,
                verdict="Missing", evidence=[], last_updated="2026-09-15",
                level=3, level_dir="03-nivel-3-advanced-architecture", number=12,
                creation={"title": "Exercício X", "body": "prólogo"})
    base.update(over)
    return f4.proposed_exercise_artifact(**base)


def test_render_exercise_markdown_frontmatter_and_body():
    md = f4.render_exercise_markdown(_exercise_artifact())
    fm, body = serialize.split_frontmatter(md)
    assert fm["title"] == "Exercício X"
    assert fm["type"] == "exercise" and fm["level"] == 3     # Check 9: type present
    assert fm["tags"] and fm["aliases"]                      # Check 9/12
    assert fm["relates-to"] == []                            # Check 11
    assert "# Exercício X" in body and "prólogo" in body
    assert "[[" not in md


def test_create_exercise_stamps_orchestrator_decided_placement():
    art = f4.create_exercise(PATTERN, slug="s", source_file="s--v.md", video_id="v",
                             evidence=[], source_context="SRC", zai_key="KEY", level=3,
                             level_dir="03-nivel-3-advanced-architecture", number=8,
                             client=lambda m, k: {"title": "T", "body": "B"},
                             today="2026-09-15")
    assert art["type"] == "exercise" and art["level"] == 3 and art["number"] == 8
    assert art["intended_destination"].endswith("/exercises/exercise-08-idempotent-diff-pipeline.md")


# ── verdict threading into skills/exercises ────────────────────────────────
def test_skill_and_exercise_prompts_carry_the_classification_verdict():
    # `verdict` is a Fase-3 classification field, never a key of the pattern dict
    assert "veredito Fase 3 = Partial" in \
        f4.build_skill_messages(PATTERN, "SRC", verdict="Partial")[1]["content"]
    assert "veredito Fase 3 = Partial" in \
        f4.build_exercise_messages(PATTERN, "SRC", verdict="Partial")[1]["content"]


def test_create_skill_and_exercise_stamp_the_verdict():
    skill = f4.create_skill(PATTERN, slug="s", source_file="s--v.md", video_id="v", evidence=[],
                            source_context="SRC", zai_key="K", verdict="Partial",
                            client=lambda m, k: {"name": "N", "description": "D", "body": "B"},
                            today="2026-09-15")
    exercise = f4.create_exercise(PATTERN, slug="s", source_file="s--v.md", video_id="v",
                                  evidence=[], source_context="SRC", zai_key="K", level=3,
                                  level_dir="03-nivel-3-advanced-architecture", number=1,
                                  verdict="Partial", today="2026-09-15",
                                  client=lambda m, k: {"title": "T", "body": "B"})
    assert skill["phase3_verdict"] == "Partial" and exercise["phase3_verdict"] == "Partial"


# ── destination-scoped convention checks (pre-promotion gate) ──────────────
CANONICAL_DEST = "docs/canonical/idempotent-diff-pipeline.md"


def test_destination_violations_accepts_a_clean_canonical_doc():
    md = f4.render_markdown(_artifact(creation={"title": "X", "body": "apenas prosa."}))
    assert f4.destination_violations(CANONICAL_DEST, md) == []


def test_destination_violations_rejects_a_raw_markdown_link():
    md = f4.render_markdown(_artifact(creation={"title": "X", "body": "veja [o doc](outro.md)"}))
    problems = f4.destination_violations(CANONICAL_DEST, md)
    assert any("link markdown cru" in p for p in problems)


def test_destination_violations_ignores_links_inside_code_fences():
    body = "```\nveja [o doc](outro.md)\n```"
    md = f4.render_markdown(_artifact(creation={"title": "X", "body": body}))
    assert f4.destination_violations(CANONICAL_DEST, md) == []


def test_destination_violations_rejects_only_unresolvable_wikilinks():
    md = f4.render_markdown(_artifact(creation={"title": "X", "body": "veja [[outro]]"}))
    assert any("wikilink quebrado" in p for p in f4.destination_violations(CANONICAL_DEST, md))
    assert f4.destination_violations(CANONICAL_DEST, md,
                                     exists=lambda rel: rel == "outro.md") == []


def test_destination_violations_requires_canonical_frontmatter():
    assert f4.destination_violations(CANONICAL_DEST, "sem frontmatter") == \
        [f"{CANONICAL_DEST}: frontmatter YAML ausente"]
    no_type = "---\ntitle: X\naliases: [a]\nrelates-to: []\n---\n\nprosa"
    assert any("sem 'type'" in p for p in f4.destination_violations(CANONICAL_DEST, no_type))


def test_destination_violations_requires_curriculum_tags():
    dest = "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-01-x.md"
    assert f4.destination_violations(
        dest, f4.render_exercise_markdown(_exercise_artifact())) == []
    no_tags = "---\ntitle: X\ntype: exercise\naliases: [a]\nrelates-to: []\n---\n\nprosa"
    assert any("sem 'tags'" in p for p in f4.destination_violations(dest, no_tags))


def test_destination_violations_skips_unmonitored_destinations():
    # .opencode/skills/ is outside the validator's monitored dirs — nothing to check
    assert f4.destination_violations(".opencode/skills/x/SKILL.md", "qualquer [x](y.md)") == []
