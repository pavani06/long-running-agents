---
title: "Drift audit entre docs e código"
type: "extract"
source: "x"
status_id: "2100190909715337487"
handle: "eng_khairallah1"
url: "https://x.com/eng_khairallah1/status/2100190909715337487"
created_at: "2026-09-16T11:51:47.000Z"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-17-eng_khairallah1-the-full-prompt-is-here-lt-purpose-gt-run-a-drift-audit-betw--2100190909715337487.json]]"
tags: ["context-engineering", "agent-context", "documentation-as-code", "repo-as-context", "verification"]
topic: "Drift audit entre docs e código"
summary: "Prompt de Khairallah para auditar a divergência entre o que a documentação do projeto afirma e o que o código realmente faz, encontrando instruções stale que agentes seguem como contexto. Vale salvar como técnica de higiene de contexto em repositórios usados por agentes."
key_points: ["Executa um 'drift audit' apenas leitura: compara claims do projeto (docs/instruções) com o comportamento real do código e não muda nada", "Alvo explícito: achar instruções e documentação que o código não obedece mais (stale claims)", "Racional central: toda claim desatualizada é uma instrução que agentes seguem — docs stale contaminam o contexto e propagam erro", "Padrão 'purpose/focus' declarado no topo do prompt, compatível com uso como instrução de sistema para agentes"]
entities: ["@eng_khairallah1"]
content_type: "resource"
revisit: "high"
grounded_in: "tweet"
thin: false
links: []
media: []
theme: "Memória e Contexto de Agentes"
relates-to: ["[[extracts/x/bookmarks/2026-09-17-eng_khairallah1-send-this-prompt-to-gpt-astra-it-might-just-change-your-life--2100187890999263603|AGENTS.md desatualizado em codebases]]", "[[extracts/x/bookmarks/2026-09-12-rlancemartin-i-recently-added-this-command-to-the-claude-api-skill-run-it--2095170001175199771|Comando prompt-audit para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-sumanth_077-i-built-a-self-evolving-code-review-agent-most-code-review-a--2098416224803987968|Agente de code review auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-12-glaucia_lemos86-caraca-absurdo-isso-aqui-segui-o-conselho-do-pvncher-em-pedi--2096649629068624378|Revisão de artefatos de contexto entre modelos]]", "[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-16-mattpocockuk-retro-will-now-aggressively-look-for-opportunities-to-turn-f--2099859946053533933|Fuzzy rules viram checks determinísticos]]", "[[extracts/x/bookmarks/2026-09-12-bzuer_-victorosaraiva-pergunto-quem-e-jefferson-silva-quem-usa-hewl--2095704063081849159|verificação de metadados de documento]]"]
---

# Drift audit entre docs e código

**@eng_khairallah1** · [2100190909715337487](https://x.com/eng_khairallah1/status/2100190909715337487) · `resource`

## Resumo
Prompt de Khairallah para auditar a divergência entre o que a documentação do projeto afirma e o que o código realmente faz, encontrando instruções stale que agentes seguem como contexto. Vale salvar como técnica de higiene de contexto em repositórios usados por agentes.

## Pontos-chave
- Executa um 'drift audit' apenas leitura: compara claims do projeto (docs/instruções) com o comportamento real do código e não muda nada
- Alvo explícito: achar instruções e documentação que o código não obedece mais (stale claims)
- Racional central: toda claim desatualizada é uma instrução que agentes seguem — docs stale contaminam o contexto e propagam erro
- Padrão 'purpose/focus' declarado no topo do prompt, compatível com uso como instrução de sistema para agentes

## Entidades
@eng_khairallah1

> **Revisit:** `high` · **fonte:** `tweet`
