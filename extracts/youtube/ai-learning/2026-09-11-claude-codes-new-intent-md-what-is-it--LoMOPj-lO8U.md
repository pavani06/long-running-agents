---
title: "Claude Codes New INTENT.MD, What is It?"
type: "extract"
source: "youtube"
video_id: "LoMOPj-lO8U"
url: "https://www.youtube.com/watch?v=LoMOPj-lO8U"
channel: "Rob Shocks"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-claude-codes-new-intent-md-what-is-it--LoMOPj-lO8U.txt]]"
tags: ["agent-loop", "agentic-coding", "agents", "arquitetura", "code-review", "context-engineering", "evals", "gate-design", "governanca", "harness", "monitoramento", "multi-agent", "permissions", "process", "production", "spec-driven-development", "stack-tooling", "testes-qa", "verification"]
thesis: "A tese central é que, no SDLC nativo de IA proposto pela Anthropic, o código deixou de ser o gargalo e o processo passou a ser, de modo que agentes devem ser aplicados a todas as etapas (planejamento, design, build, teste, deploy e manutenção) por meio de uma cadeia de artefatos legíveis por humanos e acionáveis por máquinas (intent.md → spec.md → plan.md), mantendo humanos apenas nos pontos críticos de revisão."
concepts: ["SDLC nativo de IA", "intent.md", "cadeia de artefatos (artifact chain)", "originador (originator)", "spec.md", "plan.md", "backlog triado por agentes", "hooks", "sub-agentes e paralelismo com git worktrees", "auto mode com permissões travadas", "blast radius do agente", "evals contínuos em CI", "revisão assíncrona de PR por agente", "gates de release e bloqueio de deploy", "manutenção autônoma acionada por eventos (Slack, schedule, métricas)", "governança com versionamento de artefatos", "métricas DORA", "human-in-the-loop", "checks determinísticos (linting e testes)", "contexto transferido via documentos entre agentes independentes"]
tools: ["Claude Code", "Cursor", "Codex", "Neon (MCP, CLI, skills, branching)", "Notion", "Linear", "Playwright", "Test Sprite", "Cursor Browser", "Cursor cloud agents", "Cursor bugbot", "Claude security review", "Git / git worktrees", "Skill: Switch Dimension Discovery", "Skill: Grill Me", "Skill: Requirements Discovery (Cursor)", "Superpowers", "BMAD"]
people: ["Anthropic", "Boris Cherny (transcrito como 'Baris Journey', criador do Claude Code)", "Switch Dimension (canal/curso do autor)", "Matt (autor do skill 'Grill Me')", "Neon"]
claims: ["Capture contexto fazendo o agente entrevistar o originador repetidamente até entender completamente o recurso/bug, sintetizando o resultado em um intent.md salvo numa pasta 'intent' padronizada.", "Qualquer pessoa (cliente, PM, dev) pode ser originador de um intent; cabe ao product owner revisá-los como backlog, e agentes podem triar esse backlog atribuindo tags, tamanho e prioridade.", "Ao commitar/assinar o intent, use um hook ou processo para gerar automaticamente o spec.md, aplicando guias de estilo e políticas organizacionais (agents.md, skills) como governança.", "O plan.md deve ser autossuficiente: um engenheiro ou agente independente deve conseguir implementar sem consultar intent ou spec, porque cada etapa do SDLC é executada por agentes/sub-agentes com contextos separados.", "Estruture o plano com arquivos a alterar, ordem de trabalho, riscos/restrições e critérios de sucesso com verificações determinísticas (lint e testes).", "Versione intent/spec/plan — quem tocou e como evoluíram — para rastrear indicadores líderes e atrasados e provar métricas DORA e a efetividade da IA no workflow.", "Use auto mode com permissões travadas (ferramentas, fontes web, pacotes) e blast radius controlado para acelerar o build com segurança.", "Use git worktrees para múltiplos agentes trabalharem em paralelo; divida o plano em tarefas independentes via sub-agentes (nativo no Cursor, Claude Code e Codex).", "Use hooks para manter o processo 'on rails': atualizar o plan.md após a implementação, bloquear pastas proibidas e impedir upgrades de pacotes npm não aprovados.", "Faça o agente testar o máximo possível antes de QA humano: escrever e rodar testes, lint, build e testes E2E com screenshots (Playwright, Test Sprite, Cursor cloud agents com screen recording).", "Colete ~20 issues resolvidas com resultados esperados e rode-as como evals contínuos no CI para detectar regressões a cada troca de modelo, skill ou mudança fundamental no processo.", "No deploy, o agente abre um PR e uma instância separada do Claude Code revisa assíncrona contra políticas e segurança (bugbot, claude security review), com hooks bloqueando o deploy sem permissão específica, aprovação humana ou gate de release.", "Na manutenção, triggers como alertas, mensagens no Slack, schedules ou degradação de métricas invocam o Claude sem intervenção humana, que diagnostica e gera seu próprio intent.md a partir de logs antes de propor sugestões.", "Padronize o workflow e evite mudá-lo com frequência para que equipe, agentes e skills operem o mesmo fluxo; não descarte frameworks existentes (Superpowers, BMAD) — não há one-size-fits-all."]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight acionável e arquitetural (cadeia de artefatos, hooks, gates de release, evals em CI, governança versionada) com novidade recente e relevância direta a harness, context-engineering, evals e gate-design."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-we-claude-code--IlqJqcl8ONE|How we Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-get-to-production-faster-with-claude-managed-agents--zenIB7XLZxQ|How to get to production faster with Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-proactive-agent-workflow-with-claude-code--eSP7PLTXNy8|Build a proactive agent workflow with Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]"]
---

