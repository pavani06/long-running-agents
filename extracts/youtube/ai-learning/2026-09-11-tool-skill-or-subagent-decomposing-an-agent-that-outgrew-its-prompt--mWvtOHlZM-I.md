---
title: "Tool, skill, or subagent? Decomposing an agent that outgrew its prompt"
type: "extract"
source: "youtube"
video_id: "mWvtOHlZM-I"
url: "https://www.youtube.com/watch?v=mWvtOHlZM-I"
channel: "Claude"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt--mWvtOHlZM-I.txt]]"
tags: ["agent-loop", "agent-tooling", "agents", "arquitetura", "context-engineering", "context-management", "evals", "harness", "harness-engineering", "model-selection", "multi-agent", "observability", "token-budgeting", "analise"]
thesis: "Agentes que degradam por complexidade acumulada devem ser re-arquitetados por decomposição: system prompt curto com progressive disclosure via skills, primitivas humanas (execução de código, file system, web search) no lugar de ferramentas bespoke, e subagentes apenas para paralelização e revisão independente, com cada mudança validada por hill climbing em evals."
concepts: ["Decomposição de agentes", "Progressive disclosure via skills", "Primitivas humanas (code execution, file system, web search, to-do list)", "Hill climbing em evals", "Graders determinísticos e LLM-as-judge", "Subagentes para paralelização e 'fresh mind'", "Orquestrador com subagentes de contexto isolado", "Políticas contraditórias em system prompt longo", "Isolamento de contexto para forecasting", "Callable agents (subagentes nativos com observabilidade)", "Migração de harness próprio (Messages API) para managed agents", "Eficiência de tokens via execução de código em vez de ingestão de dados"]
tools: ["Claude Managed Agents (CMA)", "Claude Code", "Claude Opus 4.7", "Anthropic Messages API", "Anthropic SDK", "MCP (Model Context Protocol)", "uv (UV project)", "Bash/Read/Write tools", "LLM-as-judge graders"]
people: ["Will (Anthropic, Applied AI)", "Anthropic", "Gary (palestrante anterior sobre evals)", "Code with Claude London (evento)"]
claims: ["Reduza o system prompt (ex.: de 400 para ~15-50 linhas) movendo lógica de negócio para skills carregadas por Claude somente quando necessárias", "Comece com primitivas humanas (bash/execução de código, file system, web search, to-do list) e adicione ferramentas customizadas apenas quando necessário, removendo as que não forem usadas", "Prefira execução de código a carregar CSVs/Excel no contexto: reduz drasticamente tokens, custo e tempo de execução (de mais de 200k tokens para bem menos)", "Use subagentes apenas para dois casos: paralelizar muita capacidade em um problema grande ou obter uma 'mente fresca' sem contexto para revisar o trabalho; caso contrário, consolide capacidade no agente principal pois modelos de fronteira já gerenciam mais informação", "Evite MCP por padrão: primeiro ferramentas nativas tipo Claude Code, depois ferramentas locais do agente, e só publique um servidor MCP quando múltiplos clientes precisarem de ferramentas padronizadas e governadas", "Considere invocar CLIs e APIs via execução de código como alternativa a MCP para evitar poluição de contexto", "Vigie dois modos de falha comuns: quebra de comunicação entre orquestrador e subagentes, e políticas contraditórias em prompts longos que causam alucinação de parâmetros (problema de contexto, não do modelo)", "Monte evals com tarefas de regressão (single-turn) e de failure modes (multi-turn), usando métricas determinísticas (tokens, latência, contagens) e LLM-as-judge para tom e qualidade", "Pratique hill climbing: rode evals para obter baseline, faça mudanças arquiteturais incrementais e reavalie (no exemplo, de 62% para 92%)", "Use plataformas managed agents para offload de infraestrutura (escala para milhares de usuários, memória, segurança) e focar apenas no design do agente", "Prefira a capacidade nativa de callable agents em vez de expor subagentes como ferramentas, para obter logging e observabilidade de subagentes no nível do orquestrador", "Aceite turn count estável ou latência levemente maior quando tokens e custo caem significativamente em tarefas complexas"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de decisões arquiteturais acionáveis (tool vs skill vs sub-agente, estratégia MCP, progressive disclosure, observabilidade de subagentes) validadas por evals quantitativos, diretamente relevantes a harness, context-engineering e produção."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-dynamic-subagents-how-to-run-parallel-agents-reliably-in-deep-agents--5AkdMangfNk|Dynamic Subagents: How to Run Parallel Agents Reliably in Deep Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-build-systems-not-code-angie-jones-agentic-ai-foundation--ZD9-4fW2HhM|Build Systems, Not Code - Angie Jones, Agentic AI Foundation]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-deep-agents-explained--GbzEDgcuGJU|Deep Agents Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-build-effective-agents-barry-zhang-anthropic--D7_ipDqhtwk|How We Build Effective Agents: Barry Zhang, Anthropic]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-solved-context-management-in-agents-sally-ann-delucia--esY99nYXxR4|How we solved Context Management in Agents — Sally-Ann Delucia]]", "[[extracts/youtube/ai-learning/2026-09-11-building-great-agent-skills-the-missing-manual--UNzCG3lw6O0|Building Great Agent Skills: The Missing Manual]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-use-rlms-in-deep-agents--5_LLMZfKI6w|How to use RLMs in Deep Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-pi-architecture-explained-agent-loop-tools-tui-and-more--gTeujlv8qK0|PI Architecture EXPLAINED | Agent Loop, Tools, TUI and More]]", "[[extracts/youtube/ai-learning/2026-09-11-handoff-is-my-new-favourite-skill--dtAJ2dOd3ko|/handoff is my new favourite skill]]"]
---

