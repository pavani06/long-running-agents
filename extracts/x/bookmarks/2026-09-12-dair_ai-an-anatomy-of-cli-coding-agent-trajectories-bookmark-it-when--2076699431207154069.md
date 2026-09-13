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
relates-to: ["[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-finally-an-open-source-runtime-security-layer-for-your-agent--2098042808221511836|runtime security layer para agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-great-paper-from-google-and-colleagues-it-proposes-an-intere--2094472291002589452|Degradação de agentes em tarefas long-horizon]]", "[[extracts/x/bookmarks/2026-09-12-anatolikopadze-anthropic-engineer-you-re-not-supposed-to-babysit-the-model--2080702441809399834|agentes paralelos em grafos]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-it-s-well-known-that-agents-hack-benchmark-rewards-the-usual--2098592449568591902|reward hacking em benchmarks de agentes]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-karpathys-agentic-engineering-finally-has-proper-devtools-wh--2098398242727940442|DevTools para engenharia agêntica]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-good-work-on-improving-memory-for-long-horizon-agents-they-s--2097555607389896732|Memória para agentes longos]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-brilliant-new-paper-from-the-qwen-team-it-provides-insights--2095880318146507139|Ambientes de treino de agentes]]", "[[extracts/x/bookmarks/2026-09-12-eya0-every-ai-accountant-fails-the-same-way-fluent-confident-unve--2097801524579864803|Agentes de IA contáveis verificáveis]]", "[[extracts/x/bookmarks/2026-09-12-svpino-i-ve-been-trying-codex-to-analyze-a-dataset-and-honestly-i-v--2098489252707541305|Codex para análise de dados]]", "[[extracts/x/bookmarks/2026-09-12-cwolferesearch-why-is-evaluating-agents-so-difficult-relative-to-evaluating--2083588813675274301|Dificuldade de avaliar agentes vs LLMs]]", "[[extracts/x/bookmarks/2026-09-12-marionlepert-catching-skin-cancer-early-is-a-home-robotics-problem-melano--2082512842742489258|detecção de melanoma via robótica doméstica]]"]
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
