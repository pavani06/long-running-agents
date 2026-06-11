---
title: "System of Record"
type: system-of-record
aliases: ["system of record", "source of truth", "governance index", "SOR", "governanca", "precedencia", "taxonomia"]
tags: ["index", "arquitetura", "governanca"]
last_updated: 2026-06-11
relates-to: []
sources: []
---
# System of Record

Mapa das fontes canônicas do `long-running-agents`. Quando duas fontes divergirem, a precedência abaixo resolve o conflito.

## Precedência

1. **ADRs aceitos** em `docs/decisions/` — decisões de arquitetura formalizadas e aprovadas
2. **Documentação canônica ativa** em `docs/canonical/` — descrições autoritativas de sistemas e contratos
3. **Evidências validadas** em `docs/evidence/` — benchmarks, resultados de teste, métricas
4. **Análises e diagnósticos** em `docs/analysis/` — investigações pontuais, comparações, diagnósticos
5. **Documentos históricos** em `docs/archive/` — versões anteriores, documentos obsoletos
6. **READMEs, planos, agent definitions e resumos operacionais** — fontes de entrada, não autoritativas

## Domínios do projeto

### Agentes e orquestração

O sistema de agentes é definido em `.opencode/` e segue o modelo HoP (Handoff Protocol): cada agente tem um escopo fechado, um dono, e gates de validação.

| Fonte | Cobre |
|---|---|
| [[.opencode/agents/hop-orchestrator-rezek|.opencode/agents/hop-orchestrator-rezek.md]] | Orquestrador principal — governança, source-of-truth, coordenação |
| [[.opencode/agents/koda-hop-init-basic|.opencode/agents/koda-hop-init-basic.md]] | Subagente de inicial guiada do KODA |
| [[.opencode/agents/hop-live-whatsapp-tester|.opencode/agents/hop-live-whatsapp-tester.md]] | Subagente de teste live de WhatsApp |
| [[.opencode/skills/issue-start/SKILL|.opencode/skills/issue-start/SKILL.md]] | Workflow claim → worktree → execution brief |
| [[.opencode/skills/issue-review/SKILL|.opencode/skills/issue-review/SKILL.md]] | Workflow validação → draft PR → second-agent review |
| [[.opencode/skills/issue-finish/SKILL|.opencode/skills/issue-finish/SKILL.md]] | Workflow merge → cleanup branch/worktree/labels |
| [[.opencode/skills/issue-workflow/SKILL|.opencode/skills/issue-workflow/SKILL.md]] | Ciclo completo de lifecycle de issue |
| [[.opencode/skills/refine-issue/SKILL|.opencode/skills/refine-issue/SKILL.md]] | Decomposição de issues em sub-issues com dependências |
| [[.opencode/skills/orchestrator/SKILL|.opencode/skills/orchestrator/SKILL.md]] | Coordenação de agentes paralelos, dashboard de status |
| [[.opencode/skills/doc-coauthoring/SKILL|.opencode/skills/doc-coauthoring/SKILL.md]] | Workflow de co-autoria de documentação |
| [[.opencode/skills/writing-plans/SKILL|.opencode/skills/writing-plans/SKILL.md]] | Criação de planos de implementação detalhados |
| [[.opencode/skills/error-context-hygiene/SKILL|.opencode/skills/error-context-hygiene/SKILL.md]] | Skill de implementação: 4 regras de higiene de erro no contexto |
| [[.opencode/skills/analyze-and-improve/SKILL|.opencode/skills/analyze-and-improve/SKILL.md]] | Pipeline knowledge → patterns → classification → improvements |
| [[AGENTS]] | Regras operacionais obrigatórias para agentes e colaboradores |

> **Pendente**: `docs/canonical/agent-lifecycle.md` descrevendo o ciclo claim → worktree → implement → review → merge → cleanup.

### Currículo e conteúdo

O currículo é o produto principal do repositório: um programa completo de 12 semanas sobre construção de agentes long-running aplicados ao KODA.

