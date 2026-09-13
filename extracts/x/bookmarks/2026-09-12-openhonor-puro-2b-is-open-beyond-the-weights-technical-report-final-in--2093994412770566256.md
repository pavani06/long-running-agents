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
relates-to: ["[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-toolgrad-an-efficient-framework-for-generating-t--2098183830968705163|ToolGrad: geração de datasets de tool-use]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-getting-ready-to-publish-my-complete-guide-to-rl-for-llms-to--2091570446164733962|RLHF e pós-treinamento de LLMs]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-soup-fine-tune-and-post-train-llms-in-one-command-no-ssh-no--2092662174443249870|Ferramenta CLI de fine-tuning de LLMs]]", "[[extracts/x/bookmarks/2026-09-12-vaibhavsisinty-baidu-just-open-sourced-an-ocr-model-that-reads-entire-40-pa--2079000862962417996|OCR open-source da Baidu]]", "[[extracts/x/bookmarks/2026-09-12-agentnativedev-so-perplexity-wrote-its-own-inference-engine-it-is-called-li--2098111913695551626|Engine de inferência Lily da Perplexity]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-brilliant-new-paper-from-the-qwen-team-it-provides-insights--2095880318146507139|Ambientes de treino de agentes]]", "[[extracts/x/bookmarks/2026-09-12-thesupermanmx-china-open-sourced-a-peanut-sized-ocr-that-parses-entire-100--2078774556249186345|OCR local de PDFs longos]]", "[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-timesfm-3-a-state-of-the-art-time-series-foundat--2094483372718580066|TimesFM-3: forecasting multivariado]]", "[[extracts/x/bookmarks/2026-09-12-tydsh-a-novel-way-to-do-rl-in-llm-post-training-inspired-by-our-pr--2080881800877134004|Dinâmica de aprendizado do RLVR]]", "[[extracts/x/bookmarks/2026-09-12-fazle_karim1-googleresearch-i-wonder-how-it-would-do-on-this-research-of--2094501145536315670|GlucoFM: foundation model para CGM]]", "[[extracts/x/bookmarks/2026-09-12-_yusufknl-as-someone-who-s-been-shipping-llms-since-the-gpt-2-days-thi--2078877591923036378|Aula de cross-entropy em LLMs]]", "[[extracts/x/bookmarks/2026-09-12-mtslive-xiaoyin-qu-breaks-down-deepseek-s-cheap-inference-philosophy--2085525434385695137|Economia de treinamento DeepSeek]]", "[[extracts/x/bookmarks/2026-09-12-aravsrinivas-we-re-open-sourcing-lily-perplexity-s-local-inference-engine--2095264908762140823|Perplexity Lily inferência local]]", "[[extracts/x/bookmarks/2026-09-12-imadeiyamu-https-t-co-dskqwecp3z-great-collection-of-exceptional-writin--2076340132370583992|Índice Billion Dollar PDFs]]", "[[extracts/x/bookmarks/2026-09-12-sitkosebastian-you-don-t-need-a-power-meter-to-know-how-many-watts-a-rider--2089763604371218674|estimativa de watts sem medidor]]", "[[extracts/x/bookmarks/2026-09-12-dwrowland-in-2022-i-wrote-a-thread-called-how-to-prepare-for-utmb-that--2093248985435705642|preparação para o UTMB]]"]
thin: false
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
