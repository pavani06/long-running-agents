---
title: "Compacção de contexto verbatim para Claude Code"
type: "extract"
source: "x"
status_id: "2100694552369897539"
handle: "tamarajtran"
url: "https://x.com/tamarajtran/status/2100694552369897539"
created_at: "2026-09-17T21:13:04.000Z"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-19-tamarajtran-run-fast-jev-compaction-https-t-co-htdjnjnlaa--2100694552369897539.json]]"
tags: ["context-engineering", "context-management", "token-budgeting", "agent-tooling", "harness", "agents"]
topic: "Compacção de contexto verbatim para Claude Code"
summary: "Plugin do Claude Code e biblioteca npm (fast-jev-compaction) que substitui o resumo de compacção por decisões do modelo Jev: cada tool call/result é pontuado, os obsoletos são removidos ou truncados e todo o resto permanece verbatim — eliminando a perda de informação inerente a sumarizações."
key_points: ["Sumarização de contexto é lossy (paths, erros exatos, constraints e comandos podem desaparecer); a lib nunca reescreve nada — só deleta/trunca tool calls e results que o Jev marca como dispensáveis, mantendo texto de user/assistant verbatim e em ordem.", "Estado completo é enviado ao Jev com fitting em estágios (truncar tool inputs para 1000/200/60 chars, abreviar textos antigos head+tail, colapsar mensagens antigas) até caber em maxStateTokens (25k default), com tokens estimados sem tokenizer.", "Para cada call não-pinada, duas perguntas ao Jev: manter a call e manter o resultado verbatim; decisões contra keepThreshold (0.5) resultam em keep / truncate (mantém cabeça de 300 chars + nota) / remove; primeiras e mais recentes mensagens (default 6) são sempre preservadas.", "Perguntas são divididas em lotes para manter state+perguntas sob 30k tokens (limite do Jev é 32k), rodando requisições concorrentes com merge das respostas; falhas do Jev lançam exceção e o hook faz fallback para o summary nativo do Claude Code.", "Distribuído como pacote npm + plugin de function hooks do Claude Code (early-access 2.1.274+, requer CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1); building blocks (collectToolCalls, fitState, decideCall, applyDecisions) são exportados e o transport é injetável via interface JevAsker."]
entities: ["Claude Code", "Jev", "TypeSafe", "fast-jev-compaction", "npm", "Tamara Tran"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/tamaratran/fast-jev-compaction"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-19-altryne-this-is-actually-insane-this-uses-typesafeai-jev-model-as-a--2100739055923425589|Compressão de contexto em sessões Claude]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-found-the-perfect-use-case-for-typesafeai-jev-instant-compac--2100694549362553153|compaction instantânea de contexto em agentes]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-theo-thank-you-for-your-post-totally-understand-but-i-disagr--2100769054789378301|compaction de contexto no Claude Code]]", "[[extracts/x/bookmarks/2026-09-19-grok-pumuonx-theo-tamarajtran-theo-is-right-on-the-core-issues-th--2100825243669409961|poda de contexto vs compaction nativa]]", "[[extracts/x/bookmarks/2026-09-12-bcherny-your-input-needed-would-you-use-this-this-is-an-early-look-a--2095590515765060076|Function Hooks no Claude Code]]", "[[extracts/x/bookmarks/2026-09-15-bcherny-claude-mods-are-landing-now-someone-already-built-a-tetris-i--2099551291601248485|Claude Mods: function hooks no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-trevin-using-fable-5-1-add-this-to-your-claude-md-file-to-help-its--2095410064492507274|Prompting Claude Fable 5.1]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-evals-call-the-model-so-they-use-tokens-and-results-vary-pil--2098501003666702344|Evals de plugins no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-then-run-claude-plugin-eval-you-ll-see-each-case-s-score-wit--2098501002588823568|Claude plugin evaluation CLI]]", "[[extracts/x/bookmarks/2026-09-19-tamarajtran-theo-thats-not-specific-to-jev-compaction-summarize-based-co--2100773452475183219|context compaction limitations]]"]
theme: "Tooling e infra de agentes"
---

# Compacção de contexto verbatim para Claude Code

**@tamarajtran** · [2100694552369897539](https://x.com/tamarajtran/status/2100694552369897539) · `tool`

## Resumo
Plugin do Claude Code e biblioteca npm (fast-jev-compaction) que substitui o resumo de compacção por decisões do modelo Jev: cada tool call/result é pontuado, os obsoletos são removidos ou truncados e todo o resto permanece verbatim — eliminando a perda de informação inerente a sumarizações.

## Pontos-chave
- Sumarização de contexto é lossy (paths, erros exatos, constraints e comandos podem desaparecer); a lib nunca reescreve nada — só deleta/trunca tool calls e results que o Jev marca como dispensáveis, mantendo texto de user/assistant verbatim e em ordem.
- Estado completo é enviado ao Jev com fitting em estágios (truncar tool inputs para 1000/200/60 chars, abreviar textos antigos head+tail, colapsar mensagens antigas) até caber em maxStateTokens (25k default), com tokens estimados sem tokenizer.
- Para cada call não-pinada, duas perguntas ao Jev: manter a call e manter o resultado verbatim; decisões contra keepThreshold (0.5) resultam em keep / truncate (mantém cabeça de 300 chars + nota) / remove; primeiras e mais recentes mensagens (default 6) são sempre preservadas.
- Perguntas são divididas em lotes para manter state+perguntas sob 30k tokens (limite do Jev é 32k), rodando requisições concorrentes com merge das respostas; falhas do Jev lançam exceção e o hook faz fallback para o summary nativo do Claude Code.
- Distribuído como pacote npm + plugin de function hooks do Claude Code (early-access 2.1.274+, requer CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1); building blocks (collectToolCalls, fitState, decideCall, applyDecisions) são exportados e o transport é injetável via interface JevAsker.

## Links
- https://github.com/tamaratran/fast-jev-compaction

## Entidades
Claude Code, Jev, TypeSafe, fast-jev-compaction, npm, Tamara Tran

> **Revisit:** `high` · **fonte:** `article`
