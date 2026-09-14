"""Concept Canon loader + validation for the metamorphic eval-harness (#288).

The canon is curated ground-truth: concepts with a canonical definition, aliases,
positive/negative examples, an `expected_repo_state.exists` correctness anchor and
— for anything that exists even partially — mandatory `evidence[]` pointing at
REAL repo paths. It also carries the 5 hand-authored paraphrases per concept, the
near-miss pairs (T4) and the reranker sanity pairs (condition (c)).

Structural validation (`validate_structure`) and the evidence-substring check
(`evidence_substring_ok`) are pure and unit-tested; `load_canon` and
`check_evidence_on_disk` are the thin file-reading wrappers.

The invariants encode the issue's non-negotiables, not an arbitrary checklist:
  - condition (a): a concept that exists MUST carry evidence; a Missing concept
    carries none (nothing to cite);
  - a concept's verdict and its `exists` flag must agree.
"""
from __future__ import annotations

from pathlib import Path

VERDICTS = {"Missing", "Partial", "Exists", "Better"}
EXISTENCE_VERDICTS = {"Partial", "Exists", "Better"}  # anything that claims coverage
GRANULARITY = {"equivalent", "broader_than", "narrower_than",
               "related_but_distinct", "unrelated"}


class CanonError(Exception):
    """The canon is structurally invalid, or its evidence does not resolve."""


def profile_text(concept: dict) -> str:
    """The text embedded to represent a concept in stage-1 retrieval. Pure.

    Definition + aliases + positive examples — the surface a paraphrase should
    land near. Negative examples are deliberately excluded (they describe what the
    concept is NOT and would pull the centroid the wrong way)."""
    parts = [concept.get("canonical_definition", "")]
    parts += list(concept.get("aliases", []) or [])
    parts += list(concept.get("positive_examples", []) or [])
    return "\n".join(p for p in parts if p).strip()


def concept_ids(canon: dict) -> list[str]:
    return [c.get("concept_id", "") for c in canon.get("concepts", [])]


def concept_by_id(canon: dict) -> dict[str, dict]:
    return {c["concept_id"]: c for c in canon.get("concepts", []) if c.get("concept_id")}


def all_variants(canon: dict) -> list[dict]:
    """Flatten to [{variant, concept_id, expected_verdict, exists}] — the 50 cases.

    Each concept's paraphrases inherit its true concept_id and expected verdict;
    this is the ground-truth the metrics score predictions against."""
    out: list[dict] = []
    for c in canon.get("concepts", []):
        for v in c.get("variants", []) or []:
            out.append({"variant": v, "concept_id": c["concept_id"],
                        "expected_verdict": c.get("expected_verdict"),
                        "exists": bool(c.get("expected_repo_state", {}).get("exists"))})
    return out


def summary(canon: dict) -> dict:
    """Counts for the report: concepts, variants, and the exists/missing/partial split."""
    concepts = canon.get("concepts", [])
    exists = sum(1 for c in concepts if c.get("expected_verdict") in ("Exists", "Better"))
    missing = sum(1 for c in concepts if c.get("expected_verdict") == "Missing")
    partial = sum(1 for c in concepts if c.get("expected_verdict") == "Partial")
    variants = sum(len(c.get("variants", []) or []) for c in concepts)
    return {"concepts": len(concepts), "variants": variants,
            "exists": exists, "missing": missing, "partial": partial}


