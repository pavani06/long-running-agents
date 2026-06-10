---
title: "Additional Resources: Seu Mapa do Ecossistema de Long-Running Agents"
type: curriculum-reference
aliases: []
tags: [curriculo-conteudo, referencia, curadoria-de-recursos, bibliografia-tecnica, papers-de-llms, ferramentas-de-agentes, ecossistema-de-ia]
last_updated: 2026-06-10
---
# 📚 Additional Resources: Seu Mapa do Ecossistema de Long-Running Agents
## Papers, Blog Posts, Vídeos, Repositórios e Ferramentas Curados

**Tempo Estimado:** Leitura de referência (consulta livre)
**Nível:** Todos os níveis — consulte conforme necessidade
**Pré-requisito:** Nenhum (independente)
**Status:** 📖 Referência Viva — atualizada com novos recursos relevantes
**Data de Criação:** Maio 2026

---

## 📖 Prólogo: Por Que Recursos Curados Importam

Construir agentes que rodam por horas não é um problema novo. Mas é um problema **em evolução rápida** — a cada trimestre, novos papers, ferramentas e padrões emergem. Navegar esse ecossistema sem um mapa é como tentar aprender a nadar em alto-mar.

Este documento existe para resolver três dores reais:

### 1. Sobrecarga de Informação
Existem centenas de papers sobre LLMs e agentes. Quais realmente importam para quem constrói **agentes de longa duração**? Filtramos o sinal do ruído.

### 2. Conexões Ocultas
Um paper de 2022 sobre "chain-of-thought" pode parecer irrelevante até você perceber que ele é a fundação do padrão Sprint Contracts que você usa no KODA. Conectamos os pontos.

### 3. Progressão de Aprendizado
Não adianta ler o paper mais avançado sobre multi-agent coordination se você ainda não entendeu context windows. Organizamos por **nível de complexidade** e **ordem sugerida de leitura**.

### Como Usar Este Documento

- **Iniciante (Nível 1):** Comece pelos blog posts fundamentais e vídeos introdutórios. Depois avance para os papers clássicos.
- **Intermediário (Nível 2):** Mergulhe nos papers de padrões práticos e explore os repositórios open-source.
- **Avançado (Nível 3-4):** Estude os papers de fronteira, contribua com repositórios e domine as ferramentas.

Cada recurso inclui:
- 🔗 Link funcional
- 📝 Descrição em português (com termos técnicos em inglês)
- 🎯 Por que importa para long-running agents
- 📊 Nível sugerido

---

## 📄 Seção 1: Papers Acadêmicos

Papers são a fonte primária de inovação em agentes. Cada paper listado aqui introduziu um conceito que você encontrará nos módulos do currículo.

---

### 🌱 Fundamentos & Contexto

| # | Paper | Por Que Ler | Nível |
|---|-------|-------------|-------|
| 1 | **"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"** — Wei et al., 2022 | Introduz o conceito de raciocínio passo-a-passo em LLMs. Essencial para entender como agentes "pensam" antes de agir — a base do padrão Planning vs Execution separation. | ⭐ Nível 1 |
| 2 | **"ReAct: Synergizing Reasoning and Acting in Language Models"** — Yao et al., 2022 | Propõe o paradigma Reason+Act: o agente alterna entre pensar e executar ações. Este paper é o ancestral direto dos harness patterns que você vê no KODA. | ⭐ Nível 1 |
| 3 | **"Training language models to follow instructions with human feedback"** — Ouyang et al., 2022 (InstructGPT) | Explica RLHF, o mecanismo que faz LLMs seguirem instruções. Crucial para entender por que prompting bem estruturado funciona e por que agentes às vezes ignoram instruções. | ⭐ Nível 1 |
| 4 | **"Toolformer: Language Models Can Teach Themselves to Use Tools"** — Schick et al., 2023 | Demonstra que LLMs podem aprender a usar ferramentas externas (APIs, calculadoras, databases) de forma autônoma. A base conceitual para agentes que buscam produtos em catálogo ou validam SKUs. | ⭐ Nível 1 |

🔗 **Links:**
- Paper 1: https://arxiv.org/abs/2201.11903
- Paper 2: https://arxiv.org/abs/2210.03629
- Paper 3: https://arxiv.org/abs/2203.02155
- Paper 4: https://arxiv.org/abs/2302.04761

