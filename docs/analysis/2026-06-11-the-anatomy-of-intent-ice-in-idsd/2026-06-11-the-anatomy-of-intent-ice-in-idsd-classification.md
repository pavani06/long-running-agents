---
title: "Comparative Classification: The Anatomy of Intent Patterns vs. long-running-agents Repo"
type: analysis
tags: ["agentes-orquestracao", "harness-engineering", "spec-driven-development", "evals", "decision-discipline", "context-engineering", "curriculo-conteudo"]
date: 2026-06-11
aliases: ["anatomy intent ice classification", "ICE anatomy classification", "intent ice pattern classification", "classificacao anatomia intent ice"]
last_updated: 2026-06-14
relates-to: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-mental-model|Anatomy of Intent Mental Model]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-12-idsd-method/2026-06-12-idsd-method-classification|IDSD Method Classification]]", "[[docs/canonical/ice-craft-separation|ICE Craft Separation]]", "[[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]", "[[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]", "[[docs/canonical/generator-evaluator|Generator-Evaluator]]", "[[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/system-of-record|System of Record]]"]
sources: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-patterns|Anatomy of Intent Patterns]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-mental-model|Anatomy of Intent Mental Model]]"]
---
<!-- OMO_INTERNAL_INITIATOR -->

# Comparative Classification: The Anatomy of Intent Patterns vs. long-running-agents Repo

**Date:** 2026-06-11
**Repo analyzed:** `pavani06/long-running-agents`
**Patterns source:** "The Anatomy of Intent - ICE in IDSD" analysis (2026-06-11), 9 extracted agentic patterns
**Evidence basis:** `docs/canonical/`, `.opencode/skills/`, `.opencode/agents/`, `curriculum/`, `docs/system-of-record.md`, `AGENTS.md`
**Precedence order:** decisions/ > canonical/ > evidence/ > analysis/ > curriculum/ > READMEs

## Classification Legend

| Class | Meaning |
|---|---|
| Already Exists | Pattern is documented, implemented, or taught with equivalent depth |
| Partial Coverage | Elements exist but missing key mechanics, reframe, or formalization |
| Missing | Not present in any form (doc, code, or curriculum) |
| Better Implementation | Repo has a superior or more mature version of the same idea |

---

## 1. ICE Ownership Boundary

**Pattern:** Explicit ownership map for each artifact -- intent, context, expectations, builder output, and validation -- to prevent artifacts from leaking into each other.

**Classification:** Already Exists

**Integration value:** Low

