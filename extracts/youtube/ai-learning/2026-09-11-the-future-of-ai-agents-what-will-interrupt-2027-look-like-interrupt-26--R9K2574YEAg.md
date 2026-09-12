---
title: "The Future of AI Agents: What Will Interrupt 2027 Look Like? | Interrupt 26"
type: "extract"
source: "youtube"
video_id: "R9K2574YEAg"
url: "https://www.youtube.com/watch?v=R9K2574YEAg"
channel: "LangChain"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-future-of-ai-agents-what-will-interrupt-2027-look-like-interrupt-26--R9K2574YEAg.txt]]"
tags: ["agents", "agent-fleets", "agent-tooling", "harness-engineering", "context-engineering", "evals", "model-selection", "governanca", "multi-agent", "permissions", "memory-architecture", "roadmap", "runtime", "tracing", "production"]
thesis: "Os agentes divergirão em duas categorias (longo-horizonte e experiência-do-cliente de baixa latência) e evoluirão via aprendizado contínuo em três camadas (modelo, harness e contexto), com especialistas de domínio construindo agentes sem código através do LangSmith Fleet."
concepts: ["Agentes de longo horizonte (minutos/horas/dias, com planejamento, subagentes, multi-agentes e skills)", "Agentes de experiência do cliente sensíveis a latência (suporte, vendas, voz, marca)", "Pipeline de voz STT→agente→TTS vs. modelos nativos speech-to-speech", "Sandboxes e execução de código para agentes (além de software: análise de dados, navegação web, image gen, deep research)", "Modelos abertos: desempenho base próximo de frontier, vantagem de custo e pós-treinamento por domínio", "Identidade do agente: credenciais delegadas do usuário vs. conta de serviço fixa", "Aprendizado contínuo em três camadas: modelo, harness e contexto", "Evals como função de força análoga ao gradiente de treinamento nos níveis de harness e contexto", "Traces e feedback como base para melhoria do sistema agêntico", "Construção de agentes sem código por especialistas de domínio (instruções + skills + ferramentas)", "Governança, credenciais e controle de custos como gargalos na escala de agentes", "Memória embutida em agentes e human-in-the-loop de primeira classe"]
tools: ["LangSmith", "LangSmith Fleet", "LangChain Labs", "deep agents", "Claude Code", "pi", "agent.md", "MetaHarness (paper MIT/Stanford)", "Terminal Bench 2", "Sonnet", "GLM4", "GPT-4", "Qwen 3.5", "Modelo de voz V2 da OpenAI (speech-to-speech)", "Arcade", "MCP", "Fireworks", "LangGraph", "Slack", "Gmail", "Outlook", "Salesforce", "BigQuery", "OpenSuite"]
people: ["Harrison Chase", "Caroline di Vittorio", "Brace", "LangChain", "LinkedIn", "OpenAI", "Ramp", "Prime Intellect", "MIT", "Stanford"]
claims: ["Agentes tenderão a divergir em dois tipos — longo-horizonte (execução de código, planejamento, subagentes, multi-agentes) e experiência-do-cliente com baixa latência — compartilhando parcialmente a mesma stack", "Modelos nativos speech-to-speech ainda não são suficientemente steerables para aplicações que exigem controle, mas isso deve mudar", "Todo agente precisará de sandbox: capacidade de escrever e executar código serve a análise de dados, navegação web, geração de imagens e deep research, não apenas engenharia de software", "Modelos abertos sem pós-treinamento já se aproximam de modelos frontier em benchmarks de deep agents; custo de tokens (especialmente agents de coding) e fine-tuning por domínio impulsionarão sua adoção", "Há dois padrões de identidade para agentes — agir em nome do usuário (credenciais delegadas) vs. conta de serviço fixa — ambos coexistirão, e ser preciso sobre quando usar cada um e deixá-lo claro ao usuário será crítico", "Aprendizado contínuo opera em três camadas: modelo (fine-tuning, ex.: Ramp/Prime Intellect afinando Qwen 3.5), harness (otimização do código ao redor do modelo) e contexto (agent.md, skills)", "Evals funcionam como gradiente de treinamento no nível de harness/contexto: rodar o agente em benchmark, capturar feedback do ambiente e alimentar um sistema agêntico que edita o harness (MetaHarness superou harnesses escritos por humanos no Terminal Bench 2)", "LangChain subiu do top 30 para o top 5 no Terminal Bench 2 alterando apenas o harness, sem mudanças no modelo", "Traces e feedback acumulados em plataformas como LangSmith são a fundação para aprendizado contínuo nas três camadas", "Os melhores construtores de agentes são quem executa o trabalho: agentes são coleções de instruções, skills e ferramentas que especialistas de domínio podem codificar sem escrever código", "Agentes precisam operar onde os usuários trabalham (Slack, Gmail, Outlook) e acessar os mesmos sistemas (200+ ferramentas nativas em Fleet, +7.500 via Arcade, suporte a MCP)", "Ao escalar agentes internamente, governança, gerenciamento de credenciais por usuário/agente e cost tracking com spend limits tornam-se requisitos de primeira classe", "Agente GTM interno da LangChain: 84% de uso semanal pelo time, +240% em conversão lead→qualificado e ~40 horas economizadas por rep/mês", "Fleet é agnóstico a modelos, construído sobre deep agents e permite baixar os arquivos do agente para modificação direta em código"]
deep_dive: "medium"
deep_dive_reason: "Combina insights arquiteturais acionáveis (aprendizado contínuo em três camadas, evals como gradiente, padrões de identidade do agente) com conteúdo promocional de lançamento de produto e previsões de keynote sem detalhes de implementação aprofundados."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-introducing-managed-deep-agents-interrupt-26--LdQpoK2TzSo|Introducing Managed Deep Agents | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-lifecycle-build-test-deploy-monitor-interrupt-26--jWy39wavbjY|The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-ai-agents-need-less-code-than-you-think--YqjR4vQwbTc|The best AI agents need less code than you think]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-ai-agents-are-simpler-than-you-think--uCKhOmth2ms|The best AI agents are simpler than you think]]", "[[extracts/youtube/ai-learning/2026-09-11-microsoft-ceo-satya-nadella-on-the-future-of-ai--w87UvmMcmW4|Microsoft CEO Satya Nadella on the Future of AI]]", "[[extracts/youtube/ai-learning/2026-09-11-grok-3-5-leaks-ai-takes-software-dev-jobs--0QPf-9El_2s|Grok 3.5 Leaks! AI Takes Software Dev Jobs!]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-interfaces-of-the-future-design-review--DBhSfROq3wU|AI Interfaces Of The Future | Design Review]]", "[[extracts/youtube/ai-learning/2026-09-11-novo-agente-com-passos-infinitos-destronou-manus-flowith-perplexity-labs--plbXQ2SbAMg|NOVO AGENTE com Passos INFINITOS Destronou MANUS? (FLOWITH + Perplexity Labs)]]"]
---

