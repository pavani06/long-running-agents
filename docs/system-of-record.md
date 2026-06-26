---
title: "System of Record"
type: system-of-record
aliases: ["system of record", "source of truth", "governance index", "SOR", "governanca", "precedencia", "taxonomia"]
tags: ["index", "arquitetura", "governanca", "harness-engineering", "agentic-coding", "spec-driven-development", "decision-discipline", "testes-qa"]
last_updated: 2026-06-26
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

Topicos cobertos: `agentes-orquestracao`, `agentic-coding`, `spec-driven-development`, `context-engineering`, `evals`, `error-handling`, `harness-engineering`, `12-factor-agents`, `production`, `code-review`, `shadow-review`, `knowledge-management`.

| Fonte | Cobre |
|---|---|
| [[.opencode/agents/hop-orchestrator-rezek.md|.opencode/agents/hop-orchestrator-rezek.md]] | Orquestrador principal — governança, source-of-truth, coordenação |
| [[.opencode/agents/koda-hop-init-basic.md|.opencode/agents/koda-hop-init-basic.md]] | Subagente de inicial guiada do KODA |
| [[.opencode/agents/hop-live-whatsapp-tester.md|.opencode/agents/hop-live-whatsapp-tester.md]] | Subagente de teste live de WhatsApp |
| [[.opencode/skills/issue-start/SKILL.md|.opencode/skills/issue-start/SKILL.md]] | Workflow claim → worktree → execution brief |
| [[.opencode/skills/issue-review/SKILL.md|.opencode/skills/issue-review/SKILL.md]] | Workflow validação → draft PR → second-agent review |
| [[.opencode/skills/issue-finish/SKILL.md|.opencode/skills/issue-finish/SKILL.md]] | Workflow merge → cleanup branch/worktree/labels |
| [[.opencode/skills/issue-workflow/SKILL.md|.opencode/skills/issue-workflow/SKILL.md]] | Ciclo completo de lifecycle de issue |
| [[.opencode/skills/refine-issue/SKILL.md|.opencode/skills/refine-issue/SKILL.md]] | Decomposição de issues em sub-issues com dependências |
| [[.opencode/skills/orchestrator/SKILL.md|.opencode/skills/orchestrator/SKILL.md]] | Coordenação de agentes paralelos, dashboard de status |
| [[.opencode/skills/doc-coauthoring/SKILL.md|.opencode/skills/doc-coauthoring/SKILL.md]] | Workflow de co-autoria de documentação |
| [[.opencode/skills/writing-plans/SKILL.md|.opencode/skills/writing-plans/SKILL.md]] | Criação de planos de implementação detalhados |
| [[.opencode/skills/karpathy-guidelines/SKILL.md|.opencode/skills/karpathy-guidelines/SKILL.md]] | Diretrizes comportamentais Karpathy: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution |
| [[.opencode/skills/error-context-hygiene/SKILL.md|.opencode/skills/error-context-hygiene/SKILL.md]] | Skill de implementação: 4 regras de higiene de erro no contexto |
| [[.opencode/skills/analyze-and-improve/SKILL.md|.opencode/skills/analyze-and-improve/SKILL.md]] | Pipeline knowledge → patterns → classification → improvements. Harness com cache, retry, model tiering, schemas, chunking, trajectory, eval, refinement (8 módulos, stdlib). Completion catalog: `.omo/plans/2026-06-18-analyze-and-improve-speedup-completion.md` |
| [[.opencode/skills/manual-brake-question-gate/SKILL.md|.opencode/skills/manual-brake-question-gate/SKILL.md]] | Gate de pergunta-freio manual que interrompe o agente antes de ações irreversíveis |
| [[.opencode/skills/deferred-ledger-agentic-work/SKILL.md|.opencode/skills/deferred-ledger-agentic-work/SKILL.md]] | Ledger de trabalho agentic diferido com rastreamento de dívida e sunset gates |
| [[.opencode/skills/owner-of-no-role/SKILL.md|.opencode/skills/owner-of-no-role/SKILL.md]] | Design pattern onde cada artefato tem um único dono e papéis são explícitos |
| [[.opencode/skills/intent-five-part-primitive/SKILL.md|.opencode/skills/intent-five-part-primitive/SKILL.md]] | Decomposição de intenção em cinco partes primitivas para especificação precisa de tarefas |
| [[.opencode/skills/presence-in-the-loop-metric/SKILL.md|.opencode/skills/presence-in-the-loop-metric/SKILL.md]] | Métrica de presença-no-loop para calibrar intervenção humana em workflows agentic |
| [[.opencode/skills/shadow-review-pipeline/SKILL.md|.opencode/skills/shadow-review-pipeline/SKILL.md]] | Pipeline de shadow review: agente shadow executa revisão paralela antes do merge |
| [[.opencode/skills/contextual-severity-calibration/SKILL.md|.opencode/skills/contextual-severity-calibration/SKILL.md]] | Calibração contextual de severidade em revisões de código |
| [[.opencode/skills/two-implementations-goal-test/SKILL.md|.opencode/skills/two-implementations-goal-test/SKILL.md]] | Teste de duas implementações para validação de goal specification |
| [[.opencode/skills/goal-atomicity-split/SKILL.md|.opencode/skills/goal-atomicity-split/SKILL.md]] | Decomposição de goals complexos em unidades atômicas |
| [[.opencode/skills/constraint-budget-gate/SKILL.md|.opencode/skills/constraint-budget-gate/SKILL.md]] | Gate de orçamento explícito de constraints por tarefa |
| [[.opencode/skills/constraint-failure-decision-rule/SKILL.md|.opencode/skills/constraint-failure-decision-rule/SKILL.md]] | Regra de decisão para falha de constraint com três caminhos |
| [[.opencode/skills/autonomy-curriculum-sampling/SKILL.md|.opencode/skills/autonomy-curriculum-sampling/SKILL.md]] | Skill de implementação: amostragem curricular progressiva (observe→assist→own) para autonomia do modelo |
| [[.opencode/skills/magnitude-direction-verifier-split/SKILL.md|.opencode/skills/magnitude-direction-verifier-split/SKILL.md]] | Skill de implementação: separação magnitude/direção em verificadores de output |
| [[.opencode/skills/tiered-context-storage/SKILL.md|.opencode/skills/tiered-context-storage/SKILL.md]] | Skill de implementação: armazenamento de contexto em três camadas com promoção/demissão dinâmica |
| [[.opencode/skills/neutral-selection-layer/SKILL.md|.opencode/skills/neutral-selection-layer/SKILL.md]] | Skill de implementação: camada de seleção model-agnostic e vendor-independent |
| [[.opencode/skills/selection-budgeted-retrieval/SKILL.md|.opencode/skills/selection-budgeted-retrieval/SKILL.md]] | Skill de implementação: retrieval com budget awareness e ranking por valor/custo |
| [[.opencode/skills/devils-advocate/SKILL.md|.opencode/skills/devils-advocate/SKILL.md]] | Skill adversarial: reviewer que encontra o caso mais forte CONTRA qualquer premissa, plano ou implementação. Usa agente momus (Claude Opus 4.7). Previne sycophancy por dissent estruturado. Wave 1 anti-sycophancy. |
| [[.opencode/skills/behavioral-eval-path-analysis/SKILL.md|.opencode/skills/behavioral-eval-path-analysis/SKILL.md]] | Skill: Behavioral Eval Path Analysis (Layer 3) — detecta wrong-path-right-answer: duplicatas, loops, uso incorreto de ferramentas, custo por query. Integrado ao trace pipeline e QI loop. |
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
| `curriculum/05-core-concepts/exercises/` | Exercícios avançados (N3): tiered-context-storage, neutral-selection-layer, selection-budgeted-retrieval |
| `curriculum/04-nivel-3-engenharia-avancada/exercises/` | Exercício N3: behavioral-eval-path-analysis — detectar wrong-path-right-answer em traces de execução |
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
| [../obsidian-eval/](../obsidian-eval/) | Runtime da CLI `obsidian-eval`: scan, query, graph, write, manifest, epistemic graph (módulos `epistemic-types.ts`, `entity-extractor.ts`, `epistemic-graph.ts`). Biblioteca `@pavani/obsidian-eval`. |
| [../scripts/telemetry/](../scripts/telemetry/) | Stack de telemetria do runtime Sisyphus: `tracer.ts` (spans), `trace-cli.ts` (CLI), `task-wrapper.sh` (wrapper --start-only/--end-last/--wrap), `collector.ts` (SQLite), `collect-session.sh` (bridge), `session-end-hook.sh` (hook pós-sessão). 25 testes. |
| [[docs/canonical/trace-instrumentation|Trace Instrumentation]] | Padrão canônico de instrumentação de tracing: 3 camadas de defesa (instrução no AGENTS.md, enforcement post-hoc, health check cross-session), 3 modos de wrapper, 8 skills instrumentados. |
| [../scripts/sisyphus/handoff-path.sh](../scripts/sisyphus/handoff-path.sh) | Single source of truth para nome determinístico de handoff (`sessions/<repo>/<YYYY-MM-DD-HHMMSS-utc>-<agent>-handoff.md`). Previne colisões same-day removendo o grau de liberdade do agente. Usado pelo `session-handoff/SKILL.md` com safety net (Camada B) de validação pós-write. |

