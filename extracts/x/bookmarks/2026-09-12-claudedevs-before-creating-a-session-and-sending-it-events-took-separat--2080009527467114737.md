---
title: "Seeding de eventos na criação de sessão"
type: "extract"
source: "x"
status_id: "2080009527467114737"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2080009527467114737"
created_at: "2026-07-22T19:18:10.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-before-creating-a-session-and-sending-it-events-took-separat--2080009527467114737.json]]"
tags: ["agent-tooling", "runtime", "state", "agents"]
topic: "Seeding de eventos na criação de sessão"
summary: "A API de sessões do Claude agora permite semear até 50 eventos user_message e define_outcome diretamente na chamada de criação, eliminando chamadas separadas para criar sessão e enviar eventos. Vale salvar como nota de changelog para quem inicializa sessões de agentes com contexto prévio ou outcomes definidos."
key_points: ["Antes, criar uma sessão e enviar eventos exigia chamadas de API separadas", "Agora a chamada de create aceita seeding de até 50 eventos por sessão", "Somente tipos user_message e define_outcome podem ser semeados no create", "Reduz round trips e simplifica a inicialização de sessões com histórico/outcomes pré-carregados"]
entities: ["Anthropic", "Claude API"]
content_type: "announcement"
revisit: "low"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/amplify_video_thumb/2080001129468014592/img/CZTc6N_HA3SuD1ek.jpg"]
---

# Seeding de eventos na criação de sessão

**@ClaudeDevs** · [2080009527467114737](https://x.com/ClaudeDevs/status/2080009527467114737) · `announcement`

## Resumo
A API de sessões do Claude agora permite semear até 50 eventos user_message e define_outcome diretamente na chamada de criação, eliminando chamadas separadas para criar sessão e enviar eventos. Vale salvar como nota de changelog para quem inicializa sessões de agentes com contexto prévio ou outcomes definidos.

## Pontos-chave
- Antes, criar uma sessão e enviar eventos exigia chamadas de API separadas
- Agora a chamada de create aceita seeding de até 50 eventos por sessão
- Somente tipos user_message e define_outcome podem ser semeados no create
- Reduz round trips e simplifica a inicialização de sessões com histórico/outcomes pré-carregados

## Entidades
Anthropic, Claude API

> **Revisit:** `low` · **fonte:** `tweet`
