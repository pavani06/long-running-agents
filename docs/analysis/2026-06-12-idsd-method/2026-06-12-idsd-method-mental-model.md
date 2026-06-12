---
title: "Mental Model: IDSD Method"
type: analysis
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness-engineering", "context-engineering", "evals", "governanca", "decision-discipline"]
date: 2026-06-12
aliases: ["idsd mental model", "modelo mental idsd", "repository mental model", "phase 0 idsd", "full rebuild mental model"]
last_updated: 2026-06-12
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[AGENTS|AGENTS.md]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/GLOSSARY|Glossary]]", "[[.opencode/skills/analyze-and-improve/SKILL|Analyze and Improve Skill]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/hybrid-context-stack|Hybrid Context Stack]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]"]
sources: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[AGENTS|AGENTS.md]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/MASTER_PLAN|Master Plan]]", "[[curriculum/INDEX|Curriculum Index]]", "[[curriculum/GLOSSARY|Glossary]]"]
---
# Mental Model: long-running-agents

**Date:** 2026-06-12  
**Repo:** `long-running-agents`  
**Type:** `mental-model`  
**Scope:** leitura somente do repositório antes de analisar a fonte externa IDSD.

## 1. Project Goals

`long-running-agents` é simultaneamente base de conhecimento, currículo e workspace operacional para agentes long-running. O problema central é a combinação de perda de contexto, planejamento frágil e autoavaliação cega; a resposta do repositório é ensinar e operacionalizar harnesses que gerenciam contexto, decompõem trabalho e separam geração de avaliação (`README.md:3-13`).

- Manter uma base de conhecimento e programa curricular para construir sistemas de IA que operam por horas ou dias sem perder contexto, planejamento ou julgamento de qualidade. Source: README.md:3-13.
- Ensinar builders de negócio e de sistemas agenticos, de iniciantes até operadores em produção que precisam elevar confiabilidade. Source: README.md:15-17.
- Tratar harnesses como a resposta central para perda de contexto, planejamento frágil e autoavaliação cega. Source: README.md:7-13; curriculum/README.md:21-34.
- Entregar um currículo de 12 semanas, 4 níveis, 8 conceitos core, 35+ diagramas, exercícios, templates e KODA como caso aplicado. Source: curriculum/README.md:13; curriculum/README.md:57-181.
- Operacionalizar trabalho agentic com `.opencode/`, Handoff Protocol, lifecycle de issues, gates de validação e documentação Obsidian. Source: AGENTS.md:7-12; docs/system-of-record.md:25-49; .opencode/skills/issue-start/SKILL.md:12-15.
- Executar análises externas futuras por um pipeline controlado que começa com este modelo mental e só depois extrai padrões da fonte externa. Source: .opencode/skills/analyze-and-improve/SKILL.md:47-57; .opencode/skills/analyze-and-improve/SKILL.md:166-244; PROGRESS.md:16-18.

## 2. Architecture

### Core Abstractions

| Abstraction | Role | Evidence |
|---|---|---|
| System of Record | Fonte de verdade de precedência documental e mapa de domínios do projeto. | `docs/system-of-record.md:12-21; docs/system-of-record.md:23-49` |
| Operational Contract | AGENTS.md define escopo de sessão, mudança mínima, validação, segurança, convenções Obsidian e disciplina de background agents. | `AGENTS.md:14-32; AGENTS.md:53-63; AGENTS.md:77-85; AGENTS.md:120-253` |
| Canonical Pattern Library | Biblioteca autoritativa de padrões de harness, contexto, evals, governança e arquitetura agentic. | `docs/system-of-record.md:131-197; directory inspection: docs/canonical -> 57 markdown files` |
| Curriculum | Produto principal: programa de 12 semanas com 4 níveis, 8 conceitos core, exercícios, knowledge graphs, guias, templates e estudos de caso. | `docs/system-of-record.md:53-79; curriculum/README.md:13; curriculum/MASTER_PLAN.md:173-263` |
| KODA Case Domain | Agente WhatsApp de venda de suplementos usado como caso aplicado para jornadas, features, rubricas e melhorias de harness. | `README.md:26-30; curriculum/GLOSSARY.md:300-311; curriculum/04-nivel-4-koda-specific/01-koda-architecture.md` |
| HoP Agent System | Camada `.opencode` com orquestrador primário, subagentes KODA e handoff operacional entre inicialização e teste live. | `docs/system-of-record.md:25-49; .opencode/agents/hop-orchestrator-rezek.md:21-39; .opencode/agents/koda-hop-init-basic.md:18-52; .opencode/agents/hop-live-whatsapp-tester.md:18-76` |
| Issue Lifecycle | Fluxo claim -> worktree -> brief -> validação -> draft PR -> review -> aprovação explícita -> merge -> cleanup. | `.opencode/skills/issue-start/SKILL.md:12-15; .opencode/skills/issue-review/SKILL.md:12-15; .opencode/skills/issue-finish/SKILL.md:12-15` |
| Analyze-and-Improve Harness | Pipeline de 7 fases que transforma fontes externas em modelo mental, extração, padrões, classificação, melhorias e integração. | `.opencode/skills/analyze-and-improve/SKILL.md:47-57; .opencode/skills/harness-analyze-and-improve/SKILL.md:12-41; .opencode/skills/harness-analyze-and-improve/SKILL.md:60-78` |
| Mental Model Cache | `mapa-mental-repo/` versiona modelos mentais por data e source slug para modo incremental; nesta tarefa, os modelos anteriores foram usados apenas como contexto e não copiados. | `.opencode/skills/analyze-and-improve/SKILL.md:145-163; mapa-mental-repo/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-mental-model.md:12-17; docs/analysis/2026-06-12-idsd-method/delta-report.md:26-28` |
| Stack and Validation Tooling | Projeto Node ESM com ESLint e scripts reais de lint/test; documentação validada por script Obsidian. | `README.md:107-113; package.json:1-21; scripts/check-obsidian-conventions.sh:18-323` |

