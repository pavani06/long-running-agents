---
title: "classificação barata de papers com LLM"
type: "extract"
source: "x"
status_id: "2100426999546184123"
handle: "nutlope"
url: "https://x.com/nutlope/status/2100426999546184123"
created_at: "2026-09-17T03:29:55.000Z"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-19-nutlope-i-used-jev-to-classify-1-018-ai-research-papers-the-result-0--2100426999546184123.json]]"
tags: ["classification", "performance", "model-selection"]
topic: "classificação barata de papers com LLM"
summary: "Pipeline concreto para classificar 1.018 papers de IA: sumarização com DeepSeek V4 Flash + classificação via Jev, custando US$ 0,08 no total com latência mediana de 256ms por paper. Vale salvar como referência de classificação em escala com custo e latência mínimos."
key_points: ["Classificou 1.018 papers por ~US$ 0,08 total (fração de centavo por item), mostrando viabilidade de classificação em massa com LLMs", "Latência mediana de 256ms end-to-end por paper, adequada para pipelines de alto throughput", "Arquitetura em duas etapas: sumarizar cada paper com DeepSeek V4 Flash antes da classificação, reduzindo o input do classificador", "Classificação via prompt estruturado: título + resumo + 24 tópicos candidatos enviados ao Jev"]
entities: ["Jev", "DeepSeek V4 Flash", "@nutlope"]
content_type: "data"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: ["https://pbs.twimg.com/amplify_video_thumb/2100425141947604992/img/AITyHwcOWq1jw-3Z.jpg"]
---

# classificação barata de papers com LLM

**@nutlope** · [2100426999546184123](https://x.com/nutlope/status/2100426999546184123) · `data`

## Resumo
Pipeline concreto para classificar 1.018 papers de IA: sumarização com DeepSeek V4 Flash + classificação via Jev, custando US$ 0,08 no total com latência mediana de 256ms por paper. Vale salvar como referência de classificação em escala com custo e latência mínimos.

## Pontos-chave
- Classificou 1.018 papers por ~US$ 0,08 total (fração de centavo por item), mostrando viabilidade de classificação em massa com LLMs
- Latência mediana de 256ms end-to-end por paper, adequada para pipelines de alto throughput
- Arquitetura em duas etapas: sumarizar cada paper com DeepSeek V4 Flash antes da classificação, reduzindo o input do classificador
- Classificação via prompt estruturado: título + resumo + 24 tópicos candidatos enviados ao Jev

## Entidades
Jev, DeepSeek V4 Flash, @nutlope

> **Revisit:** `medium` · **fonte:** `tweet`
