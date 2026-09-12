---
title: "Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline"
type: "extract"
source: "youtube"
video_id: "Uny6LpmjraI"
url: "https://www.youtube.com/watch?v=Uny6LpmjraI"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipeline--Uny6LpmjraI.txt]]"
tags: ["agents", "agent-tooling", "agentic-coding", "evals", "harness", "harness-engineering", "data-platform", "tracing", "telemetry", "observability", "production", "multi-agent", "arquitetura", "stack-tooling", "context-engineering"]
thesis: "A Clay opera agentes em escala massiva (Claygent com 300M+ execuções/mês, Sculptor com 100K+ mensagens/semana) sustentando-os em três pilares: uma filosofia de evals em camadas (local barato, staging espelhando produção, online com métricas objetivas e juízes LLM), um flywheel em que agentes internos e externos compartilham as mesmas ferramentas via CLI/API, e uma fundação unificada de dados (data lake) com agentes como usuários de primeira classe."
concepts: ["Evals em múltiplos níveis (local sem sandbox, CI/staging igual ao harness de produção)", "Cobertura de evals em matriz determinístico/não-determinístico × offline/online", "Goldens, structured eval checks e trajectory/tool assertions", "Evals multi-turn determinísticos vs. usuário simulado por agente", "LLM-as-a-judge e avaliadores percebidos (pushback do usuário)", "Eval drift: data drift, judge drift e overfitting em pequenos eval sets", "Loop de aprendizado: sinais de produção alimentando evals offline", "Flywheel de ferramentas compartilhadas entre agentes internos e externos", "Data lake unificando dados de primeira e terceira parte", "Agentes como usuários de primeira classe do data platform", "Shadow builds seguros com separação de compute de serving e desenvolvimento", "Passos de execução longos (1-2 horas) sobre dados em escala", "Uso de classificadores de use case para verificar cobertura de evals"]
tools: ["Clay", "Claygent", "Sculptor", "Sculptor for Search", "LangChain", "Claude", "Codex", "Devin", "Amazon S3", "AWS Athena", "Snowflake", "PostgreSQL", "ClickHouse", "CLI da Clay", "API pública da Clay", "NPS", "fable (modelo)"]
people: ["Clay", "Jeff", "Vishu", "Souch", "LangChain"]
claims: ["Evals locais devem ser baratos e rápidos, sem sandbox ou VFS, enquanto tudo que roda em CI/staging deve ser o mais próximo possível do harness de produção", "Fazer o eval suite rodar via linha de comando no ambiente do desenvolvedor elimina fricção e evita provisionar infraestrutura por experimento", "Com um bom eval suite é seguro deixar agentes de codificação (Claude, Codex, Devin) fazerem mudanças de prompt sem quebrar produção", "Goldens funcionam para casos simples mas quebram em queries complexas; structured checks que avaliam apenas as partes relevantes são mais resilientes", "Multi-turn evals determinísticos (turnos de usuário hardcoded) foram mais úteis na prática do que usuários simulados por LLM, que eram ruidosos e exigiam manutenção própria", "O maior desafio não resolvido em evals de agentes é o feedback loop: levar aprendizados de produção de volta para os evals offline", "Hill climbing sobre um único LLM judge ou um eval set pequeno causa overfitting do prompt aos exemplos", "Contramedidas para drift incluem: exemplos de avaliadores online, tickets de suporte como sinal de alta qualidade, goldens anotados por humanos e tagging de use cases", "Expor exatamente as mesmas ferramentas para agentes internos (via harness) e externos (via CLI/API) cria um flywheel em que falhas de trajetória melhoram tanto o harness quanto as ferramentas", "Migrar para arquitetura de data lake com agentes como usuários de primeira classe exige guardrails antecipados e shadow builds seguros", "Separar compute de serving e desenvolvimento permite que agentes criem e deployem novos modelos de dados em S3 sem derrubar produção", "Passos longos (1-2 horas) orquestrando grandes volumes via Athena agora são viáveis, permitindo agentes com objetivos de longo prazo sobre dados", "Modelos com contexto grande (ex.: 'fable') permitiram, pela primeira vez, alimentar ~10.000 exemplos no contexto para encontrar tendências, mudando de análise 'vibe-based' para análise em escala", "Unificar fontes dispersas (traces no LangChain, Snowflake, Postgres, ClickHouse) em uma única plataforma amplia o que agentes conseguem fazer autonomamente"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de práticas acionáveis em evals por camadas, harness extensível, drift de evals/juízes, flywheel de ferramentas compartilhadas e data platform centrada em agentes, com novidade e relevância direta a harness, evals e arquitetura de dados para frotas de agentes em produção."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-lifecycle-build-test-deploy-monitor-interrupt-26--jWy39wavbjY|The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-how-founders-build-on-claude-managed-agents--hm8NzEd5io0|How founders build on Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-ai-agents-need-less-code-than-you-think--YqjR4vQwbTc|The best AI agents need less code than you think]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-the-maturity-phases-of-running-evals-phil-hetzel-braintrust--FB-MLPhL9Ms|The maturity phases of running evals — Phil Hetzel, Braintrust]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-how-uber-built-ai-agents-that-save-21-000-developer-hours-with-langgraph-langcha--Bugs0dVcNI8|How Uber Built AI Agents That Save 21,000 Developer Hours with LangGraph | LangChain Interrupt]]", "[[extracts/youtube/ai-learning/2026-09-11-dynamic-subagents-how-to-run-parallel-agents-reliably-in-deep-agents--5AkdMangfNk|Dynamic Subagents: How to Run Parallel Agents Reliably in Deep Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-how-lovable-self-improves-every-hour-benjamin-verbeek-lovable--KA5kPbdkK2E|How Lovable self-improves every hour — Benjamin Verbeek, Lovable]]", "[[extracts/youtube/ai-learning/2026-09-11-building-closed-loop-evals-for-a-multimodal-agent-at-scale-soumya-gupta-jai-chop--31GUkCBD-Uc|Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-for-your-agent--VKFKyrrK-Iw|The Agent for Your Agent.]]"]
theme: "Arquiteturas de Deep Agents"
---

# Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline

## Tese
A Clay opera agentes em escala massiva (Claygent com 300M+ execuções/mês, Sculptor com 100K+ mensagens/semana) sustentando-os em três pilares: uma filosofia de evals em camadas (local barato, staging espelhando produção, online com métricas objetivas e juízes LLM), um flywheel em que agentes internos e externos compartilham as mesmas ferramentas via CLI/API, e uma fundação unificada de dados (data lake) com agentes como usuários de primeira classe.

## Conceitos-chave
- Evals em múltiplos níveis (local sem sandbox, CI/staging igual ao harness de produção)
- Cobertura de evals em matriz determinístico/não-determinístico × offline/online
- Goldens, structured eval checks e trajectory/tool assertions
- Evals multi-turn determinísticos vs. usuário simulado por agente
- LLM-as-a-judge e avaliadores percebidos (pushback do usuário)
- Eval drift: data drift, judge drift e overfitting em pequenos eval sets
- Loop de aprendizado: sinais de produção alimentando evals offline
- Flywheel de ferramentas compartilhadas entre agentes internos e externos
- Data lake unificando dados de primeira e terceira parte
- Agentes como usuários de primeira classe do data platform
- Shadow builds seguros com separação de compute de serving e desenvolvimento
- Passos de execução longos (1-2 horas) sobre dados em escala
- Uso de classificadores de use case para verificar cobertura de evals

## Ferramentas & pessoas
**Ferramentas:** Clay, Claygent, Sculptor, Sculptor for Search, LangChain, Claude, Codex, Devin, Amazon S3, AWS Athena, Snowflake, PostgreSQL, ClickHouse, CLI da Clay, API pública da Clay, NPS, fable (modelo)

**Pessoas/orgs:** Clay, Jeff, Vishu, Souch, LangChain

## Claims acionáveis
- Evals locais devem ser baratos e rápidos, sem sandbox ou VFS, enquanto tudo que roda em CI/staging deve ser o mais próximo possível do harness de produção
- Fazer o eval suite rodar via linha de comando no ambiente do desenvolvedor elimina fricção e evita provisionar infraestrutura por experimento
- Com um bom eval suite é seguro deixar agentes de codificação (Claude, Codex, Devin) fazerem mudanças de prompt sem quebrar produção
- Goldens funcionam para casos simples mas quebram em queries complexas; structured checks que avaliam apenas as partes relevantes são mais resilientes
- Multi-turn evals determinísticos (turnos de usuário hardcoded) foram mais úteis na prática do que usuários simulados por LLM, que eram ruidosos e exigiam manutenção própria
- O maior desafio não resolvido em evals de agentes é o feedback loop: levar aprendizados de produção de volta para os evals offline
- Hill climbing sobre um único LLM judge ou um eval set pequeno causa overfitting do prompt aos exemplos
- Contramedidas para drift incluem: exemplos de avaliadores online, tickets de suporte como sinal de alta qualidade, goldens anotados por humanos e tagging de use cases
- Expor exatamente as mesmas ferramentas para agentes internos (via harness) e externos (via CLI/API) cria um flywheel em que falhas de trajetória melhoram tanto o harness quanto as ferramentas
- Migrar para arquitetura de data lake com agentes como usuários de primeira classe exige guardrails antecipados e shadow builds seguros
- Separar compute de serving e desenvolvimento permite que agentes criem e deployem novos modelos de dados em S3 sem derrubar produção
- Passos longos (1-2 horas) orquestrando grandes volumes via Athena agora são viáveis, permitindo agentes com objetivos de longo prazo sobre dados
- Modelos com contexto grande (ex.: 'fable') permitiram, pela primeira vez, alimentar ~10.000 exemplos no contexto para encontrar tendências, mudando de análise 'vibe-based' para análise em escala
- Unificar fontes dispersas (traces no LangChain, Snowflake, Postgres, ClickHouse) em uma única plataforma amplia o que agentes conseguem fazer autonomamente

> **Deep dive:** `high` — Densidade alta de práticas acionáveis em evals por camadas, harness extensível, drift de evals/juízes, flywheel de ferramentas compartilhadas e data platform centrada em agentes, com novidade e relevância direta a harness, evals e arquitetura de dados para frotas de agentes em produção.
