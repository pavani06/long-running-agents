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

Exercise routing reads the manifest entry verbatim: retrieval is scoped to the
level directory the entry's own path names, with the manifest `level` field as
the authoritative consistency check (mismatch → fail closed). There is no second
level classifier and no correction layer.

Target selection is retrieval-driven gap analysis: the best section INSIDE the
entry's curriculum scope, above the repo's calibrated similarity floor
(`floor.REPO_FLOOR`) — an unrelated destination fails closed instead of landing.

Rerun semantics — single application per index state, not unconditional
idempotence: over the CACHED index (the operator rerunning `splice` right after
one landed) the run never double-applies, because a byte-identical replacement is
a detected no-op (`status: "skipped"`) and anything else fails closed on the
index/worktree hash mismatch. After a full re-index the spliced section is
current again, so the same section can be selected and enriched a second time —
that is a fresh splice behind the same human PR gate, not a silent one.

Size bounds, symmetric around one constant: a section beyond
`_MAX_SECTION_CHARS` is not splice material and fails closed (the section is
never truncated into the prompt), and so does a replacement body beyond that same
cap — the phase can never manufacture a section it would itself refuse next run.
A replacement that shrinks the body past `_MIN_BODY_RATIO` is held in quarantine,
so a short summary can never silently delete curriculum.

Pure parts (unit-tested): section localization, splice application, both diff
gates, prompt assembly, replacement parsing. `run` needs both keys but every
external call (GLM, evaluator, embeddings, validate) is injectable, matching
the Fase 3/4/5 convention.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path

import artifact_manifest
import dedup
import evaluator
import quarantine
import phase5_integrate
from chunking import _FENCE, _HEADING  # same heading semantics as the index
from floor import REPO_FLOOR
from index_store import records_for

# The bounded-knowledge cap mirrors retrieval.MAX_SECTION_CHARS/MAX_CONTEXT_CHARS:
# the generator prompt must stay well inside the provider's input limit.
_MAX_KNOWLEDGE_CHARS = 4000

# The section itself goes into the prompt IN FULL — the model rewrites exactly
# what it sees, so truncating it would make the splice replace text the model was
# never shown. A section bigger than this therefore fails closed instead: with the
# knowledge cap above, the prompt stays around 12k chars, the same "stay inside
# the provider's input limit" rationale. The repo has a handful of 40-77k-char
# sections; they are not section-splice material. The SAME cap bounds the
# replacement body: one rule, one constant, so a splice can never manufacture a
# section that the next run would itself refuse to splice.
_MAX_SECTION_CHARS = 8000

# An in-place revision is additive: the new body may be tightened, but a body
# below this fraction of the original is content LOSS (e.g. the model answering a
# huge section with a short summary), not a revision. Deterministic, so it holds
# the proposal in quarantine instead of landing it.
_MIN_BODY_RATIO = 0.5

_CITATION = re.compile(r"[\w./-]+\.(?:md|py|ts|js|yaml|yml|json):\d+")

# `curriculum/<NN>-nivel-<level>-<name>/…` — the level directory an artifact path
# already names, and the numeric level it declares.
_LEVEL_DIR = re.compile(r"^curriculum/(\d{2}-nivel-(\d+)[^/]*)/")


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


def locate_by_id(file_text: str, path: str, record_id: str, *,
                 indexed_hash: str) -> tuple[SectionRange, str, bool]:
    """Localize the exact indexed record in the CURRENT file content.

    Walks `records_for` (the index's own construction) so the id match is exact
    — duplicate headings get the right ordinal by construction — and asserts the
    localized lines equal that chunk, so the retrieval hit and the splice bounds
    can never drift apart. Returns (range, section_text, index_fresh), where
    `index_fresh` says whether the chunk still hashes to what the INDEX stored:
    a hit whose vector describes a stale version of the file must not drive a
    splice, and the caller owns that call because one stale case — a rerun over
    an already-spliced section — is the documented idempotent skip. Pure."""
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
    return rng, rec.text, rec.hash == indexed_hash


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


