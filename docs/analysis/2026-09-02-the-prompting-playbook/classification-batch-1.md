---
title: "Classification Batch 1: The Prompting Playbook (Patterns 1-6)"
type: classification
tags: ["agentes-orquestracao", "evals", "context-engineering", "harness-engineering", "production"]
date: 2026-09-02
aliases: ["prompting playbook classification batch 1", "classificacao prompting playbook padroes 1-6"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]", "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-mental-model|Mental Model: The Prompting Playbook]]", "[[docs/canonical/model-switching-architecture-enterprise-eval-gate|Model-Switching Architecture Enterprise Eval Gate]]", "[[docs/canonical/living-eval-dataset|Living Eval Dataset]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/prompt-as-code-causal-change-management|Prompt-as-Code Causal Change Management]]", "[[docs/canonical/invariant-compensation-split|Invariant-Compensation Split]]"]
sources: ["[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|The Prompting Playbook Patterns]]"]
---

# Classification Batch 1: Patterns 1-6 vs. long-running-agents

Precedence order applied per `docs/system-of-record.md:14-21`: decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs. Every classification cites file:line from the repo; `Missing` confirms NOT_FOUND with the locations searched.

---

## 1. Eval-Gated Model Migration Diagnostic

**Classification: Partial Coverage**

**Justification:** The migration-gate half of the pattern exists at canonical depth: an eval suite run before and after migration, per-case pass/fail comparison, and a structured migration decision. What is missing is the diagnostic core: the per-failure classification into behavior difference (remediable by prompt/harness tuning) versus capability gap (no amount of prompting fixes it), and the violation-count metric that gives directional signal when pass/fail has not moved. The existing gate decides Switch/Hold/Hybrid at the portfolio level but never answers, per failing case, whether prompting is even the right lever.

**Evidence:**
- `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:43-59` — side-by-side comparison: candidate vs. current model against the enterprise eval dataset, with per-category breakdown, "Regression cases: specific test cases where candidate performs worse than current" (:57), and cost comparison (:59).
- `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:61-71` — Switch/Hold/Hybrid decision framework driven by the comparison data (the regression-test signal for the migration decision).
- `docs/canonical/model-switch-driven-eval-hardening.md:40` — "Switch as regression detection": the existing eval suite runs on the new provider's outputs; pass/fail compared against the previous provider.
- `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:24` — the canonical itself declares that the concrete switching infrastructure "does not exist" in the repo (documented design, not implementation).
- NOT_FOUND (behavior-vs-capability diagnosis): grep `capability gap` across `docs/` returns only this analysis's own files and `docs/canonical/invariant-compensation-split.md:49` (a diagram label for the compensation branch, not a migration diagnostic).
- NOT_FOUND (violation-count metric): grep `violation count|violations per|per-rule violation|count-based` in `docs/canonical/` returns no matches.

**Integration value: Medium** — the eval-gate machinery is documented at depth; integration is the per-failure diagnostic step (fixable vs. capability deficit) plus count-based directional signal inside the existing comparison report.

---

## 2. Control/Edge/Boundary Eval Taxonomy

**Classification: Partial Coverage**

**Justification:** Two of the three case classes have canonical analogues. The edge class (past failures locked as permanent tests, encoding institutional memory) is deeply covered by the living eval dataset and the production failure regression flywheel. The control class (unambiguous must-pass baseline) maps onto the workflow-derived golden question set with its registered baseline score. Missing are the boundary class — eval cases testing whether the agent knows when to hand off to a human or refuse, i.e. calibration of its own competence edge — and the taxonomy itself as a case classification with class-specific regression semantics (control regression = breakage; boundary regression = calibration loss). The repo's existing eval stratifications classify by mechanism type, speed/trigger, or determinism × deployment, never by case class.

