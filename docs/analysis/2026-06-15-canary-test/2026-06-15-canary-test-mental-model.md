---
title: "Mental Model: long-running-agents"
type: analysis
date: 2026-06-15
domain: canary-test
aliases: ["modelo mental long-running-agents", "canary mental model", "repo mental model"]
tags: [analise, agentes-orquestracao, curriculo-conteudo, mental-model]
last_updated: 2026-06-15
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[curriculum/MASTER_PLAN|Master Plan]]", "[[docs/canonical/application-owned-agent-control-plane|Application-Owned Agent Control Plane]]", "[[.opencode/skills/analyze-and-improve/SKILL|analyze-and-improve Skill]]"]
sources: []
---

# Mental Model: long-running-agents

**Date:** 2026-06-15  
**Repo:** `long-running-agents`  
**Type:** `mental-model`  
**Scope:** leitura do repositorio alvo antes de analisar qualquer documento externo.

## 1. Project Goals

O repositorio e uma base de conhecimento, um curriculo e uma camada operacional para construir agentes long-running confiaveis. A tese central e que agentes falham em execucoes longas por perda de contexto, planejamento fragil e autoavaliacao cega; a resposta do repo e ensinar e operacionalizar harnesses que gerenciam contexto, decompoem trabalho e separam geracao de avaliacao (`README.md:3`, `README.md:7`, `README.md:13`).

- Construir e gerir workflows de agentes long-running com `.opencode/` como sistema de agentes, Node >= 20.18.0/ESM como stack e `.runtime/`/`artifacts/` como superficies de estado runtime (`AGENTS.md:7`, `AGENTS.md:9`, `AGENTS.md:10`, `AGENTS.md:11`, `README.md:107`, `README.md:113`).
- Ensinar um programa curricular de 12 semanas, 4 niveis, 8 conceitos core e 35+ diagramas para pessoas de negocio e builders de sistemas agenticos (`README.md:15`, `README.md:17`, `curriculum/README.md:11`, `curriculum/README.md:13`).
- Aplicar os conceitos ao KODA, agente de venda de suplementos via WhatsApp que precisa manter qualidade em conversas de 2+ horas e que serve como caso real de producao (`curriculum/README.md:33`, `curriculum/README.md:34`, `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:144`, `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:159`).
- Manter governanca documental por precedencia explicita: ADRs aceitos, canonicos ativos, evidencias, analises, arquivo historico, depois READMEs e resumos operacionais (`docs/system-of-record.md:14`, `docs/system-of-record.md:21`, `AGENTS.md:64`, `AGENTS.md:75`).
- Transformar conhecimento externo em melhorias do repo por um pipeline repetivel: mental model, extracao, padroes, classificacao, artefatos, integracao e integracao curricular (`.opencode/skills/analyze-and-improve/SKILL.md:47`, `.opencode/skills/analyze-and-improve/SKILL.md:57`, `.opencode/skills/analyze-and-improve/SKILL.md:171`, `.opencode/skills/analyze-and-improve/SKILL.md:234`).

## 2. Architecture

### Core Abstractions

