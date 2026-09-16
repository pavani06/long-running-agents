"""Fase 6 (#265) — curriculum integration by section splice.

The highest-risk phase (it edits existing curriculum in place) is governed by a
code-controlled boundary: CODE selects the exact existing curriculum section via
the retrieval index (heading + line range, provably aligned with the indexed
chunk), the model sees ONLY that bounded section and returns ONLY a replacement
body, and CODE applies the splice at the known limits. The model never chooses
file boundaries and never rewrites a whole curriculum document.

Deterministic gate: the diff must be localized (every changed line inside the
section body range) and additive in the issue's sense (only the target file
changed; `docs/canonical/` untouched; no new curriculum files). Promotion still
passes the Etapa-3 machine gate (#261 lib: adversarial evaluator + cosine dedup
+ destination-scoped validate-obsidian), routed fail-closed by
`quarantine.decide` — accepted splices land in the worktree behind a human-gated
PR; rejected ones go to `docs/analysis/<slug>/proposed/` and never touch the
authoritative layer.

Exercise routing reads the manifest's existing `level` field as the sole
authority: an exercise entry's retrieval is scoped to that level's directory,
verbatim — there is no second level classifier and no correction layer.

Idempotent rerun: a replacement identical to the current section body is a
clean detectable skip (`status: "skipped"`), not a rewrite.

Pure parts (unit-tested): section localization, splice application, both diff
gates, prompt assembly, replacement parsing. `run` needs both keys but every
external call (GLM, evaluator, embeddings, validate) is injectable, matching
the Fase 3/4/5 convention.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import artifact_manifest
import dedup
import evaluator
import quarantine
import phase5_integrate
from chunking import _FENCE, _HEADING, split_sections  # same heading semantics as the index
from index_store import records_for

# The bounded-knowledge cap mirrors retrieval.MAX_SECTION_CHARS/MAX_CONTEXT_CHARS:
# the generator prompt must stay well inside the provider's input limit.
_MAX_KNOWLEDGE_CHARS = 4000

_CITATION = re.compile(r"[\w./-]+\.(?:md|py|ts|js|yaml|yml|json):\d+")


@dataclass(frozen=True)
class SectionRange:
    """A section's raw coordinates in the FULL file (frontmatter included).

    `start` is the 0-based line index of the heading line; `end` is exclusive.
    A section spans its heading line through the line before the next ATX
    heading (code fences excluded) — the same unit `chunking.split_sections`
    embeds, but in file coordinates so code can splice at known limits."""

    heading: str
    level: int
    start: int
    end: int


def _body_start_line(text: str) -> int:
    """0-based line index of the first line after the frontmatter (0 if none).

    Mirrors `chunking.strip_frontmatter` exactly so file coordinates and the
    chunker's body agree."""
    if not text.startswith("---"):
        return 0
    end = text.find("\n---", 3)
    if end == -1:
        return 0
    nl = text.find("\n", end + 1)
    if nl == -1:
        return 0
    return text.count("\n", 0, nl + 1)


def locate_section(file_text: str, heading: str, *, ordinal: int = 0) -> SectionRange:
    """Heading + raw line range for the `ordinal`-th heading with this exact
    text. Fences are tracked so a `#` inside ``` ``` is never a heading — the
    same rule as the chunker. Fail-closed when absent. Pure."""
    body_start = _body_start_line(file_text)
    lines = file_text.split("\n")
    seen = 0
    in_fence = False
    open_range: SectionRange | None = None
    for i in range(body_start, len(lines)):
        line = lines[i]
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = _HEADING.match(line)
        if not m:
            continue
        if open_range is not None:
            return SectionRange(open_range.heading, open_range.level, open_range.start, i)
        if m.group(2).strip() == heading:
            if seen == ordinal:
                open_range = SectionRange(heading, len(m.group(1)), i, len(lines))
            seen += 1
    if open_range is not None:
        return open_range   # section runs to EOF
    raise ValueError(f"section not found: {heading!r} (ordinal {ordinal})")