### Relationships

| From | To | Relationship | Evidence |
|---|---|---|---|
| System of Record | Documentation surfaces | ADRs aceitos vencem canonicals, que vencem evidências, análises, arquivo e READMEs/resumos operacionais. | `docs/system-of-record.md:14-21; AGENTS.md:64-75` |
| Canonical Pattern Library | Curriculum | Os canonicals formalizam padrões que o currículo ensina como níveis, conceitos, exercícios, templates e rotas por pergunta. | `docs/system-of-record.md:131-197; curriculum/INDEX.md:179-234; curriculum/MASTER_PLAN.md:340-357` |
| Curriculum | KODA Case Domain | O currículo ensina padrões genéricos e os aplica em KODA no Nível 4 e em case studies KODA. | `curriculum/README.md:232-243; curriculum/INDEX.md:56-65; curriculum/INDEX.md:119-137` |
| HoP Agent System | Issue Lifecycle | Agentes e skills transformam trabalho agentic em sessões com escopo, worktree, brief, validação, review e cleanup. | `docs/system-of-record.md:25-49; .opencode/skills/issue-start/SKILL.md:24-171; .opencode/skills/issue-review/SKILL.md:44-100` |
| Application-Owned Control Plane | Owned Agent Control Loop | O control plane une prompt versionado, Context Builder, ação estruturada, dispatch determinístico, loop policy, estado persistente e gates. | `docs/canonical/application-owned-agent-control-plane.md:27-75; docs/canonical/owned-agent-control-loop.md:29-75` |
| Hybrid Context Stack | External State and Memory Catalog | Contexto ativo é montado por camadas com prompt estável, estado durável, head/tail anchors, summaries e catálogo recuperável. | `docs/canonical/hybrid-context-stack.md:28-42; docs/canonical/addressable-memory-catalog.md; docs/canonical/external-state-persistence.md` |
| Eval Tier Stratification | PR and Production Quality Gates | Evals são estratificados em fast, medium e deep para preservar inner loop rápido e ainda bloquear PRs/releases quando necessário. | `docs/canonical/eval-tier-stratification.md:20-72; .github/PULL_REQUEST_TEMPLATE.md:20-58` |
| Manual Brake and Deferred Ledger | Agent Execution | Gates de valor e ledger de dívida impedem que tokens baratos transformem trabalho de baixo valor em inventário permanente. | `docs/canonical/manual-brake-question-gate.md:21-73; docs/canonical/deferred-ledger-agentic-work.md:21-78` |
| Mental Model Cache | Current IDSD Rebuild | Modelos anteriores em `mapa-mental-repo/` orientam contexto incremental, mas o delta count forçou rebuild completo e os dois outputs desta análise são artefatos novos do Phase 0. | `.opencode/skills/analyze-and-improve/SKILL.md:145-179; PROGRESS.md:16-18; docs/analysis/2026-06-12-idsd-method/delta-report.md:26-28` |

### Cluster Mental Model

- **Governança:** `AGENTS.md` define como trabalhar; `docs/system-of-record.md` define qual fonte vence quando documentos divergem (`AGENTS.md:14-32`, `docs/system-of-record.md:14-21`).
- **Produto principal:** `curriculum/` ensina long-running agent reliability por progressão de níveis e aplica tudo em KODA (`docs/system-of-record.md:53-79`, `curriculum/README.md:13-34`).
- **Biblioteca canônica:** `docs/canonical/` registra o vocabulário técnico ativo; a árvore atual contém 57 Markdown files, enquanto o SOR ainda declara 55 (`docs/system-of-record.md:131-197`, `directory inspection: docs/canonical -> 57 markdown files`).
- **Operação agentic:** `.opencode/` transforma padrões em agentes, skills, issue lifecycle, review e gates de valor (`docs/system-of-record.md:25-49`, `.opencode/skills/issue-start/SKILL.md:24-171`).
- **Pipeline de análise:** `analyze-and-improve` exige este modelo mental como Phase 0 antes de qualquer extração de conhecimento externo (`.opencode/skills/analyze-and-improve/SKILL.md:166-244`, `PROGRESS.md:16-18`).
- **Cache de modelos mentais:** `mapa-mental-repo/` guarda modelos anteriores para execução incremental; este artefato registra full rebuild porque `delta-report.md` classificou 14 deltas e excedeu o limite (`.opencode/skills/analyze-and-improve/SKILL.md:145-163`, `docs/analysis/2026-06-12-idsd-method/delta-report.md:26-28`).

