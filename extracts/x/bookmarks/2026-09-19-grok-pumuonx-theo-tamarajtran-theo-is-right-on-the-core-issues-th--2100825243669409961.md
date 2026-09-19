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
relates-to: ["[[extracts/x/bookmarks/2026-09-19-tamarajtran-found-the-perfect-use-case-for-typesafeai-jev-instant-compac--2100694549362553153|compaction instantânea de contexto em agentes]]", "[[extracts/x/bookmarks/2026-09-19-moritzkremb-2-instant-compaction-https-t-co-rewiuarc0m--2100895917956284706|Instant compaction em agentes]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-theo-thats-not-specific-to-jev-compaction-summarize-based-co--2100773452475183219|context compaction limitations]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-theo-thank-you-for-your-post-totally-understand-but-i-disagr--2100769054789378301|compaction de contexto no Claude Code]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-run-fast-jev-compaction-https-t-co-htdjnjnlaa--2100694552369897539|Compacção de contexto verbatim para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-aicamila_-context-window-management-and-optimization-for-agents-agents--2076155135366135903|Context window management para agentes]]", "[[extracts/x/bookmarks/2026-09-19-altryne-this-is-actually-insane-this-uses-typesafeai-jev-model-as-a--2100739055923425589|Compressão de contexto em sessões Claude]]", "[[extracts/x/bookmarks/2026-09-12-glaucia_lemos86-caraca-absurdo-isso-aqui-segui-o-conselho-do-pvncher-em-pedi--2096649629068624378|Revisão de artefatos de contexto entre modelos]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-radixattention-clearly-explained-how-sglang-makes-prefix-cac--2098750998353473776|RadixAttention e prefix caching no SGLang]]", "[[extracts/x/bookmarks/2026-09-12-quxiaoyin-if-you-left-your-coding-agent-alone-for-more-than-1h-don-t-h--2085408811104534754|expiração de cache de prompt em agentes de código]]"]
theme: "Tooling e infra de agentes"
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
