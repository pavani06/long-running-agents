---
title: "Anthropic CPO Mike Krieger: Building AI Products From the Bottom Up"
type: "extract"
source: "youtube"
video_id: "Js1gU6L1Zi8"
url: "https://www.youtube.com/watch?v=Js1gU6L1Zi8"
channel: "Sequoia Capital"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-anthropic-cpo-mike-krieger-building-ai-products-from-the-bottom-up--Js1gU6L1Zi8.txt]]"
tags: ["agents", "agent-fleets", "agent-tooling", "agentic-coding", "arquitetura", "code-review", "context-engineering", "governanca", "memory-architecture", "multi-agent", "observability", "permissions", "process", "production", "roadmap"]
thesis: "A melhor estratégia de produto em IA nasce de criatividade bottom-up junto ao modelo (como MCP e Artifacts), e o próximo salto são agentes trabalhando autonomamente por horas, o que exige memória, verificabilidade, auditabilidade e discernimento sobre o que revelar."
concepts: ["criatividade bottom-up no desenvolvimento de produto (inversão do planejamento top-down)", "regra dos três: abstrair somente na terceira implementação", "MCP como protocolo aberto e padronizado", "evolução do MCP: de trazer contexto para tomar ações (agentic workflows)", "protocolos agente-para-agente e economia de agentes contratando agentes", "discernimento do agente: o que revelar vs reter (sycophancy vs over-refusal)", "auditabilidade e logging em escala (100 agentes operando na empresa)", "gerenciamento de identidade para agentes", "memória longitudinal para agentes", "limites do vibe coding e revisão de código gerado por IA", "visibilidade compartilhada do uso de IA reduz estigma interno", "alocação de compute: RL vs inferência/produto vs pre-training", "fine-tuning orientado a produto (modelos produto-específicos)", "design AI-native: expor as primitivas da aplicação ao modelo", "agente como usuário primário da aplicação", "portabilidade de tokens entre produtos", "proveniência e derivação vs marcação de 'gerado por IA'"]
tools: ["MCP (Model Context Protocol)", "Claude Code", "Artifacts", "Claude", "Claude Max", "Integrações Anthropic (GitHub, Zapier)", "Slack", "Cursor", "Windsurf", "ChatGPT", "GitHub Copilot", "Llama", "Instagram", "Midjourney"]
people: ["Mike Krieger (CPO da Anthropic, cofundador do Instagram)", "Anthropic", "Instagram", "OpenAI", "Sam Altman", "Mark Zuckerberg / Meta", "Ilya Sutskever / SSI", "Google", "Microsoft", "Amazon"]
claims: ["Construa produtos que não poderiam ser facilmente replicados apenas sobre a API; fine-tune features diretamente no modelo (ex.: Artifacts).", "Faça a mesma integração três vezes antes de abstrair — foi assim que o MCP nasceu de Google Drive + GitHub.", "Mais de 50-70% dos pull requests da Anthropic são gerados por Claude Code; revisão de código e dead-ends arquiteturais tornam-se os novos gargalos.", "Agentes de código expõem ineficiências organizacionais: uma reunião de alinhamento passa a bloquear o equivalente a 4-8 horas de trabalho acelerado.", "Exponha as primitivas da aplicação ao modelo — trate o modelo como usuário primário do produto, não como recurso de sidebar.", "Produtos 'AI-light' com IA em superfície secundária não escalam para uso agêntico; reconstrua os blocos centrais como AI-native.", "Distinguir conteúdo 'gerado por IA' torna-se inútil quando a maioria é gerada; foque em proveniência, citações e derivação.", "Agentes autônomos de longa duração exigem memória, tool use avançado, onboarding organizacional, verificabilidade e logging dedicado.", "Problemas em aberto: discernimento sobre o que revelar/reter, identidade de agentes, auditabilidade em escala e memória longitudinal.", "A alocação de compute entre RL, casos de uso de cliente e pre-training é decisão estratégica central; feedback de mercado foi essencial para o 3.7 Sonnet.", "Padronizar protocolos agente-agente cedo demais é prematuro; use protótipos internos para descobrir as primitivas corretas.", "Visibilidade pública do uso de IA (canais compartilhados no Slack) acelera adoção e elimina estigma interno.", "Portabilidade de tokens ('bring your tokens') pode viabilizar o bootstrap de novos produtos sobre assinaturas existentes."]
deep_dive: "high"
deep_dive_reason: "Combina novidade insider (gênese do MCP, ~70% dos PRs gerados por Claude Code) com insights arquiteturais acionáveis sobre agent-fleets, governança/auditabilidade de agentes e design de produtos AI-native."
---

