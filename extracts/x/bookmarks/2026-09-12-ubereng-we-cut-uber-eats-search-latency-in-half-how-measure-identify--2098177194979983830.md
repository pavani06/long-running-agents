---
title: "Uber Eats search latency halving"
type: "extract"
source: "x"
status_id: "2098177194979983830"
handle: "UberEng"
url: "https://x.com/UberEng/status/2098177194979983830"
created_at: "2026-09-10T22:30:00.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-ubereng-we-cut-uber-eats-search-latency-in-half-how-measure-identify--2098177194979983830.json]]"
tags: ["performance", "agentic-coding", "evals", "arquitetura", "production", "harness", "observability"]
topic: "Uber Eats search latency halving"
summary: "Uber Eats cortou a latência de busca pela metade via workstreams full-stack — mudança da métrica para ATF (Above-the-Fold), poda de retrieval, split de hydration, tuning de infra — e, destaque, um loop agêntico de coding que media, corrigia e validava gargalos iterativamente. Vale salvar como playbook concreto de engenharia de performance em produção e como exemplo real de agentic-coding com verificação rápida via evals."
key_points: ["Mudança de métrica-chave de tempo de resposta da API para ATF (renderização do primeiro screen com imagens); paginação com cache server-side + renderização assíncrona de templates reduziram >200 ms de ATF", "Retrieval: remoção de estratégias lexicais de broad-recall redundantes (~120 ms sem regressão), deduplication antecipada de chains, e agrupamento por embeddings de produto reduziu lookups de dados >100x e 50 ms de latência", "Ranking: split da hydration monolítica em fases paralelas (ranking vs presentation, >100 ms), remoção de falsas dependências no DAG (~35 ms), request hedging em 4 camadas de hydration (~40 ms), GPU model serving", "Infra: encoding paralelo de resultados, embeddings com 5 casas decimais + varint (-46% tamanho, metade da latência de query), múltiplas conexões no service mesh (-53%), value types em Go cortando GC que consumia >40% de CPU — ~200 ms somados", "Loop agêntico: AI coding agent com tools para puxar perfis de latência de produção, ranquear gargalos por span, abrir PRs e rodar benchmarks antes do merge; framework de avaliação assistido por LLM validava que otimizações não degradavam qualidade — mais eficaz em wins pequenos que compostos em escala e que nunca entram no roadmap"]
entities: ["Uber Eats", "Uber Engineering", "AI coding agent", "LLM-assisted evaluation framework", "Search ML team", "Go", "GPU model serving"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://www.uber.com/us/en/blog/uber-eats-search-pipeline/"]
media: []
---

# Uber Eats search latency halving

**@UberEng** · [2098177194979983830](https://x.com/UberEng/status/2098177194979983830) · `resource`

## Resumo
Uber Eats cortou a latência de busca pela metade via workstreams full-stack — mudança da métrica para ATF (Above-the-Fold), poda de retrieval, split de hydration, tuning de infra — e, destaque, um loop agêntico de coding que media, corrigia e validava gargalos iterativamente. Vale salvar como playbook concreto de engenharia de performance em produção e como exemplo real de agentic-coding com verificação rápida via evals.

## Pontos-chave
- Mudança de métrica-chave de tempo de resposta da API para ATF (renderização do primeiro screen com imagens); paginação com cache server-side + renderização assíncrona de templates reduziram >200 ms de ATF
- Retrieval: remoção de estratégias lexicais de broad-recall redundantes (~120 ms sem regressão), deduplication antecipada de chains, e agrupamento por embeddings de produto reduziu lookups de dados >100x e 50 ms de latência
- Ranking: split da hydration monolítica em fases paralelas (ranking vs presentation, >100 ms), remoção de falsas dependências no DAG (~35 ms), request hedging em 4 camadas de hydration (~40 ms), GPU model serving
- Infra: encoding paralelo de resultados, embeddings com 5 casas decimais + varint (-46% tamanho, metade da latência de query), múltiplas conexões no service mesh (-53%), value types em Go cortando GC que consumia >40% de CPU — ~200 ms somados
- Loop agêntico: AI coding agent com tools para puxar perfis de latência de produção, ranquear gargalos por span, abrir PRs e rodar benchmarks antes do merge; framework de avaliação assistido por LLM validava que otimizações não degradavam qualidade — mais eficaz em wins pequenos que compostos em escala e que nunca entram no roadmap

## Links
- https://www.uber.com/us/en/blog/uber-eats-search-pipeline/

## Entidades
Uber Eats, Uber Engineering, AI coding agent, LLM-assisted evaluation framework, Search ML team, Go, GPU model serving

> **Revisit:** `high` · **fonte:** `article`
