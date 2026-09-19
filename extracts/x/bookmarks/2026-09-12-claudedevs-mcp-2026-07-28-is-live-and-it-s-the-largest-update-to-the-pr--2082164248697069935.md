---
title: "MCP 2026-07-28 stateless release"
type: "extract"
source: "x"
status_id: "2082164248697069935"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2082164248697069935"
created_at: "2026-07-28T18:00:16.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-mcp-2026-07-28-is-live-and-it-s-the-largest-update-to-the-pr--2082164248697069935.json]]"
tags: ["agent-tooling", "agents", "arquitetura", "permissions", "observability", "production"]
topic: "MCP 2026-07-28 stateless release"
summary: "A quinta revisão da especificação MCP migra o protocolo para um núcleo stateless (request/response), viabilizando deploy em serverless/edge, e endurece autenticação com OAuth 2.0/OIDC — a maior atualização desde o lançamento, num ecossistema com 400M de downloads mensais do SDK."
key_points: ["Núcleo stateless substitui o modelo bidirecional stateful: servidores MCP agora rodam em infraestrutura serverless e edge, simplificando deploy e escala remota conforme a adoção cresce.", "Extensões padronizadas sob framework versionado: MCP Apps (UI interativa renderizada na conversa) e Tasks (trabalho long-running) sem alterar o protocolo core.", "Autenticação alinhada a OAuth 2.0 e OIDC de produção, conectando servidores MCP a sistemas de identidade corporativos como Entra e Okta sem workarounds.", "Adoção: 400M de downloads mensais de SDK (4x em um ano) e mais de 950 servidores MCP no diretório de conectores do Claude, usados por milhões diariamente.", "Novidades no Claude: auth gerenciada pelo enterprise (admin autoriza uma vez, usuários herdam acesso via grupos do IdP — zero-touch), dashboard de observabilidade para conectores publicados e MCP tunnels (research preview) para servidores em rede privada sem exposição à internet pública."]
entities: ["MCP", "Claude", "OAuth 2.0", "OIDC", "Microsoft Entra", "Okta"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
links: ["https://claude.com/blog/bringing-mcp-2026-07-28-to-claude"]
media: []
thin: false
theme: "MCP e interfaces de ferramentas"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-stateful-vs-stateless-mcp-core-anthropic-s-biggest-mcp-updat--2082454281630961687|Stateful vs. Stateless MCP]]", "[[extracts/x/bookmarks/2026-09-18-akshay_pachaar-mcp-meets-agent-skills-mcp-already-gave-agents-a-standard-wa--2100659094625636526|Descoberta de Agent Skills via MCP]]", "[[extracts/x/bookmarks/2026-09-15-dani_avila7-ok-this-is-big-mcp-now-defines-an-extension-specifically-for--2099325795822956575|Extensão MCP para Agent Skills]]", "[[extracts/x/bookmarks/2026-09-16-mitsuhiko-trq212-mcp-today-is-a-massive-improvement-over-where-it-star--2099960203131171301|Maturidade do protocolo MCP]]", "[[extracts/x/bookmarks/2026-09-16-trq212-i-was-not-expecting-things-to-go-this-way-but-i-think-mcps-a--2099958388230873165|MCP vs CLI para integrações de agentes]]", "[[extracts/x/bookmarks/2026-09-16-rhyssullivan-total-mcp-victory-some-quick-misc-thoughts-about-why-mcp-is--2099970035137794430|MCP versus CLIs para agentes]]"]
---

# MCP 2026-07-28 stateless release

**@ClaudeDevs** · [2082164248697069935](https://x.com/ClaudeDevs/status/2082164248697069935) · `announcement`

## Resumo
A quinta revisão da especificação MCP migra o protocolo para um núcleo stateless (request/response), viabilizando deploy em serverless/edge, e endurece autenticação com OAuth 2.0/OIDC — a maior atualização desde o lançamento, num ecossistema com 400M de downloads mensais do SDK.

## Pontos-chave
- Núcleo stateless substitui o modelo bidirecional stateful: servidores MCP agora rodam em infraestrutura serverless e edge, simplificando deploy e escala remota conforme a adoção cresce.
- Extensões padronizadas sob framework versionado: MCP Apps (UI interativa renderizada na conversa) e Tasks (trabalho long-running) sem alterar o protocolo core.
- Autenticação alinhada a OAuth 2.0 e OIDC de produção, conectando servidores MCP a sistemas de identidade corporativos como Entra e Okta sem workarounds.
- Adoção: 400M de downloads mensais de SDK (4x em um ano) e mais de 950 servidores MCP no diretório de conectores do Claude, usados por milhões diariamente.
- Novidades no Claude: auth gerenciada pelo enterprise (admin autoriza uma vez, usuários herdam acesso via grupos do IdP — zero-touch), dashboard de observabilidade para conectores publicados e MCP tunnels (research preview) para servidores em rede privada sem exposição à internet pública.

## Links
- https://claude.com/blog/bringing-mcp-2026-07-28-to-claude

## Entidades
MCP, Claude, OAuth 2.0, OIDC, Microsoft Entra, Okta

> **Revisit:** `high` · **fonte:** `article`
