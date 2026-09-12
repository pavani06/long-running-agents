---
title: "Build AI agent workforce - Multi agent framework with MetaGPT & chatDev"
type: "extract"
source: "youtube"
video_id: "pJwR5pv0_gs"
url: "https://www.youtube.com/watch?v=pJwR5pv0_gs"
channel: "AI Jason"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-ai-agent-workforce-multi-agent-framework-with-metagpt-chatdev--pJwR5pv0_gs.txt]]"
tags: ["agents", "multi-agent", "agent-fleets", "frameworks", "agentic-coding", "agent-tooling", "stack-tooling", "process", "arquitetura"]
thesis: "Frameworks multi-agentes como ChatDev permitem orquestrar equipes de agentes de IA com papéis especializados (definidos via roles, phases e chat chain) para executar processos complexos de ponta a ponta, como desenvolvimento de software ou operações de conteúdo, de forma customizável e a baixo custo."
concepts: ["Componentes de um agente autônomo: perfil, memória (conhecimento de domínio + memória curta), planejamento via LLM e uso de ferramentas/APIs", "Simulação de conversas entre múltiplos agentes (sóciofones de papéis)", "Roles: definição de agentes com papéis e responsabilidades (CEO, PM, CTO, QA)", "Phases: estágios de tarefa simulando diálogo entre dois agentes com papéis de assistente e usuário", "Chat chain: encadeamento de fases formando o procedimento operacional padrão do time", "Compositional phase: fase composta de sub-passos repetidos ciclicamente (ex.: code review + modificação, máximo 3 ciclos)", "Reflection: passo de reflexão pós-fase por CEO e conselheiro", "Mecanismo de término de conversa via marcador de formato especial (linha iniciada por 'info') para avançar de fase", "Passagem de variáveis globais de ambiente entre fases (ex.: task, ideas) via classes Phase em phase.py", "Customização de times de agentes além de software (ex.: agência de marketing)"]
tools: ["ChatDev", "MetaGPT", "CAMEL", "AgentVerse (citado como 'Adrian verse')", "AutoGPT", "BabyAGI", "OpenAI API", "Python (pip, run.py)", "Visual Studio Code", "GitHub", "ChatDev online_log_app.py (replay visual de conversas)", "HubSpot (pesquisa patrocinada)", "Jasper"]
people: ["HubSpot", "Jasper", "OpenAI", "AI Jason (canal/newsletter do apresentador)", "AutoGPT e BabyAGI (projetos)"]
claims: ["Agentes de IA autônomos têm quatro componentes centrais: perfil, memória, planejamento e uso de ferramentas", "No período de 6 a 12 meses, empresas começarão a contratar agentes de IA especializados (designer, desenvolvedor, PM, marketing) como parte da força de trabalho", "ChatDev entrega software funcional compacto (snake game, Flappy Bird, calculadora, 2048, editor de imagens) por menos de US$ 0,10 de custo de API por projeto", "Cada phase no ChatDev é implementada como uma conversa simulada entre dois agentes (ex.: CEO+PM para requisitos; CTO+programador para código)", "Para evitar que a conversa entre agentes divague, o prompt deve restringir o escopo e definir um marcador de término em formato específico (linha iniciada por 'info') que sinaliza o fim da fase", "Fases compostas permitem ciclos repetidos (ex.: code review com comentário e modificação) limitados a um máximo de iterações (3)", "Customizar um novo time exige: duplicar a pasta de configuração default, editar role config, phase config e chat chain config, além de implementar classes Phase em phase.py para capturar variáveis de ambiente", "O replay das conversas entre agentes pode ser visualizado numa web app carregando o arquivo de log do projeto gerado em warehouse/"]
deep_dive: "medium"
deep_dive_reason: "Tutorial prático com insights acionáveis reais de configuração do ChatDev (roles/phases/chat chain, marcador de término de conversa, passagem de estado entre fases), porém sem novidade arquitetural significativa nem cobertura de harness, evals ou governança, e com trecho promocional."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-research-agent-3-0-build-a-group-of-ai-researchers-here-is-how--AVInhYBUnKs|\"Research agent 3.0 - Build a group of AI researchers\" - Here is how]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-uber-dev-explains-his-multi-agent-workflow--utb7zYbK10c|Ex-Uber dev explains his Multi-Agent Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-could-a-swarm-of-autonomous-ai-agents-be-the-ultimate-business-asset-stage-1--UL55C80TEb8|Could a Swarm of Autonomous AI Agents be the Ultimate Business Asset? - Stage 1]]", "[[extracts/youtube/ai-learning/2026-09-11-chatgpt-for-business-updates--9lSRViLugE0|ChatGPT for Business Updates]]"]
theme: "Orquestração Multiagente em Escala"
---

