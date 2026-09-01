---
title: "Mental Model — ecossistema-pavan"
type: analysis
tags: [mental-model, arquitetura, agentes-orquestracao, curriculo-conteudo, harness-engineering, governanca]
date: 2026-06-26
aliases: ["ecossistema-pavan mental model", "modelo mental"]
relates-to:
  - "[[docs/system-of-record|System of Record]]"
  - "[[curriculum/GLOSSARY|Glossário do Currículo]]"
  - "[[docs/ecosystem-glossary|Glossário do Ecossistema]]"
  - "[[README|Repository README]]"
sources:
  - "/mnt/c/Users/pavan/AGENTS.md"
  - "/mnt/c/Users/pavan/long-running-agents/README.md"
  - "/mnt/c/Users/pavan/long-running-agents/docs/system-of-record.md"
  - "/mnt/c/Users/pavan/long-running-agents/curriculum/GLOSSARY.md"
  - "/mnt/c/Users/pavan/long-running-agents/docs/ecosystem-glossary.md"
  - "/mnt/c/Users/pavan/obsidian-eval/README.md"
  - "/mnt/c/Users/pavan/.omo/plans/"
  - "/mnt/c/Users/pavan/plans/adr/"
---

# Mental Model: ecossistema-pavan

Modelo mental estruturado do repositório `ecossistema-pavan` (`/mnt/c/Users/pavan`), construído a partir da leitura completa das fontes canônicas. Cobre a arquitetura, padrões, terminologia, currículo e gaps do ecossistema.

---

## 1. Project Goals

O ecossistema-pavan é um **workspace multi-repositório** que documenta, ensina e operacionaliza padrões de **harness engineering** para agentes de IA long-running. Não é um produto de software convencional — é um **sistema de conhecimento + runtime operacional**.

### 1.1 Meta principal

Resolver o problema de degradação de agentes de IA em execuções longas (horas/dias) através de engenharia de software sistemática aplicada ao runtime do agente, não através de prompts melhores ou modelos maiores.

> *"Não é uma limitação de modelo — é uma lacuna de engenharia."* (`long-running-agents/README.md:13-14`)

### 1.2 Sub-objetivos

| Objetivo | Onde vive | Status |
|----------|-----------|--------|
| Currículo completo de 12 semanas (4 níveis, 8 conceitos core) | `long-running-agents/curriculum/` | Ativo, expansão contínua |
| 85+ padrões canônicos de arquitetura agentica | `long-running-agents/docs/canonical/` | Ativo, evolução contínua |
| Runtime programável para vaults Obsidian (`obsidian-eval`) | `obsidian-eval/` | v0.2.x, npm público |
| Pipeline de ingestão de conhecimento externo (analyze-and-improve) | `harness/` + skills | Ativo, 7 fases |
| Sistema de agentes com Handoff Protocol | `.opencode/` + `~/.config/opencode/skills/` | Ativo, 28 skills |
| Stack de telemetria e observabilidade | `~/scripts/telemetry/` | Ativo, 80 testes |
| Learning flywheel cross-session | flywheel daemon + consumer | Ativo, fechamento de loop |
| Livro agentico (Quarto) | `livro-agentico/` | Ativo, 10 capítulos |
| Runtime privado para continuidade cross-session | `~/sisyphus-runtime/` | Ativo, vault privado |

### 1.3 Problemas estruturais atacados

1. **Perda de contexto** — a janela de tokens enche e o agente esquece. Solução: token budgeting, head-tail truncation, addressable memory catalog, tiered context storage.
2. **Planejamento frágil** — sem decomposição, o agente tenta tudo de uma vez. Solução: sprint contracts, plan-execute-verify, vertical-slice issue generation.
3. **Autoavaliação cega** — o mesmo modelo gera e avalia, aprovando qualidade ruim. Solução: generator/evaluator, compartmented evaluation, constraint-anchored evaluation, multi-model evaluation council.

---

## 2. Architecture

### 2.1 Visão geral dos componentes

```
ecossistema-pavan/
├── long-running-agents/     ← Produto principal: conhecimento canonizado + currículo
│   ├── docs/canonical/      ← 85+ padrões autoritativos
│   ├── docs/decisions/      ← ADRs aceitos (1 interno + 13 em plans/adr/)
│   ├── docs/analysis/       ← Diagnósticos, comparações, extrações de padrões
│   ├── curriculum/          ← Programa de 12 semanas, 4 níveis
│   ├── harness/             ← Sistema de orquestração do pipeline analyze-and-improve
│   ├── .opencode/           ← Definições de agentes (3 agentes) + skills (28)
│   └── web/                 ← Portais HTML estáticos (Mermaid, vanilla JS)
│
├── obsidian-eval/           ← Runtime CLI/biblioteca npm (@pavani/obsidian-eval)
│   ├── src/                 ← scan, query, graph, write, epistemic, scheduler, manifest
│   └── test/                ← 398 testes (vitest)
│
├── mhc-knowledge-base/      ← Domínio KODA (e-commerce conversacional)
├── raw-knowledge/           ← Fontes ingeridas (papers, talks, transcripts)
├── agent-analysis/          ← Diagnóstico arquitetural do KODA
├── livro-agentico/          ← Livro em Quarto (10 capítulos)
│
├── ~/sisyphus-runtime/      ← Vault privado: handoffs, fatos duráveis, estado
├── ~/scripts/telemetry/     ← Stack de telemetria: tracer, collector, dashboard
├── ~/scripts/sisyphus/      ← CLI de suporte: cache exploration, validate-or-retry, handoff-path
├── ~/.config/opencode/skills/ ← 25 skills testadas (237 testes, 26/26 suites)
│
├── .omo/plans/              ← 177 planos (executados, ativos, bloqueados)
├── plans/adr/               ← 13 ADRs aceitos
└── AGENTS.md                ← Regras operacionais do workspace
```

### 2.2 Abstrações centrais

