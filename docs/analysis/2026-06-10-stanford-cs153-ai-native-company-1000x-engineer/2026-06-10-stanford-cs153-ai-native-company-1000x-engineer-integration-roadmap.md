---
title: "Integration Roadmap: Stanford CS153 AI Native Company Patterns"
type: analysis
date: 2026-06-10
tags: ["agentes-orquestracao", "curriculo-conteudo", "context-engineering", "evals", "governanca"]
aliases: ["roadmap CS153", "integracao CS153", "AI-native roadmap", "Stanford patterns"]
last_updated: 2026-06-10
relates-to: ["[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification>|Stanford CS153 Classification]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-mental-model>|Stanford CS153 Mental Model]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/INDEX|Curriculum Index]]"]
sources: ["[[docs/system-of-record|System of Record]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis>|Stanford CS153 Analysis]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns>|Stanford CS153 Patterns]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification>|Stanford CS153 Classification]]", "[[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-mental-model>|Stanford CS153 Mental Model]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/INDEX|Curriculum Index]]"]
---
# Integration Roadmap: Stanford CS153 AI Native Company Patterns

## Scope

This roadmap maps the 11 classified Stanford CS153 AI Native Company patterns from [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification>|classification]] into concrete integration points for `long-running-agents`. It uses the repository precedence model in [[docs/system-of-record|System of Record]], the repository orientation in [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-mental-model>|mental-model]], and the level structure in [[curriculum/README|curriculum README]] and [[curriculum/INDEX|curriculum index]].

Priority is assigned as follows:

| Priority | Meaning |
|---|---|
| P0 | High integration value or newly canonicalized capability that should become part of the operating model soon |
| P1 | Medium integration value that should be integrated after P0 surfaces are stable |
| P2 | Low integration value because the repo already has equivalent or stronger coverage |

## Summary Matrix

