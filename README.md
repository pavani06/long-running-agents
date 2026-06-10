# long-running-agents

Base de conhecimento e programa curricular para construir sistemas de IA que operam de forma confiável por horas, dias ou pelo tempo que a tarefa exigir -- sem perder contexto, capacidade de planejamento ou julgamento de qualidade.

## O problema que atacamos

Agentes de IA falham em execuções longas por três razões estruturais:

1. **Perda de contexto** -- a janela de tokens enche, e o agente "esquece" o que estava fazendo.
2. **Planejamento frágil** -- sem decomposição, o agente tenta resolver tudo de uma vez e se perde.
3. **Autoavaliação cega** -- o mesmo modelo que gera também avalia, aprovando qualidade ruim como boa.

A solução está nos **harnesses**: estruturas de suporte que gerenciam contexto, decompõem trabalho em etapas menores e separam geração de avaliação. Este repositório documenta, ensina e operacionaliza esses padrões.

## Para quem é este repositório

Pessoas de negócio com skill em construção de agentes e sistemas agenticos. O conteúdo serve tanto para quem está começando quanto para quem já opera agentes em produção e quer elevar a confiabilidade do sistema.

## Navegue pelo seu perfil

| Perfil | Comece por aqui | Tempo estimado |
|---|---|---|
| Nunca ouvi falar de harness / long-running agents | `curriculum/QUICK_START.md` | 45 min |
| Tenho experiência com LLMs, quero padrões práticos | `curriculum/MASTER_PLAN.md` > seção "Pule para Prático" | 30 min |
| Sou architect / sênior, quero desenhar sistemas | `curriculum/MASTER_PLAN.md` > seção "Vá Direto para Avançado" | 30 min |
| Trabalho no KODA, quero aplicar os padrões | `curriculum/04-nivel-4-koda-specific/` | Contínuo |
| Lidero uma equipe, quero o plano de execução | `curriculum/EXECUTION_PLAN.md` | 30 min |
| Preciso de referência rápida | `curriculum/GLOSSARY.md` | Lookup |
| Preciso de visão geral dos padrões canônicos | `docs/system-of-record.md` | 20 min |
| Quero visualizar conceitos como diagramas | `curriculum/06-knowledge-graphs/` | Exploração livre |

## O que tem aqui

```
long-running-agents/
|
|-- curriculum/            Currículo de 12 semanas, 4 níveis, 8 conceitos core
|   |-- 01-nivel-1/        Conceitos fundamentais (por que agentes falham)
|   |-- 02-nivel-2/        Padrões práticos (Generator/Evaluator, Sprint Contracts,
|   |                       Rubric Design, Trace Reading)
|   |-- 03-nivel-3/        Arquitetura avançada (Multi-Agent, State Persistence,
|   |                       File-Based Coordination, Harness Evolution)
|   |-- 04-nivel-4/        Aplicação específica ao KODA (agente WhatsApp)
|   |-- 05-core-concepts/  8 conceitos com explicações, graphs e checklists
|   |-- 06-knowledge-graphs/  35+ diagramas Mermaid
|   |-- 07-implementation-guides/  Guias de setup, progressão, harness design
|   |-- 08-tools-templates/  Templates de sprint contract, rubrica, ADR, tracker
|   |-- 09-case-studies/  5 estudos de caso reais
|   |-- 10-references/    Referências externas, timeline de capacidade de modelos
|   |-- README.md, QUICK_START.md, MASTER_PLAN.md, EXECUTION_PLAN.md,
|   |   INDEX.md, GLOSSARY.md, FAQ.md
|
|-- docs/                   Documentação técnica e governança
|   |-- canonical/          16 padrões canônicos ativos de arquitetura agentica
|   |-- analysis/           Diagnósticos do backend MHC/KODA, análise 12-Factor
|   |                        Agents, análise de maturidade de evals
|   |-- decisions/          ADRs pendentes (tópicos candidatos listados)
|   |-- evidence/           Benchmarks e evidências validadas
|   |-- plans/              Planos de execução
|   |-- system-of-record.md Mapa das fontes canônicas com precedência
|
|-- .opencode/              Sistema de agentes (Handoff Protocol)
|   |-- agents/             3 agentes (orquestrador, init KODA, tester WhatsApp)
|   |-- skills/             10 skills (issue workflow, orquestração, documentação,
|   |                        planos, error hygiene, análise)
|   |-- prompts/            Prompts de configuração do sistema
|
|-- web/                    Portais estáticos
|   |-- koda_course_portal.html         Portal do curso (data-driven, vanilla JS)
|   |-- koda_knowledge_graphs_35_diagrams.html  Visualizador de 35 diagramas Mermaid
|   |-- mhc_visao_estrategica.html      Visão estratégica MHC
|
|-- rawfiles/               Material-fonte usado para gerar o currículo
|-- prompts/                Prompts usados na geração do conteúdo
|-- scripts/                Scripts operacionais
|-- .github/                Templates de PR/issue, CODEOWNERS, dependabot
```

