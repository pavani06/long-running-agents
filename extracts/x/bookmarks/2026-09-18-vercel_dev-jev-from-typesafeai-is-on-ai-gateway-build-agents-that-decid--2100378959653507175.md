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
relates-to: ["[[extracts/x/bookmarks/2026-09-18-0xlogicrw-openai-diogo-almeida-typesafe-ai-jev-token-token-jev-typesaf--2100065117127815679|Jev: modelo classificador da TypeSafe AI]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-extraordinary-claims-require-extraordinary-evidence-so-check--2099925690682630371|Modelos estruturados para automação]]", "[[extracts/x/bookmarks/2026-09-18-josharosen-george-sequeira-typesafeai-its-jev-the-super-fast-new-decisi--2100670955831824554|Modelo de decisão Jev avaliando outputs]]", "[[extracts/x/bookmarks/2026-09-19-ctatedev-every-agent-harness-can-now-use-jev-npm-install-g-ai-cli-ask--2100584917092409479|Jev CLI para agent harnesses]]", "[[extracts/x/bookmarks/2026-09-18-agtpinsights-typesafe-ai-just-launched-jev-today-here-s-what-you-need-to--2099946094570733605|Lançamento do modelo Jev pela TypeSafe AI]]", "[[extracts/x/bookmarks/2026-09-18-manthanguptaa-jev-is-one-of-the-more-interesting-model-launches-i-have-see--2100466984605417923|Lançamento do modelo Jev]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-we-believe-that-the-future-is-code-ai-so-made-workflow-evals--2099925685720760404|Anúncio do modelo Jev]]", "[[extracts/x/bookmarks/2026-09-18-hamiltonulmer-i-made-a-duckdb-extension-where-you-can-use-typesafeai-s-jev--2100370557405667768|Extensão DuckDB para classificação com Jev]]", "[[extracts/x/bookmarks/2026-09-18-0xlogicrw-jev-waitlist-api-awesome-jev-jev-1-jev-ultrafast-browser-use--2100478725393686556|Curadoria de projetos para API Jev]]"]
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
