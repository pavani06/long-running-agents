---
title: "I Tried 100+ Claude Code Skills. These 6 Are The Best"
type: "extract"
source: "youtube"
video_id: "eRS3CmvrOvA"
url: "https://www.youtube.com/watch?v=eRS3CmvrOvA"
channel: "Nate Herk | AI Automation"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-i-tried-100-claude-code-skills-these-6-are-the-best--eRS3CmvrOvA.txt]]"
tags: ["agent-tooling", "agentic-coding", "agents", "context-engineering", "context-management", "memory-architecture", "token-budgeting", "code-review", "multi-agent", "testes-qa", "verification", "stack-tooling"]
thesis: "As seis competencias 'entediantes' de Claude Code (Skill Creator, Superpowers, GSD, /re e /ultrareview, Context Mode e Claude Mem) atacam os modos de falha reais de agentes de codigo (codigo apressado, context rot, perda de memoria entre sessoes), permitindo construir automacoes confiaveis a baixo custo e vender resultados de negocio em vez de workflows."
concepts: ["Skills vs. plugins (skill = skill.md que ensina uma tarefa; plugin = pacote com multiplas skills, hooks e servidores MCP)", "Context rot / degradacao na metade da janela de contexto", "Context engineering via subagentes com janelas de contexto limpas por tarefa", "Quality gates automatizados (scope reduction detection, security enforcement ancorada ao threat model)", "Code review estruturado com fleet de agentes revisores paralelos e verificacao independente de bugs (reproducao antes de reportar)", "Roteamento de saida de ferramentas por sandbox para filtrar dados brutos do contexto", "Snapshots de sessao persistidos em banco SQL local e reinjetados apos compaction", "Memoria cross-session capturada via Agent SDK, sumarios semanticos em SQLite com vector search", "Recuperacao em tres camadas (indice compacto, timeline, detalhes completos) para economia de tokens", "TDD aplicado a agentes: testes antes do codigo e auto-revisao em dois estagios (spec + qualidade)", "Vender outcomes (horas salvas, erros removidos, leads) em vez de workflows", "Skill Creator como fabrica meta: converter SOPs em skills reutilizaveis"]
tools: ["Claude Code", "Skill Creator (Anthropic)", "Superpowers", "GSD", "/review (/re)", "/ultrareview", "Context Mode", "Claude Mem", "Claude Design (Anthropic Labs)", "Agent SDK", "CLAUDE.md / arquivos de memoria", "Plugin marketplace do Claude Code", "Playwright", "GitHub", "SQLite", "Opus 4.7", "Skill oficial de front-end design (Anthropic)"]
people: ["Anthropic", "Anthropic Labs"]
claims: ["Instale o Skill Creator globalmente em user scope (/plugin install skill-creator) para invocacao automatica em qualquer projeto; ele construi, testa, itera e empacota skills a partir de descricao em linguagem natural ou SOPs, sem editar skill.md manualmente", "Superpowers forca planejamento antes de codar, ambiente isolado, testes antes do codigo e revisao em dois estagios, elevando a primeira passagem de ~60% para ~80% e reduzindo ciclos de debug e custo de tokens", "GSD resolve context rot spawning subagentes frescos com contexto limpo por tarefa, com gates de scope reduction detection e security enforcement, alem de modo autonomo que planeja, executa e commita a partir de um spec (com custo maior de tokens porem menos retrabalho)", "/re roda review estruturado local e gratuito; /ultrareview exige Claude Code >= 2.1.86 e login em conta Claude (API key nao funciona), roda 10-20 min em background na nuvem, da 3 execucoes gratis em planos Pro/Max e depois custa ~US$5-20 por run", "Use /ultrareview apenas antes de merges criticos (refactors grandes, payments, auth, migracoes de banco) onde um bug de producao custa mais que o review; bugs so aparecem na lista apos reproducao e verificacao independente", "Context Mode roteia chamadas de ferramentas por sandbox: benchmark publicado mostra snapshot Playwright de 56KB -> 299 bytes, access log de 46KB -> 155 bytes, e 315KB de saida bruta -> 5KB por sessao; monitore com /contextmode:ctx-st stats", "Context Mode rastreia cada evento relevante (edits, tarefas, decisoes, erros) em banco SQL local e reconstrói o snapshot da sessao apos compaction, estendendo sessoes viveis de ~30 min para ~3 horas", "Claude Mem captura o ciclo de vida da sessao via Agent SDK, comprime em sumarios semanticos armazenados em SQLite com vector search, usa recuperacao em tres camadas com ~10x economia de tokens vs. despejar historico, e auto-gera/atualiza CLAUDE.md por pasta; use apenas os dois comandos do plugin marketplace (o npm install do SDK nao registra os hooks)", "Instale a skill oficial de front-end design da Anthropic globalmente para reduzir aparencia de 'IA gerada'; Claude Design (Anthropic Labs) embute isso nativamente, mas reimportar o projeto no Claude Code requer a skill", "Para vender: posicione outcomes (10 horas/semana salvas, menos erro humano, mais leads) em vez de 'AI workflow'; iniciantes devem dominar uma unica skill, construir demos e mostrar valor, nao experiencia"]
deep_dive: "medium"
deep_dive_reason: "Ha densidade util de detalhes acionaveis sobre context-engineering, memoria entre sessoes e fleets de revisao com verificacao, mas e um roundup promocional de ferramentas existentes sem novidade arquitetural propria."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-so-i-tried-matt-s-skills--0oXOOlqVu5M|So I tried Matt's skills...]]", "[[extracts/youtube/ai-learning/2026-09-11-this-claude-code-x-obsidian-agentic-os-will-be-the-new-meta--njHuj8OxIVI|This Claude Code x Obsidian Agentic OS Will Be The New Meta]]", "[[extracts/youtube/ai-learning/2026-09-11-mastering-claude-code-in-30-minutes--6eBSHbLKuN0|Mastering Claude Code in 30 minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-pstack-is-agent-overkill-use-it-anyway--lUhXa8GiXns|Pstack Is Agent Overkill. Use It Anyway!]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-fable-5-use-cases-you-must-do-now-or-lose-thousands-in-1-week--lplVBFr0Ndc|Claude Fable 5 Use Cases You Must Do NOW (Or Lose Thousands in 1 Week)]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-3-7-is-pure-insanity--afN8U7kAiLc|Claude 3.7 is pure insanity]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-just-dropped-the-biggest-claude-code-update-yet--B-YQANvDOq0|Anthropic Just Dropped the Biggest Claude Code Update Yet]]"]
theme: "Codificação Agêntica com Claude Code"
---

