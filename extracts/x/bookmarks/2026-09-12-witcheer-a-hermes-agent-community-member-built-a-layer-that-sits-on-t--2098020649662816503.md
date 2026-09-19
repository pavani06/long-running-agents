---
title: "Roteamento e memória no Hermes Agent"
type: "extract"
source: "x"
status_id: "2098020649662816503"
handle: "witcheer"
url: "https://x.com/witcheer/status/2098020649662816503"
created_at: "2026-09-10T12:07:56.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-layer-that-sits-on-t--2098020649662816503.json]]"
tags: ["agents", "agent-tooling", "agentes-orquestracao", "model-selection", "context-management", "memory-architecture", "verification", "gate-design"]
topic: "Roteamento e memória no Hermes Agent"
summary: "Membro da comunidade do Hermes Agent construiu uma camada de orquestração que decide por execução qual modelo e esforço usar, quais skills de especialista carregar e o que conta como 'done', com memória curada: candidatos passam por uma review card antes de serem aceitos. Vale salvar como referência de arquitetura com roteamento por tarefa e memória com gate de revisão."
key_points: ["Roteamento por tarefa: a camada escolhe dinamicamente o modelo e o nível de esforço alocado a cada execução", "Carregamento condicional de specialist skills, controlando o que entra no contexto de cada run", "Critério explícito de conclusão ('what counts as done'), funcionando como gate de verificação", "A peça distintiva é a memória: um candidato vai para uma review card antes de ser incorporado — memória curada por revisão, não escrita passiva", "O tweet está truncado; detalhes finais do mecanismo de review não aparecem"]
entities: ["Hermes Agent", "witcheer"]
content_type: "announcement"
revisit: "medium"
grounded_in: "tweet"
links: []
media: []
thin: false
theme: "Agent Harness Engineering"
relates-to: ["[[extracts/x/bookmarks/2026-09-17-jacquelinesyc19-a-few-weeks-ago-i-wrote-that-our-whole-team-at-artie-uses-he--2100262432413528336|Hermes como harness de agentes por equipe]]", "[[extracts/x/bookmarks/2026-09-12-sophiamyang-someone-please-tell-me-this-exists-a-meta-harness-kanban-boa--2098112529796878408|orquestração multi-plataforma de agentes]]", "[[extracts/x/bookmarks/2026-09-12-zostaff-this-paper-completely-changed-how-i-think-about-agent-memory--2078944176457359536|Arquitetura de memória para agentes]]", "[[extracts/x/bookmarks/2026-09-16-tom_doerr-manages-your-obsidian-vault-with-a-crew-of-8-ai-agents-and-1--2099928503487517062|Crew de agentes AI para Obsidian]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-google-if-you-maintain-a-skill-library-for--2093324233158045788|Evolução de skills em agentes]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-i-built-a-self-evolving-code-review-agent-most-code-review-a--2098416224803987968|Agente de code review auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-14-ethereaglehq-andrewchen-upfront-classify-then-upgrade-if-it-gets-long-is--2099290400779317310|gatilhos de complexidade em agentes]]", "[[extracts/x/bookmarks/2026-09-14-ethereaglehq-andrewchen-arch-router-picking-local-vs-cloud-is-the-piece-i--2099260781447496188|roteamento de modelos local vs cloud]]", "[[extracts/x/bookmarks/2026-09-12-voxyz_ai-codex-tip-a-cost-efficient-luna-sol-agent-tree-orchestrated--2097814698204832116|orquestração de agentes com Codex]]", "[[extracts/x/bookmarks/2026-09-16-grok-outbound-prospector-built-icp-matched-prospect-lists-researc--2099876439663243402|Agente de outbound prospecting com spec]]", "[[extracts/x/bookmarks/2026-09-18-george_sequeira-josharosen-typesafeai-the-drift-verification-split-is-a-usef--2100642769832231072|Verificação determinística vs. juiz-modelo em agentes]]", "[[extracts/x/bookmarks/2026-09-12-voxyz_ai-a-lot-of-people-have-asked-how-to-configure-this-cost-effici--2098033757504634982|Configuração de agent tree com Codex]]", "[[extracts/x/bookmarks/2026-09-18-dankrieg-introducing-ihermes-a-personal-ai-assistant-powered-by-herme--2100260309336535218|Lançamento do assistente iHermes]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-this-has-ended-up-being-better-than-expected-and-fills-an-in--2094156122441625770|AFK agent workflow vs /implement-spec]]", "[[extracts/x/bookmarks/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-kit-that-changes-two--2098361620493660493|kit para bots no Hermes Desktop]]", "[[extracts/x/bookmarks/2026-09-19-moritzkremb-6-email-classifier-https-t-co-so7gq4itsq--2100895984108913030|Classificador de e-mails com agentes]]", "[[extracts/x/bookmarks/2026-09-12-thsottiaux-hi-astra-users-a-reset-and-a-quick-update-on-quality-issues--2098612714704891959|Correções de qualidade no Astra]]"]
---

# Roteamento e memória no Hermes Agent

**@witcheer** · [2098020649662816503](https://x.com/witcheer/status/2098020649662816503) · `announcement`

## Resumo
Membro da comunidade do Hermes Agent construiu uma camada de orquestração que decide por execução qual modelo e esforço usar, quais skills de especialista carregar e o que conta como 'done', com memória curada: candidatos passam por uma review card antes de serem aceitos. Vale salvar como referência de arquitetura com roteamento por tarefa e memória com gate de revisão.

## Pontos-chave
- Roteamento por tarefa: a camada escolhe dinamicamente o modelo e o nível de esforço alocado a cada execução
- Carregamento condicional de specialist skills, controlando o que entra no contexto de cada run
- Critério explícito de conclusão ('what counts as done'), funcionando como gate de verificação
- A peça distintiva é a memória: um candidato vai para uma review card antes de ser incorporado — memória curada por revisão, não escrita passiva
- O tweet está truncado; detalhes finais do mecanismo de review não aparecem

## Entidades
Hermes Agent, witcheer

> **Revisit:** `medium` · **fonte:** `tweet`
