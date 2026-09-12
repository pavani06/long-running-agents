---
title: "Claude Fable 5 Use Cases You Must Do NOW (Or Lose Thousands in 1 Week)"
type: "extract"
source: "youtube"
video_id: "lplVBFr0Ndc"
url: "https://www.youtube.com/watch?v=lplVBFr0Ndc"
channel: "Chase AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-claude-fable-5-use-cases-you-must-do-now-or-lose-thousands-in-1-week--lplVBFr0Ndc.txt]]"
tags: ["agentic-coding", "model-selection", "token-budgeting", "multi-agent", "code-review", "spec-driven-development", "cross-session", "agent-loop", "stack-tooling", "process"]
thesis: "Com Fable 5 disponível por tempo limitado (50% do limite semanal dos planos max até 7 de julho), a estratégia é usar modelos mais baratos para planejar e reservar Fable 5 para executar cinco tipos de projetos de alto valor: clonar software, auditar sessões do Claude Code, construir um agentic OS, revisar codebases e criar software complexo guiado por PRD."
concepts: ["clone local de software existente (privacidade e customização)", "roteamento de modelos: planejamento com modelo barato, execução com modelo potente", "gestão de limite de uso (50% do plano semanal até 7 de julho)", "forward/goal para tarefas agênticas de longa duração com critérios de sucesso", "auditoria de sessões passadas com subagentes, clustering e decisão por cluster (skill/automação/correção/nada)", "agentic OS como wrapper web sobre Claude Code headless", "codificação de rotinas em skills e automações", "loop engineering aplicado a skills", "code review com revisores paralelos, deduplicação e triagem por severidade", "desenvolvimento guiado por PRD (spec-driven) parcialmente escrito por humano", "sessões autônomas longas de execução", "nuances de prompt entre modelos (Fable vs Mythos vs Opus) segundo documentação oficial"]
tools: ["Fable 5", "Opus 4.8", "Mythos", "Claude Code", "WhisperFlow", "Ollama", "Codeex", "Obsidian", "Three.js (3JS)", "Unreal Engine 5", "CLAUDE.md", "Deep Research / dynamic workflows", "forward/goal", "Claude App", "Claude Code Masterclass", "Chase AI Plus"]
people: ["Anthropic", "Chase (criador do vídeo / Chase AI Plus)", "Brapholk (criador do projeto open-source do jogo)"]
claims: ["Planeje os projetos antes de 7 de julho, pois Fable 5 fica limitado a 50% do limite semanal de uso dos planos max antes de migrar para pricing de API", "Deixe o trabalho braçal de planejamento para um modelo mais barato (ex.: Opus 4.8 com deep research/dynamic workflows) e entregue o plano pronto ao Fable 5 para conservar quota", "Não use dynamic workflows com Fable 5, pois queimará rapidamente o limite de uso", "Use prompts forward/goal com critérios de sucesso explícitos para projetos longos no Fable 5, que trabalhará até atingir o estado final", "Audite suas sessões passadas do Claude Code com subagentes que extraem sinais brutos dos transcripts, clusterizam entre sessões e decidem por cluster se é preciso nova skill, automação, correção ou nada — exigindo diagnóstico antes de executar", "Consulte a documentação oficial da Anthropic para prompting, pois há nuances entre Fable/Mythos e Opus", "Rode code review com múltiplos revisores paralelos: no exemplo, 45 achados brutos de 4 revisores foram deduplicados para 24 e triados por severidade com prioridade de correção", "Para software complexo, escreva um PRD (possivelmente iniciado com Opus 4.8) com alvo visual, pilares, instruções e constraints antes de entregar ao Fable 5", "O jogo em browser do Brapholk foi gerado a partir de um único PRD parcialmente humano, resultando em 21.000 linhas de TypeScript em 90+ commits", "Um agentic OS (web app sobre Claude Code headless, integrado ao Obsidian) pode ser empacotado e vendido por agências de IA ou distribuído a colegas que não usam CLI", "Claude Code headless não cobra mais via pricing de API, pois a Anthropic reverteu essa política semanas antes do vídeo"]
deep_dive: "medium"
deep_dive_reason: "Há padrões acionáveis concretos (roteamento de modelos, auditoria cross-session com subagentes, revisores paralelos com dedupe, PRD-driven), mas o formato é listicle de YouTube com segmento promocional e sem profundidade arquitetural ou novidade significativa."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-gpt-6-astra-fable-5-1-god-mode--KgKA0A3qlz0|GPT 6 Astra + Fable 5.1 = GOD MODE]]", "[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-i-tried-100-claude-code-skills-these-6-are-the-best--eRS3CmvrOvA|I Tried 100+ Claude Code Skills. These 6 Are The Best]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-field-guide-to-fable-thariq-shihipar-anthropic--9fubhllmsBU|Field Guide to Fable — Thariq Shihipar, Anthropic]]", "[[extracts/youtube/ai-learning/2026-09-11-this-claude-code-x-obsidian-agentic-os-will-be-the-new-meta--njHuj8OxIVI|This Claude Code x Obsidian Agentic OS Will Be The New Meta]]"]
---

