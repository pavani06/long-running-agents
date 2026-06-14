---
title: "Integration Roadmap: Context Management Patterns -> long-running-agents"
type: analysis
date: 2026-06-09
domain: context-management
aliases: ["roadmap contexto", "plano contexto", "integracao context management", "N+1"]
tags: [analise, context-engineering, context-management, roadmap]
last_updated: 2026-06-10
relates-to: ["[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification|Context Mgmt Classification]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]", "[[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]"]
---

> [!warning] Formato legado
> Este arquivo usa o formato histórico `integration-roadmap.md`.
> Sessões a partir de 2026-06-14 usam `<date>-<source-slug>-artifacts.{md,yaml}`.
> Preservado para rastreabilidade e estabilidade de wikilinks.

# Integration Roadmap: Context Management Patterns -> long-running-agents

**Date:** 2026-06-10
**Type:** Analysis
**Precedence:** Level 4 (`docs/system-of-record.md:10`)
**Source:** `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md`

---

## Objective

Map the 7 classified context-management patterns to concrete integration points in `long-running-agents`: canonical docs, curriculum levels, implementation guides, skills, exercises, eval gates, and remaining gaps. This roadmap follows the repository precedence model: canonical docs in `docs/canonical/` outrank analysis docs, while this file remains an analysis artifact (`docs/system-of-record.md:7`, `docs/system-of-record.md:8`, `docs/system-of-record.md:10`).

## Summary Matrix

| # | Pattern | Classification | Impact | Effort | Priority | Integration Surface |
|---|---|---|---|---|---|---|
| 1 | Head-Tail Context Truncation with Recoverable Middle | Partial Coverage | High | Medium | P0 | Canonical doc, Level 1 windowing exercise, Level 3 compaction, harness checklist, N+1 evals |
| 2 | Addressable Memory Catalog | Partial Coverage | High | Medium | P0 | Canonical doc, Core Concept 1 retrieval, Core Concept 5 manifests, multi-agent `output_ref` traces |
| 4 | N+1 Long-Session Evals | Partial Coverage | High | Medium | P0 | Canonical doc, Level 4 harness improvements, harness evolution playbook, rubric template |
| 6 | Late-Failure Regression Suite | Partial Coverage | High | Medium | P0 | Canonical doc, regression battery, incident-backed rubric examples, context-strategy release gate |
| 5 | Stable Harness Prompt During Context Reduction | Partial Coverage | Medium | Low | P1 | Canonical doc, Owned Agent Control Loop, Context Builder contract, replay metadata |
| 3 | Context-Scoped Sub-Agent Delegation | Already Exists | Medium | Low | P2 | Cross-reference only: multi-agent coordination, `.opencode/` workflows, context-management analysis |
| 7 | Memory Tier Separation (Active / Short-Term / Long-Term / Cross-Session) | Better Implementation | Medium | Low | P2 | Cross-reference only: Core Concept 1, Core Concept 5, Serializable Pause/Resume State |

Priority interpretation: P0 closes high-value partial gaps that now have canonical docs but still need curriculum, eval, and operational integration; P1 formalizes an already-implied invariant; P2 should avoid duplicate content and add cross-references rather than new primitives.

---

## Artifacts Created During This Session

### Canonical Docs Created in `docs/canonical/`

These 5 files now exist and directly correspond to the partial-coverage patterns from the classification.

| File | Pattern | Status | What It Adds | Evidence |
|---|---|---|---|---|
| `docs/canonical/head-tail-context-truncation.md` | Head-Tail Context Truncation with Recoverable Middle | Created | Names the compaction variant, defines `[system_prompt][head][tail][latest_result]`, and requires exact recoverability for the middle | `docs/canonical/head-tail-context-truncation.md:1`, `docs/canonical/head-tail-context-truncation.md:19`, `docs/canonical/head-tail-context-truncation.md:45` |
| `docs/canonical/addressable-memory-catalog.md` | Addressable Memory Catalog | Created | Defines catalog fields `id`, `kind`, `location`, `preview`, `scope`, and `fetch` for omitted content recovery | `docs/canonical/addressable-memory-catalog.md:1`, `docs/canonical/addressable-memory-catalog.md:19`, `docs/canonical/addressable-memory-catalog.md:21` |
| `docs/canonical/n-plus-one-long-session-evals.md` | N+1 Long-Session Evals | Created | Defines the fixture shape: load N turns, apply production context strategy, test N+1 behavior | `docs/canonical/n-plus-one-long-session-evals.md:1`, `docs/canonical/n-plus-one-long-session-evals.md:19`, `docs/canonical/n-plus-one-long-session-evals.md:29` |
| `docs/canonical/stable-harness-prompt.md` | Stable Harness Prompt During Context Reduction | Created | States that the harness prompt is a preserved, versioned input, while history and tool bulk are reducible payload | `docs/canonical/stable-harness-prompt.md:1`, `docs/canonical/stable-harness-prompt.md:19`, `docs/canonical/stable-harness-prompt.md:21` |
| `docs/canonical/late-failure-regression-suite.md` | Late-Failure Regression Suite | Created | Defines durable late-session regression cases with fixture, N+1 prompt, expected behavior, context strategy, failure class, and evidence | `docs/canonical/late-failure-regression-suite.md:1`, `docs/canonical/late-failure-regression-suite.md:19`, `docs/canonical/late-failure-regression-suite.md:21` |

