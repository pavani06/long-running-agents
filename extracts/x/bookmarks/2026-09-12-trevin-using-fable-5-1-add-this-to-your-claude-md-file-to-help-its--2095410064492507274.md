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
