---
title: "Modelo Mental: Curriculum Long-Running Agents"
type: analysis
date: 2026-06-09
domain: 12-factor-agents
aliases: []
tags: [analise, 12-factor-agents, agent-loop, mental-model]
last_updated: 2026-06-10
---

# Modelo Mental: Curriculum Long-Running Agents

**Data:** 2026-06-09
**Tipo:** Síntese / Modelo Mental
**Escopo:** Estrutura completa do diretório `curriculum/`

---

## O que é

Programa educacional de 12 semanas para ensinar uma equipe a construir agentes de IA que operam de forma confiável por horas (long-running agents). O caso prático é o **KODA** -- agente de vendas de suplementos esportivos via WhatsApp que precisa manter coerência em conversas de 2+ horas.

## O problema raiz

Agentes de IA falham em tarefas longas por três motivos:

1. **Context Amnesia** -- esquecem informações críticas após 30-60 minutos (overflow da context window)
2. **Planning Collapse** -- misturam planejar, executar e verificar num único passo, perdendo o fio
3. **Self-Evaluation Collapse** -- aprovam o próprio trabalho ruim (sycophancy: tendência a agradar)

## A solução: Harnesses

"Harness" é a infraestrutura que envolve o agente. Analogia: se o agente é o piloto, o harness é o avião + torre de controle + combustível. Componentes: gerenciamento de memória, decomposição de tarefas, separação geração/avaliação, coordenação multi-agente.

---

## Arquitetura do Currículo

### Estrutura de diretórios

```
curriculum/
├── README.md                          # Visão geral, métricas de sucesso, fluxos de leitura
├── INDEX.md                           # Navegação rápida por perfil e pergunta
├── MASTER_PLAN.md                     # Plano mestre com roadmap completo
├── QUICK_START.md                     # Onboarding em 45 minutos
├── EXECUTION_PLAN.md                  # Cronograma detalhado de 12 semanas
├── GLOSSARY.md                        # 60+ termos técnicos com definições
├── FAQ.md                             # Perguntas frequentes (3863 linhas)
├── DELIVERY-COMPLETE.md               # Status de entrega dos artefatos
│
├── 01-nivel-1-fundamentals/           # Nível 1: Fundamentos (3-4h)
├── 02-nivel-2-practical-patterns/     # Nível 2: Padrões Práticos (6-8h)
├── 03-nivel-3-advanced-architecture/  # Nível 3: Arquitetura Avançada (8-10h)
├── 04-nivel-4-koda-specific/          # Nível 4: KODA-Específico (contínuo)
│
├── 05-core-concepts/                  # 8 conceitos em profundidade
├── 06-knowledge-graphs/               # 35+ diagramas Mermaid
├── 07-implementation-guides/          # Guias de setup e operação
├── 08-tools-templates/               # Templates reutilizáveis
├── 09-case-studies/                   # 5 estudos de caso
└── 10-references/                     # Referências externas
```

### Os 4 Níveis

| Nível | Carga | Pergunta central | Resultado |
|---|---|---|---|
| **1 - Fundamentos** | 3-4h | Por que agentes falham em tarefas longas? | Compreensão dos 3 problemas principais |
| **2 - Padrões Práticos** | 6-8h | Como fazemos agentes mais confiáveis? | Aplica Generator/Evaluator, Sprint Contracts, Rubrics |
| **3 - Arquitetura Avançada** | 8-10h | Como construímos sistemas sofisticados? | Desenha multi-agent systems com state persistence |
| **4 - KODA-Específico** | Contínuo | Como aplicamos tudo no KODA? | Expert em harness do KODA, melhoria contínua |

### Camadas Transversais

| Camada | O que contém |
|---|---|
| `05-core-concepts/` | 8 conceitos em profundidade (~2000-2600 linhas cada): explicação narrativa, 3 knowledge graphs Mermaid, aplicação KODA, checklist |
| `06-knowledge-graphs/` | 35+ diagramas Mermaid: ecossistema, dependências KODA, progressão de aprendizado, problem-solution mapping |
| `07-implementation-guides/` | Setup guide, team progression, harness design checklist, evaluation rubric template, trace analysis, harness evolution playbook |
| `08-tools-templates/` | Sprint contract, evaluation rubric, knowledge graph, ADR, team progress tracker, learning assessment rubric |
| `09-case-studies/` | Retro Game Maker (Anthropic), Browser DAW App, 3 casos KODA (product discovery, order processing, fulfillment) |
| `10-references/` | Resumo da apresentação Anthropic, timeline de capacidade de modelos, recursos adicionais |

