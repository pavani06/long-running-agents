---
title: "Homelab para experimentação de IA local"
type: "extract"
source: "x"
status_id: "2099247007454142644"
handle: "andrewchen"
url: "https://x.com/andrewchen/status/2099247007454142644"
created_at: "2026-09-13T21:21:03.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-andrewchen-current-homelab-setup-for-local-ai-experimentation-hermes-bo--2099247007454142644.json]]"
tags: ["stack-tooling", "runtime", "performance", "model-selection"]
topic: "Homelab para experimentação de IA local"
summary: "Configuração concreta de homelab com hardware heterogêneo para servir LLMs localmente, separando casos de uso por trade-off entre velocidade e qualidade do modelo. Vale salvar como referência de arquitetura de inferência local com peças específicas."
key_points: ["Hermes box hospedado em Framework Desktop Mainboard AI Max+ 395 serve como máquina base do setup", "5090 como eGPU roda Qwen 3.8 27B com foco em throughput rápido (~150+ tok/s) para uso interativo de LLM", "2x DGX Spark rodam DeepSeek v4 Flash 0731, um modelo de qualidade melhor porém mais lento — separação explícita velocidade vs. qualidade", "Raspberry Pi 5 complementa o setup (função truncada no tweet)"]
entities: ["Andrew Chen", "Framework Desktop Mainboard AI Max+ 395", "NVIDIA RTX 5090", "DGX Spark", "Raspberry Pi 5", "Qwen 3.8 27B", "DeepSeek v4 Flash 0731"]
content_type: "resource"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
---

# Homelab para experimentação de IA local

**@andrewchen** · [2099247007454142644](https://x.com/andrewchen/status/2099247007454142644) · `resource`

## Resumo
Configuração concreta de homelab com hardware heterogêneo para servir LLMs localmente, separando casos de uso por trade-off entre velocidade e qualidade do modelo. Vale salvar como referência de arquitetura de inferência local com peças específicas.

## Pontos-chave
- Hermes box hospedado em Framework Desktop Mainboard AI Max+ 395 serve como máquina base do setup
- 5090 como eGPU roda Qwen 3.8 27B com foco em throughput rápido (~150+ tok/s) para uso interativo de LLM
- 2x DGX Spark rodam DeepSeek v4 Flash 0731, um modelo de qualidade melhor porém mais lento — separação explícita velocidade vs. qualidade
- Raspberry Pi 5 complementa o setup (função truncada no tweet)

## Entidades
Andrew Chen, Framework Desktop Mainboard AI Max+ 395, NVIDIA RTX 5090, DGX Spark, Raspberry Pi 5, Qwen 3.8 27B, DeepSeek v4 Flash 0731

> **Revisit:** `medium` · **fonte:** `tweet`