**Evidence:**
- `docs/canonical/living-eval-dataset.md:28` — "every production incident, every escaped edge case, every new feature specification becomes a permanent addition" (edge class: past failures as permanent tests).
- `docs/canonical/production-failure-regression-flywheel.md:32` — failure intake explicitly accepts an "escaped edge case" and converts it into a durable regression case.
- `docs/canonical/workflow-derived-golden-question-set.md:44-47` — golden questions authored from the real workflow, first-run accuracy registered as baseline, launch gated by score (control-case analogue).
- `docs/canonical/eval-coverage-matrix.md:66-68` — confirms every existing stratification is single-axis: mechanism type (`docs/canonical/3-layer-evaluation-architecture.md:28`), speed/trigger (`docs/canonical/eval-tier-stratification.md:32-36`).
- NOT_FOUND (case-class taxonomy and boundary-calibration evals): grep `control case|edge case|boundary case|capability boundary|knows when to (refuse|hand off|escalate)|self-knowledge of its limits` in `docs/canonical/` returns 26 hits in 15 files, all incidental uses of "edge case" (e.g. `docs/canonical/pain-signal-eval-progression-gate.md:48`); none define a control/edge/boundary case taxonomy or test handoff/refusal calibration as an eval class.

**Integration value: Medium** — the edge half is covered at depth; the boundary class and class-specific regression semantics would add a fourth (case-class) axis complementing the three existing eval lenses.

---

## 3. Structural Prompt Hygiene

**Classification: Partial Coverage**

**Justification:** Functional separation of prompt concerns exists: the stable harness prompt canonical enumerates role, policy, tool contracts, safety boundaries, response format, and evaluation behavior as distinct blocks with per-block policy, and prompt-as-code supplies the versioning and ownership discipline. Missing are the hygiene mechanics proper: XML-tagged sectioning of a legacy mixed-concern prompt (role/guidelines/policy/tone/data), redundancy and false-identity/pasted-copy removal, the human-readability rule of thumb ("if a human cannot tell guidelines from policy from data, the model cannot either"), and the measured-uplift-before-targeted-fixes result.

**Evidence:**
- `docs/canonical/stable-harness-prompt.md:22` — enumerates "role, policy, tool contracts, safety boundaries, response format, or evaluation behavior" as distinct harness-prompt concerns.
- `docs/canonical/stable-harness-prompt.md:30-39` — context builder assembles each call from distinct blocks with a per-block reduction policy (structural block separation, aimed at preservation during context reduction rather than hygiene refactoring).
- `docs/canonical/prompt-as-code-causal-change-management.md:116` — the concrete surface hygiene would apply to: "system prompt is hand-authored (1800+ lines). Not versioned or eval'd as a separate component" (gap recorded via `docs/canonical/owned-agent-control-loop.md:102`).
- NOT_FOUND (hygiene mechanics): repo-wide grep `XML tag|tagged section|tone of voice|prompt hygiene|structural prompt` matches only this analysis's own files (`2026-09-02-the-prompting-playbook-*`); no canonical, curriculum, or skill doc covers tagged sectioning or prompt-refactoring hygiene.

**Integration value: Medium** — directly applicable to the acknowledged 1800-line hand-authored prompt gap; a cheap practice with a curriculum-ready rule of thumb and a measured-uplift story.

---

## 4. Defensive Patch Ledger

**Classification: Partial Coverage**

**Justification:** Both halves of the pattern exist, in separate active canonicals. The rationale-at-write-time ledger exists as prompt-as-code causal change management: every prompt change must record trigger, diagnosis, and intent, with rollback and an audit trail mapping each change to the failure that justified it. The model-era decay logic exists as the invariant-compensation split: compensations that only made sense for an older model become cost surface, and the "record the rationale" rule makes removal governable. Missing is the defensive-patch frame that couples them: patches written for previous-model failures that newer, more instruction-following models overfit, and the operational rule that model migration triggers a patch audit (not merely an eval re-run).

**Evidence:**
- `docs/canonical/prompt-as-code-causal-change-management.md:32-59` — the three mandatory commit questions: causal trigger (incident/eval regression), diagnostic context, predictive intent (which failure the change addresses).
- `docs/canonical/prompt-as-code-causal-change-management.md:80-85` — rollback infrastructure: git-based prompt versioning, deploy-by-commit, rollback audit trail.
- `docs/canonical/prompt-as-code-causal-change-management.md:98-105` — cumulative audit trail answering "for any prompt change: why was it made? What failure triggered it?".
- `docs/canonical/invariant-compensation-split.md:23` — the model-generation decay case: a Context Loader kept after a newer model no longer needed it, still costing 450ms and 1200 tokens per turn.
- `docs/canonical/invariant-compensation-split.md:64-70` — core rules, including "Record the rationale: If future maintainers cannot tell why it exists, governance has failed" (:70).
- NOT_FOUND (defensive-patch frame and migration-triggered audit): grep `defensive|patch audit|patches` in `docs/canonical/` returns 10 hits in 7 files — closest is `docs/canonical/measured-harness-evolution-lifecycle.md:44` ("BUILD is defensive because a new model's production limits are still unknown"), which concerns building defensively, not auditing accumulated patches at migration; no doc links a patch ledger to model migration as trigger.

