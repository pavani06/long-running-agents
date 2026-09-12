---
title: "Introducing Managed Deep Agents | Interrupt 26"
type: "extract"
source: "youtube"
video_id: "LdQpoK2TzSo"
url: "https://www.youtube.com/watch?v=LdQpoK2TzSo"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-introducing-managed-deep-agents-interrupt-26--LdQpoK2TzSo.txt]]"
tags: ["agents", "harness", "harness-engineering", "agent-loop", "context-engineering", "context-management", "memory-architecture", "token-budgeting", "multi-agent", "agent-fleets", "model-selection", "gate-design", "permissions", "governanca", "runtime", "state", "error-handling", "production", "agent-tooling"]
thesis: "LangChain apresenta 'Managed Deep Agents' em beta privado: um harness de agentes com ambiente de execução, gestão de contexto, delegação via sub-agentes e human-in-the-loop, empacotado com runtime durável, versionamento de contexto no Context Hub e sandboxes seguras para levar agentes complexos à produção."
concepts: ["Agente como loop modelo + tool-calling", "Harness como tudo que conecta o modelo ao mundo real (skills, memória, prompt de sistema, tools, sub-agentes, contexto)", "Trabalho do harness: contexto certo na hora certa", "Ambiente de execução baseado em file system (scratch files, memórias persistentes, invocação de skills)", "Sandbox e code interpreter para resolução criativa de problemas", "Context offloading: evicção periódica de mensagens grandes para evitar overflow", "Summarization disparada quando o histórico se aproxima do limite de contexto", "Memória de curto e longo prazo como contexto que muda entre execuções", "Prompt caching provider-agnostic para agentes de longa duração", "Skills com progressive disclosure: metadados mínimos no system prompt, recursos completos carregados dinamicamente", "Planning tool para organizar tarefas complexas", "Sub-agentes com contexto isolado que retornam resultado enxuto ao agente principal", "Paralelização via sub-agentes", "Matching de modelo à complexidade da tarefa (mix de providers entre agente principal e sub-agentes)", "Middleware: hooks ao redor do agent loop para lógica customizada, código determinístico, policy enforcement (ex.: redução de PII) e controle dinâmico de modelo/tools em runtime", "Quatro padrões de decisão human-in-the-loop: approve, edit, reject, respond", "Durable execution: checkpoint de cada passo, resume/retry parcial, replay e fork de qualquer ponto do tempo", "Await indefinido de input humano habilitando agentes ambientes", "Três camadas de auth: inbound do usuário, outbound para tools/MCP com assunção de permissões em runtime, RBAC admin para criação/edição de agentes", "Interoperabilidade: remote graph (chamar agente em uma linha de outro app LangGraph) e protocolo A2A", "Versionamento e promoção staging→production de AGENT.md, skills e memórias no Context Hub", "Loop de melhoria contínua a partir de uso real de produção (LangSmith Engine)", "Quase todo agente está se tornando um agente de código; sandbox com OAuth proxy que injeta credenciais em runtime sem expor variáveis de ambiente", "Snapshot e restore da sandbox para garantir ambiente de execução correto", "Casos de uso prontos: double texting, cancelamento de run em execução, task queue e scaling horizontal para tráfego bursty"]
tools: ["Deep Agents", "Managed Deep Agents (beta privado)", "LangGraph / LangGraph Deployment", "LangSmith Engine", "Context Hub", "LangSmith Sandboxes", "Ollama", "Fireworks", "Nvidia", "OpenRouter", "B10", "CopilotKit", "Assistant UI", "A2A protocol", "MCP", "AGENT.md"]
people: ["Sydney (engenheira open source, LangChain)", "Victor (product manager)", "Harrison (keynote)", "LangChain", "Anthropic", "OpenAI", "Google"]
claims: ["Modele um agente como modelo + harness, onde o trabalho do harness é entregar o contexto certo na hora certa para a tarefa.", "Use file system como espinha dorsal do ambiente de execução do agente: scratch files, memórias quentes e invocação de skills passam por ele.", "Evite overflow de contexto combinando evicção periódica de mensagens grandes (offloading) com summarization disparada perto do limite do modelo.", "Adote progressive disclosure para skills: metadados mínimos no system prompt e carregamento completo sob demanda do agente.", "Trate memória como o contexto mais importante porque é o que muda entre execuções e permite melhoria do agente ao longo do tempo.", "Use sub-agentes com contexto isolado para evitar poluir a janela de contexto principal: eles iniciam com contexto fresco e devolvem apenas o resultado final.", "Paralelize tarefas complexas via sub-agentes e casse capacidade do modelo com a complexidade de cada sub-tarefa (providers e modelos distintos).", "Implemente human-in-the-loop com quatro padrões de decisão explícitos: approve, edit, reject e respond (para desbloquear o agente).", "Adicione middleware (hooks ao redor do agent loop) para lógica de negócio, código determinístico, enforcement de política (ex.: PII) e troca dinâmica de modelo/tools em runtime.", "Use checkpointing durável por passo para poder retomar do ponto de falha (ex.: passo 49 de 50) em vez de reiniciar a run inteira.", "Aproveite replay e fork de estados checkpoints para workflows avançados e para aguardar input humano indefinidamente (agentes ambientes).", "Planeje três camadas de autenticação: inbound do usuário, outbound para tools/MCP com permissões assumidas em runtime, e RBAC para quem cria/edita agentes.", "Exponha agentes via remote graph (invocação em uma linha a partir de outras aplicações) e suporte A2A para comunicação agente-a-agente.", "Versione AGENT.md, skills e memórias com promoção controlada entre ambientes (staging→production) e reutilize skills entre agentes.", "Feche o loop de melhoria consumindo uso real de produção para ajustar prompts, sistema e skills continuamente.", "Dê a agentes ferramentas de execução de código em sandbox segura, com OAuth proxy injetando credenciais em runtime (sem expor env vars ao agente) e snapshot/restore do ambiente.", "Considere que quase todo agente tende a se tornar um coding agent, mesmo casos de uso de pesquisa.", "Cubra tráfego bursty com task queue purpose-built e scaling horizontal, e resolva casos difíceis (double texting, cancelar run em execução) com primitivas de runtime prontas."]
deep_dive: "medium"
deep_dive_reason: "Boa densidade arquitetural sobre harness, gestão de contexto, HITL e primitivas de produção (checkpoints, camadas de auth, OAuth proxy), mas é essencialmente um lançamento de produto em beta privado que ressintetiza padrões já estabelecidos sem novidade técnica profunda."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-deep-agents-explained--GbzEDgcuGJU|Deep Agents Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-lifecycle-build-test-deploy-monitor-interrupt-26--jWy39wavbjY|The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-ai-agents-need-less-code-than-you-think--YqjR4vQwbTc|The best AI agents need less code than you think]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-s-applied-ai-team-on-the-evolution-of-agentic-surfaces--K0X9QDRkIdg|Anthropic's Applied AI team on the Evolution of Agentic Surfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-what-will-interrupt-2027-look-like-interrupt-26--R9K2574YEAg|The Future of AI Agents: What Will Interrupt 2027 Look Like? | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-get-to-production-faster-with-claude-managed-agents--zenIB7XLZxQ|How to get to production faster with Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-dynamic-subagents-how-to-run-parallel-agents-reliably-in-deep-agents--5AkdMangfNk|Dynamic Subagents: How to Run Parallel Agents Reliably in Deep Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-ship-your-first-managed-agent--19HDQ9HppOA|Ship your first Managed Agent]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-for-your-agent--VKFKyrrK-Iw|The Agent for Your Agent.]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-solved-context-management-in-agents-sally-ann-delucia--esY99nYXxR4|How we solved Context Management in Agents — Sally-Ann Delucia]]", "[[extracts/youtube/ai-learning/2026-09-11-wtf-is-loop-engineer-how-to-setup-for-real--W6x-hb44C0c|wtf is Loop Engineer & how to setup for real]]", "[[extracts/youtube/ai-learning/2026-09-11-unlock-autonomous-ai-agents-with-auth-md-michael-grinich-mcp-night-agent-mode-ke--Dqp_b8GHLXU|Unlock Autonomous AI Agents with auth.md, Michael Grinich | MCP Night: Agent Mode Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-this-ai-agent-can-do-basically-everything-agent-zero--kTs3kDlKc8w|This AI Agent can do basically everything - Agent Zero]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-use-rlms-in-deep-agents--5_LLMZfKI6w|How to use RLMs in Deep Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-getting-started-with-omnigent-the-coding-agent-meta-harness--AyV0hum_hA8|Getting Started with Omnigent | The Coding Agent Meta-Harness]]", "[[extracts/youtube/ai-learning/2026-09-11-pi-architecture-explained-agent-loop-tools-tui-and-more--gTeujlv8qK0|PI Architecture EXPLAINED | Agent Loop, Tools, TUI and More]]"]
theme: "Arquiteturas de Deep Agents"
---

