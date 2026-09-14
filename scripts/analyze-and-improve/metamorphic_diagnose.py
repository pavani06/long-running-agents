"""Gate-B dispersion diagnostic (#288 follow-up) — retrieval vs classifier.

The #288 PoC showed T2 verdict-invariance at 70%: paraphrases of one concept get
different verdicts. That dispersion has two candidate causes, and the fix differs
by cause:

  retrieval-driven  — each paraphrase embeds differently → retrieves DIFFERENT
                      repo context → the classifier sees different evidence and
                      lands on a different verdict.
  classifier-driven — the Fase-3 GLM flips the verdict on wording alone, even when
                      shown IDENTICAL evidence.

Controlled two-arm test, per concept:
  VARIABLE arm — classify each paraphrase with its OWN retrieved context (what the
                 gate does today), and record the top-k it retrieved.
  FIXED arm    — retrieve ONE context from the canonical_definition and classify
                 all five paraphrases against that SAME context.

If FIXED converges what VARIABLE disperses → retrieval-driven. If FIXED stays
dispersed → classifier-driven. A retrieval-stability metric (top-k overlap across
the five paraphrases + whether the evidence file surfaces) corroborates.

`disagreement`, `jaccard`, `retrieval_stability`, `evidence_recall`, `attribute`
and `aggregate` are pure and unit-tested; `run` makes the live calls (Actions).
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import metamorphic_canon as mc  # noqa: E402
import metamorphic_preflight as preflight  # noqa: E402
import phase3_classify  # noqa: E402
import retrieval  # noqa: E402
import sut_view  # noqa: E402
from embed import embed_texts  # noqa: E402
from glm import GLMError, RateLimited  # noqa: E402
from retrieval import rank_sections  # noqa: E402


# ── pure metrics ─────────────────────────────────────────────────────────────
def disagreement(verdicts: list[str]) -> float:
    """1 - (modal count / n): 0.0 == fully invariant, higher == more dispersed. Pure."""
    if not verdicts:
        return 0.0
    counts = Counter(verdicts)
    return round(1 - max(counts.values()) / len(verdicts), 3)


def jaccard(sets: list[set]) -> float:
    """Mean pairwise Jaccard overlap across a list of sets. Pure.

    1.0 == every paraphrase retrieved the same sections; 0.0 == disjoint."""
    pairs = list(combinations(range(len(sets)), 2))
    if not pairs:
        return 1.0
    total = 0.0
    for i, j in pairs:
        union = sets[i] | sets[j]
        total += (len(sets[i] & sets[j]) / len(union)) if union else 1.0
    return round(total / len(pairs), 3)


def retrieval_stability(topk_ids_per_variant: list[set]) -> dict:
    """How much the retrieved top-k varies across a concept's paraphrases. Pure."""
    common = set.intersection(*topk_ids_per_variant) if topk_ids_per_variant else set()
    union = set().union(*topk_ids_per_variant) if topk_ids_per_variant else set()
    return {"mean_jaccard": jaccard(topk_ids_per_variant),
            "common": len(common), "union": len(union)}


def evidence_recall(topk_paths_per_variant: list[set], evidence_files: set) -> float:
    """Fraction of paraphrases whose top-k surfaced at least one evidence file. Pure.

    If a present concept's own evidence rarely surfaces, retrieval is starving the
    classifier — a retrieval-side explanation for a Missing verdict."""
    if not evidence_files or not topk_paths_per_variant:
        return 0.0
    hit = sum(1 for paths in topk_paths_per_variant if paths & evidence_files)
    return round(hit / len(topk_paths_per_variant), 3)


def attribute(variable_verdicts: list[str], fixed_verdicts: list[str]) -> dict:
    """Attribute a concept's dispersion. Pure.

    - no variable dispersion            -> 'invariant'
    - fixing the context did not help    -> 'classifier-driven'
    - fixing nearly removed it (<=0.2)   -> 'retrieval-driven'
    - otherwise                          -> 'mixed'"""
    var = disagreement(variable_verdicts)
    fix = disagreement(fixed_verdicts)
    if var == 0.0:
        label = "invariant"
    elif fix >= var:
        label = "classifier-driven"
    elif fix <= 0.2:
        label = "retrieval-driven"
    else:
        label = "mixed"
    return {"variable_disagreement": var, "fixed_disagreement": fix, "label": label}


def aggregate(per_concept: list[dict]) -> dict:
    """Tally the attribution labels + a one-line conclusion. Pure."""
    counts = Counter(c["attribution"]["label"] for c in per_concept)
    dispersed = [c for c in per_concept if c["attribution"]["label"] != "invariant"]
    driver = "retrieval" if counts.get("retrieval-driven", 0) > counts.get("classifier-driven", 0) \
        else "classifier" if counts.get("classifier-driven", 0) > counts.get("retrieval-driven", 0) \
        else "mixed/tie"
    return {"labels": dict(counts), "dispersed_concepts": len(dispersed),
            "dominant_driver": driver}


# ── live runner ──────────────────────────────────────────────────────────────
def _summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def _classify_with(context_retriever, variant: str, zai_key: str):
    """One classification; tolerates a bad GLM reply so a single unparseable JSON
    among the ~70 calls degrades that variant (verdict None) instead of aborting."""
    pattern = {"name": variant[:80], "problem": variant, "mechanism": ""}
    try:
        cls = phase3_classify.run([pattern], zai_key, retriever=context_retriever)
    except (GLMError, RateLimited):
        return None
    return cls[0].get("verdict")


