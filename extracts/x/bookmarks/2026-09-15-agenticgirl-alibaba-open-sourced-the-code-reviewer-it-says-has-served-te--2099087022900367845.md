---
title: "Open-source code reviewer do Alibaba"
type: "extract"
source: "x"
status_id: "2099087022900367845"
handle: "agenticgirl"
url: "https://x.com/agenticgirl/status/2099087022900367845"
created_at: "2026-09-13T10:45:20.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-15-agenticgirl-alibaba-open-sourced-the-code-reviewer-it-says-has-served-te--2099087022900367845.json]]"
tags: ["code-review", "agentic-coding", "agents", "arquitetura", "production"]
topic: "Open-source code reviewer do Alibaba"
summary: "Alibaba liberou como open source o code reviewer usado internamente por dezenas de milhares de devs, que já achou milhões de defeitos. Ponto-chave da arquitetura: o loop de review não é todo entregue ao LLM — código determinístico cuida de cobertura de arquivos, bundling, matching de regras e comentários."
key_points: ["Validado em produção em escala: dezenas de milhares de desenvolvedores e milhões de defeitos encontrados internamente no Alibaba", "Arquitetura híbrida: componentes determinísticos (não-LLM) controlam file coverage, bundling, rule matching e a emissão de comentários", "Padrão de engenharia de agentes aplicado: o LLM não orquestra o loop inteiro, reduzindo não-determinismo em produção", "Relevante como referência de design para ferramentas de code review com LLM: scaffolding determinístico em volta do modelo"]
entities: ["Alibaba", "Open Code Review", "@agenticgirl"]
content_type: "announcement"
revisit: "high"
grounded_in: "tweet"
thin: false
links: []
media: ["https://pbs.twimg.com/media/HSFwnbybAAAgQ5y.jpg"]
theme: "Agentes para engenharia de código"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-chrisshort-alibaba-open-code-review-battle-tested-at-alibaba-s-scale-hy--2098555200680218872|ferramenta de code review híbrida]]", "[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-12-0xdeliriumm-boris-cherny-lead-of-claude-code-at-anthropic-published-a-pi--2081050632727793775|pipeline de code review com agentes]]", "[[extracts/x/bookmarks/2026-09-12-mihail_eric-line-by-line-code-review-will-soon-disappear-the-future-is-a--2098097592001548319|revisão de código risco-gateada]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-i-built-a-self-evolving-code-review-agent-most-code-review-a--2098416224803987968|Agente de code review auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-12-openai-we-quietly-released-the-open-source-codex-security-cli-but-h--2082263717916586117|Codex Security CLI open-source]]", "[[extracts/x/bookmarks/2026-09-12-ibesh_tech-bcherny-the-review-bar-should-follow-blast-radius-not-who-wr--2098218598997336384|Code review e blast radius]]", "[[extracts/x/bookmarks/2026-09-12-vaibhavsisinty-baidu-just-open-sourced-an-ocr-model-that-reads-entire-40-pa--2079000862962417996|OCR open-source da Baidu]]", "[[extracts/x/bookmarks/2026-09-12-wayen_ai-20-github-understand-anything--2077622505184100831|Ferramenta de compreensão de código]]", "[[extracts/x/bookmarks/2026-09-12-dan_jeffries1-tell-me-you-have-zero-devops-skills-without-telling-me-you-g--2098411466697097235|Comparação LLM e malware]]"]
---

# Open-source code reviewer do Alibaba

**@agenticgirl** · [2099087022900367845](https://x.com/agenticgirl/status/2099087022900367845) · `announcement`

## Resumo
Alibaba liberou como open source o code reviewer usado internamente por dezenas de milhares de devs, que já achou milhões de defeitos. Ponto-chave da arquitetura: o loop de review não é todo entregue ao LLM — código determinístico cuida de cobertura de arquivos, bundling, matching de regras e comentários.

## Pontos-chave
- Validado em produção em escala: dezenas de milhares de desenvolvedores e milhões de defeitos encontrados internamente no Alibaba
- Arquitetura híbrida: componentes determinísticos (não-LLM) controlam file coverage, bundling, rule matching e a emissão de comentários
- Padrão de engenharia de agentes aplicado: o LLM não orquestra o loop inteiro, reduzindo não-determinismo em produção
- Relevante como referência de design para ferramentas de code review com LLM: scaffolding determinístico em volta do modelo

## Entidades
Alibaba, Open Code Review, @agenticgirl

> **Revisit:** `high` · **fonte:** `tweet`
