---
title: "Skill de verificação para agentes"
type: "extract"
source: "x"
status_id: "2082874054483255805"
handle: "poteto"
url: "https://x.com/poteto/status/2082874054483255805"
created_at: "2026-07-30T17:00:47.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-poteto-pstack-now-includes-2-skills-i-recommend-everyone-use-or-cop--2082874054483255805.json]]"
tags: ["agent-tooling", "harness-engineering", "verification", "agentic-coding", "testes-qa", "process"]
topic: "Skill de verificação para agentes"
summary: "A skill /create-verification-skill do pstack gera uma skill project-local (.cursor/skills/verify-<app>/) que ensina um agente a lançar, dirigir e comprovar o comportamento real do app como um usuário faria, capturando evidências. É um blueprint denso e reutilizável para harnesses de verificação agent-driven em qualquer linguagem/framework."
key_points: ["A skill entrevista o codebase (Surface, Run, Drive, Observe, Isolate) e só pergunta ao usuário o que não pode observar; prefere harnesses existentes (Playwright/Cypress, expect, curl, porta de debug) antes de receitas genéricas (CDP, tmux/PTY, HTTP).", "Padrão de prova: exercitar o caminho real do usuário, não setters internos ou endpoints de teste; capturar ação + estado resultante + side effects (arquivos, linhas no DB, mensagens); mocks só onde já existe fronteira de produção; dry-runs são validados por observação, não pelo nome.", "Estrutura gerada: Launch (comando exato + sinal de pronto + teardown), Doctor (check read-only de saúde da instância), Drive (recipe com seletores estáveis reais do repo), Evidence, Cleanup (matar só o que iniciou, nunca por nome de processo; evidência sobrevive ao teardown) e Helpers executáveis.", "Inclui feature map (top 3-5 features, um arquivo por feature com sub-features, acesso POV usuário, driving com harness e gotchas) como fonte mantida de verdade da verificação; /maintain-verification-skill mantém o mapa honesto conforme o app muda.", "Uma skill gerada deve ser executada end-to-end uma vez (launch, doctor, drive de uma feature, evidence, cleanup, confirmar que a evidência sobreviveu) — nunca executada é rascunho, não entrega; e o cleanup roda também após iterações falhas para não deixar processos e portas órfãos."]
entities: ["pstack", "create-verification-skill", "maintain-verification-skill", "Cursor", "Playwright", "Cypress", "tmux", "Electron"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md", "https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-mattpocockuk-coming-soon-to-mattpocock-skills-retro-gives-you-opportuniti--2098062605407461744|Skill /retro para retroativa de agentes]]", "[[extracts/x/bookmarks/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098382953235562613|Skill de output direto para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-mattpocock-skills-v1-2-is-out-we-re-now-the-19th-most-starre--2084985277102031137|Lançamento mattpocock/skills v1.2]]", "[[extracts/x/bookmarks/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098020699365355709|Skill ADHD-friendly para agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-just-saw-a-comment-saying-that-i-ve-never-made-a-proper-over--2088290952704151671|Visão geral das 25 skills de agentes]]", "[[extracts/x/bookmarks/2026-09-12-daniel_mac8-oh-boy-this-is-amazingly-cool-very-happy-i-found-this-diagra--2097795113237762544|Skill de design de diagramas para agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-vibed-out-an-app-today-and-i-haven-t-looked-at-the-internals--2086838432102228008|Correção de arquitetura pós-vibe-coding]]", "[[extracts/x/bookmarks/2026-09-12-txbrraa-github-acaba-de-solucionar-el-mayor-problema-del-vibe-coding--2097955506891469272|GitHub Spec Kit e spec-driven development]]", "[[extracts/x/bookmarks/2026-09-12-coreyhainesco-i-made-a-skill-that-watches-videos-for-me-watch-video-youtub--2083953532903059846|AI skill para assistir vídeos]]"]
thin: false
theme: "Ecossistema Claude e Agentic Coding"
---

# Skill de verificação para agentes

**@poteto** · [2082874054483255805](https://x.com/poteto/status/2082874054483255805) · `tool`

## Resumo
A skill /create-verification-skill do pstack gera uma skill project-local (.cursor/skills/verify-<app>/) que ensina um agente a lançar, dirigir e comprovar o comportamento real do app como um usuário faria, capturando evidências. É um blueprint denso e reutilizável para harnesses de verificação agent-driven em qualquer linguagem/framework.

## Pontos-chave
- A skill entrevista o codebase (Surface, Run, Drive, Observe, Isolate) e só pergunta ao usuário o que não pode observar; prefere harnesses existentes (Playwright/Cypress, expect, curl, porta de debug) antes de receitas genéricas (CDP, tmux/PTY, HTTP).
- Padrão de prova: exercitar o caminho real do usuário, não setters internos ou endpoints de teste; capturar ação + estado resultante + side effects (arquivos, linhas no DB, mensagens); mocks só onde já existe fronteira de produção; dry-runs são validados por observação, não pelo nome.
- Estrutura gerada: Launch (comando exato + sinal de pronto + teardown), Doctor (check read-only de saúde da instância), Drive (recipe com seletores estáveis reais do repo), Evidence, Cleanup (matar só o que iniciou, nunca por nome de processo; evidência sobrevive ao teardown) e Helpers executáveis.
- Inclui feature map (top 3-5 features, um arquivo por feature com sub-features, acesso POV usuário, driving com harness e gotchas) como fonte mantida de verdade da verificação; /maintain-verification-skill mantém o mapa honesto conforme o app muda.
- Uma skill gerada deve ser executada end-to-end uma vez (launch, doctor, drive de uma feature, evidence, cleanup, confirmar que a evidência sobreviveu) — nunca executada é rascunho, não entrega; e o cleanup roda também após iterações falhas para não deixar processos e portas órfãos.

## Links
- https://github.com/cursor/plugins/blob/main/pstack/skills/create-verification-skill/SKILL.md
- https://github.com/cursor/plugins/blob/main/pstack/skills/maintain-verification-skill/SKILL.md

## Entidades
pstack, create-verification-skill, maintain-verification-skill, Cursor, Playwright, Cypress, tmux, Electron

> **Revisit:** `high` · **fonte:** `article`
