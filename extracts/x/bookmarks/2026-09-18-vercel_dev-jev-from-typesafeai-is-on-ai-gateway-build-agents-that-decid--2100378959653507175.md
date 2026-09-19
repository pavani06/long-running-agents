---
title: "Jev: decisões tipadas para agentes"
type: "extract"
source: "x"
status_id: "2100378959653507175"
handle: "vercel_dev"
url: "https://x.com/vercel_dev/status/2100378959653507175"
created_at: "2026-09-17T00:19:01.000Z"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-18-vercel_dev-jev-from-typesafeai-is-on-ai-gateway-build-agents-that-decid--2100378959653507175.json]]"
tags: ["agents", "agent-loop", "model-selection", "evals", "verification", "escalation", "performance"]
topic: "Jev: decisões tipadas para agentes"
summary: "Jev (TypeSafe AI) chega ao Vercel AI Gateway via AI SDK 7: um modelo probabilístico de decisão que recebe state e retorna Choice, Score e Boolean tipados com probabilidades, avaliando todas as perguntas em paralelo em vez de gerar texto. TypeSafe relata até 193.6x mais rapidez e 444.6x menor custo que LLMs em avaliações de workflow."
key_points: ["Jev avalia todas as perguntas declaradas em paralelo e devolve respostas tipadas (Choice, Score, Boolean) com probabilidades, eliminando geração de texto, parsing e validação", "Casos de uso centrais para agent loops: escolher próxima ferramenta/subagente, decidir continuar/retry/perguntar ao usuário/parar, pontuar urgência ou risco antes de ações, e verificar saídas para impor guardrails", "Integração via experimental_evaluate no AI SDK 7 (>=7.0.105) com model 'typesafe-ai/jev', state compartilhado e mapa de questions nomeadas; IDs de perguntas e keys de Choice são preservados na resposta", "Confidence separada para Choice e Score em result.providerMetadata.typesafe.confidence, calibrável contra exemplos rotulados do próprio workflow", "Suporta Zero Data Retention e No Training por requisição; chamadas aparecem em logs/relatórios, contam para budgets e aceitam outros providerOptions.gateway"]
entities: ["Vercel AI Gateway", "TypeSafe AI", "Jev", "AI SDK 7"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway"]
media: []
---

# Jev: decisões tipadas para agentes

**@vercel_dev** · [2100378959653507175](https://x.com/vercel_dev/status/2100378959653507175) · `announcement`

## Resumo
Jev (TypeSafe AI) chega ao Vercel AI Gateway via AI SDK 7: um modelo probabilístico de decisão que recebe state e retorna Choice, Score e Boolean tipados com probabilidades, avaliando todas as perguntas em paralelo em vez de gerar texto. TypeSafe relata até 193.6x mais rapidez e 444.6x menor custo que LLMs em avaliações de workflow.

## Pontos-chave
- Jev avalia todas as perguntas declaradas em paralelo e devolve respostas tipadas (Choice, Score, Boolean) com probabilidades, eliminando geração de texto, parsing e validação
- Casos de uso centrais para agent loops: escolher próxima ferramenta/subagente, decidir continuar/retry/perguntar ao usuário/parar, pontuar urgência ou risco antes de ações, e verificar saídas para impor guardrails
- Integração via experimental_evaluate no AI SDK 7 (>=7.0.105) com model 'typesafe-ai/jev', state compartilhado e mapa de questions nomeadas; IDs de perguntas e keys de Choice são preservados na resposta
- Confidence separada para Choice e Score em result.providerMetadata.typesafe.confidence, calibrável contra exemplos rotulados do próprio workflow
- Suporta Zero Data Retention e No Training por requisição; chamadas aparecem em logs/relatórios, contam para budgets e aceitam outros providerOptions.gateway

## Links
- https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway

## Entidades
Vercel AI Gateway, TypeSafe AI, Jev, AI SDK 7

> **Revisit:** `high` · **fonte:** `article`
