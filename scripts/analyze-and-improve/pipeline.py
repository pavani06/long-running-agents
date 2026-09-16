#!/usr/bin/env python3
"""Control plane + judgment plane (Fases 0-2) for analyze-and-improve v4.

  queue    List the `deep_dive: high` sources still needing an analysis package
           (stateless diff over the `analyzed:` marker). No network, no writes.

  index    Build/refresh the repo's per-section semantic index. `--full` embeds
           every target section; otherwise a git delta scan from the stored
           commit re-embeds only the chunks that changed. `--distribution`
           embeds and prints the pairwise-cosine distribution (to calibrate the
           floor, #262) without writing the index.

  analyze  Run Fases 1->0->2 (GLM) for one transcript and write the partial
           package to docs/analysis/<slug>/ (mental-model, analysis, patterns).
           Fase 0 updates the mental model incrementally from the git delta scan.

  integrate  Run Fase 5 (#264) for one run's manifest: recompute the four index
           surfaces (system-of-record, curriculum INDEX/README/MASTER_PLAN) from
           the explicit manifest path given as its argument
           (docs/analysis/<slug>/<slug>-artifacts.yaml). Deterministic, no
           network; only status=promoted entries mutate indexes.

Environment:
  OPENAI_API_KEY   embeddings for `index`                          — required there
  ZAI_API_KEY      GLM generator for `analyze` (Fases 0-2)          — required there

Exit: 0 = success (incl. nothing-to-do); 1 = red (missing/invalid key, git failure).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

import aai_metrics  # noqa: E402
import deltascan  # noqa: E402
from analysis_queue import scan_pending  # noqa: E402
from embed import AuthError, EmbedError, embed_texts  # noqa: E402
from floor import REPO_FLOOR, distribution  # noqa: E402
from index_store import (index_vectors, merge_index, records_for,  # noqa: E402
                         select_to_embed)

# The judgment-plane modules (Fases 0-2) and their yaml dependency are imported
# lazily inside run_analyze, so `queue`/`index` stay requests-only.

REPO_ROOT = Path(__file__).resolve().parents[2]
EXTRACTS_DIR = REPO_ROOT / "extracts" / "youtube" / "ai-learning"
STATE_PATH = REPO_ROOT / ".runtime" / "analyze-and-improve" / "index.json"
MENTAL_DIR = REPO_ROOT / "mapa-mental-repo"
TZ = ZoneInfo("America/Sao_Paulo")
MAX_DELTA_SECTIONS = 40  # cap Fase 0 context so a full scan can't blow cost


def summary(line: str) -> None:
    print(line)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def load_state() -> dict:
    """Load the index state. A restored cache is an OPTIMIZATION, never authoritative:
    a missing OR unreadable/corrupt state falls back to the empty state, which makes
    `run_index` take the full-rebuild path (base_sha is None). So a cache miss or
    corruption degrades to the existing rebuild behavior instead of crashing."""
    empty = {"version": 1, "base_sha": None, "records": {}}
    if not STATE_PATH.exists():
        return empty
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return state if isinstance(state, dict) else empty
    except (json.JSONDecodeError, OSError):
        summary("index: state unreadable/corrupt — falling back to full rebuild")
        return empty


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def run_queue() -> int:
    pending = scan_pending(EXTRACTS_DIR)
    summary(f"queue: {len(pending)} deep_dive:high source(s) pending analysis")
    for p in pending:
        print(f"  - {p.file}")
    return 0


def _collect_records(paths: list[str]) -> dict[str, list]:
    out: dict[str, list] = {}
    for rel in paths:
        fp = REPO_ROOT / rel
        if fp.exists():
            out[rel] = records_for(rel, fp.read_text(encoding="utf-8"))
    return out


def _index_scope() -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Index targets + extensions, overridable via env (production default unchanged).

    `INDEX_TARGETS` / `INDEX_EXTS` are comma-separated; unset falls back to the
    docs-only defaults. The #288 diagnostic uses this to index code too."""
    def _csv(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
        raw = os.environ.get(name, "").strip()
        return tuple(x.strip() for x in raw.split(",") if x.strip()) if raw else default
    return (_csv("INDEX_TARGETS", deltascan.DEFAULT_TARGETS),
            _csv("INDEX_EXTS", deltascan.DEFAULT_EXTS))


def run_index(full: bool, dist_only: bool) -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        summary("index: OPENAI_API_KEY not set")
        return 1

    build_t0 = time.time()
    targets, exts = _index_scope()
    state = load_state()
    if full or not state.get("base_sha"):
        paths, deleted = deltascan.full_scan(REPO_ROOT, targets, exts), []
    else:
        paths = deltascan.changed_files(REPO_ROOT, state["base_sha"], targets=targets, exts=exts)
        deleted = deltascan.deleted_files(REPO_ROOT, state["base_sha"], targets=targets, exts=exts)

    changed = _collect_records(paths)
    to_embed = [r for recs in changed.values() for r in select_to_embed(state, recs)]
    summary(f"index: {len(paths)} file(s) in scope, {len(to_embed)} chunk(s) to embed, "
            f"{len(deleted)} deleted; repo floor={REPO_FLOOR}")

    vectors: dict[str, list[float]] = {}
    if to_embed:
        try:
            embedded = embed_texts([r.text for r in to_embed], api_key)
        except AuthError as e:
            summary(f"index: {e}")
            return 1
        except EmbedError as e:
            summary(f"index: {e}")
            return 1
        vectors = {r.id: v for r, v in zip(to_embed, embedded)}

    merged = merge_index(state, changed, deleted, vectors)

    if dist_only:
        # The full pairwise distribution is O(n^2 * dim) — only pay it when the
        # caller actually wants a floor-calibration snapshot (#262), not on
        # every incremental index run.
        dist = distribution(index_vectors(merged))
        summary(f"index: distribution {json.dumps(dist)}")
        summary("index: --distribution set, not writing state")
        return 0

    merged["base_sha"] = deltascan.head_sha(REPO_ROOT)
    save_state(merged)
    summary(f"index: {len(merged['records'])} record(s) written to {STATE_PATH.relative_to(REPO_ROOT)}")

    # AAI_METRICS (#288 Stage A) — churn/latency/cost baseline. Telemetry only.
    prior = state.get("records", {})
    embed_chars = sum(len(r.text) for r in to_embed)
    fields = {"scope": aai_metrics.scope_label()}
    fields.update(aai_metrics.chunk_breakdown(merged["records"]))
    fields.update({
        "churn_add": sum(1 for r in to_embed if r.id not in prior),
        "churn_chg": sum(1 for r in to_embed if r.id in prior),
        "churn_del": len(deleted),
        "embed_chunks": len(to_embed),
        "embed_chars": embed_chars,
        "embed_cost_usd": aai_metrics.embed_cost_usd(embed_chars),
        "build_s": round(time.time() - build_t0, 1),
    })
    aai_metrics.emit("index", fields)
    return 0


def _today() -> str:
    return datetime.now(TZ).strftime("%Y-%m-%d")


def _slug_from_transcript(path: Path) -> str:
    """`<date>-<source-slug>` — the transcript stem minus the `--<video_id>` tail."""
    stem = path.stem
    return stem.rsplit("--", 1)[0] if "--" in stem else stem


def _latest_mental_model() -> tuple[dict | None, str | None]:
    """Most recent active model in mapa-mental-repo/ and its base_commit, or (None, None)."""
    import yaml
    if not MENTAL_DIR.exists():
        return None, None
    models = sorted(MENTAL_DIR.glob("*-mental-model.yaml"), reverse=True)
    if not models:
        return None, None
    data = yaml.safe_load(models[0].read_text(encoding="utf-8")) or {}
    return data, (data.get("meta") or {}).get("base_commit")


def _delta_sections(base_commit: str | None) -> list[dict]:
    """Changed target sections since `base_commit` (or a capped full scan initially)."""
    if base_commit:
        paths = deltascan.changed_files(REPO_ROOT, base_commit)
    else:
        paths = deltascan.full_scan(REPO_ROOT)
    sections: list[dict] = []
    for rel in paths:
        fp = REPO_ROOT / rel
        if not fp.exists():
            continue
        for r in records_for(rel, fp.read_text(encoding="utf-8")):
            sections.append({"path": r.path, "heading": r.heading, "text": r.text})
            if len(sections) >= MAX_DELTA_SECTIONS:
                return sections
    return sections


def run_analyze(transcript_path: str, slug: str | None, with_mental: bool) -> int:
    api_key = os.environ.get("ZAI_API_KEY")
    if not api_key:
        summary("analyze: ZAI_API_KEY not set")
        return 1
    src = Path(transcript_path)
    if not src.exists():
        summary(f"analyze: transcript not found: {transcript_path}")
        return 1

    import phase0_mental_model
    import phase1_extract
    import phase2_patterns
    from analysis_package import write_package
    from glm import AuthError as GLMAuthError
    from glm import GLMError, RateLimited

    slug = slug or _slug_from_transcript(src)
    transcript = src.read_text(encoding="utf-8")

    try:
        extraction = phase1_extract.run(transcript, api_key)          # Fase 1
        mental_model = None
        if with_mental:                                               # Fase 0
            prev, base = _latest_mental_model()
            meta = {"title": slug, "date": _today(), "repo": "long-running-agents",
                    "type": "mental-model", "base_commit": deltascan.head_sha(REPO_ROOT)}
            mental_model = phase0_mental_model.run(prev, _delta_sections(base), api_key, meta=meta)
        patterns = phase2_patterns.run(extraction, api_key)           # Fase 2
    except GLMAuthError as e:
        summary(f"analyze: {e}")
        return 1
    except (RateLimited, GLMError) as e:
        summary(f"analyze: {e}")
        return 1

    written = write_package(REPO_ROOT, slug, mental_model=mental_model,
                            extraction=extraction, patterns=patterns)
    if mental_model is not None:
        MENTAL_DIR.mkdir(parents=True, exist_ok=True)
        import serialize
        (MENTAL_DIR / f"{slug}-mental-model.yaml").write_text(
            serialize.to_yaml(mental_model), encoding="utf-8")
    summary(f"analyze: wrote {len(written)} file(s) to docs/analysis/{slug}/")
    for w in written:
        print(f"  - {w}")
    return 0


def run_classify(slug: str, k: int) -> int:
    openai_key = os.environ.get("OPENAI_API_KEY")
    zai_key = os.environ.get("ZAI_API_KEY")
    if not openai_key or not zai_key:
        summary("classify: OPENAI_API_KEY and ZAI_API_KEY both required")
        return 1

    import yaml

    import phase3_classify
    from analysis_package import package_dir, write_package
    from glm import AuthError as GLMAuthError
    from glm import GLMError, RateLimited
    from grep_verify import verify_all

    patterns_file = package_dir(REPO_ROOT, slug) / f"{slug}-patterns.yaml"
    if not patterns_file.exists():
        summary(f"classify: patterns not found: {patterns_file.relative_to(REPO_ROOT)} (run `analyze` first)")
        return 1
    patterns = (yaml.safe_load(patterns_file.read_text(encoding="utf-8")) or {}).get("patterns", [])
    index = load_state()
    if not index.get("records"):
        summary("classify: empty index — run `index --full` first")
        return 1

    import retrieval
    retriever = retrieval.make_pattern_retriever(patterns, index, openai_key, REPO_ROOT, k=k)
    try:
        classifications = phase3_classify.run(patterns, zai_key, retriever=retriever)
    except GLMAuthError as e:
        summary(f"classify: {e}")
        return 1
    except (RateLimited, GLMError) as e:
        summary(f"classify: {e}")
        return 1

    # grep-verify every citation; flag each classification (verdict-aware).
    verified = verify_all(phase3_classify.citations_of(classifications), REPO_ROOT)
    phase3_classify.mark_verified(classifications, verified)

    written = write_package(REPO_ROOT, slug, classifications=classifications)
    bad = sum(1 for v in verified if not v.get("ok"))
    summary(f"classify: {len(classifications)} classification(s), {bad} unverified citation(s); "
            f"wrote {len(written)} file(s) to docs/analysis/{slug}/")
    for w in written:
        print(f"  - {w}")
    return 0


def run_integrate(manifest_arg: str) -> int:
    """Fase 5 (#264): recompute the four index surfaces from THIS run's manifest.

    Deterministic, no network: takes the repo-relative manifest path the producer
    emitted (`docs/analysis/<slug>/<slug>-artifacts.yaml`) — the single spelling,
    never re-derived here and never a glob over historical v3-shaped manifests —
    recounts the canonical count from disk, and updates only the mechanically
    derivable projections for `status: promoted` entries. Also emits the
    fail-closed diff gate's allowed set (promoted artifacts + manifest + authorized
    index updates) so the workflow can enforce it."""
    import phase5_integrate

    rel = Path(os.path.normpath(manifest_arg))
    if rel.parts[:2] != ("docs", "analysis") or not rel.name.endswith("-artifacts.yaml"):
        summary("integrate: not a run manifest path (expected the repo-relative "
                f"docs/analysis/<slug>/<slug>-artifacts.yaml): {manifest_arg}")
        return 1
    manifest_path = REPO_ROOT / rel
    if not manifest_path.is_file():
        summary(f"integrate: manifest not found: {rel} (run the producer first)")
        return 1
    try:
        report = phase5_integrate.run(REPO_ROOT, manifest_path)
    except ValueError as e:
        summary(f"integrate: {e}")
        return 1

    n_promoted = sum(len(rows) for rows in report["promoted"].values())
    if report["sor_before"] is not None:
        summary(f"integrate: {n_promoted} promoted artifact(s); SOR canonical count "
                f"{report['sor_before']} -> {report['sor_after']} (recount from disk, "
                "never increment)")
    else:
        summary(f"integrate: {n_promoted} promoted artifact(s); no canonical promotion "
                "this run (SOR count untouched)")
    summary(f"integrate: {len(report['changed'])} index surface(s) updated")
    for c in report["changed"]:
        print(f"  - {c}")

    allowed = report["allowed"]
    print(f"INTEGRATE allowed ({len(allowed)} path(s)):")
    for a in allowed:
        print(f"  - {a}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write("allowed<<EOF\n")
            for a in allowed:
                fh.write(a + "\n")
            fh.write("EOF\n")
    return 0


def _worktree_paths() -> set[str]:
    """Repo-relative paths git reports as dirty.

    `-z` so paths are never quoted or escaped, `-uall` so an untracked directory
    is expanded into its files instead of collapsing to one directory entry, and
    rename/copy entries contribute both sides."""
    import subprocess
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "status", "--porcelain", "-z", "-uall"],
        capture_output=True, text=True).stdout
    fields = [f for f in out.split("\0") if f]
    paths: set[str] = set()
    i = 0
    while i < len(fields):
        entry = fields[i]
        i += 1
        if len(entry) < 4:
            continue
        code, path = entry[:2], entry[3:]
        paths.add(path)
        if ("R" in code or "C" in code) and i < len(fields):
            paths.add(fields[i])
            i += 1
    return paths


