---
title: "When to Build Your Own Agent Harness | Harrison Chase, LangChain"
type: "extract"
source: "youtube"
video_id: "HI2q3ci3Iuc"
url: "https://www.youtube.com/watch?v=HI2q3ci3Iuc"
channel: "Sequoia Capital"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-when-to-build-your-own-agent-harness-harrison-chase-langchain--HI2q3ci3Iuc.txt]]"
tags: ["harness", "harness-engineering", "agent-loop", "context-engineering", "context-management", "evals", "observability", "tracing", "model-selection", "agents", "agent-tooling", "frameworks", "gate-design", "verification", "token-budgeting", "multi-agent"]
thesis: "Para 'possuir a própria inteligência' agêntica é necessário controlar os três componentes do agente — harness, modelo e contexto — customizando o harness com middleware sobre o loop básico do agente e alimentando um ciclo contínuo de melhoria com evals privados e observabilidade de traces."
concepts: ["agente = harness + modelo + contexto", "loop básico de agente (LLM chamando tools)", "middleware/hooks como pontos de inserção no loop (pré-chamada de modelo, wrapping de model calls e tool calls)", "summarização de contexto e context offloading", "arquiteturas cognitivas bespoke vs harness geral", "espectro in-distribution vs out-of-distribution no design do harness", "model profiles (trocar implementação de tool conforme o modelo)", "ownership de contexto: memória, conhecimento semântico, conversas anteriores", "switchabilidade de modelos para evitar lock-in", "benchmark privado por domínio", "anatomia de task Harbor: environment (Docker sandbox), solution (golden check), tests (verifier), instruction.md", "LLM-as-a-judge e agent-as-a-judge", "trajetórias (messages) vs traces completos para debug", "falha de agente = modelo insuficiente OU contexto insuficiente (o segundo é mais comum)", "data flywheel: rodar agente → coletar traces → curar → experimentar → atualizar harness/modelo/contexto", "feedback implícito via design de UX", "avaliadores online baratos com SLMs fine-tunados", "benchmarking cruzado de harnesses para portar aprendizados ('codeexification')", "predictabilidade/controle como motivo para arquiteturas cognitivas (serviços financeiros)"]
tools: ["LangChain", "LangSmith", "LangSmith CLI", "Deep Agents", "LangEngine", "Harbor", "Terminal Bench 2", "Frontier Bench", "Issue Bench", "Claude Code", "Claude Agent SDK", "Codex", "Slack", "Docker"]
people: ["Harrison (co-fundador/CEO da LangChain)", "LangChain", "Gabe (Harvey)", "Harvey", "Lynn (Fireworks)", "Fireworks", "Satcha", "Eno (Factory)", "Factory", "Swix", "OpenAI", "Anthropic"]
claims: ["Comece com um harness geral off-the-shelf (menor time-to-value) e adicione gates e checks conforme estreita o caso de uso", "Use harness pronto quando a tarefa está in-distribution do treinamento dos modelos; customize progressivamente conforme sai da distribuição", "Mesmo em domínios out-of-distribution (ex: legal AI), mantenha subtarefas in-distribution — como edição de arquivos — no formato em que cada modelo foi RL-treinado, via model profiles", "Todo agente mission-critical merece benchmark próprio; Harbor (open-source, dos criadores do Terminal Bench 2) está virando o padrão da indústria para isso", "Ao benchmarkar agentes, rastreie não só acurácia mas também latência e custo (tokens)", "Na maioria das falhas de agente o problema é o contexto recebido pelo LLM, não a capacidade do modelo — invista em observabilidade do que entra na janela de contexto", "Projete a UX do agente para capturar feedback implícito dos usuários, já que thumbs up/down explícito raramente acontece", "Rode avaliadores online sobre traces com SLMs fine-tunados (ou código, quando suficiente) para baratear LLM-as-a-judge em escala", "É possível atualizar qualquer parte do agente com o flywheel: harness engineering, fine-tuning do modelo ou memória/contexto", "Automatize o flywheel com um agente sobre os traces (LangEngine) que curam dados, criam issues e sugerem fixes", "Crie um benchmark interno (Issue Bench) para o próprio agente de automação e compare múltiplos harnesses, portando aprendizados para o harness central", "Para requisitos de previsibilidade e controle (ex: serviços financeiros), prefira arquiteturas cognitivas customizadas a harnesses agentivos gerais", "Espera-se convergência parcial dos harnesses em domínios treinados pelos labs (ex: coding), mas divergência em domínios verticais — por isso evals e observabilidade são essenciais"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de insight arquitetural acionável (pontos de middleware no loop, model profiles, anatomia de tasks Harbor, flywheel automatizado via LangEngine) diretamente relevante a harness, context-engineering, evals e observabilidade, com novidade além do senso comum."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-why-the-harness-matters-more-than-the-model-yc-paper-club--n9xKblqyQ28|Why The Harness Matters More Than The Model | YC Paper Club]]", "[[extracts/youtube/ai-learning/2026-09-11-harnesses-in-ai-a-deep-dive-tejas-kumar-ibm--C_GG5g38vLU|Harnesses in AI: A Deep Dive — Tejas Kumar, IBM]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-what-separates-top-agentic-engineers-right-now--ulNsa0sD8N0|Harness Engineering: What Separates Top Agentic Engineers Right Now]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-the-art-of-loop-engineering-how-to-build-agents-that-improve-over-time--jPPiZ22DY3g|The Art of Loop Engineering: How to Build Agents That Improve Over Time]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-lifecycle-build-test-deploy-monitor-interrupt-26--jWy39wavbjY|The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-ryan-lopopolo-harness-engineering-how-to-build-software-when-humans-steer-and-ag--c8bE0cj7vHY|Ryan Lopopolo - Harness Engineering: How to Build Software When Humans Steer and Agents Execute]]", "[[extracts/youtube/ai-learning/2026-09-11-hermes-co-founder-on-building-an-ai-agent-that-improves-itself-karan-malhotra--UWjh5Z4s8jY|Hermes Co-Founder on Building an AI Agent That Improves Itself | Karan Malhotra]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-workshop-build-agents-that-run-for-hours-ash-prabaker-andrew-wilson--mR-WAvEPRwE|Anthropic Workshop: Build Agents That Run for Hours — Ash Prabaker & Andrew Wilson]]", "[[extracts/youtube/ai-learning/2026-09-11-hard-won-lessons-from-building-effective-ai-coding-agents-nik-pash-cline--I8fs4omN1no|Hard Won Lessons from Building Effective AI Coding Agents – Nik Pash, Cline]]"]
theme: "Processo de Engenharia Agêntica"
---

