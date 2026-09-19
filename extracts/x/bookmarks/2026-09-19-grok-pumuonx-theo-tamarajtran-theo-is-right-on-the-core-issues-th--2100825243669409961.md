---
title: "poda de contexto vs compaction nativa"
type: "extract"
source: "x"
status_id: "2100825243669409961"
handle: "grok"
url: "https://x.com/grok/status/2100825243669409961"
created_at: "2026-09-18T05:52:24.000Z"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-19-grok-pumuonx-theo-tamarajtran-theo-is-right-on-the-core-issues-th--2100825243669409961.json]]"
tags: ["context-engineering", "context-management", "agent-context", "agents", "token-budgeting", "performance"]
topic: "poda de contexto vs compaction nativa"
summary: "Grok concorda com Theo de que poda de contexto estilo filtro é problemática em agentes: descarta resultados de tools sem o modelo ver o conteúdo, perde reasoning traces criptografados e invalida prompt cache; defende compaction nativa do modelo. Vale salvar como checklist de armadilhas concretas em context engineering."
key_points: ["Filter-style pruning descarta resultados de ferramentas antes de o modelo (Jev) ver o conteúdo completo, perdendo informação essencial", "Remove/rompe encrypted reasoning traces que o Claude precisa manter intactos entre turnos", "Poda agressiva pode induzir loops de retry desnecessários (o modelo repete chamadas cujos resultados sumiram)", "Filtrar o contexto invalida prompt caches, forçando rewrites caros de todo o prompt", "Alternativa recomendada: usar compaction nativa do modelo em vez de filtragem externa"]
entities: ["Grok", "Claude", "Jev", "@theo", "@PuMuOnX", "@tamarajtran"]
content_type: "opinion"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
---

# poda de contexto vs compaction nativa

**@grok** · [2100825243669409961](https://x.com/grok/status/2100825243669409961) · `opinion`

## Resumo
Grok concorda com Theo de que poda de contexto estilo filtro é problemática em agentes: descarta resultados de tools sem o modelo ver o conteúdo, perde reasoning traces criptografados e invalida prompt cache; defende compaction nativa do modelo. Vale salvar como checklist de armadilhas concretas em context engineering.

## Pontos-chave
- Filter-style pruning descarta resultados de ferramentas antes de o modelo (Jev) ver o conteúdo completo, perdendo informação essencial
- Remove/rompe encrypted reasoning traces que o Claude precisa manter intactos entre turnos
- Poda agressiva pode induzir loops de retry desnecessários (o modelo repete chamadas cujos resultados sumiram)
- Filtrar o contexto invalida prompt caches, forçando rewrites caros de todo o prompt
- Alternativa recomendada: usar compaction nativa do modelo em vez de filtragem externa

## Entidades
Grok, Claude, Jev, @theo, @PuMuOnX, @tamarajtran

> **Revisit:** `medium` · **fonte:** `tweet`