def run_splice(manifest_arg: str) -> int:
    """Fase 6 (#265): one section splice for this run's first promoted entry.

    Code selects the exact curriculum section via the retrieval index (heading +
    line range), the model sees only that bounded section and returns only a
    replacement body, code applies the splice at the known limits, and the
    localized+additive diff gate plus the #261 machine gate decide landing
    (worktree) vs quarantine. Needs both keys and a built index (`index --full`)."""
    import phase6_splice

    rel = Path(os.path.normpath(manifest_arg))
    if rel.parts[:2] != ("docs", "analysis") or not rel.name.endswith("-artifacts.yaml"):
        summary("splice: not a run manifest path (expected the repo-relative "
                f"docs/analysis/<slug>/<slug>-artifacts.yaml): {manifest_arg}")
        return 1
    manifest_path = REPO_ROOT / rel
    if not manifest_path.is_file():
        summary(f"splice: manifest not found: {rel} (run the producer first)")
        return 1
    openai_key = os.environ.get("OPENAI_API_KEY")
    zai_key = os.environ.get("ZAI_API_KEY")
    if not openai_key or not zai_key:
        summary("splice: OPENAI_API_KEY and ZAI_API_KEY both required")
        return 1
    index = load_state()
    if not index.get("records"):
        summary("splice: empty index — run `index --full` first")
        return 1

    before = _worktree_paths()

    def changed_paths(target: str) -> list[str]:
        """What the splice itself changed: the worktree delta it produced over the
        pre-splice snapshot (so this run's earlier docs/analysis/ writes are not
        attributed to it), plus the target when it was already dirty."""
        after = _worktree_paths()
        return sorted((after - before) | (after & {target}))

    try:
        out = phase6_splice.run(REPO_ROOT, manifest_path, zai_key=zai_key,
                                openai_key=openai_key, index=index,
                                changed_paths_fn=changed_paths)
    except ValueError as e:
        summary(f"splice: {e}")
        return 1

    summary(f"splice: {out['status']} — {out['target']} :: {out['section']['heading']} "
            f"(linhas {out['section']['start'] + 1}..{out['section']['end']})")
    for r in out.get("reasons", []):
        print(f"  - {r}")
    if out.get("quarantine_path"):
        print(f"  - quarentena: {out['quarantine_path']}")
    return 0 if out["status"] in ("applied", "skipped") else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="analyze-and-improve control + judgment plane")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("queue", help="list deep_dive:high sources pending analysis")
    pi = sub.add_parser("index", help="build/refresh the repo semantic index")
    pi.add_argument("--full", action="store_true", help="embed every target section")
    pi.add_argument("--distribution", action="store_true",
                    help="embed + print cosine distribution, write nothing")
    pa = sub.add_parser("analyze", help="run Fases 1->0->2 (GLM) for one transcript")
    pa.add_argument("transcript", help="path to the raw transcript .txt")
    pa.add_argument("--slug", help="package slug (default: derived from the filename)")
    pa.add_argument("--mental-model", action="store_true",
                    help="also run Fase 0 (incremental repo mental model)")
    pc = sub.add_parser("classify", help="run Fase 3 (classify patterns) for a package")
    pc.add_argument("slug", help="package slug (must already have <slug>-patterns.yaml)")
    pc.add_argument("-k", type=int, default=8, help="dense top-k sections (default: 8)")
    pi5 = sub.add_parser("integrate", help="run Fase 5 (index integration) for a run's manifest")
    pi5.add_argument("manifest",
                     help="repo-relative docs/analysis/<slug>/<slug>-artifacts.yaml of this run")
    pi6 = sub.add_parser("splice", help="run Fase 6 (#265: section splice) for a run's manifest")
    pi6.add_argument("manifest",
                     help="repo-relative docs/analysis/<slug>/<slug>-artifacts.yaml of this run")
    args = ap.parse_args(argv)

    if args.cmd == "queue":
        return run_queue()
    if args.cmd == "analyze":
        return run_analyze(args.transcript, args.slug, args.mental_model)
    if args.cmd == "classify":
        return run_classify(args.slug, args.k)
    if args.cmd == "integrate":
        return run_integrate(args.manifest)
    if args.cmd == "splice":
        return run_splice(args.manifest)
    return run_index(args.full, args.distribution)


if __name__ == "__main__":
    raise SystemExit(main())
