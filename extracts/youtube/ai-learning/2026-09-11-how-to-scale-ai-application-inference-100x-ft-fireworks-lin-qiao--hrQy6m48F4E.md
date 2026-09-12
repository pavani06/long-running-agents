---
title: "How to Scale AI Application Inference 100x ft. Fireworks’ Lin Qiao"
type: "extract"
source: "youtube"
video_id: "hrQy6m48F4E"
url: "https://www.youtube.com/watch?v=hrQy6m48F4E"
channel: "Sequoia Capital"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-scale-ai-application-inference-100x-ft-fireworks-lin-qiao--hrQy6m48F4E.txt]]"
tags: ["arquitetura", "runtime", "production", "stack-tooling", "model-selection", "data-platform"]
thesis: "O futuro da inferência é a co-otimização de pós-treinamento e inferência personalizada por aplicação, tratando qualidade, velocidade e concorrência (custo) como uma lei de escala tridimensional capaz de reduzir o custo de inferência em 10-100x."
concepts: ["Alinhamento em múltiplas camadas: comportamento do usuário ↔ design do produto ↔ inferência", "Lei de escala futura em 3 dimensões: qualidade, velocidade e concorrência/custo", "Alinhamento da distribuição de dados da carga da aplicação com a distribuição dos dados de treinamento do modelo", "Co-otimização de pós-treinamento e inferência (fora do espaço da aplicação)", "Explosão combinatória da otimização de inferência (mais de 100.000 combinações)", "Predição multi-token (10 tokens por vez em vez de um por vez)", "Alinhamento de numérica/precisão à distribuição de dados da aplicação", "Seleção de hardware por SKU conforme vantagens específicas para a carga", "Sharding de modelo e inferência distribuída cross-host", "Seleção de kernel otimizada por distribuição da aplicação", "Reinforcement tuning orientado por dados de produção", "Data flywheel como diferencial competitivo de produtos de IA", "Metáfora do iceberg: a alta 'linha d'água' do custo de inferência esconde aplicações viáveis", "Infraestrutura de nuvem virtual abstraindo gestão de GPUs multi-fornecedor"]
tools: ["Fireworks AI (plataforma de inferência)", "Bibliotecas de modelos abertos", "Plataforma self-serve para desenvolvedores da Fireworks"]
people: ["Lin Qiao (Lynn Chow)", "Fireworks AI"]
claims: ["Otimizar inferência de forma isolada é insuficiente; a próxima fronteira de inovação é combinar pós-treinamento e inferência em co-otimização específica por aplicação", "O espaço de configuração (numérica, seleção de hardware, sharding, kernels, mecanismos de tuning de qualidade) excede 100.000 combinações possíveis", "Reduzir o custo de inferência em 10-100x ampliaria drasticamente o conjunto de aplicações com product-market fit que podem virar negócios sustentáveis", "Uma cadeia de fast food escalou um recurso de IA de 1 loja para 1.000 lojas em 3 meses usando a plataforma", "Uma empresa de software escalou seu recurso de IA de 100 mil para 25 milhões de desenvolvedores em 3 meses", "Modelos off-the-shelf dirigidos apenas por prompt engineering representam a fase frágil e imatura do alinhamento produto-modelo; infundir conhecimento do produto via dados de produção é a fronteira", "Pesquisadores precisam assumir usos do modelo que raramente coincidem com cargas reais, criando um gap permanente entre treinamento e aplicação que exige tuning com dados de produção"]
deep_dive: "low"
deep_dive_reason: "Keynote promocional de fornecedor: apresenta uma tese arquitetural interessante (escala tridimensional e co-otimização) mas sem detalhes técnicos, benchmarks ou métodos acionáveis, com estudos de caso de marketing."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-building-the-real-world-infrastructure-for-ai-with-google-cisco-a16z--OsLRf6r5U9E|Building the Real-World Infrastructure for AI, with Google, Cisco & a16z]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-anjney-midha-from-amp-pbc-on-frontier-systems--O5PfU_uDhS0|Stanford CS153 Frontier Systems | Anjney Midha from AMP PBC on Frontier Systems]]", "[[extracts/youtube/ai-learning/2026-09-11-jeff-dean-the-1-rule-for-building-in-ai--CxXgV54KzpQ|Jeff Dean: The 1% Rule for Building in AI]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-scale-agi-and-the-future-of-everything--F_7M4Hc-usM|Stanford CS153 Frontier Systems | Scale, AGI, and the Future of Everything]]", "[[extracts/youtube/ai-learning/2026-09-11-gpus-tpus-the-economics-of-ai-explained-gavin-baker-interview--cmUo4841KQw|GPUs, TPUs, & The Economics of AI Explained | Gavin Baker Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-scaling-agents-for-gen-ai-products-anju-kambadur-bloomberg-head-of-ai-engineerin--b2GqTDWtg6s|Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-10-inference--EfM546A79aM|Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 10: Inference]]", "[[extracts/youtube/ai-learning/2026-09-11-fine-tune-the-biggest-open-source-models-even-with-a-bad-pc--kxstlfc8Lw4|Fine-Tune the biggest open-source models (even with a bad PC)]]"]
---

