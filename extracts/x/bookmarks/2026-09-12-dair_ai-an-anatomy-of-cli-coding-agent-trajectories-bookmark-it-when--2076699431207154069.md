---
title: "análise de trajetórias de agentes de código"
type: "extract"
source: "x"
status_id: "2076699431207154069"
handle: "dair_ai"
url: "https://x.com/dair_ai/status/2076699431207154069"
created_at: "2026-07-13T16:05:02.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-dair_ai-an-anatomy-of-cli-coding-agent-trajectories-bookmark-it-when--2076699431207154069.json]]"
tags: ["agentic-coding", "agents", "evals", "tracing", "observability"]
topic: "análise de trajetórias de agentes de código"
summary: "Paper que dissec a trajetórias de execução de agentes de código via CLI para identificar onde a run de fato degenerou, em vez de julgar apenas pelo rótulo final de sucesso/falha. Vale salvar porque propõe o passo seguinte aos benchmarks de pass/fail: diagnóstico do ponto de falha dentro da trajetória."
key_points: ["Estudos de confiabilidade de agentes tipicamente usam apenas o rótulo final (passou/falhou), tratando a trajetória intermediária como caixa-preta", "O trabalho anatomiza trajetórias de agentes de código em CLI para localizar o momento em que a execução realmente saiu dos trilhos", "Premissa prática: saber 'quando a run deu errado' é necessário para diagnosticar e melhorar confiabilidade, não apenas medir taxa de acerto", "Foco empírico em agentes de codificação operando por linha de comando"]
entities: ["DAIR.AI (dair_ai)", "An Anatomy of CLI Coding Agent Trajectories (paper)"]
content_type: "resource"
revisit: "high"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HNHrIEBbcAA2Me7.jpg"]
---

# análise de trajetórias de agentes de código

**@dair_ai** · [2076699431207154069](https://x.com/dair_ai/status/2076699431207154069) · `resource`

## Resumo
Paper que dissec a trajetórias de execução de agentes de código via CLI para identificar onde a run de fato degenerou, em vez de julgar apenas pelo rótulo final de sucesso/falha. Vale salvar porque propõe o passo seguinte aos benchmarks de pass/fail: diagnóstico do ponto de falha dentro da trajetória.

## Pontos-chave
- Estudos de confiabilidade de agentes tipicamente usam apenas o rótulo final (passou/falhou), tratando a trajetória intermediária como caixa-preta
- O trabalho anatomiza trajetórias de agentes de código em CLI para localizar o momento em que a execução realmente saiu dos trilhos
- Premissa prática: saber 'quando a run deu errado' é necessário para diagnosticar e melhorar confiabilidade, não apenas medir taxa de acerto
- Foco empírico em agentes de codificação operando por linha de comando

## Entidades
DAIR.AI (dair_ai), An Anatomy of CLI Coding Agent Trajectories (paper)

> **Revisit:** `high` · **fonte:** `tweet`
