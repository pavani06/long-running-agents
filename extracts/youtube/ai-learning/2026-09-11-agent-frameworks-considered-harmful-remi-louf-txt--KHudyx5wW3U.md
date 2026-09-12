---
title: "Agent Frameworks Considered Harmful — Rémi Louf, .txt"
type: "extract"
source: "youtube"
video_id: "KHudyx5wW3U"
url: "https://www.youtube.com/watch?v=KHudyx5wW3U"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-agent-frameworks-considered-harmful-remi-louf-txt--KHudyx5wW3U.txt]]"
tags: ["agent-loop", "agent-tooling", "agentes-orquestracao", "arquitetura", "context-engineering", "error-handling", "evals", "harness-engineering", "memory-architecture", "model-selection", "multi-agent", "observability", "runtime", "tracing", "verification", "production"]
thesis: "Agentes em segundo plano devem rodar sobre um runtime de orquestração por eventos tipados — com agentes definidos em Markdown sem código, log append-only como memória e prompts endereçados por conteúdo para rastreabilidade e replay — porque os problemas reais são os clássicos de orquestração de software, não grafos ou frameworks."
concepts: ["Background agents (agentes autônomos sem supervisão, analogia do robo-mower)", "Orquestração orientada a eventos em vez de grafos (sem edges; topologia emerge das assinaturas)", "Agentes declarativos em Markdown: versionáveis, diffáveis, revisáveis em PR, editáveis por não-programadores", "Cron/schedules apenas para gatilhos temporais; eventos para reatividade (email, PR, voice note)", "Eventos tipados como fronteira entre agentes e tool calls tipadas como fronteira com o mundo externo", "Log append-only como memória do sistema, com eventos causalmente encadeados para debugging", "Prompts endereçados por conteúdo (hashes por componente: system prompt, skills, tools, user message)", "Diffs de prompt entre execuções e replay de requests com modelos alternativos", "Compaction facilitada manipulando grafos de prompt em vez de strings", "Analogia kernel/userland: runtime agenda, isola e journala processos-agente", "Invalidação/rejeição de eventos por structured outputs mal validados (~20% de eventos errados)", "Auditabilidade do que efetivamente entrou no contexto do modelo", "Dogfooding e build-before-you-buy em infra de agentes"]
tools: ["Claude Opus 4.x (Anthropic)", "Codex (OpenAI)", "Linear", "Jira", "Slack", "cron jobs", "git", "Nix", "Markdown/YAML", "modelos open source", "modelos locais (rodando no laptop)", "apps de agente no celular ('SSH with vibes')", "CRM (genérico)"]
people: ["Palestrante — CEO da Text (empresa de ~15 pessoas especializada em structured outputs)", "OpenAI", "Anthropic", "CTO e board da empresa do palestrante"]
claims: ["Defina agentes em arquivos Markdown (não em código): pode versionar, diffar e revisar em PR, e pessoas não-técnicas podem contribuir", "Orquestre por eventos, não por grafos em código: cada agente declara o que aceita e o que emite, fan-in/fan-out sai de graça e não há edges a manter", "Use cron apenas para o 'quando' temporal; conecte o 'porque aconteceu' a eventos emitidos pelo sistema (novo email, PR, voice note)", "Mantenha um log append-only causalmente encadeado de todos os eventos — com 3-4 agentes os headaches de debugging já começam e nada deve ser perdido", "Enderece cada componente do prompt por hash (content addressing estilo git/Nix) para rastrear exatamente o que entrou no contexto do modelo — a UI de chat do agente 'mente' sobre isso (compaction, thinking traces ocultos)", "Com o grafo de prompts endereçados você ganha de graça: diffs entre execuções, replay exato de requests com outro modelo (útil para evals e redução de custo) e auditabilidade", "O trabalho do runtime/kernel é tornar ações ruins impossíveis, não apenas improváveis: valide tool calls tipadas na fronteira com o mundo externo e eventos tipados entre agentes — isso é inegociável", "Structured outputs mal feitos geram alta taxa de rejeição (Anthropic tinha ~20% de eventos inválidos), então validação de schema é infra crítica", "Modelos open source já são bons o bastante para tarefas não-coding: o palestrante substituiu todas as APIs terceiras, incluindo modelo local no laptop", "A categoria de infraestrutura de agentes está instável: construa um protótipo antes de comprar para conhecer seus requisitos reais", "Frameworks de orquestração devem fazer dogfooding — fica evidente quando não usam o próprio produto", "CEO/técnicos devem imergir na tecnologia em primeira mão (as duas semanas do palestrante mudaram a trajetória da empresa)"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de arquitetura acionável e relativamente nova (prompts content-addressed com diff e replay, log causal append-only, eventos tipados como única fronteira, agentes em Markdown sobre runtime estilo kernel) diretamente relevante a harness, context-engineering, observability e evals."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-12-factor-agents-patterns-of-reliable-llm-applications-dex-horthy-humanlayer--8kMaTybvDUw|12-Factor Agents: Patterns of reliable LLM applications — Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-build-systems-not-code-angie-jones-agentic-ai-foundation--ZD9-4fW2HhM|Build Systems, Not Code - Angie Jones, Agentic AI Foundation]]", "[[extracts/youtube/ai-learning/2026-09-11-from-coding-to-knowledge-work-agents-karan-vaidya-composio--xxfMT-bPEmU|From coding to Knowledge work agents — Karan Vaidya, Composio]]", "[[extracts/youtube/ai-learning/2026-09-11-ci-cd-is-dead-agents-need-continuous-compute-and-computers-hugo-santos-and-madis--VktrqzQgytY|CI/CD Is Dead, Agents Need Continuous Compute and Computers — Hugo Santos and Madison Faulkner]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-cogent-s-three-agent-architecture-for-autonomous-defense-geng-sng-co-foun--D6XWu54oG4g|Inside Cogent's three-agent architecture for autonomous defense | Geng Sng (Co-founder, Cogent)]]", "[[extracts/youtube/ai-learning/2026-09-11-unlock-autonomous-ai-agents-with-auth-md-michael-grinich-mcp-night-agent-mode-ke--Dqp_b8GHLXU|Unlock Autonomous AI Agents with auth.md, Michael Grinich | MCP Night: Agent Mode Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-zta-zero-token-architecture-kelsey-hightower-platformcon-2026--A7WFt2JQ5sg|ZTA: Zero Token Architecture - Kelsey Hightower | PlatformCon 2026]]"]
---