### Governança de repositório

Topicos cobertos: `governanca`, `decision-discipline`, `spec-driven-development`.

| Fonte | Cobre |
|---|---|
| [[.github/PULL_REQUEST_TEMPLATE|.github/PULL_REQUEST_TEMPLATE.md]] | Template de PR com checklist de crossroad files e revisão |
| [.github/CODEOWNERS](.github/CODEOWNERS) | Política de code ownership para crossroad files |
| [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) | Templates de issue (config.yml, technical.md) |
| [.github/dependabot.yml](.github/dependabot.yml) | Configuração de atualização automática de dependências |
| [scripts/create-curriculum-issues.sh](scripts/create-curriculum-issues.sh) | Script de automação de criação de issues do currículo |

> **Nota**: O PR template referencia crossroad files (`src/lib/safe-console.js`, `src/lib/logger.js`, etc.) e `docs/guides/crossroad-change-policy.md` que ainda não existem no repositório. Esses arquivos devem ser criados quando houver código fonte.

### Testes e QA

Topicos cobertos: `testes-qa`.

| Fonte | Cobre |
|---|---|
| [[docs/canonical/skill-testing-conventions|Skill Testing Conventions]] | Framework de test harness para skills |
| [[docs/canonical/measured-harness-evolution-lifecycle|Measured Harness Evolution Lifecycle]] | Ciclo de vida BUILD → STABILIZE → SIMPLIFY → REMOVE |