| Abstração | Definição | Localização |
|-----------|-----------|-------------|
| **Vault** | Repositório de conhecimento em Markdown gerenciado pelo `obsidian-eval`. Cada vault declara `exports`/`imports` no `MANIFEST.md`. | `obsidian-eval/src/types.ts` — interface `Vault` |
| **Canonical Doc** | Documento autoritativo (`type: canonical`) que define um padrão reutilizável de design de agente. | `long-running-agents/docs/canonical/` |
| **Skill** | Conjunto de instruções e workflows para domínio específico, carregado via `skill(name="...")`. | `~/.config/opencode/skills/` |
| **Handoff** | Snapshot do estado de sessão OpenCode, persistido como nota no vault de runtime (`type: session-handoff`). | `~/sisyphus-runtime/sessions/` |
| **Durable Fact** | Conhecimento persistido com `valid_from`/`valid_to`, `confidence`, `provenance`. | `~/sisyphus-runtime/facts/` |
| **Execution Graph** | DAG de tarefas que modela orquestração de sessões com nós, status, estimativas de tokens. | `obsidian-eval/src/execution-graph.ts` |
| **Trace Span** | Registro instrumentado de chamada `task()` (categoria, duração, tokens, success/failure). | `~/scripts/telemetry/trace-cli.ts` |
| **Knowledge Pipeline** | Fluxo completo: handoff → compressWorkingMemory → relevanceScore → promotePatterns → buildProvenance → checkDrift → appendFact. | `obsidian-eval/src/memory-layers.ts` |
| **Learning Flywheel** | Sistema que detecta padrões de falha, classifica severidade e dispara correção automática (QI loop). | `~/scripts/telemetry/flywheel-daemon.service` |
| **Token Budget** | Orçamento de tokens da sessão com 4 fases: green (>60%), yellow (>40%), orange (>20%), red (≤20%). | `~/.config/opencode/skills/budget-monitor/` |
| **Ground Truth** | Assertions imutáveis definidas por humanos que bloqueiam contaminação do pipeline de conhecimento. | `~/sisyphus-runtime/facts/_global/ground-truth.md` |
| **ADR** | Architecture Decision Record — decisão formalizada com contexto, opções, trade-offs e consequências. | `plans/adr/` (13 aceitos) |
| **System of Record** | Documento que define precedência (6 níveis) e fontes canônicas de cada domínio. | `long-running-agents/docs/system-of-record.md` |

### 2.3 Relacionamentos entre abstrações

```
Handoff (sessão N)
  │
  ├──→ canonical-context skill (sessão N+1): injeta contexto de continuidade
  │
  ├──→ Knowledge Pipeline: compressWorkingMemory → promotePatterns
  │       │
  │       ├──→ Durable Fact (promovido após ≥3 handoffs similares)
  │       │       │
  │       │       └──→ checkDrift (Ground Truth validation)
  │       │              │
  │       │              ├── PASS → appendFact no vault de runtime
  │       │              └── FAIL → bloqueado (DriftAlert)
  │       │
  │       └──→ Reflection Loop (diário, 09:00 BRT): Gather → Analyze → Synthesize → Apply
  │
  ├──→ Telemetry DB: session data, task_calls, trace_spans
  │       │
  │       ├──→ Daily Summary
  │       ├──→ SLO Checker
  │       └──→ Flywheel Daemon (60s loop)
  │              │
  │              └──→ Consumer: anomaly_score ≥ 80 → auto-trigger QI loop
  │
  └──→ Epistemic Graph: entidades + relacionamentos extraídos do vault
          │
          └──→ Queries: affectedBy, mostModifiedFiles, staleFacts
```

### 2.4 Stack tecnológico

| Camada | Tecnologia | Versão/Config |
|--------|-----------|---------------|
| Runtime | Node.js | ≥ 20.18.0, ESM |
| Linguagem | TypeScript | tsc + vitest |
| Lint | ESLint 10 | + plugin-n + unicorn + 2 custom rules |
| Agentes | OpenCode | Handoff Protocol (`.opencode/`) |
| Vaults | Obsidian | Wikilinks, dataview, YAML frontmatter |
| Runtime de vaults | `@pavani/obsidian-eval` | v0.2.x, npm público |
| Telemetria | SQLite | `~/sisyphus-runtime/telemetry.db` |
| Tokenização | `@goliapkg/tiktoken-wasm` | encoding `deepseek_v3` |
| Automação | systemd | 5 timers (daily, retention, SLO, collect, flywheel) |
| Publicação | Quarto | livro-agentico (HTML + PDF) |
| Orquestração | bash + Python + TypeScript | scripts em `~/scripts/` |

---

## 3. Patterns

Os padrões do ecossistema são formalizados em `long-running-agents/docs/canonical/` (85+ documentos). Abaixo, as categorias principais com exemplos representativos.

### 3.1 Context Engineering (Gerenciamento de Contexto)

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `explicit-token-budget-ledger` | Cálculo de custo de prompt, reservas e saldo de tokens por passo | Implementado (budget-monitor skill) |
| `burn-rate-runtime-forecast` | Projeção em tempo real do consumo e autonomia restante | Implementado |
| `phase-gated-token-health-monitor` | Conversão de orçamento + burn rate em fases operacionais (green/yellow/orange/red) | Implementado |
| `head-tail-context-truncation` | Preservação de cabeça (objetivo) e cauda (estado atual); middle recuperável via handles | Canonical doc |
| `addressable-memory-catalog` | Catálogo de memória omitida com id, location, preview, scope, fetch | Canonical doc |
| `durable-fact-selective-history` | Política seletiva que combina fatos duráveis com histórico recente | Canonical doc |
| `summary-buffer-continuity` | Buffer de resumo contínuo com atualização incremental e frescor explícito | Canonical doc |
| `semantic-topic-bucketing` | Agrupamento semântico por tópico para reter e resumir contexto por tema | Canonical doc |
| `hybrid-context-stack` | Pilha híbrida: prompt + memória + estado durável + omissões recuperáveis | Canonical doc |
| `tiered-context-storage` | 3 tiers (hot/warm/cold) com promoção/demissão dinâmica por relevância | Canonical doc + exercícios N3 |
| `neutral-selection-layer` | Camada de seleção model-agnostic e vendor-independent | Canonical doc + exercícios N3 |
| `selection-budgeted-retrieval` | Retrieval com budget awareness: ranking por valor/custo | Canonical doc + exercícios N3 |
| `deliberate-forgetting` | Esquecimento intencional como operação de primeira classe | Canonical doc |
| `smallest-sufficient-context` | Contexto mínimo suficiente via travessia relacional | Canonical doc |
| `relational-context-graph` | Grafo com edges tipados (dependency, provenance, supersession, causation) | Canonical doc |
| `context-health-monitoring` | Monitoramento além de tokens: effective size, near-miss rate, contradiction rate | Canonical doc |
| `agent-degradation-loop-prevention` | Prevenção do loop de degradação de 4 elos | Canonical doc |
| `cross-context-knowledge-siloing` | Conhecimento criado em um contexto que se torna invisível em outro | Canonical doc |

