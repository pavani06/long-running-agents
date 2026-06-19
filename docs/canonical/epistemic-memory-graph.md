---
title: "Epistemic Memory Graph"
type: canonical
tags: ["context-engineering", "agentes-orquestracao"]
aliases: ["belief-status memory graph", "epistemic graph memory", "belief-aware retrieval"]
last_updated: 2026-06-19
relates-to: ["[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]]", "[[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Stanford CS153 Classification]]", "[[curriculum/06-knowledge-graphs/01-concept-ecosystem|Concept Ecosystem]]"]
sources: ["[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Agentic Patterns from Stanford CS153 AI Native Company]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|Classification: Stanford CS153 AI Native Company Patterns]]"]
---
# Epistemic Memory Graph

**Type:** canonical
**Status:** active
**Source:** analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/
**Classification:** Partial Coverage, Medium integration value
**Precedence:** document-level 2 (canonical) per [[docs/system-of-record|System of Record]]

---

## Problem

As agent memory grows, grep, flat notes, and undifferentiated vector retrieval flatten very different kinds of knowledge into the same retrieval surface. A confirmed fact, a user's personal belief, a team hunch, a stale assumption, and world knowledge can all look like equally usable context once retrieved.

Long-running agents need memory that preserves epistemic status. Without belief labels, source provenance, and graph relationships, agents can act on speculation as if it were fact or ignore useful hypotheses because they are not connected to the workflow where they matter.

## Solution

Represent operational memory as a graph whose nodes carry both retrieval metadata and epistemic labels.

Minimum node fields:

| Field | Purpose |
|---|---|
| `id` | Stable handle for citation, retrieval, and audit |
| `kind` | Decision, fact, hunch, person-specific belief, world knowledge, observation, incident, source artifact, or open question |
| `epistemic_status` | Confirmed, inferred, contested, stale, hypothesis, preference, policy, or unknown |
| `source` | Repo file, trace, conversation, meeting note, customer artifact, evaluator output, or external source |
| `owner` | Person, agent, team, or domain owner responsible for updates |
| `validity_scope` | Product area, customer, session, time window, or workflow boundary where the memory applies |
| `retrieval_keys` | Keywords, embeddings, backlinks, graph edges, and related handles |
| `last_verified` | Timestamp or evidence pointer for freshness checks |

Retrieval should combine multiple signals instead of relying on one lookup mode:

1. Search for exact keywords and stable IDs.
2. Retrieve semantically similar nodes through embeddings.
3. Follow backlinks and explicit graph edges to adjacent decisions, incidents, rubrics, and workflow concepts.
4. Fuse ranked candidates from search, vector retrieval, backlinks, and graph traversal.
5. Return epistemic labels with every result so the agent can distinguish fact, belief, hypothesis, and stale memory before acting.
6. Govern ontology changes through ownership and migration rules so new domains can add useful labels without fragmenting memory.

## Implementation in this repo

### What already exists

The repo already has structural memory and graph foundations:

- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] says external memory must expose compact information so the agent can choose what to retrieve without reloading all history:22-24.
- The same canonical pattern defines stable IDs, kind, location, preview, scope, and fetch contract for omitted memory in [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] cites adjacent retrieval, privacy and scope filters, output refs, manifests, and prior memory-store mechanics:51-55.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] also records that the repo still lacks an explicit omitted-memory catalog implementation and observability for offered and fetched IDs:57-66.
- Knowledge graphs are framed as a connected ecosystem of concepts rather than isolated techniques in [[curriculum/06-knowledge-graphs/01-concept-ecosystem|Concept Ecosystem]]:75-91.
- The graph template defines knowledge graphs as methodical diagrams for dependencies, operational order, and maturity timelines in [[curriculum/08-tools-templates/knowledge-graph-template|Knowledge Graph Template]]:51-60.

### What was implemented (2026-06-19)

The Fase C3 implementation (`obsidian-eval` module) addresses items 1, 3, and 4 from the gap analysis. Item 2 (hybrid vector retrieval) is deferred to Phase 2.

**Implementation plan:** `.omo/plans/2026-06-19-epistemic-memory-graph.md`

