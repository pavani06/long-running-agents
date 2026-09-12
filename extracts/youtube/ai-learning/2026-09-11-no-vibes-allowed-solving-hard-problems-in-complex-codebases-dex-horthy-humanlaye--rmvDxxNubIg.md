---
title: "No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer"
type: "extract"
source: "youtube"
video_id: "rmvDxxNubIg"
url: "https://www.youtube.com/watch?v=rmvDxxNubIg"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg.txt]]"
tags: ["context-engineering", "context-management", "token-budgeting", "memory-architecture", "agent-loop", "agentic-coding", "multi-agent", "agent-tooling", "harness-engineering", "knowledge-management", "code-review", "verification", "process", "stack-tooling", "ontologia"]
thesis: "O gargalo dominante de agentes de código é a gestão da janela de contexto: com compação intencional, sub-agentes usados para controle de contexto e o fluxo research→plan→implement, equipes obtêm 2-3x de throughput sem 'slop' mesmo em codebases brownfield complexos."
concepts: ["engenharia de contexto (context engineering)", "compação intencional (intentional compaction)", "zona 'dumb' da janela de contexto (~40% de uso como limiar de retornos decrescentes)", "sub-agentes para controle de contexto (não para antropomorfizar papéis)", "fluxo research→plan→implement (RPI)", "alinhamento mental como propósito real do code review", "compressão de verdade (research) vs. compressão de intenção (plan)", "difusão semântica de termos (ex.: 'spec-driven development', 'agent')", "onboarding de agentes e contexto compactado sob demanda", "divulgação progressiva / sharding de contexto por nível do monorepo", "trajetória da conversa condiciona a continuação do LLM (gritar corrói o contexto)", "harness engineering como customização dos pontos de integração do agente", "trade-off plano longo: mais confiabilidade de execução, menos legibilidade", "calibrar o peso do processo ao tamanho da tarefa (de mudar cor de botão a multi-repo)", "documentação estática interna apodrece ('quantidade de mentiras' cresce do código aos docs)", "mudança cultural top-down do SDLC para um mundo com 99% de código gerado por IA"]
tools: ["Claude Code", "Cursor", "Codex", "MCPs", "GitHub", "AMP", "BAML (Boundary ML)", "Parquet Java", "Hadoop", "Jira", "Linear", "Vercel", "CLAUDE.md/hooks", "HackerNews"]
people: ["Dex (ponente)", "Yegor/Eigor (survey de 100k devs)", "Vib (CEO da Boundary ML)", "Jeff Huntley", "Birgitta ('Brietta') da ThoughtWorks", "Martin Fowler", "Simon Willison", "Sean (swyx)", "Jake (blog post sobre human-in-the-loop)", "Mitchell (post sobre threads de AMP em PRs)", "Peter", "Blake", "Boundary ML", "ThoughtWorks"]
claims: ["Em vez de resteerear um agente fora de trilha, inicie nova janela de contexto com a mesma tarefa e uma instrução do caminho que falhou", "Compação intencional: peça ao agente que comprima o contexto em um arquivo markdown revisável e usável como ponto de partida do próximo agente", "Mantenha o uso da janela abaixo de ~40% ('smart zone'); quanto mais tokens usados, piores os resultados", "Use sub-agentes para delegar leitura/busca em codebases grandes e retornar apenas um resumo sucinto ao agente pai — não para papéis como 'QA sub-agent' ou 'frontend sub-agent'", "Estruture o trabalho em research (entender o sistema, objetivo) → plan (passos exatos com arquivos, linhas e snippets de código) → implement (execução com contexto baixo)", "Inclua snippets reais de código nos planos para alavancar execução confiável; um plano legível pode ser lido por um modelo fraco sem erro", "Prefira contexto compactado sob demanda (snapshots de research derivados do código-fonte verdadeiro) a documentos de onboarding estáticos que ficam desatualizados", "Shard o onboarding progressivamente: contexto raiz no repo + subcontextos por diretório, puxando só o necessário", "Cuidado com trajetória: sequências de erro→bronca no histórico tornam 'errar de novo' a continuação mais provável", "Riscos de ordem no pipeline: uma linha ruim de research contamina tudo; uma parte ruim de plano vale ~100 linhas ruins de código", "Anexe threads/prompts do agente aos PRs para levar o revisor pela jornada (prática do Mitchell com AMP), sustentando alinhamento mental em times que enviam 2-3x mais código", "Não terceirize o pensamento: o humano deve ler e validar research e planos; não existe prompt perfeito nem bala de prata", "Calibre o processo ao tamanho da tarefa: conversa direta para trivia, research+plan para features multi-repo", "Escolha uma ferramenta e acumule reps; evite min-maxing entre Claude Code, Codex, Cursor etc.", "Desconfie de ferramentas que geram monte de markdown só para agradar — spec-driven development como termo sofreu difusão semântica e está inútil", "A adoção de IA requer mudança cultural vinda do topo; senão staff/seniors ficam limpando o slop dos mid-levels"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de práticas acionáveis e arquiteturais diretamente relevantes a context-engineering e harness (limiar de ~40% da janela, compação intencional, sub-agentes como controle de contexto, RPI, divulgação progressiva de onboarding), com novidade e consequências organizacionais concretas."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-why-more-context-makes-your-agent-dumber-and-what-to-do-about-it-nupur-sharma-qo--EcqMYoIV57A|Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo]]", "[[extracts/youtube/ai-learning/2026-09-11-full-walkthrough-workflow-for-ai-coding-matt-pocock---QFHIoCo-Ko|Full Walkthrough: Workflow for AI Coding — Matt Pocock]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-frontrunners-say-coding-is-solved-but-engineering-is-not--Q7l8YGiMgUw|Why the Frontrunners Say Coding Is Solved BUT Engineering is Not]]", "[[extracts/youtube/ai-learning/2026-09-11-your-attention-is-the-bottleneck-not-your-agents-zack-proser-workos--so9l_MwS2yg|Your Attention Is the Bottleneck, Not Your Agents — Zack Proser, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-understanding-is-the-new-bottleneck-geoffrey-litt-notion--WkBPX-oDMnA|Understanding is the new bottleneck — Geoffrey Litt, Notion]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-solved-context-management-in-agents-sally-ann-delucia--esY99nYXxR4|How we solved Context Management in Agents — Sally-Ann Delucia]]", "[[extracts/youtube/ai-learning/2026-09-11-everything-we-got-wrong-about-research-plan-implement-dexter-horthy--YwZR6tc7qYg|Everything We Got Wrong About Research-Plan-Implement -  Dexter Horthy]]", "[[extracts/youtube/ai-learning/2026-09-11-bdd-adr-prd-wtf-capturing-decisions-for-humans-and-ai-alike-michal-cichra-safe-i--504PvfXou5Y|BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike — Michal Cichra, Safe Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-ci-cd-is-dead-agents-need-continuous-compute-and-computers-hugo-santos-and-madis--VktrqzQgytY|CI/CD Is Dead, Agents Need Continuous Compute and Computers — Hugo Santos and Madison Faulkner]]", "[[extracts/youtube/ai-learning/2026-09-11-the-new-code-sean-grove-openai--8rABwKRsec4|The New Code — Sean Grove, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-your-company-brain-will-leak-secrets-how-we-stopped-it-for-big-banks-tanmai-gopa--0uC6u0lJJl4|Your company brain will leak secrets: how we stopped it for big banks — Tanmai Gopal, PromptQL]]", "[[extracts/youtube/ai-learning/2026-09-11-beyond-the-prompt-goodbye-slop-welcome-determinism-david-khourshid--uMvTAF280so|Beyond the Prompt: \"Goodbye slop; welcome determinism\" David Khourshid]]", "[[extracts/youtube/ai-learning/2026-09-11-handoff-is-my-new-favourite-skill--dtAJ2dOd3ko|/handoff is my new favourite skill]]", "[[extracts/youtube/ai-learning/2026-09-11-the-end-of-the-static-screen-architecting-intent-driven-ux-gus-iwanaga-commercet--QrMcNe2jjt8|The End of the Static Screen: Architecting Intent-Driven UX — Gus Iwanaga, commercetools]]", "[[extracts/youtube/ai-learning/2026-09-11-headroom-a-context-optimization-layer-for-llm-applications-tejas-chopra-netflix--UOWSHg18cL0|Headroom: A Context Optimization Layer for LLM Applications - Tejas Chopra, Netflix, Inc.]]", "[[extracts/youtube/ai-learning/2026-09-11-systems-thinking-for-leaders-designing-solutions-that-work--wSuQQYv-E64|Systems Thinking for Leaders: Designing Solutions That Work]]"]
---

