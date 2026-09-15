---
title: "Superpowers: metodologia para coding agents"
type: "extract"
source: "x"
status_id: "2098652326248493447"
handle: "cyrilXBT"
url: "https://x.com/cyrilXBT/status/2098652326248493447"
created_at: "2026-09-12T05:58:00.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-cyrilxbt-every-department-installable-developers-superpowers-https-t--2098652326248493447.json]]"
tags: ["agent-tooling", "agentic-coding", "spec-driven-development", "testes-qa", "code-review", "multi-agent", "harness"]
topic: "Superpowers: metodologia para coding agents"
summary: "Superpowers é uma metodologia completa de engenharia de software para agentes de código, baseada em skills compostáveis que disparam automaticamente — do brainstorm/spec à execução por subagentes com TDD e revisão em dois estágios. Vale salvar como referência concreta de como estruturar workflows obrigatórios (não sugestões) em agentes de código."
key_points: ["Pipeline completo e automático: brainstorming extrai a spec da conversa, apresenta o design em pedaços digeríveis, e após aprovação gera plano de implementação explícito enfatizando TDD vermelho-verde verdadeiro, YAGNI e DRY.", "Subagent-driven-development: um subagente novo por tarefa com revisão em dois estágios (conformidade com a spec, depois qualidade de código); o agente pode trabalhar autonomamente por horas sem desviar do plano.", "Skills são workflows obrigatórios, não sugestões: o agente checa skills relevantes antes de qualquer tarefa; a skill de TDD chega a deletar código escrito antes dos testes; issues críticos de code review bloqueiam progresso.", "Instalável em praticamente todos os harnesses (Claude Code, Codex, Cursor, Gemini, Copilot, Grok, Kimi Code, OpenCode, Devin, Droid, Antigravity, Pi, Hermes), sempre separadamente por harness; skills cobrem também debugging sistemático em 4 fases e verificação antes de declarar conclusão.", "Filosofia explícita: sistemático sobre ad-hoc, simplicidade como objetivo primário, evidência sobre afirmações; MIT, criado por Jesse Vincent/Prime Radiant, com suporte comercial para enterprise e telemetry opcional desativável."]
entities: ["Superpowers", "Jesse Vincent", "Prime Radiant", "Claude Code", "Codex", "Cursor", "GitHub Copilot", "Gemini", "Grok", "Kimi Code", "OpenCode", "Devin", "Context7", "Skill Creator", "MCP Builder", "Webapp Testing", "Claude-Mem"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/obra/superpowers", "https://github.com/upstash/context7", "https://github.com/anthropics/skills"]
media: []
---

# Superpowers: metodologia para coding agents

**@cyrilXBT** · [2098652326248493447](https://x.com/cyrilXBT/status/2098652326248493447) · `tool`

## Resumo
Superpowers é uma metodologia completa de engenharia de software para agentes de código, baseada em skills compostáveis que disparam automaticamente — do brainstorm/spec à execução por subagentes com TDD e revisão em dois estágios. Vale salvar como referência concreta de como estruturar workflows obrigatórios (não sugestões) em agentes de código.

## Pontos-chave
- Pipeline completo e automático: brainstorming extrai a spec da conversa, apresenta o design em pedaços digeríveis, e após aprovação gera plano de implementação explícito enfatizando TDD vermelho-verde verdadeiro, YAGNI e DRY.
- Subagent-driven-development: um subagente novo por tarefa com revisão em dois estágios (conformidade com a spec, depois qualidade de código); o agente pode trabalhar autonomamente por horas sem desviar do plano.
- Skills são workflows obrigatórios, não sugestões: o agente checa skills relevantes antes de qualquer tarefa; a skill de TDD chega a deletar código escrito antes dos testes; issues críticos de code review bloqueiam progresso.
- Instalável em praticamente todos os harnesses (Claude Code, Codex, Cursor, Gemini, Copilot, Grok, Kimi Code, OpenCode, Devin, Droid, Antigravity, Pi, Hermes), sempre separadamente por harness; skills cobrem também debugging sistemático em 4 fases e verificação antes de declarar conclusão.
- Filosofia explícita: sistemático sobre ad-hoc, simplicidade como objetivo primário, evidência sobre afirmações; MIT, criado por Jesse Vincent/Prime Radiant, com suporte comercial para enterprise e telemetry opcional desativável.

## Links
- https://github.com/obra/superpowers
- https://github.com/upstash/context7
- https://github.com/anthropics/skills

## Entidades
Superpowers, Jesse Vincent, Prime Radiant, Claude Code, Codex, Cursor, GitHub Copilot, Gemini, Grok, Kimi Code, OpenCode, Devin, Context7, Skill Creator, MCP Builder, Webapp Testing, Claude-Mem

> **Revisit:** `high` · **fonte:** `article`
