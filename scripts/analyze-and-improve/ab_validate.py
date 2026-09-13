"""A/B validation of the Tier-A spine against a historical package (Etapa 4, #262).

Runs `spine.run_spine` (Fases 0->3) live for one source and compares its
classification labels to the curated historical package, checks that a seeded
known-duplicate is caught by the cosine dedup, and emits the empirical index
distribution + evaluator score so the provisional floor/cut can be calibrated.

The comparison + report logic is pure and unit-tested; `run` (network: GLM +
OpenAI) executes only in the Actions job that holds the secrets. This is the
Tier-B progression gate: proceed only if the criteria pass.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Historical labels and our canonical verdicts both map onto one scale.
_CANON = {
    "already exists": "Exists", "exists": "Exists",
    "partial coverage": "Partial", "partial": "Partial",
    "missing": "Missing",
    "better implementation": "Better", "better": "Better",
}
MIN_AGREEMENT = 0.80  # epic criterion 1
# Criterion 1 also needs a meaningful sample: agreement over 1-2 coincidental
# name matches (fresh names are GLM-generated, historical are curated) would pass
# ≥80% trivially. Require at least this many shared patterns before it can pass.
MIN_SHARED = 5


def canonical_verdict(label: str) -> str | None:
    """Map a historical or fresh label onto {Missing,Partial,Exists,Better}."""
    if not label:
        return None
    return _CANON.get(re.sub(r"\s+", " ", str(label)).strip().lower())


def normalize_name(name: str) -> str:
    """Loose key for matching pattern names across the two packages."""
    return re.sub(r"[^a-z0-9]+", " ", (name or "").lower()).strip()


def historical_from_yaml(data: dict) -> list[dict]:
    """[{name, verdict}] from a historical classification.yaml dict."""
    out = []
    for p in (data or {}).get("patterns", []):
        v = canonical_verdict(p.get("classification", ""))
        if p.get("name") and v:
            out.append({"name": p["name"], "verdict": v})
    return out


def fresh_from_classifications(classifications: list[dict]) -> list[dict]:
    """[{name, verdict}] from a fresh Fase-3 classifications list."""
    out = []
    for c in classifications or []:
        v = canonical_verdict(c.get("verdict", ""))
        if c.get("pattern") and v:
            out.append({"name": c["pattern"], "verdict": v})
    return out


def label_agreement(fresh: list[dict], historical: list[dict]) -> dict:
    """Agreement over patterns present in BOTH packages (matched by name).

    {shared, matched, agreement, mismatches[]}. agreement is 0 when nothing is
    shared (no false confidence from an empty intersection)."""
    fresh_by = {normalize_name(x["name"]): x["verdict"] for x in fresh}
    hist_by = {normalize_name(x["name"]): x["verdict"] for x in historical}
    shared = sorted(set(fresh_by) & set(hist_by))
    matched = [k for k in shared if fresh_by[k] == hist_by[k]]
    mismatches = [{"name": k, "fresh": fresh_by[k], "historical": hist_by[k]}
                  for k in shared if fresh_by[k] != hist_by[k]]
    agreement = (len(matched) / len(shared)) if shared else 0.0
    return {"shared": len(shared), "matched": len(matched),
            "agreement": round(agreement, 3), "mismatches": mismatches}


def decide_ab(agreement: dict, dup_caught: bool, *, min_agreement: float = MIN_AGREEMENT,
              min_shared: int = MIN_SHARED) -> dict:
    """Both epic criteria must pass to green-light Tier B. Criterion 1 also needs
    a meaningful shared sample (>= min_shared) so a lucky 1-2 name matches can't
    green-light on their own."""
    c1 = agreement.get("shared", 0) >= min_shared and agreement["agreement"] >= min_agreement
    return {"passed": bool(c1 and dup_caught), "min_agreement": min_agreement,
            "min_shared": min_shared,
            "criteria": {"label_agreement": c1, "seeded_duplicate_caught": bool(dup_caught)}}


def ab_report(agreement: dict, dup: dict, distribution: dict, evaluator_mean, decision: dict,
              *, suggested_floor, suggested_cut) -> str:
    """Short A/B report (markdown). Pure."""
    verdict = "✅ PROSSEGUIR PRO TIER B" if decision["passed"] else "⛔ ITERAR (não prosseguir)"
    lines = [
        "# A/B validation — Tier A vs histórico (12-factor-agents)", "",
        f"## Veredito: {verdict}", "",
        "## Critérios",
        f"1. Concordância de rótulos ≥ {int(decision['min_agreement']*100)}% "
        f"(sobre ≥ {decision.get('min_shared', MIN_SHARED)} padrões compartilhados): "
        f"**{agreement['agreement']*100:.0f}%** ({agreement['matched']}/{agreement['shared']} "
        f"compartilhados) — {'PASS' if decision['criteria']['label_agreement'] else 'FAIL'}"
        + ("  ⚠️ amostra compartilhada abaixo do mínimo"
           if agreement["shared"] < decision.get("min_shared", MIN_SHARED) else ""),
        f"2. Duplicado-semente pego pelo dedup: score {dup.get('score')} — "
        f"{'PASS' if decision['criteria']['seeded_duplicate_caught'] else 'FAIL'}", "",
        "## Divergências de rótulo (padrões compartilhados)",
    ]
    if agreement["mismatches"]:
        for m in agreement["mismatches"]:
            lines.append(f"- `{m['name']}`: fresh=**{m['fresh']}** vs histórico=**{m['historical']}**")
    else:
        lines.append("_(nenhuma — todos os rótulos compartilhados bateram)_")
    lines += [
        "", "## Calibração (finaliza os provisórios)",
        f"- Distribuição de cosseno do índice: `{json.dumps(distribution)}`",
        f"- **Floor sugerido** (repo): `{suggested_floor}`",
        f"- Evaluator mean observado: `{evaluator_mean}` → **corte mínimo sugerido**: `{suggested_cut}`",
    ]
    return "\n".join(lines)


def suggest_floor(distribution: dict) -> float:
    """A defensible repo floor from the empirical distribution: the p90 of
    pairwise cosine (the related tail sits above ambient similarity)."""
    return float(distribution.get("p90", 0.0)) if distribution else 0.0


def _summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def run(transcript_path: str, historical_yaml: str, seed_section_path: str) -> int:
    """Live A/B run (Actions only): needs OPENAI_API_KEY + ZAI_API_KEY. Exit 0 on
    a PASS decision, 1 on FAIL or setup error — so the job's status reflects the gate."""
    import yaml

    import dedup
    import evaluator
    import floor as floor_mod
    import landing
    import spine
    from embed import embed_texts
    from index_store import index_vectors

    openai_key = os.environ.get("OPENAI_API_KEY")
    zai_key = os.environ.get("ZAI_API_KEY")
    if not openai_key or not zai_key:
        _summary("ab-validate: OPENAI_API_KEY and ZAI_API_KEY both required")
        return 1

    repo_root = Path(__file__).resolve().parents[2]
    state_path = repo_root / ".runtime" / "analyze-and-improve" / "index.json"
    if not state_path.exists():
        _summary("ab-validate: index not built — run `pipeline.py index --full` first")
        return 1
    index = json.loads(state_path.read_text(encoding="utf-8"))

    transcript = (repo_root / transcript_path).read_text(encoding="utf-8")
    result = spine.run_spine(
        transcript, "ab-12-factor", index,
        openai_key=openai_key, zai_key=zai_key,
        plan=landing.LandingPlan(auto_merge=False, dry_run=True),
        repo_root=repo_root, run_validate=False)

    fresh = fresh_from_classifications(result["classifications"])
    historical = historical_from_yaml(yaml.safe_load((repo_root / historical_yaml).read_text(encoding="utf-8")))
    agreement = label_agreement(fresh, historical)

    # Seeded duplicate: embed the text of a section we KNOW is in the repo/index;
    # the dedup gate must flag it (cosine ~1.0 against itself).
    seed_text = (repo_root / seed_section_path).read_text(encoding="utf-8")[:2000]
    seed_vec = embed_texts([seed_text], openai_key)[0]
    dup = dedup.is_duplicate(seed_vec, index)

    distribution = floor_mod.distribution(index_vectors(index))
    ev_mean = (result["summary"]["evaluation"] or {}).get("mean")
    decision = decide_ab(agreement, dup["duplicate"])
    report = ab_report(agreement, dup, distribution, ev_mean, decision,
                       suggested_floor=suggest_floor(distribution),
                       suggested_cut=ev_mean)
    _summary(report)
    return 0 if decision["passed"] else 1


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="A/B validation of the Tier-A spine (#262)")
    ap.add_argument("transcript", help="repo-relative path to the source transcript")
    ap.add_argument("historical_yaml", help="repo-relative path to the historical classification.yaml")
    ap.add_argument("seed_section", help="repo-relative path to a known indexed file (seeded duplicate)")
    args = ap.parse_args(argv)
    return run(args.transcript, args.historical_yaml, args.seed_section)


if __name__ == "__main__":
    raise SystemExit(main())
