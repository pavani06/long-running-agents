---
title: "How Uber Runs 60,000 AI Agent Tasks Per Week With MCP"
type: "extract"
source: "youtube"
video_id: "yVqMxBahjfA"
url: "https://www.youtube.com/watch?v=yVqMxBahjfA"
channel: "Agentic AI Foundation"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-uber-runs-60-000-ai-agent-tasks-per-week-with-mcp--yVqMxBahjfA.txt]]"
tags: ["agent-fleets", "agent-tooling", "agentic-coding", "arquitetura", "context-engineering", "evals", "gate-design", "governanca", "observability", "permissions", "production", "roadmap", "stack-tooling"]
thesis: "Uber escalou MCP de protocolo promissor a padrão operacional (5.000+ engenheiros, 10.000+ serviços, 1.500+ agentes ativos/mês, 60.000+ execuções/semana) construindo um gateway e registro centrais que geram automaticamente ferramentas MCP a partir dos IDLs de serviços, impõem governança e segurança em todas as camadas e servem três superfícies de consumo (builder no-code, SDK code-first e agentes de codificação)."
concepts: ["Gateway MCP e registro central como plano de controle para todas as interações MCP", "Geração automática de ferramentas MCP a partir de IDLs (proto/thrift) de serviços", "Descrições de ferramentas geradas por LLM a partir de nomes de mensagens e comentários", "Maior blast radius e velocidade de agentes exigem governança não negociável", "Estratégia de confiança diferenciada: gating e scanning mais rigorosos para MCPs de terceiros vs internos", "Ciclo de vida config-driven: definições versionadas em código, sem ambientes playground ad-hoc", "Deploy de definições via diff (pull request) escaneado por APIs unificadas de segurança", "Seleção explícita de ferramentas e overrides de parâmetros para reduzir alucinação e aumentar confiabilidade do agente", "Descoberta e qualidade de MCPs com tiers baseados em SLA, confiabilidade e disponibilidade", "Tool search com carregamento sob demanda para reduzir context bloat", "Skills como receitas compartilháveis para uso de MCPs, com avaliações e A/B testing", "Guardrails bloqueando endpoints mutáveis que poderiam derrubar serviços críticos"]
tools: ["MCP (Model Context Protocol)", "Uber MCP Gateway", "Uber MCP Registry", "Gateway Orchestrator", "Gateway Service", "Uber Agent Builder", "Uber Agent SDK", "AIFX CLI", "Claude Code", "Cursor", "Minions (agente de fundo no Claude harness)", "Serviço de redação de PII", "Unified scanning APIs de engenharia de segurança", "Object storage para definições MCP", "Tool search tool (planejado)", "Protobuf/Thrift IDL"]
people: ["Uber", "Magna", "Rash", "James"]
claims: ["Traduza endpoints de serviços automaticamente em ferramentas MCP crawling os IDLs (proto/thrift) e usando um LLM para gerar descrições baseadas em nomes de mensagens e comentários", "Mantenha service owners no controle de quais ferramentas são expostas e permita que refinem as descrições para os LLMs", "Aplique níveis mais altos de gating, scanning e checagens a MCPs de terceiros do que a sistemas internos confiáveis", "Depreque ambientes playground individuais e centralize todas as definições MCP em código versionado e gerenciado", "Estabeleça um registro central como fonte única de verdade para descoberta de MCPs e suas versões", "Integre centralmente o serviço de autorização para impedir acesso não autorizado a dados e endpoints críticos", "Integre um redator de PII para redação automática de dados sensíveis em todas as interações MCP", "Faça scanning periódico de código tanto no commit do diff quanto na base de código para detectar padrões perigosos e exposições de endpoint", "Implemente guardrails bloqueando endpoints mutáveis e forneça logging, métricas e tracing extensivos para todas as operações", "Faça updates de definições acionarem diffs (pull requests) escaneados por segurança antes do commit e deploy", "Em builders no-code, delimite MCPs via app mentions nas instruções de sistema, permita seleção explícita de ferramentas e overrides de parâmetros estáticos para confiabilidade", "No SDK code-first, use configuração YAML com nome do MCP, seleção de ferramentas e overrides de parâmetros carregados automaticamente", "Exponha um comando CLI (ex.: mcp add) que disponibiliza MCPs remotos ou locais a todos os agentes de IDE", "Exponha métricas de avaliação e SLAs (confiabilidade, disponibilidade) no registro para ranquear MCPs em tiers de qualidade", "Adicione uma tool de busca de tools para descoberta automática e carregamento sob demanda, reduzindo context bloat", "Trate skills como receitas compartilháveis entre equipes e adicione avaliações de qualidade de saída, correção de invocação e A/B testing entre versões"]
deep_dive: "high"
deep_dive_reason: "Apresenta alta densidade de detalhes arquiteturais e acionáveis (orquestrador IDL→MCP com LLM, diffs com scanning de segurança, guardrails, overrides de parâmetros, tiers de SLA no registro, tool search contra context bloat) diretamente relevantes a harness, governança, agent-fleets, context-engineering e evals em escala de produção."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-mcp-vs-api-simplifying-ai-agent-integration-with-external-data--7j1t3UZA1TY|MCP vs API: Simplifying AI Agent Integration with External Data]]", "[[extracts/youtube/ai-learning/2026-09-11-mcp-just-got-a-whole-lot-better--BqRhBq-_kgE|MCP Just Got a Whole Lot Better]]", "[[extracts/youtube/ai-learning/2026-09-11-model-context-protocol-mcp-overview-why-you-care--1Pf2rW5FsqQ|Model Context Protocol (MCP) Overview - Why You Care!]]", "[[extracts/youtube/ai-learning/2026-09-11-how-founders-build-on-claude-managed-agents--hm8NzEd5io0|How founders build on Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-building-agent-interfaces-lessons-from-chrome-devtools-mcp-for-agents-michael-ha--_B4Pv9ttFgY|Building Agent Interfaces: Lessons from Chrome DevTools (MCP) for Agents — Michael Hablich, Google]]", "[[extracts/youtube/ai-learning/2026-09-11-n8n-mcp-simplified-0-hype-what-why-how-of-mcp---gtlrI1TqZE|N8N MCP Simplified | 0% Hype | What, Why & How of MCP]]"]
---

