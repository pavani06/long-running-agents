---
title: "Open Code Review da Alibaba"
type: "extract"
source: "x"
status_id: "2100194977523331489"
handle: "trending_repos"
url: "https://x.com/trending_repos/status/2100194977523331489"
created_at: "2026-09-16T12:07:57.000Z"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-17-trending_repos-trending-repository-of-the-day-open-code-review-fast-efficie--2100194977523331489.json]]"
tags: ["code-review", "agents", "multi-agent", "arquitetura", "evals", "token-budgeting", "performance", "testes-qa", "production"]
topic: "Open Code Review da Alibaba"
summary: "CLI open-source de code review com IA, incubada pela Alibaba após 2 anos servindo dezenas de milhares de devs; combina pipelines determinísticos com agente LLM e bate Claude Code em Precision/F1 consumindo ~1/9 dos tokens. Acompanha o AACR-Bench, benchmark real de code review (200 PRs, 10 linguagens, validado por 80+ engenheiros seniores)."
key_points: ["Arquitetura híbrida: engenharia determinística garante hard constraints (seleção precisa de arquivos, bundling de arquivos relacionados em sub-agentes com contexto isolado, matching fino de regras via template engine, módulos externos de posicionamento e reflexão de comentários) enquanto o agente cuida de decisões dinâmicas e retrieval de contexto.", "Diagnóstico dos problemas de agentes genéricos (ex.: Claude Code com Skills): cobertura incompleta em changesets grandes, drift de posição nos comentários e qualidade instável — causa raiz é arquitetura puramente dirigida por linguagem sem restrições rígidas no processo.", "Vs. Claude Code no AACR-Bench: Precision e F1 significativamente maiores com o mesmo modelo, ~1/9 dos tokens e revisões mais rápidas; Recall menor é trade-off deliberado (precisão sobre ruído/falsos alarmes).", "Toolset do agente destilado de traces de tool-calls em produção em larga escala (frequência de chamadas, taxas de repetição por ferramenta, impacto na cadeia de chamadas) — mais estável e previsível que toolkit genérico.", "Funcionalidades: modos review (workspace, branch range, commit), scan de arquivo inteiro para auditar codebases, delegation mode (o agente host faz a review sem API key), saída JSON para agentes, MCP server, integrações com Claude Code/Codex/Cursor/OpenCode, CI/CD (GitHub Actions, GitLab, Gerrit) e telemetria OpenTelemetry."]
entities: ["Alibaba Group", "Open Code Review (ocr)", "Claude Code", "AACR-Bench", "Hugging Face", "Git", "npm", "OpenTelemetry", "Codex", "Cursor", "OpenCode"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/alibaba/open-code-review"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-chrisshort-alibaba-open-code-review-battle-tested-at-alibaba-s-scale-hy--2098555200680218872|ferramenta de code review híbrida]]", "[[extracts/x/bookmarks/2026-09-15-agenticgirl-alibaba-open-sourced-the-code-reviewer-it-says-has-served-te--2099087022900367845|Open-source code reviewer do Alibaba]]", "[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-12-0xdeliriumm-boris-cherny-lead-of-claude-code-at-anthropic-published-a-pi--2081050632727793775|pipeline de code review com agentes]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-tencent-opensource-ai-red-teaming-platform-a-full-stack-ai-r--2092420578875527174|Plataforma open-source de AI red teaming]]", "[[extracts/x/bookmarks/2026-09-18-devagrawal09-built-jev-review-a-small-code-review-workflow-powered-by-typ--2100341005690298687|Code-review workflow com julgamentos LLM]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-i-built-a-self-evolving-code-review-agent-most-code-review-a--2098416224803987968|Agente de code review auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-12-openai-we-quietly-released-the-open-source-codex-security-cli-but-h--2082263717916586117|Codex Security CLI open-source]]", "[[extracts/x/bookmarks/2026-09-14-ryrenz-claude-code-alphaxiv-openresearch-openresearch-6-github-1000--2098577841944207463|OpenResearch: agente de pesquisa científica]]", "[[extracts/x/bookmarks/2026-09-12-thsottiaux-more-opensource-goodness-we-have-just-released-a-cli-and-typ--2082241164850364555|Codex Security CLI e SDK]]", "[[extracts/x/bookmarks/2026-09-12-tom_doerr-hyperresearch-turns-claude-code-into-a-research-agent-that-i--2097841937642332595|Agente de pesquisa profunda para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-ohansemmanuel-mermaid-diagrams-are-the-floor-every-pr-at-coldteaai-ships-w--2096996689680978148|Diagramas animados de pull requests]]", "[[extracts/x/bookmarks/2026-09-12-vaibhavsisinty-baidu-just-open-sourced-an-ocr-model-that-reads-entire-40-pa--2079000862962417996|OCR open-source da Baidu]]", "[[extracts/x/bookmarks/2026-09-12-zodchiii-moonshot-just-cloned-claude-code-and-made-it-free-it-s-calle--2078222648539271430|Lançamento do Kimi Code CLI]]", "[[extracts/x/bookmarks/2026-09-12-wayen_ai-20-github-understand-anything--2077622505184100831|Ferramenta de compreensão de código]]", "[[extracts/x/bookmarks/2026-09-12-qwendevs-alibabas-zvec-team-open-sourced-zg-a-local-search-tool-for-d--2095157452904018263|busca local para agentes de IA]]", "[[extracts/x/bookmarks/2026-09-12-thesupermanmx-china-open-sourced-a-peanut-sized-ocr-that-parses-entire-100--2078774556249186345|OCR local de PDFs longos]]", "[[extracts/x/bookmarks/2026-09-15-sumanth_077-microsoft-open-sourced-an-ai-engineer-coach-ai-engineer-coac--2098785284745990298|Microsoft AI Engineer Coach]]", "[[extracts/x/bookmarks/2026-09-12-askalphaxiv-introducing-deepseek-v4-1-flash-for-understanding-research-p--2098309348858704095|alphaXiv AI paper Q&A]]"]
theme: "Tooling para agentes de código"
---