# Introducing Managed Deep Agents | Interrupt 26

## Tese
LangChain apresenta 'Managed Deep Agents' em beta privado: um harness de agentes com ambiente de execução, gestão de contexto, delegação via sub-agentes e human-in-the-loop, empacotado com runtime durável, versionamento de contexto no Context Hub e sandboxes seguras para levar agentes complexos à produção.

## Conceitos-chave
- Agente como loop modelo + tool-calling
- Harness como tudo que conecta o modelo ao mundo real (skills, memória, prompt de sistema, tools, sub-agentes, contexto)
- Trabalho do harness: contexto certo na hora certa
- Ambiente de execução baseado em file system (scratch files, memórias persistentes, invocação de skills)
- Sandbox e code interpreter para resolução criativa de problemas
- Context offloading: evicção periódica de mensagens grandes para evitar overflow
- Summarization disparada quando o histórico se aproxima do limite de contexto
- Memória de curto e longo prazo como contexto que muda entre execuções
- Prompt caching provider-agnostic para agentes de longa duração
- Skills com progressive disclosure: metadados mínimos no system prompt, recursos completos carregados dinamicamente
- Planning tool para organizar tarefas complexas
- Sub-agentes com contexto isolado que retornam resultado enxuto ao agente principal
- Paralelização via sub-agentes
- Matching de modelo à complexidade da tarefa (mix de providers entre agente principal e sub-agentes)
- Middleware: hooks ao redor do agent loop para lógica customizada, código determinístico, policy enforcement (ex.: redução de PII) e controle dinâmico de modelo/tools em runtime
- Quatro padrões de decisão human-in-the-loop: approve, edit, reject, respond
- Durable execution: checkpoint de cada passo, resume/retry parcial, replay e fork de qualquer ponto do tempo
- Await indefinido de input humano habilitando agentes ambientes
- Três camadas de auth: inbound do usuário, outbound para tools/MCP com assunção de permissões em runtime, RBAC admin para criação/edição de agentes
- Interoperabilidade: remote graph (chamar agente em uma linha de outro app LangGraph) e protocolo A2A
- Versionamento e promoção staging→production de AGENT.md, skills e memórias no Context Hub
- Loop de melhoria contínua a partir de uso real de produção (LangSmith Engine)
- Quase todo agente está se tornando um agente de código; sandbox com OAuth proxy que injeta credenciais em runtime sem expor variáveis de ambiente
- Snapshot e restore da sandbox para garantir ambiente de execução correto
- Casos de uso prontos: double texting, cancelamento de run em execução, task queue e scaling horizontal para tráfego bursty