| Abstraction | Role in the repo | Evidence |
|---|---|---|
| System of Record | Fonte de verdade para precedencia documental, dominios do projeto e inventario de canonicos, agentes, curriculo, tooling e lacunas. | `docs/system-of-record.md:12`, `docs/system-of-record.md:14`, `docs/system-of-record.md:23` |
| Documentation Precedence | Resolve conflitos entre fontes: ADRs aceitos > canonicos ativos > evidencias > analises > arquivo > READMEs/resumos. | `docs/system-of-record.md:16`, `docs/system-of-record.md:21`, `AGENTS.md:64`, `AGENTS.md:75` |
| Canonical Pattern Catalog | Camada autoritativa de padroes de arquitetura agentic, com 55 padroes ativos listados no SOR. | `docs/system-of-record.md:133`, `docs/system-of-record.md:135`, `docs/system-of-record.md:137` |
| Curriculum | Produto principal: programa de 12 semanas, 4 niveis, 8 conceitos core, exercicios, solutions, KODA applications, knowledge graphs, guias, templates e case studies. | `docs/system-of-record.md:55`, `docs/system-of-record.md:80`, `curriculum/README.md:57`, `curriculum/README.md:181` |
| Agent System / HoP | `.opencode/` define agentes e skills seguindo HoP/Handoff Protocol com escopo, dono e gates de validacao. | `AGENTS.md:9`, `docs/system-of-record.md:25`, `docs/system-of-record.md:29`, `.opencode/skills/orchestrator/SKILL.md:12` |
| Issue Lifecycle | Ciclo claim -> branch/worktree -> execution brief -> validation -> draft PR -> second-agent review -> explicit merge -> cleanup. | `.opencode/skills/issue-start/SKILL.md:12`, `.opencode/skills/issue-start/SKILL.md:14`, `.opencode/skills/issue-review/SKILL.md:12`, `.opencode/skills/issue-review/SKILL.md:14`, `.opencode/skills/issue-finish/SKILL.md:12`, `.opencode/skills/issue-finish/SKILL.md:14` |
| Application-Owned Control Plane | Contrato que junta prompt versionado, context builder, action schema, dispatch deterministico, loop policy, estado persistente e gates de intervencao. | `docs/canonical/application-owned-agent-control-plane.md:27`, `docs/canonical/application-owned-agent-control-plane.md:29`, `docs/canonical/application-owned-agent-control-plane.md:66`, `docs/canonical/application-owned-agent-control-plane.md:75` |
| Context and Memory Stack | Pilha de prompt estavel, head-tail truncation, middle recuperavel, estado duravel, catalogo de memoria e ledger de tokens. | `docs/canonical/stable-harness-prompt.md:26`, `docs/canonical/stable-harness-prompt.md:41`, `docs/canonical/head-tail-context-truncation.md:26`, `docs/canonical/head-tail-context-truncation.md:39`, `docs/canonical/external-state-persistence.md:29`, `docs/canonical/external-state-persistence.md:57`, `docs/canonical/explicit-token-budget-ledger.md:28`, `docs/canonical/explicit-token-budget-ledger.md:88` |
| Eval and Regression Stack | Tiers fast/medium/deep, PR gates, regressao por falha de producao, spot-checks, amostragem de producao e escalacao humana. | `docs/canonical/eval-tier-stratification.md:20`, `docs/canonical/eval-tier-stratification.md:49`, `docs/canonical/tested-degradation-ladder.md:27`, `docs/canonical/tested-degradation-ladder.md:65` |
| KODA | Aplicacao concreta do curriculo: sistema multi-agente de vendas WhatsApp com oito agentes internos, SQLite/JSON checkpointing e pipeline discovery -> pedido -> fulfillment. | `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:144`, `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:159`, `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:161`, `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:173` |
| Tooling and Validation | Projeto Node ESM com scripts reais `lint`, `test:unit` e `test:integration`; gates devem vir do `package.json`, nao de comandos inventados. | `package.json:4`, `package.json:12`, `AGENTS.md:53`, `AGENTS.md:62` |

### Relationships