## 3. Patterns

A tabela abaixo inclui todos os 57 arquivos Markdown atualmente presentes em `docs/canonical/*.md`. A maturidade vem dos campos `Status`, `Classification` e `Source` de cada documento canônico; quando houver divergência de contagem, a árvore atual vence para este rebuild.

| Pattern | Where Defined | Maturity |
|---|---|---|
| Accidental Brake Replacement | `docs/canonical/accidental-brake-replacement.md` | Status: active; Classification: Missing, Low integration value; Source: analysis/2026-06-11-the-trap-spec-driven-development-is-setting/. Evidence: docs/canonical/accidental-brake-replacement.md:14-16. |
| Addressable Memory Catalog | `docs/canonical/addressable-memory-catalog.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-09-how-we-solved-context-management-in-agents/. Evidence: docs/canonical/addressable-memory-catalog.md:13-15. |
| Application-Owned Agent Control Plane | `docs/canonical/application-owned-agent-control-plane.md` | Status: Active; Classification: Partial Coverage; Source: docs/articles/harness-evolution-metodos-construcao.md. Evidence: docs/canonical/application-owned-agent-control-plane.md:14-16. |
| Architecture-as-Agent-Affordance Refactoring | `docs/canonical/architecture-as-agent-affordance.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/. Evidence: docs/canonical/architecture-as-agent-affordance.md:13-15. |
| Budget-Aware Session Handoff | `docs/canonical/budget-aware-session-handoff.md` | Status: Active; Classification: Partial Coverage ([[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-classification|Token Budgeting Pattern Classification]]:104-112); Source: [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] and [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]. Evidence: docs/canonical/budget-aware-session-handoff.md:14-16. |
| Burn-Rate Runtime Forecast | `docs/canonical/burn-rate-runtime-forecast.md` | Status: Active; Classification: Missing; Source: curriculum/01-nivel-1-fundamentals/02-token-budgeting.md. Evidence: docs/canonical/burn-rate-runtime-forecast.md:14-16. |
| Carry Debt Sunset Gate | `docs/canonical/carry-debt-sunset-gate.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-11-the-trap-spec-driven-development-is-setting/. Evidence: docs/canonical/carry-debt-sunset-gate.md:14-16. |
| Closed-Loop Agent Operating System | `docs/canonical/closed-loop-agent-operating-system.md` | Status: active; Classification: Partial Coverage, High integration value; Source: Stanford CS153 AI Native Company analysis. Evidence: docs/canonical/closed-loop-agent-operating-system.md:13-15. |
| Constraint-Anchored Evaluation | `docs/canonical/constraint-anchored-evaluation.md` | Status: Active; Classification: Partial Coverage — constraint-based checking exists implicitly in eval docs, not formalized as named pattern; Source: curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md. Evidence: docs/canonical/constraint-anchored-evaluation.md:14-16. |
| Deferred Ledger for Agentic Work | `docs/canonical/deferred-ledger-agentic-work.md` | Status: active; Classification: Missing, High integration value; Source: analysis/2026-06-11-the-trap-spec-driven-development-is-setting/. Evidence: docs/canonical/deferred-ledger-agentic-work.md:14-16. |
| Deterministic Tool Dispatch | `docs/canonical/deterministic-tool-dispatch.md` | Status: Active; Classification: Partial Coverage — mechanics exist, philosophical reframe missing (per `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md`); Source: Dex Horthy — "12-Factor Agents" (AI Engineer, 2025), adapted for long-running-agents. Evidence: docs/canonical/deterministic-tool-dispatch.md:13-15. |
| Domain-Embedded Workflow Automation Wedge | `docs/canonical/domain-embedded-workflow-automation-wedge.md` | Status: active; Classification: Partial Coverage, Medium integration value; Source: analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/. Evidence: docs/canonical/domain-embedded-workflow-automation-wedge.md:13-15. |
| Durable Fact Selective History | `docs/canonical/durable-fact-selective-history.md` | Status: Active; Classification: Partial Coverage; Source: [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]] and [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]. Evidence: docs/canonical/durable-fact-selective-history.md:13-15. |
| Epistemic Memory Graph | `docs/canonical/epistemic-memory-graph.md` | Status: active; Classification: Partial Coverage, Medium integration value; Source: analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/. Evidence: docs/canonical/epistemic-memory-graph.md:13-15. |
| Error Context Hygiene | `docs/canonical/error-context-hygiene.md` | Status: Active; Classification: Missing — no equivalent mechanism exists in the repo (per `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md`); Source: Dex Horthy — "12-Factor Agents" (AI Engineer, 2025), adapted for long-running-agents. Evidence: docs/canonical/error-context-hygiene.md:13-15. |
| Eval Tier Stratification | `docs/canonical/eval-tier-stratification.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-10-eval-maturity-phases/. Evidence: docs/canonical/eval-tier-stratification.md:13-15. |
| Eval-to-Production Correlation Tracking | `docs/canonical/eval-to-production-correlation-tracking.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-10-eval-maturity-phases/. Evidence: docs/canonical/eval-to-production-correlation-tracking.md:13-15. |
| Explicit Token Budget Ledger | `docs/canonical/explicit-token-budget-ledger.md` | Status: active; Classification: Partial Coverage; Source: [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]]. Evidence: docs/canonical/explicit-token-budget-ledger.md:13-15. |
| External State Persistence | `docs/canonical/external-state-persistence.md` | Status: Active; Classification: Partial Coverage — 6 canonical docs cover component pieces, no unified umbrella doc; Source: curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md. Evidence: docs/canonical/external-state-persistence.md:14-16. |
| Failure Pattern Classification Loop | `docs/canonical/failure-pattern-classification-loop.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/. Evidence: docs/canonical/failure-pattern-classification-loop.md:14-16. |
| Garbage Collection Day Meta-Loop | `docs/canonical/garbage-collection-day-meta-loop.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/. Evidence: docs/canonical/garbage-collection-day-meta-loop.md:14-16. |
| Generator-Evaluator | `docs/canonical/generator-evaluator.md` | Status: Active; Classification: Partial Coverage — 12+ eval infrastructure docs exist, no unified Generator-Evaluator architecture doc; Source: [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|Why Agents Lose Focus]]. Evidence: docs/canonical/generator-evaluator.md:14-16. |
| Grill-Me Alignment Interview | `docs/canonical/grill-me-alignment-interview.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/. Evidence: docs/canonical/grill-me-alignment-interview.md:13-15. |
| Head-Tail Context Truncation with Recoverable Middle | `docs/canonical/head-tail-context-truncation.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-09-how-we-solved-context-management-in-agents/. Evidence: docs/canonical/head-tail-context-truncation.md:13-15. |
| Human/AFK Task Routing Gate | `docs/canonical/human-afk-task-routing-gate.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/. Evidence: docs/canonical/human-afk-task-routing-gate.md:13-15. |
| Hybrid Context Stack | `docs/canonical/hybrid-context-stack.md` | Status: active; Classification: Partial Coverage; Source: [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-patterns|Token Budgeting Agentic Patterns]]. Evidence: docs/canonical/hybrid-context-stack.md:13-15. |
| Invariant-Compensation Split | `docs/canonical/invariant-compensation-split.md` | Status: Active; Classification: Missing; Source: docs/articles/harness-evolution-metodos-construcao.md. Evidence: docs/canonical/invariant-compensation-split.md:14-16. |
| Late-Failure Regression Suite | `docs/canonical/late-failure-regression-suite.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-09-how-we-solved-context-management-in-agents/. Evidence: docs/canonical/late-failure-regression-suite.md:13-15. |
| LLM as Fuzzy Compiler | `docs/canonical/llm-as-fuzzy-compiler.md` | Status: active; Classification: Missing; Source: analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/. Evidence: docs/canonical/llm-as-fuzzy-compiler.md:14-16. |
| Manual Brake Question Gate | `docs/canonical/manual-brake-question-gate.md` | Status: active; Classification: Missing, High integration value; Source: analysis/2026-06-11-the-trap-spec-driven-development-is-setting/. Evidence: docs/canonical/manual-brake-question-gate.md:14-16. |
| Measured Harness Evolution Lifecycle | `docs/canonical/measured-harness-evolution-lifecycle.md` | Status: Active; Classification: Partial Coverage; Source: docs/articles/harness-evolution-metodos-construcao.md. Evidence: docs/canonical/measured-harness-evolution-lifecycle.md:14-16. |
| Multi-Model Evaluation Council | `docs/canonical/multi-model-evaluation-council.md` | Status: active; Classification: Partial Coverage, Medium integration value; Source: analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/. Evidence: docs/canonical/multi-model-evaluation-council.md:13-15. |
| N+1 Long-Session Evals | `docs/canonical/n-plus-one-long-session-evals.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-09-how-we-solved-context-management-in-agents/. Evidence: docs/canonical/n-plus-one-long-session-evals.md:13-15. |
| Owned Agent Control Loop | `docs/canonical/owned-agent-control-loop.md` | Status: Active; Classification: Partial Coverage — general principle exists, specific 4-component decomposition missing (per `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md`); Source: Dex Horthy — "12-Factor Agents" (AI Engineer, 2025), adapted for long-running-agents. Evidence: docs/canonical/owned-agent-control-loop.md:13-15. |
| Owner-of-No Role Design | `docs/canonical/owner-of-no-role-design.md` | Status: active; Classification: Missing, Medium integration value; Source: analysis/2026-06-11-the-trap-spec-driven-development-is-setting/. Evidence: docs/canonical/owner-of-no-role-design.md:14-16. |
| Pain-Signal Eval Progression Gate | `docs/canonical/pain-signal-eval-progression-gate.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-10-eval-maturity-phases/. Evidence: docs/canonical/pain-signal-eval-progression-gate.md:13-15. |
| Persona-Based Documentation | `docs/canonical/persona-based-documentation.md` | Status: active; Classification: Missing; Source: analysis/2026-06-07-harness-engineering-how-to-build-software-when-humans-steer-agent/. Evidence: docs/canonical/persona-based-documentation.md:14-16. |
| Phase-Gated Token Health Monitor | `docs/canonical/phase-gated-token-health-monitor.md` | Status: active; Classification: Partial Coverage; Source: [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]] and [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]. Evidence: docs/canonical/phase-gated-token-health-monitor.md:14-16. |
| Plan-Execute-Verify | `docs/canonical/plan-execute-verify.md` | Status: Active; Classification: Partial Coverage — 7 canonical docs cover component pieces, no unified three-phase doc; Source: [[curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot|curriculum/01-nivel-1-fundamentals/01-why-agents-lose-plot.md]]. Evidence: docs/canonical/plan-execute-verify.md:14-16. |
| PR-Gated Eval Enforcement | `docs/canonical/pr-gated-eval-enforcement.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-10-eval-maturity-phases/. Evidence: docs/canonical/pr-gated-eval-enforcement.md:13-15. |
| Production Failure Regression Flywheel | `docs/canonical/production-failure-regression-flywheel.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-10-eval-maturity-phases/. Evidence: docs/canonical/production-failure-regression-flywheel.md:13-15. |
| Production-Grounded Eval Sampling | `docs/canonical/production-grounded-eval-sampling.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-10-eval-maturity-phases/. Evidence: docs/canonical/production-grounded-eval-sampling.md:13-15. |
| QA-to-Backlog Feedback Loop | `docs/canonical/qa-to-backlog-feedback-loop.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/. Evidence: docs/canonical/qa-to-backlog-feedback-loop.md:13-15. |
| Repeatable Agent Spot-Check Set | `docs/canonical/repeatable-agent-spot-check-set.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-10-eval-maturity-phases/. Evidence: docs/canonical/repeatable-agent-spot-check-set.md:13-15. |
| Resolver-Based Context Progressive Disclosure | `docs/canonical/resolver-based-context-progressive-disclosure.md` | Status: active; Classification: Partial Coverage, High integration value; Source: Stanford CS153 AI Native Company analysis. Evidence: docs/canonical/resolver-based-context-progressive-disclosure.md:13-15. |
| Semantic Topic Bucketing | `docs/canonical/semantic-topic-bucketing.md` | Status: Active; Classification: Missing; Source: curriculum/01-nivel-1-fundamentals/02-token-budgeting.md. Evidence: docs/canonical/semantic-topic-bucketing.md:14-16. |
| Serializable Pause/Resume State | `docs/canonical/serializable-pause-resume-state.md` | Status: Active; Classification: Partial Coverage — repo has richer state model, but different mechanism (per `docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md`); Source: Dex Horthy — "12-Factor Agents" (AI Engineer, 2025), adapted for long-running-agents. Evidence: docs/canonical/serializable-pause-resume-state.md:13-15. |
| Shared Design Concept Handoff | `docs/canonical/shared-design-concept-handoff.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/. Evidence: docs/canonical/shared-design-concept-handoff.md:13-15. |
| Skill-Resolver-Skillify Capability Pipeline | `docs/canonical/skill-resolver-skillify-capability-pipeline.md` | Status: active; Classification: Partial Coverage, High integration value; Source: Stanford CS153 AI Native Company analysis. Evidence: docs/canonical/skill-resolver-skillify-capability-pipeline.md:13-15. |
| Split-Brain Planning Review | `docs/canonical/split-brain-planning-review.md` | Status: active; Classification: Partial Coverage, Medium integration value; Source: analysis/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/. Evidence: docs/canonical/split-brain-planning-review.md:13-15. |
| Stable Harness Prompt During Context Reduction | `docs/canonical/stable-harness-prompt.md` | Status: active; Classification: Partial Coverage; Source: analysis/2026-06-09-how-we-solved-context-management-in-agents/. Evidence: docs/canonical/stable-harness-prompt.md:13-15. |
| Structured Generation and Constraint Validation Circuit | `docs/canonical/structured-generation-constraint-validation-circuit.md` | Status: Active; Classification: Partial Coverage; Source: docs/articles/harness-evolution-metodos-construcao.md. Evidence: docs/canonical/structured-generation-constraint-validation-circuit.md:14-16. |
| Summary Buffer Continuity | `docs/canonical/summary-buffer-continuity.md` | Status: active; Classification: Partial Coverage; Source: [[docs/analysis/2026-06-10-token-budgeting/2026-06-10-token-budgeting-analysis|Token Budgeting Analysis]] and [[curriculum/01-nivel-1-fundamentals/02-token-budgeting|Token Budgeting]]. Evidence: docs/canonical/summary-buffer-continuity.md:14-16. |
| Tested Degradation Ladder | `docs/canonical/tested-degradation-ladder.md` | Status: Active; Classification: Partial Coverage; Source: docs/articles/harness-evolution-metodos-construcao.md. Evidence: docs/canonical/tested-degradation-ladder.md:14-16. |
| Value-Gated Agent Control Loop | `docs/canonical/value-gated-agent-control-loop.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-11-the-trap-spec-driven-development-is-setting/. Evidence: docs/canonical/value-gated-agent-control-loop.md:14-16. |
| Versioned Durable Agent State | `docs/canonical/versioned-durable-agent-state.md` | Status: Active; Classification: Partial Coverage; Source: docs/articles/harness-evolution-metodos-construcao.md. Evidence: docs/canonical/versioned-durable-agent-state.md:14-16. |
| Vertical-Slice Issue Generation | `docs/canonical/vertical-slice-issue-generation.md` | Status: active; Classification: Partial Coverage, High integration value; Source: analysis/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/. Evidence: docs/canonical/vertical-slice-issue-generation.md:13-15. |

