"""Fase 5 — deterministic index integration from the artifact manifest (#264).

The consumer side of the #263 contract: reads ONE run's manifest
(`docs/analysis/<slug>/<slug>-artifacts.yaml`, by explicit path — never a glob
over historical v3-shaped manifests) and recomputes the mechanically derivable
projections of authoritative disk state onto the four index surfaces named by
#264's DoD:

  - `docs/system-of-record.md`   canonical count (RECOUNT from disk, never an
                                 increment — the first live run absorbs legacy
                                 count drift by construction), `last_updated`
                                 (the manifest's date) and one active-patterns
                                 table row per promoted canonical doc (filename +
                                 title read from the promoted file's own
                                 frontmatter on disk)
  - `curriculum/INDEX.md`        one exercise-listing line per promoted exercise
  - `curriculum/README.md`       one directory-tree line per promoted exercise
  - `curriculum/MASTER_PLAN.md`  one directory-tree line per promoted exercise

Editorial boundary: ONLY those projections change. Narrative, priorities,
interpretation and human-authored semantics are never rewritten, and rows/lines
are never fabricated for docs outside the run's manifest (legacy drift stays
VISIBLE — surfaced, not silently absorbed). `status: quarantined` entries never
mutate any index.

`load_manifest` fails fast on composition mismatch (a v3 manifest has no
per-entry `status` and no `meta.type: artifact-manifest` — a hard error, not a
best-effort parse). Every pure updater is unit-tested; `run` is the thin I/O
shell the `pipeline.py integrate <slug>` verb drives.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

SOR_PATH = "docs/system-of-record.md"
CURRICULUM_INDEX_PATH = "curriculum/INDEX.md"
CURRICULUM_README_PATH = "curriculum/README.md"
CURRICULUM_MASTER_PLAN_PATH = "curriculum/MASTER_PLAN.md"
CANONICAL_DIR = "docs/canonical"

SOR_ACTIVE_HEADING = "### Padrões canônicos ativos"
_COUNT_RE = re.compile(r"Há (\d+) padrões canônicos ativos")
_LAST_UPDATED_RE = re.compile(r"^last_updated:.*$", re.MULTILINE)
_LEVEL_RE = re.compile(r"nivel-(\d+)")
_TREE_DIR_RE = "([│ ]*)"


# ── manifest contract ────────────────────────────────────────────────────────
def validate_manifest(manifest: dict) -> dict:
    """Fail fast on anything that is not the v4 artifact-manifest contract. Pure."""
    if not isinstance(manifest, dict):
        raise ValueError("manifest: top level must be a mapping")
    meta = manifest.get("meta")
    if not isinstance(meta, dict) or meta.get("type") != "artifact-manifest":
        raise ValueError("manifest: meta.type must be 'artifact-manifest' "
                         "(v3-shaped historical manifests are not consumable)")
    for key in ("date", "source_slug"):
        if not isinstance(meta.get(key), str) or not meta[key]:
            raise ValueError(f"manifest: meta.{key} must be a non-empty string")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("manifest: artifacts must be a mapping")
    for key in ("canonical_docs", "skills", "exercises"):
        rows = artifacts.get(key)
        if not isinstance(rows, list):
            raise ValueError(f"manifest: artifacts.{key} must be a list")
        for row in rows:
            if not isinstance(row, dict) or row.get("status") not in ("promoted", "quarantined"):
                raise ValueError(f"manifest: artifacts.{key} entry without a valid "
                                 "'status' (promoted|quarantined) — v3 shape?")
            if not isinstance(row.get("path"), str) or not row["path"]:
                raise ValueError(f"manifest: artifacts.{key} entry without a 'path'")
    return manifest


def load_manifest(path: Path) -> dict:
    """Read + validate one run's manifest (explicit path, never a glob). I/O."""
    if not path.is_file():
        raise ValueError(f"manifest not found: {path}")
    return validate_manifest(yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def manifest_paths(slug: str) -> list[str]:
    """The manifest's own committed files. Pure."""
    return [f"docs/analysis/{slug}/{slug}-artifacts.yaml",
            f"docs/analysis/{slug}/{slug}-artifacts.md"]


def _promoted(manifest: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for key, rows in manifest["artifacts"].items():
        out[key] = [r for r in rows if r["status"] == "promoted"]
    return out


def expected_index_paths(manifest: dict) -> list[str]:
    """Which index surfaces this run's manifest authorizes updating. Pure.

    A promoted canonical doc moves the SOR surface; a promoted exercise moves the
    three curriculum surfaces; a promoted skill has no mechanically derivable
    projection on the four #264 surfaces (SOR's domain tables are editorial).
    Quarantined-only manifests authorize nothing."""
    promoted = _promoted(manifest)
    paths: list[str] = []
    if promoted["canonical_docs"]:
        paths.append(SOR_PATH)
    if promoted["exercises"]:
        paths += [CURRICULUM_INDEX_PATH, CURRICULUM_README_PATH, CURRICULUM_MASTER_PLAN_PATH]
    return paths


def allowed_paths(manifest: dict) -> list[str]:
    """The fail-closed diff gate's allowed set: exactly what this run's manifest
    declares (promoted destinations + quarantined copies), the manifest's own two
    files, and the derived index updates it authorizes. Pure."""
    slug = manifest["meta"]["source_slug"]
    allowed = list(manifest_paths(slug))
    for rows in manifest["artifacts"].values():
        for row in rows:
            if row["status"] == "promoted":
                allowed.append(row["path"])
            elif row.get("quarantine_path"):
                allowed.append(row["quarantine_path"])
    allowed += expected_index_paths(manifest)
    return sorted(set(allowed))


# ── SOR updaters (pure) ─────────────────────────────────────────────────────
def update_sor_count(text: str, n: int) -> str:
    if not _COUNT_RE.search(text):
        raise ValueError("SOR: active-canonical count claim not found "
                         "('Há N padrões canônicos ativos')")
    return _COUNT_RE.sub(f"Há {n} padrões canônicos ativos", text, count=1)


def update_sor_date(text: str, date: str) -> str:
    if not _LAST_UPDATED_RE.search(text):
        raise ValueError("SOR: frontmatter last_updated not found")
    return _LAST_UPDATED_RE.sub(f"last_updated: {date}", text, count=1)


def sor_row(filename: str, title: str) -> str:
    return f"| `{filename}` | {title.replace('|', '\\|')} |"


def sor_row_present(text: str, filename: str) -> bool:
    return f"| `{filename}` |" in text


def insert_sor_row(text: str, row: str) -> str:
    """Append `row` after the LAST row of the active-patterns table (the first
    table under `### Padrões canônicos ativos`). Pure."""
    lines = text.split("\n")
    try:
        hi = next(i for i, l in enumerate(lines) if l.strip() == SOR_ACTIVE_HEADING)
    except StopIteration:
        raise ValueError(f"SOR: heading not found: {SOR_ACTIVE_HEADING!r}") from None
    ti = hi + 1
    while ti < len(lines) and not lines[ti].lstrip().startswith("|"):
        ti += 1
    if ti >= len(lines):
        raise ValueError("SOR: active-patterns table not found")
    end = ti + 2  # skip the header and separator rows
    while end < len(lines) and lines[end].lstrip().startswith("|"):
        end += 1
    lines.insert(end, row)
    return "\n".join(lines)


# ── curriculum INDEX listing (pure) ──────────────────────────────────────────
def level_number(level_dir: str) -> int:
    m = _LEVEL_RE.search(level_dir)
    if not m:
        raise ValueError(f"cannot derive curriculum level from dir: {level_dir!r}")
    return int(m.group(1))


def exercise_listing_line(rel_path: str, title: str) -> str:
    return f"- `{rel_path}` ({title})"


def insert_exercise_listing(text: str, level_dir: str, line: str) -> str:
    """Append `line` at the end of INDEX.md's `**Nível N (...)**` bullet group. Pure."""
    heading = f"**Nível {level_number(level_dir)} ("
    lines = text.split("\n")
    hi = next((i for i, l in enumerate(lines) if l.startswith(heading)), None)
    if hi is None:
        raise ValueError(f"curriculum INDEX: level group not found: {heading!r}")
    end = hi + 1
    while end < len(lines) and lines[end].startswith("- "):
        end += 1
    lines.insert(end, line)
    return "\n".join(lines)


# ── directory trees (README / MASTER_PLAN, pure) ────────────────────────────
def _tree_content(line: str) -> str:
    """The filename part of a tree line (`│   ├── exercises/` → `exercises/`)."""
    return re.sub(r"^[│ ]*[├└]── ", "", line)


def _tree_child_prefix(line: str) -> str:
    """The prefix its children carry (`│   ├── x/` → `│   │   `)."""
    m = re.match(r"^([│ ]*)[├└]── ", line)
    prefix = m.group(1) if m else ""
    return prefix + ("│   " if "├──" in line else "    ")


def insert_tree_exercise(text: str, level_dir: str, filename: str) -> str:
    """Insert `filename` into the level's `exercises/` subtree. Pure.

    Primary path: immediately before the `└── solutions/` line (the shape both
    real trees use), keeping the previous last exercise a `├──` sibling. Without a
    solutions entry, the block's last child is flipped from `└──` to `├──` and
    the new line becomes the last child."""
    lines = text.split("\n")
    dir_re = re.compile(rf"^{_TREE_DIR_RE}[├└]── {re.escape(level_dir)}/$")
    di = next((i for i, l in enumerate(lines) if dir_re.match(l)), None)
    if di is None:
        raise ValueError(f"tree: level dir not found: {level_dir!r}")
    children_prefix = _tree_child_prefix(lines[di])
    ex = next((i for i in range(di + 1, len(lines))
               if not lines[i].startswith(children_prefix)
               or _tree_content(lines[i]) == "exercises/"), None)
    if ex is None or _tree_content(lines[ex]) != "exercises/":
        raise ValueError(f"tree: exercises/ not found under {level_dir!r}")
    child_prefix = _tree_child_prefix(lines[ex])
    block_end = ex + 1
    while block_end < len(lines) and lines[block_end].startswith(child_prefix):
        block_end += 1
    sol = next((i for i in range(ex + 1, block_end)
                if _tree_content(lines[i]) == "solutions/"), None)
    if sol is not None:
        m = re.match(r"^([│ ]*)└── ", lines[sol])
        lines.insert(sol, f"{m.group(1)}├── {filename}")
        return "\n".join(lines)
    last = block_end - 1
    if last <= ex:
        raise ValueError(f"tree: exercises/ block under {level_dir!r} is empty")
    line = lines[last]
    m = re.match(r"^([│ ]*)([├└])── ", line)
    if m.group(2) == "└":
        lines[last] = f"{m.group(1)}├── {_tree_content(line)}"
        lines.insert(last + 1, f"{m.group(1)}└── {filename}")
    else:
        lines.insert(last + 1, f"{m.group(1)}├── {filename}")
    return "\n".join(lines)


# ── disk truth ───────────────────────────────────────────────────────────────
def recount_canonical(repo_root: Path) -> int:
    """Count `docs/canonical/*.md` on disk — the authoritative number. I/O."""
    return len(list((repo_root / CANONICAL_DIR).glob("*.md")))


def frontmatter_title(path: Path) -> str:
    """The `title` of a promoted file's own frontmatter, read from disk. I/O."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"promoted artifact has no frontmatter: {path}")
    block = text.split("---", 2)
    if len(block) < 3:
        raise ValueError(f"promoted artifact has malformed frontmatter: {path}")
    fm = yaml.safe_load(block[1]) or {}
    title = fm.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError(f"promoted artifact frontmatter lacks a title: {path}")
    return title.strip()


def _level_dir_of(rel_path: str) -> str:
    parts = Path(rel_path).parts
    if len(parts) != 4 or parts[0] != "curriculum" or parts[2] != "exercises":
        raise ValueError(f"promoted exercise not under curriculum/<level>/exercises/: {rel_path}")
    return parts[1]


# ── the thin integrator ──────────────────────────────────────────────────────
def run(repo_root: Path, manifest_path: Path) -> dict:
    """Apply this run's manifest to the four index surfaces. I/O.

    Deterministic and idempotent: counts are RECOUNTed from disk (never
    incremented), rows/listings already present are skipped, and only
    `status: promoted` entries mutate anything."""
    manifest = load_manifest(manifest_path)
    date = manifest["meta"]["date"]
    promoted = _promoted(manifest)

    for row in [r for rows in promoted.values() for r in rows]:
        if not (repo_root / row["path"]).is_file():
            raise ValueError(f"promoted artifact not on disk: {row['path']}")

    changed: list[str] = []
    report: dict = {"promoted": promoted, "sor_before": None, "sor_after": None,
                    "changed": changed, "allowed": allowed_paths(manifest)}

    if promoted["canonical_docs"]:
        sor_file = repo_root / SOR_PATH
        text = sor_file.read_text(encoding="utf-8")
        claimed = _COUNT_RE.search(text)
        report["sor_before"] = int(claimed.group(1)) if claimed else None
        after = recount_canonical(repo_root)
        text = update_sor_count(text, after)
        text = update_sor_date(text, date)
        report["sor_after"] = after
        for row in promoted["canonical_docs"]:
            filename = Path(row["path"]).name
            if not sor_row_present(text, filename):
                text = insert_sor_row(text, sor_row(filename,
                                                    frontmatter_title(repo_root / row["path"])))
        sor_file.write_text(text, encoding="utf-8")
        changed.append(SOR_PATH)

    for row in promoted["exercises"]:
        rel = row["path"]
        level_dir = _level_dir_of(rel)
        title = frontmatter_title(repo_root / rel)
        # INDEX.md lists curriculum-relative paths (no `curriculum/` prefix) — the
        # file's own convention; the manifest path stays repo-relative everywhere else.
        idx_rel = rel[len("curriculum/"):]
        listing = exercise_listing_line(idx_rel, title)
        idx_file = repo_root / CURRICULUM_INDEX_PATH
        idx_text = idx_file.read_text(encoding="utf-8")
        if listing not in idx_text:
            idx_file.write_text(insert_exercise_listing(idx_text, level_dir, listing),
                                encoding="utf-8")
            if CURRICULUM_INDEX_PATH not in changed:
                changed.append(CURRICULUM_INDEX_PATH)
        for surf in (CURRICULUM_README_PATH, CURRICULUM_MASTER_PLAN_PATH):
            sfile = repo_root / surf
            stext = sfile.read_text(encoding="utf-8")
            tree_line = f"├── {Path(rel).name}"
            if tree_line not in stext and f"└── {Path(rel).name}" not in stext:
                sfile.write_text(insert_tree_exercise(stext, level_dir, Path(rel).name),
                                 encoding="utf-8")
                if surf not in changed:
                    changed.append(surf)

    return report
