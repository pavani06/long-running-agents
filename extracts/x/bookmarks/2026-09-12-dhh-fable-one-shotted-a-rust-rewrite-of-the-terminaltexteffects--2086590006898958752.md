---
title: "AI one-shot Rust rewrite performance"
type: "extract"
source: "x"
status_id: "2086590006898958752"
handle: "dhh"
url: "https://x.com/dhh/status/2086590006898958752"
created_at: "2026-08-09T23:06:39.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-dhh-fable-one-shotted-a-rust-rewrite-of-the-terminaltexteffects--2086590006898958752.json]]"
tags: ["agentic-coding", "performance", "agents", "agent-tooling"]
topic: "AI one-shot Rust rewrite performance"
summary: "DHH relata que o agente de código Fable reescreveu de uma vez a biblioteca TerminalTextEffects de Python para Rust usando 11M de tokens, derrubando o startup de 87ms para 2ms e acelerando a renderização em 9.6x. Resultado: binário único de 3MB com zero dependências, evidência concreta de agentes resolvendo rewrites inteiros de linguagem."
key_points: ["Rewrite completo de Python para Rust executado em um único 'shot' pelo agente Fable, consumindo 11M de tokens", "Tempo de startup caiu de 87ms para 2ms (ganho de ~43x)", "Velocidade de renderização 9.6x maior que a versão original em Python", "Produto final: executável único de 3MB com zero dependências, eliminando o overhead do ecossistema Python", "Caso prático de agentic coding aplicado a engenharia de performance e migração de runtime"]
entities: ["DHH", "Fable", "TerminalTextEffects", "Rust", "Python"]
content_type: "announcement"
revisit: "medium"
grounded_in: "article"
links: ["https://claude.ai/code/artifact/287825bc-7aad-4541-a7e7-fa4ba8d03612"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-openaidevs-habitat-is-openai-s-online-storage-platform-that-powers-ever--2098502006935814272|Habitat: storage da OpenAI em Rust]]", "[[extracts/x/bookmarks/2026-09-12-openaidevs-while-we-ve-now-launched-a-rust-rewrite-we-re-sharing-those--2098502031338340416|Escalonando storage Python na OpenAI]]", "[[extracts/x/bookmarks/2026-09-12-ubereng-we-cut-uber-eats-search-latency-in-half-how-measure-identify--2098177194979983830|Uber Eats search latency halving]]", "[[extracts/x/bookmarks/2026-09-12-zodchiii-the-creator-of-claude-code-boris-cherny-every-night-i-have-h--2079182515462369399|Engenharia com loops de agentes]]", "[[extracts/x/bookmarks/2026-09-12-agenticgirl-ripwire-from-red-hat-emerging-technologies-is-a-remarkably-s--2096612794145911260|contexto de repositório para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-hwchase17-kai-is-very-cool-and-every-company-should-have-a-kai-this-ep--2097355841183596632|Stripe Kai: agente interno com Deep Agents]]"]
---

# AI one-shot Rust rewrite performance

**@dhh** · [2086590006898958752](https://x.com/dhh/status/2086590006898958752) · `announcement`

## Resumo
DHH relata que o agente de código Fable reescreveu de uma vez a biblioteca TerminalTextEffects de Python para Rust usando 11M de tokens, derrubando o startup de 87ms para 2ms e acelerando a renderização em 9.6x. Resultado: binário único de 3MB com zero dependências, evidência concreta de agentes resolvendo rewrites inteiros de linguagem.

## Pontos-chave
- Rewrite completo de Python para Rust executado em um único 'shot' pelo agente Fable, consumindo 11M de tokens
- Tempo de startup caiu de 87ms para 2ms (ganho de ~43x)
- Velocidade de renderização 9.6x maior que a versão original em Python
- Produto final: executável único de 3MB com zero dependências, eliminando o overhead do ecossistema Python
- Caso prático de agentic coding aplicado a engenharia de performance e migração de runtime

## Links
- https://claude.ai/code/artifact/287825bc-7aad-4541-a7e7-fa4ba8d03612

## Entidades
DHH, Fable, TerminalTextEffects, Rust, Python

> **Revisit:** `medium` · **fonte:** `article`
