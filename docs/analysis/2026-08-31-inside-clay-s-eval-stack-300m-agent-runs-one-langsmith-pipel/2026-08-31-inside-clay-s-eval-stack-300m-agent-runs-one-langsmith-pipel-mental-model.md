---
title: "Mental Model: Inside Clay's Eval Stack — 300M Agent Runs, One LangSmith Pipel (Repository Full Rebuild)"
type: analysis
tags: ["harness-engineering", "agentes-orquestracao", "curriculo-conteudo", "governanca"]
date: 2026-08-31
aliases: ["mental model inside clay eval stack", "modelo mental full rebuild 2026-08-31", "phase 0 mental model clay eval stack"]
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[AGENTS|Agent Rules]]", "[[curriculum/GLOSSARY|Glossário]]", "[[.opencode/skills/analyze-and-improve/SKILL|analyze-and-improve]]"]
---

# Mental Model — long-running-agents (full rebuild, 2026-08-31)

Escopo: **somente o repositório**. A fonte externa (Inside Clay's Eval Stack) NÃO foi analisada neste passo — Phase 0 modela o repositório; a fonte é tratada pelo agente da Phase 1.

Modo: **full rebuild** (`incremental=false` explícito). O modelo foi reconstruído por leitura direta do repositório; o modelo anterior em `mapa-mental-repo/` serviu apenas de cross-check final, não de base.

Contagens verificadas em 2026-08-31 por listagem direta: **161** canonical docs em `docs/canonical/`, **35** skills em `.opencode/skills/`, **3** agentes em `.opencode/agents/`, **1** ADR aceito em `docs/decisions/`, **28** diretórios de análise em `docs/analysis/` (incl. `mhc-backend/`).

---

## 1. Project Goals

O que o repositório constrói e ensina:

1. **Base de conhecimento + currículo para agentes long-running confiáveis** — sistemas de IA que operam por horas ou dias sem perder contexto, planejamento ou julgamento de qualidade (`README.md:12`).
2. **Operacionalizar harness engineering** — a degradação de agentes longos é tratada como lacuna de engenharia (não de modelo); o harness é a infraestrutura de suporte ao redor do modelo (`README.md:16-18`).
3. **Atacar três falhas estruturais** de agentes em execução longa: perda de contexto, planejamento frágil, autoavaliação cega (`README.md:24-30`).
4. **Entregar o currículo como produto principal** — programa de 12 semanas, 4 níveis, 8 conceitos core, 35+ diagramas, ancorado no caso real KODA (agente de venda de suplementos via WhatsApp, conversas de 2+ horas) (`curriculum/README.md:13,34`; `docs/system-of-record.md:72-74`).
5. **Rodar pipeline automatizado de análise de conhecimento externo** — harness `analyze-and-improve` em 7 fases com evaluators e gates, convertendo fontes externas (talks, papers, transcripts) em canonical docs, skills e exercícios (`README.md:102,136`; `.opencode/skills/analyze-and-improve/SKILL.md:49-57`).
6. **Servir de template de sistema de agentes reutilizável** — `.opencode/` com Handoff Protocol (HoP), 35 skills e 3 agentes, adaptável a outros projetos (`README.md:103-104,140`).
7. **Governar documentação por precedência** — ADRs > canonical > evidence > analysis > archive > READMEs, via system of record (`docs/system-of-record.md:14-21`).
8. **Disciplina operacional de agentes** — uma tarefa por sessão, não assumir, mudança mínima, sucesso verificável antes de implementar, issues/branches traceáveis, gates reais de validação (`AGENTS.md:14-16,18-22,26-32,42-48,50-57,69-78`).
9. **Audiência declarada** — pessoas de negócio com skill em construção de agentes e sistemas agênticos, de iniciantes a operadores de produção (`README.md:34`).

---

## 2. Architecture — abstrações core e relações

### 2.1 Abstrações core

| Abstração | Papel | Evidência |
|---|---|---|
| **System of Record (SOR)** | Fonte da verdade; define precedência de 6 níveis, os domínios do projeto (agentes/orquestração, currículo/conteúdo, portal web, stack/tooling, governança, testes/QA) e cataloga padrões ativos, análises e ADRs | `docs/system-of-record.md:12-21,23-153` |
| **Biblioteca de padrões canônicos** | Camada autoritativa Level 2: 161 docs, cada um com problema/mecanismo/trade-offs, frontmatter `type: canonical`, `relates-to` obrigatório, wikilinks | `docs/system-of-record.md:171`; listagem `docs/canonical/` (161 .md); ex. `docs/canonical/generator-evaluator.md:1-17` |
| **Currículo** | Produto principal: 4 níveis + 8 conceitos core + knowledge graphs + guias + templates + case studies + referências | `curriculum/README.md:13`; `curriculum/MASTER_PLAN.md:50-190` |
| **Pipeline `analyze-and-improve`** | 7 fases (0-6) delegadas a sub-agentes (`ultrabrain`, `deep`, `quick`): mental model → extraction → patterns → classification → artifacts → integration → curriculum integration | `.opencode/skills/analyze-and-improve/SKILL.md:49-57`; `harness/GUIDE-analyze-and-improve.md` (tabela de fases) |
| **Harness de execução** | Loop `harness.sh` + `PROGRESS.md` (estado persistente), `test-results.json` default-FAIL (contrato por fase), `guardian` (valida evidência), `STEER.md` + `AGENT_STOP` (redirecionamento e kill switch humanos) | `harness/GUIDE-analyze-and-improve.md` §1-3 |
| **Sistema de agentes HoP (House of Pace)** | 3 agentes: `hop-orchestrator-rezek` (primary — governança, coordenação, fonte de verdade), `koda-hop-init-basic` (subagente de inicial guiada), `hop-live-whatsapp-tester` (subagente de teste live) | `.opencode/agents/` (3 arquivos); `docs/system-of-record.md:33-35` |
| **Biblioteca de skills** | 35 skills com SKILL.md: workflow de issues, orquestração, análise, documentação, error hygiene, gates, decomposição de intenção, métricas, anti-sycophancy | `.opencode/skills/` (35 dirs); `docs/system-of-record.md:36-67` |
| **Cache de modelos mentais** | `mapa-mental-repo/` versiona os modelos mentais do repo (max 5 ativos, `archive/` além disso, remoção >90 dias); alimenta modo incremental | `.opencode/skills/analyze-and-improve/SKILL.md:160-172` |
| **Convenções Obsidian + validação** | Rule 16: frontmatter obrigatório por tipo de doc, wikilinks `[[path|display]]` para todo cross-ref interno, tags derivadas dos domínios do SOR, `relates-to` hard error, slugs lowercase-hyphen, validador `scripts/validate-obsidian.ts` | `AGENTS.md:136-257` |
| **Camadas de apresentação** | 3 dashboards Obsidian (dataview), 3 portais HTML vanilla JS + 1 proposta SPA, 35+ diagramas Mermaid no currículo, canvas Obsidian | `README.md:105,110-121` |
| **Stack/tooling** | Node >= 20.18.0 ESM, ESLint 10 + plugin-n + unicorn + 2 regras customizadas (`no-catch-message`, `no-raw-console-in-scripts`), Makefile, `obsidian-eval` CLI (`@pavani/obsidian-eval`) para scan/query/graph cross-vault | `package.json`; `README.md:153-161`; `docs/system-of-record.md:114-131` |

### 2.2 Relações estruturais

- **SOR governa tudo**: qualquer conflito entre docs resolve-se pela precedência (`AGENTS.md:80-91` = Rule 8 espelha `docs/system-of-record.md:14-21`).
- **Pipeline → repositório**: outputs da Phase 0-4 vão para `docs/analysis/<date>-<slug>/`; artefatos concretos da Phase 4 vão aos diretórios definitivos (`docs/canonical/`, `.opencode/skills/`, `curriculum/`); a Phase 5 atualiza SOR e índices (`.opencode/skills/analyze-and-improve/SKILL.md:140-158`).
- **Modelo mental é insumo canônico das fases seguintes**: Phase 3 (classification) compara padrões extraídos da fonte externa contra este modelo; por isso as contagens precisam estar corretas.
- **Agentes → canonical**: cada agente declara fonte de verdade apontando para `docs/system-of-record.md` e canonical docs (`.opencode/agents/hop-orchestrator-rezek.md:23-29`).
- **Currículo ↔ canonical ↔ glossário**: lições referenciam padrões canônicos via wikilink; o glossário define termos com "Ver também" apontando a canonical docs e níveis (`curriculum/GLOSSARY.md`, passim).
- **ADRs > canonical**: a única ADR aceita (Skill-Canons Bridge) documenta decisões cross-cutting com opções/trade-offs/consequências e revisitas pendentes (`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:33-93`).
- **Análises alimentam padrões**: 28 diretórios de análise (12-Factor Agents, eval maturity, Matt Pocock, IDSD, memory selection, Kavak, Snowflake GTM, Qodo, macro fund, etc.) são a proveniência da maioria dos 161 canonical docs (`docs/system-of-record.md:344-452`).
- **Formato de sessão de análise**: pós-2026-06-14 usa `<date>-<source-slug>-artifacts.{md,yaml}` como manifest; antes disso `integration-roadmap.md` legacy (`docs/system-of-record.md:447-452`).
- **Disciplina de sessão**: Rule 0 (uma tarefa por sessão) e Rule 17 (coletar resultados de background tasks somente após ALL COMPLETE, em batch único) regem a operação do próprio pipeline (`AGENTS.md:14-16,259-272`).

---

## 3. Patterns — padrões existentes

### 3.1 Famílias de padrões canônicos (161 docs, `docs/canonical/`)

| Família | Exemplos representativos | Fonte/proveniência |
|---|---|---|
| **12-Factor Agents (12FA)** | `owned-agent-control-loop`, `deterministic-tool-dispatch`, `error-context-hygiene`, `serializable-pause-resume-state` | Talk Dex Horthy, AI Engineer 2025 (`docs/system-of-record.md:177-180`) |
| **Context management / memória** | `head-tail-context-truncation`, `addressable-memory-catalog`, `tiered-context-storage`, `neutral-selection-layer`, `selection-budgeted-retrieval`, `deliberate-forgetting`, `smallest-sufficient-context`, `relational-context-graph`, `context-health-monitoring`, `agent-degradation-loop-prevention`, `hybrid-context-stack` | Análises context-management e memory-selection-problem (`docs/system-of-record.md:187-197,269-276`) |
| **Token economics** | `explicit-token-budget-ledger`, `burn-rate-runtime-forecast`, `phase-gated-token-health-monitor`, `token-economics-gap-filling`, `budget-aware-session-handoff` | `docs/system-of-record.md:188-195` |
| **Evals (a maior família)** | `eval-tier-stratification`, `pain-signal-eval-progression-gate`, `production-failure-regression-flywheel`, `production-grounded-eval-sampling`, `living-eval-dataset`, `eval-driven-development-timeline`, `3-layer-evaluation-architecture`, `behavioral-eval-path-analysis`, `eval-dashboard-primary-detection-surface`, `business-outcome-first-eval-pipeline`, `eval-investment-parity`, `outcome-level-eval-hierarchy`, `evals-as-brakes`, `n-plus-one-long-session-evals`, `late-failure-regression-suite`, `pr-gated-eval-enforcement` | Múltiplas análises (eval maturity, Kavak, Sierra, Snowflake GTM) (`docs/system-of-record.md:197-207,282-315`) |
| **Arquitetura de execução** | `plan-execute-verify`, `generator-evaluator`, `closed-loop-agent-operating-system`, `application-owned-agent-control-plane`, `versioned-durable-agent-state`, `tested-degradation-ladder`, `measured-harness-evolution-lifecycle` (BUILD→STABILIZE→SIMPLIFY→REMOVE), `multi-agent-fault-tolerance`, `llm-as-fuzzy-compiler`, `invariant-compensation-split` | `docs/system-of-record.md:181-186,208,217,227-229` |
| **Intenção e especificação** | `intent-five-part-primitive`, `ice-craft-separation`, `three-part-intent-contract`, `scenario-destination-split`, `goal-atomicity-split`, `two-implementations-goal-test`, `constraint-budget-gate`, `constraint-failure-decision-rule`, `constraint-anchored-evaluation`, `compartmented-evaluation-architecture`, `human-owned-expectations-boundary`, `vertical-slice-issue-generation`, `grill-me-alignment-interview` | Análise IDSD/ICE (`docs/system-of-record.md:219-223,237,252-257`) |
| **Governança e intervenção humana** | `manual-brake-question-gate`, `deferred-ledger-agentic-work`, `carry-debt-sunset-gate`, `owner-of-no-role-design`, `presence-in-the-loop-metric`, `human-afk-task-routing-gate`, `value-gated-agent-control-loop`, `accidental-brake-replacement`, `shadow-review-pipeline`, `contextual-severity-calibration`, `review-contract-checklist`, `pre-commit-ai-review-gate`, `qa-to-backlog-feedback-loop`, `garbage-collection-day-meta-loop`, `failure-pattern-classification-loop` | `docs/system-of-record.md:226,229-251` |
| **Enterprise (Sierra)** | `multi-provider-model-routing`, `confidence-gated-continual-learning`, `regulated-data-boundary`, `auth-coupled-memory-architecture`, `task-routed-model-tiering`, `temporal-context-injection`, `three-tier-memory-persistence`, `always-on-monitoring-human-triage`, `model-switch-driven-eval-hardening`, `file-system-materialization`, `centralized-cross-framework-tracing`, `prompt-as-code-causal-change-management` | `docs/system-of-record.md:293-302` |
| **Kavak (2026-08-30)** | `model-agnostic-agent-vm-harness`, `alarm-clock-agent-lifecycle`, `carve-out-pilot-hard-target`, `mega-expert-consolidation`, `sidekick-pattern-physical-boundaries`, `agent-per-customer-outcome-ownership`, `goal-driven-agents-over-workflows`, `shared-fleet-learning`, `closed-loop-help-api`, `production-contact-training-loop` | `docs/system-of-record.md:303-315` |
| **Snowflake GTM (2026-08-30)** | `workflow-derived-golden-question-set`, `quality-over-coverage-trust-scoping`, `retention-gated-phased-rollout`, `centralized-data-plane-inherited-rbac`, `human-review-staged-workflow-automation`, `pull-based-infrastructure-on-pain`, `continuous-re-architecture-budget`, `gap-to-content-feedback-circuit`, `llm-classified-log-taxonomy`, `trial-retention-attribution-split`, `owner-led-activation-blitz`, `agent-value-maturity-ladder` | `docs/system-of-record.md:316-327` |
| **Qodo / code review (2026-08-31)** | `software-graph-review-substrate`, `semantic-rule-gated-auto-approve-block`, `dual-interface-context-engine`, `graph-addressed-context-placement`, `agent-to-agent-review-comment-protocol`, `rule-lifecycle-analytics`, `comment-decay-readiness-signal` | `docs/system-of-record.md:328-334` |
| **Domínio financeiro/institucional** | `asymmetric-binary-outcome-positioning`, `institutional-layer-amplification`, `credibility-cascade-regulated-assets`, `energy-value-chain-spread-analysis`, `inelastic-market-flow-dominance-model`, `spread-capture-analytical-primitive`, `capex-revenue-credit-mispricing`, `social-archetype-classification` | `docs/system-of-record.md:225,241-244,277-280` |
| **Publishing / misc** | `quarto-publishing-architecture`, `quarto-authoring-workflow`, `quarto-content-structure`, `skill-resolver-skillify-capability-pipeline`, `resolver-based-context-progressive-disclosure`, `epistemic-memory-graph`, `cross-context-knowledge-siloing`, `operator-channel-authority`, `structural-guarantee-over-compliance`, `trace-instrumentation`, `skill-testing-conventions`, `obsidian-document-conventions` | `docs/system-of-record.md:209-215,258-260,338+` |

### 3.2 Padrões de processo / operacionais (não-canonical)

- **Ciclo de vida de issue**: `issue-start` (claim → worktree → execution brief) → `issue-review` (validação → draft PR → second-agent review) → `issue-finish` (merge → cleanup); ciclo completo em `issue-workflow`; decomposição em `refine-issue` (`.opencode/skills/`; `docs/system-of-record.md:36-40`).
- **Regras Karpathy** (skill `karpathy-guidelines`): Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution — referenciadas pelas Rules 1-4 do AGENTS.md (`AGENTS.md:24,32,40,48`).
- **Bridge skill-canons**: skills do ecossistema conectadas a padrões canônicos do vault; ADR aceito define inline injection, promotion rule D8, baseline por snapshot, budget gate 4 fases, cópia local até >5 skills (`docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:36-43`).
- **Anti-sycophancy Wave 1**: skill `devils-advocate` (agente momus) para dissent estruturado (`docs/system-of-record.md:63`).
- **No-fabricated-premises em delegações**: delegação nunca afirma convenções do repo como fato; sub-agente detecta convenção lendo 2-3 artefatos irmãos e reporta (`.opencode/skills/analyze-and-improve/SKILL.md:130-138`).
- **Commit style**: `type(scope): short description`; `[FUP-N]` para follow-ups; branch `issue/<N>-<slug>` a partir de `main`; label `agent:working` (`AGENTS.md:50-67`).
- **Gates**: `npm run lint`, `npm run test:unit`, `npx tsx scripts/validate-obsidian.ts` para docs (`AGENTS.md:69-78,214`).

---

## 4. Abstrações e terminologia chave

Termos centrais (definições completas em `curriculum/GLOSSARY.md`; seleção dos mais load-bearing):

**Nível 1 — Fundamentos**: **Agent** (:17-24), **Agent Loop** (:41-47), **Context Window** (:158-168), **Amnesia/Context Amnesia** (:50-57), **Context Rot** (:149-155), **Context Anxiety** (:138-145), **Token** (:770-780), **Token Budget** (:783-794), **Harness** (:370-383 — "se agente é piloto, harness é avião + torre + combustível"), **METR** (:474-481), **Weights** (:886-893).

**Nível 2 — Padrões práticos**: **Generator** (:320-330), **Evaluator** (:220-232), **Generator/Evaluator Pattern** (:333-352), **Sycophancy** (:754-764), **Sprint** (:734-744 — 30-120 min de agente), **Sprint Contract** (:191-199), **Evaluation Rubric** (:236-253), **Granularity** (:355-364), **Trace** (:830-845), **Verification Loop** (:867-880), **Planner** (:547-561), **MCP** (:499-508), **Ralph Loop** (:625-641 — padrão anterior, substituído por generator/evaluator), **ICE Craft Separation** (:419-432 — Intent/Context/Expectations com donos explícitos), **Intent as Five-Part Primitive** (:436-451 — description, constraints, failure scenarios, success scenarios, connections), **Human-Owned Expectations Boundary** (:403-413), **Goal Atomicity Split** (:304-316 — regra do "e"), **Two-Implementations Goal Test** (:849-861), **Token Economics of Gap-Filling** (:797-810).

**Nível 3 — Arquitetura avançada**: **Multi-Agent System** (:512-524 — Planner/Generator/Evaluator), **Memory/State** (:485-495), **Compaction** (:81-87), **Harness Evolution** (:387-399), **ADR** (:61-68), **Closed-Loop Company** (:74-78), **Skillify Pipeline** (:654-658), **Context Progressive Disclosure** (:184-188), **LLM as Fuzzy Compiler** (:271-285 — constraints de domínio são o source durável; código é build descartável), **Persona-Based Documentation** (:574-588), **Failure Pattern Classification Loop** (:258-267), **Garbage Collection Day** (:291-300), **Presence-in-the-Loop Metric** (:592-606), **Constraint Budget Gate** (:106-118 — regra 5-7), **Constraint-Failure Decision Rule** (:122-134), **Compartmented Evaluation Architecture** (:90-102), **Relational Context Graph** (:612-621 — edges tipados: dependency, provenance, supersession, causation), **Deliberate Forgetting** (:205-214), **Smallest Sufficient Context** (:697-706), **Tiered Context Storage** (:814-826 — hot/warm/cold), **Neutral Selection Layer** (:530-541), **Selection-Budgeted Retrieval** (:661-670), **Context Health Monitoring** (:171-180), **Agent Degradation Loop Prevention** (:28-37 — 4 links do loop de degradação).

**Nível 4 / transversal**: **KODA** (:457-468 — agente de venda de suplementos via WhatsApp; case study e aplicação prática de todos os padrões).

Termos estruturais do repositório (fora do glossário): **System of Record**, **canonical doc**, **handoff protocol (HoP)**, **skill**, **mental model cache**, **artifacts manifest**, ** wikilinks/relates-to** (convenções Obsidian).

---

## 5. Curriculum Structure

**Programa**: 12 semanas, 4 níveis de profundidade, 8 conceitos core, 35+ diagramas Mermaid, dezenas de exercícios (`curriculum/README.md:13`; `README.md:54`).

| Nível | Diretório | Foco | Carga | Tópicos |
|---|---|---|---|---|
| 1 — Fundamentos | `curriculum/01-nivel-1-fundamentals/` | Por que agentes falham | 3-4h | why-agents-lose-plot, token-budgeting, basic-harness-patterns + exercises + koda-applications (`curriculum/MASTER_PLAN.md:196-213`) |
| 2 — Padrões Práticos | `curriculum/02-nivel-2-practical-patterns/` | Padrões de confiabilidade | 6-8h | generator/evaluator, sprint contracts, rubric design, trace reading + exercises (incl. two-implementations, goal-atomicity, intent-five-part) (`MASTER_PLAN.md:217-236`) |
| 3 — Arquitetura Avançada | `curriculum/03-nivel-3-advanced-architecture/` | Sistemas multi-agente | 8-10h | multi-agent systems, state persistence, file-based coordination, server-side compaction, harness evolution + 16 exercícios (`MASTER_PLAN.md:240-259`) |
| 4 — Aplicação KODA | `curriculum/04-nivel-4-koda-specific/` | Aplicação real | Contínuo | KODA architecture, customer journeys, feature design patterns, rubrics KODA, harness improvements + real-world exercises + case studies (`MASTER_PLAN.md:263-282`) |

**Conceitos core** (`curriculum/05-core-concepts/`, 8 arquivos): 01-context-management, 02-planning-execution-separation, 03-generator-evaluator-pattern, 04-sprint-contracts, 05-state-persistence, 06-harness-evolution, 07-multi-agent-coordination, 08-evaluation-rubrics + `exercises/` avançados (tiered-context-storage, neutral-selection-layer, selection-budgeted-retrieval).

**Diretórios satélite de exercícios** (fora da numeração principal): `03-nivel-arquiteto/exercises/` (owner-of-no-role), `03-nivel-3-operational/exercises/` (shadow-review-pipeline, contextual-severity-calibration), `04-nivel-3-engenharia-avancada/exercises/` (behavioral-eval-path-analysis) — `docs/system-of-record.md:90`; `curriculum/MASTER_PLAN.md:109-121`.

**Camadas de suporte**: `06-knowledge-graphs/` (35+ diagramas: concept-ecosystem, koda-feature-dependencies, learning-progression, problem-solution-mapping + detailed-graphs), `07-implementation-guides/` (setup, team progression, harness design checklist, eval template, trace analysis, harness evolution playbook), `08-tools-templates/` (sprint contract, rubric, ADR, progress tracker, knowledge graph templates), `09-case-studies/` (retro-game-maker, browser-daw-app, 3× KODA), `10-references/` (anthropic presentation, model capability timeline, additional resources) (`curriculum/MASTER_PLAN.md:153-189`).

**Documentos mestres**: `MASTER_PLAN.md` (mapa completo + roadmap semanal + progress tracking), `QUICK_START.md` (45 min), `INDEX.md` (navegação por perfil), `EXECUTION_PLAN.md` (cronograma 12 semanas), `GLOSSARY.md` (~50 termos), `FAQ.md`, `DELIVERY-COMPLETE.md`, `tag-suggestions.yaml`.

**Progresão pedagógica**: fundamentos conceituais → padrões aplicáveis → arquitetura de sistema → aplicação contínua no caso real KODA; cada nível tem critérios de conclusão checkáveis (`MASTER_PLAN.md:208-282`) e o roadmap semanal mapeia semanas 1-12 com deliverables (`MASTER_PLAN.md:286-330`).

**Materiais-fonte**: `rawfiles/` (material que gerou o currículo) e `prompts/` (prompts de geração) — `docs/system-of-record.md:96-97`.

---

## 6. Existing Gaps — documentado como pendente ou ausente

| # | Gap | Onde documentado |
|---|---|---|
| 1 | Canonical `agent-lifecycle.md` (ciclo claim → worktree → implement → review → merge → cleanup) pendente | `docs/system-of-record.md:70` |
| 2 | Canonical `curriculum-model.md` (taxonomia de níveis, tipos de artefato, critérios de qualidade) pendente | `docs/system-of-record.md:99` |
| 3 | Canonical `portal-architecture.md` pendente — só quando a SPA proposta for implementada | `docs/system-of-record.md:112` |
| 4 | `docs/guides/crossroad-change-policy.md` e crossroad files (`src/lib/safe-console.js`, `src/lib/logger.js`, etc.) referenciados pelo PR template mas inexistentes — criar "quando houver código fonte" | `docs/system-of-record.md:144` |
| 5 | ADRs candidatos ainda não escritos: stack do portal (vanilla vs framework), modelo de content chunking, estratégia de persistência de estado entre agentes, política de versionamento do currículo | `docs/system-of-record.md:163-167` |
| 6 | `docs/canonical/operations/koda-init-basic-flow.md` e `docs/canonical/operations/live-whatsapp-testing-system.md` (e `docs/canonical/product/prd.md`, `architecture/architecture.md`, `voice-and-narrative.md`, `agents/roles/`, `agents/playbooks/`) referenciados como fonte de verdade pelos agentes KODA mas **inexistentes** no repositório | `.opencode/agents/koda-hop-init-basic.md:30-34`; `.opencode/agents/hop-live-whatsapp-tester.md:24-30` |
| 7 | `index.md` desatualizado: afirma que `docs/decisions/` está vazio ("no accepted ADRs exist") quando o SOR registra 1 ADR aceito (2026-06-24) — drift de documentação (index last_updated 2026-06-10) | `index.md:77` vs `docs/system-of-record.md:161` |
| 8 | README subconta o repositório: "85+ padrões canônicos" vs 161 reais; "28 skills" vs 35 reais; "3 skills: ..." listadas no SOR vs 35 dirs — contagens desatualizadas | `README.md:67,104` vs listagens 2026-08-31 |
| 9 | Classificação interna do `generator-evaluator.md` registra cobertura parcial: "12+ eval infrastructure docs exist, no unified Generator-Evaluator architecture doc" | `docs/canonical/generator-evaluator.md:16` |
| 10 | Ações abertas da ADR do Skill-Canons Bridge: atualizar `system-design` para budget gate de 4 fases; extrair shared module quando >5 skills tiverem bridge; capturar baselines via runs manuais quando houver budget | `docs/decisions/2026-06-24-skill-canons-bridge-implementation.md:91-93` |
| 11 | `package.json` scripts referenciam `src/` e `tests/` que não existem como árvore de código (repositório é majoritariamente conhecimento/documentação; `tests/unit` existe apenas para scripts utilitários) — gates de lint/test operam sobre superfície parcial | `package.json` (scripts lint/test:unit); ausência de `src/` confirmada por listagem |
| 12 | `FAQ.md` marcado "(em construção)" no README do currículo | `curriculum/README.md:69` |
| 13 | Skill `devils-advocate` referenciada no SOR (com path `.opencode/skills/devils-advocate/SKILL.md`) mas **ausente** de `.opencode/skills/` — referência quebrada | `docs/system-of-record.md:63` vs listagem `.opencode/skills/` (35 dirs, sem devils-advocate) |
| 14 | Nomenclatura de níveis inconsistente no currículo: coexistem `03-nivel-3-advanced-architecture`, `03-nivel-arquiteto`, `03-nivel-3-operational`, `04-nivel-3-engenharia-avancada`, `04-nivel-4-koda-specific` — diretórios satélite fora da numeração canonical dos 4 níveis | estrutura de `curriculum/` (listagem); `curriculum/MASTER_PLAN.md:109-121` |
| 15 | 16 violações pré-existentes do `validate-obsidian.ts` (relates-to/aliases ausentes) nos pacotes de análise 2026-06-25 e 2026-06-26 — descobertas ao validar este run | execução de `npx tsx scripts/validate-obsidian.ts` em 2026-08-31 (16 errors) |
| 16 | Diretório top-level `curso-reimplementar-runtime/` (PR #144) não mapeado no README nem no Knowledge Index | listagem da raiz do repo; ausência em `README.md:48-129` e `index.md` |

---

## Verificação e método

- Leitura direta: `AGENTS.md`, `README.md`, `docs/system-of-record.md` (460 linhas completas), `docs/decisions/2026-06-24-skill-canons-bridge-implementation.md`, os 3 agentes em `.opencode/agents/`, `curriculum/GLOSSARY.md` (1002 linhas), `curriculum/MASTER_PLAN.md` (estrutura + níveis), `curriculum/README.md`, `docs/canonical/generator-evaluator.md` (amostra de formato), `.opencode/skills/analyze-and-improve/SKILL.md` (Phases e mapa mental), `harness/GUIDE-analyze-and-improve.md`, `index.md`, `package.json`.
- Contagens por listagem direta de diretórios em 2026-08-31 (canonical=161, skills=35, agents=3, analysis dirs=28, ADRs=1).
- Cross-check final contra `mapa-mental-repo/2026-08-31-the-last-human-code-review-...-mental-model.yaml` (após a escrita; ver nota abaixo).

*Full rebuild Phase 0 — pipeline `analyze-and-improve`, fonte: Inside Clay's Eval Stack.*
