---
title: "The Agent for Your Agent."
type: "extract"
source: "youtube"
video_id: "VKFKyrrK-Iw"
url: "https://www.youtube.com/watch?v=VKFKyrrK-Iw"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-agent-for-your-agent--VKFKyrrK-Iw.txt]]"
tags: ["evals", "observability", "tracing", "agent-tooling", "monitoramento", "testes-qa", "verification", "production", "process", "agents", "error-handling"]
thesis: "LangChain lançou o LangSmith Engine, um agente que melhora outros agentes automatizando o ciclo de vida de desenvolvimento (construir, testar, monitorar) ao minerar traces, agrupar problemas em issues, redigir PRs com evals novos e verificar a correção em produção."
concepts: ["agent development lifecycle", "traces", "online evals", "regression testing", "monitoramento em produção", "clusterização de issues a partir de traces", "auto-melhoria de agentes (agents improving agents)", "draft de PR automatizado", "geração de exemplos e evals para suíte de testes", "loop construir-testar-deployar-monitorar-corrigir"]
tools: ["LangSmith", "Engine (LangSmith Engine)", "LangChain (ecosistema)"]
people: ["LangChain", "Vanta", "Campfire", "Cogent"]
claims: ["Estruture o desenvolvimento de agentes como um ciclo de quatro etapas: construir, testar, deployar e monitorar, repetindo o loop após cada correção", "Teste agentes com datasets cobrindo ampla gama de exemplos e evals focados nas métricas que definem sucesso", "Como não é possível prever todas as mensagens dos usuários e ações do agente, complemente testes offline com tracing e evals online após o deploy", "Mescle todos os traces e atue priorizando os padrões recorrentes antes de corrigir casos isolados", "Ao conectar o repositório do agente, o Engine redige um PR com mudança direcionada e propõe exemplos e evals novos para prevenir regressões futuras", "Após o merge, monitore o mesmo issue em produção para verificar se a correção realmente resolveu o problema", "Vanta, Campfire e Cogent já identificaram milhares de issues de agentes usando Engine, capturando regressões mais cedo e acelerando fixes"]
deep_dive: "low"
deep_dive_reason: "Trata-se de um anúncio promocional de produto: descreve o ciclo de vida e o fluxo do Engine em alto nível, mas sem densidade técnica, novidade arquitetural ou detalhes acionáveis além do pitch."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-best-ai-agents-need-less-code-than-you-think--YqjR4vQwbTc|The best AI agents need less code than you think]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-lifecycle-build-test-deploy-monitor-interrupt-26--jWy39wavbjY|The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-introducing-managed-deep-agents-interrupt-26--LdQpoK2TzSo|Introducing Managed Deep Agents | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-deep-agents-explained--GbzEDgcuGJU|Deep Agents Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-how-uber-built-ai-agents-that-save-21-000-developer-hours-with-langgraph-langcha--Bugs0dVcNI8|How Uber Built AI Agents That Save 21,000 Developer Hours with LangGraph | LangChain Interrupt]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-clay-s-eval-stack-300m-agent-runs-one-langsmith-pipeline--Uny6LpmjraI|Inside Clay's Eval Stack: 300M Agent Runs, One LangSmith Pipeline]]", "[[extracts/youtube/ai-learning/2026-09-11-introducing-openwiki-an-open-source-agent-for-repo-documentation--nIVu3zfYprI|Introducing OpenWiki, an open source agent for repo documentation]]"]
theme: "Arquiteturas de Deep Agents"
---

# The Agent for Your Agent.

## Tese
LangChain lançou o LangSmith Engine, um agente que melhora outros agentes automatizando o ciclo de vida de desenvolvimento (construir, testar, monitorar) ao minerar traces, agrupar problemas em issues, redigir PRs com evals novos e verificar a correção em produção.

## Conceitos-chave
- agent development lifecycle
- traces
- online evals
- regression testing
- monitoramento em produção
- clusterização de issues a partir de traces
- auto-melhoria de agentes (agents improving agents)
- draft de PR automatizado
- geração de exemplos e evals para suíte de testes
- loop construir-testar-deployar-monitorar-corrigir

## Ferramentas & pessoas
**Ferramentas:** LangSmith, Engine (LangSmith Engine), LangChain (ecosistema)

**Pessoas/orgs:** LangChain, Vanta, Campfire, Cogent

## Claims acionáveis
- Estruture o desenvolvimento de agentes como um ciclo de quatro etapas: construir, testar, deployar e monitorar, repetindo o loop após cada correção
- Teste agentes com datasets cobrindo ampla gama de exemplos e evals focados nas métricas que definem sucesso
- Como não é possível prever todas as mensagens dos usuários e ações do agente, complemente testes offline com tracing e evals online após o deploy
- Mescle todos os traces e atue priorizando os padrões recorrentes antes de corrigir casos isolados
- Ao conectar o repositório do agente, o Engine redige um PR com mudança direcionada e propõe exemplos e evals novos para prevenir regressões futuras
- Após o merge, monitore o mesmo issue em produção para verificar se a correção realmente resolveu o problema
- Vanta, Campfire e Cogent já identificaram milhares de issues de agentes usando Engine, capturando regressões mais cedo e acelerando fixes

> **Deep dive:** `low` — Trata-se de um anúncio promocional de produto: descreve o ciclo de vida e o fluxo do Engine em alto nível, mas sem densidade técnica, novidade arquitetural ou detalhes acionáveis além do pitch.
