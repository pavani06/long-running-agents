---
title: "Agentic Patterns from How We Solved Context Management in Agents"
type: digest
date: 2026-06-09
sources_covered: 1
sources: ["docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis.md"]
tags: [synthesis, ai, agents, context-engineering, memory]
relates-to: ["[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/analysis|Context Mgmt Analysis]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]"]
aliases: ["padrões contexto", "context patterns", "catálogo contexto"]
---

# Agentic Patterns from How We Solved Context Management in Agents

Scope: extracted from Sally-Ann Delucia's Arize talk analysis on context management in agents. Kept only reusable patterns with concrete mechanics for agentic systems; product-only observations, generic tradeoffs, and failure modes without an actionable system shape were excluded.

## 1. Head-Tail Context Truncation with Recoverable Middle

- **name:** Head-Tail Context Truncation with Recoverable Middle
- **problem solved:** An agent must reduce an oversized conversation or trace payload without erasing the original task setup, the latest state, or access to omitted details.
- **inputs:**
  - Stable system prompt or harness instructions.
  - Ordered conversation, trace, tool-call, or prompt payload.
  - Context budget and truncation thresholds.
  - Latest user request or latest tool result.
  - Memory store and retrieval tool for omitted content.
- **outputs:**
  - Bounded active context containing the system prompt, head, tail, and latest result.
  - Omitted middle content stored outside the active window.
  - Retrieval handles for bringing selected omitted content back on demand.
- **benefits:**
  - Preserves both the initial anchor and the current conversational state.
  - Avoids the follow-up failures caused by first-only truncation.
  - Is more auditable than opaque LLM summarization because omitted content remains recoverable.
- **limitations:**
  - Still uses a heuristic selection policy unless paired with stronger context-quality metrics.
  - Requires storage, metadata, and retrieval tooling.
  - Can preserve the wrong spans if the payload structure changes or the head/tail cut points are poorly chosen.

## 2. Addressable Memory Catalog

- **name:** Addressable Memory Catalog
- **problem solved:** A memory store does not help an agent if the agent cannot decide what to retrieve without reloading everything into context.
- **inputs:**
  - Omitted messages, tool calls, spans, prompts, or intermediate results.
  - Stable IDs for each omitted item or blob.
  - Conversational location, message distance, or span position metadata.
  - Compact previews sized to guide retrieval without recreating the context problem.
  - Current agent task or follow-up question.
- **outputs:**
  - Catalog of retrievable omitted items.
  - Selected memory items fetched into the active context when needed.
  - A smaller context window that can still recover specific details.
- **benefits:**
  - Turns memory into an addressable tool rather than an unstructured archive.
  - Lets the agent retrieve exact details instead of relying on lossy summaries.
  - Makes context omissions easier to inspect and debug.
- **limitations:**
  - Preview quality is a hard tradeoff: too small hides relevance, too large pollutes context.
  - Retrieval can still fail if the agent chooses the wrong ID.
  - It solves in-session recoverability, not long-term memory across new chats.

## 3. Heavy-Context Sub-Agent Isolation

- **name:** Heavy-Context Sub-Agent Isolation
- **problem solved:** Data-intensive work such as trace search can flood the main agent with spans, prompts, tool calls, and intermediate reasoning that the user conversation does not need to carry.
- **inputs:**
  - Main agent intent or user request.
  - Scoped delegation request.
  - Heavy data sources such as traces, spans, prompts, messages, and metadata.
  - Sub-agent tools for search, analysis, and synthesis.
  - Result contract for returning a compact answer.
- **outputs:**
  - Sub-agent result, summary, or evidence packet.
  - Main conversation updated only with compact findings and relevant references.
  - Separate context windows for heavy analysis and user-facing continuity.
- **benefits:**
  - Prevents heavy search context from contaminating the main chat.
  - Gives data-intensive reasoning its own context budget.
  - Handles provider-limit collisions better than local compaction alone.
- **limitations:**
  - Adds delegation, coordination, and result-composition complexity.
  - Requires the main agent to trust but verify compressed sub-agent outputs.
  - Can hide important evidence if the sub-agent return contract is too lossy.

## 4. Lightweight Main Conversation Surface