| Fonte | Cobre |
|---|---|
| [[curriculum/README|curriculum/README.md]] | Visão geral do programa, estrutura, métricas de sucesso |
| [[curriculum/MASTER_PLAN|curriculum/MASTER_PLAN.md]] | Plano mestre com todos os níveis e conceitos |
| [[curriculum/INDEX|curriculum/INDEX.md]] | Índice executivo com navegação por perfil |
| [[curriculum/QUICK_START|curriculum/QUICK_START.md]] | Onboarding rápido em 45 minutos |
| [[curriculum/EXECUTION_PLAN|curriculum/EXECUTION_PLAN.md]] | Cronograma detalhado de 12 semanas |
| [[curriculum/GLOSSARY|curriculum/GLOSSARY.md]] | Glossário de termos técnicos |
| `curriculum/01-nivel-1-fundamentals/` | Nível 1 — conceitos fundamentais (3-4h) |
| `curriculum/02-nivel-2-practical-patterns/` | Nível 2 — padrões práticos (6-8h) |
| `curriculum/03-nivel-3-advanced-architecture/` | Nível 3 — arquitetura avançada (8-10h) |
| `curriculum/04-nivel-4-koda-specific/` | Nível 4 — aplicação específica ao KODA (contínuo) |
| `curriculum/05-core-concepts/` | 8 conceitos core com explicações, graphs e checklists |
| `curriculum/06-knowledge-graphs/` | 35+ diagramas Mermaid |
| `curriculum/07-implementation-guides/` | Guias de setup, progressão, harness design |
| `curriculum/08-tools-templates/` | Templates de sprint contract, rubrica, ADR, progress tracker |
| `curriculum/09-case-studies/` | 5 estudos de caso (retro-game-maker, browser-daw, 3× KODA) |
| `curriculum/10-references/` | Referências externas e timeline de capacidade de modelos |
| [rawfiles/](rawfiles/) | Material-fonte usado para gerar o currículo |
| [prompts/](prompts/) | Prompts usados na geração do conteúdo do currículo |

> **Pendente**: `docs/canonical/curriculum-model.md` definindo taxonomia de níveis, tipos de artefato e critérios de qualidade.

### Portal web

Três artefatos HTML estáticos e uma proposta de arquitetura futura.

| Fonte | Cobre |
|---|---|
| [web/koda_course_portal.html](web/koda_course_portal.html) | Portal do curso — data-driven, vanilla JS, metadata-only |
| [web/koda_knowledge_graphs_35_diagrams.html](web/koda_knowledge_graphs_35_diagrams.html) | Visualizador dos 35 diagramas Mermaid com renderização sequencial |
| [web/mhc_visao_estrategica.html](web/mhc_visao_estrategica.html) | Visão estratégica MHC |
| [[webpage/analise-arquitetural|webpage/analise-arquitetural.md]] | Proposta de arquitetura SPA com content chunking, hash routing, lazy Mermaid, busca full-text, dark mode |

> **Pendente**: `docs/canonical/portal-architecture.md` quando a SPA proposta for implementada.

### Stack e tooling

| Fonte | Cobre |
|---|---|
| [package.json](package.json) | Dependências, scripts, engine Node (>= 20.18, ESM) |
| [jsconfig.json](jsconfig.json) | Configuração de módulos e paths para o editor |
| [eslint.config.js](eslint.config.js) | Regras de lint: ESLint 10 + plugin-n + unicorn + 2 regras customizadas |
| [eslint-rules/no-catch-message.js](eslint-rules/no-catch-message.js) | Regra customizada: proíbe mensagem em catch vazio |
| [eslint-rules/no-raw-console-in-scripts.js](eslint-rules/no-raw-console-in-scripts.js) | Regra customizada: proíbe console.log direto em scripts |
| [.editorconfig](.editorconfig) | Convenções de formatação (UTF-8, LF, indent 2 espaços) |
| [Makefile](Makefile) | Atalhos para lint e testes |
| [.env.example](.env.example) | Template de variáveis de ambiente |
| [opencode.json](opencode.json) | Configuração do OpenCode (MCP context7) |

### Governança de repositório

