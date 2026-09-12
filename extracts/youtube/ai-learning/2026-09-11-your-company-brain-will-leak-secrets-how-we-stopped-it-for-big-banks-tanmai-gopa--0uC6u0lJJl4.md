---
title: "Your company brain will leak secrets: how we stopped it for big banks — Tanmai Gopal, PromptQL"
type: "extract"
source: "youtube"
video_id: "0uC6u0lJJl4"
url: "https://www.youtube.com/watch?v=0uC6u0lJJl4"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-your-company-brain-will-leak-secrets-how-we-stopped-it-for-big-banks-tanmai-gopa--0uC6u0lJJl4.txt]]"
tags: ["context-engineering", "knowledge-management", "memory-architecture", "permissions", "governanca", "gate-design", "agents", "agent-tooling", "arquitetura", "escalation"]
thesis: "Um 'cérebro da empresa' seguro para agentes de codificação exige uma wiki única com escopos por arquivo, adições de memória apenas sugeridas pelo agente e aceitas por um humano nomeado, e execução de ferramentas sempre com as credenciais do usuário injetadas nas camadas HTTP/SQL — nunca armazenadas no sandbox."
concepts: ["company brain como wiki compartilhada + regras de acesso para coding agents", "grow vs. build: crescimento orgânico do brain por auto-serviço de cada pessoa", "escopos de leitura/escrita por arquivo da wiki", "sugestão de memória pelo agente com gate humano de aceitar/rejeitar", "atribuição de toda mudança a um humano nomeado (accountability)", "leitura de contexto com credenciais/claims do usuário em cada interação", "injeção de credenciais do usuário nas camadas HTTP e SQL", "anti-pattern de silos: team brains e memória per-channel", "multiplayer/shared AI e escalation de privilégios", "updates diários crescentes como métrica de saúde do brain", "coding agents como arquitetura geral para problemas de propósito geral"]
tools: ["PromptQL (PromQL)", "Hasura GraphQL Engine", "Claude Code", "Claude Cowork", "Codex app", "Claude Tag (claw tag)", "Hermes", "OpenClaw", "Slack", "GitHub (markdown)", "OpenTelemetry", "GLM", "GPT", "Claude Opus 4.5"]
people: ["Tanmai (cofundador da PromptQL/Hasura)", "Hasura", "Apple", "Meta", "JP Morgan", "Instacart", "StitchFix"]
claims: ["Uma company brain saudável mostra número crescente de updates diários, porque as pessoas ensinam mais conforme o sistema passa a funcionar", "Não deixe o agente auto-adicionar memória: ele deve sugerir a mudança com escopos e um humano aceita ou rejeita", "Todo contexto deve ir para uma única wiki company-wide; recuse silos de team-brain e memória per-channel de agentes em Slack", "Toda mudança na wiki deve ser atribuída a um humano nomeado (nunca 'o agente adicionou'), permitindo accountability e ação remedial", "Cada página/arquivo da wiki recebe escopos de read/write definidos no momento da adição", "O agente deve ler o contexto usando sempre as credenciais/claims do usuário que está interagindo", "Nunca armazene credenciais no sandbox do agente; injete as credenciais do usuário nas camadas HTTP e SQL durante a execução de ferramentas para o agir-como-o-humano", "Quem adiciona uma ferramenta controla quem acessa essa ferramenta; virtualize/proxie todas as interações com dados reais", "Não dá para construir top-down o brain de uma organização centenária; cada pessoa deve self-serve sua parte (grow, not build)", "Pessoas não escrevem shared skills no GitHub para desconhecidos usarem no futuro; esse modelo de contribuição falha", "Colaboração multi-pessoa com agentes gera o contexto de maior qualidade (ex.: argumentos em threads de Slack revelando decisões técnicas não documentadas), mas é onde o risco de escalation de privilégios é maior", "Coding agents como Claude Code, Cowork e o app Codex compartilham a mesma arquitetura de resolver problemas gerais, e é para esse paradigma que o brain deve ser construído"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight arquitetural acionável e relativamente novo (wiki única com escopos, gate humano para memória, injeção de credenciais do usuário em HTTP/SQL), diretamente relevante a context-engineering, permissions e governança de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-every-company-should-have-a-brain-garry-tan-y-combinator--eBUyTS7SzV4|Every company should have a Brain — Garry Tan, Y Combinator]]", "[[extracts/youtube/ai-learning/2026-09-11-from-coding-to-knowledge-work-agents-karan-vaidya-composio--xxfMT-bPEmU|From coding to Knowledge work agents — Karan Vaidya, Composio]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-openwiki-brains-general-purpose-memory-for-agents--sBg90v2qfas|OpenWiki Brains, general-purpose memory for agents]]"]
---

