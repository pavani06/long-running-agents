---
title: "Plugin de code review para Pi"
type: "extract"
source: "x"
status_id: "2098752822221365732"
handle: "RiverAi7z"
url: "https://x.com/RiverAi7z/status/2098752822221365732"
created_at: "2026-09-12T12:37:20.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-riverai7z-pi-review-pi-install-git-https-t-co-ezws490o0e--2098752822221365732.json]]"
tags: ["code-review", "agent-tooling", "agentic-coding", "process"]
topic: "Plugin de code review para Pi"
summary: "pi-review é um plugin do próprio autor do Pi (usado na Earendil) que adiciona fluxos práticos de revisão de código via /review e /end-review, cobrindo diffs, commits e PRs do GitHub. Vale salvar como referência de tooling de revisão assistida por agente com verdict priorizado."
key_points: ["Suporta revisar mudanças uncommitted, diff contra branch base, commit específico, PR do GitHub (via gh checkout local) ou snapshot de pastas/arquivos", "Gera findings priorizados com verdict claro e follow-ups acionáveis, separando feedback para o agente de callouts para humanos", "Permite instruções compartilhadas customizadas carregadas de REVIEW_GUIDELINES.md, além de --extra para foco pontual (ex.: performance e error handling)", "O encerramento com /end-review oferece três modos: apenas retornar, retornar + resumir, ou retornar + enfileirar trabalho de correção"]
entities: ["Pi", "pi-review", "Earendil", "GitHub", "REVIEW_GUIDELINES.md"]
content_type: "tool"
revisit: "medium"
grounded_in: "article"
thin: false
links: ["https://github.com/earendil-works/pi-review"]
media: []
---

# Plugin de code review para Pi

**@RiverAi7z** · [2098752822221365732](https://x.com/RiverAi7z/status/2098752822221365732) · `tool`

## Resumo
pi-review é um plugin do próprio autor do Pi (usado na Earendil) que adiciona fluxos práticos de revisão de código via /review e /end-review, cobrindo diffs, commits e PRs do GitHub. Vale salvar como referência de tooling de revisão assistida por agente com verdict priorizado.

## Pontos-chave
- Suporta revisar mudanças uncommitted, diff contra branch base, commit específico, PR do GitHub (via gh checkout local) ou snapshot de pastas/arquivos
- Gera findings priorizados com verdict claro e follow-ups acionáveis, separando feedback para o agente de callouts para humanos
- Permite instruções compartilhadas customizadas carregadas de REVIEW_GUIDELINES.md, além de --extra para foco pontual (ex.: performance e error handling)
- O encerramento com /end-review oferece três modos: apenas retornar, retornar + resumir, ou retornar + enfileirar trabalho de correção

## Links
- https://github.com/earendil-works/pi-review

## Entidades
Pi, pi-review, Earendil, GitHub, REVIEW_GUIDELINES.md

> **Revisit:** `medium` · **fonte:** `article`