### 3.2 Harness Design & Evolution

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `invariant-compensation-split` | Classificação: invariantes de domínio vs compensações temporárias de modelo | Canonical doc |
| `application-owned-agent-control-plane` | Contrato unificado de control plane: prompt versionado, schema, dispatch, estado | Canonical doc |
| `structured-generation-constraint-validation-circuit` | Geração estruturada + validação de constraints com repair, rejeição e audit | Canonical doc |
| `versioned-durable-agent-state` | Estado durável versionado com schema, migração, writeback, reload | Canonical doc |
| `tested-degradation-ladder` | Escada de degradação testada: classificação → retry → fallback → escalação | Canonical doc |
| `measured-harness-evolution-lifecycle` | Ciclo BUILD → STABILIZE → SIMPLIFY → REMOVE com ROI e archive | Canonical doc |
| `closed-loop-agent-operating-system` | Sistema operacional de loop fechado para agentes long-running | Canonical doc |
| `skill-resolver-skillify-capability-pipeline` | Pipeline: workflow → skill resolvível e testado | Canonical doc |
| `domain-embedded-workflow-automation-wedge` | Wedge de automação guiado por evidência | Canonical doc |
| `llm-as-fuzzy-compiler` | LLM como compilador fuzzy: código como artefato de build descartável | Canonical doc |
| `garbage-collection-day-meta-loop` | Meta-loop semanal de limpeza de harness | Canonical doc |
| `failure-pattern-classification-loop` | Classificação de padrões de falha → guardrails automatizados | Canonical doc |
| `plan-execute-verify` | Separação em 3 fases com checkpoints e contratos | Canonical doc |
| `external-state-persistence` | Persistência de estado externo como estratégia unificada | Canonical doc |
| `budget-aware-session-handoff` | Handoff consciente do orçamento com reset do contexto ativo | Implementado (session-handoff skill) |

### 3.3 Evaluation (Avaliação)

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `eval-tier-stratification` | Estratificação fast/medium/deep para suites de eval | Canonical doc |
| `pain-signal-eval-progression-gate` | Progressão de evals guiada por sinais de dor reais | Canonical doc |
| `production-grounded-eval-sampling` | Amostragem ancorada em produção com replay representativo | Canonical doc |
| `production-failure-regression-flywheel` | Conversão de falhas de produção em evals estratificadas | Implementado |
| `pr-gated-eval-enforcement` | Enforcement de evals no fluxo de PR e merge | Canonical doc |
| `eval-to-production-correlation-tracking` | Rastreamento de correlação eval score ↔ outcomes de produção | Canonical doc |
| `n-plus-one-long-session-evals` | Evals N+1 para validar continuidade após redução de contexto | Canonical doc |
| `late-failure-regression-suite` | Suite de regressão para falhas tardias em sessões longas | Canonical doc |
| `repeatable-agent-spot-check-set` | Seed set repetível de spot-checks para workflows críticos | Canonical doc |
| `stable-harness-prompt` | Preservação do harness prompt estável durante redução de contexto | Canonical doc |

### 3.4 Agent Governance & Multi-Agent

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `owned-agent-control-loop` | Loop de controle decomposto em Prompt, Context Builder, Switch, Loop | Canonical doc |
| `deterministic-tool-dispatch` | Ferramentas como JSON + código determinístico | Canonical doc |
| `error-context-hygiene` | Higiene de erros: sumarizar, limpar ao recuperar, nunca blind-append | Canonical doc (implementado em skills) |
| `serializable-pause-resume-state` | Serialização de estado para pause/resume | Canonical doc |
| `generator-evaluator` | Dois agentes: Generator (criativo) + Evaluator (imparcial) com loop de feedback | Canonical doc |
| `constraint-anchored-evaluation` | Avaliação objetiva ancorada em constraints explícitas | Canonical doc |
| `compartmented-evaluation-architecture` | Builder e Validator com superfícies de informação seladas | Canonical doc |
| `multi-model-evaluation-council` | Conselho de avaliação com múltiplos modelos e política de divergência | Canonical doc |
| `split-brain-planning-review` | Revisão de planejamento com rubricas separadas de engenharia e destino | Canonical doc |
| `resolver-based-context-progressive-disclosure` | Disclosure progressivo de contexto guiado por resolver | Canonical doc |
| `grill-me-alignment-interview` | Entrevista de alinhamento uma-pergunta-por-vez com ledger de decisões | Canonical doc |
| `shared-design-concept-handoff` | Contrato de handoff entre entrevista de alinhamento e artefatos downstream | Canonical doc |
| `vertical-slice-issue-generation` | Issues como fatias verticais cross-layer com comportamento observável | Canonical doc |
| `architecture-as-agent-affordance` | Arquitetura como affordance: deep modules, interfaces simples, testes de fronteira | Canonical doc |

