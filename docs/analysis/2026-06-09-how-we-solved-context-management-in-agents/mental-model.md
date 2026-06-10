# Mental Model: long-running-agents

**Date:** 2026-06-09  
**Repo:** `long-running-agents`  
**Type:** `mental-model`  
**Scope:** leitura do repositório alvo antes de analisar qualquer documento externo.

## 1. Project Goals

O repositório tem dois centros de gravidade. O primeiro é construir e gerir workflows de agentes de IA long-running, com `.opencode/` como sistema de agentes e skills, Node >= 20.18.0 como stack, e `.runtime/`/`artifacts/` como estado de runtime (`AGENTS.md:5`, `AGENTS.md:7`, `AGENTS.md:9`, `AGENTS.md:10`, `AGENTS.md:11`; `README.md:1`, `README.md:3`, `README.md:27`). O segundo é ensinar esse domínio por meio de um currículo de 12 semanas para KODA, um agente de venda de suplementos via WhatsApp que precisa manter qualidade em conversas de 2+ horas (`docs/system-of-record.md:39`, `docs/system-of-record.md:41`; `curriculum/README.md:9`, `curriculum/README.md:11`, `curriculum/README.md:25`, `curriculum/README.md:26`).

- Ensinar harnesses que gerenciam memória/contexto, decompõem trabalho e separam geração de avaliação (`curriculum/README.md:19`, `curriculum/README.md:20`, `curriculum/README.md:21`, `curriculum/README.md:22`, `curriculum/README.md:23`).
- Organizar um programa completo com 4 níveis, 8 conceitos core e 35+ diagramas (`curriculum/README.md:5`, `curriculum/README.md:49`, `curriculum/README.md:119`, `curriculum/README.md:129`).
- Aplicar os padrões ao KODA, incluindo descoberta de produtos, pedidos, fulfillment e melhoria contínua (`curriculum/GLOSSARY.md:232`, `curriculum/GLOSSARY.md:235`, `curriculum/GLOSSARY.md:236`, `curriculum/GLOSSARY.md:237`, `curriculum/GLOSSARY.md:238`, `curriculum/GLOSSARY.md:241`).
- Operacionalizar trabalho de agentes por issues, worktrees, review por segundo agente, PR draft, merge confirmado e cleanup (`.opencode/skills/issue-start/SKILL.md:12`, `.opencode/skills/issue-start/SKILL.md:14`, `.opencode/skills/issue-review/SKILL.md:12`, `.opencode/skills/issue-review/SKILL.md:14`, `.opencode/skills/issue-finish/SKILL.md:12`, `.opencode/skills/issue-finish/SKILL.md:14`).
- Manter governança documental por precedência explícita: ADRs aceitos, docs canônicos ativos, evidências, análises, arquivo histórico, depois READMEs e resumos operacionais (`docs/system-of-record.md:5`, `docs/system-of-record.md:7`, `docs/system-of-record.md:8`, `docs/system-of-record.md:9`, `docs/system-of-record.md:10`, `docs/system-of-record.md:11`, `docs/system-of-record.md:12`).

## 2. Architecture

### Core abstractions

| Abstraction | Role in the repo | Sources |
|---|---|---|
| System of record | Resolve conflitos documentais e mapear domínios do projeto. | `docs/system-of-record.md:1`, `docs/system-of-record.md:3`, `docs/system-of-record.md:5` |
| Curriculum | Produto principal: programa de 12 semanas com níveis, conceitos, diagramas, guias, templates e case studies. | `docs/system-of-record.md:39`, `docs/system-of-record.md:41`, `docs/system-of-record.md:45`, `docs/system-of-record.md:60`; `curriculum/README.md:49` |
| Agent system | Camada `.opencode/` com definições de agentes e skills; segue HoP/Handoff Protocol com escopo fechado, dono e gates. | `AGENTS.md:9`; `docs/system-of-record.md:16`, `docs/system-of-record.md:18` |
| HoP agents | Orquestrador Rezek, init básico KODA e tester live WhatsApp. | `.opencode/agents/hop-orchestrator-rezek.md:21`, `.opencode/agents/koda-hop-init-basic.md:16`, `.opencode/agents/hop-live-whatsapp-tester.md:16` |
| Issue lifecycle | Setup seguro, review e finish de issues por branch/worktree isolado. | `.opencode/skills/issue-start/SKILL.md:24`, `.opencode/skills/issue-review/SKILL.md:24`, `.opencode/skills/issue-finish/SKILL.md:25` |
| Canonical patterns | Quatro padrões ativos com status canônico: deterministic dispatch, owned control loop, pause/resume state e error context hygiene. | `docs/system-of-record.md:115`, `docs/system-of-record.md:117`, `docs/system-of-record.md:121`, `docs/system-of-record.md:122`, `docs/system-of-record.md:123`, `docs/system-of-record.md:124`, `docs/system-of-record.md:125`, `docs/system-of-record.md:126` |
| Tooling/runtime | Projeto ESM com Node >=20.18.0, ESLint e scripts `lint`, `test:unit`, `test:integration`. | `package.json:4`, `package.json:5`, `package.json:6`, `package.json:8`, `package.json:9`, `package.json:11`, `package.json:12` |
| Static web portal | Artefatos HTML estáticos e proposta futura de SPA. | `docs/system-of-record.md:66`, `docs/system-of-record.md:68`, `docs/system-of-record.md:72`, `docs/system-of-record.md:75` |

