---
title: "Memory Selection Problem — Pattern Classification"
type: analysis
date: 2026-06-18
tags: ["context-engineering", "agentes-orquestracao", "harness-engineering", "token-budgeting"]
aliases: ["2026-06-18 memory selection problem classification", "memory selection classification"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]", "[[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]", "[[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]", "[[docs/canonical/external-state-persistence|External State Persistence]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]", "[[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]", "[[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]", "[[docs/canonical/burn-rate-runtime-forecast|Burn-Rate Runtime Forecast]]", "[[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]", "[[docs/canonical/error-context-hygiene|Error Context Hygiene]]", "[[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]", "[[docs/canonical/budget-aware-session-handoff|Budget-Aware Session Handoff]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem Patterns]]", "[[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-mental-model|Memory Selection Problem Mental Model]]"]
---

# Memory Selection Problem — Pattern Classification

Classification of 8 extracted patterns from the Memory Selection Problem analysis against the `long-running-agents` repository. Evidence-based with `file:line` citations per the system-of-record precedence: `docs/decisions/ > docs/canonical/ > docs/evidence/ > docs/analysis/ > curriculum/ > READMEs`.

Source patterns: [[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|Memory Selection Problem — Reusable Patterns (YAML)]].

**Classification date**: 2026-06-18 | **Repository**: `long-running-agents` at `main` branch.

---

## 1. Deliberate Forgetting

**Classification**: Partial Coverage | **Integration Value**: High

### What the pattern proposes

Informed, deliberate decision-making about what to keep vs. discard from context, using a relational context graph, a relevance evaluator, a promotion/demotion engine, a discard logger with rationale, and a budget gate on evaluation cost. The core shift: "what can I afford to forget now" rather than "how to store everything."

### What the repository has

The repo has extensive context management infrastructure that covers related but distinct concerns:

- **Deliberate context construction**: The Owned Agent Control Loop makes Context Builder an owned component that constructs every token deliberately — summarization, compression, and injection are explicit builder responsibilities ([[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]:60-62).
- **Explicit dropping of transient turns**: Durable Fact Selective History explicitly drops transient conversational turns that are not recent, keeping only durable facts and recent texture ([[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]:32-35, 104).
- **Head-tail truncation with recoverable middle**: Moves omitted content to external memory instead of discarding it — the middle is stored as exact recoverable content, not lost ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:37-39).
- **Budget-driven compaction triggers**: The Phase-Gated Token Health Monitor triggers summarization at orange phase and session handoff at red phase, making compaction a deterministic response to budget pressure ([[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:65-66).

### What is missing

The repo's context management treats summarization, compaction, and truncation as **reactive or budget-driven interventions**, not as a **proactive relevance-scoring loop**. Missing components:

1. **Relevance Evaluator**: No mechanism scores each context unit by relevance to the current task state using relational graph traversal. The repo decides *when* to reduce context (budget threshold) but not *what* to keep based on relevance scoring.
2. **Promotion/Demotion Engine**: No explicit tier movement decisions based on relevance scores. The repo has binary keep/omit decisions, not scored transitions.
3. **Discard Logger**: No record of what was dropped and why. The addressable-memory-catalog stores omitted content for recovery, but no rationale log exists.
4. **Budget Gate on evaluation cost**: The explicit token budget ledger tracks per-call costs ([[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:30-46) but does not gate the evaluation cost of forgetting decisions against the savings.

### Evidence

| File | Line | Evidence |
|---|---|---|
| `docs/canonical/owned-agent-control-loop.md` | 60-62 | Context Builder constructs every token deliberately; summarization and compression are owned responsibilities |
| `docs/canonical/durable-fact-selective-history.md` | 32-35 | Explicit separation: recent conversational texture + structured durable facts; older transient turns are dropped |
| `docs/canonical/head-tail-context-truncation.md` | 37-39 | Middle is not discarded — stored as exact recoverable content with retrieval handles |
| `docs/canonical/phase-gated-token-health-monitor.md` | 65-66 | Orange phase triggers summarize/compress; red phase triggers new_session/handoff |
| `docs/canonical/explicit-token-budget-ledger.md` | 30-46 | Per-call budget ledger with remaining percentage gating actions |

---

## 2. Smallest Sufficient Context

**Classification**: Partial Coverage | **Integration Value**: High

### What the pattern proposes

Instead of dumping the full context window, retrieve only the minimal token set needed for the current reasoning step. Selection is driven by structure (relational relevance via a Relational Context Graph) rather than similarity (embedding proximity). Includes a sufficiency estimator, relational traversal engine, order-preserving assembler, and capacity profiler that maps model head/tail attention bias.

### What the repository has

The repo has significant foundations for budget-aware, layered context assembly:

- **Hybrid context stack with ordered layers**: Assembles context in a fixed order: response reserve → stable harness → durable state → head anchor → summary/topic → tail anchor → memory catalog. Each layer has a budget policy ([[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]:36-42).
- **Bounded active context with anchors**: Head-tail truncation preserves only the head (goal, constraints) and tail (latest state, current request) with the middle stored externally ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:28-39).
- **Retrieval by handle**: The addressable memory catalog provides stable IDs, location, and previews so the agent can select specific items for retrieval rather than loading everything ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- **Per-call budget awareness**: Explicit token budget ledger computes remaining budget before each call ([[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:30-46).

### What is missing

The repo assembles context by structural layers (harness, durable, summary, tail), not by relational relevance to the current reasoning step. Missing components:

1. **Sufficiency Estimator**: No mechanism determines the minimum token set needed for correct reasoning about the current step. The hybrid stack layers are fixed, not computed per step.
2. **Relational Traversal Engine**: No graph traversal along typed edges to collect connected context. Retrieval is by catalog handle (addressable-memory-catalog) or semantic topic (semantic-topic-bucketing), not by dependency/provenance/causation traversal.
3. **Order-Preserving Assembler**: Head-tail truncation preserves temporal order but as a fixed strategy (head → middle → tail), not as a computed assembly from graph traversal results.
4. **Capacity Profiler**: No formal mapping of model head/tail attention bias to token placement. Head-tail truncation is structural (goal/setup in head, current state in tail), not attention-profile-driven.

### Evidence

| File | Line | Evidence |
|---|---|---|
| `docs/canonical/hybrid-context-stack.md` | 36-42 | Stack assembly order with per-layer budget policy (reserve → durable → head → summary → tail → catalog) |
| `docs/canonical/head-tail-context-truncation.md` | 28-39 | Bounded active context: stable prompt + head + tail + latest result; middle stored externally |
| `docs/canonical/addressable-memory-catalog.md` | 28-43 | Catalog fields: id, kind, location, preview, scope, tool, path for selective retrieval |
| `docs/canonical/explicit-token-budget-ledger.md` | 30-46 | Per-call ledger: fixed_prompt_cost, accumulated_context, reserved_response, remaining_budget |

---

## 3. Tiered Context Storage with Promotion/Demotion

**Classification**: Missing | **Integration Value**: Medium

### What the pattern proposes

Dynamic three-tier storage (hot/warm/cold) with explicit promotion/demotion decisions based on relevance. Hot tier (in-memory, sub-millisecond) holds active context; warm tier (NVMe, ~1ms) holds recently relevant content; cold tier (object storage, ~100ms) holds complete history. A Tier Orchestrator executes promotion/demotion and prefetch predictions.

### What the repository has

The repo has adjacent infrastructure but no tiered storage model:

- **Two-tier model** (active vs. external): Head-tail truncation separates active context (head + tail + latest result) from external memory (middle + older messages). This is a binary model, not a three-tier system with promotion/demotion ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:28-39).
- **Retrieval handles for external memory**: Addressable memory catalog provides access to externally stored content, approximating warm-tier access patterns, but without tier orchestration ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).

### What is missing (NOT_FOUND)

Searched `docs/canonical/` for "hot", "warm", "cold", "tier storage", "promotion", "demotion" in the context of storage tiers:

1. **Three-tier architecture**: No hot/warm/cold tier definitions exist in any canonical doc. The only "tiers" in the repo refer to eval tier stratification (fast/medium/deep), not storage.
2. **Promotion/Demotion Engine**: No dynamic movement of context between storage tiers. The only "promotion" patterns found are `cross-context-knowledge-siloing.md` (knowledge promotion pipeline across agent contexts) and `carry-debt-sunset-gate.md` (artifact promotion to production), neither of which relates to storage tier management.
3. **Tier Orchestrator**: No component that monitors relevance and executes tier transitions with prefetch predictions.
4. **Latency-aware storage policies**: No documentation of latency characteristics for different storage backends used by context retrieval.

**Locations searched**: All 85 canonical docs in `docs/canonical/`, system-of-record pattern inventory ([[docs/system-of-record|System of Record]]:144-235).

### Evidence

| File | Line | Evidence |
|---|---|---|
| `docs/canonical/head-tail-context-truncation.md` | 28-39 | Binary separation: active context vs. external memory — closest existing pattern, but no tier layers |
| `docs/canonical/addressable-memory-catalog.md` | 28-43 | Retrieval handles for external memory — provides access pattern but no tier orchestration |

---

## 4. Relational Context Graph

**Classification**: Partial Coverage | **Integration Value**: High

### What the pattern proposes

A queryable graph with typed edges (dependency, provenance, supersession, causation) that transforms retrieval into selection — returning context connected by real semantic relationships rather than similarity. Components: Node Ingestor, Edge Classifier, Supersession Updater, Traversal Engine.

### What the repository has

The repo has significant graph infrastructure and epistemic labeling, but not the full typed-edge relational model:

- **Epistemic Memory Graph**: Memory nodes carry epistemic labels (confirmed, inferred, contested, stale, hypothesis, preference, policy, unknown), source provenance, and retrieval keys. Retrieval fuses search, vectors, backlinks, and graph traversal ([[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]]:28-49).
- **Provenance tracking for durable facts**: Durable Fact Selective History requires provenance (source turn, tool result, artifact, owner) and freshness metadata for every durable fact ([[docs/canonical/durable-fact-selective-history|Durable Fact Selective History]]:94-96).
- **Knowledge graph curriculum**: The repo teaches knowledge graphs as a connected ecosystem of concepts with dependency, operational order, and maturity timeline diagrams ([[curriculum/06-knowledge-graphs/01-concept-ecosystem|Concept Ecosystem]]:75-91; [[curriculum/08-tools-templates/knowledge-graph-template|Knowledge Graph Template]]:51-60).
- **Addressable memory catalog**: Provides stable IDs, kind classification, and retrieval handles — foundational node metadata for a graph ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).

### What is missing

The epistemic-memory-graph focuses on belief-status labeling and retrieval fusion, not on formal typed edges for context selection. Missing components:

1. **Edge Classifier**: No component classifies relationships between context units into typed edges (dependency, provenance, supersession, causation). The epistemic graph has graph edges but without the four formal edge types.
2. **Supersession Updater**: No mechanism marks obsolete nodes and redirects edges when context is superseded. Durable facts track `last_verified` but do not formalize supersession as a graph operation.
3. **Traversal Engine for context selection**: Graph traversal exists conceptually (epistemic graph mentions backlinks and graph edges) but is not formalized as a "traverse from task node to collect connected context along typed edges."
4. **Node Ingestor for context units**: Intercepting every tool result, decision, and state snapshot as graph nodes is not implemented.

### Evidence

| File | Line | Evidence |
|---|---|---|
| `docs/canonical/epistemic-memory-graph.md` | 28-49 | Memory nodes with epistemic labels, source provenance, hybrid retrieval (search + vectors + backlinks + graph traversal) |
| `docs/canonical/durable-fact-selective-history.md` | 94-96 | Provenance tracking: source turn, tool result, artifact, owner; freshness metadata |
| `docs/canonical/addressable-memory-catalog.md` | 28-43 | Stable IDs, kind classification, location, scope — foundational node metadata |
| `curriculum/06-knowledge-graphs/01-concept-ecosystem.md` | 75-91 | Knowledge graph as connected ecosystem of concepts |
| `curriculum/08-tools-templates/knowledge-graph-template.md` | 51-60 | Graph templates for dependencies, operational order, maturity timelines |

---

## 5. Neutral Selection Layer

**Classification**: Missing | **Integration Value**: Medium

### What the pattern proposes

A model-agnostic, vendor-independent selection layer that makes organizational context portable across models, agents, and sessions. Components: Model-Agnostic Context Format, Context Router, Multi-Tenant Registry, Vendor Adapter. The core thesis: context is the organization's most durable asset in agentic systems and should not be soldered to vendor-specific memory features.

### What the repository has

The repo has philosophical alignment but no implementation:

- **LLM as Fuzzy Compiler**: Mental model that code is a disposable build artifact and constraints are the durable asset — promotes independence from specific model outputs ([[docs/canonical/llm-as-fuzzy-compiler|LLM as Fuzzy Compiler]]:25).
- **`obsidian-eval` CLI**: Cross-vault context retrieval tool that queries Obsidian vaults independently of any single model. Could serve as a primitive neutral retrieval layer but is a CLI, not a selection architecture.

### What is missing (NOT_FOUND)

Searched `docs/canonical/` for "neutral", "model-agnostic", "vendor", "vendor-independent", "cross-model", "selection layer", "portable context":

1. **Model-Agnostic Context Format**: No standardized schema for context units that any model can consume. The repo's context is stored in Markdown with Obsidian frontmatter — designed for human consumption, not as a model-agnostic machine-readable format.
2. **Context Router**: No routing layer that receives queries from any agent/model and routes to appropriate selection strategy.
3. **Multi-Tenant Registry**: No registry tracking which context belongs to which agent, session, and model with isolation and sharing policies.
4. **Vendor Adapter**: No translation layer from model-agnostic format to model-native input format.

**Locations searched**: All 85 canonical docs, system-of-record pattern inventory. The only mention of vendor/model independence is `llm-as-fuzzy-compiler.md:25` ("no guarantees about consistency across model versions") — focused on code generation, not context selection.

### Evidence

| File | Line | Evidence |
|---|---|---|
| `docs/canonical/llm-as-fuzzy-compiler.md` | 25 | "The LLM is a probabilistic transformer with no guarantees about consistency across model versions" — philosophical alignment with model independence |

---

## 6. Context Health Monitoring

**Classification**: Partial Coverage | **Integration Value**: High

### What the pattern proposes

Continuous monitoring of context health beyond token budgets: effective context size (fraction of window reliably usable), near-miss rate (retrieved context that was irrelevant), and contradiction rate (outputs contradicting prior decisions). A health score predicts proximity to the cliff before degradation becomes catastrophic, enabling preemptive intervention (context flush and reload).

### What the repository has

The repo has sophisticated token-budget-oriented health monitoring that covers many related concerns:

- **Phase-Gated Token Health Monitor**: Converts budget percentage and burn rate into green/yellow/orange/red phases with deterministic actions (continue, monitor, summarize, compress, new_session, handoff). Operates as a pre-call gate rather than post-failure reactive mechanism ([[docs/canonical/phase-gated-token-health-monitor|Phase-Gated Token Health Monitor]]:29-55).
- **Burn-Rate Runtime Forecast**: Predicts session runway from consumption velocity, acceleration, and reserved capacity. Addresses the "large remaining context can still be unsafe when burn rate accelerates" scenario ([[docs/canonical/burn-rate-runtime-forecast|Burn-Rate Runtime Forecast]]:31-54).
- **Tested Degradation Ladder**: Classifies failures by severity (retryable/unsafe/hold) with ordered rungs: retry → safe fallback → human escalation → outcome log ([[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29-65).
- **Failure Pattern Classification Loop**: Classifies observed failures into root cause classes and maps to guardrail surfaces ([[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]:31).
- **Late-Failure Regression Suite**: Preserves late-session forgetting failures as durable regression cases ([[docs/canonical/late-failure-regression-suite|Late-Failure Regression Suite]]:20-42).
- **N+1 Long-Session Evals**: Validates that prior constraints survive context reduction ([[docs/canonical/n-plus-one-long-session-evals|N+1 Long-Session Evals]]:20-40).

### What is missing

The repo's monitoring is **token-budget-oriented** (how many tokens remain, how fast are they burning), not **context-quality-oriented**. Missing components:

1. **Effective Context Estimator**: No mechanism measures what fraction of the window the model reliably attends to (accounting for head/tail attention bias). The burn-rate forecast predicts runway from token velocity, not attention effectiveness.
2. **Near-Miss Detector**: No comparison of retrieved context against task requirements to flag context that entered the window but was irrelevant. The repo does not measure retrieval quality at runtime.
3. **Contradiction Scanner**: No comparison of model outputs against prior decisions stored in the relational graph. The generator-evaluator architecture evaluates output quality but does not scan for contradictions against prior decisions.
4. **Health Score Aggregator**: No combined metric that merges effective context, near-miss rate, and contradiction rate into a single trajectory score. The phase-gated monitor produces a single score from budget percentage and burn rate only.

The repo's `phase-gated-token-health-monitor.md` is a **Better Implementation** of **token health monitoring** but the pattern's concept of **context health** (quality metrics beyond token count) is **Partial Coverage**.

### Evidence

| File | Line | Evidence |
|---|---|---|
| `docs/canonical/phase-gated-token-health-monitor.md` | 29-55 | Token monitor: green/yellow/orange/red phases with deterministic actions; operates pre-call |
| `docs/canonical/burn-rate-runtime-forecast.md` | 31-54 | Burn-rate forecast with acceleration detection and runway estimation |
| `docs/canonical/tested-degradation-ladder.md` | 29-65 | Degradation classification: retryable/unsafe/hold with ordered rungs |
| `docs/canonical/failure-pattern-classification-loop.md` | 31 | "Classify every observed agent failure into a root cause class" |
| `docs/canonical/late-failure-regression-suite.md` | 20-42 | Late-session context failures preserved as durable regression cases |
| `docs/canonical/n-plus-one-long-session-evals.md` | 20-40 | Validates prior constraints, preferences, and decisions survive context reduction |

---

## 7. Selection-Budgeted Retrieval

**Classification**: Missing | **Integration Value**: High

### What the pattern proposes

Cost-benefit ranking of retrieval candidates by token cost vs. predicted information value, with a utility feedback loop that learns which retrievals were actually referenced. Prevents the memory feedback loop where "every retrieval adds tokens, every added token shrinks effective context, and the system built to help becomes the engine of failure." Components: Token Cost Estimator, Information Value Predictor, Budget Tracker, Utility Feedback Loop.

### What the repository has

The repo has the two foundational pieces that Selection-Budgeted Retrieval would bridge, but neither is retrieval-aware:

- **Token budget tracking**: Explicit Token Budget Ledger computes per-call remaining budget and recommends continue/monitor/compact/retrieve/handoff actions, but `retrieve` as an action is listed without cost-benefit ranking of individual retrieval candidates ([[docs/canonical/explicit-token-budget-ledger|Explicit Token Budget Ledger]]:63).
- **Retrieval infrastructure**: Addressable Memory Catalog provides stable IDs, previews, and fetch handles for omitted content — the retrieval mechanism exists but without budget awareness ([[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]]:28-43).
- **Semantic topic bucketing**: Groups context by topic for targeted retrieval, but no per-topic retrieval budget allocation ([[docs/canonical/semantic-topic-bucketing|Semantic Topic Bucketing]]:92).

### What is missing (NOT_FOUND)

Searched `docs/canonical/` for "retrieval budget", "selection-budgeted", "information value", "utility feedback", "retrieval cost", "cost-benefit retrieval":

1. **Information Value Predictor**: No mechanism estimates the expected reduction in task uncertainty if a candidate context item is retrieved. The repo retrieves by handle or topic, not by predicted utility.
2. **Cost-Benefit Ranking**: No ranking of retrieval candidates by value/cost ratio with budget allocation from most to least valuable. The addressable-memory-catalog makes content retrievable but does not guide *which* to retrieve under budget constraints.
3. **Utility Feedback Loop**: No instrumentation to track which retrieved items the model actually referenced, and no feedback mechanism that updates retrieval utility estimates based on actual usage.
4. **Token Cost Estimator for retrieval**: The explicit token budget ledger estimates total call cost but does not estimate per-retrieval-candidate token costs for ranking decisions.

**Locations searched**: All 85 canonical docs. The gap is explicit: the budget ledger has a `retrieve` action but no mechanism for deciding *what* to retrieve within a budget; the addressable memory catalog enables retrieval but without budget constraints.

### Evidence

| File | Line | Evidence |
|---|---|---|
| `docs/canonical/explicit-token-budget-ledger.md` | 63 | `action` field includes "retrieve" as a loop decision, but no retrieval candidate ranking |
| `docs/canonical/addressable-memory-catalog.md` | 28-43 | Memory catalog with id, kind, location, preview for retrieval — retrieval mechanism without budget awareness |
| `docs/canonical/semantic-topic-bucketing.md` | 92 | "No canonical doc defines per-topic summary and retention policy for topic buckets" — adjacent gap |

---

## 8. Agent Degradation Loop Prevention

**Classification**: Partial Coverage | **Integration Value**: High

### What the pattern proposes

A diagnostic framework that models agent degradation in long-running tasks as a self-reinforcing 4-link feedback loop: (1) unequal context attention → (2) compounding errors → (3) state externalization → (4) inert memory feedback. Each link has a specific interceptor: structured context ordering, verification gate, relational state externalization, and budgeted retrieval. The loop model explains why standalone fixes fail — solving only one link leaves the other three to drive degradation.

### What the repository has

The repo extensively addresses individual links of the degradation loop, with sophisticated infrastructure for 3 of the 4 links:

**Link 1 (Unequal Context Attention)** — Partial Coverage:
- Head-tail truncation preserves head anchors (goal, constraints) and tail state (latest turns, current request) in active context, ensuring critical tokens are at positions the model attends to ([[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation]]:28-39).
- However, this is structural (fixed head/tail), not attention-profile-driven placement.

**Link 2 (Compounding Errors)** — Strong Coverage:
- Error Context Hygiene prevents error pollution: summarize failures into one line, inject with attempt count, clear on success ([[docs/canonical/error-context-hygiene|Error Context Hygiene]]:93-106).
- Tested Degradation Ladder classifies failures and provides ordered recovery: retry → safe fallback → human escalation ([[docs/canonical/tested-degradation-ladder|Tested Degradation Ladder]]:29-65).
- Generator-Evaluator separates generation from evaluation, reducing self-evaluation confirmation bias from ~3% to ~14% error detection ([[docs/canonical/generator-evaluator|Generator-Evaluator]]:27-31).
- Constraint-Anchored Evaluation anchors every evaluation to explicit, verifiable constraints from persisted state ([[docs/canonical/constraint-anchored-evaluation|Constraint-Anchored Evaluation]]:31).

**Link 3 (State Externalization)** — Strong Coverage:
- External State Persistence decouples agent memory from model memory, externalizing critical state (allergies, preferences, constraints) to persistent storage loaded every turn ([[docs/canonical/external-state-persistence|External State Persistence]]:31-57).
- Versioned Durable Agent State provides versioned schemas, migration, writeback, and reload ([[docs/canonical/versioned-durable-agent-state|Versioned Durable Agent State]]:25).

**Link 4 (Inert Memory Feedback)** — Not Covered:
- The Addressable Memory Catalog makes content retrievable but without budget awareness — retrieval can still feed the feedback loop by adding tokens indiscriminately.
- Selection-Budgeted Retrieval (pattern 7, classified as Missing) is the Link 4 interceptor.

### What is missing

The repo has strong individual link coverage but lacks the unified diagnostic framework:

1. **Diagnostic Classification**: No mechanism identifies *which* link is currently driving degradation. The failure pattern classification loop classifies root causes but does not map them to degradation loop links ([[docs/canonical/failure-pattern-classification-loop|Failure Pattern Classification Loop]]:31).
2. **Link-Specific Interceptor Orchestration**: The individual patterns exist (head-tail for link 1, error hygiene + degradation ladder for link 2, external state for link 3) but are not orchestrated as a coordinated defense system with link-specific triggers.
3. **Degradation Trajectory Forecast**: No mechanism estimates time-to-cliff based on which link is currently dominant.
4. **Cross-Link Interaction Awareness**: No documentation of how optimizing one link can shift pressure to another (e.g., aggressive truncation solves link 1 but worsens link 3 if state is lost).

### Evidence

| File | Line | Evidence |
|---|---|---|
| `docs/canonical/head-tail-context-truncation.md` | 28-39 | Link 1: Bounded active context with head/tail anchors. Structural, not attention-profile-driven |
| `docs/canonical/error-context-hygiene.md` | 93-106 | Link 2: Bounded retry with summarized errors, attempt count, cleanup on success |
| `docs/canonical/tested-degradation-ladder.md` | 29-65 | Link 2: Ordered degradation rungs: classify → retry → safe fallback → human escalation → log |
| `docs/canonical/generator-evaluator.md` | 27-31 | Link 2: Self-evaluation detects ~3%, external evaluation detects ~14% of real errors |
| `docs/canonical/external-state-persistence.md` | 31-57 | Link 3: Extract → write → load → merge → respond cycle; decouples agent from model memory |
| `docs/canonical/versioned-durable-agent-state.md` | 25 | Link 3: Durable state with schema, migration, writeback, and audit trail |
| `docs/canonical/failure-pattern-classification-loop.md` | 31 | Adjacent: classifies failures by root cause, but does not map to degradation loop links |

---

## Summary Table

| # | Pattern | Classification | Integration Value |
|---|---|---|---|
| 1 | Deliberate Forgetting | Partial Coverage | High |
| 2 | Smallest Sufficient Context | Partial Coverage | High |
| 3 | Tiered Context Storage with Promotion/Demotion | Missing | Medium |
| 4 | Relational Context Graph | Partial Coverage | High |
| 5 | Neutral Selection Layer | Missing | Medium |
| 6 | Context Health Monitoring | Partial Coverage | High |
| 7 | Selection-Budgeted Retrieval | Missing | High |
| 8 | Agent Degradation Loop Prevention | Partial Coverage | High |

### Classification Summary

- **Partial Coverage**: 5 patterns (1, 2, 4, 6, 8) — the repo has substantial adjacent infrastructure, component pieces, or related patterns, but key mechanics, formalizations, or unified contracts are missing.
- **Missing**: 3 patterns (3, 5, 7) — no equivalent exists in any form (doc, code, or curriculum). Tiered Storage has no tier-based architecture; Neutral Selection Layer has no model-agnostic context format or routing; Selection-Budgeted Retrieval has no retrieval cost-benefit ranking.

### Integration Priority

All 8 patterns target the core harness concern of context engineering, which is the repo's primary domain. Patterns marked "High" integration value directly extend existing canonical patterns. Patterns marked "Medium" (Tiered Context Storage, Neutral Selection Layer) require new infrastructure that is architecturally significant but would benefit from building on existing foundations (addressable-memory-catalog for tiered storage; llm-as-fuzzy-compiler philosophy for neutral layer).

### Cross-Pattern Dependencies

Per the source patterns YAML ([[docs/analysis/2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns|patterns.md]]:389-412), the Relational Context Graph is the foundation of all other selection patterns. Deliberate Forgetting and Smallest Sufficient Context both require it. Tiered Context Storage enables Deliberate Forgetting and Selection-Budgeted Retrieval. Selection-Budgeted Retrieval directly counters Link 4 of the Agent Degradation Loop. The Neutral Selection Layer wraps the Relational Context Graph and Tiered Context Storage as a vendor-independent interface.

This dependency graph means integration should start with the Relational Context Graph (pattern 4) as the foundational building block, then layer Selection-Budgeted Retrieval (pattern 7) and Tiered Context Storage (pattern 3) on top.

---

*Generated: 2026-06-18 | Phase 3: Pattern Classification | Analysis pipeline*
