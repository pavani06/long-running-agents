---
title: "Classification Batch 2: GTM AI Agents — Lessons from Deploying to 6,000 Users (Patterns 9-13)"
type: analysis
tags: [agentes-orquestracao, evals, production, harness-engineering, knowledge-management]
date: 2026-08-30
aliases: ["gtm ai agents classification batch 2", "gtm agents 6000 users classification batch 2"]
relates-to:
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-mental-model|Mental Model]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|Patterns]]"
  - "[[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-analysis|Knowledge Extraction]]"
  - "[[docs/canonical/pain-signal-eval-progression-gate|Pain-Signal Eval Progression Gate]]"
  - "[[docs/canonical/eval-investment-parity|Eval-Investment Parity]]"
  - "[[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]]"
  - "[[docs/canonical/3-layer-evaluation-architecture|3-Layer Evaluation Architecture]]"
  - "[[docs/canonical/production-contact-training-loop|Production-Contact Training Loop]]"
  - "[[docs/system-of-record|System of Record]]"
sources:
  - "docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns.yaml"
---

# Classification Batch 2: GTM AI Agents — Lessons from Deploying to 6,000 Users

Scope: evidence-based classification of patterns 9-13 from [[docs/analysis/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users/2026-08-30-gtm-ai-agents-lessons-from-deploying-to-6000-users-patterns|the extracted patterns]] against the `long-running-agents` repository. Batch 2 of 2. Precedence order per [[docs/system-of-record|System of Record]]: `docs/decisions/` > `docs/canonical/` > `docs/evidence/` > `docs/analysis/` > `curriculum/` > READMEs. All searches executed 2026-08-30.

## 1. Pull-Based Infrastructure on Pain

**Classification: Partial Coverage**

The core investment philosophy (build capability only when observed pain pulls it) exists at canonical depth, but scoped to eval capability and harness governance, not to the full infrastructure stack. `pain-signal-eval-progression-gate.md:28` states the exact pull principle ("Treat eval maturity as a gate driven by pain signals instead of a calendar roadmap") and `:36` adds the smallest-sufficient mandate ("Approve only the smallest eval capability that addresses the observed pain"), with the trigger mapping table and decision record at `:40-51`. The measured harness lifecycle applies the same evidence-gated logic to harness components (`measured-harness-evolution-lifecycle.md:29`, ROI threshold and quarterly cadence at `:52-62`), and `symphony-trap-awareness.md:27` names the push-based failure mode the source pattern warns against (demanding upfront "a precision that usually exists only after the system has run"), with the build-then-distill inversion at `:33`. `eval-investment-parity.md:58` even reconciles the two regimes (pain-signal gating for *which* capability, parity for aggregate allocation).

What is missing: the generalization from evals/harness to the whole infrastructure stack (CI/CD for instructions, skills, progressive disclosure, memory, interfaces beyond chat) and the launch-strategy sequencing (minimal viable launch stack, then reactive hardening in the order constraints bind). The repo's canonical depth covers the decision gate for one asset class, not the launch-minimal strategy with its explicit re-architecture-tax trade-off. NOT_FOUND for a minimal-launch-stack or reactive-hardening-sequence pattern: searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `docs/analysis/`, `curriculum/`, and `.opencode/skills/` for `pull-based`, `on pain`, `minimal launch`, `reactive hardening` (2026-08-30); matches outside the source package were scoped to eval/harness as cited above.

**Evidence:**
- `docs/canonical/pain-signal-eval-progression-gate.md:28` — pull principle: eval maturity gated by pain signals, not calendar roadmap.
- `docs/canonical/pain-signal-eval-progression-gate.md:36` — "Approve only the smallest eval capability that addresses the observed pain".
- `docs/canonical/pain-signal-eval-progression-gate.md:40-51` — pain-signal-to-minimum-capability trigger table plus decision record.
- `docs/canonical/eval-investment-parity.md:58` — stated reconciliation: pain-signal gating governs which capability to build next.
- `docs/canonical/measured-harness-evolution-lifecycle.md:29` — harness as measured lifecycle, not one-time architecture; `:52-62` — ROI threshold, quarterly cadence, One In One Out.
- `docs/canonical/symphony-trap-awareness.md:27` — anti-upfront-spec stance (push-based failure mode named); `:33` — build then distill.
- `docs/system-of-record.md:198` — Pain-Signal Eval Progression Gate as active canonical (Level 2 precedence).
- NOT_FOUND — full-stack pull-based infrastructure pattern and minimal-launch sequencing (locations searched listed above).