# The Future of AI Agents: What Will Interrupt 2027 Look Like? | Interrupt 26

## Tese
Os agentes divergirão em duas categorias (longo-horizonte e experiência-do-cliente de baixa latência) e evoluirão via aprendizado contínuo em três camadas (modelo, harness e contexto), com especialistas de domínio construindo agentes sem código através do LangSmith Fleet.

## Conceitos-chave
- Agentes de longo horizonte (minutos/horas/dias, com planejamento, subagentes, multi-agentes e skills)
- Agentes de experiência do cliente sensíveis a latência (suporte, vendas, voz, marca)
- Pipeline de voz STT→agente→TTS vs. modelos nativos speech-to-speech
- Sandboxes e execução de código para agentes (além de software: análise de dados, navegação web, image gen, deep research)
- Modelos abertos: desempenho base próximo de frontier, vantagem de custo e pós-treinamento por domínio
- Identidade do agente: credenciais delegadas do usuário vs. conta de serviço fixa
- Aprendizado contínuo em três camadas: modelo, harness e contexto
- Evals como função de força análoga ao gradiente de treinamento nos níveis de harness e contexto
- Traces e feedback como base para melhoria do sistema agêntico
- Construção de agentes sem código por especialistas de domínio (instruções + skills + ferramentas)
- Governança, credenciais e controle de custos como gargalos na escala de agentes
- Memória embutida em agentes e human-in-the-loop de primeira classe

