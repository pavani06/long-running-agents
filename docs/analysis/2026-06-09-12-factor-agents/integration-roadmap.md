# Integration Roadmap: 12-Factor Agents Patterns → long-running-agents

**Date:** 2026-06-09
**Type:** Analysis
**Precedence:** Level 4 (`docs/system-of-record.md:10`)
**Source:** `docs/analysis/2026-06-09-12-factor-agents/classification.md`

---

## Objective

Map each of the 8 agentic patterns extracted from Dex Horthy's "12-Factor Agents" talk to concrete integration points in the long-running-agents curriculum, codebase, and future roadmap. Prioritize by impact and implementation effort.

## Summary Matrix

| # | Pattern | Classification | Impact | Effort | Priority | Integration Surface |
|---|---|---|---|---|---|---|
| 6 | Error Context Hygiene | **Missing** | High | Low | **P0** | New skill, canonical doc, curriculum exercise |
| 2 | Deterministic Tool Dispatch | Partial | Medium | Low | P1 | Curriculum reframe, naming convention |
| 3 | Owned Agent Control Loop | Partial | Medium | Medium | P1 | Curriculum module, architectural ADR |
| 4 | Serializable Pause/Resume State | Partial | Medium | Medium | P2 | Canonical doc, complementary mechanism |
| 7 | Human Contact Intent Tool | Partial | Medium | High | P3 | Domain-specific, low urgency |
| 1 | Structured Output Contract | Exists | — | — | — | Already covered |
| 5 | Token-Level Prompt & Context Builder | Exists | — | — | — | Repo exceeds depth |
| 8 | Micro-Agent Islands in DAG | Exists | — | — | — | Architectural thesis |

---

## Artifacts Created (2026-06-09)

### New Documentation (Canonical) — `docs/canonical/`

| File | Pattern | Category |
|---|---|---|
| `error-context-hygiene.md` | 6 | New Pattern, New Documentation |
| `deterministic-tool-dispatch.md` | 2 | New Pattern, New Documentation |
| `owned-agent-control-loop.md` | 3 | New Pattern, New Agent Architectures |
| `serializable-pause-resume-state.md` | 4 | New Pattern, New Documentation |

### New Skill — `.opencode/skills/`

| Directory | Pattern | Category |
|---|---|---|
| `error-context-hygiene/SKILL.md` | 6 | New Skill, New Runtime Features |

### New Analysis — `docs/analysis/`

| File | Scope |
|---|---|
| `2026-06-09-integration-roadmap.md` (this file) | Cross-cutting roadmap |

### New Exercise — `curriculum/`

| File | Pattern | Category |
|---|---|---|
| `02-nivel-2-practical-patterns/exercises/exercise-04-error-context-hygiene.md` | 6 | New Exercise, New Examples |

---

## Detailed Integration Plan

### P0: Error Context Hygiene (Missing → Fill the gap)

**Why P0:** Only pattern classified as Missing. Addresses documented failure mode (context pollution → spiral-out) in the harness diagnostic and nivel-2 diagnostic.

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Authoritative pattern description | `docs/canonical/error-context-hygiene.md` | Done |
| Implementation skill | Skill for agents to apply hygiene rules | `.opencode/skills/error-context-hygiene/SKILL.md` | Done |
| Curriculum exercise | Scenario-based exercise for Nivel 2 | `curriculum/.../exercise-04-error-context-hygiene.md` | Done |
| Nivel 2 module | Add "Error Context Hygiene" topic | `curriculum/02-nivel-2-practical-patterns/05-error-context-hygiene.md` | Future |
| Core Concept 9 | If patterns grow beyond 8 core concepts | `curriculum/05-core-concepts/09-error-context-hygiene.md` | Future |
| mhc-backend | Implement hygiene in `OrchestratorAgent` error handling | Code change (separate issue) | Future |
| Harness diagnostic update | Re-evaluate Fallback & Retry with hygiene lens | `docs/analysis/mhc-backend/` | Future |

### P1: Deterministic Tool Dispatch (Partial → Formalize reframe)

**Why P1:** Mechanics exist, naming/reframe missing. Low effort, high teaching value.

