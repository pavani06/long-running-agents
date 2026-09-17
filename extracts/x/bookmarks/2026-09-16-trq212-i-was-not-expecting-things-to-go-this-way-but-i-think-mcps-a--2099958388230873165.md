---
title: "MCP vs CLI para integrações de agentes"
type: "extract"
source: "x"
status_id: "2099958388230873165"
handle: "trq212"
url: "https://x.com/trq212/status/2099958388230873165"
created_at: "2026-09-15T20:27:49.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-trq212-i-was-not-expecting-things-to-go-this-way-but-i-think-mcps-a--2099958388230873165.json]]"
tags: ["agent-tooling", "agents", "arquitetura", "stack-tooling"]
topic: "MCP vs CLI para integrações de agentes"
summary: "Opinião de que MCPs superam CLIs na maioria das integrações de agentes porque os modelos melhoraram muito em tool calling, ferramentas podem ser diferidas e o MCP agora é stateless. Vale salvar como diretriz prática de arquitetura de tooling para agentes."
key_points: ["Modelos atuais ficaram muito melhores em tool calling, reduzindo a vantagem de usar CLIs (texto livre) como interface de integração", "MCP agora suporta deferred tools e é stateless, eliminando objeções anteriores de custo/complexidade de contexto", "Para compor ou filtrar dados, o padrão recomendado é expor parâmetros como query nas próprias ferramentas MCP, em vez de fazer composição no modelo", "A conclusão prática: na dúvida entre expor um CLI ou um servidor MCP ao agente, prefira MCP para a maioria dos casos"]
entities: ["MCP (Model Context Protocol)", "CLI", "@trq212"]
content_type: "opinion"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
---

# MCP vs CLI para integrações de agentes

**@trq212** · [2099958388230873165](https://x.com/trq212/status/2099958388230873165) · `opinion`

## Resumo
Opinião de que MCPs superam CLIs na maioria das integrações de agentes porque os modelos melhoraram muito em tool calling, ferramentas podem ser diferidas e o MCP agora é stateless. Vale salvar como diretriz prática de arquitetura de tooling para agentes.

## Pontos-chave
- Modelos atuais ficaram muito melhores em tool calling, reduzindo a vantagem de usar CLIs (texto livre) como interface de integração
- MCP agora suporta deferred tools e é stateless, eliminando objeções anteriores de custo/complexidade de contexto
- Para compor ou filtrar dados, o padrão recomendado é expor parâmetros como query nas próprias ferramentas MCP, em vez de fazer composição no modelo
- A conclusão prática: na dúvida entre expor um CLI ou um servidor MCP ao agente, prefira MCP para a maioria dos casos

## Entidades
MCP (Model Context Protocol), CLI, @trq212

> **Revisit:** `medium` · **fonte:** `tweet`