def body_preserved_ok(original_body: str, body: str) -> tuple[bool, list[str]]:
    """The content-preservation gate: the replacement may not shrink the section
    body below `_MIN_BODY_RATIO` of what was there. Pure."""
    floor_chars = int(len(original_body.strip()) * _MIN_BODY_RATIO)
    if len(body.strip()) < floor_chars:
        return False, [f"corpo encurtado além do limite: {len(body.strip())} chars < "
                       f"{floor_chars} ({_MIN_BODY_RATIO:.0%} do original)"]
    return True, []


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
    """Validate the model's replacement body. Pure.

    The body is spliced between known section limits, so it must not carry
    structure the code owns: an ATX heading outside a fence would create or
    destroy a section boundary inside the spliced range (re-chunking the file on
    the next run), and frontmatter belongs to the file, not to a section. Nor may
    it exceed `_MAX_SECTION_CHARS`, the same cap that decides which sections are
    splice-eligible — the phase never produces a section it would later refuse."""
    body = reply.get("body")
    if not isinstance(body, str) or not body.strip():
        raise ValueError("splice: 'body' deve ser string não vazia")
    body = body.strip()
    if len(body) > _MAX_SECTION_CHARS:
        raise ValueError(f"splice: corpo de {len(body)} chars acima do limite de "
                         f"{_MAX_SECTION_CHARS} para uma seção")
    if body.startswith("---"):
        raise ValueError("splice: 'body' não pode abrir com frontmatter")
    in_fence = False
    for line in body.split("\n"):
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and _HEADING.match(line):
            raise ValueError(f"splice: 'body' não pode conter heading ATX: {line.strip()!r}")
    if in_fence:
        raise ValueError("splice: 'body' tem code fence não fechado")
    return body


def _index_scoped(index: dict, keep) -> dict:
    """The index narrowed to the records `keep` accepts, as an index dict the
    ranking/dedup helpers consume unchanged. Pure."""
    return {**index, "records": {rid: rec for rid, rec in index.get("records", {}).items()
                                 if keep(rid, rec)}}


def splice_scope(entry_path: str, level) -> str:
    """The curriculum path prefix retrieval may select a target from. Pure.

    An exercise is routed to the level directory its OWN manifest path names —
    the producer already placed it there — with the manifest `level` field as the
    authoritative consistency check: a path outside a level directory, a missing
    level, or a level that disagrees with the path fails closed. There is no
    second classifier and no level→directory mapping to disagree with (the repo
    has several directories per level). A canonical entry carries no level and is
    scoped to the whole curriculum."""
    m = _LEVEL_DIR.match(entry_path or "")
    if level is None or level == "":
        if m:
            raise ValueError(f"entrada de exercício sem level no manifesto: {entry_path}")
        return "curriculum/"
    if not m:
        raise ValueError(f"manifest level {level}: caminho da entrada não está sob um "
                         f"diretório de nível do currículo: {entry_path!r}")
    if int(m.group(2)) != int(level):
        raise ValueError(f"manifest level {level} diverge do diretório do caminho: "
                         f"{m.group(1)}")
    return f"curriculum/{m.group(1)}/"