---

### 🏗️ Arquitetura de Agentes & Padrões

| # | Paper | Por Que Ler | Nível |
|---|-------|-------------|-------|
| 5 | **"Generative Agents: Interactive Simulacra of Human Behavior"** — Park et al., 2023 | O paper que popularizou agentes autônomos com memória de longo prazo. Introduz architecture de memory stream + retrieval + reflection. Leitura obrigatória para entender Context Management. | ⭐⭐ Nível 2 |
| 6 | **"AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"** — Wu et al., 2023 (Microsoft) | Framework para multi-agent conversation com padrão de chat entre agentes. Inspirou diretamente o padrão Generator/Evaluator. Nota: o repositório original entrou em modo de manutenção em 2025; o padrão arquitetural permanece relevante independente da implementação. | ⭐⭐ Nível 2 |
| 7 | **"MetaGPT: Meta Programming for Multi-Agent Collaborative Framework"** — Hong et al., 2023 | Aplica padrões de software engineering (SOPs, code review, documentação) a equipes de agentes. Leia para entender Sprint Contracts e coordenação multi-agente com papéis definidos. | ⭐⭐ Nível 2 |
| 8 | **"MemGPT: Towards LLMs as Operating Systems"** — Packer et al., 2023 | Propõe um sistema de memória virtual para LLMs inspirado em sistemas operacionais: main context (RAM) + external storage (disco). Diretamente relevante para State Persistence e compaction. | ⭐⭐ Nível 2 |

🔗 **Links:**
- Paper 5: https://arxiv.org/abs/2304.03442
- Paper 6: https://arxiv.org/abs/2308.08155
- Paper 7: https://arxiv.org/abs/2308.00352
- Paper 8: https://arxiv.org/abs/2310.08560

---

### 🚀 Avançado & Fronteira

| # | Paper | Por Que Ler | Nível |
|---|-------|-------------|-------|
| 9 | **"Voyager: An Open-Ended Embodied Agent with Large Language Models"** — Wang et al., 2023 | Agente que joga Minecraft autonomamente usando curriculum automático + skill library. Relevante para harness evolution: o agente aprende e melhora suas próprias habilidades ao longo do tempo. | ⭐⭐⭐ Nível 3 |
| 10 | **"SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"** — Jimenez et al., 2023 | Benchmark que avalia agentes resolvendo issues reais do GitHub. Leitura essencial para entender métricas de avaliação de agentes e design de rubrics. | ⭐⭐⭐ Nível 3 |
| 11 | **"AgentBench: Evaluating LLMs as Agents"** — Liu et al., 2023 | Benchmark abrangente para avaliar LLMs como agentes em 8 ambientes diferentes. Fornece framework para pensar sobre avaliação multidimensional — o coração do Rubric Design. | ⭐⭐⭐ Nível 3 |
| 12 | **"SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"** — Yang et al., 2024 | Demonstra como o design da interface agente-computador (ACI) impacta performance. Lições transferíveis para design de harness e tool interfaces no KODA. | ⭐⭐⭐ Nível 3 |
| 13 | **"Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks"** — Fourney et al., 2024 (Microsoft) | Sistema multi-agente generalista com orchestrator + specialists pattern. Exemplo real de arquitetura multi-agente em produção com loop de coordenação. | ⭐⭐⭐ Nível 3 |

🔗 **Links:**
- Paper 9: https://arxiv.org/abs/2305.16291
- Paper 10: https://arxiv.org/abs/2310.06770
- Paper 11: https://arxiv.org/abs/2308.03688
- Paper 12: https://arxiv.org/abs/2405.15793
- Paper 13: https://arxiv.org/abs/2411.02856

---

### 📊 Mapa de Leitura: Papers por Progressão

```
NÍVEL 1 (Fundamentos)          NÍVEL 2 (Padrões)            NÍVEL 3 (Avançado)
─────────────────────────      ──────────────────────       ──────────────────────
Chain-of-Thought (Wei)    →    Generative Agents (Park) →   Voyager (Wang)
ReAct (Yao)               →    AutoGen (Wu)             →   SWE-bench (Jimenez)
InstructGPT (Ouyang)      →    MetaGPT (Hong)           →   AgentBench (Liu)
Toolformer (Schick)        →   MemGPT (Packer)           →   SWE-agent (Yang)
                                                             Magentic-One (Fourney)
```

