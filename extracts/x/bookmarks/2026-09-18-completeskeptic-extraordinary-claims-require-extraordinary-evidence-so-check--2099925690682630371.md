---
title: "Modelos estruturados para automação"
type: "extract"
source: "x"
status_id: "2099925690682630371"
handle: "CompleteSkeptic"
url: "https://x.com/CompleteSkeptic/status/2099925690682630371"
created_at: "2026-09-15T18:17:54.000Z"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-18-completeskeptic-extraordinary-claims-require-extraordinary-evidence-so-check--2099925690682630371.json]]"
tags: ["agents", "performance", "evals", "decision-discipline", "model-selection", "production", "startups"]
topic: "Modelos estruturados para automação"
summary: "TypeSafe AI (Diogo Almeida, ex-OpenAI) sai do stealth e lança Jev, primeiro \"System One Model\": sem geração de strings, emite decisões estruturadas tipadas com probabilidades calibradas, alegando 40-200x mais velocidade e ~2 ordens de magnitude menos custo que LLMs de fronteira. Vale salvar como proposta de novo paradigma de modelo pensado para automação em software, não para chat."
key_points: ["Nova stack dedicada a automação: arquitetura nova, sampler paralelo (toda a saída numa única query) e RLCD (Reinforcement Learning for Calibrated Decisions), otimizando decisões epistemicamente calibradas em vez de preferência humana (RLHF/RLVR).", "Outputs type-safe definidos por schema de antemão: zero erros de tipo e alucinação matematicamente impossível; toda resposta acompanha probabilidade e score de confiança calibrados (mais confiança = mais acerto).", "Economia e latência: $0.042/MTok de input com output gratuito, respostas em 70-500ms vs 3-329s de LLMs de fronteira; workflow evals públicos sustentam os números de 193.6x mais rápido e 444.6x mais barato divulgados na homepage.", "Casos de uso: \"smart if-statements\" (classificar, rotear, pontuar, extrair, branchear) embutidos em código comum, aplicações em tempo real, map-reduce sobre petabytes e verificação/guardrails de prompts, traços de raciocínio e outputs de LLMs.", "Metodologia das evals: cada modelo recebe o mesmo workflow e é comparado à média de referência dos modelos mais caros (GPT-6 Astra e Fable 5.1); o post é incomum ao listar nuances/vieses de cada claim, e demos incluem um bot de Doom em tempo real e Wikiracing com cardinalidade até 255."]
entities: ["TypeSafe AI", "Diogo Almeida", "Jev", "OpenAI", "ChatGPT", "GPT-5.6 Terra", "GPT-6 Astra", "Fable 5.1", "DeepSeek", "OpenRouter"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://typesafe.ai/blog/introducing-system-one-models-and-jev", "https://typesafe.ai/"]
media: []
---

# Modelos estruturados para automação

**@CompleteSkeptic** · [2099925690682630371](https://x.com/CompleteSkeptic/status/2099925690682630371) · `announcement`

## Resumo
TypeSafe AI (Diogo Almeida, ex-OpenAI) sai do stealth e lança Jev, primeiro "System One Model": sem geração de strings, emite decisões estruturadas tipadas com probabilidades calibradas, alegando 40-200x mais velocidade e ~2 ordens de magnitude menos custo que LLMs de fronteira. Vale salvar como proposta de novo paradigma de modelo pensado para automação em software, não para chat.

## Pontos-chave
- Nova stack dedicada a automação: arquitetura nova, sampler paralelo (toda a saída numa única query) e RLCD (Reinforcement Learning for Calibrated Decisions), otimizando decisões epistemicamente calibradas em vez de preferência humana (RLHF/RLVR).
- Outputs type-safe definidos por schema de antemão: zero erros de tipo e alucinação matematicamente impossível; toda resposta acompanha probabilidade e score de confiança calibrados (mais confiança = mais acerto).
- Economia e latência: $0.042/MTok de input com output gratuito, respostas em 70-500ms vs 3-329s de LLMs de fronteira; workflow evals públicos sustentam os números de 193.6x mais rápido e 444.6x mais barato divulgados na homepage.
- Casos de uso: "smart if-statements" (classificar, rotear, pontuar, extrair, branchear) embutidos em código comum, aplicações em tempo real, map-reduce sobre petabytes e verificação/guardrails de prompts, traços de raciocínio e outputs de LLMs.
- Metodologia das evals: cada modelo recebe o mesmo workflow e é comparado à média de referência dos modelos mais caros (GPT-6 Astra e Fable 5.1); o post é incomum ao listar nuances/vieses de cada claim, e demos incluem um bot de Doom em tempo real e Wikiracing com cardinalidade até 255.

## Links
- https://typesafe.ai/blog/introducing-system-one-models-and-jev
- https://typesafe.ai/

## Entidades
TypeSafe AI, Diogo Almeida, Jev, OpenAI, ChatGPT, GPT-5.6 Terra, GPT-6 Astra, Fable 5.1, DeepSeek, OpenRouter

> **Revisit:** `high` · **fonte:** `article`
