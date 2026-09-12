---
title: "How we solved Context Management in Agents — Sally-Ann Delucia"
type: "extract"
source: "youtube"
video_id: "esY99nYXxR4"
url: "https://www.youtube.com/watch?v=esY99nYXxR4"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-we-solved-context-management-in-agents-sally-ann-delucia--esY99nYXxR4.txt]]"
tags: ["context-engineering", "context-management", "memory-architecture", "evals", "harness", "multi-agent", "observability", "token-budgeting", "agent-tooling", "agents", "arquitetura", "testes-qa"]
thesis: "Agentes de produção falham por causa do contexto, não dos prompts, e a Arise resolveu isso com truncamento inteligente (cabeça+cauda com meio armazenado em memória recuperável), sub-agentes para descarregar tarefas pesadas e evals de sessão longa para detectar falhas tardias."
concepts: ["context engineering vs prompt engineering", "gestão de contexto como problema de produto/UX", "loop vicioso de crescimento de contexto (agente analisando traces/spans)", "truncamento ingênuo e quebra de raciocínio", "summarização via LLM inconsistente", "smart truncation memory (head 100 + tail 100, meio na memória)", "separação entre contexto e memória ('contexto decide o que o modelo vê, memória decide o que sobrevive')", "deduplicação de tool calls mantendo o resultado mais recente", "não resetar o system prompt", "recuperação sob demanda da memória via IDs e previews", "long session evals (carregar 10 turnos, testar o 11º)", "offload de tarefas pesadas para sub-agentes", "agente principal com contexto leve", "memória de longo prazo entre sessões (cross-chat)", "orçamento de contexto e métricas de qualidade de contexto ainda heurísticos", "invalidação de cache de contexto"]
tools: ["Arise (plataforma de observabilidade)", "Alex (AI harness/agente)", "Claude Code", "Cursor", "X/Twitter"]
people: ["Salian (head de produto na Arise)", "Andrej Karpathy", "Arise"]
claims: ["A melhor estratégia de contexto permite ao agente lembrar o que precisa e esquecer o que não precisa", "Engenharia de contexto é escolher estrategicamente o que o modelo vê, não apenas caber no limite de tokens", "Truncamento excessivo quebra o raciocínio: follow-ups passam a parecer novas conversas", "Sumarização por LLM do contexto é inconsistente demais para produção porque não há controle sobre o que é importante", "Manter cabeça e cauda da conversa, truncar o meio e armazená-lo em memória recuperável funciona em produção há meses", "Deduplicar tool calls mantendo apenas o resultado mais recente e nunca resetar o system prompt reduz contexto desperdiçado", "Conversas longas naturais dos usuários fazem falhas aparecerem tarde; evals que carregam 10 turnos e testam o 11º tornam esses bugs testáveis", "Nem todo contexto pertence ao mesmo agente: descarregue tarefas pesadas de dados para sub-agentes e mantenha a conversa principal leve", "Sub-agentes retornam apenas o resultado ao agente principal, que pode ainda buscar contexto adicional na memória", "O padrão recorrente para contextos gigantes (limites de provider) é decompor em mais sub-agentes", "Memória de longo prazo entre sessões ainda é necessária: usuários querem referenciar issues discutidas em chats anteriores", "A seleção de contexto ainda é heurística (primeiros/últimos 100 chars) sem orçamento de contexto principista ou métricas claras de qualidade; evals são usadas como proxy", "O Claude Code usa estratégia similar de truncamento e compressão de contexto", "Agentes não falham por prompts; falham por contexto — e contexto, memória e avaliação são os três pilares"]
deep_dive: "high"
deep_dive_reason: "Apresentação densa de um praticante com técnicas concretas de arquitetura de contexto/memória (smart truncation com memória recuperável), offloading para sub-agentes e protocolo de evals de sessão longa, diretamente relevantes a harness, context-engineering e evals, apesar de leve tom promocional do produto."
---

# How we solved Context Management in Agents — Sally-Ann Delucia

## Tese
Agentes de produção falham por causa do contexto, não dos prompts, e a Arise resolveu isso com truncamento inteligente (cabeça+cauda com meio armazenado em memória recuperável), sub-agentes para descarregar tarefas pesadas e evals de sessão longa para detectar falhas tardias.

## Conceitos-chave
- context engineering vs prompt engineering
- gestão de contexto como problema de produto/UX
- loop vicioso de crescimento de contexto (agente analisando traces/spans)
- truncamento ingênuo e quebra de raciocínio
- summarização via LLM inconsistente
- smart truncation memory (head 100 + tail 100, meio na memória)
- separação entre contexto e memória ('contexto decide o que o modelo vê, memória decide o que sobrevive')
- deduplicação de tool calls mantendo o resultado mais recente
- não resetar o system prompt
- recuperação sob demanda da memória via IDs e previews
- long session evals (carregar 10 turnos, testar o 11º)
- offload de tarefas pesadas para sub-agentes
- agente principal com contexto leve
- memória de longo prazo entre sessões (cross-chat)
- orçamento de contexto e métricas de qualidade de contexto ainda heurísticos
- invalidação de cache de contexto

## Ferramentas & pessoas
**Ferramentas:** Arise (plataforma de observabilidade), Alex (AI harness/agente), Claude Code, Cursor, X/Twitter

**Pessoas/orgs:** Salian (head de produto na Arise), Andrej Karpathy, Arise

## Claims acionáveis
- A melhor estratégia de contexto permite ao agente lembrar o que precisa e esquecer o que não precisa
- Engenharia de contexto é escolher estrategicamente o que o modelo vê, não apenas caber no limite de tokens
- Truncamento excessivo quebra o raciocínio: follow-ups passam a parecer novas conversas
- Sumarização por LLM do contexto é inconsistente demais para produção porque não há controle sobre o que é importante
- Manter cabeça e cauda da conversa, truncar o meio e armazená-lo em memória recuperável funciona em produção há meses
- Deduplicar tool calls mantendo apenas o resultado mais recente e nunca resetar o system prompt reduz contexto desperdiçado
- Conversas longas naturais dos usuários fazem falhas aparecerem tarde; evals que carregam 10 turnos e testam o 11º tornam esses bugs testáveis
- Nem todo contexto pertence ao mesmo agente: descarregue tarefas pesadas de dados para sub-agentes e mantenha a conversa principal leve
- Sub-agentes retornam apenas o resultado ao agente principal, que pode ainda buscar contexto adicional na memória
- O padrão recorrente para contextos gigantes (limites de provider) é decompor em mais sub-agentes
- Memória de longo prazo entre sessões ainda é necessária: usuários querem referenciar issues discutidas em chats anteriores
- A seleção de contexto ainda é heurística (primeiros/últimos 100 chars) sem orçamento de contexto principista ou métricas claras de qualidade; evals são usadas como proxy
- O Claude Code usa estratégia similar de truncamento e compressão de contexto
- Agentes não falham por prompts; falham por contexto — e contexto, memória e avaliação são os três pilares

> **Deep dive:** `high` — Apresentação densa de um praticante com técnicas concretas de arquitetura de contexto/memória (smart truncation com memória recuperável), offloading para sub-agentes e protocolo de evals de sessão longa, diretamente relevantes a harness, context-engineering e evals, apesar de leve tom promocional do produto.