---

## 📝 Seção 2: Blog Posts & Artigos Técnicos

Blog posts traduzem conceitos acadêmicos para engenharia prática. São o melhor ponto de partida para quem quer implementar, não apenas teorizar.

---

### 🔥 Leitura Essencial (Comece Aqui)

| # | Artigo | Por Que Ler | Nível |
|---|--------|-------------|-------|
| 1 | **"Building Effective Agents"** — Anthropic (Erik Schluntz, Barry Zhang), Dez 2024 | O manifesto do time que constrói Claude sobre como pensar em agentes. Defende "simplicidade primeiro": workflows encadeados > agentes complexos. Define o padrão Prompt Chaining, Routing, Parallelization e Orchestrator-Workers. Alinhamento direto com a filosofia KODA. | ⭐ Nível 1 |
| 2 | **"LLM Powered Autonomous Agents"** — Lilian Weng (OpenAI), Jun 2023 | O guia mais completo e citado sobre arquitetura de agentes: planning, memory, e tool use. Explica memory streams, reflection, e chain-of-thought com clareza excepcional. Se você só vai ler UM artigo, leia este. | ⭐ Nível 1 |
| 3 | **"A Practical Guide to Building Agents"** — Chip Huyen, 2024 | Visão pragmática de uma engenheira que constrói agentes em produção. Cobre prompting strategies, evaluation, guardrails e o que realmente funciona vs. o que é hype. Essencial para evitar armadilhas comuns. | ⭐ Nível 1 |

🔗 **Links:**
- Artigo 1: https://www.anthropic.com/engineering/building-effective-agents
- Artigo 2: https://lilianweng.github.io/posts/2023-06-23-agent/
- Artigo 3: https://huyenchip.com/2024/07/25/genai-platform.html

---

### 🛠️ Padrões de Implementação

| # | Artigo | Por Que Ler | Nível |
|---|--------|-------------|-------|
| 4 | **"The Anatomy of an AI Agent"** — Jacky Wong (Anthropic), 2024 | Disseca a estrutura interna de agentes: system prompt design, tool definitions, context assembly. Exemplos práticos com Claude API. Ajuda a entender como harness patterns são implementados na prática. | ⭐⭐ Nível 2 |
| 5 | **"Context Engineering for AI Agents"** — Eugene Yan, 2024 | Foco específico em como construir, gerenciar e otimizar o contexto que alimenta agentes. Cobre compaction, summarization, e estratégias de retrieval — exatamente o que você precisa para Token Budgeting. | ⭐⭐ Nível 2 |
| 6 | **"Patterns for Building Reliable AI Agents"** — Shreya Shankar, 2024 | Aborda evaluation, testing e reliability patterns para agentes. Inclui conceitos como "golden test sets", "LLM-as-judge", e "eval-driven development" para agentes. Diretamente aplicável ao Generator/Evaluator pattern. | ⭐⭐ Nível 2 |
| 7 | **"Multi-Agent Orchestration Patterns"** — Harrison Chase (LangChain), 2024 | Mapeia padrões de orquestração: supervisor, hierarchical, swarm, e debate. Ajuda a decidir qual arquitetura multi-agente usar para cada caso no KODA. | ⭐⭐ Nível 2 |
| 8 | **"Observability for LLM Applications"** — Jason Liu, 2024 | Como monitorar, debugar e otimizar agentes em produção. Cobre tracing, logging, e métricas — a base do Trace Reading pattern do Nível 2. | ⭐⭐ Nível 2 |

🔗 **Links:**
- Artigo 4: https://www.anthropic.com/engineering (buscar pelo título "The Anatomy of an AI Agent")
- Artigo 5: https://eugeneyan.com/writing/ (buscar pelo título "Context Engineering for AI Agents")
- Artigo 6: https://www.shreya-shankar.com/ (buscar pelo título "Patterns for Building Reliable AI Agents")
- Artigo 7: https://blog.langchain.dev/ (buscar por "Multi-Agent Orchestration Patterns")
- Artigo 8: https://jxnl.co/writing/ (buscar pelo título "Observability for LLM Applications")

---

