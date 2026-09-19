---
title: "Stop Chunking Like It's 2022 — Yuval Belfer, AI21 Labs"
type: "extract"
source: "youtube"
video_id: "r9OwPx_HoV0"
url: "https://www.youtube.com/watch?v=r9OwPx_HoV0"
channel: "AI Engineer"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-18-stop-chunking-like-it-s-2022-yuval-belfer-ai21-labs--r9OwPx_HoV0.txt]]"
tags: ["context-engineering", "context-management", "index", "evals", "knowledge-management", "analise", "arquitetura", "data-platform", "token-budgeting"]
thesis: "Chunking não morreu com a busca agentic: o tamanho ótimo de chunk é dependente da query, e indexar o mesmo corpus em múltiplas escalas combinadas via Reciprocal Rank Fusion recupera 20-40% de recall perdido por chunking de tamanho fixo."
concepts: ["RAG (retrieval-augmented generation)", "chunking de tamanho fixo como compressão com perdas", "busca agentic (grep/ls/find) versus retrieval indexado", "chunking como problema de dependência da query", "experimento oracle (recall@k por melhor chunk size por query)", "multiscale indexing (duplicação do corpus em múltiplos tamanhos de chunk)", "recuperação de documentos inteiros em vez de chunks para tornar rankings comparáveis", "agregação de rankings como votação", "Reciprocal Rank Fusion (RRF)", "contextual retrieval (Anthropic) como trabalho relacionado", "trade-off custo de memória (2-5x) vs latência paralela", "datasets de avaliação: QMSum, NarrativeQA, Seinfeld, FinanceBench, MTEB"]
tools: ["AI21", "LlamaIndex", "Model Context Protocol (MCP)", "vector DB", "grep", "ls", "find"]
people: ["Yuval", "AI21", "Jerry (CEO da LlamaIndex)", "Anthropic"]
claims: ["Retrieval tuning (ajustar top-k, hybrid search por query) é o que a busca agentic realmente matou, não o chunking nem a indexação", "Não existe um tamanho de chunk universalmente correto: queries focadas se beneficiam de chunks pequenos e queries difusas/temáticas exigem chunks grandes", "O experimento oracle mostra gap de 20-40% de recall entre escolher o melhor chunk size por query versus qualquer tamanho fixo", "Implementação prática: duplique o corpus em N tamanhos de chunk (ex.: 50/100/200/...), consulte todos em paralelo por query e fusione com RRF", "Para fundir rankings de escalas diferentes, recupere o documento inteiro (não o chunk), tornando os N rankings comparáveis como votação sobre documentos", "RRF é um script simples sem modelo treinado, com latência negligível; o custo real é 2-5x de memória para guardar as cópias do índice", "O método iguala ou supera o melhor chunk fixo em QMSum, NarrativeQA, Seinfeld e FinanceBench, com ganhos de 10-40% no MTEB", "Trabalho futuro aberto: como determinar quantos e quais tamanhos de chunk usar (os valores testados foram arbitrários) e explorar métodos de fusão melhores que RRF"]
deep_dive: "medium"
deep_dive_reason: "Oferece um método concreto e quantificado (multiscale indexing + RRF com ganhos de 20-40% em recall e custos claros), mas é um talk de escopo estreito sobre uma única técnica de indexação, sem densidade arquitetural em harness, governança ou fleets."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-building-production-ready-rag-applications-jerry-liu--TRjq7t2Ms5I|Building Production-Ready RAG Applications: Jerry Liu]]", "[[extracts/youtube/ai-learning/2026-09-11-rag-vs-cag-solving-knowledge-gaps-in-ai-models--HdafI0t3sEY|RAG vs. CAG: Solving Knowledge Gaps in AI Models]]", "[[extracts/youtube/ai-learning/2026-09-11-rag-is-exploding-58-new-rag-methods-in-48-hours--cHVQj7w9TD4|RAG is Exploding: 58 NEW RAG Methods in 48 hours]]", "[[extracts/youtube/ai-learning/2026-09-11-i-want-llama3-to-perform-10x-with-my-private-knowledge-local-agentic-rag-w-llama--u5Vcrwpzoz8|\"I want Llama3 to perform 10x with my private knowledge\" - Local Agentic RAG w/ llama3]]", "[[extracts/youtube/ai-learning/2026-09-11-benchmarking-semantic-code-retrieval-on-claude-code-kuba-rogut-turbopuffer--zKk7sDMGDEQ|Benchmarking semantic code retrieval on Claude Code — Kuba Rogut, Turbopuffer]]", "[[extracts/youtube/ai-learning/2026-09-11-turn-10-994-notes-into-memory-paul-iusztin-decoding-ai-louis-francois-bouchard-t--ZRM_TfEZcIo|Turn 10,994 Notes Into Memory - Paul Iusztin, Decoding AI & Louis-François Bouchard, Towards AI]]"]
theme: "Deep Agents e Engenharia de Contexto"
---

# Stop Chunking Like It's 2022 — Yuval Belfer, AI21 Labs

## Tese
Chunking não morreu com a busca agentic: o tamanho ótimo de chunk é dependente da query, e indexar o mesmo corpus em múltiplas escalas combinadas via Reciprocal Rank Fusion recupera 20-40% de recall perdido por chunking de tamanho fixo.

## Conceitos-chave
- RAG (retrieval-augmented generation)
- chunking de tamanho fixo como compressão com perdas
- busca agentic (grep/ls/find) versus retrieval indexado
- chunking como problema de dependência da query
- experimento oracle (recall@k por melhor chunk size por query)
- multiscale indexing (duplicação do corpus em múltiplos tamanhos de chunk)
- recuperação de documentos inteiros em vez de chunks para tornar rankings comparáveis
- agregação de rankings como votação
- Reciprocal Rank Fusion (RRF)
- contextual retrieval (Anthropic) como trabalho relacionado
- trade-off custo de memória (2-5x) vs latência paralela
- datasets de avaliação: QMSum, NarrativeQA, Seinfeld, FinanceBench, MTEB

## Ferramentas & pessoas
**Ferramentas:** AI21, LlamaIndex, Model Context Protocol (MCP), vector DB, grep, ls, find

**Pessoas/orgs:** Yuval, AI21, Jerry (CEO da LlamaIndex), Anthropic

## Claims acionáveis
- Retrieval tuning (ajustar top-k, hybrid search por query) é o que a busca agentic realmente matou, não o chunking nem a indexação
- Não existe um tamanho de chunk universalmente correto: queries focadas se beneficiam de chunks pequenos e queries difusas/temáticas exigem chunks grandes
- O experimento oracle mostra gap de 20-40% de recall entre escolher o melhor chunk size por query versus qualquer tamanho fixo
- Implementação prática: duplique o corpus em N tamanhos de chunk (ex.: 50/100/200/...), consulte todos em paralelo por query e fusione com RRF
- Para fundir rankings de escalas diferentes, recupere o documento inteiro (não o chunk), tornando os N rankings comparáveis como votação sobre documentos
- RRF é um script simples sem modelo treinado, com latência negligível; o custo real é 2-5x de memória para guardar as cópias do índice
- O método iguala ou supera o melhor chunk fixo em QMSum, NarrativeQA, Seinfeld e FinanceBench, com ganhos de 10-40% no MTEB
- Trabalho futuro aberto: como determinar quantos e quais tamanhos de chunk usar (os valores testados foram arbitrários) e explorar métodos de fusão melhores que RRF

> **Deep dive:** `medium` — Oferece um método concreto e quantificado (multiscale indexing + RRF com ganhos de 20-40% em recall e custos claros), mas é um talk de escopo estreito sobre uma única técnica de indexação, sem densidade arquitetural em harness, governança ou fleets.