### Skills

| Artifact | Status | Evidence |
|---|---|---|
| Context-management-specific skill for head-tail truncation, memory catalog, N+1 evals, stable harness prompt, or late-failure regression | NOT_FOUND | Searched `.opencode/skills/` for exact pattern names and slug variants; no matching skill files were found. The existing agent system is documented as `.opencode/` in the system of record (`docs/system-of-record.md:16`, `docs/system-of-record.md:18`, `docs/system-of-record.md:34`). |

### Exercises

| Artifact | Status | Evidence |
|---|---|---|
| New exercise dedicated to the 5 context-management canonical patterns | NOT_FOUND | Searched `curriculum/` for exact pattern names and slug variants; no matching exercise files were found. Adjacent exercises exist, especially Level 1 windowing, which teaches sliding windows, compression, metadata preservation, and optimized context (`curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:13`, `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:46`). |

### Analysis Artifacts Already Present

| File | Role |
|---|---|
| `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md` | Source analysis and non-obvious knowledge extraction |
| `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-patterns.md` | Extracted reusable patterns |
| `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md` | Repo-fit classification used as the source for this roadmap |
| `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-integration-roadmap.md` | This integration map |

---

## Cross-Reference Table: Patterns -> Curriculum Levels and Canonical Docs

| # | Pattern | Curriculum Level / Surface | Existing Coverage | Canonical Docs to Link |
|---|---|---|---|---|
| 1 | Head-Tail Context Truncation with Recoverable Middle | Level 1 exercise; Level 3 architecture; Level 7 harness checklist | Level 1 already teaches keeping recent messages, compressing old history, preserving metadata, and returning optimized context (`curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:13`, `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:46`). Level 3 compaction keeps recent context complete, stores older ranges at different summary densities, and always injects external state (`curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:327`). The harness checklist requires explicit context policy and token budget (`curriculum/07-implementation-guides/03-harness-design-checklist.md:273`). | `docs/canonical/head-tail-context-truncation.md`; `docs/canonical/addressable-memory-catalog.md`; `docs/canonical/stable-harness-prompt.md` |
| 2 | Addressable Memory Catalog | Core Concept 1; Core Concept 5; Core Concept 7 | Core Concept 1 teaches retrieval over conversation chunks, documents, and events plus ranking and filters (`curriculum/05-core-concepts/01-context-management.md:580`). It also warns about similar-but-wrong retrieval and the need for privacy/scope filters (`curriculum/05-core-concepts/01-context-management.md:600`). Core Concept 5 asks for manifests and replay metadata through state/recovery practices (`curriculum/05-core-concepts/05-state-persistence.md:140`, `curriculum/05-core-concepts/05-state-persistence.md:1414`). Core Concept 7 uses `output_ref` handles in traces (`curriculum/05-core-concepts/07-multi-agent-coordination.md:552`). | `docs/canonical/addressable-memory-catalog.md`; `docs/canonical/head-tail-context-truncation.md`; `docs/canonical/serializable-pause-resume-state.md` |
| 3 | Context-Scoped Sub-Agent Delegation | Core Concept 7; `.opencode/` workflows | The repo already says the agent system lives in `.opencode/` and follows HoP with closed scope, owner, and validation gates (`docs/system-of-record.md:16`, `docs/system-of-record.md:18`). Core Concept 7 splits Search, Filter, Ranking, Recommendation, and Evaluator into distinct agents (`curriculum/05-core-concepts/07-multi-agent-coordination.md:486`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:488`) and says each agent receives only necessary context, reducing context rot (`curriculum/05-core-concepts/07-multi-agent-coordination.md:571`). Token-budget examples show separate per-agent windows instead of one monolithic context (`curriculum/05-core-concepts/07-multi-agent-coordination.md:1417`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1424`). | `docs/canonical/owned-agent-control-loop.md`; `docs/canonical/addressable-memory-catalog.md` |
| 4 | N+1 Long-Session Evals | Level 4 KODA-specific harness; Level 7 harness evolution; Tools/Templates rubric | The source analysis defines the target `load N, test N+1` mechanism (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:98`). Level 4 already proposes 50 long conversations for compaction shadow tests (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:570`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:577`). The harness evolution playbook requires a component-specific regression battery for long conversations and context limits (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:748`). | `docs/canonical/n-plus-one-long-session-evals.md`; `docs/canonical/late-failure-regression-suite.md`; `docs/canonical/stable-harness-prompt.md` |
| 5 | Stable Harness Prompt During Context Reduction | Level 7 harness checklist; Core Concept 5; canonical agent loop | The context window is documented as system prompt plus messages, summaries, tools, and injected state (`curriculum/05-core-concepts/05-state-persistence.md:140`). State Persistence says prompt, rubric, catalog, and schema need versions for replay (`curriculum/05-core-concepts/05-state-persistence.md:1414`). Owned Agent Control Loop separates Prompt from Context Builder (`docs/canonical/owned-agent-control-loop.md:20`, `docs/canonical/owned-agent-control-loop.md:47`, `docs/canonical/owned-agent-control-loop.md:51`). | `docs/canonical/stable-harness-prompt.md`; `docs/canonical/owned-agent-control-loop.md`; `docs/canonical/serializable-pause-resume-state.md` |
| 6 | Late-Failure Regression Suite | Level 4 harness improvements; Level 7 harness evolution; Tools/Templates rubric | The rubric template requires old incident outputs as a regression set and real problem outputs as regression examples (`curriculum/08-tools-templates/evaluation-rubric-template.md:812`, `curriculum/08-tools-templates/evaluation-rubric-template.md:875`). Harness evolution requires regression tests before canary and staged rollout metrics (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:776`). Level 4 harness improvements require shadow testing, rollback/disablement, ownership, and review cadence (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:560`). | `docs/canonical/late-failure-regression-suite.md`; `docs/canonical/n-plus-one-long-session-evals.md`; `docs/canonical/head-tail-context-truncation.md`; `docs/canonical/addressable-memory-catalog.md` |
| 7 | Memory Tier Separation (Active / Short-Term / Long-Term / Cross-Session) | Core Concept 1; Core Concept 5; glossary | Core Concept 1 separates working memory, medium-term state, and long-term memory (`curriculum/05-core-concepts/01-context-management.md:242`). Core Concept 5 separates context window, hot state, durable state, audit trail, curated summary, and external state (`curriculum/05-core-concepts/05-state-persistence.md:156`). The glossary distinguishes short-term, long-term, and file-based memory (`curriculum/GLOSSARY.md:260`). Serializable Pause/Resume State documents richer rebuild and persistence layers in the repo (`docs/canonical/serializable-pause-resume-state.md:50`, `docs/canonical/serializable-pause-resume-state.md:91`). | `docs/canonical/serializable-pause-resume-state.md`; `docs/canonical/head-tail-context-truncation.md`; `docs/canonical/addressable-memory-catalog.md` |

