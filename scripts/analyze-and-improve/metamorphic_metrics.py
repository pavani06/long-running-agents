"""Metrics + gates for the metamorphic eval-harness (#288) — all pure.

Four SEPARATE tests (never a single blended score — the whole point of #288):

  T1 concept identification — does the matcher map paraphrases to the right
     concept?  recall / precision / false-merge.
  T2 verdict invariance   — do correctly-mapped paraphrases of one concept get
     the SAME verdict?  % agreement + Exists∧Missing dispersion flags.
  T3 dedup invariance     — are reformulations of one concept flagged duplicates
     of each other (TP) without flagging distinct concepts (FP)?
  T4 novelty discrimination — over near-but-distinct pairs, how often is a
     paraphrase of A merged into B?  false-merge rate.

The three PoC gates:
  A (identification): recall ≥ 0.90 AND false-merge < 0.05.
  B (invariance):     agreement ≥ 0.90 AND no unexplained Exists∧Missing dispersion.
  C (evidence):       every existence verdict carries repo evidence that verified
                      (condition (a): invariance only counts paired with correction).
"""
from __future__ import annotations

from collections import Counter

from floor import cosine
from metamorphic_canon import EXISTENCE_VERDICTS

GATE_A_MIN_RECALL = 0.90
GATE_A_MAX_FALSE_MERGE = 0.05
GATE_B_MIN_AGREEMENT = 0.90


# ── T1 — concept identification ──────────────────────────────────────────────
def t1_identification(cases: list[dict]) -> dict:
    """cases: [{true, predicted}] (predicted None == unmatched).

    recall = correct / all; precision = correct / matched; false_merge = matched
    to the WRONG concept (mapped somewhere real, just not the right place)."""
    total = len(cases)
    correct = sum(1 for c in cases if c.get("predicted") == c.get("true"))
    matched = sum(1 for c in cases if c.get("predicted") is not None)
    false_merge = sum(1 for c in cases
                      if c.get("predicted") is not None and c.get("predicted") != c.get("true"))
    return {
        "total": total, "correct": correct, "matched": matched,
        "recall": round(correct / total, 3) if total else 0.0,
        "precision": round(correct / matched, 3) if matched else 0.0,
        "false_merge": false_merge,
        "false_merge_rate": round(false_merge / total, 3) if total else 0.0,
    }


# ── T2 — verdict invariance ──────────────────────────────────────────────────
def t2_invariance(cases: list[dict]) -> dict:
    """cases: [{true, predicted, verdict, exists?}]. Only CORRECTLY-mapped variants
    (predicted == true) count — an invariance measured over misrouted variants is
    meaningless. agreement = variants matching their concept's modal verdict /
    considered. Groups mixing an existence verdict with Missing are flagged
    (Exists∧Missing dispersion).

    Condition (a): invariance alone is not enough — a spine that answers Missing
    for EVERY paraphrase of an existing concept is invariant AND has no dispersion
    yet is uniformly wrong. When a case carries the ground-truth `exists`, the
    concept's modal verdict is checked against it: a modal existence verdict for an
    absent concept, or a modal Missing for a present one, is a `correctness_flag`.
    This is the `expected_repo_state` half of the correction anchor (the evidence
    half is Gate C)."""
    groups: dict[str, list[str]] = {}
    expected: dict[str, bool] = {}
    for c in cases:
        if c.get("predicted") == c.get("true") and c.get("verdict"):
            groups.setdefault(c["true"], []).append(c["verdict"])
        if isinstance(c.get("exists"), bool):
            expected[c["true"]] = c["exists"]
    considered = sum(len(v) for v in groups.values())
    agreeing = 0
    per_concept, dispersion, correctness = {}, [], []
    for cid, verdicts in groups.items():
        counts = Counter(verdicts)
        mode_n = max(counts.values())
        agreeing += mode_n
        modal = counts.most_common(1)[0][0]
        per_concept[cid] = {"n": len(verdicts), "agreement": round(mode_n / len(verdicts), 3),
                            "verdicts": dict(counts), "modal": modal}
        has_exist = any(v in EXISTENCE_VERDICTS for v in verdicts)
        if has_exist and "Missing" in counts:
            dispersion.append({"concept_id": cid, "verdicts": dict(counts)})
        if cid in expected and (modal in EXISTENCE_VERDICTS) != expected[cid]:
            correctness.append({"concept_id": cid, "modal": modal,
                                "expected_exists": expected[cid]})
    return {
        "considered": considered,
        "agreement": round(agreeing / considered, 3) if considered else 0.0,
        "per_concept": per_concept, "dispersion_flags": dispersion,
        "correctness_flags": correctness,
    }