| # | Pattern | Classification | Impact | Effort | Priority | Integration Surface |
|---|---|---|---|---|---|---|
| 1 | Closed-Loop Agent Operating System | Partial Coverage | High: unifies governance, orchestration, issue lifecycle, analysis, validation, and memory writeback into one operating loop | Medium: canonical exists, but operational writeback policy and observability still need design | P0 | [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]], [[docs/system-of-record|System of Record]], [[.opencode/skills/orchestrator/SKILL|orchestrator skill]], [[.opencode/skills/analyze-and-improve/SKILL|analyze-and-improve skill]], issue lifecycle skills |
| 2 | Agentic Software Factory Quality Gate | Better Implementation | Medium: useful Stanford label for the existing anti-slop gate, but the repo already has stronger PR and eval enforcement | Low: mostly aliasing and cross-reference work unless a dedicated canonical doc is created later | P2 | [[.opencode/skills/issue-review/SKILL|issue-review skill]], [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]], [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]], [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]], repository validation gates |
| 3 | Latent-Deterministic Boundary Enforcement | Already Exists | Medium: important teaching frame, but equivalent mechanics already exist under deterministic dispatch and multi-agent coordination | Low: add alias or curriculum callout only | P2 | [[docs/canonical/deterministic-tool-dispatch|Deterministic Tool Dispatch]], [[curriculum/05-core-concepts/07-multi-agent-coordination|Multi-Agent Coordination]], [[curriculum/07-implementation-guides/03-harness-design-checklist|Harness Design Checklist]] |
| 4 | Skill-Resolver-Skillify Capability Pipeline | Partial Coverage | High: turns successful workflows into tested, routable, deduplicated agent capabilities | High: requires resolver metadata schema, trigger evals, check-resolvable, smoke evidence, and storage conventions | P0 | [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]], [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]], `.opencode/skills/`, [[docs/canonical/pr-gated-eval-enforcement|PR-Gated Eval Enforcement]] |
| 5 | Resolver-Based Context Progressive Disclosure | Partial Coverage | High: reduces global instruction bloat and makes skill loading testable | Medium: canonical exists, but skill trigger examples, negative triggers, and resolver eval fixtures still need implementation | P0 | [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]], `.opencode/skills/`, [[docs/canonical/stable-harness-prompt|Stable Harness Prompt During Context Reduction]], [[docs/canonical/head-tail-context-truncation|Head-Tail Context Truncation with Recoverable Middle]] |
| 6 | Split-Brain Planning Review | Partial Coverage | Medium: improves high-impact planning by separating engineering feasibility from product destination | Medium: canonical exists; next work is rubrics, trigger policy, and reconciliation records | P1 | [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]], [[.opencode/skills/refine-issue/SKILL|refine-issue skill]], [[.opencode/skills/writing-plans/SKILL|writing-plans skill]], [[.opencode/skills/issue-start/SKILL|issue-start skill]] |
| 7 | Multi-Model Evaluation Council | Partial Coverage | Medium: strengthens high-risk evals by adding model diversity and disagreement policy | Medium to High: needs model-selection policy, cost tiering, aggregation, and calibration tracking | P1 | [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]], [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]], [[docs/canonical/eval-tier-stratification|Eval Tier Stratification]], [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] |
| 8 | Trace-Eval-Replay Self-Healing Flywheel | Already Exists | Medium: the label is useful, but the repo already has the same flywheel at canonical depth | Low: naming alignment and curriculum cross-reference only | P2 | [[docs/canonical/production-failure-regression-flywheel|Production Failure Regression Flywheel]], [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]], [[curriculum/07-implementation-guides/05-trace-analysis-guide|Trace Analysis Guide]] |
| 9 | Epistemic Memory Graph | Partial Coverage | Medium: extends addressable memory and knowledge graphs with belief-status-aware retrieval | High: requires schema, ontology governance, freshness metadata, retrieval fusion, and implementation ownership | P1 | [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]], [[docs/canonical/addressable-memory-catalog|Addressable Memory Catalog]], [[curriculum/06-knowledge-graphs/01-concept-ecosystem|Concept Ecosystem]], [[curriculum/08-tools-templates/knowledge-graph-template|Knowledge Graph Template]] |
| 10 | Taste-to-Domain-Eval Ownership Loop | Better Implementation | Medium: valuable Stanford framing, but KODA rubrics and eval correlation already cover the mechanism deeply | Low: add alias and navigation to existing KODA eval material | P2 | [[curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda|KODA Evaluation Rubrics]], [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]], [[docs/canonical/eval-to-production-correlation-tracking|Eval-to-Production Correlation Tracking]] |
| 11 | Domain-Embedded Workflow Automation Wedge | Partial Coverage | Medium: improves how new domain automations are discovered before implementation | Medium: canonical exists; templates and wedge-selection rubric remain uncovered | P1 | [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]], [[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|KODA Customer Journey Flows]], [[curriculum/09-case-studies/04-koda-order-processing|KODA Order Processing Case Study]], [[docs/canonical/production-grounded-eval-sampling|Production-Grounded Eval Sampling]] |

## Recommended Integration Sequence

| Phase | Priority | Patterns | Concrete Integration Points | Done When |
|---|---|---|---|---|
| 1. Operating loop and context routing | P0 | Closed-Loop Agent Operating System; Skill-Resolver-Skillify Capability Pipeline; Resolver-Based Context Progressive Disclosure | Add the closed-loop OS as the top-level operating frame for `.opencode` work; define skill resolver metadata; add positive and negative trigger examples for reusable skills; define writeback destinations for outcomes | New agent capabilities are routed through tested skills, and significant outcomes have a documented writeback target |
| 2. Planning and evaluation governance | P1 | Split-Brain Planning Review; Multi-Model Evaluation Council | Add dual planning-review rubrics for high-impact work; define model council trigger thresholds; attach council output to medium/deep eval gates | High-impact plans have separate engineering and product-destination review, and high-risk evals have aggregation and disagreement policy |
| 3. Memory and domain discovery | P1 | Epistemic Memory Graph; Domain-Embedded Workflow Automation Wedge | Define belief-status metadata for memory entries; create shadowing-note, decision-inventory, and wedge-selection templates; convert observed edge cases into eval seeds | New domain automations start from observed work and memory entries expose epistemic status before retrieval is trusted |
| 4. Naming alignment and curriculum navigation | P2 | Agentic Software Factory Quality Gate; Latent-Deterministic Boundary Enforcement; Trace-Eval-Replay Self-Healing Flywheel; Taste-to-Domain-Eval Ownership Loop | Add aliases and cross-links to existing canonical docs and curriculum pages instead of creating duplicate systems | Stanford labels route readers to the stronger existing implementation without duplicating concepts |

