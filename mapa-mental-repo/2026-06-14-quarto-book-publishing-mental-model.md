---
title: "Mental Model: Quarto Book Publishing Repository Context"
type: analysis
tags: ["agentes-orquestracao", "curriculo-conteudo", "harness-engineering", "context-engineering", "evals", "governanca", "decision-discipline"]
date: 2026-06-14
aliases: ["quarto book publishing mental model", "modelo mental quarto", "repository mental model", "phase 0 quarto", "long-running-agents mental model"]
last_updated: 2026-06-14
relates-to: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[AGENTS|AGENTS.md]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]", "[[curriculum/GLOSSARY|Glossary]]", "[[.opencode/skills/analyze-and-improve/SKILL|Analyze and Improve Skill]]", "[[docs/canonical/owned-agent-control-loop|Owned Agent Control Loop]]", "[[docs/canonical/eval-tier-stratification|Eval Tier Stratification]]", "[[docs/canonical/closed-loop-agent-operating-system|Closed-Loop Agent Operating System]]"]
sources: ["[[docs/system-of-record|System of Record]]", "[[README|Repository README]]", "[[AGENTS|AGENTS.md]]", "[[curriculum/README|Curriculum README]]", "[[curriculum/MASTER_PLAN|Curriculum Master Plan]]", "[[curriculum/GLOSSARY|Glossary]]"]
---
# Mental Model: long-running-agents

**Date:** 2026-06-14  
**Repo:** `long-running-agents`  
**Type:** `mental-model`  
**Scope:** leitura somente do repositório antes de analisar a fonte externa sobre Quarto. O `PROGRESS.md` desta análise declara Phase 0 como mental model em andamento e as demais fases como pendentes, então este artefato não usa a fonte externa (`docs/analysis/2026-06-14-quarto-book-publishing/PROGRESS.md:8-16`).

## 1. Project Goals

| Goal | Evidence |
|---|---|
| Manter uma base de conhecimento e programa curricular para construir sistemas de IA que operam por horas ou dias sem perder contexto, planejamento ou julgamento de qualidade. | `README.md:3-13` |
| Ensinar builders de negócio e sistemas agenticos, incluindo iniciantes e operadores em produção que buscam confiabilidade. | `README.md:15-18` |
| Tratar harnesses como resposta central para perda de contexto, planejamento frágil e autoavaliação cega. | `README.md:7-13`; `curriculum/README.md:21-34` |
| Entregar um currículo de 12 semanas, 4 níveis, 8 conceitos core e 35+ diagramas. | `curriculum/README.md:13`; `curriculum/README.md:251-270`; `curriculum/README.md:274-288` |
| Aplicar os padrões em KODA, agente de venda de suplementos via WhatsApp usado como caso real do currículo. | `README.md:26-30`; `curriculum/README.md:33-35`; `curriculum/GLOSSARY.md:416-427` |
| Operacionalizar trabalho agentic com `.opencode/`, Handoff Protocol, issue lifecycle, validation gates e documentação Obsidian. | `AGENTS.md:7-12`; `docs/system-of-record.md:25-58`; `.opencode/skills/issue-start/SKILL.md:12-15` |
| Processar fontes externas futuras via pipeline controlado: modelo mental do repo, extração, padrões, classificação, melhorias, integração e integração curricular. | `.opencode/skills/analyze-and-improve/SKILL.md:47-57`; `.opencode/skills/analyze-and-improve/SKILL.md:171-279` |

## 2. Architecture

### Core Abstractions

