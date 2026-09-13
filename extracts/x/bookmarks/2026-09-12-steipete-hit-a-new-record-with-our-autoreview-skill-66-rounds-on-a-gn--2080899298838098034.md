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
relates-to: ["[[extracts/x/bookmarks/2026-09-12-chrisshort-alibaba-open-code-review-battle-tested-at-alibaba-s-scale-hy--2098555200680218872|ferramenta de code review híbrida]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-i-built-a-self-evolving-code-review-agent-most-code-review-a--2098416224803987968|Agente de code review auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-12-0xdeliriumm-boris-cherny-lead-of-claude-code-at-anthropic-published-a-pi--2081050632727793775|pipeline de code review com agentes]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-what-techniques-do-you-use-for-making-ai-authored-pr-s-easie--2096666329495257563|revisão de PRs gerados por IA]]", "[[extracts/x/bookmarks/2026-09-12-mihail_eric-line-by-line-code-review-will-soon-disappear-the-future-is-a--2098097592001548319|revisão de código risco-gateada]]", "[[extracts/x/bookmarks/2026-09-12-ohansemmanuel-mermaid-diagrams-are-the-floor-every-pr-at-coldteaai-ships-w--2096996689680978148|Diagramas animados de pull requests]]", "[[extracts/x/bookmarks/2026-09-12-tom_doerr-hyperresearch-turns-claude-code-into-a-research-agent-that-i--2097841937642332595|Agente de pesquisa profunda para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-poteto-pstack-now-includes-2-skills-i-recommend-everyone-use-or-cop--2082874054483255805|Skill de verificação para agentes]]", "[[extracts/x/bookmarks/2026-09-12-thsottiaux-more-opensource-goodness-we-have-just-released-a-cli-and-typ--2082241164850364555|Codex Security CLI e SDK]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-vibed-out-an-app-today-and-i-haven-t-looked-at-the-internals--2086838432102228008|Correção de arquitetura pós-vibe-coding]]", "[[extracts/x/bookmarks/2026-09-12-glaucia_lemos86-caraca-absurdo-isso-aqui-segui-o-conselho-do-pvncher-em-pedi--2096649629068624378|Revisão de artefatos de contexto entre modelos]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-evals-call-the-model-so-they-use-tokens-and-results-vary-pil--2098501003666702344|Evals de plugins no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-ibesh_tech-bcherny-the-review-bar-should-follow-blast-radius-not-who-wr--2098218598997336384|Code review e blast radius]]", "[[extracts/x/bookmarks/2026-09-12-poteto-new-in-dr-eggbot-v0-2-0-eggbot-can-do-a-health-check-on-all--2094967827019243547|Dr Eggbot rotinas health check]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-15-months-later-and-i-would-probably-now-describe-the-effect--2094787007184511082|Documentação exemplar do Effect]]"]
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
