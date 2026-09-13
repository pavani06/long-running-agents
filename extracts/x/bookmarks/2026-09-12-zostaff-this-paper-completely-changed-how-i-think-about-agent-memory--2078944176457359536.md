---
title: "Arquitetura de memória para agentes"
type: "extract"
source: "x"
status_id: "2078944176457359536"
handle: "zostaff"
url: "https://x.com/zostaff/status/2078944176457359536"
created_at: "2026-07-19T20:44:51.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-zostaff-this-paper-completely-changed-how-i-think-about-agent-memory--2078944176457359536.json]]"
tags: ["memory-architecture", "agents", "context-management"]
topic: "Arquitetura de memória para agentes"
summary: "Recomendação de um paper que propõe um pipeline estruturado de 5 estágios para acesso à memória de agentes (Rewrite → Tag → Traverse → Prune → Reconstruct), em vez de armazenamento/recuperação brutos. Vale salvar como blueprint reutilizável para projetar sistemas de memória persistente em agentes."
key_points: ["Pipeline de memória em 5 passos: Rewrite → Tag → Traverse → Prune → Reconstruct, cada estágio com função definida na transformação do diálogo em memória consultável", "Rewrite normaliza cada turno de diálogo numa sentença autocontida: pronomes resolvidos para entidades e tempos relativos convertidos em absolutos, eliminando dependência de contexto externo", "Abordagem muda o paradigma de acesso à memória: pré-processamento estruturado do que é armazenado, e não apenas recuperação por similaridade"]
entities: ["zostaff"]
content_type: "resource"
revisit: "high"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HNnAEWpWoAAVfzm.jpg"]
---

# Arquitetura de memória para agentes

**@zostaff** · [2078944176457359536](https://x.com/zostaff/status/2078944176457359536) · `resource`

## Resumo
Recomendação de um paper que propõe um pipeline estruturado de 5 estágios para acesso à memória de agentes (Rewrite → Tag → Traverse → Prune → Reconstruct), em vez de armazenamento/recuperação brutos. Vale salvar como blueprint reutilizável para projetar sistemas de memória persistente em agentes.

## Pontos-chave
- Pipeline de memória em 5 passos: Rewrite → Tag → Traverse → Prune → Reconstruct, cada estágio com função definida na transformação do diálogo em memória consultável
- Rewrite normaliza cada turno de diálogo numa sentença autocontida: pronomes resolvidos para entidades e tempos relativos convertidos em absolutos, eliminando dependência de contexto externo
- Abordagem muda o paradigma de acesso à memória: pré-processamento estruturado do que é armazenado, e não apenas recuperação por similaridade

## Entidades
zostaff

> **Revisit:** `high` · **fonte:** `tweet`
