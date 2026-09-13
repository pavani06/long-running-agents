"""Spine runner — composes Fases 0→3 + gates + quarantine routing + landing.

Minimal glue, not a framework: it chains the Etapa 1-2 phase functions for one
source, runs the deterministic gates (validate-obsidian, grep-verify, cosine
dedup) and the adversarial evaluator, routes accept/quarantine, and builds the
landing summary. This is the entry point #262 invokes for its A/B run. Live keys
are required, so `run_spine` itself is exercised end-to-end there; the pure
pieces (`artifact_for_eval`, `dedup_text`) are unit-tested, and the gates/route/
landing they feed are tested in their own modules.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import dedup
import evaluator
import grep_verify
import landing
import phase0_mental_model
import phase1_extract
import phase2_patterns
import phase3_classify
import quarantine
import retrieval
from embed import embed_texts


def artifact_for_eval(extraction: dict, patterns: list[dict],
                      classifications: list[dict]) -> dict:
    """The compact artifact the adversarial evaluator scores. Pure."""
    return {
        "thesis": extraction.get("thesis", ""),
        "patterns": [{"name": p.get("name"), "problem": p.get("problem")} for p in patterns],
        "classifications": [{"pattern": c.get("pattern"), "verdict": c.get("verdict"),
                             "verified": c.get("verified")} for c in classifications],
    }


def dedup_text(extraction: dict, patterns: list[dict]) -> str:
    """The text embedded to check the source against the repo for duplication. Pure."""
    parts = [extraction.get("thesis", "")]
    parts += [f"{p.get('name','')}: {p.get('problem','')}" for p in patterns]
    return "\n".join(p for p in parts if p).strip()


def validate_obsidian_ok(repo_root: Path) -> bool:
    """Run the repo's own doc validator; True on exit 0 (I/O).

    NOTE (Tier-A limitation): `run_spine` does not materialise the proposed
    artifact to disk (writing is out of scope — #262/#266), so this gate
    currently validates the *committed* repo, not the generated package. It only
    gains teeth once the write step feeds the artifact through validate-obsidian
    before landing; until then it guards against a repo that is already dirty.
    """
    return subprocess.run(
        ["npx", "tsx", "scripts/validate-obsidian.ts"],
        cwd=str(repo_root), capture_output=True, text=True,
    ).returncode == 0


def run_spine(transcript: str, slug: str, index: dict, *, openai_key: str, zai_key: str,
              plan: landing.LandingPlan, repo_root: Path, with_mental: bool = False,
              min_mean: float = evaluator.PROVISIONAL_MIN_MEAN,
              dup_threshold: float = dedup.PROVISIONAL_DUP_THRESHOLD,
              run_validate: bool = True) -> dict:
    """Fases 1->0->2->3 + gates + route. Returns the landing summary + artifacts."""
    extraction = phase1_extract.run(transcript, zai_key)                       # Fase 1
    mental_model = None
    if with_mental:                                                           # Fase 0
        mental_model = phase0_mental_model.run(None, [], zai_key)
    patterns = phase2_patterns.run(extraction, zai_key)                        # Fase 2
    retriever = retrieval.make_pattern_retriever(patterns, index, openai_key, repo_root)
    classifications = phase3_classify.run(patterns, zai_key, retriever=retriever)  # Fase 3

    # Deterministic gates.
    verified = grep_verify.verify_all(phase3_classify.citations_of(classifications), repo_root)
    phase3_classify.mark_verified(classifications, verified)
    citations_ok = grep_verify.all_ok(verified)
    dup = dedup.is_duplicate(embed_texts([dedup_text(extraction, patterns)], openai_key)[0],
                             index, dup_threshold)
    validate_ok = validate_obsidian_ok(repo_root) if run_validate else True

    # Adversarial evaluator.
    evaluation = evaluator.run(artifact_for_eval(extraction, patterns, classifications),
                               openai_key, min_mean=min_mean)

    report = quarantine.report_from_gates(
        validate_obsidian=validate_ok, citations_ok=citations_ok,
        duplicate=dup["duplicate"], evaluation_passed=evaluation["passed"])
    decision = quarantine.decide(report)

    summary = {"slug": slug, "accepted": decision["accepted"], "reasons": decision["reasons"],
               "classifications": classifications, "evaluation": evaluation,
               "dedup": dup, "plan": plan}
    return {"summary": summary, "extraction": extraction, "mental_model": mental_model,
            "patterns": patterns, "classifications": classifications,
            "report": report, "decision": decision,
            "destination_subdir": quarantine.destination_subdir(decision["accepted"]),
            "pr_body": landing.pr_body(summary)}
