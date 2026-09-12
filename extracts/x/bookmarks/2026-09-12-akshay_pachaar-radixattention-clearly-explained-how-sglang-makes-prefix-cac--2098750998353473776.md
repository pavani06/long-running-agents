---
title: "RadixAttention e prefix caching no SGLang"
type: "extract"
source: "x"
status_id: "2098750998353473776"
handle: "akshay_pachaar"
url: "https://x.com/akshay_pachaar/status/2098750998353473776"
created_at: "2026-09-12T12:30:05.000Z"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
item: "[[raw/x/bookmarks/items/2026-09-12-akshay_pachaar-radixattention-clearly-explained-how-sglang-makes-prefix-cac--2098750998353473776.json]]"
tags: ["performance", "runtime", "arquitetura", "context-management", "production"]
topic: "RadixAttention e prefix caching no SGLang"
summary: "Thread explicando como o RadixAttention usa estrutura radix-tree para reutilizar o KV cache entre requisições que compartilham prefixos, tornando o prefix caching do SGLang eficiente mesmo quando conversas ramificam (ex.: assistente de coding sobre o mesmo repositório). Vale salvar como referência clara de otimização de inferência LLM."
entities: ["SGLang", "RadixAttention", "akshay_pachaar"]
content_type: "thread"
revisit: "high"
links: []
media: ["https://pbs.twimg.com/tweet_video_thumb/HSBC53PawAEXZLa.jpg"]
---

# RadixAttention e prefix caching no SGLang

**@akshay_pachaar** · [2098750998353473776](https://x.com/akshay_pachaar/status/2098750998353473776) · `thread`

## Resumo
Thread explicando como o RadixAttention usa estrutura radix-tree para reutilizar o KV cache entre requisições que compartilham prefixos, tornando o prefix caching do SGLang eficiente mesmo quando conversas ramificam (ex.: assistente de coding sobre o mesmo repositório). Vale salvar como referência clara de otimização de inferência LLM.

## Entidades
SGLang, RadixAttention, akshay_pachaar

> **Revisit:** `high`
