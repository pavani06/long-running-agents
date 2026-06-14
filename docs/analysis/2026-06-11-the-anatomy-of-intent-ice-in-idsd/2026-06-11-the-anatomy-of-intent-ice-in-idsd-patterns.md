---
title: "Agentic Patterns from The Anatomy of Intent - ICE in IDSD"
type: analysis
tags: ["agentes-orquestracao", "harness-engineering", "spec-driven-development", "evals", "decision-discipline", "context-engineering", "curriculo-conteudo"]
date: 2026-06-11
aliases: ["intent ice patterns", "agentic intent patterns", "ice idsd reusable patterns", "patterns anatomy of intent"]
relates-to: ["[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-analysis|Anatomy of Intent Analysis]]", "[[docs/analysis/2026-06-11-the-anatomy-of-intent-ice-in-idsd/2026-06-11-the-anatomy-of-intent-ice-in-idsd-mental-model|Anatomy of Intent Mental Model]]"]
---

# Agentic Patterns from The Anatomy of Intent - ICE in IDSD

Scope: extracted from the ICE in IDSD knowledge analysis. Kept only patterns that shape agentic systems: how agents are instructed, constrained, evaluated, checkpointed, and orchestrated. Excluded generic tradeoffs, source-specific anecdotes, and observations that do not imply a reusable skill, canonical document, or curriculum exercise.

## 1. ICE Ownership Boundary

- **name:** ICE Ownership Boundary
- **problem solved:** Agent workflows become brittle when the same person or agent owns intent, context, expected outcomes, generation, and validation, because each artifact starts leaking into the others.
- **inputs:**
  - Human-owned intent describing the desired outcome.
  - Harness-owned context assembled from stack, architecture, team standards, and prior work.
  - Human-vetted expectations generated from intent plus context.
  - Builder agent that receives only the instruction surface it needs.
  - Validator that checks output against the approved evaluation surface.
- **outputs:**
  - Explicit ownership map for intent, context, expectations, builder output, and validation.
  - Agent task packet with intent and context separated from expectations.
  - Reviewable checkpoint where humans can veto generated expectations before execution proceeds.
- **benefits:**
  - Prevents human-written task specs from becoming overloaded with implementation context and hidden eval criteria.
  - Makes the harness responsible for repeatable context assembly instead of asking humans to rewrite environment knowledge per task.
  - Gives curriculum and skills a clear teaching target: who owns which artifact, and when each artifact is visible.
- **limitations:**
  - Requires a harness or workflow discipline that can enforce ownership boundaries.
  - Slows down small tasks where the overhead is larger than the risk.
  - Breaks down if humans bypass the checkpoint and stuff context or checks back into the intent.

## 2. Three-Part Intent Contract

- **name:** Three-Part Intent Contract
- **problem solved:** Agents receive task prompts that mix outcome, implementation, evaluation, and contextual facts, making it hard to know what should guide generation and what should be checked after output exists.
- **inputs:**
  - Candidate goal statement.
  - Candidate non-functional constraints.
  - Candidate failure conditions.
  - Task context supplied separately by the harness.
  - Human reviewer or skill gate that checks the contract before execution.
- **outputs:**
  - Intent artifact with exactly three slots: goal, constraints, and failure conditions.
  - Builder-facing subset containing the goal and constraints.
  - Validator-facing subset containing failure conditions.
- **benefits:**
  - Gives agents an outcome to pursue instead of a procedural script to imitate.
  - Creates a reusable template for skills, issue briefs, and curriculum exercises.
  - Makes later compartmented evaluation possible because each field already has a destination.
- **limitations:**
  - Does not decide context or success expectations by itself.
  - Requires disciplined review because bad fields can still be written inside the right slot.
  - Loses the granularity of larger intent models unless connections and scenarios are handled elsewhere.

## 3. Two-Implementations Goal Test

