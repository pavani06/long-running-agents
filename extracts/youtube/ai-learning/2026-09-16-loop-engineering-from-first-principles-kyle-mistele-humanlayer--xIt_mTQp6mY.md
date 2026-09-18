---
title: "Loop Engineering from First Principles — Kyle Mistele, HumanLayer"
type: "extract"
source: "youtube"
video_id: "xIt_mTQp6mY"
url: "https://www.youtube.com/watch?v=xIt_mTQp6mY"
channel: "AI Engineer"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-16-loop-engineering-from-first-principles-kyle-mistele-humanlayer--xIt_mTQp6mY.txt]]"
tags: ["agent-loop", "agentic-coding", "harness-engineering", "context-engineering", "code-review", "gate-design", "decision-discipline", "telemetry", "process", "production", "error-handling"]
thesis: "Em vez de loops \"Ralph\" cegos que geram PRs gigantes que ninguém lê, equipes devem construir loops de controle agentivos baseados em teoria de controle (sensor, set point, controlador, atuador) que migram e melhoram o código incrementalmente, com feedback humano de baixa atrito e controle de fluxo."
concepts: ["Teoria de controle aplicada a agentes (sensor, set point, erro medido, controlador, atuador, distúrbios)", "Loops de controle agentivos vs. loops Ralph cegos", "Mudança incremental minimizando risco em vez de PRs de 40.000 linhas", "Sensores determinísticos (linters, AST) vs. não-determinísticos (agentes + regras em linguagem natural) vs. híbridos", "Amortecedor de distúrbios: scan completo rastreado em version control para bloquear novo código não-conforme em PRs", "Golden patterns: exemplos idiomáticos escritos à mão como contexto para o agente atuador", "Arquivo de feedback em markdown versionado, carregado deterministicamente no contexto do agente", "Reesteeramento humano via label no PR + comentário /iterate", "Controle de fluxo: no máximo um PR aberto por loop; desligar se o último PR não foi revisado", "Nunca enviar um agente para fazer trabalho de código determinístico", "Priorização por telemetria (erros, lacunas de APM/instrumentação) para enriquecer o sinal de controle", "Aceleração de velocidade: múltiplas migrações por PR, contextos separados por migração, ou workflows paralelos por pessoa"]
tools: ["ast-grep", "ripgrep", "ESLint", "Grep", "Effect", "React Doctor", "GitHub Actions", "GitLab CI", "CircleCI", "jq", "bash", "Claude Code", "OpenClaw", "Kubernetes (autoscaling)", "PostgreSQL (autovacuum)", "React (virtual DOM)", "MCP", "OpenAPI", "Next.js", "APM"]
people: ["Kyle (palestrante, HumanLayer)", "HumanLayer", "Geoffrey Huntley (criador do Ralph)", "Peter Steinberger", "Boris Cherny (criador do Claude Code)", "Matt Pocock", "Aiden Bai", "OpenCode team"]
claims: ["Defina um set point (estado final desejado mensurável do codebase) antes de construir qualquer loop agentivo", "Use ast-grep como sensor language-agnostic, fora da config de TypeScript/ESLint que agentes facilmente desabilitam com comentários inline", "Rode um scan completo no main, ordene violações deterministicamente e versione o resultado para detectar em cada PR se novos procedimentos não migrados foram adicionados", "Faça o controlador escolher deterministicamente (ex.: a menor violação primeiro) para reduzir risco, e só use agente quando a decisão exigir julgamento", "Inclua dados de telemetria (erros, lacunas de instrumentação/APM) no sinal de controle para que o agente melhore o código, não apenas migre 1:1", "Construa golden patterns à mão antes de soltar o agente, pois agentes são replicadores de padrões e caso contrário copiam docs/internet", "Faça commit, push e abertura de PR deterministicamente, usando a mensagem final do agente como descrição do PR", "Rode o loop em GitHub Actions (ou CI existente) com dispatch e agendamento (ex.: diário) em vez de provisionar infraestrutura nova", "Rastreie correções de rumo num arquivo de feedback markdown versionado, carregado no contexto do agente a cada iteração, permitindo auditoria e revert", "Dê a cada loop um label e um trigger de comentário (/iterate) para que o workflow recarregue diff, comentários e skill e reesteere o agente", "Implemente controle de fluxo: se o último PR do loop ainda está aberto, encerre a execução — no máximo um PR aberto por loop", "Escale a velocidade aumentando violações por iteração, dando a cada migração seu próprio contexto window (mais barato e confiável), ou rodando workflows paralelos distribuídos entre revisores"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de insight arquitetural acionável (sensores com ast-grep, feedback files versionados, controle de fluxo de um PR por loop, priorização por telemetria) com enquadramento novo via teoria de controle, diretamente relevante a harness e context-engineering para agentes de código em produção."
theme: "Agentic Coding com Evals"
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-art-of-loop-engineering-how-to-build-agents-that-improve-over-time--jPPiZ22DY3g|The Art of Loop Engineering: How to Build Agents That Improve Over Time]]", "[[extracts/youtube/ai-learning/2026-09-11-7-insane-loops-you-need-to-try-right-now--F4a8aMLb678|7 INSANE loops you need to try right now]]", "[[extracts/youtube/ai-learning/2026-09-11-wtf-is-loop-engineer-how-to-setup-for-real--W6x-hb44C0c|wtf is Loop Engineer & how to setup for real]]", "[[extracts/youtube/ai-learning/2026-09-11-ryan-lopopolo-harness-engineering-how-to-build-software-when-humans-steer-and-ag--c8bE0cj7vHY|Ryan Lopopolo - Harness Engineering: How to Build Software When Humans Steer and Agents Execute]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]"]
---