def eligible_target(path: str, scope: str, *, exclude: str) -> bool:
    """Whether an indexed section's file may be spliced. Pure.

    Inside the entry's scope, and inside a curriculum SUBdirectory: the top-level
    `curriculum/*.md` surfaces (INDEX/README/MASTER_PLAN are rewritten
    deterministically by Fase 5; GLOSSARY/FAQ/QUICK_START/… are hand-curated
    indexes) have their own owner and are never section-splice targets. `exclude`
    is the promoted entry's own path: an exercise already sitting in its level
    directory is the SOURCE of this splice, never its destination."""
    return (path.startswith(scope) and "/" in path[len("curriculum/"):]
            and path != exclude)


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
        index: dict, changed_paths_fn, embed_fn=None, splice_client=None,
        eval_client=None, validate_fn=None, validate_destination_fn=None,
        min_mean: float = evaluator.PROVISIONAL_MIN_MEAN,
        dup_threshold: float = dedup.DUP_THRESHOLD) -> dict:
    """One section splice for the first promoted manifest entry.

    Every external call is injectable (None → the module default) except
    `changed_paths_fn(target) -> [repo-relative path]`, which is required: the
    file-set gate has no fail-open mode. It is called AFTER the splice is written
    so it reports what the splice itself changed in the worktree; a failing
    file-set gate restores the file and routes to quarantine. Returns the outcome
    record with the full proof chain: entry → target file/section → bounded input
    → replacement → diff gate → evaluation/dedup/decision → status."""
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
    if not entries:
        raise ValueError("manifest has no promoted curriculum entry to splice")
    entry = entries[0]
    level = entry.get("level")   # exercises: the manifest's own level, verbatim

    source_path = str(entry.get("path", ""))
    source = repo_root / source_path
    if not source.is_file():
        raise ValueError(f"promoted entry file not found: {source_path}")
    source_text = source.read_text(encoding="utf-8")
    query = f"{entry.get('pattern', '')}\n{source_text[:600]}"

    qvec = embed_fn([query], openai_key)[0]
    scope = splice_scope(source_path, level)
    in_scope = _index_scoped(index, lambda _rid, rec: (
        eligible_target(str(rec.get("path", "")), scope, exclude=source_path)
        and int(rec.get("level") or 0) > 0))
    ranked = retrieval.rank_sections(qvec, in_scope, k=1, floor=REPO_FLOOR)
    if not ranked:
        raise ValueError(f"retrieval: nenhuma seção de currículo em {scope} acima do "
                         f"piso de similaridade ({REPO_FLOOR})")
    hit = ranked[0]

    target_rel = str(hit["path"])
    target = repo_root / target_rel
    if not target.is_file():
        raise ValueError(f"índice aponta para arquivo inexistente: {target_rel}")
    file_text = target.read_text(encoding="utf-8")
    rng, section_text, index_fresh = locate_by_id(
        file_text, target_rel, str(hit["id"]),
        indexed_hash=str(index.get("records", {}).get(str(hit["id"]), {}).get("hash", "")))
    lines = file_text.split("\n")
    b0, b1 = body_range(rng, lines)
    if len(section_text) > _MAX_SECTION_CHARS:
        raise ValueError(f"seção grande demais para splice: {rng.heading!r} em "
                         f"{target_rel} ({len(section_text)} chars > "
                         f"{_MAX_SECTION_CHARS})")

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
    if not index_fresh:
        raise ValueError(f"índice desatualizado vs arquivo atual: {hit['id']}")

    localized_ok, diff_violations = localized_diff_ok(file_text, updated, b0, b1)
    preserved_ok, size_violations = body_preserved_ok("\n".join(lines[b0:b1]), body)
    evaluation = evaluator.run(
        {"type": "curriculum_section_splice", "title": rng.heading, "content": body,
         "source_pattern": entry, "phase3_verdict": str(entry.get("classification", ""))},
        openai_key, min_mean=min_mean, client=eval_client)
    vec = embed_fn([f"{rng.heading}\n{body}"], openai_key)[0]
    others = _index_scoped(index, lambda rid, _rec: rid != str(hit["id"]))
    dup = dedup.is_duplicate(vec, others, dup_threshold)
    checked = validate_destination_fn(repo_root, target_rel, updated)
    violations = list(checked["violations"])
    report = quarantine.report_from_gates(
        validate_obsidian=bool(validate_fn(repo_root)),
        destination_validated=bool(checked["available"]),
        destination_valid=not violations,
        citations_ok=_citations_ok(body, repo_root),
        duplicate=dup["duplicate"], evaluation_passed=evaluation["passed"])
    decision = quarantine.decide(report)

    accepted = decision["accepted"] and localized_ok and preserved_ok
    path_violations: list[str] = []
    if accepted:
        target.write_text(updated, encoding="utf-8")
        paths_ok, path_violations = changed_paths_ok(changed_paths_fn(target_rel), target_rel)
        if not paths_ok:
            target.write_text(file_text, encoding="utf-8")
            accepted = False

    reasons = (decision["reasons"] + violations + diff_violations + size_violations
               + path_violations)
    if accepted:
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