**Why:**
The repo formalized ICE Craft Separation as a canonical doc that defines explicit ownership for each craft: "The separation of owners is the central architectural point: the human owns Intent and Expectations and never abandons them; the harness owns Context and the execution Loop and is never invited to invent what the human wanted" ([[docs/canonical/ice-craft-separation|ICE Craft Separation]]:31). The doc provides a formal ownership table assigning each craft to a specific owner ([[docs/canonical/ice-craft-separation|ICE Craft Separation]]:53-58). The Ownership-of-No pattern further provides a refusal role design that complements craft ownership ([[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]:29-51).

**What exists:**

- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:53-58 -- explicit ownership table mapping Intent to Outcome owner, Context to Harness, Expectations to Outcome owner, and Loop execution to Harness.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:31 -- "The separation of owners is the central architectural point."
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:39-43 -- Context owned by harness with progressive disclosure policy, not dumped by the human.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:62 -- gap list mechanism that makes boundaries visible when crafts are separated.
- [[docs/canonical/owner-of-no-role-design|Owner-of-No Role Design]]:29-51 -- explicit ownership role with refusal authority, complementing the craft ownership model.
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:43-48 -- ownership rule: the same person who wrote the Intent writes the Expectations.

**What is missing from the pattern:**
The repo already defines ownership boundaries with equivalent or greater depth than the pattern. The ownership map is formalized in the ICE Craft Separation table. The pattern describes a generalized ownership boundary; the repo implements it with named crafts, a formal table, and operational skills that enforce it.

---

## 2. Three-Part Intent Contract

**Pattern:** Intent artifact with exactly three slots -- goal, constraints, and failure conditions -- separating what guides generation from what should be checked after output exists.

**Classification:** Partial Coverage

**Integration value:** Medium

**Why:**
The repo formalizes intent as a five-part primitive (description, constraints, failure scenarios, success scenarios, connections) rather than a three-part contract. The core elements overlap: the repo's description maps to goal, constraints maps to constraints, and failure scenarios maps to failure conditions. However, the repo deliberately chose a five-field decomposition that adds success scenarios and connections fields, treating them as equally first-class rather than routing them out of intent. The three-part contract is a simpler model that the five-part primitive subsumes but does not exactly match.

**What exists:**

- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- five-field intent schema with description, constraints, failure scenarios, success scenarios, and connections.
- [[.opencode/skills/intent-five-part-primitive/SKILL.md|intent-five-part-primitive skill]]:19-23 -- operational skill enforcing the five-field completeness gate.
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:43-48 -- completeness gate mechanics blocking agent execution when fields are missing.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:35 -- the five-part structure ensures completeness: "any missing field is a visible gap, not an invisible delegation to the agent."

**What is missing from the pattern:**
The three-slot contract (goal, constraints, failure conditions) as a named decomposition. The repo chose five fields instead of three. The five-part primitive includes the three fields but adds success scenarios (which the pattern routes to Expectations) and connections (which the pattern does not address). The structural difference is that the repo treats success scenarios as an intent field, while the three-part contract treats them as external to intent.

**Searched locations for "three-part intent contract" / "three slots":**
- `docs/canonical/` -- 57 canonical docs searched; `three-part`, `three-slot`, `three-field intent` returned NOT_FOUND except in the five-part primitive which uses five fields.
- `docs/canonical/intent-five-part-primitive.md` -- defines five fields; no three-slot variant exists.
- `.opencode/skills/` -- intent-five-part-primitive skill uses five fields; no three-part variant.

---

## 3. Two-Implementations Goal Test

**Pattern:** Heuristic to distinguish goals from specifications in disguise. Review question: "Can two substantially different implementations both satisfy this?" If yes, it is a goal. If no, it is a specification masked as a goal.

**Classification:** Missing

**Integration value:** Medium

**Why:**
No canonical doc, curriculum lesson, skill, or agent defines a "two-implementations test" or any equivalent heuristic for distinguishing goals from implementation specifications. The repo has extensive material on intent composition and has the vertical-slice-issue-generation pattern that generates observable behavior, but no lightweight pre-flight test that asks whether two different implementations could satisfy the same statement. The concept is present only in the source analysis being classified, not in the target repository.

**Searched locations (NOT_FOUND):**
- `docs/canonical/` -- 57 docs searched for `two-implementation`, `alternative implementation`, `different implementation`, `goal.*test`, `spec.*disguise`, `implementation.*satisfy`. All returned NOT_FOUND.
- `docs/canonical/vertical-slice-issue-generation.md` -- generates issues with observable behavior but does not apply a two-implementations test to distinguish goals from specs.
- `.opencode/skills/` -- no skill performs this classification test. intent-five-part-primitive checks completeness but does not distinguish goal-vs-spec statements.
- `curriculum/` -- 35+ lessons searched; no training example or exercise teaches the two-implementations test.
- `docs/analysis/` -- the heuristic appears only in the source analysis `2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis.md:174`, not in any prior repo analysis.

**What exists nearby:**
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 decomposes intent into structured fields but does not include a goal-vs-spec classification test.
- [[docs/canonical/grill-me-alignment-interview|Grill-Me Alignment Interview]]:28-46 captures decisions through structured interview questions, but none probe whether the statement is a goal or a specification.
- [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]]: generates issues as observable behavior but does not validate goal-vs-spec purity.

**Integration opportunity:**
This would be a lightweight addition -- a single review question that could live as a skill trigger or a review gate in the intent-five-part-primitive workflow. It pairs naturally with the Goal Atomicity Split and could be taught as a curriculum drill in Level 2 or 3.

---

## 4. Goal Atomicity Split

**Pattern:** One goal equals one sentence, no "and." Split into multiple goals when conjunction appears. Prevents multi-goal intents from hiding coordination complexity.

**Classification:** Missing

**Integration value:** Medium

**Why:**
The repo has no rule, heuristic, or gate that enforces goal atomicity through conjunction scanning. No canonical doc, skill, or curriculum lesson teaches "if the goal needs 'and', it's two goals." The repo decomposes work through vertical-slice-issue-generation and plan-execute-verify, but the specific discipline of splitting on conjunctions in goal statements is not present. The concept appears in the source analysis (`2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis.md:136`) but not in any repo artifact.