**Location:** `obsidian-eval/src/`

| Module | Lines | Responsibility |
|---|---|---|
| `epistemic-types.ts` | 59 | `EpistemicNode` (8 canonical fields), `EpistemicEdge`, `EpistemicStatus` (8 labels), `NodeKind` (13 categories) |
| `entity-extractor.ts` | 178 | `extractFromNote()` extracts Session, Decision, FileRef, SkillUse from handoffs; Fact from durable-facts. Deterministic, zero LLM. Maps `confidence` → epistemic status, `valid_to` → stale. |
| `epistemic-graph.ts` | 180 | `EpistemicGraph` class: `build()`, `backlinks()`, `forwardLinks()`, `affectedBy()`, `mostModifiedFiles()`, `contestedFacts()`, `staleFacts()`, `hypotheses()`, `decisionsByRepo()`, `sessionContext()`, `stats()` |

**CLI integration:** `obsidian-eval/src/cli.ts` — three subcommands:
- `epistemic build` — scans vault, builds graph, caches to `~/.cache/obsidian-eval/`
- `epistemic query <keyword>` — queries the graph (affectedBy, mostModifiedFiles, staleFacts, etc.)
- `epistemic stats` — prints summary (node kinds, edge kinds, epistemic statuses, repos)

**Test coverage:** 29 tests across 4 suites (`test/epistemic-*.test.ts`), all passing.

**Validated against real vault:** `~/sisyphus-runtime/` yields 174 nodes (19 sessions, 45 decisions, 55 file refs, 11 facts, 42 skill uses), 191 edges, across 4 repos (`_global`, `a-casa-conta`, `long-running-agents`, `obsidian-eval`).

**Example queries:**
```bash
obsidian-eval ~/sisyphus-runtime epistemic query budget-monitor
# → 2 decisions referencing budget-monitor

obsidian-eval ~/sisyphus-runtime epistemic query mostModifiedFiles
# → session-handoff/SKILL.md (5×), reflection-run.ts (4×), canonical-context/SKILL.md (3×)
```

**Still missing (Phase 2):**
- Hybrid retrieval fusing keyword search, vector embeddings, backlinks, and graph traversal into ranked results.
- Integration with `canonical-context` skill for automated context injection.

## Tradeoffs

| Benefit | Cost |
|---|---|
| Helps agents distinguish facts from hunches before acting | Adds schema and ontology governance overhead |
| Improves retrieval as memory volume grows across artifacts | Requires maintenance of graph edges and freshness metadata |
| Supports workflow-specific memory without flattening all knowledge | Dynamic ontologies can fragment without ownership rules |
| Creates better audit trails for why an agent trusted a memory item | Retrieval fusion does not fix inaccurate source material |

## Relationship to Other Patterns

- **Extends:** [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] by adding epistemic labels and graph relationships to stable memory handles.
- **Supports:** [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] when omitted context must be recovered with belief status intact.
- **Feeds:** [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]] by preserving whether a failure came from stale memory, contested belief, or missing source evidence.
- **Builds on:** [[curriculum/06-knowledge-graphs/01-concept-ecosystem|Concept Ecosystem]] and [[curriculum/08-tools-templates/knowledge-graph-template|Knowledge Graph Template]] for graph thinking.
- **Comes from:** [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|Stanford CS153 Patterns]]:182-201 and its Partial Coverage classification in [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|classification]]:140-155.

## References

- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns|patterns]]:182-201 - extracted pattern definition.
- [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification|classification]]:140-155 - Partial Coverage classification and epistemic-memory gap.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:22-24 - existing need for compact retrieval choice.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43 - existing addressable catalog schema.
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:57-66 - current missing implementation details.
- [[curriculum/06-knowledge-graphs/01-concept-ecosystem|Concept Ecosystem]]:75-91 - existing knowledge-graph framing.
- [[curriculum/08-tools-templates/knowledge-graph-template|Knowledge Graph Template]]:51-60 - existing graph-template mechanics.

---

*Created: 2026-06-10 | Implemented: 2026-06-19 | From: Stanford CS153 pattern classification | Precedence: canonical*