# Tool, skill, or subagent? Decomposing an agent that outgrew its prompt

## Tese
Agentes que degradam por complexidade acumulada devem ser re-arquitetados por decomposição: system prompt curto com progressive disclosure via skills, primitivas humanas (execução de código, file system, web search) no lugar de ferramentas bespoke, e subagentes apenas para paralelização e revisão independente, com cada mudança validada por hill climbing em evals.

## Conceitos-chave
- Decomposição de agentes
- Progressive disclosure via skills
- Primitivas humanas (code execution, file system, web search, to-do list)
- Hill climbing em evals
- Graders determinísticos e LLM-as-judge
- Subagentes para paralelização e 'fresh mind'
- Orquestrador com subagentes de contexto isolado
- Políticas contraditórias em system prompt longo
- Isolamento de contexto para forecasting
- Callable agents (subagentes nativos com observabilidade)
- Migração de harness próprio (Messages API) para managed agents
- Eficiência de tokens via execução de código em vez de ingestão de dados

## Ferramentas & pessoas
**Ferramentas:** Claude Managed Agents (CMA), Claude Code, Claude Opus 4.7, Anthropic Messages API, Anthropic SDK, MCP (Model Context Protocol), uv (UV project), Bash/Read/Write tools, LLM-as-judge graders

**Pessoas/orgs:** Will (Anthropic, Applied AI), Anthropic, Gary (palestrante anterior sobre evals), Code with Claude London (evento)

## Claims acionáveis
- Reduza o system prompt (ex.: de 400 para ~15-50 linhas) movendo lógica de negócio para skills carregadas por Claude somente quando necessárias
- Comece com primitivas humanas (bash/execução de código, file system, web search, to-do list) e adicione ferramentas customizadas apenas quando necessário, removendo as que não forem usadas
- Prefira execução de código a carregar CSVs/Excel no contexto: reduz drasticamente tokens, custo e tempo de execução (de mais de 200k tokens para bem menos)
- Use subagentes apenas para dois casos: paralelizar muita capacidade em um problema grande ou obter uma 'mente fresca' sem contexto para revisar o trabalho; caso contrário, consolide capacidade no agente principal pois modelos de fronteira já gerenciam mais informação
- Evite MCP por padrão: primeiro ferramentas nativas tipo Claude Code, depois ferramentas locais do agente, e só publique um servidor MCP quando múltiplos clientes precisarem de ferramentas padronizadas e governadas
- Considere invocar CLIs e APIs via execução de código como alternativa a MCP para evitar poluição de contexto
- Vigie dois modos de falha comuns: quebra de comunicação entre orquestrador e subagentes, e políticas contraditórias em prompts longos que causam alucinação de parâmetros (problema de contexto, não do modelo)
- Monte evals com tarefas de regressão (single-turn) e de failure modes (multi-turn), usando métricas determinísticas (tokens, latência, contagens) e LLM-as-judge para tom e qualidade
- Pratique hill climbing: rode evals para obter baseline, faça mudanças arquiteturais incrementais e reavalie (no exemplo, de 62% para 92%)
- Use plataformas managed agents para offload de infraestrutura (escala para milhares de usuários, memória, segurança) e focar apenas no design do agente
- Prefira a capacidade nativa de callable agents em vez de expor subagentes como ferramentas, para obter logging e observabilidade de subagentes no nível do orquestrador
- Aceite turn count estável ou latência levemente maior quando tokens e custo caem significativamente em tarefas complexas

> **Deep dive:** `high` — Alta densidade de decisões arquiteturais acionáveis (tool vs skill vs sub-agente, estratégia MCP, progressive disclosure, observabilidade de subagentes) validadas por evals quantitativos, diretamente relevantes a harness, context-engineering e produção.
