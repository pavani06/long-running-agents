---
title: "Agente de outbound prospecting com spec"
type: "extract"
source: "x"
status_id: "2099876439663243402"
handle: "grok"
url: "https://x.com/grok/status/2099876439663243402"
created_at: "2026-09-15T15:02:11.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-grok-outbound-prospector-built-icp-matched-prospect-lists-researc--2099876439663243402.json]]"
tags: ["agents", "agent-loop", "state", "gate-design", "verification", "context-management", "startups"]
topic: "Agente de outbound prospecting com spec"
summary: "Spec de um agente que monta listas ICP a partir da web pública, pesquisa cada prospect e redige a primeira mensagem, com todo fato atrelado a URL-fonte e nada enviado sem aprovação explícita (economia de 12h/semana). Vale salvar como referência de design: estado de trabalho em arquivos, enums fixos e gates humanos."
key_points: ["Estado de trabalho vive em arquivos, não em memória: lista-alvo (uma linha por pessoa), notas de enriquecimento, rascunhos datados e log de outreach; re-ler antes de cada execução e escrever de volta — o chat não é fonte de verdade.", "Campos com vocabulário fixo: icp_fit (strong/maybe/weak), canal (email/linkedin/x/other) e status ordenado new→enriched→drafted→approved→sent→replied→meeting/no/on hold; linha só chega a 'sent' quando o usuário confirma.", "Zero fabricação: nunca inventar pessoa, cargo, email, rodada de funding ou citação; fato sem URL de fonte fica em branco e email nunca é construído por padrão; diz quando uma linha está rasa.", "Human-in-the-loop por padrão: rascunha mas nunca envia/mensagem sem 'sim' explícito; rotinas agendadas (rascunhos em dia útil, recap de sexta, top-up de lista de segunda) ficam desligadas até ativação e rodam no timezone do usuário.", "Escopo restrito e onboarding rápido: só primeiro contato outbound (sem inbound, CRM ou sequências além de 4 toques); skill 'Getting started' coleta prefs (o que vende, títulos-alvo, ask, provas, do-not-contact, idioma, volume diário) e entrega lista real ou rascunho em menos de um minuto."]
entities: ["Outbound Prospector", "Krista Letz", "Grok"]
content_type: "resource"
revisit: "medium"
grounded_in: "article"
thin: false
links: ["https://x.ai/bot/marketplace/bots/pg"]
media: ["https://pbs.twimg.com/media/HSRBvXRXEAAdSUJ.jpg"]
---

# Agente de outbound prospecting com spec

**@grok** · [2099876439663243402](https://x.com/grok/status/2099876439663243402) · `resource`

## Resumo
Spec de um agente que monta listas ICP a partir da web pública, pesquisa cada prospect e redige a primeira mensagem, com todo fato atrelado a URL-fonte e nada enviado sem aprovação explícita (economia de 12h/semana). Vale salvar como referência de design: estado de trabalho em arquivos, enums fixos e gates humanos.

## Pontos-chave
- Estado de trabalho vive em arquivos, não em memória: lista-alvo (uma linha por pessoa), notas de enriquecimento, rascunhos datados e log de outreach; re-ler antes de cada execução e escrever de volta — o chat não é fonte de verdade.
- Campos com vocabulário fixo: icp_fit (strong/maybe/weak), canal (email/linkedin/x/other) e status ordenado new→enriched→drafted→approved→sent→replied→meeting/no/on hold; linha só chega a 'sent' quando o usuário confirma.
- Zero fabricação: nunca inventar pessoa, cargo, email, rodada de funding ou citação; fato sem URL de fonte fica em branco e email nunca é construído por padrão; diz quando uma linha está rasa.
- Human-in-the-loop por padrão: rascunha mas nunca envia/mensagem sem 'sim' explícito; rotinas agendadas (rascunhos em dia útil, recap de sexta, top-up de lista de segunda) ficam desligadas até ativação e rodam no timezone do usuário.
- Escopo restrito e onboarding rápido: só primeiro contato outbound (sem inbound, CRM ou sequências além de 4 toques); skill 'Getting started' coleta prefs (o que vende, títulos-alvo, ask, provas, do-not-contact, idioma, volume diário) e entrega lista real ou rascunho em menos de um minuto.

## Links
- https://x.ai/bot/marketplace/bots/pg

## Entidades
Outbound Prospector, Krista Letz, Grok

> **Revisit:** `medium` · **fonte:** `article`
