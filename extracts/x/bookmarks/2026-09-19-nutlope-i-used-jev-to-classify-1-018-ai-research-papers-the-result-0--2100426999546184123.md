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
relates-to: ["[[extracts/x/bookmarks/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256|Puro-2B: receita aberta de pré-treinamento barato]]", "[[extracts/x/bookmarks/2026-09-12-argona0x-whoever-leaked-this-has-bigger-balls-than-sense-two-research--2082193490956476521|confiabilidade de LLM-as-judge]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-extraordinary-claims-require-extraordinary-evidence-so-check--2099925690682630371|Modelos estruturados para automação]]", "[[extracts/x/bookmarks/2026-09-12-xudong07452910-netflix-llm-as-a-judge-netflix-judge-judge-rart-judge--2095444189743902927|LLM-as-a-Judge em produção na Netflix]]", "[[extracts/x/bookmarks/2026-09-18-0xlogicrw-openai-diogo-almeida-typesafe-ai-jev-token-token-jev-typesaf--2100065117127815679|Jev: modelo classificador da TypeSafe AI]]", "[[extracts/x/bookmarks/2026-09-12-keepgoings0-oalanicolas-from-my-experience-for-the-orchestrator-astra-xh--2097766199450829151|seleção de modelos por papel de agente]]", "[[extracts/x/bookmarks/2026-09-12-askalphaxiv-introducing-deepseek-v4-1-flash-for-understanding-research-p--2098309348858704095|alphaXiv AI paper Q&A]]", "[[extracts/x/bookmarks/2026-09-19-eriksreinfelds-omg-togethercompute-i-love-you-this-is-time-to-first-token-f--2100218519636037929|Benchmark TTFT DeepSeek v4.1 Flash]]", "[[extracts/x/bookmarks/2026-09-18-nielsrogge-12-million-views-for-a-json-classifier-yeah-we-re-in-a-bubbl--2100114968460820986|Bolha de hype em IA]]", "[[extracts/x/bookmarks/2026-09-12-mtslive-xiaoyin-qu-breaks-down-deepseek-s-cheap-inference-philosophy--2085525434385695137|Economia de treinamento DeepSeek]]", "[[extracts/x/bookmarks/2026-09-12-thesupermanmx-china-open-sourced-a-peanut-sized-ocr-that-parses-entire-100--2078774556249186345|OCR local de PDFs longos]]"]
theme: "Treinamento de modelos e atletas"
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