# Anthropic CPO Mike Krieger: Building AI Products From the Bottom Up

## Tese
A melhor estratégia de produto em IA nasce de criatividade bottom-up junto ao modelo (como MCP e Artifacts), e o próximo salto são agentes trabalhando autonomamente por horas, o que exige memória, verificabilidade, auditabilidade e discernimento sobre o que revelar.

## Conceitos-chave
- criatividade bottom-up no desenvolvimento de produto (inversão do planejamento top-down)
- regra dos três: abstrair somente na terceira implementação
- MCP como protocolo aberto e padronizado
- evolução do MCP: de trazer contexto para tomar ações (agentic workflows)
- protocolos agente-para-agente e economia de agentes contratando agentes
- discernimento do agente: o que revelar vs reter (sycophancy vs over-refusal)
- auditabilidade e logging em escala (100 agentes operando na empresa)
- gerenciamento de identidade para agentes
- memória longitudinal para agentes
- limites do vibe coding e revisão de código gerado por IA
- visibilidade compartilhada do uso de IA reduz estigma interno
- alocação de compute: RL vs inferência/produto vs pre-training
- fine-tuning orientado a produto (modelos produto-específicos)
- design AI-native: expor as primitivas da aplicação ao modelo
- agente como usuário primário da aplicação
- portabilidade de tokens entre produtos
- proveniência e derivação vs marcação de 'gerado por IA'

## Ferramentas & pessoas
**Ferramentas:** MCP (Model Context Protocol), Claude Code, Artifacts, Claude, Claude Max, Integrações Anthropic (GitHub, Zapier), Slack, Cursor, Windsurf, ChatGPT, GitHub Copilot, Llama, Instagram, Midjourney

**Pessoas/orgs:** Mike Krieger (CPO da Anthropic, cofundador do Instagram), Anthropic, Instagram, OpenAI, Sam Altman, Mark Zuckerberg / Meta, Ilya Sutskever / SSI, Google, Microsoft, Amazon

## Claims acionáveis
- Construa produtos que não poderiam ser facilmente replicados apenas sobre a API; fine-tune features diretamente no modelo (ex.: Artifacts).
- Faça a mesma integração três vezes antes de abstrair — foi assim que o MCP nasceu de Google Drive + GitHub.
- Mais de 50-70% dos pull requests da Anthropic são gerados por Claude Code; revisão de código e dead-ends arquiteturais tornam-se os novos gargalos.
- Agentes de código expõem ineficiências organizacionais: uma reunião de alinhamento passa a bloquear o equivalente a 4-8 horas de trabalho acelerado.
- Exponha as primitivas da aplicação ao modelo — trate o modelo como usuário primário do produto, não como recurso de sidebar.
- Produtos 'AI-light' com IA em superfície secundária não escalam para uso agêntico; reconstrua os blocos centrais como AI-native.
- Distinguir conteúdo 'gerado por IA' torna-se inútil quando a maioria é gerada; foque em proveniência, citações e derivação.
- Agentes autônomos de longa duração exigem memória, tool use avançado, onboarding organizacional, verificabilidade e logging dedicado.
- Problemas em aberto: discernimento sobre o que revelar/reter, identidade de agentes, auditabilidade em escala e memória longitudinal.
- A alocação de compute entre RL, casos de uso de cliente e pre-training é decisão estratégica central; feedback de mercado foi essencial para o 3.7 Sonnet.
- Padronizar protocolos agente-agente cedo demais é prematuro; use protótipos internos para descobrir as primitivas corretas.
- Visibilidade pública do uso de IA (canais compartilhados no Slack) acelera adoção e elimina estigma interno.
- Portabilidade de tokens ('bring your tokens') pode viabilizar o bootstrap de novos produtos sobre assinaturas existentes.

> **Deep dive:** `high` — Combina novidade insider (gênese do MCP, ~70% dos PRs gerados por Claude Code) com insights arquiteturais acionáveis sobre agent-fleets, governança/auditabilidade de agentes e design de produtos AI-native.