# How to Scale AI Application Inference 100x ft. Fireworks’ Lin Qiao

## Tese
O futuro da inferência é a co-otimização de pós-treinamento e inferência personalizada por aplicação, tratando qualidade, velocidade e concorrência (custo) como uma lei de escala tridimensional capaz de reduzir o custo de inferência em 10-100x.

## Conceitos-chave
- Alinhamento em múltiplas camadas: comportamento do usuário ↔ design do produto ↔ inferência
- Lei de escala futura em 3 dimensões: qualidade, velocidade e concorrência/custo
- Alinhamento da distribuição de dados da carga da aplicação com a distribuição dos dados de treinamento do modelo
- Co-otimização de pós-treinamento e inferência (fora do espaço da aplicação)
- Explosão combinatória da otimização de inferência (mais de 100.000 combinações)
- Predição multi-token (10 tokens por vez em vez de um por vez)
- Alinhamento de numérica/precisão à distribuição de dados da aplicação
- Seleção de hardware por SKU conforme vantagens específicas para a carga
- Sharding de modelo e inferência distribuída cross-host
- Seleção de kernel otimizada por distribuição da aplicação
- Reinforcement tuning orientado por dados de produção
- Data flywheel como diferencial competitivo de produtos de IA
- Metáfora do iceberg: a alta 'linha d'água' do custo de inferência esconde aplicações viáveis
- Infraestrutura de nuvem virtual abstraindo gestão de GPUs multi-fornecedor

## Ferramentas & pessoas
**Ferramentas:** Fireworks AI (plataforma de inferência), Bibliotecas de modelos abertos, Plataforma self-serve para desenvolvedores da Fireworks

**Pessoas/orgs:** Lin Qiao (Lynn Chow), Fireworks AI

## Claims acionáveis
- Otimizar inferência de forma isolada é insuficiente; a próxima fronteira de inovação é combinar pós-treinamento e inferência em co-otimização específica por aplicação
- O espaço de configuração (numérica, seleção de hardware, sharding, kernels, mecanismos de tuning de qualidade) excede 100.000 combinações possíveis
- Reduzir o custo de inferência em 10-100x ampliaria drasticamente o conjunto de aplicações com product-market fit que podem virar negócios sustentáveis
- Uma cadeia de fast food escalou um recurso de IA de 1 loja para 1.000 lojas em 3 meses usando a plataforma
- Uma empresa de software escalou seu recurso de IA de 100 mil para 25 milhões de desenvolvedores em 3 meses
- Modelos off-the-shelf dirigidos apenas por prompt engineering representam a fase frágil e imatura do alinhamento produto-modelo; infundir conhecimento do produto via dados de produção é a fronteira
- Pesquisadores precisam assumir usos do modelo que raramente coincidem com cargas reais, criando um gap permanente entre treinamento e aplicação que exige tuning com dados de produção

> **Deep dive:** `low` — Keynote promocional de fornecedor: apresenta uma tese arquitetural interessante (escala tridimensional e co-otimização) mas sem detalhes técnicos, benchmarks ou métodos acionáveis, com estudos de caso de marketing.
