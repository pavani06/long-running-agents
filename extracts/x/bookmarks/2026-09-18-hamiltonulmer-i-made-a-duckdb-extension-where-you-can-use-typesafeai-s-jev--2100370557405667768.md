---
title: "Extensão DuckDB para classificação com Jev"
type: "extract"
source: "x"
status_id: "2100370557405667768"
handle: "hamiltonulmer"
url: "https://x.com/hamiltonulmer/status/2100370557405667768"
created_at: "2026-09-16T23:45:38.000Z"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-18-hamiltonulmer-i-made-a-duckdb-extension-where-you-can-use-typesafeai-s-jev--2100370557405667768.json]]"
tags: ["classification", "stack-tooling", "data-platform", "analise"]
topic: "Extensão DuckDB para classificação com Jev"
summary: "Hamilton Ulmer criou uma extensão do DuckDB que usa o Jev (Typesafe AI) para classificar linhas diretamente em arquivos csv/parquet ou tabelas DuckDB. Vale salvar como alternativa rápida e ergonômica a LLMs e classificadores tradicionais em fluxos de análise de dados."
key_points: ["A extensão integra o Jev ao DuckDB, permitindo classificação de linhas diretamente em qualquer arquivo csv/parquet ou tabela DuckDB", "Performance de ~10 segundos para 1.000 linhas, sendo mais rápido que usar um LLM para a mesma tarefa", "Mais ergonômico que treinar/usar um classificador tradicional, eliminando o overhead de pipelines de ML", "Caso de uso principal: classificação dentro do próprio fluxo de análise de dados, sem sair do ambiente SQL"]
entities: ["DuckDB", "Jev", "Typesafe AI", "Hamilton Ulmer"]
content_type: "tool"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: ["https://pbs.twimg.com/media/HSYD5B1bsAAWqeg.jpg"]
relates-to: ["[[extracts/x/bookmarks/2026-09-18-0xlogicrw-openai-diogo-almeida-typesafe-ai-jev-token-token-jev-typesaf--2100065117127815679|Jev: modelo classificador da TypeSafe AI]]", "[[extracts/x/bookmarks/2026-09-18-hot_town-jev-is-here-how-is-different-from-an-llm-how-does-it-work-un--2100570516612382787|Jev: o que é e quando usar]]", "[[extracts/x/bookmarks/2026-09-18-nielsrogge-for-anyone-curious-how-jev-works-i-made-a-visual-explanation--2100239244501430438|Jev: decodificação não-autorregressiva em LLMs]]", "[[extracts/x/bookmarks/2026-09-18-manthanguptaa-jev-is-one-of-the-more-interesting-model-launches-i-have-see--2100466984605417923|Lançamento do modelo Jev]]", "[[extracts/x/bookmarks/2026-09-18-josharosen-george-sequeira-typesafeai-its-jev-the-super-fast-new-decisi--2100670955831824554|Modelo de decisão Jev avaliando outputs]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-extraordinary-claims-require-extraordinary-evidence-so-check--2099925690682630371|Modelos estruturados para automação]]"]
theme: "Confiabilidade e avaliação de agentes"
---

# Extensão DuckDB para classificação com Jev

**@hamiltonulmer** · [2100370557405667768](https://x.com/hamiltonulmer/status/2100370557405667768) · `tool`

## Resumo
Hamilton Ulmer criou uma extensão do DuckDB que usa o Jev (Typesafe AI) para classificar linhas diretamente em arquivos csv/parquet ou tabelas DuckDB. Vale salvar como alternativa rápida e ergonômica a LLMs e classificadores tradicionais em fluxos de análise de dados.

## Pontos-chave
- A extensão integra o Jev ao DuckDB, permitindo classificação de linhas diretamente em qualquer arquivo csv/parquet ou tabela DuckDB
- Performance de ~10 segundos para 1.000 linhas, sendo mais rápido que usar um LLM para a mesma tarefa
- Mais ergonômico que treinar/usar um classificador tradicional, eliminando o overhead de pipelines de ML
- Caso de uso principal: classificação dentro do próprio fluxo de análise de dados, sem sair do ambiente SQL

## Entidades
DuckDB, Jev, Typesafe AI, Hamilton Ulmer

> **Revisit:** `medium` · **fonte:** `tweet`
