# scripts/analyze-and-improve — control plane (Etapa 0)

Deterministic control plane for the **analyze-and-improve v4** rewrite
([EPIC #257](https://github.com/pavani06/long-running-agents/issues/257) ·
design: `docs/plans/2026-09-13-analyze-and-improve-v4.md`). This is the
**Etapa 0** slice: only the code plane + the repo's semantic index. **No LLM
calls** here — model judgment (Fases 0–6) lands in Etapa 1+.

Mirrors the stateless pattern of the YouTube/X pipelines: the repo is the source
of truth, so every job is a diff and re-runs are idempotent.

## Modules

| Module | Role | Pure? |
|---|---|---|
| `frontmatter.py` | Parse extract frontmatter; read/write the `analyzed:` marker surgically | ✅ (except `mark_analyzed` I/O) |
| `analysis_queue.py` | Stateless diff: `deep_dive: "high"` sources without an `analyzed:` marker | ✅ (except `scan_pending` I/O) |
| `deltascan.py` | Git delta scan — which index-target files changed since the last indexed commit | `under_targets` pure; git calls I/O |
| `chunking.py` | Split a doc into sections by heading (code-fence aware) | ✅ |
| `index_store.py` | Section records + incremental index merge (re-embed only changed chunks) | ✅ (vectors supplied by caller) |
| `floor.py` | Cosine + pairwise-similarity distribution + provisional floor | ✅ |
| `embed.py` | OpenAI embeddings client (reused technique; network — not unit-tested) | — |
| `pipeline.py` | CLI tying the above (`queue`, `index`) | — |

Tests: `tests/unit/analyze_and_improve_test.py` — the pure functions the DoD
names (diff, chunking, frontmatter) plus floor and the incremental merge.
Run in isolation (the repo's convention for its pipeline tests):

```bash
python3 -m pytest tests/unit/analyze_and_improve_test.py -q
```

## CLI

```bash
# List deep_dive:high sources still needing an analysis package (no network, no writes)
python3 scripts/analyze-and-improve/pipeline.py queue

# Build/refresh the repo semantic index (needs OPENAI_API_KEY)
python3 scripts/analyze-and-improve/pipeline.py index --full          # initial full index
python3 scripts/analyze-and-improve/pipeline.py index                 # incremental (git delta scan)
python3 scripts/analyze-and-improve/pipeline.py index --distribution  # embed + print distribution, write nothing
```

## Stateless markers & state

- **`analyzed:` marker** — written back into an extract's frontmatter as
  `analyzed: "docs/analysis/<slug>/"` once a source has produced an analysis
  package. The pending queue is `deep_dive: "high"` minus this marker. (Seeding
  the ~9 historical packages onto existing extracts is **Etapa 8**, not here.)
- **Index state** — `.runtime/analyze-and-improve/index.json` (gitignored). It
  is *derived* state (section records + vectors + the `base_sha` the next delta
  scan starts from), rebuilt from the repo; it is a cache, never committed.
  Persisting it across GitHub Actions runs is **Etapa 8** wiring.

## Semantic index

Targets — the repo's authoritative knowledge layers (retrieval surfaces for the
Fase 3 classifier): `docs/canonical/`, `docs/decisions/`, `curriculum/`,
`.opencode/skills/`. Chunk = one section per ATX heading. On an incremental run,
the git delta scan flags changed **files** and a content-hash diff re-embeds
only the changed **chunks** within them — "atualizado só nos chunks que o delta
scan aponta".

### Provisional floor (calibration is #262)

The **floor** is the cosine threshold below which two sections are treated as
unrelated during retrieval. `floor.PROVISIONAL_FLOOR = 0.38` is a **starting
value only**, anchored to the connections layer's cross-video floor (~0.38).

The repo's section-embedding distribution differs from the videos' (denser
shared vocabulary), so the empirical floor must be calibrated to the repo. The
methodology, deferred to **Etapa 4 (#262)**:

1. Run `pipeline.py index --distribution` once a key is available. It embeds
   every target section and prints the pairwise-cosine distribution
   (`min / p50 / p75 / p90 / p95 / p99 / max`) without writing state.
2. Set the floor from that distribution (a high percentile — e.g. p90/p95 —
   selects the genuinely-related tail while rejecting ambient similarity).
3. Record the chosen floor + the distribution snapshot alongside the #262 A/B
   validation.

Running live embeddings is an external, billed side effect and is intentionally
**not** performed in this Etapa 0 slice (no live model calls).
