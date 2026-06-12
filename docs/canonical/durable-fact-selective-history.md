---
title: "Durable Fact Selective History"
type: canonical
aliases: ["historico seletivo com fatos duraveis", "selective history", "critical context injection"]
tags: ["context-engineering", "agentes-orquestracao"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]", "[[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
---
# Durable Fact Selective History

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] and [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]
**Classification:** Partial Coverage
**Precedence:** Level 2, because active canonical docs outrank analysis and curriculum according to [[docs/system-of-record|System of Record]]:14-21.

---

## Problem

Passing the entire transcript into every model call gives high early quality but creates late-session failure as history grows. The source lesson shows the anti-pattern directly: `full_history = get_all_messages_ever()` grows to 80K tokens, feels excellent in the first minutes, starts producing bugs after 30 minutes, and can crash after 60 minutes ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:172-190).

Blind windowing fixes token growth but can drop distant facts that still govern later decisions. The same lesson therefore defines the correct pattern as recent messages plus critical client context such as allergies, budget, and purchase history ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:191-217). The Phase 3 analysis generalizes that mechanism: keep recent history plus critical structured context, separating durable facts from transient conversation turns ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:65-70).

The repository already has adjacent canonical pieces, but no single contract for selective history. Phase 3 classifies this pattern as Partial Coverage because existing docs cover durable state extraction, persistence, injection, and omitted-memory handles, but do not unify recent conversational texture, structured durable facts, durable-memory updates, and explicit dropping of transient turns ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:44-50).

## Solution

Build every long-running model call from two different memory classes, not from one undifferentiated transcript:

1. **Recent conversational texture:** the current request, latest turns, short-lived phrasing, and immediate local state needed to answer naturally.
2. **Structured durable facts:** constraints, preferences, commitments, task state, business facts, and other critical context that must survive windowing, summarization, compaction, and session handoff.

The active context must include recent texture plus the durable fact block, while older transient turns are omitted from active context unless they are recoverable through a catalog handle. Durable facts are updated whenever a new critical fact appears; transient turns are not persisted just because they occurred.

```text
Incoming turn
     |
     v
+-----------------------+
| Classify new content  |
| durable or transient  |
+-----------------------+
     |                         
     | durable fact             transient turn
     v                         v
+-----------------------+   +-------------------------+
| Update durable store  |   | Keep only if recent     |
| with provenance       |   | or catalog as omitted   |
+-----------------------+   +-------------------------+
     |                         |
     +-----------+-------------+
                 v
        +----------------+
        | Context build  |
        | durable facts  |
        | recent turns   |
        | catalog IDs    |
        +----------------+
                 |
                 v
          Model call under
          token budget
```

## Canonical Contract

| Contract element | Requirement |
|---|---|
| Inputs | Recent conversation turns, current user request or objective, durable fact store, structured memory schema, and available token budget. |
| Durable fact block | Inject as a separate context block, not as rewritten transcript prose. [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]] lists durable state as its own block governed by freshness rules ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:30-40). |
| Recent texture block | Keep a bounded tail of recent turns for tone, deixis, unresolved local references, and current task flow. The token-budget source uses recent messages as the windowed part of selective history ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:197-210). |
| Durable update path | Extract critical facts, write them to an external store, load them on later turns, and merge them with current context. This follows [[docs/canonical/external-state-persistence|External State Persistence]]:31-57. |
| Omission path | Drop transient turns from active context once they are outside the recent window, unless exact recovery is needed through addressable memory. [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] defines `id`, `kind`, `location`, `preview`, `scope`, and `fetch` for omitted content ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43). |
| Output | A bounded active context containing recent conversational texture, structured durable facts, optional catalog previews, and no unbounded full transcript. |

## Durable Fact Rules

Persist facts when they can change future decisions. Do not persist turns only because they are old, emotionally salient, or expensive to re-read.

| Persist as durable fact | Drop or catalog as transient |
|---|---|
| Allergies, dietary restrictions, medical constraints, safety constraints | Greetings, acknowledgements, filler, social niceties |
| Budget, delivery constraints, preferred brands, excluded products, purchase history | One-off phrasing choices and tone from old turns |
| Commitments made by the agent, promised follow-ups, approvals, denials, unresolved decisions | Digressions that do not affect future choices |
| Current task state, open blockers, selected plan, accepted constraints, latest business state | Tool scratchpads and intermediate reasoning that are only useful inside the current turn |

This boundary follows the existing external-state distinction between allergies/preferences/commitments/critical history and greetings, digressions, temporary phrasing, or ephemeral scratchpads ([[docs/canonical/external-state-persistence|External State Persistence]]:59-65).

## Update, Freshness, and Provenance Rules

