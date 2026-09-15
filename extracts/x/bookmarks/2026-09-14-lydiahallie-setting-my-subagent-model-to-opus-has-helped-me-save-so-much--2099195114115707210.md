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
relates-to: ["[[extracts/x/bookmarks/2026-09-14-addyosmani-get-more-out-of-your-fable-usage-by-using-opus-for-subagents--2099210491059122471|Opus como modelo de subagents]]", "[[extracts/x/bookmarks/2026-09-12-daniel_mac8-fable-advisor-now-uses-opus-5-as-orchestrator-opus-5-shines--2081056595555868752|fable-advisor com Opus 5 como orquestrador]]", "[[extracts/x/bookmarks/2026-09-12-keepgoings0-oalanicolas-from-my-experience-for-the-orchestrator-astra-xh--2097766199450829151|seleção de modelos por papel de agente]]", "[[extracts/x/bookmarks/2026-09-12-stretchcloud-spotify-s-engineering-team-cut-claude-code-token-usage-by-90--2096439998539321653|Portal: roteamento de dois modelos no Claude Code]]", "[[extracts/x/bookmarks/2026-09-14-andrewchen-ethereaglehq-classifies-it-upfront-but-the-way-i-set-up-the--2099278183837397469|model selection com escalonamento]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420|Arquitetura de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-voxyz_ai-codex-tip-a-cost-efficient-luna-sol-agent-tree-orchestrated--2097814698204832116|orquestração de agentes com Codex]]", "[[extracts/x/bookmarks/2026-09-14-ethereaglehq-andrewchen-upfront-classify-then-upgrade-if-it-gets-long-is--2099290400779317310|gatilhos de complexidade em agentes]]", "[[extracts/x/bookmarks/2026-09-14-ethereaglehq-andrewchen-arch-router-picking-local-vs-cloud-is-the-piece-i--2099260781447496188|roteamento de modelos local vs cloud]]", "[[extracts/x/bookmarks/2026-09-12-voxyz_ai-a-lot-of-people-have-asked-how-to-configure-this-cost-effici--2098033757504634982|Configuração de agent tree com Codex]]", "[[extracts/x/bookmarks/2026-09-12-claudeai-we-re-making-claude-sonnet-5-s-introductory-pricing-permanen--2086891169217122586|Preço permanente do Claude Sonnet 5]]"]
theme: "Tooling e arquitetura de agentes"
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
