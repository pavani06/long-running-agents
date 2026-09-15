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