### 3.5 Intent & Constraint Engineering

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `intent-five-part-primitive` | Intenção decomposta em 5 campos: description, constraints, failure scenarios, success scenarios, connections | Canonical doc + skill + exercícios N2 |
| `ice-craft-separation` | Separação Intent/Context/Expectations com donos explícitos | Canonical doc |
| `human-owned-expectations-boundary` | Fronteira: definição de "pronto" é do outcome owner, não do agente | Canonical doc |
| `constraint-budget-gate` | Limite rígido de 5-7 constraints direcionais e incondicionais | Canonical doc + skill + exercícios N3 |
| `constraint-failure-decision-rule` | Classificação: "Saber isso mudaria o código?" → constraint ou failure condition | Canonical doc + skill + exercícios N3 |
| `two-implementations-goal-test` | Heurística: duas implementações diferentes podem satisfazer? → goal vs spec | Canonical doc + exercícios N2 |
| `goal-atomicity-split` | Um goal = uma sentença, sem "and", sem "then" | Canonical doc + exercícios N2 |
| `token-economics-gap-filling` | Custo de tokens do preenchimento de lacunas vs especificação completa | Canonical doc |
| `symphony-trap-awareness` | Risco de over-specification e perda de adaptabilidade | Canonical doc |

### 3.6 Human-in-the-Loop & Oversight

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `manual-brake-question-gate` | 3 perguntas de valor antes de autorizar construção por agente | Canonical doc + skill |
| `human-afk-task-routing-gate` | Classificação de tarefas como AFK-ready ou human-in-loop em 4 dimensões | Canonical doc |
| `presence-in-the-loop-metric` | Métrica de presença humana DURANTE execução, não só aprovação final | Canonical doc + exercícios N3 |
| `deferred-ledger-agentic-work` | Ledger de dívida agentica com rastreamento e sunset gates | Canonical doc + skill |
| `carry-debt-sunset-gate` | Prazo máximo para resolver débitos antes que bloqueiem o pipeline | Canonical doc |
| `owner-of-no-role-design` | Cada artefato tem exatamente um dono; papéis explícitos | Canonical doc + skill |
| `accidental-brake-replacement` | Anti-padrão: gates de segurança removidos silenciosamente | Canonical doc |
| `value-gated-agent-control-loop` | Agente só avança quando valor incremental é validado | Canonical doc |

### 3.7 Model Training & Autonomy

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `on-policy-rollout-feedback-loop` | Loop de feedback on-policy com correção contínua professor→estudante | Canonical doc |
| `autonomy-curriculum-sampling` | Amostragem curricular progressiva (observe→assist→own) | Canonical doc + skill + exercícios N3 |
| `privileged-context-self-distillation` | Self-distillation com contexto privilegiado | Canonical doc |
| `consensus-gated-privileged-information` | Gate de consenso entre múltiplos avaliadores | Canonical doc |
| `asymmetric-failure-correction-router` | Roteador que separa correção de falhas de reforço de sucessos | Canonical doc |
| `magnitude-direction-verifier-split` | Separação magnitude/direção em verificadores | Canonical doc + skill + exercícios N3 |
| `adaptive-style-compression-teacher` | Professor adaptativo de compressão de estilo | Canonical doc |

### 3.8 Review & Quality

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `qa-to-backlog-feedback-loop` | Achados de QA/review como entrada de backlog | Canonical doc |
| `persona-based-documentation` | Documentação por persona (dev, QA, architect, manager) | Canonical doc + exercícios N3 |
| `shadow-review-pipeline` | Shadow review: agente executa revisão paralela antes do merge | Canonical doc + skill |
| `contextual-severity-calibration` | Severidade ajustada por perfil de risco do módulo | Canonical doc + skill |
| `review-contract-checklist` | Itens verificáveis obrigatórios em toda revisão de código | Canonical doc |
| `pre-commit-ai-review-gate` | Validação automática por agente antes do commit | Canonical doc |
| `three-part-intent-contract` | Contrato de intenção: goal, scenario, destination | Canonical doc |
| `scenario-destination-split` | Separação cenário (contexto) vs destino (resultado) | Canonical doc |

### 3.9 Analysis & Strategy

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `asymmetric-binary-outcome-positioning` | Modelagem de eventos binários com probabilidade real vs implícita | Canonical doc |
| `institutional-layer-amplification` | Gaps regulatórios que se ampliam a cada nível institucional | Canonical doc |
| `second-order-institutional-interaction` | Interações de segunda ordem entre reformas institucionais | Canonical doc |
| `institutional-safety-valve-escalation-cycle` | Ciclo de escalada da válvula de segurança institucional | Canonical doc |
| `credibility-cascade-regulated-assets` | Cascata de credibilidade em ativos regulados | Canonical doc |
| `energy-value-chain-spread-analysis` | Análise de spread em cadeias de valor multi-camada (MWh→tokens→inferência) | Canonical doc |
| `inelastic-market-flow-dominance-model` | Modelo de dominância de fluxo em mercados inelásticos | Canonical doc |
| `social-archetype-classification` | Taxonomia: Criação, Abundância, Predação | Canonical doc |
| `spread-capture-analytical-primitive` | "Quem captura o spread?" como primitiva analítica | Canonical doc |
| `capex-revenue-credit-mispricing` | Mispricing de crédito por obsolescência tecnológica | Canonical doc |

### 3.10 Publishing

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `quarto-publishing-architecture` | Arquitetura Quarto: config-driven, source bridge, multi-format fan-out | Canonical doc |
| `quarto-authoring-workflow` | Fluxo de autoria: live preview, dependency-gated build, single-command deploy | Canonical doc |
| `quarto-content-structure` | Estrutura de conteúdo: parts-based chapters, landing page | Canonical doc |

### 3.11 Cross-Cutting

| Padrão | O que resolve | Maturidade |
|--------|--------------|------------|
| `obsidian-document-conventions` | Convenções de frontmatter, wikilinks, tags, validação | Implementado (AGENTS.md Rule 16 + validate-obsidian.ts) |
| `epistemic-memory-graph` | Grafo de memória com status epistêmico e proveniência | Implementado (obsidian-eval epistemic) |
| `trace-instrumentation` | 3 camadas de defesa: instrução AGENTS.md, enforcement post-hoc, health check cross-session | Implementado (task-wrapper.sh) |

