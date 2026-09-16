"""Fase 4 flow — generate → quarantine write → Etapa-3 gates → promote-on-pass → manifest.

The #263 remainder composition (the full creation phase): for one source's
classifications, `phase4_routing.plan_of_work` decides what to generate and in
which order; each artifact is generated with full content (GLM), written to the
quarantine dir (`docs/analysis/<slug>/proposed/<destination>` — never the
authoritative layers), gated by the Etapa-3 lib (adversarial evaluator on OpenAI
+ cosine dedup + the repo-level validate-obsidian + the same validator re-run
over the artifact at its intended destination + the classification's
grep-verified flag, routed fail-closed by `quarantine.decide`), and only the
accepted ones are promoted (moved) to their authoritative destinations. The run
is recorded in the artifacts manifest — the contract Fase 5 (#264) consumes.

Governance invariants: creation != promotion (promotion here is an in-worktree
move gated by the machine gates; landing on main stays behind a human-gated PR);
the evaluator is a different provider from the generator; the quarantine write
can never touch `docs/canonical/`, `curriculum/` or `.opencode/skills/`.

`first_loop.py` is the single production caller since #264 landed the
producer/consumer wiring (manifest consumption + index integration), so both
sides of the contract are validated as one integration boundary.

`write_quarantined`/`promote` are thin I/O over pure path computation;
`run_fase4` needs both keys but every external call (GLM, evaluator, embeddings,
validate) is injectable for unit tests. Classifications must be post-
`mark_verified` (the citations gate reads the `verified` flag, fail-closed).
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import artifact_manifest
import dedup
import evaluator
import phase4_create
import phase4_routing
import quarantine
from analysis_package import package_dir

_LEVEL_RE = re.compile(r"nivel-(\d+)")
ALREADY_AT_DESTINATION = "conteúdo idêntico já no destino, promovido numa execução anterior"
_LAST_UPDATED_RE = re.compile(r"^last_updated:.*$", re.MULTILINE)


def _comparable(text: str) -> str:
    """`text` with the frontmatter's volatile `last_updated` stamp neutralised. Pure."""
    return _LAST_UPDATED_RE.sub("last_updated: <normalizado>", text, count=1)


def _assert_quarantine_target(path: Path, repo_root: Path, slug: str) -> None:
    """The quarantine write stays inside docs/analysis/<slug>/proposed/ — never an
    authoritative layer (fail-closed containment of the un-gated creation write)."""
    prefix = f"docs/analysis/{slug}/{quarantine.QUARANTINE_SUBDIR}/"
    actual = path.resolve().relative_to(repo_root.resolve()).as_posix()
    if not actual.startswith(prefix):
        raise ValueError(f"quarantine write escaped {prefix}: {actual}")