- **name:** Two-Implementations Goal Test
- **problem solved:** Humans often write implementation methods and call them goals, turning the agent into a typist instead of a decision-maker.
- **inputs:**
  - Candidate goal sentence.
  - Review question: can two substantially different implementations both satisfy this?
  - Existing architecture and team conventions held outside the goal.
  - Human or agent reviewer that can rewrite or split the candidate statement.
- **outputs:**
  - Goal that states an outcome without naming tools, classes, protocols, or storage choices.
  - Rejected implementation details routed to context, constraints, or separate intents.
  - Training example showing the difference between a goal and a spec in disguise.
- **benefits:**
  - Preserves the agent's decision space where the harness actually wants model judgment.
  - Produces simpler, more portable task intents.
  - Works well as a lightweight pre-flight skill or curriculum drill.
- **limitations:**
  - Needs reviewer judgment about what counts as substantially different implementation.
  - Can be misapplied to tasks where a tool choice is already an external constraint.
  - Does not guarantee the goal is atomic or valuable, only that it is not method-bound.

## 4. Goal Atomicity Split

- **name:** Goal Atomicity Split
- **problem solved:** Multi-goal intents hide coordination complexity behind a single sentence, causing agents to optimize for one part while silently dropping another.
- **inputs:**
  - Candidate goal statement.
  - Conjunction and dependency scan for words such as "and", "then", or multi-outcome clauses.
  - Backlog or orchestration surface that can hold multiple related intents.
  - Human decision about whether the goals must run together or separately.
- **outputs:**
  - One-sentence goal with a single outcome.
  - Additional intents for additional outcomes.
  - Optional dependency ordering between split intents.
- **benefits:**
  - Scales agent work by decomposition instead of by dense mega-prompts.
  - Makes validation sharper because each output has one primary outcome.
  - Helps orchestration systems route, parallelize, or sequence work safely.
- **limitations:**
  - Can create too many tiny tasks if applied mechanically.
  - Requires dependency tracking once one overloaded intent becomes several tasks.
  - Does not solve ambiguous constraints or weak evals on the resulting goals.

## 5. Constraint Budget Gate

- **name:** Constraint Budget Gate
- **problem solved:** Constraint lists grow until they become hidden implementation specs, removing degrees of freedom from the agent and drifting the workflow back toward spec-driven development.
- **inputs:**
  - Candidate constraints for an intent.
  - Hard budget of five to seven constraint lines.
  - Business-language review rule.
  - Context destination for implementation standards and team patterns.
  - Expectations destination for generated done criteria.
- **outputs:**
  - Short list of directional, unconditional, non-functional constraints.
  - Reclassified implementation choices moved to context.
  - Reclassified checks moved to failure conditions or expectations.
- **benefits:**
  - Keeps constraints legible enough for humans and agents to use.
  - Protects the model's useful design latitude while still bounding unacceptable outcomes.
  - Gives a concrete review gate for issue briefs, skills, and exercises.
- **limitations:**
  - The numeric budget is a heuristic, not proof that every remaining constraint is valid.
  - Some regulated or high-risk tasks may legitimately need a larger external policy surface.
  - Requires a separate context system so removed implementation details are not simply lost.

## 6. Constraint-Failure Decision Rule

- **name:** Constraint-Failure Decision Rule
- **problem solved:** Teams mix builder guidance with validator checks, which exposes eval targets to the agent and turns directional constraints into arbitrary pass/fail thresholds.
- **inputs:**
  - Candidate requirement or quality statement.
  - Decision question: would knowing this change how the builder writes the solution?
  - Builder-facing instruction surface.
  - Validator-facing failure-condition surface.
  - Human review gate for ambiguous cases.
- **outputs:**
  - Requirement classified as a constraint when the builder needs it for design decisions.
  - Requirement classified as a failure condition when it can only be checked after output exists.
  - Cleaner separation between generation guidance and evaluation criteria.
