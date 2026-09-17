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
relates-to: ["[[extracts/x/bookmarks/2026-09-12-simonw-wow-turns-out-another-openai-agent-swarm-was-busy-spamming-a--2098573718142452055|Ataque de agentes OpenAI ao RubyGems]]", "[[extracts/x/bookmarks/2026-09-12-andrewcurran_-a-man-in-australia-asked-his-agent-claude-running-on-opencla--2086567854850384054|agente explora vulnerabilidade em agendamento]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-it-s-well-known-that-agents-hack-benchmark-rewards-the-usual--2098592449568591902|reward hacking em benchmarks de agentes]]", "[[extracts/x/bookmarks/2026-09-12-yenkel-great-to-see-the-muse-team-took-security-seriously-https-t-c--2097428458120835085|Arquitetura de segurança de agentes pessoais]]", "[[extracts/x/bookmarks/2026-09-17-mstryoda_-cloudflare-ai-agentlar-icin-security-skill-yaynlams-direkt-y--2099560068362441009|Skill de segurança da Cloudflare]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-finally-an-open-source-runtime-security-layer-for-your-agent--2098042808221511836|runtime security layer para agentes]]", "[[extracts/x/bookmarks/2026-09-12-bzuer_-victorosaraiva-pergunto-quem-e-jefferson-silva-quem-usa-hewl--2095704063081849159|verificação de metadados de documento]]", "[[extracts/x/bookmarks/2026-09-12-david_agape_-mendonca-tirou-o-sigilo-da-pet-15-556-e-de-14-processos-do-m--2098255698933006755|Sigilo STF caso Master]]"]
theme: "Claude Code e Coding Agêntico"
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