### Relationships

- O system-of-record controla precedência: decisões aceitas em `docs/decisions/` superam docs canônicos, que superam evidências, análises, arquivo histórico e READMEs (`docs/system-of-record.md:5`, `docs/system-of-record.md:7`, `docs/system-of-record.md:8`, `docs/system-of-record.md:9`, `docs/system-of-record.md:10`, `docs/system-of-record.md:11`, `docs/system-of-record.md:12`).
- A skill `analyze-and-improve` modela o pipeline desta família de trabalho: primeiro constrói o mental model do repo, depois extrai conhecimento de fonte externa, padrões, classificação, melhorias e integração (`.opencode/skills/analyze-and-improve/SKILL.md:30`, `.opencode/skills/analyze-and-improve/SKILL.md:32`, `.opencode/skills/analyze-and-improve/SKILL.md:34`, `.opencode/skills/analyze-and-improve/SKILL.md:35`, `.opencode/skills/analyze-and-improve/SKILL.md:36`, `.opencode/skills/analyze-and-improve/SKILL.md:37`, `.opencode/skills/analyze-and-improve/SKILL.md:38`, `.opencode/skills/analyze-and-improve/SKILL.md:39`, `.opencode/skills/analyze-and-improve/SKILL.md:106`, `.opencode/skills/analyze-and-improve/SKILL.md:108`).
- Deterministic Tool Dispatch depende de structured output, habilita Owned Agent Control Loop, é fortalecido por Error Context Hygiene e se relaciona com micro-agent islands (`docs/canonical/deterministic-tool-dispatch.md:96`, `docs/canonical/deterministic-tool-dispatch.md:98`, `docs/canonical/deterministic-tool-dispatch.md:99`, `docs/canonical/deterministic-tool-dispatch.md:100`, `docs/canonical/deterministic-tool-dispatch.md:101`).
- Owned Agent Control Loop contém Deterministic Tool Dispatch, complementa micro-agent islands e se baseia em prompt/context builder (`docs/canonical/owned-agent-control-loop.md:117`, `docs/canonical/owned-agent-control-loop.md:119`, `docs/canonical/owned-agent-control-loop.md:120`, `docs/canonical/owned-agent-control-loop.md:121`, `docs/canonical/owned-agent-control-loop.md:122`).
- Serializable Pause/Resume State depende de context builder, complementa o loop de controle, fortalece micro-agent islands e contrasta com a abordagem de rebuild state do repo (`docs/canonical/serializable-pause-resume-state.md:124`, `docs/canonical/serializable-pause-resume-state.md:126`, `docs/canonical/serializable-pause-resume-state.md:127`, `docs/canonical/serializable-pause-resume-state.md:128`, `docs/canonical/serializable-pause-resume-state.md:129`).
- Error Context Hygiene depende de context builder, complementa o loop de controle e fortalece fallback/retry (`docs/canonical/error-context-hygiene.md:136`, `docs/canonical/error-context-hygiene.md:138`, `docs/canonical/error-context-hygiene.md:139`, `docs/canonical/error-context-hygiene.md:140`).
- O currículo fornece o modelo pedagógico; `.opencode/skills/` fornece o modelo operacional para transformar análise, issues e documentação em artefatos rastreáveis (`curriculum/README.md:231`, `curriculum/README.md:239`; `.opencode/skills/doc-coauthoring/SKILL.md:6`, `.opencode/skills/doc-coauthoring/SKILL.md:8`; `.opencode/skills/writing-plans/SKILL.md:6`, `.opencode/skills/writing-plans/SKILL.md:10`).

