---
title: "Dificuldade de avaliar agentes vs LLMs"
type: "extract"
source: "x"
status_id: "2083588813675274301"
handle: "cwolferesearch"
url: "https://x.com/cwolferesearch/status/2083588813675274301"
created_at: "2026-08-01T16:20:59.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-cwolferesearch-why-is-evaluating-agents-so-difficult-relative-to-evaluating--2083588813675274301.json]]"
tags: ["evals", "agents", "agent-loop", "verification"]
topic: "Dificuldade de avaliar agentes vs LLMs"
summary: "Explica por que avaliar agentes é mais difícil que avaliar um LLM padrão: enquanto o LLM produz uma única resposta a um prompt, o agente interage iterativamente com um ambiente (raciocina, chama ferramentas, observa resultados e repete). Vale salvar como formulação do problema central de evals para agentes."
key_points: ["Avaliar um LLM padrão reduz-se a julgar uma única resposta gerada para um prompt fixo", "Um agente opera em loop com o ambiente: raciocina, chama ferramentas, observa resultados e itera", "A avaliação deixa de ser sobre um output único e passa a exigir julgar trajetórias multi-etapas interdependentes", "A interação com o ambiente introduz variabilidade e dependência de estado que não existem no caso do LLM isolado"]
entities: ["@cwolferesearch"]
content_type: "question"
revisit: "medium"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HOpk7z0XIAAYjFl.png"]
---

# Dificuldade de avaliar agentes vs LLMs

**@cwolferesearch** · [2083588813675274301](https://x.com/cwolferesearch/status/2083588813675274301) · `question`

## Resumo
Explica por que avaliar agentes é mais difícil que avaliar um LLM padrão: enquanto o LLM produz uma única resposta a um prompt, o agente interage iterativamente com um ambiente (raciocina, chama ferramentas, observa resultados e repete). Vale salvar como formulação do problema central de evals para agentes.

## Pontos-chave
- Avaliar um LLM padrão reduz-se a julgar uma única resposta gerada para um prompt fixo
- Um agente opera em loop com o ambiente: raciocina, chama ferramentas, observa resultados e itera
- A avaliação deixa de ser sobre um output único e passa a exigir julgar trajetórias multi-etapas interdependentes
- A interação com o ambiente introduz variabilidade e dependência de estado que não existem no caso do LLM isolado

## Entidades
@cwolferesearch

> **Revisit:** `medium` · **fonte:** `tweet`