def locate_by_id(file_text: str, path: str, record_id: str) -> tuple[SectionRange, str]:
    """Localize the exact indexed record in the CURRENT file content.

    Walks `records_for` (the index's own construction) so the id match is exact
    — duplicate headings get the right ordinal by construction — and asserts the
    localized lines still equal the indexed chunk text, so the retrieval hit and
    the splice bounds can never drift apart. Returns (range, section_text).
    Pure."""
    recs = records_for(path, file_text)
    idx = next((i for i, r in enumerate(recs) if r.id == record_id), None)
    if idx is None:
        raise ValueError(f"index record not in current file: {record_id}")
    rec = recs[idx]
    if rec.level == 0:
        raise ValueError("preamble has no heading to splice at")
    ordinal = sum(1 for r in recs[:idx] if r.heading == rec.heading)
    rng = locate_section(file_text, rec.heading, ordinal=ordinal)
    lines = file_text.split("\n")
    chunk = "\n".join(lines[rng.start:rng.end]).strip("\n")
    if chunk != rec.text:
        raise ValueError(f"localization drift vs index record: {record_id}")
    return rng, rec.text


def body_range(rng: SectionRange, lines: list[str]) -> tuple[int, int]:
    """The replaceable body bounds [start+1, end) with trailing blank lines
    kept out of the replacement (the chunker ignores them; splicing must too).
    Pure."""
    end = rng.end
    while end > rng.start + 1 and lines[end - 1].strip() == "":
        end -= 1
    return rng.start + 1, end


def apply_splice(file_text: str, rng: SectionRange, body: str) -> tuple[str, str]:
    """Replace the section BODY (the heading line is code-owned) at the known
    limits. Returns (updated_text, status) with status "changed" | "unchanged";
    re-applying the same body over an already-spliced file is a detected no-op.
    Pure."""
    lines = file_text.split("\n")
    b0, b1 = body_range(rng, lines)
    new_section = [lines[rng.start]] + body.strip("\n").split("\n")
    updated = "\n".join(lines[:rng.start] + new_section + lines[b1:])
    return updated, ("changed" if updated != file_text else "unchanged")


def localized_diff_ok(original: str, updated: str, b0: int, b1: int) -> tuple[bool, list[str]]:
    """The diff gate: every changed line must lie inside the body range
    [b0, b1). Pure."""
    a = original.split("\n")
    b = updated.split("\n")
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    violations: list[str] = []
    for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if i1 < b0 or i2 > b1:
            violations.append(f"diff fora da seção: linhas {i1 + 1}..{i2} ({tag})")
    return not violations, violations


def changed_paths_ok(changed: list[str], target: str) -> tuple[bool, list[str]]:
    """The additive/file-set gate: exactly the target file changed — which
    forbids `docs/canonical/` edits, new curriculum files and any straggler.
    Pure."""
    violations: list[str] = []
    if target not in changed:
        violations.append(f"arquivo-alvo não modificado: {target}")
    for p in sorted(set(changed) - {target}):
        if p.startswith("docs/canonical/"):
            violations.append(f"docs/canonical/ modificado: {p}")
        elif p.startswith("curriculum/"):
            violations.append(f"arquivo novo/extra no currículo: {p}")
        else:
            violations.append(f"caminho inesperado modificado: {p}")
    return not violations, violations