## 3. Patterns

| Pattern | Where defined | Maturity |
|---|---|---|
| Deterministic Tool Dispatch | `docs/canonical/deterministic-tool-dispatch.md:1` | Active canonical pattern, Partial Coverage because mechanics exist but the named reframe is missing (`docs/canonical/deterministic-tool-dispatch.md:3`, `docs/canonical/deterministic-tool-dispatch.md:4`, `docs/canonical/deterministic-tool-dispatch.md:6`, `docs/canonical/deterministic-tool-dispatch.md:69`). |
| Owned Agent Control Loop | `docs/canonical/owned-agent-control-loop.md:1` | Active canonical pattern, Partial Coverage because the 4-component decomposition and named intervention points are missing (`docs/canonical/owned-agent-control-loop.md:3`, `docs/canonical/owned-agent-control-loop.md:4`, `docs/canonical/owned-agent-control-loop.md:6`, `docs/canonical/owned-agent-control-loop.md:87`, `docs/canonical/owned-agent-control-loop.md:89`). |
| Serializable Pause/Resume State | `docs/canonical/serializable-pause-resume-state.md:1` | Active canonical pattern, Partial Coverage plus complementary opportunity because repo rebuilds state rather than serializing token-level pause/resume context (`docs/canonical/serializable-pause-resume-state.md:3`, `docs/canonical/serializable-pause-resume-state.md:4`, `docs/canonical/serializable-pause-resume-state.md:6`, `docs/canonical/serializable-pause-resume-state.md:50`, `docs/canonical/serializable-pause-resume-state.md:52`, `docs/canonical/serializable-pause-resume-state.md:109`, `docs/canonical/serializable-pause-resume-state.md:111`). |
| Error Context Hygiene | `docs/canonical/error-context-hygiene.md:1` and `.opencode/skills/error-context-hygiene/SKILL.md:1` | Active canonical pattern, but classified as Missing in repo implementation; skill defines the implementation workflow (`docs/canonical/error-context-hygiene.md:3`, `docs/canonical/error-context-hygiene.md:4`, `docs/canonical/error-context-hygiene.md:6`, `.opencode/skills/error-context-hygiene/SKILL.md:13`, `.opencode/skills/error-context-hygiene/SKILL.md:15`). |
| HoP issue lifecycle | `.opencode/skills/issue-start/SKILL.md:1`, `.opencode/skills/issue-review/SKILL.md:1`, `.opencode/skills/issue-finish/SKILL.md:1`, `.opencode/skills/issue-workflow/SKILL.md:1` | Operationally active as skills, but canonical `agent-lifecycle.md` is still pending (`docs/system-of-record.md:37`, `docs/system-of-record.md:128`, `docs/system-of-record.md:132`). |
| Agent ownership and queue coordination | `.opencode/skills/orchestrator/SKILL.md:1` | Active operational skill: agents are tracked by issue number and active work is marked with `agent:working` (`.opencode/skills/orchestrator/SKILL.md:12`, `.opencode/skills/orchestrator/SKILL.md:14`, `.opencode/skills/orchestrator/SKILL.md:16`, `.opencode/skills/orchestrator/SKILL.md:49`). |
| Issue refinement into sub-issues | `.opencode/skills/refine-issue/SKILL.md:1` | Active planning skill: decomposes high-level issues into single-file-focused sub-issues with dependencies and a verification gate (`.opencode/skills/refine-issue/SKILL.md:8`, `.opencode/skills/refine-issue/SKILL.md:10`, `.opencode/skills/refine-issue/SKILL.md:46`, `.opencode/skills/refine-issue/SKILL.md:48`, `.opencode/skills/refine-issue/SKILL.md:80`, `.opencode/skills/refine-issue/SKILL.md:82`). |
| Writing plans | `.opencode/skills/writing-plans/SKILL.md:1` | Active planning/documentation skill for multi-step implementation plans saved under `docs/plans/` (`.opencode/skills/writing-plans/SKILL.md:8`, `.opencode/skills/writing-plans/SKILL.md:10`, `.opencode/skills/writing-plans/SKILL.md:16`). |
| Doc co-authoring | `.opencode/skills/doc-coauthoring/SKILL.md:1` | Active documentation skill with context gathering, iterative structure, and reader testing (`.opencode/skills/doc-coauthoring/SKILL.md:6`, `.opencode/skills/doc-coauthoring/SKILL.md:8`, `.opencode/skills/doc-coauthoring/SKILL.md:20`, `.opencode/skills/doc-coauthoring/SKILL.md:21`, `.opencode/skills/doc-coauthoring/SKILL.md:22`). |
| Generator/Evaluator | `curriculum/GLOSSARY.md:160` and `curriculum/README.md:186` | Mature curriculum pattern taught at Level 2 and applied to KODA (`curriculum/GLOSSARY.md:160`, `curriculum/GLOSSARY.md:161`, `curriculum/GLOSSARY.md:172`, `curriculum/README.md:186`, `curriculum/README.md:190`). |
| Sprint Contracts and rubrics | `curriculum/GLOSSARY.md:95` and `curriculum/GLOSSARY.md:125` | Level 2 curriculum patterns for defining done and measurable subjective quality (`curriculum/GLOSSARY.md:95`, `curriculum/GLOSSARY.md:96`, `curriculum/GLOSSARY.md:125`, `curriculum/GLOSSARY.md:126`, `curriculum/README.md:191`, `curriculum/README.md:192`). |
| Multi-agent coordination | `curriculum/GLOSSARY.md:287` | Level 3 architecture pattern for Planner + Generator + Evaluator coordination (`curriculum/GLOSSARY.md:287`, `curriculum/GLOSSARY.md:288`, `curriculum/GLOSSARY.md:290`, `curriculum/README.md:201`, `curriculum/README.md:205`). |