**Integration value: Medium** — mostly a generalization of an existing repo philosophy from evals to all infrastructure; the new surface is the launch-strategy framing and the explicit pairing with the re-architecture tax, a natural fit for [[curriculum/05-core-concepts/06-harness-evolution|Harness Evolution]] and KODA N4.

## 2. Continuous Re-Architecture Budget

**Classification: Partial Coverage**

Standing capacity-allocation rules exist, but for a different track, and the repo's documented answer to technology churn is to *avoid* rewrites rather than budget for them. `eval-investment-parity.md:43-53` defines a structurally analogous standing budget: an explicit, accepted sprint allocation (agents 50% / evals 50% across time, tokens, money) sustained every sprint, with `:56` naming the acceptance of halved builder capacity as an explicit decision. Re-architecture governance exists as cadence: `measured-harness-evolution-lifecycle.md:60` (quarterly cycle plus One In One Out) and `garbage-collection-day-meta-loop.md:48`, `:54` (weekly, non-negotiable, time-boxed re-investment protected from feature pressure). Deferred rework is tracked by `deferred-ledger-agentic-work.md` and `carry-debt-sunset-gate.md` (indexed at `docs/system-of-record.md:230`, `:234`). On churn absorption specifically, the repo canonized the Kavak alternative: `model-agnostic-agent-vm-harness.md:36-37` (harness must absorb smarter models arriving monthly without rewrites) and `:79` ("the fleet swaps by config change, not by rewrite").

What is missing: the feature-vs-re-architecture portfolio split itself (60-70/30-40), the technology-wave watchlist, and the PRD/core-design drift audit with the 80%-persistence claim. NOT_FOUND by direct search: `60-70`, `30-40`, `portfolio split`, `wave watchlist`, `watchlist`, `PRD drift`, `drift audit` across `docs/`, `curriculum/`, `.opencode/`, and READMEs returned matches only inside this source package (2026-08-30).

**Evidence:**
- `docs/canonical/eval-investment-parity.md:43-53` — standing parity allocation as explicit accepted sprint budget (analogous standing-allocation rule, different target track).
- `docs/canonical/eval-investment-parity.md:56` — halved builder capacity accepted as an explicit decision.
- `docs/canonical/measured-harness-evolution-lifecycle.md:60` — quarterly review cycle and One In One Out rule governing harness re-architecture.
- `docs/canonical/garbage-collection-day-meta-loop.md:48` — weekly GC Day working session; `:54` — cadence non-negotiable under feature pressure, time-boxed.
- `docs/canonical/model-agnostic-agent-vm-harness.md:36-37` — design constraint: absorb model waves without rewrites; `:79` — fleet swaps by config change, not rewrite.
- `docs/system-of-record.md:230`, `:234` — Deferred-Ledger Agentic Work and Carry-Debt Sunset Gate as active canonicals for deferred rework.
- NOT_FOUND — 60-70/30-40 split, technology-wave watchlist, PRD-drift audit (searched `docs/`, `curriculum/`, `.opencode/`, READMEs; only the source package matches).

**Integration value: Medium** — names a budget discipline the repo lacks for the mechanics-churn track (skills, MCP, progressive disclosure); complements parity (which covers the eval track) and would give the KODA harness-improvements curriculum a portfolio-level allocation rule.

## 3. LLM-Classified Log Taxonomy

**Classification: Partial Coverage**