| Fonte | Cobre |
|---|---|
| [[.github/PULL_REQUEST_TEMPLATE|.github/PULL_REQUEST_TEMPLATE.md]] | Template de PR com checklist de crossroad files e revisão |
| [.github/CODEOWNERS](.github/CODEOWNERS) | Política de code ownership para crossroad files |
| [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) | Templates de issue (config.yml, technical.md) |
| [.github/dependabot.yml](.github/dependabot.yml) | Configuração de atualização automática de dependências |
| [scripts/create-curriculum-issues.sh](scripts/create-curriculum-issues.sh) | Script de automação de criação de issues do currículo |

> **Nota**: O PR template referencia crossroad files (`src/lib/safe-console.js`, `src/lib/logger.js`, etc.) e `docs/guides/crossroad-change-policy.md` que ainda não existem no repositório. Esses arquivos devem ser criados quando houver código fonte.

## Decisões de arquitetura (ADRs)

`docs/decisions/` está vazio. Nenhum ADR formal foi registrado.

Tópicos candidatos a ADR:
- Escolha de stack do portal (vanilla JS estático vs. framework)
- Modelo de content chunking e carregamento sob demanda
- Estratégia de persistência de estado entre agentes
- Política de versionamento do currículo

## Documentação canônica pendente

`docs/canonical/` não está mais vazio. Há 28 padrões canônicos ativos.

### Padrões canônicos ativos

| Documento | Cobre |
|---|---|
| `error-context-hygiene.md` | Padrão 6 (12FA): higiene de erros no contexto do agente |
| `deterministic-tool-dispatch.md` | Padrão 2 (12FA): dispatch determinístico de ferramentas |
| `owned-agent-control-loop.md` | Padrão 3 (12FA): loop de controle do agente com 4 componentes |
| `serializable-pause-resume-state.md` | Padrão 4 (12FA): serialização de estado para pause/resume |
| `invariant-compensation-split.md` | Classificação de componentes do harness como invariantes de domínio vs compensações temporárias de modelo |
| `application-owned-agent-control-plane.md` | Contrato unificado de control plane: prompt versionado, schema de ação, dispatch determinístico, estado persistente e gates de intervenção |
| `structured-generation-constraint-validation-circuit.md` | Circuito de geração estruturada + validação de constraints de domínio com repair, rejeição e audit |
| `versioned-durable-agent-state.md` | Contrato de estado durável versionado com schema, migração, writeback, reload e audit trail |
| `tested-degradation-ladder.md` | Escada de degradação testada: classificação de falha → retry → fallback seguro → escalação humana com testes por degrau |
| `measured-harness-evolution-lifecycle.md` | Ciclo de vida BUILD → STABILIZE → SIMPLIFY → REMOVE com ROI, archive e reativação |
| `head-tail-context-truncation.md` | Context reduction com head, tail e middle recuperável por handle |
| `explicit-token-budget-ledger.md` | Ledger explícito para calcular custo de prompt, reservas e saldo de tokens por passo |
| `burn-rate-runtime-forecast.md` | Projeção em tempo real do consumo de tokens e da autonomia restante da sessão |
| `phase-gated-token-health-monitor.md` | Monitor de saúde que converte orçamento e burn rate em fases operacionais |
| `durable-fact-selective-history.md` | Política seletiva que combina fatos duráveis com histórico recente |
| `summary-buffer-continuity.md` | Buffer de resumo contínuo com atualização incremental e frescor explícito |
| `semantic-topic-bucketing.md` | Agrupamento semântico por tópico para reter e resumir contexto por tema |
| `hybrid-context-stack.md` | Pilha híbrida de contexto com prompt, memória, estado durável e omissões recuperáveis |
| `budget-aware-session-handoff.md` | Handoff de sessão consciente do orçamento com reset do contexto ativo |
| `addressable-memory-catalog.md` | Catálogo de memória omitida com `id`, `location`, `preview`, `scope` e `fetch` |
| `n-plus-one-long-session-evals.md` | Evals long-session no padrão N+1 para validar continuidade após redução de contexto |
| `stable-harness-prompt.md` | Preservação do harness prompt estável durante redução de contexto |
| `late-failure-regression-suite.md` | Suite de regressão para falhas tardias em sessões longas |
| `pain-signal-eval-progression-gate.md` | Gate de progressão de evals dirigido por sinais de dor |
| `repeatable-agent-spot-check-set.md` | Seed set repetível de spot-checks para workflows críticos |
| `production-grounded-eval-sampling.md` | Amostragem de evals ancorada em produção e replay representativo |
| `eval-tier-stratification.md` | Estratificação fast/medium/deep para suites de eval |
| `pr-gated-eval-enforcement.md` | Enforcement de evals no fluxo de PR e merge |
| `production-failure-regression-flywheel.md` | Flywheel de regressão para falhas de produção |
| `eval-to-production-correlation-tracking.md` | Rastreamento de correlação entre score de eval e outcomes de produção |
| `closed-loop-agent-operating-system.md` | Sistema operacional de loop fechado para agentes long-running |
| `skill-resolver-skillify-capability-pipeline.md` | Pipeline de capacidade do workflow ao skill resolvível e testado |
| `resolver-based-context-progressive-disclosure.md` | Disclosure de contexto progressivo guiado por resolver |
| `split-brain-planning-review.md` | Revisão de planejamento com rubricas separadas de engenharia e destino |
| `multi-model-evaluation-council.md` | Conselho de avaliação com múltiplos modelos e política de divergência |
| `epistemic-memory-graph.md` | Grafo de memória com status epistêmico e proveniência |
| `domain-embedded-workflow-automation-wedge.md` | Wedge de automação de workflow embutido no domínio e guiado por evidência |
| `obsidian-document-conventions.md` | Convencoes de frontmatter, wikilinks, tags e validacao para documentos Obsidian-ready (AGENTS.md Rule 16) |
| `external-state-persistence.md` | Persistência de estado externo como estratégia unificada: catálogo, recuperação exata, pause/resume e writeback |
| `plan-execute-verify.md` | Separação explícita em três fases (planejar → executar → verificar) com checkpoints e contratos por fase |
| `generator-evaluator.md` | Arquitetura de dois agentes: Generator (criativo) + Evaluator (imparcial) com loop de feedback |
| `constraint-anchored-evaluation.md` | Avaliação objetiva ancorada em constraints explícitas e verificáveis do estado persistido |
| `grill-me-alignment-interview.md` | Entrevista de alinhamento um-pergunta-por-vez com respostas recomendadas e ledger de decisões/deferrals |
| `shared-design-concept-handoff.md` | Contrato de handoff do conceito compartilhado entre entrevista de alinhamento e artefatos downstream |
| `human-afk-task-routing-gate.md` | Gate de classificação que roteia tarefas como AFK-ready ou human-in-loop em 4 dimensões |
| `vertical-slice-issue-generation.md` | Geração de issues como fatias verticais cross-layer com comportamento observável |
| `architecture-as-agent-affordance.md` | Arquitetura como affordance para agentes: deep modules, interfaces simples, testes de fronteira |
| `qa-to-backlog-feedback-loop.md` | Achados de QA/review como entrada de backlog com captura, triagem e conversão em issues |

