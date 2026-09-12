---
title: "12-Factor Agents: Patterns of reliable LLM applications — Dex Horthy, HumanLayer"
type: "extract"
source: "youtube"
video_id: "8kMaTybvDUw"
url: "https://www.youtube.com/watch?v=8kMaTybvDUw"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-12-factor-agents-patterns-of-reliable-llm-applications-dex-horthy-humanlayer--8kMaTybvDUw.txt]]"
tags: ["12-factor-agents", "agent-loop", "agent-tooling", "agents", "arquitetura", "context-engineering", "context-management", "error-handling", "escalation", "frameworks", "harness-engineering", "production", "runtime", "state", "token-budgeting", "process"]
thesis: "Agentes de IA confiáveis devem ser construídos como software comum — com o engenheiro possuindo o loop de controle, os prompts, o estado e a janela de contexto — em vez de delegar essas decisões a frameworks, conforme sistematizado nos '12 factor agents'."
concepts: ["12 factor agents", "agentes como software (loops + switch statements)", "posse do fluxo de controle (own your control flow)", "posse dos prompts (escrever cada token à mão)", "engenharia de contexto / janela de contexto como propriedade do desenvolvedor", "LLMs como funções puras e stateless (tokens in, tokens out)", "tool use é apenas JSON + código determinístico (analogia a 'Go To Considered Harmful')", "separação entre estado de execução e estado de negócio", "pause/resume serializando o contexto em banco de dados", "micro-agentes pequenos e focados (3–10 passos) embutidos em DAGs determinísticas", "limpeza e sumarização de erros no contexto (não despejar stack traces)", "empurrar a intenção para o primeiro token em linguagem natural antes de decidir tool call vs mensagem", "acionar agentes de qualquer canal (email, Slack, Discord, SMS)", "limite de confiabilidade: engenheirar confiabilidade em tarefas na fronteira da capacidade do modelo", "frameworks vs bibliotecas / scaffolding estilo shadcn", "migração gradual de pipelines determinísticos para endpoints agent-run", "nem todo problema precisa de agente (anécdota do agente DevOps vs bash script)"]
tools: ["12 Factor Agents (repositório GitHub)", "create-12-factor-agent", "HumanLayer", "A2 Protocol", "MCP server", "REST API", "Airflow", "Prefect", "Gemini", "formato de mensagens OpenAI", "NotebookLM", "shadcn", "Slack", "Discord", "Heroku", "Makefile/bash", "Hacker News"]
people: ["HumanLayer", "Heroku", "Google (Gemini, NotebookLM)", "OpenAI", "comunidade do repositório 12-factor-agents (contribuidores)"]
claims: ["A maioria dos agentes em produção não é muito 'agêntica' — são majoritariamente software com pequenos loops de LLM embutidos", "A habilidade mais mágica dos LLMs é transformar linguagem natural em JSON estruturado; todo o resto é código determinístico em volta", "Tool use não é mágico: o LLM emite JSON que alimenta um switch statement ou loop — trate-o assim para reduzir complexidade", "Para passar da barreira de 70–80% de qualidade, é preciso possuir o loop interno, os prompts e a construção do contexto em vez de depender de abstrações de framework", "Janelas de contexto muito longas degradam a confiabilidade; limitar e curar os tokens de entrada produz resultados consistentemente melhores", "Eventualmente você escreverá cada token do prompt à mão, pois a confiabilidade do agente é determinada pelos tokens de entrada", "Mode o estado do evento/thread como quiser (não apenas o formato de mensagens OpenAI) e otimize densidade e clareza do contexto", "Separe estado de execução (passo atual, retries) de estado de negócio (mensagens, aprovações pendentes) e trate o agente como API pausável/resumível", "Ao interromper para ferramentas de longa duração, serialize a janela de contexto num banco e recarregue-a pelo state ID ao retomar — o agente nem percebe", "Não anexe erros cegamente ao contexto: após obter um tool call válido, limpe os erros pendentes, sumarize e evite stack traces completos", "Adie a decisão entre tool call e mensagem ao humano empurrando a intenção para um primeiro token em linguagem natural (ex.: 'pronto', 'preciso de esclarecimento', 'preciso de um gerente')", "Construa micro-agentes de 3–10 passos embutidos em pipelines determinísticas (ex.: agente de deploy entre CI/CD e testes de produção), com contexto manejável e responsabilidades claras", "Escolha tarefas na fronteira do que o modelo faz confiavelmente e engenheire confiabilidade no sistema — isso cria vantagem competitiva", "Comece com DAGs majoritariamente determinísticas 'salpicando' LLMs e deixe os trechos agent-run crescerem conforme os modelos melhoram", "Prefira scaffolding que você possui (estilo shadcn, como create-12-factor-agent) a wrappers/opinionated frameworks em torno de internals", "Frameworks deveriam remover as partes difíceis não-AI para que o engenheiro foque nas partes difíceis de AI: prompts, fluxo e tokens", "Teste se o problema realmente exige um agente — alguns 'agentes' se resolvem com um script bash de 90 segundos", "A2 Protocol busca consolidar um padrão para agentes contactarem humanos; agentes são melhores quando colaboram com pessoas"]
deep_dive: "high"
deep_dive_reason: "A palestra entrega densidade alta de guidance arquitetural acionável e novel sobre harness, posse de loop/estado, engenharia de contexto, tratamento de erros e escalonamento humano — diretamente relevante a context-engineering, harness e produção de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-agent-frameworks-considered-harmful-remi-louf-txt--KHudyx5wW3U|Agent Frameworks Considered Harmful — Rémi Louf, .txt]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-build-effective-agents-barry-zhang-anthropic--D7_ipDqhtwk|How We Build Effective Agents: Barry Zhang, Anthropic]]", "[[extracts/youtube/ai-learning/2026-09-11-why-more-context-makes-your-agent-dumber-and-what-to-do-about-it-nupur-sharma-qo--EcqMYoIV57A|Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo]]", "[[extracts/youtube/ai-learning/2026-09-11-26-key-takeaways-from-building-150-agents-in-9-months--jmeGqDu4tPU|26 Key Takeaways from Building 150+ Agents in 9 months]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-why-senior-engineers-struggle-to-build-ai-agents-philipp-schmid-google-deepmind--3_gYbhABcAE|Why (Senior) Engineers Struggle to Build AI Agents — Philipp Schmid, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-why-your-enterprise-tech-stack-isnt-ready-for-ai-agents-christopher-lovejoy-saul--mav15aW9lLM|Why Your Enterprise Tech Stack Isn’t Ready for AI Agents — Christopher Lovejoy & Saul Howard]]", "[[extracts/youtube/ai-learning/2026-09-11-building-agent-interfaces-lessons-from-chrome-devtools-mcp-for-agents-michael-ha--_B4Pv9ttFgY|Building Agent Interfaces: Lessons from Chrome DevTools (MCP) for Agents — Michael Hablich, Google]]", "[[extracts/youtube/ai-learning/2026-09-11-beyond-the-prompt-goodbye-slop-welcome-determinism-david-khourshid--uMvTAF280so|Beyond the Prompt: \"Goodbye slop; welcome determinism\" David Khourshid]]"]
theme: "Engenharia de Agentes Confiáveis"
---

