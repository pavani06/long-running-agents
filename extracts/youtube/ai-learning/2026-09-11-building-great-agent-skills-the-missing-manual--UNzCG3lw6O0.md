---
title: "Building Great Agent Skills: The Missing Manual"
type: "extract"
source: "youtube"
video_id: "UNzCG3lw6O0"
url: "https://www.youtube.com/watch?v=UNzCG3lw6O0"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-building-great-agent-skills-the-missing-manual--UNzCG3lw6O0.txt]]"
tags: ["context-engineering", "context-management", "token-budgeting", "agent-tooling", "agentic-coding", "harness", "evals", "decision-discipline", "verification", "process"]
thesis: "Para escapar do 'skill hell', desenvolvedores e organizações precisam de um rubric compartilhado para avaliar e escrever skills de agentes, cobrindo quatro dimensões: trigger (invocação), structure (composição), steering (direcionamento do agente) e pruning (minimização)."
concepts: ["skill hell", "user-invoked vs model-invoked skills", "context load vs cognitive load", "context pointer", "description de skill como ponteiro de contexto", "steps e reference como unidades estruturais de uma skill", "external reference", "leading words", "leg work do agente por step", "ocultar steps futuros para aumentar esforço no step atual", "deletion test", "no-ops em skills", "sedimento (sediment) em documentação colaborativa", "single source of truth", "vertical slice", "human-in-the-loop checkpoint", "unpredictabilidade de invocação pelo modelo e necessidade de evals"]
tools: ["Matt Pocock skills repo (Matt's skills)", "writing great skills (skill)", "two-PRD (skill)", "grill with docs (skill)", "grill me (skill)", "codebase design (skill)", "domain modeling (skill)", "superpowers (conjunto de skills)", "plan mode (recurso de harness)", "aihero.dev (newsletter)", "AI coding crash course (curso planejado)", "skill.md"]
people: ["Matt Pocock", "AI Engineer World's Fair", "aihero.dev"]
claims: ["Decida explicitamente se cada skill é user-invoked ou model-invoked: skills model-invoked adicionam context load (a description entra no contexto a cada request e pode não ser invocada, exigindo evals), enquanto user-invoked impõem cognitive load no usuário.", "Estruture skills em duas unidades — steps (procedimento passo a passo) e reference (material de apoio) — escrevendo primeiro os steps e depois o reference material que eles precisam.", "Mantenha o skill.md o menor possível: skills menores são mais fáceis de manter, auditar e economizam tokens a cada request.", "Mova material de referência relevante apenas para um branch da skill para arquivos externos atrás de context pointers, em vez de mantê-lo no skill.md.", "Use leading words (ex.: 'vertical slice') repetidos consistentemente na skill para direcionar o comportamento do agente, e verifique sua eficácia observando se aparecem nos reasoning traces.", "Aumente o leg work de um step quebrando skills multi-step em skills separadas para que o agente veja apenas o step atual (ex.: separar 'ask clarifying questions' de 'create plan', como em grill-with-docs seguido de two-PRD).", "Aplique deletion tests: se remover um parágrafo da skill não muda o comportamento do agente, trata-se de um no-op e deve ser removido.", "Garanta single source of truth: não repita material de referência em múltiplos lugares dentro da skill.", "Pode skill com muito sedimento: verifique relevância por branch, mova material para o branch correto ou remova conteúdo irrelevante/stale.", "Use o flag 'disable model invocation: true' para tornar uma skill visível apenas ao usuário e invisível ao agente.", "Com 100 skills model-invoked, há 100 descriptions carregadas no contexto do agente a cada request.", "Use a skill 'writing great skills' do repo para auditar e melhorar skills próprias e de terceiros antes de adotá-las."]
deep_dive: "high"
deep_dive_reason: "O talk entrega um rubric concreto e denso em heurísticas acionáveis (context pointers, leading words, deletion tests, trade-off context load vs cognitive load) diretamente relevantes a harness, context-engineering e redução da necessidade de evals, com terminologia nova (no-ops, sediment, skill hell)."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-so-i-tried-matt-s-skills--0oXOOlqVu5M|So I tried Matt's skills...]]", "[[extracts/youtube/ai-learning/2026-09-11-don-t-ship-skills-without-evals-philipp-schmid-google-deepmind--0vphxNt4wyk|Don't Ship Skills Without Evals — Philipp Schmid, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt--mWvtOHlZM-I|Tool, skill, or subagent? Decomposing an agent that outgrew its prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-9-things-people-get-wrong-with-my-grill-skills--UzMNBN6xLLA|9 Things People Get Wrong With My /grill-* skills]]", "[[extracts/youtube/ai-learning/2026-09-11-handoff-is-my-new-favourite-skill--dtAJ2dOd3ko|/handoff is my new favourite skill]]", "[[extracts/youtube/ai-learning/2026-09-11-wayfinder-nothing-is-too-big-to-plan-anymore--F3lL98Pj90o|/wayfinder: Nothing is too big to plan anymore]]"]
theme: "Skills e conhecimento para agentes"
---