def validate_structure(canon: dict) -> list[str]:
    """Return a list of structural problems (empty == valid). Pure.

    Enforces the issue's non-negotiables: existence is paired with an evidence
    anchor, and each concept's verdict agrees with its `exists` flag."""
    problems: list[str] = []
    concepts = canon.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        return ["canon: 'concepts' must be a non-empty list"]

    seen: set[str] = set()
    ids = set()
    for i, c in enumerate(concepts):
        cid = c.get("concept_id")
        where = f"concept[{i}] ({cid or '?'})"
        if not cid or not isinstance(cid, str):
            problems.append(f"{where}: missing concept_id")
            continue
        ids.add(cid)
        if cid in seen:
            problems.append(f"{where}: duplicate concept_id")
        seen.add(cid)
        if not (c.get("canonical_definition") or "").strip():
            problems.append(f"{where}: empty canonical_definition")
        for field in ("aliases", "positive_examples", "negative_examples", "variants", "evidence"):
            if not isinstance(c.get(field), list):
                problems.append(f"{where}: '{field}' must be a list")
        state = c.get("expected_repo_state")
        if not isinstance(state, dict) or not isinstance(state.get("exists"), bool):
            problems.append(f"{where}: expected_repo_state.exists must be a bool")
            continue
        verdict = c.get("expected_verdict")
        if verdict not in VERDICTS:
            problems.append(f"{where}: expected_verdict {verdict!r} not in {sorted(VERDICTS)}")
            continue
        exists = state["exists"]
        evidence = c.get("evidence") if isinstance(c.get("evidence"), list) else []
        # condition (a): existence must be anchored to real evidence; Missing has none.
        if exists and not evidence:
            problems.append(f"{where}: exists=true but evidence[] is empty (condition a)")
        if not exists and evidence:
            problems.append(f"{where}: exists=false but carries evidence[] (a Missing concept cites nothing)")
        if exists and verdict == "Missing":
            problems.append(f"{where}: exists=true contradicts verdict 'Missing'")
        if not exists and verdict in EXISTENCE_VERDICTS:
            problems.append(f"{where}: exists=false contradicts verdict {verdict!r}")
        for j, e in enumerate(evidence):
            if not isinstance(e, dict) or not e.get("file"):
                problems.append(f"{where}: evidence[{j}] must be an object with a 'file'")

    for i, pair in enumerate(canon.get("near_miss_pairs", []) or []):
        if not isinstance(pair, list) or len(pair) != 2:
            problems.append(f"near_miss_pairs[{i}]: must be a 2-item list")
            continue
        for cid in pair:
            if cid not in ids:
                problems.append(f"near_miss_pairs[{i}]: unknown concept_id {cid!r}")

    for i, s in enumerate(canon.get("reranker_sanity", []) or []):
        if not isinstance(s, dict) or not s.get("a") or not s.get("b") \
                or not isinstance(s.get("same"), bool):
            problems.append(f"reranker_sanity[{i}]: needs non-empty 'a', 'b' and a bool 'same'")
    return problems


def evidence_substring_ok(quote: str, file_text: str) -> bool:
    """True if `quote` (whitespace-collapsed) appears anywhere in `file_text`. Pure.

    Robust to line drift: the curated canon anchors a concept to a real string in
    a real file, not a pinned line number (the live Gate C uses grep_verify with
    line+quote for the classifier's own citations)."""
    import re
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    return bool(quote) and norm(quote) in norm(file_text)


def check_evidence_on_disk(canon: dict, repo_root: Path, *, reader=None) -> list[str]:
    """Verify every concept's evidence file exists and every quote resolves (I/O).

    `reader(path)->str|None` is injectable (None == file missing) so the pure
    resolution logic is unit-testable without disk."""
    if reader is None:
        def reader(rel: str) -> str | None:
            fp = repo_root / rel
            return fp.read_text(encoding="utf-8") if fp.is_file() else None
    problems: list[str] = []
    cache: dict[str, str | None] = {}
    for c in canon.get("concepts", []):
        for e in c.get("evidence", []) or []:
            f = e.get("file", "")
            if f not in cache:
                cache[f] = reader(f)
            text = cache[f]
            if text is None:
                problems.append(f"{c.get('concept_id')}: evidence file not found: {f}")
                continue
            q = e.get("quote", "")
            if q and not evidence_substring_ok(q, text):
                problems.append(f"{c.get('concept_id')}: quote not found in {f}: {q!r}")
    return problems


def load_canon(path: Path) -> dict:
    """Read + structurally validate the canon YAML. Raises CanonError on any
    structural problem (evidence-on-disk is checked separately, where a repo_root
    is available)."""
    import yaml
    canon = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    problems = validate_structure(canon)
    if problems:
        raise CanonError("invalid canon:\n  - " + "\n  - ".join(problems))
    return canon