# ── T3 — dedup invariance ────────────────────────────────────────────────────
def t3_dedup_invariance(items: list[dict], *, threshold: float) -> dict:
    """items: [{concept_id, vec}]. Same-concept pairs SHOULD be near-duplicates
    (TP); different-concept pairs should NOT (FP). Reuses the cosine + the repo's
    DUP_THRESHOLD so this measures the same dedup gate the spine uses."""
    tp = fp = same_pairs = diff_pairs = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            dup = cosine(items[i]["vec"], items[j]["vec"]) >= threshold
            if items[i]["concept_id"] == items[j]["concept_id"]:
                same_pairs += 1
                tp += dup
            else:
                diff_pairs += 1
                fp += dup
    return {
        "same_pairs": same_pairs, "tp": tp,
        "tp_rate": round(tp / same_pairs, 3) if same_pairs else 0.0,
        "diff_pairs": diff_pairs, "fp": fp,
        "fp_rate": round(fp / diff_pairs, 3) if diff_pairs else 0.0,
    }


# ── T4 — novelty discrimination ──────────────────────────────────────────────
def t4_novelty(cases: list[dict], near_miss_pairs: list[list[str]]) -> dict:
    """A false merge across a near-miss boundary: a variant of A predicted as its
    near-but-distinct neighbour B (or vice-versa). Rate over the variants whose
    true concept appears in any near-miss pair."""
    boundary: set[tuple[str, str]] = set()
    concepts: set[str] = set()
    for a, b in near_miss_pairs:
        boundary.add((a, b))
        boundary.add((b, a))
        concepts.update((a, b))
    considered = [c for c in cases if c.get("true") in concepts]
    offenders = [{"true": c["true"], "predicted": c["predicted"]}
                 for c in considered
                 if (c.get("true"), c.get("predicted")) in boundary]
    n = len(considered)
    return {"considered": n, "false_merge": len(offenders),
            "false_merge_rate": round(len(offenders) / n, 3) if n else 0.0,
            "offenders": offenders}


# ── Gates ────────────────────────────────────────────────────────────────────
def gate_a(t1: dict) -> dict:
    passed = (t1["recall"] >= GATE_A_MIN_RECALL
              and t1["false_merge_rate"] < GATE_A_MAX_FALSE_MERGE)
    return {"passed": bool(passed), "recall": t1["recall"],
            "false_merge_rate": t1["false_merge_rate"],
            "min_recall": GATE_A_MIN_RECALL, "max_false_merge": GATE_A_MAX_FALSE_MERGE}


def gate_b(t2: dict) -> dict:
    """Invariance passes only when it is HIGH, has no Exists∧Missing dispersion,
    AND each concept's modal verdict matches its `expected_repo_state` — an
    invariant-but-uniformly-wrong spine (e.g. all-Missing on a present concept)
    must not pass (condition (a))."""
    correctness = t2.get("correctness_flags", [])
    passed = (t2["agreement"] >= GATE_B_MIN_AGREEMENT
              and not t2["dispersion_flags"] and not correctness)
    return {"passed": bool(passed), "agreement": t2["agreement"],
            "min_agreement": GATE_B_MIN_AGREEMENT,
            "dispersion_flags": t2["dispersion_flags"],
            "correctness_flags": correctness}


def gate_c(existence_cases: list[dict]) -> dict:
    """existence_cases: [{concept_id, verdict, verified}] for every variant whose
    verdict claims coverage. Passes iff every one has verified repo evidence."""
    unverified = [{"concept_id": c.get("concept_id"), "verdict": c.get("verdict")}
                  for c in existence_cases if not c.get("verified")]
    return {"passed": not unverified, "total_existence": len(existence_cases),
            "verified": len(existence_cases) - len(unverified), "unverified": unverified}


def poc_decision(ga: dict, gb: dict, gc: dict, sanity: dict) -> dict:
    """The PoC holds only if all three gates pass AND the reranker cleared its own
    sanity mini-eval (an unvalidated judge invalidates the whole measurement)."""
    passed = ga["passed"] and gb["passed"] and gc["passed"] and sanity.get("passed", False)
    return {"passed": bool(passed),
            "gates": {"A_identification": ga["passed"], "B_invariance": gb["passed"],
                      "C_evidence": gc["passed"], "reranker_sanity": bool(sanity.get("passed"))}}
