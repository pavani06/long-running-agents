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
theme: "Tooling Agêntico para Código"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-mattpocockuk-what-techniques-do-you-use-for-making-ai-authored-pr-s-easie--2096666329495257563|revisão de PRs gerados por IA]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-i-built-a-self-evolving-code-review-agent-most-code-review-a--2098416224803987968|Agente de code review auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-12-mihail_eric-line-by-line-code-review-will-soon-disappear-the-future-is-a--2098097592001548319|revisão de código risco-gateada]]", "[[extracts/x/bookmarks/2026-09-18-mattpocockuk-thinking-about-creating-a-pr-skill-you-invoke-it-to-create-a--2100521948786667822|Skill de criação de PRs]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-coming-soon-to-mattpocock-skills-retro-gives-you-opportuniti--2098062605407461744|Skill /retro para retroativa de agentes]]", "[[extracts/x/bookmarks/2026-09-15-shadcn-introducing-shadcn-lint-an-agent-first-linter-for-tailwind-d--2099534231114314145|shadcn/lint, linter agent-first para Tailwind]]", "[[extracts/x/bookmarks/2026-09-17-eng_khairallah1-the-full-prompt-is-here-lt-purpose-gt-run-a-drift-audit-betw--2100190909715337487|Drift audit entre docs e código]]"]
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