- `docs/system-of-record.md` governa todos os dominios: agentes/orquestracao, curriculo, portal web, stack/tooling, governanca, ADRs, canonicos, analises e planos (`docs/system-of-record.md:23`, `docs/system-of-record.md:295`).
- `AGENTS.md` e o SOR formam o contrato operacional: uma tarefa por sessao, mudanca minima, tocar apenas o necessario, verificar com gates reais, buscar antes de codar e seguir convenções Obsidian para docs (`AGENTS.md:14`, `AGENTS.md:32`, `AGENTS.md:53`, `AGENTS.md:107`, `AGENTS.md:120`, `AGENTS.md:238`).
- O curriculo traduz os padroes em progressao didatica: Nivel 1 diagnostica falhas estruturais, Nivel 2 ensina padroes praticos, Nivel 3 ensina arquitetura avancada, Nivel 4 aplica ao KODA (`curriculum/README.md:186`, `curriculum/README.md:243`, `curriculum/MASTER_PLAN.md:173`, `curriculum/MASTER_PLAN.md:262`).
- `.opencode` operacionaliza o trabalho: o `orchestrator` seleciona e prepara agentes sem implementar, `issue-start` cria worktree e brief, `issue-review` valida e abre PR, `issue-finish` mergeia apenas apos confirmacao explicita (`.opencode/skills/orchestrator/SKILL.md:12`, `.opencode/skills/orchestrator/SKILL.md:14`, `.opencode/skills/issue-start/SKILL.md:24`, `.opencode/skills/issue-review/SKILL.md:44`, `.opencode/skills/issue-finish/SKILL.md:18`).
- O control plane owned depende de `Owned Agent Control Loop` para os quatro componentes, de `Deterministic Tool Dispatch` para JSON -> handler e de `Stable Harness Prompt` para separar contrato estavel de payload reduzivel (`docs/canonical/application-owned-agent-control-plane.md:114`, `docs/canonical/application-owned-agent-control-plane.md:118`).
- A estrategia de contexto combina preservar contrato, manter head/tail, externalizar middle, persistir fatos, medir ledger de tokens e validar com N+1/late-failure evals (`docs/canonical/stable-harness-prompt.md:30`, `docs/canonical/head-tail-context-truncation.md:28`, `docs/canonical/external-state-persistence.md:31`, `docs/canonical/explicit-token-budget-ledger.md:48`, `docs/canonical/eval-tier-stratification.md:28`).
- O KODA e a superficie de prova: o curriculo descreve como os conceitos N1-N3 viram arquitetura de vendas WhatsApp com separation of concerns, state over memory, artifacts over promises, fail fast/recover gracefully e harness evolution (`curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:161`, `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:173`).

## 3. Patterns

