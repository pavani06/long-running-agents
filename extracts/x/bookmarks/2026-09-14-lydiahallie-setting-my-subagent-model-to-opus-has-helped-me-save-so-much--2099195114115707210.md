---
title: "Roteamento de modelo para subagentes"
type: "extract"
source: "x"
status_id: "2099195114115707210"
handle: "lydiahallie"
url: "https://x.com/lydiahallie/status/2099195114115707210"
created_at: "2026-09-13T17:54:51.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-lydiahallie-setting-my-subagent-model-to-opus-has-helped-me-save-so-much--2099195114115707210.json]]"
tags: ["model-selection", "agent-tooling", "stack-tooling", "token-budgeting", "performance"]
topic: "Roteamento de modelo para subagentes"
summary: "Dica prática do Claude Code: definir um modelo mais barato (Opus) para subagentes via CLAUDE_CODE_SUBAGENT_MODEL economiza bastante cota do modelo principal (Fable 5.1), que tende a spawnar subagentes com frequência. Vale salvar como padrão de configuração para reduzir consumo sem perder qualidade nas tarefas principais."
key_points: ["Fable 5.1 (modelo principal) usa subagentes com muita frequência, o que consome cota do modelo caro desnecessariamente", "A maioria das tarefas delegadas a subagentes (busca, coleta de contexto, verificações simples) não exige raciocínio de nível frontier", "Basta exportar CLAUDE_CODE_SUBAGENT_MODEL=opus para rotear todos os subagentes a um modelo mais barato, mantendo o modelo principal só para o loop central", "O ganho é direto em custo/uso (usage), sem perda perceptível de qualidade na maioria dos fluxos"]
entities: ["Claude Code", "Fable 5.1", "Opus", "Lydia Hallie"]
content_type: "tool"
revisit: "medium"
grounded_in: "tweet"
thin: false
links: []
media: []
---

# Roteamento de modelo para subagentes

**@lydiahallie** · [2099195114115707210](https://x.com/lydiahallie/status/2099195114115707210) · `tool`

## Resumo
Dica prática do Claude Code: definir um modelo mais barato (Opus) para subagentes via CLAUDE_CODE_SUBAGENT_MODEL economiza bastante cota do modelo principal (Fable 5.1), que tende a spawnar subagentes com frequência. Vale salvar como padrão de configuração para reduzir consumo sem perder qualidade nas tarefas principais.

## Pontos-chave
- Fable 5.1 (modelo principal) usa subagentes com muita frequência, o que consome cota do modelo caro desnecessariamente
- A maioria das tarefas delegadas a subagentes (busca, coleta de contexto, verificações simples) não exige raciocínio de nível frontier
- Basta exportar CLAUDE_CODE_SUBAGENT_MODEL=opus para rotear todos os subagentes a um modelo mais barato, mantendo o modelo principal só para o loop central
- O ganho é direto em custo/uso (usage), sem perda perceptível de qualidade na maioria dos fluxos

## Entidades
Claude Code, Fable 5.1, Opus, Lydia Hallie

> **Revisit:** `medium` · **fonte:** `tweet`
