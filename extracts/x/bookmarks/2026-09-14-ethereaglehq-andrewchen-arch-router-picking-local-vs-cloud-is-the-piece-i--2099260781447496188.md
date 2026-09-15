---
title: "roteamento de modelos local vs cloud"
type: "extract"
source: "x"
status_id: "2099260781447496188"
handle: "ethereaglehq"
url: "https://x.com/ethereaglehq/status/2099260781447496188"
created_at: "2026-09-13T22:15:47.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-ethereaglehq-andrewchen-arch-router-picking-local-vs-cloud-is-the-piece-i--2099260781447496188.json]]"
tags: ["model-selection", "escalation", "agent-tooling", "arquitetura", "runtime"]
topic: "roteamento de modelos local vs cloud"
summary: "Pergunta a Andrew Chen sobre o Arch-Router: se ele classifica o prompt antecipadamente para escolher modelo local ou cloud, ou faz upgrade mid-run quando o modelo local falha em tool calls. Vale salvar pela distinção de design de roteamento: classificação estática vs escalonamento dinâmico."
key_points: ["Distinção central de design em routing: classificar o prompt upfront (estático) vs escalar dinamicamente para nuvem durante a execução", "O gatilho de escalonamento discutido é a falha do modelo local em chamadas de ferramentas (tool calls), não apenas custo ou latência", "Arch-Router citado como componente 'copiável' para pipelines de agentes que misturam modelos locais e em nuvem"]
entities: ["Arch-Router", "Andrew Chen"]
content_type: "question"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
---

# roteamento de modelos local vs cloud

**@ethereaglehq** · [2099260781447496188](https://x.com/ethereaglehq/status/2099260781447496188) · `question`

## Resumo
Pergunta a Andrew Chen sobre o Arch-Router: se ele classifica o prompt antecipadamente para escolher modelo local ou cloud, ou faz upgrade mid-run quando o modelo local falha em tool calls. Vale salvar pela distinção de design de roteamento: classificação estática vs escalonamento dinâmico.

## Pontos-chave
- Distinção central de design em routing: classificar o prompt upfront (estático) vs escalar dinamicamente para nuvem durante a execução
- O gatilho de escalonamento discutido é a falha do modelo local em chamadas de ferramentas (tool calls), não apenas custo ou latência
- Arch-Router citado como componente 'copiável' para pipelines de agentes que misturam modelos locais e em nuvem

## Entidades
Arch-Router, Andrew Chen

> **Revisit:** `medium` · **fonte:** `tweet`