---

## 4. Terminology

Termos-chave do ecossistema, com definições e localização da fonte canônica.

### 4.1 Termos do currículo (Nível 1 — Fundamentos)

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Agent (Agente)** | Entidade autônoma de IA (baseada em LLM) que toma ações, usa ferramentas e executa tarefas em sequência | `curriculum/GLOSSARY.md:18` |
| **Context Window** | Número total de tokens que um modelo pode processar por vez — a "memória imediata" do agente | `curriculum/GLOSSARY.md:158` |
| **Context Amnesia** | Quando um agente "esquece" contexto anterior por ter excedido a janela de contexto | `curriculum/GLOSSARY.md:50` |
| **Context Rot** | Perda gradual de coerência conforme o agente avança na janela de contexto | `curriculum/GLOSSARY.md:149` |
| **Context Anxiety** | Comportamento ansioso/precipitado do agente ao se aproximar do limite de contexto | `curriculum/GLOSSARY.md:138` |
| **Token** | Unidade básica de texto que um LLM processa (~4 caracteres) | `curriculum/GLOSSARY.md:770` |
| **Token Budget** | Gerenciamento consciente de quantos tokens estão disponíveis e como são alocados | `curriculum/GLOSSARY.md:783` |
| **Harness** | Infraestrutura e padrões que envolvem agentes para torná-los confiáveis por períodos longos | `curriculum/GLOSSARY.md:370` |
| **METR** | Model Evaluation Task Completion Rate — percentagem de tarefas completadas com sucesso | `curriculum/GLOSSARY.md:474` |

### 4.2 Termos do currículo (Nível 2 — Padrões Práticos)

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Generator/Evaluator** | Duas entidades separadas: uma gera, outra avalia. Previne sycophancy | `curriculum/GLOSSARY.md:333` |
| **Sprint Contract** | Acordo negociado entre generator e evaluator sobre o que "pronto" significa | `curriculum/GLOSSARY.md:191` |
| **Evaluation Rubric** | Conjunto de critérios mensuráveis para avaliar qualidade subjetiva | `curriculum/GLOSSARY.md:236` |
| **Trace (Agent Trace)** | Log detalhado de cada passo do agente — ferramenta primária de debugging | `curriculum/GLOSSARY.md:830` |
| **ICE Craft Separation** | Decomposição em Intent, Context, Expectations com donos explícitos | `curriculum/GLOSSARY.md:419` |
| **Intent as Five-Part Primitive** | Formalização do intent em 5 campos obrigatórios | `curriculum/GLOSSARY.md:436` |
| **Two-Implementations Goal Test** | Heurística: duas implementações diferentes podem ambas satisfazer? → goal vs spec | `curriculum/GLOSSARY.md:849` |
| **Goal Atomicity Split** | Um goal = uma sentença sem conjunções | `curriculum/GLOSSARY.md:304` |
| **Token Economics of Gap-Filling** | Custo de tokens do preenchimento de lacunas vs especificação completa | `curriculum/GLOSSARY.md:797` |

### 4.3 Termos do currículo (Nível 3 — Arquitetura Avançada)

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Multi-Agent System** | Múltiplos agentes independentes que coordenam entre si | `curriculum/GLOSSARY.md:512` |
| **Harness Evolution** | Processo de simplificar/remover componentes de harness conforme o modelo melhora | `curriculum/GLOSSARY.md:387` |
| **LLM as Fuzzy Compiler** | LLM como compilador fuzzy, harness como passes de otimização, código como artefato descartável | `curriculum/GLOSSARY.md:271` |
| **Constraint Budget Gate** | Limite rígido de 5-7 constraints direcionais por tarefa | `curriculum/GLOSSARY.md:106` |
| **Constraint-Failure Decision Rule** | "Saber isso mudaria o código?" → classifica como constraint ou failure condition | `curriculum/GLOSSARY.md:122` |
| **Compartmented Evaluation** | Builder e Validator com superfícies de informação seladas | `curriculum/GLOSSARY.md:90` |
| **Presence-in-the-Loop Metric** | Métrica de envolvimento humano DURANTE execução, não só aprovação final | `curriculum/GLOSSARY.md:592` |
| **Garbage Collection Day** | Meta-loop semanal de limpeza de harness: revisão de slop, guardrails, manutenção | `curriculum/GLOSSARY.md:291` |
| **Persona-Based Documentation** | Documentação por especialidade (front-end, security, UX, product) como NFRs | `curriculum/GLOSSARY.md:574` |
| **Relational Context Graph** | Grafo com edges tipados (dependency, provenance, supersession, causation) | `curriculum/GLOSSARY.md:612` |
| **Tiered Context Storage** | 3 tiers (hot/warm/cold) com promoção/demissão dinâmica por relevância | `curriculum/GLOSSARY.md:814` |
| **Neutral Selection Layer** | Camada de seleção model-agnostic e vendor-independent | `curriculum/GLOSSARY.md:530` |
| **Selection-Budgeted Retrieval** | Retrieval com ranking por valor/custo, budget awareness | `curriculum/GLOSSARY.md:661` |
| **Deliberate Forgetting** | Esquecimento como operação intencional de primeira classe | `curriculum/GLOSSARY.md:205` |
| **Smallest Sufficient Context** | Subconjunto mínimo que o agente precisa para raciocinar corretamente | `curriculum/GLOSSARY.md:697` |

