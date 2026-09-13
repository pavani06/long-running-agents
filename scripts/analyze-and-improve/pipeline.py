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
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))

import deltascan  # noqa: E402
from analysis_queue import scan_pending  # noqa: E402
from embed import AuthError, EmbedError, embed_texts  # noqa: E402
from floor import PROVISIONAL_FLOOR, distribution  # noqa: E402
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
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"version": 1, "base_sha": None, "records": {}}


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


def run_index(full: bool, dist_only: bool) -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        summary("index: OPENAI_API_KEY not set")
        return 1

    state = load_state()
    if full or not state.get("base_sha"):
        paths, deleted = deltascan.full_scan(REPO_ROOT), []
    else:
        paths = deltascan.changed_files(REPO_ROOT, state["base_sha"])
        deleted = deltascan.deleted_files(REPO_ROOT, state["base_sha"])

    changed = _collect_records(paths)
    to_embed = [r for recs in changed.values() for r in select_to_embed(state, recs)]
    summary(f"index: {len(paths)} file(s) in scope, {len(to_embed)} chunk(s) to embed, "
            f"{len(deleted)} deleted; provisional floor={PROVISIONAL_FLOOR}")

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


def _make_retriever(patterns: list[dict], index: dict, openai_key: str, *, k: int):
    """A `retriever(need_more)->context` closure over the Etapa-0 index.

    need_more=None → initial context: dense top-k for the patterns' text + grep
    of the pattern names. Otherwise: grep the model-named identifiers + append
    the named files' content. Embedding (network) happens here, not in Fase 3.
    """
    import retrieval
    from embed import embed_texts

    def _dense(query_text: str) -> list[dict]:
        qvec = embed_texts([query_text], openai_key)[0]
        return retrieval.fetch_texts(retrieval.rank_sections(qvec, index, k=k), REPO_ROOT)

    def retriever(need_more):
        if need_more is None:
            query = "\n".join(f"{p.get('name','')} {p.get('problem','')} {p.get('mechanism','')}"
                              for p in patterns)
            dense = _dense(query)
            grep = retrieval.grep_identifiers([p.get("name", "") for p in patterns], REPO_ROOT)
            return retrieval.build_context(dense, grep)
        grep = retrieval.grep_identifiers(need_more.get("greps", []), REPO_ROOT)
        extra = []
        for rel in need_more.get("files", []):
            fp = REPO_ROOT / rel
            if fp.exists():
                extra.append({"path": rel, "heading": "(arquivo pedido)", "score": 0.0,
                              "text": fp.read_text(encoding="utf-8")[:4000]})
        return retrieval.build_context(extra, grep)

    return retriever


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

    retriever = _make_retriever(patterns, index, openai_key, k=k)
    try:
        classifications = phase3_classify.run(patterns, zai_key, retriever=retriever)
    except GLMAuthError as e:
        summary(f"classify: {e}")
        return 1
    except (RateLimited, GLMError) as e:
        summary(f"classify: {e}")
        return 1

    # grep-verify every citation; annotate each classification with the verdict.
    verified = verify_all(phase3_classify.citations_of(classifications), REPO_ROOT)
    ok_by_pattern: dict[str, bool] = {}
    for v in verified:
        pat = v.get("pattern")
        ok_by_pattern[pat] = ok_by_pattern.get(pat, True) and bool(v.get("ok"))
    for c in classifications:
        c["verified"] = ok_by_pattern.get(c.get("pattern"), True)

    written = write_package(REPO_ROOT, slug, classifications=classifications)
    bad = sum(1 for v in verified if not v.get("ok"))
    summary(f"classify: {len(classifications)} classification(s), {bad} unverified citation(s); "
            f"wrote {len(written)} file(s) to docs/analysis/{slug}/")
    for w in written:
        print(f"  - {w}")
    return 0


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
    args = ap.parse_args(argv)

    if args.cmd == "queue":
        return run_queue()
    if args.cmd == "analyze":
        return run_analyze(args.transcript, args.slug, args.mental_model)
    if args.cmd == "classify":
        return run_classify(args.slug, args.k)
    return run_index(args.full, args.distribution)


if __name__ == "__main__":
    raise SystemExit(main())
