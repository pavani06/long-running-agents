---
title: 'Semantic Topic Bucketing'
type: canonical
aliases: ["agrupamento semantico", "topic bucketing", "semantic grouping", "topical summarization"]
tags: ["context-engineering", "agentes-orquestracao"]
last_updated: 2026-06-10
relates-to: ["[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]"]
sources: ["[[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]"]
---

# Semantic Topic Bucketing

**Type:** Canonical Pattern
**Status:** Active
**Source:** curriculum/01-nivel-1-fundamentals/02-token-budgeting.md
**Classification:** Missing
**Precedence:** Level 2 (docs/system-of-record.md)

---

## Problem

A raw chronological transcript makes unrelated concerns compete inside one retention path. The token-budgeting analysis names the failure directly: raw chronological history mixes topics, which makes selective retention harder, while the extracted pattern says chronological transcripts mix unrelated topics and make selective retention and summarization brittle ([[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:95-101; [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:169-181).

The concrete failure appears when a long shopping conversation contains price negotiation, allergy constraints, delivery timing, and recommendation details across many turns. The source lesson shows price messages and allergy messages as separate semantic groups that should be summarized independently instead of left interleaved in chronology ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:323-343).

The root cause is not only token pressure. It is that a single chronological summary has no topic-level retention policy: the system cannot decide that allergy facts should be durable, price discussion should be compact, delivery details should be refreshed near checkout, and low-value chatter should expire. The extracted pattern therefore requires a domain-specific topic taxonomy, assignment mechanism, per-topic retention policy, and mappings from active summaries back to source spans or memory handles ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:173-181).

## Solution

Classify conversation messages, tool outputs, and trace events into semantic buckets, summarize each bucket independently, and preserve a source-span mapping for every retained summary. The source analysis describes the mechanism as classifying messages into topical buckets and summarizing each topic group independently, while the extracted pattern generalizes the inputs to messages, tool outputs, trace events, a topic taxonomy, a classifier, and per-topic summary or retention policy ([[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:95-101; [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:173-181).

```text
Chronological transcript / tool outputs / trace events
        |
        v
+-------------------------+
| Topic assignment        |
| taxonomy + classifier   |
+-----------+-------------+
            |
            v
+-------------------------+
| Bucket store            |
| price, allergies,       |
| delivery, recommendations
+-----------+-------------+
            |
            v
+-------------------------+
| Per-topic policy        |
| summarize, retain,      |
| expire, or fetch exact  |
+-----------+-------------+
            |
            v
+-------------------------+
| Active context          |
| topic summaries +       |
| source-span handles     |
+-------------------------+
```

| Component | Rule |
|---|---|
| Topic taxonomy | Use workflow-native topics such as preferences, constraints, orders, delivery, recommendations, price, or allergies when they recur in the domain ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:183-189; [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:349-354). |
| Topic assignment | Assign each message, tool output, or trace event to one or more buckets; multi-topic messages need duplication or handles so critical information is not lost ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:173-189). |
| Per-topic summary | Summarize each topic group independently instead of producing one chronological summary ([[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:95-101; [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:323-343). |
| Retention policy | Decide per bucket whether to retain facts, compact discussion, refresh from source, or omit low-value material; this follows the extracted pattern's per-topic retention policy requirement ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:173-181). |
| Source-span mapping | Keep source spans or memory handles behind every active summary so later decisions can recover exact evidence ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:179-181; [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43). |

Before Semantic Topic Bucketing, active context receives a mixed sequence: `msg1 price`, `msg2 allergy`, `msg3 delivery`, `msg4 price`, `msg5 recommendation`. A single summary can blur which constraints are durable and which details are only negotiation context; the analysis identifies summary information loss as a failure mode when later-relevant details are removed, and it recommends topic-aware summaries for older content ([[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:207-217).

After Semantic Topic Bucketing, active context receives bucket summaries such as `allergies: gluten, corn syrup, lactose`, `price: asks about discounts and volume`, and `delivery: unresolved shipping constraints`, each with source-span handles. The source lesson uses exactly this shape for price and allergy groups, and the extracted pattern requires the output to include topic-specific buckets, per-bucket summaries, and mappings back to source spans or memory handles ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:327-343; [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:179-181).

## Implementation in this repo

### What already exists

- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] introduces Semantic Bucketing as one of five token-budgeting strategies and frames it as grouping related information before summarization ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:221-224; [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:323-325).
- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] gives the concrete price/allergy example and a sketch that detects a topic for each message, appends it to `topics[topic]`, then summarizes each group ([[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:327-362).
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]] records Semantic Bucketing as a pattern whose mechanism is classifying messages into topical buckets and summarizing each topic group independently ([[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:95-101).
- [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]] formalizes the pattern inputs as conversation messages, tool outputs, trace events, a topic taxonomy, assignment rules, and per-topic summary or retention policy ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:169-181).
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] defines stable handles, locations, previews, scopes, and fetch contracts for omitted content, which can back the source-span mappings of topic summaries ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] defines memory nodes with epistemic status, source provenance, validity scope, retrieval keys, and graph traversal, which can label the trust status of facts extracted into buckets ([[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:28-50).
- [[docs/canonical/external-state-persistence|External State Persistence]] distinguishes durable external facts such as allergies, preferences, budget, delivery constraints, commitments, and purchase history from greetings, filler, digressions, and temporary phrasing ([[docs/canonical/external-state-persistence|External State Persistence]]:59-65).
- [[docs/system-of-record|System of Record]] gives active canonical docs Level 2 precedence above evidence, analysis, archive, READMEs, plans, agent definitions, and operational summaries ([[docs/system-of-record|System of Record]]:14-21).

### What is missing

1. No active canonical doc defines a topic taxonomy for grouping conversation messages, tool outputs, or trace events; the classification records Semantic Topic Bucketing as `Missing` after reading the system of record and canonical docs ([[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]:84-90).
2. No canonical doc defines per-topic summary and retention policy for topic buckets; the classification says closest memory docs provide handles, kinds, scopes, labels, provenance, graph retrieval, and durable categories, but not topic-bucketed retention or summarization ([[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]:88-90).
3. No canonical doc maps active bucket summaries back to source spans or memory handles as a required invariant; the extracted pattern lists this mapping as a required output, while the classification says the canonical gap remains ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:179-181; [[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]:84-90).
4. No canonical doc specifies how to handle messages that span multiple topics; the extracted limitations say multi-topic messages may need duplication or source handles to avoid loss ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:186-189).
5. No canonical doc defines taxonomy maintenance as workflows evolve; the extracted limitations identify taxonomy maintenance as necessary when the workflow changes ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:186-189).

## Tradeoffs

| Benefit | Cost |
|---|---|
| Preserves logical structure better than one chronological summary ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:182-185) | Depends on reliable topic classification ([[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:159-164) |
| Lets the agent retrieve or refresh only the topic needed for the next decision ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:182-185) | Multi-topic messages require duplication or source handles to avoid loss ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:186-189) |
| Fits structured domains with recurring themes such as preferences, constraints, orders, delivery, or recommendations ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:182-185) | Bucket taxonomies need maintenance as the workflow evolves ([[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:186-189) |
| Supports topic-aware summaries for older content when summary information loss is a risk ([[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:207-217) | Cannot replace exact recoverability when later audit requires original wording or tool output ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:24-39) |

## Relationship to Other Patterns

- **Depends on:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] for stable source handles and exact fetch contracts behind bucket summaries ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43), and [[docs/canonical/external-state-persistence|External State Persistence]] for durable fact categories that should survive beyond a topic summary ([[docs/canonical/external-state-persistence|External State Persistence]]:31-65).
- **Validated by:** [[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]], because the N+1 turn tests whether the right earlier information survived or can be recovered after the production context strategy runs ([[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]:28-40), and [[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]], because late-session failures should preserve session shape, context strategy, expected N+1 behavior, and root-cause category ([[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]:28-42).
- **Complements:** [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] by adding topic structure while the graph adds epistemic labels, provenance, validity scope, retrieval keys, and graph relationships ([[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:28-50), and [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]] by making omitted middle content easier to summarize and recover by topic rather than only by chronological span ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:28-39).

## References

- [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]:323-371 — original lesson section for Semantic Bucketing, example groups, implementation sketch, tradeoffs, and best fit.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:95-101 — extracted Semantic Bucketing problem, mechanism, and best fit.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:159-164 — Semantic Bucketing tradeoff in the analysis.
- [[docs/analysis/2026-06-10-token-budgeting/analysis|Knowledge Extraction]]:207-217 — summary information loss and topic classifier weakness failure patterns.
- [[docs/analysis/2026-06-10-token-budgeting/patterns|Token Budgeting Patterns]]:169-189 — formalized inputs, outputs, benefits, and limitations for Semantic Topic Bucketing.
- [[docs/analysis/2026-06-10-token-budgeting/classification|Token Budgeting Classification]]:84-90 — Missing classification and adjacent-doc evidence.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43 — stable handles, locations, previews, scopes, and fetch contracts.
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:28-50 — epistemic labels, source provenance, graph edges, and retrieval fusion.
- [[docs/canonical/external-state-persistence|External State Persistence]]:59-65 — durable versus non-durable external state categories.