## O currículo em 4 níveis

| Nível | Foco | Carga | Pergunta central |
|---|---|---|---|
| **1 -- Fundamentos** | Context windows, token budgeting, harness patterns básicos | 3-4h | Por que agentes falham em tarefas longas? |
| **2 -- Padrões Práticos** | Generator/Evaluator, Sprint Contracts, Rubric Design, Trace Reading | 6-8h | Como construir agentes confiáveis? |
| **3 -- Arquitetura Avançada** | Multi-agent systems, state persistence, file-based coordination, harness evolution | 8-10h | Como projetar sistemas complexos? |
| **4 -- Aplicação KODA** | Arquitetura real, customer journeys, feature patterns, implementação | Contínuo | Como aplicar tudo em produção? |

Cada nível tem conteúdo teórico, exercícios práticos com soluções e aplicação direta no KODA -- o agente de venda de suplementos via WhatsApp que serve como caso real do currículo.

## Padrões canônicos de arquitetura

Os `docs/canonical/` contêm 16 padrões extraídos de análises de sistemas agenticos em produção e da talk "12-Factor Agents" (Dex Horthy, AI Engineer 2025). Padrões de maior relevância para builders de negócio:

| Padrão | Problema que resolve |
|---|---|
| **Owned Agent Control Loop** | Frameworks controlam o loop do agente como caixa-preta. Assuma o controle: decomponha em Prompt, Context Builder, Switch Statement e Loop com pontos de intervenção explícitos. |
| **Deterministic Tool Dispatch** | Ferramentas não são mágicas -- são JSON + código determinístico. O modelo converte linguagem natural em JSON; daí pra frente é engenharia de software comum. |
| **Error Context Hygiene** | Erros crus (stack traces, HTTP 500) poluem a janela de contexto e enviesam decisões futuras do modelo. Resuma erros em uma linha, limpe ao recuperar. |
| **Serializable Pause/Resume State** | Agentes precisam pausar (async APIs, aprovação humana) e retomar sem perder estado. Serialize o contexto ou reconstrua com fidelidade. |
| **Head-Tail Context Truncation** | Quando o contexto estoura, preserve cabeça (objetivo original) e cauda (estado atual); mova o meio para memória endereçável com handles de recuperação. |
| **Addressable Memory Catalog** | Memória externa sem catálogo é inútil. Cada item omitido precisa de `id`, `location`, `preview` e `fetch` para o agente decidir o que recuperar. |
| **Eval Tier Stratification** | Uma única suite de evals não serve para tudo. Estratifique em fast (inner loop), medium (PR gate) e deep (release/canary). |
| **Pain-Signal Eval Progression Gate** | Invista em evals guiado por sinais de dor reais (incidentes, regressões, bottlenecks manuais), não por calendário. |

A lista completa está em `docs/system-of-record.md`.

## Stack e tooling

- **Runtime**: Node.js >= 20.18.0, ESM
- **Qualidade**: ESLint 10 com regras customizadas (`no-catch-message`, `no-raw-console-in-scripts`)
- **Orquestração de agentes**: OpenCode com Handoff Protocol (`.opencode/`)
- **Knowledge management**: Obsidian (`.obsidian/`)
- **Portais**: HTML estático com vanilla JS e Mermaid.js

## Quick start

```bash
cp .env.example .env
npm install
npm run lint
npm run test:unit
```

Para começar a estudar, vá direto para `curriculum/QUICK_START.md`.

## Governança do repositório

A fonte da verdade é `docs/system-of-record.md`. A precedência de documentação é:

1. ADRs aceitos em `docs/decisions/`
2. Documentação canônica ativa em `docs/canonical/`
3. Evidências validadas em `docs/evidence/`
4. Análises em `docs/analysis/`
5. Documentos históricos em `docs/archive/`
6. READMEs e resumos operacionais

Commits seguem o padrão `type(scope): short description`. PRs exigem checklist de crossroad files, seção de eval impact e revisão. Detalhes em `AGENTS.md`.

## Requirements

- Node.js >= 20.18.0