The classification mechanics exist as canonical, but every existing instrument classifies agent behavior or failures; the reframe (production question logs as a demand-side instrument) is absent. Layer 2 of `3-layer-evaluation-architecture.md:45` runs LLM-as-Judge with rubric dimensions (`:82`), and `failure-pattern-classification-loop.md:31-33` defines an observe-classify-build-verify loop with a 6-class root cause taxonomy (`:54-63`), both LLM- or rubric-driven classification at production scale. The detection surface exists: `eval-dashboard-primary-detection-surface.md:50` and `:77` surface pain signals and anomalies in near-real time. Production log harvesting exists for eval grounding (`production-contact-training-loop.md:64-66`, citing production-grounded sampling and the monotonically growing dataset), and `semantic-topic-bucketing.md` (indexed at `docs/system-of-record.md:191`) does semantic topic grouping, but for context retention, not logs. The `analyze-and-improve` skill (`docs/system-of-record.md:46`) is a working LLM classification pipeline over source content, proving the tooling.

What is missing: classification of user *questions* into a hierarchical topic taxonomy (category, subcategory, example questions), the feature-gap radar over unanswered or poorly answered demand concentrations, and the cost-engineering constraint at scale. All existing consumers classify what the agent did wrong, not what users ask for. NOT_FOUND: `log taxonomy`, `question log`, `battle card`, and demand-side taxonomy searches across `docs/canonical/`, `docs/analysis/`, `curriculum/`, and `.opencode/` returned matches only inside this source package (2026-08-30).

**Evidence:**
- `docs/canonical/3-layer-evaluation-architecture.md:45` — Layer 2 Semantic/LLM-as-Judge defined; `:82` — LLM-as-Judge with rubric as the quality-surface mechanism.
- `docs/canonical/failure-pattern-classification-loop.md:31-33` — observe-classify-build-verify classification loop; `:54-63` — root cause taxonomy with class-to-surface mapping.
- `docs/canonical/eval-dashboard-primary-detection-surface.md:50` — dashboard makes pain signals visible; `:77` — anomaly alerts calibrated per layer.
- `docs/canonical/production-contact-training-loop.md:64-66` — harvesting real production interactions into the growing corpus (data source precedent).
- `docs/system-of-record.md:191` — semantic-topic-bucketing (topic grouping for context retention; different object).
- `docs/system-of-record.md:46` — analyze-and-improve skill: LLM extraction/classification pipeline with model tiering (tooling precedent).
- NOT_FOUND — hierarchical demand taxonomy over user question logs and feature-gap radar (locations searched listed above).

**Integration value: High** — fills a genuine hole: the repo has no demand-side analytics instrument. It would supply evidence to the pain-signal gate (which currently relies on complaint heuristics, `pain-signal-eval-progression-gate.md:44`), feed production-grounded eval sampling with demand-shaped cases, and give the KODA GTM curriculum a measurable coverage roadmap input.

## 4. Gap-to-Content Feedback Circuit

**Classification: Partial Coverage**

Several gap-to-improvement feedback circuits exist as canonical, but the update artifacts are eval cases, policies, or backlog items, never generated knowledge content. `on-policy-rollout-feedback-loop.md:41` feeds scored production prefixes back as update targets (prompt rules, skills, eval cases, memory policy), and `production-contact-training-loop.md:37` closes the expose-harvest-update-redeploy loop (daily cadence at `:39-54`), while explicitly listing its own missing pieces at `:69-75`. `confidence-gated-continual-learning.md:32` is the closest structural analog: a four-stage detect-suggest-review-deploy loop for knowledge fixes with confidence gating. `production-failure-regression-flywheel.md:28` converts failures into durable regression content, and `qa-to-backlog-feedback-loop.md:30-44` converts findings into backlog issues (its own partial gap declared at `:57-59`). The `analyze-and-improve` skill (`docs/system-of-record.md:46`) is a working gap-to-content circuit for the repository's own knowledge base.

What is missing: the demand-side trigger (emerging or unanswered topics from classified logs, pattern 3 upstream), the content-generation step (battle cards and enablement docs auto-generated from internal sources), the feed-back channel into the agent's knowledge, and gap-closure confirmation in subsequent logs. NOT_FOUND: `battle card`, `enablement`, `gap-to-content`, `feedback circuit` across `docs/`, `curriculum/`, and `.opencode/` matched only this source package (2026-08-30).

