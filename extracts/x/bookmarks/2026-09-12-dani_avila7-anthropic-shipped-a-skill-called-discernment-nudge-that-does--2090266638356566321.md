---
title: "Skill discernment-nudge da Anthropic"
type: "extract"
source: "x"
status_id: "2090266638356566321"
handle: "dani_avila7"
url: "https://x.com/dani_avila7/status/2090266638356566321"
created_at: "2026-08-20T02:36:16.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-dani_avila7-anthropic-shipped-a-skill-called-discernment-nudge-that-does--2090266638356566321.json]]"
tags: ["agent-tooling", "gate-design", "decision-discipline", "agents", "analise"]
topic: "Skill discernment-nudge da Anthropic"
summary: "Anthropic lançou uma skill chamada discernment-nudge cuja única função é decidir quando Claude deve demonstrar autocrítica/duvidar de si na frente do usuário. O detalhe notável: a seção de quando NÃO disparar o comportamento é 3x maior que a de quando disparar."
key_points: ["A skill tem propósito único e restrito: gate para quando o modelo deve externar segunda suposição sobre a própria resposta", "Design dominado por condições negativas — a lista de quando não ativar é 3x maior que a de ativação, priorizando supressão de falsos positivos", "Autor considera a escrita da lógica de triggers exemplar, como referência para escrever gates de comportamento em skills", "Lição implícita para design de agentes: em comportamentos invasivos/visíveis ao usuário, o custo do disparo indevido supera o da omissão"]
entities: ["Anthropic", "Claude", "discernment-nudge", "dani_avila7"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
links: []
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098382953235562613|Skill de output direto para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-rlancemartin-i-recently-added-this-command-to-the-claude-api-skill-run-it--2095170001175199771|Comando prompt-audit para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420|Arquitetura de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098020699365355709|Skill ADHD-friendly para agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-claude-code-can-design-now-the-new-design-skill-research-pre--2089471692762673408|Claude Code /design skill]]", "[[extracts/x/bookmarks/2026-09-12-david_tornai-people-are-using-notebooklm-to-mass-produce-specialized-clau--2093337464215932962|Criar Claude Skills com NotebookLM]]", "[[extracts/x/bookmarks/2026-09-12-alperortac-pro-tip-for-anyone-using-grill-me-tell-the-agent-fyi-we-dont--2097661439901048852|Ajustando rigor do agente no /grill-me]]"]
thin: false
theme: "Ecossistema Claude e Agentic Coding"
---

# Skill discernment-nudge da Anthropic

**@dani_avila7** · [2090266638356566321](https://x.com/dani_avila7/status/2090266638356566321) · `announcement`

## Resumo
Anthropic lançou uma skill chamada discernment-nudge cuja única função é decidir quando Claude deve demonstrar autocrítica/duvidar de si na frente do usuário. O detalhe notável: a seção de quando NÃO disparar o comportamento é 3x maior que a de quando disparar.

## Pontos-chave
- A skill tem propósito único e restrito: gate para quando o modelo deve externar segunda suposição sobre a própria resposta
- Design dominado por condições negativas — a lista de quando não ativar é 3x maior que a de ativação, priorizando supressão de falsos positivos
- Autor considera a escrita da lógica de triggers exemplar, como referência para escrever gates de comportamento em skills
- Lição implícita para design de agentes: em comportamentos invasivos/visíveis ao usuário, o custo do disparo indevido supera o da omissão

## Entidades
Anthropic, Claude, discernment-nudge, dani_avila7

> **Revisit:** `medium` · **fonte:** `tweet`
