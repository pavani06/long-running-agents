#!/usr/bin/env python3
"""First Useful Governed Loop — one real end-to-end path (#263 slice).

`real source → F1/F2/F3 → one Missing → F4 creation → quarantine → gates → PR`.

Minimal glue over existing primitives — NOT a general orchestration framework:
one real pending source traverses the existing analysis/classification path, exactly
one eligible Missing is selected (explicit `--pattern-id`, else deterministic first
eligible), F4 creates exactly ONE proposed canonical doc into quarantine, the existing
content gates (adversarial evaluator + cosine dedup + citation grounding) run against it,
and a single human-review PR body is assembled. auto_merge stays OFF; nothing is promoted.
validate-obsidian is a PROMOTION-time convention gate (the #262 path runs the spine with
run_validate=False) and is deliberately not run at creation — creation != promotion.

Selection is deterministic and self-reported. This script writes the proposal + a PR-body
file and prints the facts; opening the PR is the workflow's job (this script never calls gh).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dedup
import evaluator
import grep_verify
import landing
import phase1_extract
import phase2_patterns
import phase3_classify
import phase4_create
import retrieval
from analysis_queue import scan_pending
from embed import embed_texts
from pipeline import EXTRACTS_DIR, REPO_ROOT, load_state

TRANSCRIPTS_DIR = REPO_ROOT / "raw" / "youtube" / "ai-learning" / "transcripts"
# The 12-factor-agents source is the #262 / ab-validate BENCHMARK — excluded so the loop
# runs a genuine non-benchmark source (requirement 1).
BENCHMARK_MARKERS = ("12-factor-agents",)


def _out(line: str) -> None:
    print(line, flush=True)
    p = os.environ.get("GITHUB_STEP_SUMMARY")
    if p:
        try:
            with open(p, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
        except OSError:
            pass


def _emit_output(key: str, value: str) -> None:
    """Expose a value to the workflow via $GITHUB_OUTPUT (and stdout)."""
    print(f"FIRST_LOOP {key}={value}", flush=True)
    p = os.environ.get("GITHUB_OUTPUT")
    if p:
        try:
            with open(p, "a", encoding="utf-8") as fh:
                fh.write(f"{key}={value}\n")
        except OSError:
            pass


def select_source(pending: list, source_arg: str | None):
    """Deterministic source pick. Returns (extract_filename, rule). Pure."""
    if source_arg:
        return source_arg, "explicit --source"
    real = [p for p in pending if not any(m in p.file for m in BENCHMARK_MARKERS)]
    if not real:
        return None, "no eligible non-benchmark pending source"
    # `pending` is already sorted by filename (analysis_queue), so [0] is deterministic.
    return real[0].file, "first pending source in filename order, excluding the 12-factor benchmark"


def select_missing(classifications: list[dict], pattern_id: str | None):
    """Deterministic Missing pick. Returns (classification, rule). Pure."""
    missing = [c for c in classifications if c.get("verdict") == "Missing"]
    if pattern_id:
        for c in missing:
            if c.get("pattern") == pattern_id:
                return c, f"explicit --pattern-id={pattern_id}"
        return None, f"pattern-id {pattern_id!r} is not an eligible Missing"
    if not missing:
        return None, "no eligible Missing verdict"
    # classifications preserve Fase-2 pattern order → [0] is the first eligible.
    return missing[0], "first eligible Missing in Fase-2 pattern order"


def _transcript_for(extract_file: str) -> Path:
    """Map a pending extract `<stem>.md` to its raw transcript `<stem>.txt`."""
    return TRANSCRIPTS_DIR / (Path(extract_file).stem + ".txt")


def _pr_body(*, slug, source_file, source_rule, missing, missing_rule, pattern,
             artifact, proposed_path, gates, evaluation, dup) -> str:
    ev = evaluation
    plan = landing.LandingPlan(auto_merge=False, dry_run=False)
    lines = [
        f"## First Useful Governed Loop — proposta para revisão humana (`{slug}`)", "",
        f"**Landing:** {plan.describe()}  ·  **creation != promotion** (nada promovido automaticamente)", "",
        "### Fonte (real, não-benchmark)",
        f"- `{source_file}` — _selecionada por:_ {source_rule}", "",
        "### Missing selecionado",
        f"- **{missing.get('pattern')}** — _selecionado por:_ {missing_rule}",
        f"- Racional Fase-3: {missing.get('rationale','')}", "",
        "### Proposta criada (quarentena)",
        f"- `{proposed_path}`",
        f"- Destino pretendido (se promovida): `{artifact['intended_destination']}`", "",
        "### Evidência que fundamenta",
        f"- Fase-3 verdict: **{missing.get('verdict')}** (Missing = ausente no repo → sem citação de repo; "
        "fundamentado no padrão da fonte)",
        f"- Padrão: problema — {pattern.get('problem','')[:300]}",
        f"- Citações Fase-3 verificadas: {gates['citations_ok']} "
        f"({len(missing.get('evidence',[]))} citação(ões))", "",
        "### Gates (rodados contra a proposta)",
        f"- Adversarial evaluator: mean **{ev.get('mean','n/a')}** — "
        f"{'passou' if ev.get('passed') else 'reprovou'} (corte {evaluator.PROVISIONAL_MIN_MEAN})",
        f"  - scores: {ev.get('scores')}",
        f"  - rationale: {ev.get('rationale','')[:400]}",
        f"- Dedup cosseno: {'DUPLICADO' if dup.get('duplicate') else 'não-duplicado'} "
        f"(score {dup.get('score','n/a')})",
        f"- Citação/grounding: {'ok' if gates['citations_ok'] else 'falhou'}",
        "- validate-obsidian: _diferido para a promoção_ (gate de convenção; o caminho #262 roda com "
        "`run_validate=False`; creation != promotion)", "",
        "### O que o humano está sendo pedido a aprovar",
        "Promover (ou não) esta proposta de doc canônico da quarentena para o destino pretendido. "
        "A aprovação do PR não promove automaticamente — a promoção (mover para `docs/canonical/`, "
        "adicionar frontmatter de convenção, validate-obsidian, integração de índice) é um passo humano "
        "separado, fora deste loop. Rejeitar = fechar o PR; a proposta permanece só na quarentena.", "",
        "_auto_merge=OFF — merge/promção exigem ação humana._",
    ]
    return "\n".join(lines)


def run(source_arg: str | None, pattern_id: str | None) -> int:
    zai = os.environ.get("ZAI_API_KEY")
    openai = os.environ.get("OPENAI_API_KEY")
    if not zai or not openai:
        _out("first-loop: ZAI_API_KEY and OPENAI_API_KEY both required")
        return 1
    index = load_state()
    if not index.get("records"):
        _out("first-loop: empty index — run `pipeline.py index --full` first")
        return 1

    pending = scan_pending(EXTRACTS_DIR)
    source_file, source_rule = select_source(pending, source_arg)
    if not source_file:
        _out(f"first-loop: {source_rule}")
        return 1
    transcript_path = _transcript_for(source_file)
    if not transcript_path.exists():
        _out(f"first-loop: transcript not found for {source_file}: {transcript_path}")
        return 1
    slug = Path(source_file).stem.rsplit("--", 1)[0]
    _out(f"first-loop: source `{source_file}` ({source_rule})")

    transcript = transcript_path.read_text(encoding="utf-8")
    extraction = phase1_extract.run(transcript, zai)                       # F1
    patterns = phase2_patterns.run(extraction, zai)                        # F2
    retriever = retrieval.make_pattern_retriever(patterns, index, openai, REPO_ROOT)
    classifications = phase3_classify.run(patterns, zai, retriever=retriever)  # F3
    verified = grep_verify.verify_all(phase3_classify.citations_of(classifications), REPO_ROOT)
    phase3_classify.mark_verified(classifications, verified)
    phase3_classify.mark_grounding(classifications, verified)

    missing, missing_rule = select_missing(classifications, pattern_id)
    if not missing:
        _out(f"first-loop: {missing_rule} — no F4 creation (loop needs one eligible Missing)")
        return 1
    _out(f"first-loop: Missing selected — {missing.get('pattern')} ({missing_rule})")

    by_name = {p.get("name"): p for p in patterns}
    pattern = by_name.get(missing.get("pattern"), {"name": missing.get("pattern")})

    # F4 — create exactly ONE proposed canonical doc into quarantine.
    source_context = (f"Tese: {extraction.get('thesis','')}\n"
                      f"Trade-offs: {pattern.get('tradeoffs','')}")
    artifact = phase4_create.create(
        pattern, slug=slug, source_file=source_file,
        video_id=str(extraction.get("video_id", "")), evidence=missing.get("evidence", []),
        source_context=source_context, zai_key=zai)
    proposed_path = phase4_create.write_proposed(REPO_ROOT, artifact, slug, pattern)
    _out(f"first-loop: proposed artifact written to `{proposed_path}`")

    # Gates against the proposal (existing primitives; validate-obsidian deferred to promotion).
    eval_artifact = {"type": artifact["type"], "title": artifact["title"],
                     "content": artifact["content"], "source_pattern": pattern,
                     "phase3_verdict": "Missing"}
    evaluation = evaluator.run(eval_artifact, openai)
    proposal_vec = embed_texts([artifact["title"] + "\n" + artifact["content"]], openai)[0]
    dup = dedup.is_duplicate(proposal_vec, index)
    missing_verified = [v for v in verified if v.get("pattern") == missing.get("pattern")]
    citations_ok = grep_verify.all_ok(missing_verified)
    gates = {"citations_ok": citations_ok}

    pr_title = f"[proposta] analyze-and-improve: {missing.get('pattern')} ({slug})"
    pr_body = _pr_body(slug=slug, source_file=source_file, source_rule=source_rule,
                       missing=missing, missing_rule=missing_rule, pattern=pattern,
                       artifact=artifact, proposed_path=proposed_path, gates=gates,
                       evaluation=evaluation, dup=dup)
    body_path = Path(os.environ.get("PR_BODY_PATH", "pr-body.md"))
    body_path.write_text(pr_body, encoding="utf-8")
    _out("\n" + pr_body)

    branch = f"proposal/{slug}--{phase4_create.slugify(missing.get('pattern',''))}"
    _emit_output("proposed_path", proposed_path)
    _emit_output("pr_title", pr_title)
    _emit_output("pr_body_path", str(body_path))
    _emit_output("branch", branch)
    _emit_output("slug", slug)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="First Useful Governed Loop (#263 slice)")
    ap.add_argument("--source", default=os.environ.get("SOURCE") or None,
                    help="extract filename (default: deterministic first non-benchmark pending)")
    ap.add_argument("--pattern-id", default=os.environ.get("PATTERN_ID") or None,
                    help="explicit Missing pattern to create (default: first eligible Missing)")
    args = ap.parse_args(argv)
    return run(args.source, args.pattern_id)


if __name__ == "__main__":
    raise SystemExit(main())
