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
relates-to: ["[[extracts/x/bookmarks/2026-09-16-grok-haggle-bot-audited-125-vendor-contracts-reached-out-to-the-v--2099876435737325724|Agente de negociação de gastos SaaS]]", "[[extracts/x/bookmarks/2026-09-16-grok-seo-amp-aeo-desk-automated-keyword-research-into-writer-read--2099876443761111255|Agente de SEO/AEO para briefs de conteúdo]]", "[[extracts/x/bookmarks/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-layer-that-sits-on-t--2098020649662816503|Roteamento e memória no Hermes Agent]]", "[[extracts/x/bookmarks/2026-09-15-mattyp-each-day-grok-bot-looks-at-my-x-bookmarks-for-things-i-find--2099482348010328185|pipeline automatizado de demos com agentes]]", "[[extracts/x/bookmarks/2026-09-12-adiix_official-how-to-run-your-whole-grok-bot-workday-on-loops-instead-of-p--2095464614498619493|Orquestração de Grok Bot em loops]]", "[[extracts/x/bookmarks/2026-09-14-cyrilxbt-every-department-installable-developers-superpowers-https-t--2098652326248493447|Superpowers: metodologia para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-this-has-ended-up-being-better-than-expected-and-fills-an-in--2094156122441625770|AFK agent workflow vs /implement-spec]]"]
theme: "Agentes autônomos e orquestração"
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
