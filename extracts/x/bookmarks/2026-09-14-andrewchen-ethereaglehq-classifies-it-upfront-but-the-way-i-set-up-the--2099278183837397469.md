---
title: "model selection com escalonamento"
type: "extract"
source: "x"
status_id: "2099278183837397469"
handle: "andrewchen"
url: "https://x.com/andrewchen/status/2099278183837397469"
created_at: "2026-09-13T23:24:56.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-andrewchen-ethereaglehq-classifies-it-upfront-but-the-way-i-set-up-the--2099278183837397469.json]]"
tags: ["model-selection", "escalation", "agent-loop"]
topic: "model selection com escalonamento"
summary: "Andrew Chen descreve seu setup de plug-in que classifica a requisição upfront para escolher o modelo, fazendo upgrade para um modelo frontier quando a sessão fica longa ou complexa. Vale salvar como tática concreta de roteamento custo/performance entre modelos."
key_points: ["Classificação da requisição no início da sessão decide o modelo inicial (mais barato)", "Escalonamento automático para modelo frontier quando a sessão tem múltiplos turnos ou ganha complexidade", "Padrão de tradeoff entre custo e qualidade: frontier só quando a complexidade justifica"]
entities: ["Andrew Chen", "@ethereaglehq"]
content_type: "opinion"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-14-ethereaglehq-andrewchen-arch-router-picking-local-vs-cloud-is-the-piece-i--2099260781447496188|roteamento de modelos local vs cloud]]", "[[extracts/x/bookmarks/2026-09-12-keepgoings0-oalanicolas-from-my-experience-for-the-orchestrator-astra-xh--2097766199450829151|seleção de modelos por papel de agente]]", "[[extracts/x/bookmarks/2026-09-14-lydiahallie-setting-my-subagent-model-to-opus-has-helped-me-save-so-much--2099195114115707210|Roteamento de modelo para subagentes]]", "[[extracts/x/bookmarks/2026-09-14-ethereaglehq-andrewchen-upfront-classify-then-upgrade-if-it-gets-long-is--2099290400779317310|gatilhos de complexidade em agentes]]", "[[extracts/x/bookmarks/2026-09-12-stretchcloud-spotify-s-engineering-team-cut-claude-code-token-usage-by-90--2096439998539321653|Portal: roteamento de dois modelos no Claude Code]]", "[[extracts/x/bookmarks/2026-09-14-addyosmani-get-more-out-of-your-fable-usage-by-using-opus-for-subagents--2099210491059122471|Opus como modelo de subagents]]", "[[extracts/x/bookmarks/2026-09-17-omarsar0-banger-paper-from-nvidia-it-s-on-the-topic-of-choosing-which--2100235516918849661|seleção de modelos para sistemas multi-agentes]]", "[[extracts/x/bookmarks/2026-09-17-openrouter-openrouter-users-spent-more-on-openai-models-than-on-anthrop--2099898254905549220|share de gastos LLM OpenRouter]]", "[[extracts/x/bookmarks/2026-09-18-alexfinn-in-case-local-ai-models-are-banned-it-s-critical-you-start-e--2100369670952137067|modelos locais de IA]]", "[[extracts/x/bookmarks/2026-09-12-mtslive-xiaoyin-qu-breaks-down-deepseek-s-cheap-inference-philosophy--2085525434385695137|Economia de treinamento DeepSeek]]", "[[extracts/x/bookmarks/2026-09-14-treytaylorceo-illscience-super-fair-and-honestly-it-depends-on-the-core-mo--2099212116959920547|viés político em modelos de linguagem]]"]
theme: "Ecossistema Claude e Agent Tooling"
---

# model selection com escalonamento

**@andrewchen** · [2099278183837397469](https://x.com/andrewchen/status/2099278183837397469) · `opinion`

## Resumo
Andrew Chen descreve seu setup de plug-in que classifica a requisição upfront para escolher o modelo, fazendo upgrade para um modelo frontier quando a sessão fica longa ou complexa. Vale salvar como tática concreta de roteamento custo/performance entre modelos.

## Pontos-chave
- Classificação da requisição no início da sessão decide o modelo inicial (mais barato)
- Escalonamento automático para modelo frontier quando a sessão tem múltiplos turnos ou ganha complexidade
- Padrão de tradeoff entre custo e qualidade: frontier só quando a complexidade justifica

## Entidades
Andrew Chen, @ethereaglehq

> **Revisit:** `medium` · **fonte:** `tweet`
