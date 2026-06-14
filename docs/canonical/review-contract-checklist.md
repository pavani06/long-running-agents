---
title: "Review Contract Checklist"
type: canonical
aliases: ["review contract", "checklist contract", "review dimensions", "structured review checklist", "review-contract.yaml", "review contract yaml"]
tags: ["evals", "agentic-coding", "governanca"]
last_updated: 2026-06-15
relates-to: ["[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]]", "[[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]"]
sources: ["[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|Canary Test Patterns]]", "[[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|Canary Test Classification]]"]
---

# Review Contract Checklist

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|Canary Test Analysis]]
**Classification:** Partial Coverage ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:70-98)
**Precedence:** Level 2 ([[docs/system-of-record|System of Record]])

---

## Problem

Freeform agent review produces ambiguous comments that are hard to verify, compare, or turn into repeatable gates. When told to "review this code," an AI reviewer generates prose commentary that the developer must reinterpret — the reviewer did not know which dimensions to check, the developer does not know what was checked, and downstream gates cannot consume the unstructured output. The canary-test analysis identifies this as the freeform AI commentary failure pattern: ambiguous, hard-to-verify output that increases action latency and can cause issues to be ignored due to lack of clarity ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:327-338).

The repo has rich evaluation infrastructure — constraint-anchored evaluation with verification matrices, sprint contracts with acceptance criteria, independent rubrics in split-brain review — but these structures are oriented toward evaluating agent output quality (product recommendations, generated code correctness), not toward structured checklist contracts specifically for AI code review ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:75-79). The structural foundation exists; the specific format and application to AI code review dimensions is missing.

## Solution

Replace open-ended review prompts with a `review-contract.yaml` checklist attached to each change. The contract declares explicit review dimensions and per-item statuses, turning AI review from "comment on whatever you notice" into "verify these specific properties and return structured pass/fail/not-applicable results."

**Review contract format:**

```yaml
items:
  - dimension: security_surface
    status: pass | fail | not-applicable
  - dimension: data_model_migrations
    status: pass | fail | not-applicable
  - dimension: api_compatibility
    status: pass | fail | not-applicable
  - dimension: error_handling_coverage
    status: pass | fail | not-applicable
  - dimension: test_coverage_new_paths
    status: pass | fail | not-applicable
```

This format is specified in the analysis source ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:97-113) and is confirmed NOT_FOUND as a file or template outside the canary-test analysis itself ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:90).

**Review dimensions defined:**

| Dimension | What it covers | Typical sources of rules |
|---|---|---|
| `security_surface` | New attack surface: auth changes, input validation, secret handling, permission boundaries | Security policy, OWASP guidelines, team conventions |
| `data_model_migrations` | Schema changes: column additions, deprecations, migration rollback safety, data integrity | Database policy, migration guidelines |
| `api_compatibility` | Breaking changes: endpoint signatures, response format, error codes, versioning | API versioning policy, consumer contracts |
| `error_handling_coverage` | Error paths: try/catch completeness, error propagation, user-facing messages, retry policy | Error handling standards, NFR documents |
| `test_coverage_new_paths` | Test evidence: new code paths have tests, edge cases covered, regression protection | Testing policy, coverage thresholds |

**Processing mechanics:**

The AI reviewer processes each contract item independently. For each dimension declared as applicable, the reviewer:
1. Reads the `review-contract.yaml` to identify active dimensions.
2. For each dimension, analyzes the diff against dimension-specific rules.
3. Returns a structured finding per dimension: `pass`, `fail`, or `not-applicable`.
4. When `fail`, includes the specific violation and location for immediate remediation.

Independent processing per item is the structural property that makes AI reviewers more effective — the reviewer does not blend concerns across dimensions, and each verdict stands alone as a verifiable claim ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|patterns]]:53-54).

**Relationship to AI review confidence:**

Without contract checklists, shadow review pipeline agreement metrics are ambiguous — you cannot compare human and AI findings per category if the AI was asked an open-ended question. With contracts, each dimension produces a discrete, comparable data point: did the AI and human agree on `security_surface` for this change? Over many changes, per-dimension agreement rates drive gating decisions ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:382-384).

## Implementation in this repo

### What already exists

The repo has evaluation infrastructure that provides the structural foundation for review contracts:

- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:31-49 — formal verification-matrix format (`constraint → check → pass/fail → violation detail`) with aggregate verdict approving only when all constraints pass. This is the closest structural match to the review contract checklist, but is oriented toward agent output constraints, not code review dimensions.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:57-65 — evaluator applies quality rubrics and business rules with access to `cliente_data` and rubrics, producing approve/reject with specific feedback.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 — independent rubrics applied by separate engineering and destination reviewers, reconciled through explicit decisions.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:30-43 — structured PR eval report with `change_scope`, `baseline_version`, `quality_delta`, `latency_delta`, `cost_delta`, `thresholds`, `failure_examples`, `merge_policy`.
- [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]:30-42 — eval cases with `expected_outcome`, `acceptable_tool_behavior`, `baseline`, and `grading_notes`.
- [[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md]]:72-131 — teaches sprint contracts as a pre-agreed definition of "done" between Generator and Evaluator.
- [[curriculum/08-tools-templates/evaluation-rubric-template|Evaluation Rubric Template]] — template for structured evaluation rubrics with measurable criteria.

The classification identifies this infrastructure as rich but notes it is primarily about evaluating agent output quality, not AI code review specifically ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:77-79).

### What is missing

1. The `review-contract.yaml` format: a structured checklist with explicit review dimensions (security surface, migrations, API compatibility, error handling, test coverage) attached to each change. NOT_FOUND as a file or template anywhere outside the canary-test analysis ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:90).
2. Per-item status of `pass`, `fail`, or `not-applicable` specifically for code review dimensions — the existing verification matrix in constraint-anchored evaluation is for agent output constraints, not code review items ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:91).
3. Review dimensions as an explicit named concept for AI code review — existing dimensions are about eval quality (quality, latency, cost), not code review dimensions (security, migrations, API compatibility) ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:92).
4. Contract attachment to the change itself — sprint contracts exist in the curriculum, but they define work scope, not review scope per change ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:93).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Structured, comparable output: every review produces the same five dimensions with discrete verdicts | A weak or incomplete contract can omit important risks without signaling the omission |
| AI reviewers are more effective processing independent, bounded checks than open-ended instructions | Checklist maintenance costs grow as the system and review policy evolve |
| Per-dimension agreement metrics feed shadow pipeline gating decisions with comparable data | Does not replace human architectural judgment when dimensions require tradeoff evaluation |
| Eliminates the "I didn't know I was supposed to check that" problem — the contract makes expectations explicit | Contract attachment per change adds a process step; automation is needed to avoid manual overhead |
| Downstream gates (pre-commit, PR enforcement) consume the same structured output | May surface gaps when an important dimension was marked `not-applicable` but should have been checked |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]] because the verification-matrix format (`constraint → check → pass/fail → violation detail`) is the structural foundation for per-dimension review contract items.
- **Uses:** [[docs/canonical/generator-evaluator|Generator-Evaluator]] because the AI reviewer acts as the evaluator and the code author acts as the generator, with the review contract serving as the rubric.
- **Enables:** [[docs/canonical/shadow-review-pipeline|Shadow Review Pipeline]] because structured, per-dimension findings are required to compute agreement metrics that are comparable with human review outcomes. The analysis states this dependency explicitly: without contracts, shadow period agreement data would be ambiguous ([[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:382-384).
- **Enables:** [[docs/canonical/pre-commit-ai-review-gate|Pre-Commit AI Review Gate]] because the pre-commit gate uses review contract dimensions as the checklist the AI reviewer validates before push.
- **Complements:** [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] because independent rubrics applied by separate engineering and destination reviewers are contract items applied by review dimension.
- **Complements:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] because the structured PR eval report fields (`change_scope`, `thresholds`, `failure_examples`) align with review contract dimensions.
- **Validated by:** [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] because spot-check cases can include review contracts as expected outcomes per dimension.

## References

- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:62-70 — review contract model with five dimensions and per-item status.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:93-121 — Review Contract as Checklist pattern mechanics and YAML structure.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:272-279 — tradeoff: comentario livre vs. resultado estruturado.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:327-338 — failure pattern: freeform AI commentary.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-analysis|analysis]]:382-384 — dependency: shadow pipeline requires structured contracts for comparable metrics.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-patterns|patterns]]:39-59 — extracted pattern definition with inputs, outputs, benefits, limitations.
- [[docs/analysis/2026-06-15-canary-test/2026-06-15-canary-test-classification|classification]]:70-98 — Partial Coverage classification with what exists and what is missing.
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:31-49 — verification matrix format (structural foundation).
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:57-65 — evaluator applying rubrics with approve/reject verdicts.
- [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]]:28-41 — independent rubrics and reconciliation.
- [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]:30-43 — structured PR eval report fields.
- [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]:30-42 — eval cases with expected outcomes and grading notes.
- [[curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern|curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md]]:72-131 — sprint contracts as pre-agreed acceptance criteria.

---

*Created: 2026-06-15 | From: Canary Test Code Review pattern classification | Precedence: canonical*
