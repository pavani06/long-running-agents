---
title: "sistema de orquestração multi-agente em grafo"
type: "extract"
source: "x"
status_id: "2080980071813177629"
handle: "leopardracer"
url: "https://x.com/leopardracer/status/2080980071813177629"
created_at: "2026-07-25T11:34:46.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-leopardracer-the-2-2m-anthropic-engineer-who-built-this-graph-system-just--2080980071813177629.json]]"
tags: ["agentes-orquestracao", "multi-agent", "state", "arquitetura", "agents"]
topic: "sistema de orquestração multi-agente em grafo"
summary: "Descreve a arquitetura de um sistema de agentes em grafo atribuído a um engenheiro da Anthropic: pipeline de seis nós (Task → Researcher → Planner → Writer + Code Agent → Reviewer → Deploy) operando sobre um estado compartilhado único, com comunicação via pacotes."
key_points: ["Pipeline de seis nós encadeados: tarefa, pesquisa, planejamento, geração (texto + código), revisão e deploy", "Um único estado compartilhado entre todos os nós, em vez de estados isolados por agente", "Fluxo de dados entre nós feito por 'packets', sugerindo troca estruturada de contexto", "Argumento do autor: a maioria dos debatedores de 'graphs vs. loops' nunca observou um grafo executando de fato"]
entities: ["Anthropic", "leopardracer"]
content_type: "resource"
revisit: "medium"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/amplify_video_thumb/2080979877566496769/img/CV0t30IehD1kOmFt.jpg"]
thin: false
theme: "Engenharia de Agentes e Loops"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-anatolikopadze-anthropic-engineer-you-re-not-supposed-to-babysit-the-model--2080702441809399834|agentes paralelos em grafos]]", "[[extracts/x/bookmarks/2026-09-12-rvaniaaaa-someone-published-the-architecture-for-an-ai-agent-that-neve--2082562583131726050|arquitetura de agente autodidata]]", "[[extracts/x/bookmarks/2026-09-12-0xmovez-anthropic-engineer-80-of-our-engineers-are-using-selfimprovi--2079985963862786352|agentes auto-melhorantes orquestrados por grafos]]", "[[extracts/x/bookmarks/2026-09-12-sprytixl-stanford-and-anthropic-spent-3-1m-to-prove-your-agent-perfor--2078969602189746340|memória de agentes via grafos]]", "[[extracts/x/bookmarks/2026-09-12-voxyz_ai-codex-tip-a-cost-efficient-luna-sol-agent-tree-orchestrated--2097814698204832116|orquestração de agentes com Codex]]", "[[extracts/x/bookmarks/2026-09-12-svpino-the-frontieragent-framework-is-here-star-the-repo-https-t-co--2098489264749334565|FrontierAgent: runtime de agentes e evals]]"]
---

# sistema de orquestração multi-agente em grafo

**@leopardracer** · [2080980071813177629](https://x.com/leopardracer/status/2080980071813177629) · `resource`

## Resumo
Descreve a arquitetura de um sistema de agentes em grafo atribuído a um engenheiro da Anthropic: pipeline de seis nós (Task → Researcher → Planner → Writer + Code Agent → Reviewer → Deploy) operando sobre um estado compartilhado único, com comunicação via pacotes.

## Pontos-chave
- Pipeline de seis nós encadeados: tarefa, pesquisa, planejamento, geração (texto + código), revisão e deploy
- Um único estado compartilhado entre todos os nós, em vez de estados isolados por agente
- Fluxo de dados entre nós feito por 'packets', sugerindo troca estruturada de contexto
- Argumento do autor: a maioria dos debatedores de 'graphs vs. loops' nunca observou um grafo executando de fato

## Entidades
Anthropic, leopardracer

> **Revisit:** `medium` · **fonte:** `tweet`