| Pattern | Where defined | Maturity |
|---|---|---|
| Application-Owned Agent Control Plane | `docs/canonical/application-owned-agent-control-plane.md:11` | Active canonical; Partial Coverage porque unifica componentes antes espalhados e ainda chama lacunas de contrato unico e vocabulario de gates (`docs/canonical/application-owned-agent-control-plane.md:13`, `docs/canonical/application-owned-agent-control-plane.md:17`, `docs/canonical/application-owned-agent-control-plane.md:98`, `docs/canonical/application-owned-agent-control-plane.md:104`). |
| Owned Agent Control Loop | `docs/canonical/owned-agent-control-loop.md:10` | Active canonical; Partial Coverage porque o repo tem fundamento de harness, mas faltam decomposicao ensinada em quatro componentes e hooks nomeados no loop (`docs/canonical/owned-agent-control-loop.md:12`, `docs/canonical/owned-agent-control-loop.md:16`, `docs/canonical/owned-agent-control-loop.md:96`, `docs/canonical/owned-agent-control-loop.md:107`). |
| Deterministic Tool Dispatch | `docs/canonical/deterministic-tool-dispatch.md:10` | Active canonical; Partial Coverage porque a mecanica existe, mas faltavam nome pedagogico, testing guidance sem LLM e audit logging como reframe (`docs/canonical/deterministic-tool-dispatch.md:12`, `docs/canonical/deterministic-tool-dispatch.md:16`, `docs/canonical/deterministic-tool-dispatch.md:68`, `docs/canonical/deterministic-tool-dispatch.md:86`). |
| Structured Generation and Constraint Validation Circuit | `docs/canonical/structured-generation-constraint-validation-circuit.md:11` | Active canonical; Partial Coverage porque unifica shape validation, domain constraints, repair/rejection, risk flags, dispatch e audit em um circuito unico (`docs/canonical/structured-generation-constraint-validation-circuit.md:13`, `docs/canonical/structured-generation-constraint-validation-circuit.md:17`, `docs/canonical/structured-generation-constraint-validation-circuit.md:27`, `docs/canonical/structured-generation-constraint-validation-circuit.md:64`). |
| Versioned Durable Agent State | `docs/canonical/versioned-durable-agent-state.md:11` | Active canonical; Partial Coverage porque define schema version, writeback, reload, migration e audit trail como contrato de estado duravel ainda nao consolidado (`docs/canonical/versioned-durable-agent-state.md:13`, `docs/canonical/versioned-durable-agent-state.md:17`, `docs/canonical/versioned-durable-agent-state.md:29`, `docs/canonical/versioned-durable-agent-state.md:84`). |
| External State Persistence | `docs/canonical/external-state-persistence.md:11` | Active canonical; Partial Coverage porque varias pecas existem, mas faltava guarda-chuva nomeado para estado externo e politica de persistir vs. manter no contexto (`docs/canonical/external-state-persistence.md:13`, `docs/canonical/external-state-persistence.md:17`, `docs/canonical/external-state-persistence.md:78`, `docs/canonical/external-state-persistence.md:83`). |
| Stable Harness Prompt During Context Reduction | `docs/canonical/stable-harness-prompt.md:10` | Active canonical; Partial Coverage porque a separacao prompt/contexto e implicita, mas faltava invariavel canonica de prompt nao-reduzivel durante compaction (`docs/canonical/stable-harness-prompt.md:12`, `docs/canonical/stable-harness-prompt.md:16`, `docs/canonical/stable-harness-prompt.md:55`, `docs/canonical/stable-harness-prompt.md:64`). |
| Head-Tail Context Truncation with Recoverable Middle | `docs/canonical/head-tail-context-truncation.md:10` | Active canonical; Partial Coverage porque nomeia a politica de preservar head/tail e guardar middle recuperavel por handles (`docs/canonical/head-tail-context-truncation.md:12`, `docs/canonical/head-tail-context-truncation.md:16`, `docs/canonical/head-tail-context-truncation.md:26`, `docs/canonical/head-tail-context-truncation.md:61`). |
| Explicit Token Budget Ledger | `docs/canonical/explicit-token-budget-ledger.md:10` | Active canonical; Partial Coverage porque transforma token budgeting em ledger pre-call com custo fixo, custo reduzivel, reservas, saldo e acao de loop (`docs/canonical/explicit-token-budget-ledger.md:12`, `docs/canonical/explicit-token-budget-ledger.md:16`, `docs/canonical/explicit-token-budget-ledger.md:28`, `docs/canonical/explicit-token-budget-ledger.md:117`). |
| Eval Tier Stratification | `docs/canonical/eval-tier-stratification.md:10` | Active canonical; Partial Coverage porque o repo tem multiplos gates, mas faltava taxonomia explicita fast/medium/deep com metadados de runtime, custo, trigger, threshold, owner e escalacao (`docs/canonical/eval-tier-stratification.md:12`, `docs/canonical/eval-tier-stratification.md:16`, `docs/canonical/eval-tier-stratification.md:26`, `docs/canonical/eval-tier-stratification.md:72`). |
| Closed-Loop Agent Operating System | `docs/canonical/closed-loop-agent-operating-system.md:10` | Active canonical; Partial Coverage porque conecta state intake, priority synthesis, execution routing e feedback writeback em um OS de agentes (`docs/canonical/closed-loop-agent-operating-system.md:12`, `docs/canonical/closed-loop-agent-operating-system.md:16`, `docs/canonical/closed-loop-agent-operating-system.md:26`, `docs/canonical/closed-loop-agent-operating-system.md:68`). |
| Tested Degradation Ladder | `docs/canonical/tested-degradation-ladder.md:11` | Active canonical; Partial Coverage porque ordena classify -> retry -> safe fallback/hold -> human escalation -> outcome log/tests, mas ainda falta ladder contract completo (`docs/canonical/tested-degradation-ladder.md:13`, `docs/canonical/tested-degradation-ladder.md:17`, `docs/canonical/tested-degradation-ladder.md:27`, `docs/canonical/tested-degradation-ladder.md:85`). |
| Generator/Evaluator | `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:72` | Mature curriculum pattern: separa Generator e Evaluator para reduzir sycophancy, criar checkpoint critico e elevar qualidade do KODA (`curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:21`, `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:43`, `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:76`, `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:127`). |
| HoP Issue Lifecycle | `.opencode/skills/issue-start/SKILL.md:12`, `.opencode/skills/issue-review/SKILL.md:12`, `.opencode/skills/issue-finish/SKILL.md:12` | Operationally active as skills; canonical `agent-lifecycle.md` is still documented as pending (`docs/system-of-record.md:53`, `.opencode/skills/issue-start/SKILL.md:14`, `.opencode/skills/issue-review/SKILL.md:14`, `.opencode/skills/issue-finish/SKILL.md:14`). |
| Manual Brake / Owner-of-No / Deferred Ledger | `.opencode/skills/manual-brake-question-gate/SKILL.md:13`, `.opencode/skills/owner-of-no-role/SKILL.md:13`, `.opencode/skills/deferred-ledger-agentic-work/SKILL.md:13` | Active governance skills: value gate before build, explicit owner of refusal, and risk ledger for skill/dependence/carry debt (`.opencode/skills/manual-brake-question-gate/SKILL.md:15`, `.opencode/skills/manual-brake-question-gate/SKILL.md:21`, `.opencode/skills/owner-of-no-role/SKILL.md:15`, `.opencode/skills/owner-of-no-role/SKILL.md:21`, `.opencode/skills/deferred-ledger-agentic-work/SKILL.md:15`, `.opencode/skills/deferred-ledger-agentic-work/SKILL.md:21`). |
| Intent Five-Part Primitive | `.opencode/skills/intent-five-part-primitive/SKILL.md:13` | Active alignment skill that requires description, constraints, failure scenarios, success scenarios and connections before execution (`.opencode/skills/intent-five-part-primitive/SKILL.md:15`, `.opencode/skills/intent-five-part-primitive/SKILL.md:25`, `.opencode/skills/intent-five-part-primitive/SKILL.md:75`, `.opencode/skills/intent-five-part-primitive/SKILL.md:180`). |
| Persona-Based Documentation and LLM-as-Fuzzy-Compiler | `.opencode/skills/persona-based-documentation/SKILL.md:13`, `.opencode/skills/llm-as-fuzzy-compiler/SKILL.md:13` | Active documentation/design skills: split quality standards into persona NFRs and treat harness assets as compiler passes/source, generated code as build artifact (`.opencode/skills/persona-based-documentation/SKILL.md:15`, `.opencode/skills/persona-based-documentation/SKILL.md:20`, `.opencode/skills/llm-as-fuzzy-compiler/SKILL.md:15`, `.opencode/skills/llm-as-fuzzy-compiler/SKILL.md:21`). |

