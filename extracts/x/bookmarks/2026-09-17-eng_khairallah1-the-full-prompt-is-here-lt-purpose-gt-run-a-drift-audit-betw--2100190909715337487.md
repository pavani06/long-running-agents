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