## Ferramentas & pessoas
**Ferramentas:** Deep Agents, Managed Deep Agents (beta privado), LangGraph / LangGraph Deployment, LangSmith Engine, Context Hub, LangSmith Sandboxes, Ollama, Fireworks, Nvidia, OpenRouter, B10, CopilotKit, Assistant UI, A2A protocol, MCP, AGENT.md

**Pessoas/orgs:** Sydney (engenheira open source, LangChain), Victor (product manager), Harrison (keynote), LangChain, Anthropic, OpenAI, Google

## Claims acionáveis
- Modele um agente como modelo + harness, onde o trabalho do harness é entregar o contexto certo na hora certa para a tarefa.
- Use file system como espinha dorsal do ambiente de execução do agente: scratch files, memórias quentes e invocação de skills passam por ele.
- Evite overflow de contexto combinando evicção periódica de mensagens grandes (offloading) com summarization disparada perto do limite do modelo.
- Adote progressive disclosure para skills: metadados mínimos no system prompt e carregamento completo sob demanda do agente.
- Trate memória como o contexto mais importante porque é o que muda entre execuções e permite melhoria do agente ao longo do tempo.
- Use sub-agentes com contexto isolado para evitar poluir a janela de contexto principal: eles iniciam com contexto fresco e devolvem apenas o resultado final.
- Paralelize tarefas complexas via sub-agentes e casse capacidade do modelo com a complexidade de cada sub-tarefa (providers e modelos distintos).
- Implemente human-in-the-loop com quatro padrões de decisão explícitos: approve, edit, reject e respond (para desbloquear o agente).
- Adicione middleware (hooks ao redor do agent loop) para lógica de negócio, código determinístico, enforcement de política (ex.: PII) e troca dinâmica de modelo/tools em runtime.
- Use checkpointing durável por passo para poder retomar do ponto de falha (ex.: passo 49 de 50) em vez de reiniciar a run inteira.
- Aproveite replay e fork de estados checkpoints para workflows avançados e para aguardar input humano indefinidamente (agentes ambientes).
- Planeje três camadas de autenticação: inbound do usuário, outbound para tools/MCP com permissões assumidas em runtime, e RBAC para quem cria/edita agentes.
- Exponha agentes via remote graph (invocação em uma linha a partir de outras aplicações) e suporte A2A para comunicação agente-a-agente.
- Versione AGENT.md, skills e memórias com promoção controlada entre ambientes (staging→production) e reutilize skills entre agentes.
- Feche o loop de melhoria consumindo uso real de produção para ajustar prompts, sistema e skills continuamente.
- Dê a agentes ferramentas de execução de código em sandbox segura, com OAuth proxy injetando credenciais em runtime (sem expor env vars ao agente) e snapshot/restore do ambiente.
- Considere que quase todo agente tende a se tornar um coding agent, mesmo casos de uso de pesquisa.
- Cubra tráfego bursty com task queue purpose-built e scaling horizontal, e resolva casos difíceis (double texting, cancelar run em execução) com primitivas de runtime prontas.

> **Deep dive:** `medium` — Boa densidade arquitetural sobre harness, gestão de contexto, HITL e primitivas de produção (checkpoints, camadas de auth, OAuth proxy), mas é essencialmente um lançamento de produto em beta privado que ressintetiza padrões já estabelecidos sem novidade técnica profunda.