---

## Concrete Integration Points

### P0: Head-Tail Context Truncation with Recoverable Middle

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Keep the new doc as the authoritative pattern reference | `docs/canonical/head-tail-context-truncation.md` | Done |
| Level 1 exercise | Add an extension to `exercise-01-windowing.md`: preserve head + tail, move middle to recoverable store, expose retrieval handles | `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md` | Future |
| Level 3 compaction | Add a named variant to server-side compaction for exact recoverable middle, separate from summary-only compaction | `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md` | Future |
| Harness checklist | Add a checklist item: old context may be summarized, but exact omitted spans needed for follow-up must be recoverable | `curriculum/07-implementation-guides/03-harness-design-checklist.md` | Future |
| Evals | Validate with N+1 and late-failure regression cases | `docs/canonical/n-plus-one-long-session-evals.md` and `docs/canonical/late-failure-regression-suite.md` | Future |

### P0: Addressable Memory Catalog

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Keep catalog schema and retrieval contract as the authoritative reference | `docs/canonical/addressable-memory-catalog.md` | Done |
| Core Concept 1 | Add deterministic omitted-item catalog alongside vector retrieval, contrasting handle-based recovery with semantic search | `curriculum/05-core-concepts/01-context-management.md` | Future |
| Core Concept 5 | Add catalog version, offered IDs, fetched IDs, and replay manifest fields | `curriculum/05-core-concepts/05-state-persistence.md` | Future |
| Core Concept 7 | Reuse `output_ref` trace practice as the multi-agent version of catalog handles | `curriculum/05-core-concepts/07-multi-agent-coordination.md` | Future |
| Observability | Record which IDs were offered to the agent and which were fetched during N+1 evals | Evaluation/reporting convention | Future |