## 4. Abstractions

| Term | Definition | Source |
|---|---|---|
| Agent | Entidade autonoma baseada em LLM que toma acoes, usa ferramentas e executa tarefas em sequencia. | `curriculum/GLOSSARY.md:17`, `curriculum/GLOSSARY.md:24` |
| Agent Loop | Ciclo repetitivo input -> pensar -> acao -> resultado -> repetir. | `curriculum/GLOSSARY.md:28`, `curriculum/GLOSSARY.md:35` |
| Context Window | Numero total de tokens que um modelo processa por vez, usado como memoria imediata do agente. | `curriculum/GLOSSARY.md:97`, `curriculum/GLOSSARY.md:106` |
| Context Amnesia | Esquecimento de contexto anterior quando a conversa excede a janela util. | `curriculum/GLOSSARY.md:37`, `curriculum/GLOSSARY.md:44` |
| Context Rot | Perda gradual de coerencia conforme o agente avanca na janela de contexto. | `curriculum/GLOSSARY.md:88`, `curriculum/GLOSSARY.md:94` |
| Token Budget | Planejamento e controle do uso de tokens e espaco disponivel antes da proxima chamada. | `docs/canonical/explicit-token-budget-ledger.md:20`, `docs/canonical/explicit-token-budget-ledger.md:30` |
| Harness | Infraestrutura e padroes que envolvem agentes para torna-los confiaveis por periodos longos. | `curriculum/GLOSSARY.md:265`, `curriculum/GLOSSARY.md:278` |
| Harness Evolution | Processo de simplificar ou remover componentes de harness conforme modelos melhoram. | `curriculum/GLOSSARY.md:282`, `curriculum/GLOSSARY.md:294` |
| Generator | Agente responsavel por criar uma solucao sem tentar auto-validar o resultado final. | `curriculum/GLOSSARY.md:215`, `curriculum/GLOSSARY.md:224`, `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:108`, `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:119` |
| Evaluator | Agente separado que avalia criticamente uma solucao contra rubrica, checklist ou contrato. | `curriculum/GLOSSARY.md:131`, `curriculum/GLOSSARY.md:143`, `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:120`, `curriculum/02-nivel-2-practical-patterns/01-generator-evaluator-pattern.md:131` |
| Sprint Contract | Acordo previo entre generator e evaluator sobre o que pronto significa. | `curriculum/GLOSSARY.md:117`, `curriculum/GLOSSARY.md:125` |
| Evaluation Rubric | Criterios mensuraveis para avaliar qualidade subjetiva. | `curriculum/GLOSSARY.md:147`, `curriculum/GLOSSARY.md:163` |
| Memory / State | Informacoes retidas entre operacoes, incluindo short-term, long-term e file-based. | `curriculum/GLOSSARY.md:380`, `curriculum/GLOSSARY.md:390` |
| Multi-Agent System | Sistema com multiplos agentes coordenados, frequentemente Planner + Generator + Evaluator. | `curriculum/GLOSSARY.md:407`, `curriculum/GLOSSARY.md:419` |
| Planner | Agente especializado em quebrar problemas em etapas. | `curriculum/GLOSSARY.md:425`, `curriculum/GLOSSARY.md:439` |
| KODA | Agente conversacional de venda de suplementos via WhatsApp e caso de aplicacao do curriculo. | `curriculum/GLOSSARY.md:352`, `curriculum/GLOSSARY.md:363` |
| Deterministic Tool Dispatch | Modelo em que o LLM emite JSON e codigo deterministico faz parsing, roteamento, validacao, execucao e handling. | `docs/canonical/deterministic-tool-dispatch.md:20`, `docs/canonical/deterministic-tool-dispatch.md:36` |
| Application-Owned Control Plane | Contrato da aplicacao para prompt, contexto, action schema, dispatch, loop, estado e gates. | `docs/canonical/application-owned-agent-control-plane.md:27`, `docs/canonical/application-owned-agent-control-plane.md:75` |
| External State Persistence | Persistir fatos criticos fora da janela de contexto e recarrega-los em cada turno. | `docs/canonical/external-state-persistence.md:29`, `docs/canonical/external-state-persistence.md:64` |
| Stable Harness Prompt | Prompt do harness preservado, versionado e avaliado separadamente da reducao de payload. | `docs/canonical/stable-harness-prompt.md:26`, `docs/canonical/stable-harness-prompt.md:41` |
| Head-Tail Context Truncation | Politica que mantem head e tail no contexto ativo e move middle para memoria recuperavel. | `docs/canonical/head-tail-context-truncation.md:26`, `docs/canonical/head-tail-context-truncation.md:39` |
| Eval Tier | Taxonomia fast, medium e deep para decidir custo, trigger, threshold, owner e poder de bloqueio de evals. | `docs/canonical/eval-tier-stratification.md:26`, `docs/canonical/eval-tier-stratification.md:50` |
| Manual Brake | Tres perguntas de valor antes de construir: quem precisa, se ainda valeria com custo real, e quem e dono de dizer nao. | `.opencode/skills/manual-brake-question-gate/SKILL.md:13`, `.opencode/skills/manual-brake-question-gate/SKILL.md:21` |
| Intent Five-Part Primitive | Intent com cinco campos: descricao, constraints, cenarios de falha, cenarios de sucesso e conexoes. | `.opencode/skills/intent-five-part-primitive/SKILL.md:13`, `.opencode/skills/intent-five-part-primitive/SKILL.md:25` |

