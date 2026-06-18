---
title: Cross-Context Knowledge Siloing
type: canonical
aliases:
  - silos de conhecimento cross-contexto
  - knowledge siloing
  - cross-boundary knowledge
  - namespace isolation
  - buried knowledge
tags:
  - knowledge-management
  - cross-session
  - session-handoff
  - durable-facts
  - context-engineering
last_updated: 2026-06-17
relates-to:
  - "[[docs/canonical/durable-fact-selective-history|Durable Fact Selective
    History]]"
  - "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]"
  - "[[docs/canonical/external-state-persistence|External State Persistence]]"
  - "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]"
  - "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session
    Handoff]]"
sources:
  - "[[vault:sisyphus-runtime/sessions/_global/2026-06-17-sisyphus-paths-update\
    -handoff|Paths Update Session]]"
  - "[[vault:sisyphus-runtime/sessions/a-casa-conta/2026-06-17-sisyphus-handoff\
    |a-casa-conta T1 Session]]"
  - "[[vault:sisyphus-runtime/facts/_global/paths|Path Mappings Durable Fact]]"
---

# Cross-Context Knowledge Siloing

**Type:** Canonical Pattern
**Status:** Active
**Source:** [[vault:sisyphus-runtime/sessions/_global/2026-06-17-sisyphus-paths-update-handoff|Paths Update Session]] and [[vault:sisyphus-runtime/sessions/a-casa-conta/2026-06-17-sisyphus-handoff|a-casa-conta Session]]
**Classification:** Full Coverage — two sub-patterns with concrete evidence and mitigation strategies
**Precedence:** Level 2 canonical per `docs/system-of-record.md`

---

## Problem

Knowledge created in one agent context becomes invisible to agents operating in a different context, causing repeated investigation of already-solved problems. This is not a failure of memory persistence — the knowledge exists in the system. It is a failure of **discoverability**: the retrieval path that works for the creating context does not work for the consuming context.

The failure manifests in two distinct forms:

1. **Namespace-bound isolation**: knowledge created in a repo-specific session (e.g., `a-casa-conta`) that has cross-domain applicability (e.g., filesystem access patterns) is invisible to sessions in a different namespace (`_global`).
2. **Unstructured body burial**: knowledge documented in the **body** of a handoff or durable fact is invisible to structured queries that only index frontmatter fields, even when the handoff is in the correct namespace.

Both forms share the same root cause: the metadata that makes knowledge *retrievable* (frontmatter tags, repo namespace, memory_handles) is decoupled from the content that makes knowledge *valuable* (handoff body sections, discovered methods, cross-cutting insights).

## Solution

Introduce a **knowledge promotion pipeline** that runs at handoff time and when canonical-context loads context. The pipeline detects knowledge with cross-boundary applicability and promotes it from its creation context to a globally discoverable form.

The pipeline has two stages:

### Stage 1: Cross-namespace promotion (at handoff time)

When `session-handoff` creates a handoff in a repo-specific namespace, scan the handoff body for sections with cross-domain applicability (filesystem paths, tool configurations, environment patterns, access methods). Promote qualifying discoveries to `memory_handles` with `scope: "cross-session"` and, if the knowledge is truly global, create or update a durable fact in `_global`.

Detection heuristics for cross-domain content:
- Filesystem paths (`/mnt/`, `G:`, `shortcut-targets-by-id`)
- Tool executable paths (`powershell.exe`, `wslpath`)
- Environment configuration patterns
- Access methods that don't depend on repo-specific domain knowledge

### Stage 2: Body-to-frontmatter indexing (at canonical-context load time)

When `canonical-context` searches for relevant context and structured queries return empty, execute a full-text fallback (`rg`) on handoff bodies in the vault. Promote matches to `memory_handles` or `relevance_log` entries so the knowledge becomes reachable in future structured queries.

The full-text fallback should be scoped and cost-aware:
- Only execute when structured query returns 0 results for a non-trivial search term
- Limit to handoff files in the current repo namespace first, then expand cross-repo
- Cache results in `relevance_log` to avoid repeated full-text scans

### Memory handle contract extension

Extend `memory_handles` entries with a `discovered_in` field that records where the knowledge was found, enabling traceability:

```json
{
  "id": "gdrive-powershell-method",
  "kind": "discovery",
  "location": "sessions/a-casa-conta/2026-06-17-sisyphus-handoff.md",
  "preview": "PowerShell shortcut-targets-by-id method for G: drive access",
  "scope": "cross-session",
  "tool": "read",
  "path": "~/sisyphus-runtime/facts/_global/paths.md",
  "discovered_in": {
    "repo": "a-casa-conta",
    "section": "Repo Access",
    "date": "2026-06-17"
  }
}
```

## Evidence

### Case Study: G: Drive PowerShell Method

**Timeline (2026-06-17, single day, 3 sessions):**

| Session | Repo | What happened |
|---|---|---|
| 1. a-casa-conta T1 | `a-casa-conta` | Discovered PowerShell + `shortcut-targets-by-id` method for G: access. Documented in handoff body section "Repo Access". Did NOT create a durable fact. |
| 2. G: Drive Path Mapping | `_global` | User reported agent couldn't remember G: access pattern. Investigated from scratch. Created `facts/_global/paths.md` with only WSL auto-mount method (`/mnt/g/`). Full-text search NOT performed on cross-repo handoffs. |
| 3. Drive Investigation | `_global` | User asked again about G: access. Exhaustive search (21 handoffs, session_search, shell history) found nothing — because the search was namespaced to `_global`. |
| 4. Paths Update (this session) | `_global` | User mentioned "a-casa-conta session found a method." Cross-repo search of a-casa-conta handoff v1 revealed the PowerShell method. Updated `paths.md`. **Total tokens wasted across sessions 2-3: ~3 handoffs re-investigating solved problem.** |