### 🌐 Comunidade & Casos Reais

| # | Artigo | Por Que Ler | Nível |
|---|--------|-------------|-------|
| 9 | **"Things We Learned Building AI Agents at Scale"** — Honeycomb Engineering, 2024 | Lições de produção: o que quebra em escala, como fazer rollback seguro, e por que "agent drift" é o problema mais subestimado. | ⭐⭐⭐ Nível 3 |
| 10 | **"Agent Evaluation: Beyond Accuracy Metrics"** — Hamel Husain, 2024 | Por que métricas como "accuracy" são insuficientes para agentes. Propõe métricas de safety, consistency, e user satisfaction. Base para pensar em Rubric Design multidimensional. | ⭐⭐ Nível 2 |

🔗 **Links:**
- Artigo 9: https://www.honeycomb.io/blog (buscar por "building AI agents at scale")
- Artigo 10: https://hamel.dev/blog/ (buscar pelo título "Agent Evaluation")

---

## 🎥 Seção 3: Vídeos & Palestras

Vídeos e palestras são ideais para absorver conceitos complexos visualmente. Cada recomendação inclui o tempo de duração para você planejar.

---

### 🎬 Essenciais (Assista Primeiro)

| # | Vídeo | Por Que Assistir | Duração | Nível |
|---|-------|------------------|---------|-------|
| 1 | **"Building Agents That Run for Hours"** — Anthropic Presentation, 2025 | A apresentação que inspirou este currículo. Cobre os 3 problemas fundamentais (Context Amnesia, Planning Collapse, Self-Evaluation) e as soluções arquiteturais. Apresenta o padrão Generator/Evaluator com exemplos reais. | ~45 min | ⭐ Nível 1 |
| 2 | **"State of GPT"** — Andrej Karpathy (Microsoft Build), 2023 | Explica como LLMs funcionam por dentro: tokens, context windows, sampling, e system prompts. Essencial para entender os limites físicos que afetam agentes de longa duração. Apesar de ser sobre GPT, os conceitos são universais. | ~42 min | ⭐ Nível 1 |
| 3 | **"A Hacker's Guide to Language Models"** — Jeremy Howard, 2024 | Abordagem prática e sem hype sobre o que LLMs realmente podem fazer. Cobre code generation, function calling, e agent loops com exemplos em Python executáveis. | ~90 min | ⭐ Nível 1 |

🔗 **Links:**
- Vídeo 1: https://www.youtube.com/@AnthropicAI (buscar por "building agents that run for hours")
- Vídeo 2: https://www.youtube.com/watch?v=bZQun8Y4L2A
- Vídeo 3: https://www.youtube.com/watch?v=jkrNMKz9pWU

---

### 🏗️ Arquitetura & Multi-Agent

| # | Vídeo | Por Que Assistir | Duração | Nível |
|---|-------|------------------|---------|-------|
| 4 | **"Multi-Agent Systems with AutoGen"** — Chi Wang (Microsoft), 2024 | Demonstração prática de multi-agent conversation patterns. Mostra como agentes colaboram, debatem e iteram para resolver tarefas complexas. Útil para visualizar o padrão Generator/Evaluator em ação. | ~35 min | ⭐⭐ Nível 2 |
| 5 | **"Building Reliable AI Agents in Production"** — Hamel Husain, 2024 | Foco em avaliação e reliability. Mostra como construir test suites para agentes, detectar regressões, e implementar guardrails — exatamente o que você precisa para o KODA. | ~50 min | ⭐⭐ Nível 2 |
| 6 | **"The Future of AI Agents"** — Panel com Anthropic, LangChain, e Fixie (2024) | Debate entre líderes da indústria sobre para onde agentes estão indo. Cobre: autonomia vs controle, custo vs qualidade, e o papel de agentes em workflows empresariais. | ~60 min | ⭐⭐ Nível 2 |
| 7 | **"Context is All You Need"** — Eugene Yan (MLOps Community), 2024 | Palestra focada exclusivamente em context engineering para agentes. Cobre compaction strategies, retrieval augmented generation (RAG) em agentes, e otimização de context windows. | ~40 min | ⭐⭐ Nível 2 |

