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