**Searched locations (NOT_FOUND):**
- `docs/canonical/` -- 57 docs searched for `goal atomic`, `one goal one sentence`, `split.*goal`, `conjunction.*goal`, `no.*and.*goal`. All returned NOT_FOUND.
- `docs/canonical/vertical-slice-issue-generation.md` -- decomposes work into vertical slices but does not use conjunction-based splitting of goal statements.
- `docs/canonical/plan-execute-verify.md` -- separates work into phases but does not split goals by conjunction.
- `.opencode/skills/` -- issue-start and orchestrator skills split work into issues but do not use a conjunction-scanning atomicity rule.
- `curriculum/` -- no lesson teaches goal atomicity by conjunction splitting.

**What exists nearby:**
- [[docs/canonical/vertical-slice-issue-generation|Vertical Slice Issue Generation]] -- generates single-purpose vertical slices with observable behavior. Conceptually adjacent to atomic goals but uses a different decomposition method (cross-layer behavior) rather than conjunction splitting.
- `.opencode/skills/refine-issue/SKILL` -- decomposes issues into sub-issues with dependencies. Structurally adjacent to goal splitting but uses issue decomposition logic, not goal-language heuristics.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-60 -- separates work into three explicit phases. Adjacent to work decomposition but at the plan phase level, not the goal atomicity level.

**Integration opportunity:**
A lightweight pre-flight rule that could be added to the intent-five-part-primitive skill or the Grill-Me alignment interview. Complements the Two-Implementations Goal Test and Constraint Budget Gate as a trio of intent-quality heuristics.

---

## 5. Constraint Budget Gate

**Pattern:** Hard limit of five to seven directional, unconditional constraints in business language. Constraints that choose tools, name patterns, or describe implementation become context; checks that measure output become failure conditions. Prevents constraint lists from growing into hidden implementation specs.

**Classification:** Missing

**Integration value:** Medium

**Why:**
The repo's Constraint-Anchored Evaluation pattern anchors evaluation on explicit, verifiable constraint lists but does not impose a numeric budget or a classification gate on those constraints. The canonical doc explicitly notes constraint list growth as a cost: "Constraint list can grow large, adding evaluation latency" ([[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:89). The repo treats this as a risk to manage, not as a hard gate. No mechanism limits constraints to 5-7, filters out implementation-level constraints, or routes them to Context/Expectations instead.

**Searched locations (NOT_FOUND):**
- `docs/canonical/` -- 57 docs searched for `constraint budget`, `constraint limit`, `5 constraint`, `7 constraint`, `directional constraint`, `unconditional constraint`. All returned NOT_FOUND.
- `docs/canonical/constraint-anchored-evaluation.md`:29-56 -- defines constraint-verification mechanics but imposes no budget or classification gate on which items qualify as constraints.
- `docs/canonical/intent-five-part-primitive.md`:33-41 -- the constraints field of the five-part intent has no numeric limit or business-language filter.
- `.opencode/skills/` -- no skill applies a constraint budget gate before execution.
- `curriculum/` -- no exercise teaches constraint budgeting as a discipline.

**What exists nearby:**
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 -- anchors evaluation on explicit constraints with verification matrix. Provides the evaluation mechanics but no constraint budget or classification gate.
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- includes constraints as an intent field but imposes no limit or business-language gate.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:62 -- gap list mechanism surfaces gaps between crafts, which could surface overgrown constraint lists, but does not gate them at a numeric budget.

**Integration opportunity:**
A concrete review gate that pairs naturally with the Constraint-Failure Decision Rule. Could be added as a skill that runs against candidate intent constraints before the agent receives them. The 5-7 budget is a heuristic that would need calibration per domain -- the source analysis acknowledges this is not proof but a practical discipline.

---

## 6. Constraint-Failure Decision Rule

**Pattern:** Classification heuristic: "Would knowing this change how the builder writes code?" If yes, it is a constraint (builder-facing guidance). If no -- it can only be checked after output exists -- it is a failure condition (validator-facing check). Prevents teams from mixing builder guidance with validator checks.

**Classification:** Missing

