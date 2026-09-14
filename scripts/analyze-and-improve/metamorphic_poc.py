"""Metamorphic eval-harness — the 50-case PoC runner (#288, Tier-B gate).

Wires the pieces the pure modules define into one live run (Actions only — needs
OPENAI_API_KEY + ZAI_API_KEY):

  reranker sanity (OpenAI)  → is the measurement instrument trustworthy? (cond. c)
  for each of the 50 cases:
    stage 1  embed the variant, cosine-rank against the concept profiles;
    stage 2  rerank the top-k with the OpenAI judge → matched concept_id;   (cond. b/c)
    classify the variant against the repo with the GLM Fase-3 classifier,
      then grep-verify its evidence.                                        (cond. a)
  T1 identification · T2 invariance · T3 dedup · T4 novelty → Gates A/B/C.

Each variant is classified INDEPENDENTLY (its own GLM call) on purpose: batching a
concept's paraphrases into one prompt would let the model trivially harmonise
their verdicts and inflate T2. That independence is the cost — ~50 GLM calls — so
`MAX_VARIANTS` allows a cheap smoke of the first N before the full run.

Exit 0 when the PoC HOLDS (all gates + sanity pass), 1 otherwise or on setup
error — so the Actions job status is the Tier-B progression gate.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import grep_verify  # noqa: E402
import metamorphic_canon as mc  # noqa: E402
import metamorphic_match as mm  # noqa: E402
import metamorphic_metrics as met  # noqa: E402
import metamorphic_rerank as rr  # noqa: E402
import phase3_classify  # noqa: E402
import retrieval  # noqa: E402
from dedup import DUP_THRESHOLD  # noqa: E402
from embed import embed_texts  # noqa: E402
from glm import GLMError, RateLimited  # noqa: E402


def _summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def safe_call(fn, default):
    """Run one network step, tolerating a bad GLM/OpenAI reply.

    A single unparseable JSON reply or a persisted rate-limit among the ~50
    per-variant calls must NOT abort the whole run — that variant degrades to the
    `default` (unmatched / unclassified) and is counted as an error in the report.
    An AuthError (bad key) is NOT caught: that is fatal for every variant and
    should stop the run. Returns (result, error_str|None)."""
    try:
        return fn(), None
    except (GLMError, RateLimited) as e:
        return default, str(e)


def classify_variant(variant: str, index: dict, openai_key: str, zai_key: str,
                     repo_root: Path) -> dict:
    """Classify one variant against the repo (GLM) + grep-verify its evidence.

    Treats the variant as a single candidate pattern so it reuses the exact
    Fase-3 classifier, hybrid retriever and one 'ask-for-more' round the spine
    uses. Returns the classification augmented with a `verified` flag."""
    pattern = {"name": variant[:80], "problem": variant, "mechanism": ""}
    retriever = retrieval.make_pattern_retriever([pattern], index, openai_key, repo_root)
    cls = phase3_classify.run([pattern], zai_key, retriever=retriever)
    verified = grep_verify.verify_all(phase3_classify.citations_of(cls), repo_root)
    phase3_classify.mark_verified(cls, verified)
    return cls[0]


def run(canon_path: str) -> int:
    openai_key = os.environ.get("OPENAI_API_KEY")
    zai_key = os.environ.get("ZAI_API_KEY")
    if not openai_key or not zai_key:
        _summary("metamorphic-poc: OPENAI_API_KEY and ZAI_API_KEY both required")
        return 1

    repo_root = Path(__file__).resolve().parents[2]
    state_path = repo_root / ".runtime" / "analyze-and-improve" / "index.json"
    if not state_path.exists():
        _summary("metamorphic-poc: index not built — run `pipeline.py index --full` first")
        return 1
    index = json.loads(state_path.read_text(encoding="utf-8"))

    canon = mc.load_canon(Path(canon_path))
    evidence_problems = mc.check_evidence_on_disk(canon, repo_root)
    if evidence_problems:
        _summary("metamorphic-poc: canon evidence does not resolve:\n- "
                 + "\n- ".join(evidence_problems))
        return 1

    by_id = mc.concept_by_id(canon)
    variants = mc.all_variants(canon)
    limit = int(os.environ.get("MAX_VARIANTS", "0") or "0")
    if limit > 0:
        variants = variants[:limit]
    rerank_k = int(os.environ.get("RERANK_K", "2") or "2")
    min_conf = float(os.environ.get("RERANK_MIN_CONFIDENCE", "0.5") or "0.5")

    # (c) reranker sanity mini-eval — validate the instrument before trusting it.
    sanity = rr.run_sanity(canon.get("reranker_sanity", []), openai_key)

    # Embed concept profiles + the variants (one batched call).
    concept_ids = mc.concept_ids(canon)
    profiles = [mc.profile_text(by_id[cid]) for cid in concept_ids]
    var_texts = [v["variant"] for v in variants]
    vecs = embed_texts(profiles + var_texts, openai_key)
    concept_vecs = dict(zip(concept_ids, vecs[:len(profiles)]))
    var_vecs = vecs[len(profiles):]

    t1_cases, t2_cases, t3_items, gate_c_cases = [], [], [], []
    per_variant = []
    errors = 0
    for v, vvec in zip(variants, var_vecs):
        candidates = mm.rank_candidates(vvec, concept_vecs, k=rerank_k)
        match, rerr = safe_call(
            lambda: mm.decide_match(
                rr.rerank_candidates(v["variant"], candidates, by_id, openai_key),
                min_confidence=min_conf),
            {"concept_id": None, "granularity_relation": None})
        predicted = match["concept_id"]

        cls, cerr = safe_call(
            lambda: classify_variant(v["variant"], index, openai_key, zai_key, repo_root),
            {"verdict": None, "verified": False})
        verdict, verified = cls.get("verdict"), bool(cls.get("verified"))
        if rerr or cerr:
            errors += 1

        t1_cases.append({"true": v["concept_id"], "predicted": predicted})
        t2_cases.append({"true": v["concept_id"], "predicted": predicted,
                         "verdict": verdict, "exists": v["exists"]})
        t3_items.append({"concept_id": v["concept_id"], "vec": vvec})
        if verdict in mc.EXISTENCE_VERDICTS:
            gate_c_cases.append({"concept_id": v["concept_id"], "verdict": verdict,
                                 "verified": verified})
        per_variant.append({"true": v["concept_id"], "predicted": predicted,
                            "granularity": match["granularity_relation"],
                            "verdict": verdict, "verified": verified,
                            "error": rerr or cerr})

    t1 = met.t1_identification(t1_cases)
    t2 = met.t2_invariance(t2_cases)
    t3 = met.t3_dedup_invariance(t3_items, threshold=DUP_THRESHOLD)
    t4 = met.t4_novelty(t1_cases, canon.get("near_miss_pairs", []))
    ga, gb, gc = met.gate_a(t1), met.gate_b(t2), met.gate_c(gate_c_cases)
    decision = met.poc_decision(ga, gb, gc, sanity)

    _summary(_report(canon, len(variants), sanity, t1, t2, t3, t4, ga, gb, gc, decision, errors))
    print("\n=== per-variant (log) ===")
    print(json.dumps(per_variant, ensure_ascii=False, indent=2))
    return 0 if decision["passed"] else 1


def _report(canon, n_run, sanity, t1, t2, t3, t4, ga, gb, gc, decision, errors=0) -> str:
    s = mc.summary(canon)
    ok = lambda b: "PASS" if b else "FAIL"
    verdict = "✅ PROSSEGUIR (PoC segura → Tier B pode avançar)" if decision["passed"] \
        else "⛔ ITERAR (PoC não segura → Tier B NÃO avança)"
    lines = [
        "# Metamorphic eval-harness — PoC (#288)", "",
        f"## Veredito: {verdict}", "",
        f"Canon: {s['concepts']} conceitos ({s['exists']} exist / {s['missing']} missing / "
        f"{s['partial']} partial), {s['variants']} paráfrases · rodadas: {n_run} variantes"
        + (f" · ⚠️ {errors} variante(s) com erro de LLM (degradadas, não abortaram)" if errors else "")
        + ".", "",
        "## Gates",
        f"- **Gate A (identificação)**: recall **{t1['recall']*100:.0f}%** "
        f"(≥{met.GATE_A_MIN_RECALL*100:.0f}%), false-merge **{t1['false_merge_rate']*100:.1f}%** "
        f"(<{met.GATE_A_MAX_FALSE_MERGE*100:.0f}%) — {ok(ga['passed'])}",
        f"- **Gate B (invariância)**: agreement **{t2['agreement']*100:.0f}%** "
        f"(≥{met.GATE_B_MIN_AGREEMENT*100:.0f}%), dispersão Exists∧Missing: "
        f"{len(t2['dispersion_flags'])}, modal ≠ expected_repo_state: "
        f"{len(t2['correctness_flags'])} — {ok(gb['passed'])}",
        f"- **Gate C (evidência)**: {gc['verified']}/{gc['total_existence']} vereditos de "
        f"existência com evidência verificada — {ok(gc['passed'])}",
        f"- **Reranker sanity (cond. c)**: {sanity['correct']}/{sanity['total']} "
        f"({sanity['accuracy']*100:.0f}%) — {ok(sanity['passed'])}", "",
        "## Quatro testes (nunca um score único)",
        f"- **T1 concept retrieval**: recall {t1['recall']}, precision {t1['precision']}, "
        f"false-merge {t1['false_merge']}/{t1['total']}",
        f"- **T2 verdict invariance**: agreement {t2['agreement']} sobre {t2['considered']} "
        "variantes corretamente mapeadas",
        f"- **T3 dedup invariance**: TP {t3['tp']}/{t3['same_pairs']} "
        f"(rate {t3['tp_rate']}), FP {t3['fp']}/{t3['diff_pairs']} (rate {t3['fp_rate']})",
        f"- **T4 novelty discrimination**: false-merge {t4['false_merge']}/{t4['considered']} "
        f"(rate {t4['false_merge_rate']}) sobre pares near-miss", "",
    ]
    if t2["dispersion_flags"]:
        lines.append("### ⚠️ Dispersão Exists∧Missing (condição (a) — precisa de motivo evidencial)")
        for d in t2["dispersion_flags"]:
            lines.append(f"- `{d['concept_id']}`: {d['verdicts']}")
        lines.append("")
    if t2["correctness_flags"]:
        lines.append("### ⚠️ Modal contradiz expected_repo_state (condição (a) — spine invariante-porém-errado)")
        for c in t2["correctness_flags"]:
            lines.append(f"- `{c['concept_id']}`: modal **{c['modal']}** vs "
                         f"expected_exists={c['expected_exists']}")
        lines.append("")
    if gc["unverified"]:
        lines.append("### ⚠️ Vereditos de existência SEM evidência verificada (Gate C)")
        for u in gc["unverified"]:
            lines.append(f"- `{u['concept_id']}` → {u['verdict']}")
        lines.append("")
    if t4["offenders"]:
        lines.append("### Near-miss merges (T4)")
        for o in t4["offenders"]:
            lines.append(f"- `{o['true']}` → `{o['predicted']}`")
        lines.append("")
    lines += [
        "## Decisão de gate do Tier B",
        "Tier B (#263–#266) só avança se A **e** B **e** C **e** sanity passarem — "
        "alta recuperação de conceito + alta invariância de veredito + baixo false-merge + "
        "instrumento validado. Consistência sem evidência (Gate C) certificaria o spine "
        "\"consistentemente errado\".",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    import argparse
    default = str(Path(__file__).resolve().parent / "metamorphic_canon.yaml")
    ap = argparse.ArgumentParser(description="Metamorphic eval-harness PoC (#288)")
    ap.add_argument("canon", nargs="?", default=default,
                    help="path to the Concept Canon YAML (default: shipped canon)")
    return run(ap.parse_args(argv).canon)


if __name__ == "__main__":
    raise SystemExit(main())
