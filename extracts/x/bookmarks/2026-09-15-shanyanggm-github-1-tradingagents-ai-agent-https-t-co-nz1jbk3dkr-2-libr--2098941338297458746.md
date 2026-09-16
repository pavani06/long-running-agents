---
title: "Framework multi-agente de trading LLM"
type: "extract"
source: "x"
status_id: "2098941338297458746"
handle: "shanyanggm"
url: "https://x.com/shanyanggm/status/2098941338297458746"
created_at: "2026-09-13T01:06:26.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-15-shanyanggm-github-1-tradingagents-ai-agent-https-t-co-nz1jbk3dkr-2-libr--2098941338297458746.json]]"
tags: ["agents", "multi-agent", "agentes-orquestracao", "frameworks", "investimentos", "memory-architecture", "state", "model-selection"]
topic: "Framework multi-agente de trading LLM"
summary: "TradingAgents é um framework open-source (TauricResearch, construído sobre LangGraph) que simula uma mesa de trading com agentes LLM especializados — analistas fundamentalista, sentimento, notícias e técnico, debatedores bull/bear, gestão de risco e portfolio manager — emitindo decisões de trade. O tweet curia projetos gratuitos no GitHub que substituem software pago; o conteúdo denso está no README do TradingAgents."
key_points: ["Arquitetura espelha uma firma de trading: equipe de analistas (fundamentos, sentimento via StockTwits/Reddit, notícias/macro, técnico com MACD/RSI), pesquisadores bull/bear em debates estruturados, Research Manager, Trader, time de risco e Portfolio Manager que aprova/rejeita a ordem no exchange simulado", "Multi-provider via configuração (OpenAI, Gemini, Claude, Grok, DeepSeek, Qwen, GLM, MiniMax, OpenRouter, Ollama local, Azure, Bedrock) com separação deep_think_llm/quick_think_llm e backend openai_compatible para vLLM/LM Studio/llama.cpp", "Memória persistente: decision log em ~/.tradingagents/memory/trading_memory.md registra cada decisão; na execução seguinte do mesmo ticker busca retorno realizado (raw e alpha vs SPY), gera reflexão e injeta lições no prompt do Portfolio Manager; checkpoint resume opt-in via LangGraph com SQLite por ticker", "Releases recentes focam correção de look-ahead/point-in-time (Alpha Vantage, FRED, sentimento social, decision-log memory), price grounding do Trader e fidelidade de datas no backtesting — preocupação central com correção de dados para pesquisa", "Documenta não-determinismo: sampling de LLM (pior em modelos reasoning), drift de dados sociais/notícias em tempo real; mitiga com temperatura baixa ou modelos non-reasoning; explicitamente ferramenta de pesquisa, não conselho financeiro"]
entities: ["TradingAgents", "TauricResearch", "LangGraph", "LibreChat", "HeyGen", "OpenAI", "Anthropic", "Google Gemini", "DeepSeek", "Ollama", "OpenRouter", "AWS Bedrock", "Azure OpenAI", "Alpha Vantage", "FRED"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/TauricResearch/TradingAgents", "https://github.com/danny-avila/LibreChat"]
media: ["https://pbs.twimg.com/media/HSDquaUbIAARiTF.jpg"]
---

# Framework multi-agente de trading LLM

**@shanyanggm** · [2098941338297458746](https://x.com/shanyanggm/status/2098941338297458746) · `tool`

## Resumo
TradingAgents é um framework open-source (TauricResearch, construído sobre LangGraph) que simula uma mesa de trading com agentes LLM especializados — analistas fundamentalista, sentimento, notícias e técnico, debatedores bull/bear, gestão de risco e portfolio manager — emitindo decisões de trade. O tweet curia projetos gratuitos no GitHub que substituem software pago; o conteúdo denso está no README do TradingAgents.

## Pontos-chave
- Arquitetura espelha uma firma de trading: equipe de analistas (fundamentos, sentimento via StockTwits/Reddit, notícias/macro, técnico com MACD/RSI), pesquisadores bull/bear em debates estruturados, Research Manager, Trader, time de risco e Portfolio Manager que aprova/rejeita a ordem no exchange simulado
- Multi-provider via configuração (OpenAI, Gemini, Claude, Grok, DeepSeek, Qwen, GLM, MiniMax, OpenRouter, Ollama local, Azure, Bedrock) com separação deep_think_llm/quick_think_llm e backend openai_compatible para vLLM/LM Studio/llama.cpp
- Memória persistente: decision log em ~/.tradingagents/memory/trading_memory.md registra cada decisão; na execução seguinte do mesmo ticker busca retorno realizado (raw e alpha vs SPY), gera reflexão e injeta lições no prompt do Portfolio Manager; checkpoint resume opt-in via LangGraph com SQLite por ticker
- Releases recentes focam correção de look-ahead/point-in-time (Alpha Vantage, FRED, sentimento social, decision-log memory), price grounding do Trader e fidelidade de datas no backtesting — preocupação central com correção de dados para pesquisa
- Documenta não-determinismo: sampling de LLM (pior em modelos reasoning), drift de dados sociais/notícias em tempo real; mitiga com temperatura baixa ou modelos non-reasoning; explicitamente ferramenta de pesquisa, não conselho financeiro

## Links
- https://github.com/TauricResearch/TradingAgents
- https://github.com/danny-avila/LibreChat

## Entidades
TradingAgents, TauricResearch, LangGraph, LibreChat, HeyGen, OpenAI, Anthropic, Google Gemini, DeepSeek, Ollama, OpenRouter, AWS Bedrock, Azure OpenAI, Alpha Vantage, FRED

> **Revisit:** `high` · **fonte:** `article`