## Decisões de arquitetura (ADRs)

`docs/decisions/`:

| ADR | Status | Data |
|-----|--------|------|
| [[docs/decisions/2026-06-24-skill-canons-bridge-implementation|Skill-Canons Bridge — Decisões de Implementação (Ondas 0-2)]] | accepted | 2026-06-24 |

Tópicos candidatos a ADR:
- Escolha de stack do portal (vanilla JS estático vs. framework)
- Modelo de content chunking e carregamento sob demanda
- Estratégia de persistência de estado entre agentes
- Política de versionamento do currículo

## Documentação canônica pendente

`docs/canonical/` não está mais vazio. Há ~116 padrões canônicos ativos.

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
| `behavioral-eval-path-analysis.md` | Layer 3 da arquitetura de avaliação: detecção de duplicatas, loops, uso incorreto de ferramentas e atribuição de custo em traces de execução de agentes |
| `pr-gated-eval-enforcement.md` | Enforcement de evals no fluxo de PR e merge |
| `production-failure-regression-flywheel.md` | Flywheel de regressão para falhas de produção |
| `eval-to-production-correlation-tracking.md` | Rastreamento de correlação entre score de eval e outcomes de produção |
| `closed-loop-agent-operating-system.md` | Sistema operacional de loop fechado para agentes long-running |
| `skill-resolver-skillify-capability-pipeline.md` | Pipeline de capacidade do workflow ao skill resolvível e testado |
| `resolver-based-context-progressive-disclosure.md` | Disclosure de contexto progressivo guiado por resolver |
| `split-brain-planning-review.md` | Revisão de planejamento com rubricas separadas de engenharia e destino |
| `multi-model-evaluation-council.md` | Conselho de avaliação com múltiplos modelos e política de divergência |
| `epistemic-memory-graph.md` | Grafo de memória com status epistêmico e proveniência. Implementado 2026-06-19 em `obsidian-eval/src/`. |
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
| `asymmetric-binary-outcome-positioning.md` | Posicionamento binário assimétrico: quatro etapas para precificar eventos de resultado binário modelando probabilidade real vs. implícita, convexidade negativa e risco de ruína em sequência |
| `qa-to-backlog-feedback-loop.md` | Achados de QA/review como entrada de backlog com captura, triagem e conversão em issues |
| `llm-as-fuzzy-compiler.md` | LLM como compilador fuzzy: código como artefato de build descartável, separação entre prompt e output |
| `persona-based-documentation.md` | Documentação baseada em personas: NFRs e documentos por especialidade (dev, QA, architect, manager) |
| `garbage-collection-day-meta-loop.md` | Meta-loop semanal de limpeza de harness: revisão de slop, guardrails e cadência de manutenção |
| `failure-pattern-classification-loop.md` | Loop de classificação de padrões de falha: categorização de slop e misbehavior de agentes |
| `manual-brake-question-gate.md` | Gate de pergunta-freio manual: intervenção humana obrigatória antes de ações irreversíveis do agente |
| `deferred-ledger-agentic-work.md` | Ledger de trabalho agentic diferido: rastreamento explícito de dívida técnica com sunset gates |
| `owner-of-no-role-design.md` | Design pattern Owner of No Role: cada artefato tem exatamente um dono, papéis são explícitos e não ambíguos |
| `accidental-brake-replacement.md` | Anti-padrão de substituição acidental de freios: como gates de segurança são removidos silenciosamente |
| `value-gated-agent-control-loop.md` | Loop de controle do agente com gates de valor: o agente só avança quando o valor incremental é validado |
| `carry-debt-sunset-gate.md` | Gate de sunset para dívida carregada: prazo máximo para resolver débitos antes que bloqueiem o pipeline |
| `intent-five-part-primitive.md` | Intenção decomposta em cinco partes primitivas: goal, context, constraints, verification, handoff |
| `presence-in-the-loop-metric.md` | Métrica de presença-no-loop: calibração do grau de intervenção humana necessária por tarefa |
| `ice-craft-separation.md` | ICE Craft Separation: separação entre intenção (ICE) e execução artesanal (craft) no workflow agentic |
| `human-owned-expectations-boundary.md` | Fronteira de expectativas de propriedade humana: delimitação explícita do que o humano mantém sob seu controle |
| `institutional-layer-amplification.md` | Amplificação institucional em camadas: gaps regulatórios que se ampliam a cada nível (lei → jurisprudência → advocacia), destruindo previsibilidade para alocadores de capital que analisam apenas a lei formal |
| `second-order-institutional-interaction.md` | Interação institucional de segunda ordem: duas reformas analisadas isoladamente que, combinadas, invertem a estrutura de poder pretendida e criam vantagens compostas não antecipadas |
| `institutional-safety-valve-escalation-cycle.md` | Ciclo de escalada da válvula de segurança institucional: intervenções de emergência de um ramo para conter outro resolvem crises imediatas mas erodem legitimidade e amplificam conflito a cada ciclo |
| `credibility-cascade-regulated-assets.md` | Cascata de credibilidade em ativos regulados: falhas sequenciais de credibilidade (restatement → auditor → rating → venda forçada) que descolam o preço de mercado do valor intrínseco, criando oportunidades assimétricas em ativos fundamentalmente sólidos |
| `token-economics-gap-filling.md` | Economia de tokens do preenchimento de lacunas: custo de inferência vs. custo de especificação |
| `symphony-trap-awareness.md` | Consciência da armadilha da sinfonia: risco de over-specification e perda de adaptabilidade em sistemas agentic |
| `shadow-review-pipeline.md` | Pipeline de shadow review: agente shadow executa revisão paralela antes do merge |
| `contextual-severity-calibration.md` | Calibração contextual de severidade: ajuste de severidade baseado no contexto do código revisado |
| `review-contract-checklist.md` | Checklist de contrato de review: itens verificáveis obrigatórios em toda revisão de código |
| `pre-commit-ai-review-gate.md` | Gate de AI review pré-commit: validação automática por agente antes do commit |
| `compartmented-evaluation-architecture.md` | Arquitetura de avaliação compartimentada com separação de responsabilidades entre componentes |
| `three-part-intent-contract.md` | Contrato de intenção em três partes: goal, scenario, destination |
| `scenario-destination-split.md` | Separação entre cenário (contexto de execução) e destino (resultado esperado) |
| `two-implementations-goal-test.md` | Teste de duas implementações para validar se o goal está corretamente especificado |
| `goal-atomicity-split.md` | Decomposição de goals complexos em unidades atômicas verificáveis |
| `constraint-budget-gate.md` | Gate de orçamento de constraints: limite explícito de constraints por tarefa |
| `constraint-failure-decision-rule.md` | Regra de decisão para falha de constraint: degrade, retry ou escalate |
| `quarto-publishing-architecture.md` | Arquitetura de publicação Quarto: contrato config-driven, source bridge notebook/Markdown, multi-format fan-out |
| `quarto-authoring-workflow.md` | Fluxo de autoria Quarto: live preview loop, dependency-gated build, single-command deploy, push-to-publish CI/CD |
| `quarto-content-structure.md` | Estrutura de conteúdo Quarto: parts-based chapter organization, landing page como orientação do leitor |
| `on-policy-rollout-feedback-loop.md` | Loop de feedback on-policy com rollout e correção contínua professor→estudante |
| `autonomy-curriculum-sampling.md` | Amostragem curricular progressiva (observe→assist→own) para autonomia do modelo estudante |
| `privileged-context-self-distillation.md` | Self-distillation com contexto privilegiado para transferência de raciocínio professor→estudante |
| `consensus-gated-privileged-information.md` | Gate de consenso entre múltiplos avaliadores para filtrar informações privilegiadas |
| `asymmetric-failure-correction-router.md` | Roteador assimétrico que separa correção de falhas de reforço de sucessos |
| `magnitude-direction-verifier-split.md` | Separação magnitude/direção em verificadores para avaliação mais precisa e grounded |
| `adaptive-style-compression-teacher.md` | Professor adaptativo de compressão de estilo que ajusta dificuldade por exemplo para preservar qualidade |
| `cross-context-knowledge-siloing.md` | Conhecimento criado em um contexto de agente (namespace de repo, corpo de handoff) que se torna invisível para agentes em outro contexto — dois sub-padrões: isolamento por namespace e soterramento em corpo não indexado |
| `tiered-context-storage.md` | Armazenamento de contexto em três camadas (hot/warm/cold) com promoção e demissão dinâmica baseada em relevância |
| `neutral-selection-layer.md` | Camada de seleção de contexto model-agnostic e vendor-independent: formato portável, router multi-tenant, adaptador por modelo |
| `selection-budgeted-retrieval.md` | Retrieval com budget awareness: ranking de candidatos por valor/custo, feedback loop de utilidade, prevenção do loop de memória inerte |
| `deliberate-forgetting.md` | Esquecimento intencional como operação de primeira classe: avaliador de relevância, motor de promoção/demissão, log de descarte com rationale |
| `smallest-sufficient-context.md` | Contexto mínimo suficiente: estimador de suficiência, travessia relacional, montagem order-preserving, capacity profiler |
| `relational-context-graph.md` | Grafo de contexto relacional com arestas tipadas (dependência, proveniência, suplantação, causação) que transforma retrieval em seleção |
| `context-health-monitoring.md` | Monitoramento de saúde do contexto além de tokens: tamanho efetivo, taxa de near-misses, taxa de contradições, score agregado |
| `agent-degradation-loop-prevention.md` | Prevenção do loop de degradação de 4 elos: interceptores por elo, classificação diagnóstica, orquestração cross-link |
| `energy-value-chain-spread-analysis.md` | Modelo de análise de spread em cadeias de valor multi-camada (MWh→tokens→inferência) |
| `inelastic-market-flow-dominance-model.md` | Modelo de dominância de fluxo em mercados inelásticos (elasticidade ~0.2) |
| `social-archetype-classification.md` | Taxonomia de arquétipos sociais: Criação, Abundância, Predação |
| `spread-capture-analytical-primitive.md` | Primitiva analítica: substituir "qual o valor?" por "quem captura o spread?" |
| `capex-revenue-credit-mispricing.md` | Mispricing de crédito quando obsolescência tecnológica supera depreciação contábil |
| `eval-dashboard-primary-detection-surface.md` | Dashboard de qualidade como superfície primária de detecção: pass/fail rates por layer/categoria/agente em tempo real, anomaly alerts calibrados por regressão de qualidade, drill-down para trace individual |
| `multi-agent-fault-tolerance.md` | Tolerância a falhas multi-agente: Saga pattern (compensating transactions), Circuit Breaker na camada de orquestração, escalação humana com contexto completo, contrato de orquestração por step |
| `agent-specific-data-freshness-pipeline.md` | Pipeline de frescor de dados para agentes: garantias de frescor com SLAs, consistency checks antes da ingestão, staleness monitoring na camada de tracing, pipeline event-driven |
| `governance-context-injection-pii-prevention.md` | Prevenção de PII via injeção de governance context: data catalog PII tagging, injeção before-generation, post-generation deterministic scan como safety net, audit record por query |
| `business-outcome-first-eval-pipeline.md` | Pipeline de eval ancorado em business outcomes: define success em termos de negócio → golden answers de domain experts → Python pipeline comparativo, deflection rate prediction |
| `model-switching-architecture-enterprise-eval-gate.md` | Arquitetura de model-switching com enterprise eval gate: dataset de eval independente de provider, side-by-side comparison infrastructure, switch/hold/hybrid decision framework, continuous eval monitoring |
| `3-layer-evaluation-architecture.md` | Arquitetura de avaliação em 3 camadas por tipo de mecanismo: Deterministic (regex/schema/PII, custo zero), Semantic (LLM-as-Judge, groundedness/safety/faithfulness), Behavioral (trace path analysis, redundancy/loop/efficiency/cost). Compõe generator-evaluator, constraint-anchored-evaluation, trace-instrumentation. |
| `eval-driven-development-timeline.md` | Timeline de desenvolvimento eval-first com model-selection-last: 6 semanas de infraestrutura de eval antes de qualquer experimentação com modelos. Modelo escolhido por desempenho no dataset de eval do domínio, não por benchmarks públicos. Complementa pain-signal-eval-progression-gate com o princípio de sequência. |
| `living-eval-dataset.md` | Dataset de eval com crescimento monotônico: cada incidente de produção adiciona um caso permanente. Categorização por domínio (security, auth, tool calls, knowledge retrieval, math/reasoning) com ownership model. Execução particionada (stratified CI → full merge → scheduled regression). Compõe production-failure-regression-flywheel + production-grounded-eval-sampling. |
| `centralized-cross-framework-tracing.md` | Camada de tracing centralizada com schema unificado para múltiplos agent frameworks. Per-framework adapter pattern, OpenTelemetry integration, text-to-SQL query interface, cross-framework performance comparison, trace sampling em escala enterprise. Extensão do trace-instrumentation de single-framework para multi-framework. |
| `prompt-as-code-causal-change-management.md` | Disciplina de commit causal para prompts: 3 perguntas obrigatórias (why changed, what failure caused it, what failure it addresses). Prompt rollback infrastructure via git revert. Audit trail ligando cada mudança de prompt a incident/regressão/feature. Pre-deploy eval gate quantificando impacto antes do deploy. |

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
| `2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis.md` | Extração de conhecimento não-óbvio da talk 12-Factor Agents |
| `2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis.yaml` | YAML com frameworks, padrões, lições operacionais |
| `2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-patterns.md` | 8 padrões agentic extraídos com 6 campos cada |
| `2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-patterns.yaml` | YAML com componentes e fluxo por padrão |
| `2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.md` | Classificação comparativa dos 8 padrões vs. repo |
| `2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-classification.yaml` | YAML com evidência por padrão |
| `2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-integration-roadmap.md` | Roadmap de integração dos padrões ao currículo |

