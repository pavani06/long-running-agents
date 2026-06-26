---
title: "Living Eval Dataset"
type: canonical
aliases: ["living eval", "growing eval dataset", "monotonic eval dataset"]
tags: ["evals", "production"]
last_updated: 2026-06-26
relates-to: ["[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]]", "[[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]", "[[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]]", "[[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]]", "[[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]"]
sources: []
---
# Living Eval Dataset

**Type:** canonical
**Status:** active
**Source:** The Production AI Playbook (Bhaumik, Databricks)
**Classification:** Partial Coverage
**Precedence:** document-level 2 (canonical) per `docs/system-of-record.md`

---

## Problem

Static test suites do not catch regressions from new failure modes discovered in production. Every incident teaches a lesson that is lost unless codified as a permanent test case that prevents reoccurrence. Without a mechanism that guarantees the eval dataset grows with every incident, the system's safety does not improve over time — it resets after each fix.

Additionally, eval datasets tend to become unmanageable monoliths: uncategorized test cases, unclear ownership, and a single execution plan that runs everything on every change, making eval economically unsustainable and operationally painful.

## Solution

A **monotonically growing** eval dataset: every production incident, every escaped edge case, every new feature specification becomes a permanent addition to the dataset. The dataset never shrinks — obsolete cases are archived (not deleted, for traceability). The system gets strictly safer over time because each failure invests in future quality.

### Core Properties

**Monotonic growth guarantee:** The dataset only grows. Cases are never deleted. When a feature is deprecated or a failure mode becomes impossible, the corresponding cases are moved to an archive partition — preserved for audit trail and traceability, but excluded from execution.

**Categorization taxonomy:** Every test case is assigned to a category with an explicit owner. Recommended taxonomy:

| Category | Example | Owner |
|---|---|---|
| Security | PII leak, authentication bypass, unsafe action | Security team |
| Login / Auth | Authentication flow failures, session handling | Auth team |
| Tool calls | Wrong tool selection, wrong parameters, tool loop | Platform team |
| Knowledge retrieval | Stale embeddings, hallucinated facts, wrong document version | Data engineering |
| Math / Reasoning | Incorrect calculations, logic errors, multi-step reasoning failures | Domain experts |
| Format / Schema | Malformed outputs, missing required fields, invalid JSON | Engineering |
| Safety / Policy | Content policy violations, harmful responses | Compliance |

**Per-category ownership and maintenance cycles:** Each category has a named owner responsible for:
- Triaging new cases from the production failure flywheel
- Ensuring golden answers are authored or reviewed by humans
- Archiving obsolete cases when features are deprecated
- Reviewing category health quarterly (coverage gaps, stale cases, false-positive rate)

**Partitioned execution plans:** Not every test case runs on every commit. The dataset is partitioned by execution plan:

| Execution plan | Trigger | Dataset subset |
|---|---|---|
| Stratified CI | Every PR | Stratified sample across all categories (e.g., 10% per category) |
| Category CI | PRs touching a specific domain | Full category suite for affected categories |
| Full merge suite | Merge to main | All non-archived cases across all categories |
| Scheduled regression | Nightly / weekly | Full suite including deep/expensive cases |

This partitioning keeps eval economically sustainable: fast feedback on PRs via stratified sampling, complete coverage on merge, and deep coverage on schedule.

### Dataset Lifecycle

```
Production Incident
    │
    ├──→ Capture interaction, trace, tool results
    ├──→ Apply privacy filters and retention rules
    ├──→ Classify into category (security, tool calls, knowledge retrieval...)
    ├──→ Assign owner
    ├──→ Author golden answer (human-reviewed, not model-generated)
    ├──→ Deduplicate against existing cases
    ├──→ Add to dataset (never deleted, only archived)
    ├──→ Backfill baseline (prove the case catches the failure)
    └──→ Link to incident, PR, or root cause analysis
```

The dataset starts with an initial ~200 golden answer pairs (real production queries + human-authored correct responses) and grows with every incident. After 6 months of operation, a healthy dataset should contain 500-1000+ cases, each traceable to its originating incident.

### Data Governance

- **Privacy filters:** Production-derived fixtures must have PII redacted and sensitive data anonymized before entering the dataset.
- **Retention policy:** Cases are permanent (archived, not deleted). Archived cases are excluded from CI but available for historical analysis.
- **Golden answer authorship:** Golden answers must be authored or reviewed by humans to avoid training the eval against model-generated hallucinations. LLMs may assist in drafting but a human must approve.
- **Coverage metadata:** Each case carries metadata about what failure class it covers, which query category it belongs to, when it was added, and what incident created it.

## Implementation in this repo

### What already exists

The repo has the individual building blocks of a living eval dataset distributed across multiple canonical docs. The pieces exist but are not composed into a single named entity:

