---
title: "TimesFM-3: forecasting multivariado"
type: "extract"
source: "x"
status_id: "2094483372718580066"
handle: "GoogleResearch"
url: "https://x.com/GoogleResearch/status/2094483372718580066"
created_at: "2026-08-31T17:52:04.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-googleresearch-introducing-timesfm-3-a-state-of-the-art-time-series-foundat--2094483372718580066.json]]"
tags: ["analise", "arquitetura", "data-platform", "model-selection", "performance"]
topic: "TimesFM-3: forecasting multivariado"
summary: "Google Research anuncia o TimesFM-3, modelo fundacional de séries temporais com 330M de parâmetros pré-treinado em mais de 1 trilhão de pontos, que faz previsão multivariada (múltiplos alvos, covariáveis passadas e futuras) em uma única passagem, superando Chronos-2 e Toto 2.0 nos benchmarks Gift-Eval, FEV-Bench e Time. Vale salvar por combinar precisão zero-shot, saída probabilística (9 quantis) e disponibilidade imediata em GitHub/Hugging Face, com integração BigQuery a caminho."
key_points: ["Nativamente multivariado e zero-shot: suporta múltiplos alvos previstos simultaneamente (ponto e quantis), covariáveis apenas históricas (ex.: tráfego na loja) e covariáveis dinâmicas passadas-futuras (ex.: promoções planejadas, previsão do tempo, feriados), sem fine-tuning por tarefa.", "Arquitetura decoder-only com patches de 32 passos e atenção em grade 2D alternando camadas: atenção temporal estritamente causal (dentro de cada série, evitando vazamento) e atenção variate completa (entre séries no mesmo instante, capturando correlações cruzadas); covariáveis futuras usam tokens 'lookahead' que concatenam patch atual com patches futuros conhecidos.", "Contiguous Patch Masking gera todo o horizonte de previsão numa única forward pass (sem decoding iterativo patch a patch, eliminando latência e acúmulo de erro) e emite 9 quantis (P10–P90) por alvo em cada passo, dando visão probabilística completa da incerteza.", "SOTA entre modelos fundacionais: 1º lugar em métricas pontuais e probabilísticas nos três benchmarks (Gift-Eval, FEV-Bench, Time); mesmo em modo univariado já iguala ou supera concorrentes como Chronos-2 e Toto 2.0, ganhando folga no modo multivariado pleno.", "Exemplo concreto de impacto: ao receber o calendário de promoções como covariável futuro, o modelo antecipa ~20% de aumento de vendas em cada dia promocional — algo que o modelo univariado ignora — somando em receita projetada mais precisa; disponível em GitHub e Hugging Face, com AI.FORECAST no BigQuery em semanas."]
entities: ["Google Research", "TimesFM-3", "TimesFM-2.5", "Chronos-2", "Toto 2.0", "Gift-Eval", "FEV-Bench", "BigQuery", "AI.FORECAST", "GitHub", "Hugging Face"]
content_type: "announcement"
revisit: "medium"
grounded_in: "article"
links: ["https://goo.gle/4x5WGpD"]
media: ["https://pbs.twimg.com/media/HREZb7FbwAAUjhK.jpg"]
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-fazle_karim1-googleresearch-i-wonder-how-it-would-do-on-this-research-of--2094501145536315670|GlucoFM: foundation model para CGM]]", "[[extracts/x/bookmarks/2026-09-16-googleresearch-introducing-retrieve-for-train-a-framework-that-accelerates--2099951761985601580|Retrieve-for-Train: difusão para retrieval]]", "[[extracts/x/bookmarks/2026-09-15-shanyanggm-github-1-tradingagents-ai-agent-https-t-co-nz1jbk3dkr-2-libr--2098941338297458746|Framework multi-agente de trading LLM]]", "[[extracts/x/bookmarks/2026-09-12-openhonor-puro-2b-is-open-beyond-the-weights-technical-report-final-in--2093994412770566256|Puro-2B: receita aberta de pré-treinamento barato]]", "[[extracts/x/bookmarks/2026-09-12-openai-now-available-chatgpt-for-financial-services-this-is-a-tailo--2098118191029624911|ChatGPT para serviços financeiros]]", "[[extracts/x/bookmarks/2026-09-12-googleresearch-introducing-toolgrad-an-efficient-framework-for-generating-t--2098183830968705163|ToolGrad: geração de datasets de tool-use]]", "[[extracts/x/bookmarks/2026-09-12-finviz_com-introducing-the-finviz-matrix-we-created-a-tool-that-no-othe--2098168161455514035|Lançamento Finviz Matrix]]"]
theme: "IA, execução e vencedores"
---

# TimesFM-3: forecasting multivariado

**@GoogleResearch** · [2094483372718580066](https://x.com/GoogleResearch/status/2094483372718580066) · `announcement`

## Resumo
Google Research anuncia o TimesFM-3, modelo fundacional de séries temporais com 330M de parâmetros pré-treinado em mais de 1 trilhão de pontos, que faz previsão multivariada (múltiplos alvos, covariáveis passadas e futuras) em uma única passagem, superando Chronos-2 e Toto 2.0 nos benchmarks Gift-Eval, FEV-Bench e Time. Vale salvar por combinar precisão zero-shot, saída probabilística (9 quantis) e disponibilidade imediata em GitHub/Hugging Face, com integração BigQuery a caminho.

## Pontos-chave
- Nativamente multivariado e zero-shot: suporta múltiplos alvos previstos simultaneamente (ponto e quantis), covariáveis apenas históricas (ex.: tráfego na loja) e covariáveis dinâmicas passadas-futuras (ex.: promoções planejadas, previsão do tempo, feriados), sem fine-tuning por tarefa.
- Arquitetura decoder-only com patches de 32 passos e atenção em grade 2D alternando camadas: atenção temporal estritamente causal (dentro de cada série, evitando vazamento) e atenção variate completa (entre séries no mesmo instante, capturando correlações cruzadas); covariáveis futuras usam tokens 'lookahead' que concatenam patch atual com patches futuros conhecidos.
- Contiguous Patch Masking gera todo o horizonte de previsão numa única forward pass (sem decoding iterativo patch a patch, eliminando latência e acúmulo de erro) e emite 9 quantis (P10–P90) por alvo em cada passo, dando visão probabilística completa da incerteza.
- SOTA entre modelos fundacionais: 1º lugar em métricas pontuais e probabilísticas nos três benchmarks (Gift-Eval, FEV-Bench, Time); mesmo em modo univariado já iguala ou supera concorrentes como Chronos-2 e Toto 2.0, ganhando folga no modo multivariado pleno.
- Exemplo concreto de impacto: ao receber o calendário de promoções como covariável futuro, o modelo antecipa ~20% de aumento de vendas em cada dia promocional — algo que o modelo univariado ignora — somando em receita projetada mais precisa; disponível em GitHub e Hugging Face, com AI.FORECAST no BigQuery em semanas.

## Links
- https://goo.gle/4x5WGpD

## Entidades
Google Research, TimesFM-3, TimesFM-2.5, Chronos-2, Toto 2.0, Gift-Eval, FEV-Bench, BigQuery, AI.FORECAST, GitHub, Hugging Face

> **Revisit:** `medium` · **fonte:** `article`
