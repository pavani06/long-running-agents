---
title: "expiração de cache de prompt em agentes de código"
type: "extract"
source: "x"
status_id: "2085408811104534754"
handle: "quxiaoyin"
url: "https://x.com/quxiaoyin/status/2085408811104534754"
created_at: "2026-08-06T16:53:00.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-quxiaoyin-if-you-left-your-coding-agent-alone-for-more-than-1h-don-t-h--2085408811104534754.json]]"
tags: ["token-budgeting", "agentic-coding", "agent-tooling", "context-management"]
topic: "expiração de cache de prompt em agentes de código"
summary: "O cache de prompt que sustenta a sessão de um agente de código expira em exatamente 60 minutos; retomar depois de pausas longas faz o contexto inteiro ser reprocessado, multiplicando o custo em até ~13x. Por isso, após mais de 1h longe, é mais barato abrir uma sessão nova do que clicar em continue."
key_points: ["O cache da sessão expira em exatamente 60 minutos de inatividade; após isso, todo o contexto acumulado precisa ser reprocessado sem desconto de cache", "Custo relativo da retomada: 1x durante uso contínuo, ~1,3x após uma pausa curta (café), ~1,6x após uma ligação, ~13x após o almoço (cache expirado)", "Recomendação prática: se ficou ausente por mais de 1h, não use 'continue' — abra uma nova sessão e reenvie exatamente a mesma mensagem", "Implicação de fluxo de trabalho: concentrar interações com o agente em janelas contínuas preserva os cache hits e reduz drasticamente o custo por token"]
entities: ["quxiaoyin"]
content_type: "opinion"
revisit: "medium"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HPAAnKObIAAWMfB.jpg"]
thin: false
theme: "Engenharia de Agentes e Loops"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-aicamila_-context-window-management-and-optimization-for-agents-agents--2076155135366135903|Context window management para agentes]]", "[[extracts/x/bookmarks/2026-09-12-marwan_3atef-cloudflare-ai-gateway-custom-costs-finally-understand-prompt--2098027728624570486|Cloudflare AI Gateway custo com prompt caching]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-great-paper-from-google-and-colleagues-it-proposes-an-intere--2094472291002589452|Degradação de agentes em tarefas long-horizon]]", "[[extracts/x/bookmarks/2026-09-12-anatolikopadze-anthropic-engineer-you-re-not-supposed-to-prompt-claude-you--2080286550005358977|Sistemas que se auto-promptam em agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-good-work-on-improving-memory-for-long-horizon-agents-they-s--2097555607389896732|Memória para agentes longos]]", "[[extracts/x/bookmarks/2026-09-12-trevin-using-fable-5-1-add-this-to-your-claude-md-file-to-help-its--2095410064492507274|Prompting Claude Fable 5.1]]"]
---

# expiração de cache de prompt em agentes de código

**@quxiaoyin** · [2085408811104534754](https://x.com/quxiaoyin/status/2085408811104534754) · `opinion`

## Resumo
O cache de prompt que sustenta a sessão de um agente de código expira em exatamente 60 minutos; retomar depois de pausas longas faz o contexto inteiro ser reprocessado, multiplicando o custo em até ~13x. Por isso, após mais de 1h longe, é mais barato abrir uma sessão nova do que clicar em continue.

## Pontos-chave
- O cache da sessão expira em exatamente 60 minutos de inatividade; após isso, todo o contexto acumulado precisa ser reprocessado sem desconto de cache
- Custo relativo da retomada: 1x durante uso contínuo, ~1,3x após uma pausa curta (café), ~1,6x após uma ligação, ~13x após o almoço (cache expirado)
- Recomendação prática: se ficou ausente por mais de 1h, não use 'continue' — abra uma nova sessão e reenvie exatamente a mesma mensagem
- Implicação de fluxo de trabalho: concentrar interações com o agente em janelas contínuas preserva os cache hits e reduz drasticamente o custo por token

## Entidades
quxiaoyin

> **Revisit:** `medium` · **fonte:** `tweet`
