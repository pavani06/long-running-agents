---
title: "Compressão de contexto em sessões Claude"
type: "extract"
source: "x"
status_id: "2100739055923425589"
handle: "altryne"
url: "https://x.com/altryne/status/2100739055923425589"
created_at: "2026-09-18T00:09:55.000Z"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-19-altryne-this-is-actually-insane-this-uses-typesafeai-jev-model-as-a--2100739055923425589.json]]"
tags: ["context-engineering", "context-management", "token-budgeting", "agent-tooling", "performance", "stack-tooling"]
topic: "Compressão de contexto em sessões Claude"
summary: "Plugin que usa o modelo Jev da Typesafe AI dentro do Claude para revisar e remover tool calls desnecessárias, comprimindo a sessão de ~1M para 86K tokens em cerca de 1 segundo. Vale salvar como solução prática de token-budgeting em sessões longas de agentes."
key_points: ["Funciona como plugin no Claude, invocável na própria sessão (instalação via prompt ao Claude)", "Usa o modelo Jev da Typesafe AI especializado em revisar tool calls desnecessárias do histórico", "Redução observada: de quase 1M de tokens para 86K tokens", "Latência extremamente baixa (~1 segundo) para o processo de compressão"]
entities: ["altryne", "Typesafe AI", "Jev", "Claude"]
content_type: "tool"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: ["https://pbs.twimg.com/media/HSdTBk8bAAAPtk8.png", "https://pbs.twimg.com/media/HSdTCa_a0AAKYLw.png"]
---

# Compressão de contexto em sessões Claude

**@altryne** · [2100739055923425589](https://x.com/altryne/status/2100739055923425589) · `tool`

## Resumo
Plugin que usa o modelo Jev da Typesafe AI dentro do Claude para revisar e remover tool calls desnecessárias, comprimindo a sessão de ~1M para 86K tokens em cerca de 1 segundo. Vale salvar como solução prática de token-budgeting em sessões longas de agentes.

## Pontos-chave
- Funciona como plugin no Claude, invocável na própria sessão (instalação via prompt ao Claude)
- Usa o modelo Jev da Typesafe AI especializado em revisar tool calls desnecessárias do histórico
- Redução observada: de quase 1M de tokens para 86K tokens
- Latência extremamente baixa (~1 segundo) para o processo de compressão

## Entidades
altryne, Typesafe AI, Jev, Claude

> **Revisit:** `medium` · **fonte:** `tweet`