def run(canon_path: str) -> int:
    openai_key = os.environ.get("OPENAI_API_KEY")
    zai_key = os.environ.get("ZAI_API_KEY")
    if not openai_key or not zai_key:
        _summary("diagnose: OPENAI_API_KEY and ZAI_API_KEY both required")
        return 1

    real_root = Path(__file__).resolve().parents[2]
    state_path = real_root / ".runtime" / "analyze-and-improve" / "index.json"
    if not state_path.exists():
        _summary("diagnose: index not built — run `pipeline.py index --full` first")
        return 1
    index = json.loads(state_path.read_text(encoding="utf-8"))

    canon = mc.load_canon(Path(canon_path))
    sentinel = preflight.sentinel_of(canon)
    if not sentinel:
        _summary("diagnose: canon has no _leak_sentinel — refusing (decontamination gate)")
        return 1
    by_id = mc.concept_by_id(canon)
    wanted = [c.strip() for c in os.environ.get("DIAGNOSE_CONCEPTS", "").split(",") if c.strip()]
    concept_ids = wanted or mc.concept_ids(canon)

    per_concept = []
    # Classifier sees only the disposable SUT-view (HEAD minus eval/truth); the
    # preflight proves the answer key is unreachable there before any LLM call.
    with sut_view.session(real_root) as view:
        fails = preflight.assert_isolated(view, index, Path(canon_path), sentinel)
        if fails:
            _summary("diagnose: PREFLIGHT FAILED — eval-truth reachable; refusing:\n- "
                     + "\n- ".join(fails))
            return 1
        for cid in concept_ids:
            concept = by_id.get(cid)
            if not concept:
                continue
            variants = concept.get("variants", [])
            evidence_files = {e["file"] for e in concept.get("evidence", []) if e.get("file")}

            # embed variants for the retrieval-stability trace (one batch)
            vvecs = embed_texts(variants, openai_key)
            topk_ids = [{r["id"] for r in rank_sections(v, index, k=8)} for v in vvecs]
            topk_paths = [{r["path"] for r in rank_sections(v, index, k=8)} for v in vvecs]

            # VARIABLE arm — each paraphrase drives its own retrieval (the gate's behaviour)
            variable = []
            for v in variants:
                ret = retrieval.make_pattern_retriever(
                    [{"name": v[:80], "problem": v, "mechanism": ""}], index, openai_key, view)
                variable.append(_classify_with(ret, v, zai_key))

            # FIXED arm — one context from the canonical_definition, shared by all 5
            def_ret = retrieval.make_pattern_retriever(
                [{"name": cid, "problem": concept["canonical_definition"], "mechanism": ""}],
                index, openai_key, view)
            fixed_context = def_ret(None)
            fixed_ret = lambda nm: fixed_context if nm is None else ""  # identical context, 1-shot
            fixed = [_classify_with(fixed_ret, v, zai_key) for v in variants]

            per_concept.append({
                "concept_id": cid, "expected_exists": bool(concept["expected_repo_state"]["exists"]),
                "variable_verdicts": variable, "fixed_verdicts": fixed,
                "retrieval_stability": retrieval_stability(topk_ids),
                "evidence_recall": evidence_recall(topk_paths, evidence_files),
                "attribution": attribute(variable, fixed),
            })

    _summary(_report(aggregate(per_concept), per_concept))
    print("\n=== per-concept (log) ===")
    print(json.dumps(per_concept, ensure_ascii=False, indent=2))
    return 0


def _report(agg: dict, per_concept: list[dict]) -> str:
    lines = [
        "# Gate-B dispersion diagnostic (#288) — retrieval vs classifier", "",
        f"**Driver dominante: {agg['dominant_driver']}** · labels: {agg['labels']} · "
        f"conceitos dispersos: {agg['dispersed_concepts']}", "",
        "| concept | exists | variable | fixed | var/fix disagree | retr. Jaccard | evid. recall | veredito |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for c in per_concept:
        a, s = c["attribution"], c["retrieval_stability"]
        lines.append(
            f"| `{c['concept_id']}` | {c['expected_exists']} | "
            f"{Counter(c['variable_verdicts'])} | {Counter(c['fixed_verdicts'])} | "
            f"{a['variable_disagreement']}/{a['fixed_disagreement']} | "
            f"{s['mean_jaccard']} (∩{s['common']}) | {c['evidence_recall']} | **{a['label']}** |")
    lines += [
        "", "## Como ler",
        "- **retrieval-driven**: fixar o contexto derrubou a dispersão → o problema é "
        "a recuperação variar com a paráfrase (baixo Jaccard / baixa evidence-recall corroboram).",
        "- **classifier-driven**: fixar o contexto NÃO ajudou → a Fase-3 GLM troca o "
        "veredito só pela redação, com evidência idêntica.",
        "- **mixed**: fixar reduziu mas não eliminou.",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse
    default = str(Path(__file__).resolve().parents[2] / "eval" / "truth" / "metamorphic_canon.yaml")
    ap = argparse.ArgumentParser(description="Gate-B dispersion diagnostic (#288)")
    ap.add_argument("canon", nargs="?", default=default)
    return run(ap.parse_args(argv).canon)


if __name__ == "__main__":
    raise SystemExit(main())