| Abstraction | Role | Evidence |
|---|---|---|
| System of Record | Fonte de verdade para precedência documental e mapa dos domínios do projeto. | `docs/system-of-record.md:12-21`; `docs/system-of-record.md:23-29` |
| Operational Contract | `AGENTS.md` define regras obrigatórias: uma tarefa por sessão, não assumir, mudança mínima, validação, segurança, busca antes de codar e convenções Obsidian. | `AGENTS.md:14-48`; `AGENTS.md:69-123`; `AGENTS.md:136-154`; `AGENTS.md:239-254` |
| Canonical Pattern Library | `docs/canonical/` é a camada autoritativa ativa para padrões de sistemas e contratos, abaixo apenas de ADRs aceitos. | `docs/system-of-record.md:14-21`; `docs/system-of-record.md:140-223` |
| Curriculum | Produto principal do repo: programa completo de 12 semanas aplicado a KODA, com níveis, exercícios, knowledge graphs, guias, templates e estudos de caso. | `docs/system-of-record.md:62-88`; `curriculum/README.md:13`; `curriculum/README.md:57-186` |
| KODA Case Domain | Domínio aplicado: sistema multi-agente de venda via WhatsApp com discovery, catálogo, recomendação, pedido, pagamento e fulfillment. | `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:144-159`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:313-327` |
| HoP Agent System | Camada `.opencode` com orquestrador primário, subagentes KODA e tester live; segue escopo fechado, dono e gates. | `docs/system-of-record.md:25-58`; `.opencode/agents/hop-orchestrator-rezek.md:21-39`; `.opencode/agents/koda-hop-init-basic.md:18-52`; `.opencode/agents/hop-live-whatsapp-tester.md:18-76` |
| Issue Lifecycle | Fluxo operacional claim -> worktree -> execution brief -> validation -> draft PR -> second-agent review -> explicit merge -> cleanup. | `.opencode/skills/issue-start/SKILL.md:12-15`; `.opencode/skills/issue-start/SKILL.md:24-171`; `.opencode/skills/issue-review/SKILL.md:12-15`; `.opencode/skills/issue-finish/SKILL.md:12-15` |
| Analyze-and-Improve Harness | Pipeline que transforma fonte externa em análise, padrões classificados, artefatos concretos e integração no repo. | `.opencode/skills/analyze-and-improve/SKILL.md:47-57`; `.opencode/skills/analyze-and-improve/SKILL.md:130-149`; `.opencode/skills/analyze-and-improve/SKILL.md:653-807` |
| Mental Model Cache | `mapa-mental-repo/` versiona modelos mentais por data e source slug para uso incremental. | `.opencode/skills/analyze-and-improve/SKILL.md:150-168`; `mapa-mental-repo/2026-06-12-idsd-method-mental-model.md:1-16` |
| Stack and Validation Tooling | Projeto Node ESM com Node >= 20.18.0, ESLint e scripts reais de lint/test; docs são validadas por script Obsidian. | `README.md:107-113`; `package.json:1-21`; `scripts/check-obsidian-conventions.sh:18-46`; `scripts/check-obsidian-conventions.sh:283-312` |

### Relationships

| From | To | Relationship | Evidence |
|---|---|---|---|
| System of Record | Documentation Surfaces | Conflitos documentais resolvem por ADRs aceitos, canonicals ativos, evidências, análises, arquivo e READMEs/resumos operacionais. | `docs/system-of-record.md:14-21`; `AGENTS.md:80-91` |
| Canonical Pattern Library | Curriculum | Canonicals formalizam padrões que o currículo ensina por níveis, conceitos, exercícios e aplicações KODA. | `docs/system-of-record.md:140-223`; `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| Curriculum | KODA Case Domain | O Nível 4 converte padrões gerais em arquitetura KODA, customer journeys, feature patterns, rubricas, melhorias e exercícios reais. | `curriculum/README.md:236-247`; `curriculum/MASTER_PLAN.md:251-270`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:89-101` |
| HoP Agent System | Issue Lifecycle | Skills e agentes transformam trabalho em sessões rastreáveis com issue, worktree, validação, PR, revisão e cleanup. | `docs/system-of-record.md:31-58`; `.opencode/skills/issue-start/SKILL.md:24-171`; `.opencode/skills/issue-review/SKILL.md:44-100`; `.opencode/skills/issue-finish/SKILL.md:50-84` |
| Orchestrator Skill | Worker Sessions | O orchestrator lista issues/PRs/worktrees, sugere próxima issue e gera prompt de worker que carrega `issue-start`, implementa, roda `issue-review` e só finaliza com `issue-finish`. | `.opencode/skills/orchestrator/SKILL.md:12-25`; `.opencode/skills/orchestrator/SKILL.md:27-62`; `.opencode/skills/orchestrator/SKILL.md:74-96` |
| Owned Agent Control Loop | Deterministic Tool Dispatch | O loop do agente é decomposto em Prompt, Context Builder, Switch Statement e Loop; o dispatch determinístico é o Switch Statement. | `docs/canonical/owned-agent-control-loop.md:29-75`; `docs/canonical/deterministic-tool-dispatch.md:31-67`; `docs/canonical/owned-agent-control-loop.md:126-131` |
| Serializable State | KODA State Persistence | O padrão canônico descreve serialização/rebuild de estado; KODA usa SQLite, JSON state files, locks e audit trail como camada de persistência. | `docs/canonical/serializable-pause-resume-state.md:31-76`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:259-269`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:303-309` |
| Eval Tier Stratification | PR and Release Gates | A taxonomia fast/medium/deep define quando uma suite bloqueia inner loop, PR ou rollout; `issue-review` exige gates reais e seleção de tier para mudanças eval-sensitive. | `docs/canonical/eval-tier-stratification.md:20-49`; `.opencode/skills/issue-review/SKILL.md:44-85` |
| Closed-Loop Agent OS | Analyze-and-Improve | O OS conecta intake de estado, síntese de prioridade, execução roteada e writeback; `analyze-and-improve` implementa um loop knowledge -> patterns -> classification -> improvements -> integration. | `docs/canonical/closed-loop-agent-operating-system.md:26-45`; `.opencode/skills/analyze-and-improve/SKILL.md:47-57` |

## 3. Patterns

A amostra abaixo cobre 7 padrões canônicos diversos, acima do mínimo de 5 solicitado. A maturidade usa os campos `Status` e `Classification` dos próprios docs canônicos.

| Pattern | Where Defined | Maturity | Mental Model |
|---|---|---|---|
| Owned Agent Control Loop | `docs/canonical/owned-agent-control-loop.md` | Active; Partial Coverage. | Padrão de ownership do loop com 4 componentes e pontos explícitos de intervenção; lacuna registrada é a decomposição de 4 componentes e hooks de intervenção. Evidence: `docs/canonical/owned-agent-control-loop.md:12-16`; `docs/canonical/owned-agent-control-loop.md:29-75`; `docs/canonical/owned-agent-control-loop.md:96-115`. |
| Deterministic Tool Dispatch | `docs/canonical/deterministic-tool-dispatch.md` | Active; Partial Coverage. | Ferramentas são JSON + código determinístico; o repo possui mecânica, mas precisa nomear o reframe, orientar testes sem LLM e reforçar audit logging. Evidence: `docs/canonical/deterministic-tool-dispatch.md:12-16`; `docs/canonical/deterministic-tool-dispatch.md:31-36`; `docs/canonical/deterministic-tool-dispatch.md:68-95`. |
| Error Context Hygiene | `docs/canonical/error-context-hygiene.md` | Active; Missing for equivalent repo mechanism. | Erros devem ser resumidos, não blind-appended; a skill operacional reforça resumir, limpar no sucesso, nunca despejar stack trace e manter só o necessário. Evidence: `docs/canonical/error-context-hygiene.md:12-16`; `docs/canonical/error-context-hygiene.md:28-40`; `.opencode/skills/error-context-hygiene/SKILL.md:13-20`. |
| Serializable Pause/Resume State | `docs/canonical/serializable-pause-resume-state.md` | Active; Partial Coverage. | O repo tem reconstrução rica de estado por camadas, mas o padrão aponta lacuna de pause/resume com fidelidade de token em mid-reasoning. Evidence: `docs/canonical/serializable-pause-resume-state.md:12-16`; `docs/canonical/serializable-pause-resume-state.md:59-76`; `docs/canonical/serializable-pause-resume-state.md:118-122`. |
| Addressable Memory Catalog | `docs/canonical/addressable-memory-catalog.md` | active; Partial Coverage. | Catálogo de memória omitida precisa de `id`, `kind`, `location`, `preview`, `scope` e `fetch`; lacuna é schema determinístico, contrato de fetch e observabilidade. Evidence: `docs/canonical/addressable-memory-catalog.md:12-16`; `docs/canonical/addressable-memory-catalog.md:26-43`; `docs/canonical/addressable-memory-catalog.md:57-66`. |
| Eval Tier Stratification | `docs/canonical/eval-tier-stratification.md` | active; Partial Coverage. | Evals são separados em fast, medium e deep com metadata de runtime, custo, flakiness, trigger, threshold, reporting e owner; faltam registry e política explícita. Evidence: `docs/canonical/eval-tier-stratification.md:12-16`; `docs/canonical/eval-tier-stratification.md:20-49`; `docs/canonical/eval-tier-stratification.md:51-72`. |
| Closed-Loop Agent Operating System | `docs/canonical/closed-loop-agent-operating-system.md` | active; Partial Coverage, High integration value. | Modelo operacional une state intake, priority synthesis, execution routing e feedback writeback; lacunas são modelo único, política de writeback e observabilidade de loop. Evidence: `docs/canonical/closed-loop-agent-operating-system.md:12-16`; `docs/canonical/closed-loop-agent-operating-system.md:26-45`; `docs/canonical/closed-loop-agent-operating-system.md:59-68`. |

## 4. Terminology

| Term | Definition | Source |
|---|---|---|
| Agent | Entidade autônoma de IA que toma ações, usa ferramentas e executa tarefas em sequência. | `curriculum/GLOSSARY.md:17-24` |
| Agent Loop | Ciclo repetitivo input -> pensamento -> ação -> resultado -> repetição. | `curriculum/GLOSSARY.md:28-35` |
| Context Amnesia | Esquecimento de contexto anterior por excesso da janela de contexto. | `curriculum/GLOSSARY.md:37-45` |
| Context Window | Total de tokens que um modelo processa de uma vez, equivalente à memória imediata. | `curriculum/GLOSSARY.md:145-154` |
| Context Progressive Disclosure | Arquitetura em que instruções/capacidades vivem em skills acionadas por resolver, não em prompt monolítico. | `curriculum/GLOSSARY.md:158-162` |
| Sprint Contract | Acordo prévio entre generator e evaluator sobre o que significa pronto. | `curriculum/GLOSSARY.md:165-174` |
| Evaluator | Agente separado responsável por avaliar o trabalho de um Generator contra rubrics. | `curriculum/GLOSSARY.md:179-191` |
| Evaluation Rubric | Critérios mensuráveis para avaliar qualidade subjetiva. | `curriculum/GLOSSARY.md:195-211` |
| Generator | Agente responsável por construir ou criar algo. | `curriculum/GLOSSARY.md:279-288` |
| Generator/Evaluator Pattern | Duas entidades separadas colaboram: uma gera, outra avalia. | `curriculum/GLOSSARY.md:292-310` |
| Harness | Infraestrutura e padrões que envolvem agentes para torná-los confiáveis em execuções longas. | `curriculum/GLOSSARY.md:329-342` |
| Harness Evolution | Processo de simplificar ou remover componentes de harness conforme o modelo melhora. | `curriculum/GLOSSARY.md:346-358` |
| Intent as Five-Part Primitive | Intent formalizada como description, constraints, failure scenarios, success scenarios e connections. | `curriculum/GLOSSARY.md:395-410` |
| KODA | Agente conversacional para venda de suplementos via WhatsApp e case study do programa. | `curriculum/GLOSSARY.md:416-427` |
| Memory / State | Informações retidas entre operações em short-term, long-term ou file-based storage. | `curriculum/GLOSSARY.md:444-454` |
| Multi-Agent System | Sistema com múltiplos agentes independentes, como Planner, Generator e Evaluator. | `curriculum/GLOSSARY.md:471-483` |
| Planner | Agente especializado em quebrar problemas em etapas. | `curriculum/GLOSSARY.md:489-503` |
| Self-Evaluation | Anti-padrão em que o agente avalia o próprio trabalho. | `curriculum/GLOSSARY.md:590-609` |
| Token Budget | Gerenciamento consciente de tokens usados e disponíveis. | `curriculum/GLOSSARY.md:686-696` |
| Trace | Log detalhado de input, reasoning, ações e output do agente. | `curriculum/GLOSSARY.md:717-732` |
| Verification Loop | Ciclo Generator -> Test -> Evaluator -> Feedback. | `curriculum/GLOSSARY.md:754-767` |

## 5. Curriculum Structure

### Levels

| Level | Focus | Duration | Artifacts | Source |
|---|---|---|---|---|
| Nível 1 - Fundamentos | Por que agentes falham: context windows, token budgeting e padrões básicos de harness. | 3-4 horas. | Lições de fundamentos, 2 exercícios, KODA applications e critério de mapear conceitos para KODA. | `curriculum/README.md:190-203`; `curriculum/MASTER_PLAN.md:184-202` |
| Nível 2 - Padrões Práticos | Generator/Evaluator, Sprint Contracts, Rubric Design e Trace Reading. | 6-8 horas. | 4 tópicos principais, exercícios, KODA applications e aplicação de padrões em código real. | `curriculum/README.md:206-218`; `curriculum/MASTER_PLAN.md:205-225` |
| Nível 3 - Arquitetura Avançada | Multi-agent systems, state persistence, file-based coordination, server-side compaction e harness evolution. | 8-10 horas. | 5 tópicos arquiteturais, exercícios avançados e suporte a decisões arquiteturais KODA. | `curriculum/README.md:221-233`; `curriculum/MASTER_PLAN.md:228-248` |
| Nível 4 - KODA-Específico | Arquitetura real KODA, customer journeys, feature patterns, rubrics KODA e melhorias de harness. | Contínuo, 10+ horas no Master Plan. | 5 módulos KODA, real-world exercises, case studies e participação em decisões arquiteturais. | `curriculum/README.md:236-248`; `curriculum/MASTER_PLAN.md:251-270` |

### Concepts

| Concept | Source |
|---|---|
| Context Management | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| Planning vs. Execution | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| Generator/Evaluator | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| Sprint Contracts | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| State Persistence | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| Harness Evolution | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| Multi-Agent Coordination | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |
| Evaluation Rubrics | `curriculum/README.md:251-270`; `curriculum/MASTER_PLAN.md:349-367` |

### Supporting Surfaces

| Surface | Role | Source |
|---|---|---|
| Knowledge graphs | Visualizam ecossistema, dependências KODA, progressão de aprendizado e mapping problema-solução. | `curriculum/README.md:149-158`; `curriculum/MASTER_PLAN.md:370-380` |
| Implementation guides | Cobrem setup, progressão de time, harness design checklist, rubrics, trace analysis e harness evolution playbook. | `curriculum/README.md:159-165`; `curriculum/MASTER_PLAN.md:383-393` |
| Tools and templates | Fornecem tracker, assessment rubric, knowledge graph template, sprint contract, evaluation rubric e ADR template. | `curriculum/README.md:167-173`; `curriculum/MASTER_PLAN.md:396-418` |
| Case studies | Incluem 2 casos gerais e 3 casos KODA com objetivo, arquitetura, estado, verificação e lições. | `curriculum/README.md:175-185`; `curriculum/MASTER_PLAN.md:422-440` |
| KODA architecture module | Ensina desenho completo, fluxo end-to-end, responsabilidades, WhatsApp API, pipeline de vendas, métricas e tradeoffs. | `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:89-101`; `curriculum/04-nivel-4-koda-specific/01-koda-architecture.md:104-138` |

## 6. Existing Gaps

| Gap | Where Documented |
|---|---|
| Nenhum ADR formal foi registrado em `docs/decisions/`; o diretório verificado contém só `.gitkeep`. | `docs/system-of-record.md:130-139`; directory inspection `docs/decisions/` -> `.gitkeep` only |
| ADRs candidatos ainda pendentes: stack do portal, content chunking, persistência de estado entre agentes e versionamento do currículo. | `docs/system-of-record.md:134-139` |
| `docs/canonical/agent-lifecycle.md` é pendente para o ciclo claim -> worktree -> implement -> review -> merge -> cleanup. | `docs/system-of-record.md:60`; `docs/system-of-record.md:224-232` |
| `docs/canonical/curriculum-model.md` é pendente para taxonomia de níveis, tipos de artefato e critérios de qualidade. | `docs/system-of-record.md:87`; `docs/system-of-record.md:224-232` |
| `docs/canonical/portal-architecture.md` é pendente quando a SPA proposta for implementada. | `docs/system-of-record.md:89-100`; `docs/system-of-record.md:224-232` |
| `docs/canonical/crossroad-change-policy.md` e arquivos crossroad citados pelo PR template ainda não existem e devem nascer quando houver código fonte. | `docs/system-of-record.md:116-129`; `docs/system-of-record.md:224-232` |
| README e SOR divergem sobre a escala da biblioteca canônica: README ainda fala em 16 padrões, enquanto o SOR declara 62 padrões ativos. | `README.md:53-60`; `README.md:90-105`; `docs/system-of-record.md:140-223` |
| `docs/evidence/` e `docs/archive/` estão na hierarquia de precedência, mas a inspeção atual mostra só `.gitkeep`. | `docs/system-of-record.md:14-21`; directory inspection `docs/evidence/` -> `.gitkeep` only; directory inspection `docs/archive/` -> `.gitkeep` only |
| `issue-review` menciona gates que não existem em `package.json`; os scripts reais atuais são `lint`, `lint:fix`, `test:unit` e `test:integration`. | `.opencode/skills/issue-review/SKILL.md:44-75`; `package.json:8-13` |
| Diretórios curriculares auxiliares ainda são placeholders ou quase vazios: `curriculum/04-nivel-4-koda-specific/exercises/` e `koda-applications/` contêm só `.gitkeep`. | directory inspection `curriculum/04-nivel-4-koda-specific/exercises/` -> `.gitkeep` only; directory inspection `curriculum/04-nivel-4-koda-specific/koda-applications/` -> `.gitkeep` only |
| A análise atual ainda está só na Phase 0; knowledge extraction, pattern extraction, classification, improvement generation, integration e curriculum deep integration permanecem pendentes. | `docs/analysis/2026-06-14-quarto-book-publishing/PROGRESS.md:8-16` |

## Synthesis

| Synthesis Claim | Evidence |
|---|---|
| O repo é melhor entendido como três camadas acopladas: currículo aplicado, biblioteca canônica de padrões e sistema operacional `.opencode` para trabalho agentic. | `README.md:32-77`; `docs/system-of-record.md:23-88`; `docs/system-of-record.md:140-223` |
| Qualquer análise externa posterior deve primeiro classificar novas ideias contra ADRs/canonicals, depois contra evidências/análises, e só então contra currículo e READMEs. | `docs/system-of-record.md:14-21`; `.opencode/skills/analyze-and-improve/SKILL.md:552-586` |
| Para a fonte Quarto, o próximo passo correto é manter este modelo como Phase 0 e só depois ler a fonte externa para extrair conhecimento. | `.opencode/skills/analyze-and-improve/SKILL.md:171-279`; `docs/analysis/2026-06-14-quarto-book-publishing/PROGRESS.md:8-16` |
