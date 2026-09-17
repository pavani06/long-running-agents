---
title: "Executor: gateway MCP para agentes"
type: "extract"
source: "x"
status_id: "2099995262802641129"
handle: "nateberkopec"
url: "https://x.com/nateberkopec/status/2099995262802641129"
created_at: "2026-09-15T22:54:21.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-17-nateberkopec-for-the-last-3-months-i-ve-been-telling-all-my-clients-to-mo--2099995262802641129.json]]"
tags: ["agent-tooling", "agents", "permissions", "token-budgeting", "arquitetura"]
topic: "Executor: gateway MCP para agentes"
summary: "Executor é um gateway MCP ('MCP of MCPs') que conecta todas as integrações uma única vez e expõe ao agente uma só ferramenta, com políticas de segurança derivadas da fonte e segredos que nunca chegam ao modelo. Nate Berkopec diz que recomenda a abordagem a clientes há 3 meses, citando adoção similar em empresas como Ramp."
key_points: ["Conecte cada integração uma vez (MCP, OpenAPI e GraphQL viram a mesma forma: nome, input, output) e todos os agentes — Claude Code, Cursor, Codex — recebem as mesmas ferramentas, eliminando OAuth e API keys duplicados em cinco lugares.", "O modelo vê apenas uma ferramenta: o Executor faz lookup em tempo de execução, então dá para conectar 50 serviços mantendo o prompt do mesmo tamanho.", "Segurança derivada da fonte: GET vs DELETE no OpenAPI, destructiveHint no MCP, mutations no GraphQL — chamadas seguras rodam sozinhas, destrutivas pedem confirmação, e qualquer ferramenta pode ser sobrescrita.", "Segredos nunca chegam ao modelo: chamadas rodam em sandbox JavaScript isolado com credenciais anexadas host-side no momento da chamada; workspace compartilha conexões com políticas centrais e bloqueio de ferramentas em um clique.", "Open source e self-hostável (credenciais em WorkOS Vault no cloud ou 1Password local); gratuito até 3 pessoas e 100k execuções/mês, Team a $15/membro/mês; backed by Y Combinator, fundador Rhys Sullivan."]
entities: ["Executor", "Nate Berkopec", "Rhys Sullivan", "Y Combinator", "Ramp", "jsharkey", "WorkOS Vault", "1Password", "MCP"]
content_type: "tool"
revisit: "medium"
grounded_in: "article"
thin: false
links: ["https://executor.sh"]
media: []
---

# Executor: gateway MCP para agentes

**@nateberkopec** · [2099995262802641129](https://x.com/nateberkopec/status/2099995262802641129) · `tool`

## Resumo
Executor é um gateway MCP ('MCP of MCPs') que conecta todas as integrações uma única vez e expõe ao agente uma só ferramenta, com políticas de segurança derivadas da fonte e segredos que nunca chegam ao modelo. Nate Berkopec diz que recomenda a abordagem a clientes há 3 meses, citando adoção similar em empresas como Ramp.

## Pontos-chave
- Conecte cada integração uma vez (MCP, OpenAPI e GraphQL viram a mesma forma: nome, input, output) e todos os agentes — Claude Code, Cursor, Codex — recebem as mesmas ferramentas, eliminando OAuth e API keys duplicados em cinco lugares.
- O modelo vê apenas uma ferramenta: o Executor faz lookup em tempo de execução, então dá para conectar 50 serviços mantendo o prompt do mesmo tamanho.
- Segurança derivada da fonte: GET vs DELETE no OpenAPI, destructiveHint no MCP, mutations no GraphQL — chamadas seguras rodam sozinhas, destrutivas pedem confirmação, e qualquer ferramenta pode ser sobrescrita.
- Segredos nunca chegam ao modelo: chamadas rodam em sandbox JavaScript isolado com credenciais anexadas host-side no momento da chamada; workspace compartilha conexões com políticas centrais e bloqueio de ferramentas em um clique.
- Open source e self-hostável (credenciais em WorkOS Vault no cloud ou 1Password local); gratuito até 3 pessoas e 100k execuções/mês, Team a $15/membro/mês; backed by Y Combinator, fundador Rhys Sullivan.

## Links
- https://executor.sh

## Entidades
Executor, Nate Berkopec, Rhys Sullivan, Y Combinator, Ramp, jsharkey, WorkOS Vault, 1Password, MCP

> **Revisit:** `medium` · **fonte:** `article`
