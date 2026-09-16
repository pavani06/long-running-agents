---
title: "Eval de plugins Claude Code"
type: "extract"
source: "x"
status_id: "2098501001447870499"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2098501001447870499"
created_at: "2026-09-11T19:56:41.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-start-in-your-plugin-s-folder-and-run-claude-plugin-eval-ini--2098501001447870499.json]]"
tags: ["evals", "agent-tooling", "testes-qa", "process"]
topic: "Eval de plugins Claude Code"
summary: "Anúncio do comando `claude plugin eval init`, que gera automaticamente uma suíte de evals para plugins do Claude Code a partir de exemplos reais e critérios de saída boa/ruína fornecidos pelo usuário, incluindo estimativa de custo da execução completa. Vale salvar por reduzir drasticamente a barreira de adicionar testes de qualidade a plugins de agentes."
key_points: ["Comando rodado na pasta do plugin (`claude plugin eval init`) inicializa a suíte de avaliação", "O desenvolvedor fornece critérios de saída boa/ruína e alguns prompts reais; o Claude redige os casos de teste e checks automaticamente", "Claude faz um piloto da suíte antes da execução completa e informa o custo estimado do run inteiro", "Abstrai o trabalho manual de escrever evals, integrando verificação de qualidade ao ciclo de desenvolvimento de plugins"]
entities: ["Claude Code", "claude plugin eval init", "Anthropic"]
content_type: "announcement"
revisit: "high"
grounded_in: "tweet"
links: []
media: []
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-claudedevs-new-in-claude-code-claude-plugin-eval-see-what-value-your-pl--2098500999656923145|Claude Code plugin evals]]", "[[extracts/x/bookmarks/2026-09-12-trq212-we-heard-feedback-that-it-s-hard-to-know-if-your-skills-are--2098531560643539440|Claude plugin evals]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-then-run-claude-plugin-eval-you-ll-see-each-case-s-score-wit--2098501002588823568|Claude plugin evaluation CLI]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-evals-call-the-model-so-they-use-tokens-and-results-vary-pil--2098501003666702344|Evals de plugins no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-rlancemartin-i-recently-added-this-command-to-the-claude-api-skill-run-it--2095170001175199771|Comando prompt-audit para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-here-s-how-our-team-uses-claude-tag-for-on-call-when-an-aler--2098508880921899197|On-call automation with Claude]]"]
theme: "Agentic Coding com Claude"
---

# Eval de plugins Claude Code

**@ClaudeDevs** · [2098501001447870499](https://x.com/ClaudeDevs/status/2098501001447870499) · `announcement`

## Resumo
Anúncio do comando `claude plugin eval init`, que gera automaticamente uma suíte de evals para plugins do Claude Code a partir de exemplos reais e critérios de saída boa/ruína fornecidos pelo usuário, incluindo estimativa de custo da execução completa. Vale salvar por reduzir drasticamente a barreira de adicionar testes de qualidade a plugins de agentes.

## Pontos-chave
- Comando rodado na pasta do plugin (`claude plugin eval init`) inicializa a suíte de avaliação
- O desenvolvedor fornece critérios de saída boa/ruína e alguns prompts reais; o Claude redige os casos de teste e checks automaticamente
- Claude faz um piloto da suíte antes da execução completa e informa o custo estimado do run inteiro
- Abstrai o trabalho manual de escrever evals, integrando verificação de qualidade ao ciclo de desenvolvimento de plugins

## Entidades
Claude Code, claude plugin eval init, Anthropic

> **Revisit:** `high` · **fonte:** `tweet`
