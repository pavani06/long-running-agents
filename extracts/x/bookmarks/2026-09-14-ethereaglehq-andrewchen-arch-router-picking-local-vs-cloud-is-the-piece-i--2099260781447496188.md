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
relates-to: ["[[extracts/x/bookmarks/2026-09-14-andrewchen-ethereaglehq-classifies-it-upfront-but-the-way-i-set-up-the--2099278183837397469|model selection com escalonamento]]", "[[extracts/x/bookmarks/2026-09-14-ethereaglehq-andrewchen-upfront-classify-then-upgrade-if-it-gets-long-is--2099290400779317310|gatilhos de complexidade em agentes]]", "[[extracts/x/bookmarks/2026-09-12-keepgoings0-oalanicolas-from-my-experience-for-the-orchestrator-astra-xh--2097766199450829151|seleção de modelos por papel de agente]]", "[[extracts/x/bookmarks/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-layer-that-sits-on-t--2098020649662816503|Roteamento e memória no Hermes Agent]]", "[[extracts/x/bookmarks/2026-09-12-stretchcloud-spotify-s-engineering-team-cut-claude-code-token-usage-by-90--2096439998539321653|Portal: roteamento de dois modelos no Claude Code]]", "[[extracts/x/bookmarks/2026-09-14-lydiahallie-setting-my-subagent-model-to-opus-has-helped-me-save-so-much--2099195114115707210|Roteamento de modelo para subagentes]]"]
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