- **benefits:**
  - Prevents agents from gaming checks that should belong to the validator.
  - Gives reviewers a simple, teachable classification rule.
  - Enables encrypted or hidden evals because failure conditions are already separated.
- **limitations:**
  - Borderline cases still require human judgment.
  - Some requirements may need both a builder-facing direction and a separate hidden eval.
  - The rule depends on honest routing; it fails if failure conditions are copied back into the builder prompt.

## 7. Compartmented Evaluation Architecture

- **name:** Compartmented Evaluation Architecture
- **problem solved:** LLM builders reward-hack visible tests, scenarios, and rubrics, producing outputs that pass checks without satisfying the intended outcome.
- **inputs:**
  - Builder-facing goal and constraints.
  - Validator-facing failure conditions or evals.
  - Output artifact produced by the builder.
  - Human authority to approve intent and checkpoint expectations.
  - Harness mechanism that prevents leakage between builder and validator surfaces.
- **outputs:**
  - Builder output generated without access to hidden failure conditions.
  - Validator result based on independent checks.
  - Audit trail showing which information each participant could see.
- **benefits:**
  - Provides a structural defense against reward-hacking rather than relying on prompt wording.
  - Makes generator and evaluator roles more independent.
  - Supports future implementation as skills, PR gates, eval harnesses, or exercises about information boundaries.
- **limitations:**
  - Adds infrastructure and operational complexity.
  - Hidden evals can become stale, incomplete, or misaligned with the real outcome.
  - The validator may miss design intent if failure conditions are too narrow or poorly written.

## 8. Scenario Destination Split

- **name:** Scenario Destination Split
- **problem solved:** Scenarios serve conflicting roles as builder guidance and validator checks; sharing the same scenarios causes over-fitting and weakens independent validation.
- **inputs:**
  - Candidate success and failure scenarios.
  - Intent artifact with failure-condition slot.
  - Context assembled by the harness.
  - Expectation generator that can derive success scenarios from intent plus context.
  - Human checkpoint that approves or rejects generated expectations.
- **outputs:**
  - Failure scenarios converted into binary validator-owned failure conditions.
  - Success scenarios moved into expectations generated from intent and context.
  - Approved expectation set that remains separate from hidden failure checks.
- **benefits:**
  - Keeps validator-owned checks independent from builder hints.
  - Lets success criteria include real context without making the human hand-author every scenario.
  - Gives curriculum a concrete exercise for separating examples, expectations, and evals.
- **limitations:**
  - Requires an expectations generation step and a human checkpoint.
  - Poorly generated expectations can still bias downstream work.
  - Teams may resist the split because shared scenarios feel simpler at first.

## 9. Harness-Owned Context Assembly

- **name:** Harness-Owned Context Assembly
- **problem solved:** Humans repeatedly copy stack details, architectural conventions, and team practices into task prompts, creating drift, stale context, and incentives to over-specify the agent's method.
- **inputs:**
  - Stable repository or organization standards.
  - Architecture, service, dependency, and prior-work metadata.
  - Task intent supplied by the human.
  - Resolver, skill loader, memory catalog, or context builder inside the harness.
  - Validation checkpoint for whether the assembled context is sufficient.
- **outputs:**
  - Context packet assembled by infrastructure rather than the intent author.
  - Cleaner human intent focused on outcome, constraints, and failure conditions.
  - Repeatable context provenance that can be inspected and improved over time.
- **benefits:**
  - Converts prompt-writing discipline into reusable infrastructure.
  - Reduces copy-paste drift and conflicting local interpretations of team standards.
  - Makes ICE economically useful because the harness returns value for the discipline humans spend on intent.
- **limitations:**
  - Needs maintained metadata, resolvers, or skills that know where context lives.
  - Bad context assembly can mislead the builder even when the intent is well written.
  - Without adoption pressure, users may keep bypassing the harness with ad hoc context in prompts.
