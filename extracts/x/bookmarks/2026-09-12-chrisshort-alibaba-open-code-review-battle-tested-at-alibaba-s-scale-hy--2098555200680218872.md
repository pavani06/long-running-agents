---
title: "ferramenta de code review híbrida"
type: "extract"
source: "x"
status_id: "2098555200680218872"
handle: "ChrisShort"
url: "https://x.com/ChrisShort/status/2098555200680218872"
created_at: "2026-09-11T23:32:03.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-chrisshort-alibaba-open-code-review-battle-tested-at-alibaba-s-scale-hy--2098555200680218872.json]]"
tags: ["code-review", "agent-tooling", "agents", "arquitetura", "stack-tooling"]
topic: "ferramenta de code review híbrida"
summary: "Projeto open-source da Alibaba (open-code-review) que combina pipelines determinísticos com agente LLM para revisão de código, gerando comentários precisos em nível de linha. Vale salvar por ser validado na escala da Alibaba e compatível com APIs OpenAI e Anthropic."
key_points: ["Arquitetura híbrida: regras determinísticas + LLM Agent para reduzir ruído/falsos positivos do LLM puro", "Ruleset interno ajustado para classes específicas de bugs: NPE, thread-safety, XSS e SQL injection", "Comentários precisos ancorados em nível de linha, não apenas feedback genérico do PR", "Compatível com APIs OpenAI e Anthropic, permitindo trocar o modelo subjacente", "Battle-tested na escala de produção da Alibaba"]
entities: ["Alibaba", "ChrisShort", "open-code-review", "OpenAI", "Anthropic"]
content_type: "tool"
revisit: "high"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HR-Q1Z7WkAAWSuV.jpg"]
thin: false
theme: "Tooling Agêntico para Código"
relates-to: ["[[extracts/x/bookmarks/2026-09-17-trending_repos-trending-repository-of-the-day-open-code-review-fast-efficie--2100194977523331489|Open Code Review da Alibaba]]", "[[extracts/x/bookmarks/2026-09-15-agenticgirl-alibaba-open-sourced-the-code-reviewer-it-says-has-served-te--2099087022900367845|Open-source code reviewer do Alibaba]]", "[[extracts/x/bookmarks/2026-09-18-devagrawal09-built-jev-review-a-small-code-review-workflow-powered-by-typ--2100341005690298687|Code-review workflow com julgamentos LLM]]", "[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-i-built-a-self-evolving-code-review-agent-most-code-review-a--2098416224803987968|Agente de code review auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-12-mihail_eric-line-by-line-code-review-will-soon-disappear-the-future-is-a--2098097592001548319|revisão de código risco-gateada]]", "[[extracts/x/bookmarks/2026-09-12-openai-we-quietly-released-the-open-source-codex-security-cli-but-h--2082263717916586117|Codex Security CLI open-source]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-tencent-opensource-ai-red-teaming-platform-a-full-stack-ai-r--2092420578875527174|Plataforma open-source de AI red teaming]]", "[[extracts/x/bookmarks/2026-09-12-thsottiaux-more-opensource-goodness-we-have-just-released-a-cli-and-typ--2082241164850364555|Codex Security CLI e SDK]]", "[[extracts/x/bookmarks/2026-09-12-ohansemmanuel-mermaid-diagrams-are-the-floor-every-pr-at-coldteaai-ships-w--2096996689680978148|Diagramas animados de pull requests]]", "[[extracts/x/bookmarks/2026-09-14-riverai7z-pi-review-pi-install-git-https-t-co-ezws490o0e--2098752822221365732|Plugin de code review para Pi]]", "[[extracts/x/bookmarks/2026-09-12-theprimeagen-something-that-has-greatly-improved-the-reliability-of-the-c--2081066227619836308|técnica de confiabilidade em código via LLM]]", "[[extracts/x/bookmarks/2026-09-15-shadcn-introducing-shadcn-lint-an-agent-first-linter-for-tailwind-d--2099534231114314145|shadcn/lint, linter agent-first para Tailwind]]", "[[extracts/x/bookmarks/2026-09-12-agenticgirl-ripwire-from-red-hat-emerging-technologies-is-a-remarkably-s--2096612794145911260|contexto de repositório para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-wayen_ai-20-github-understand-anything--2077622505184100831|Ferramenta de compreensão de código]]", "[[extracts/x/bookmarks/2026-09-12-txbrraa-github-acaba-de-solucionar-el-mayor-problema-del-vibe-coding--2097955506891469272|GitHub Spec Kit e spec-driven development]]", "[[extracts/x/bookmarks/2026-09-12-vaibhavsisinty-baidu-just-open-sourced-an-ocr-model-that-reads-entire-40-pa--2079000862962417996|OCR open-source da Baidu]]", "[[extracts/x/bookmarks/2026-09-16-schteppe-the-crap-change-risk-anti-patterns-metric-is-a-software-qual--2099728101366276474|Métrica CRAP de risco de mudança]]", "[[extracts/x/bookmarks/2026-09-12-dan_jeffries1-tell-me-you-have-zero-devops-skills-without-telling-me-you-g--2098411466697097235|Comparação LLM e malware]]"]
---

# ferramenta de code review híbrida

**@ChrisShort** · [2098555200680218872](https://x.com/ChrisShort/status/2098555200680218872) · `tool`

## Resumo
Projeto open-source da Alibaba (open-code-review) que combina pipelines determinísticos com agente LLM para revisão de código, gerando comentários precisos em nível de linha. Vale salvar por ser validado na escala da Alibaba e compatível com APIs OpenAI e Anthropic.

## Pontos-chave
- Arquitetura híbrida: regras determinísticas + LLM Agent para reduzir ruído/falsos positivos do LLM puro
- Ruleset interno ajustado para classes específicas de bugs: NPE, thread-safety, XSS e SQL injection
- Comentários precisos ancorados em nível de linha, não apenas feedback genérico do PR
- Compatível com APIs OpenAI e Anthropic, permitindo trocar o modelo subjacente
- Battle-tested na escala de produção da Alibaba

## Entidades
Alibaba, ChrisShort, open-code-review, OpenAI, Anthropic

> **Revisit:** `high` · **fonte:** `tweet`
