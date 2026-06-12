---
title: "Pattern Classification: How We Solved Context Management in Agents"
type: analysis
date: 2026-06-09
domain: context-management
aliases: ["classificacao contexto", "gap contexto", "cobertura contexto", "N+1"]
tags: [analise, context-engineering, context-management, classification]
last_updated: 2026-06-10
relates-to: ["[[docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis|Context Mgmt Analysis]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]"]
---

# Pattern Classification: How We Solved Context Management in Agents

Scope: classifies the 7 extracted context-management patterns against `long-running-agents` using the repository precedence order in `docs/system-of-record.md`: decisions, canonical docs, evidence, analysis, curriculum, then operational READMEs and skills (`docs/system-of-record.md:5`, `docs/system-of-record.md:7`, `docs/system-of-record.md:8`, `docs/system-of-record.md:9`, `docs/system-of-record.md:10`, `docs/system-of-record.md:11`, `docs/system-of-record.md:12`). `docs/decisions/` is currently empty, so no ADR overrides were found (`docs/system-of-record.md:105`, `docs/system-of-record.md:107`).

## 1. Head-Tail Context Truncation with Recoverable Middle

**Classification:** Partial Coverage

The repo teaches context reduction, sliding windows, summaries, state persistence, retrieval, and server-side compaction, but it does not formalize the specific `head + tail + omitted middle with retrieval handles` mechanism. Existing material keeps recent turns, summaries, critical state, and backup/auditability, which covers the intent. The missing mechanics are preserving both the beginning and latest tail as active anchors while storing the middle as exact, addressable, recoverable content.

**Evidence:**

