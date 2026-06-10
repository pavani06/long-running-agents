---
title: "Agentic Patterns from 12-Factor Agents"
type: digest
date: 2026-06-09
sources_covered: 1
sources: ["sources/2026-06-09-12-factor-agents"]
tags: [synthesis, ai, agents, software-engineering, context-engineering]
---

# Agentic Patterns from 12-Factor Agents

Scope: extracted only from the transcript body of Dex Horthy's "12-Factor Agents" talk (AI Engineer, 2025). Marketing, anecdotes, repetition, product delivery advice, and mechanics-free principles were excluded.

## 1. Structured Output Contract

- **name:** Structured Output Contract
- **problem solved:** Natural-language requests are difficult for deterministic application code to consume directly.
- **inputs:**
  - User sentence, event, task request, or operational message.
  - A target data shape such as JSON.
  - Prompt instructions that ask the model to transform the input into that shape.
- **outputs:**
  - A structured JSON object representing intent, parameters, or the next action.
  - A machine-readable contract that downstream code can inspect.
- **benefits:**
  - Turns model output into something ordinary software can route, validate, and execute.
  - Lets agentic behavior be introduced as one modular capability inside an existing app.
  - Keeps the model focused on the high-value conversion from language to structure.
- **limitations:**
  - The JSON does not do anything by itself; downstream control flow is still required.
  - Reliability depends on the prompt and the chosen structure.
  - It is only one piece of an agentic system, not the whole agent loop.

## 2. Deterministic Tool Dispatch

- **name:** Deterministic Tool Dispatch
- **problem solved:** Treating tool use as a magical agent abstraction obscures what actually happens and makes systems harder to debug.
- **inputs:**
  - JSON emitted by the model.
  - Deterministic handlers, switch statements, or loop branches.
  - Optional tool results to feed back into later context.
- **outputs:**
  - Invoked code paths or API calls selected from the JSON.
  - Tool results that can be appended, summarized, or routed into the next step.
- **benefits:**
  - Reframes tools as plain JSON plus code.
  - Makes dispatch inspectable and testable with normal software techniques.
  - Avoids hiding critical routing logic inside opaque framework internals.
- **limitations:**
  - Requires the application to own the mapping between JSON shapes and code paths.
  - Bad or ambiguous JSON still needs handling by the surrounding loop.
  - Feeding tool results back blindly can create context-window problems.

## 3. Owned Agent Control Loop

- **name:** Owned Agent Control Loop
- **problem solved:** Naive agent loops that repeatedly send the whole context back to the model become unreliable on longer workflows.
- **inputs:**
  - Incoming event or user message.
  - Prompt that instructs the model how to select the next step.
  - Context-window builder.
  - Switch statement or dispatcher for model-selected actions.
  - Exit, break, summarize, or judge conditions.
- **outputs:**
  - A materialized sequence of executed steps.
  - Final answer, completion signal, or handoff to another branch.
  - Updated execution context for the next loop iteration.
- **benefits:**
  - Gives developers explicit control over when to continue, pause, summarize, judge, or exit.
  - Makes agent behavior easier to reason about as ordinary control flow.
  - Reduces reliance on hidden framework loops and unbounded context growth.
- **limitations:**
  - Requires building and maintaining the inner loop instead of outsourcing it entirely.
  - Does not eliminate the need to design prompts, context, dispatch, and state carefully.
  - Long workflows still need bounded decomposition to stay reliable.

## 4. Serializable Pause/Resume State

- **name:** Serializable Pause/Resume State
- **problem solved:** Long-running tools and asynchronous work do not fit cleanly into a single synchronous model loop.
- **inputs:**
  - Execution state such as current step, next step, retry counts, and loop position.
  - Business state such as messages, displayed data, and pending approvals.
  - Context window owned by the application.
  - State ID stored in a database.
  - Callback result from a long-running tool.
- **outputs:**
  - Serialized state that can be paused and later reloaded.
  - Resumed agent execution with the callback result appended to the program state.
  - REST API or MCP-style interaction surface for launching and resuming workflows.
- **benefits:**
  - Supports launch, pause, and resume semantics like standard APIs.
  - Lets long-running work happen outside the immediate model call.
  - Keeps the model unaware of background execution details while the application preserves continuity.
