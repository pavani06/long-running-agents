---
title: "Extensão MCP para Agent Skills"
type: "extract"
source: "x"
status_id: "2099325795822956575"
handle: "dani_avila7"
url: "https://x.com/dani_avila7/status/2099325795822956575"
created_at: "2026-09-14T02:34:07.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-15-dani_avila7-ok-this-is-big-mcp-now-defines-an-extension-specifically-for--2099325795822956575.json]]"
tags: ["agents", "agent-tooling", "agent-context", "frameworks"]
topic: "Extensão MCP para Agent Skills"
summary: "O MCP (Model Context Protocol) passou a definir uma extensão padrão para descobrir e carregar Agent Skills diretamente de servidores MCP, padronizando como agentes adquirem novas habilidades. Vale salvar como referência do novo fluxo de interoperabilidade de skills."
key_points: ["Servidores MCP agora podem expor Agent Skills de forma padronizada, tornando as habilidades portáveis entre clientes/agentes diferentes", "O fluxo definido é: conectar ao MCP Server → descobrir as skills disponíveis → obter metadados da skill → carregar o arquivo SKILL.md", "Padroniza o carregamento de skills via protocolo em vez de integrações ad-hoc, reduzindo acoplamento entre agente e fonte de conhecimento"]
entities: ["MCP", "Agent Skills", "SKILL.md", "dani_avila7"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-claudedevs-mcp-2026-07-28-is-live-and-it-s-the-largest-update-to-the-pr--2082164248697069935|MCP 2026-07-28 stateless release]]", "[[extracts/x/bookmarks/2026-09-16-trq212-i-was-not-expecting-things-to-go-this-way-but-i-think-mcps-a--2099958388230873165|MCP vs CLI para integrações de agentes]]", "[[extracts/x/bookmarks/2026-09-16-rhyssullivan-total-mcp-victory-some-quick-misc-thoughts-about-why-mcp-is--2099970035137794430|MCP versus CLIs para agentes]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-stateful-vs-stateless-mcp-core-anthropic-s-biggest-mcp-updat--2082454281630961687|Stateful vs. Stateless MCP]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-mattpocock-skills-v1-2-is-out-we-re-now-the-19th-most-starre--2084985277102031137|Lançamento mattpocock/skills v1.2]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-just-saw-a-comment-saying-that-i-ve-never-made-a-proper-over--2088290952704151671|Visão geral das 25 skills de agentes]]", "[[extracts/x/bookmarks/2026-09-16-trq212-rin-cale-thats-what-the-deferred-tools-is-for-it-s-basically--2099959418909851997|MCP deferred tools e progressive disclosure]]"]
theme: "Evals e Infra de Agentes"
---

# Extensão MCP para Agent Skills

**@dani_avila7** · [2099325795822956575](https://x.com/dani_avila7/status/2099325795822956575) · `announcement`

## Resumo
O MCP (Model Context Protocol) passou a definir uma extensão padrão para descobrir e carregar Agent Skills diretamente de servidores MCP, padronizando como agentes adquirem novas habilidades. Vale salvar como referência do novo fluxo de interoperabilidade de skills.

## Pontos-chave
- Servidores MCP agora podem expor Agent Skills de forma padronizada, tornando as habilidades portáveis entre clientes/agentes diferentes
- O fluxo definido é: conectar ao MCP Server → descobrir as skills disponíveis → obter metadados da skill → carregar o arquivo SKILL.md
- Padroniza o carregamento de skills via protocolo em vez de integrações ad-hoc, reduzindo acoplamento entre agente e fonte de conhecimento

## Entidades
MCP, Agent Skills, SKILL.md, dani_avila7

> **Revisit:** `medium` · **fonte:** `tweet`
