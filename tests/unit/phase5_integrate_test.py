#!/usr/bin/env python3
"""Unit tests for Fase 5 (#264): deterministic index integration from the artifact
manifest. Pure parts + a thin run() over a synthetic repo; no network, no GLM."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "analyze-and-improve"))

import phase5_integrate as p5  # noqa: E402

SLUG = "2026-09-16-src"


def _manifest(*, canonical=(), skill=(), exercise=(), quarantined=()):
    """A minimal v4-shaped manifest. Promoted args are paths (exercises as
    (path, level)); quarantined args are (path, quarantine_path) tuples."""
    arts = {
        "canonical_docs": [],
        "skills": [],
        "exercises": [],
    }
    for p in canonical:
        arts["canonical_docs"].append({"path": p, "pattern": "X",
                                       "classification": "Missing", "priority": "P0",
                                       "status": "promoted"})
    for p in skill:
        arts["skills"].append({"path": p, "pattern": "X", "classification": "Missing",
                               "status": "promoted"})
    for p, level in exercise:
        arts["exercises"].append({"path": p, "pattern": "X", "classification": "Missing",
                                  "status": "promoted", "level": level})
    for p, q in quarantined:
        for rows in arts.values():
            rows.append({"path": p, "pattern": "X", "classification": "Missing",
                         "status": "quarantined", "quarantine_path": q})
    return {"meta": {"type": "artifact-manifest", "date": "2026-09-16", "source_slug": SLUG,
                     "classification_file": f"docs/analysis/{SLUG}/{SLUG}-classification.yaml"},
            "artifacts": arts,
            "skipped": {"already_exists": [], "better_implementation": [], "not_applicable": []},
            "gate": {"phase4_complete": True,
                     "artifacts_count": {k: len(v) for k, v in arts.items()}}}


SOR_SNIPPET = """---
title: "System of Record"
type: system-of-record
last_updated: 2026-09-12
---

# System of Record

## Documentação canônica pendente

Há 2 padrões canônicos ativos.

### Padrões canônicos ativos

| Documento | Cobre |
|---|---|
| `one.md` | Um padrão |
| `two.md` | Outro padrão |

Prosa após a tabela.

| Documento | Cobre |
|---|---|
| `outra-tabela.md` | não é a tabela ativa |
"""

INDEX_SNIPPET = """## Seção de exercícios

**Nível 2 (Padrões)**
- `02-nivel-2-practical-patterns/exercises/exercise-01.md` (Um)
- `02-nivel-2-practical-patterns/exercises/exercise-02.md` (Dois)

**Nível 3 (Arquitetura)**
- `03-nivel-3-advanced-architecture/exercises/exercise-01.md` (Multi-Agent Design)
- `03-nivel-arquiteto/exercises/exercise-04-owner-of-no-role.md` (Owner of No Role)

