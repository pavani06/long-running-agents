---
title: "Claude Mods: function hooks no Claude Code"
type: "extract"
source: "x"
status_id: "2099551291601248485"
handle: "bcherny"
url: "https://x.com/bcherny/status/2099551291601248485"
created_at: "2026-09-14T17:30:10.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-15-bcherny-claude-mods-are-landing-now-someone-already-built-a-tetris-i--2099551291601248485.json]]"
tags: ["agent-tooling", "frameworks", "permissions", "runtime", "observability"]
topic: "Claude Mods: function hooks no Claude Code"
summary: "Anúncio de que o Claude Code vai lançar 'Claude Mods' — plugins TypeScript construídos sobre 'function hooks' no estilo middleware Express/Koa, que permitem modificar profundamente o produto (inclusive a UI React) com side-effect tracking e controle administrativo fino. Vale salvar por definir a arquitetura de extensibilidade/governança do harness mais usado em coding com agentes."
key_points: ["Mods são plugins sobre function hooks: funções TypeScript com tipos e suporte a LSP que interceptam e alteram o comportamento do Claude Code, compondo como middleware Express/Koa (ordem de registro = aninhamento; continuação via 'next'); admins registram primeiro para controle e depois para defaults.", "Segurança via side-effect tracking sobre um objeto $: plugins só agem através de side-effects parametrizados, e administradores podem remover affordances do $ para impedir que qualquer plugin abaixo invoque aquele efeito — controle programático fino em workplaces.", "Extensibilidade chega à UI: como o CC usa React em toda parte, hooks podem modificar props de componentes ou envolver nós de renderização — demo esconde valores sensíveis no Desktop até hover, permitindo compartilhar tela sem vazar dados.", "Um único hook em '*' observa todos os eventos, incluindo as chamadas dos próprios plugins ao $, tornando audit logging trivial (uma função); hooks também capturam interações de UI (ui.press) de forma idêntica no terminal e no app desktop.", "Já testável via flag CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude; os fontes dos três primeiros mods built-in foram publicados, e uma demo mostra Claude escrevendo, validando e carregando um plugin (que saniiza segredos em tool output) a partir de uma frase.", "Prioridade de registro determina precedência: o primeiro plugin registrado envolve os demais — modelo algébrico descrito como 'continuation model endômico parametrizado por efeitos' para plugins."]
entities: ["Claude Code", "Claude Mods", "Function Hooks", "TypeScript", "Express", "Koa", "React", "GitHub", "CLAUDE_CODE_ENABLE_FUNCTION_HOOKS", "@bcherny"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/anthropics/claude-code/issues/91870#issuecomment-5666255143"]
media: ["https://pbs.twimg.com/tweet_video_thumb/HSMaUpXbwAAvdSL.jpg"]
relates-to: ["[[extracts/x/bookmarks/2026-09-12-bcherny-your-input-needed-would-you-use-this-this-is-an-early-look-a--2095590515765060076|Function Hooks no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-leoxbtt-bro-el-ingeniero-que-creo-claude-code-solto-un-video-de-28-m--2082108948505674112|Uso avançado do Claude Code]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-run-fast-jev-compaction-https-t-co-htdjnjnlaa--2100694552369897539|Compacção de contexto verbatim para Claude Code]]", "[[extracts/x/bookmarks/2026-09-17-claudedevs-claude-design-claude-slides-and-claude-docs-also-work-inside--2100270861555228770|Apps Claude dentro do Claude Code]]", "[[extracts/x/bookmarks/2026-09-18-trq212-projects-brings-the-architecture-of-claude-tag-to-claude-cod--2100638355872706571|agente por projeto no Claude Code]]", "[[extracts/x/bookmarks/2026-09-18-claudedevs-today-we-re-rolling-out-projects-in-claude-code-on-desktop-a--2100633571543367691|Projects no Claude Code]]"]
theme: "Tooling e infra de agentes"
---

# Claude Mods: function hooks no Claude Code

**@bcherny** · [2099551291601248485](https://x.com/bcherny/status/2099551291601248485) · `announcement`

## Resumo
Anúncio de que o Claude Code vai lançar 'Claude Mods' — plugins TypeScript construídos sobre 'function hooks' no estilo middleware Express/Koa, que permitem modificar profundamente o produto (inclusive a UI React) com side-effect tracking e controle administrativo fino. Vale salvar por definir a arquitetura de extensibilidade/governança do harness mais usado em coding com agentes.

## Pontos-chave
- Mods são plugins sobre function hooks: funções TypeScript com tipos e suporte a LSP que interceptam e alteram o comportamento do Claude Code, compondo como middleware Express/Koa (ordem de registro = aninhamento; continuação via 'next'); admins registram primeiro para controle e depois para defaults.
- Segurança via side-effect tracking sobre um objeto $: plugins só agem através de side-effects parametrizados, e administradores podem remover affordances do $ para impedir que qualquer plugin abaixo invoque aquele efeito — controle programático fino em workplaces.
- Extensibilidade chega à UI: como o CC usa React em toda parte, hooks podem modificar props de componentes ou envolver nós de renderização — demo esconde valores sensíveis no Desktop até hover, permitindo compartilhar tela sem vazar dados.
- Um único hook em '*' observa todos os eventos, incluindo as chamadas dos próprios plugins ao $, tornando audit logging trivial (uma função); hooks também capturam interações de UI (ui.press) de forma idêntica no terminal e no app desktop.
- Já testável via flag CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude; os fontes dos três primeiros mods built-in foram publicados, e uma demo mostra Claude escrevendo, validando e carregando um plugin (que saniiza segredos em tool output) a partir de uma frase.
- Prioridade de registro determina precedência: o primeiro plugin registrado envolve os demais — modelo algébrico descrito como 'continuation model endômico parametrizado por efeitos' para plugins.

## Links
- https://github.com/anthropics/claude-code/issues/91870#issuecomment-5666255143

## Entidades
Claude Code, Claude Mods, Function Hooks, TypeScript, Express, Koa, React, GitHub, CLAUDE_CODE_ENABLE_FUNCTION_HOOKS, @bcherny

> **Revisit:** `high` · **fonte:** `article`
