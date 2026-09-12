---
title: "Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 10: Inference"
type: "extract"
source: "youtube"
video_id: "EfM546A79aM"
url: "https://www.youtube.com/watch?v=EfM546A79aM"
channel: "Stanford Online"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-10-inference--EfM546A79aM.txt]]"
tags: ["agents", "analise", "arquitetura", "curriculo-conteudo", "runtime", "stack-tooling", "production", "token-budgeting"]
thesis: "Porque a geração autoregressiva impede paralelização ao longo da sequência, a decodificação de LLMs é memory-bound (ao contrário do prefill e do training), tornando a redução do KV cache (GQA, MLA, atenção local/híbrida) e da precisão numérica (quantização) as alavancas centrais para melhorar latência, throughput e TTFT sem degradar acurácia."
concepts: ["inferência autoregressiva vs. paralelismo do training", "KV cache e sua reutilização entre prefixos causais", "fases de prefill (compute-bound) e geração/decode (memory-bound)", "intensidade aritmética (FLOPs/bytes) e limite do acelerador (~295 no H100)", "métricas de serving: TTFT, latência por token, throughput (tokens/s)", "trade-off latência vs. throughput via batch size", "grouped-query attention (GQA) e multi-query attention (MQA)", "multi-latent attention (MLA) com compressão latente e incompatibilidade com RoPE", "cross-layer attention (CLA) com compartilhamento de KV entre camadas", "sliding window attention, atenção global+local e modelos híbridos", "atenção linear, Mamba, delta net e gated attention como compressão de histórico", "atenção esparsa/comprimida do DeepSeek (seleção via indexer)", "quantização: QAT vs. PTQ, GPTQ (compensação de erro via Hessiana), AWQ (precisão por canal conforme ativações)", "continuous batching para cargas com concorrência variável", "pruning de modelos como técnica de redução pós-treino", "tokens gerados como medida de gasto de computação em workloads agênticos"]
tools: ["vLLM", "SGLang", "TensorRT", "llama.cpp", "ChatGPT", "NVIDIA H100", "NVIDIA B200", "HBM/SRAM"]
people: ["Tatsu", "OpenAI", "DeepSeek", "Google (scaling book)", "NVIDIA"]
claims: ["Trate o número de tokens gerados como o gasto real de compute: em cenários agênticos não há teto de valor em acelerar inferência, ao contrário do mundo chatbot limitado pela velocidade de leitura humana", "A escala de inferência já rivaliza com o training: OpenAI produziria ~8,6 trilhões de tokens/dia, superando em <4 dias os 32 trilhões de tokens de treino do DeepSeek-V4", "Na geração, a intensidade aritmética da atenção é ~S/(S+1)≈1, muito abaixo do ponto de saturação do H100 (~295), o que explica por que a inferência é memory-bound", "Batch menor melhora latência e TTFT; batch maior melhora throughput mas piora latência e eventualmente estoura a memória HBM pelo crescimento do KV cache", "Reduzir o KV cache melhora simultaneamente latência e throughput (porque o gargalo é memória); a tensão fica apenas no dimensionamento do batch", "GQA reduz o KV cache por fator N/K com boa acurácia segundo o paper de 2023, mas resultados do DeepSeek indicam que pode haver perda — verifique acurácia por modelo antes de adotar", "MLA comprime K/V para um latente pequeno (16k→512 no DeepSeek-V2) mantendo acurácia próxima à MHA, mas exige dimensões extras para lidar com RoPE", "Sliding window torna o KV cache independente do comprimento da sequência (ótimo para contexto longo), mas perde expressividade — modele híbridos intercalando camadas locais e globais", "Para quantização: QAT dá melhores resultados mas exige retreino caro; PTQ com GPTQ (compensação de erro camada a camada via Hessiana) e AWQ (alocar precisão alta apenas a canais com ativações salientes) são alternativas baratas e eficazes", "Escolha de stack: vLLM como opção padrão, SGLang para workloads agênticos, TensorRT quando velocidade bruta importa e o escopo é estreito, llama.cpp para inferência em CPU", "Prefill é paralelizável como o training (todo o prompt visível de uma vez); apenas a geração é sequencial e limitante", "Toda mudança com perda (GQA, quantização, atenção esparsa) exige validação de acurácia em evals específicos do modelo antes de produção"]
deep_dive: "medium"
deep_dive_reason: "Há alta densidade de análise arquitetural quantitativa (intensidade aritmética, KV cache, tradeoffs de batch), mas é material de curso em grande parte revisão, sem novidade e com relevância apenas indireta aos domínios de harness, context-engineering, evals ou agent-fleets."
---

# Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 10: Inference

## Tese
Porque a geração autoregressiva impede paralelização ao longo da sequência, a decodificação de LLMs é memory-bound (ao contrário do prefill e do training), tornando a redução do KV cache (GQA, MLA, atenção local/híbrida) e da precisão numérica (quantização) as alavancas centrais para melhorar latência, throughput e TTFT sem degradar acurácia.

## Conceitos-chave
- inferência autoregressiva vs. paralelismo do training
- KV cache e sua reutilização entre prefixos causais
- fases de prefill (compute-bound) e geração/decode (memory-bound)
- intensidade aritmética (FLOPs/bytes) e limite do acelerador (~295 no H100)
- métricas de serving: TTFT, latência por token, throughput (tokens/s)
- trade-off latência vs. throughput via batch size
- grouped-query attention (GQA) e multi-query attention (MQA)
- multi-latent attention (MLA) com compressão latente e incompatibilidade com RoPE
- cross-layer attention (CLA) com compartilhamento de KV entre camadas
- sliding window attention, atenção global+local e modelos híbridos
- atenção linear, Mamba, delta net e gated attention como compressão de histórico
- atenção esparsa/comprimida do DeepSeek (seleção via indexer)
- quantização: QAT vs. PTQ, GPTQ (compensação de erro via Hessiana), AWQ (precisão por canal conforme ativações)
- continuous batching para cargas com concorrência variável
- pruning de modelos como técnica de redução pós-treino
- tokens gerados como medida de gasto de computação em workloads agênticos

## Ferramentas & pessoas
**Ferramentas:** vLLM, SGLang, TensorRT, llama.cpp, ChatGPT, NVIDIA H100, NVIDIA B200, HBM/SRAM

**Pessoas/orgs:** Tatsu, OpenAI, DeepSeek, Google (scaling book), NVIDIA

## Claims acionáveis
- Trate o número de tokens gerados como o gasto real de compute: em cenários agênticos não há teto de valor em acelerar inferência, ao contrário do mundo chatbot limitado pela velocidade de leitura humana
- A escala de inferência já rivaliza com o training: OpenAI produziria ~8,6 trilhões de tokens/dia, superando em <4 dias os 32 trilhões de tokens de treino do DeepSeek-V4
- Na geração, a intensidade aritmética da atenção é ~S/(S+1)≈1, muito abaixo do ponto de saturação do H100 (~295), o que explica por que a inferência é memory-bound
- Batch menor melhora latência e TTFT; batch maior melhora throughput mas piora latência e eventualmente estoura a memória HBM pelo crescimento do KV cache
- Reduzir o KV cache melhora simultaneamente latência e throughput (porque o gargalo é memória); a tensão fica apenas no dimensionamento do batch
- GQA reduz o KV cache por fator N/K com boa acurácia segundo o paper de 2023, mas resultados do DeepSeek indicam que pode haver perda — verifique acurácia por modelo antes de adotar
- MLA comprime K/V para um latente pequeno (16k→512 no DeepSeek-V2) mantendo acurácia próxima à MHA, mas exige dimensões extras para lidar com RoPE
- Sliding window torna o KV cache independente do comprimento da sequência (ótimo para contexto longo), mas perde expressividade — modele híbridos intercalando camadas locais e globais
- Para quantização: QAT dá melhores resultados mas exige retreino caro; PTQ com GPTQ (compensação de erro camada a camada via Hessiana) e AWQ (alocar precisão alta apenas a canais com ativações salientes) são alternativas baratas e eficazes
- Escolha de stack: vLLM como opção padrão, SGLang para workloads agênticos, TensorRT quando velocidade bruta importa e o escopo é estreito, llama.cpp para inferência em CPU
- Prefill é paralelizável como o training (todo o prompt visível de uma vez); apenas a geração é sequencial e limitante
- Toda mudança com perda (GQA, quantização, atenção esparsa) exige validação de acurácia em evals específicos do modelo antes de produção

> **Deep dive:** `medium` — Há alta densidade de análise arquitetural quantitativa (intensidade aritmética, KV cache, tradeoffs de batch), mas é material de curso em grande parte revisão, sem novidade e com relevância apenas indireta aos domínios de harness, context-engineering, evals ou agent-fleets.