- **production-failure-regression-flywheel** (`docs/canonical/production-failure-regression-flywheel.md:28`) defines converting production failures into durable regression cases with a 9-step process (intake, capture, privacy, labeling, deduplication, tier assignment, backfill, incident linking, pruning) and an 8-category failure taxonomy. This covers the lifecycle mechanics.
- **production-grounded-eval-sampling** (`docs/canonical/production-grounded-eval-sampling.md:28`) defines the data pipeline: capture, privacy filters, retention policy, sampling criteria, coverage metadata, expected-behavior labeling, replay infrastructure, and refresh cadence. This covers the data engineering.
- **repeatable-agent-spot-check-set** (`docs/canonical/repeatable-agent-spot-check-set.md`) provides a seed of repeatable cases — the initial bootstrap for the living dataset.
- **eval-tier-stratification** (`docs/canonical/eval-tier-stratification.md:28`) provides the fast/medium/deep tier model that supports partitioned execution (stratified CI subset vs. full merge suite).
- **The flywheel daemon** (systemd timer, 60s loop processing `~/.reflection/qi-pending/`) with anomaly detection (anomaly_score ≥ 80 triggers QI loop) provides the operational infrastructure for automated failure-to-eval conversion.
- **The QI loop** (review-work → recommendation-writer → writing-plans → implement → re-verify) provides the correction mechanism that fixes failures after they are detected.

### What is missing

The explicit "living eval dataset" concept as a single named artifact with monotonic growth guarantee, per-category ownership, and partitioned execution plans is not formalized:

1. **Monotonic growth is not named as a guarantee.** The flywheel docs say "every production failure should become a durable regression case" but do not state the monotonic property (never shrinks, only archives) as an invariant of the dataset.

2. **No per-category ownership model.** The failure taxonomy exists (8 categories) but ownership assignment per category is not documented. Who maintains the security category? Who triages new tool-call cases? The ownership model is missing.

3. **Partitioned execution is distributed across docs.** The concept of stratified CI subset vs. full merge suite exists implicitly in eval-tier-stratification but is not named as an explicit execution plan of the living dataset.

4. **No single named "living eval dataset" entity.** The repo has the flywheel (how cases enter), the sampling doc (how data is captured), the spot-check set (initial seed), and tier stratification (how cases are scheduled). But "the living eval dataset" as a composed, named artifact with all its properties in one place is NOT_FOUND.

Add:

1. A named "Living Eval Dataset" entity (this doc) that composes the existing building blocks.
2. A per-category ownership model with named owners and maintenance cycles.
3. Explicit monotonic growth guarantee: cases are permanent, archived when obsolete, never deleted.
4. Named partitioned execution plans: stratified CI, category CI, full merge, scheduled regression.
5. A dataset health dashboard tracking total cases, growth rate, category coverage, archive ratio.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Every incident leaves a permanent scar in the test suite — that scar prevents the same failure from happening twice | Unchecked growth without maintenance leads to an uncategorized monolith that is expensive to run |
| Monotonic growth means the system gets strictly safer over time; each failure invests in future quality | Requires a human or automated process to convert each incident into a well-formed test case — raw incident logs are not test cases |
| Categorization and ownership prevent the dataset from becoming an unmanageable monolith | Golden answers must be authored or reviewed by humans to avoid training the eval against model-generated hallucinations |
| Cost-controlled execution (stratified CI subset vs. full suite on merge) keeps eval economically sustainable | The dataset must be actively groomed; test cases for deprecated features must be archived (not deleted, for traceability) |
| Traceable lineage from every test case back to the incident or feature that created it | Adding a case requires capture, privacy, labeling, deduplication, backfill — the intake pipeline is non-trivial |

## Relationship to Other Patterns

- **Implemented by:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] — the intake mechanism that converts incidents into dataset cases.
- **Data foundation from:** [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] — the capture, privacy, labeling, and replay pipeline.
- **Seeded by:** [[docs/canonical/repeatable-agent-spot-check-set|Repeatable Agent Spot-Check Set]] — the initial bootstrap of repeatable cases.
- **Scheduled by:** [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]] — the tier model that enables partitioned execution.
- **Evaluated by:** [[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]] — the three evaluation layers that consume the dataset.
- **Enforced by:** [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] — the gate that requires eval dataset results on PRs.
- **Validated by:** [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] — ensuring eval scores correlate with production outcomes.
- **Generalizes:** [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]] from late-session context failures to all production failure classes.

## References

- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-patterns.md:77` — original pattern definition (Bhaumik).
- `docs/analysis/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc/2026-06-26-the-production-ai-playbook-deploying-agents-at-enterprise-sc-classification.yaml:82` — Partial Coverage classification with evidence.
- `docs/canonical/production-failure-regression-flywheel.md:28` — failure-to-regression conversion with 9-step process.
- `docs/canonical/production-grounded-eval-sampling.md:28` — capture, privacy, labeling, replay pipeline.
- `docs/canonical/repeatable-agent-spot-check-set.md` — seed set of repeatable cases.
- `docs/canonical/eval-tier-stratification.md:28` — fast/medium/deep tier model.
- `docs/canonical/production-failure-regression-flywheel.md:71` — failure intake process and taxonomy.
- `docs/canonical/eval-tier-stratification.md:36` — tier-based partitioned execution.

---

*Created: 2026-06-26 | From: Production AI Playbook classification | Precedence: canonical*
