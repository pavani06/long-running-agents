---
title: "Evals de plugins no Claude Code"
type: "extract"
source: "x"
status_id: "2098501003666702344"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2098501003666702344"
created_at: "2026-09-11T19:56:42.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-evals-call-the-model-so-they-use-tokens-and-results-vary-pil--2098501003666702344.json]]"
tags: ["evals", "harness", "agent-tooling", "testes-qa", "verification", "token-budgeting"]
topic: "Evals de plugins no Claude Code"
summary: "Documentação do `claude plugin eval`, que roda plugins do Claude Code contra suítes de casos com graders (regex, tool_used, LLM-judge) e compara com baseline sem plugin (Δ) para medir a contribuição real; cada run consome tokens reais da conta, então pilotar com --runs 1 antes do run completo."
key_points: ["Graders vêm em 6 tipos: regex, tool_used, tool_order e file_exists são computados do transcript/arquivos e custam zero; llm e baseline chamam um modelo juiz (pequeno/rápido por padrão, --judge-model sonnet para rubricas sutis) e somam ao custo.", "Cada caso roda em dois braços por padrão (com e sem plugin) e 3 vezes cada; Δ = score WITH - W/OUT isola o que o plugin contribuiu — score alto nos dois braços significa que o plugin não foi o responsável; --ablation none dobra a economia ao iterar.", "`claude plugin eval init` gera a suíte automaticamente: lê o plugin, propõe prompts que devem/não devem dispará-lo, pilota os graders uma vez e escreve os arquivos; achado comum inicial é Δ~0 com grader tool_used: Skill falhando, indicando que a description da skill precisa de ajuste.", "Receita para sinal estável: regex grader para saídas longas (determinístico), llm grader só para saídas curtas com rubrica de condições PASS/FAIL concretas; combine um grader de resultado com um de processo (tool_used/tool_order); Δ negativo com skill disparada sugere juiz fraco, não plugin ruim.", "Custo e segurança: cada run e juiz é chamada real no plano/API (~casos × runs + baseline + 3 juízes por grader llm por run); hooks e servidores MCP do plugin rodam como o usuário, então só avaliar plugins confiáveis; graders arm: with-only são excluídos da pontuação nos dois braços para manter comparabilidade."]
entities: ["Claude Code", "claude plugin eval", "claude plugin eval init", "@ClaudeDevs", "MCP", "Claude Sonnet", "skill-creator"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://code.claude.com/docs/en/plugin-evals"]
media: []
---

# Evals de plugins no Claude Code

**@ClaudeDevs** · [2098501003666702344](https://x.com/ClaudeDevs/status/2098501003666702344) · `resource`

## Resumo
Documentação do `claude plugin eval`, que roda plugins do Claude Code contra suítes de casos com graders (regex, tool_used, LLM-judge) e compara com baseline sem plugin (Δ) para medir a contribuição real; cada run consome tokens reais da conta, então pilotar com --runs 1 antes do run completo.

## Pontos-chave
- Graders vêm em 6 tipos: regex, tool_used, tool_order e file_exists são computados do transcript/arquivos e custam zero; llm e baseline chamam um modelo juiz (pequeno/rápido por padrão, --judge-model sonnet para rubricas sutis) e somam ao custo.
- Cada caso roda em dois braços por padrão (com e sem plugin) e 3 vezes cada; Δ = score WITH - W/OUT isola o que o plugin contribuiu — score alto nos dois braços significa que o plugin não foi o responsável; --ablation none dobra a economia ao iterar.
- `claude plugin eval init` gera a suíte automaticamente: lê o plugin, propõe prompts que devem/não devem dispará-lo, pilota os graders uma vez e escreve os arquivos; achado comum inicial é Δ~0 com grader tool_used: Skill falhando, indicando que a description da skill precisa de ajuste.
- Receita para sinal estável: regex grader para saídas longas (determinístico), llm grader só para saídas curtas com rubrica de condições PASS/FAIL concretas; combine um grader de resultado com um de processo (tool_used/tool_order); Δ negativo com skill disparada sugere juiz fraco, não plugin ruim.
- Custo e segurança: cada run e juiz é chamada real no plano/API (~casos × runs + baseline + 3 juízes por grader llm por run); hooks e servidores MCP do plugin rodam como o usuário, então só avaliar plugins confiáveis; graders arm: with-only são excluídos da pontuação nos dois braços para manter comparabilidade.

## Links
- https://code.claude.com/docs/en/plugin-evals

## Entidades
Claude Code, claude plugin eval, claude plugin eval init, @ClaudeDevs, MCP, Claude Sonnet, skill-creator

> **Revisit:** `high` · **fonte:** `article`