def write_quarantined(repo_root: Path, slug: str, artifact: dict) -> str:
    """Write the artifact's rendered markdown under the quarantine dir; return the
    repo-relative path (also stamped onto the artifact as `quarantine_path`)."""
    rel = quarantine.quarantine_relpath(slug, artifact["intended_destination"])
    path = repo_root / rel
    _assert_quarantine_target(path, repo_root, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(phase4_create.render(artifact), encoding="utf-8")
    artifact["quarantine_path"] = rel
    return rel


def promote(repo_root: Path, slug: str, artifact: dict) -> str | None:
    """Move an ACCEPTED artifact from quarantine to its authoritative destination.

    Returns None for a normal move, or `ALREADY_AT_DESTINATION` when the
    destination already holds the same content — a re-run over a source a previous
    run already promoted, which is the same landing, not a refusal. The comparison
    neutralises the canonical frontmatter's `last_updated` stamp on both sides:
    that field is the run's own date, so without it a re-run on any later day
    would read its own landing as a conflict. The destination file is left exactly
    as it is — a re-run never rewrites an authoritative file.

    Fail-closed: refuses a destination occupied by DIFFERENT content (a generated
    artifact never overwrites an authoritative file) and a missing quarantine
    copy."""
    dest_rel = artifact["intended_destination"]
    dest = repo_root / dest_rel
    src_rel = artifact.get("quarantine_path") or quarantine.quarantine_relpath(slug, dest_rel)
    src = repo_root / src_rel
    if not src.is_file():
        raise ValueError(f"promotion refused — no quarantined copy at {src_rel}")
    content = src.read_text(encoding="utf-8")
    if dest.exists():
        if _comparable(dest.read_text(encoding="utf-8")) != _comparable(content):
            raise ValueError(f"promotion refused — destination exists: {dest_rel}")
        src.unlink()
        return ALREADY_AT_DESTINATION
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    src.unlink()
    return None


def _same_exercise_already_promoted(exercises_root: Path, repo_root: Path,
                                    rendered: str) -> str | None:
    """The repo-relative path of an exercise in this level that already holds exactly
    `rendered`, or None. I/O.

    Exercise filenames carry an allocated number, so a re-run over a source a prior
    run already promoted would otherwise take the next free number and write a
    byte-identical duplicate into curriculum/. Matching by content routes the
    artifact at the file it already landed as, where `promote` recognises it."""
    if not exercises_root.is_dir():
        return None
    for path in sorted(exercises_root.glob("exercise-*.md")):
        if path.read_text(encoding="utf-8") == rendered:
            return path.resolve().relative_to(repo_root.resolve()).as_posix()
    return None


def _level_of(level_dir: str) -> int:
    """The numeric level of a repo level dir (`03-nivel-3-…` → 3). Fail-closed."""
    m = _LEVEL_RE.search(level_dir)
    if not m:
        raise ValueError(f"cannot derive exercise level from level dir: {level_dir!r}")
    return int(m.group(1))


def _eval_artifact(artifact: dict, pattern: dict) -> dict:
    """The compact artifact the adversarial evaluator scores (first-loop shape). Pure."""
    return {"type": artifact["type"], "title": artifact["title"],
            "content": artifact["content"], "source_pattern": pattern,
            "phase3_verdict": artifact["phase3_verdict"]}


def run_fase4(repo_root: Path, slug: str, classifications: list[dict], patterns: list[dict],
              extraction: dict, index: dict, *, openai_key: str, zai_key: str,
              source_file: str, reporting_classifications: list[dict] | None = None,
              level_dir: str = phase4_create.DEFAULT_LEVEL_DIR,
              min_mean: float = evaluator.PROVISIONAL_MIN_MEAN,
              dup_threshold: float = dedup.DUP_THRESHOLD,
              zai_client=None, eval_client=None, embed_fn=None, validate_fn=None,
              validate_destination_fn=None, today: str | None = None) -> dict:
    """The full Fase-4 run for one source. Returns {manifest, outcomes, promoted, held}.

    Every external call is injectable (`zai_client`/`eval_client`/`embed_fn`/
    `validate_fn`/`validate_destination_fn`; None → the module default).
    `validate_fn` is called once after all quarantine writes; its bool feeds every
    artifact's gate report. Because that repo-wide run cannot see the canonical-/
    curriculum-scoped checks while the artifact sits in quarantine, each artifact
    is additionally validated by the same validator at its intended destination
    (`spine.validate_destination`, fail-closed) before it can be promoted; its
    concrete violations are carried into the hold reasons, and a validator that
    could not run is recorded as such rather than as a content violation.
    `level_dir` is INTERIM (see `phase4_create.DEFAULT_LEVEL_DIR`): the resolved
    level is recorded per exercise in the manifest for Etapa 7 (#265).

    `classifications` scopes planning and generation. A caller that deliberately
    plans a subset (`first_loop` passes the one selected Missing) passes the full
    classified set as `reporting_classifications` so the manifest's skipped rows
    still describe every pattern Fase 3 judged, not just the planned one; None
    keeps the two identical.

    Gating is per artifact: an unexpected failure on one (a provider outage, say)
    holds that artifact with the concrete error and the loop continues, so the
    manifest is always written — with `gate.phase4_complete` false to say the run
    did not finish cleanly. Generation failures still abort before any promotion
    happens, leaving no manifest at all rather than an untruthful one."""
    import retrieval

    if zai_client is None:
        from glm import chat_json as zai_client
    if eval_client is None:
        from openai_chat import chat_json as eval_client
    if embed_fn is None:
        from embed import embed_texts as embed_fn
    if validate_fn is None:
        from spine import validate_obsidian_ok as validate_fn
    if validate_destination_fn is None:
        from spine import validate_destination as validate_destination_fn

    today = today or date.today().isoformat()
    plan = phase4_routing.plan_of_work(classifications)
    by_name = {p.get("name"): p for p in patterns}
    by_pattern_cls = {c.get("pattern"): c for c in classifications}
    level = _level_of(level_dir)
    exercises_root = repo_root / "curriculum" / level_dir / phase4_create.EXERCISES_SUBDIR
    existing = [f.name for f in exercises_root.glob("exercise-*.md")] if exercises_root.exists() else []
    next_number = phase4_create.next_exercise_number(existing)
    video_id = str(extraction.get("video_id", ""))

    generated: list[dict] = []
    claimed: dict[str, str] = {}
    repo_contexts: dict[str, str] = {}
    for item in plan:
        pattern = by_name.get(item["pattern"], {"name": item["pattern"]})
        cls = by_pattern_cls.get(item["pattern"], {})
        if item["pattern"] not in repo_contexts:
            repo_contexts[item["pattern"]] = retrieval.make_pattern_retriever(
                [pattern], index, openai_key, repo_root, k=6, embed_fn=embed_fn)(None)
        repo_context = repo_contexts[item["pattern"]]
        source_context = (f"Tese: {extraction.get('thesis','')}\n"
                          f"Trade-offs: {pattern.get('tradeoffs','')}")
        common = dict(slug=slug, source_file=source_file, video_id=video_id,
                      evidence=cls.get("evidence", []), source_context=source_context,
                      repo_context=repo_context, zai_key=zai_key, today=today)
        if item["category"] == "canonical":
            artifact = phase4_create.create(pattern, verdict=item["verdict"],
                                            client=zai_client, **common)
        elif item["category"] == "skill":
            artifact = phase4_create.create_skill(pattern, verdict=item["verdict"],
                                                  client=zai_client, **common)
        else:
            artifact = phase4_create.create_exercise(pattern, verdict=item["verdict"],
                                                     level=level, level_dir=level_dir,
                                                     number=next_number, client=zai_client,
                                                     **common)
            landed = _same_exercise_already_promoted(
                exercises_root, repo_root, phase4_create.render(artifact))
            if landed is None:
                next_number += 1
            else:
                artifact["intended_destination"] = landed
        artifact["priority"] = item["priority"]
        entry = {"category": item["category"], "artifact": artifact,
                 "classification": cls, "pattern": pattern}
        dest = artifact["intended_destination"]
        # Two patterns can slugify to the same destination; the later one must be
        # held, never overwrite the earlier one's quarantined copy (which would
        # promote the wrong content under the earlier artifact's passing gates).
        if dest in claimed:
            entry["collision"] = (f"colisão de destino — {dest} já reivindicado pelo "
                                  f"padrão {claimed[dest]!r} neste plano")
        else:
            claimed[dest] = item["pattern"]
            write_quarantined(repo_root, slug, artifact)
        generated.append(entry)

    validate_ok = bool(validate_fn(repo_root)) if claimed else True

    outcomes: list[dict] = []
    aborted = False
    for g in generated:
        artifact = g["artifact"]
        if g.get("collision"):
            outcomes.append({"category": g["category"], "artifact": artifact,
                             "accepted": False, "reasons": [g["collision"]],
                             "evaluation": None, "dedup": None})
            continue
        try:
            evaluation = evaluator.run(_eval_artifact(artifact, g["pattern"]), openai_key,
                                       min_mean=min_mean, client=eval_client)
            vec = embed_fn([artifact["title"] + "\n" + artifact["content"]], openai_key)[0]
            dup = dedup.is_duplicate(vec, index, dup_threshold)
            checked = validate_destination_fn(
                repo_root, artifact["intended_destination"], phase4_create.render(artifact))
            violations = list(checked["violations"])
            report = quarantine.report_from_gates(
                validate_obsidian=validate_ok,
                destination_validated=bool(checked["available"]),
                destination_valid=not violations,
                citations_ok=bool(g["classification"].get("verified")),
                duplicate=dup["duplicate"], evaluation_passed=evaluation["passed"])
            decision = quarantine.decide(report)
            accepted, reasons = decision["accepted"], decision["reasons"] + violations
            if accepted:
                try:
                    note = promote(repo_root, slug, artifact)
                except ValueError as exc:
                    # A fail-closed promotion refusal holds THIS artifact; the run
                    # still finishes and records it (manifest = the Fase-5 contract).
                    accepted, reasons = False, reasons + [str(exc)]
                else:
                    reasons = reasons + [note] if note else reasons
        except Exception as exc:
            # An unexpected failure (a provider call, the filesystem) holds THIS
            # artifact and marks the run incomplete, so the manifest is still
            # written and never claims a phase that did not finish.
            aborted = True
            outcomes.append({"category": g["category"], "artifact": artifact,
                             "accepted": False,
                             "reasons": [f"erro inesperado no gating: {exc!r}"],
                             "evaluation": None, "dedup": None})
            continue
        outcomes.append({"category": g["category"], "artifact": artifact,
                         "accepted": accepted, "reasons": reasons,
                         "evaluation": evaluation, "dedup": dup})

    manifest = artifact_manifest.build_manifest(
        slug, today,
        classifications if reporting_classifications is None else reporting_classifications,
        outcomes,
        planned_categories={item["category"] for item in plan},
        complete=not aborted)
    out = package_dir(repo_root, slug)
    out.mkdir(parents=True, exist_ok=True)
    for suffix, text in (("yaml", artifact_manifest.manifest_yaml(manifest)),
                         ("md", artifact_manifest.manifest_md(manifest))):
        body = text if text.endswith("\n") else text + "\n"
        (out / f"{slug}-artifacts.{suffix}").write_text(body, encoding="utf-8")

    return {"manifest": manifest, "outcomes": outcomes,
            "promoted": [o["artifact"]["intended_destination"] for o in outcomes if o["accepted"]],
            "held": [{"path": o["artifact"]["intended_destination"], "reasons": o["reasons"]}
                     for o in outcomes if not o["accepted"]]}
