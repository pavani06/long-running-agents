---
title: "Why Enterprise AI Adoption Is Slower Than You Think — Aaron Levie (Box) + Harrison Chase"
type: "extract"
source: "youtube"
video_id: "agSRMrhNTf4"
url: "https://www.youtube.com/watch?v=agSRMrhNTf4"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-enterprise-ai-adoption-is-slower-than-you-think-aaron-levie-box-harrison-cha--agSRMrhNTf4.txt]]"
tags: ["agents", "agentic-coding", "harness", "harness-engineering", "context-engineering", "permissions", "governanca", "model-selection", "token-budgeting", "evals", "verification", "data-platform", "knowledge-management", "agent-tooling"]
thesis: "O sucesso dos agentes de código não se transferirá automaticamente para o restante do conhecimento corporativo porque este carece de verificabilidade, usuários técnicos, permissões abertas e acesso completo a dados — a lacuna exige pontes como agentes verticais, dados prontos para agentes, e harnesses de código como espinha dorsal, com orçamento de tokens e seleção multi-modelo."
concepts: ["Difusão lenta de IA em empresas vs. progresso hiperbólico dos agentes de código", "Verificabilidade do trabalho como vantagem dos agentes de código", "Permissões como permutações por indivíduo/time herdadas pelos agentes", "Agentes verticais/específicos de domínio com forward-deployed engineers", "Headless (via MCP/APIs) vs. experiência de agente na interface", "Paradoxo de Jevons aplicado ao uso de dados por agentes", "Modelo canônico único de dados (um filesystem, um ID, uma governança)", "Dados agent-ready: pipeline de conversão para markdown", "Reranqueamento de busca para agentes que consomem ~100x mais resultados", "Heurística busca vs. navegação em árvore de pastas no system prompt", "Harness de código como espinha dorsal de todo trabalho do conhecimento (sandbox, execução, conectores)", "Diferenciação por capacidade, performance e custo em estratégias multi-modelo", "Penalidade de prompt caching em execuções multi-modelo", "Limiar de custo que justifica harness dedicado por workload", "Descascar workloads para modelos 'frontier minus one' mais baratos", "Orçamento de tokens e ciclos de planejamento para empresas com metas de EPS", "Incentivos perversos de recompensar consumo de tokens", "Evals para specialização do harness em extração de documentos"]
tools: ["Box", "BoxAgent", "MCP (Model Context Protocol)", "Salesforce headless MCP", "Claude Code", "Claude for Legal", "Claude Cowork", "ChatGPT", "Codex", "Harvey", "Gemini Flash", "Opus 4", "Deep Agents", "NPM", "Excel"]
people: ["Aaron Levie", "Box", "Salesforce", "Harvey", "Anthropic (implícito via Claude)", "Facebook/Meta", "Nvidia", "Uber (CTO)", "ServiceNow"]
claims: ["Codar com agentes funciona porque o trabalho é verificável, os modelos são treinados em código abundante, os usuários são técnicos e as permissões de codebases são abertas — conhecimento corporativo falta nessas quatro dimensões.", "Agentes herdam as permutações de permissões de cada usuário, multiplicando a complexidade de acesso; um agente não pode 'pedir acesso à Sally' como um humano.", "Empresas de software devem construir simultaneamente uma experiência de agente world-class no produto E APIs headless world-class, aceitando que o volume será majoritariamente headless.", "Um modelo canônico único de arquivos, IDs e governança (decisões de arquitetura tomadas há 10 anos) dá aos agentes os mesmos benefícios que deu a humanos.", "Motores de busca precisam aceitar novos sinais porque agentes consomem ~100x mais resultados que humanos, e contexto pode importar mais que ranking.", "Expor uma API que converte qualquer tipo de conteúdo em markdown torna o dado pronto para agentes.", "Harnesses de código devem ser a espinha dorsal de agentes de conhecimento: computador, sandbox, escrever/executar código, conectores MCP, mais overlay de expertise vertical/horizontal.", "Treine o agente (via system prompt) a decidir entre buscar (encontrar documento único) e navegar pastas (entender o workspace ao redor), pois a busca omite contexto do entorno.", "Estratégias multi-modelo dão três vantagens: diferenciação de capacidade (via evals), performance (ex.: Gemini Flash mais rápido que Opus 4) e custo — que pode ser a grande história dos próximos três anos.", "Prompt caching impõe penalidades a execuções multi-modelo; o híbrido ótimo ainda está em descoberta.", "Workflows de alto valor (ex.: claims de seguro com US$50M/ano em jogo) justificam harness hiperajustado ao modelo certo; tarefas casuais não.", "Com inteligência de fronteira sempre cara, faz sentido migrar workloads para modelos 'frontier minus one' mais baratos.", "Empresas públicas com metas trimestrais de EPS não podem converter 'dólares de VC em tokens'; precisarão de misturas de modelos e orçamentos de tokens.", "Não recompense consumo de tokens (incentivo perverso); use o roadmap empilhado como mecanismo de controle da utilização.", "Agentes verticais de domínio com forward-deployed engineers são a maior oportunidade startup nesse gap; empresas têm vantagem análoga com forward-deployed engineers internos.", "A lentidão da difusão organizacional é razão pela qual 'doomers' provavelmente errarão sobre takeoff rápidos."]
deep_dive: "high"
deep_dive_reason: "Densidade alta de insights acionáveis e arquiteturais de produção (modelo canônico de dados, reranking de busca para agentes, heurística busca-vs-pastas no system prompt, trade-offs multi-modelo com prompt caching, limiar de custo para harness dedicado) diretamente relevantes a harness, context-engineering, governança e token-budgeting, com novidade além do discurso padrão sobre agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-ms-e435-economics-of-the-ai-supercycle-spring-2026-infrasctructure-ente--sRvrXL83N-c|Stanford MS&E435 Economics of the AI Supercycle | Spring 2026 | Infrasctructure, Enterprise AI, SaaS]]", "[[extracts/youtube/ai-learning/2026-09-11-why-your-enterprise-tech-stack-isnt-ready-for-ai-agents-christopher-lovejoy-saul--mav15aW9lLM|Why Your Enterprise Tech Stack Isn’t Ready for AI Agents — Christopher Lovejoy & Saul Howard]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-from-coding-to-knowledge-work-agents-karan-vaidya-composio--xxfMT-bPEmU|From coding to Knowledge work agents — Karan Vaidya, Composio]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-26-key-takeaways-from-building-150-agents-in-9-months--jmeGqDu4tPU|26 Key Takeaways from Building 150+ Agents in 9 months]]", "[[extracts/youtube/ai-learning/2026-09-11-how-ai-is-reinventing-software-business-models-ft-bret-taylor-of-sierra--xlQB_0Nzoog|How AI is Reinventing Software Business Models ft. Bret Taylor of Sierra]]", "[[extracts/youtube/ai-learning/2026-09-11-jensen-huang-why-companies-need-open-agent-systems--Yy3JH6dDugc|Jensen Huang: Why companies need open agent systems]]", "[[extracts/youtube/ai-learning/2026-09-11-vertical-ai-agents-could-be-10x-bigger-than-saas--ASABxNenD_U|Vertical AI Agents Could Be 10X Bigger Than SaaS]]", "[[extracts/youtube/ai-learning/2026-09-11-parallels-parag-agrawal-building-a-new-web-for-ai-agents--fUcnE6pjq5w|Parallel’s Parag Agrawal: Building a New Web for AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-rip-to-rpa-how-ai-makes-operations-work--O6DtzLGLNWY|RIP to RPA: How AI Makes Operations Work]]", "[[extracts/youtube/ai-learning/2026-09-11-unlock-autonomous-ai-agents-with-auth-md-michael-grinich-mcp-night-agent-mode-ke--Dqp_b8GHLXU|Unlock Autonomous AI Agents with auth.md, Michael Grinich | MCP Night: Agent Mode Keynote]]"]
theme: "Estratégias corporativas de agentes"
---

