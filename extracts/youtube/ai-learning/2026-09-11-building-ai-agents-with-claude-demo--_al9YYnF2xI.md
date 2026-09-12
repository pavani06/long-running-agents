---
title: "Building AI Agents with Claude! (Demo)"
type: "extract"
source: "youtube"
video_id: "_al9YYnF2xI"
url: "https://www.youtube.com/watch?v=_al9YYnF2xI"
channel: "Elvis Saravia"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-building-ai-agents-with-claude-demo--_al9YYnF2xI.txt]]"
tags: ["agent-tooling", "agents", "stack-tooling", "documentation-publishing"]
thesis: "Ao conectar servidores MCP (GitHub e Brave Search) ao Claude Desktop, é possível montar um fluxo semi-automatizado — dirigido apenas por prompts — que busca notícias de IA, resume e publica os resultados como markdown em um repositório GitHub para curadoria pessoal e compartilhamento com a comunidade."
concepts: ["MCP (Model Context Protocol)", "servidores MCP e exposição de definições de ferramentas", "Claude Desktop como cliente de agentes", "agregação personalizada de notícias de IA", "curadoria humana no loop", "busca web via API", "integração programática com GitHub", "publicação de resultados em markdown", "automação orientada a prompts", "personal access token para autenticação"]
tools: ["Claude Desktop", "MCP servers", "Brave Web Search (API)", "GitHub MCP server", "GitHub", "ChatGPT (mencionado para comparação)"]
people: ["Anthropic", "OpenAI (ChatGPT)", "GitHub", "Brave", "Dev Agents (empresa citada na notícia)"]
claims: ["O Claude na versão web não tem acesso a navegador ou ferramentas, enquanto o ChatGPT oferece busca nativa — daí a necessidade de MCP servers para dar capacidades ao Claude Desktop", "Servidores MCP expõem as definições de capacidades das ferramentas, permitindo que o Claude invoque automaticamente APIs como a do Brave Search", "Com um personal access token configurado no GitHub MCP server, o agente cria repositórios e faz push de arquivos markdown sem intervenção manual", "Os resultados de busca do Brave ainda exigem refinamento de prompts e verificação de datas/fontes — o workflow funciona, mas a qualidade da busca não é perfeita", "Todo o processo (buscar → resumir → versionar em repo) pode ser totalmente automatizado, mas a curadoria manual foi mantida deliberadamente por causa dos newsletters", "A configuração inicial dos servidores MCP demandou tempo devido a problemas de setup, indicando que o ecossistema ainda está em estágio inicial"]
deep_dive: "low"
deep_dive_reason: "Trata-se de um demo casual de primeira experimentação com MCP servers no Claude Desktop, sem densidade arquitetural, avaliação ou novidade relevante para harness, evals, context-engineering ou governança."
---

# Building AI Agents with Claude! (Demo)

## Tese
Ao conectar servidores MCP (GitHub e Brave Search) ao Claude Desktop, é possível montar um fluxo semi-automatizado — dirigido apenas por prompts — que busca notícias de IA, resume e publica os resultados como markdown em um repositório GitHub para curadoria pessoal e compartilhamento com a comunidade.

## Conceitos-chave
- MCP (Model Context Protocol)
- servidores MCP e exposição de definições de ferramentas
- Claude Desktop como cliente de agentes
- agregação personalizada de notícias de IA
- curadoria humana no loop
- busca web via API
- integração programática com GitHub
- publicação de resultados em markdown
- automação orientada a prompts
- personal access token para autenticação

## Ferramentas & pessoas
**Ferramentas:** Claude Desktop, MCP servers, Brave Web Search (API), GitHub MCP server, GitHub, ChatGPT (mencionado para comparação)

**Pessoas/orgs:** Anthropic, OpenAI (ChatGPT), GitHub, Brave, Dev Agents (empresa citada na notícia)

## Claims acionáveis
- O Claude na versão web não tem acesso a navegador ou ferramentas, enquanto o ChatGPT oferece busca nativa — daí a necessidade de MCP servers para dar capacidades ao Claude Desktop
- Servidores MCP expõem as definições de capacidades das ferramentas, permitindo que o Claude invoque automaticamente APIs como a do Brave Search
- Com um personal access token configurado no GitHub MCP server, o agente cria repositórios e faz push de arquivos markdown sem intervenção manual
- Os resultados de busca do Brave ainda exigem refinamento de prompts e verificação de datas/fontes — o workflow funciona, mas a qualidade da busca não é perfeita
- Todo o processo (buscar → resumir → versionar em repo) pode ser totalmente automatizado, mas a curadoria manual foi mantida deliberadamente por causa dos newsletters
- A configuração inicial dos servidores MCP demandou tempo devido a problemas de setup, indicando que o ecossistema ainda está em estágio inicial

> **Deep dive:** `low` — Trata-se de um demo casual de primeira experimentação com MCP servers no Claude Desktop, sem densidade arquitetural, avaliação ou novidade relevante para harness, evals, context-engineering ou governança.
