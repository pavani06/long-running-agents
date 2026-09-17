---
title: "Crew de agentes AI para Obsidian"
type: "extract"
source: "x"
status_id: "2099928503487517062"
handle: "tom_doerr"
url: "https://x.com/tom_doerr/status/2099928503487517062"
created_at: "2026-09-15T18:29:04.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-tom_doerr-manages-your-obsidian-vault-with-a-crew-of-8-ai-agents-and-1--2099928503487517062.json]]"
tags: ["agents", "multi-agent", "agentes-orquestracao", "knowledge-management", "memory-architecture", "agent-tooling"]
topic: "Crew de agentes AI para Obsidian"
summary: "Sistema de 8 agentes AI especializados e 14 skills que gerenciam um vault do Obsidian via conversa, com dispatcher que roteia mensagens para skills (fluxos conversacionais multi-etapa) ou agentes (tarefas reativas). Feito por um pesquisador de PhD para pessoas sobrecarregadas, funciona em qualquer idioma e se instala em quatro plataformas (Claude Code, Gemini CLI, OpenCode, Codex CLI) a partir de um único código-base."
key_points: ["Dispatcher com dupla delegação: skills rodam no contexto principal da conversa para workflows complexos (onboarding, email-triage, vault-audit) e são checadas primeiro; agentes cuidam de operações single-shot, com chaining automático entre agentes (ex.: Transcriber detecta novo projeto → Architect cria estrutura de pastas)", "Cada agente é isolado com seu próprio system prompt, restrições de ferramentas e atribuição de modelo — arquitetura clara de separação de responsabilidades em multi-agent", "Agentes customizados criados sem código via conversa com o Architect (/create-agent); agentes como budget-tracker, project-pulse e client-tracker resolvem problemas específicos do usuário", "Um único codebase compilado para quatro plataformas de agentes (Claude Code, Gemini CLI, OpenCode, Codex CLI), com installer traduzindo agentes, skills, hooks e MCP servers para o formato nativo de cada uma", "Vault segue estrutura híbrida PARA + Zettelasten que se adapta a pastas existentes durante onboarding; integra Gmail/Hey.com, Google Calendar e Apple Contacts via agente Postman"]
entities: ["Obsidian", "Claude Code", "Gemini CLI", "OpenCode", "Codex CLI", "Gmail", "Hey.com", "Google Calendar", "Apple Contacts"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/gnekt/My-Brain-Is-Full-Crew"]
media: ["https://pbs.twimg.com/media/HSRx2INWgAA4dWI.jpg"]
---

# Crew de agentes AI para Obsidian

**@tom_doerr** · [2099928503487517062](https://x.com/tom_doerr/status/2099928503487517062) · `tool`

## Resumo
Sistema de 8 agentes AI especializados e 14 skills que gerenciam um vault do Obsidian via conversa, com dispatcher que roteia mensagens para skills (fluxos conversacionais multi-etapa) ou agentes (tarefas reativas). Feito por um pesquisador de PhD para pessoas sobrecarregadas, funciona em qualquer idioma e se instala em quatro plataformas (Claude Code, Gemini CLI, OpenCode, Codex CLI) a partir de um único código-base.

## Pontos-chave
- Dispatcher com dupla delegação: skills rodam no contexto principal da conversa para workflows complexos (onboarding, email-triage, vault-audit) e são checadas primeiro; agentes cuidam de operações single-shot, com chaining automático entre agentes (ex.: Transcriber detecta novo projeto → Architect cria estrutura de pastas)
- Cada agente é isolado com seu próprio system prompt, restrições de ferramentas e atribuição de modelo — arquitetura clara de separação de responsabilidades em multi-agent
- Agentes customizados criados sem código via conversa com o Architect (/create-agent); agentes como budget-tracker, project-pulse e client-tracker resolvem problemas específicos do usuário
- Um único codebase compilado para quatro plataformas de agentes (Claude Code, Gemini CLI, OpenCode, Codex CLI), com installer traduzindo agentes, skills, hooks e MCP servers para o formato nativo de cada uma
- Vault segue estrutura híbrida PARA + Zettelasten que se adapta a pastas existentes durante onboarding; integra Gmail/Hey.com, Google Calendar e Apple Contacts via agente Postman

## Links
- https://github.com/gnekt/My-Brain-Is-Full-Crew

## Entidades
Obsidian, Claude Code, Gemini CLI, OpenCode, Codex CLI, Gmail, Hey.com, Google Calendar, Apple Contacts

> **Revisit:** `high` · **fonte:** `article`
