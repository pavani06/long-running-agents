#!/usr/bin/env python3
"""Unit tests for Fase 6 (#265): section splice over the manifest boundary.
Pure parts (localização de seção, splice, gates de diff) + run() com fakes
injetados sobre repo sintético; sem rede, sem GLM/OpenAI reais."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import artifact_manifest as am  # noqa: E402
import index_store  # noqa: E402
import phase6_splice as p6  # noqa: E402
from chunking import split_sections  # noqa: E402
from index_store import records_for  # noqa: E402

DOC = """---
title: Lição
type: curriculum-lesson
tags: []
---

# Lição

Intro da lição.

## Alavanca

Corpo da alavanca.

```python
# não é heading
x = 1
```

## ROI

Corpo do ROI.

## Alavanca

Segunda alavanca (ordinal 1).

Última seção sem heading seguinte.
"""


def _lines(text: str) -> list[str]:
    return text.split("\n")


class TestLocateSection:
    def test_range_basics(self):
        rng = p6.locate_section(DOC, "ROI")
        lines = _lines(DOC)
        assert lines[rng.start] == "## ROI"
        body = "\n".join(lines[rng.start + 1:rng.end])
        assert body.strip() == "Corpo do ROI."

    def test_fence_protects_heading(self):
        rng = p6.locate_section(DOC, "Alavanca", ordinal=0)
        nxt = p6.locate_section(DOC, "ROI")
        # a seção "Alavanca" (ordinal 0) atravessa o fence e termina no "## ROI"
        assert rng.end == nxt.start

    def test_duplicate_heading_ordinal(self):
        first = p6.locate_section(DOC, "Alavanca", ordinal=0)
        second = p6.locate_section(DOC, "Alavanca", ordinal=1)
        assert first.start < second.start
        assert second.end == len(_lines(DOC))  # vai até o EOF

    def test_not_found_fails_closed(self):
        with pytest.raises(ValueError, match="section not found"):
            p6.locate_section(DOC, "Inexistente")

    def test_frontmatter_coordinates(self):
        rng = p6.locate_section(DOC, "Alavanca", ordinal=0)
        lines = _lines(DOC)
        assert lines[rng.start] == "## Alavanca"
        assert lines[0] == "---"  # coordenadas incluem o frontmatter


class TestLocateById:
    def test_alignment_with_chunker_for_every_section(self):
        for rec in records_for("curriculum/x/lição.md", DOC):
            if rec.level == 0:
                continue
            rng, text = p6.locate_by_id(DOC, "curriculum/x/lição.md", rec.id)
            lines = _lines(DOC)
            assert lines[rng.start] == f"{'#' * rec.level} {rec.heading}"
            assert "\n".join(lines[rng.start:rng.end]).strip("\n") == rec.text
            assert text == rec.text

    def test_unknown_record_fails_closed(self):
        with pytest.raises(ValueError, match="index record not in current file"):
            p6.locate_by_id(DOC, "curriculum/x/lição.md", "curriculum/x/lição.md#2-nao-existe")


class TestApplySplice:
    def test_replaces_body_only(self):
        rng = p6.locate_section(DOC, "ROI")
        updated, status = p6.apply_splice(DOC, rng, "Novo corpo do ROI.")
        assert status == "changed"
        lines = _lines(updated)
        assert lines[rng.start] == "## ROI"
        assert "Novo corpo do ROI." in updated
        assert "Corpo do ROI." not in updated
        # fora da seção, byte a byte
        assert updated.split("## Alavanca")[0] == DOC.split("## Alavanca")[0]

    def test_idempotent_rerun_is_detected_noop(self):
        rng = p6.locate_section(DOC, "ROI")
        once, _ = p6.apply_splice(DOC, rng, "Corpo estável.")
        rng2 = p6.locate_section(once, "ROI")
        twice, status = p6.apply_splice(once, rng2, "Corpo estável.")
        assert status == "unchanged"
        assert twice == once

    def test_trailing_blanks_survive(self):
        text = "# T\n\n## A\ncorpo\n\n\n## B\nb\n"
        rng = p6.locate_section(text, "A")
        updated, status = p6.apply_splice(text, rng, "novo")
        assert status == "changed"
        assert "\n\n\n## B\n" in updated  # os blanks antes do próximo heading ficam


class TestDiffGates:
    def test_localized_ok(self):
        rng = p6.locate_section(DOC, "ROI")
        updated, _ = p6.apply_splice(DOC, rng, "novo corpo")
        b0, b1 = p6.body_range(rng, _lines(DOC))
        ok, violations = p6.localized_diff_ok(DOC, updated, b0, b1)
        assert ok and violations == []

    def test_localized_catches_out_of_range(self):
        tampered = DOC.replace("Intro da lição.", "Intro alterada.")
        rng = p6.locate_section(DOC, "ROI")
        b0, b1 = p6.body_range(rng, _lines(DOC))
        ok, violations = p6.localized_diff_ok(DOC, tampered, b0, b1)
        assert not ok
        assert any("fora da seção" in v for v in violations)

    def test_changed_paths_ok(self):
        ok, _ = p6.changed_paths_ok(["curriculum/03/x/lesson.md"], "curriculum/03/x/lesson.md")
        assert ok
        for changed in (["docs/canonical/foo.md"],
                        ["curriculum/03/x/lesson.md", "curriculum/03/x/new.md"],
                        ["docs/canonical/foo.md", "outro.md"]):
            ok, violations = p6.changed_paths_ok(changed, "curriculum/03/x/lesson.md")
            assert not ok and violations


class TestModelBoundary:
    def test_bounded_input_has_section_and_knowledge_only(self):
        msgs = p6.build_messages("ROI", "Corpo do ROI.", "Fonte promovida.", path="c/l.md")
        user = msgs[-1]["content"]
        assert "Corpo do ROI." in user
        assert "Fonte promovida." in user
        assert "Intro da lição." not in user  # o arquivo inteiro nunca vai

    def test_parse_replacement(self):
        assert p6.parse_replacement({"body": " novo\n"}) == "novo"
        with pytest.raises(ValueError):
            p6.parse_replacement({"body": "  "})
        with pytest.raises(ValueError):
            p6.parse_replacement({"other": 1})

    def test_body_with_heading_is_rejected(self):
        with pytest.raises(ValueError, match="heading ATX"):
            p6.parse_replacement({"body": "texto\n\n## Nova subseção\n\nmais"})

    def test_heading_inside_fence_is_allowed(self):
        body = "exemplo:\n\n```md\n## isto é código\n```\n\nfim"
        assert p6.parse_replacement({"body": body}) == body

    def test_body_opening_with_frontmatter_is_rejected(self):
        with pytest.raises(ValueError, match="frontmatter"):
            p6.parse_replacement({"body": "---\ntitle: x\n---\n\ncorpo"})


# ---------------------------------------------------------------- E2E (fakes)

SLUG = "2026-09-16-src"
CANONICAL = ("---\ntitle: Capability Escalation Ladder\ntype: canonical\n---\n"
             "# Capability Escalation Ladder\n\n"
             "## Problema\n\n Quando um agente falha, ordenar escalation por custo de teste.\n"
             "## Solução\n\n Rung por rung até o vencedor economico, nunca o primeiro que passa.\n")
BODY = ("Quando a tarefa reprova no eval, suba a escada em ordem de custo de teste: "
        "prompt, budget, depois decomposição — o rung vencedor é o economico. "
        "A escada de escalation ordena capability por custo de teste; o oposto de "
        "remove sem fallback. Referência: docs/canonical/capability-escalation-ladder.md.")
LESSON = ("---\ntitle: Harness Evolution\ntype: curriculum-lesson\ntags: []\n---\n"
          "# Harness Evolution\n\n## Visão Geral\n\nFases do harness.\n\n"
          "## ROI de um Componente\n\nROI corrente sem a escada de escalation.\n\n"
          "## Fase 4: REMOVE\n\nRemoção segura.\n")


def _embed_fn():
    vocab = ["escalation", "harness", "roi", "remove", "capability", "ladder",
             "eval", "budget", "trace", "fallback", "rung", "economic"]

    def embed(texts, _key):
        out = []
        for t in texts:
            toks = [w.strip(".,:;!?()[]\"'") for w in t.lower().split()]
            out.append([float(toks.count(w)) for w in vocab])
        return out
    return embed


def _repo(tmp_path: Path, *, lesson: str = LESSON, extra_level2: bool = False) -> Path:
    (tmp_path / "docs" / "canonical").mkdir(parents=True)
    (tmp_path / "docs" / "canonical" / "capability-escalation-ladder.md").write_text(CANONICAL)
    level3 = tmp_path / "curriculum" / "03-nivel-3-advanced-architecture"
    level3.mkdir(parents=True)
    (level3 / "05-harness-evolution.md").write_text(lesson)
    if extra_level2:
        level2 = tmp_path / "curriculum" / "02-nivel-2-practical-patterns"
        level2.mkdir(parents=True)
        (level2 / "04-trace-reading.md").write_text(lesson)   # decoy idêntico
    return tmp_path


def _index(repo: Path, embed) -> dict:
    index: dict = {}
    for md in sorted(repo.glob("curriculum/*/*.md")) + sorted(repo.glob("docs/canonical/*.md")):
        rel = md.relative_to(repo).as_posix()
        recs = records_for(rel, md.read_text(encoding="utf-8"))
        vecs = {r.id: v for r, v in zip(recs, embed([r.text for r in recs], "k"))}
        index = index_store.merge_index(index, {rel: recs}, [], vecs)
    return index


def _manifest(path: Path, *, category: str = "canonical", dest: str,
              level=None) -> Path:
    artifact = {"intended_destination": dest, "pattern": "Capability Escalation Ladder",
                "phase3_verdict": "Missing", "title": "Capability Escalation Ladder",
                "content": CANONICAL}
    if category == "exercise":
        artifact["level"] = level
    manifest = am.build_manifest(
        SLUG, "2026-09-16",
        [{"pattern": "Capability Escalation Ladder", "verdict": "Missing", "evidence": []}],
        [{"category": category, "artifact": artifact, "accepted": True, "reasons": []}],
        {category}, complete=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(am.manifest_yaml(manifest), encoding="utf-8")
    return path


def _run(repo: Path, manifest: Path, *, splice_body: str = BODY, eval_ok: bool = True,
         changed: list[str] | None = None, **kw):
    """`changed` is what git would report as the splice's own worktree delta;
    absent a path scenario, a splice changes exactly the file it wrote."""
    calls: list[list[dict]] = []

    def fake_splice(messages, _key):
        calls.append(messages)
        return {"body": splice_body}

    def fake_eval(_messages, _key):
        scores = {"fidelity": 5, "evidence": 5, "non_duplication": 5, "format": 5} \
            if eval_ok else {"fidelity": 0, "evidence": 0, "non_duplication": 0, "format": 0}
        return {"scores": scores, "rationale": "ok" if eval_ok else "ruim"}

    embed = _embed_fn()
    out = p6.run(repo, manifest, zai_key="z", openai_key="o", index=_index(repo, embed),
                 changed_paths_fn=lambda target: [target] if changed is None else changed,
                 embed_fn=embed, splice_client=fake_splice, eval_client=fake_eval,
                 validate_fn=lambda _root: True,
                 validate_destination_fn=lambda _r, _d, _t: {"available": True, "violations": []},
                 **kw)
    return out, calls


def test_end_to_end_applied(tmp_path):
    repo = _repo(tmp_path)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         dest="docs/canonical/capability-escalation-ladder.md")
    target = repo / "curriculum" / "03-nivel-3-advanced-architecture" / "05-harness-evolution.md"
    before = target.read_text(encoding="utf-8")

    out, calls = _run(repo, manifest, changed=[target.relative_to(repo).as_posix()])

    assert out["status"] == "applied"
    assert out["decision"]["accepted"] is True
    assert out["target"].endswith("05-harness-evolution.md")
    assert "ROI de um Componente" in out["section"]["heading"]
    # input limitado ao modelo: só a seção, nunca o arquivo inteiro
    user = calls[0][-1]["content"]
    assert "ROI corrente" in user and "Remoção segura." not in user
    # splice exato: corpo novo dentro da seção; tudo fora dela byte-idêntico
    after = target.read_text(encoding="utf-8")
    assert BODY in after and "ROI corrente sem a escada" not in after
    head = before[:before.index("## ROI de um Componente")]
    assert after.startswith(head)
    tail = before[before.index("## Fase 4: REMOVE"):]
    assert after[after.index("## Fase 4: REMOVE"):] == tail
    # gates
    assert out["diff"]["localized_ok"] is True
    assert out["evaluation"]["passed"] is True


def test_idempotent_rerun_skips(tmp_path):
    repo = _repo(tmp_path)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         dest="docs/canonical/capability-escalation-ladder.md")
    target = repo / "curriculum" / "03-nivel-3-advanced-architecture" / "05-harness-evolution.md"

    first, _ = _run(repo, manifest)
    assert first["status"] == "applied"
    snapshot = target.read_bytes()

    second, _ = _run(repo, manifest)
    assert second["status"] == "skipped"
    assert "rerun idempotente" in second["reason"]
    assert target.read_bytes() == snapshot


def test_gate_rejection_goes_to_quarantine(tmp_path):
    repo = _repo(tmp_path)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         dest="docs/canonical/capability-escalation-ladder.md")
    target = repo / "curriculum" / "03-nivel-3-advanced-architecture" / "05-harness-evolution.md"
    before = target.read_text(encoding="utf-8")

    out, _ = _run(repo, manifest, eval_ok=False)

    assert out["status"] == "quarantined"
    assert out["decision"]["accepted"] is False
    assert target.read_text(encoding="utf-8") == before  # currículo intocado
    qp = repo / out["quarantine_path"]
    assert qp.is_file()
    assert out["quarantine_path"].startswith(f"docs/analysis/{SLUG}/proposed/curriculum/")
    assert BODY in qp.read_text(encoding="utf-8")


def test_out_of_scope_diff_is_held(tmp_path):
    repo = _repo(tmp_path)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         dest="docs/canonical/capability-escalation-ladder.md")
    target_rel = "curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md"

    out, _ = _run(repo, manifest, changed=[target_rel, "docs/canonical/other.md"])
    assert out["status"] == "quarantined"
    assert any("docs/canonical/" in r for r in out["reasons"])


def test_exercise_level_routes_by_manifest_field(tmp_path):
    repo = _repo(tmp_path, extra_level2=True)
    ex = ("---\ntitle: Exercise\ntype: exercise\ntags: []\nlevel: 2\n---\n"
          "# Exercise\n\n## Tarefa\n\nOrdene escalation por custo de teste.\n")
    ex2 = repo / "curriculum" / "02-nivel-2-practical-patterns" / "exercises"
    ex2.mkdir(parents=True)
    (ex2 / "exercise-09-capability-escalation-ladder.md").write_text(ex)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         category="exercise", level=2,
                         dest="curriculum/02-nivel-2-practical-patterns/exercises/"
                              "exercise-09-capability-escalation-ladder.md")

    out, _ = _run(repo, manifest)

    assert out["level"] == 2  # o level do manifesto, verbatim
    assert out["target"].startswith("curriculum/02-nivel-2-practical-patterns/")
    assert out["status"] == "applied"


def test_level_without_dir_fails_closed(tmp_path):
    repo = _repo(tmp_path)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         category="exercise", level=9,
                         dest="docs/canonical/capability-escalation-ladder.md")
    with pytest.raises(ValueError, match="manifest level 9"):
        _run(repo, manifest)


def test_revision_of_the_target_section_is_not_a_duplicate_of_itself(tmp_path):
    """Enriquecer a seção alvo reformula o próprio texto indexado dela: o gate de
    dedup compara contra o RESTO do índice, nunca contra o registro da seção que
    está sendo revisada."""
    repo = _repo(tmp_path)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         dest="docs/canonical/capability-escalation-ladder.md")
    target = repo / "curriculum" / "03-nivel-3-advanced-architecture" / "05-harness-evolution.md"

    out, _ = _run(repo, manifest, splice_body="ROI corrente, sem a escada de escalation.")

    assert out["dedup"]["duplicate"] is False
    assert out["status"] == "applied"
    assert "ROI corrente, sem a escada de escalation." in target.read_text(encoding="utf-8")


def test_rewrite_duplicating_another_section_is_quarantined(tmp_path):
    """A isenção vale só para a seção revisada: duplicar OUTRA seção indexada
    continua barrando o splice (fail-closed)."""
    repo = _repo(tmp_path)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         dest="docs/canonical/capability-escalation-ladder.md")
    target = repo / "curriculum" / "03-nivel-3-advanced-architecture" / "05-harness-evolution.md"
    before = target.read_text(encoding="utf-8")

    out, _ = _run(repo, manifest,
                  splice_body="Remoção segura: remove o componente, remove o fallback, remove o resto.")

    assert out["dedup"]["duplicate"] is True
    assert out["dedup"]["nearest"]["heading"] == "Fase 4: REMOVE"
    assert out["status"] == "quarantined"
    assert any("duplicação" in r for r in out["reasons"])
    assert target.read_text(encoding="utf-8") == before


def test_canonical_hits_outranking_curriculum_do_not_abort_selection(tmp_path):
    """O conhecimento promovido vem de docs/canonical/, que está no mesmo índice:
    seções canônicas dominam o topo do ranking global. A seleção é feita DENTRO do
    escopo curricular, então isso não pode derrubar o splice."""
    repo = _repo(tmp_path)
    decoys = "\n".join(f"## Capability Escalation Ladder {i}\n\n"
                       "capability escalation ladder rung eval budget\n" for i in range(20))
    (repo / "docs" / "canonical" / "escalation-notes.md").write_text(
        "---\ntitle: Notas\ntype: canonical\n---\n\n# Notas\n\n" + decoys)
    manifest = _manifest(repo / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml",
                         dest="docs/canonical/capability-escalation-ladder.md")

    out, _ = _run(repo, manifest)

    assert out["target"] == ("curriculum/03-nivel-3-advanced-architecture/"
                            "05-harness-evolution.md")
    assert out["status"] == "applied"


def test_real_repo_section_localizes(tmp_path):
    """A maquinaria localiza a seção real alvo do slice no arquivo real do repo."""
    real = ROOT / "curriculum" / "03-nivel-3-advanced-architecture" / "05-harness-evolution.md"
    text = real.read_text(encoding="utf-8")
    rel = "curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md"
    recs = records_for(rel, text)
    roi = [r for r in recs if r.heading == "Como Calcular o ROI de um Componente"]
    assert len(roi) == 1
    rng, sec_text = p6.locate_by_id(text, rel, roi[0].id)
    assert 500 < rng.start < 600          # a seção real fica perto da linha 568
    assert "ROI = (Erros Prevenidos" in sec_text