# Open Code Review da Alibaba

**@trending_repos** · [2100194977523331489](https://x.com/trending_repos/status/2100194977523331489) · `tool`

## Resumo
CLI open-source de code review com IA, incubada pela Alibaba após 2 anos servindo dezenas de milhares de devs; combina pipelines determinísticos com agente LLM e bate Claude Code em Precision/F1 consumindo ~1/9 dos tokens. Acompanha o AACR-Bench, benchmark real de code review (200 PRs, 10 linguagens, validado por 80+ engenheiros seniores).

## Pontos-chave
- Arquitetura híbrida: engenharia determinística garante hard constraints (seleção precisa de arquivos, bundling de arquivos relacionados em sub-agentes com contexto isolado, matching fino de regras via template engine, módulos externos de posicionamento e reflexão de comentários) enquanto o agente cuida de decisões dinâmicas e retrieval de contexto.
- Diagnóstico dos problemas de agentes genéricos (ex.: Claude Code com Skills): cobertura incompleta em changesets grandes, drift de posição nos comentários e qualidade instável — causa raiz é arquitetura puramente dirigida por linguagem sem restrições rígidas no processo.
- Vs. Claude Code no AACR-Bench: Precision e F1 significativamente maiores com o mesmo modelo, ~1/9 dos tokens e revisões mais rápidas; Recall menor é trade-off deliberado (precisão sobre ruído/falsos alarmes).
- Toolset do agente destilado de traces de tool-calls em produção em larga escala (frequência de chamadas, taxas de repetição por ferramenta, impacto na cadeia de chamadas) — mais estável e previsível que toolkit genérico.
- Funcionalidades: modos review (workspace, branch range, commit), scan de arquivo inteiro para auditar codebases, delegation mode (o agente host faz a review sem API key), saída JSON para agentes, MCP server, integrações com Claude Code/Codex/Cursor/OpenCode, CI/CD (GitHub Actions, GitLab, Gerrit) e telemetria OpenTelemetry.

## Links
- https://github.com/alibaba/open-code-review

## Entidades
Alibaba Group, Open Code Review (ocr), Claude Code, AACR-Bench, Hugging Face, Git, npm, OpenTelemetry, Codex, Cursor, OpenCode

> **Revisit:** `high` · **fonte:** `article`
