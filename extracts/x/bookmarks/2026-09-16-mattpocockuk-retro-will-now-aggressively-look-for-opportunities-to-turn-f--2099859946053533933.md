---
title: "Fuzzy rules viram checks determinísticos"
type: "extract"
source: "x"
status_id: "2099859946053533933"
handle: "mattpocockuk"
url: "https://x.com/mattpocockuk/status/2099859946053533933"
created_at: "2026-09-15T13:56:39.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-mattpocockuk-retro-will-now-aggressively-look-for-opportunities-to-turn-f--2099859946053533933.json]]"
tags: ["agentic-coding", "agent-tooling", "code-review", "error-handling", "gate-design", "testes-qa", "verification"]
topic: "Fuzzy rules viram checks determinísticos"
summary: "PR mergeado no repo de skills do Matt Pocock muda o /retro para classificar violações de coding standards como mecânicas (gerar lint/pre-commit/CI) vs. julgamento (doc), evitando que o agente revisor re-deriva a mesma checagem em todo diff. Vale salvar como padrão de design: pagar uma vez por um check determinístico em vez de custo recorrente de julgamento do agente."
key_points: ["Antes o /retro tratava todo gap do reviewer-agent igual (nova linha em CODING_STANDARDS.md); para padrões sintáticos fixos isso fazia o agente re-derivar a mesma decisão em todo diff futuro, em vez de pagar uma vez por um check", "Repos sem pre-commit hook ou CI job rodando lint/typecheck/test agora são finding por si mesmos (categoria Automated checks), não apenas consequência de um erro específico", "Antes de escrever um finding, o retro classifica a violação como mecânica (check determinístico) vs. judgement call (CODING_STANDARDS.md) e por padrão constrói o check", "Mantido language-agnostic (sem nomes tipo ESLint/ts-specific) porque o retro roda em repos de várias linguagens; PR co-autorado por Claude Sonnet 5", "Filosofia central: 'Found an error? Do a /retro, and make it impossible next time' — converter cada erro em prevenção mecânica (lint rule, hook ou workflow de CI)"]
entities: ["Matt Pocock", "/retro", "mattpocock-skills", "CODING_STANDARDS.md", "Claude Sonnet 5", "CLAUDE.md"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/mattpocock/skills/pull/1083"]
media: []
---

# Fuzzy rules viram checks determinísticos

**@mattpocockuk** · [2099859946053533933](https://x.com/mattpocockuk/status/2099859946053533933) · `announcement`

## Resumo
PR mergeado no repo de skills do Matt Pocock muda o /retro para classificar violações de coding standards como mecânicas (gerar lint/pre-commit/CI) vs. julgamento (doc), evitando que o agente revisor re-deriva a mesma checagem em todo diff. Vale salvar como padrão de design: pagar uma vez por um check determinístico em vez de custo recorrente de julgamento do agente.

## Pontos-chave
- Antes o /retro tratava todo gap do reviewer-agent igual (nova linha em CODING_STANDARDS.md); para padrões sintáticos fixos isso fazia o agente re-derivar a mesma decisão em todo diff futuro, em vez de pagar uma vez por um check
- Repos sem pre-commit hook ou CI job rodando lint/typecheck/test agora são finding por si mesmos (categoria Automated checks), não apenas consequência de um erro específico
- Antes de escrever um finding, o retro classifica a violação como mecânica (check determinístico) vs. judgement call (CODING_STANDARDS.md) e por padrão constrói o check
- Mantido language-agnostic (sem nomes tipo ESLint/ts-specific) porque o retro roda em repos de várias linguagens; PR co-autorado por Claude Sonnet 5
- Filosofia central: 'Found an error? Do a /retro, and make it impossible next time' — converter cada erro em prevenção mecânica (lint rule, hook ou workflow de CI)

## Links
- https://github.com/mattpocock/skills/pull/1083

## Entidades
Matt Pocock, /retro, mattpocock-skills, CODING_STANDARDS.md, Claude Sonnet 5, CLAUDE.md

> **Revisit:** `high` · **fonte:** `article`
