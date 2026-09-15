---
title: "Harnesses customizados para agentes"
type: "extract"
source: "x"
status_id: "2098866608785473858"
handle: "hwchase17"
url: "https://x.com/hwchase17/status/2098866608785473858"
created_at: "2026-09-12T20:09:29.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-hwchase17-in-case-you-want-to-build-a-domain-specific-harness-https-t--2098866608785473858.json]]"
tags: ["harness", "harness-engineering", "agent-loop", "agents", "context-engineering", "agent-tooling", "frameworks", "arquitetura", "context-management"]
topic: "Harnesses customizados para agentes"
summary: "Artigo do LangChain defende que agent = model + harness e que a utilidade de um agente depende do fit entre o harness e a tarefa; create_agent é o primitivo minimalista para construir harnesses sob medida, customizados via middleware. Vale salvar como referência de engenharia de harness/harness fit."
key_points: ["Agente = modelo + harness: o harness é o scaffolding que conecta o modelo ao mundo real e cujo trabalho é entregar o contexto certo ao modelo a cada passo do loop", "create_agent é propositalmente minimalista (implementa só o agent loop), em contraste com harnesses pré-montados e opinativos como Deep Agents e Claude Agent SDK, que não suportam fine-grained customization (prompting próprio, business logic, guardrails)", "Middleware engancha no loop em pontos específicos (antes/depois de chamadas de modelo e tools, startup/teardown) e oferece 4 alavancas: lógica determinística, ciclo de vida completo de tools, estado customizado persistente entre hooks, e stream handlers para filtrar/rotear eventos", "Middleware é composável e reutilizável: cada peça isolada pode ser compartilhada pela organização, fazendo novos agentes herdarem comportamento testado em batalha sem reconstrução", "Task-harness fit é o conceito-chave: todos os agentes internos do LangChain (GTM agent, coding agent assíncrono, no-code agent builder) são construídos sobre create_agent com stack de middleware ajustada à missão de cada agente"]
entities: ["LangChain", "Harrison Chase", "Sydney Runkle", "create_agent", "Deep Agents", "Claude Agent SDK", "Pi", "Anthropic"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://www.langchain.com/blog/how-to-build-a-custom-agent-harness"]
media: ["https://pbs.twimg.com/media/HSCsDIpXQAEQ0wV.jpg"]
---

# Harnesses customizados para agentes

**@hwchase17** · [2098866608785473858](https://x.com/hwchase17/status/2098866608785473858) · `resource`

## Resumo
Artigo do LangChain defende que agent = model + harness e que a utilidade de um agente depende do fit entre o harness e a tarefa; create_agent é o primitivo minimalista para construir harnesses sob medida, customizados via middleware. Vale salvar como referência de engenharia de harness/harness fit.

## Pontos-chave
- Agente = modelo + harness: o harness é o scaffolding que conecta o modelo ao mundo real e cujo trabalho é entregar o contexto certo ao modelo a cada passo do loop
- create_agent é propositalmente minimalista (implementa só o agent loop), em contraste com harnesses pré-montados e opinativos como Deep Agents e Claude Agent SDK, que não suportam fine-grained customization (prompting próprio, business logic, guardrails)
- Middleware engancha no loop em pontos específicos (antes/depois de chamadas de modelo e tools, startup/teardown) e oferece 4 alavancas: lógica determinística, ciclo de vida completo de tools, estado customizado persistente entre hooks, e stream handlers para filtrar/rotear eventos
- Middleware é composável e reutilizável: cada peça isolada pode ser compartilhada pela organização, fazendo novos agentes herdarem comportamento testado em batalha sem reconstrução
- Task-harness fit é o conceito-chave: todos os agentes internos do LangChain (GTM agent, coding agent assíncrono, no-code agent builder) são construídos sobre create_agent com stack de middleware ajustada à missão de cada agente

## Links
- https://www.langchain.com/blog/how-to-build-a-custom-agent-harness

## Entidades
LangChain, Harrison Chase, Sydney Runkle, create_agent, Deep Agents, Claude Agent SDK, Pi, Anthropic

> **Revisit:** `high` · **fonte:** `article`
