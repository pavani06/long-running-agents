---
title: "PydanticAI - The NEW Agent Builder on the Block"
type: "extract"
source: "youtube"
video_id: "UnH7S5044GA"
url: "https://www.youtube.com/watch?v=UnH7S5044GA"
channel: "Sam Witteveen"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-pydanticai-the-new-agent-builder-on-the-block--UnH7S5044GA.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "frameworks", "stack-tooling", "model-selection", "context-management", "memory-architecture", "observability", "tracing", "runtime", "state", "arquitetura", "analise", "token-budgeting", "production"]
thesis: "O Pydantic AI é um novo framework de agentes/LLMs construído pela equipe do Pydantic com validação de schemas como base, oferecendo saída estruturada, injeção de dependências, prompts dinâmicos, histórico de mensagens em Python puro e agnosticidade de modelo, prometendo menos código que LangChain/LangGraph/LlamaIndex."
concepts: ["Validação de schemas com Pydantic como base para saída estruturada de LLMs", "Structured output e function calling com conformidade a schema", "Model-agnostic (OpenAI, Gemini, Grok; Anthropic em breve)", "Injeção de dependências para prompts de sistema e tools", "Prompts de sistema dinâmicos via decorators", "Controle de fluxo e composição de agentes em Python puro (vanilla)", "Gerenciamento de histórico de mensagens como lista Python (trimming, exportação JSON, memória)", "Transferência de histórico entre LLMs diferentes", "Type safety por design", "Biblioteca assíncrona (exige nest_asyncio no Colab)", "Anexação de tools via decorator @agent.tool", "Contabilização de tokens por tipo, incluindo reasoning tokens (o1)", "Observabilidade opcional via LogFire"]
tools: ["Pydantic", "Pydantic AI", "Instructor", "LangChain", "LangGraph", "LlamaIndex", "LogFire", "LangSmith", "Swarm", "OpenAI GPT-4o", "Gemini 1.5 Flash", "Gemini 1.5 Pro", "Google Vertex AI", "Grok API", "Anthropic", "Google Colab", "nest_asyncio"]
people: ["Equipe do Pydantic (PydanticAI)", "LangChain", "LlamaIndex", "OpenAI", "Google", "Anthropic"]
claims: ["A essência de um framework de agentes é garantir que os outputs do modelo conformem a um schema utilizável programaticamente — e Pydantic AI nasce dessa constatação", "Saída estruturada fica trivial: basta definir uma classe Pydantic como result_type; adicionar campos à classe estende automaticamente o output retornado", "O modelo pode ser trocado em runtime via agent.model, e prompts de sistema podem ser injetados dinamicamente via decorator sem recriar o agente", "O histórico de mensagens é uma lista Python simples, permitindo trimming seletivo, exportação para JSON e uso como memória entre chamadas", "O histórico pode ser transferido entre LLMs distintos (ex.: OpenAI para Gemini) no meio de uma conversa sem quebra", "Tools são anexadas via decorator @agent.tool, com dependências (API keys, clients) injetadas via contexto do agente", "A validação com Pydantic funciona mesmo durante streaming de respostas", "Relatórios de uso detalham tokens por tipo, incluindo reasoning tokens em modelos o1 e audio tokens", "A integração com LogFire é opcional, não obrigatória", "Para rodar no Colab é preciso instalar nest_asyncio e reiniciar o notebook, pois a biblioteca é assíncrona", "Para produção, o autor costuma recriar protótipos de LangGraph em Python puro; frameworks como Pydantic AI e Swarm eliminam esse passo por usarem Python puro desde o início", "Para muitos casos de uso, é provável obter resultados com bem menos código que em outros agent frameworks graças às abstrações simples e Pythonic"]
deep_dive: "medium"
deep_dive_reason: "É um tutorial prático de lançamento com padrões acionáveis concretos (injeção de dependências, histórico como lista, troca de modelo em runtime, tool calling), porém sem profundidade em arquitetura avançada, evals, governança ou fleets."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-we-ve-been-building-ai-agents-wrong-until-now--pC17ge_2n0Q|We've Been Building AI Agents WRONG Until Now]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-an-agent-in-10-mins-with-ai-sdk-5-with-nico-albanese-from-vercel-ai-demo-d--TjAbtsPC-Sw|Build An Agent in 10 mins with AI SDK 5 with Nico Albanese from Vercel, AI Demo Days]]", "[[extracts/youtube/ai-learning/2026-09-11-deep-agents-explained--GbzEDgcuGJU|Deep Agents Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-this-ai-agent-can-do-basically-everything-agent-zero--kTs3kDlKc8w|This AI Agent can do basically everything - Agent Zero]]"]
theme: "Agentes de IA No-Code"
---

