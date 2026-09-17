---
title: "OpenMausBot: agentes em app de mensagens"
type: "extract"
source: "x"
status_id: "2099824976325157319"
handle: "milindlabs"
url: "https://x.com/milindlabs/status/2099824976325157319"
created_at: "2026-09-15T11:37:41.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-17-milindlabs-grok-bot-check-it-out-here-https-t-co-ujtre6f8mz-post-your-f--2099824976325157319.json]]"
tags: ["agents", "agent-tooling", "multi-agent", "harness", "permissions", "runtime", "context-management"]
topic: "OpenMausBot: agentes em app de mensagens"
summary: "OpenMausBot é um app desktop open-source e local-first, inspirado no Grok Bot, que transforma agentes locais (CLIs Claude/Codex/Grok) num roster de bots estilo app de mensagens — cada um com modelo próprio, memória do thread, computador e apps conectados. Vale salvar como referência de harness local com permission broker, drivers por provedor e plano de controle MCP."
key_points: ["Bring-your-own-agent: os bots rodam sobre os CLIs claude, codex e grok já instalados, usando logins/assinaturas existentes, sem contas novas nem proxy intermediário; qualquer engine pode apontar para um binário CLI customizado.", "Arquitetura de dois processos: app React sem transportes próprios envia comandos HTTP e consome um stream SSE; um harness server em 127.0.0.1 dono de todos os processos de agente, com registry de drivers (stream-JSON/JSON-RPC/ACP) que normalizam protocolos num stream canônico de eventos, logado como NDJSON por thread.", "Permission broker: comandos de shell, edições de arquivo e perguntas viram cards inline Allow/Deny no chat; controle do host é opt-in explícito e fail-closed (Wayland desabilitado até a issue #345), com runtime Cua verificado por hash e allowlist no empacotamento Linux.", "'Agentes com mãos': cada bot pode usar desktop Linux na nuvem (Box), VM local isolada ou o próprio computador, mais 500+ apps via sessões Composio (Gmail, Slack, GitHub, Notion, Linear); credenciais são write-only e persistem localmente em ~/.openmausbot.", "Expõe servidor MCP stdio com plano de controle deliberadamente limitado para clientes como Claude Desktop e Cursor (criar/configurar bots e canais, enviar trabalho, trocar modelo, interromper — sem aprovações, credenciais, deleção ou ciclo de vida do computador); times portáveis via .md com YAML frontmatter e rotinas com escalonamento que evita fila descontrolada."]
entities: ["OpenMausBot", "Grok Bot", "xAI", "Claude", "Codex", "Grok", "Composio", "Box", "ElevenLabs", "Fish Audio", "Chatterbox", "BotMRR", "Claude Desktop", "Cursor", "Tailscale", "Electron"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/milind-soni/OpenMausBot", "https://discord.com/invite/9Wb8MEpXRs"]
media: []
---

# OpenMausBot: agentes em app de mensagens

**@milindlabs** · [2099824976325157319](https://x.com/milindlabs/status/2099824976325157319) · `tool`

## Resumo
OpenMausBot é um app desktop open-source e local-first, inspirado no Grok Bot, que transforma agentes locais (CLIs Claude/Codex/Grok) num roster de bots estilo app de mensagens — cada um com modelo próprio, memória do thread, computador e apps conectados. Vale salvar como referência de harness local com permission broker, drivers por provedor e plano de controle MCP.

## Pontos-chave
- Bring-your-own-agent: os bots rodam sobre os CLIs claude, codex e grok já instalados, usando logins/assinaturas existentes, sem contas novas nem proxy intermediário; qualquer engine pode apontar para um binário CLI customizado.
- Arquitetura de dois processos: app React sem transportes próprios envia comandos HTTP e consome um stream SSE; um harness server em 127.0.0.1 dono de todos os processos de agente, com registry de drivers (stream-JSON/JSON-RPC/ACP) que normalizam protocolos num stream canônico de eventos, logado como NDJSON por thread.
- Permission broker: comandos de shell, edições de arquivo e perguntas viram cards inline Allow/Deny no chat; controle do host é opt-in explícito e fail-closed (Wayland desabilitado até a issue #345), com runtime Cua verificado por hash e allowlist no empacotamento Linux.
- 'Agentes com mãos': cada bot pode usar desktop Linux na nuvem (Box), VM local isolada ou o próprio computador, mais 500+ apps via sessões Composio (Gmail, Slack, GitHub, Notion, Linear); credenciais são write-only e persistem localmente em ~/.openmausbot.
- Expõe servidor MCP stdio com plano de controle deliberadamente limitado para clientes como Claude Desktop e Cursor (criar/configurar bots e canais, enviar trabalho, trocar modelo, interromper — sem aprovações, credenciais, deleção ou ciclo de vida do computador); times portáveis via .md com YAML frontmatter e rotinas com escalonamento que evita fila descontrolada.

## Links
- https://github.com/milind-soni/OpenMausBot
- https://discord.com/invite/9Wb8MEpXRs

## Entidades
OpenMausBot, Grok Bot, xAI, Claude, Codex, Grok, Composio, Box, ElevenLabs, Fish Audio, Chatterbox, BotMRR, Claude Desktop, Cursor, Tailscale, Electron

> **Revisit:** `high` · **fonte:** `article`
