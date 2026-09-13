---
title: "Stateful vs. Stateless MCP"
type: "extract"
source: "x"
status_id: "2082454281630961687"
handle: "akshay_pachaar"
url: "https://x.com/akshay_pachaar/status/2082454281630961687"
created_at: "2026-07-29T13:12:45.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-akshay_pachaar-stateful-vs-stateless-mcp-core-anthropic-s-biggest-mcp-updat--2082454281630961687.json]]"
tags: ["agents", "agent-tooling", "arquitetura", "runtime", "frameworks"]
topic: "Stateful vs. Stateless MCP"
summary: "Explicação do update mais recente do MCP da Anthropic, que introduz um core stateless em contraste com o modelo anterior stateful, no qual cliente e servidor faziam handshake de inicialização e o servidor retornava um session id usado em toda requisição posterior. Vale salvar como registro da mudança arquitetural no protocolo padrão de ferramentas para agentes."
key_points: ["Até este release, a comunicação com um MCP server era stateful: exigia um handshake de initialize entre cliente e servidor.", "O servidor retornava um session id que precisava ser carregado em toda requisição seguinte — analogia a uma 'ligação telefônica' persistente.", "A maior atualização do MCP pela Anthropic introduz a alternativa de core stateless, mudando o modelo de sessão do protocolo."]
entities: ["Anthropic", "MCP (Model Context Protocol)", "Akshay Pachaar"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/amplify_video_thumb/2082451799387361280/img/MNNknWSolW-6CeEP.jpg"]
---

# Stateful vs. Stateless MCP

**@akshay_pachaar** · [2082454281630961687](https://x.com/akshay_pachaar/status/2082454281630961687) · `announcement`

## Resumo
Explicação do update mais recente do MCP da Anthropic, que introduz um core stateless em contraste com o modelo anterior stateful, no qual cliente e servidor faziam handshake de inicialização e o servidor retornava um session id usado em toda requisição posterior. Vale salvar como registro da mudança arquitetural no protocolo padrão de ferramentas para agentes.

## Pontos-chave
- Até este release, a comunicação com um MCP server era stateful: exigia um handshake de initialize entre cliente e servidor.
- O servidor retornava um session id que precisava ser carregado em toda requisição seguinte — analogia a uma 'ligação telefônica' persistente.
- A maior atualização do MCP pela Anthropic introduz a alternativa de core stateless, mudando o modelo de sessão do protocolo.

## Entidades
Anthropic, MCP (Model Context Protocol), Akshay Pachaar

> **Revisit:** `medium` · **fonte:** `tweet`
