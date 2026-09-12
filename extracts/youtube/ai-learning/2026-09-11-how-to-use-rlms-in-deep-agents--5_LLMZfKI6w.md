---
title: "How to use RLMs in Deep Agents"
type: "extract"
source: "youtube"
video_id: "5_LLMZfKI6w"
url: "https://www.youtube.com/watch?v=5_LLMZfKI6w"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-use-rlms-in-deep-agents--5_LLMZfKI6w.txt]]"
tags: ["harness", "context-engineering", "context-management", "agent-loop", "multi-agent", "agent-fleets", "agent-tooling", "evals", "classification", "token-budgeting", "agentic-coding"]
thesis: "Modelos de linguagem recursivos (RLMs) — agentes que escrevem e executam código para chamar a si mesmos e a subagentes — permitem orquestração determinística de dividir-e-conquistar com contexto em variáveis/arquivos, superando agentes comuns em tarefas de agregação de dados de contexto longo."
concepts: ["Modelos de linguagem recursivos (RLMs)", "Auto-recursão via código", "Orquestração de agentes em código em vez de prompts", "Contexto em variáveis e arquivos vs. janela de contexto", "Estratégia de dividir e conquistar", "Cobertura determinística de dados em escala", "Orquestração sob medida com primitivas de código (loops, fan-out, pipelining)", "Perda de informação por sumarização em conversas longas", "Code interpreter como superfície leve de execução", "Função task para spawn de subagentes", "Middleware de code interpreter / code mode", "Palavra-chave 'workflow' para disparar RLMs", "Padrão de torneio para seleção de melhores candidatos", "Dataset Oolong (raciocínio de contexto longo e agregação de dados)", "Classificação ag_news em 4 categorias (World, Sports, Science and Tech, Business)", "Perguntas distribucionais: contagem, filtro por usuário, raciocínio temporal", "Desistência precoce do modelo sob sobrecarga de contexto", "Trade-offs de latência e custo de tokens", "Skills como otimização de custo de tokens", "Diferença de desempenho entre 64k e 128k tokens de contexto"]
tools: ["LangChain deep agents", "Code interpreter middleware", "create_deep_agent", "dcode", "JSEval", "Oolong dataset", "ag_news dataset"]
people: ["Sydney", "LangChain"]
claims: ["Dê ao agente principal acesso a um code interpreter contendo uma função task, para que ele escreva código que chama subagentes, cercado por código de preparação e agregação de dados", "Habilite RLMs passando o middleware de code interpreter ao create_deep_agent para ativar o code mode", "A palavra-chave 'workflow' no prompt dispara o uso de RLMs em deep agents", "Em 128k tokens de contexto no Oolong, o deep agent com RLM supera significativamente o agente puro; em 64k a diferença é pequena", "Agentes puros desistem cedo de tarefas de dados densos, respondendo 'não consigo responder exatamente' por sobrecarga de contexto", "RLMs têm trade-offs de latência mais lenta e custo de tokens mais alto, mas o design de skills específicas poderia reduzir token count e custo significativamente", "Use torneios com fan-out de subagentes como padrão de seleção quando houver muitos candidatos gerados em paralelo"]
deep_dive: "high"
deep_dive_reason: "Apresenta um primitivo arquitetural novo (auto-recursão via code interpreter) com detalhes concretos de implementação no harness deep agents, evidência de eval em 128k de contexto e trade-offs de custo acionáveis."
---

# How to use RLMs in Deep Agents

## Tese
Modelos de linguagem recursivos (RLMs) — agentes que escrevem e executam código para chamar a si mesmos e a subagentes — permitem orquestração determinística de dividir-e-conquistar com contexto em variáveis/arquivos, superando agentes comuns em tarefas de agregação de dados de contexto longo.

## Conceitos-chave
- Modelos de linguagem recursivos (RLMs)
- Auto-recursão via código
- Orquestração de agentes em código em vez de prompts
- Contexto em variáveis e arquivos vs. janela de contexto
- Estratégia de dividir e conquistar
- Cobertura determinística de dados em escala
- Orquestração sob medida com primitivas de código (loops, fan-out, pipelining)
- Perda de informação por sumarização em conversas longas
- Code interpreter como superfície leve de execução
- Função task para spawn de subagentes
- Middleware de code interpreter / code mode
- Palavra-chave 'workflow' para disparar RLMs
- Padrão de torneio para seleção de melhores candidatos
- Dataset Oolong (raciocínio de contexto longo e agregação de dados)
- Classificação ag_news em 4 categorias (World, Sports, Science and Tech, Business)
- Perguntas distribucionais: contagem, filtro por usuário, raciocínio temporal
- Desistência precoce do modelo sob sobrecarga de contexto
- Trade-offs de latência e custo de tokens
- Skills como otimização de custo de tokens
- Diferença de desempenho entre 64k e 128k tokens de contexto

## Ferramentas & pessoas
**Ferramentas:** LangChain deep agents, Code interpreter middleware, create_deep_agent, dcode, JSEval, Oolong dataset, ag_news dataset

**Pessoas/orgs:** Sydney, LangChain

## Claims acionáveis
- Dê ao agente principal acesso a um code interpreter contendo uma função task, para que ele escreva código que chama subagentes, cercado por código de preparação e agregação de dados
- Habilite RLMs passando o middleware de code interpreter ao create_deep_agent para ativar o code mode
- A palavra-chave 'workflow' no prompt dispara o uso de RLMs em deep agents
- Em 128k tokens de contexto no Oolong, o deep agent com RLM supera significativamente o agente puro; em 64k a diferença é pequena
- Agentes puros desistem cedo de tarefas de dados densos, respondendo 'não consigo responder exatamente' por sobrecarga de contexto
- RLMs têm trade-offs de latência mais lenta e custo de tokens mais alto, mas o design de skills específicas poderia reduzir token count e custo significativamente
- Use torneios com fan-out de subagentes como padrão de seleção quando houver muitos candidatos gerados em paralelo

> **Deep dive:** `high` — Apresenta um primitivo arquitetural novo (auto-recursão via code interpreter) com detalhes concretos de implementação no harness deep agents, evidência de eval em 128k de contexto e trade-offs de custo acionáveis.
