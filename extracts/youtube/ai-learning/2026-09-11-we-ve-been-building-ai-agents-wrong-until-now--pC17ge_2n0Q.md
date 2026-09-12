---
title: "We've Been Building AI Agents WRONG Until Now"
type: "extract"
source: "youtube"
video_id: "pC17ge_2n0Q"
url: "https://www.youtube.com/watch?v=pC17ge_2n0Q"
channel: "Cole Medin"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-we-ve-been-building-ai-agents-wrong-until-now--pC17ge_2n0Q.txt]]"
tags: ["agent-tooling", "agents", "arquitetura", "context-management", "error-handling", "evals", "frameworks", "model-selection", "observability", "stack-tooling", "testes-qa", "tracing", "verification"]
thesis: "Pydantic AI, framework de agentes open-source em Python criado pelo time do Pydantic, viabiliza agentes de nível produtivo ao trazer validação de saídas, injeção de dependências tipada, retries, testes/avaliação com modelos mock e observabilidade via Logfire — recursos ausentes ou imaturos em LangChain, CrewAI, Swarm e construtores no-code."
concepts: ["agentes de nível produtivo (production-grade)", "validação de saída estruturada de LLMs com Pydantic", "injeção de dependências tipada e segura para ferramentas", "gerenciamento de contexto do agente (chaves de API, conexões de banco) sem expor credenciais ao LLM", "model-agnosticismo e troca automática de provedor pelo nome do modelo", "binding de ferramentas via decorator (@agent.tool)", "docstring como descrição de ferramenta para o LLM decidir quando/usar como", "retry automático de chamadas (model_retry) em erros de sobrecarga", "testes e avaliação com TestModel e dependências mockadas (sem custo de LLM)", "histórico de mensagens e memória de conversa multi-turno", "streaming de respostas", "execução 100% local de agentes via Ollama com base URL sobrescrita", "observabilidade e tracing de chamadas LLM/tool com spans do Logfire", "resultados com metadados (custo, histórico, mensagens)", "arquitetura de agente de busca web com Brave Search API e httpx"]
tools: ["Pydantic AI", "Pydantic", "LangChain", "CrewAI", "Swarm", "LlamaIndex", "FastAPI", "OpenAI API (GPT-4o)", "Anthropic API", "Google Gemini 1.5 Flash", "Ollama", "Qwen 2.5 Coder 32B", "Brave Search API", "Logfire", "Streamlit", "httpx", "python-dotenv (env)", "debug (pretty printing)"]
people: ["Pydantic (time/mantenedores)", "OpenAI", "Anthropic", "Google", "Brave", "Streamlit (empresa)"]
claims: ["Frameworks como LangChain, CrewAI, Swarm e builders no-code exigem trabalho adicional substancial para agentes maduros em produção", "O time do Pydantic já fornece a camada de validação usada por OpenAI, Anthropic, FastAPI, LangChain e CrewAI, o que fundamenta a confiabilidade do Pydantic AI", "Use injeção de dependências tipada para fornecer chaves de API e conexões às ferramentas sem nunca passá-las como argumento ao LLM", "Use TestModel/dependências mock para rodar testes unitários e de integração sem pagar por chamadas reais de LLM", "Configure model_retry para reintentar chamadas automaticamente em erros como overload do provedor", "Rode agentes 100% locais apontando um cliente OpenAI assíncrono customizado para localhost:11434 (Ollama)", "O nome do modelo resolve o provedor automaticamente (ex.: gemini-1.5-flash → Google; gpt-4o → OpenAI)", "Docstrings das funções definem para o LLM quando e como invocar cada ferramenta", "Passe o histórico de mensagens ao agent.run para habilitar memória conversacional multi-turno", "Logfire dá visibilidade completa (UI com spans por tool call) para depuração e monitoramento do agente", "Um agente de busca web funcional cabe em ~100 linhas com Pydantic AI + Brave Search API", "Na data do vídeo, streaming não funcionava via compatibilidade OpenAI do Ollama com Pydantic AI, exigindo GPT-4o para o demo com streaming", "Ao validar ferramentas, retorne sempre uma string: o retorno da tool é o que o LLM recebe para raciocinar e responder"]
deep_dive: "medium"
deep_dive_reason: "Tutorial prático com insights acionáveis relevantes a context-engineering (DI), evals (TestModel) e observabilidade (Logfire), mas sem novidade arquitetural profunda nem cobertura de harness, fleets ou governança além do nível introdutório de um único framework."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-pydanticai-the-new-agent-builder-on-the-block--UnH7S5044GA|PydanticAI - The NEW Agent Builder on the Block]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-an-agent-in-10-mins-with-ai-sdk-5-with-nico-albanese-from-vercel-ai-demo-d--TjAbtsPC-Sw|Build An Agent in 10 mins with AI SDK 5 with Nico Albanese from Vercel, AI Demo Days]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-production-ai-playbook-deploying-agents-at-enterprise-scale-sandipan-bhaumik--ObTPqBGsEbA|The Production AI Playbook: Deploying Agents at Enterprise Scale — Sandipan Bhaumik, Databricks]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]"]
theme: "Agentes de IA No-Code"
---