# Agent Frameworks Considered Harmful — Rémi Louf, .txt

## Tese
Agentes em segundo plano devem rodar sobre um runtime de orquestração por eventos tipados — com agentes definidos em Markdown sem código, log append-only como memória e prompts endereçados por conteúdo para rastreabilidade e replay — porque os problemas reais são os clássicos de orquestração de software, não grafos ou frameworks.

## Conceitos-chave
- Background agents (agentes autônomos sem supervisão, analogia do robo-mower)
- Orquestração orientada a eventos em vez de grafos (sem edges; topologia emerge das assinaturas)
- Agentes declarativos em Markdown: versionáveis, diffáveis, revisáveis em PR, editáveis por não-programadores
- Cron/schedules apenas para gatilhos temporais; eventos para reatividade (email, PR, voice note)
- Eventos tipados como fronteira entre agentes e tool calls tipadas como fronteira com o mundo externo
- Log append-only como memória do sistema, com eventos causalmente encadeados para debugging
- Prompts endereçados por conteúdo (hashes por componente: system prompt, skills, tools, user message)
- Diffs de prompt entre execuções e replay de requests com modelos alternativos
- Compaction facilitada manipulando grafos de prompt em vez de strings
- Analogia kernel/userland: runtime agenda, isola e journala processos-agente
- Invalidação/rejeição de eventos por structured outputs mal validados (~20% de eventos errados)
- Auditabilidade do que efetivamente entrou no contexto do modelo
- Dogfooding e build-before-you-buy em infra de agentes

## Ferramentas & pessoas
**Ferramentas:** Claude Opus 4.x (Anthropic), Codex (OpenAI), Linear, Jira, Slack, cron jobs, git, Nix, Markdown/YAML, modelos open source, modelos locais (rodando no laptop), apps de agente no celular ('SSH with vibes'), CRM (genérico)

**Pessoas/orgs:** Palestrante — CEO da Text (empresa de ~15 pessoas especializada em structured outputs), OpenAI, Anthropic, CTO e board da empresa do palestrante

## Claims acionáveis
- Defina agentes em arquivos Markdown (não em código): pode versionar, diffar e revisar em PR, e pessoas não-técnicas podem contribuir
- Orquestre por eventos, não por grafos em código: cada agente declara o que aceita e o que emite, fan-in/fan-out sai de graça e não há edges a manter
- Use cron apenas para o 'quando' temporal; conecte o 'porque aconteceu' a eventos emitidos pelo sistema (novo email, PR, voice note)
- Mantenha um log append-only causalmente encadeado de todos os eventos — com 3-4 agentes os headaches de debugging já começam e nada deve ser perdido
- Enderece cada componente do prompt por hash (content addressing estilo git/Nix) para rastrear exatamente o que entrou no contexto do modelo — a UI de chat do agente 'mente' sobre isso (compaction, thinking traces ocultos)
- Com o grafo de prompts endereçados você ganha de graça: diffs entre execuções, replay exato de requests com outro modelo (útil para evals e redução de custo) e auditabilidade
- O trabalho do runtime/kernel é tornar ações ruins impossíveis, não apenas improváveis: valide tool calls tipadas na fronteira com o mundo externo e eventos tipados entre agentes — isso é inegociável
- Structured outputs mal feitos geram alta taxa de rejeição (Anthropic tinha ~20% de eventos inválidos), então validação de schema é infra crítica
- Modelos open source já são bons o bastante para tarefas não-coding: o palestrante substituiu todas as APIs terceiras, incluindo modelo local no laptop
- A categoria de infraestrutura de agentes está instável: construa um protótipo antes de comprar para conhecer seus requisitos reais
- Frameworks de orquestração devem fazer dogfooding — fica evidente quando não usam o próprio produto
- CEO/técnicos devem imergir na tecnologia em primeira mão (as duas semanas do palestrante mudaram a trajetória da empresa)

> **Deep dive:** `high` — Densidade alta de arquitetura acionável e relativamente nova (prompts content-addressed com diff e replay, log causal append-only, eventos tipados como única fronteira, agentes em Markdown sobre runtime estilo kernel) diretamente relevante a harness, context-engineering, observability e evals.
