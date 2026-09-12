---
title: "Deep Agents Explained"
type: "extract"
source: "youtube"
video_id: "GbzEDgcuGJU"
url: "https://www.youtube.com/watch?v=GbzEDgcuGJU"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-deep-agents-explained--GbzEDgcuGJU.txt]]"
tags: ["harness", "harness-engineering", "agent-loop", "context-engineering", "context-management", "token-budgeting", "memory-architecture", "multi-agent", "agent-fleets", "runtime", "observability", "evals", "production", "model-selection", "permissions", "gate-design", "frameworks", "stack-tooling"]
thesis: "Deep Agents é um harness open-source da LangChain (sobre o runtime LangGraph) que estende o loop ReAct com planejamento, sub-agentes, file system/backends para progressive disclosure, sandboxes e compaction automática, capacitando agentes a executar tarefas longas e complexas em produção com human-in-the-loop, execução durável e observabilidade via LangSmith."
concepts: ["harness de agentes (suporte ao redor do loop modelo+tools)", "deep agents / tarefas de longa duração", "planning tool (todo-list para agentes)", "sub-agentes e delegação", "file system abstrato / backends (Notion, GitHub, bancos de dados, composite backend)", "progressive disclosure", "context engineering e offloading de inputs/outputs de tools", "summarização/compaction da janela de contexto (gatilho ~80-85% ou controlado pelo modelo)", "skills como prompts compartilháveis", "sandbox e execution environment (REPL/tool leve vs sandbox completo)", "human-in-the-loop e approval gates", "durable execution (rollback, replay, documentação de passos)", "streaming como primitiva de primeira classe", "observabilidade de traces longos e análise agregada de falhas", "arquiteturas multi-agente: router, sub-agents, skills/personas, swarm", "trade-off nº de tools vs nº de sub-agentes na precisão de seleção/roteamento", "custom middleware como escape hatch para lógica determinística/compliance", "model-agnostic routing por especialidade do modelo", "isolamento de sandbox: agente inteiro vs apenas tool calls (secrets vs latência)", "padrões de colaboração: MCP, A2A, programmatic tool calling"]
tools: ["Deep Agents (SDK)", "Deep Agent CLI", "LangChain v1", "LangGraph", "LangSmith", "LangSmith Deployments (agent service)", "create-agent (equivalente ao create_react_agent)", "Pydantic", "Claude Code", "Cursor Agents", "Notion", "GitHub", "Modal", "Daytona", "LiteLLM", "MCP", "A2A", "Skill Hub"]
people: ["Sydney (core maintainer de Deep Agents, ex-mantenedor de Pydantic/Pydantic AI)", "Jake (deployed engineer)", "LangChain", "Harrison Chase (CEO da LangChain, blog sobre paradigmas de sandbox)", "Lance (post 'Learning the Bigger Lesson')", "Anthropic", "OpenAI", "Google (Gemini)"]
claims: ["Coloque a complexidade no prompt: um prompt específico do use case é o principal fator de performance e um deep agent parte de ~5 linhas de código", "Configure evals quantitativos desde cedo para gerar um ciclo de auto-melhoria; sem evals é impossível validar se versões de prompt são melhores", "Descarregue outputs grandes de tools no file system e passe apenas referências, porque sumarizar inerentemente perde informação e desvia o agente do objetivo", "Use progressive disclosure: anuncie skills no prompt e carregue o conteúdo completo apenas quando necessário, evitando poluir o contexto", "Dispare compaction em torno de 80-85% da janela de contexto; há experimento dando ao próprio modelo o controle do momento de compactar", "A arquitetura de sub-agentes foi escolhida após mapear quatro padrões multi-agente (router, sub-agents, skills, swarm), mas sub-agentes aninhados demais sofrem de latência", "Existe um paralelo entre quantas tools um modelo suporta antes de errar a seleção e quantos sub-agentes suporta antes de errar o roteamento; profundidade só se justifica em espaços de problema muito grandes", "Rodar o agente inteiro no sandbox expõe API keys/secrets ao ambiente; executar só os tool calls no sandbox cruza a fronteira de rede e adiciona latência — o mercado ainda não convergiu", "Use custom middleware como escape hatch para passos determinísticos/compliance dentro do loop; workflows determinísticos (LangGraph) seguem válidos e são composíveis com deep agents em um único passo agêntico", "As descrições de tools também entram no prompt: mantenha-as organizadas e com bons e maus exemplos", "Roteie modelos por especialidade (ex.: Gemini para imagem/vídeo, Anthropic para SQL/código, OpenAI para escrita expressiva) aproveitando o harness model-agnostic para evitar lock-in", "Produção exige human-in-the-loop antes de ações sensíveis, durable execution com rollback/replay, streaming first-class e observabilidade com estatísticas agregadas de falha em traces com centenas de tool calls", "O custo de agentes longos vem majoritariamente das chamadas de modelo, não da infraestrutura, e agentes de pesquisa longos muitas vezes fazem menos chamadas que chatbots curtos"]
deep_dive: "medium"
deep_dive_reason: "Há densidade razoável de detalhe arquitetural acionável (offloading, compaction, trade-offs de sandbox e sub-agentes, middleware), mas o formato é introdutório e promocional do ecossistema LangChain, com pouca novidade além dos padrões já publicados."
---