# PydanticAI - The NEW Agent Builder on the Block

## Tese
O Pydantic AI é um novo framework de agentes/LLMs construído pela equipe do Pydantic com validação de schemas como base, oferecendo saída estruturada, injeção de dependências, prompts dinâmicos, histórico de mensagens em Python puro e agnosticidade de modelo, prometendo menos código que LangChain/LangGraph/LlamaIndex.

## Conceitos-chave
- Validação de schemas com Pydantic como base para saída estruturada de LLMs
- Structured output e function calling com conformidade a schema
- Model-agnostic (OpenAI, Gemini, Grok; Anthropic em breve)
- Injeção de dependências para prompts de sistema e tools
- Prompts de sistema dinâmicos via decorators
- Controle de fluxo e composição de agentes em Python puro (vanilla)
- Gerenciamento de histórico de mensagens como lista Python (trimming, exportação JSON, memória)
- Transferência de histórico entre LLMs diferentes
- Type safety por design
- Biblioteca assíncrona (exige nest_asyncio no Colab)
- Anexação de tools via decorator @agent.tool
- Contabilização de tokens por tipo, incluindo reasoning tokens (o1)
- Observabilidade opcional via LogFire

## Ferramentas & pessoas
**Ferramentas:** Pydantic, Pydantic AI, Instructor, LangChain, LangGraph, LlamaIndex, LogFire, LangSmith, Swarm, OpenAI GPT-4o, Gemini 1.5 Flash, Gemini 1.5 Pro, Google Vertex AI, Grok API, Anthropic, Google Colab, nest_asyncio

**Pessoas/orgs:** Equipe do Pydantic (PydanticAI), LangChain, LlamaIndex, OpenAI, Google, Anthropic

## Claims acionáveis
- A essência de um framework de agentes é garantir que os outputs do modelo conformem a um schema utilizável programaticamente — e Pydantic AI nasce dessa constatação
- Saída estruturada fica trivial: basta definir uma classe Pydantic como result_type; adicionar campos à classe estende automaticamente o output retornado
- O modelo pode ser trocado em runtime via agent.model, e prompts de sistema podem ser injetados dinamicamente via decorator sem recriar o agente
- O histórico de mensagens é uma lista Python simples, permitindo trimming seletivo, exportação para JSON e uso como memória entre chamadas
- O histórico pode ser transferido entre LLMs distintos (ex.: OpenAI para Gemini) no meio de uma conversa sem quebra
- Tools são anexadas via decorator @agent.tool, com dependências (API keys, clients) injetadas via contexto do agente
- A validação com Pydantic funciona mesmo durante streaming de respostas
- Relatórios de uso detalham tokens por tipo, incluindo reasoning tokens em modelos o1 e audio tokens
- A integração com LogFire é opcional, não obrigatória
- Para rodar no Colab é preciso instalar nest_asyncio e reiniciar o notebook, pois a biblioteca é assíncrona
- Para produção, o autor costuma recriar protótipos de LangGraph em Python puro; frameworks como Pydantic AI e Swarm eliminam esse passo por usarem Python puro desde o início
- Para muitos casos de uso, é provável obter resultados com bem menos código que em outros agent frameworks graças às abstrações simples e Pythonic

> **Deep dive:** `medium` — É um tutorial prático de lançamento com padrões acionáveis concretos (injeção de dependências, histórico como lista, troca de modelo em runtime, tool calling), porém sem profundidade em arquitetura avançada, evals, governança ou fleets.
