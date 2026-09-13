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