# How Uber Runs 60,000 AI Agent Tasks Per Week With MCP

## Tese
Uber escalou MCP de protocolo promissor a padrão operacional (5.000+ engenheiros, 10.000+ serviços, 1.500+ agentes ativos/mês, 60.000+ execuções/semana) construindo um gateway e registro centrais que geram automaticamente ferramentas MCP a partir dos IDLs de serviços, impõem governança e segurança em todas as camadas e servem três superfícies de consumo (builder no-code, SDK code-first e agentes de codificação).

## Conceitos-chave
- Gateway MCP e registro central como plano de controle para todas as interações MCP
- Geração automática de ferramentas MCP a partir de IDLs (proto/thrift) de serviços
- Descrições de ferramentas geradas por LLM a partir de nomes de mensagens e comentários
- Maior blast radius e velocidade de agentes exigem governança não negociável
- Estratégia de confiança diferenciada: gating e scanning mais rigorosos para MCPs de terceiros vs internos
- Ciclo de vida config-driven: definições versionadas em código, sem ambientes playground ad-hoc
- Deploy de definições via diff (pull request) escaneado por APIs unificadas de segurança
- Seleção explícita de ferramentas e overrides de parâmetros para reduzir alucinação e aumentar confiabilidade do agente
- Descoberta e qualidade de MCPs com tiers baseados em SLA, confiabilidade e disponibilidade
- Tool search com carregamento sob demanda para reduzir context bloat
- Skills como receitas compartilháveis para uso de MCPs, com avaliações e A/B testing
- Guardrails bloqueando endpoints mutáveis que poderiam derrubar serviços críticos

## Ferramentas & pessoas
**Ferramentas:** MCP (Model Context Protocol), Uber MCP Gateway, Uber MCP Registry, Gateway Orchestrator, Gateway Service, Uber Agent Builder, Uber Agent SDK, AIFX CLI, Claude Code, Cursor, Minions (agente de fundo no Claude harness), Serviço de redação de PII, Unified scanning APIs de engenharia de segurança, Object storage para definições MCP, Tool search tool (planejado), Protobuf/Thrift IDL

**Pessoas/orgs:** Uber, Magna, Rash, James

## Claims acionáveis
- Traduza endpoints de serviços automaticamente em ferramentas MCP crawling os IDLs (proto/thrift) e usando um LLM para gerar descrições baseadas em nomes de mensagens e comentários
- Mantenha service owners no controle de quais ferramentas são expostas e permita que refinem as descrições para os LLMs
- Aplique níveis mais altos de gating, scanning e checagens a MCPs de terceiros do que a sistemas internos confiáveis
- Depreque ambientes playground individuais e centralize todas as definições MCP em código versionado e gerenciado
- Estabeleça um registro central como fonte única de verdade para descoberta de MCPs e suas versões
- Integre centralmente o serviço de autorização para impedir acesso não autorizado a dados e endpoints críticos
- Integre um redator de PII para redação automática de dados sensíveis em todas as interações MCP
- Faça scanning periódico de código tanto no commit do diff quanto na base de código para detectar padrões perigosos e exposições de endpoint
- Implemente guardrails bloqueando endpoints mutáveis e forneça logging, métricas e tracing extensivos para todas as operações
- Faça updates de definições acionarem diffs (pull requests) escaneados por segurança antes do commit e deploy
- Em builders no-code, delimite MCPs via app mentions nas instruções de sistema, permita seleção explícita de ferramentas e overrides de parâmetros estáticos para confiabilidade
- No SDK code-first, use configuração YAML com nome do MCP, seleção de ferramentas e overrides de parâmetros carregados automaticamente
- Exponha um comando CLI (ex.: mcp add) que disponibiliza MCPs remotos ou locais a todos os agentes de IDE
- Exponha métricas de avaliação e SLAs (confiabilidade, disponibilidade) no registro para ranquear MCPs em tiers de qualidade
- Adicione uma tool de busca de tools para descoberta automática e carregamento sob demanda, reduzindo context bloat
- Trate skills como receitas compartilháveis entre equipes e adicione avaliações de qualidade de saída, correção de invocação e A/B testing entre versões

> **Deep dive:** `high` — Apresenta alta densidade de detalhes arquiteturais e acionáveis (orquestrador IDL→MCP com LLM, diffs com scanning de segurança, guardrails, overrides de parâmetros, tiers de SLA no registro, tool search contra context bloat) diretamente relevantes a harness, governança, agent-fleets, context-engineering e evals em escala de produção.