# Build AI agent workforce - Multi agent framework with MetaGPT & chatDev

## Tese
Frameworks multi-agentes como ChatDev permitem orquestrar equipes de agentes de IA com papéis especializados (definidos via roles, phases e chat chain) para executar processos complexos de ponta a ponta, como desenvolvimento de software ou operações de conteúdo, de forma customizável e a baixo custo.

## Conceitos-chave
- Componentes de um agente autônomo: perfil, memória (conhecimento de domínio + memória curta), planejamento via LLM e uso de ferramentas/APIs
- Simulação de conversas entre múltiplos agentes (sóciofones de papéis)
- Roles: definição de agentes com papéis e responsabilidades (CEO, PM, CTO, QA)
- Phases: estágios de tarefa simulando diálogo entre dois agentes com papéis de assistente e usuário
- Chat chain: encadeamento de fases formando o procedimento operacional padrão do time
- Compositional phase: fase composta de sub-passos repetidos ciclicamente (ex.: code review + modificação, máximo 3 ciclos)
- Reflection: passo de reflexão pós-fase por CEO e conselheiro
- Mecanismo de término de conversa via marcador de formato especial (linha iniciada por 'info') para avançar de fase
- Passagem de variáveis globais de ambiente entre fases (ex.: task, ideas) via classes Phase em phase.py
- Customização de times de agentes além de software (ex.: agência de marketing)

## Ferramentas & pessoas
**Ferramentas:** ChatDev, MetaGPT, CAMEL, AgentVerse (citado como 'Adrian verse'), AutoGPT, BabyAGI, OpenAI API, Python (pip, run.py), Visual Studio Code, GitHub, ChatDev online_log_app.py (replay visual de conversas), HubSpot (pesquisa patrocinada), Jasper

**Pessoas/orgs:** HubSpot, Jasper, OpenAI, AI Jason (canal/newsletter do apresentador), AutoGPT e BabyAGI (projetos)

## Claims acionáveis
- Agentes de IA autônomos têm quatro componentes centrais: perfil, memória, planejamento e uso de ferramentas
- No período de 6 a 12 meses, empresas começarão a contratar agentes de IA especializados (designer, desenvolvedor, PM, marketing) como parte da força de trabalho
- ChatDev entrega software funcional compacto (snake game, Flappy Bird, calculadora, 2048, editor de imagens) por menos de US$ 0,10 de custo de API por projeto
- Cada phase no ChatDev é implementada como uma conversa simulada entre dois agentes (ex.: CEO+PM para requisitos; CTO+programador para código)
- Para evitar que a conversa entre agentes divague, o prompt deve restringir o escopo e definir um marcador de término em formato específico (linha iniciada por 'info') que sinaliza o fim da fase
- Fases compostas permitem ciclos repetidos (ex.: code review com comentário e modificação) limitados a um máximo de iterações (3)
- Customizar um novo time exige: duplicar a pasta de configuração default, editar role config, phase config e chat chain config, além de implementar classes Phase em phase.py para capturar variáveis de ambiente
- O replay das conversas entre agentes pode ser visualizado numa web app carregando o arquivo de log do projeto gerado em warehouse/

> **Deep dive:** `medium` — Tutorial prático com insights acionáveis reais de configuração do ChatDev (roles/phases/chat chain, marcador de término de conversa, passagem de estado entre fases), porém sem novidade arquitetural significativa nem cobertura de harness, evals ou governança, e com trecho promocional.