### Análises comparativas (Eval Maturity Phases)

| Arquivo | Cobre |
|---|---|
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis.md` | Framework de maturidade de evals e sinais de transição |
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-analysis.yaml` | YAML com framework, fases e sinais |
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-patterns.md` | Padrões operacionais extraídos da maturidade de evals |
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-patterns.yaml` | YAML com padrões operacionais |
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.md` | Classificação das lacunas e coberturas do repositório |
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-classification.yaml` | YAML com evidências e lacunas |
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-mental-model.md` | Modelo mental e precedência da análise |
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-mental-model.yaml` | YAML do modelo mental |
| `2026-06-10-eval-maturity-phases/2026-06-10-eval-maturity-phases-integration-roadmap.md` | Roadmap de integração dos padrões ao currículo |

### Análises comparativas (Stanford CS153 AI Native Company)

| Arquivo | Cobre |
|---|---|
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis.md` | Extração de conhecimento não-óbvio da fonte Stanford CS153 |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-analysis.yaml` | YAML com a extração estruturada |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns.md` | Catálogo dos 11 padrões agentic extraídos |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-patterns.yaml` | YAML com o catálogo de padrões |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification.md` | Classificação dos 11 padrões contra o repositório |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-classification.yaml` | YAML com a classificação estruturada |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-mental-model.md` | Modelo mental de orientação do pacote |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-mental-model.yaml` | YAML do modelo mental |
| `2026-06-10-stanford-cs153-ai-native-company-1000x-engineer/2026-06-10-stanford-cs153-ai-native-company-1000x-engineer-integration-roadmap.md` | Mapa de integração dos padrões classificados nas superfícies do repositório |

