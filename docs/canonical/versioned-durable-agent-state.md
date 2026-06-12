---
title: 'Versioned Durable Agent State'
type: canonical
aliases: ["versioned state", "estado versionado", "durable state versioning", "state versioning"]
tags: ["agentes-orquestracao", "harness", "arquitetura"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]", "[[docs/articles/harness-evolution-metodos-construcao|A Arquitetura Invisivel]]"]
sources: ["[[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction: Harness Evolution]]"]
---

# Versioned Durable Agent State

**Type:** Canonical Pattern
**Status:** Active
**Source:** docs/articles/harness-evolution-metodos-construcao.md
**Classification:** Partial Coverage
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

Agents that keep durable facts only in the active model context lose continuity when a server fails, a payment callback arrives, or a long-running session resumes after a pause; the source analysis names this failure as state that lives only in the context window and turns failures or payment events into amnesia ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction: Harness Evolution]]:61-64). The extracted pattern generalizes the same problem to crashes, restarts, payment events, callbacks, and long pauses ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:175-176).

The breakage is not only forgetting a preference. The durable-state inputs include preferences, decisions, commitments, cart or workflow state, and active constraints, so losing them can lose a cart, erase a decision, drop a commitment, or remove a constraint that later generation and validation should still observe ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:177-181). The same source classifies state persistence as an invariant because without persisted state there is no auditability, debugging, or recovery ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction: Harness Evolution]]:61-64).

Without schema versioning and migration rules, durable state can survive the interruption but still corrupt continuity when the stored shape changes. The extracted pattern lists `State schema version and migration policy` as an input, `Versioned state schema` and `Migration path` as components, and names migration mistakes as a limitation that can corrupt continuity across versions ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:177-200).

## Solution

Define durable agent state as a versioned contract made of five pieces: schema version, writeback policy, reload policy, migration path, and audit trail. The extracted pattern requires the state schema version and migration policy as inputs, writeback rules from agent events and tool results as inputs, reload policy at conversation start or resume as an input, and audit trail plus migration path as components ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:177-200).

The operational loop is:

```
Agent event / tool result
          |
          v
  Extract durable facts
          |
          v
+----------------------------+
| Versioned State Contract   |
| schema_version             |
| writeback_policy           |
| migration_path             |
| audit_trail                |
+----------------------------+
          |
          v
  Durable State Store
          |
          v
Crash / callback / pause / restart
          |
          v
  Reload + migrate if needed
          |
          v
Inject relevant state into active context
```

Writeback must extract durable facts from agent events and tool results, then write through the versioned schema; this mirrors the extracted flow `Extract durable facts`, `Write state through a versioned schema`, and `Audit state changes` ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:201-206). Reload must run at conversation start or paused-loop resume, then inject only relevant state into the active context, because the extracted flow separates reload from selective context injection ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:201-206).

The contract should make state durable outside the context window, reconstruct the agent context after interruption or resume, and preserve an audit trail for decisions and commitments; these are the stated outputs of the extracted pattern ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:182-185). It should also keep stored facts independent from fragile conversation history, which the extracted benefits identify as continuity across failures, debugging and auditability, and reduced dependence on conversation history ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:186-189).

## Implementation in this repo

### What already exists

- [[docs/canonical/external-state-persistence|External State Persistence]] already defines the core externalization loop: extract critical data, write it to an external store keyed by client or session, load it on the next turn, merge it with current context, and generate or evaluate the response ([[docs/canonical/external-state-persistence|External State Persistence]]:29-57).
- [[docs/canonical/external-state-persistence|External State Persistence]] already identifies durable categories such as allergies, preferences, constraints, commitments, prior purchases, returns, unresolved issues, and evaluator failures, while excluding greetings, filler, digressions, one-turn phrasing, and ephemeral scratchpads ([[docs/canonical/external-state-persistence|External State Persistence]]:59-64).
- [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]] already covers serializing context window, execution state, and business state to persistent storage, then deserializing and continuing from where the agent paused ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-34).
- [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]] already documents the repo's alternative state-rebuild approach, where state lives in the database and is reconstructed rather than stored only as serialized graph state ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:59-76).
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]] already requires durable state to be injected from state stores according to freshness rules and requires prompt changes to be deliberate, versioned, and evaluated separately from context compaction ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:30-41).
- The [[docs/system-of-record|System of Record]] places active canonical docs at precedence level 2, ahead of evidence, analysis, archive, READMEs, and operational summaries ([[docs/system-of-record|System of Record]]:14-21).