- **limitations:**
  - Requires the application to own state and context serialization.
  - Requires reliable state IDs and callback plumbing.
  - The loop must distinguish execution state from business state.

## 5. Token-Level Prompt and Context Builder

- **name:** Token-Level Prompt and Context Builder
- **problem solved:** Hidden prompt construction and generic message history make it difficult to improve agent reliability past a quality threshold.
- **inputs:**
  - Hand-authored prompt tokens.
  - Event state, thread model, memory, retrieval results, history, and business data.
  - Formatting choice such as standard message arrays, a single user message, or system-message structure.
  - Evaluation cases and knobs to test prompt/context variants.
- **outputs:**
  - A deliberately constructed prompt and context window.
  - Dense, clear model input optimized for the next decision.
  - Repeatable variants that can be evaluated.
- **benefits:**
  - Improves reliability by controlling what tokens enter the model.
  - Allows experimentation with different context layouts and prompt variants.
  - Treats prompt, memory, RAG, and history as one context-engineering surface.
- **limitations:**
  - Requires inspecting and tuning individual tokens instead of relying on defaults.
  - There is no single guaranteed best format; the transcript frames this as something to try and evaluate.
  - The approach costs more engineering effort than generated or framework-owned prompts.

## 6. Error Context Hygiene

- **name:** Error Context Hygiene
- **problem solved:** Blindly appending tool errors and stack traces to context can cause retry loops to spin out, lose context, or get stuck.
- **inputs:**
  - Failed tool call.
  - Associated API error or exception.
  - Pending error list.
  - Subsequent valid tool call, if one occurs.
- **outputs:**
  - A concise error summary placed into the context window.
  - Cleared pending errors after a valid tool call.
  - Retry context that tells the model what it needs without dumping full stack traces.
- **benefits:**
  - Enables model-assisted recovery from wrong API calls or unavailable APIs.
  - Reduces context pollution from raw errors.
  - Prevents stale errors from biasing later steps after progress resumes.
- **limitations:**
  - The transcript calls this pattern controversial when used alone.
  - It depends on owning the context window rather than blindly appending messages.
  - Poorly managed retries can still loop or degrade reliability.

## 7. Human Contact Intent Tool

- **name:** Human Contact Intent Tool
- **problem solved:** Agents often avoid the early decision between calling a software tool and sending a message to a human.
- **inputs:**
  - Current agent state and trace.
  - Natural-language intent options such as done, need clarification, or need approval from a manager.
  - Human-contact tool or communication channel.
  - Human response to bring back into the trace.
- **outputs:**
  - Routed message to a human when the model selects a human-facing intent.
  - Clarification, approval, rejection, or instruction from the human.
  - Updated context that lets the workflow continue.
- **benefits:**
  - Moves the tool-versus-human choice into tokens the model understands naturally.
  - Supports agents that collaborate with humans instead of pretending every step is autonomous.
  - Gives the model multiple human-facing outcomes beyond a single final answer.
- **limitations:**
  - Requires explicit design of human-contact intents and routing.
  - Human latency and availability become part of the workflow.
  - The transcript only sketches the mechanism and points to deeper treatment elsewhere.

## 8. Micro-Agent Islands in a Deterministic DAG

- **name:** Micro-Agent Islands in a Deterministic DAG
- **problem solved:** Fully open-ended agents with long workflows and large context windows are unreliable, while fully deterministic workflows cannot handle every natural-language decision point.
- **inputs:**
  - Mostly deterministic workflow or DAG.
  - Small focused agent loop bounded to roughly three to ten steps.
  - Natural-language decision point that can be converted into JSON.
  - Human approvals or corrections when required.
  - Deterministic code to resume after the agent island finishes.
- **outputs:**
  - JSON next-step decision or bounded sequence of decisions.
  - Completed subtask handed back to deterministic workflow code.
  - Optional rollback or follow-up micro-agent when the deterministic path fails.
- **benefits:**
  - Keeps context manageable.
  - Gives each agent loop a clear responsibility.
  - Allows large systems with many tools and steps while preserving deterministic scaffolding.
- **limitations:**
  - Requires decomposition into small agent loops and deterministic surrounding code.
  - Not every problem needs an agent; purely scripted sequences may be simpler.
  - The boundary of what the model can do reliably must be engineered and tested.
