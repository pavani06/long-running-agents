---
title: "On-call automation with Claude"
type: "extract"
source: "x"
status_id: "2098508880921899197"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2098508880921899197"
created_at: "2026-09-11T20:28:00.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-here-s-how-our-team-uses-claude-tag-for-on-call-when-an-aler--2098508880921899197.json]]"
tags: ["agents", "agent-tooling", "monitoramento", "production", "escalation"]
topic: "On-call automation with Claude"
summary: "Equipe usa Claude Tag para triagem automática de incidentes: ao disparar alerta no Slack, Claude coleta métricas, compara deploys recentes e checa flags, diagnostica causa provável e propõe fix que o time aprova e faz merge. Vale salvar como padrão concreto de agente on-call com gate humano."
key_points: ["Alerta no Slack dispara o Claude automaticamente, sem espera humana para iniciar a triagem", "O agente puxa métricas, faz diff dos deploys recentes e verifica feature flags para investigar a causa", "Claude chega a uma causa provável e propõe uma correção concreta", "Fluxo mantém humano no circuito: o time aprova e faz o merge da fix proposta", "Motivação central é tempo de resposta — cada minuto conta em incidentes"]
entities: ["Claude Tag", "Claude", "Slack"]
content_type: "announcement"
revisit: "low"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/amplify_video_thumb/2098500211106832385/img/aF0irpPNkK3x7jrM.jpg"]
thin: false
theme: "Ecossistema Claude e Agentic Coding"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-claudedevs-our-ci-team-s-on-call-first-responder-is-claude-tag-it-reads--2097437571634639035|Agente Claude on-call para incidentes]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-sat-down-with-the-founders-of-wisprflow-useactively-and-p--2097415273645228460|Claude Managed Agents em produção]]", "[[extracts/x/bookmarks/2026-09-12-0xdeliriumm-boris-cherny-lead-of-claude-code-at-anthropic-published-a-pi--2081050632727793775|pipeline de code review com agentes]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420|Arquitetura de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-leoxbtt-bro-el-ingeniero-que-creo-claude-code-solto-un-video-de-28-m--2082108948505674112|Uso avançado do Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-undefinedki-spotify-just-published-the-internal-setup-their-engineers-us--2095942506433089832|Setup Claude Code no Spotify]]", "[[extracts/x/bookmarks/2026-09-12-marwan_3atef-datadog-put-agent-observability-in-your-coding-agent-and-the--2097986925088903355|Datadog Agent Observability para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-rlancemartin-i-recently-added-this-command-to-the-claude-api-skill-run-it--2095170001175199771|Comando prompt-audit para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-start-in-your-plugin-s-folder-and-run-claude-plugin-eval-ini--2098501001447870499|Eval de plugins Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-new-in-claude-code-your-sessions-can-now-message-each-other--2085817074816070014|Mensageria entre sessões no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-then-run-claude-plugin-eval-you-ll-see-each-case-s-score-wit--2098501002588823568|Claude plugin evaluation CLI]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-before-creating-a-session-and-sending-it-events-took-separat--2080009527467114737|Seeding de eventos na criação de sessão]]", "[[extracts/x/bookmarks/2026-09-12-poteto-new-in-dr-eggbot-v0-2-0-eggbot-can-do-a-health-check-on-all--2094967827019243547|Dr Eggbot rotinas health check]]"]
---

# On-call automation with Claude

**@ClaudeDevs** · [2098508880921899197](https://x.com/ClaudeDevs/status/2098508880921899197) · `announcement`

## Resumo
Equipe usa Claude Tag para triagem automática de incidentes: ao disparar alerta no Slack, Claude coleta métricas, compara deploys recentes e checa flags, diagnostica causa provável e propõe fix que o time aprova e faz merge. Vale salvar como padrão concreto de agente on-call com gate humano.

## Pontos-chave
- Alerta no Slack dispara o Claude automaticamente, sem espera humana para iniciar a triagem
- O agente puxa métricas, faz diff dos deploys recentes e verifica feature flags para investigar a causa
- Claude chega a uma causa provável e propõe uma correção concreta
- Fluxo mantém humano no circuito: o time aprova e faz o merge da fix proposta
- Motivação central é tempo de resposta — cada minuto conta em incidentes

## Entidades
Claude Tag, Claude, Slack

> **Revisit:** `low` · **fonte:** `tweet`
