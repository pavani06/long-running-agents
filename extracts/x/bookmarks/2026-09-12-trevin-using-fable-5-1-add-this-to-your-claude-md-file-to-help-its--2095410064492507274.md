---
title: "Prompting Claude Fable 5.1"
type: "extract"
source: "x"
status_id: "2095410064492507274"
handle: "trevin"
url: "https://x.com/trevin/status/2095410064492507274"
created_at: "2026-09-03T07:14:24.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-trevin-using-fable-5-1-add-this-to-your-claude-md-file-to-help-its--2095410064492507274.json]]"
tags: ["agent-loop", "harness-engineering", "evals", "context-management", "model-selection"]
topic: "Prompting Claude Fable 5.1"
summary: "Documentação oficial de prompting do Claude Fable 5.1: diferenças comportamentais vs Fable 5 e receitas concretas para effort levels, progress updates, batching de tool calls, histórico append-only e compactação. Vale salvar como referência de harness para os novos betas de API (thinking display, turn-scoped system messages, block binding)."
key_points: ["Effort é o controle primário do tradeoff inteligência/latência/custo; re rode o sweep de níveis (low/medium/xhigh/max) mesmo quem já testou no Fable 5, pois os nomes não correspondem ao mesmo amount de thinking entre modelos; no low, Fable 5.1 compete com Opus/Sonnet em custo por tarefa", "Fable 5.1 emite menos updates visíveis ao usuário entre tool calls; ativar thinking.display: \"updates\" (beta header) e renderizar blocos thinking como status lines; auditar e remover instruções antigas que suprimem narração", "Em loops de coding/computer-use o modelo pode emitir um tool call por turno; corrigir com nudge turn-scoped system message (clear_at: \"next_user_message\", beta) reanexado a cada turno byte-for-byte, sem deletar cópias anteriores", "Histórico deve ser append-only: thinking blocks só são válidos na conversa exata que os produziu (enforcement para contas criadas após 31/08/2026); editar turnos anteriores retorna 400 ou dropa blocos, além de reiniciar o prompt cache", "Na compactação client-side, substituir todo o histórico por uma mensagem-resumo + novo user turn sem replay; com cache reads mais baratos, compactar cedo pode deixar de valer a pena — testar compactação mais tardia"]
entities: ["Claude Fable 5.1", "Claude Fable 5", "Claude Mythos 5.1", "Claude Opus", "Claude Sonnet", "Anthropic API", "CLAUDE.md", "@trevin"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#writing-density"]
media: []
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-trq212-we-removed-80-of-the-claude-code-system-prompt-for-our-newes--2080710971228918066|System prompts e CLAUDE.md para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-pawelhuryn-opus-5-is-way-better-than-4-8-but-cutting-80-of-its-instruct--2086732722261643450|CLAUDE.md blocks for Opus 5]]", "[[extracts/x/bookmarks/2026-09-12-daniel_mac8-fable-advisor-now-uses-opus-5-as-orchestrator-opus-5-shines--2081056595555868752|fable-advisor com Opus 5 como orquestrador]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420|Arquitetura de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-anatolikopadze-anthropic-engineer-you-re-not-supposed-to-prompt-claude-you--2080286550005358977|Sistemas que se auto-promptam em agentes]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-a-few-days-ago-anthropic-shared-this-brilliant-prompt-i-was--2097059598960132110|Prompt de escrita da Anthropic]]", "[[extracts/x/bookmarks/2026-09-12-felixrieseberg-today-we-re-releasing-fable-5-1-and-mythos-5-1-while-the-mod--2094849655167471773|Lançamento Fable 5.1 e Mythos 5.1]]"]
theme: "Ecossistema Claude e Agent Tooling"
---

# Prompting Claude Fable 5.1

**@trevin** · [2095410064492507274](https://x.com/trevin/status/2095410064492507274) · `resource`

## Resumo
Documentação oficial de prompting do Claude Fable 5.1: diferenças comportamentais vs Fable 5 e receitas concretas para effort levels, progress updates, batching de tool calls, histórico append-only e compactação. Vale salvar como referência de harness para os novos betas de API (thinking display, turn-scoped system messages, block binding).

## Pontos-chave
- Effort é o controle primário do tradeoff inteligência/latência/custo; re rode o sweep de níveis (low/medium/xhigh/max) mesmo quem já testou no Fable 5, pois os nomes não correspondem ao mesmo amount de thinking entre modelos; no low, Fable 5.1 compete com Opus/Sonnet em custo por tarefa
- Fable 5.1 emite menos updates visíveis ao usuário entre tool calls; ativar thinking.display: "updates" (beta header) e renderizar blocos thinking como status lines; auditar e remover instruções antigas que suprimem narração
- Em loops de coding/computer-use o modelo pode emitir um tool call por turno; corrigir com nudge turn-scoped system message (clear_at: "next_user_message", beta) reanexado a cada turno byte-for-byte, sem deletar cópias anteriores
- Histórico deve ser append-only: thinking blocks só são válidos na conversa exata que os produziu (enforcement para contas criadas após 31/08/2026); editar turnos anteriores retorna 400 ou dropa blocos, além de reiniciar o prompt cache
- Na compactação client-side, substituir todo o histórico por uma mensagem-resumo + novo user turn sem replay; com cache reads mais baratos, compactar cedo pode deixar de valer a pena — testar compactação mais tardia

## Links
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1#writing-density

## Entidades
Claude Fable 5.1, Claude Fable 5, Claude Mythos 5.1, Claude Opus, Claude Sonnet, Anthropic API, CLAUDE.md, @trevin

> **Revisit:** `high` · **fonte:** `article`