### Documentos esperados quando o domínio correspondente amadurecer

| Documento | Cobre |
|---|---|
| `agent-lifecycle.md` | Ciclo completo claim → worktree → implement → review → merge → cleanup |
| `curriculum-model.md` | Taxonomia de níveis, tipos de artefato, critérios de qualidade |
| `portal-architecture.md` | Decisões de design do portal, modelo de dados, pipeline de renderização |
| `crossroad-change-policy.md` | Política de alteração em arquivos de alto blast radius |
| `obsidian-document-conventions.md` | AGENTS.md Rule 16 ja cobre — documento canonico so precisa ser criado se a convencao crescer alem de uma regra |

## Análises e diagnósticos

Diagnósticos do backend MHC/KODA em `docs/analysis/mhc-backend/`:

- [[docs/analysis/mhc-backend/2026-05-28-output-validation-structured-generation]] — validação estruturada com Zod/LangChain
- [[docs/analysis/mhc-backend/2026-05-28-janela-deslizante-contexto]] — janela deslizante, resumo e metadados no contexto do agente
- [[docs/analysis/mhc-backend/2026-05-28-output-validation-state-persistence]] — camadas de validação e persistência de estado
- [[docs/analysis/mhc-backend/2026-05-26-nivel-3-comparacao]] — comparação KODA vs. padrões Nível 3
- [[docs/analysis/mhc-backend/2026-05-26-harness-diagnostic]] — arquitetura KODA vs. padrões de harness
- [[docs/analysis/mhc-backend/2026-05-26-nivel-2-diagnostic]] — maturidade de padrões Nível 2 no sistema
- [[docs/analysis/mhc-backend/2026-05-26-pedido-bling-agente]] — falha de notificação de pedido pago (webhook/ERP)

