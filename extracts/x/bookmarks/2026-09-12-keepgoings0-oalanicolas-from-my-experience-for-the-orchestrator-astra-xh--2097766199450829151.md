---
title: "seleção de modelos por papel de agente"
type: "extract"
source: "x"
status_id: "2097766199450829151"
handle: "keepgoings0"
url: "https://x.com/keepgoings0/status/2097766199450829151"
created_at: "2026-09-09T19:16:51.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-keepgoings0-oalanicolas-from-my-experience-for-the-orchestrator-astra-xh--2097766199450829151.json]]"
tags: ["model-selection", "agents", "multi-agent", "agentic-coding", "performance"]
topic: "seleção de modelos por papel de agente"
summary: "Heurística prática de alocação de modelos em pipeline multi-agente de coding: concentrar os modelos mais fortes em orquestração, pesquisa e exploração, e usar modelos mais leves para implementação. Vale salvar como referência de trade-off custo/capacidade por papel."
key_points: ["Orquestrador deve usar o modelo mais forte disponível (Astra xhigh/high), pois coordena o fluxo inteiro", "Pesquisador e explorador também merecem modelos fortes (Astra low ou Sol 5.6 xhigh) para qualidade de contexto e descoberta", "Implementação funciona bem com modelo mais leve (Luna), que pode ser escalado com Sol ou Astra se necessário", "Princípio geral: alocar compute onde a decisão/direção acontece, economizar na execução mecânica"]
entities: ["Astra", "Sol 5.6", "Luna", "@keepgoings0", "@oalanicolas"]
content_type: "opinion"
revisit: "medium"
grounded_in: "tweet"
links: []
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-voxyz_ai-codex-tip-a-cost-efficient-luna-sol-agent-tree-orchestrated--2097814698204832116|orquestração de agentes com Codex]]", "[[extracts/x/bookmarks/2026-09-12-daniel_mac8-fable-advisor-now-uses-opus-5-as-orchestrator-opus-5-shines--2081056595555868752|fable-advisor com Opus 5 como orquestrador]]", "[[extracts/x/bookmarks/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-layer-that-sits-on-t--2098020649662816503|Roteamento e memória no Hermes Agent]]", "[[extracts/x/bookmarks/2026-09-12-stretchcloud-spotify-s-engineering-team-cut-claude-code-token-usage-by-90--2096439998539321653|Portal: roteamento de dois modelos no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-highly-recommended-model-harness-co-optimization-is-where-yo--2097790938911498494|model-harness co-optimization]]", "[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-voxyz_ai-a-lot-of-people-have-asked-how-to-configure-this-cost-effici--2098033757504634982|Configuração de agent tree com Codex]]", "[[extracts/x/bookmarks/2026-09-12-a16z-an-hour-of-agentic-computer-use-may-now-be-cheaper-than-an-h--2086906363947737406|custo de agentes vs trabalho humano]]", "[[extracts/x/bookmarks/2026-09-12-glaucia_lemos86-caraca-absurdo-isso-aqui-segui-o-conselho-do-pvncher-em-pedi--2096649629068624378|Revisão de artefatos de contexto entre modelos]]", "[[extracts/x/bookmarks/2026-09-12-mtslive-xiaoyin-qu-breaks-down-deepseek-s-cheap-inference-philosophy--2085525434385695137|Economia de treinamento DeepSeek]]"]
thin: false
theme: "Engenharia de agentes de código"
---

# seleção de modelos por papel de agente

**@keepgoings0** · [2097766199450829151](https://x.com/keepgoings0/status/2097766199450829151) · `opinion`

## Resumo
Heurística prática de alocação de modelos em pipeline multi-agente de coding: concentrar os modelos mais fortes em orquestração, pesquisa e exploração, e usar modelos mais leves para implementação. Vale salvar como referência de trade-off custo/capacidade por papel.

## Pontos-chave
- Orquestrador deve usar o modelo mais forte disponível (Astra xhigh/high), pois coordena o fluxo inteiro
- Pesquisador e explorador também merecem modelos fortes (Astra low ou Sol 5.6 xhigh) para qualidade de contexto e descoberta
- Implementação funciona bem com modelo mais leve (Luna), que pode ser escalado com Sol ou Astra se necessário
- Princípio geral: alocar compute onde a decisão/direção acontece, economizar na execução mecânica

## Entidades
Astra, Sol 5.6, Luna, @keepgoings0, @oalanicolas

> **Revisit:** `medium` · **fonte:** `tweet`