# No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer

## Tese
O gargalo dominante de agentes de código é a gestão da janela de contexto: com compação intencional, sub-agentes usados para controle de contexto e o fluxo research→plan→implement, equipes obtêm 2-3x de throughput sem 'slop' mesmo em codebases brownfield complexos.

## Conceitos-chave
- engenharia de contexto (context engineering)
- compação intencional (intentional compaction)
- zona 'dumb' da janela de contexto (~40% de uso como limiar de retornos decrescentes)
- sub-agentes para controle de contexto (não para antropomorfizar papéis)
- fluxo research→plan→implement (RPI)
- alinhamento mental como propósito real do code review
- compressão de verdade (research) vs. compressão de intenção (plan)
- difusão semântica de termos (ex.: 'spec-driven development', 'agent')
- onboarding de agentes e contexto compactado sob demanda
- divulgação progressiva / sharding de contexto por nível do monorepo
- trajetória da conversa condiciona a continuação do LLM (gritar corrói o contexto)
- harness engineering como customização dos pontos de integração do agente
- trade-off plano longo: mais confiabilidade de execução, menos legibilidade
- calibrar o peso do processo ao tamanho da tarefa (de mudar cor de botão a multi-repo)
- documentação estática interna apodrece ('quantidade de mentiras' cresce do código aos docs)
- mudança cultural top-down do SDLC para um mundo com 99% de código gerado por IA

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Cursor, Codex, MCPs, GitHub, AMP, BAML (Boundary ML), Parquet Java, Hadoop, Jira, Linear, Vercel, CLAUDE.md/hooks, HackerNews