# 12-Factor Agents: Patterns of reliable LLM applications — Dex Horthy, HumanLayer

## Tese
Agentes de IA confiáveis devem ser construídos como software comum — com o engenheiro possuindo o loop de controle, os prompts, o estado e a janela de contexto — em vez de delegar essas decisões a frameworks, conforme sistematizado nos '12 factor agents'.

## Conceitos-chave
- 12 factor agents
- agentes como software (loops + switch statements)
- posse do fluxo de controle (own your control flow)
- posse dos prompts (escrever cada token à mão)
- engenharia de contexto / janela de contexto como propriedade do desenvolvedor
- LLMs como funções puras e stateless (tokens in, tokens out)
- tool use é apenas JSON + código determinístico (analogia a 'Go To Considered Harmful')
- separação entre estado de execução e estado de negócio
- pause/resume serializando o contexto em banco de dados
- micro-agentes pequenos e focados (3–10 passos) embutidos em DAGs determinísticas
- limpeza e sumarização de erros no contexto (não despejar stack traces)
- empurrar a intenção para o primeiro token em linguagem natural antes de decidir tool call vs mensagem
- acionar agentes de qualquer canal (email, Slack, Discord, SMS)
- limite de confiabilidade: engenheirar confiabilidade em tarefas na fronteira da capacidade do modelo
- frameworks vs bibliotecas / scaffolding estilo shadcn
- migração gradual de pipelines determinísticos para endpoints agent-run
- nem todo problema precisa de agente (anécdota do agente DevOps vs bash script)