def build_messages(heading: str, section_text: str, knowledge: str, *,
                   path: str) -> list[dict]:
    """The bounded model input: ONLY this section (the code keeps the heading
    line) plus the promoted knowledge. JSON-strict output {"body": string}.
    Pure."""
    system = (
        "Você revisa UMA seção de currículo, e somente ela. "
        "Entrada: o texto atual da seção e o conhecimento promovido (fonte). "
        "Saída: APENAS um objeto JSON válido {\"body\": string} com o novo CORPO "
        "da seção (sem a linha de heading — o código a preserva). Regras: "
        "enriquecimento aditivo fundamentado no conhecimento promovido; mesmo "
        "idioma da seção; nenhum heading ATX; nenhum link ou wikilink novo; "
        "nenhum frontmatter; não invente fatos fora da fonte."
    )
    user = (f"ARQUIVO: {path}\n\n"
            f"SEÇÃO ATUAL (heading: {heading!r}):\n{section_text}\n\n"
            f"CONHECIMENTO PROMOVIDO (fonte):\n{knowledge[:_MAX_KNOWLEDGE_CHARS]}")
    return [{"role": "system", "content": system},
            {"role": "user", "content": user}]


def parse_replacement(reply: dict) -> str:
    """Validate the model's replacement body. Pure."""
    body = reply.get("body")
    if not isinstance(body, str) or not body.strip():
        raise ValueError("splice: 'body' deve ser string não vazia")
    return body.strip()


def level_dir(repo_root: Path, level: int) -> str:
    """The curriculum directory for a manifest `level` value — used verbatim,
    never recomputed or corrected (the producer's decision boundary). Pure
    path computation over a repo glob (I/O)."""
    prefix = f"{level:02d}-nivel-{level}-"
    dirs = sorted(p.name for p in (repo_root / "curriculum").iterdir()
                  if p.is_dir() and p.name.startswith(prefix))
    if len(dirs) != 1:
        raise ValueError(f"manifest level {level}: expected one curriculum dir "
                         f"matching {prefix}*, found {dirs}")
    return f"curriculum/{dirs[0]}"


def _citations_ok(body: str, repo_root: Path) -> bool:
    """grep-verify every file:line citation the replacement body makes; a body
    that cites nothing passes vacuously. Deterministic."""
    from grep_verify import all_ok, verify_all
    cites = [{"file": m.group(0).rsplit(":", 1)[0],
              "line": int(m.group(0).rsplit(":", 1)[1]), "quote": ""}
             for m in _CITATION.finditer(body)]
    if not cites:
        return True
    return all_ok(verify_all(cites, repo_root))


def _promoted_entries(manifest: dict) -> list[dict]:
    """Promoted curriculum-eligible entries in stable order (canonical, then
    exercise). Skills are not curriculum. Pure."""
    arts = manifest["artifacts"]
    canon = [e for e in arts.get("canonical_docs", [])
             if e.get("status") == artifact_manifest.STATUS_PROMOTED]
    ex = [e for e in arts.get("exercises", [])
          if e.get("status") == artifact_manifest.STATUS_PROMOTED]
    return canon + ex


