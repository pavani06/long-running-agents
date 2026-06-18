---
title: "Long-Running Agents — Repository Home"
type: index
aliases: ["readme", "home", "início", "sobre", "README"]
tags: [index, agentes-orquestracao, curriculo-conteudo, harness-engineering, governanca]
last_updated: 2026-06-17
relates-to: ["[[docs/system-of-record|System of Record]]", "[[index|Knowledge Index]]", "[[curriculum/README|Curriculum README]]", "[[AGENTS|Agent Rules]]"]
---

# long-running-agents

Base de conhecimento e programa curricular para construir sistemas de IA que operam de forma confiável por horas, dias ou pelo tempo que a tarefa exigir -- sem perder contexto, capacidade de planejamento ou julgamento de qualidade.

## Por que este repositório existe

Agentes de IA são cada vez mais capazes em tarefas curtas, mas degradam rapidamente conforme a execução se alonga. Não é uma limitação de modelo -- é uma lacuna de engenharia. Sem estruturas de suporte que gerenciem contexto, decomponham trabalho e separem geração de avaliação, o agente inevitavelmente se perde.

Este repositório existe para resolver esse problema de forma sistemática. Ele documenta, ensina e operacionaliza os padrões de **harness engineering**: a disciplina de construir a infraestrutura de suporte que envolve o modelo e garante confiabilidade em execuções longas. Não se trata de prompts melhores ou modelos maiores -- trata-se de engenharia de software aplicada ao runtime do agente.

O conteúdo cobre desde os fundamentos (por que agentes falham) até arquitetura avançada (multi-agent systems, state persistence, harness evolution), passando por um sistema completo de avaliação (evals estratificadas, amostragem ancorada em produção, flywheel de regressão) e um pipeline automatizado de análise de conhecimento externo. Tudo ancorado em um caso real: o KODA, agente de venda de suplementos via WhatsApp.

## O problema que atacamos

Agentes de IA falham em execuções longas por três razões estruturais:

1. **Perda de contexto** -- a janela de tokens enche, e o agente "esquece" o que estava fazendo.
2. **Planejamento frágil** -- sem decomposição, o agente tenta resolver tudo de uma vez e se perde.
3. **Autoavaliação cega** -- o mesmo modelo que gera também avalia, aprovando qualidade ruim como boa.

A solução está nos **harnesses**: estruturas de suporte que gerenciam contexto, decompõem trabalho em etapas menores e separam geração de avaliação. Este repositório documenta, ensina e operacionaliza esses padrões.

## Para quem é

Pessoas de negócio com skill em construção de agentes e sistemas agenticos. O conteúdo serve tanto para quem está começando quanto para quem já opera agentes em produção e quer elevar a confiabilidade do sistema.

| Perfil | Comece por aqui | Tempo estimado |
|---|---|---|
| Nunca ouvi falar de harness / long-running agents | [[curriculum/QUICK_START|Quick Start]] | 45 min |
| Tenho experiência com LLMs, quero padrões práticos | [[curriculum/MASTER_PLAN|Master Plan]] > "Pule para Prático" | 30 min |
| Sou architect / sênior, quero desenhar sistemas | [[curriculum/MASTER_PLAN|Master Plan]] > "Vá Direto para Avançado" | 30 min |
| Trabalho no KODA, quero aplicar os padrões | [[curriculum/04-nivel-4-koda-specific/01-koda-architecture|Nível 4 — Arquitetura KODA]] | Contínuo |
| Lidero uma equipe, quero o plano de execução | [[curriculum/EXECUTION_PLAN|Execution Plan]] | 30 min |
| Preciso de referência rápida de conceitos | [[curriculum/GLOSSARY|Glossário]] | Lookup |
| Quero visão geral de todos os padrões canônicos | [[docs/system-of-record|System of Record]] | 20 min |
| Quero visualizar conceitos como diagramas | [[curriculum/06-knowledge-graphs/01-concept-ecosystem|Knowledge Graphs]] | Exploração livre |
| Quero entender o mapa completo do repositório | [[index|Knowledge Index]] | 10 min |

## O que você encontra aqui

O repositório está organizado em camadas funcionais. Não é uma coleção de documentos soltos -- cada camada se conecta às outras via wikilinks e converge para o [[docs/system-of-record|system of record]], que define precedência e resolução de conflitos.

### Aprender — o currículo

Um programa completo de 12 semanas, estruturado em 4 níveis de profundidade crescente, 8 conceitos core e dezenas de exercícios práticos. Do fundamento (por que agentes falham) à aplicação em produção (arquitetura do KODA).

| Nível | Foco | Carga |
|---|---|---|
| 1 -- Fundamentos | Context windows, token budgeting, harness patterns básicos | 3-4h |
| 2 -- Padrões Práticos | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading | 6-8h |
| 3 -- Arquitetura Avançada | Multi-agent systems, state persistence, file-based coordination, harness evolution | 8-10h |
| 4 -- Aplicação KODA | Arquitetura real, customer journeys, feature patterns, implementação | Contínuo |