**Root cause chain:**
1. Session 1 discovered method → documented in handoff body (unstructured)
2. Session 1 handoff was in `a-casa-conta` namespace (cross-repo invisible)
3. Session 2 `canonical-context` queried only `_global` handoffs → empty result
4. Session 2 created incomplete durable fact (only WSL method, not PowerShell)
5. Session 3 `canonical-context` loaded the incomplete durable fact → user still stuck
6. Session 4 manual cross-repo investigation finally found the method

**What should have happened:**
1. Session 1 handoff → Stage 1 promotion detects "Repo Access" section with filesystem path patterns → creates/updates `facts/_global/paths.md` with PowerShell method
2. Session 2 `canonical-context` → Stage 2 full-text fallback on cross-repo handoffs → finds PowerShell method → surfaces it
3. Sessions 2-3 saved: ~2 handoffs of redundant investigation eliminated

## Sub-Pattern 1: Namespace-Bound Knowledge Isolation

**Trigger**: A session in repo-specific namespace discovers knowledge with cross-domain applicability.

**Failure mode**: The knowledge is persisted in the repo-specific handoff/state but is invisible to `canonical-context` queries scoped to a different repo.

**Detection**: When a handoff body contains sections like "Repo Access", "Environment Setup", "Tool Configuration", or patterns matching filesystem paths, tool executables, or platform-specific access methods.

**Mitigation**: Stage 1 promotion pipeline at handoff time. The `session-handoff` skill scans the handoff body for cross-domain patterns and promotes qualifying discoveries to `_global` durable facts or cross-session memory handles.

## Sub-Pattern 2: Unindexed Body Knowledge Burial

**Trigger**: Valuable knowledge is documented in the body of a handoff or durable fact but not surfaced in frontmatter fields (tags, memory_handles, summary_buffer).

**Failure mode**: `obsidian-eval query` only indexes frontmatter. Structured queries return empty even when the knowledge exists in the vault. Full-text search (`rg`) would find it, but the canonical-context workflow doesn't include a full-text fallback.

**Detection**: When structured queries return 0 results for a search term that should have matches, and a subsequent `rg` on the vault finds the term in handoff bodies.

**Mitigation**: Stage 2 full-text fallback in `canonical-context`. When structured queries return empty, execute a scoped `rg` on the vault. Promote matches to structured form (memory_handles, relevance_log) to prevent future misses.

## Implementation

### Phase 1: session-handoff body scanner

Add a post-write hook to `session-handoff` skill that scans the handoff body for cross-domain patterns before finalizing:

```bash
# Cross-domain pattern detection (run before write)
CROSS_DOMAIN_SECTIONS=$(grep -nE '(Repo Access|Environment|Paths? Mapping|Tool (Configuration|Paths?)|Access (Method|Pattern))' "$HANDOFF_BODY_FILE")
if [ -n "$CROSS_DOMAIN_SECTIONS" ]; then
  # Flag for promotion review
  echo "WARNING: cross-domain sections detected — consider promoting to _global durable fact"
fi
```

### Phase 2: canonical-context full-text fallback

Add a full-text fallback step between Passo 2 (structured query) and Passo 3 (scoring) in `canonical-context`:

```bash
# After structured query returns empty for non-trivial search
if [ "$STRUCTURED_RESULTS_COUNT" -eq 0 ] && [ -n "$SEARCH_TERM" ]; then
  # Full-text fallback on vault
  RG_RESULTS=$(rg -li "$SEARCH_TERM" ~/sisyphus-runtime/sessions/ 2>/dev/null | head -10)
  if [ -n "$RG_RESULTS" ]; then
    # Promote to relevance_log for future structured queries
    echo "Full-text fallback found $RG_RESULTS — promoting to relevance_log"
  fi
fi
```

### Phase 3: memory_handles promotion automation

When a cross-domain discovery is promoted to a `_global` durable fact, automatically add a `memory_handle` entry in the promoting handoff so future sessions can trace the discovery chain:

```json
{
  "id": "promoted-gdrive-method",
  "kind": "promotion",
  "location": "facts/_global/paths.md",
  "preview": "PowerShell G: method promoted from a-casa-conta session",
  "scope": "cross-session",
  "tool": "read",
  "path": "~/sisyphus-runtime/facts/_global/paths.md",
  "promoted_from": "sessions/a-casa-conta/2026-06-17-sisyphus-handoff.md"
}
```

## Tradeoffs

| Dimension | Benefit | Cost |
|---|---|---|
| **Recall** | Cross-domain knowledge no longer lost between namespaces | Additional processing at handoff time (~50-100 tokens for pattern scanning) |
| **Precision** | Full-text fallback catches knowledge that structured queries miss | `rg` on vault adds ~200ms latency per fallback query |
| **Storage** | Promoted facts prevent redundant investigation | Vault grows with promotion metadata (negligible: ~200 bytes per promotion) |
| **Complexity** | Pipeline is additive — doesn't change existing handoff/query behavior | Two new code paths to maintain (body scanner, full-text fallback) |
| **False positives** | Cross-domain detection may flag repo-specific content | Manual review gate before promotion (acceptable for low-frequency operation) |

## See Also

- [[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]] — principles for what knowledge deserves durable storage
- [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]] — structured metadata for knowledge retrieval
- [[docs/canonical/external-state-persistence|External State Persistence]] — why in-context memory alone fails
- [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] — graph-based knowledge representation across sessions
- [[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]] — handoff payload contract
- [[vault:sisyphus-runtime/facts/_global/paths|Path Mappings]] — concrete example of promoted cross-domain knowledge