## Artifacts Created During This Analysis Session

### Analysis Package

The Stanford CS153 analysis package now contains these analysis artifacts:

| Artifact | Status | Role |
|---|---|---|
| [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-mental-model>|mental-model.md]] | Created | Repository orientation before external-source comparison |
| `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-mental-model.yaml` | Created | Structured form of the repository mental model |
| [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis>|analysis.md]] | Created | Non-obvious knowledge extraction from the Stanford CS153 source |
| `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis.yaml` | Created | Structured extraction output |
| [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns>|patterns.md]] | Created | 11 agentic patterns extracted from the analysis |
| `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns.yaml` | Created | Structured pattern catalog |
| [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification>|classification.md]] | Created | Classification of all 11 patterns against the repo |
| `docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification.yaml` | Created | Structured classification output |
| [[docs/analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-integration-roadmap>|integration-roadmap.md]] | Created by this step | Integration map from classified patterns to repository surfaces |

### Canonical Docs

The following canonical docs from this session now exist and should be treated as document-level 2 sources under [[docs/system-of-record|System of Record]] precedence:

| Canonical Doc | Pattern Covered | Status |
|---|---|---|
| [[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]] | Pattern 1 | Created |
| [[docs/canonical/skill-resolver-skillify-capability-pipeline|Skill-Resolver-Skillify Capability Pipeline]] | Pattern 4 | Created |
| [[docs/canonical/resolver-based-context-progressive-disclosure|Resolver-Based Context Progressive Disclosure]] | Pattern 5 | Created |
| [[docs/canonical/split-brain-planning-review|Split-Brain Planning Review]] | Pattern 6 | Created |
| [[docs/canonical/multi-model-evaluation-council|Multi-Model Evaluation Council]] | Pattern 7 | Created |
| [[docs/canonical/epistemic-memory-graph|Epistemic Memory Graph]] | Pattern 9 | Created |
| [[docs/canonical/domain-embedded-workflow-automation-wedge|Domain-Embedded Workflow Automation Wedge]] | Pattern 11 | Created |
| `docs/canonical/agentic-software-factory-quality-gate.md` | Pattern 2 | Not created in this checkout; the pattern is currently covered through existing issue-review and eval-gate docs |

No new canonical doc was required for Pattern 3, Pattern 8, or Pattern 10 because the classification marked them as `Already Exists` or `Better Implementation` and pointed to existing stronger surfaces.

## Curriculum Cross-Reference

The curriculum has four levels: Level 1 fundamentals, Level 2 practical patterns, Level 3 advanced architecture, and Level 4 KODA-specific application. It also has 8 core concepts, implementation guides, templates, knowledge graphs, and case studies. The mapping below shows where each Stanford pattern should enter the learning path.

