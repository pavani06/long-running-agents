---
title: "Analise de Conhecimento: Agent Focus Problems"
type: analysis
date: 2026-06-10
aliases: ["analise foco agente", "agent focus problems", "perda de contexto agentes", "problemas de atencao"]
tags: ["agentes-orquestracao", "context-engineering", "analise"]
relates-to: ["[[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Plot]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]"]
---

# Knowledge Extraction: 01-why-agents-lose-plot.md

**Source:** `curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md`
**Date:** 2026-06-10

---

## 1. Frameworks & Models

### Three Fundamental Problems of Long-Running Agents

The document presents a tripartite framework for why AI agents degrade over long sessions:

1. **Context Amnesia** — Finite context windows cause information loss as conversations grow. The degradation follows a predictable curve: 0-60min excellent, 60-120min good, 120-180min acceptable, 180+min erratic. The root cause is architectural (finite token windows), not a bug.

2. **Planning-Execution Collapse** — When agents attempt to plan, execute, and verify in a single pass, quality collapses under task complexity. The agent has no explicit plan, no checkpoints, and context becomes chaotic as planning information mixes with execution information.

3. **Self-Evaluation Collapse** — Agents cannot reliably evaluate their own outputs due to confirmation bias. The document quantifies the gap: self-evaluation detects ~3% of real errors, while an external evaluator detects ~14%. The silent failure rate gap is 10-12 percentage points.

## 2. Patterns & Architectures

### Context Rot Degradation Curve

The quality degradation is not linear — it follows a step-function pattern where entire information bands become inaccessible at context thresholds. The middle of the conversation (not the oldest content) is the first to degrade, due to head-tail attention mechanics.

### Generator-Evaluator Pattern

A unified architectural solution to all three problems:
- **Generator** — focused on creativity and response generation (small context window)
- **Evaluator** — separate agent that verifies output against constraints (impartial, access to client data, rubrics)
- Loop: Generator → Evaluator → Approved/Rejected → feedback loop

### Architecture vs Prompting Ratio

Prompting improvements solve 20-30% of the problem. Architecture solves 70-80%. The remaining gap is inherent system noise.

### Token Noise Problem

Not all tokens carry valuable information. Natural conversations contain greetings, digressions, redundant confirmations that consume context without value. The extraction of "what is safe to discard" is a judgment problem, not a technical one.

## 3. Operational Lessons

### Cascade Effect

The three problems amplify each other: amnesia causes loss of critical constraints → planning collapse during reprocessing → self-evaluation fails to detect the new error. The client sees three sequential failures, not one.

### Context Budgeting

The practical conversation limit is not `window_size / tokens_per_message` but `(window_size - generation_buffer) / tokens_per_message`, where the generation buffer can consume 30-50% of the window for complex multi-step reasoning.

## 4. Tradeoffs

| Decision | Benefit | Cost |
|---|---|---|
| External state persistence (vs. in-context only) | Survives any conversation length; cross-session memory | Requires extraction logic + I/O latency per turn |
| Plan-Execute-Verify separation (vs. single pass) | Clear debugging, checkpoint verification, quality preservation | Adds latency from 3 separate phases |
| External evaluator (vs. self-evaluation) | Catches 10-12% more errors; impartial | 2x LLM calls per turn |
| Constraint-anchored evaluation (vs. subjective) | Objective, auditable, actionable feedback | Only catches explicitly modeled constraints |

## 5. Failure Patterns

### Silent Failure Propagation

Self-evaluation leaves 10-12% of errors undetected. In e-commerce contexts, these manifest as: recommending allergenic products, forgetting dietary restrictions, contradicting earlier commitments.

### Mid-Conversation Information Loss

The middle of long conversations degrades first (head-tail truncation effect), not the oldest content as intuition would suggest. Critical information stated at minute 5-15 is most vulnerable.

### Single-Pass Processing Errors

Without planning/execution separation, agents make cascading errors during complex multi-step tasks like order processing (validation → stock → pricing → shipping → payment).

## 6. Synthesis

The document's core insight is that these are **architectural problems, not model weaknesses**. Any LLM, regardless of context window size, faces these three structural limits. The solution is not better prompting but separation of concerns: externalize state, separate planning from execution, and use impartial external evaluation. The Generator-Evaluator pattern is presented as the unified architectural answer that solves all three problems simultaneously.
