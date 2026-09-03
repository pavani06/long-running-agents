---
title: "Classification Batch 2: The Prompting Playbook (Patterns 7-12)"
type: classification
tags: ["agentes-orquestracao", "harness-engineering", "evals", "context-engineering", "production"]
date: 2026-09-02
aliases: ["prompting playbook classification batch 2", "prompting playbook classification 7-12", "grader split classification", "generate evaluate repair classification"]
last_updated: 2026-09-02
relates-to:
  - "[[docs/system-of-record|System of Record]]"
  - "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns|Agentic Patterns from The Prompting Playbook]]"
  - "[[docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-mental-model|Mental Model: The Prompting Playbook]]"
sources:
  - "docs/analysis/2026-09-02-the-prompting-playbook/2026-09-02-the-prompting-playbook-patterns.md"
---

# Classification Batch 2: Patterns 7-12 vs. long-running-agents

Precedence order applied per `docs/system-of-record.md:14-21`: decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs. Every classification cites file:line from the repo; `Missing` confirms NOT_FOUND with the locations searched. Pattern names are used exactly as they appear in `2026-09-02-the-prompting-playbook-patterns.md` (sections 7-12).

---

## 7. Hard/Soft Constraint Grader Split

**Classification: Partial Coverage**

**Justification:** The core partition — deterministic programmatic checks for binary rules, LLM judge for fuzzy preferences — exists at canonical depth, generalized by evaluation-mechanism type: the 3-Layer Evaluation Architecture separates Layer 1 Deterministic (regex/schema/PII, zero LLM cost, blocks deployment/response) from Layer 2 Semantic/LLM-as-Judge (groundedness, safety, relevance), and Constraint-Anchored Evaluation defines the binary verification matrix `constraint -> check -> pass/fail -> violation detail`. The curriculum's Evaluation Rubrics teaches hard rules as veto inside the Evaluator and, in its anti-pattern corrections, already prescribes the split direction of the source ("implementar verificação programática de hard rules, não depender só do LLM"). Missing are three mechanics: (1) the constraint-partitioning guidance itself — which constraint goes to which grader — is a gap the repo self-acknowledges at `constraint-anchored-evaluation.md:77`; (2) multi-trial violation-count reporting (counts per hard rule per trial as directional signal when pass/fail does not move) exists as a concept only in a different axis (magnitude-direction splits internal confidence vs external verdict, not deterministic checker vs LLM judge); (3) soft constraints as runtime-tunable evaluator prompt content without backend deploys is absent everywhere outside this source package.