### P0: N+1 Long-Session Evals

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Keep N-turn fixture plus N+1 prompt as the authoritative eval pattern | `docs/canonical/n-plus-one-long-session-evals.md` | Done |
| Harness improvements | Convert the planned 50 long conversations into explicit N-turn fixtures with N+1 prompts | `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` | Future |
| Harness evolution | Add N+1 cases to component-specific regression batteries for Budget Guard and context changes | `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Future |
| Rubric template | Add continuity, reference resolution, retrieval correctness, and task correctness dimensions | `curriculum/08-tools-templates/evaluation-rubric-template.md` | Future |
| Release gate | Require N+1 results before changing truncation, retrieval, prompt, memory, or delegation policy | Context-strategy release checklist | Future |

### P1: Stable Harness Prompt During Context Reduction

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Keep prompt-preservation invariant as the authoritative rule | `docs/canonical/stable-harness-prompt.md` | Done |
| Owned Agent Control Loop | Link prompt stability to the Prompt and Context Builder boundary | `docs/canonical/owned-agent-control-loop.md` | Future |
| State Persistence | Add `prompt_version` and context-block versioning to replay examples | `curriculum/05-core-concepts/05-state-persistence.md` | Future |
| Harness checklist | Add PASS/FAIL item: context reduction cannot trim or mutate the stable harness prompt | `curriculum/07-implementation-guides/03-harness-design-checklist.md` | Future |

### P0: Late-Failure Regression Suite

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical doc | Keep case schema and failure taxonomy as the authoritative regression pattern | `docs/canonical/late-failure-regression-suite.md` | Done |
| Rubric template | Add late-session context failures as a named source of regression examples | `curriculum/08-tools-templates/evaluation-rubric-template.md` | Future |
| Harness evolution | Add this suite as a required pre-canary gate for context-strategy changes | `curriculum/07-implementation-guides/06-harness-evolution-playbook.md` | Future |
| Harness improvements | Seed first cases from long-conversation shadow tests and critical-fact retention tests | `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md` | Future |
| Ownership | Assign suite ownership and refresh cadence, matching existing technical-owner/review-cadence language | Harness runbook or future canonical eval doc | Future |

### P2: Context-Scoped Sub-Agent Delegation

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical cross-reference | Do not create a duplicate canonical doc; link the context-management analysis to existing multi-agent coordination and owned loop docs | `docs/canonical/owned-agent-control-loop.md`; `curriculum/05-core-concepts/07-multi-agent-coordination.md` | Future |
| Skill workflow | Optional: add a short note in analysis skills that sub-agent delegation is also context-window partitioning, not only specialization | `.opencode/skills/analyze-and-improve/SKILL.md` | Future |
| Curriculum | Add a sentence to Core Concept 7: each agent's context window is an isolation boundary for heavy data | `curriculum/05-core-concepts/07-multi-agent-coordination.md` | Future |

### P2: Memory Tier Separation

| Integration Point | Action | Artifact | Status |
|---|---|---|---|
| Canonical cross-reference | Do not create a duplicate canonical doc; link to State Persistence and Serializable Pause/Resume State | `docs/canonical/serializable-pause-resume-state.md`; `curriculum/05-core-concepts/05-state-persistence.md` | Future |
| Core Concept 1 | Add a sidebar distinguishing in-session recoverable middle from cross-session long-term memory | `curriculum/05-core-concepts/01-context-management.md` | Future |
| Glossary | Expand `Memory / State` with active context, in-session recovery memory, and cross-session memory | `curriculum/GLOSSARY.md` | Future |

---

## Gap Analysis

| Gap | Affected Patterns | Current Evidence | Needed Integration |
|---|---|---|---|
| Curriculum does not yet teach exact recoverable-middle mechanics | 1, 2 | Classification found no exact head-tail recoverable-middle pattern outside this analysis (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md:16`), even though adjacent windowing and compaction coverage exists (`curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:13`, `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:327`). | Add Level 1 exercise extension and Level 3 compaction section. |
| Omitted-memory catalog is canonical but not operationalized in curriculum or skills | 2 | Classification found no explicit `id + location + preview` catalog (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md:32`). The new canonical doc defines the schema (`docs/canonical/addressable-memory-catalog.md:21`). | Add catalog schema to Core Concept 1, Core Concept 5 manifest/replay guidance, and eval reports. |
| N+1 eval shape is canonical but not present as runnable curriculum/template artifact | 4 | Classification found no named N+1 eval outside this analysis (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md:64`). Long-conversation shadow tests already exist as roadmap items (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:570`). | Add fixture format, rubric dimensions, and harness-evolution gate. |
| Stable harness prompt is still an implied invariant in most docs | 5 | Classification found no explicit rule for preserving system prompt while truncating payload (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md:80`). Owned Agent Control Loop separates Prompt and Context Builder (`docs/canonical/owned-agent-control-loop.md:47`, `docs/canonical/owned-agent-control-loop.md:51`). | Link the new canonical invariant into harness checklist and replay/versioning docs. |
| Late-session context regressions are not yet a named suite in curriculum or release process | 6 | Classification found no named late-session suite (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md:95`). Existing regression practice is broad rather than context-failure-specific (`curriculum/08-tools-templates/evaluation-rubric-template.md:812`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`). | Add suite ownership, case schema, and pre-canary gate for context-strategy changes. |
| No new skills or exercises were created for these context-management patterns | 1, 2, 4, 5, 6 | Direct artifact inventory found the 5 canonical docs, but NOT_FOUND for matching `.opencode/skills/` or dedicated `curriculum/` exercises. | Decide whether to create a context-strategy skill and at least one hands-on exercise in a later task. |
| System of record still lists only 4 canonical active patterns | All 5 new canonical docs | `docs/system-of-record.md` says there are 4 active canonical patterns and lists only 12-Factor-derived docs (`docs/system-of-record.md:115`, `docs/system-of-record.md:117`, `docs/system-of-record.md:121`). | Update `docs/system-of-record.md` in a separate task if this repository wants the 5 new canonical docs registered there. |

