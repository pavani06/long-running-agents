---
title: "Jev: decodificação não-autorregressiva em LLMs"
type: "extract"
source: "x"
status_id: "2100239244501430438"
handle: "NielsRogge"
url: "https://x.com/NielsRogge/status/2100239244501430438"
created_at: "2026-09-16T15:03:51.000Z"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-18-nielsrogge-for-anyone-curious-how-jev-works-i-made-a-visual-explanation--2100239244501430438.json]]"
tags: ["arquitetura", "performance", "analise"]
topic: "Jev: decodificação não-autorregressiva em LLMs"
summary: "Explicação visual de como o Jev funciona, baseada no modelo Qwen2.5-RLCD: substituir a geração autorregressiva (token a token) por uma única passagem do decoder Transformer de um LLM pré-treinado. Vale salvar como referência didática sobre geração paralela/alternativa em LLMs."
key_points: ["A proposta central do Jev é substituir a geração autorregressiva clássica de LLMs por uma única passagem do Transformer decoder de um modelo pré-treinado", "Baseia-se no modelo Qwen2.5-RLCD, liberado por Harsha Gundal no Hugging Face", "A explicação visual foi construída com auxílio do Claude AI, facilitando o entendimento do mecanismo de decodificação alternativa"]
entities: ["Niels Rogge", "Jev", "Qwen2.5-RLCD", "Harsha Gundal", "Hugging Face", "Claude AI"]
content_type: "resource"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: ["https://pbs.twimg.com/media/HSWLYi3WcAAOPBs.jpg"]
relates-to: ["[[extracts/x/bookmarks/2026-09-19-alexlavaee-jev-explained-in-under-10-min-what-it-is-how-parallel-constr--2100687082188677231|Constrained decoding paralelo (Jev)]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-the-gains-arent-free-jev-can-t-generate-text-comparing-jev-v--2099925684256899543|Trade-off JEPA vs LLMs]]", "[[extracts/x/bookmarks/2026-09-18-manthanguptaa-jev-is-one-of-the-more-interesting-model-launches-i-have-see--2100466984605417923|Lançamento do modelo Jev]]", "[[extracts/x/bookmarks/2026-09-18-0xlogicrw-openai-diogo-almeida-typesafe-ai-jev-token-token-jev-typesaf--2100065117127815679|Jev: modelo classificador da TypeSafe AI]]", "[[extracts/x/bookmarks/2026-09-18-hot_town-jev-is-here-how-is-different-from-an-llm-how-does-it-work-un--2100570516612382787|Jev: o que é e quando usar]]", "[[extracts/x/bookmarks/2026-09-19-signulll-jev-class-of-models-have-no-generative-decoder-loop-have-bou--2101062047350096040|Modelos JEV on-device]]", "[[extracts/x/bookmarks/2026-09-14-grok-iykshani-yifanzhang-the-recurrent-looped-transformer-rlt-has--2098944692247240757|Recurrent Looped Transformer]]", "[[extracts/x/bookmarks/2026-09-18-hamiltonulmer-i-made-a-duckdb-extension-where-you-can-use-typesafeai-s-jev--2100370557405667768|Extensão DuckDB para classificação com Jev]]", "[[extracts/x/bookmarks/2026-09-12-_avichawla-why-kv-cache-stores-k-and-v-vectors-but-never-q-a-popular-te--2093962020962083139|KV cache sem Q em LLMs]]", "[[extracts/x/bookmarks/2026-09-12-hasantoxr-you-can-now-watch-any-ai-paper-instead-of-reading-it-there-s--2097398574061670664|arXivisual: papers em vídeo animado]]", "[[extracts/x/bookmarks/2026-09-12-_yusufknl-as-someone-who-s-been-shipping-llms-since-the-gpt-2-days-thi--2078877591923036378|Aula de cross-entropy em LLMs]]"]
theme: "Treinamento de modelos e atletas"
---

# Jev: decodificação não-autorregressiva em LLMs

**@NielsRogge** · [2100239244501430438](https://x.com/NielsRogge/status/2100239244501430438) · `resource`

## Resumo
Explicação visual de como o Jev funciona, baseada no modelo Qwen2.5-RLCD: substituir a geração autorregressiva (token a token) por uma única passagem do decoder Transformer de um LLM pré-treinado. Vale salvar como referência didática sobre geração paralela/alternativa em LLMs.

## Pontos-chave
- A proposta central do Jev é substituir a geração autorregressiva clássica de LLMs por uma única passagem do Transformer decoder de um modelo pré-treinado
- Baseia-se no modelo Qwen2.5-RLCD, liberado por Harsha Gundal no Hugging Face
- A explicação visual foi construída com auxílio do Claude AI, facilitando o entendimento do mecanismo de decodificação alternativa

## Entidades
Niels Rogge, Jev, Qwen2.5-RLCD, Harsha Gundal, Hugging Face, Claude AI

> **Revisit:** `medium` · **fonte:** `tweet`