# We've Been Building AI Agents WRONG Until Now

## Tese
Pydantic AI, framework de agentes open-source em Python criado pelo time do Pydantic, viabiliza agentes de nível produtivo ao trazer validação de saídas, injeção de dependências tipada, retries, testes/avaliação com modelos mock e observabilidade via Logfire — recursos ausentes ou imaturos em LangChain, CrewAI, Swarm e construtores no-code.

## Conceitos-chave
- agentes de nível produtivo (production-grade)
- validação de saída estruturada de LLMs com Pydantic
- injeção de dependências tipada e segura para ferramentas
- gerenciamento de contexto do agente (chaves de API, conexões de banco) sem expor credenciais ao LLM
- model-agnosticismo e troca automática de provedor pelo nome do modelo
- binding de ferramentas via decorator (@agent.tool)
- docstring como descrição de ferramenta para o LLM decidir quando/usar como
- retry automático de chamadas (model_retry) em erros de sobrecarga
- testes e avaliação com TestModel e dependências mockadas (sem custo de LLM)
- histórico de mensagens e memória de conversa multi-turno
- streaming de respostas
- execução 100% local de agentes via Ollama com base URL sobrescrita
- observabilidade e tracing de chamadas LLM/tool com spans do Logfire
- resultados com metadados (custo, histórico, mensagens)
- arquitetura de agente de busca web com Brave Search API e httpx

## Ferramentas & pessoas
**Ferramentas:** Pydantic AI, Pydantic, LangChain, CrewAI, Swarm, LlamaIndex, FastAPI, OpenAI API (GPT-4o), Anthropic API, Google Gemini 1.5 Flash, Ollama, Qwen 2.5 Coder 32B, Brave Search API, Logfire, Streamlit, httpx, python-dotenv (env), debug (pretty printing)

**Pessoas/orgs:** Pydantic (time/mantenedores), OpenAI, Anthropic, Google, Brave, Streamlit (empresa)

## Claims acionáveis
- Frameworks como LangChain, CrewAI, Swarm e builders no-code exigem trabalho adicional substancial para agentes maduros em produção
- O time do Pydantic já fornece a camada de validação usada por OpenAI, Anthropic, FastAPI, LangChain e CrewAI, o que fundamenta a confiabilidade do Pydantic AI
- Use injeção de dependências tipada para fornecer chaves de API e conexões às ferramentas sem nunca passá-las como argumento ao LLM
- Use TestModel/dependências mock para rodar testes unitários e de integração sem pagar por chamadas reais de LLM
- Configure model_retry para reintentar chamadas automaticamente em erros como overload do provedor
- Rode agentes 100% locais apontando um cliente OpenAI assíncrono customizado para localhost:11434 (Ollama)
- O nome do modelo resolve o provedor automaticamente (ex.: gemini-1.5-flash → Google; gpt-4o → OpenAI)
- Docstrings das funções definem para o LLM quando e como invocar cada ferramenta
- Passe o histórico de mensagens ao agent.run para habilitar memória conversacional multi-turno
- Logfire dá visibilidade completa (UI com spans por tool call) para depuração e monitoramento do agente
- Um agente de busca web funcional cabe em ~100 linhas com Pydantic AI + Brave Search API
- Na data do vídeo, streaming não funcionava via compatibilidade OpenAI do Ollama com Pydantic AI, exigindo GPT-4o para o demo com streaming
- Ao validar ferramentas, retorne sempre uma string: o retorno da tool é o que o LLM recebe para raciocinar e responder

> **Deep dive:** `medium` — Tutorial prático com insights acionáveis relevantes a context-engineering (DI), evals (TestModel) e observabilidade (Logfire), mas sem novidade arquitetural profunda nem cobertura de harness, fleets ou governança além do nível introdutório de um único framework.