# I Tried 100+ Claude Code Skills. These 6 Are The Best

## Tese
As seis competencias 'entediantes' de Claude Code (Skill Creator, Superpowers, GSD, /re e /ultrareview, Context Mode e Claude Mem) atacam os modos de falha reais de agentes de codigo (codigo apressado, context rot, perda de memoria entre sessoes), permitindo construir automacoes confiaveis a baixo custo e vender resultados de negocio em vez de workflows.

## Conceitos-chave
- Skills vs. plugins (skill = skill.md que ensina uma tarefa; plugin = pacote com multiplas skills, hooks e servidores MCP)
- Context rot / degradacao na metade da janela de contexto
- Context engineering via subagentes com janelas de contexto limpas por tarefa
- Quality gates automatizados (scope reduction detection, security enforcement ancorada ao threat model)
- Code review estruturado com fleet de agentes revisores paralelos e verificacao independente de bugs (reproducao antes de reportar)
- Roteamento de saida de ferramentas por sandbox para filtrar dados brutos do contexto
- Snapshots de sessao persistidos em banco SQL local e reinjetados apos compaction
- Memoria cross-session capturada via Agent SDK, sumarios semanticos em SQLite com vector search
- Recuperacao em tres camadas (indice compacto, timeline, detalhes completos) para economia de tokens
- TDD aplicado a agentes: testes antes do codigo e auto-revisao em dois estagios (spec + qualidade)
- Vender outcomes (horas salvas, erros removidos, leads) em vez de workflows
- Skill Creator como fabrica meta: converter SOPs em skills reutilizaveis

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Skill Creator (Anthropic), Superpowers, GSD, /review (/re), /ultrareview, Context Mode, Claude Mem, Claude Design (Anthropic Labs), Agent SDK, CLAUDE.md / arquivos de memoria, Plugin marketplace do Claude Code, Playwright, GitHub, SQLite, Opus 4.7, Skill oficial de front-end design (Anthropic)

**Pessoas/orgs:** Anthropic, Anthropic Labs

## Claims acionáveis
- Instale o Skill Creator globalmente em user scope (/plugin install skill-creator) para invocacao automatica em qualquer projeto; ele construi, testa, itera e empacota skills a partir de descricao em linguagem natural ou SOPs, sem editar skill.md manualmente
- Superpowers forca planejamento antes de codar, ambiente isolado, testes antes do codigo e revisao em dois estagios, elevando a primeira passagem de ~60% para ~80% e reduzindo ciclos de debug e custo de tokens
- GSD resolve context rot spawning subagentes frescos com contexto limpo por tarefa, com gates de scope reduction detection e security enforcement, alem de modo autonomo que planeja, executa e commita a partir de um spec (com custo maior de tokens porem menos retrabalho)
- /re roda review estruturado local e gratuito; /ultrareview exige Claude Code >= 2.1.86 e login em conta Claude (API key nao funciona), roda 10-20 min em background na nuvem, da 3 execucoes gratis em planos Pro/Max e depois custa ~US$5-20 por run
- Use /ultrareview apenas antes de merges criticos (refactors grandes, payments, auth, migracoes de banco) onde um bug de producao custa mais que o review; bugs so aparecem na lista apos reproducao e verificacao independente
- Context Mode roteia chamadas de ferramentas por sandbox: benchmark publicado mostra snapshot Playwright de 56KB -> 299 bytes, access log de 46KB -> 155 bytes, e 315KB de saida bruta -> 5KB por sessao; monitore com /contextmode:ctx-st stats
- Context Mode rastreia cada evento relevante (edits, tarefas, decisoes, erros) em banco SQL local e reconstrói o snapshot da sessao apos compaction, estendendo sessoes viveis de ~30 min para ~3 horas
- Claude Mem captura o ciclo de vida da sessao via Agent SDK, comprime em sumarios semanticos armazenados em SQLite com vector search, usa recuperacao em tres camadas com ~10x economia de tokens vs. despejar historico, e auto-gera/atualiza CLAUDE.md por pasta; use apenas os dois comandos do plugin marketplace (o npm install do SDK nao registra os hooks)
- Instale a skill oficial de front-end design da Anthropic globalmente para reduzir aparencia de 'IA gerada'; Claude Design (Anthropic Labs) embute isso nativamente, mas reimportar o projeto no Claude Code requer a skill
- Para vender: posicione outcomes (10 horas/semana salvas, menos erro humano, mais leads) em vez de 'AI workflow'; iniciantes devem dominar uma unica skill, construir demos e mostrar valor, nao experiencia

> **Deep dive:** `medium` — Ha densidade util de detalhes acionaveis sobre context-engineering, memoria entre sessoes e fleets de revisao com verificacao, mas e um roundup promocional de ferramentas existentes sem novidade arquitetural propria.
