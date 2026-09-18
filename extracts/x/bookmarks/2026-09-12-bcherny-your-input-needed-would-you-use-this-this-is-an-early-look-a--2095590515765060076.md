---
title: "Function Hooks no Claude Code"
type: "extract"
source: "x"
status_id: "2095590515765060076"
handle: "bcherny"
url: "https://x.com/bcherny/status/2095590515765060076"
created_at: "2026-09-03T19:11:27.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-bcherny-your-input-needed-would-you-use-this-this-is-an-early-look-a--2095590515765060076.json]]"
tags: ["agent-tooling", "agentic-coding", "arquitetura", "permissions", "frameworks", "runtime"]
topic: "Function Hooks no Claude Code"
summary: "Anúncio e RFC comunitário da extensibilidade profunda do Claude Code via function hooks em TypeScript (modelo de middleware Express/Koa), depois renomeado para 'Claude Mods', com shipping previsto em semanas. Vale salvar porque define a direção da plataforma de plugins do CC, incluindo controle administrativo fino e hooks de renderização/eventos."
key_points: ["Hooks são funções TypeScript com tipos completos e suporte a LSP que compõem como middleware: a ordem de registro define o aninhamento (admins prependam para controle, appendam para defaults) via modelo de continuação 'next' a la Express/Koa", "Segurança via rastreamento de side-effects sobre um objeto $ parametrizado; admins podem remover affordances de $ para impedir que plugins inferiores invoquem certos efeitos (governança programática fina)", "Renomeado para 'Claude Mods' no produto ('function hook' permanece como primitiva de implementação); primeiro, três mods built-in foram publicados e features existentes do CC serão migradas para forma de mod", "Hooks interceptam renderização (React: props e wrap de render nodes) e eventos de UI (ui.press vale em terminal e desktop); hook curinga em * vê todos os eventos, incluindo chamadas de plugins, permitindo audit log em uma função", "Casos de uso demonstrados: redação de segredos em tool output antes do modelo ler (plugin gerado por uma frase do Claude) e ocultar valores sensíveis na UI durante screen share; habilitar com CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude"]
entities: ["Claude Code", "Claude Mods", "function hooks", "Express", "Koa", "React", "TypeScript", "CLAUDE_CODE_ENABLE_FUNCTION_HOOKS", "Boris Cherny"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/anthropics/claude-code/issues/91870"]
media: []
thin: false
theme: "Claude Code e Coding Agêntico"
relates-to: ["[[extracts/x/bookmarks/2026-09-15-bcherny-claude-mods-are-landing-now-someone-already-built-a-tetris-i--2099551291601248485|Claude Mods: function hooks no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-leoxbtt-bro-el-ingeniero-que-creo-claude-code-solto-un-video-de-28-m--2082108948505674112|Uso avançado do Claude Code]]", "[[extracts/x/bookmarks/2026-09-17-claudedevs-claude-design-claude-slides-and-claude-docs-also-work-inside--2100270861555228770|Apps Claude dentro do Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-rohanpaul_ai-claude-code-creator-boris-cherny-bcherny-for-people-who-aren--2082695402953031825|Podar configuração do Claude Code]]", "[[extracts/x/bookmarks/2026-09-18-claudedevs-today-we-re-rolling-out-projects-in-claude-code-on-desktop-a--2100633571543367691|Projects no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098382953235562613|Skill de output direto para coding agents]]"]
---

# Function Hooks no Claude Code

**@bcherny** · [2095590515765060076](https://x.com/bcherny/status/2095590515765060076) · `announcement`

## Resumo
Anúncio e RFC comunitário da extensibilidade profunda do Claude Code via function hooks em TypeScript (modelo de middleware Express/Koa), depois renomeado para 'Claude Mods', com shipping previsto em semanas. Vale salvar porque define a direção da plataforma de plugins do CC, incluindo controle administrativo fino e hooks de renderização/eventos.

## Pontos-chave
- Hooks são funções TypeScript com tipos completos e suporte a LSP que compõem como middleware: a ordem de registro define o aninhamento (admins prependam para controle, appendam para defaults) via modelo de continuação 'next' a la Express/Koa
- Segurança via rastreamento de side-effects sobre um objeto $ parametrizado; admins podem remover affordances de $ para impedir que plugins inferiores invoquem certos efeitos (governança programática fina)
- Renomeado para 'Claude Mods' no produto ('function hook' permanece como primitiva de implementação); primeiro, três mods built-in foram publicados e features existentes do CC serão migradas para forma de mod
- Hooks interceptam renderização (React: props e wrap de render nodes) e eventos de UI (ui.press vale em terminal e desktop); hook curinga em * vê todos os eventos, incluindo chamadas de plugins, permitindo audit log em uma função
- Casos de uso demonstrados: redação de segredos em tool output antes do modelo ler (plugin gerado por uma frase do Claude) e ocultar valores sensíveis na UI durante screen share; habilitar com CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude

## Links
- https://github.com/anthropics/claude-code/issues/91870

## Entidades
Claude Code, Claude Mods, function hooks, Express, Koa, React, TypeScript, CLAUDE_CODE_ENABLE_FUNCTION_HOOKS, Boris Cherny

> **Revisit:** `high` · **fonte:** `article`