### Análises comparativas (Matt Pocock AI Coding Workflow)

| Arquivo | Cobre |
|---|---|
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-mental-model.md` | Modelo mental do repositório long-running-agents |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-mental-model.yaml` | YAML do modelo mental |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis.md` | Extração de conhecimento não-óbvio: frameworks, patterns, tradeoffs, failure patterns |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-analysis.yaml` | YAML com extração estruturada |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns.md` | 15 padrões agentic extraídos com 6 campos cada |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-patterns.yaml` | YAML com componentes e fluxo por padrão |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification.md` | Classificação comparativa: 1 Better Impl, 12 Partial, 2 Exists |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-classification.yaml` | YAML com evidência file:line por padrão |
| `2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock/2026-06-07-full-walkthrough-workflow-for-ai-coding-matt-pocock-integration-roadmap.md` | Roadmap de integração com 5 fases sequenciais e 12 canonical docs |

### Análises comparativas (IDSD Method — Intent-Driven Specification Development)

| Arquivo | Cobre |
|---|---|
| `2026-06-12-idsd-method/` | Pacote de análise do método IDSD: especificação via intenção decomposta em cinco primitivas |

### Análises comparativas (Memory Selection Problem)

| Arquivo | Cobre |
|---|---|
| `2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis.md` | Extração de frameworks (4-link degradation loop, selection vs. capacity axis shift) |
| `2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-analysis.yaml` | YAML com frameworks, lições operacionais, tradeoffs, failure patterns |
| `2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns.md` | 8 padrões agentic extraídos com 6 campos cada |
| `2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-patterns.yaml` | YAML com componentes e fluxo por padrão |
| `2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification.md` | Classificação comparativa: 3 Missing (P0), 5 Partial Coverage High (P1) |
| `2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-classification.yaml` | YAML com evidência file:line e missing mechanics por padrão |
| `2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-mental-model.md` | Modelo mental: selection vs. capacity, similarity is not relevance, effective context |
| `2026-06-18-memory-selection-problem/2026-06-18-memory-selection-problem-mental-model.yaml` | YAML do modelo mental |

> **Nota sobre formato**: Sessões de análise anteriores a 2026-06-14 contêm
> `integration-roadmap.md` (formato legacy). Sessões a partir de 2026-06-14 usam
> `<date>-<source-slug>-artifacts.{md,yaml}` como artifacts manifest.
> Ambos os formatos servem ao mesmo propósito: rastreabilidade classificação →
> artefatos → integração. Consulte o [[.opencode/skills/analyze-and-improve/SKILL.md|analyze-and-improve SKILL.md]]
> para o contrato atual.

## Planos

- [[docs/plans/2026-05-26-curriculum-completion-strategy|docs/plans/2026-05-26-curriculum-completion-strategy.md]] — estratégia de execução para completar o currículo via GitHub Issues/Milestones

---

*Última atualização: 2026-06-26*