### Análises comparativas (12-Factor Agents)

| Arquivo | Cobre |
|---|---|
| `2026-06-09-12-factor-agents/analysis.md` | Extração de conhecimento não-óbvio da talk 12-Factor Agents |
| `2026-06-09-12-factor-agents/analysis.yaml` | YAML com frameworks, padrões, lições operacionais |
| `2026-06-09-12-factor-agents/patterns.md` | 8 padrões agentic extraídos com 6 campos cada |
| `2026-06-09-12-factor-agents/patterns.yaml` | YAML com componentes e fluxo por padrão |
| `2026-06-09-12-factor-agents/classification.md` | Classificação comparativa dos 8 padrões vs. repo |
| `2026-06-09-12-factor-agents/classification.yaml` | YAML com evidência por padrão |
| `2026-06-09-12-factor-agents/integration-roadmap.md` | Roadmap de integração dos padrões ao currículo |

### Análises comparativas (Eval Maturity Phases)

| Arquivo | Cobre |
|---|---|
| `2026-06-10-eval-maturity-phases/analysis.md` | Framework de maturidade de evals e sinais de transição |
| `2026-06-10-eval-maturity-phases/analysis.yaml` | YAML com framework, fases e sinais |
| `2026-06-10-eval-maturity-phases/patterns.md` | Padrões operacionais extraídos da maturidade de evals |
| `2026-06-10-eval-maturity-phases/patterns.yaml` | YAML com padrões operacionais |
| `2026-06-10-eval-maturity-phases/classification.md` | Classificação das lacunas e coberturas do repositório |
| `2026-06-10-eval-maturity-phases/classification.yaml` | YAML com evidências e lacunas |
| `2026-06-10-eval-maturity-phases/mental-model.md` | Modelo mental e precedência da análise |
| `2026-06-10-eval-maturity-phases/mental-model.yaml` | YAML do modelo mental |
| `2026-06-10-eval-maturity-phases/integration-roadmap.md` | Roadmap de integração dos padrões ao currículo |

### Análises comparativas (Stanford CS153 AI Native Company)

| Arquivo | Cobre |
|---|---|
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/analysis.md` | Extração de conhecimento não-óbvio da fonte Stanford CS153 |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/analysis.yaml` | YAML com a extração estruturada |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/patterns.md` | Catálogo dos 11 padrões agentic extraídos |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/patterns.yaml` | YAML com o catálogo de padrões |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/classification.md` | Classificação dos 11 padrões contra o repositório |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/classification.yaml` | YAML com a classificação estruturada |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/mental-model.md` | Modelo mental de orientação do pacote |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/mental-model.yaml` | YAML do modelo mental |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/integration-roadmap.md` | Mapa de integração dos padrões classificados nas superfícies do repositório |

### Análises comparativas (Matt Pocock AI Coding Workflow)

| Arquivo | Cobre |
|---|---|
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/mental-model.md` | Modelo mental do repositório long-running-agents |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/mental-model.yaml` | YAML do modelo mental |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/analysis.md` | Extração de conhecimento não-óbvio: frameworks, patterns, tradeoffs, failure patterns |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/analysis.yaml` | YAML com extração estruturada |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/patterns.md` | 15 padrões agentic extraídos com 6 campos cada |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/patterns.yaml` | YAML com componentes e fluxo por padrão |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/classification.md` | Classificação comparativa: 1 Better Impl, 12 Partial, 2 Exists |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/classification.yaml` | YAML com evidência file:line por padrão |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/integration-roadmap.md` | Roadmap de integração com 5 fases sequenciais e 12 canonical docs |

## Planos

- [[docs/plans/2026-05-26-curriculum-completion-strategy|docs/plans/2026-05-26-curriculum-completion-strategy.md]] — estratégia de execução para completar o currículo via GitHub Issues/Milestones

---

*Última atualização: 2026-06-11*