1. **Update on observation:** when a new user statement, tool result, evaluator finding, or business event changes a durable fact, write the new fact before the next context build.
2. **Attach provenance:** every durable fact should record its source turn, tool result, artifact, or owner. The memory graph pattern requires `source`, `owner`, `validity_scope`, retrieval keys, and `last_verified` so retrieved memory is not flattened into context without evidence ([[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:30-42).
3. **Track freshness:** facts that can expire need `last_verified`, validity scope, or equivalent freshness metadata before injection. Stable prompt reduction already treats durable state injection as freshness-governed ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:30-40).
4. **Do not overwrite silently:** when a new fact contradicts an older durable fact, keep enough provenance to explain which source superseded the other. If the conflict cannot be resolved automatically, inject the conflict as current task state instead of hiding it.
5. **Keep transient content recoverable only when needed:** if an omitted old turn may matter later but is not itself a durable fact, expose it through catalog metadata rather than re-injecting the full transcript ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:41-43).

## Context Assembly Order

Assemble selective history after the stable harness prompt and before generation. A practical order is:

1. Stable harness prompt and tool contracts.
2. Structured durable facts, with freshness and provenance metadata.
3. Current objective, unresolved task state, and latest tool/evaluator result.
4. Recent conversational texture within a fixed message or token budget.
5. Compact catalog previews for omitted content that can be fetched by handle.
6. Current user request.

This keeps the durable state from competing with the raw transcript. It also matches the hybrid token-budgeting lesson, which places critical client context, older summary, and recent window into separate layers ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:375-415), and the Phase 3 synthesis, which says stable critical facts, compressed older history, and recent conversational texture should not compete in one undifferentiated transcript ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:225-227).

## Tradeoffs

| Benefit | Cost | Mitigation |
|---|---|---|
| Keeps model input bounded without losing decision-critical facts | Fact extraction can miss important details | Test with N+1 long-session fixtures that require old facts after compaction ([[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]:28-40). |
| Durable facts survive windowing, summarization, and session handoff | Memory can become stale | Require freshness metadata and `last_verified` for facts that expire ([[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:30-42). |
| Recent turns preserve conversational texture and local references | Old nuance may disappear when turns are dropped | Store omitted content with catalog previews and exact fetch handles when nuance may matter ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43). |
| Separates stable state from transient transcript noise | Schema and provenance maintenance add operational overhead | Keep the durable schema focused on facts that change future decisions. |
| Makes context construction auditable | Contradictory facts require conflict handling | Preserve source and validity scope instead of overwriting silently. |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/external-state-persistence|External State Persistence]], because the durable fact store must extract, persist, reload, and merge critical state ([[docs/canonical/external-state-persistence|External State Persistence]]:31-57).
- **Depends on:** [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]], because durable state is a separate block and the stable harness must not be compacted as transcript payload ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:26-41).
- **Depends on:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]], because omitted non-durable turns need stable handles and previews rather than hidden loss ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- **Complements:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]], because this pattern defines what belongs in durable fact memory while head-tail truncation defines how to preserve anchors and recover omitted middle ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]:28-39).
- **Strengthened by:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]], because provenance, validity scope, and freshness make durable facts safer to inject ([[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:28-50).
- **Validated by:** [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]], because the pass condition is behavior after production context policy has run, not only staying under token budget ([[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]:28-40).

## Implementation in This Repo

### What already exists

- [[docs/canonical/external-state-persistence|External State Persistence]] defines the durable-memory loop: extract critical data, write to external store, load on next turn, merge with current context, and generate or evaluate ([[docs/canonical/external-state-persistence|External State Persistence]]:31-57).
- [[docs/canonical/external-state-persistence|External State Persistence]] distinguishes facts worth persisting from greetings, digressions, temporary phrasing, and ephemeral scratchpads ([[docs/canonical/external-state-persistence|External State Persistence]]:59-65).
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]] defines distinct context-builder blocks and includes durable state as a freshness-governed block ([[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:30-40).
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] defines stable handles and previews for omitted content ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- [[docs/system-of-record|System of Record]] lists those adjacent context and memory patterns as active canonical docs, including external state persistence, addressable memory catalog, stable harness prompt, and head-tail context truncation ([[docs/system-of-record|System of Record]]:130-163).

### What this doc canonicalizes

This document names the missing selective-history contract identified by Phase 3: active context is not full history, not blind windowing, and not durable state alone. It is the deliberate combination of recent conversational texture plus structured durable facts, with explicit update, freshness, provenance, and omission rules. That gap is the exact NOT_FOUND in the Phase 3 classification ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:44-50).

## References

- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:172-217 - full-history anti-pattern and selective-history example.
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:375-415 - hybrid context layers with critical context, summary buffer, and recent window.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:65-70 - selective history as recent history plus critical structured context.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:121-127 - operational lessons on degradation, buffers, and critical facts.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]:225-227 - synthesis that stable critical facts, older history, and recent texture should not compete in one transcript.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]:81-101 - extracted Durable Fact Selective History pattern.
- [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:44-50 - Partial Coverage classification and NOT_FOUND gap.
- [[docs/canonical/external-state-persistence|External State Persistence]]:31-65 - durable extraction, external store, merge, and persistence boundary.
- [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]]:30-40 - context blocks and durable-state freshness injection.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43 - omitted-memory handles, previews, and exact fetch contract.

---

*Created: 2026-06-10 | From: Token Budgeting pattern classification | Precedence: canonical*