---

## Os 8 Conceitos Core

Cada conceito tem: explicação narrativa (história do Fernando/KODA), 3 knowledge graphs Mermaid, aplicação prática no KODA, checklist de implementação.

| # | Conceito | Nível | Complexidade | Prioridade |
|---|---|---|---|---|
| 1 | Context Management | 1 | Baixa | Alta |
| 2 | Planning vs. Execution Separation | 2 | Média | Alta |
| 3 | Generator/Evaluator Pattern | 2 | Média | Alta |
| 4 | Sprint Contracts | 2 | Média | Média |
| 5 | State Persistence | 3 | Alta | Média |
| 6 | Harness Evolution | 3 | Alta | Média |
| 7 | Multi-Agent Coordination | 3 | Alta | Média |
| 8 | Evaluation Rubrics | 2 | Média | Média |

### Progressão dos conceitos

```
Context Management (N1)
       ↓
Planning/Execution Separation (N2)
       ↓
Generator/Evaluator (N2) ←→ Sprint Contracts (N2) ←→ Evaluation Rubrics (N2)
       ↓
Multi-Agent Coordination (N3) ←→ State Persistence (N3)
       ↓
Harness Evolution (N3)
       ↓
Aplicação completa em KODA (N4)
```

---

## Glossário dos Termos-Chave

| Termo | Significado |
|---|---|
| **Harness** | Infraestrutura que sustenta agentes (memória, planejamento, avaliação, coordenação) |
| **Context Window** | Memória imediata do modelo. Opus 4.6: ~1M tokens (~6h de trabalho) |
| **Token Budget** | Gerenciamento consciente de quantos tokens estão disponíveis vs. usados |
| **Generator/Evaluator** | Padrão onde um agente gera e outro avalia -- evita sycophancy |
| **Sprint** | Unidade de trabalho de 30-120 minutos de execução do agente |
| **Sprint Contract** | Acordo negociado entre Generator e Evaluator sobre critérios de conclusão |
| **Rubric** | Conjunto de critérios mensuráveis (escala 1-10) para avaliar qualidade subjetiva |
| **Trace** | Log detalhado de cada passo do agente -- ferramenta principal de debugging |
| **Sycophancy** | Tendência do LLM de agradar/aprovar trabalho ruim |
| **Context Amnesia** | Quando o agente "esquece" contexto anterior por ter excedido a janela |
| **Context Anxiety** | Comportamento ansioso do agente ao se aproximar do limite de contexto |
| **Context Rot** | Perda gradual de coerência conforme avança na janela de contexto |
| **Harness Evolution** | Remover componentes de harness quando o modelo subjacente melhora |
| **Planner** | Agente especializado em decompor problemas em sprints |
| **Compaction** | Resumir/comprimir contexto antigo mantendo informações-chave |
| **MCP** | Model Context Protocol -- protocolo para agentes usarem ferramentas/APIs externas |
| **METR** | Model Evaluation Task Completion Rate -- % de tarefas completadas com sucesso |
| **Ralph Loop** | Técnica de loop incremental (Jeffrey Huntley, jul/2025) -- substituída por Generator/Evaluator |
| **ADR** | Architecture Decision Record -- documento de decisão arquitetural |

---

## Cronograma de 12 Semanas

| Semanas | Fase | Nível | Entregável Principal |
|---|---|---|---|
| 1-2 | Fundação | Nível 1 | Todos entendem os 3 problemas; exercícios completos |
| 3-4 | Padrões | Nível 2 | Generator/Evaluator para 1 feature KODA; sprint contracts escritos; rubrics iniciais |
| 5-6 | Arquitetura | Nível 3 | Multi-agent design para KODA; state persistence implementada; harness evolution plan |
| 7-12 | Aplicação | Nível 4 | Melhorias contínuas no KODA; mentoring; features novas usando padrões aprendidos |

### Métricas de sucesso

- **Semana 2**: 100% da equipe entende os 3 problemas
- **Semana 4**: 100% domina padrões práticos; rubrics para 2+ features KODA
- **Semana 6**: 60-80% em Nível 3; arquitetura melhorada proposta
- **Semana 12**: 50%+ em Nível 4; equipe mentoreia novos membros; KODA significativamente melhorado