### 4.4 Termos do ecossistema (Runtime)

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Vault** | Repositório de conhecimento em Markdown gerenciado pelo `obsidian-eval` | `docs/ecosystem-glossary.md:40` |
| **MANIFEST.md** | Declaração de dependências cross-vault (exports/imports) | `docs/ecosystem-glossary.md:65` |
| **Cross-vault Wikilink** | Wikilink com prefixo `vault:<nome>/` que referencia outro vault | `docs/ecosystem-glossary.md:96` |
| **Knowledge Pipeline** | Fluxo completo: handoff → compress → relevance → promote → provenance → drift → append | `docs/ecosystem-glossary.md:194` |
| **Handoff** | Snapshot de estado de sessão OpenCode (`type: session-handoff`) | `docs/ecosystem-glossary.md:208` |
| **Durable Fact** | Conhecimento persistido com valid_from/valid_to, confidence, provenance | `docs/ecosystem-glossary.md:248` |
| **Provenance Chain** | Trilha de auditoria que registra origem de cada fato durável | `docs/ecosystem-glossary.md:527` |
| **Relevance Score** | Pontuação 0-1 em 5 dimensões: recência, importância, frequência, similaridade, confiança | `docs/ecosystem-glossary.md:283` |
| **Promotion Candidate** | Padrão detectado em ≥3 handoffs similares, candidato a virar princípio | `docs/ecosystem-glossary.md:306` |
| **Reflection Loop** | Pipeline cross-session: Gather → Analyze → Synthesize → Apply | `docs/ecosystem-glossary.md:327` |
| **Ground Truth** | Assertions imutáveis que bloqueiam contaminação do pipeline | `docs/ecosystem-glossary.md:492` |
| **Drift Detection** | Verificação de que princípio candidato não contradiz ground truth | `docs/ecosystem-glossary.md:510` |
| **Simulation** | Geração de handoffs sintéticos para testar propriedades emergentes do pipeline | `docs/ecosystem-glossary.md:546` |
| **Telemetry DB** | Banco SQLite com métricas de sessão: tokens, traces, SLOs, burn rates | `docs/ecosystem-glossary.md:117` |
| **Trace Span** | Registro instrumentado de chamada `task()`: categoria, duração, tokens, success/failure | `docs/ecosystem-glossary.md:138` |
| **Execution Graph** | DAG de tarefas com nós, status, estimativas de tokens, contexto de retomada | `docs/ecosystem-glossary.md:177` |
| **Epistemic Graph** | Grafo de entidades e relacionamentos extraído do vault de runtime | `docs/ecosystem-glossary.md:469` |
| **System of Record** | Documento que define precedência (6 níveis) e fontes canônicas | `docs/ecosystem-glossary.md:569` |
| **MOC (Map of Content)** | Arquivo `_moc-` que agrega wikilinks para cluster temático | `docs/ecosystem-glossary.md:581` |
| **Orchestrator** | Agente principal (Sisyphus) que decompõe e delega para sub-agentes | `docs/ecosystem-glossary.md:445` |
| **Token Budget** | Orçamento de tokens com 4 fases: green/yellow/orange/red | `docs/ecosystem-glossary.md:418` |

### 4.5 Siglas e acrônimos

| Sigla | Significado |
|-------|-------------|
| ADR | Architecture Decision Record |
| KODA | Agente conversacional de venda de suplementos via WhatsApp |
| METR | Model Evaluation Task Completion Rate |
| MCP | Model Context Protocol |
| SOR | System of Record |
| ICE | Intent, Context, Expectations |
| QI | Quality Improvement |
| SLO | Service Level Objective |
| DAG | Directed Acyclic Graph |
| PRNG | Pseudo-Random Number Generator |

---

## 5. Curriculum Structure

O currículo `long-running-agents/curriculum/` é o produto principal do repositório: um programa completo de 12 semanas sobre construção de agentes long-running, aplicado ao caso real do KODA.

### 5.1 Estrutura de diretórios

```
curriculum/
├── README.md                     ← Visão geral, estrutura, métricas
├── MASTER_PLAN.md                ← Plano mestre com níveis e conceitos
├── INDEX.md                      ← Índice executivo com navegação por perfil
├── QUICK_START.md                ← Onboarding rápido (45 min)
├── EXECUTION_PLAN.md             ← Cronograma detalhado de 12 semanas
├── GLOSSARY.md                   ← 1002 linhas de termos técnicos
├── FAQ.md                        ← Perguntas frequentes
│
├── 01-nivel-1-fundamentals/      ← N1: Por que agentes falham (3-4h)
│   ├── 01-why-agents-lose-plot.md
│   ├── 02-token-budgeting.md
│   ├── 03-basic-harness-patterns.md
│   ├── exercises/ (3 exercícios)
│   └── koda-applications/
│
├── 02-nivel-2-practical-patterns/ ← N2: Padrões práticos (6-8h)
│   ├── 01-generator-evaluator-pattern.md
│   ├── 02-sprint-contracts.md
│   ├── 03-rubric-design.md
│   ├── 04-trace-reading.md
│   ├── exercises/ (7 exercícios + solutions)
│   └── koda-applications/
│
├── 03-nivel-3-advanced-architecture/ ← N3: Arquitetura avançada (8-10h)
│   ├── 01-multi-agent-systems.md
│   ├── 02-state-persistence.md
│   ├── 03-file-based-coordination.md
│   ├── 04-server-side-compaction.md
│   ├── 05-harness-evolution.md
│   ├── exercises/ (10 exercícios + solutions)
│   └── koda-applications/
│
├── 04-nivel-4-koda-specific/     ← N4: Aplicação KODA (contínuo)
│   ├── 01-koda-architecture.md
│   ├── 02-customer-journey-flows.md
│   ├── 03-feature-design-patterns.md
│   ├── 04-evaluation-rubrics-koda.md
│   ├── 05-harness-improvements.md
│   ├── real-world-exercises/ (5 exercícios)
│   └── case-studies/ (3 estudos de caso KODA)
│
├── 05-core-concepts/             ← 8 conceitos core aprofundados
│   ├── 01-context-management.md
│   ├── 02-planning-execution-separation.md
│   ├── 03-generator-evaluator-pattern.md
│   ├── 04-sprint-contracts.md
│   ├── 05-state-persistence.md
│   ├── 06-harness-evolution.md
│   ├── 07-multi-agent-coordination.md
│   ├── 08-evaluation-rubrics.md
│   └── exercises/
│       ├── exercise-tiered-context-storage.md
│       ├── exercise-neutral-selection-layer.md
│       └── exercise-selection-budgeted-retrieval.md
│
├── 06-knowledge-graphs/         ← 35+ diagramas Mermaid
├── 07-implementation-guides/    ← 6 guias: setup, progression, harness design, trace analysis, etc.
├── 08-tools-templates/          ← 6 templates: ADR, rubric, sprint contract, tracker, etc.
├── 09-case-studies/             ← 5 estudos de caso (2 genéricos + 3 KODA)
└── 10-references/               ← Timeline de capacidade de modelos, recursos adicionais
```