| Integration Point | Action | Status |
|---|---|---|
| Canonical doc | Pattern with reframe and testing guidance | Done |
| Nivel 2, sprint-contracts.md | Add sidebar: "Tools are JSON + Code" | Future |
| Core Concept 4 (Sprint Contracts) | Add "Deterministic Dispatch" sub-pattern | Future |
| Nivel 2 exercise-02 | Add step: "Test your dispatch handler with a JSON fixture — no LLM" | Future |

### P1: Owned Agent Control Loop (Partial → Add decomposition)

**Why P1:** 4-component decomposition adds precision to existing harness teaching.

| Integration Point | Action | Status |
|---|---|---|
| Canonical doc | Pattern with 4 components + intervention points | Done |
| Nivel 3, harness-evolution.md | Add "Loop Ownership vs. Framework Delegation" section | Future |
| ADR candidate | Decision: own the loop or delegate to LangGraph? | Future |
| New agent architecture | Example of an owned loop (not LangGraph-based) | Future |

### P2: Serializable Pause/Resume State (Partial → Complementary mechanism)

**Why P2:** Repo has richer state model. 12FA serialization is complementary, not replacement.

| Integration Point | Action | Status |
|---|---|---|
| Canonical doc | Comparison of both approaches with when-to-use guidance | Done |
| Core Concept 5 (State Persistence) | Add "Pause/Resume vs. Rebuild" comparison | Future |
| ADR candidate | Decision: when to use serialization vs. rebuild | Future |

### P3: Human Contact Intent Tool (Partial → Niche, low urgency)

**Why P3:** Domain-appropriate alternatives exist (WhatsApp flow model). The first-token mechanism is clever but niche.

| Integration Point | Action | Status |
|---|---|---|
| Nivel 4, customer-journey-flows.md | Add design rationale for WhatsApp flow vs. intent-token routing | Future |
| No blocking action | Current model is appropriate for domain | — |

---

## Impact by Category

| Category | Artifacts Created | Highest-Value Gap Addressed |
|---|---|---|
| **New Skills** | `error-context-hygiene` skill | Pattern 6 implementation guidance |
| **New Patterns** | 4 canonical docs | All 4 partial/missing patterns formalized |
| **New Examples** | Exercise scenario (error trace before/after) | Pattern 6 operational example |
| **New Exercises** | `exercise-04-error-context-hygiene.md` | Pattern 6 hands-on practice |
| **New Documentation** | Integration roadmap + 4 canonical docs | First canonical docs in repo |
| **New Agent Architectures** | Control loop 4-component decomposition | Pattern 3 architectural precision |
| **New Runtime Features** | Error hygiene rules (summarize, clear, format) | Pattern 6 operational patterns |

---

## Precedence Alignment

Per `docs/system-of-record.md`:

- **Level 2 (canonical):** `docs/canonical/` now contains 4 pattern docs — the first canonical content in the repo. These take precedence over analysis docs and READMEs.
- **Level 4 (analysis):** This roadmap and the classification doc remain at analysis level — they inform but don't override canonical docs.
- **Level 1 (ADRs):** `docs/decisions/` remains empty. The "loop ownership vs. framework delegation" question is the strongest ADR candidate from this work.

## Future ADR Candidates

From the pattern analysis, these decisions warrant formal ADRs:

1. **Loop ownership model** — Own the agent control loop directly vs. delegate to LangGraph. Tradeoffs: control vs. framework optimizations.
2. **State serialization strategy** — Context window serialization vs. state rebuild from DB. Tradeoffs: token fidelity vs. state richness.
3. **Error handling layer separation** — Infrastructure-level (retry, fallback) vs. context-level (hygiene, curation). Are they separate concerns or should they be unified?

## References

- `docs/analysis/2026-06-09-12-factor-agents/classification.md` — full classification with evidence
- `docs/analysis/2026-06-09-12-factor-agents/patterns.md` — 8 pattern definitions with 6 fields each
- `docs/analysis/2026-06-09-12-factor-agents/analysis.md` — non-obvious knowledge extraction
- `docs/canonical/error-context-hygiene.md` — canonical pattern doc
- `docs/canonical/deterministic-tool-dispatch.md` — canonical pattern doc
- `docs/canonical/owned-agent-control-loop.md` — canonical pattern doc
- `docs/canonical/serializable-pause-resume-state.md` — canonical pattern doc
- `docs/system-of-record.md` — documentation precedence

---

*Created: 2026-06-09 | From: Pattern Classification analysis | Precedence: analysis*
