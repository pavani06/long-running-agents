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
theme: "Agentic Coding com Claude"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-svpino-the-frontieragent-framework-is-here-star-the-repo-https-t-co--2098489264749334565|FrontierAgent: runtime de agentes e evals]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-also-see-our-open-source-reference-implementation-this-inclu--2095233747562180849|implementação de referência de agentes de comércio]]", "[[extracts/x/bookmarks/2026-09-16-tom_doerr-manages-your-obsidian-vault-with-a-crew-of-8-ai-agents-and-1--2099928503487517062|Crew de agentes AI para Obsidian]]", "[[extracts/x/bookmarks/2026-09-12-akitaonrails-acabei-de-soltar-a-versao-2-0-do-meu-ai-memory-e-eu-acho-que--2095186765535392249|ai-memory 2.0: memória compartilhada de agentes]]", "[[extracts/x/bookmarks/2026-09-16-liambraus-esto-es-una-locura-jack-dorsey-ex-ceo-de-twitter-acaba-de-la--2099852769389604973|Framework gratuito de agentes de IA]]", "[[extracts/x/bookmarks/2026-09-12-realfxw-multi-agent-victor-dibia-designing-multiagent-systems-picoag--2097956088792396200|Arquitetura multi-agente do zero]]", "[[extracts/x/bookmarks/2026-09-12-hnshah-im-late-to-this-party-but-https-t-co-2qvqvyamhq-just-showed--2098603214065332290|Lançamento agent-native com demo de Excel]]", "[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-timesfm-3-a-state-of-the-art-time-series-foundat--2094483372718580066|TimesFM-3: forecasting multivariado]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-i-just-published-my-complete-guide-to-reinforcement-learning--2091872097723359673|Guia completo de RL para LLMs]]", "[[extracts/x/bookmarks/2026-09-12-zostaff-a-jane-street-engineer-in-a-talk-on-how-an-exchange-is-actua--2081088443698868526|arquitetura de exchanges financeiras]]", "[[extracts/x/bookmarks/2026-09-12-thenarrator-a-prediction-markets-true-quality-metric-is-repricing-latenc--2082684092768751792|Métrica de qualidade em prediction markets]]", "[[extracts/x/bookmarks/2026-09-12-finviz_com-introducing-the-finviz-matrix-we-created-a-tool-that-no-othe--2098168161455514035|Lançamento Finviz Matrix]]"]
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