## 4. Abstractions

| Term | Definition | Source |
|---|---|---|
| Agent | Entidade autônoma de IA que toma ações, usa ferramentas e executa tarefas em sequência. | `curriculum/GLOSSARY.md:9`, `curriculum/GLOSSARY.md:10` |
| Agent Loop | Ciclo input -> pensar -> agir -> receber resultado -> repetir. | `curriculum/GLOSSARY.md:20`, `curriculum/GLOSSARY.md:21` |
| Context Window | Total de tokens que o modelo processa por vez, tratado como memória imediata. | `curriculum/GLOSSARY.md:82`, `curriculum/GLOSSARY.md:83` |
| Context Rot | Degradação gradual de coerência conforme o agente avança na janela de contexto. | `curriculum/GLOSSARY.md:73`, `curriculum/GLOSSARY.md:74` |
| Harness | Infraestrutura e padrões que envolvem agentes para torná-los confiáveis por períodos longos. | `curriculum/GLOSSARY.md:197`, `curriculum/GLOSSARY.md:198` |
| Contract / Sprint Contract | Acordo entre generator e evaluator sobre o que pronto significa antes de começar. | `curriculum/GLOSSARY.md:95`, `curriculum/GLOSSARY.md:96` |
| Generator | Agente responsável por construir ou criar algo. | `curriculum/GLOSSARY.md:147`, `curriculum/GLOSSARY.md:148` |
| Evaluator | Agente separado que avalia e dá nota ao trabalho de um Generator. | `curriculum/GLOSSARY.md:109`, `curriculum/GLOSSARY.md:110` |
| Evaluation Rubric | Critérios mensuráveis para avaliar qualidade subjetiva. | `curriculum/GLOSSARY.md:125`, `curriculum/GLOSSARY.md:126` |
| Memory / State | Informações retidas entre operações, podendo ser short-term, long-term ou file-based. | `curriculum/GLOSSARY.md:260`, `curriculum/GLOSSARY.md:261`, `curriculum/GLOSSARY.md:263` |
| Multi-Agent System | Sistema com múltiplos agentes independentes que coordenam entre si. | `curriculum/GLOSSARY.md:287`, `curriculum/GLOSSARY.md:288` |
| Planner | Agente especializado em quebrar problema em etapas. | `curriculum/GLOSSARY.md:305`, `curriculum/GLOSSARY.md:306` |
| KODA | Agente conversacional de IA para venda de suplementos esportivos via WhatsApp. | `curriculum/GLOSSARY.md:232`, `curriculum/GLOSSARY.md:233` |
| Deterministic Tool Dispatch | Reframe de tool use como JSON + código determinístico testável. | `docs/canonical/deterministic-tool-dispatch.md:22`, `docs/canonical/deterministic-tool-dispatch.md:24`, `docs/canonical/deterministic-tool-dispatch.md:26` |
| Owned Agent Control Loop | Loop próprio com prompt, context builder, switch statement e loop explícito. | `docs/canonical/owned-agent-control-loop.md:20`, `docs/canonical/owned-agent-control-loop.md:22`, `docs/canonical/owned-agent-control-loop.md:24` |
| Serializable Pause/Resume State | Serialização do estado do agente para pausar e retomar long-running tools. | `docs/canonical/serializable-pause-resume-state.md:11`, `docs/canonical/serializable-pause-resume-state.md:13`, `docs/canonical/serializable-pause-resume-state.md:22`, `docs/canonical/serializable-pause-resume-state.md:24` |
| Error Context Hygiene | Curadoria do que o modelo vê sobre falhas, sem blind-append de erros. | `docs/canonical/error-context-hygiene.md:19`, `docs/canonical/error-context-hygiene.md:21`, `docs/canonical/error-context-hygiene.md:23` |
| Architecture Decision Record | Documento que registra decisão arquitetural, contexto e consequências. | `curriculum/GLOSSARY.md:40`, `curriculum/GLOSSARY.md:41` |

