---
title: "Puro-2B: receita aberta de pré-treinamento barato"
type: "extract"
source: "x"
status_id: "2093994412770566256"
handle: "openhonor"
url: "https://x.com/openhonor/status/2093994412770566256"
created_at: "2026-08-30T09:29:07.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256.json]]"
tags: ["analise", "performance", "curriculo-conteudo", "data-platform", "stack-tooling"]
topic: "Puro-2B: receita aberta de pré-treinamento barato"
summary: "Paper técnico que apresenta uma receita completa de pré-treinamento open-source: modelos de 2B parâmetros treinados do zero em até 1.4 trilhões de tokens com FP8 em GPUs de consumo RTX 5090, custando menos de $6.9K e aproximando a performance do Qwen2.5-1.5B. Vale salvar por derivar uma lei de escala de custo (~$4.4K para igualar Qwen2-1.5B) e liberar pipeline completo (dados, código, checkpoints, pesos) sob Apache 2.0."
key_points: ["Pré-treinamento de LLM de 2B parâmetros do zero em até 1.4T tokens com FP8 em GPUs de consumo (RTX 5090), com melhor modelo custando menos de $6.9K e aproximando Qwen2.5-1.5B — contra >$1.5M do Llama-3.2-3B e >$700K para reproduzir SmolLM3-3B", "Eficiência de custo vem da combinação de: seleção de hardware, treino em baixa precisão (FP8), otimização hyperball, curriculum model averaging e a receita de dados", "Puro Cost Scaling Law: lei ajustada relacionando custo de treino a performance média, prevendo que ~$4.4K bastam para alcançar a performance do Qwen2-1.5B", "Estudo controlado end-to-end de como currículos de dados de pré-treinamento moldam a performance downstream após o post-training — possível apenas por ter acesso ao pipeline completo, não só aos pesos", "Release completo sob Apache 2.0: relatório técnico, checkpoints finais e intermediários, código de treino + configs, framework de processamento de dados e datasets com manifests"]
entities: ["Puro-2B", "Qwen2-1.5B", "Qwen2.5-1.5B", "Llama-3.2-3B", "SmolLM3-3B", "RTX 5090", "Shengqi Chen", "Apache 2.0", "Hugging Face", "arXiv"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://arxiv.org/abs/2608.27370", "https://github.com/thu-pacman/Puro-Megatron", "https://huggingface.co/collections/thu-pacman/puro-2b"]
media: []
---

# Puro-2B: receita aberta de pré-treinamento barato

**@openhonor** · [2093994412770566256](https://x.com/openhonor/status/2093994412770566256) · `resource`

## Resumo
Paper técnico que apresenta uma receita completa de pré-treinamento open-source: modelos de 2B parâmetros treinados do zero em até 1.4 trilhões de tokens com FP8 em GPUs de consumo RTX 5090, custando menos de $6.9K e aproximando a performance do Qwen2.5-1.5B. Vale salvar por derivar uma lei de escala de custo (~$4.4K para igualar Qwen2-1.5B) e liberar pipeline completo (dados, código, checkpoints, pesos) sob Apache 2.0.

## Pontos-chave
- Pré-treinamento de LLM de 2B parâmetros do zero em até 1.4T tokens com FP8 em GPUs de consumo (RTX 5090), com melhor modelo custando menos de $6.9K e aproximando Qwen2.5-1.5B — contra >$1.5M do Llama-3.2-3B e >$700K para reproduzir SmolLM3-3B
- Eficiência de custo vem da combinação de: seleção de hardware, treino em baixa precisão (FP8), otimização hyperball, curriculum model averaging e a receita de dados
- Puro Cost Scaling Law: lei ajustada relacionando custo de treino a performance média, prevendo que ~$4.4K bastam para alcançar a performance do Qwen2-1.5B
- Estudo controlado end-to-end de como currículos de dados de pré-treinamento moldam a performance downstream após o post-training — possível apenas por ter acesso ao pipeline completo, não só aos pesos
- Release completo sob Apache 2.0: relatório técnico, checkpoints finais e intermediários, código de treino + configs, framework de processamento de dados e datasets com manifests

## Links
- https://arxiv.org/abs/2608.27370
- https://github.com/thu-pacman/Puro-Megatron
- https://huggingface.co/collections/thu-pacman/puro-2b

## Entidades
Puro-2B, Qwen2-1.5B, Qwen2.5-1.5B, Llama-3.2-3B, SmolLM3-3B, RTX 5090, Shengqi Chen, Apache 2.0, Hugging Face, arXiv

> **Revisit:** `high` · **fonte:** `article`
