---
title: "Full Walkthrough: Workflow for AI Coding — Matt Pocock"
type: "extract"
source: "youtube"
video_id: "-QFHIoCo-Ko"
url: "https://www.youtube.com/watch?v=-QFHIoCo-Ko"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-full-walkthrough-workflow-for-ai-coding-matt-pocock---QFHIoCo-Ko.txt]]"
tags: ["context-engineering", "context-management", "token-budgeting", "harness", "agent-loop", "agent-fleets", "multi-agent", "agentic-coding", "spec-driven-development", "process", "state", "arquitetura", "decision-discipline", "verification"]
thesis: "Fundamentos clássicos de engenharia de software (tarefas pequenas, tracer bullets, kanban com dependências) continuam sendo a forma mais eficaz de estruturar trabalho com agentes de IA, em vez de tratar IA como um paradigma completamente novo."
concepts: ["smart zone vs dumb zone (degradação quadrática da atenção com o tamanho do contexto)", "compacting vs limpar contexto (metáfora de Memento / estado determinístico)", "sub-agentes com contexto isolado reportando sumários", "grill me skill / entrevista relentless para entendimento compartilhado", "design concept compartilhado (Frederick P. Brooks)", "crítica ao movimento specs-to-code (vibe coding por outro nome)", "PRD como documento de destino (destination document)", "issues independentemente agarráveis (independently grabbable)", "vertical slices / tracer bullets para feedback rápido entre camadas", "kanban com relações de bloqueio formando DAGs para paralelização de agentes", "tarefas human-in-the-loop vs AFK (away from keyboard)", "Ralph Wiggum como prática de loop incremental", "loops de fase n em vez de planos multifásicos numerados", "posse do stack de planejamento (inversão de controle)", "bad codebases make bad agents", "estágios de uma sessão: system prompt, exploração, implementação, teste"]
tools: ["Claude Code", "Opus", "Gemini Meetings", "Slido", "Tldraw", "Cucumber", "GitHub Issues", "skill grill-me", "skill write-a-PRD", "skill PRD-to-issues", "status line de contagem de tokens"]
people: ["Matt (Matt Pocock / AI Hero)", "Dex (HumanLayer)", "Martin Fowler", "Pragmatic Programmer", "Frederick P. Brooks", "Sarah Chen (cliente fictícia)", "Anthropic", "GitHub"]
claims: ["Cerca de 100k tokens é o limite prático do smart zone independentemente da janela (1M); janelas maiores servem para retrieval, não para coding", "Prefira limpar o contexto a compactar, pois o estado inicial é sempre o mesmo e pode ser otimizado", "Dimensione tarefas para caber inteiramente no smart zone em vez de oscilar entre smart e dumb zone", "Use entrevistas interativas (grill me) para alcançar um design concept compartilhado com o agente em vez de gerar e ler planos", "Não revise PRDs gerados após uma sessão de alinhamento: você estaria testando apenas a sumarização do LLM", "Quebre PRDs em issues com fatias verticais (tracer bullets) que atravessem todas as camadas para obter feedback imediato e integrado", "Force o agente a evitar fatias horizontais (camada por camada), pois atrasam o feedback até as fases finais", "Modele planos como kanban com dependências de bloqueio (DAG) para permitir execução paralela por múltiplos agentes", "Classifique tarefas como human-in-the-loop (planejamento, alinhamento) ou AFK (implementação) e mantenha humanos apenas nas primeiras", "Use sub-agentes de exploração com contexto isolado para não inflar o contexto do agente orquestrador", "Exiba a contagem exata de tokens em toda sessão de coding para saber a distância até o dumb zone", "Possua seu stack de planejamento em vez de depender de frameworks prontos, para ter observabilidade e capacidade de correção", "Práticas de livros clássicos (20+ anos) verbalizadas em inglês são material excelente para prompts", "Bases de código ruins produzem agentes ruins; entender profundamente o código melhora os resultados com IA", "Sessões com stakeholders podem ser gravadas, transcritas e alimentadas em sessões de grilling para validar suposições"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de práticas acionáveis e arquiteturais diretamente relevantes a context-engineering (smart/dumb zone, clear vs compact), harness (skills de grilling/PRD/issues), paralelização de agentes via kanban/DAG e disciplina de decisão humano-no-loop, com grau razoável de novidade na síntese."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-software-fundamentals-matter-more-than-ever-matt-pocock--v4F1gFy-hqg|\"Software Fundamentals Matter More Than Ever\" — Matt Pocock]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-working-with-ai-not-just-using-it-brendan-o-leary--BEKc4P87XKo|Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary]]", "[[extracts/youtube/ai-learning/2026-09-11-fabio-akita-minha-experiencia-com-agile-vibe-coding--U3bZavG8qQY|Fabio Akita: Minha Experiência com Agile Vibe Coding]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-conductor-ceo-charlie-holtz-walks-us-through-his-ai-coding-setup--fQmlML9Lay4|Conductor CEO Charlie Holtz Walks Us Through His AI Coding Setup]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-in-the-sdlc-rethinking-ai-coding-tools-ai-agents--4wMRXmLpdA8|AI in the SDLC: Rethinking AI Coding Tools & AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-why-senior-engineers-struggle-to-build-ai-agents-philipp-schmid-google-deepmind--3_gYbhABcAE|Why (Senior) Engineers Struggle to Build AI Agents — Philipp Schmid, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-build-systems-not-code-angie-jones-agentic-ai-foundation--ZD9-4fW2HhM|Build Systems, Not Code - Angie Jones, Agentic AI Foundation]]", "[[extracts/youtube/ai-learning/2026-09-11-bdd-adr-prd-wtf-capturing-decisions-for-humans-and-ai-alike-michal-cichra-safe-i--504PvfXou5Y|BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike — Michal Cichra, Safe Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-the-new-code-sean-grove-openai--8rABwKRsec4|The New Code — Sean Grove, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-everything-we-got-wrong-about-research-plan-implement-dexter-horthy--YwZR6tc7qYg|Everything We Got Wrong About Research-Plan-Implement -  Dexter Horthy]]", "[[extracts/youtube/ai-learning/2026-09-11-7-insane-loops-you-need-to-try-right-now--F4a8aMLb678|7 INSANE loops you need to try right now]]", "[[extracts/youtube/ai-learning/2026-09-11-9-things-people-get-wrong-with-my-grill-skills--UzMNBN6xLLA|9 Things People Get Wrong With My /grill-* skills]]", "[[extracts/youtube/ai-learning/2026-09-11-zta-zero-token-architecture-kelsey-hightower-platformcon-2026--A7WFt2JQ5sg|ZTA: Zero Token Architecture - Kelsey Hightower | PlatformCon 2026]]"]
---