### What is missing

- No active canonical doc currently names `Versioned Durable Agent State` as the unified durable-state contract; the [[docs/system-of-record|System of Record]] lists `external-state-persistence.md`, `serializable-pause-resume-state.md`, and `stable-harness-prompt.md`, but it does not list `versioned-durable-agent-state.md` among the 28 active canonical patterns ([[docs/system-of-record|System of Record]]:124-159).
- The existing external persistence doc says schemas must evolve without breaking existing sessions, but it does not define the schema-version contract, migration policy, writeback policy, reload policy, and audit trail as one canonical contract ([[docs/canonical/external-state-persistence|External State Persistence]]:85-93).
- The existing pause/resume doc covers serialization and state rebuild, but its stated gap is token-level fidelity across pauses rather than versioned durable-state governance, so it does not supply the durable schema and migration policy requested by this pattern ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:118-122).
- The stable harness prompt doc mentions durable state freshness and versioned prompt changes, but its missing implementation details focus on prompt non-reducibility, prompt version metadata, eval failures, and truncation boundaries rather than durable-state schema migration or audit trail requirements ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:55-64).
- The extracted pattern explicitly includes schema version, migration policy, writeback rules, reload policy, audit trail, and migration path in one pattern, which is the unification missing from the existing adjacent canonicals ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:177-206).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Preserves continuity across failures and asynchronous workflows ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:186-189) | Requires schema governance, privacy handling, and stale-state management ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:190-193) |
| Enables debugging and auditability for long-running behavior ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:186-189) | Migration mistakes can corrupt continuity across versions ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:190-193) |
| Keeps critical facts from depending on fragile conversation history ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:186-189) | Still requires a policy for selecting which stored state belongs in active context ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:190-193) |
| Reconstructs agent context after interruption or resume ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:182-185) | Adds a durable-state store and reload step to the loop ([[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:194-206) |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/external-state-persistence|External State Persistence]], because durable state first requires extracting critical facts, writing them outside the context window, loading them on future turns, and merging them with current context ([[docs/canonical/external-state-persistence|External State Persistence]]:29-57).
- **Validated by:** [[docs/canonical/serializable-pause-resume-state|Serializable Pause-Resume State]], because pause/resume validation checks whether context, execution state, and business state can persist and continue after interruption ([[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:20-34).
- **Complements:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]], because durable state is injected as a separate context-builder block under freshness rules while stable harness instructions remain separately versioned and evaluated ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:30-41).

## References

- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-analysis|Knowledge Extraction: Harness Evolution]]:61-64 - state persistence problem, versioned fields, reload on each conversation, and invariant status.
- [[docs/analysis/2026-06-10-harness-evolution-metodos-construcao/2026-06-10-harness-evolution-metodos-construcao-patterns|Harness Evolution Patterns]]:175-206 - extracted `Versioned Durable Agent State` pattern, inputs, outputs, benefits, limitations, components, and flow.
- [[docs/canonical/external-state-persistence|External State Persistence]]:29-65 - existing external-store extraction, write, reload, merge, and durable/ephemeral split.
- [[docs/canonical/serializable-pause-resume-state|Serializable Pause/Resume State]]:31-89 - existing pause/resume serialization and state-rebuild comparison.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt]]:30-41 - existing context-builder blocks, durable-state freshness, and versioned stable prompt policy.
- [[docs/system-of-record|System of Record]]:14-21 - documentation precedence levels.