## 5. Curriculum Structure

O currículo é organizado em documentos mestres, conteúdo por nível, core concepts, knowledge graphs, implementation guides, templates, case studies e referências (`curriculum/README.md:49`, `curriculum/README.md:56`, `curriculum/README.md:63`, `curriculum/README.md:119`, `curriculum/README.md:129`, `curriculum/README.md:139`, `curriculum/README.md:147`, `curriculum/README.md:155`, `curriculum/README.md:162`). O plano de execução divide o programa em quatro fases: Fundação, Padrões, Arquitetura e Aplicação (`curriculum/EXECUTION_PLAN.md:28`, `curriculum/EXECUTION_PLAN.md:31`, `curriculum/EXECUTION_PLAN.md:36`, `curriculum/EXECUTION_PLAN.md:41`, `curriculum/EXECUTION_PLAN.md:46`).

| Level | Duration | Central question | Topics | Exercises |
|---|---|---|---|---|
| Level 1 - Fundamentals | 3-4h | Por que agentes falham em tarefas longas? | 3 problemas principais, context windows, token budgeting, harness basics. | 2 exercícios: History Windowing e Structured Output (`curriculum/README.md:172`, `curriculum/README.md:175`, `curriculum/README.md:176`, `curriculum/README.md:177`, `curriculum/README.md:178`; `curriculum/INDEX.md:93`, `curriculum/INDEX.md:94`, `curriculum/INDEX.md:95`; `curriculum/01-nivel-1-fundamentals/exercises/exercise-01-windowing.md:1`; `curriculum/01-nivel-1-fundamentals/exercises/exercise-02-structured-output.md:1`). |
| Level 2 - Practical Patterns | 6-8h | Como fazemos agentes mais confiáveis? | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading. | 4 exercícios no índice, incluindo Error Context Hygiene (`curriculum/README.md:186`, `curriculum/README.md:189`, `curriculum/README.md:190`, `curriculum/README.md:191`, `curriculum/README.md:192`, `curriculum/README.md:193`; `curriculum/INDEX.md:97`, `curriculum/INDEX.md:98`, `curriculum/INDEX.md:99`, `curriculum/INDEX.md:100`, `curriculum/INDEX.md:101`; `curriculum/02-nivel-2-practical-patterns/exercises/exercise-04-error-context-hygiene.md:1`, `curriculum/02-nivel-2-practical-patterns/exercises/exercise-04-error-context-hygiene.md:7`). |
| Level 3 - Advanced Architecture | 8-10h | Como construímos sistemas sofisticados? | Multi-agent systems, state persistence, file-based coordination, harness evolution. | 3 exercícios: multi-agent Planner/Generator/Evaluator, state persistence e harness evolution (`curriculum/README.md:201`, `curriculum/README.md:204`, `curriculum/README.md:205`, `curriculum/README.md:206`, `curriculum/README.md:207`, `curriculum/README.md:208`; `curriculum/INDEX.md:103`, `curriculum/INDEX.md:104`, `curriculum/INDEX.md:105`, `curriculum/INDEX.md:106`; `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-01.md:1`, `curriculum/03-nivel-3-advanced-architecture/exercises/exercise-01.md:7`). |
| Level 4 - KODA-specific | Continuous | Como aplicamos tudo em KODA? | Arquitetura KODA, customer journey flows, feature design patterns, real implementations. | 2 real-world exercises, incluindo feature de recomendação KODA com Generator/Evaluator (`curriculum/README.md:216`, `curriculum/README.md:219`, `curriculum/README.md:220`, `curriculum/README.md:221`, `curriculum/README.md:222`, `curriculum/README.md:223`; `curriculum/INDEX.md:108`, `curriculum/INDEX.md:109`, `curriculum/INDEX.md:110`; `curriculum/04-nivel-4-koda-specific/real-world-exercises/exercise-01.md:1`, `curriculum/04-nivel-4-koda-specific/real-world-exercises/exercise-01.md:7`). |