## 5. Curriculum Structure

O curriculo e organizado como leitura por perfil, nivel, conceito, exercicio, guia, template, case study e referencia. `curriculum/INDEX.md` oferece rotas por persona e por pergunta, enquanto `curriculum/MASTER_PLAN.md` define objetivos de 4, 8 e 12 semanas e criterios de conclusao por nivel (`curriculum/INDEX.md:15`, `curriculum/INDEX.md:80`, `curriculum/MASTER_PLAN.md:31`, `curriculum/MASTER_PLAN.md:47`).

| Level | Focus | Progression and outputs | Evidence |
|---|---|---|---|
| Nivel 1 - Fundamentals | Por que agentes falham: context amnesia, planning/execution collapse e autoavaliacao ruim. | 3-4h no plano mestre; inclui 3 lessons, 2 exercicios e aplicacao KODA. | `README.md:81`, `README.md:86`, `curriculum/MASTER_PLAN.md:173`, `curriculum/MASTER_PLAN.md:192`, `curriculum/QUICK_START.md:35`, `curriculum/QUICK_START.md:90` |
| Nivel 2 - Practical Patterns | Generator/Evaluator, Sprint Contracts, Rubric Design e Trace Reading. | 6-8h; inclui exercicios de generator/evaluator, contracts, rubrics, error hygiene e intent primitive, alem de aplicacao KODA. | `README.md:83`, `README.md:85`, `curriculum/MASTER_PLAN.md:196`, `curriculum/MASTER_PLAN.md:215`, `curriculum/INDEX.md:105`, `curriculum/INDEX.md:111` |
| Nivel 3 - Advanced Architecture | Multi-agent systems, state persistence, file-based coordination, server-side compaction e harness evolution. | 8-10h; exercicios de design 3-agent, state persistence, harness evolution, LLM fuzzy compiler, persona docs, presence metric e Owner-of-No. | `README.md:84`, `README.md:86`, `curriculum/MASTER_PLAN.md:219`, `curriculum/MASTER_PLAN.md:238`, `curriculum/INDEX.md:112`, `curriculum/INDEX.md:120` |
| Nivel 4 - KODA-specific | Arquitetura KODA, customer journeys, feature design patterns, rubrics KODA, melhorias de harness e real-world exercises. | Continuo; semanas 7-12; foca aplicar tudo em producao, propor melhorias e implementar features. | `README.md:85`, `README.md:88`, `curriculum/MASTER_PLAN.md:242`, `curriculum/MASTER_PLAN.md:262`, `curriculum/EXECUTION_PLAN.md:238`, `curriculum/EXECUTION_PLAN.md:264` |

