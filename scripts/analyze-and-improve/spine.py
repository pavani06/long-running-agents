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

import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import aai_metrics
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


def validate_destination_ok(repo_root: Path, destination: str, text: str) -> bool:
    """Run the repo's own doc validator over PROPOSED content laid out at its
    authoritative `destination`, in a throwaway validation root; True on exit 0 (I/O).

    `validate-obsidian.ts` scopes its canonical checks to `docs/canonical/<file>.md`
    and its curriculum checks to `curriculum/`, so content held in the quarantine
    dir never trips them. The root is a temp dir holding a copy of the validator
    plus the proposed file at `destination`, with the run scoped to that path — the
    conventions come from the validator itself, so there is no second copy to drift
    from it. Nothing is written into an authoritative layer. Fail-closed: False
    whenever the validator reports violations OR cannot be run at all."""
    script = repo_root / "scripts" / "validate-obsidian.ts"
    if not script.is_file():
        return False
    root = Path(tempfile.mkdtemp(prefix=".validate-destination-", dir=str(repo_root)))
    try:
        target = (root / destination).resolve()
        if not target.is_relative_to(root.resolve()):
            return False
        (root / "scripts").mkdir()
        shutil.copyfile(script, root / "scripts" / "validate-obsidian.ts")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return subprocess.run(
            ["npx", "tsx", "scripts/validate-obsidian.ts", "--no-cache",
             "--paths", destination],
            cwd=str(root), capture_output=True, text=True, timeout=300,
        ).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False
    finally:
        shutil.rmtree(root, ignore_errors=True)


def run_spine(transcript: str, slug: str, index: dict, *, openai_key: str, zai_key: str,
              plan: landing.LandingPlan, repo_root: Path, with_mental: bool = False,
              min_mean: float = evaluator.PROVISIONAL_MIN_MEAN,
              dup_threshold: float = dedup.DUP_THRESHOLD,
              run_validate: bool = True) -> dict:
    """Fases 1->0->2->3 + gates + route. Returns the landing summary + artifacts."""
    def _step(label, fn):
        t0 = time.time()
        print(f"[spine] {label} …", flush=True)
        out = fn()
        print(f"[spine] {label} done in {time.time() - t0:.1f}s", flush=True)
        return out

    extraction = _step("Fase 1 (extract)", lambda: phase1_extract.run(transcript, zai_key))
    mental_model = None
    if with_mental:                                                           # Fase 0
        mental_model = _step("Fase 0 (mental model)",
                             lambda: phase0_mental_model.run(None, [], zai_key))
    patterns = _step("Fase 2 (patterns)", lambda: phase2_patterns.run(extraction, zai_key))
    retriever = retrieval.make_pattern_retriever(patterns, index, openai_key, repo_root)
    classifications = _step("Fase 3 (classify)",
                            lambda: phase3_classify.run(patterns, zai_key, retriever=retriever))

    # Deterministic gates.
    verified = grep_verify.verify_all(phase3_classify.citations_of(classifications), repo_root)
    phase3_classify.mark_verified(classifications, verified)
    phase3_classify.mark_grounding(classifications, verified)   # derived provenance for the coverage guard
    citations_ok = grep_verify.all_ok(verified)
    dup = _step("gate: dedup embed", lambda: dedup.is_duplicate(
        embed_texts([dedup_text(extraction, patterns)], openai_key)[0], index, dup_threshold))
    validate_ok = validate_obsidian_ok(repo_root) if run_validate else True

    # Adversarial evaluator.
    evaluation = _step("gate: evaluator", lambda: evaluator.run(
        artifact_for_eval(extraction, patterns, classifications), openai_key, min_mean=min_mean))

    report = quarantine.report_from_gates(
        validate_obsidian=validate_ok, citations_ok=citations_ok,
        duplicate=dup["duplicate"], evaluation_passed=evaluation["passed"])
    decision = quarantine.decide(report)

    summary = {"slug": slug, "accepted": decision["accepted"], "reasons": decision["reasons"],
               "classifications": classifications, "evaluation": evaluation,
               "dedup": dup, "plan": plan}
    # AAI_METRICS (#288 Stage A) — verdict-drift + guard baseline. Telemetry only.
    aai_metrics.emit("classify", {"slug": slug, "scope": aai_metrics.scope_label(),
                                  **aai_metrics.classify_fields(classifications)})
    return {"summary": summary, "extraction": extraction, "mental_model": mental_model,
            "patterns": patterns, "classifications": classifications,
            "report": report, "decision": decision,
            "destination_subdir": quarantine.destination_subdir(decision["accepted"]),
            "pr_body": landing.pr_body(summary)}