- Existing coverage: Level 1 windowing asks learners to keep only the last K messages, compress old history, preserve critical metadata, and return optimized context (`curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:13`, `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:14`, `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:15`, `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:16`, `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:46`).
- Existing coverage: the harness checklist requires an explicit context policy, system-prompt budget, structured old-history summaries, durable critical state, and explainability for each block in a call (`curriculum/07-implementation-guides/03-harness-design-checklist.md:273`, `curriculum/07-implementation-guides/03-harness-design-checklist.md:275`, `curriculum/07-implementation-guides/03-harness-design-checklist.md:276`, `curriculum/07-implementation-guides/03-harness-design-checklist.md:277`, `curriculum/07-implementation-guides/03-harness-design-checklist.md:278`, `curriculum/07-implementation-guides/03-harness-design-checklist.md:279`).
- Existing coverage: server-side compaction keeps recent context complete, older ranges summarized at different densities, and external state always injected (`curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:327`, `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:328`, `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:329`, `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:330`, `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:331`, `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:332`, `curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction.md:333`).
- Missing mechanic: NOT_FOUND for an exact head-tail recoverable-middle pattern in `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, and `.opencode/skills/`. Existing material prefers sliding window, summaries, retrieval, state, and compaction rather than exact middle recovery.

**Integration value:** High. The repo already has the vocabulary for context management; adding head/tail/middle as a named compaction variant would strengthen auditability and late follow-up recovery without replacing the current curriculum.

## 2. Addressable Memory Catalog

**Classification:** Partial Coverage

The repo has retrieval, state persistence, trace references, output references, and source metadata, but it does not define a compact catalog of omitted items with stable IDs, location metadata, and previews specifically for recovering truncated middle content. The closest equivalent is general retrieval and artifact/reference discipline.

**Evidence:**

- Existing coverage: Context Management teaches vector retrieval that indexes conversation chunks, documents, and events, then retrieves top ranked context by query and filters (`curriculum/05-core-concepts/01-context-management.md:580`, `curriculum/05-core-concepts/01-context-management.md:582`, `curriculum/05-core-concepts/01-context-management.md:583`, `curriculum/05-core-concepts/01-context-management.md:587`, `curriculum/05-core-concepts/01-context-management.md:589`, `curriculum/05-core-concepts/01-context-management.md:590`, `curriculum/05-core-concepts/01-context-management.md:591`).
- Existing coverage: Context Management warns that retrieval can return a similar but wrong chunk and needs privacy/scope filters, which overlaps with catalog-quality concerns (`curriculum/05-core-concepts/01-context-management.md:600`, `curriculum/05-core-concepts/01-context-management.md:601`, `curriculum/05-core-concepts/01-context-management.md:602`, `curriculum/05-core-concepts/01-context-management.md:603`, `curriculum/05-core-concepts/01-context-management.md:604`).
- Existing coverage: multi-agent traces store `output_ref` handles for each internal agent output (`curriculum/05-core-concepts/07-multi-agent-coordination.md:552`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:556`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:558`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:559`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:560`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:561`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:562`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:563`).
- Existing coverage: state-persistence notes require a human-readable manifest with the files and decisions used by a response (`curriculum/05-core-concepts/05-state-persistence.md:1864`, `curriculum/05-core-concepts/05-state-persistence.md:1866`, `curriculum/05-core-concepts/05-state-persistence.md:1868`, `curriculum/05-core-concepts/05-state-persistence.md:1870`).
- Missing mechanic: NOT_FOUND for an explicit addressable omitted-memory catalog with `id + location + preview` in `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, and `.opencode/skills/`.

**Integration value:** High. It would turn existing retrieval and trace-reference concepts into a more concrete operational interface for recoverable context omissions.

## 3. Context-Scoped Sub-Agent Delegation

**Classification:** Already Exists

The repo documents and operationalizes scoped delegation at equivalent depth. The curriculum teaches that separate agents receive only the context needed for their role and can reduce context rot. The `.opencode` analysis workflow delegates mental modeling, knowledge extraction, pattern extraction, classification, improvement, and integration to specialized agents. This matches the pattern's core reframe: heavy or specialized work gets its own context window and returns compact evidence or results to the main workflow.

**Evidence:**

- Canonical/system-of-record coverage: `.opencode/` is the agent system and follows HoP with closed scope, owner, and validation gates (`docs/system-of-record.md:16`, `docs/system-of-record.md:18`).
- Operational coverage: `analyze-and-improve` defines a six-phase pipeline, all delegated to specialized sub-agents, including Classification as a `deep` delegation (`.opencode/skills/analyze-and-improve/SKILL.md:30`, `.opencode/skills/analyze-and-improve/SKILL.md:32`, `.opencode/skills/analyze-and-improve/SKILL.md:34`, `.opencode/skills/analyze-and-improve/SKILL.md:35`, `.opencode/skills/analyze-and-improve/SKILL.md:36`, `.opencode/skills/analyze-and-improve/SKILL.md:37`, `.opencode/skills/analyze-and-improve/SKILL.md:38`, `.opencode/skills/analyze-and-improve/SKILL.md:39`).
- Curriculum coverage: the KODA multi-agent pipeline separates Search, Filter, Ranking, Recommendation, and Evaluator responsibilities (`curriculum/05-core-concepts/07-multi-agent-coordination.md:486`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:488`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:490`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:491`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:492`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:493`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:494`).
- Curriculum coverage: the pipeline explicitly says each agent receives only necessary context and that this reduces context rot (`curriculum/05-core-concepts/07-multi-agent-coordination.md:571`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:572`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:573`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:574`).
- Curriculum coverage: token-budget examples show each sub-agent has a scoped context instead of one monolithic 12K-token context (`curriculum/05-core-concepts/07-multi-agent-coordination.md:1417`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1419`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1424`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1425`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1426`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1427`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1428`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1429`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1437`, `curriculum/05-core-concepts/07-multi-agent-coordination.md:1438`).

**Integration value:** Low. The repo already teaches and uses the pattern. Any integration should be a cross-reference to the new context-management analysis, not a new concept.

## 4. N+1 Long-Session Evals

**Classification:** Partial Coverage

The repo has long-conversation tests, shadow tests, regression batteries, and rubrics that use old incidents as regression examples. It does not yet define the precise eval shape `load N turns, apply production context strategy, test turn N+1` as a named gate.

**Evidence:**