# Why Enterprise AI Adoption Is Slower Than You Think — Aaron Levie (Box) + Harrison Chase

## Tese
O sucesso dos agentes de código não se transferirá automaticamente para o restante do conhecimento corporativo porque este carece de verificabilidade, usuários técnicos, permissões abertas e acesso completo a dados — a lacuna exige pontes como agentes verticais, dados prontos para agentes, e harnesses de código como espinha dorsal, com orçamento de tokens e seleção multi-modelo.

## Conceitos-chave
- Difusão lenta de IA em empresas vs. progresso hiperbólico dos agentes de código
- Verificabilidade do trabalho como vantagem dos agentes de código
- Permissões como permutações por indivíduo/time herdadas pelos agentes
- Agentes verticais/específicos de domínio com forward-deployed engineers
- Headless (via MCP/APIs) vs. experiência de agente na interface
- Paradoxo de Jevons aplicado ao uso de dados por agentes
- Modelo canônico único de dados (um filesystem, um ID, uma governança)
- Dados agent-ready: pipeline de conversão para markdown
- Reranqueamento de busca para agentes que consomem ~100x mais resultados
- Heurística busca vs. navegação em árvore de pastas no system prompt
- Harness de código como espinha dorsal de todo trabalho do conhecimento (sandbox, execução, conectores)
- Diferenciação por capacidade, performance e custo em estratégias multi-modelo
- Penalidade de prompt caching em execuções multi-modelo
- Limiar de custo que justifica harness dedicado por workload
- Descascar workloads para modelos 'frontier minus one' mais baratos
- Orçamento de tokens e ciclos de planejamento para empresas com metas de EPS
- Incentivos perversos de recompensar consumo de tokens
- Evals para specialização do harness em extração de documentos