# Loop Engineering from First Principles — Kyle Mistele, HumanLayer

## Tese
Em vez de loops "Ralph" cegos que geram PRs gigantes que ninguém lê, equipes devem construir loops de controle agentivos baseados em teoria de controle (sensor, set point, controlador, atuador) que migram e melhoram o código incrementalmente, com feedback humano de baixa atrito e controle de fluxo.

## Conceitos-chave
- Teoria de controle aplicada a agentes (sensor, set point, erro medido, controlador, atuador, distúrbios)
- Loops de controle agentivos vs. loops Ralph cegos
- Mudança incremental minimizando risco em vez de PRs de 40.000 linhas
- Sensores determinísticos (linters, AST) vs. não-determinísticos (agentes + regras em linguagem natural) vs. híbridos
- Amortecedor de distúrbios: scan completo rastreado em version control para bloquear novo código não-conforme em PRs
- Golden patterns: exemplos idiomáticos escritos à mão como contexto para o agente atuador
- Arquivo de feedback em markdown versionado, carregado deterministicamente no contexto do agente
- Reesteeramento humano via label no PR + comentário /iterate
- Controle de fluxo: no máximo um PR aberto por loop; desligar se o último PR não foi revisado
- Nunca enviar um agente para fazer trabalho de código determinístico
- Priorização por telemetria (erros, lacunas de APM/instrumentação) para enriquecer o sinal de controle
- Aceleração de velocidade: múltiplas migrações por PR, contextos separados por migração, ou workflows paralelos por pessoa

## Ferramentas & pessoas
**Ferramentas:** ast-grep, ripgrep, ESLint, Grep, Effect, React Doctor, GitHub Actions, GitLab CI, CircleCI, jq, bash, Claude Code, OpenClaw, Kubernetes (autoscaling), PostgreSQL (autovacuum), React (virtual DOM), MCP, OpenAPI, Next.js, APM

**Pessoas/orgs:** Kyle (palestrante, HumanLayer), HumanLayer, Geoffrey Huntley (criador do Ralph), Peter Steinberger, Boris Cherny (criador do Claude Code), Matt Pocock, Aiden Bai, OpenCode team

## Claims acionáveis
- Defina um set point (estado final desejado mensurável do codebase) antes de construir qualquer loop agentivo
- Use ast-grep como sensor language-agnostic, fora da config de TypeScript/ESLint que agentes facilmente desabilitam com comentários inline
- Rode um scan completo no main, ordene violações deterministicamente e versione o resultado para detectar em cada PR se novos procedimentos não migrados foram adicionados
- Faça o controlador escolher deterministicamente (ex.: a menor violação primeiro) para reduzir risco, e só use agente quando a decisão exigir julgamento
- Inclua dados de telemetria (erros, lacunas de instrumentação/APM) no sinal de controle para que o agente melhore o código, não apenas migre 1:1
- Construa golden patterns à mão antes de soltar o agente, pois agentes são replicadores de padrões e caso contrário copiam docs/internet
- Faça commit, push e abertura de PR deterministicamente, usando a mensagem final do agente como descrição do PR
- Rode o loop em GitHub Actions (ou CI existente) com dispatch e agendamento (ex.: diário) em vez de provisionar infraestrutura nova
- Rastreie correções de rumo num arquivo de feedback markdown versionado, carregado no contexto do agente a cada iteração, permitindo auditoria e revert
- Dê a cada loop um label e um trigger de comentário (/iterate) para que o workflow recarregue diff, comentários e skill e reesteere o agente
- Implemente controle de fluxo: se o último PR do loop ainda está aberto, encerre a execução — no máximo um PR aberto por loop
- Escale a velocidade aumentando violações por iteração, dando a cada migração seu próprio contexto window (mais barato e confiável), ou rodando workflows paralelos distribuídos entre revisores

> **Deep dive:** `high` — Densidade alta de insight arquitetural acionável (sensores com ast-grep, feedback files versionados, controle de fluxo de um PR por loop, priorização por telemetria) com enquadramento novo via teoria de controle, diretamente relevante a harness e context-engineering para agentes de código em produção.