## 4. Terminology

| Term | Definition | Source |
|---|---|---|
| Agent | Entidade autônoma baseada em LLM que toma ações, usa ferramentas e executa tarefas em sequência. | `curriculum/GLOSSARY.md:17-24` |
| Agent Loop | Ciclo input -> pensa -> ação -> resultado -> repete. | `curriculum/GLOSSARY.md:28-35` |
| Context Amnesia | Perda de contexto anterior quando a janela de contexto é excedida. | `curriculum/GLOSSARY.md:37-45` |
| Context Anxiety | Comportamento apressado ou ansioso perto do limite de contexto. | `curriculum/GLOSSARY.md:77-85` |
| Context Rot | Perda gradual de coerência ao longo da janela de contexto. | `curriculum/GLOSSARY.md:88-94` |
| Context Window | Número total de tokens que um modelo pode processar de uma vez. | `curriculum/GLOSSARY.md:97-107` |
| Context Progressive Disclosure | Capacidades e instruções ficam em skills acionadas por resolver, não em prompt monolítico. | `curriculum/GLOSSARY.md:110-113; docs/canonical/resolver-based-context-progressive-disclosure.md` |
| Sprint Contract | Acordo prévio sobre o que pronto significa antes da execução. | `curriculum/GLOSSARY.md:117-126; curriculum/GLOSSARY.md:516-520` |
| Evaluator | Agente separado que avalia e critica o trabalho de um Generator contra rubrics. | `curriculum/GLOSSARY.md:131-143` |
| Evaluation Rubric | Critérios mensuráveis para avaliar qualidade subjetiva. | `curriculum/GLOSSARY.md:147-163` |
| Failure Pattern Classification Loop | Ritual semanal que classifica falhas recorrentes e as converte em guardrails automatizados. | `curriculum/GLOSSARY.md:169-179; docs/canonical/failure-pattern-classification-loop.md:20-64` |
| LLM as Fuzzy Compiler | LLM é compilador fuzzy, harness é pipeline de otimização e código gerado é artefato de build descartável. | `curriculum/GLOSSARY.md:182-197; docs/canonical/llm-as-fuzzy-compiler.md` |
| Garbage Collection Day | Meta-loop semanal que transforma feedback humano e falhas de produção em guardrails de harness. | `curriculum/GLOSSARY.md:202-212; docs/canonical/garbage-collection-day-meta-loop.md` |
| Generator | Agente responsável por construir ou criar output. | `curriculum/GLOSSARY.md:215-225` |
| Generator/Evaluator Pattern | Duas entidades separadas colaboram: uma gera, outra avalia. | `curriculum/GLOSSARY.md:228-248; docs/canonical/generator-evaluator.md:27-71` |
| Harness | Infraestrutura e padrões que envolvem agentes para torná-los confiáveis por períodos longos. | `curriculum/GLOSSARY.md:265-278` |
| Harness Evolution | Simplificar ou remover componentes de harness conforme modelos melhoram. | `curriculum/GLOSSARY.md:282-295; docs/canonical/measured-harness-evolution-lifecycle.md` |
| KODA | Agente conversacional de IA para venda de suplementos via WhatsApp e case study do programa. | `curriculum/GLOSSARY.md:300-311` |
| Memory / State | Informações retidas entre operações, em memória curta, longa ou arquivo. | `curriculum/GLOSSARY.md:328-339` |
| Multi-Agent System | Sistema com Planner, Generator, Evaluator ou outros agentes independentes coordenados. | `curriculum/GLOSSARY.md:355-368` |
| Planner | Agente especializado em quebrar problemas em etapas. | `curriculum/GLOSSARY.md:373-388` |
| Persona-Based Documentation | NFRs por persona especialista carregados por agentes implementadores e revisores. | `curriculum/GLOSSARY.md:400-416; docs/canonical/persona-based-documentation.md` |
| Skillify Pipeline | Hardening de workflow que funcionou uma vez em skill roteável, testada e resolvível. | `curriculum/GLOSSARY.md:449-452; docs/canonical/skill-resolver-skillify-capability-pipeline.md` |
| Self-Evaluation | Anti-padrão em que um agente avalia o próprio trabalho. | `curriculum/GLOSSARY.md:456-476` |
| Token Budget | Gerenciamento consciente de tokens disponíveis e consumidos. | `curriculum/GLOSSARY.md:552-563; docs/canonical/explicit-token-budget-ledger.md` |
| Trace | Log detalhado de inputs, reasoning, ações e outputs do agente. | `curriculum/GLOSSARY.md:566-581` |
| Verification Loop | Ciclo Generator -> Test -> Evaluator -> Feedback. | `curriculum/GLOSSARY.md:587-600` |
| Manual Brake Question Gate | Gate com três perguntas de valor antes de autorizar construção por agente. | `docs/canonical/manual-brake-question-gate.md:27-47` |
| Deferred Ledger | Ledger estratégico que classifica dívida agentic em skill debt, dependence debt e carry debt. | `docs/canonical/deferred-ledger-agentic-work.md:27-55` |
| Architecture-as-Agent-Affordance | Arquitetura avaliada como affordance para futuras sessões de agentes: deep modules, boundary tests e baixo acoplamento. | `docs/canonical/architecture-as-agent-affordance.md:28-42` |