- Existing coverage: the extracted source analysis defines the target N+1 mechanic as loading 10 turns, applying normal context/memory strategy, then testing the 11th turn (`docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:98`, `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:100`, `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:102`, `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:104`, `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:105`, `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:106`, `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:107`, `docs/analysis/2026-06-09-how-we-solved-context-management-in-agents/2026-06-09-how-we-solved-context-management-in-agents-analysis.md:108`).
- Existing repo coverage: Harness Improvements proposes a sample of 50 long conversations for compaction shadow tests (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:570`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:574`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:577`).
- Existing repo coverage: the same document prescribes measuring critical-fact retention in long, noisy conversations after shadow compaction (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:1030`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:1032`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:1033`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:1034`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:1035`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:1036`).
- Existing repo coverage: the harness evolution playbook includes a component-specific regression battery focused on long conversations, incomplete responses, and context limits (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:748`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:752`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:756`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:760`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:764`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:768`).
- Missing mechanic: NOT_FOUND for a named `N+1` long-session eval in `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, and `.opencode/skills/` outside this analysis output.

**Integration value:** High. The repo is ready for this because it already has long-session fixtures and regression vocabulary; adding N+1 would make late context failures reproducible by construction.

## 5. Stable Harness Prompt During Context Reduction

**Classification:** Partial Coverage

The repo recognizes system prompts as separate, budgeted, versioned inputs, and it teaches prompt/context ownership. It does not yet formalize the rule that context reduction should preserve stable harness instructions while reducing only payload/history/tool bulk.

**Evidence:**

- Canonical coverage: Owned Agent Control Loop treats Prompt as its own component and Context Builder as the separate component that assembles history, memory, tool results, and business state (`docs/canonical/owned-agent-control-loop.md:20`, `docs/canonical/owned-agent-control-loop.md:22`, `docs/canonical/owned-agent-control-loop.md:24`, `docs/canonical/owned-agent-control-loop.md:30`, `docs/canonical/owned-agent-control-loop.md:33`, `docs/canonical/owned-agent-control-loop.md:47`, `docs/canonical/owned-agent-control-loop.md:51`, `docs/canonical/owned-agent-control-loop.md:52`).
- Canonical coverage and gap: the repo has a hand-authored system prompt and an excellent context builder, but the prompt is not versioned or evaled as a separate component (`docs/canonical/owned-agent-control-loop.md:87`, `docs/canonical/owned-agent-control-loop.md:89`, `docs/canonical/owned-agent-control-loop.md:93`, `docs/canonical/owned-agent-control-loop.md:94`).
- Curriculum coverage: context window explicitly includes system prompt, recent messages, summaries, tools, and injected state; state persistence says prompt, rubric, catalog, and schema need versions for replay (`curriculum/05-core-concepts/05-state-persistence.md:140`, `curriculum/05-core-concepts/05-state-persistence.md:142`, `curriculum/05-core-concepts/05-state-persistence.md:146`, `curriculum/05-core-concepts/05-state-persistence.md:1414`, `curriculum/05-core-concepts/05-state-persistence.md:1416`).
- Curriculum coverage: prompt version is called out as a decision note because replay with LLM depends on the prompt used, and the recommended action is persisting `prompt_version` in decision artifacts (`curriculum/05-core-concepts/05-state-persistence.md:1834`, `curriculum/05-core-concepts/05-state-persistence.md:1836`, `curriculum/05-core-concepts/05-state-persistence.md:1838`, `curriculum/05-core-concepts/05-state-persistence.md:1840`).
- Missing mechanic: NOT_FOUND for an explicit rule named `Stable Harness Prompt During Context Reduction` or equivalent `preserve system prompt while truncating payload` in `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, and `.opencode/skills/` outside this analysis output.

**Integration value:** Medium. This is a small formalization that would clarify existing prompt/context-builder separation and protect future compaction implementations from trimming the harness itself.

## 6. Late-Failure Regression Suite

**Classification:** Partial Coverage

The repo has mature regression practices for rubrics, harness evolution, canaries, and long-conversation shadow tests. What is missing is a named suite specifically for late-session context failures, where observed forgetting or degraded follow-up behavior becomes a durable regression case tied to the context strategy.

**Evidence:**

- Existing coverage: the evaluation rubric template requires applying rubrics to old incident outputs as a regression set and using real problem outputs as regression examples (`curriculum/08-tools-templates/evaluation-rubric-template.md:812`, `curriculum/08-tools-templates/evaluation-rubric-template.md:813`, `curriculum/08-tools-templates/evaluation-rubric-template.md:814`, `curriculum/08-tools-templates/evaluation-rubric-template.md:859`, `curriculum/08-tools-templates/evaluation-rubric-template.md:875`).
- Existing coverage: the harness evolution playbook requires regression tests before canary, then staged rollout with shadow diffs, canary metrics, rollback decisions, and 14-day observation (`curriculum/07-implementation-guides/06-harness-evolution-playbook.md:741`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:748`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:776`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:780`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:781`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:782`, `curriculum/07-implementation-guides/06-harness-evolution-playbook.md:783`).
- Existing coverage: Harness Improvements defines comparison-controlled shadow testing, rollback/disablement, technical ownership, and review cadence as acceptance criteria for proposed improvements (`curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:480`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:482`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:483`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:484`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:485`, `curriculum/04-nivel-4-koda-specific/05-harness-improvements.md:486`).
- Missing mechanic: NOT_FOUND for a named late-session context regression suite in `docs/decisions/`, `docs/canonical/`, `docs/evidence/`, `curriculum/`, and `.opencode/skills/`. Existing suites are broader harness/rubric regressions rather than context-failure-specific.

