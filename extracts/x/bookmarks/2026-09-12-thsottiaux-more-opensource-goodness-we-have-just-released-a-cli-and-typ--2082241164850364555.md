---
title: "Codex Security CLI e SDK"
type: "extract"
source: "x"
status_id: "2082241164850364555"
handle: "thsottiaux"
url: "https://x.com/thsottiaux/status/2082241164850364555"
created_at: "2026-07-28T23:05:54.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-thsottiaux-more-opensource-goodness-we-have-just-released-a-cli-and-typ--2082241164850364555.json]]"
tags: ["code-review", "classification", "agent-tooling", "stack-tooling", "verification", "model-selection"]
topic: "Codex Security CLI e SDK"
summary: "OpenAI lançou o @openai/codex-security, CLI e SDK TypeScript para definir política de segurança e encontrar, validar e corrigir vulnerabilidades em código, com scans em CI, geração de SECURITY.md e serviço de findings com dedupe por embeddings. Vale salvar como referência prática de ferramenta agêntica de segurança para adotar em pipelines."
key_points: ["Instalação via npm (@openai/codex-security), requer Node.js 22.13+ e Python 3.10+; em CI basta definir OPENAI_API_KEY em vez de login interativo; parte das capacidades de cyber exige aprovação no Trusted Access for Cyber", "Gera rascunhos de política SECURITY.md no escopo do repositório ou por componente (com knowledge-base de documentos de arquitetura/threat model mantidos fora do repo); o rascunho não é instalado automaticamente nem dispara scan", "SDK programático com opções de execução (mode deep, workers, subagents, maxDiscoveryRuns, maxTimeHours) e imagem Docker (ghcr.io/openai/codex-security) com Compose para escanear muitos repositórios", "Serviço de findings persiste findings e embeddings em SQLite, expõe dashboard read-only que atualiza a cada 5s, detecta duplicatas por similaridade de embedding (escopo por repo ou --all-repositories) e faz revisão independente com Codex antes de aceitar grupos", "classify-severity avalia findings sob rubrica própria (policy.md) com checkpoints em SQLite e reuso em reruns (--reprocess força); suporta provedores alternativos: Amazon Bedrock, OpenRouter e Fireworks com seleção de modelo"]
entities: ["OpenAI", "Codex Security", "@openai/codex-security", "TypeScript", "Node.js", "Python", "npm", "Docker Compose", "SQLite", "Amazon Bedrock", "OpenRouter", "Fireworks"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/openai/codex-security"]
media: []
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-openai-we-quietly-released-the-open-source-codex-security-cli-but-h--2082263717916586117|Codex Security CLI open-source]]", "[[extracts/x/bookmarks/2026-09-17-mstryoda_-cloudflare-ai-agentlar-icin-security-skill-yaynlams-direkt-y--2099560068362441009|Skill de segurança da Cloudflare]]", "[[extracts/x/bookmarks/2026-09-18-trending_repos-trending-repository-of-the-day-security-audit-skill-a-coding--2100557033829261738|auditoria de segurança multi-agente]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-tencent-opensource-ai-red-teaming-platform-a-full-stack-ai-r--2092420578875527174|Plataforma open-source de AI red teaming]]", "[[extracts/x/bookmarks/2026-09-17-trending_repos-trending-repository-of-the-day-open-code-review-fast-efficie--2100194977523331489|Open Code Review da Alibaba]]", "[[extracts/x/bookmarks/2026-09-16-gergelyorosz-here-s-what-openai-s-agentic-software-factory-looks-like-tod--2099945497377091902|Fábrica de software agêntica da OpenAI]]", "[[extracts/x/bookmarks/2026-09-12-eric_wallace_-today-we-are-releasing-gpt-5-6-cyber-the-model-is-our-first--2086866306167656901|Lançamento de modelo de cibersegurança]]", "[[extracts/x/bookmarks/2026-09-18-openai-we-re-sharing-our-new-framework-for-tracking-investigating-a--2100344867507327087|framework de disclosure de misalignment]]"]
theme: "Codificação Agêntica e Code Review"
---

# Codex Security CLI e SDK

**@thsottiaux** · [2082241164850364555](https://x.com/thsottiaux/status/2082241164850364555) · `announcement`

## Resumo
OpenAI lançou o @openai/codex-security, CLI e SDK TypeScript para definir política de segurança e encontrar, validar e corrigir vulnerabilidades em código, com scans em CI, geração de SECURITY.md e serviço de findings com dedupe por embeddings. Vale salvar como referência prática de ferramenta agêntica de segurança para adotar em pipelines.

## Pontos-chave
- Instalação via npm (@openai/codex-security), requer Node.js 22.13+ e Python 3.10+; em CI basta definir OPENAI_API_KEY em vez de login interativo; parte das capacidades de cyber exige aprovação no Trusted Access for Cyber
- Gera rascunhos de política SECURITY.md no escopo do repositório ou por componente (com knowledge-base de documentos de arquitetura/threat model mantidos fora do repo); o rascunho não é instalado automaticamente nem dispara scan
- SDK programático com opções de execução (mode deep, workers, subagents, maxDiscoveryRuns, maxTimeHours) e imagem Docker (ghcr.io/openai/codex-security) com Compose para escanear muitos repositórios
- Serviço de findings persiste findings e embeddings em SQLite, expõe dashboard read-only que atualiza a cada 5s, detecta duplicatas por similaridade de embedding (escopo por repo ou --all-repositories) e faz revisão independente com Codex antes de aceitar grupos
- classify-severity avalia findings sob rubrica própria (policy.md) com checkpoints em SQLite e reuso em reruns (--reprocess força); suporta provedores alternativos: Amazon Bedrock, OpenRouter e Fireworks com seleção de modelo

## Links
- https://github.com/openai/codex-security

## Entidades
OpenAI, Codex Security, @openai/codex-security, TypeScript, Node.js, Python, npm, Docker Compose, SQLite, Amazon Bedrock, OpenRouter, Fireworks

> **Revisit:** `high` · **fonte:** `article`