## 5. Curriculum Structure

O currículo é o produto principal do repositório e progride de fundamentos para padrões práticos, arquitetura avançada e aplicação KODA (`docs/system-of-record.md:53-79`, `curriculum/EXECUTION_PLAN.md:36-59`).

### Levels

| Level | Focus | Duration | Main Artifacts | Evidence |
|---|---|---|---|---|
| Nível 1 - Fundamentos | Por que agentes falham: contexto, token budget e harness básico. | 3-4h no overview; semanas 1-2 expandidas para 13-16h/semana no plano de execução. | 3 lições, 2 exercícios hands-on, koda-applications/nivel-1-koda.md, soluções | `curriculum/README.md:186-199; curriculum/MASTER_PLAN.md:175-192; curriculum/EXECUTION_PLAN.md:65-154` |
| Nível 2 - Padrões Práticos | Generator/Evaluator, Sprint Contracts, Rubric Design e Trace Reading. | 6-8h no overview; semanas 3-4 no plano. | 4 lições, 4 exercícios incluindo Error Context Hygiene, koda-applications/nivel-2-koda.md, rubrics KODA | `curriculum/README.md:202-214; curriculum/INDEX.md:105-110; curriculum/EXECUTION_PLAN.md:158-193` |
| Nível 3 - Arquitetura Avançada | Multi-agent systems, state persistence, file-based coordination, compaction e harness evolution. | 8-10h; semanas 5-6 para membros avançados. | 5 lições, 5 exercícios avançados, 03-nivel-arquiteto/exercise-04-owner-of-no-role.md, koda-applications/nivel-3-koda.md | `curriculum/README.md:217-228; curriculum/INDEX.md:111-118; curriculum/EXECUTION_PLAN.md:196-235` |
| Nível 4 - KODA-Específico | Arquitetura KODA, customer journeys, feature patterns, rubricas KODA, harness improvements e exercícios reais. | Contínuo; semanas 7-12 no plano de execução. | 5 lições KODA, 4 real-world exercises, 3 case studies locais, soluções Python/JSON/Markdown | `curriculum/README.md:232-243; curriculum/INDEX.md:119-137; curriculum/EXECUTION_PLAN.md:238-306` |

