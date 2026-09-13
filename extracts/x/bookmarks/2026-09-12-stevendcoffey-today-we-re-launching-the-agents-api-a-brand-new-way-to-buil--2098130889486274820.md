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