# When to Build Your Own Agent Harness | Harrison Chase, LangChain

## Tese
Para 'possuir a própria inteligência' agêntica é necessário controlar os três componentes do agente — harness, modelo e contexto — customizando o harness com middleware sobre o loop básico do agente e alimentando um ciclo contínuo de melhoria com evals privados e observabilidade de traces.

## Conceitos-chave
- agente = harness + modelo + contexto
- loop básico de agente (LLM chamando tools)
- middleware/hooks como pontos de inserção no loop (pré-chamada de modelo, wrapping de model calls e tool calls)
- summarização de contexto e context offloading
- arquiteturas cognitivas bespoke vs harness geral
- espectro in-distribution vs out-of-distribution no design do harness
- model profiles (trocar implementação de tool conforme o modelo)
- ownership de contexto: memória, conhecimento semântico, conversas anteriores
- switchabilidade de modelos para evitar lock-in
- benchmark privado por domínio
- anatomia de task Harbor: environment (Docker sandbox), solution (golden check), tests (verifier), instruction.md
- LLM-as-a-judge e agent-as-a-judge
- trajetórias (messages) vs traces completos para debug
- falha de agente = modelo insuficiente OU contexto insuficiente (o segundo é mais comum)
- data flywheel: rodar agente → coletar traces → curar → experimentar → atualizar harness/modelo/contexto
- feedback implícito via design de UX
- avaliadores online baratos com SLMs fine-tunados
- benchmarking cruzado de harnesses para portar aprendizados ('codeexification')
- predictabilidade/controle como motivo para arquiteturas cognitivas (serviços financeiros)

## Ferramentas & pessoas
**Ferramentas:** LangChain, LangSmith, LangSmith CLI, Deep Agents, LangEngine, Harbor, Terminal Bench 2, Frontier Bench, Issue Bench, Claude Code, Claude Agent SDK, Codex, Slack, Docker

**Pessoas/orgs:** Harrison (co-fundador/CEO da LangChain), LangChain, Gabe (Harvey), Harvey, Lynn (Fireworks), Fireworks, Satcha, Eno (Factory), Factory, Swix, OpenAI, Anthropic

## Claims acionáveis
- Comece com um harness geral off-the-shelf (menor time-to-value) e adicione gates e checks conforme estreita o caso de uso
- Use harness pronto quando a tarefa está in-distribution do treinamento dos modelos; customize progressivamente conforme sai da distribuição
- Mesmo em domínios out-of-distribution (ex: legal AI), mantenha subtarefas in-distribution — como edição de arquivos — no formato em que cada modelo foi RL-treinado, via model profiles
- Todo agente mission-critical merece benchmark próprio; Harbor (open-source, dos criadores do Terminal Bench 2) está virando o padrão da indústria para isso
- Ao benchmarkar agentes, rastreie não só acurácia mas também latência e custo (tokens)
- Na maioria das falhas de agente o problema é o contexto recebido pelo LLM, não a capacidade do modelo — invista em observabilidade do que entra na janela de contexto
- Projete a UX do agente para capturar feedback implícito dos usuários, já que thumbs up/down explícito raramente acontece
- Rode avaliadores online sobre traces com SLMs fine-tunados (ou código, quando suficiente) para baratear LLM-as-a-judge em escala
- É possível atualizar qualquer parte do agente com o flywheel: harness engineering, fine-tuning do modelo ou memória/contexto
- Automatize o flywheel com um agente sobre os traces (LangEngine) que curam dados, criam issues e sugerem fixes
- Crie um benchmark interno (Issue Bench) para o próprio agente de automação e compare múltiplos harnesses, portando aprendizados para o harness central
- Para requisitos de previsibilidade e controle (ex: serviços financeiros), prefira arquiteturas cognitivas customizadas a harnesses agentivos gerais
- Espera-se convergência parcial dos harnesses em domínios treinados pelos labs (ex: coding), mas divergência em domínios verticais — por isso evals e observabilidade são essenciais

> **Deep dive:** `high` — Alta densidade de insight arquitetural acionável (pontos de middleware no loop, model profiles, anatomia de tasks Harbor, flywheel automatizado via LangEngine) diretamente relevante a harness, context-engineering, evals e observabilidade, com novidade além do senso comum.