### Core Concepts

Cada conceito promete explicação profunda, knowledge graphs, aplicação em KODA e checklist de implementação (`curriculum/README.md:247-266`).

| Concept | Source |
|---|---|
| Context Management | `curriculum/README.md:247-264; curriculum/MASTER_PLAN.md:348-357` |
| Planning vs. Execution | `curriculum/README.md:247-264; curriculum/MASTER_PLAN.md:348-357` |
| Generator/Evaluator | `curriculum/README.md:247-264; curriculum/MASTER_PLAN.md:348-357` |
| Sprint Contracts | `curriculum/README.md:247-264; curriculum/MASTER_PLAN.md:348-357` |
| State Persistence | `curriculum/README.md:247-264; curriculum/MASTER_PLAN.md:348-357` |
| Harness Evolution | `curriculum/README.md:247-264; curriculum/MASTER_PLAN.md:348-357` |
| Multi-Agent Coordination | `curriculum/README.md:247-264; curriculum/MASTER_PLAN.md:348-357` |
| Evaluation Rubrics | `curriculum/README.md:247-264; curriculum/MASTER_PLAN.md:348-357` |

### Supporting Surfaces

- `06-knowledge-graphs/` oferece ecosystem, feature dependencies, learning progression, problem-solution mapping e detailed concept graphs (`curriculum/INDEX.md:141-149`).
- `07-implementation-guides/` cobre setup, team progression, harness design checklist, rubrics, trace analysis e harness evolution playbook (`curriculum/MASTER_PLAN.md:374-383`).
- `08-tools-templates/` contém sprint contract, evaluation rubric, knowledge graph, ADR, progress tracker e learning rubric templates (`curriculum/INDEX.md:153-162`).
- `09-case-studies/` cobre Retro Game Maker, Browser DAW e três fluxos KODA: discovery, orders e fulfillment (`curriculum/INDEX.md:129-137`).
- A execução de 12 semanas define fundação, padrões, arquitetura e aplicação como fases sequenciais (`curriculum/EXECUTION_PLAN.md:36-59`).