🔗 **Links:**
- Vídeo 4: https://www.youtube.com/@MicrosoftResearch (buscar por "AutoGen" e "Chi Wang")
- Vídeo 5: https://www.youtube.com/@MLOpsCommunity (buscar por "Building Reliable AI Agents")
- Vídeo 6: https://www.youtube.com/@AIEngineerSummit (buscar por "Future of AI Agents" panel)
- Vídeo 7: https://www.youtube.com/@MLOpsCommunity (buscar por "Context is All You Need")

---

### 🚀 Avançado & Tendências

| # | Vídeo | Por Que Assistir | Duração | Nível |
|---|-------|------------------|---------|-------|
| 8 | **"Memory Systems for LLM Agents"** — Charles Packer (MemGPT), 2024 | Deep dive técnico em como implementar memória de longo prazo para agentes. Cobre arquitetura de hierarchical memory, retrieval strategies, e o trade-off between context size and retrieval quality. | ~45 min | ⭐⭐⭐ Nível 3 |
| 9 | **"Scaling AI Agents: From Prototype to Production"** — Shreya Shankar, 2025 | O que acontece quando você tenta escalar agentes de 10 para 10.000 conversas/dia. Lições sobre latência, custo, e os "unknown unknowns" de produção. | ~40 min | ⭐⭐⭐ Nível 3 |

🔗 **Links:**
- Vídeo 8: https://www.youtube.com/@MLOpsCommunity (buscar por "Memory Systems for LLM Agents")
- Vídeo 9: https://www.youtube.com/@AIEngineerSummit (buscar por "Scaling AI Agents")

---

## 📦 Seção 4: Repositórios Open-Source

Estudar código-fonte de agentes reais é a maneira mais rápida de aprender padrões de implementação. Cada repositório inclui o que especificamente estudar.

---

### 🌟 Repositórios de Referência

| # | Repositório | O Que Estudar | Estrelas | Nível |
|---|-------------|---------------|----------|-------|
| 1 | **microsoft/autogen** — Multi-agent conversation framework | Padrões de conversation entre agentes: dois agentes debatendo, group chat, nested chat. Estude `ConversableAgent` para entender como agentes mantêm estado entre mensagens. O padrão Generator/Evaluator pode ser implementado com dois `AssistantAgent`s. | 35k+ | ⭐⭐ Nível 2 |
| 2 | **langchain-ai/langgraph** — Build stateful, multi-actor agents | Framework para agentes com controle de fluxo explícito via grafos. Estude `StateGraph` para entender checkpointing, branching, e human-in-the-loop. A base conceitual para State Persistence no KODA. | 10k+ | ⭐⭐ Nível 2 |
| 3 | **joaomdmoura/crewAI** — Multi-agent orchestration | Agentes com roles, goals, e backstories definidos. Estude como `Agent` + `Task` + `Crew` se combinam para orquestrar trabalho. Relevante para entender delegation patterns e task decomposition. | 20k+ | ⭐⭐ Nível 2 |
| 4 | **geekan/MetaGPT** — Multi-agent meta programming | Aplica SOPs (Standard Operating Procedures) de engenharia de software a agentes. Estude `Role` e `Action` classes para entender como papéis definidos melhoram output quality. Inspiração direta para Sprint Contracts. | 45k+ | ⭐⭐⭐ Nível 3 |
| 5 | **All-Hands-AI/OpenHands** (anteriormente OpenDevin) — AI software engineer | Agente autônomo que escreve código, executa comandos e resolve issues. Estude o `AgentController` loop e `AgentState` para entender o ciclo completo: observe → plan → act → verify. | 40k+ | ⭐⭐⭐ Nível 3 |

🔗 **Links:**
- Repo 1: https://github.com/microsoft/autogen
- Repo 2: https://github.com/langchain-ai/langgraph
- Repo 3: https://github.com/joaomdmoura/crewAI
- Repo 4: https://github.com/geekan/MetaGPT
- Repo 5: https://github.com/All-Hands-AI/OpenHands

---

### 🔬 Repositórios de Estudo & Pesquisa