**Pontos de entrada:** [[curriculum/QUICK_START|Quick Start]] · [[curriculum/MASTER_PLAN|Master Plan]] · [[curriculum/INDEX|Índice do Currículo]] · [[curriculum/EXECUTION_PLAN|Execution Plan]] · [[curriculum/FAQ|FAQ]] · [[curriculum/GLOSSARY|Glossário]]

### Referenciar — os padrões canônicos

`docs/canonical/` contém **85+ padrões canônicos de arquitetura agentica** -- extraídos de análises de sistemas em produção, da talk "12-Factor Agents" (Dex Horthy, AI Engineer 2025) e de múltiplas fontes externas processadas pelo pipeline `analyze-and-improve`. Cada padrão documenta um problema, o mecanismo de solução e os trade-offs. A lista completa está em [[docs/system-of-record|system of record]].

Destaques para builders de negócio:

| Padrão | Problema que resolve |
|---|---|
| **Owned Agent Control Loop** | Frameworks controlam o loop como caixa-preta. Assuma o controle: decomponha em Prompt, Context Builder, Switch Statement e Loop com pontos de intervenção explícitos. |
| **Deterministic Tool Dispatch** | Ferramentas não são mágicas -- são JSON + código determinístico. O modelo converte linguagem natural em JSON; daí pra frente é engenharia de software comum. |
| **Error Context Hygiene** | Erros crus (stack traces, HTTP 500) poluem a janela de contexto e enviesam decisões futuras. Resuma erros em uma linha, limpe ao recuperar. |
| **Serializable Pause/Resume State** | Agentes precisam pausar (async APIs, aprovação humana) e retomar sem perder estado. Serialize o contexto ou reconstrua com fidelidade. |
| **Head-Tail Context Truncation** | Quando o contexto estoura, preserve cabeça (objetivo original) e cauda (estado atual); mova o meio para memória endereçável com handles de recuperação. |
| **Addressable Memory Catalog** | Memória externa sem catálogo é inútil. Cada item omitido precisa de `id`, `location`, `preview` e `fetch` para decidir o que recuperar. |
| **Eval Tier Stratification** | Uma única suite de evals não serve para tudo. Estratifique em fast (inner loop), medium (PR gate) e deep (release/canary). |
| **Pain-Signal Eval Progression Gate** | Invista em evals guiado por sinais de dor reais (incidentes, regressões, bottlenecks manuais), não por calendário. |
| **Budget-Aware Session Handoff** | Sessões de agente têm orçamento de tokens finito. Handoff automático preserva estado durável e reseta contexto ativo antes do estouro. |
| **Generator/Evaluator** | O modelo que gera não deve avaliar o próprio output. Separe em dois agentes com loop de feedback e rubricas objetivas. |
| **Plan-Execute-Verify** | Decomponha cada tarefa em três fases com checkpoints explícitos. Cada fase tem contrato de entrada/saída e não avança sem verificação. |
| **Production Failure Regression Flywheel** | Falhas de produção não são só incidentes -- são casos de teste. Converta cada uma em evals estratificadas que impedem regressão. |

### Analisar — diagnósticos e artigos

Análises de sistemas reais (backend MHC/KODA, arquitetura agentica de fundos macro) e artigos sobre temas transversais.

| Diretório | Conteúdo |
|---|---|
| `docs/analysis/` | Diagnósticos do backend MHC/KODA, análise 12-Factor Agents, maturidade de evals, context management, arquitetura de fundo macro -- veja [[docs/analysis/2026-06-09-12-factor-agents/2026-06-09-12-factor-agents-analysis|12-Factor Agents Analysis]] e [[docs/analysis/2026-06-17-macro-fund-agentic-architecture/2026-06-17-macro-fund-agentic-architecture-analysis|Macro Fund Analysis]] |
| `docs/articles/` | Artigos: [[docs/articles/harness-evolution-metodos-construcao|harness evolution]], [[docs/articles/evals-ecommerce-koda|avaliação em e-commerce]], [[docs/articles/rubricas-multidimensionais-arquitetura|rubricas multidimensionais]], [[docs/articles/obsidian-eval-runtime|runtime obsidian-eval]] |
| `docs/evidence/` | Benchmarks e evidências validadas |

### Operar — o harness e o sistema de agentes

O repositório não é só conhecimento -- é um sistema operacional. Você pode rodar o pipeline de análise, usar os agentes e navegar os dashboards.

| Diretório | Conteúdo |
|---|---|
| `harness/` | Sistema de harness que orquestra o pipeline `analyze-and-improve` em 7 fases com evaluators e gates automáticos -- guia completo em [[harness/GUIDE-analyze-and-improve|Guia do Harness]] |
| `.opencode/agents/` | 3 agentes: [[.opencode/agents/hop-orchestrator-rezek|orquestrador principal]], [[.opencode/agents/koda-hop-init-basic|inicializador KODA]], [[.opencode/agents/hop-live-whatsapp-tester|testador WhatsApp]] |
| `.opencode/skills/` | 28 skills: workflow de issues, orquestração, documentação, planos, error hygiene, shadow review, token budget, constraint gates, intent decomposition, e mais |
| `dashboards/` | 3 dashboards Obsidian: [[dashboards/analysis-hub|analysis hub]], [[dashboards/curriculum-progress|curriculum progress]], [[dashboards/obsidian-home|home page]] com dataview queries |
| `templates/` | Templates reutilizáveis: canonical doc, analysis doc, curriculum lesson, curriculum index |
| `concepts/` | Conceitos transversais como [[concepts/sub-agents|sub-agents]] |
| `scripts/` | Scripts operacionais e de validação (`validate-obsidian.ts`, `create-curriculum-issues.sh`) |