# Deep Agents Explained

## Tese
Deep Agents é um harness open-source da LangChain (sobre o runtime LangGraph) que estende o loop ReAct com planejamento, sub-agentes, file system/backends para progressive disclosure, sandboxes e compaction automática, capacitando agentes a executar tarefas longas e complexas em produção com human-in-the-loop, execução durável e observabilidade via LangSmith.

## Conceitos-chave
- harness de agentes (suporte ao redor do loop modelo+tools)
- deep agents / tarefas de longa duração
- planning tool (todo-list para agentes)
- sub-agentes e delegação
- file system abstrato / backends (Notion, GitHub, bancos de dados, composite backend)
- progressive disclosure
- context engineering e offloading de inputs/outputs de tools
- summarização/compaction da janela de contexto (gatilho ~80-85% ou controlado pelo modelo)
- skills como prompts compartilháveis
- sandbox e execution environment (REPL/tool leve vs sandbox completo)
- human-in-the-loop e approval gates
- durable execution (rollback, replay, documentação de passos)
- streaming como primitiva de primeira classe
- observabilidade de traces longos e análise agregada de falhas
- arquiteturas multi-agente: router, sub-agents, skills/personas, swarm
- trade-off nº de tools vs nº de sub-agentes na precisão de seleção/roteamento
- custom middleware como escape hatch para lógica determinística/compliance
- model-agnostic routing por especialidade do modelo
- isolamento de sandbox: agente inteiro vs apenas tool calls (secrets vs latência)
- padrões de colaboração: MCP, A2A, programmatic tool calling

## Ferramentas & pessoas
**Ferramentas:** Deep Agents (SDK), Deep Agent CLI, LangChain v1, LangGraph, LangSmith, LangSmith Deployments (agent service), create-agent (equivalente ao create_react_agent), Pydantic, Claude Code, Cursor Agents, Notion, GitHub, Modal, Daytona, LiteLLM, MCP, A2A, Skill Hub

**Pessoas/orgs:** Sydney (core maintainer de Deep Agents, ex-mantenedor de Pydantic/Pydantic AI), Jake (deployed engineer), LangChain, Harrison Chase (CEO da LangChain, blog sobre paradigmas de sandbox), Lance (post 'Learning the Bigger Lesson'), Anthropic, OpenAI, Google (Gemini)

## Claims acionáveis
- Coloque a complexidade no prompt: um prompt específico do use case é o principal fator de performance e um deep agent parte de ~5 linhas de código
- Configure evals quantitativos desde cedo para gerar um ciclo de auto-melhoria; sem evals é impossível validar se versões de prompt são melhores
- Descarregue outputs grandes de tools no file system e passe apenas referências, porque sumarizar inerentemente perde informação e desvia o agente do objetivo
- Use progressive disclosure: anuncie skills no prompt e carregue o conteúdo completo apenas quando necessário, evitando poluir o contexto
- Dispare compaction em torno de 80-85% da janela de contexto; há experimento dando ao próprio modelo o controle do momento de compactar
- A arquitetura de sub-agentes foi escolhida após mapear quatro padrões multi-agente (router, sub-agents, skills, swarm), mas sub-agentes aninhados demais sofrem de latência
- Existe um paralelo entre quantas tools um modelo suporta antes de errar a seleção e quantos sub-agentes suporta antes de errar o roteamento; profundidade só se justifica em espaços de problema muito grandes
- Rodar o agente inteiro no sandbox expõe API keys/secrets ao ambiente; executar só os tool calls no sandbox cruza a fronteira de rede e adiciona latência — o mercado ainda não convergiu
- Use custom middleware como escape hatch para passos determinísticos/compliance dentro do loop; workflows determinísticos (LangGraph) seguem válidos e são composíveis com deep agents em um único passo agêntico
- As descrições de tools também entram no prompt: mantenha-as organizadas e com bons e maus exemplos
- Roteie modelos por especialidade (ex.: Gemini para imagem/vídeo, Anthropic para SQL/código, OpenAI para escrita expressiva) aproveitando o harness model-agnostic para evitar lock-in
- Produção exige human-in-the-loop antes de ações sensíveis, durable execution com rollback/replay, streaming first-class e observabilidade com estatísticas agregadas de falha em traces com centenas de tool calls
- O custo de agentes longos vem majoritariamente das chamadas de modelo, não da infraestrutura, e agentes de pesquisa longos muitas vezes fazem menos chamadas que chatbots curtos

> **Deep dive:** `medium` — Há densidade razoável de detalhe arquitetural acionável (offloading, compaction, trade-offs de sandbox e sub-agentes, middleware), mas o formato é introdutório e promocional do ecossistema LangChain, com pouca novidade além dos padrões já publicados.