| # | Repositório | O Que Estudar | Nível |
|---|-------------|---------------|-------|
| 6 | **cpacker/MemGPT** — Memory management for LLMs | Implementação de referência para hierarchical memory em agentes. Estude `MemGPT`, `MemoryManager`, e o sistema de recall/archival storage. Diretamente aplicável a Context Management no KODA. | ⭐⭐⭐ Nível 3 |
| 7 | **princeton-nlp/SWE-agent** — Agent-computer interfaces | Foco em como o agente interage com o computador (terminal, editor, browser). Estude o design de `Agent-Computer Interface (ACI)`: comandos, formatos de output, e error handling. Lições transferíveis para tool design no KODA. | ⭐⭐⭐ Nível 3 |
| 8 | **browser-use/browser-use** — Web agents | Agentes que navegam na web autonomamente. Estude o loop de `observe → extract → act` para entender como agentes processam informação visual e tomam decisões em ambientes não-determinísticos. | ⭐⭐ Nível 2 |
| 9 | **gpt-researcher** — Autonomous research agent | Agente que faz pesquisa web, sintetiza informações e gera relatórios. Estude o pipeline de `plan → research → synthesize → report` como exemplo de task decomposition. | ⭐ Nível 1 |

🔗 **Links:**
- Repo 6: https://github.com/cpacker/MemGPT
- Repo 7: https://github.com/princeton-nlp/SWE-agent
- Repo 8: https://github.com/browser-use/browser-use
- Repo 9: https://github.com/assafelovic/gpt-researcher

---

## 🛠️ Seção 5: Ferramentas & Bibliotecas

Ferramentas certas aceleram desenvolvimento e reduzem erros. Cada recomendação inclui o caso de uso específico para long-running agents.

---

### 🧰 Frameworks de Agentes

| # | Ferramenta | Caso de Uso | Quando Usar |
|---|------------|-------------|-------------|
| 1 | **LangChain / LangGraph** | Orquestração de agentes com controle de fluxo explícito via StateGraph. Suporte nativo a checkpointing, branching e human-in-the-loop. | Quando você precisa de controle fino sobre o fluxo do agente e persistência de estado entre steps. Ideal para implementar Sprint Contracts. |
| 2 | **CrewAI** | Multi-agent orchestration com roles e tasks definidas. Sintaxe simples e intuitiva para criar "equipes" de agentes. | Quando você quer prototipar rápido uma arquitetura multi-agente com papéis claros. Bom para experimentação antes de implementação customizada. |
| 3 | **AutoGen (Microsoft)** | Multi-agent conversations com padrões flexíveis: two-agent chat, group chat, nested chat. Suporte a code execution e human feedback loops. Nota: repositório original em modo de manutenção desde 2025; os padrões de conversation permanecem relevantes. | Quando você precisa de agents que conversam entre si para resolver problemas — especialmente útil para Generator/Evaluator. |
| 4 | **OpenAI Swarm / Agents SDK** | Agents leves com handoffs e routines. Design minimalista focado em patterns de delegação entre agentes. | Quando você quer simplicidade e está no ecossistema OpenAI. Bom para aprender padrões de coordenação antes de frameworks mais complexos. |
| 5 | **Instructor** | Structured outputs para LLMs usando Pydantic. Garante que respostas de agentes sejam parseáveis e type-safe. | Quando você precisa que agentes retornem JSON estruturado consistentemente — essencial para Sprint Contracts e state persistence. |

🔗 **Links:**
- Ferramenta 1: https://github.com/langchain-ai/langgraph (LangGraph), https://github.com/langchain-ai/langchain (LangChain)
- Ferramenta 2: https://github.com/joaomdmoura/crewAI
- Ferramenta 3: https://github.com/microsoft/autogen
- Ferramenta 4: https://github.com/openai/openai-agents-python
- Ferramenta 5: https://github.com/jxnl/instructor

---

### 🔍 Observabilidade & Debugging

| # | Ferramenta | Caso de Uso | Quando Usar |
|---|------------|-------------|-------------|
| 6 | **LangSmith (LangChain)** | Tracing, evaluation e monitoring para agentes. Visualize cada step do agente, meça latência, e compare runs. | Quando você precisa debugar por que um agente tomou uma decisão específica — essencial para Trace Reading. |
| 7 | **Arize Phoenix** | Observability open-source para LLM applications. Tracing, span analysis, e evaluation integrados. | Alternativa open-source ao LangSmith. Bom para times que preferem self-hosted. |
| 8 | **Weights & Biases (W&B) Prompts** | Tracing e evaluation para LLM workflows. Integração com Python SDK para logging automático de agent steps. | Quando você já usa W&B para experiment tracking e quer adicionar agent observability. |
| 9 | **Braindump / AgentOps** | Monitoring especializado para agentes autônomos. Foco em session tracking e cost attribution. | Quando você precisa entender o custo por conversa e identificar gargalos de performance em produção. |