### 5.2 Progressão de níveis

| Nível | Carga | Pergunta central | Conceitos-chave |
|-------|-------|-----------------|-----------------|
| **N1 — Fundamentos** | 3-4h | Por que agentes falham em tarefas longas? | Context window, token budget, harness básico, amnesia, context rot |
| **N2 — Padrões Práticos** | 6-8h | Como fazer agentes mais confiáveis? | Generator/Evaluator, sprint contracts, rubrics, trace reading, ICE separation, intent primitives |
| **N3 — Arquitetura Avançada** | 8-10h | Como construir sistemas sofisticados? | Multi-agent, state persistence, file coordination, harness evolution, LLM as fuzzy compiler, context storage tiers |
| **N4 — Aplicação KODA** | Contínuo | Como aplicar tudo em produção? | Arquitetura KODA, customer journeys, feature patterns, evaluation, harness improvements |

### 5.3 8 conceitos core

Cada conceito tem explicação profunda, 3 knowledge graphs (Mermaid), aplicação KODA e checklist:

1. **Context Management** — Gerenciamento de janela de contexto, token budgeting, truncation
2. **Planning-Execution Separation** — Separação entre planejar e executar
3. **Generator-Evaluator Pattern** — Dois agentes, geração e avaliação separadas
4. **Sprint Contracts** — Acordos explícitos sobre definição de "pronto"
5. **State Persistence** — Persistência de estado entre sessões
6. **Harness Evolution** — Evolução do harness conforme modelos melhoram
7. **Multi-Agent Coordination** — Coordenação entre múltiplos agentes
8. **Evaluation Rubrics** — Critérios mensuráveis para qualidade subjetiva

### 5.4 Exercícios por nível

| Nível | Total de exercícios | Destaques |
|-------|-------------------|-----------|
| N1 | 3 | Fundamentos de context window, token budget, harness básico |
| N2 | 7 | Error context hygiene, intent five-part primitive, two-implementations goal test, goal atomicity split |
| N3 | 10 + 3 core | Constraint budget gate, constraint-failure decision rule, persona-based documentation, LLM as fuzzy compiler, autonomy curriculum sampling, magnitude-direction verifier split + tiered-context-storage, neutral-selection-layer, selection-budgeted-retrieval |
| N4 | 5 + 3 cases | Manual brake question gate, deferred ledger, KODA-specific exercises |

---

## 6. Existing Gaps

Gaps documentados como pendentes ou em andamento, extraídos de `.omo/plans/`, `system-of-record.md` e análise direta.

### 6.1 Gaps de runtime (P0 — observabilidade e evals automatizadas)

| Gap | Descrição | Plano | Status |
|-----|-----------|-------|--------|
| **Gap 2a — Runtime Canonical Eval Gate** | Avaliação automatizada pós-task() que verifica conformidade com regras canônicas. 8 tasks, design completo, 12 decisões resolvidas. | `2026-06-21-runtime-canonical-eval-gate.md` | Aguardando autorização |
| **Gap 2b — KODA Domain Evals** | Golden dataset de 20-30 cenários ecommerce, CI gate para regressão de prompt. Fora do escopo do runtime. | Mencionado em runtime-canonical-eval-gate.md | Não iniciado |
| **Handoff como RunContext (Opção B)** | ~730 LOC para "crash = pause" na fronteira de task(). 4 gates P0 pendentes. | `2026-06-20-handoff-runcontext-option-b.md` | Bloqueado (REV 3) |
| **Gap 2 (classifier calibration)** | Calibração do classificador LLM-as-judge com dados reais de produção | `2026-06-23-correction-first-scavenger-pipeline-unified.md` | Pendente |
| **Gap 4 (scavenger dry-run)** | Dry-run do scavenger pipeline com dados reais | `2026-06-23-correction-first-scavenger-pipeline-unified.md` | Pendente |
| **E2E smoke test (8.4)** | Teste end-to-end completo do scavenger pipeline | `2026-06-23-correction-first-scavenger-pipeline-unified.md` | Pendente |

### 6.2 Gaps de documentação canônica

Documentos esperados quando o domínio correspondente amadurecer, listados em `system-of-record.md:277-285`:

| Documento | Cobre | Status |
|-----------|-------|--------|
| `agent-lifecycle.md` | Ciclo completo claim → worktree → implement → review → merge → cleanup | Pendente |
| `curriculum-model.md` | Taxonomia de níveis, tipos de artefato, critérios de qualidade | Pendente |
| `portal-architecture.md` | Decisões de design do portal, modelo de dados, pipeline de renderização | Pendente (quando SPA for implementada) |
| `crossroad-change-policy.md` | Política de alteração em arquivos de alto blast radius | Pendente |

### 6.3 Gaps de ADRs

Tópicos candidatos a ADR, listados em `system-of-record.md:158-163`:

| Tópico | Descrição |
|--------|-----------|
| Stack do portal | Vanilla JS estático vs. framework |
| Content chunking | Modelo de carregamento sob demanda |
| Persistência de estado | Estratégia entre agentes |
| Versionamento do currículo | Política de versionamento |

### 6.4 Gaps de implementação