| # | Pattern | Primary Curriculum Level | Supporting Curriculum Surfaces | Curriculum Integration |
|---|---|---|---|---|
| 1 | Closed-Loop Agent Operating System | Level 3 and Level 4 | [[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems|Multi-Agent Systems]], [[curriculum/03-nivel-3-advanced-architecture/05-harness-evolution|Harness Evolution]], [[curriculum/04-nivel-4-koda-specific/05-harness-improvements|KODA Harness Improvements]] | Teach as the macro operating loop that connects issue lifecycle, memory, evals, and writeback after students understand multi-agent coordination |
| 2 | Agentic Software Factory Quality Gate | Level 2 and Level 3 | [[curriculum/02-nivel-2-practical-patterns/02-sprint-contracts|Sprint Contracts]], [[curriculum/02-nivel-2-practical-patterns/03-rubric-design|Rubric Design]], [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]] | Use as an alias for the existing anti-slop validation gate and route learners to eval tiers, PR gates, and production-grounded sampling |
| 3 | Latent-Deterministic Boundary Enforcement | Level 2 and Level 3 | [[curriculum/05-core-concepts/07-multi-agent-coordination|Multi-Agent Coordination]], [[curriculum/03-nivel-3-advanced-architecture/01-multi-agent-systems|Multi-Agent Systems]], [[curriculum/07-implementation-guides/03-harness-design-checklist|Harness Design Checklist]] | Add the Stanford name as a boundary-check lens: deterministic services own exactness, agents own semantic judgment |
| 4 | Skill-Resolver-Skillify Capability Pipeline | Level 3 | [[curriculum/03-nivel-3-advanced-architecture/03-file-based-coordination|File-Based Coordination]], [[curriculum/03-nivel-3-advanced-architecture/05-harness-evolution|Harness Evolution]], [[curriculum/08-tools-templates|Tools and Templates]] | Add a capability lifecycle module after students know state persistence and coordination: capture workflow, skillify, test, register, smoke |
| 5 | Resolver-Based Context Progressive Disclosure | Level 1 and Level 3 | [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]], [[curriculum/05-core-concepts/01-context-management|Context Management]], [[curriculum/03-nivel-3-advanced-architecture/04-server-side-compaction|Server-Side Compaction]] | Introduce as an advanced answer to context-window pressure: do not load every rule globally; route instructions through resolver-visible skills |
| 6 | Split-Brain Planning Review | Level 2 and Level 4 | [[curriculum/05-core-concepts/02-planning-execution-separation|Planning vs Execution]], [[curriculum/05-core-concepts/04-sprint-contracts|Sprint Contracts]], [[curriculum/04-nivel-4-koda-specific/03-feature-design-patterns|KODA Feature Design Patterns]] | Teach as a high-impact planning gate that separates engineering feasibility from product-destination ambition |
| 7 | Multi-Model Evaluation Council | Level 2 and Level 3 | [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]], [[curriculum/02-nivel-2-practical-patterns/03-rubric-design|Rubric Design]], [[curriculum/06-knowledge-graphs/detailed-graphs/evaluation-rubrics-graphs|Evaluation Rubrics Graphs]] | Extend existing dual/ensemble evaluator material with model diversity, aggregation policy, and disagreement escalation |
| 8 | Trace-Eval-Replay Self-Healing Flywheel | Level 2 and Level 4 | [[curriculum/02-nivel-2-practical-patterns/04-trace-reading|Trace Reading]], [[curriculum/07-implementation-guides/05-trace-analysis-guide|Trace Analysis Guide]], [[curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda|KODA Evaluation Rubrics]] | Route learners from trace diagnosis into production-failure regression and replay-based self-healing |
| 9 | Epistemic Memory Graph | Level 3 | [[curriculum/05-core-concepts/05-state-persistence|State Persistence]], [[curriculum/06-knowledge-graphs/01-concept-ecosystem|Concept Ecosystem]], [[curriculum/08-tools-templates/knowledge-graph-template|Knowledge Graph Template]] | Add belief-status-aware memory as the advanced form of state persistence and knowledge graph design |
| 10 | Taste-to-Domain-Eval Ownership Loop | Level 4 | [[curriculum/04-nivel-4-koda-specific/04-evaluation-rubrics-koda|KODA Evaluation Rubrics]], [[curriculum/05-core-concepts/08-evaluation-rubrics|Evaluation Rubrics]], [[curriculum/09-case-studies/03-koda-product-discovery|KODA Product Discovery Case Study]] | Use as a product-lead framing for the repo's existing KODA-specific rubric and eval ownership system |
| 11 | Domain-Embedded Workflow Automation Wedge | Level 4 | [[curriculum/04-nivel-4-koda-specific/02-customer-journey-flows|KODA Customer Journey Flows]], [[curriculum/09-case-studies/04-koda-order-processing|KODA Order Processing Case Study]], [[curriculum/09-case-studies/05-koda-fulfillment-workflow|KODA Fulfillment Workflow Case Study]] | Add a discovery-before-automation template: shadowing notes, decision inventory, edge-case catalog, wedge rubric, eval seeds |

## Gap Analysis

