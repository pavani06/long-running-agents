# eval-truth store (#288)

Curated **evaluation ground-truth** for the metamorphic eval-harness. This
directory is the *answer key*: it defines, for each concept, its identity, the
expected repo state, the evidence anchor, and the hand-authored paraphrases that
map back to it.

## Why it lives here (and nowhere else)

The eval-harness classifies whether the repo covers a concept. If the classifier
could retrieve or `git grep` this directory, it would be grading against its own
answer key — exactly the contamination the #288 E/R/V run exposed (the classifier
cited the canon as "repo evidence" for every concept). So this store is kept
**outside the system-under-test's observable universe**: each run builds a
disposable SUT-view (`sut_view.py`) — a worktree of HEAD with `eval/truth/`
removed — and hands *that* to the retriever. A deterministic preflight
(`metamorphic_preflight.py`) proves the leak sentinel below is unreachable in the
view before any model call, and refuses to run otherwise.

**Invariant (harness):** no artifact that contains or derives the evaluation
ground truth may be reachable by the system-under-test's retrieval / grep /
classifier during evaluation. New truth artifacts belong **under this prefix**, so
they are invisible to the SUT by default. (See the evidence-provenance ADR,
`docs/decisions/2026-09-14-evidence-provenance-non-collapse.md`.)

## Contents

- `metamorphic_canon.yaml` — the Concept Canon: **10 concepts × 5 paraphrases**
  (5 that exist in the repo, 3 that do not, 2 partial/borderline), each with
  `concept_id`, `canonical_definition`, `aliases`, `positive/negative_examples`,
  `expected_repo_state {exists}`, `expected_verdict`, real `evidence[]`, plus the
  `near_miss_pairs` (T4) and `reranker_sanity` pairs. Carries `_leak_sentinel`
  (`EVALTRUTH-SENTINEL-…`) — the token the preflight asserts is unreachable.

## Maintenance note

`expected_repo_state` is subjective, curated ground-truth and **rots with the
repo** — the partial concepts and their evidence lines drift first. History
becomes a regression corpus, not primary ground-truth.
