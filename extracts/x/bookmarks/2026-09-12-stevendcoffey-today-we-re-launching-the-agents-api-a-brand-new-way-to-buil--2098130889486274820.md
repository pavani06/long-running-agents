---
title: "OpenAI Agents API launch"
type: "extract"
source: "x"
status_id: "2098130889486274820"
handle: "stevendcoffey"
url: "https://x.com/stevendcoffey/status/2098130889486274820"
created_at: "2026-09-10T19:26:00.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-stevendcoffey-today-we-re-launching-the-agents-api-a-brand-new-way-to-buil--2098130889486274820.json]]"
tags: ["agents", "harness", "agent-tooling", "context-management", "multi-agent", "token-budgeting"]
topic: "OpenAI Agents API launch"
summary: "OpenAI lança a Agents API em beta público, expondo via uma única chamada o mesmo harness e infraestrutura que rodam o Codex, com gerenciamento de contexto, uso eficiente de ferramentas e suporte multi-agente. Vale salvar como referência de plataforma para colocar agentes em produção sem construir o próprio harness."
key_points: ["Criar um agente pronto para produção em uma única chamada de API especificando task, model, tools e environment; OpenAI hospeda e mantém o harness open-source do Codex, com versionamento junto aos lançamentos de modelos", "Compute flexível: sandbox gerenciado pela OpenAI, infraestrutura própria/VPC, ou parceiros como Blaxel, Cloudflare, Daytona, DigitalOcean, E2B, Modal, Oracle, Runloop e Vercel, com opções de CPU/GPU/memória e perfis de cold-start e custo", "Context management com compaction automática ao aproximar do limite de contexto, permitindo workflows que atravessam múltiplas janelas de contexto sem lógica própria de compactação", "Tool search carrega definições de ferramentas sob demanda (reduzindo tokens e custo e preservando cache) e programmatic tool calling executa chamadas em paralelo, encadeia operações e filtra resultados em código; suporta MCP, funções customizadas e web search", "Multi-agent nativo: subagentes trabalham em paralelo cada um com seu próprio contexto, com o agente principal coordenando e consolidando resultados, sem orquestração própria; sem taxa adicional além de tokens e ferramentas usadas"]
entities: ["OpenAI", "Agents API", "Codex", "ChatGPT", "Blaxel", "Cloudflare", "Daytona", "DigitalOcean", "E2B", "Modal", "Oracle", "Runloop", "Vercel", "MCP", "Astra"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
links: ["https://openai.com/index/introducing-the-agents-api/"]
media: []
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-omarsar0-agents-api-is-a-bigger-deal-than-it-seems-openai-s-bet-on-ma--2098524621439914375|OpenAI Agents API e harness-as-a-service]]", "[[extracts/x/bookmarks/2026-09-12-svpino-the-frontieragent-framework-is-here-star-the-repo-https-t-co--2098489264749334565|FrontierAgent: runtime de agentes e evals]]", "[[extracts/x/bookmarks/2026-09-12-kevinwhinnery-the-era-of-the-dumb-token-pipe-is-ending-agent-harness-apis--2098444890602455431|Agent harness APIs como integração]]", "[[extracts/x/bookmarks/2026-09-12-xudong07452910-openai-skills-agents-md-blog-agent-engineering-astra-skill--2098655277197201752|OpenAI ensina Skills e AGENTS.md]]", "[[extracts/x/bookmarks/2026-09-12-simonw-here-s-my-attempt-at-explaining-what-chatgpt-work-can-actual--2094214737957691854|Capacidades do ChatGPT Work]]", "[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-chatgpt-now-everyone-can-put-data-to-work-were-introducing-a-new-dat--2098065296968011853|Data agent no ChatGPT Work]]", "[[extracts/x/bookmarks/2026-09-12-a16z-today-applied-intuition-is-launching-dana-an-agentic-platfor--2079585013482561548|Dana: plataforma agêntica de IA física]]", "[[extracts/x/bookmarks/2026-09-12-thsottiaux-more-opensource-goodness-we-have-just-released-a-cli-and-typ--2082241164850364555|Codex Security CLI e SDK]]", "[[extracts/x/bookmarks/2026-09-12-openai-now-available-chatgpt-for-financial-services-this-is-a-tailo--2098118191029624911|ChatGPT para serviços financeiros]]", "[[extracts/x/bookmarks/2026-09-12-simonw-wow-turns-out-another-openai-agent-swarm-was-busy-spamming-a--2098573718142452055|Ataque de agentes OpenAI ao RubyGems]]", "[[extracts/x/bookmarks/2026-09-12-openaidevs-python-allowed-for-rapid-prototyping-of-our-platform-to-supp--2098502018998649036|Python em escala na OpenAI]]", "[[extracts/x/bookmarks/2026-09-12-marwan_3atef-cloudflare-ai-gateway-custom-costs-finally-understand-prompt--2098027728624570486|Cloudflare AI Gateway custo com prompt caching]]", "[[extracts/x/bookmarks/2026-09-12-maxforai-nvidia-harness-sol-pi-nvlabs-sol-pi-scaling-auto-research-lo--2098050525279478059|NVIDIA open-sources SoL-Pi agent harness]]"]
theme: "Tooling e harness de agentes"
---

# OpenAI Agents API launch

**@stevendcoffey** · [2098130889486274820](https://x.com/stevendcoffey/status/2098130889486274820) · `announcement`

## Resumo
OpenAI lança a Agents API em beta público, expondo via uma única chamada o mesmo harness e infraestrutura que rodam o Codex, com gerenciamento de contexto, uso eficiente de ferramentas e suporte multi-agente. Vale salvar como referência de plataforma para colocar agentes em produção sem construir o próprio harness.

## Pontos-chave
- Criar um agente pronto para produção em uma única chamada de API especificando task, model, tools e environment; OpenAI hospeda e mantém o harness open-source do Codex, com versionamento junto aos lançamentos de modelos
- Compute flexível: sandbox gerenciado pela OpenAI, infraestrutura própria/VPC, ou parceiros como Blaxel, Cloudflare, Daytona, DigitalOcean, E2B, Modal, Oracle, Runloop e Vercel, com opções de CPU/GPU/memória e perfis de cold-start e custo
- Context management com compaction automática ao aproximar do limite de contexto, permitindo workflows que atravessam múltiplas janelas de contexto sem lógica própria de compactação
- Tool search carrega definições de ferramentas sob demanda (reduzindo tokens e custo e preservando cache) e programmatic tool calling executa chamadas em paralelo, encadeia operações e filtra resultados em código; suporta MCP, funções customizadas e web search
- Multi-agent nativo: subagentes trabalham em paralelo cada um com seu próprio contexto, com o agente principal coordenando e consolidando resultados, sem orquestração própria; sem taxa adicional além de tokens e ferramentas usadas

## Links
- https://openai.com/index/introducing-the-agents-api/

## Entidades
OpenAI, Agents API, Codex, ChatGPT, Blaxel, Cloudflare, Daytona, DigitalOcean, E2B, Modal, Oracle, Runloop, Vercel, MCP, Astra

> **Revisit:** `high` · **fonte:** `article`