- **name:** Lightweight Main Conversation Surface
- **problem solved:** Users want one continuous chat across a product journey, but the implementation cannot safely keep every payload, trace, and intermediate step in the main context window.
- **inputs:**
  - User-visible conversation thread.
  - Current user goal and latest result.
  - Compact summaries from tools or sub-agents.
  - Memory references for omitted history.
  - Delegation and retrieval triggers for heavier work.
- **outputs:**
  - Main agent context focused on continuity and final results.
  - Bulky data retained in memory stores or sub-agent contexts.
  - Follow-up handling that retrieves or delegates only when needed.
- **benefits:**
  - Separates UX continuity from data completeness.
  - Keeps the main agent responsive and context-bounded during long sessions.
  - Reduces the chance that intermediate reasoning or bulk telemetry competes with the next user request.
- **limitations:**
  - Requires reliable links between the chat, memory store, and delegated work.
  - Follow-ups can still fail if summaries or references are too thin.
  - Does not by itself provide continuity across separate chat sessions.

## 5. Long-Session N+1 Context Eval

- **name:** Long-Session N+1 Context Eval
- **problem solved:** Context bugs often appear only after many turns, after simple single-turn or short-session tests have already passed.
- **inputs:**
  - Realistic N-turn conversation history.
  - The production context-building, truncation, memory, and delegation strategy.
  - A next-turn prompt that depends on prior context.
  - Expected behavior or grading criteria for continuity, reference resolution, and task correctness.
- **outputs:**
  - Regression result for the N+1 turn.
  - Reproducible failure cases for late-session forgetting or degraded follow-up handling.
  - Evidence that a context strategy preserves behavior, not just token budget.
- **benefits:**
  - Converts late-session forgetting into a testable regression.
  - Catches over-truncation and lossy summarization failures that pass short tests.
  - Measures the agent through behavior rather than prompt size alone.
- **limitations:**
  - Covers only the conversation regimes modeled by the fixtures.
  - Does not replace a formal context-quality metric.
  - Requires ongoing maintenance as real user sessions change.

## 6. Context Strategy Feedback Loop

- **name:** Context Strategy Feedback Loop
- **problem solved:** No single compaction or memory technique handles every way an agent's context grows as usage patterns change.
- **inputs:**
  - Current context strategy and heuristics.
  - Observed failures, eval regressions, and user behavior changes.
  - Tradeoffs between truncation, summarization, retrieval, sub-agents, and long-term memory.
  - Product or observability signals showing where context degradation appears.
- **outputs:**
  - Updated context strategy or heuristic.
  - New regression evals based on observed failures.
  - Revised boundaries for what belongs in active context, memory, or sub-agent contexts.
- **benefits:**
  - Keeps context management aligned with real usage instead of the initial product regime.
  - Turns failures into durable tests before they recur.
  - Encourages the simplest working strategy first, then adds architecture where failures prove it is needed.
- **limitations:**
  - Requires ownership across product behavior, evals, and observability.
  - Can remain heuristic without a principled context budget or metric.
  - Slower than a one-off truncation fix because it treats context as an evolving system property.

## 7. Memory Tier Separation

- **name:** Memory Tier Separation
- **problem solved:** Teams often confuse active context, in-session recovery memory, and long-term product memory, causing one memory mechanism to be expected to solve incompatible continuity problems.
- **inputs:**
  - Active task context needed for the next model call.
  - Omitted in-session history that may need exact retrieval.
  - Cross-session facts, preferences, decisions, or unresolved work that users expect the agent to remember later.
  - Retrieval policies for each memory tier.
  - Promotion criteria for deciding what deserves durable memory.
- **outputs:**
  - Active context for immediate reasoning.
  - In-session memory for recoverable truncation.
  - Separate long-term memory surface for cross-session continuity.
  - Clear retrieval paths that tell the agent which tier to query for which kind of need.
- **benefits:**
  - Prevents conversation-truncation memory from being overloaded with product-memory responsibilities.
  - Clarifies why restoring omitted middle content is different from remembering prior chats.
  - Makes context continuity and user relationship continuity independently designable and testable.
- **limitations:**
  - Requires explicit policies for what becomes durable memory.
  - Adds privacy, freshness, deletion, and retrieval-quality concerns beyond in-session memory.
  - The source analysis identifies long-term memory as an unresolved hard gap, so implementations need additional design beyond the talk's concrete mechanics.