**Evidence:**
- `docs/canonical/on-policy-rollout-feedback-loop.md:41` — scored prefixes fed back as update targets (prompt rules, skills, eval cases, memory policy).
- `docs/canonical/production-contact-training-loop.md:37` — expose, harvest, feed back as updates, redeploy, repeat; `:39-54` — the assembled daily loop; `:69-75` — declared missing pieces.
- `docs/canonical/confidence-gated-continual-learning.md:32` — four-stage detect-suggest-review-deploy loop, confidence-gated (closest structural analog).
- `docs/canonical/production-failure-regression-flywheel.md:28` — production failures become durable eval regression cases.
- `docs/canonical/qa-to-backlog-feedback-loop.md:30-44` — capture, triage, convert, return-to-board; `:57-59` — structured-conversion gap declared.
- `docs/system-of-record.md:46` — analyze-and-improve: automated knowledge-to-content pipeline for the repo itself.
- NOT_FOUND — enablement-content generation fed back as agent knowledge and closure confirmation (locations searched listed above).

**Integration value: Medium** — the repo's loops already close gaps with eval cases and policy updates; the delta is the generated-content artifact and the demand-side trigger. Directly applicable to KODA N4 (sales knowledge gaps becoming generated agent knowledge).

## 5. Agent Value Maturity Ladder

**Classification: Missing**

NOT_FOUND in any form (doc, code, or curriculum): agent-product value stages, a switching-cost or lock-in ladder, habituation or wow-collapse signals, and a staged capability roadmap as adoption strategy. Searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `docs/analysis/`, `curriculum/`, `.opencode/`, and READMEs for `maturity ladder`, `value ladder`, `value stage`, `switching cost`, `four-stage`, `hyper-personaliz`, `wow`, `habitua` (2026-08-30). All matches are either inside this source package or in different domains: `energy-value-chain-spread-analysis.md:90` discusses switching costs in energy-market analysis, and `confidence-gated-continual-learning.md:32` has a four-stage repair loop (not value stages).

Nearest non-equivalent coverage, all progressions of *other objects*: `autonomy-curriculum-sampling.md:41` and `:60` (observe-assist-own ladder for agent autonomy with readiness gates), `measured-harness-evolution-lifecycle.md:29` (BUILD-STABILIZE-SIMPLIFY-REMOVE for harness components), the 4-level learner curriculum (`curriculum/README.md:192-247`, cited as adjacent-in-spirit at `autonomy-curriculum-sampling.md:72`), and the eval maturity phases analysis (`docs/system-of-record.md:351-359`). None models user-perceived value stages of an agent product or the lock-in economics between them. The dimension is genuinely uncovered even though the audience would receive it: `README.md:34` targets business people building agent systems.

**Evidence:**
- NOT_FOUND — value-stage model, switching-cost ladder, habituation listener, staged capability roadmap; searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `docs/analysis/`, `curriculum/`, `.opencode/`, READMEs (greps listed above; only source-package or cross-domain matches).
- `docs/canonical/autonomy-curriculum-sampling.md:41`, `:60` — nearest ladder, wrong object (agent autonomy phases, not product value stages).
- `docs/canonical/measured-harness-evolution-lifecycle.md:29` — component lifecycle progression (different object).
- `docs/system-of-record.md:351-359` — eval maturity phases analysis (maturity of evals, not agent product value).
- `README.md:34` — audience (business people) confirms the GTM/value dimension has a home but no content.

**Integration value: Medium** — opens the product-value and adoption dimension the repo does not treat; natural fit as a KODA N4 roadmap concept (staged value delivery for the WhatsApp sales agent) and as the strategic counterpoint to the reliability-centric curriculum.

## Summary

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Pull-Based Infrastructure on Pain | Partial Coverage | Medium |
| 2 | Continuous Re-Architecture Budget | Partial Coverage | Medium |
| 3 | LLM-Classified Log Taxonomy | Partial Coverage | High |
| 4 | Gap-to-Content Feedback Circuit | Partial Coverage | Medium |
| 5 | Agent Value Maturity Ladder | Missing | Medium |
