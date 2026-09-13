---
title: "Memória para agentes longos"
type: "extract"
source: "x"
status_id: "2097555607389896732"
handle: "dair_ai"
url: "https://x.com/dair_ai/status/2097555607389896732"
created_at: "2026-09-09T05:20:02.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-dair_ai-good-work-on-improving-memory-for-long-horizon-agents-they-s--2097555607389896732.json]]"
tags: ["memory-architecture", "agents", "context-management", "token-budgeting", "context-engineering", "agent-loop"]
topic: "Memória para agentes longos"
summary: "Destaca trabalho que separa duas funções usualmente colapsadas em sistemas de memória de agentes: como memórias são mescladas na escrita e como o conteúdo recuperado é montado no prompt, sob orçamento de prompt restrito. Vale salvar por formalizar uma distinção arquitetural central para agentes de longo horizonte."
key_points: ["Separa o merge de memórias no momento da escrita da montagem do prompt no momento da recuperação — duas preocupações que papers de memória de agentes costumam tratar como uma só.", "O cenário avaliado opera sob orçamento de prompt restrito, tornando a gestão de contexto um constraint explícito do design.", "A distinção é diretamente aplicável ao desenho de sistemas de memória para agentes de longo horizonte (decidir o que consolidar vs. o que incluir no contexto)."]
entities: ["DAIR.AI"]
content_type: "announcement"
revisit: "high"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HRwDtUeawAA0h5X.png"]
---

# Memória para agentes longos

**@dair_ai** · [2097555607389896732](https://x.com/dair_ai/status/2097555607389896732) · `announcement`

## Resumo
Destaca trabalho que separa duas funções usualmente colapsadas em sistemas de memória de agentes: como memórias são mescladas na escrita e como o conteúdo recuperado é montado no prompt, sob orçamento de prompt restrito. Vale salvar por formalizar uma distinção arquitetural central para agentes de longo horizonte.

## Pontos-chave
- Separa o merge de memórias no momento da escrita da montagem do prompt no momento da recuperação — duas preocupações que papers de memória de agentes costumam tratar como uma só.
- O cenário avaliado opera sob orçamento de prompt restrito, tornando a gestão de contexto um constraint explícito do design.
- A distinção é diretamente aplicável ao desenho de sistemas de memória para agentes de longo horizonte (decidir o que consolidar vs. o que incluir no contexto).

## Entidades
DAIR.AI

> **Revisit:** `high` · **fonte:** `tweet`
