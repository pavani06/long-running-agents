---
title: "Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI"
type: "extract"
source: "youtube"
video_id: "am_oeAoUhew"
url: "https://www.youtube.com/watch?v=am_oeAoUhew"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew.txt]]"
tags: ["harness-engineering", "context-engineering", "agentic-coding", "agent-tooling", "code-review", "testes-qa", "evals", "token-budgeting", "knowledge-management", "arquitetura", "multi-agent", "gate-design", "error-handling", "verification", "process", "stack-tooling", "spec-driven-development"]
thesis: "Com a implementação 'gratuita' (código abundante gerado por agentes), os recursos escassos passam a ser tempo/atenção humana e janela de contexto do modelo, e o papel do engenheiro se torna projetar harnesses — documentação de requisitos não-funcionais, lints customizados, testes estruturais e agentes revisores — que entregam ao agente a instrução certa no momento certo para que ele execute o trabalho completo."
concepts: ["código é gratuito; implementação deixou de ser o gargalo", "recursos escassos: tempo humano, atenção humano+modelo, janela de contexto", "requisitos não-funcionais especificados por escrito como critério de 'trabalho aceitável'", "injeção just-in-time de instruções via lint, teste e agente revisor em vez de frontload no prompt", "agentes revisores por persona (segurança, confiabilidade, QA) disparados a cada push", "centralização de alavancagem em 5–10 skills em vez de milhares", "harnesses de primeira parte pós-treinados junto ao modelo (aproveitar a onda do post-training)", "LLM como compilador fuzzy; código como artefato descartável de compilação da spec", "dia de 'garbage collection' (sexta-feira) para eliminar categoricamente classes de slop", "PR como domínio hub-and-spoke onde agentes e humanos colaboram; agente implementador pode aceitar/deferir/rejeitar feedback", "uniformização do repositório (uma implementação canônica por conceito) para tokens previsíveis", "auto-compaction de contexto; construir assumindo que contexto será paginado para fora", "testes que afirmam a estrutura do próprio código-fonte, não só sintaxe/comportamento", "cada interação humana ('continue') é falha do harness em fornecer contexto suficiente", "orquestração de longo prazo: humano ranqueia métricas de sucesso e fornece orçamento de tokens; agentes trabalham continuamente"]
tools: ["OpenAI Codex", "GPT 5.2", "GPT 5.4", "Claude Code", "OpenCode", "agents.md", "Agent SDK", "ESLint", "PNPM", "Electron", "Chrome DevTools", "Zod", "GitHub", "LLVM", "Cranelift", "Rust", "Kafka", "Slido", "Symfony (orquestrador de agentes citado)", "exec plans"]
people: ["Ryan Leapo", "OpenAI", "Latent Space (podcast)"]
claims: ["Bane o uso de editores pelo time e opere exclusivamente pelos agentes para forçar a disciplina de harness", "Converta cada comentário de code review em falha de contexto documentada no repositório, com injeção automática (lint/teste/revisor) para o agente se autocorrigir", "Escreva lints bespoke ao codebase (ex.: fetch sempre envolto por retry+timeout) para resolver de forma durável classes de falha", "Crie testes que verificam a estrutura do código (arquivos ≤350 linhas, privacidade de pacotes, arestas de dependência, schemas Zod deduplicados) para adaptar o codebase ao limite de contexto", "Escreva mensagens de erro com passos de remediação explícitos — elas são prompts para o modelo", "Centralize em 5–10 skills de alta qualidade e esconda a complexidade do dev environment embaixo delas, com o Codex como ponto de entrada", "Estruture o repositório em muitas pacotes isolados por domínio (~750 no PNPM workspace) para escopar subárvores locais às mudanças", "Padronize o códigobase (uma linguagem, um ORM, um jeito de CI, um helper de concorrência) para tornar os tokens previsíveis independentemente de onde o agente olha", "Deferia instruções para o momento do lint/teste em vez de frontload no prompt, evitando sobrecarregar o agente", "Prefira harnesses de primeira parte (Codex, Claude Code) pois o post-training inclui o harness; plugue-se via SDK/app server para 'surfar' essa alavancagem", "Se usar planos, submeta-os como PR único revisado linha a linha por humano antes da execução; não aprove planos sem ler", "Token spend ~1/3 planejamento/curadoria de tickets/docs, ~1/3 implementação, ~1/3 CI", "Trate código como artefato descartável: a spec/documentação é o ativo durável; trocar de modelo é trocar o backend de geração (LLVM→Cranelift)", "Não exija que todo feedback de review seja endereçado — evite o agente ser 'intimidado' por revisores; vies para código aceito, não perfeito", "Ao começar, use agentes primeiro para aumentar confiança no código existente (mais testes) e para automatizar onde seu tempo é gasto", "Bucket o feedback de review por persona e crie um agente revisor por persona por push, com docs do que 'bom' significa", "Aumente paralelismo dos PRs e minimize tempo aberto para reduzir merge conflicts em alta velocidade (3–5 PRs/dia por engenheiro)", "Métrica de maturidade do harness: zero interações humanas; se você digita 'continue', o harness falhou em prover contexto de conclusão"]
deep_dive: "high"
deep_dive_reason: "Praticante de produção em escala extrema entrega densidade alta de técnicas acionáveis e arquiteturais (injeção just-in-time de contexto, loop de eliminação de slop, repositório estruturado para agentes, revisores por persona) diretamente relevantes a harness, context-engineering e evals."
---

# Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI

## Tese
Com a implementação 'gratuita' (código abundante gerado por agentes), os recursos escassos passam a ser tempo/atenção humana e janela de contexto do modelo, e o papel do engenheiro se torna projetar harnesses — documentação de requisitos não-funcionais, lints customizados, testes estruturais e agentes revisores — que entregam ao agente a instrução certa no momento certo para que ele execute o trabalho completo.

## Conceitos-chave
- código é gratuito; implementação deixou de ser o gargalo
- recursos escassos: tempo humano, atenção humano+modelo, janela de contexto
- requisitos não-funcionais especificados por escrito como critério de 'trabalho aceitável'
- injeção just-in-time de instruções via lint, teste e agente revisor em vez de frontload no prompt
- agentes revisores por persona (segurança, confiabilidade, QA) disparados a cada push
- centralização de alavancagem em 5–10 skills em vez de milhares
- harnesses de primeira parte pós-treinados junto ao modelo (aproveitar a onda do post-training)
- LLM como compilador fuzzy; código como artefato descartável de compilação da spec
- dia de 'garbage collection' (sexta-feira) para eliminar categoricamente classes de slop
- PR como domínio hub-and-spoke onde agentes e humanos colaboram; agente implementador pode aceitar/deferir/rejeitar feedback
- uniformização do repositório (uma implementação canônica por conceito) para tokens previsíveis
- auto-compaction de contexto; construir assumindo que contexto será paginado para fora
- testes que afirmam a estrutura do próprio código-fonte, não só sintaxe/comportamento
- cada interação humana ('continue') é falha do harness em fornecer contexto suficiente
- orquestração de longo prazo: humano ranqueia métricas de sucesso e fornece orçamento de tokens; agentes trabalham continuamente

## Ferramentas & pessoas
**Ferramentas:** OpenAI Codex, GPT 5.2, GPT 5.4, Claude Code, OpenCode, agents.md, Agent SDK, ESLint, PNPM, Electron, Chrome DevTools, Zod, GitHub, LLVM, Cranelift, Rust, Kafka, Slido, Symfony (orquestrador de agentes citado), exec plans

**Pessoas/orgs:** Ryan Leapo, OpenAI, Latent Space (podcast)

## Claims acionáveis
- Bane o uso de editores pelo time e opere exclusivamente pelos agentes para forçar a disciplina de harness
- Converta cada comentário de code review em falha de contexto documentada no repositório, com injeção automática (lint/teste/revisor) para o agente se autocorrigir
- Escreva lints bespoke ao codebase (ex.: fetch sempre envolto por retry+timeout) para resolver de forma durável classes de falha
- Crie testes que verificam a estrutura do código (arquivos ≤350 linhas, privacidade de pacotes, arestas de dependência, schemas Zod deduplicados) para adaptar o codebase ao limite de contexto
- Escreva mensagens de erro com passos de remediação explícitos — elas são prompts para o modelo
- Centralize em 5–10 skills de alta qualidade e esconda a complexidade do dev environment embaixo delas, com o Codex como ponto de entrada
- Estruture o repositório em muitas pacotes isolados por domínio (~750 no PNPM workspace) para escopar subárvores locais às mudanças
- Padronize o códigobase (uma linguagem, um ORM, um jeito de CI, um helper de concorrência) para tornar os tokens previsíveis independentemente de onde o agente olha
- Deferia instruções para o momento do lint/teste em vez de frontload no prompt, evitando sobrecarregar o agente
- Prefira harnesses de primeira parte (Codex, Claude Code) pois o post-training inclui o harness; plugue-se via SDK/app server para 'surfar' essa alavancagem
- Se usar planos, submeta-os como PR único revisado linha a linha por humano antes da execução; não aprove planos sem ler
- Token spend ~1/3 planejamento/curadoria de tickets/docs, ~1/3 implementação, ~1/3 CI
- Trate código como artefato descartável: a spec/documentação é o ativo durável; trocar de modelo é trocar o backend de geração (LLVM→Cranelift)
- Não exija que todo feedback de review seja endereçado — evite o agente ser 'intimidado' por revisores; vies para código aceito, não perfeito
- Ao começar, use agentes primeiro para aumentar confiança no código existente (mais testes) e para automatizar onde seu tempo é gasto
- Bucket o feedback de review por persona e crie um agente revisor por persona por push, com docs do que 'bom' significa
- Aumente paralelismo dos PRs e minimize tempo aberto para reduzir merge conflicts em alta velocidade (3–5 PRs/dia por engenheiro)
- Métrica de maturidade do harness: zero interações humanas; se você digita 'continue', o harness falhou em prover contexto de conclusão

> **Deep dive:** `high` — Praticante de produção em escala extrema entrega densidade alta de técnicas acionáveis e arquiteturais (injeção just-in-time de contexto, loop de eliminação de slop, repositório estruturado para agentes, revisores por persona) diretamente relevantes a harness, context-engineering e evals.