**Integration value:** High. The repo already has regression infrastructure and long-conversation examples; this pattern would make late context degradation a first-class regression family.

## 7. Memory Tier Separation (Active / Short-Term / Long-Term / Cross-Session)

**Classification:** Better Implementation

The repo has a more mature memory-tier model than the source pattern. It separates context window, hot/session state, durable state, audit trail, curated summaries, external systems, working memory, medium-term state, and long-term memory. It also provides practical rules for promotion, retrieval, persistence, recovery, and audit.

**Evidence:**

- Canonical coverage: Serializable Pause/Resume State states that the repo rebuilds state each turn from PostgreSQL, Redis, Pinecone, conversation history, memories, orders, metadata, constraints, and phase instead of relying on a context blob (`docs/canonical/serializable-pause-resume-state.md:50`, `docs/canonical/serializable-pause-resume-state.md:52`, `docs/canonical/serializable-pause-resume-state.md:58`, `docs/canonical/serializable-pause-resume-state.md:59`, `docs/canonical/serializable-pause-resume-state.md:60`, `docs/canonical/serializable-pause-resume-state.md:61`, `docs/canonical/serializable-pause-resume-state.md:62`).
- Canonical coverage: the same doc says the repo has richer state persistence, including four persistence layers, memory extraction, expiration, contradiction detection, and Core Concept 5 (`docs/canonical/serializable-pause-resume-state.md:91`, `docs/canonical/serializable-pause-resume-state.md:93`, `docs/canonical/serializable-pause-resume-state.md:95`, `docs/canonical/serializable-pause-resume-state.md:97`, `docs/canonical/serializable-pause-resume-state.md:99`, `docs/canonical/serializable-pause-resume-state.md:100`, `docs/canonical/serializable-pause-resume-state.md:101`).
- Curriculum coverage: Context Management explicitly separates Working memory, Medium-term state, and Long-term memory, and warns against solving everything with working memory (`curriculum/05-core-concepts/01-context-management.md:242`, `curriculum/05-core-concepts/01-context-management.md:244`, `curriculum/05-core-concepts/01-context-management.md:248`, `curriculum/05-core-concepts/01-context-management.md:249`, `curriculum/05-core-concepts/01-context-management.md:250`, `curriculum/05-core-concepts/01-context-management.md:252`).
- Curriculum coverage: State Persistence separates `context window`, hot state, durable state, audit trail, curated summary, and external state with duration, use, and risk (`curriculum/05-core-concepts/05-state-persistence.md:156`, `curriculum/05-core-concepts/05-state-persistence.md:158`, `curriculum/05-core-concepts/05-state-persistence.md:160`, `curriculum/05-core-concepts/05-state-persistence.md:161`, `curriculum/05-core-concepts/05-state-persistence.md:162`, `curriculum/05-core-concepts/05-state-persistence.md:163`, `curriculum/05-core-concepts/05-state-persistence.md:164`, `curriculum/05-core-concepts/05-state-persistence.md:165`).
- Curriculum coverage: the glossary also distinguishes short-term, long-term, and file-based memory (`curriculum/GLOSSARY.md:260`, `curriculum/GLOSSARY.md:261`, `curriculum/GLOSSARY.md:263`, `curriculum/GLOSSARY.md:264`, `curriculum/GLOSSARY.md:265`, `curriculum/GLOSSARY.md:266`, `curriculum/GLOSSARY.md:268`).

**Integration value:** Low. The repo already exceeds the source pattern; integration should mainly add cross-references from the new analysis to existing Core Concept 1 and Core Concept 5.

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Head-Tail Context Truncation with Recoverable Middle | Partial Coverage | High |
| 2 | Addressable Memory Catalog | Partial Coverage | High |
| 3 | Context-Scoped Sub-Agent Delegation | Already Exists | Low |
| 4 | N+1 Long-Session Evals | Partial Coverage | High |
| 5 | Stable Harness Prompt During Context Reduction | Partial Coverage | Medium |
| 6 | Late-Failure Regression Suite | Partial Coverage | High |
| 7 | Memory Tier Separation (Active / Short-Term / Long-Term / Cross-Session) | Better Implementation | Low |