# Full Walkthrough: Workflow for AI Coding — Matt Pocock

## Tese
Fundamentos clássicos de engenharia de software (tarefas pequenas, tracer bullets, kanban com dependências) continuam sendo a forma mais eficaz de estruturar trabalho com agentes de IA, em vez de tratar IA como um paradigma completamente novo.

## Conceitos-chave
- smart zone vs dumb zone (degradação quadrática da atenção com o tamanho do contexto)
- compacting vs limpar contexto (metáfora de Memento / estado determinístico)
- sub-agentes com contexto isolado reportando sumários
- grill me skill / entrevista relentless para entendimento compartilhado
- design concept compartilhado (Frederick P. Brooks)
- crítica ao movimento specs-to-code (vibe coding por outro nome)
- PRD como documento de destino (destination document)
- issues independentemente agarráveis (independently grabbable)
- vertical slices / tracer bullets para feedback rápido entre camadas
- kanban com relações de bloqueio formando DAGs para paralelização de agentes
- tarefas human-in-the-loop vs AFK (away from keyboard)
- Ralph Wiggum como prática de loop incremental
- loops de fase n em vez de planos multifásicos numerados
- posse do stack de planejamento (inversão de controle)
- bad codebases make bad agents
- estágios de uma sessão: system prompt, exploração, implementação, teste

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Opus, Gemini Meetings, Slido, Tldraw, Cucumber, GitHub Issues, skill grill-me, skill write-a-PRD, skill PRD-to-issues, status line de contagem de tokens

**Pessoas/orgs:** Matt (Matt Pocock / AI Hero), Dex (HumanLayer), Martin Fowler, Pragmatic Programmer, Frederick P. Brooks, Sarah Chen (cliente fictícia), Anthropic, GitHub

## Claims acionáveis
- Cerca de 100k tokens é o limite prático do smart zone independentemente da janela (1M); janelas maiores servem para retrieval, não para coding
- Prefira limpar o contexto a compactar, pois o estado inicial é sempre o mesmo e pode ser otimizado
- Dimensione tarefas para caber inteiramente no smart zone em vez de oscilar entre smart e dumb zone
- Use entrevistas interativas (grill me) para alcançar um design concept compartilhado com o agente em vez de gerar e ler planos
- Não revise PRDs gerados após uma sessão de alinhamento: você estaria testando apenas a sumarização do LLM
- Quebre PRDs em issues com fatias verticais (tracer bullets) que atravessem todas as camadas para obter feedback imediato e integrado
- Force o agente a evitar fatias horizontais (camada por camada), pois atrasam o feedback até as fases finais
- Modele planos como kanban com dependências de bloqueio (DAG) para permitir execução paralela por múltiplos agentes
- Classifique tarefas como human-in-the-loop (planejamento, alinhamento) ou AFK (implementação) e mantenha humanos apenas nas primeiras
- Use sub-agentes de exploração com contexto isolado para não inflar o contexto do agente orquestrador
- Exiba a contagem exata de tokens em toda sessão de coding para saber a distância até o dumb zone
- Possua seu stack de planejamento em vez de depender de frameworks prontos, para ter observabilidade e capacidade de correção
- Práticas de livros clássicos (20+ anos) verbalizadas em inglês são material excelente para prompts
- Bases de código ruins produzem agentes ruins; entender profundamente o código melhora os resultados com IA
- Sessões com stakeholders podem ser gravadas, transcritas e alimentadas em sessões de grilling para validar suposições

> **Deep dive:** `high` — Alta densidade de práticas acionáveis e arquiteturais diretamente relevantes a context-engineering (smart/dumb zone, clear vs compact), harness (skills de grilling/PRD/issues), paralelização de agentes via kanban/DAG e disciplina de decisão humano-no-loop, com grau razoável de novidade na síntese.