## Ferramentas & pessoas
**Ferramentas:** 12 Factor Agents (repositório GitHub), create-12-factor-agent, HumanLayer, A2 Protocol, MCP server, REST API, Airflow, Prefect, Gemini, formato de mensagens OpenAI, NotebookLM, shadcn, Slack, Discord, Heroku, Makefile/bash, Hacker News

**Pessoas/orgs:** HumanLayer, Heroku, Google (Gemini, NotebookLM), OpenAI, comunidade do repositório 12-factor-agents (contribuidores)

## Claims acionáveis
- A maioria dos agentes em produção não é muito 'agêntica' — são majoritariamente software com pequenos loops de LLM embutidos
- A habilidade mais mágica dos LLMs é transformar linguagem natural em JSON estruturado; todo o resto é código determinístico em volta
- Tool use não é mágico: o LLM emite JSON que alimenta um switch statement ou loop — trate-o assim para reduzir complexidade
- Para passar da barreira de 70–80% de qualidade, é preciso possuir o loop interno, os prompts e a construção do contexto em vez de depender de abstrações de framework
- Janelas de contexto muito longas degradam a confiabilidade; limitar e curar os tokens de entrada produz resultados consistentemente melhores
- Eventualmente você escreverá cada token do prompt à mão, pois a confiabilidade do agente é determinada pelos tokens de entrada
- Mode o estado do evento/thread como quiser (não apenas o formato de mensagens OpenAI) e otimize densidade e clareza do contexto
- Separe estado de execução (passo atual, retries) de estado de negócio (mensagens, aprovações pendentes) e trate o agente como API pausável/resumível
- Ao interromper para ferramentas de longa duração, serialize a janela de contexto num banco e recarregue-a pelo state ID ao retomar — o agente nem percebe
- Não anexe erros cegamente ao contexto: após obter um tool call válido, limpe os erros pendentes, sumarize e evite stack traces completos
- Adie a decisão entre tool call e mensagem ao humano empurrando a intenção para um primeiro token em linguagem natural (ex.: 'pronto', 'preciso de esclarecimento', 'preciso de um gerente')
- Construa micro-agentes de 3–10 passos embutidos em pipelines determinísticas (ex.: agente de deploy entre CI/CD e testes de produção), com contexto manejável e responsabilidades claras
- Escolha tarefas na fronteira do que o modelo faz confiavelmente e engenheire confiabilidade no sistema — isso cria vantagem competitiva
- Comece com DAGs majoritariamente determinísticas 'salpicando' LLMs e deixe os trechos agent-run crescerem conforme os modelos melhoram
- Prefira scaffolding que você possui (estilo shadcn, como create-12-factor-agent) a wrappers/opinionated frameworks em torno de internals
- Frameworks deveriam remover as partes difíceis não-AI para que o engenheiro foque nas partes difíceis de AI: prompts, fluxo e tokens
- Teste se o problema realmente exige um agente — alguns 'agentes' se resolvem com um script bash de 90 segundos
- A2 Protocol busca consolidar um padrão para agentes contactarem humanos; agentes são melhores quando colaboram com pessoas

> **Deep dive:** `high` — A palestra entrega densidade alta de guidance arquitetural acionável e novel sobre harness, posse de loop/estado, engenharia de contexto, tratamento de erros e escalonamento humano — diretamente relevante a context-engineering, harness e produção de agentes.
