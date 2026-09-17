---
title: "Recurrent Looped Transformer"
type: "extract"
source: "x"
status_id: "2098944692247240757"
handle: "grok"
url: "https://x.com/grok/status/2098944692247240757"
created_at: "2026-09-13T01:19:45.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-grok-iykshani-yifanzhang-the-recurrent-looped-transformer-rlt-has--2098944692247240757.json]]"
tags: ["arquitetura", "memory-architecture", "state"]
topic: "Recurrent Looped Transformer"
summary: "Explica a arquitetura do RLT em duas partes: um encoder paralelo que comprime os tokens conhecidos em uma memória compartilhada e um decoder recorrente que processa um token por vez mantendo um estado oculto de 'pensamento'. Vale salvar como referência concisa de como loops recorrentes podem reduzir custo de inferência em transformers."
key_points: ["O encoder processa todos os tokens conhecidos em paralelo, consolidando-os em uma memória compartilhada", "O decoder recorrente opera um token por vez, ao invés de atenção quadrática sobre toda a sequência", "O decoder carrega um estado oculto de 'pensamento' anterior e o funde com o novo token antes de cada iteração de loop", "O tweet está truncado, cortando a explicação antes do final do mecanismo"]
entities: ["Recurrent Looped Transformer (RLT)", "Grok"]
content_type: "resource"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
theme: "Fundamentos de treino e avaliação"
relates-to: ["[[extracts/x/bookmarks/2026-09-14-yifanzhang_-rasbt-https-t-co-tovrlbceki--2099180888684937556|Recurrent Looped Transformer]]", "[[extracts/x/bookmarks/2026-09-14-yifanzhang_-we-are-at-the-dawn-of-superintelligence-introducing-the-recu--2098886268033945610|Recurrent Looped Transformer]]", "[[extracts/x/bookmarks/2026-09-14-orcarouter-why-does-everyone-suddenly-want-to-pace-ai-recurrent-looped--2098922505591505139|Recurrent Looped Transformers]]", "[[extracts/x/bookmarks/2026-09-14-rasbt-yifanzhang-very-interesting-article-thanks-for-sharing-is-th--2099180639308169595|Looped Transformer prova de conceito]]", "[[extracts/x/bookmarks/2026-09-14-aryan_sakhala-yifanzhang-https-t-co-r9fe8sx8jh-where-it-all-started--2098988144892797057|Transformer: atenção sem recorrência]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-this-is-a-brilliant-paper-it-s-of-the-cleanest-long-context--2098140712504332411|Sequential memory agents para long-context]]", "[[extracts/x/bookmarks/2026-09-14-antoniolupetti-a-mathematical-explanation-of-transformers-is-a-recent-paper--2098759228269682727|Fundamentos matemáticos dos Transformers]]", "[[extracts/x/bookmarks/2026-09-12-_avichawla-why-kv-cache-stores-k-and-v-vectors-but-never-q-a-popular-te--2093962020962083139|KV cache sem Q em LLMs]]"]
---

# Recurrent Looped Transformer

**@grok** · [2098944692247240757](https://x.com/grok/status/2098944692247240757) · `resource`

## Resumo
Explica a arquitetura do RLT em duas partes: um encoder paralelo que comprime os tokens conhecidos em uma memória compartilhada e um decoder recorrente que processa um token por vez mantendo um estado oculto de 'pensamento'. Vale salvar como referência concisa de como loops recorrentes podem reduzir custo de inferência em transformers.

## Pontos-chave
- O encoder processa todos os tokens conhecidos em paralelo, consolidando-os em uma memória compartilhada
- O decoder recorrente opera um token por vez, ao invés de atenção quadrática sobre toda a sequência
- O decoder carrega um estado oculto de 'pensamento' anterior e o funde com o novo token antes de cada iteração de loop
- O tweet está truncado, cortando a explicação antes do final do mecanismo

## Entidades
Recurrent Looped Transformer (RLT), Grok

> **Revisit:** `medium` · **fonte:** `tweet`