Core concepts:

1. Context Management (`curriculum/MASTER_PLAN.md:334`)
2. Planning vs. Execution (`curriculum/MASTER_PLAN.md:335`)
3. Generator/Evaluator (`curriculum/MASTER_PLAN.md:336`)
4. Sprint Contracts (`curriculum/MASTER_PLAN.md:337`)
5. State Persistence (`curriculum/MASTER_PLAN.md:338`)
6. Harness Evolution (`curriculum/MASTER_PLAN.md:339`)
7. Multi-Agent Coordination (`curriculum/MASTER_PLAN.md:340`)
8. Evaluation Rubrics (`curriculum/MASTER_PLAN.md:341`)

Cross-cutting materials:

- Knowledge graphs: ecosystem, KODA feature dependencies, learning progression, problem-solution mapping, plus detailed concept graphs (`curriculum/INDEX.md:128`, `curriculum/INDEX.md:132`, `curriculum/INDEX.md:133`, `curriculum/INDEX.md:134`, `curriculum/INDEX.md:135`, `curriculum/INDEX.md:136`).
- Templates: sprint contract, evaluation rubric, knowledge graph, ADR, progress tracker and learning rubric (`curriculum/INDEX.md:140`, `curriculum/INDEX.md:144`, `curriculum/INDEX.md:145`, `curriculum/INDEX.md:146`, `curriculum/INDEX.md:147`, `curriculum/INDEX.md:148`, `curriculum/INDEX.md:149`).
- Implementation guides: setup, team progression, harness checklist, rubrics, trace analysis and harness evolution (`curriculum/INDEX.md:153`, `curriculum/INDEX.md:157`, `curriculum/INDEX.md:158`, `curriculum/INDEX.md:159`, `curriculum/INDEX.md:160`, `curriculum/INDEX.md:161`, `curriculum/INDEX.md:162`).

## 6. Existing Gaps

