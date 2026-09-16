---
title: "Escalando CI/test selection para agentic coding"
type: "extract"
source: "x"
status_id: "2099577600159158765"
handle: "addyosmani"
url: "https://x.com/addyosmani/status/2099577600159158765"
created_at: "2026-09-14T19:14:42.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-15-addyosmani-at-anthropic-claude-now-writes-80-of-our-code-engineers-ship--2099577600159158765.json]]"
tags: ["agentic-coding", "harness", "performance", "arquitetura", "state", "testes-qa", "observability", "production"]
topic: "Escalando CI/test selection para agentic coding"
summary: "Anthropic relata que agentic coding (Claude escreve 80% do código, engineers ship 8x mais código/trimestre) elevou jobs de CI 25x em 6 meses; a solução sustentável foi redesenhar o serviço de test impact analysis como workers stateless com journal em in-memory store, não aplicar patches incrementais."
key_points: ["Métricas do impacto: 8x mais código por engenheiro por trimestre desde 2021-2025, 80% escrito por Claude, 10x mais testes e 25x mais jobs de CI em 6 meses, com número quase constante de engenheiros.", "Três quick fixes tiveram vida útil decrescente — dobrar cores (70 dias), shard por pacote com um writer por pacote (29 dias), restart (<1 dia) — ilustrando a lição: sempre planejar para o exponencial em vez de half-measures.", "Redesenho final: listener stateless processa qualquer resultado e anexa a um journal em in-memory store; um consumer separado consolida histórico por teste a cada segundos; selector consulta rapidamente — caro, mas horizontalmente escalável e 3 semanas para 1 engenheiro (antes ~um trimestre).", "Agentes mudam o formato de carga: PRs menores e mais granulares, atividade contínua (noites/fins de semana) sobre piso elevado e ainda bursty via humanos — mais razão para seleção determinística de testes em vez de rodar tudo em todo PR.", "Recomendações acionáveis: projetar v0 assumindo 25x de carga em dois trimestres (a bar de over-engineering subiu), instrumentar serviços como 'olhos e ouvidos' do Claude para hill-climbing autônomo, manter estado fora do processo e evitar singletons sem medição/canary."]
entities: ["Anthropic", "Claude", "Claude Tag", "@addyosmani"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://claude.com/blog/agentic-coding-is-straining-ci-heres-how-we-scaled-test-impact-analysis-at-anthropic"]
media: ["https://pbs.twimg.com/media/HSMyfjPaUAApdN6.jpg"]
---

# Escalando CI/test selection para agentic coding

**@addyosmani** · [2099577600159158765](https://x.com/addyosmani/status/2099577600159158765) · `resource`

## Resumo
Anthropic relata que agentic coding (Claude escreve 80% do código, engineers ship 8x mais código/trimestre) elevou jobs de CI 25x em 6 meses; a solução sustentável foi redesenhar o serviço de test impact analysis como workers stateless com journal em in-memory store, não aplicar patches incrementais.

## Pontos-chave
- Métricas do impacto: 8x mais código por engenheiro por trimestre desde 2021-2025, 80% escrito por Claude, 10x mais testes e 25x mais jobs de CI em 6 meses, com número quase constante de engenheiros.
- Três quick fixes tiveram vida útil decrescente — dobrar cores (70 dias), shard por pacote com um writer por pacote (29 dias), restart (<1 dia) — ilustrando a lição: sempre planejar para o exponencial em vez de half-measures.
- Redesenho final: listener stateless processa qualquer resultado e anexa a um journal em in-memory store; um consumer separado consolida histórico por teste a cada segundos; selector consulta rapidamente — caro, mas horizontalmente escalável e 3 semanas para 1 engenheiro (antes ~um trimestre).
- Agentes mudam o formato de carga: PRs menores e mais granulares, atividade contínua (noites/fins de semana) sobre piso elevado e ainda bursty via humanos — mais razão para seleção determinística de testes em vez de rodar tudo em todo PR.
- Recomendações acionáveis: projetar v0 assumindo 25x de carga em dois trimestres (a bar de over-engineering subiu), instrumentar serviços como 'olhos e ouvidos' do Claude para hill-climbing autônomo, manter estado fora do processo e evitar singletons sem medição/canary.

## Links
- https://claude.com/blog/agentic-coding-is-straining-ci-heres-how-we-scaled-test-impact-analysis-at-anthropic

## Entidades
Anthropic, Claude, Claude Tag, @addyosmani

> **Revisit:** `high` · **fonte:** `article`
