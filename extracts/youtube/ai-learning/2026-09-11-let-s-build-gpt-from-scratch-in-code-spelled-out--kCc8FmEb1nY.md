---
title: "Let's build GPT: from scratch, in code, spelled out."
type: "extract"
source: "youtube"
video_id: "kCc8FmEb1nY"
url: "https://www.youtube.com/watch?v=kCc8FmEb1nY"
channel: "Andrej Karpathy"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-let-s-build-gpt-from-scratch-in-code-spelled-out--kCc8FmEb1nY.txt]]"
tags: ["arquitetura", "curriculo-conteudo", "stack-tooling", "context-management"]
thesis: "Construir do zero um Transformer de nível caractere (no estilo nanoGPT, treinado em tiny Shakespeare) é a forma mais esclarecedora de entender como o ChatGPT funciona por dentro, da tokenização à self-attention."
concepts: ["modelos de linguagem probabilísticos", "arquitetura Transformer (Attention Is All You Need, 2017)", "tokenização nível caractere vs subword", "trade-off codebook vs comprimento de sequência", "block size / comprimento de contexto", "empacotamento de múltiplos exemplos em um chunk (block_size+1)", "batching para paralelismo em GPU", "bigram language model como baseline", "tabela de embeddings de tokens", "cross-entropy / negative log likelihood", "split treino/validação e detecção de overfitting", "geração autorregressiva (softmax + torch.multinomial)", "otimizador AdamW vs SGD", "modos train/eval e torch.no_grad", "causalidade: tokens só acessam o passado", "média incremental via matriz triangular inferior (precursor matemático da self-attention)"]
tools: ["ChatGPT", "nanoGPT", "PyTorch", "Google Colab / Jupyter", "tiktoken", "SentencePiece", "GPT-2", "tiny Shakespeare", "OpenWebText", "CUDA"]
people: ["OpenAI", "Google", "autores de 'Attention Is All You Need' (2017)"]
claims: ["Um chunk de block_size+1 caracteres contém block_size exemplos de treino embutidos; treinar em contextos de 1 até block_size garante que a inferência funcione com qualquer contexto parcial antes do truncamento.", "A escolha do tokenizer é um trade-off explícito: vocabulário pequeno (65 caracteres) produz sequências longas, enquanto subword (GPT-2 usa 50.257 tokens, ex. 'hi there' vira 3 inteiros) comprime a sequência ao custo de um codebook maior.", "O baseline bigram atinge loss ~2.5 em tiny Shakespeare, e a loss teórica de um modelo aleatório é ln(vocab_size)≈4.17 — usar isso como sanity check do treinamento.", "F.cross_entropy do PyTorch exige os canais na segunda dimensão: reshaping logits (B,T,C)→(B*T,C) e targets (B,T)→(B*T).", "Usar AdamW com learning rate ~3e-4 como padrão (valores muito maiores toleráveis em redes minúsculas) em vez de SGD simples.", "Estimar a loss pela média sobre múltiplos batches, dentro de model.eval() e torch.no_grad(), para reduzir o ruído de batches individuais e medir overfitting treino vs validação.", "A comunicação entre tokens deve ser causal: o token na posição t só pode ver posições ≤ t, porque as posições futuras são exatamente o que o modelo deve prever.", "A média cumulativa (bag of words) sobre o passado — forma fraca e com perda de informação de arranjo espacial — pode ser computada eficientemente como multiplicação por uma matriz triangular inferior normalizada por linha, que é o truque matemático no coração da implementação eficiente da self-attention."]
deep_dive: "medium"
deep_dive_reason: "Aula densa e acionável sobre fundamentos arquiteturais de Transformers (tokenização, batching, causalidade, truque matricial da atenção), mas é conteúdo introdutório consolidado, sem novidade nem foco em harness, evals de agentes, agent-fleets ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-10-inference--EfM546A79aM|Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 10: Inference]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs25-transformers-united-v6-i-from-language-models-to-native-multimodal--NDdc39KYqDU|Stanford CS25: Transformers United V6 I From Language Models to Native Multimodal Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-intro-to-fine-tuning-large-language-models--H-oCV5brtU4|Intro to Fine-Tuning Large Language Models]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-get-ahead-of-99-of-people-with-ai--0tLHVyd7WtM|How to Get Ahead of 99% of People (with AI)]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-harness-matters-more-than-the-model-yc-paper-club--n9xKblqyQ28|Why The Harness Matters More Than The Model | YC Paper Club]]"]
---

# Let's build GPT: from scratch, in code, spelled out.

## Tese
Construir do zero um Transformer de nível caractere (no estilo nanoGPT, treinado em tiny Shakespeare) é a forma mais esclarecedora de entender como o ChatGPT funciona por dentro, da tokenização à self-attention.

## Conceitos-chave
- modelos de linguagem probabilísticos
- arquitetura Transformer (Attention Is All You Need, 2017)
- tokenização nível caractere vs subword
- trade-off codebook vs comprimento de sequência
- block size / comprimento de contexto
- empacotamento de múltiplos exemplos em um chunk (block_size+1)
- batching para paralelismo em GPU
- bigram language model como baseline
- tabela de embeddings de tokens
- cross-entropy / negative log likelihood
- split treino/validação e detecção de overfitting
- geração autorregressiva (softmax + torch.multinomial)
- otimizador AdamW vs SGD
- modos train/eval e torch.no_grad
- causalidade: tokens só acessam o passado
- média incremental via matriz triangular inferior (precursor matemático da self-attention)

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, nanoGPT, PyTorch, Google Colab / Jupyter, tiktoken, SentencePiece, GPT-2, tiny Shakespeare, OpenWebText, CUDA

**Pessoas/orgs:** OpenAI, Google, autores de 'Attention Is All You Need' (2017)

## Claims acionáveis
- Um chunk de block_size+1 caracteres contém block_size exemplos de treino embutidos; treinar em contextos de 1 até block_size garante que a inferência funcione com qualquer contexto parcial antes do truncamento.
- A escolha do tokenizer é um trade-off explícito: vocabulário pequeno (65 caracteres) produz sequências longas, enquanto subword (GPT-2 usa 50.257 tokens, ex. 'hi there' vira 3 inteiros) comprime a sequência ao custo de um codebook maior.
- O baseline bigram atinge loss ~2.5 em tiny Shakespeare, e a loss teórica de um modelo aleatório é ln(vocab_size)≈4.17 — usar isso como sanity check do treinamento.
- F.cross_entropy do PyTorch exige os canais na segunda dimensão: reshaping logits (B,T,C)→(B*T,C) e targets (B,T)→(B*T).
- Usar AdamW com learning rate ~3e-4 como padrão (valores muito maiores toleráveis em redes minúsculas) em vez de SGD simples.
- Estimar a loss pela média sobre múltiplos batches, dentro de model.eval() e torch.no_grad(), para reduzir o ruído de batches individuais e medir overfitting treino vs validação.
- A comunicação entre tokens deve ser causal: o token na posição t só pode ver posições ≤ t, porque as posições futuras são exatamente o que o modelo deve prever.
- A média cumulativa (bag of words) sobre o passado — forma fraca e com perda de informação de arranjo espacial — pode ser computada eficientemente como multiplicação por uma matriz triangular inferior normalizada por linha, que é o truque matemático no coração da implementação eficiente da self-attention.

> **Deep dive:** `medium` — Aula densa e acionável sobre fundamentos arquiteturais de Transformers (tokenização, batching, causalidade, truque matricial da atenção), mas é conteúdo introdutório consolidado, sem novidade nem foco em harness, evals de agentes, agent-fleets ou governança.
