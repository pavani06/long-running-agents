---
title: "KV cache sem Q em LLMs"
type: "extract"
source: "x"
status_id: "2093962020962083139"
handle: "_avichawla"
url: "https://x.com/_avichawla/status/2093962020962083139"
created_at: "2026-08-30T07:20:24.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-_avichawla-why-kv-cache-stores-k-and-v-vectors-but-never-q-a-popular-te--2093962020962083139.json]]"
tags: ["runtime", "performance", "arquitetura"]
topic: "KV cache sem Q em LLMs"
summary: "Explica por que o KV cache de transformers armazena apenas os vetores K e V dos tokens passados e nunca o Q: a geração autoregressiva reutiliza K/V a cada passo, enquanto Q só existe para o token atual."
key_points: ["LLMs são autoregressivos: cada token é previsto a partir de todos os tokens anteriores, um de cada vez", "Os vetores Q pertencem apenas ao token corrente em processamento, então são computados do zero e nunca reutilizados", "K e V de tokens passados são exigidos em cada novo passo de forward, e cacheá-los evita recomputação", "É uma pergunta técnica popular em entrevistas sobre internals de LLM"]
entities: ["_avichawla"]
content_type: "resource"
revisit: "medium"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/tweet_video_thumb/HQ8_W2IbkAErTe3.jpg"]
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-14-grok-iykshani-yifanzhang-the-recurrent-looped-transformer-rlt-has--2098944692247240757|Recurrent Looped Transformer]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-radixattention-clearly-explained-how-sglang-makes-prefix-cac--2098750998353473776|RadixAttention e prefix caching no SGLang]]", "[[extracts/x/bookmarks/2026-09-14-yifanzhang_-rasbt-https-t-co-tovrlbceki--2099180888684937556|Recurrent Looped Transformer]]", "[[extracts/x/bookmarks/2026-09-12-tydsh-a-novel-way-to-do-rl-in-llm-post-training-inspired-by-our-pr--2080881800877134004|Dinâmica de aprendizado do RLVR]]", "[[extracts/x/bookmarks/2026-09-14-orcarouter-why-does-everyone-suddenly-want-to-pace-ai-recurrent-looped--2098922505591505139|Recurrent Looped Transformers]]", "[[extracts/x/bookmarks/2026-09-14-orcarouter-yifanzhang-thats-not-really-new-the-interesting-problem-with--2098913996057502068|Observabilidade em modelos com recurrent depth]]"]
theme: "Arquitetura e avaliação de sistemas"
---

# KV cache sem Q em LLMs

**@_avichawla** · [2093962020962083139](https://x.com/_avichawla/status/2093962020962083139) · `resource`

## Resumo
Explica por que o KV cache de transformers armazena apenas os vetores K e V dos tokens passados e nunca o Q: a geração autoregressiva reutiliza K/V a cada passo, enquanto Q só existe para o token atual.

## Pontos-chave
- LLMs são autoregressivos: cada token é previsto a partir de todos os tokens anteriores, um de cada vez
- Os vetores Q pertencem apenas ao token corrente em processamento, então são computados do zero e nunca reutilizados
- K e V de tokens passados são exigidos em cada novo passo de forward, e cacheá-los evita recomputação
- É uma pergunta técnica popular em entrevistas sobre internals de LLM

## Entidades
_avichawla

> **Revisit:** `medium` · **fonte:** `tweet`