**Nível 4 (KODA)**
- `04-nivel-4-koda-specific/real-world-exercises/exercise-01.md`
"""

TREE_SNIPPET_README = """📦 root/
│
├── 📚 CONTEÚDO/
│   ├── 03-nivel-3-advanced-architecture/
│   │   ├── 01-multi-agent-systems.md
│   │   ├── exercises/
│   │   │   ├── exercise-01.md
│   │   │   ├── exercise-22-capability.md
│   │   │   └── solutions/
│   │   └── koda-applications/
│   │       └── nivel-3-koda.md
│
├── 04-nivel-4-koda-specific/
"""

TREE_SNIPPET_MASTER_PLAN = """📦 root/
│
├── 03-nivel-3-advanced-architecture/
│   ├── 01-multi-agent-systems.md
│   ├── exercises/
│   │   ├── exercise-01.md
│   │   ├── exercise-22-capability.md
│   │   └── solutions/
│   └── koda-applications/
"""


# ── manifest loading: v4 contract, fail-fast on v3 composition mismatch ─────
def test_validate_manifest_accepts_v4():
    m = _manifest(canonical=["docs/canonical/x.md"],
                  exercise=[("curriculum/03-nivel-3-advanced-architecture/exercises/exercise-23-x.md", 3)])
    assert p5.validate_manifest(m)["meta"]["source_slug"] == SLUG


def test_validate_manifest_rejects_v3_shape_missing_type():
    v3 = {"meta": {"date": "2026-09-02", "source_slug": "old"},
          "artifacts": {"canonical_docs": [{"path": "docs/canonical/a.md",
                                            "pattern": "A", "priority": "P0"}],
                        "skills": [], "exercises": []},
          "gate": {"notes": "v3 had notes"}}
    with pytest.raises(ValueError, match="artifact-manifest"):
        p5.validate_manifest(v3)


def test_validate_manifest_rejects_entry_without_status():
    m = _manifest()
    m["artifacts"]["canonical_docs"].append({"path": "docs/canonical/a.md",
                                             "pattern": "A", "priority": "P0"})
    with pytest.raises(ValueError, match="status"):
        p5.validate_manifest(m)


def test_validate_manifest_rejects_wrong_type():
    m = _manifest()
    m["meta"]["type"] = "something-else"
    with pytest.raises(ValueError, match="artifact-manifest"):
        p5.validate_manifest(m)


def test_load_manifest_reads_yaml_from_disk(tmp_path):
    import yaml
    mp = tmp_path / "m-artifacts.yaml"
    mp.write_text(yaml.safe_dump(_manifest(canonical=["docs/canonical/x.md"]),
                                 allow_unicode=True), encoding="utf-8")
    assert p5.load_manifest(mp)["meta"]["source_slug"] == SLUG


def test_load_manifest_missing_file(tmp_path):
    with pytest.raises(ValueError, match="manifest not found"):
        p5.load_manifest(tmp_path / "nope.yaml")


# ── expected_index_paths / allowed_paths ────────────────────────────────────
def test_expected_index_paths_all_four_surfaces():
    m = _manifest(canonical=["docs/canonical/x.md"],
                  skill=[".opencode/skills/x/SKILL.md"],
                  exercise=[("curriculum/03-nivel-3-advanced-architecture/exercises/exercise-23-x.md", 3)])
    assert p5.expected_index_paths(m) == [
        "docs/system-of-record.md", "curriculum/INDEX.md",
        "curriculum/README.md", "curriculum/MASTER_PLAN.md"]


def test_expected_index_paths_only_canonical_is_sor_only():
    m = _manifest(canonical=["docs/canonical/x.md"])
    assert p5.expected_index_paths(m) == ["docs/system-of-record.md"]


def test_expected_index_paths_quarantined_only_is_empty():
    m = _manifest(quarantined=[("docs/canonical/held.md",
                                "docs/analysis/s/proposed/docs/canonical/held.md")])
    assert p5.expected_index_paths(m) == []


def test_allowed_paths_is_promoted_manifest_and_indexes_only():
    m = _manifest(canonical=["docs/canonical/x.md"],
                  quarantined=[("docs/canonical/held.md",
                                "docs/analysis/s/proposed/docs/canonical/held.md")])
    assert p5.allowed_paths(m) == sorted([
        "docs/canonical/x.md",
        f"docs/analysis/{SLUG}/{SLUG}-artifacts.yaml",
        f"docs/analysis/{SLUG}/{SLUG}-artifacts.md",
        "docs/system-of-record.md"])


def test_allowed_paths_all_held_run_commits_only_the_manifest():
    m = _manifest(quarantined=[("docs/canonical/held.md",
                                "docs/analysis/s/proposed/docs/canonical/held.md")])
    assert p5.allowed_paths(m) == sorted(p5.manifest_paths(SLUG))


# ── SOR updaters ─────────────────────────────────────────────────────────────
def test_update_sor_count_replaces_claim():
    out = p5.update_sor_count(SOR_SNIPPET, 202)
    assert "Há 202 padrões canônicos ativos" in out
    assert "Há 2 padrões" not in out


def test_update_sor_count_fails_without_claim():
    with pytest.raises(ValueError, match="padrões canônicos ativos"):
        p5.update_sor_count("no claim here", 5)


def test_update_sor_date_replaces_frontmatter_stamp():
    out = p5.update_sor_date(SOR_SNIPPET, "2026-09-16")
    assert "last_updated: 2026-09-16" in out
    assert "2026-09-12" not in out


def test_sor_row_escapes_pipes():
    row = p5.sor_row("x.md", "Title with | pipe")
    assert row == "| `x.md` | Title with \\| pipe |"


def test_insert_sor_row_appends_to_active_table_only():
    row = p5.sor_row("three.md", "Terceiro")
    out = p5.insert_sor_row(SOR_SNIPPET, row)
    lines = out.split("\n")
    i = lines.index("| `two.md` | Outro padrão |")
    assert lines[i + 1] == "| `three.md` | Terceiro |"
    assert "| `outra-tabela.md` | não é a tabela ativa |" in lines  # other table untouched


# ── curriculum INDEX listing ─────────────────────────────────────────────────
def test_insert_exercise_listing_appends_to_level_group():
    line = p5.exercise_listing_line(
        "03-nivel-3-advanced-architecture/exercises/exercise-23-new.md", "New Pattern")
    out = p5.insert_exercise_listing(INDEX_SNIPPET,
                                     "03-nivel-3-advanced-architecture", line)
    lines = out.split("\n")
    i = lines.index("- `03-nivel-arquiteto/exercises/exercise-04-owner-of-no-role.md` (Owner of No Role)")
    assert lines[i + 1] == ("- `03-nivel-3-advanced-architecture/exercises/"
                            "exercise-23-new.md` (New Pattern)")
    # Nível 2 group untouched
    j = lines.index("- `02-nivel-2-practical-patterns/exercises/exercise-02.md` (Dois)")
    assert lines[j + 1] == ""


def test_insert_exercise_listing_unknown_level_fails():
    with pytest.raises(ValueError, match="Nível 9"):
        p5.insert_exercise_listing(INDEX_SNIPPET, "09-nivel-9-x",
                                   "- `09-nivel-9-x/exercises/exercise-01.md` (Y)")


# ── directory trees (README / MASTER_PLAN) ──────────────────────────────────
def test_insert_tree_exercise_before_solutions():
    out = p5.insert_tree_exercise(TREE_SNIPPET_README, "03-nivel-3-advanced-architecture",
                                  "exercise-23-new.md")
    lines = out.split("\n")
    i = lines.index("│   │   │   ├── exercise-22-capability.md")
    assert lines[i + 1] == "│   │   │   ├── exercise-23-new.md"
    assert lines[i + 2] == "│   │   │   └── solutions/"


def test_insert_tree_exercise_without_solutions_fails_closed():
    no_solutions = TREE_SNIPPET_MASTER_PLAN.replace("│   │   └── solutions/\n", "")
    with pytest.raises(ValueError, match="solutions/"):
        p5.insert_tree_exercise(no_solutions, "03-nivel-3-advanced-architecture",
                                "exercise-23-new.md")


def test_insert_tree_exercise_unknown_dir_fails():
    with pytest.raises(ValueError, match="tree"):
        p5.insert_tree_exercise(TREE_SNIPPET_README, "99-nivel-x", "exercise-01.md")


# ── recount ──────────────────────────────────────────────────────────────────
def test_recount_canonical_counts_md_on_disk(tmp_path):
    canonical = tmp_path / "docs" / "canonical"
    canonical.mkdir(parents=True)
    (canonical / "a.md").write_text("x", encoding="utf-8")
    (canonical / "b.md").write_text("x", encoding="utf-8")
    (canonical / "notes.txt").write_text("x", encoding="utf-8")
    sub = canonical / "sub"
    sub.mkdir()
    (sub / "nested.md").write_text("x", encoding="utf-8")
    assert p5.recount_canonical(tmp_path) == 2


# ── run(): the thin integrator over a synthetic repo ────────────────────────
def _synth_repo(tmp_path):
    root = tmp_path
    (root / "docs" / "canonical").mkdir(parents=True)
    for name in ("one.md", "two.md"):
        (root / "docs" / "canonical" / name).write_text(
            f"---\ntitle: {name}\ntype: canonical\n---\nbody", encoding="utf-8")
    (root / "docs" / "canonical" / "new.md").write_text(
        "---\ntitle: New Pattern Title\ntype: canonical\n---\nbody", encoding="utf-8")
    ex_rel = "curriculum/03-nivel-3-advanced-architecture/exercises/exercise-23-new.md"
    ex = root / ex_rel
    ex.parent.mkdir(parents=True)
    ex.write_text("---\ntitle: New Pattern Exercise\ntype: exercise\nlevel: 3\n---\nbody",
                  encoding="utf-8")
    (root / "docs" / "system-of-record.md").write_text(SOR_SNIPPET, encoding="utf-8")
    (root / "curriculum" / "INDEX.md").write_text(INDEX_SNIPPET, encoding="utf-8")
    (root / "curriculum" / "README.md").write_text(TREE_SNIPPET_README, encoding="utf-8")
    (root / "curriculum" / "MASTER_PLAN.md").write_text(TREE_SNIPPET_MASTER_PLAN,
                                                        encoding="utf-8")
    import yaml
    m = _manifest(canonical=["docs/canonical/new.md"],
                  quarantined=[("docs/canonical/held.md",
                                "docs/analysis/s/proposed/docs/canonical/held.md")])
    m["artifacts"]["exercises"].append(
        {"path": ex_rel, "pattern": "X", "classification": "Missing",
         "status": "promoted", "level": 3})
    mp = root / "docs" / "analysis" / SLUG / f"{SLUG}-artifacts.yaml"
    mp.parent.mkdir(parents=True)
    mp.write_text(yaml.safe_dump(m, allow_unicode=True), encoding="utf-8")
    return root, mp


def test_run_updates_all_four_surfaces_from_disk_truth(tmp_path):
    root, mp = _synth_repo(tmp_path)
    report = p5.run(root, mp)
    sor = (root / "docs" / "system-of-record.md").read_text(encoding="utf-8")
    assert "Há 3 padrões canônicos ativos" in sor          # recount (2 old + 1 new), never increment
    assert "last_updated: 2026-09-16" in sor               # manifest date
    assert "| `new.md` | New Pattern Title |" in sor        # row from on-disk frontmatter
    idx = (root / "curriculum" / "INDEX.md").read_text(encoding="utf-8")
    assert ("`03-nivel-3-advanced-architecture/exercises/exercise-23-new.md` "
            "(New Pattern Exercise)") in idx   # curriculum-relative, the file's convention
    rdt = (root / "curriculum" / "README.md").read_text(encoding="utf-8")
    assert "│   │   │   ├── exercise-23-new.md" in rdt
    mst = (root / "curriculum" / "MASTER_PLAN.md").read_text(encoding="utf-8")
    assert "│   │   ├── exercise-23-new.md" in mst
    assert report["sor_before"] == 2 and report["sor_after"] == 3
    assert set(report["changed"]) == {"docs/system-of-record.md", "curriculum/INDEX.md",
                                      "curriculum/README.md", "curriculum/MASTER_PLAN.md"}


def test_run_is_idempotent_on_rerun(tmp_path):
    root, mp = _synth_repo(tmp_path)
    p5.run(root, mp)
    first = {p: (root / p).read_text(encoding="utf-8") for p in
             ("docs/system-of-record.md", "curriculum/INDEX.md",
              "curriculum/README.md", "curriculum/MASTER_PLAN.md")}
    report = p5.run(root, mp)
    for p, text in first.items():
        assert (root / p).read_text(encoding="utf-8") == text
    assert report["changed"] == []   # nothing moved, so nothing is reported as updated


def test_run_quarantined_only_never_mutates_indexes(tmp_path):
    root, mp = _synth_repo(tmp_path)
    import yaml
    m = yaml.safe_load(mp.read_text(encoding="utf-8"))
    for rows in m["artifacts"].values():
        for row in rows:
            row["status"] = "quarantined"
            row["quarantine_path"] = f"docs/analysis/s/proposed/{row['path']}"
    mp.write_text(yaml.safe_dump(m, allow_unicode=True), encoding="utf-8")
    report = p5.run(root, mp)
    assert report["changed"] == []
    assert (root / "docs" / "system-of-record.md").read_text(encoding="utf-8") == SOR_SNIPPET


def test_run_fails_fast_when_promoted_path_missing_on_disk(tmp_path):
    root, mp = _synth_repo(tmp_path)
    (root / "docs" / "canonical" / "new.md").unlink()
    with pytest.raises(ValueError, match="new.md"):
        p5.run(root, mp)


def test_run_fails_fast_when_frontmatter_lacks_title(tmp_path):
    root, mp = _synth_repo(tmp_path)
    (root / "docs" / "canonical" / "new.md").write_text(
        "---\ntype: canonical\n---\nbody", encoding="utf-8")
    with pytest.raises(ValueError, match="title"):
        p5.run(root, mp)
