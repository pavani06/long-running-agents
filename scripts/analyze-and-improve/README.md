# scripts/analyze-and-improve — control plane + judgment plane (Fases 0–2)

The **analyze-and-improve v4** rewrite
([EPIC #257](https://github.com/pavani06/long-running-agents/issues/257) ·
design: `docs/plans/2026-09-13-analyze-and-improve-v4.md`). Two planes:

- **Control plane (Etapa 0, #258)** — deterministic, no LLM: stateless queue +
  the repo's per-section semantic index.
- **Judgment plane (Etapa 1, #259)** — HTTP-portable GLM 5.3 (generator): Fases
  0 (repo mental model, incremental), 1 (source extraction), 2 (patterns), as
  stateless functions. Classification (Fase 3, #260) and the adversarial
  gate/quarantine (#261) come later.

Mirrors the stateless pattern of the YouTube/X pipelines: the repo is the source
of truth, so every job is a diff and re-runs are idempotent. The pure control
plane stays free of I/O; the judgment plane isolates the single GLM call per
phase behind an injectable client so prompt-assembly and output-parsing are
unit-tested with no network.

## Modules

### Control plane (Etapa 0)

| Module | Role | Pure? |
|---|---|---|
| `frontmatter.py` | Parse extract frontmatter; read/write the `analyzed:` marker surgically | ✅ (except `mark_analyzed` I/O) |
| `analysis_queue.py` | Stateless diff: `deep_dive: "high"` sources without an `analyzed:` marker | ✅ (except `scan_pending` I/O) |
| `deltascan.py` | Git delta scan — which index-target files changed since the last indexed commit | `under_targets` pure; git calls I/O |
| `chunking.py` | Split a doc into sections by heading (code-fence aware) | ✅ |
| `index_store.py` | Section records + incremental index merge (re-embed only changed chunks) | ✅ (vectors supplied by caller) |
| `floor.py` | Cosine + pairwise-similarity distribution + provisional floor | ✅ |
| `embed.py` | OpenAI embeddings client (reused technique; network — not unit-tested) | — |

### Judgment plane (Etapa 1 — GLM, Fases 0–2)

| Module | Role | Pure? |
|---|---|---|
| `glm.py` | Generic GLM chat client, JSON-strict + backoff (`chat_json`, `extract_json`) | `extract_json` pure; HTTP not tested |
| `phase1_extract.py` | Fase 1 — extraction from the full raw transcript | `build_messages`/`parse_extraction` pure; `run` injects the client |
| `phase0_mental_model.py` | Fase 0 — incremental repo mental model from the delta scan | `build_messages`/`parse_model` pure; `run` injects the client |
| `phase2_patterns.py` | Fase 2 — patterns synthesised over the Fase 1 output | `build_messages`/`parse_patterns` pure; `run` injects the client |
| `retrieval.py` | Fase 3 hybrid retrieval — dense top-k over the index + grep | `rank_sections`/`build_context` pure; embed/grep/file reads I/O |
| `grep_verify.py` | Deterministic grep-verify of citations (existence + content) | `verify_citation`/`all_ok` pure; `verify_all` reads files |
| `phase3_classify.py` | Fase 3 — classify Missing/Partial/Exists/Better, 1 'ask-for-more' round | `build_messages`/`parse_*`/`citations_of` pure; `run` injects client + retriever |
| `serialize.py` | Render phase outputs to `.yaml`/`.md` (PyYAML) | ✅ |
| `analysis_package.py` | Write the partial package to `docs/analysis/<slug>/` | I/O over the pure serializers |
| `pipeline.py` | CLI: `queue`, `index`, `analyze`, `classify` | — |

### Machine gate + landing (Etapa 3 — closes Tier A)

The gate that replaces the operator (who can't review at volume): deterministic
checks + an adversarial evaluator + quarantine + a landing library.

| Module | Role | Pure? |
|---|---|---|
| `dedup.py` | Cosine duplication check vs the Etapa-0 index (a proposed artifact at/above the threshold is held) | ✅ (`is_duplicate`/`nearest`) |
| `openai_chat.py` | OpenAI chat client (the evaluator's transport — a *different* provider from GLM) | `extract_json` reused; HTTP not tested |
| `evaluator.py` | Adversarial evaluator: fixed rubric (fidelity/evidence/non-duplication/format), provisional min score | `build_messages`/`parse_evaluation` pure; `run` injects client |
| `quarantine.py` | Route accept vs `proposed/`; fail-closed gate report; `quarantine_relpath` (the quarantined copy path `docs/analysis/<slug>/proposed/<dest>`) | ✅ |
| `landing.py` | Build the PR body + rolling quarantine-Issue digest; `LandingPlan` (`auto_merge`, `dry_run`) — the library, **not** the workflow | ✅ |
| `spine.py` | `run_spine` — chains Fases 0→3 + gates + evaluator + route + landing (the entry point #262 invokes) | `artifact_for_eval`/`dedup_text` pure; `run_spine` needs both keys |
| `ab_validate.py` | A/B validation (Etapa 4, #262): fresh-vs-historical label agreement + seeded-duplicate check + report; suggests the calibrated floor/cut | `label_agreement`/`decide_ab`/`ab_report`/`suggest_floor` pure; `run` needs both keys |

### Creation phase (Etapa 5, #263 — Fase 4 + artifact manifest)

Canonical-doc creation is the proven-live First-Loop path (`first_loop.py` +
`first-loop.yml`: one canonical doc at its destination on the proposal branch,
PR = quarantine, human merge = promotion). The #263 remainder generalizes
creation to all three artifact types behind the same gates:

| Module | Role | Pure? |
|---|---|---|
| `phase4_create.py` | Fase 4 generation — canonical doc (proven path; verdict-aware for Partial P1/P2), **skill** (`.opencode/skills/<slug>/SKILL.md`) and **exercise** (`curriculum/<level>/exercises/exercise-<NN>-<slug>.md`, level/number orchestrator-decided) with full content, frontmatter-compliant renderers | `build_messages*`/`parse_*`/`render_*`/`*_destination`/`next_exercise_number` pure; `create*` inject the client |
| `phase4_routing.py` | Priorização por classificação (Missing=P0, Partial high=P1, medium=P2, Exists/Better=skip) + roteamento de categoria (P0 → canonical+skill+exercise; P1 → canonical+exercise; P2 → canonical) + the ordered `plan_of_work` | ✅ |
| `artifact_manifest.py` | The artifacts manifest (`<slug>-artifacts.{yaml,md}`) — the typed contract Fase 5 (#264) reads: artifacts by category (canonical/skill/exercise) with promoted/quarantined status, the per-exercise curriculum `level`, skipped patterns, not-applicable rows, integration map | `build_manifest`/`manifest_yaml`/`manifest_md` pure |
| `phase4_flow.py` | The governed loop: `plan_of_work` → generation → **quarantine write** (`docs/analysis/<slug>/proposed/<dest>`, never the authoritative layers) → Etapa-3 gates (evaluator + dedup + validate + verified citations + the destination-scoped convention check, fail-closed) → **promote-on-pass** (in-worktree move; refuses occupied destinations) → manifest | path/wiring pure parts tested; `run_fase4` needs both keys (all injectable) |

**Destination-scoped validation.** `validate-obsidian` scopes Checks 1/5/6 to
`docs/canonical/<file>.md` and Check 9 to `curriculum/`, so a quarantined copy
never triggers them. `spine.validate_destination` runs *the same validator* over a
throwaway root holding the proposed file at its intended destination — the rules
stay owned by `scripts/validate-obsidian.ts`, with no second copy to drift from
it, and no authoritative layer is written. It is fail-closed on two distinct
gates: `destination_valid` (the validator's own violations, carried verbatim into
the manifest's hold reasons) and `destination_validated` (the validator could not
run at all — held, but never reported as a content violation).

The root carries the repo's *rules* but not its *vault*: it holds only the
proposed file, so Check 6 reads every wikilink as broken and the verdict is
stricter than the repo-wide run. That is deliberate for generated pre-review
output — the generator prompt forbids links outright — and a human editing the
quarantined copy can add conventional cross-links afterwards, with the PR's own
obsidian CI as the full-context authority.

**Exercise level (INTERIM).** `DEFAULT_LEVEL_DIR` places every generated exercise
at curriculum level 3; there is no level routing yet. The resolved level is
recorded per exercise in the manifest, and Etapa 7 (#265) must decide whether and
how to own the routing using that field as its re-routing input.

**Boundaries.** The evaluator is OpenAI on purpose — a different provider from
the GLM generator, so it never grades its own homework (`OPENAI_API_KEY`, model
via `OPENAI_EVAL_MODEL`, provisional default). `auto_merge=False` is the
require-approval brake, usable from day 1; the **real Actions wiring**
(open/auto-merge PR, update the rolling quarantine Issue) is **#266**, not here.
Both the dedup threshold and the evaluator's minimum score are **provisional** —
final calibration is **#262**. Fases that create/mutate the product (4–7) are out
of scope for this Tier-A slice.

**Dependencies:** control plane needs only `requests` (+ stdlib). The judgment
plane's `serialize.py` needs **PyYAML** — a workflow running `analyze` must
`pip install requests pyyaml`. `queue`/`index` do not import PyYAML (the
judgment-plane imports are lazy).

Tests — run in isolation (the repo's convention for its pipeline tests):

```bash
python3 -m pytest tests/unit/analyze_and_improve_test.py -q          # control plane
python3 -m pytest tests/unit/analyze_and_improve_phases_test.py -q   # judgment plane (Fases 0–2)
python3 -m pytest tests/unit/analyze_and_improve_classify_test.py -q # Fase 3 (retrieval + grep-verify)
python3 -m pytest tests/unit/analyze_and_improve_spine_test.py -q    # Etapa 3 (dedup + rubric + quarantine + landing)
python3 -m pytest tests/unit/analyze_and_improve_ab_test.py -q       # Etapa 4 (A/B agreement + report)
python3 -m pytest tests/unit/phase4_routing_test.py -q               # Fase 4 (priorização + roteamento de categoria)
python3 -m pytest tests/unit/phase4_create_test.py -q                # Fase 4 (canonical/skill/exercise creation)
python3 -m pytest tests/unit/artifact_manifest_test.py -q            # Fase 4 (manifesto — contrato da Fase 5)
python3 -m pytest tests/unit/phase4_flow_test.py -q                  # Fase 4 (escrita em quarentena + promoção)
python3 -m pytest tests/unit/metamorphic_canon_test.py -q            # #288 canon (load/validate + real-evidence check)
python3 -m pytest tests/unit/metamorphic_match_test.py -q            # #288 two-stage matcher
python3 -m pytest tests/unit/metamorphic_rerank_test.py -q           # #288 reranker + sanity mini-eval
python3 -m pytest tests/unit/metamorphic_metrics_test.py -q          # #288 T1–T4 + gates
```

### A/B validation (Etapa 4, #262 — Tier-B progression gate)

The live A/B run needs the API keys, which live in **GitHub Actions secrets** —
so it runs as the `A/B Validate (Tier A · #262)` workflow (`workflow_dispatch`,
read-only, writes nothing to the repo): it builds the index, runs `run_spine`
for the 12-factor source, compares the fresh classification labels to the
historical package (agreement ≥ 80%), confirms the cosine dedup catches a seeded
duplicate, and prints the empirical distribution. **#262 finalized the floor
(`floor.REPO_FLOOR = 0.535`, p90 of the repo distribution) and validated the
dedup threshold (`dedup.DUP_THRESHOLD = 0.85`, seed caught at ~1.0)**; the
evaluator cut (`evaluator.PROVISIONAL_MIN_MEAN`) stays provisional (n=2). The
job's exit reflects the gate (0 = proceed, 1 = iterate). NOTE: the historical
label-agreement criterion was **retired** as mis-specified (it compared a fresh
transcript to a Jun-2026 curated package — too few comparable patterns); the
real Tier-B progression gate is the metamorphic eval-harness (#288).

### Metamorphic eval-harness (#288 — the Tier-B progression gate)

The durable replacement for the retired A/B criterion. Instead of comparing a
fresh run to a curated package of another source/state (which measured
source/naming *alignment*, not *quality*), it measures **semantic invariance**:
reformulating the same concept must not change the verdict. That is a
self-contained metamorphic test — no historical package needed.

The Concept Canon (the curated ground-truth) lives **outside this module**, in the
eval-truth store `eval/truth/` (see its own README) — it is deliberately kept out
of the system-under-test's observable universe so the classifier cannot retrieve
its own answer key (#288 decontamination).

| Module | Role | Pure? |
|---|---|---|
| `metamorphic_canon.py` | Load + validate the canon (existence paired with evidence; verdict agrees with `exists`); flatten the cases | `validate_structure`/`evidence_substring_ok`/`profile_text`/`all_variants` pure |
| `metamorphic_match.py` | Two-stage matcher: stage-1 cosine rank of candidates + stage-2 decision from reranker verdicts | ✅ (`rank_candidates`/`decide_match`) |
| `metamorphic_rerank.py` | Stage-2 reranker on **OpenAI** (≠ GLM): `same_concept` + `granularity_relation`, plus its own sanity mini-eval | `build_messages`/`parse_rerank`/`score_sanity` pure; `run*` need the key |
| `metamorphic_metrics.py` | T1 identification · T2 invariance · T3 dedup · T4 novelty + Gates A/B/C (never a single blended score) | ✅ |
| `sut_view.py` | Disposable system-under-test view — a worktree of HEAD minus `eval/truth/` handed to the existing retriever as `repo_root`, so the classifier's whole observable universe excludes eval-truth | `path_within` pure; git I/O tested over a tmp repo |
| `metamorphic_preflight.py` | Deterministic negative gate: proves the eval-truth sentinel is unreachable in the SUT-view (grep + index + realpath boundary) and refuses to run otherwise | `sentinel_of`/`index_has_truth_paths`/`assess` pure |
| `metamorphic_poc.py` | Live PoC runner: builds the SUT-view, runs the preflight, wires the stages, classifies each variant independently (GLM) against the view, emits the gate report | `run` needs both keys |

**The three non-negotiables (from the #288 grill):** (a) invariance (T2) only
counts paired with the correction anchor — Gate C requires real repo evidence for
every existence verdict; consistency without correction would certify the spine
"consistently wrong". (b) The paraphrases are hand-authored (a different model
than the GLM classifier), never GLM-generated — otherwise it measures "the model
agrees with its own paraphrases". (c) The reranker is on the OpenAI side (≠ the
GLM generator) and passes its own sanity mini-eval before its verdicts are
trusted.

**Gates (PoC DoD):** A (identification) recall ≥ 90% and false-merge < 5%;
B (invariance) agreement ≥ 90%, no unexplained Exists∧Missing dispersion, and
each concept's modal verdict matching its `expected_repo_state` (so an
invariant-but-uniformly-wrong spine — e.g. all-Missing on a present concept — is
caught, not certified);
C (evidence) every existence verdict grep-verified. Tier B (#263–#266) advances
only if A **and** B **and** C **and** the reranker sanity all pass. The
`expected_repo_state` is subjective, curated ground-truth and rots with the repo
(documented maintenance cost); history becomes a regression corpus, not
ground-truth.

The live run needs the API keys (Actions secrets), so it is the
`Metamorphic Eval (Tier B gate · #288)` workflow (`workflow_dispatch`,
read-only). `max_variants` runs a cheap smoke of the first N cases before the
full 50 (each run is billed: index build + ~50 independent GLM classify calls +
the reranker). Job exit reflects the gate (0 = proceed, 1 = iterate).

## CLI

```bash
# List deep_dive:high sources still needing an analysis package (no network, no writes)
python3 scripts/analyze-and-improve/pipeline.py queue

# Build/refresh the repo semantic index (needs OPENAI_API_KEY)
python3 scripts/analyze-and-improve/pipeline.py index --full          # initial full index
python3 scripts/analyze-and-improve/pipeline.py index                 # incremental (git delta scan)
python3 scripts/analyze-and-improve/pipeline.py index --distribution  # embed + print distribution, write nothing

# Run Fases 1->0->2 (GLM) for one transcript (needs ZAI_API_KEY)
python3 scripts/analyze-and-improve/pipeline.py analyze <transcript.txt>                  # Fases 1 + 2
python3 scripts/analyze-and-improve/pipeline.py analyze <transcript.txt> --mental-model   # also Fase 0

# Run Fase 3 (classify a package's patterns against the repo) — needs OPENAI_API_KEY + ZAI_API_KEY
python3 scripts/analyze-and-improve/pipeline.py classify <slug>        # reads <slug>-patterns.yaml, writes classification
python3 scripts/analyze-and-improve/pipeline.py classify <slug> -k 12  # more dense sections in context
```

**Fase 3 (classification).** Hybrid retrieval builds the context: dense top-k
sections from the Etapa-0 index (the query is the patterns' text, embedded) plus
`git grep` on the pattern identifiers. The model classifies each pattern
Missing/Partial/Exists/Better with `file:line` evidence; if it declares the
context insufficient it names exact greps/files (`need_more`) and the code does
**one** more retrieval + call. Every cited `file:line` is then **grep-verified**
deterministically (the line exists and contains the claimed quote); a
classification whose citations fail verification is flagged `verified: false`.

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

### Repo floor (calibrated via #262)

The **floor** is the cosine threshold below which two sections are treated as
unrelated during retrieval. `floor.REPO_FLOOR = 0.535` was **calibrated via #262**
as the p90 of the repo's empirical section-cosine distribution (p50 0.415 / p75
0.479 / p90 0.535 / p99 0.64) — the genuinely-related tail sits above ambient
similarity. Recompute by re-running the methodology below when the corpus shifts:

1. Run `pipeline.py index --distribution` once a key is available. It embeds
   every target section and prints the pairwise-cosine distribution
   (`min / p50 / p75 / p90 / p95 / p99 / max`) without writing state.
2. Set the floor from that distribution (a high percentile — e.g. p90/p95 —
   selects the genuinely-related tail while rejecting ambient similarity).
3. Record the chosen floor + the distribution snapshot alongside the #262 A/B
   validation.

Running live embeddings is an external, billed side effect and is intentionally
**not** performed in this Etapa 0 slice (no live model calls).