---

## Padrões de Design Fundamentais

### Generator/Evaluator Pattern

```
┌───────────┐     cria      ┌──────────┐
│ Generator │ ────────────→ │ Evaluator │
│  (agente) │               │  (agente) │
└───────────┘               └──────────┘
                                  │
                            avalia contra
                            rubric + testes
                                  │
                            ┌─────┴─────┐
                            │ feedback  │
                            │ estruturado│
                            └───────────┘
```

Por que funciona: separa criação de julgamento. Generator não sofre de sycophancy porque não avalia o próprio trabalho. Evaluator é treinado para ser crítico.

### Multi-Agent System (Planner + Generator + Evaluator)

```
  ┌─────────┐     sprints     ┌───────────┐     artefato    ┌──────────┐
  │ Planner │ ──────────────→ │ Generator │ ──────────────→ │ Evaluator│
  └─────────┘                 └───────────┘                 └──────────┘
       │                                                         │
       │                    ┌──────────┐                         │
       └──────────────────→ │  State   │ ←───────────────────────┘
                             │ (arquivo)│
                             └──────────┘
```

Cada papel é um agente separado com responsabilidades distintas, coordenando via estado persistente (arquivos).

### Sprint Contract

Acordo negociado entre Generator e Evaluator ANTES da execução:

- Generator: "Vou implementar checkout com Stripe"
- Evaluator: "Aceito se: (1) testa com 3 cartões reais, (2) maneja erros, (3) não expõe dados"
- Ambos concordam: contrato firmado

### Harness Evolution

Conforme o modelo melhora, componentes de harness se tornam desnecessários:

| Componente | Opus 4.5 | Opus 4.6 |
|---|---|---|
| Context reset | Essencial | Não precisa |
| Sprint decomposition | Necessário | Opcional |
| Eval cadence | Per-sprint | Single pass |

---

## Contexto do Repositório

O currículo é o produto principal. O repositório também contém:

- **`.opencode/agents/`** -- Definições de agentes no padrão HoP (Handoff Protocol): orquestrador, inicializador KODA, tester WhatsApp
- **`.opencode/skills/`** -- Skills de workflow: issue-start, issue-review, issue-finish, orchestrator, doc-coauthoring, writing-plans
- **`docs/analysis/mhc-backend/`** -- 7 diagnósticos do backend real do KODA (harness, Nível 2, Nível 3, output validation, etc.)
- **`rawfiles/` + `prompts/`** -- Material-fonte e prompts usados para gerar o conteúdo do currículo
- **`web/`** -- Portal HTML estático do curso + visualizador de 35 diagramas Mermaid
- **`scripts/`** -- Script de automação para criação de issues do currículo
- Stack: Node >= 20.18, ESLint 10, sem código fonte `src/` ainda

---

## Navegação por Perfil

| Perfil | Por onde começar |
|---|---|
| Iniciante total | `curriculum/QUICK_START.md` → Nível 1 → exercícios |
| Conhece LLMs, quer padrões | Nível 2: `01-generator-evaluator-pattern.md` |
| Arquiteto / sênior | Nível 3: `01-multi-agent-systems.md` |
| Trabalha no KODA | Nível 4: `01-koda-architecture.md` |
| Precisa de referência rápida | `GLOSSARY.md` ou `INDEX.md` |
| Líder de projeto | `MASTER_PLAN.md` → `EXECUTION_PLAN.md` |

---

## Princípios do Programa

1. **Aprenda no seu ritmo** -- cada pessoa é diferente
2. **Compreenda antes de memorizar** -- foco no "porquê", não só no "como"
3. **Aplique no KODA** -- melhor forma de aprender é usando em código real
4. **Ensine outros** -- você realmente aprendeu quando pode ensinar
5. **Documente** -- compartilhe aprendizados com a equipe
6. **Itere** -- padrões evoluem conforme novos modelos chegam

---

*Síntese produzida a partir da leitura completa de: README.md, MASTER_PLAN.md, INDEX.md, QUICK_START.md, GLOSSARY.md, FAQ.md, EXECUTION_PLAN.md, DELIVERY-COMPLETE.md, system-of-record.md, AGENTS.md, e arquivos de core concepts.*