Core concepts:

1. Context Management (`curriculum/MASTER_PLAN.md:350`)
2. Planning vs. Execution (`curriculum/MASTER_PLAN.md:351`)
3. Generator/Evaluator (`curriculum/MASTER_PLAN.md:352`)
4. Sprint Contracts (`curriculum/MASTER_PLAN.md:353`)
5. State Persistence (`curriculum/MASTER_PLAN.md:354`)
6. Harness Evolution (`curriculum/MASTER_PLAN.md:355`)
7. Multi-Agent Coordination (`curriculum/MASTER_PLAN.md:356`)
8. Evaluation Rubrics (`curriculum/MASTER_PLAN.md:357`)

Cross-cutting curriculum surfaces:

- Knowledge graphs conectam os 8 conceitos em quatro dominios: Context & State, Planning, Verification e Architecture (`curriculum/06-knowledge-graphs/01-concept-ecosystem.md:128`, `curriculum/06-knowledge-graphs/01-concept-ecosystem.md:144`).
- Templates incluem sprint contract, evaluation rubric, knowledge graph, ADR, progress tracker e learning rubric (`curriculum/INDEX.md:155`, `curriculum/INDEX.md:164`).
- Implementation guides cobrem setup, progressao de equipe, harness checklist, rubrics, trace analysis e harness evolution (`curriculum/INDEX.md:168`, `curriculum/INDEX.md:177`).
- Case studies cobrem Retro Game Maker, Browser DAW e tres fluxos KODA: product discovery, order processing e fulfillment (`curriculum/INDEX.md:131`, `curriculum/INDEX.md:139`).
- Execution plan divide a jornada em Fundacao, Padroes, Arquitetura e Aplicacao nas semanas 1-12 (`curriculum/EXECUTION_PLAN.md:36`, `curriculum/EXECUTION_PLAN.md:59`).

