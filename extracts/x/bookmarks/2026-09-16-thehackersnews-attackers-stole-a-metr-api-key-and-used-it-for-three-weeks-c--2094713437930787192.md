---
title: "Vazamento de chave API da METR"
type: "extract"
source: "x"
status_id: "2094713437930787192"
handle: "TheHackersNews"
url: "https://x.com/TheHackersNews/status/2094713437930787192"
created_at: "2026-09-01T09:06:16.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-16-thehackersnews-attackers-stole-a-metr-api-key-and-used-it-for-three-weeks-c--2094713437930787192.json]]"
tags: ["agents", "evals", "permissions", "error-handling", "monitoramento"]
topic: "Vazamento de chave API da METR"
summary: "Atacantes exploraram um bug fail-open que desativou a autenticação Google em um dashboard público de agentes da METR, induziram um agente a revelar uma chave de API e a usaram por três semanas (~US$ 600 mil em créditos). Caso concreto dos riscos de expor agentes com segredos e autenticação que falha aberta."
key_points: ["Bug fail-open desativou a autenticação Google em um dashboard público de agentes, deixando o acesso aberto", "Atacante usou prompting para fazer o agente revelar a chave de API", "Chave foi usada por cerca de três semanas, consumindo ~US$ 600.000 em créditos", "Atacante adicionou persistência via SSH para manter acesso ao sistema exposto", "Lição: autenticação deve falhar fechada (fail-closed) e agentes não devem portar segredos exploráveis via prompt"]
entities: ["METR", "Google", "SSH"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: ["https://pbs.twimg.com/media/HRHqvMKbEAATASs.jpg"]
---

# Vazamento de chave API da METR

**@TheHackersNews** · [2094713437930787192](https://x.com/TheHackersNews/status/2094713437930787192) · `announcement`

## Resumo
Atacantes exploraram um bug fail-open que desativou a autenticação Google em um dashboard público de agentes da METR, induziram um agente a revelar uma chave de API e a usaram por três semanas (~US$ 600 mil em créditos). Caso concreto dos riscos de expor agentes com segredos e autenticação que falha aberta.

## Pontos-chave
- Bug fail-open desativou a autenticação Google em um dashboard público de agentes, deixando o acesso aberto
- Atacante usou prompting para fazer o agente revelar a chave de API
- Chave foi usada por cerca de três semanas, consumindo ~US$ 600.000 em créditos
- Atacante adicionou persistência via SSH para manter acesso ao sistema exposto
- Lição: autenticação deve falhar fechada (fail-closed) e agentes não devem portar segredos exploráveis via prompt

## Entidades
METR, Google, SSH

> **Revisit:** `medium` · **fonte:** `tweet`