## Ferramentas & pessoas
**Ferramentas:** Box, BoxAgent, MCP (Model Context Protocol), Salesforce headless MCP, Claude Code, Claude for Legal, Claude Cowork, ChatGPT, Codex, Harvey, Gemini Flash, Opus 4, Deep Agents, NPM, Excel

**Pessoas/orgs:** Aaron Levie, Box, Salesforce, Harvey, Anthropic (implícito via Claude), Facebook/Meta, Nvidia, Uber (CTO), ServiceNow

## Claims acionáveis
- Codar com agentes funciona porque o trabalho é verificável, os modelos são treinados em código abundante, os usuários são técnicos e as permissões de codebases são abertas — conhecimento corporativo falta nessas quatro dimensões.
- Agentes herdam as permutações de permissões de cada usuário, multiplicando a complexidade de acesso; um agente não pode 'pedir acesso à Sally' como um humano.
- Empresas de software devem construir simultaneamente uma experiência de agente world-class no produto E APIs headless world-class, aceitando que o volume será majoritariamente headless.
- Um modelo canônico único de arquivos, IDs e governança (decisões de arquitetura tomadas há 10 anos) dá aos agentes os mesmos benefícios que deu a humanos.
- Motores de busca precisam aceitar novos sinais porque agentes consomem ~100x mais resultados que humanos, e contexto pode importar mais que ranking.
- Expor uma API que converte qualquer tipo de conteúdo em markdown torna o dado pronto para agentes.
- Harnesses de código devem ser a espinha dorsal de agentes de conhecimento: computador, sandbox, escrever/executar código, conectores MCP, mais overlay de expertise vertical/horizontal.
- Treine o agente (via system prompt) a decidir entre buscar (encontrar documento único) e navegar pastas (entender o workspace ao redor), pois a busca omite contexto do entorno.
- Estratégias multi-modelo dão três vantagens: diferenciação de capacidade (via evals), performance (ex.: Gemini Flash mais rápido que Opus 4) e custo — que pode ser a grande história dos próximos três anos.
- Prompt caching impõe penalidades a execuções multi-modelo; o híbrido ótimo ainda está em descoberta.
- Workflows de alto valor (ex.: claims de seguro com US$50M/ano em jogo) justificam harness hiperajustado ao modelo certo; tarefas casuais não.
- Com inteligência de fronteira sempre cara, faz sentido migrar workloads para modelos 'frontier minus one' mais baratos.
- Empresas públicas com metas trimestrais de EPS não podem converter 'dólares de VC em tokens'; precisarão de misturas de modelos e orçamentos de tokens.
- Não recompense consumo de tokens (incentivo perverso); use o roadmap empilhado como mecanismo de controle da utilização.
- Agentes verticais de domínio com forward-deployed engineers são a maior oportunidade startup nesse gap; empresas têm vantagem análoga com forward-deployed engineers internos.
- A lentidão da difusão organizacional é razão pela qual 'doomers' provavelmente errarão sobre takeoff rápidos.

> **Deep dive:** `high` — Densidade alta de insights acionáveis e arquiteturais de produção (modelo canônico de dados, reranking de busca para agentes, heurística busca-vs-pastas no system prompt, trade-offs multi-modelo com prompt caching, limiar de custo para harness dedicado) diretamente relevantes a harness, context-engineering, governança e token-budgeting, com novidade além do discurso padrão sobre agentes.
