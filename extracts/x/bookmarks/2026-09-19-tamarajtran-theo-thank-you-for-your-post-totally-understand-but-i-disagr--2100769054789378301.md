---
title: "compaction de contexto no Claude Code"
type: "extract"
source: "x"
status_id: "2100769054789378301"
handle: "tamarajtran"
url: "https://x.com/tamarajtran/status/2100769054789378301"
created_at: "2026-09-18T02:09:07.000Z"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-19-tamarajtran-theo-thank-you-for-your-post-totally-understand-but-i-disagr--2100769054789378301.json]]"
tags: ["context-engineering", "context-management", "agent-context", "state", "verification"]
topic: "compaction de contexto no Claude Code"
summary: "Réplica de Tam (Anthropic) a uma crítica de Theo sobre compaction no Claude Code: o estado é retido em toda requisição de compactação e os pares de chamada/resultado de tool são casados por ID, preservando o contexto sobre o que é relevante. Inclui link para a documentação do mecanismo."
key_points: ["O estado é retido em cada requisição de compaction, ou seja, a compactação não descarta tudo indiscriminadamente.", "Tool requests (tool_use) e tool calls/results (tool_result) são casados por ID, mantendo os pares íntegros no contexto.", "Graças a esse pareamento por ID, o modelo consegue distinguir o que é relevante vs. irrelevante ao decidir o que manter após a compactação.", "O tweet linka a documentação oficial que explica como o mecanismo funciona, servindo de contraponto técnico à crítica original."]
entities: ["@tamarajtran", "theo", "Claude Code"]
content_type: "opinion"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-19-tamarajtran-run-fast-jev-compaction-https-t-co-htdjnjnlaa--2100694552369897539|Compacção de contexto verbatim para Claude Code]]", "[[extracts/x/bookmarks/2026-09-19-grok-pumuonx-theo-tamarajtran-theo-is-right-on-the-core-issues-th--2100825243669409961|poda de contexto vs compaction nativa]]", "[[extracts/x/bookmarks/2026-09-19-moritzkremb-2-instant-compaction-https-t-co-rewiuarc0m--2100895917956284706|Instant compaction em agentes]]", "[[extracts/x/bookmarks/2026-09-12-leoxbtt-bro-el-ingeniero-que-creo-claude-code-solto-un-video-de-28-m--2082108948505674112|Uso avançado do Claude Code]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-found-the-perfect-use-case-for-typesafeai-jev-instant-compac--2100694549362553153|compaction instantânea de contexto em agentes]]", "[[extracts/x/bookmarks/2026-09-19-altryne-this-is-actually-insane-this-uses-typesafeai-jev-model-as-a--2100739055923425589|Compressão de contexto em sessões Claude]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-new-in-claude-code-your-sessions-can-now-message-each-other--2085817074816070014|Mensageria entre sessões no Claude Code]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-theo-thats-not-specific-to-jev-compaction-summarize-based-co--2100773452475183219|context compaction limitations]]", "[[extracts/x/bookmarks/2026-09-12-polydao-claude-obsidian-loop-engineering-a-vault-that-runs-itself-th--2098288931620184216|Claude + Obsidian vault como estado do agente]]", "[[extracts/x/bookmarks/2026-09-19-pumuonx-theo-tamarajtran-grok-read-the-whole-story-who-is-right--2100825040132428182|disputa não especificada no X]]"]
theme: "Tooling e infra de agentes"
---

# compaction de contexto no Claude Code

**@tamarajtran** · [2100769054789378301](https://x.com/tamarajtran/status/2100769054789378301) · `opinion`

## Resumo
Réplica de Tam (Anthropic) a uma crítica de Theo sobre compaction no Claude Code: o estado é retido em toda requisição de compactação e os pares de chamada/resultado de tool são casados por ID, preservando o contexto sobre o que é relevante. Inclui link para a documentação do mecanismo.

## Pontos-chave
- O estado é retido em cada requisição de compaction, ou seja, a compactação não descarta tudo indiscriminadamente.
- Tool requests (tool_use) e tool calls/results (tool_result) são casados por ID, mantendo os pares íntegros no contexto.
- Graças a esse pareamento por ID, o modelo consegue distinguir o que é relevante vs. irrelevante ao decidir o que manter após a compactação.
- O tweet linka a documentação oficial que explica como o mecanismo funciona, servindo de contraponto técnico à crítica original.

## Entidades
@tamarajtran, theo, Claude Code

> **Revisit:** `medium` · **fonte:** `tweet`
