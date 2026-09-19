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
theme: "Confiabilidade e avaliação de agentes"
relates-to: ["[[extracts/x/bookmarks/2026-09-15-suraj_sharma14-as-an-ai-infrastructure-engineer-you-must-build-these-projec--2099113368942465438|Projetos de infraestrutura de inferência]]", "[[extracts/x/bookmarks/2026-09-14-andrewchen-vitostrokov-agreed-but-i-think-theres-two-issues-you-really--2099279190491353442|Apple M5 Ultra vs Nvidia para IA]]", "[[extracts/x/bookmarks/2026-09-12-kay2289123-ai-infra-ai-kv--2098270561151676829|Reading list de AI Infra]]", "[[extracts/x/bookmarks/2026-09-12-agentnativedev-so-perplexity-wrote-its-own-inference-engine-it-is-called-li--2098111913695551626|Engine de inferência Lily da Perplexity]]", "[[extracts/x/bookmarks/2026-09-18-alexfinn-in-case-local-ai-models-are-banned-it-s-critical-you-start-e--2100369670952137067|modelos locais de IA]]", "[[extracts/x/bookmarks/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256|Puro-2B: receita aberta de pré-treinamento barato]]", "[[extracts/x/bookmarks/2026-09-15-chadwahl-what-operating-a-sovereign-ai-stack-looks-like-nvidia-palant--2099510309991948550|Sovereign AI stack NVIDIA + Palantir]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-we-love-how-this-doomo-doomonstrates-real-time-intelligence--2099925687465570372|Demo de Doom em tempo real com IA]]", "[[extracts/x/bookmarks/2026-09-12-aravsrinivas-we-re-open-sourcing-lily-perplexity-s-local-inference-engine--2095264908762140823|Perplexity Lily inferência local]]"]
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
