---
title: "Diagramas animados de pull requests"
type: "extract"
source: "x"
status_id: "2096996689680978148"
handle: "OhansEmmanuel"
url: "https://x.com/OhansEmmanuel/status/2096996689680978148"
created_at: "2026-09-07T16:19:05.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-ohansemmanuel-mermaid-diagrams-are-the-floor-every-pr-at-coldteaai-ships-w--2096996689680978148.json]]"
tags: ["code-review", "agent-tooling", "agentic-coding", "arquitetura", "stack-tooling"]
topic: "Diagramas animados de pull requests"
summary: "PR Lens (open source, MIT) desenha cada pull request como diagramas animados de arquitetura e fluxo de dados, postados como comentário no próprio PR, reduzindo a carga cognitiva do code review. Funciona via GitHub App, GitHub Action, CLI, ou pelo próprio agente de código que escreve o grafo da mudança."
key_points: ["Diagramas mostram o blast radius contra o sistema ao redor, com cores de delta (verde=novo, âmbar=alterado, vermelho=removido), pipeline animado passo a passo e walkthrough interativo (pan/zoom, temas claro/escuro).", "O agente de código pode gerar o documento do grafo diretamente (npx skills add coldteadotai/pr-lens) e iterar com npx @coldtea/pr-lens-cli validate até satisfazer o contrato — evitando gastar chave de provedor para descrever um diff que ele já entende.", "Múltiplos modos de execução: GitHub App (sticky comment, sem chave própria), GitHub Action em CI próprio (provider gemini/openai/openai-compatible, incluindo Ollama, DeepSeek, OpenRouter) e CLI local para renderizar antes de o PR existir ou revisar trabalho de agentes.", "Configuração por overlay .github/pr-lens.yml (renomear componentes, excluir arquivos, fixar lanes) resiste a refactors; o comando export gera pós-merge um mapa versionável do sistema (.github/pr-lens.map.json).", "Validado em PRs históricos grandes: React Hooks (react#13968), Node fetch (node#41749), Kubernetes Ingress (#14175), Tokio work-stealing, Neovim LSP, Django ASGI, webpack module federation, vLLM PagedAttention V2."]
entities: ["PR Lens", "Coldtea", "GitHub", "Mermaid", "Gemini", "OpenAI", "OpenRouter", "DeepSeek", "Ollama", "React", "Node.js", "Kubernetes", "Vue", "Rust", "Tokio", "Neovim", "Django", "webpack", "vLLM", "pnpm"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/coldteadotai/pr-lens"]
media: ["https://pbs.twimg.com/amplify_video_thumb/2096996668474548224/img/9h9-pMhJCjNMqVJP.jpg"]
---

# Diagramas animados de pull requests

**@OhansEmmanuel** · [2096996689680978148](https://x.com/OhansEmmanuel/status/2096996689680978148) · `tool`

## Resumo
PR Lens (open source, MIT) desenha cada pull request como diagramas animados de arquitetura e fluxo de dados, postados como comentário no próprio PR, reduzindo a carga cognitiva do code review. Funciona via GitHub App, GitHub Action, CLI, ou pelo próprio agente de código que escreve o grafo da mudança.

## Pontos-chave
- Diagramas mostram o blast radius contra o sistema ao redor, com cores de delta (verde=novo, âmbar=alterado, vermelho=removido), pipeline animado passo a passo e walkthrough interativo (pan/zoom, temas claro/escuro).
- O agente de código pode gerar o documento do grafo diretamente (npx skills add coldteadotai/pr-lens) e iterar com npx @coldtea/pr-lens-cli validate até satisfazer o contrato — evitando gastar chave de provedor para descrever um diff que ele já entende.
- Múltiplos modos de execução: GitHub App (sticky comment, sem chave própria), GitHub Action em CI próprio (provider gemini/openai/openai-compatible, incluindo Ollama, DeepSeek, OpenRouter) e CLI local para renderizar antes de o PR existir ou revisar trabalho de agentes.
- Configuração por overlay .github/pr-lens.yml (renomear componentes, excluir arquivos, fixar lanes) resiste a refactors; o comando export gera pós-merge um mapa versionável do sistema (.github/pr-lens.map.json).
- Validado em PRs históricos grandes: React Hooks (react#13968), Node fetch (node#41749), Kubernetes Ingress (#14175), Tokio work-stealing, Neovim LSP, Django ASGI, webpack module federation, vLLM PagedAttention V2.

## Links
- https://github.com/coldteadotai/pr-lens

## Entidades
PR Lens, Coldtea, GitHub, Mermaid, Gemini, OpenAI, OpenRouter, DeepSeek, Ollama, React, Node.js, Kubernetes, Vue, Rust, Tokio, Neovim, Django, webpack, vLLM, pnpm

> **Revisit:** `high` · **fonte:** `article`