**Evidence:**
- `docs/canonical/3-layer-evaluation-architecture.md:30-43` — Layer 1 Deterministic: regex, schema validation, NER PII detection, zero LLM cost, blocks deployment/response delivery.
- `docs/canonical/3-layer-evaluation-architecture.md:45-59` — Layer 2 Semantic/LLM-as-Judge for groundedness, safety, relevance, faithfulness, completeness.
- `docs/canonical/constraint-anchored-evaluation.md:31-33` — verification matrix with one row per constraint, binary pass/fail, violation detail; aggregate verdict approved only if all rows pass.
- `docs/canonical/constraint-anchored-evaluation.md:77` — self-acknowledged gap: "No guidance on constraint granularity, such as what deserves a hard constraint versus what should remain reviewer judgment".
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:2176` — anti-pattern correction: "Implementar verificacao programatica de hard rules (nao depender so do LLM)".
- `curriculum/05-core-concepts/08-evaluation-rubrics.md:705` — hard rules as veto: "Transformar a falha em veto, não em peso"; `:1232` — "hard rules PRIMEIRO. Sempre" na Decision Policy.
- `docs/canonical/magnitude-direction-verifier-split.md:100` — adjacent split ("trust but verify" as architectural split), but its axis is internal-confidence vs external-verifier, not deterministic checker vs LLM judge.
- NOT_FOUND: violation counts per rule per trial as an eval reporting convention, and runtime-injected soft constraints — searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/` (grep `violation count`, `soft constraint`, `runtime.*inject`; matches only inside this package's own analysis/patterns files).

**Integration value: Medium** — The partition question is real and open in the repo (self-acknowledged at `constraint-anchored-evaluation.md:77`); count-based directional reporting would compose with magnitude-direction-verifier-split and eval-tier-stratification, and runtime-tunable soft constraints would extend the rubric/evaluator teaching.

---

## 8. Two-Layer Output Contract

**Classification: Partial Coverage**

**Justification:** Harness-side format enforcement is covered at canonical depth and taught from Nivel 1: structured outputs as the agent's exit contract with kernel validation at typed event boundaries; the generation + validation circuit (output schema, generation prompt, post-generation validator, repair/rejection, audit); Zod tool-input schemas; the N1 structured-output exercise teaching it as one of the 5 basic harness patterns; and the harness-evolution table listing Format Validator / Output Parser / Schema Enforcer as the enforcement components. The general principle behind the pattern — move the guarantee from prompt text into structure — is codified in structural-guarantee-over-compliance ("the rule lives in the gate, not the memory"). Stop sequences even appear in the curriculum's generator config. Missing: (1) the explicit two-layer pairing — the same format defined at prompt level (XML tags) and enforced at harness level (stop sequence detecting the closing tag; structured outputs for nested JSON) as one contract; (2) the right-sizing rule — conversational outputs carry a light contract, structured outputs with machine consumers carry heavy enforcement; (3) stop sequence as format boundary — the curriculum's `stop_sequences` are content delimiters for cost/bloat control ("Controla custo e evita responses bloated"), not closing-tag contract enforcement.

**Evidence:**
- `docs/canonical/typed-event-boundaries.md:42` — structured outputs as contrato de saída; kernel validates the event at publish and consume.
- `docs/canonical/typed-event-boundaries.md:44` — "A fronteira rejeita, não corrige" — enforcement, not correction.
- `docs/canonical/structured-generation-constraint-validation-circuit.md:29` — one action-safety circuit: output schema, generation prompt, domain constraint set, post-generation validator, repair/rejection policy, audit log.
- `docs/canonical/deterministic-tool-dispatch.md:24` — "The model emits JSON (a structured output)"; `:107` — "Built on: Pattern 1 (Structured Output Contract)".
- `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md:37-39` — "The repo treats structured output as a foundational assumption"; N1 exercise teaches it as one of the 5 basic harness patterns.
- `curriculum/01-nivel-1-fundamentals/exercises/exercise-02-structured-output.md:5` — N1 exercise (aliases: "structured output", "validação JSON", "exercício schema").
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:737-748` — `stop_sequences` in generator_config, justified as cost/bloat control, not format-contract boundary.
- `docs/canonical/structural-guarantee-over-compliance.md:46-47` — move the guarantee from compliance to structure; `:69-71` — "the rule lives in the gate, not the memory" (gate/schema, not prompt recall).
- `curriculum/03-nivel-3-advanced-architecture/05-harness-evolution.md:947` — "Structured Output nativo | Format Validator, Output Parser, Schema Enforcer" as harness components.
- NOT_FOUND: conversational-vs-structured contract sizing and stop-sequence-as-closing-tag detection — searched `docs/canonical/`, `docs/decisions/`, `curriculum/` (grep `stop sequence`, `stop_sequences`: the two matches above are the only occurrences outside this package).

**Integration value: Medium** — The heavy layer is mature; the missing deltas (prompt-layer/harness-layer pairing of one format contract, the sizing rule by output type, stop-sequence mechanics) are a focused addition to the structured-output teaching surface in N1/N2 and to typed-event-boundaries' motivation section.

---

## 9. Tool Integration Triad

**Classification: Partial Coverage**

**Justification:** Two of the three integration points exist at canonical depth plus implementation: the tool schema leg (every tool is a `DynamicStructuredTool` with Zod schema input and typed return, 20+ tools in mhc-backend) and the deterministic implementation leg (dispatch is a switch statement testable with JSON fixtures without an LLM; the KODA reference architecture ships calculator tools such as `calculator_tool.py` and `price_calculator.py`). The behavioral risk the pattern flags ("wrong time to call") is covered by eval machinery — Behavioral Eval Path Analysis RF3 validates tool dispatch against per-category permitted/prohibited tool templates. The prompt leg exists only as "tool contracts" inside the stable harness prompt, not as a mandatory per-tool when-to-use instruction. Missing: the triad formalization itself — instruction + schema + deterministic implementation as three required integration points that fail individually — and the motivating reframe "instructions don't add capability"; the repo's reframe covers a different axis ("tools are not magical; tools are JSON + deterministic code" demystifies dispatch, not the capability gap that makes exhortation useless).

**Evidence:**
- `docs/canonical/deterministic-tool-dispatch.md:22-27` — the 4-step dispatch reality: model emits JSON, app code reads, switch/router dispatches, deterministic handler executes.
- `docs/canonical/deterministic-tool-dispatch.md:31-35` — reframe: "Tools are not magical. Tools are JSON + deterministic code" (dispatch mechanics, not capability-vs-instruction).
- `docs/canonical/deterministic-tool-dispatch.md:74` — "Every tool is a `DynamicStructuredTool` with Zod schema input and typed return" (schema leg + implementation leg).
- `docs/canonical/deterministic-tool-dispatch.md:61-63` — testability: JSON fixtures, no LLM needed (deterministic implementation leg).
- `curriculum/07-implementation-guides/01-setup-guide.md:115` — `calculator_tool.py # Cálculos (preço, desconto)`; `:1475` — `price_calculator.py # Cálculo de preços + descontos` (deterministic calculation tools in the KODA reference stack).
- `curriculum/04-nivel-3-engenharia-avancada/exercises/exercise-behavioral-eval-path-analysis.md:449` — RF3 Tool Dispatch Validation: permitted/prohibited tools per query category (the wrong-time-to-call eval coverage); `:481` — "ferramenta proibida para a categoria, ou excesso de chamadas".
- `docs/canonical/invariant-compensation-split.md:87` — Stable Harness Prompt protects "role, policy, tool contracts, safety boundaries, response format" (prompt leg exists as generic tool contracts, not as per-tool when-to-use instruction).
- NOT_FOUND: the three-leg triad with the prompt instruction as mandatory leg and the principle "instructions don't add capability" — searched `docs/canonical/`, `docs/decisions/`, `curriculum/`, `.opencode/skills/` (grep `tool schema`, `when to use`, `instructions don't add`, `instrução.*ferramenta`; no doc formalizes the triad).

**Integration value: Low** — The substance is mature (canonical pattern, implemented stack, eval coverage of misuse); the delta is one framing: a sidebar in the Sprint Contracts / Deterministic Tool Dispatch teaching stating all three legs are required and why instruction-only fixes fail.

---

## 10. Generate-Evaluate-Repair Loop

**Classification: Partial Coverage**

**Justification:** The loop exists at canonical and curriculum depth: Generator-Evaluator formalizes generate → evaluate → reject-with-feedback → regenerate; the N2 lesson operationalizes it with structured feedback carrying `fix_instruction` ("Exatamente o que o Generator precisa fazer") and bounded `max_iterations` with `escalate_to_human`; the N3 KODA orchestration pseudocode literally calls `generator_agent.repair_recommendation(draft, evaluation)` — repair targeted by the evaluation; Structured Generation Constraint Validation Circuit composes generation + validation + repair/rejection + audit as one contract; rubrics require cited evidence per evaluation. Missing: (1) the three-prompt decomposition framing — generator, evaluator, and an independent repairer as three simple maintainable prompts instead of one mega-prompt (the repo's repair is the Generator repairing its own draft under feedback — same capability, different decomposition); (2) the economics comparison that motivates the loop — passed all cases with fewer tokens and lower latency than the bigger-model and bigger-output-limit routes (the repo's token economics doc covers inference-vs-specification cost, a different trade-off); (3) soft constraints injected into the evaluator prompt at runtime (same NOT_FOUND as pattern 7).

**Evidence:**
- `docs/canonical/generator-evaluator.md:31` — two agents; Evaluator returns approve/reject verdict with specific feedback.
- `docs/canonical/generator-evaluator.md:70-72` — rejected output "volta para GENERATOR com feedback"; `:116` — "Rejection loops add latency if Generator needs multiple revisions".
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:752-767` — mandatory feedback structure: `severity`, `issue_code`, `issue_text`, `affected_item`, `fix_instruction` (targeted fixes from violations).
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:712-722` — `max_iterations: 3`, `action_if_max: "escalate_to_human"` (bounded loop).
- `curriculum/03-nivel-3-advanced-architecture/koda-applications/nivel-3-koda.md:383-396` — `create_recommendation` → `evaluator_agent.check` → `generator_agent.repair_recommendation(draft, evaluation)` (repair step in orchestration pseudocode).
- `docs/canonical/structured-generation-constraint-validation-circuit.md:29` — generation, validation, repair or rejection, risk flags, dispatch, audit as one path.
- `docs/canonical/constraint-anchored-evaluation.md:33` — violation detail per constraint row (evidence of every violation); `curriculum/05-core-concepts/08-evaluation-rubrics.md:1218` — trace records "evidence citada, hard rule aplicada".
- `docs/canonical/tested-degradation-ladder.md:42` — "Retry with repair" rung (failure-recovery ladder; adjacent, different loop).
- NOT_FOUND: loop-vs-model-upsizing/output-limit economics comparison and runtime-injected evaluator soft constraints — searched `docs/canonical/`, `curriculum/`, `docs/analysis/` (nearest: `token-economics-gap-filling` per `docs/system-of-record.md:255` is inference-vs-specification cost, a different trade-off).

**Integration value: Medium** — The loop itself is mature; the sharpest missing delta is the economics argument (decomposition beats upsizing on tokens/latency), which composes with harness-evolution, task-routed-model-tiering and the escalation-ladder material, plus the independent-repairer variant as a maintainability option.

---

## 11. Ban-to-Source-of-Truth Rebalancing

**Classification: Partial Coverage**

**Justification:** The decay mechanism that makes old-model bans dangerous is canonical: Invariant-Compensation Split documents that compensations written for a past model's weakness become drag when models improve (separate domain risk from model weakness before removing), and Prompt-as-Code Causal Change Management records trigger/diagnosis/intent for every defensive prompt change — exactly the audit that lets a team judge which bans are still load-bearing (the pattern itself declares this dependency on the patch ledger). Adjacent source-of-truth designation exists for data (KODA mitigation: add a `source_of_truth` field to every output field) and for state (single source of truth in State Persistence). Missing is the rebalancing move itself: replacing a prohibition instruction with a balanced designation of the in-context data as the accurate source of truth, and its reframe — information withholding as the inverse failure of hallucination, both fixed by designating the source of truth instead of prohibiting output. No doc, code, or curriculum material treats prompt ban lists as a class to be rebalanced against in-context data.

**Evidence:**
- `docs/canonical/prompt-as-code-causal-change-management.md:30-59` — the three mandatory causal questions (why changed / what failure caused it / what failure it addresses) for every prompt change — the rationale ledger that makes stale-ban audits possible.
- `docs/canonical/invariant-compensation-split.md:23` — compensation written for a 32K model still costing latency/tokens after the newer model no longer needs it (the decay mechanism).
- `docs/canonical/invariant-compensation-split.md:67` — decision test: "Separate domain risk from model weakness — if the failure still exists with a better model, it is an invariant candidate".
- `curriculum/06-knowledge-graphs/02-koda-feature-dependencies.md:1373` — failure mitigation: "Adicionar `source_of_truth` em cada campo do output" (data-provenance use of source of truth, not instruction design).
- `curriculum/05-core-concepts/02-planning-execution-separation.md:366` — interface crítica as "single source of truth" (different object: phase contract, not in-context customer data vs ban).
- NOT_FOUND: ban-list replacement with in-context source-of-truth designation, and the withholding-as-inverse-hallucination framing — searched `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, `.opencode/` (grep `ban`, `proibi`, `withhold`, `source of truth`, `source_of_truth`, `grandfather`, `allowance`: every match is a governance/state-provenance sense, a policy prohibition inside rubrics (e.g. `curriculum/08-tools-templates/evaluation-rubric-template.md:991`), or this package's own analysis/patterns files).

**Integration value: Medium** — The move is the missing "how to neutralize a stale patch" complement to prompt-as-code's audit (which records why, but not how to rewrite); it slots into the prompt-as-code / invariant-compensation canonical family and into KODA prompt-design curriculum as a one-page design rule.

---

## 12. Self-Check Reasoning Instruction

**Classification: Better Implementation**

**Justification:** The repo solves the same problem — a capable-enough model submitting unverified work — with a more mature architectural answer, and explicitly teaches against relying on self-checks: the curriculum checklist item "Generator cria SEM se auto-verificar" and the Generator-Evaluator trade-off "Separation of concerns: Generator doesn't need to self-police" externalize verification to an impartial Evaluator, grounded in the quantified finding that self-evaluation detects ~3% of real errors versus ~14% external (an ~11pp silent gap). Plan-Execute-Verify adds the explicit Verify phase with success gates; Structural Guarantee over Compliance codifies the meta-rule that knowing does not prevent violating ("I know this" did not prevent anything — move the rule into structure). The source's own escalation ladder terminates at the same endpoint: the self-check instruction lifted the weak model only from 0/5 to 2/5, and the winning route was the generate-evaluate-repair decomposition, which the repo already holds at canonical depth. The residual deltas — the instruction rung as a cheap pre-architecture lever, and the dictum that truncation under enriched reasoning is a budget failure, not a quality failure — are small: the budget-failure class is already covered by the token-budget response/safety-buffer machinery.

**Evidence:**
- `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:1992` — checklist: "Entendo que Generator cria SEM se auto-verificar?" (self-check deliberately out of the Generator's job).
- `docs/canonical/generator-evaluator.md:115` — trade-off: "Separation of concerns: Generator doesn't need to self-police".
- `docs/canonical/generator-evaluator.md:23-27` — confirmation bias of self-evaluation; ~3% self vs ~14% external detection, ~11pp silent gap.
- `docs/canonical/plan-execute-verify.md:29-31` — Plan/Execute/Verify decomposition; `:68-72` — Verify phase validates all steps against success gates ("All planned success criteria pass or the failed step is returned for re-execution").
- `docs/canonical/structural-guarantee-over-compliance.md:23-27` — "Knowing a rule does not prevent violating it" (field observation: assertion-without-verification despite the rule being known); `:46-47` — move the guarantee from compliance to structure.
- `curriculum/01-nivel-1-fundamentals/02-token-budgeting.md:445-451` (cited via `docs/canonical/hybrid-context-stack.md:75`) — response and safety reserve before prompt assembly (the output-limit budget machinery that treats truncation as budget failure).
- `docs/canonical/generator-evaluator.md:116` — "Rejection loops add latency if Generator needs multiple revisions" (the loop endpoint the source converges to).

**Integration value: Low** — The repo already teaches the endpoint of this lever's escalation path; only the interim-lever framing (prompt-only lift before architecture exists) and the truncation-vs-quality diagnostic dictum are new, each a one-paragraph curriculum note.

---

## Summary

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 7 | Hard/Soft Constraint Grader Split | Partial Coverage | Medium |
| 8 | Two-Layer Output Contract | Partial Coverage | Medium |
| 9 | Tool Integration Triad | Partial Coverage | Low |
| 10 | Generate-Evaluate-Repair Loop | Partial Coverage | Medium |
| 11 | Ban-to-Source-of-Truth Rebalancing | Partial Coverage | Medium |
| 12 | Self-Check Reasoning Instruction | Better Implementation | Low |
