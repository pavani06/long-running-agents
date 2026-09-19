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
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-voxyz_ai-codex-tip-a-cost-efficient-luna-sol-agent-tree-orchestrated--2097814698204832116|orquestração de agentes com Codex]]", "[[extracts/x/bookmarks/2026-09-17-omarsar0-banger-paper-from-nvidia-it-s-on-the-topic-of-choosing-which--2100235516918849661|seleção de modelos para sistemas multi-agentes]]", "[[extracts/x/bookmarks/2026-09-14-lydiahallie-setting-my-subagent-model-to-opus-has-helped-me-save-so-much--2099195114115707210|Roteamento de modelo para subagentes]]", "[[extracts/x/bookmarks/2026-09-14-andrewchen-ethereaglehq-classifies-it-upfront-but-the-way-i-set-up-the--2099278183837397469|model selection com escalonamento]]", "[[extracts/x/bookmarks/2026-09-14-addyosmani-get-more-out-of-your-fable-usage-by-using-opus-for-subagents--2099210491059122471|Opus como modelo de subagents]]", "[[extracts/x/bookmarks/2026-09-12-daniel_mac8-fable-advisor-now-uses-opus-5-as-orchestrator-opus-5-shines--2081056595555868752|fable-advisor com Opus 5 como orquestrador]]", "[[extracts/x/bookmarks/2026-09-14-ethereaglehq-andrewchen-arch-router-picking-local-vs-cloud-is-the-piece-i--2099260781447496188|roteamento de modelos local vs cloud]]", "[[extracts/x/bookmarks/2026-09-12-voxyz_ai-a-lot-of-people-have-asked-how-to-configure-this-cost-effici--2098033757504634982|Configuração de agent tree com Codex]]", "[[extracts/x/bookmarks/2026-09-18-alexfinn-in-case-local-ai-models-are-banned-it-s-critical-you-start-e--2100369670952137067|modelos locais de IA]]", "[[extracts/x/bookmarks/2026-09-19-nutlope-i-used-jev-to-classify-1-018-ai-research-papers-the-result-0--2100426999546184123|classificação barata de papers com LLM]]", "[[extracts/x/bookmarks/2026-09-17-omarsar0-banger-report-from-salesforce-pretty-interesting-to-see-more--2100080746056777899|Modelo agente empresarial Koa (Salesforce)]]"]
theme: "Seleção e roteamento de modelos para agentes"
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