| Gap | Descrição | Plano |
|-----|-----------|-------|
| **Gap 4 — Observabilidade** | Dashboard de telemetria com dados reais, runbooks completos | `2026-06-18-observabilidade-agentica-plano-macro.md` (fases 3-5) |
| **Gap 5 — Skill test harness** | Expansão para todos os 25 skills | `2026-06-18-skill-test-harness-expansion.md` |
| **P1 — Experimentação de prompts** | Infraestrutura para A/B test de prompts entre sessões | `2026-06-14-maturidade-llm-estado-atual-e-gaps.md` |
| **P1 — Memória cross-session** | Aprimoramento do pipeline de conhecimento para capturar mais padrões | `2026-06-14-maturidade-llm-estado-atual-e-gaps.md` |

### 6.5 Gaps de currículo

| Gap | Descrição | Evidência |
|-----|-----------|-----------|
| Core concepts com status ⏳ | Todos os 8 core concepts estão marcados como "⏳" (pending) no README | `curriculum/README.md` (tabela de conceitos) |
| FAQ em construção | FAQ.md listado como "em construção" | `curriculum/README.md` |
| Maturidade de exercises | Nem todos os níveis têm solutions/ completas | Inspeção de diretórios |
| Integração com canonical docs | Vários exercícios N3 referenciam canonical docs que foram criados depois do currículo | Cross-reference |

### 6.6 Decisões arquiteturais pendentes de formalização

Os 13 ADRs em `plans/adr/` estão aceitos, mas:

- `docs/decisions/` (long-running-agents) contém apenas 1 ADR interno (`skill-canons-bridge-implementation`)
- A maioria das decisões arquiteturais do runtime (flywheel, telemetry, tracer, scavenger) está documentada em planos `.omo/plans/`, não em ADRs formais
- O system-of-record referencia `docs/decisions/` como fonte de precedência #1, mas os ADRs reais vivem em `plans/adr/` (workspace-level)

---

## 7. Invariants & Constraints

### 7.1 Invariantes do workspace (AGENTS.md)

- Nunca usar `as any`, `@ts-ignore`, `@ts-expect-error` para silenciar erro de tipo
- Nunca apagar/enfraquecer teste para passar
- Nunca usar comando git destrutivo sem aprovação explícita
- Nunca commitar sem pedido explícito
- Toda delegação `task()` DEVE ser instrumentada com `task-wrapper.sh` (Trace Instrumentation Gate)
- Toda verificação de token budget DEVE usar o tokenizer real primeiro, heurística só como fallback
- Exploration cache DEVE ser consultado antes de disparar `explore`/`librarian` agents
- Task output DEVE ser validado contra schema após delegações `deep`/`ultrabrain`/`unspecified-high`

### 7.2 Ground Truths (5)

Assertions imutáveis em `~/sisyphus-runtime/facts/_global/ground-truth.md`:

1. Nunca usar `grep`, `sed`, `awk` para leitura via bash (usar tools dedicadas)
2. Nunca suprimir erros de tipo com `as any`, `@ts-ignore`
3. Nunca apagar ou enfraquecer testes para "passar"
4. Sempre carregar `canonical-context` antes de decisões de arquitetura
5. Sempre usar `obsidian-eval` para navegar vaults

### 7.3 Precedência de documentação

Definida em `long-running-agents/docs/system-of-record.md:14-21`:

1. ADRs aceitos em `docs/decisions/`
2. Documentação canônica ativa em `docs/canonical/`
3. Evidências validadas em `docs/evidence/`
4. Análises e diagnósticos em `docs/analysis/`
5. Documentos históricos em `docs/archive/`
6. READMEs, planos, agent definitions e resumos operacionais

---

## 8. Governance Model

### 8.1 Sistema de agentes

- **Orquestrador**: Sisyphus (principal) — decompõe tarefas, delega para sub-agentes
- **Sub-agentes**: `explore`, `librarian`, `oracle`, `deep`, `ultrabrain`, `quick`
- **Modelo**: Handoff Protocol (HoP) — cada agente tem escopo fechado, dono, gates de validação
- **Skills**: 28 no total (25 em `~/.config/opencode/skills/`, 3 em `.opencode/skills/`)
- **Testes**: 237 testes para skills, 26/26 suites passam

### 8.2 Automatização (systemd timers)

| Timer | Frequência | Função |
|-------|-----------|--------|
| `reflection-runner.timer` | Diário 09:00 BRT | Pipeline de aprendizado cross-session |
| `telemetry-daily.timer` | Diário 09:00 BRT | Sumário diário de métricas |
| `telemetry-retention.timer` | Dominical 03:00 BRT | Limpeza de dados antigos |
| `telemetry-slo-check.timer` | A cada 6h | Verificação de SLOs e burn rate |
| `telemetry-collect.timer` | A cada 15 min | Coleta de artifacts órfãos (safety net) |
| `flywheel-daemon.timer` | A cada 60s | Processamento de triggers de falha → correção automática |
| `telemetry-backup.timer` | Diário 04:07 BRT | Backup do telemetry.db |

### 8.3 Learning Flywheel (ciclo fechado)

O flywheel é o sistema que fecha o loop entre detecção e correção:

1. **Trigger**: Flywheel daemon processa arquivos em `~/.reflection/qi-pending/` a cada 60s
2. **Classificação**: Classifier (regex + cache + LLM-as-judge) categoriza erros
3. **Consumer**: Findings com `anomaly_score ≥ 80` e `skills_affected ≤ 2` disparam QI loop automático
4. **Correção**: QI loop executa `review-work → recommendation-writer → writing-plans → implement → re-verify`
5. **Verificação**: `canonical-context` skill injeta findings na próxima sessão se houver P1 ou score ≥ 60

---

*Modelo mental construído em 2026-06-26. Fontes: `AGENTS.md`, `long-running-agents/README.md`, `system-of-record.md`, `curriculum/GLOSSARY.md`, `ecosystem-glossary.md`, `obsidian-eval/README.md`, `.omo/plans/`, `plans/adr/`.*
