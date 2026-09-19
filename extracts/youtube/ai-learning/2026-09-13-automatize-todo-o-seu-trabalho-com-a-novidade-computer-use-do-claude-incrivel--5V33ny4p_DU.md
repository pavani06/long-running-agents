---
title: "AUTOMATIZE TODO O SEU TRABALHO com a novidade “Computer use” do CLAUDE - INCRÍVEL!"
type: "extract"
source: "youtube"
video_id: "5V33ny4p_DU"
url: "https://www.youtube.com/watch?v=5V33ny4p_DU"
channel: "Negócios em Mente"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-13-automatize-todo-o-seu-trabalho-com-a-novidade-computer-use-do-claude-incrivel--5V33ny4p_DU.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "agentic-coding", "error-handling", "permissions", "runtime"]
thesis: "O recurso 'computer use' do Claude marca a transição da IA passiva para ativa ao controlar diretamente o computador do usuário (capturas de tela, mover cursor, clicar, digitar) para executar tarefas completas de forma autônoma, embora ainda em beta, exigindo supervisão humana e futuras salvaguardas de permissão."
concepts: ["Computer use (controle de computador pelo agente)", "Transição de IA passiva para IA ativa", "Loop de percepção por screenshots e ação (cursor, cliques, digitação)", "Delegação de tarefas complexas multi-etapas", "Elaboração proativa de prompts vagos em instruções específicas", "Correção de erros em tempo real via prompts do usuário", "Autocorreção do agente (detectar e instalar dependências faltantes)", "Agente usando outro agente ('inception' - Claude controlando Claude)", "Automação de tarefas repetitivas operacionais", "Supervisão humana obrigatória", "Riscos de segurança e necessidade de limitações/permissions", "Analogia do 'estagiário' e do acesso remoto estilo TeamViewer", "Acesso restrito via API em fase beta"]
tools: ["Claude (computer use)", "ChatGPT (modo de voz)", "Gemini", "API da Anthropic", "Google (busca)", "Google Lens (tradução)", "Chrome", "Python 3", "TeamViewer", "Bitrix24 (patrocinador)", "MindMaster"]
people: ["Anthropic (Claude)", "OpenAI (ChatGPT)", "Google (Gemini)", "Bitrix24", "TeamViewer"]
claims: ["O Claude computer use preenche formulários de solicitação de fornecedor cruzando dados de uma planilha com pesquisa em outros sites/abas abertas", "O agente opera capturando screenshots da tela para entender o contexto e executando ações físicas como mover o cursor, clicar em botões e digitar texto", "O agente consegue planejar tarefas pessoais complexas como encontrar ponto de observação do nascer do sol, verificar tempo de deslocamento, horário do nascer do sol e criar o evento no calendário com tempo suficiente de deslocamento", "Ao receber um prompt amplo, o Claude expande proativamente com detalhes específicos (ex.: site anos 90 virou gifs animados, contador de visitantes, background colorido, banner 'under construction') antes de executar", "Quando encontra erro de Python não instalado, o agente identifica o problema e instala o Python 3 por conta própria para concluir a tarefa", "O usuário pode coordenar o agente em tempo real com prompts corretivos adicionais quando ele para ou erra (ex.: pedir para remover linha problemática de código)", "O recurso está em beta restrito: apenas desenvolvedores com acesso à API ou empresas parceiras conseguem usar, exigindo rodar na própria máquina, e ainda apresenta bugs", "Há risco real de o agente causar danos (enviar documento para pessoa errada, executar transações), sendo esperado que restrições sejam implementadas, como proibir abrir apps privados ou sites de bancos", "Por enquanto o uso é por conta e risco do usuário e requer supervisão humana constante, mas tende a aumentar fortemente automação e produtividade (ex.: responder e organizar e-mails durante a noite)", "É questão de tempo para que ChatGPT, Gemini e outros concorrentes implementarem funcionalidade equivalente de computer use"]
deep_dive: "low"
deep_dive_reason: "Trata-se de comentário reativo de nível consumidor sobre vídeos de demonstração, com alta carga promocional (patrocinador e canal), sem densidade arquitetural, evals, harness ou detalhes técnicos acionáveis além do superficial."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-automatize-todo-o-seu-trabalho-com-a-ia-project-mariner-do-google-incrivel--E0Jbaikf0o4|AUTOMATIZE TODO O SEU TRABALHO com a IA “Project Mariner” do GOOGLE - INCRÍVEL!]]", "[[extracts/youtube/ai-learning/2026-09-11-building-ai-agents-with-claude-demo--_al9YYnF2xI|Building AI Agents with Claude! (Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-instantly-build-ai-agents-in-n8n-using-claude--uAtSMEBosGU|How to INSTANTLY Build AI Agents in N8N Using Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-head-of-claude-code-on-the-future-of-work-and-productivity--kRgdkOw82F0|Head of Claude Code on the future of work and productivity]]", "[[extracts/youtube/ai-learning/2026-09-11-this-claude-code-x-obsidian-agentic-os-will-be-the-new-meta--njHuj8OxIVI|This Claude Code x Obsidian Agentic OS Will Be The New Meta]]", "[[extracts/youtube/ai-learning/2026-09-11-finally-this-ai-agent-actually-works--XeWZIzndlY4|FINALLY, this AI agent actually works!]]", "[[extracts/youtube/ai-learning/2026-09-18-claude-cowork-and-chat-are-now-one-claude--qMUf-jwSpMo|Claude Cowork and chat are now one Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-integre-o-claude-cowork-com-seu-banco-openfinance-pj-ou-pf--i_AjyQmYvbE|INTEGRE o CLAUDE COWORK com SEU BANCO (OpenFinance - PJ ou PF)]]"]
theme: "Engenharia de Contexto e Agentes"
---

# AUTOMATIZE TODO O SEU TRABALHO com a novidade “Computer use” do CLAUDE - INCRÍVEL!

## Tese
O recurso 'computer use' do Claude marca a transição da IA passiva para ativa ao controlar diretamente o computador do usuário (capturas de tela, mover cursor, clicar, digitar) para executar tarefas completas de forma autônoma, embora ainda em beta, exigindo supervisão humana e futuras salvaguardas de permissão.

## Conceitos-chave
- Computer use (controle de computador pelo agente)
- Transição de IA passiva para IA ativa
- Loop de percepção por screenshots e ação (cursor, cliques, digitação)
- Delegação de tarefas complexas multi-etapas
- Elaboração proativa de prompts vagos em instruções específicas
- Correção de erros em tempo real via prompts do usuário
- Autocorreção do agente (detectar e instalar dependências faltantes)
- Agente usando outro agente ('inception' - Claude controlando Claude)
- Automação de tarefas repetitivas operacionais
- Supervisão humana obrigatória
- Riscos de segurança e necessidade de limitações/permissions
- Analogia do 'estagiário' e do acesso remoto estilo TeamViewer
- Acesso restrito via API em fase beta

## Ferramentas & pessoas
**Ferramentas:** Claude (computer use), ChatGPT (modo de voz), Gemini, API da Anthropic, Google (busca), Google Lens (tradução), Chrome, Python 3, TeamViewer, Bitrix24 (patrocinador), MindMaster

**Pessoas/orgs:** Anthropic (Claude), OpenAI (ChatGPT), Google (Gemini), Bitrix24, TeamViewer

## Claims acionáveis
- O Claude computer use preenche formulários de solicitação de fornecedor cruzando dados de uma planilha com pesquisa em outros sites/abas abertas
- O agente opera capturando screenshots da tela para entender o contexto e executando ações físicas como mover o cursor, clicar em botões e digitar texto
- O agente consegue planejar tarefas pessoais complexas como encontrar ponto de observação do nascer do sol, verificar tempo de deslocamento, horário do nascer do sol e criar o evento no calendário com tempo suficiente de deslocamento
- Ao receber um prompt amplo, o Claude expande proativamente com detalhes específicos (ex.: site anos 90 virou gifs animados, contador de visitantes, background colorido, banner 'under construction') antes de executar
- Quando encontra erro de Python não instalado, o agente identifica o problema e instala o Python 3 por conta própria para concluir a tarefa
- O usuário pode coordenar o agente em tempo real com prompts corretivos adicionais quando ele para ou erra (ex.: pedir para remover linha problemática de código)
- O recurso está em beta restrito: apenas desenvolvedores com acesso à API ou empresas parceiras conseguem usar, exigindo rodar na própria máquina, e ainda apresenta bugs
- Há risco real de o agente causar danos (enviar documento para pessoa errada, executar transações), sendo esperado que restrições sejam implementadas, como proibir abrir apps privados ou sites de bancos
- Por enquanto o uso é por conta e risco do usuário e requer supervisão humana constante, mas tende a aumentar fortemente automação e produtividade (ex.: responder e organizar e-mails durante a noite)
- É questão de tempo para que ChatGPT, Gemini e outros concorrentes implementarem funcionalidade equivalente de computer use

> **Deep dive:** `low` — Trata-se de comentário reativo de nível consumidor sobre vídeos de demonstração, com alta carga promocional (patrocinador e canal), sem densidade arquitetural, evals, harness ou detalhes técnicos acionáveis além do superficial.