# Building Great Agent Skills: The Missing Manual

## Tese
Para escapar do 'skill hell', desenvolvedores e organizações precisam de um rubric compartilhado para avaliar e escrever skills de agentes, cobrindo quatro dimensões: trigger (invocação), structure (composição), steering (direcionamento do agente) e pruning (minimização).

## Conceitos-chave
- skill hell
- user-invoked vs model-invoked skills
- context load vs cognitive load
- context pointer
- description de skill como ponteiro de contexto
- steps e reference como unidades estruturais de uma skill
- external reference
- leading words
- leg work do agente por step
- ocultar steps futuros para aumentar esforço no step atual
- deletion test
- no-ops em skills
- sedimento (sediment) em documentação colaborativa
- single source of truth
- vertical slice
- human-in-the-loop checkpoint
- unpredictabilidade de invocação pelo modelo e necessidade de evals

## Ferramentas & pessoas
**Ferramentas:** Matt Pocock skills repo (Matt's skills), writing great skills (skill), two-PRD (skill), grill with docs (skill), grill me (skill), codebase design (skill), domain modeling (skill), superpowers (conjunto de skills), plan mode (recurso de harness), aihero.dev (newsletter), AI coding crash course (curso planejado), skill.md

**Pessoas/orgs:** Matt Pocock, AI Engineer World's Fair, aihero.dev

## Claims acionáveis
- Decida explicitamente se cada skill é user-invoked ou model-invoked: skills model-invoked adicionam context load (a description entra no contexto a cada request e pode não ser invocada, exigindo evals), enquanto user-invoked impõem cognitive load no usuário.
- Estruture skills em duas unidades — steps (procedimento passo a passo) e reference (material de apoio) — escrevendo primeiro os steps e depois o reference material que eles precisam.
- Mantenha o skill.md o menor possível: skills menores são mais fáceis de manter, auditar e economizam tokens a cada request.
- Mova material de referência relevante apenas para um branch da skill para arquivos externos atrás de context pointers, em vez de mantê-lo no skill.md.
- Use leading words (ex.: 'vertical slice') repetidos consistentemente na skill para direcionar o comportamento do agente, e verifique sua eficácia observando se aparecem nos reasoning traces.
- Aumente o leg work de um step quebrando skills multi-step em skills separadas para que o agente veja apenas o step atual (ex.: separar 'ask clarifying questions' de 'create plan', como em grill-with-docs seguido de two-PRD).
- Aplique deletion tests: se remover um parágrafo da skill não muda o comportamento do agente, trata-se de um no-op e deve ser removido.
- Garanta single source of truth: não repita material de referência em múltiplos lugares dentro da skill.
- Pode skill com muito sedimento: verifique relevância por branch, mova material para o branch correto ou remova conteúdo irrelevante/stale.
- Use o flag 'disable model invocation: true' para tornar uma skill visível apenas ao usuário e invisível ao agente.
- Com 100 skills model-invoked, há 100 descriptions carregadas no contexto do agente a cada request.
- Use a skill 'writing great skills' do repo para auditar e melhorar skills próprias e de terceiros antes de adotá-las.

> **Deep dive:** `high` — O talk entrega um rubric concreto e denso em heurísticas acionáveis (context pointers, leading words, deletion tests, trade-off context load vs cognitive load) diretamente relevantes a harness, context-engineering e redução da necessidade de evals, com terminologia nova (no-ops, sediment, skill hell).