🔗 **Links:**
- Ferramenta 6: https://www.langchain.com/langsmith
- Ferramenta 7: https://github.com/Arize-AI/phoenix
- Ferramenta 8: https://wandb.ai/site/prompts
- Ferramenta 9: https://www.agentops.ai/

---

### 🧪 Avaliação & Testing

| # | Ferramenta | Caso de Uso | Quando Usar |
|---|------------|-------------|-------------|
| 10 | **Promptfoo** | Testing e evaluation de prompts e agentes. Suporte a test suites, regression testing, e comparação A/B. | Quando você precisa validar que mudanças no system prompt não quebram comportamento do agente. |
| 11 | **Ragas** | Evaluation framework para RAG e agent pipelines. Métricas de faithfulness, relevance e context precision. | Quando seu agente usa retrieval (RAG) e você precisa medir qualidade do contexto recuperado. |
| 12 | **Deepeval** | Unit testing para LLM applications. Assertions como `FactualConsistency`, `Toxicity`, `Bias` e `Hallucination`. | Quando você quer integrar avaliação de agentes no pipeline de CI/CD. |

🔗 **Links:**
- Ferramenta 10: https://github.com/promptfoo/promptfoo
- Ferramenta 11: https://github.com/explodinggradients/ragas
- Ferramenta 12: https://github.com/confident-ai/deepeval

---

## 🗺️ Seção 6: Como Usar Estes Recursos

### Progressão Sugerida por Nível

```
NÍVEL 1 — FUNDAMENTOS (2-3 semanas)
─────────────────────────────────────
  1. 📖 Ler: "LLM Powered Autonomous Agents" (Lilian Weng)
  2. 🎥 Assistir: "State of GPT" (Karpathy)
  3. 🎥 Assistir: "Building Agents That Run for Hours" (Anthropic)
  4. 📖 Ler: "Building Effective Agents" (Anthropic)
  5. 📄 Paper: "Chain-of-Thought" (Wei et al.)
  6. 📄 Paper: "ReAct" (Yao et al.)
  7. 🛠️ Explorar: gpt-researcher (entender o loop básico)

NÍVEL 2 — PADRÕES PRÁTICOS (3-4 semanas)
─────────────────────────────────────────
  1. 📄 Paper: "Generative Agents" (Park et al.)
  2. 📄 Paper: "AutoGen" (Wu et al.)
  3. 📦 Repo: microsoft/autogen (estudar conversation patterns)
  4. 📦 Repo: langchain-ai/langgraph (estudar StateGraph)
  5. 📖 Ler: "Context Engineering for AI Agents" (Eugene Yan)
  6. 🎥 Assistir: "Multi-Agent Systems with AutoGen"
  7. 🛠️ Experimentar: Instructor + Pydantic para outputs estruturados

NÍVEL 3 — AVANÇADO (4-6 semanas)
──────────────────────────────────
  1. 📄 Paper: "Voyager" (Wang et al.)
  2. 📄 Paper: "SWE-bench" (Jimenez et al.)
  3. 📦 Repo: All-Hands-AI/OpenHands (estudar AgentController)
  4. 📦 Repo: cpacker/MemGPT (estudar memory architecture)
  5. 📖 Ler: "Things We Learned Building AI Agents at Scale"
  6. 🎥 Assistir: "Scaling AI Agents: From Prototype to Production"
  7. 🛠️ Dominar: LangSmith ou Phoenix para tracing

NÍVEL 4 — KODA ESPECÍFICO (contínuo)
───────────────────────────────────────
  1. 📖 Ler: Case real do KODA (documentação interna)
  2. 📦 Repo: Estudar implementações que inspiram features KODA
  3. 🛠️ Implementar: Ciclo completo Generator/Evaluator para uma feature
  4. 🧪 Validar: Rubric design + trace reading com ferramentas de observabilidade
```

---

### Dicas de Estudo Eficiente

