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
