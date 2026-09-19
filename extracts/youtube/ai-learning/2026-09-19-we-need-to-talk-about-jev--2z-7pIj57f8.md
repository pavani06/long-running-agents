---
title: "We need to talk about Jev..."
type: "extract"
source: "youtube"
video_id: "2z-7pIj57f8"
url: "https://www.youtube.com/watch?v=2z-7pIj57f8"
channel: "Matthew Berman"
extracted: "2026-09-19"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-19-we-need-to-talk-about-jev--2z-7pIj57f8.txt]]"
tags: ["agents", "agent-loop", "arquitetura", "analise", "model-selection", "decision-discipline", "classification"]
thesis: "Jev é um novo tipo de modelo de decisão (não de chat), treinado com RLCD em vez de RLHF, capaz de tomar milhares de decisões paralelas até 200x mais rápido e 400x mais barato que LLMs tradicionais, sendo ideal para roteamento, classificação e controle em tempo real, mas inadequado para codificação do zero ou estratégia de longo prazo."
concepts: ["RLCD (Reinforcement Learning for Calibrated Decisions) vs RLHF", "modelo de decisão generalizado vs modelo de chat", "decisões paralelas em massa em milissegundos", "alegação de zero alucinação via calibração de decisões", "trade-off velocidade/custo vs raciocínio profundo (ex.: xadrez)", "model routing (rotear prompts para o modelo certo)", "loops de decisão em tempo real (Doom, Melee, FSD)", "casos de uso críticos onde alucinação é catastrófica (saúde, militar, tráfego)", "token de saída gratuito e token de entrada a fração de centavo", "divisão de trabalho: LLMs tradicionais constroem o mundo, Jev decide em runtime"]
tools: ["Jev", "RLCD", "RLHF", "ChatGPT", "Zapier", "Claude Sonnet 5", "Claude Opus 5", "Claude Haiku 4.5", "GPT-6 Astra", "Fable", "Codex", "Doom", "Super Smash Bros. Melee", "Unclutter"]
people: ["co-criador do ChatGPT e fundador do Jev (não nomeado)", "Riley Brown", "Kitsy", "Justin Schroeder", "Alex (time do apresentador)", "Anthropic", "Nvidia", "Shopify", "Meta", "Cursor", "Samsung"]
claims: ["Use Jev como motor de decisão paralelo (roteamento de tickets, classificação, triagem) e não como modelo de chat ou gerador de código do zero", "Output tokens do Jev são gratuitos e input tokens custam fração de centavo, tornando-o muito mais barato que LLMs tradicionais para decisão de alto volume", "A arquitetura RLCD substitui o ajuste por feedback humano, reduzindo alucinação (alegação de zero) — relevante para casos críticos como saúde e tráfego", "Posicione Jev como model router entre prompt e modelos maiores/mais caros, escolhendo destino com custo/latência mínimos", "Padrão de arquitetura emergente: use Claude/Codex para construir o ambiente ou código base, e Jev para o loop de decisão em tempo real (demos de FSD e simulação da cidade)", "Evite Jev para tarefas de raciocínio de longo prazo como xadrez clássico: ele perde em qualidade material para Fable/GPT-6 Astra, embora vença bullet chess por tempo de resposta (~2,6s por lance)", "Jev pode ser integrado a workflows de automação (ex.: Zapier com 9.000+ apps) para decisões empresariais a alta velocidade e baixo custo", "A velocidade real-time permite controlar jogos e agentes (Doom, Melee, browser/wiki-race) onde LLMs tradicionais levam 4-5 segundos por passo"]
deep_dive: "medium"
deep_dive_reason: "O vídeo apresenta uma distinção arquitetural genuinamente nova (RLCD, modelo de decisão vs chat) com tradeoffs e padrões de uso acionáveis, mas é majoritariamente promocional e baseado em demos, sem profundidade de implementação em harness, evals ou context-engineering."
---

# We need to talk about Jev...

## Tese
Jev é um novo tipo de modelo de decisão (não de chat), treinado com RLCD em vez de RLHF, capaz de tomar milhares de decisões paralelas até 200x mais rápido e 400x mais barato que LLMs tradicionais, sendo ideal para roteamento, classificação e controle em tempo real, mas inadequado para codificação do zero ou estratégia de longo prazo.

## Conceitos-chave
- RLCD (Reinforcement Learning for Calibrated Decisions) vs RLHF
- modelo de decisão generalizado vs modelo de chat
- decisões paralelas em massa em milissegundos
- alegação de zero alucinação via calibração de decisões
- trade-off velocidade/custo vs raciocínio profundo (ex.: xadrez)
- model routing (rotear prompts para o modelo certo)
- loops de decisão em tempo real (Doom, Melee, FSD)
- casos de uso críticos onde alucinação é catastrófica (saúde, militar, tráfego)
- token de saída gratuito e token de entrada a fração de centavo
- divisão de trabalho: LLMs tradicionais constroem o mundo, Jev decide em runtime

## Ferramentas & pessoas
**Ferramentas:** Jev, RLCD, RLHF, ChatGPT, Zapier, Claude Sonnet 5, Claude Opus 5, Claude Haiku 4.5, GPT-6 Astra, Fable, Codex, Doom, Super Smash Bros. Melee, Unclutter

**Pessoas/orgs:** co-criador do ChatGPT e fundador do Jev (não nomeado), Riley Brown, Kitsy, Justin Schroeder, Alex (time do apresentador), Anthropic, Nvidia, Shopify, Meta, Cursor, Samsung

## Claims acionáveis
- Use Jev como motor de decisão paralelo (roteamento de tickets, classificação, triagem) e não como modelo de chat ou gerador de código do zero
- Output tokens do Jev são gratuitos e input tokens custam fração de centavo, tornando-o muito mais barato que LLMs tradicionais para decisão de alto volume
- A arquitetura RLCD substitui o ajuste por feedback humano, reduzindo alucinação (alegação de zero) — relevante para casos críticos como saúde e tráfego
- Posicione Jev como model router entre prompt e modelos maiores/mais caros, escolhendo destino com custo/latência mínimos
- Padrão de arquitetura emergente: use Claude/Codex para construir o ambiente ou código base, e Jev para o loop de decisão em tempo real (demos de FSD e simulação da cidade)
- Evite Jev para tarefas de raciocínio de longo prazo como xadrez clássico: ele perde em qualidade material para Fable/GPT-6 Astra, embora vença bullet chess por tempo de resposta (~2,6s por lance)
- Jev pode ser integrado a workflows de automação (ex.: Zapier com 9.000+ apps) para decisões empresariais a alta velocidade e baixo custo
- A velocidade real-time permite controlar jogos e agentes (Doom, Melee, browser/wiki-race) onde LLMs tradicionais levam 4-5 segundos por passo

> **Deep dive:** `medium` — O vídeo apresenta uma distinção arquitetural genuinamente nova (RLCD, modelo de decisão vs chat) com tradeoffs e padrões de uso acionáveis, mas é majoritariamente promocional e baseado em demos, sem profundidade de implementação em harness, evals ou context-engineering.