**Pessoas/orgs:** Dex (ponente), Yegor/Eigor (survey de 100k devs), Vib (CEO da Boundary ML), Jeff Huntley, Birgitta ('Brietta') da ThoughtWorks, Martin Fowler, Simon Willison, Sean (swyx), Jake (blog post sobre human-in-the-loop), Mitchell (post sobre threads de AMP em PRs), Peter, Blake, Boundary ML, ThoughtWorks

## Claims acionáveis
- Em vez de resteerear um agente fora de trilha, inicie nova janela de contexto com a mesma tarefa e uma instrução do caminho que falhou
- Compação intencional: peça ao agente que comprima o contexto em um arquivo markdown revisável e usável como ponto de partida do próximo agente
- Mantenha o uso da janela abaixo de ~40% ('smart zone'); quanto mais tokens usados, piores os resultados
- Use sub-agentes para delegar leitura/busca em codebases grandes e retornar apenas um resumo sucinto ao agente pai — não para papéis como 'QA sub-agent' ou 'frontend sub-agent'
- Estruture o trabalho em research (entender o sistema, objetivo) → plan (passos exatos com arquivos, linhas e snippets de código) → implement (execução com contexto baixo)
- Inclua snippets reais de código nos planos para alavancar execução confiável; um plano legível pode ser lido por um modelo fraco sem erro
- Prefira contexto compactado sob demanda (snapshots de research derivados do código-fonte verdadeiro) a documentos de onboarding estáticos que ficam desatualizados
- Shard o onboarding progressivamente: contexto raiz no repo + subcontextos por diretório, puxando só o necessário
- Cuidado com trajetória: sequências de erro→bronca no histórico tornam 'errar de novo' a continuação mais provável
- Riscos de ordem no pipeline: uma linha ruim de research contamina tudo; uma parte ruim de plano vale ~100 linhas ruins de código
- Anexe threads/prompts do agente aos PRs para levar o revisor pela jornada (prática do Mitchell com AMP), sustentando alinhamento mental em times que enviam 2-3x mais código
- Não terceirize o pensamento: o humano deve ler e validar research e planos; não existe prompt perfeito nem bala de prata
- Calibre o processo ao tamanho da tarefa: conversa direta para trivia, research+plan para features multi-repo
- Escolha uma ferramenta e acumule reps; evite min-maxing entre Claude Code, Codex, Cursor etc.
- Desconfie de ferramentas que geram monte de markdown só para agradar — spec-driven development como termo sofreu difusão semântica e está inútil
- A adoção de IA requer mudança cultural vinda do topo; senão staff/seniors ficam limpando o slop dos mid-levels

> **Deep dive:** `high` — Alta densidade de práticas acionáveis e arquiteturais diretamente relevantes a context-engineering e harness (limiar de ~40% da janela, compação intencional, sub-agentes como controle de contexto, RPI, divulgação progressiva de onboarding), com novidade e consequências organizacionais concretas.
