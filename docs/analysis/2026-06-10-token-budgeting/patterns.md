---
title: "Token Budgeting Agentic Patterns"
type: analysis
date: 2026-06-10
tags: ["agentes-orquestracao", "curriculo-conteudo", "context-engineering"]
aliases: ["token budgeting patterns", "agentic token budgeting patterns", "token budget pattern catalog"]
relates-to: ["[[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
---

# Token Budgeting Agentic Patterns

Scope: extracted from [[docs/analysis/2026-06-10-token-budgeting/analysis|Token Budgeting Analysis]]. Only reusable mechanisms that can be implemented inside agentic systems, agent harnesses, long-running sessions, or context builders are kept. Pure explanatory lessons, generic tradeoff notes, and failure names without an operational mechanism are excluded.

## 1. Explicit Token Budget Ledger

- **name:** Explicit Token Budget Ledger
- **problem solved:** Agent loops that treat context as unbounded cannot know whether the next model call has enough room for history, tools, and a useful response.
- **inputs:**
  - Model context-window size.
  - Fixed harness, system prompt, and tool-schema tokens.
  - Accumulated history, memory, tool-result, and current-prompt tokens.
  - Reserved response buffer and safety buffer.
- **outputs:**
  - Remaining budget after fixed, accumulated, response, and safety allocations.
  - Available-budget percentage for the next agent step.
  - A budget breakdown that the harness can inspect before building context.
- **benefits:**
  - Makes token pressure visible before the agent reaches a hard context limit.
  - Reserves output capacity instead of spending the whole window on input.
  - Gives the context builder an explicit constraint for pruning, summarizing, or handoff.
- **limitations:**
  - Token estimates can be approximate unless measured with the same tokenizer as the model.
  - It reports budget state but does not decide which memories are worth retaining.
  - Requires every prompt-building path to report its token cost consistently.

## 2. Burn-Rate Runtime Forecast

- **name:** Burn-Rate Runtime Forecast
- **problem solved:** The same remaining context can be safe in a slow session and risky in an accelerating multi-step agent run.
- **inputs:**
  - Timestamped input and output token usage per turn, tool call, or loop iteration.
  - Elapsed session time and recent message cadence.
  - Typical user, tool-result, and agent-response sizes.
  - Reserved response and safety buffers.
- **outputs:**
  - Current burn rate in tokens per minute or tokens per loop iteration.
  - Estimated remaining messages, loop iterations, or operating minutes.
  - Acceleration signal when consumption is rising faster than expected.
- **benefits:**
  - Adds a time dimension to context health instead of relying only on remaining tokens.
  - Triggers summarization or handoff before a busy session becomes unrecoverable.
  - Helps operators compare long-running agent workloads by expected runway.
- **limitations:**
  - Forecasts degrade when user behavior or tool payload size changes abruptly.
  - Needs calibration by product, workflow, model, and context-builder strategy.
  - Overly conservative estimates can trigger unnecessary compression.

## 3. Phase-Gated Token Health Monitor

- **name:** Phase-Gated Token Health Monitor
- **problem solved:** Agents often discover token pressure only after answer quality degrades, reasoning weakens, or the context limit is reached.
- **inputs:**
  - Remaining-budget percentage from the token budget ledger.
  - Burn-rate forecast and recent acceleration signal.
  - Green, yellow, orange, and red thresholds.
  - Current context stack and available compaction or handoff actions.
- **outputs:**
  - A health phase such as green, yellow, orange, or red.
  - A recommended action such as continue, monitor, compress, summarize, or new_session.
  - An intervention reason that can be logged or shown to downstream orchestration.
- **benefits:**
  - Converts token budgeting from reactive truncation into a runtime control loop.
  - Gives deterministic intervention points inside an owned agent loop.
  - Reduces late-session quality collapse by acting while there is still room to compact safely.
- **limitations:**
  - Thresholds need tuning against real traces and model behavior.
  - The monitor is only useful if the harness implements the returned action.
  - Aggressive thresholds can increase latency or summary churn.

## 4. Durable Fact Selective History

- **name:** Durable Fact Selective History
- **problem solved:** Full-history prompts grow without bound, while simple windowing can drop critical user or task facts needed later.
- **inputs:**
  - Recent conversation turns.
  - Extracted critical facts, constraints, preferences, and task state.
  - Structured memory schema for durable facts.
  - Current user request or agent objective.
- **outputs:**
  - Active context containing recent conversational texture plus structured durable facts.
  - Omitted transient turns that are no longer needed verbatim.
  - Updated durable memory when new critical facts appear.
- **benefits:**
  - Separates stable state from transient transcript history.
  - Lets facts survive windowing, summarization, and session transition.
  - Keeps model input bounded while preserving decision-critical context.
- **limitations:**
  - Fact extraction can miss important details or retain low-value noise.
  - Requires update, freshness, and provenance rules for structured memory.
  - Can lose conversational nuance when durable facts are too sparse.

## 5. Windowed Recent History

- **name:** Windowed Recent History
- **problem solved:** Long-running conversations exceed predictable input limits when every prior turn remains in the active prompt.
- **inputs:**
  - Ordered message history.
  - Window size or token target for recent turns.
  - Current user request and current agent state.
  - Pinned non-history blocks such as harness prompt and durable facts.
- **outputs:**
  - Active prompt history limited to the last N messages or last budgeted token span.
  - Older turns dropped from active context or moved to external memory.
  - Predictable upper bound for transcript tokens in each model call.
- **benefits:**
  - Simple to implement and cheap to run.
  - Gives strong control over context growth in very long sessions.
  - Preserves immediate conversational continuity and latest state.
- **limitations:**
  - Distant dependencies disappear unless another memory mechanism preserves them.
  - Blind windows can cut across a task boundary or tool-result sequence.
  - Works best when paired with durable facts, summaries, or recoverable memory handles.

## 6. Summary Buffer Continuity

- **name:** Summary Buffer Continuity
- **problem solved:** Older conversation may contain useful state but cannot remain verbatim in every model call.
- **inputs:**
  - Older transcript span or full-history segment selected for summarization.
  - Existing summary buffer, if one already exists.
  - Durable facts that must not be lost or blurred.
  - Target token budget and summary freshness metadata.
- **outputs:**
  - Compact summary buffer included alongside recent messages.
  - Updated summary after older context is folded in.
  - Smaller active prompt with continuity across earlier session phases.
- **benefits:**
  - Preserves broad continuity through one-to-three-hour or longer agent sessions.
  - Reduces token load without discarding all older context.
  - Creates a portable handoff artifact for new sessions or sub-agents.
- **limitations:**
  - Summaries are lossy and can remove details that become relevant later.
  - Requires extra model calls, scheduling, and quality checks.
  - Summary drift accumulates if updates are not anchored to source state.

## 7. Targeted Semantic Compression

- **name:** Targeted Semantic Compression
- **problem solved:** Individual messages, tool results, and trace chunks can contain redundant wording that consumes context without adding task-relevant information.
- **inputs:**
  - Source text or payload selected for compression.
  - Required facts, constraints, decisions, and unresolved questions.
  - Target token budget.
  - Fidelity criteria for what must survive compression.
- **outputs:**
  - Compressed text that preserves the critical meaning under the target budget.
  - Smaller context block suitable for inclusion in the next model call.
  - Optional note about omitted redundant or low-value material.
- **benefits:**
  - Recovers budget without dropping an entire message or tool result.
  - Useful for verbose payloads where exact tone is less important than meaning.
  - Can be applied selectively to high-cost blocks before broader truncation.
- **limitations:**
  - May lose exact wording, tone, or evidence needed for later audit.
  - Compression quality depends on well-defined fidelity criteria.
  - High-risk domains may need source handles or evals to catch semantic loss.

## 8. Semantic Topic Bucketing

- **name:** Semantic Topic Bucketing
- **problem solved:** Chronological transcripts mix unrelated topics, making selective retention and summarization brittle.
- **inputs:**
  - Conversation messages, tool outputs, or trace events.
  - Domain-specific topic taxonomy or bucket list.
  - Classifier, rules, or model prompt for assigning items to buckets.
  - Per-topic summary or retention policy.
- **outputs:**
  - Topic-specific buckets with grouped source material.
  - Per-bucket summaries or retained facts.
  - Mapping from active summaries back to source spans or memory handles.
- **benefits:**
  - Preserves logical structure better than one chronological summary.
  - Lets the agent retrieve or refresh only the topic needed for the next decision.
  - Fits structured domains with recurring themes such as preferences, constraints, orders, delivery, or recommendations.
- **limitations:**
  - Topic classifier weakness can misplace critical information.
  - Multi-topic messages may need duplication or source handles to avoid loss.
  - Bucket taxonomies need maintenance as the workflow evolves.

## 9. Hybrid Context Stack

- **name:** Hybrid Context Stack
- **problem solved:** No single budgeting strategy handles all agent phases, memory types, and information densities reliably.
- **inputs:**
  - Stable harness prompt and tool contracts.
  - Durable structured facts.
  - Summary buffer for older turns.
  - Recent-message window.
  - Optional compressed blocks, topic buckets, and token-health action.
- **outputs:**
  - Layered active context assembled under a known token budget.
  - Inclusion order that prioritizes stable harness, critical state, compressed history, and current tail.
  - Context-builder decision trace explaining what was kept, summarized, compressed, or omitted.
- **benefits:**
  - Balances continuity, latency, and quality across long-running agent sessions.
  - Prevents stable facts, summaries, and recent texture from competing in one raw transcript.
  - Gives production harnesses a composable policy instead of a single truncation trick.
- **limitations:**
  - More complex than a window or summary alone.
  - Component interactions can hide bugs unless the context builder is observable.
  - Needs evals or replay traces to prove continuity after compaction.

## 10. Budget-Aware Session Handoff

- **name:** Budget-Aware Session Handoff
- **problem solved:** Continuing inside a red budget phase can hide degradation, shorten answers, weaken reasoning, or crash at the context limit.
- **inputs:**
  - Red-phase signal from the token health monitor.
  - Durable facts, current objective, open decisions, and latest state.
  - Summary buffer and recoverable memory handles.
  - Handoff instructions for the next session, agent, or orchestration branch.
- **outputs:**
  - Fresh-session start payload or agent handoff record.
  - User-visible or system-visible transition that explains continuity state.
  - Reset active context budget with the essential state carried forward.
- **benefits:**
  - Turns token exhaustion into an intentional product or orchestration flow.
  - Resets the active context budget before quality collapses.
  - Preserves enough state for continuity instead of relying on a hidden truncated transcript.
- **limitations:**
  - Handoff quality depends on accurate summaries, durable facts, and memory handles.
  - Users or downstream agents may notice discontinuity if state capture is incomplete.
  - Exact historical continuity still requires recoverable source memory outside the new prompt.

