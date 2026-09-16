#!/usr/bin/env python3
"""First Useful Governed Loop — one real end-to-end path (#263 slice; #264 wiring).

`source → analyze → Missing → F4 → canonical/skill/exercise on the proposal branch →
gates/CI → PR → REJECT/EDIT/ACCEPT → human merge = promotion`.

Minimal glue over existing primitives — NOT a general orchestration framework:
one real pending source traverses the existing analysis/classification path, exactly
one eligible Missing is selected (explicit `--pattern-id`, else deterministic first
eligible), and F4 is the #263 creation engine (`phase4_flow.run_fase4`) — the single
production F4 path since #264 swapped out the hand-rolled single-doc block. The
engine writes each artifact into quarantine, runs the existing content gates
(adversarial evaluator + cosine dedup + destination-scoped validation) against it,
promotes-on-pass (in-worktree), and records the run in the artifacts manifest
(`docs/analysis/<slug>/<slug>-artifacts.{yaml,md}`) — the producer→consumer contract
the Fase-5 integrator (`pipeline.py integrate`) reads to recompute index projections.
creation != promotion, boundary redefined: **the PR is the quarantine** — creation is the
branch write; promotion is the human merge to main. auto_merge stays OFF; nothing reaches main
without a human merge. validate-obsidian runs in CI ("Check Obsidian Conventions") over
`docs/canonical/` on the PR, so the doc carries complete canonical frontmatter/conventions.

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

import evaluator
import grep_verify
import landing
import phase1_extract
import phase2_patterns
import phase3_classify
import phase4_create
import phase4_flow
import retrieval
from analysis_queue import scan_pending
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
             result, citations_ok) -> str:
    plan = landing.LandingPlan(auto_merge=False, dry_run=False)
    lines = [
        f"## First Useful Governed Loop — proposta para revisão humana (`{slug}`)", "",
        f"**Landing:** {plan.describe()}  ·  **creation != promotion** (nada promovido automaticamente)", "",
        "### Fonte (real, não-benchmark)",
        f"- `{source_file}` — _selecionada por:_ {source_rule}", "",
        "### Missing selecionado",
        f"- **{missing.get('pattern')}** — _selecionado por:_ {missing_rule}",
        f"- Racional Fase-3: {missing.get('rationale','')}", "",
        "### Artefatos Fase 4 (engine #263 `run_fase4`; este PR é a quarentena)",
    ]
    for o in result["outcomes"]:
        art = o["artifact"]
        ev, dup = o.get("evaluation") or {}, o.get("dedup") or {}
        status = ("promovido neste branch (aguarda merge humano)" if o["accepted"]
                  else "**RETIDO em quarentena** — não muta índices")
        lines.append(f"- **[{o['category']}]** `{art['intended_destination']}` — {status}")
        if ev:
            lines.append(f"  - evaluator adversarial: mean **{ev.get('mean','n/a')}** — "
                         f"{'passou' if ev.get('passed') else 'reprovou'} "
                         f"(corte {evaluator.PROVISIONAL_MIN_MEAN})")
            lines.append(f"    - scores: {ev.get('scores')}")
            lines.append(f"    - rationale: {str(ev.get('rationale',''))[:400]}")
        if dup:
            lines.append(f"  - dedup cosseno: {'DUPLICADO' if dup.get('duplicate') else 'não-duplicado'} "
                         f"(score {dup.get('score','n/a')})")
        for reason in o.get("reasons", []):
            lines.append(f"  - hold/motivo: {str(reason)[:300]}")
    lines += [
        "",
        "### Manifesto de artefatos (contrato produtor→consumidor)",
        f"- `docs/analysis/{slug}/{slug}-artifacts.yaml` (+ `.md`) — diz exatamente quais "
        "artefatos desta execução foram promovidos vs retidos, com motivos.", "",
        "### Integração determinística dos índices (Fase 5, #264)",
        f"- `pipeline.py integrate docs/analysis/{slug}/{slug}-artifacts.yaml` leu ESTE "
        "manifesto (o caminho explícito desta execução, grafado uma única vez: o produtor o "
        "emite, o workflow o repassa, o consumidor não o re-deriva) e recomputou do disco as "
        "projeções derivadas: contagem canônica por recount (nunca incremento), "
        "`last_updated` do SOR, linha da tabela de padrões ativos e listagens de exercícios. "
        "Entradas `quarantined` nunca mutam índices.", "",
        "### Evidência que fundamenta",
        f"- Fase-3 verdict: **{missing.get('verdict')}** (Missing = ausente no repo → sem citação de repo; "
        "fundamentado no padrão da fonte)",
        f"- Padrão: problema — {pattern.get('problem','')[:300]}",
        f"- Citações Fase-3 verificadas: {citations_ok} "
        f"({len(missing.get('evidence',[]))} citação(ões))",
        "- validate-obsidian: **roda no CI** ('Check Obsidian Conventions') sobre `docs/canonical/` "
        "neste PR; os artefatos já carregam o frontmatter/convenção exigida.", "",
        "### O que o humano está sendo pedido a aprovar",
        "REJECT / EDIT / ACCEPT destes artefatos. **O merge deste PR é a promoção** — ele move "
        "os artefatos para seus destinos no `main`. Enquanto o PR estiver aberto, nada foi "
        "promovido (o PR é a quarentena). Rejeitar = fechar o PR; nada entra no `main`.", "",
        "_auto_merge=OFF — o merge (promoção) é um ato humano._",
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
        if pattern_id:
            # An explicit --pattern-id that isn't an eligible Missing is an unsatisfiable
            # request, not a clean "nothing to propose" — surface it as an error.
            _out(f"first-loop: {missing_rule}")
            return 1
        # No eligible Missing on a deterministic run = the analysis found nothing worth
        # proposing. That is a SUCCESSFUL no-op, not a failure: exit 0, emit no PR metadata,
        # and the workflow's branch/commit/PR steps stay skipped (has_proposal=false).
        _out(f"first-loop: SUCCESS — analyzed; no proposal needed ({missing_rule})")
        _emit_output("has_proposal", "false")
        return 0
    _out(f"first-loop: Missing selected — {missing.get('pattern')} ({missing_rule})")

    by_name = {p.get("name"): p for p in patterns}
    pattern = by_name.get(missing.get("pattern"), {"name": missing.get("pattern")})

    # F4 — the #263 creation engine, the SINGLE production F4 path since #264 (the
    # hand-rolled single-doc block it replaces is deleted, not kept beside). Passing
    # only the selected Missing preserves the select_missing determinism: plan_of_work
    # on one P0 yields canonical+skill+exercise for exactly that pattern. The engine
    # does repo-grounding per pattern, writes each artifact into quarantine
    # (docs/analysis/<slug>/proposed/), runs the Etapa-3 gates fail-closed,
    # promotes-on-pass (in-worktree move) and writes the artifacts manifest — the
    # contract the Fase-5 consumer reads. The full F3 set goes in as the REPORTING
    # input so the manifest's skipped rows cover every pattern this run classified,
    # not just the one it planned.
    result = phase4_flow.run_fase4(
        REPO_ROOT, slug, [missing], patterns, extraction, index,
        openai_key=openai, zai_key=zai, source_file=source_file,
        reporting_classifications=classifications)
    _out(f"first-loop: run_fase4 — {len(result['promoted'])} promoted, "
         f"{len(result['held'])} held; manifest at docs/analysis/{slug}/{slug}-artifacts.yaml")

    missing_verified = [v for v in verified if v.get("pattern") == missing.get("pattern")]
    citations_ok = grep_verify.all_ok(missing_verified)

    pr_title = f"[proposta] analyze-and-improve: {missing.get('pattern')} ({slug})"
    pr_body = _pr_body(slug=slug, source_file=source_file, source_rule=source_rule,
                       missing=missing, missing_rule=missing_rule, pattern=pattern,
                       result=result, citations_ok=citations_ok)
    body_path = Path(os.environ.get("PR_BODY_PATH", "pr-body.md"))
    body_path.write_text(pr_body, encoding="utf-8")
    _out("\n" + pr_body)

    branch = f"proposal/{slug}--{phase4_create.slugify(missing.get('pattern',''))}"
    _emit_output("has_proposal", "true")
    _emit_output("manifest_path", f"docs/analysis/{slug}/{slug}-artifacts.yaml")
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
