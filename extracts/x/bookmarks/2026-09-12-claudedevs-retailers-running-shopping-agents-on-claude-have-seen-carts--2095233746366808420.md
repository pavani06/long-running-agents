---
title: "Arquitetura de agentes de comércio com Claude"
type: "extract"
source: "x"
status_id: "2095233746366808420"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2095233746366808420"
created_at: "2026-09-02T19:33:47.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420.json]]"
tags: ["agents", "agent-loop", "arquitetura", "agent-tooling", "evals", "performance", "context-management", "token-budgeting", "harness", "production", "model-selection"]
topic: "Arquitetura de agentes de comércio com Claude"
summary: "Guia da Anthropic sobre agentes de e-commerce em produção com Claude: um agente único com skills (em vez de subagentes por domínio), ferramentas construídas sobre sistemas core, UI-como-tool e práticas de latência e evals. Deployments enterprise reportam carrinhos até 35% maiores e 60% mais compras concluídas."
key_points: ["Agente único com skills supera consistentemente tanto o design one-prompt-for-everything quanto subagente-por-domínio em qualidade, muitas vezes com menor custo e latência: cada handoff é state-lossy, multiplica tokens e adiciona segundos; subagentes só valem para tarefas estreitas e autocontidas (ex.: deep research) ou hand-off real para agentes com compliance próprio (farmácia, financeiro).", "Regra de colocação prompt vs skill: instruções relevantes a ≥1/3 do tráfego vão no system prompt (ex.: busca de produtos); o resto em skills; regras críticas de segurança/legal/marca e fatos do usuário (ex.: alergias) sempre no prompt; skills previsíveis por sinal (página de origem) devem ser injetadas pelo harness antes da primeira chamada, poupando um turno.", "Ferramentas devem chamar os sistemas core existentes (busca/ranking, carrinho, inventário, promoções) em vez de reimplementá-los — o limite da tool é onde a lógica deles termina e o julgamento do modelo começa; resultados de tool são contexto: retornar só os campos que o modelo usa (URLs de imagem por linha de busca são o ofensor comum) e usar instruções de erro em vez de códigos genéricos.", "UI como tool: o modelo chama present_products/present_itinerary com argumentos tipados, o servidor valida/enriquece e o cliente renderiza; por estarem no formato nativo de messages, preservam histórico sem re-parse e dão ao agente o registro do que está na tela ('o primeiro hotel') — os argumentos devem espelhar o layout renderizado; eager_input_streaming:true devolve streaming em nível de token ao custo da garantia de schema no servidor.", "Latência de conclusão = Σ por turno (time-to-last-token + processamento de tool); alavancas: menos turnos (contexto pré-carregado, modelos mais inteligentes que planejam melhor, chamadas paralelas de tools independentes), tools mais rápidos e tokens mais rápidos — minimizar a soma; qualidade do resultado move retenção/carrinho mais que ganhos marginais de latência, então gerenciar também a latência percebida."]
entities: ["Anthropic", "Claude", "Claude Sonnet"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://claude.com/blog/the-anatomy-of-effective-commerce-agents"]
media: []
---

# Arquitetura de agentes de comércio com Claude

**@ClaudeDevs** · [2095233746366808420](https://x.com/ClaudeDevs/status/2095233746366808420) · `resource`

## Resumo
Guia da Anthropic sobre agentes de e-commerce em produção com Claude: um agente único com skills (em vez de subagentes por domínio), ferramentas construídas sobre sistemas core, UI-como-tool e práticas de latência e evals. Deployments enterprise reportam carrinhos até 35% maiores e 60% mais compras concluídas.

## Pontos-chave
- Agente único com skills supera consistentemente tanto o design one-prompt-for-everything quanto subagente-por-domínio em qualidade, muitas vezes com menor custo e latência: cada handoff é state-lossy, multiplica tokens e adiciona segundos; subagentes só valem para tarefas estreitas e autocontidas (ex.: deep research) ou hand-off real para agentes com compliance próprio (farmácia, financeiro).
- Regra de colocação prompt vs skill: instruções relevantes a ≥1/3 do tráfego vão no system prompt (ex.: busca de produtos); o resto em skills; regras críticas de segurança/legal/marca e fatos do usuário (ex.: alergias) sempre no prompt; skills previsíveis por sinal (página de origem) devem ser injetadas pelo harness antes da primeira chamada, poupando um turno.
- Ferramentas devem chamar os sistemas core existentes (busca/ranking, carrinho, inventário, promoções) em vez de reimplementá-los — o limite da tool é onde a lógica deles termina e o julgamento do modelo começa; resultados de tool são contexto: retornar só os campos que o modelo usa (URLs de imagem por linha de busca são o ofensor comum) e usar instruções de erro em vez de códigos genéricos.
- UI como tool: o modelo chama present_products/present_itinerary com argumentos tipados, o servidor valida/enriquece e o cliente renderiza; por estarem no formato nativo de messages, preservam histórico sem re-parse e dão ao agente o registro do que está na tela ('o primeiro hotel') — os argumentos devem espelhar o layout renderizado; eager_input_streaming:true devolve streaming em nível de token ao custo da garantia de schema no servidor.
- Latência de conclusão = Σ por turno (time-to-last-token + processamento de tool); alavancas: menos turnos (contexto pré-carregado, modelos mais inteligentes que planejam melhor, chamadas paralelas de tools independentes), tools mais rápidos e tokens mais rápidos — minimizar a soma; qualidade do resultado move retenção/carrinho mais que ganhos marginais de latência, então gerenciar também a latência percebida.

## Links
- https://claude.com/blog/the-anatomy-of-effective-commerce-agents

## Entidades
Anthropic, Claude, Claude Sonnet

> **Revisit:** `high` · **fonte:** `article`