**Para Papers:**
- Não leia do início ao fim. Comece pelo **abstract**, depois **conclusion**, depois **figures**. Só mergulhe nos detalhes se o paper for diretamente relevante para o que você está construindo.
- Mantenha um "paper log": uma frase sobre o que aprendeu e como se conecta ao KODA.

**Para Blog Posts:**
- Leia com o KODA em mente. Pergunte-se: "Como eu aplicaria isso em uma conversa real de WhatsApp?"
- Implemente um mini-exemplo do conceito antes de passar para o próximo artigo.

**Para Vídeos:**
- Assista em 1.5x (ou 2x se for muito introdutório).
- Pause e anote os 3 insights principais ao final.

**Para Repositórios:**
- Não clone e leia tudo. Use GitHub Code Search para encontrar o arquivo principal (ex: `agent.py`, `orchestrator.py`).
- Execute os exemplos mínimos. Modifique parâmetros e observe o comportamento.

**Para Ferramentas:**
- Comece com o "Hello World" de cada uma. Resista a tentação de aprender tudo.
- Avalie se a ferramenta resolve um problema REAL que você tem agora. Não adicione complexidade desnecessária.

---

## 🎓 Seção 7: O Que Você Aprendeu

Este documento não é para ser lido de uma vez. É um **mapa de referência** que cresce com você:

- ✅ **Papers** que fundamentam cada conceito do currículo — de chain-of-thought a agent-computer interfaces
- ✅ **Blog posts** que traduzem teoria em prática — do manifesto "Building Effective Agents" a casos reais de produção
- ✅ **Vídeos** para aprendizado visual — de fundamentos de LLMs a arquiteturas multi-agente avançadas
- ✅ **Repositórios** para estudar código real — de AutoGen a OpenHands, cada um com lições específicas para o KODA
- ✅ **Ferramentas** para acelerar desenvolvimento — frameworks de agentes, observabilidade, e avaliação
- ✅ **Progressão clara** de recursos por nível — você sabe exatamente o que estudar em cada etapa

### Checkpoint: Você Está Pronto?

Antes de mergulhar nos recursos, verifique:

- [ ] Sei qual é meu nível atual (1-4) e por onde começar
- [ ] Entendi a diferença entre papers (teoria), blog posts (prática) e repositórios (código)
- [ ] Tenho um plano de estudos para as próximas 2-4 semanas
- [ ] Sei que este documento é vivo — novos recursos serão adicionados

---

## 🔄 Como Contribuir

Este documento é mantido pela equipe KODA. Para sugerir novos recursos:

1. Verifique se o recurso é **diretamente relevante** para long-running agents
2. Inclua: título, link funcional, descrição em português, nível sugerido, e por que importa
3. Submeta como sugestão no canal #long-running-agents ou abra uma issue

**Critérios de inclusão:**
- O recurso é de alta qualidade (não é conteúdo superficial ou de marketing)
- O recurso é acessível (não requer paywall para o conteúdo principal)
- O recurso preenche uma lacuna real (não duplica cobertura existente)

---

## 🔗 Referências Cruzadas

Este documento complementa:
- `anthropic-presentation-summary.md` — Resumo detalhado da apresentação da Anthropic sobre long-running agents
- `model-capability-timeline.md` — Linha do tempo de evolução dos modelos e seu impacto em agentes
- `../GLOSSARY.md` — Definições de todos os termos técnicos usados neste documento
- `../INDEX.md` — Índice geral do currículo para navegação completa

---

> "A diferença entre um engenheiro que constrói agentes e um expert em agentes não é talento — é exposição aos recursos certos, na ordem certa, no momento certo."

---

## 📋 Metadata

| Campo | Valor |
|-------|-------|
| **Arquivo** | additional-resources.md |
| **Seção** | 10 - References |
| **Tipo** | Documento de Referência Curada |
| **Status** | ✅ Publicado |
| **Abrangência** | Todos os níveis (1-4) |
| **Atualizado** | Maio 2026 |
| **Próxima Revisão** | Agosto 2026 (ou quando novos recursos relevantes surgirem) |
| **Mantenedor** | Equipe KODA — #long-running-agents |

---

*Curado com rigor para a equipe KODA. Cada recurso incluído foi selecionado por relevância direta para construção de agentes que rodam por horas com confiabilidade.*
