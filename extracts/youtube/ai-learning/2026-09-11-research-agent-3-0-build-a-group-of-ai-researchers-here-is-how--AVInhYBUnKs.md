---
title: "\"Research agent 3.0 - Build a group of AI researchers\" - Here is how"
type: "extract"
source: "youtube"
video_id: "AVInhYBUnKs"
url: "https://www.youtube.com/watch?v=AVInhYBUnKs"
channel: "AI Jason"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-research-agent-3-0-build-a-group-of-ai-researchers-here-is-how--AVInhYBUnKs.txt]]"
tags: ["agents", "multi-agent", "agentes-orquestracao", "agent-fleets", "agent-loop", "agent-tooling", "frameworks", "context-management", "memory-architecture", "gate-design", "stack-tooling", "token-budgeting"]
thesis: "A evolução de agentes de pesquisa em IA — de cadeias lineares de LLM para sistemas multi-agente hierárquicos (diretor, gerente de pesquisa e pesquisador) orquestrados via AutoGen e Assistant API — permite pesquisa autônoma com controle de qualidade e persistência de resultados no Airtable."
concepts: ["Agente de IA como LLM + memória + ferramentas, orientado a objetivos", "Sistemas multi-agente com hierarquia e delegação (diretor → gerente → pesquisador)", "Agente gerente como controle de qualidade persistente que critica e força novas tentativas", "Function calling (busca Google, scraping web, leitura/escrita no Airtable)", "Gerenciamento de memória via sumarização de conteúdo longo antes de passar ao agente", "Processamento sequencial de tarefas para preservar qualidade vs. chamadas paralelas", "Condição de término explícita ('terminate') controlada pelo agente revisor", "Diferença entre RAG (dados precisos/atualizados) e fine-tuning (estilo/habilidade de tarefa)", "User proxy agent no AutoGen para executar código e dar feedback em nome do usuário", "Customização do fluxo do group chat para particionar memória entre agentes"]
tools: ["AutoGen (versão 0.2.0b5 para GPT Assistants)", "OpenAI Assistant API", "GPTs customizados", "GPT-4 Turbo", "Airtable API (tokens, leitura e atualização de registros)", "Serper (busca Google)", "Browserless (scraping)", "LangChain (summarize chain, text splitter, refine)", "RapidAPI", "Gradient AI (fine-tuning pay-per-token)", "Visual Studio Code", "Llama 2 / Nous Hermes"]
people: ["OpenAI", "Sam Altman", "AutoGen", "Gradient AI", "Airtable", "LangChain", "MGPT", "ChatDev"]
claims: ["Estruture a frota em três papéis: diretor (lê/escreve Airtable e decompõe o objetivo), gerente de pesquisa (gera plano, critica resultados e só diz 'terminate' quando a informação for encontrada) e pesquisador (busca e scraping com no máximo 3 iterações).", "Use o GPTAssistantAgent do AutoGen para encapsular a Assistant API e evitar o boilerplate de criar run, enviar mensagem e fazer polling manual do status.", "Fixe a versão autogen 0.2.0b5 — versão específica exigida para rodar GPT Assistants no AutoGen.", "Sumarize automaticamente qualquer conteúdo extraído com mais de ~10.000 caracteres (via LangChain summarize chain) para não estourar a memória do agente.", "Passe um campo 'objective' junto à URL no scraping para que a sumarização preserve os detalhes relevantes ao objetivo da pesquisa.", "Instrua o diretor a delegar uma tarefa por vez e atualizar o registro no Airtable após cada pesquisa concluída — delegar tudo em paralelo (muitas buscas simultâneas) degrada a qualidade quando há muitos itens.", "Limite o contexto do diretor ao output final do gerente em vez do transcript completo da conversa, para controlar a memória por agente.", "Exclua fontes com gated content ou baixa qualidade (ex.: G2, LinkedIn) diretamente no prompt do pesquisador.", "Escreva o prompt do gerente como 'harsh and relentless', exigindo persistência e propondo o próximo método quando o pesquisador não encontrar a informação.", "Use RAG quando precisar de dados precisos e atualizados; use fine-tuning quando quiser melhorar a habilidade/estilo do modelo em tarefas específicas.", "Monitore o consumo da API OpenAI: loops multi-agente autônomos podem gerar custos altos rapidamente.", "A nova capacidade de chamadas paralelas de funções permite disparar múltiplas atualizações do Airtable numa única ação do assistente."]
deep_dive: "medium"
deep_dive_reason: "Tutorial passo a passo com padrões arquiteturais acionáveis (hierarquia de agentes, gate de QA persistente, sumarização e particionamento de memória), mas sem novidade profunda em evals, harness ou governança e com trecho promocional de patrocinador."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-to-build-deep-research-google-docs-ai-agents-full-tutorial--yQ4F553zhQw|How to Build Deep Research Google Docs AI AGENTS - Full Tutorial]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-create-agent-swarms-with-the-new-openai-assistants-api--8fMnAZI1bdA|How to Create Agent Swarms With the NEW OpenAI Assistants API]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-uber-dev-explains-his-multi-agent-workflow--utb7zYbK10c|Ex-Uber dev explains his Multi-Agent Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-could-a-swarm-of-autonomous-ai-agents-be-the-ultimate-business-asset-stage-1--UL55C80TEb8|Could a Swarm of Autonomous AI Agents be the Ultimate Business Asset? - Stage 1]]", "[[extracts/youtube/ai-learning/2026-09-11-build-ai-agent-workforce-multi-agent-framework-with-metagpt-chatdev--pJwR5pv0_gs|Build AI agent workforce - Multi agent framework with MetaGPT & chatDev]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-power-each-ai-agent-with-a-different-local-llm-autogen-ollama-tutorial--y7wMTwJN7rA|Power Each AI Agent With A Different LOCAL LLM (AutoGen + Ollama Tutorial)]]", "[[extracts/youtube/ai-learning/2026-09-11-rag-is-exploding-58-new-rag-methods-in-48-hours--cHVQj7w9TD4|RAG is Exploding: 58 NEW RAG Methods in 48 hours]]"]
---

