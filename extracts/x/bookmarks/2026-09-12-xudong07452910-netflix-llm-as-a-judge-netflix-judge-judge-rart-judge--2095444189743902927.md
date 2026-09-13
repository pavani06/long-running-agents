---
title: "LLM-as-a-Judge em produção na Netflix"
type: "extract"
source: "x"
status_id: "2095444189743902927"
handle: "Xudong07452910"
url: "https://x.com/Xudong07452910/status/2095444189743902927"
created_at: "2026-09-03T09:30:00.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-xudong07452910-netflix-llm-as-a-judge-netflix-judge-judge-rart-judge--2095444189743902927.json]]"
tags: ["evals", "production", "verification", "process"]
topic: "LLM-as-a-Judge em produção na Netflix"
summary: "Paper documenta como a Netflix usa LLM-as-a-Judge em produção para avaliar as centenas de milhares de explicações de recomendação geradas semanalmente, impossíveis de revisar humanamente. Descreve o ciclo completo: padrões humanos, treino do Judge, interceptação em produção e monitoramento contínuo, incluindo um design chamado RART."
key_points: ["Netflix gera dezenas de milhares a centenas de milhares de explicações de 'por que recomendamos' por semana, volume inviável para revisão humana", "LLM-as-a-Judge foi efetivamente implantado no sistema de produção, não apenas em experimentos", "O paper cobre o ciclo de vida completo do Judge: estabelecimento de padrões anotados por humanos, treinamento, deploy com interceptação, e monitoramento/atualização contínuos", "Um dos designs apresentados chama-se RART, citado como destaque da arquitetura"]
entities: ["Netflix", "LLM-as-a-Judge", "RART"]
content_type: "resource"
revisit: "high"
grounded_in: "tweet"
links: []
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-argona0x-whoever-leaked-this-has-bigger-balls-than-sense-two-research--2082193490956476521|confiabilidade de LLM-as-judge]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-harness-engineering-is-a-top-skill-right-now-this-new-meta-p--2098426608793362916|Harness engineering e Auto-RecSys]]", "[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-suraj_sharma14-as-an-ai-engineer-you-must-build-these-projects-systems-that--2098026202464243908|Projetos práticos para AI Engineers]]", "[[extracts/x/bookmarks/2026-09-12-theprimeagen-something-that-has-greatly-improved-the-reliability-of-the-c--2081066227619836308|técnica de confiabilidade em código via LLM]]", "[[extracts/x/bookmarks/2026-09-12-ubereng-we-cut-uber-eats-search-latency-in-half-how-measure-identify--2098177194979983830|Uber Eats search latency halving]]"]
thin: false
theme: "Agent Harness e Evals"
---

# LLM-as-a-Judge em produção na Netflix

**@Xudong07452910** · [2095444189743902927](https://x.com/Xudong07452910/status/2095444189743902927) · `resource`

## Resumo
Paper documenta como a Netflix usa LLM-as-a-Judge em produção para avaliar as centenas de milhares de explicações de recomendação geradas semanalmente, impossíveis de revisar humanamente. Descreve o ciclo completo: padrões humanos, treino do Judge, interceptação em produção e monitoramento contínuo, incluindo um design chamado RART.

## Pontos-chave
- Netflix gera dezenas de milhares a centenas de milhares de explicações de 'por que recomendamos' por semana, volume inviável para revisão humana
- LLM-as-a-Judge foi efetivamente implantado no sistema de produção, não apenas em experimentos
- O paper cobre o ciclo de vida completo do Judge: estabelecimento de padrões anotados por humanos, treinamento, deploy com interceptação, e monitoramento/atualização contínuos
- Um dos designs apresentados chama-se RART, citado como destaque da arquitetura

## Entidades
Netflix, LLM-as-a-Judge, RART

> **Revisit:** `high` · **fonte:** `tweet`
