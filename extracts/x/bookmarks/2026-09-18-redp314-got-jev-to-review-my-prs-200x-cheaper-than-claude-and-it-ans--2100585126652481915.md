---
title: "Code review barato via typesafe"
type: "extract"
source: "x"
status_id: "2100585126652481915"
handle: "redp314"
url: "https://x.com/redp314/status/2100585126652481915"
created_at: "2026-09-17T13:58:15.000Z"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-18-redp314-got-jev-to-review-my-prs-200x-cheaper-than-claude-and-it-ans--2100585126652481915.json]]"
tags: ["code-review", "stack-tooling", "performance"]
topic: "Code review barato via typesafe"
summary: "Promo do Jev (@typesafeai): um único call enviando o diff do PR retorna 14 checks tipados como probabilidades (ex.: hardcoded secret, SQL injection) por ~$0.00007 por review, ~200x mais barato que Claude Opus 5. Vale salvar como opção de code review automatizado de baixíssimo custo e latência para CI em escala."
key_points: ["Fluxo simples: colar o diff → 1 call ao serviço → 14 checks tipados retornados como probabilidades, em ~0,5s", "Custo de ~$0.00007 por PR; 1.000 PRs custam ~$0,07 vs ~$14,50 no Opus 5 (~200x mais barato)", "Checks cobrem riscos de segurança como hardcoded secrets e SQL injection", "Demonstração com 6 PRs reais em vídeo"]
entities: ["Jev", "Typesafe AI (@typesafeai)", "Claude Opus 5", "@redp314"]
content_type: "tool"
revisit: "low"
grounded_in: "tweet"
thin: false
links: []
media: ["https://pbs.twimg.com/amplify_video_thumb/2100585029533372416/img/ZcrsntW2yWgtB_HD.jpg"]
---

# Code review barato via typesafe

**@redp314** · [2100585126652481915](https://x.com/redp314/status/2100585126652481915) · `tool`

## Resumo
Promo do Jev (@typesafeai): um único call enviando o diff do PR retorna 14 checks tipados como probabilidades (ex.: hardcoded secret, SQL injection) por ~$0.00007 por review, ~200x mais barato que Claude Opus 5. Vale salvar como opção de code review automatizado de baixíssimo custo e latência para CI em escala.

## Pontos-chave
- Fluxo simples: colar o diff → 1 call ao serviço → 14 checks tipados retornados como probabilidades, em ~0,5s
- Custo de ~$0.00007 por PR; 1.000 PRs custam ~$0,07 vs ~$14,50 no Opus 5 (~200x mais barato)
- Checks cobrem riscos de segurança como hardcoded secrets e SQL injection
- Demonstração com 6 PRs reais em vídeo

## Entidades
Jev, Typesafe AI (@typesafeai), Claude Opus 5, @redp314

> **Revisit:** `low` · **fonte:** `tweet`
