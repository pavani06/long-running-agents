"""Artifacts manifest — the contract Fase 5 (#264) reads as input.

Typed record of one Fase-4 run (meta / artifacts{canonical_docs,skills,exercises}
/ skipped / gate) with per-artifact status fields for the governed loop: `status`
(promoted|quarantined), `reasons` when a gate held the artifact, and
`quarantine_path` — present only when a quarantined copy exists on disk, so a
consumer never resolves a path to a file that was never written. Exercises additionally carry `level`, the curriculum level they were
placed at — INTERIM while there is no level routing (see
`phase4_create.DEFAULT_LEVEL_DIR`); Etapa 7 (#265) must decide whether and how to
own that routing, and this field is its re-routing input. `build_manifest` and
`manifest_md` are pure and unit-tested; writing the files is the flow's job
(analysis_package conventions).
"""
from __future__ import annotations

import serialize

STATUS_PROMOTED = "promoted"
STATUS_QUARANTINED = "quarantined"

_CATEGORY_KEYS = {"canonical": "canonical_docs", "skill": "skills", "exercise": "exercises"}
_MD_LABELS = {"canonical_docs": "canonical", "skills": "skill", "exercises": "exercise"}


def _entry(category: str, artifact: dict, status: str, reasons: list[str]) -> dict:
    """One manifest row for a generated artifact. Pure."""
    entry = {
        "path": artifact["intended_destination"],
        "pattern": artifact.get("pattern", ""),
        "classification": artifact.get("phase3_verdict", ""),
        "status": status,
    }
    if category == "canonical_docs":
        entry["priority"] = artifact.get("priority", "")
    if category == "exercises":
        entry["level"] = artifact.get("level", "")
    if status == STATUS_QUARANTINED:
        if artifact.get("quarantine_path"):
            entry["quarantine_path"] = artifact["quarantine_path"]
        entry["reasons"] = reasons
    return entry


def _skipped_rows(classifications: list[dict]) -> dict:
    """already_exists/better_implementation rows for verdicts that generate nothing. Pure."""
    from phase4_routing import skip_reason
    rows = {"already_exists": [], "better_implementation": []}
    for c in classifications:
        if c.get("verdict") == "Exists":
            ev = "; ".join(f"{e.get('file','')}:{e.get('line','')}"
                           for e in c.get("evidence", []) if isinstance(e, dict))
            rows["already_exists"].append(
                {"pattern": c.get("pattern", ""),
                 "evidence": ev or skip_reason("Exists")})
        elif c.get("verdict") == "Better":
            rows["better_implementation"].append(
                {"pattern": c.get("pattern", ""), "reason": skip_reason("Better")})
    return rows


def not_applicable_rows(planned_categories: set[str]) -> list[dict]:
    """Rows explaining artifact types with no work this run (e.g. 0 Missing → no skills). Pure."""
    rows = []
    if "skill" not in planned_categories:
        rows.append({"artifact_type": "skills",
                     "reason": "Nenhum padrão Missing (P0) — skills são criadas apenas para Missing."})
    if "exercise" not in planned_categories:
        rows.append({"artifact_type": "exercises",
                     "reason": "Nenhum padrão Missing/P1 — exercícios são criados apenas para Missing e Partial High."})
    return rows


def build_manifest(slug: str, date: str, classifications: list[dict],
                   outcomes: list[dict], planned_categories: set[str]) -> dict:
    """Assemble the typed manifest. Pure.

    `outcomes`: [{category, artifact, accepted, reasons}] — one per generated artifact.
    `planned_categories`: the categories plan_of_work scheduled (for not_applicable)."""
    artifacts: dict[str, list] = {"canonical_docs": [], "skills": [], "exercises": []}
    for o in outcomes:
        key = _CATEGORY_KEYS[o["category"]]
        artifacts[key].append(_entry(key, o["artifact"],
                                     STATUS_PROMOTED if o["accepted"] else STATUS_QUARANTINED,
                                     o.get("reasons", [])))
    skipped = _skipped_rows(classifications)
    skipped["not_applicable"] = not_applicable_rows(planned_categories)
    return {
        "meta": {
            "type": "artifact-manifest",
            "date": date,
            "source_slug": slug,
            "classification_file": f"docs/analysis/{slug}/{slug}-classification.yaml",
        },
        "artifacts": artifacts,
        "skipped": skipped,
        "gate": {
            "phase4_complete": True,
            "artifacts_count": {k: len(v) for k, v in artifacts.items()},
        },
    }


def manifest_yaml(manifest: dict) -> str:
    """The `<slug>-artifacts.yaml` body. Pure."""
    return serialize.to_yaml(manifest)


def manifest_md(manifest: dict) -> str:
    """The `<slug>-artifacts.md` body (analysis-doc conventions + integration map). Pure.

    Frontmatter carries the docs/analysis/ requirements (title/type/date/aliases/
    tags/relates-to) so the committed manifest passes validate-obsidian."""
    slug = manifest["meta"]["source_slug"]
    date = manifest["meta"]["date"]
    fm = {
        "title": f"Artifacts Manifest: {slug}",
        "type": "analysis",
        "date": date,
        "aliases": [f"manifesto {slug}", f"artifacts {slug}"],
        "tags": ["agentes-orquestracao"],
        "relates-to": [],
    }
    lines = ["---", serialize.to_yaml(fm).rstrip(), "---", "",
             f"# Artifacts Manifest: {slug}", "", "## Summary", "",
             "| # | Pattern | Classification | Priority | Artifacts |", "|---|---|---|---|---|"]
    by_pattern: dict[str, dict] = {}
    for key in ("canonical_docs", "skills", "exercises"):
        for e in manifest["artifacts"][key]:
            row = by_pattern.setdefault(e["pattern"], {"cls": e["classification"],
                                                        "prio": e.get("priority", "—"),
                                                        "cats": [], "held": False})
            row["cats"].append(_MD_LABELS[key])
            if e.get("status") == STATUS_QUARANTINED:
                row["held"] = True
    for i, (pattern, row) in enumerate(by_pattern.items(), 1):
        held = " ⚠️ quarentena" if row["held"] else ""
        lines.append(f"| {i} | {pattern} | {row['cls']} | {row['prio']} | "
                     f"{', '.join(row['cats'])}{held} |")
    lines += ["", "## Integration Map", "",
              "| Artifact | Path | Status |", "|---|---|---|"]
    for key in ("canonical_docs", "skills", "exercises"):
        for e in manifest["artifacts"][key]:
            lines.append(f"| {_MD_LABELS[key]} | `{e['path']}` | {e['status']} |")
    lines += ["", "## Skipped", ""]
    any_skipped = False
    for group, label in (("already_exists", "Already Exists"),
                         ("better_implementation", "Better Implementation"),
                         ("not_applicable", "Not applicable")):
        for row in manifest["skipped"][group]:
            any_skipped = True
            who = row.get("pattern") or row.get("artifact_type", "")
            why = row.get("evidence") or row.get("reason", "")
            lines.append(f"- **{who}** — {label}: {why}")
    if not any_skipped:
        lines.append("_(nenhum padrão ignorado)_")
    lines.append("")
    return "\n".join(lines)