---

## Recommended Sequence

1. **Register the 5 new canonical docs in the system of record** so the canonical index matches the current `docs/canonical/` directory.
2. **Add curriculum links before new implementation work**: Level 1 windowing, Level 3 compaction, Core Concept 1, Core Concept 5, Core Concept 7, Level 7 harness evolution, and the rubric template are the highest-leverage targets.
3. **Create N+1 fixture and late-failure case templates** before changing any runtime context strategy, because the classification identifies eval coverage as the mechanism that proves context quality (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:50`).
4. **Defer new skills unless a repeatable operational workflow emerges**; current evidence shows canonical docs were created, but no dedicated skill or exercise exists yet.

## References

- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-classification.md` - source classification for all 7 patterns.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-patterns.md` - extracted pattern definitions.
- `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md` - source analysis and non-obvious context-management mechanics.
- `docs/canonical/head-tail-context-truncation.md` - canonical Pattern 1 doc.
- `docs/canonical/addressable-memory-catalog.md` - canonical Pattern 2 doc.
- `docs/canonical/n-plus-one-long-session-evals.md` - canonical Pattern 4 doc.
- `docs/canonical/stable-harness-prompt.md` - canonical Pattern 5 doc.
- `docs/canonical/late-failure-regression-suite.md` - canonical Pattern 6 doc.
- `docs/canonical/owned-agent-control-loop.md` - adjacent canonical doc for prompt/context-builder and delegation boundaries.
- `docs/canonical/serializable-pause-resume-state.md` - adjacent canonical doc for state and memory tier separation.
- `docs/system-of-record.md` - repository precedence and canonical index.

---

*Created: 2026-06-10 | From: Context Management pattern classification | Precedence: analysis*
