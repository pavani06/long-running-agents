---
title: "Autoreview: code review multi-engine"
type: "extract"
source: "x"
status_id: "2080899298838098034"
handle: "steipete"
url: "https://x.com/steipete/status/2080899298838098034"
created_at: "2026-07-25T06:13:48.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034.json]]"
tags: ["agent-tooling", "code-review", "harness", "verification", "process", "model-selection"]
topic: "Autoreview: code review multi-engine"
summary: "Documentação da skill autoreview (usada por steipete, que bateu recorde de 66 rodadas num refactor difícil) que orquestra revisões de código estruturadas com Codex (padrão), Claude, Amp, Pi ou Kimi em sandbox isolado, com alvos Git explícitos, threshold de severidade e relatório JSON validado. Vale salvar como referência de harness de code review agêntico com isolamento e verificação rigorosos."
key_points: ["Seleção explícita de alvo Git: --mode local/branch/commit com base pinada (merge-base para PRs), revisando estados staged e unstaged separadamente — defeito presente só no index permanece acionável (rotulado INDEX-only).", "Isolamento forte: revisor roda em sandbox vazio sem acesso a arquivos não alterados; autenticação sanitizada via launcher privado que restaura HOME só para o executável de auth; /tmp compartilhado é bloqueado no macOS; credenciais reais no bundle viram findings P0 sem reproduzir valores.", "Default reporta apenas P0 (bloqueadores materiais); --max-priority P1-P3 amplia o escopo; findings são conselho a verificar contra o código real, não instruções a aplicar às cegas; sem rodadas extras de revisão para obter veredito 'mais bonito'.", "Saída estruturada e à prova de falhas: relatório JSON validado + sidecar de status (scoped-clean/findings/filtered/incorrect/incomplete/reviewer_unavailable) com exit codes 0/1/2; pass posterior falhada nunca publica relatório parcial; dry-run valida preparação sem contactar o revisor.", "Engines alternativas com pré-requisitos (Claude CLI 2.1.169+ em safe mode, Amp via AMP_API_KEY, Pi 0.79.0+, Kimi 0.30.0+); default é Codex gpt-5.6-sol high reasoning com retry gpt-5.6-terra apenas em falha de acesso à conta, honrando escolhas explícitas de engine/modelo."]
entities: ["steipete", "Codex", "Claude", "Amp", "Pi", "Kimi", "OpenClaw", "gpt-5.6-sol", "gpt-5.6-terra"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/openclaw/agent-skills/blob/main/skills/autoreview/SKILL.md"]
media: []
thin: false
theme: "Tooling para agentes de código"
relates-to: ["[[extracts/x/bookmarks/2026-09-17-trending_repos-trending-repository-of-the-day-open-code-review-fast-efficie--2100194977523331489|Open Code Review da Alibaba]]", "[[extracts/x/bookmarks/2026-09-18-devagrawal09-built-jev-review-a-small-code-review-workflow-powered-by-typ--2100341005690298687|Code-review workflow com julgamentos LLM]]", "[[extracts/x/bookmarks/2026-09-14-riverai7z-pi-review-pi-install-git-https-t-co-ezws490o0e--2098752822221365732|Plugin de code review para Pi]]", "[[extracts/x/bookmarks/2026-09-12-chrisshort-alibaba-open-code-review-battle-tested-at-alibaba-s-scale-hy--2098555200680218872|ferramenta de code review híbrida]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-i-built-a-self-evolving-code-review-agent-most-code-review-a--2098416224803987968|Agente de code review auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-18-mattpocockuk-thinking-about-creating-a-pr-skill-you-invoke-it-to-create-a--2100521948786667822|Skill de criação de PRs]]", "[[extracts/x/bookmarks/2026-09-18-redp314-got-jev-to-review-my-prs-200x-cheaper-than-claude-and-it-ans--2100585126652481915|Code review barato via typesafe]]", "[[extracts/x/bookmarks/2026-09-16-mattpocockuk-retro-will-now-aggressively-look-for-opportunities-to-turn-f--2099859946053533933|Fuzzy rules viram checks determinísticos]]", "[[extracts/x/bookmarks/2026-09-17-mstryoda_-cloudflare-ai-agentlar-icin-security-skill-yaynlams-direkt-y--2099560068362441009|Skill de segurança da Cloudflare]]", "[[extracts/x/bookmarks/2026-09-15-agenticgirl-alibaba-open-sourced-the-code-reviewer-it-says-has-served-te--2099087022900367845|Open-source code reviewer do Alibaba]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-vibed-out-an-app-today-and-i-haven-t-looked-at-the-internals--2086838432102228008|Correção de arquitetura pós-vibe-coding]]", "[[extracts/x/bookmarks/2026-09-12-glaucia_lemos86-caraca-absurdo-isso-aqui-segui-o-conselho-do-pvncher-em-pedi--2096649629068624378|Revisão de artefatos de contexto entre modelos]]", "[[extracts/x/bookmarks/2026-09-17-eng_khairallah1-the-full-prompt-is-here-lt-purpose-gt-run-a-drift-audit-betw--2100190909715337487|Drift audit entre docs e código]]", "[[extracts/x/bookmarks/2026-09-12-ibesh_tech-bcherny-the-review-bar-should-follow-blast-radius-not-who-wr--2098218598997336384|Code review e blast radius]]"]
---

# Autoreview: code review multi-engine

**@steipete** · [2080899298838098034](https://x.com/steipete/status/2080899298838098034) · `tool`

## Resumo
Documentação da skill autoreview (usada por steipete, que bateu recorde de 66 rodadas num refactor difícil) que orquestra revisões de código estruturadas com Codex (padrão), Claude, Amp, Pi ou Kimi em sandbox isolado, com alvos Git explícitos, threshold de severidade e relatório JSON validado. Vale salvar como referência de harness de code review agêntico com isolamento e verificação rigorosos.

## Pontos-chave
- Seleção explícita de alvo Git: --mode local/branch/commit com base pinada (merge-base para PRs), revisando estados staged e unstaged separadamente — defeito presente só no index permanece acionável (rotulado INDEX-only).
- Isolamento forte: revisor roda em sandbox vazio sem acesso a arquivos não alterados; autenticação sanitizada via launcher privado que restaura HOME só para o executável de auth; /tmp compartilhado é bloqueado no macOS; credenciais reais no bundle viram findings P0 sem reproduzir valores.
- Default reporta apenas P0 (bloqueadores materiais); --max-priority P1-P3 amplia o escopo; findings são conselho a verificar contra o código real, não instruções a aplicar às cegas; sem rodadas extras de revisão para obter veredito 'mais bonito'.
- Saída estruturada e à prova de falhas: relatório JSON validado + sidecar de status (scoped-clean/findings/filtered/incorrect/incomplete/reviewer_unavailable) com exit codes 0/1/2; pass posterior falhada nunca publica relatório parcial; dry-run valida preparação sem contactar o revisor.
- Engines alternativas com pré-requisitos (Claude CLI 2.1.169+ em safe mode, Amp via AMP_API_KEY, Pi 0.79.0+, Kimi 0.30.0+); default é Codex gpt-5.6-sol high reasoning com retry gpt-5.6-terra apenas em falha de acesso à conta, honrando escolhas explícitas de engine/modelo.

## Links
- https://github.com/openclaw/agent-skills/blob/main/skills/autoreview/SKILL.md

## Entidades
steipete, Codex, Claude, Amp, Pi, Kimi, OpenClaw, gpt-5.6-sol, gpt-5.6-terra

> **Revisit:** `high` · **fonte:** `article`
