---
title: "Cloudflare AI Gateway custo com prompt caching"
type: "extract"
source: "x"
status_id: "2098027728624570486"
handle: "Marwan_3atef"
url: "https://x.com/Marwan_3atef/status/2098027728624570486"
created_at: "2026-09-10T12:36:04.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-marwan_3atef-cloudflare-ai-gateway-custom-costs-finally-understand-prompt--2098027728624570486.json]]"
tags: ["observability", "telemetry", "token-budgeting", "stack-tooling", "production"]
topic: "Cloudflare AI Gateway custo com prompt caching"
summary: "Cloudflare AI Gateway agora entende prompt caching no custom costs: ao definir per_cache_read_token / per_cache_write_token em cf-aig-custom-cost, as taxas negociadas de cache aparecem nas métricas em vez de cobrar todo token a preço cheio. Vale salvar como referência prática de configuração de custos reais de LLM."
key_points: ["Custom costs do AI Gateway passaram a suportar pricing por token de cache (leitura e escrita)", "Configuração via per_cache_read_token / per_cache_write_token no cf-aig-custom-cost", "Sem isso, todos os tokens eram contabilizados como preço cheio de input, inflando o custo aparente", "Taxa de cache omitida assume um valor default (tweet truncado nesse ponto)"]
entities: ["Cloudflare", "Cloudflare AI Gateway", "cf-aig-custom-cost", "Marwan_3atef"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
links: []
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-quxiaoyin-if-you-left-your-coding-agent-alone-for-more-than-1h-don-t-h--2085408811104534754|expiração de cache de prompt em agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-stretchcloud-spotify-s-engineering-team-cut-claude-code-token-usage-by-90--2096439998539321653|Portal: roteamento de dois modelos no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-radixattention-clearly-explained-how-sglang-makes-prefix-cac--2098750998353473776|RadixAttention e prefix caching no SGLang]]", "[[extracts/x/bookmarks/2026-09-12-kay2289123-ai-infra-ai-kv--2098270561151676829|Reading list de AI Infra]]", "[[extracts/x/bookmarks/2026-09-12-stevendcoffey-today-we-re-launching-the-agents-api-a-brand-new-way-to-buil--2098130889486274820|OpenAI Agents API launch]]", "[[extracts/x/bookmarks/2026-09-12-ubereng-we-cut-uber-eats-search-latency-in-half-how-measure-identify--2098177194979983830|Uber Eats search latency halving]]", "[[extracts/x/bookmarks/2026-09-12-claudeai-we-re-making-claude-sonnet-5-s-introductory-pricing-permanen--2086891169217122586|Preço permanente do Claude Sonnet 5]]"]
---

# Cloudflare AI Gateway custo com prompt caching

**@Marwan_3atef** · [2098027728624570486](https://x.com/Marwan_3atef/status/2098027728624570486) · `announcement`

## Resumo
Cloudflare AI Gateway agora entende prompt caching no custom costs: ao definir per_cache_read_token / per_cache_write_token em cf-aig-custom-cost, as taxas negociadas de cache aparecem nas métricas em vez de cobrar todo token a preço cheio. Vale salvar como referência prática de configuração de custos reais de LLM.

## Pontos-chave
- Custom costs do AI Gateway passaram a suportar pricing por token de cache (leitura e escrita)
- Configuração via per_cache_read_token / per_cache_write_token no cf-aig-custom-cost
- Sem isso, todos os tokens eram contabilizados como preço cheio de input, inflando o custo aparente
- Taxa de cache omitida assume um valor default (tweet truncado nesse ponto)

## Entidades
Cloudflare, Cloudflare AI Gateway, cf-aig-custom-cost, Marwan_3atef

> **Revisit:** `medium` · **fonte:** `tweet`