| Gap | Patterns Affected | Current Coverage | Remaining Work |
|---|---|---|---|
| No dedicated Software Factory canonical doc | Pattern 2 | Strong coverage exists through issue review, PR-gated evals, eval tiering, and production-grounded sampling | Decide whether the Stanford label warrants an alias section in existing docs or a small canonical overview; do not duplicate the existing quality gate system |
| Resolver lifecycle is canonical but not operationally enforced | Patterns 4 and 5 | Canonical docs exist for skillify pipeline and progressive disclosure | Define resolver metadata schema, negative triggers, trigger eval fixtures, check-resolvable command or checklist, deduplication policy, and smoke evidence expectations |
| Closed-loop OS lacks implementation observability | Pattern 1 | Canonical doc exists and current workflows have source precedence, orchestrator, issue lifecycle, and analysis loop | Track recommendations made, accepted, rejected, executed, blocked, and written back into durable memory |
| Feedback writeback policy is still underspecified | Patterns 1, 8, 10, 11 | System-of-record precedence exists; eval and regression flywheel docs cover some writeback cases | Define what outcomes become canonical docs, evidence, analysis artifacts, issue comments, eval fixtures, or ephemeral notes |
| Planning review lacks dual rubrics and reconciliation record | Pattern 6 | Split-brain planning canonical doc exists; planning/execution separation already exists in curriculum | Add engineering-review rubric, product-destination rubric, trigger policy for high-impact plans, and durable disagreement/reconciliation format |
| Evaluation council lacks model-selection and aggregation policy | Pattern 7 | Curriculum has dual/ensemble evaluator concept; canonical council doc exists | Define model diversity criteria, score aggregation, blocker handling, divergence thresholds, cost tiering, and calibration storage |
| Epistemic memory is documented but not implemented | Pattern 9 | Addressable memory catalog and knowledge graph curriculum exist; epistemic canonical doc exists | Add schema for epistemic status, ownership, freshness, validity scope, retrieval fusion, ontology governance, and migration rules |
| Domain wedge lacks reusable templates | Pattern 11 | KODA domain workflows and case studies exist; wedge canonical doc exists | Add shadowing-note template, decision-inventory template, edge-case catalog format, wedge-selection rubric, and eval-seed conversion checklist |
| Curriculum navigation has not yet absorbed the new Stanford labels | All 11 | Curriculum already has matching levels and many equivalent concepts | Add aliases or callouts in relevant levels so learners can find these patterns without creating parallel duplicate modules |
| System-of-record has not yet been updated for the new Stanford canonical docs | Patterns 1, 4, 5, 6, 7, 9, 11 | `docs/canonical/` contains the new docs, but the current system-of-record canonical list predates them | Update [[docs/system-of-record|System of Record]] in a separate governance task so active canonical pattern count and list match the checkout |

## Roadmap Decisions

1. Do not create duplicate canonical systems for patterns already marked `Already Exists` or `Better Implementation`; integrate them through aliases, references, and curriculum navigation.
2. Treat the three High integration value gaps as the first operating-system increment: closed-loop OS, skillify capability lifecycle, and resolver-based context disclosure.
3. Treat P1 patterns as governance and learning-depth expansions after P0 routing and writeback are stable.
4. Keep Level 4 focused on KODA and domain workflows; introduce domain wedge and taste-to-eval ownership there rather than in generic foundations.
5. Keep Pattern 9 tied to memory and graph infrastructure, not generic documentation search, because the missing value is epistemic status and retrieval fusion.

## Next Integration Backlog

| Order | Backlog Item | Output |
|---|---|---|
| 1 | Add resolver metadata and trigger-eval contract for `.opencode/skills/` | Canonical schema or guide plus one migrated skill example |
| 2 | Define closed-loop writeback policy | Table mapping outcome types to canonical, evidence, analysis, issue, eval, or archive destination |
| 3 | Add split-brain planning-review templates | Engineering rubric, product-destination rubric, reconciliation record |
| 4 | Add multi-model council policy | Model selection, aggregation, disagreement, escalation, and calibration policy |
| 5 | Add domain wedge templates to curriculum tools | Shadowing notes, decision inventory, edge-case catalog, wedge rubric, eval seed checklist |
| 6 | Add epistemic memory schema | Node fields, status taxonomy, ownership, freshness, retrieval fusion, ontology governance |
| 7 | Update curriculum navigation with Stanford aliases | Cross-links from levels and core concepts to the new canonical docs |
| 8 | Update system-of-record canonical list | Active canonical docs count and table reflect the 7 new canonical docs |