## Ferramentas & pessoas
**Ferramentas:** LangSmith, LangSmith Fleet, LangChain Labs, deep agents, Claude Code, pi, agent.md, MetaHarness (paper MIT/Stanford), Terminal Bench 2, Sonnet, GLM4, GPT-4, Qwen 3.5, Modelo de voz V2 da OpenAI (speech-to-speech), Arcade, MCP, Fireworks, LangGraph, Slack, Gmail, Outlook, Salesforce, BigQuery, OpenSuite

**Pessoas/orgs:** Harrison Chase, Caroline di Vittorio, Brace, LangChain, LinkedIn, OpenAI, Ramp, Prime Intellect, MIT, Stanford

## Claims acionáveis
- Agentes tenderão a divergir em dois tipos — longo-horizonte (execução de código, planejamento, subagentes, multi-agentes) e experiência-do-cliente com baixa latência — compartilhando parcialmente a mesma stack
- Modelos nativos speech-to-speech ainda não são suficientemente steerables para aplicações que exigem controle, mas isso deve mudar
- Todo agente precisará de sandbox: capacidade de escrever e executar código serve a análise de dados, navegação web, geração de imagens e deep research, não apenas engenharia de software
- Modelos abertos sem pós-treinamento já se aproximam de modelos frontier em benchmarks de deep agents; custo de tokens (especialmente agents de coding) e fine-tuning por domínio impulsionarão sua adoção
- Há dois padrões de identidade para agentes — agir em nome do usuário (credenciais delegadas) vs. conta de serviço fixa — ambos coexistirão, e ser preciso sobre quando usar cada um e deixá-lo claro ao usuário será crítico
- Aprendizado contínuo opera em três camadas: modelo (fine-tuning, ex.: Ramp/Prime Intellect afinando Qwen 3.5), harness (otimização do código ao redor do modelo) e contexto (agent.md, skills)
- Evals funcionam como gradiente de treinamento no nível de harness/contexto: rodar o agente em benchmark, capturar feedback do ambiente e alimentar um sistema agêntico que edita o harness (MetaHarness superou harnesses escritos por humanos no Terminal Bench 2)
- LangChain subiu do top 30 para o top 5 no Terminal Bench 2 alterando apenas o harness, sem mudanças no modelo
- Traces e feedback acumulados em plataformas como LangSmith são a fundação para aprendizado contínuo nas três camadas
- Os melhores construtores de agentes são quem executa o trabalho: agentes são coleções de instruções, skills e ferramentas que especialistas de domínio podem codificar sem escrever código
- Agentes precisam operar onde os usuários trabalham (Slack, Gmail, Outlook) e acessar os mesmos sistemas (200+ ferramentas nativas em Fleet, +7.500 via Arcade, suporte a MCP)
- Ao escalar agentes internamente, governança, gerenciamento de credenciais por usuário/agente e cost tracking com spend limits tornam-se requisitos de primeira classe
- Agente GTM interno da LangChain: 84% de uso semanal pelo time, +240% em conversão lead→qualificado e ~40 horas economizadas por rep/mês
- Fleet é agnóstico a modelos, construído sobre deep agents e permite baixar os arquivos do agente para modificação direta em código

> **Deep dive:** `medium` — Combina insights arquiteturais acionáveis (aprendizado contínuo em três camadas, evals como gradiente, padrões de identidade do agente) com conteúdo promocional de lançamento de produto e previsões de keynote sem detalhes de implementação aprofundados.