def run(repo_root: Path, manifest_path: Path, *, zai_key: str, openai_key: str,
        index: dict, embed_fn=None, splice_client=None, eval_client=None,
        validate_fn=None, validate_destination_fn=None,
        min_mean: float = evaluator.PROVISIONAL_MIN_MEAN,
        dup_threshold: float = dedup.DUP_THRESHOLD, entry_index: int = 0,
        changed_paths: list[str] | None = None,
        today: str | None = None) -> dict:
    """One section splice for one promoted manifest entry.

    Every external call is injectable (None → the module default). `changed_paths`
    is the caller's worktree diff (`git status` relative paths); None skips the
    file-set gate (unit tests drive it explicitly). Returns the outcome record
    with the full proof chain: entry → target file/section → bounded input →
    replacement → diff gate → evaluation/dedup/decision → status."""
    import retrieval

    if splice_client is None:
        from glm import chat_json as splice_client
    if eval_client is None:
        from openai_chat import chat_json as eval_client
    if embed_fn is None:
        from embed import embed_texts as embed_fn
    if validate_fn is None:
        from spine import validate_obsidian_ok as validate_fn
    if validate_destination_fn is None:
        from spine import validate_destination as validate_destination_fn

    manifest = phase5_integrate.load_manifest(manifest_path)
    slug = manifest["meta"]["source_slug"]
    entries = _promoted_entries(manifest)
    if entry_index >= len(entries):
        raise ValueError(f"manifest has {len(entries)} promoted curriculum entry(ies); "
                         f"entry_index={entry_index}")
    entry = entries[entry_index]
    level = entry.get("level")   # exercises: the manifest's own level, verbatim

    source_path = str(entry.get("path", ""))
    source = repo_root / source_path
    if not source.is_file():
        raise ValueError(f"promoted entry file not found: {source_path}")
    source_text = source.read_text(encoding="utf-8")
    query = f"{entry.get('pattern', '')}\n{source_text[:600]}"

    qvec = embed_fn([query], openai_key)[0]
    ranked = retrieval.rank_sections(qvec, index, k=16)
    if level is not None:
        scope = level_dir(repo_root, int(level))   # manifest level, verbatim
        ranked = [r for r in ranked if str(r.get("path", "")).startswith(scope + "/")]
    else:
        ranked = [r for r in ranked if str(r.get("path", "")).startswith("curriculum/")]
    if not ranked:
        raise ValueError("retrieval: nenhuma seção de currículo acima do piso "
                         "para este item promovido")
    hit = ranked[0]

    target_rel = str(hit["path"])
    target = repo_root / target_rel
    file_text = target.read_text(encoding="utf-8")
    rng, section_text = locate_by_id(file_text, target_rel, str(hit["id"]))
    lines = file_text.split("\n")
    b0, b1 = body_range(rng, lines)

    messages = build_messages(rng.heading, section_text, source_text, path=target_rel)
    body = parse_replacement(splice_client(messages, zai_key))
    updated, status = apply_splice(file_text, rng, body)

    outcome: dict = {
        "slug": slug, "entry": entry, "level": level, "target": target_rel,
        "section": {"heading": rng.heading, "start": rng.start, "end": rng.end},
        "bounded_input": messages, "replacement": body,
    }
    if status == "unchanged":
        outcome.update({"status": "skipped",
                        "reason": "seção já contém este enriquecimento (rerun idempotente)"})
        return outcome

    localized_ok, diff_violations = localized_diff_ok(file_text, updated, b0, b1)
    if changed_paths is None:
        paths_ok, path_violations = True, []
    else:
        paths_ok, path_violations = changed_paths_ok(changed_paths, target_rel)
    gate_ok = localized_ok and paths_ok
    evaluation = evaluator.run(
        {"type": "curriculum_section_splice", "title": rng.heading, "content": body,
         "source_pattern": entry, "phase3_verdict": str(entry.get("classification", ""))},
        openai_key, min_mean=min_mean, client=eval_client)
    vec = embed_fn([f"{rng.heading}\n{body}"], openai_key)[0]
    dup = dedup.is_duplicate(vec, index, dup_threshold)
    checked = validate_destination_fn(repo_root, target_rel, updated)
    violations = list(checked["violations"])
    report = quarantine.report_from_gates(
        validate_obsidian=bool(validate_fn(repo_root)),
        destination_validated=bool(checked["available"]),
        destination_valid=not violations,
        citations_ok=_citations_ok(body, repo_root),
        duplicate=dup["duplicate"], evaluation_passed=evaluation["passed"])
    decision = quarantine.decide(report)

    gate_violations = diff_violations + path_violations
    reasons = decision["reasons"] + violations + gate_violations
    if decision["accepted"] and gate_ok:
        target.write_text(updated, encoding="utf-8")
        status = "applied"
        quarantine_path = None
    else:
        rel = quarantine.quarantine_relpath(slug, target_rel)
        qp = repo_root / rel
        qp.parent.mkdir(parents=True, exist_ok=True)
        qp.write_text(updated, encoding="utf-8")
        status = "quarantined"
        quarantine_path = rel
    outcome.update({"status": status, "diff": {"localized_ok": localized_ok,
                                               "violations": diff_violations},
                    "evaluation": evaluation, "dedup": dup, "decision": decision,
                    "reasons": reasons, "quarantine_path": quarantine_path})
    return outcome