# Claude Codes New INTENT.MD, What is It?

## Tese
A tese central é que, no SDLC nativo de IA proposto pela Anthropic, o código deixou de ser o gargalo e o processo passou a ser, de modo que agentes devem ser aplicados a todas as etapas (planejamento, design, build, teste, deploy e manutenção) por meio de uma cadeia de artefatos legíveis por humanos e acionáveis por máquinas (intent.md → spec.md → plan.md), mantendo humanos apenas nos pontos críticos de revisão.

## Conceitos-chave
- SDLC nativo de IA
- intent.md
- cadeia de artefatos (artifact chain)
- originador (originator)
- spec.md
- plan.md
- backlog triado por agentes
- hooks
- sub-agentes e paralelismo com git worktrees
- auto mode com permissões travadas
- blast radius do agente
- evals contínuos em CI
- revisão assíncrona de PR por agente
- gates de release e bloqueio de deploy
- manutenção autônoma acionada por eventos (Slack, schedule, métricas)
- governança com versionamento de artefatos
- métricas DORA
- human-in-the-loop
- checks determinísticos (linting e testes)
- contexto transferido via documentos entre agentes independentes

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Cursor, Codex, Neon (MCP, CLI, skills, branching), Notion, Linear, Playwright, Test Sprite, Cursor Browser, Cursor cloud agents, Cursor bugbot, Claude security review, Git / git worktrees, Skill: Switch Dimension Discovery, Skill: Grill Me, Skill: Requirements Discovery (Cursor), Superpowers, BMAD

**Pessoas/orgs:** Anthropic, Boris Cherny (transcrito como 'Baris Journey', criador do Claude Code), Switch Dimension (canal/curso do autor), Matt (autor do skill 'Grill Me'), Neon

## Claims acionáveis
- Capture contexto fazendo o agente entrevistar o originador repetidamente até entender completamente o recurso/bug, sintetizando o resultado em um intent.md salvo numa pasta 'intent' padronizada.
- Qualquer pessoa (cliente, PM, dev) pode ser originador de um intent; cabe ao product owner revisá-los como backlog, e agentes podem triar esse backlog atribuindo tags, tamanho e prioridade.
- Ao commitar/assinar o intent, use um hook ou processo para gerar automaticamente o spec.md, aplicando guias de estilo e políticas organizacionais (agents.md, skills) como governança.
- O plan.md deve ser autossuficiente: um engenheiro ou agente independente deve conseguir implementar sem consultar intent ou spec, porque cada etapa do SDLC é executada por agentes/sub-agentes com contextos separados.
- Estruture o plano com arquivos a alterar, ordem de trabalho, riscos/restrições e critérios de sucesso com verificações determinísticas (lint e testes).
- Versione intent/spec/plan — quem tocou e como evoluíram — para rastrear indicadores líderes e atrasados e provar métricas DORA e a efetividade da IA no workflow.
- Use auto mode com permissões travadas (ferramentas, fontes web, pacotes) e blast radius controlado para acelerar o build com segurança.
- Use git worktrees para múltiplos agentes trabalharem em paralelo; divida o plano em tarefas independentes via sub-agentes (nativo no Cursor, Claude Code e Codex).
- Use hooks para manter o processo 'on rails': atualizar o plan.md após a implementação, bloquear pastas proibidas e impedir upgrades de pacotes npm não aprovados.
- Faça o agente testar o máximo possível antes de QA humano: escrever e rodar testes, lint, build e testes E2E com screenshots (Playwright, Test Sprite, Cursor cloud agents com screen recording).
- Colete ~20 issues resolvidas com resultados esperados e rode-as como evals contínuos no CI para detectar regressões a cada troca de modelo, skill ou mudança fundamental no processo.
- No deploy, o agente abre um PR e uma instância separada do Claude Code revisa assíncrona contra políticas e segurança (bugbot, claude security review), com hooks bloqueando o deploy sem permissão específica, aprovação humana ou gate de release.
- Na manutenção, triggers como alertas, mensagens no Slack, schedules ou degradação de métricas invocam o Claude sem intervenção humana, que diagnostica e gera seu próprio intent.md a partir de logs antes de propor sugestões.
- Padronize o workflow e evite mudá-lo com frequência para que equipe, agentes e skills operem o mesmo fluxo; não descarte frameworks existentes (Superpowers, BMAD) — não há one-size-fits-all.

> **Deep dive:** `high` — Alta densidade de insight acionável e arquitetural (cadeia de artefatos, hooks, gates de release, evals em CI, governança versionada) com novidade recente e relevância direta a harness, context-engineering, evals e gate-design.