### Visualizar — portais e diagramas

| Arquivo | Função |
|---|---|
| [web/koda_course_portal.html](web/koda_course_portal.html) | Portal do curso -- data-driven, vanilla JS |
| [web/koda_knowledge_graphs_35_diagrams.html](web/koda_knowledge_graphs_35_diagrams.html) | Visualizador de 35+ diagramas Mermaid |
| [web/mhc_visao_estrategica.html](web/mhc_visao_estrategica.html) | Visão estratégica MHC |
| [[curriculum/06-knowledge-graphs/01-concept-ecosystem|Knowledge Graphs]] | 35+ diagramas Mermaid no currículo |
| `mapa-mental-repo/` | Mapas mentais de fontes externas processadas |
| `document-architecture.canvas` | Canvas Obsidian da arquitetura de documentos |
| `reading-flow.canvas` | Canvas Obsidian do fluxo de leitura recomendado |

### Navegar — índices e mapas

| Arquivo | Função |
|---|---|
| [[index|Knowledge Index]] | Índice completo com wikilinks para todos os padrões, análises, currículo e ADRs |
| [[docs/system-of-record|System of Record]] | Fonte da verdade: precedência, domínios, padrões ativos, status de ADRs |
| [[AGENTS|Agent Rules]] | Regras obrigatórias para agentes de IA trabalhando neste repositório |

## O que é possível fazer com este repositório

**Estudar e aplicar padrões de confiabilidade.** Siga o currículo do Nível 1 ao 4, aplique os padrões canônicos no seu próprio sistema agentico. Comece por [[curriculum/QUICK_START|Quick Start]].

**Usar como referência de arquitetura.** Consulte `docs/canonical/` ao projetar qualquer sistema agentico. Os padrões cobrem context engineering, evals, harness design, multi-agent coordination, token economics e governança. A lista completa está em [[docs/system-of-record|system of record]].

**Rodar o pipeline de análise de conhecimento.** O harness em `harness/` orquestra o pipeline `analyze-and-improve`: alimente uma fonte externa (talk, paper, transcript) e obtenha padrões extraídos, classificados contra o repositório e integrados como canonical docs, skills ou exercícios. Guia completo em [[harness/GUIDE-analyze-and-improve|Guia do Harness]].

**Navegar o knowledge graph.** Use os dashboards em `dashboards/` no Obsidian para queries dinâmicas (dataview) sobre análises por domínio, progresso do currículo e conexões entre documentos. O [[index|Knowledge Index]] oferece um ponto de entrada com todos os wikilinks.

**Usar o sistema de agentes como template.** O diretório `.opencode/` é um sistema de agentes completo com Handoff Protocol, 28 skills especializadas e 3 agentes. Pode ser adaptado como template para seu próprio projeto agentico. Comece por [[AGENTS|Agent Rules]].

## Quick start

```bash
cp .env.example .env
npm install
npm run lint
npm run test:unit
```

Para começar a estudar, vá direto para [[curriculum/QUICK_START|Quick Start]].

## Stack e tooling

- **Runtime**: Node.js >= 20.18.0, ESM
- **Qualidade**: ESLint 10 com regras customizadas (`no-catch-message`, `no-raw-console-in-scripts`)
- **Orquestração de agentes**: OpenCode com Handoff Protocol (`.opencode/`)
- **Knowledge management**: Obsidian (`.obsidian/`) com wikilinks e dataview
- **Navegação entre vaults**: [`obsidian-eval`](https://www.npmjs.com/package/@pavani/obsidian-eval) -- CLI para scan, query, grafo e cross-vault wikilinks
- **Portais**: HTML estático com vanilla JS e Mermaid.js
- **Validação de documentos**: `npx tsx scripts/validate-obsidian.ts` (frontmatter, wikilinks, tags, `relates-to`)

## Governança do repositório

A fonte da verdade é [[docs/system-of-record|system of record]]. A precedência de documentação é:

1. ADRs aceitos em `docs/decisions/`
2. Documentação canônica ativa em `docs/canonical/`
3. Evidências validadas em `docs/evidence/`
4. Análises em `docs/analysis/`
5. Documentos históricos em `docs/archive/`
6. READMEs e resumos operacionais

Commits seguem o padrão `type(scope): short description`. PRs exigem checklist de crossroad files, seção de eval impact e revisão. Detalhes em [[AGENTS|Agent Rules]].

## Requirements

- Node.js >= 20.18.0
