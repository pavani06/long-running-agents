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
thin: false
theme: "Agentic Coding com Claude"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-claudedevs-mcp-2026-07-28-is-live-and-it-s-the-largest-update-to-the-pr--2082164248697069935|MCP 2026-07-28 stateless release]]", "[[extracts/x/bookmarks/2026-09-16-mitsuhiko-trq212-mcp-today-is-a-massive-improvement-over-where-it-star--2099960203131171301|Maturidade do protocolo MCP]]", "[[extracts/x/bookmarks/2026-09-16-trq212-i-was-not-expecting-things-to-go-this-way-but-i-think-mcps-a--2099958388230873165|MCP vs CLI para integrações de agentes]]", "[[extracts/x/bookmarks/2026-09-15-dani_avila7-ok-this-is-big-mcp-now-defines-an-extension-specifically-for--2099325795822956575|Extensão MCP para Agent Skills]]", "[[extracts/x/bookmarks/2026-09-16-rhyssullivan-total-mcp-victory-some-quick-misc-thoughts-about-why-mcp-is--2099970035137794430|MCP versus CLIs para agentes]]", "[[extracts/x/bookmarks/2026-09-16-tobi-trq212-i-think-this-is-true-as-long-as-the-models-can-use-th--2100055404650573833|MCP acessível via REPL para agentes]]"]
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