# Claude Fable 5 Use Cases You Must Do NOW (Or Lose Thousands in 1 Week)

## Tese
Com Fable 5 disponível por tempo limitado (50% do limite semanal dos planos max até 7 de julho), a estratégia é usar modelos mais baratos para planejar e reservar Fable 5 para executar cinco tipos de projetos de alto valor: clonar software, auditar sessões do Claude Code, construir um agentic OS, revisar codebases e criar software complexo guiado por PRD.

## Conceitos-chave
- clone local de software existente (privacidade e customização)
- roteamento de modelos: planejamento com modelo barato, execução com modelo potente
- gestão de limite de uso (50% do plano semanal até 7 de julho)
- forward/goal para tarefas agênticas de longa duração com critérios de sucesso
- auditoria de sessões passadas com subagentes, clustering e decisão por cluster (skill/automação/correção/nada)
- agentic OS como wrapper web sobre Claude Code headless
- codificação de rotinas em skills e automações
- loop engineering aplicado a skills
- code review com revisores paralelos, deduplicação e triagem por severidade
- desenvolvimento guiado por PRD (spec-driven) parcialmente escrito por humano
- sessões autônomas longas de execução
- nuances de prompt entre modelos (Fable vs Mythos vs Opus) segundo documentação oficial

## Ferramentas & pessoas
**Ferramentas:** Fable 5, Opus 4.8, Mythos, Claude Code, WhisperFlow, Ollama, Codeex, Obsidian, Three.js (3JS), Unreal Engine 5, CLAUDE.md, Deep Research / dynamic workflows, forward/goal, Claude App, Claude Code Masterclass, Chase AI Plus

**Pessoas/orgs:** Anthropic, Chase (criador do vídeo / Chase AI Plus), Brapholk (criador do projeto open-source do jogo)

## Claims acionáveis
- Planeje os projetos antes de 7 de julho, pois Fable 5 fica limitado a 50% do limite semanal de uso dos planos max antes de migrar para pricing de API
- Deixe o trabalho braçal de planejamento para um modelo mais barato (ex.: Opus 4.8 com deep research/dynamic workflows) e entregue o plano pronto ao Fable 5 para conservar quota
- Não use dynamic workflows com Fable 5, pois queimará rapidamente o limite de uso
- Use prompts forward/goal com critérios de sucesso explícitos para projetos longos no Fable 5, que trabalhará até atingir o estado final
- Audite suas sessões passadas do Claude Code com subagentes que extraem sinais brutos dos transcripts, clusterizam entre sessões e decidem por cluster se é preciso nova skill, automação, correção ou nada — exigindo diagnóstico antes de executar
- Consulte a documentação oficial da Anthropic para prompting, pois há nuances entre Fable/Mythos e Opus
- Rode code review com múltiplos revisores paralelos: no exemplo, 45 achados brutos de 4 revisores foram deduplicados para 24 e triados por severidade com prioridade de correção
- Para software complexo, escreva um PRD (possivelmente iniciado com Opus 4.8) com alvo visual, pilares, instruções e constraints antes de entregar ao Fable 5
- O jogo em browser do Brapholk foi gerado a partir de um único PRD parcialmente humano, resultando em 21.000 linhas de TypeScript em 90+ commits
- Um agentic OS (web app sobre Claude Code headless, integrado ao Obsidian) pode ser empacotado e vendido por agências de IA ou distribuído a colegas que não usam CLI
- Claude Code headless não cobra mais via pricing de API, pois a Anthropic reverteu essa política semanas antes do vídeo

> **Deep dive:** `medium` — Há padrões acionáveis concretos (roteamento de modelos, auditoria cross-session com subagentes, revisores paralelos com dedupe, PRD-driven), mas o formato é listicle de YouTube com segmento promocional e sem profundidade arquitetural ou novidade significativa.