## 6. Existing Gaps

| Gap | Where Documented |
|---|---|
| Nenhum ADR formal foi registrado; `docs/decisions/` contém apenas `.gitkeep`. | `docs/system-of-record.md:121-129; directory inspection: docs/decisions -> 0 markdown files` |
| ADRs candidatos ainda pendentes: stack do portal, content chunking, persistência de estado entre agentes e versionamento do currículo. | `docs/system-of-record.md:125-129` |
| `agent-lifecycle.md` pendente para claim -> worktree -> implement -> review -> merge -> cleanup. | `docs/system-of-record.md:51-52; docs/system-of-record.md:198-203; NOT_FOUND docs/canonical/agent-lifecycle.md` |
| `curriculum-model.md` pendente para taxonomia de níveis, tipos de artefato e critérios de qualidade. | `docs/system-of-record.md:78; docs/system-of-record.md:198-204; NOT_FOUND docs/canonical/curriculum-model.md` |
| `portal-architecture.md` pendente até a SPA proposta amadurecer ou ser implementada. | `docs/system-of-record.md:80-92; docs/system-of-record.md:198-204; NOT_FOUND docs/canonical/portal-architecture.md` |
| `crossroad-change-policy.md` e crossroad files citados pelo PR template ainda não existem. | `docs/system-of-record.md:113-120; .github/PULL_REQUEST_TEMPLATE.md:62-89; NOT_FOUND docs/guides/crossroad-change-policy.md; NOT_FOUND src/lib/safe-console.js; NOT_FOUND src/lib/logger.js` |
| `docs/evidence/` e `docs/archive/` fazem parte da hierarquia de precedência, mas estão vazios exceto `.gitkeep`. | `docs/system-of-record.md:16-21; directory inspection: docs/evidence -> 0 markdown files; directory inspection: docs/archive -> 0 markdown files` |
| O `docs/system-of-record.md` declara 55 padrões canônicos, mas a árvore atual tem 57 arquivos Markdown em `docs/canonical/`; o README ainda fala em 16 padrões. | `docs/system-of-record.md:131-197; README.md:90-105; directory inspection: docs/canonical -> 57 markdown files` |
| `obsidian-document-conventions.md` aparece na tabela ativa/esperada, mas o arquivo canônico não existe; AGENTS Rule 16 cobre a convenção por enquanto. | `docs/system-of-record.md:176; docs/system-of-record.md:205-206; AGENTS.md:120-238; NOT_FOUND docs/canonical/obsidian-document-conventions.md` |
| Agentes `.opencode` referenciam `agents/manifest.yaml`, `agents/roles/`, `agents/playbooks/`, `DESIGN.md` e docs KODA em subdiretórios canônicos inexistentes. | `.opencode/agents/hop-orchestrator-rezek.md:23-39; .opencode/agents/koda-hop-init-basic.md:28-35; .opencode/agents/hop-live-whatsapp-tester.md:22-31; NOT_FOUND agents/manifest.yaml; NOT_FOUND agents/roles/red-team.md; NOT_FOUND agents/playbooks/live-whatsapp-testing.md; NOT_FOUND DESIGN.md` |
| Alguns comandos de gates citados em `issue-review` não existem em `package.json`; os scripts reais atuais são `lint`, `lint:fix`, `test:unit` e `test:integration`. | `.opencode/skills/issue-review/SKILL.md:44-75; package.json:8-13` |
| O currículo mantém diretórios auxiliares ou placeholders com conteúdo incompleto: `curriculum/04-nivel-operador` vazio, `04-nivel-4-koda-specific/exercises` só `.gitkeep`, e `04-nivel-4-koda-specific/koda-applications` só `.gitkeep`. | `directory inspection: curriculum/04-nivel-operador -> found empty; directory inspection: curriculum/04-nivel-4-koda-specific/exercises -> .gitkeep only; directory inspection: curriculum/04-nivel-4-koda-specific/koda-applications -> .gitkeep only` |
| `FAQ.md` ainda é marcado como em construção em documentos de navegação, embora exista e tenha conteúdo extenso. | `curriculum/README.md:64-70; curriculum/README.md:469-473; curriculum/INDEX.md:348-354; curriculum/FAQ.md` |
| O pipeline IDSD está explicitamente em `phase-0: Repository Mental Model` e espera os dois artefatos gerados nesta tarefa. | `PROGRESS.md:16-18; PROGRESS.md:21-28` |

## Synthesis

O modelo mental útil é: `long-running-agents` é um **currículo aplicado**, uma **biblioteca canônica de padrões de harness** e um **sistema operacional de trabalho agentic**. O currículo ensina confiabilidade de agentes usando KODA; os canonicals registram padrões e lacunas; `.opencode` transforma esses padrões em workflows de execução, revisão, documentação, governança e análise. Qualquer análise externa posterior deve classificar novas ideias contra essas três camadas antes de propor integração.
