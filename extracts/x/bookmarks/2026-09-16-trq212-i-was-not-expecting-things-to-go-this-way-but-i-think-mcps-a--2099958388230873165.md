---
title: "MCP vs CLI para integrações de agentes"
type: "extract"
source: "x"
status_id: "2099958388230873165"
handle: "trq212"
url: "https://x.com/trq212/status/2099958388230873165"
created_at: "2026-09-15T20:27:49.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-trq212-i-was-not-expecting-things-to-go-this-way-but-i-think-mcps-a--2099958388230873165.json]]"
tags: ["agent-tooling", "agents", "arquitetura", "stack-tooling"]
topic: "MCP vs CLI para integrações de agentes"
summary: "Opinião de que MCPs superam CLIs na maioria das integrações de agentes porque os modelos melhoraram muito em tool calling, ferramentas podem ser diferidas e o MCP agora é stateless. Vale salvar como diretriz prática de arquitetura de tooling para agentes."
key_points: ["Modelos atuais ficaram muito melhores em tool calling, reduzindo a vantagem de usar CLIs (texto livre) como interface de integração", "MCP agora suporta deferred tools e é stateless, eliminando objeções anteriores de custo/complexidade de contexto", "Para compor ou filtrar dados, o padrão recomendado é expor parâmetros como query nas próprias ferramentas MCP, em vez de fazer composição no modelo", "A conclusão prática: na dúvida entre expor um CLI ou um servidor MCP ao agente, prefira MCP para a maioria dos casos"]
entities: ["MCP (Model Context Protocol)", "CLI", "@trq212"]
content_type: "opinion"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-16-rhyssullivan-total-mcp-victory-some-quick-misc-thoughts-about-why-mcp-is--2099970035137794430|MCP versus CLIs para agentes]]", "[[extracts/x/bookmarks/2026-09-16-rhyssullivan-trq212-the-one-remaining-issue-i-have-with-mcp-is-piping-loc--2099966630206009449|MCP vs CLIs para agentes]]", "[[extracts/x/bookmarks/2026-09-17-omarsar0-i-agree-mcp-is-clearly-better-than-cli-for-most-integrations--2099970990935867485|MCP versus CLI em harnesses]]", "[[extracts/x/bookmarks/2026-09-16-tobi-trq212-i-think-this-is-true-as-long-as-the-models-can-use-th--2100055404650573833|MCP acessível via REPL para agentes]]", "[[extracts/x/bookmarks/2026-09-18-akshay_pachaar-mcp-meets-agent-skills-mcp-already-gave-agents-a-standard-wa--2100659094625636526|Descoberta de Agent Skills via MCP]]", "[[extracts/x/bookmarks/2026-09-16-trq212-rin-cale-thats-what-the-deferred-tools-is-for-it-s-basically--2099959418909851997|MCP deferred tools e progressive disclosure]]", "[[extracts/x/bookmarks/2026-09-15-dani_avila7-ok-this-is-big-mcp-now-defines-an-extension-specifically-for--2099325795822956575|Extensão MCP para Agent Skills]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-stateful-vs-stateless-mcp-core-anthropic-s-biggest-mcp-updat--2082454281630961687|Stateful vs. Stateless MCP]]", "[[extracts/x/bookmarks/2026-09-16-mitsuhiko-trq212-mcp-today-is-a-massive-improvement-over-where-it-star--2099960203131171301|Maturidade do protocolo MCP]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-mcp-2026-07-28-is-live-and-it-s-the-largest-update-to-the-pr--2082164248697069935|MCP 2026-07-28 stateless release]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-the-bitter-lesson-of-tool-calling-tool-calling-is-a-design-c--2086846794840019178|Comparação de métodos de tool calling]]", "[[extracts/x/bookmarks/2026-09-17-nateberkopec-for-the-last-3-months-i-ve-been-telling-all-my-clients-to-mo--2099995262802641129|Executor: gateway MCP para agentes]]", "[[extracts/x/bookmarks/2026-09-16-dair_ai-is-bash-all-you-need-interesting-paper-from-microsoft-if-you--2099925472629150164|Comparando interfaces de ferramentas para agentes]]", "[[extracts/x/bookmarks/2026-09-12-marwan_3atef-google-cloud-put-data-agent-kit-in-the-ide-and-the-pitch-is--2097976275373531523|Data Agent Kit no IDE]]"]
theme: "MCP e interfaces de ferramentas"
---

# MCP vs CLI para integrações de agentes

**@trq212** · [2099958388230873165](https://x.com/trq212/status/2099958388230873165) · `opinion`

## Resumo
Opinião de que MCPs superam CLIs na maioria das integrações de agentes porque os modelos melhoraram muito em tool calling, ferramentas podem ser diferidas e o MCP agora é stateless. Vale salvar como diretriz prática de arquitetura de tooling para agentes.

## Pontos-chave
- Modelos atuais ficaram muito melhores em tool calling, reduzindo a vantagem de usar CLIs (texto livre) como interface de integração
- MCP agora suporta deferred tools e é stateless, eliminando objeções anteriores de custo/complexidade de contexto
- Para compor ou filtrar dados, o padrão recomendado é expor parâmetros como query nas próprias ferramentas MCP, em vez de fazer composição no modelo
- A conclusão prática: na dúvida entre expor um CLI ou um servidor MCP ao agente, prefira MCP para a maioria dos casos

## Entidades
MCP (Model Context Protocol), CLI, @trq212

> **Revisit:** `medium` · **fonte:** `tweet`