# Your company brain will leak secrets: how we stopped it for big banks — Tanmai Gopal, PromptQL

## Tese
Um 'cérebro da empresa' seguro para agentes de codificação exige uma wiki única com escopos por arquivo, adições de memória apenas sugeridas pelo agente e aceitas por um humano nomeado, e execução de ferramentas sempre com as credenciais do usuário injetadas nas camadas HTTP/SQL — nunca armazenadas no sandbox.

## Conceitos-chave
- company brain como wiki compartilhada + regras de acesso para coding agents
- grow vs. build: crescimento orgânico do brain por auto-serviço de cada pessoa
- escopos de leitura/escrita por arquivo da wiki
- sugestão de memória pelo agente com gate humano de aceitar/rejeitar
- atribuição de toda mudança a um humano nomeado (accountability)
- leitura de contexto com credenciais/claims do usuário em cada interação
- injeção de credenciais do usuário nas camadas HTTP e SQL
- anti-pattern de silos: team brains e memória per-channel
- multiplayer/shared AI e escalation de privilégios
- updates diários crescentes como métrica de saúde do brain
- coding agents como arquitetura geral para problemas de propósito geral

## Ferramentas & pessoas
**Ferramentas:** PromptQL (PromQL), Hasura GraphQL Engine, Claude Code, Claude Cowork, Codex app, Claude Tag (claw tag), Hermes, OpenClaw, Slack, GitHub (markdown), OpenTelemetry, GLM, GPT, Claude Opus 4.5

**Pessoas/orgs:** Tanmai (cofundador da PromptQL/Hasura), Hasura, Apple, Meta, JP Morgan, Instacart, StitchFix

## Claims acionáveis
- Uma company brain saudável mostra número crescente de updates diários, porque as pessoas ensinam mais conforme o sistema passa a funcionar
- Não deixe o agente auto-adicionar memória: ele deve sugerir a mudança com escopos e um humano aceita ou rejeita
- Todo contexto deve ir para uma única wiki company-wide; recuse silos de team-brain e memória per-channel de agentes em Slack
- Toda mudança na wiki deve ser atribuída a um humano nomeado (nunca 'o agente adicionou'), permitindo accountability e ação remedial
- Cada página/arquivo da wiki recebe escopos de read/write definidos no momento da adição
- O agente deve ler o contexto usando sempre as credenciais/claims do usuário que está interagindo
- Nunca armazene credenciais no sandbox do agente; injete as credenciais do usuário nas camadas HTTP e SQL durante a execução de ferramentas para o agir-como-o-humano
- Quem adiciona uma ferramenta controla quem acessa essa ferramenta; virtualize/proxie todas as interações com dados reais
- Não dá para construir top-down o brain de uma organização centenária; cada pessoa deve self-serve sua parte (grow, not build)
- Pessoas não escrevem shared skills no GitHub para desconhecidos usarem no futuro; esse modelo de contribuição falha
- Colaboração multi-pessoa com agentes gera o contexto de maior qualidade (ex.: argumentos em threads de Slack revelando decisões técnicas não documentadas), mas é onde o risco de escalation de privilégios é maior
- Coding agents como Claude Code, Cowork e o app Codex compartilham a mesma arquitetura de resolver problemas gerais, e é para esse paradigma que o brain deve ser construído

> **Deep dive:** `high` — Alta densidade de insight arquitetural acionável e relativamente novo (wiki única com escopos, gate humano para memória, injeção de credenciais do usuário em HTTP/SQL), diretamente relevante a context-engineering, permissions e governança de agentes.