| Gap | Where documented |
|---|---|
| Nenhum ADR formal foi registrado; `docs/decisions/` está vazio. | `docs/system-of-record.md:105`, `docs/system-of-record.md:107` |
| `docs/canonical/agent-lifecycle.md` ainda falta para descrever claim -> worktree -> implement -> review -> merge -> cleanup. | `docs/system-of-record.md:37`, `docs/system-of-record.md:128`, `docs/system-of-record.md:132` |
| `docs/canonical/curriculum-model.md` ainda falta para taxonomia de níveis, tipos de artefato e critérios de qualidade. | `docs/system-of-record.md:64`, `docs/system-of-record.md:128`, `docs/system-of-record.md:133` |
| `docs/canonical/portal-architecture.md` ainda falta enquanto a SPA proposta não for implementada. | `docs/system-of-record.md:77`, `docs/system-of-record.md:128`, `docs/system-of-record.md:134` |
| `docs/canonical/crossroad-change-policy.md` e crossroad files referenciados pelo PR template ainda não existem. | `docs/system-of-record.md:103`, `docs/system-of-record.md:128`, `docs/system-of-record.md:135` |
| Os agentes `.opencode` apontam para `docs/canonical/operations/`, `docs/canonical/product/` e `docs/canonical/architecture/`, mas estes diretórios não foram encontrados na leitura direta (`NOT_FOUND` em `/mnt/c/Users/pavan/long-running-agents/docs/canonical/operations`, `/mnt/c/Users/pavan/long-running-agents/docs/canonical/product`, `/mnt/c/Users/pavan/long-running-agents/docs/canonical/architecture`). | `.opencode/agents/koda-hop-init-basic.md:28`, `.opencode/agents/koda-hop-init-basic.md:32`, `.opencode/agents/koda-hop-init-basic.md:33`, `.opencode/agents/hop-live-whatsapp-tester.md:22`, `.opencode/agents/hop-live-whatsapp-tester.md:24`, `.opencode/agents/hop-live-whatsapp-tester.md:25`, `.opencode/agents/hop-live-whatsapp-tester.md:26`, `.opencode/agents/hop-live-whatsapp-tester.md:27`, `.opencode/agents/hop-live-whatsapp-tester.md:28` |
| Deterministic Tool Dispatch está em Partial Coverage porque a mecânica existe, mas o reframe e orientação de teste/auditoria ainda faltam. | `docs/canonical/deterministic-tool-dispatch.md:6`, `docs/canonical/deterministic-tool-dispatch.md:69`, `docs/canonical/deterministic-tool-dispatch.md:71`, `docs/canonical/deterministic-tool-dispatch.md:73`, `docs/canonical/deterministic-tool-dispatch.md:75`, `docs/canonical/deterministic-tool-dispatch.md:76` |
| Owned Agent Control Loop está em Partial Coverage porque falta decomposição em 4 componentes e hooks como `break`, `summarize` e `LM-as-judge`. | `docs/canonical/owned-agent-control-loop.md:6`, `docs/canonical/owned-agent-control-loop.md:87`, `docs/canonical/owned-agent-control-loop.md:89`, `docs/canonical/owned-agent-control-loop.md:91`, `docs/canonical/owned-agent-control-loop.md:96` |
| Serializable Pause/Resume State não oferece fidelidade token-level de mid-reasoning pause/resume; o repo reconstrói estado a cada turno. | `docs/canonical/serializable-pause-resume-state.md:6`, `docs/canonical/serializable-pause-resume-state.md:50`, `docs/canonical/serializable-pause-resume-state.md:52`, `docs/canonical/serializable-pause-resume-state.md:109`, `docs/canonical/serializable-pause-resume-state.md:111` |
| Error Context Hygiene é canônico, mas ainda marcado como Missing em mecanismo equivalente do repo. | `docs/canonical/error-context-hygiene.md:6`, `docs/canonical/error-context-hygiene.md:99`, `docs/canonical/error-context-hygiene.md:101`, `docs/canonical/error-context-hygiene.md:107` |
| O README/INDEX ainda marcam `FAQ.md` como em construção, mas `curriculum/FAQ.md` existe e declara status completo, indicando desatualização de índice. | `curriculum/README.md:61`, `curriculum/README.md:447`, `curriculum/INDEX.md:326`, `curriculum/FAQ.md:1`, `curriculum/FAQ.md:7` |
| Há inconsistência no inventário do Level 2: o `MASTER_PLAN.md` fala em 3 exercícios, enquanto README/INDEX incluem o quarto exercício de Error Context Hygiene. | `curriculum/MASTER_PLAN.md:198`, `curriculum/README.md:81`, `curriculum/README.md:85`, `curriculum/INDEX.md:97`, `curriculum/INDEX.md:101`, `curriculum/02-nivel-2-practical-patterns/exercises/exercise-04-error-context-hygiene.md:1` |
| O template de knowledge graph permite status IN PROGRESS durante desenvolvimento e contém exemplo com KODA flow pendente. | `curriculum/08-tools-templates/knowledge-graph-template.md:466`, `curriculum/08-tools-templates/knowledge-graph-template.md:492` |

## Synthesis

O mental model útil para este repositório é: `long-running-agents` é simultaneamente currículo, sistema operacional de agentes e laboratório de padrões canônicos. O currículo ensina conceitos de harness para KODA; `.opencode` transforma trabalho em ciclos rastreáveis de issue/review/finish; `docs/system-of-record.md` define a hierarquia de verdade; `docs/canonical/` cristaliza padrões maduros ou gaps importantes. As próximas fases de análise devem comparar qualquer fonte externa contra essas três camadas: currículo, operação `.opencode` e canônicos ativos.