**Integration value:** Medium

**Why:**
No canonical doc, skill, or curriculum lesson provides a decision rule for classifying requirements as constraints versus failure conditions. The repo has both constraints (in the five-part intent and constraint-anchored evaluation) and failure conditions (in the expectations boundary and five-part intent as failure scenarios), but no heuristic tells an intent author or reviewer how to decide which category a statement belongs to. The classification is left to author judgment without a formal rule.

**Searched locations (NOT_FOUND):**
- `docs/canonical/` -- 57 docs searched for `constraint.*failure decision`, `would knowing this change`, `builder guidance.*validator`, `constraint or failure condition`, `what changes how the builder`. All returned NOT_FOUND.
- `docs/canonical/intent-five-part-primitive.md`:33-41 -- lists constraints and failure scenarios as separate fields but provides no decision rule for classifying an item into one field or the other.
- `docs/canonical/human-owned-expectations-boundary.md`:35-41 -- defines failed scenarios as an expectations field but does not define the boundary between constraints (intent) and failure conditions (expectations).
- `.opencode/skills/` -- intent-five-part-primitive skill checks field completeness but does not classify items into constraint vs. failure condition using a decision rule.
- `curriculum/` -- sprint contracts separate scope from success criteria and failure handling, but use a contract negotiation frame, not a constraint-vs-failure heuristic.

**What exists nearby:**
- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:33-41 -- defines constraints and failure scenarios as separate intent fields. The structure implies they are different, but no rule explains how to decide which is which.
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:35-41 -- defines failed scenarios and limits as expectations fields. Adjacent to failure conditions but does not define the constraint/failure boundary.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:77-83 -- the Generator builds, the Evaluator checks. The architecture implies different information surfaces, but no rule classifies what goes on which surface.

**Integration opportunity:**
A single decision question that could be embedded in the intent-five-part-primitive skill as a classification gate during intent authoring or review. Complements the Constraint Budget Gate and Compartmented Evaluation Architecture.

---

## 7. Compartmented Evaluation Architecture

**Pattern:** Builder receives goal and constraints only; validator receives failure conditions (potentially encrypted or hidden). Information surfaces are sealed so the builder cannot reward-hack visible tests or scenarios. Provides a structural defense against the agent optimizing for checks instead of outcomes.

**Classification:** Partial Coverage

**Integration value:** High

**Why:**
The repo's Generator-Evaluator architecture structurally separates the Generator (builder) from the Evaluator (validator). The Generator receives conversation context and produces output; the Evaluator receives persisted client state, rubrics, and constraints to validate ([[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-85). The ICE Craft Separation further separates crafts with explicit owners ([[docs/canonical/ice-craft-separation|ICE Craft Separation]]:53-58). However, the repo does not explicitly formalize "sealed information surfaces" -- there is no mechanism that prevents the Generator from accessing the Evaluator's rubrics, no concept of "encrypted evals," and no audit trail of which information each participant could see. The repo has the architectural separation but not the formal compartmentation with explicit information boundaries and leakage prevention.

**What exists:**

- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:31-85 -- separates Generator from Evaluator with distinct information contexts. Generator receives conversation context and produces candidate output; Evaluator receives persisted client state, rubrics, and constraints.
- [[docs/canonical/generator-evaluator|Generator-Evaluator]]:77-83 -- dimension table showing Generator and Evaluator have different primary responsibilities, context needs, model characteristics, success outputs, and failure modes.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:53-58 -- ownership table separating Intent (human), Context (harness), Expectations (human), and Loop execution (harness).
- [[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:29-56 -- the Evaluator's verification matrix checks output against explicit constraints, providing independent validation mechanics.
- [[docs/canonical/plan-execute-verify|Plan-Execute-Verify]]:31-60 -- separates planning from execution from verification, with explicit phase boundaries.

**What is missing from the pattern:**
1. Formal "sealed information surfaces" as an architectural property. The Generator-Evaluator separation is documented, but the docs do not frame it as compartmentation that prevents information leakage.
2. "Encrypted evals" or hidden failure conditions -- the pattern proposes that failure conditions are compiled into evals that the builder cannot see. The repo has no equivalent mechanic.
3. Audit trail of information visibility -- no mechanism records which information each participant in the Generator-Evaluator loop could see.
4. Leakage prevention -- no explicit rule or mechanism prevents a human from copying failure conditions into the builder prompt.
5. The structural defense against reward-hacking as a named concept. The repo's architecture creates the separation but does not name "reward-hacking prevention" as the design intent behind it.

**Searched locations for "compartmented" / "sealed" / "information surface":**
- `docs/canonical/` -- searched for `compartment`, `sealed`, `information surface`, `hidden eval`, `reward hack`, `builder cannot`. These terms are NOT_FOUND outside the source analysis.
- `docs/canonical/generator-evaluator.md` -- separates information contexts implicitly but does not name them as sealed compartments.

---

## 8. Scenario Destination Split

**Pattern:** Failure scenarios become binary failure conditions in Intent; success scenarios move to Expectations (generated from intent plus context, with a human checkpoint). Prevents scenarios from serving conflicting roles as both builder guidance and validator checks.

**Classification:** Partial Coverage

**Integration value:** Medium

**Why:**
The repo's five-part intent includes both failure scenarios and success scenarios as fields of the Intent artifact ([[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:39-40). The Human-Owned Expectations Boundary also includes done scenarios and failed scenarios as fields of the Expectations artifact ([[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:36-37). Both artifacts cover both types of scenarios, creating an intentional overlap rather than a destination split. The repo does not formalize a routing rule that sends failure scenarios exclusively to Intent and success scenarios exclusively to Expectations. The scenarios exist in both locations, with the Expectations artifact adding additional fields (limits, non-goals, outcome owner).

**What exists:**

- [[docs/canonical/intent-five-part-primitive|Intent as Five-Part Primitive]]:39-40 -- failure scenarios and success scenarios are both fields of the five-part intent.
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:36-37 -- done scenarios (success) and failed scenarios (failure) are both fields of the Expectations artifact.
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:35 -- the Intent includes "failure scenarios, success scenarios" as fields. The Expectations include "scenarios, limits, non-goals" (line 47).
- [[docs/canonical/human-owned-expectations-boundary|Human-Owned Expectations Boundary]]:110 -- acknowledges the overlap: "The five-part intent's success/failure scenarios overlap with Expectations, but Expectations add the ownership rule, limits, non-goals, and escalation conditions."

**What is missing from the pattern:**
1. An explicit routing rule: "failure scenarios belong to Intent as binary failure conditions; success scenarios belong to Expectations as done scenarios." The repo has both in both places.
2. The human checkpoint for generated expectations -- the Expectations artifact is authored by the outcome owner, not generated from intent+context with a human checkpoint. The pattern proposes expectations-as-generated-artifact; the repo treats them as directly authored.
3. The specific naming "scenario destination split" and the framing of the problem as scenarios serving conflicting roles.

**Searched locations for "scenario destination split" / "scenario routing":**
- `docs/canonical/` -- searched for `scenario destination`, `scenario split`, `scenario routing`, `binary.*failure condition`. These terms are NOT_FOUND outside the source analysis.

---

## 9. Harness-Owned Context Assembly

**Pattern:** Stable context packet assembled by infrastructure rather than the intent author. Humans write only the outcome, constraints, and failure conditions; the harness assembles stack details, architectural conventions, team practices, and prior-work metadata into a reusable context packet. Prevents copy-paste drift and stale context.

**Classification:** Already Exists

**Integration value:** Low

**Why:**
The repo has extensive, mature harness-owned context assembly infrastructure formalized across multiple canonical docs. The Application-Owned Agent Control Plane explicitly states "Context is constructed, not appended" and owns prompt construction and context building as application code ([[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:70-71). The ICE Craft Separation assigns Context ownership to the harness: "The harness constructs Context from its inventory (docs, architecture decisions, state, tool results, constraints). The agent never decides what context it needs -- it receives context from the harness at the right time for the right step" ([[docs/canonical/ice-craft-separation|ICE Craft Separation]]:43). The repo's context infrastructure exceeds what the pattern describes -- it includes resolver-based progressive disclosure, a layered hybrid context stack, addressable memory catalogs, budget-ledgered assembly, and stable harness prompt preservation.

**What exists:**

- [[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]:70-71 -- "Context is constructed, not appended. Build each model call from approved state, history, memory, tool results, and business facts, choosing every token deliberately."
- [[docs/canonical/ice-craft-separation|ICE Craft Separation]]:39-43 -- Context owned by the harness: "The harness owns Context selection, freshness, and disclosure policy."
- [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]]:28-53 -- five-part resolver model (thin base context, capability directory, positive triggers, negative triggers, trigger evals) for progressive context delivery.
- [[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:28-42 -- layered context assembly with explicit budget ordering across prompt, memory, durable state, summaries, latest result, and recoverable handles.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:26-41 -- preserves invariant harness instructions separately from reducible context payload.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-53 -- catalogs omitted context with id, location, preview, scope, and fetch for recovery.
- [[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:29-62 -- per-call ledger separating fixed harness cost from reducible context cost.
- [[docs/canonical/external-state-persistence|External State Persistence]]:29-57 -- durable state outside the context window.
- [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:26-41 -- preserves head (goal, constraints) and tail (current state) while keeping middle recoverable.
- [[curriculum/GLOSSARY|Glossary]]:110-113 -- defines "Context Progressive Disclosure" as a curriculum concept, taught and not just documented.
- [[.opencode/skills/issue-start/SKILL.md|issue-start]]:16-23 -- demonstrates load-on-demand skill triggers in production, implementing progressive context disclosure in the agent lifecycle.

**What is missing from the pattern:**
The repo already implements context assembly at greater depth and maturity than the pattern describes. The repo's resolver-based model adds trigger contracts, evals, deduplication, and a layered context stack that handles both disclosure and reduction -- elements not present in the pattern's "harness assembles context" description. The repo also teaches this in the curriculum (Context Management core concept, Level 1 token budgeting) and implements it in operational skills.

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | ICE Ownership Boundary | Already Exists | Low |
| 2 | Three-Part Intent Contract | Partial Coverage | Medium |
| 3 | Two-Implementations Goal Test | Missing | Medium |
| 4 | Goal Atomicity Split | Missing | Medium |
| 5 | Constraint Budget Gate | Missing | Medium |
| 6 | Constraint-Failure Decision Rule | Missing | Medium |
| 7 | Compartmented Evaluation Architecture | Partial Coverage | High |
| 8 | Scenario Destination Split | Partial Coverage | Medium |
| 9 | Harness-Owned Context Assembly | Already Exists | Low |

**Totals:** Already Exists: 2, Partial Coverage: 3, Missing: 4, Better Implementation: 0

**Highest integration priorities:** Compartmented Evaluation Architecture (High). This pattern adds the "sealed information surfaces" concept to the existing Generator-Evaluator separation, providing a structural defense against reward-hacking that the repo's current architecture implies but does not explicitly enforce.

**Repo strengths in this classification:** Harness-Owned Context Assembly and ICE Ownership Boundary are mature, well-documented patterns in the repo. The repo's context engineering infrastructure (resolver-based progressive disclosure, hybrid context stack, addressable memory catalog, stable harness prompt, token budget ledger) exceeds the pattern's description of harness-owned context assembly. The ICE Craft Separation canonical doc provides explicit ownership boundaries with a formal table, gap list mechanism, and the method-vs-harness distinction.

**Patterns with the most integration opportunity:** The four Missing patterns (Two-Implementations Goal Test, Goal Atomicity Split, Constraint Budget Gate, Constraint-Failure Decision Rule) are lightweight heuristics and decision rules that could be added as review gates or skill triggers within existing workflows. They complement the repo's existing intent and constraint infrastructure without requiring new architectural components. The Constraint-Failure Decision Rule and Constraint Budget Gate pair naturally with the five-part intent and constraint-anchored evaluation; the Two-Implementations Goal Test and Goal Atomicity Split pair naturally with intent authoring and the Grill-Me alignment interview.

**Related prior classifications:** The IDSD Method classification (2026-06-12) classified 8 patterns including ICE Craft Separation (Partial Coverage), Intent as Five-Part Primitive (Missing), Human-Owned Expectations Boundary (Partial Coverage), and Token Economics of Gap-Filling (Partial Coverage). Those patterns have since been promoted to canonical docs with operational skills. This classification covers a different set of 9 patterns from the same author's "Anatomy of Intent" analysis, focusing more on the mechanics of constraint management, goal composition, and evaluation compartmentation -- dimensions the prior classification did not cover.
