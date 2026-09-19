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
relates-to: ["[[extracts/x/bookmarks/2026-09-16-grok-try-grok-bot-https-t-co-fo8jkd1aeq--2099876446864867561|Lançamento do Grok Bot (agentes computer-use)]]", "[[extracts/x/bookmarks/2026-09-16-tom_doerr-manages-your-obsidian-vault-with-a-crew-of-8-ai-agents-and-1--2099928503487517062|Crew de agentes AI para Obsidian]]", "[[extracts/x/bookmarks/2026-09-18-hnshah-i-watched-matt-silberman-show-how-he-uses-grok-bot-for-marke--2100648731003724156|Setup multi-bot para marketing ops]]", "[[extracts/x/bookmarks/2026-09-17-teddyinmedia-your-ai-agent-can-now-collect-data-from-almost-any-website-x--2099859887102558507|Agent Reach: acesso web para agentes]]", "[[extracts/x/bookmarks/2026-09-12-simonw-here-s-my-attempt-at-explaining-what-chatgpt-work-can-actual--2094214737957691854|Capacidades do ChatGPT Work]]", "[[extracts/x/bookmarks/2026-09-16-benln-new-grok-bot-guides-added-includes-bot-for-engineering-suppo--2099849826120683967|Grok Bot usage guides]]", "[[extracts/x/bookmarks/2026-09-12-andrewyng-openworker-an-open-source-agent-that-doesn-t-just-chat-but-c--2092315079576555806|OpenWorker: agente open source de tarefas locais]]", "[[extracts/x/bookmarks/2026-09-17-milindlabs-some-people-are-already-saying-this-is-better-than-grok-bot--2099819771151933539|alternativa open-source ao Grok]]", "[[extracts/x/bookmarks/2026-09-12-simonw-just-noticed-the-chatgpt-desktop-app-previously-named-codex--2094864223683903800|LibreOffice embutido no ChatGPT desktop]]", "[[extracts/x/bookmarks/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-kit-that-changes-two--2098361620493660493|kit para bots no Hermes Desktop]]", "[[extracts/x/bookmarks/2026-09-19-signulll-all-of-my-imessages-amp-email-now-run-through-a-single-agent--2100728355414737351|Agente único para mensagens e email]]"]
theme: "Tooling e infra de agentes"
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