## 6. Existing Gaps

| Gap | Where documented |
|---|---|
| `docs/decisions/` esta vazio; nenhum ADR formal foi registrado, apesar de ADRs terem precedencia maxima. | `docs/system-of-record.md:123`, `docs/system-of-record.md:132`; direct read of `docs/decisions/` showed only `.gitkeep`. |
| `docs/canonical/agent-lifecycle.md` esta pendente para descrever claim -> worktree -> implement -> review -> merge -> cleanup. | `docs/system-of-record.md:53`, `docs/system-of-record.md:206`, `docs/system-of-record.md:210` |
| `docs/canonical/curriculum-model.md` esta pendente para taxonomia de niveis, tipos de artefato e criterios de qualidade. | `docs/system-of-record.md:80`, `docs/system-of-record.md:206`, `docs/system-of-record.md:211` |
| `docs/canonical/portal-architecture.md` esta pendente enquanto a SPA proposta nao for implementada. | `docs/system-of-record.md:93`, `docs/system-of-record.md:206`, `docs/system-of-record.md:212` |
| `docs/canonical/crossroad-change-policy.md` e os crossroad files citados pelo PR template ainda nao existem; devem ser criados quando houver codigo fonte. | `docs/system-of-record.md:121`, `docs/system-of-record.md:206`, `docs/system-of-record.md:213` |
| Application-Owned Control Plane ainda aponta lacunas de contrato unico, ponte explicita entre componentes, estado persistente no loop e vocabulario unificado de gates. | `docs/canonical/application-owned-agent-control-plane.md:98`, `docs/canonical/application-owned-agent-control-plane.md:104` |
| External State Persistence ainda registra falta de politica unificada para que dados viram estado externo, tradeoffs vs. janelas maiores/summarization-only e conexao entre catalog, exact recovery, pause/resume e writeback. | `docs/canonical/external-state-persistence.md:78`, `docs/canonical/external-state-persistence.md:83` |
| Eval Tier Stratification ainda precisa de registry, metadados por suite, regra de selecao por tipo de mudanca, reporting para tiers pulados e processo de quarantine. | `docs/canonical/eval-tier-stratification.md:62`, `docs/canonical/eval-tier-stratification.md:72` |
| Tested Degradation Ladder ainda falta como ladder contract completo, classifier de falha, politica de fallback/hold, schema de outcome log e teste por rung antes de producao. | `docs/canonical/tested-degradation-ladder.md:79`, `docs/canonical/tested-degradation-ladder.md:85` |
| O SOR observa que o PR template referencia arquivos crossroad e guia de politica que ainda nao existem, um gap de governanca a resolver quando houver codigo fonte. | `docs/system-of-record.md:109`, `docs/system-of-record.md:121` |

## Synthesis

O modelo mental util e: `long-running-agents` opera em quatro camadas acopladas. A camada `docs/system-of-record.md` decide autoridade; `docs/canonical/` nomeia padroes e lacunas; `curriculum/` transforma esses padroes em progressao didatica aplicada ao KODA; `.opencode/` transforma o trabalho de agentes em lifecycle governado por issue, handoff, review, merge e cleanup. Qualquer analise futura deve comparar fontes externas contra essas quatro camadas, preservando a ordem de precedencia e os gaps ja documentados.