**Integration value: High** — the coupling (migration triggers patch audit; patches deprecate across model generations) operationalizes two mature canonicals into one migration procedure, load-bearing for the repo's model-agnostic thesis.

---

## 5. Two-Sided Trade-off Instruction

**Classification: Missing**

**Justification:** Not present in any form. The repo's escalation coverage is architectural (degradation ladders, help APIs, routing gates), never instructional: no document teaches stating both the cost and the counter-cost of an action (escalate, refund, hand off) in the prompt so the model exercises per-case judgment, and no document addresses single-objective overfit such as under-escalation caused by stating only one side.

**Evidence (NOT_FOUND with locations searched):**
- NOT_FOUND: repo-wide grep `cost of escalat|counter-cost|cost of not escalat|stating both sides|balanced instruction` matches only this analysis's own files (`2026-09-02-the-prompting-playbook-*`).
- NOT_FOUND: grep `trade-off|tradeoff|both sides|under-escalat|over-optimiz` in `docs/canonical/` (30 hits in 23 files) — all architectural or design-level tradeoffs (e.g. `docs/canonical/task-routed-model-tiering.md:40`, quality/cost routing tradeoff); none concern prompt instruction design.
- Non-equivalent adjacents searched and rejected: `docs/canonical/tested-degradation-ladder.md:29` (escalation as a runtime failure rung, not instruction economics); `docs/canonical/closed-loop-help-api.md:30-32` (terminal-escalation loop closure); `docs/canonical/human-afk-task-routing-gate.md:37` (routing judgment to humans by task type).

**Integration value: Medium** — a compact instruction-design principle with direct curriculum fit (Level 2 prompt/rubric design; Level 4 KODA escalation journeys); no infrastructure dependency.

---

## 6. Capability Escalation Ladder

**Classification: Missing**

**Justification:** Not present in any form. The repo holds each lever separately — model tiering for cost routing, decomposition as an architecture choice, harness evolution ROI discipline — but has no ordered escalation procedure for a failing task (capability, then reasoning budget, then instruction, then architecture) with cost/latency compared across passing routes, and no economic-winner analysis. The two existing repo "ladders" are different patterns: the tested degradation ladder orders runtime failure handling (retry, fallback, human escalation), and the agent-value maturity ladder is an organizational maturity model.

**Evidence (NOT_FOUND with locations searched):**
- NOT_FOUND: grep `bigger model|larger model|model upsiz|escalation ladder|reasoning budget|adaptive thinking` in `docs/canonical/` returns 2 hits, both cross-references to the runtime degradation ladder (`docs/canonical/multi-agent-fault-tolerance.md:110`, `docs/canonical/multi-provider-model-routing.md:85`).
- Non-equivalent adjacents searched and rejected: `docs/canonical/tested-degradation-ladder.md:29` (runtime failure ladder: classify, retry, safe fallback, human escalation — not capability investment ordering); `docs/canonical/task-routed-model-tiering.md:32` (per-subtask tier routing for cost/latency of working tasks, not escalation for failing ones); `docs/canonical/model-switching-architecture-enterprise-eval-gate.md:61-71` (migration gate between candidate models, not intra-task lever ordering); `docs/canonical/invariant-compensation-split.md:23` (measuring obsolete compensations, not choosing between capability levers).

**Integration value: High** — supplies the measured decision procedure for the repo's central harness-over-model thesis (per the Phase-0 mental model, `2026-09-02-the-prompting-playbook-mental-model.md:23`): in the source case the decomposition rung won on economics, which is precisely the harness-over-model argument the curriculum teaches; it unifies tiering, prompt, and decomposition canonicals under one escalation protocol.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Eval-Gated Model Migration Diagnostic | Partial Coverage | Medium |
| 2 | Control/Edge/Boundary Eval Taxonomy | Partial Coverage | Medium |
| 3 | Structural Prompt Hygiene | Partial Coverage | Medium |
| 4 | Defensive Patch Ledger | Partial Coverage | High |
| 5 | Two-Sided Trade-off Instruction | Missing | Medium |
| 6 | Capability Escalation Ladder | Missing | High |