# "Research agent 3.0 - Build a group of AI researchers" - Here is how

## Tese
A evolução de agentes de pesquisa em IA — de cadeias lineares de LLM para sistemas multi-agente hierárquicos (diretor, gerente de pesquisa e pesquisador) orquestrados via AutoGen e Assistant API — permite pesquisa autônoma com controle de qualidade e persistência de resultados no Airtable.

## Conceitos-chave
- Agente de IA como LLM + memória + ferramentas, orientado a objetivos
- Sistemas multi-agente com hierarquia e delegação (diretor → gerente → pesquisador)
- Agente gerente como controle de qualidade persistente que critica e força novas tentativas
- Function calling (busca Google, scraping web, leitura/escrita no Airtable)
- Gerenciamento de memória via sumarização de conteúdo longo antes de passar ao agente
- Processamento sequencial de tarefas para preservar qualidade vs. chamadas paralelas
- Condição de término explícita ('terminate') controlada pelo agente revisor
- Diferença entre RAG (dados precisos/atualizados) e fine-tuning (estilo/habilidade de tarefa)
- User proxy agent no AutoGen para executar código e dar feedback em nome do usuário
- Customização do fluxo do group chat para particionar memória entre agentes

## Ferramentas & pessoas
**Ferramentas:** AutoGen (versão 0.2.0b5 para GPT Assistants), OpenAI Assistant API, GPTs customizados, GPT-4 Turbo, Airtable API (tokens, leitura e atualização de registros), Serper (busca Google), Browserless (scraping), LangChain (summarize chain, text splitter, refine), RapidAPI, Gradient AI (fine-tuning pay-per-token), Visual Studio Code, Llama 2 / Nous Hermes

**Pessoas/orgs:** OpenAI, Sam Altman, AutoGen, Gradient AI, Airtable, LangChain, MGPT, ChatDev

## Claims acionáveis
- Estruture a frota em três papéis: diretor (lê/escreve Airtable e decompõe o objetivo), gerente de pesquisa (gera plano, critica resultados e só diz 'terminate' quando a informação for encontrada) e pesquisador (busca e scraping com no máximo 3 iterações).
- Use o GPTAssistantAgent do AutoGen para encapsular a Assistant API e evitar o boilerplate de criar run, enviar mensagem e fazer polling manual do status.
- Fixe a versão autogen 0.2.0b5 — versão específica exigida para rodar GPT Assistants no AutoGen.
- Sumarize automaticamente qualquer conteúdo extraído com mais de ~10.000 caracteres (via LangChain summarize chain) para não estourar a memória do agente.
- Passe um campo 'objective' junto à URL no scraping para que a sumarização preserve os detalhes relevantes ao objetivo da pesquisa.
- Instrua o diretor a delegar uma tarefa por vez e atualizar o registro no Airtable após cada pesquisa concluída — delegar tudo em paralelo (muitas buscas simultâneas) degrada a qualidade quando há muitos itens.
- Limite o contexto do diretor ao output final do gerente em vez do transcript completo da conversa, para controlar a memória por agente.
- Exclua fontes com gated content ou baixa qualidade (ex.: G2, LinkedIn) diretamente no prompt do pesquisador.
- Escreva o prompt do gerente como 'harsh and relentless', exigindo persistência e propondo o próximo método quando o pesquisador não encontrar a informação.
- Use RAG quando precisar de dados precisos e atualizados; use fine-tuning quando quiser melhorar a habilidade/estilo do modelo em tarefas específicas.
- Monitore o consumo da API OpenAI: loops multi-agente autônomos podem gerar custos altos rapidamente.
- A nova capacidade de chamadas paralelas de funções permite disparar múltiplas atualizações do Airtable numa única ação do assistente.

> **Deep dive:** `medium` — Tutorial passo a passo com padrões arquiteturais acionáveis (hierarquia de agentes, gate de QA persistente, sumarização e particionamento de memória), mas sem novidade profunda em evals, harness ou governança e com trecho promocional de patrocinador.
