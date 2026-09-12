---
title: "I Built the Ultimate Team of AI Agents in n8n With No Code (Free Template)"
type: "extract"
source: "youtube"
video_id: "9FuNtfsnRNo"
url: "https://www.youtube.com/watch?v=9FuNtfsnRNo"
channel: "Nate Herk | AI Automation"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-i-built-the-ultimate-team-of-ai-agents-in-n8n-with-no-code-free-template--9FuNtfsnRNo.txt]]"
tags: ["agent-fleets", "agentes-orquestracao", "agent-tooling", "multi-agent", "arquitetura", "error-handling", "model-selection", "agent-loop"]
thesis: "Um assistente pessoal construído no n8n funciona melhor como um orquestrador enxuto que delega a sub-agentes especializados (e-mail, calendário, contatos, conteúdo) expostos como ferramentas via workflow-as-tool, com preenchimento de parâmetros pelo LLM e ramificações de erro que permitem retry."
concepts: ["orquestrador roteador delegando a sub-agentes especializados", "sub-agentes com prompts curtos e poucas ferramentas em vez de um agente monolítico", "workflow-as-tool (chamar workflow n8n como ferramenta do agente)", "injeção de parâmetros pelo LLM via função fromAI (chave + descrição)", "dependência de IDs encadeando ferramentas (get emails → message ID → label/reply)", "regra de lookup de contato antes de ações de e-mail/calendário com participantes", "branch de erro 'on error continue (error output)' gerando resposta 'tente novamente' lida pelo orquestrador", "normalização de entrada voz/texto em um único campo via switch + transcrição", "seleção de modelo por agente/tarefa", "memória conversacional para follow-ups contextuais", "separação de create event com/sem attendees devido a parâmetro obrigatório", "placeholders em corpo HTTP (Tavily) preenchidos pelo modelo"]
tools: ["n8n", "Telegram", "Gmail", "Google Calendar", "Airtable", "Tavily", "OpenAI GPT-4o", "Claude 3.5 Sonnet", "Call n8n Workflow as Tool", "fromAI (expressão n8n)", "Execute Workflow Trigger", "Skool"]
people: ["Nate Herkelman", "UpAD Digital"]
claims: ["Divida o assistente em sub-agentes especializados com prompts curtos e poucas ferramentas, coordenados por um orquestrador que apenas delega, em vez de sobrecarregar um único agente com muitas ferramentas e um prompt enorme", "Exponha sub-workflows ao agente orquestrador via 'Call n8n Workflow as Tool': o workflow chamado deve iniciar com Execute Workflow Trigger e a resposta é lida no último nó", "Imponha no prompt do orquestrador a regra de buscar informações de contato (agente de contatos/Airtable) antes de enviar e-mails ou criar eventos com participantes", "Use a expressão fromAI (chave + descrição opcional) nos parâmetros das ferramentas para o LLM preencher valores diretamente a partir da query, eliminando lógica manual de extração", "Para ferramentas que exigem IDs (message ID, label ID, event ID), instrua o agente a chamar primeiro as ferramentas de 'get' (get emails, get labels, get events) para obter os IDs antes de gravar", "Ative 'On Error → Continue (using error output)' no sub-agente para bifurcar falhas em uma resposta 'unable to perform task, please try again' que o orquestrador pode ler e reenviar a query", "Basta um exemplo one-shot no prompt do orquestrador demonstrando a sequência contato→e-mail para o padrão de delegação funcionar bem", "Forneça data/hora atual no system prompt para consultas relativas a tempo e defina duração padrão de 1 hora quando o evento não especificar", "Normalize entradas de voz e texto do Telegram em um único campo 'text' (switch + download + transcrição) para o agente tratar ambos uniformemente, e responda no mesmo chat ID do trigger", "Selecione modelo por função: GPT-4o para orquestração/e-mail/calendário e Claude 3.5 Sonnet para geração de conteúdo estruturado em HTML", "Separe ferramentas de criação de evento em duas versões (com e sem attendees) porque deixar o parâmetro de attendees vazio faz a requisição falhar", "Use placeholders nomeados com descrição no corpo HTTP (ex.: {{search_term}} para Tavily) para o modelo preencher parâmetros de requisições externas, funcionando como o fromAI"]
deep_dive: "medium"
deep_dive_reason: "Há densidade razoável de padrões acionáveis de orquestração multi-agente no n8n (workflow-as-tool, fromAI, encadeamento de IDs, branch de retry), mas é um tutorial de walkthrough com baixa novidade conceitual e trechos promocionais, sem cobertura de evals, harness ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-i-built-a-marketing-team-with-1-ai-agent-and-no-code-free-n8n-template--ldETapkr8Hg|I Built a Marketing Team with 1 AI Agent and No Code (free n8n template)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-everything-with-ai-agents-here-s-how--XVO3zsHdvio|Build Everything with AI Agents: Here's How]]", "[[extracts/youtube/ai-learning/2026-09-11-n8n-full-tutorial-building-ai-agents-in-2025-for-beginners--ZbIVOy_GPyQ|N8N Full Tutorial: Building AI Agents in 2025 for Beginners!]]", "[[extracts/youtube/ai-learning/2026-09-11-top-4-must-have-ai-agents-for-beginners-easy-setup-guide--4keUCOVpsxQ|Top 4 Must-Have AI Agents for Beginners – Easy Setup Guide]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-ai-agents-you-must-have-beginners-guide--WLvQCIUWebs|5 simple AI Agents you must have - beginners guide]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-lovable-n8n-ai-agents-no-code--EN0-KNqs6aA|Build Anything With Lovable + n8n AI Agents (No-Code)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-a-startup-team-of-ai-agents-n8n-openai-feedhive--Hm0DZtiKUI8|How To Build a Startup Team of AI Agents (n8n, OpenAI, FeedHive)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-create-any-n8n-workflow-using-chatgpt--lZuxqbw8IX4|How to create any n8n workflow using ChatGPT]]", "[[extracts/youtube/ai-learning/2026-09-11-stop-hallucinations-best-n8n-ai-agent-settings-explained--pR51uBNb5es|Stop Hallucinations! Best n8n AI Agent Settings Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-como-automatizei-um-escritorio-de-advocacia-com-6-agentes-i-a--bFnY2tONtSs|Como Automatizei um Escritório de Advocacia com 6 Agentes I.A]]", "[[extracts/youtube/ai-learning/2026-09-11-4-agentic-frameworks-for-more-efficient-workflows-in-n8n--nSQnJoqK4DQ|4 Agentic Frameworks for More Efficient Workflows in n8n]]"]
theme: "Agentes de IA No-Code"
---

# I Built the Ultimate Team of AI Agents in n8n With No Code (Free Template)

## Tese
Um assistente pessoal construído no n8n funciona melhor como um orquestrador enxuto que delega a sub-agentes especializados (e-mail, calendário, contatos, conteúdo) expostos como ferramentas via workflow-as-tool, com preenchimento de parâmetros pelo LLM e ramificações de erro que permitem retry.

## Conceitos-chave
- orquestrador roteador delegando a sub-agentes especializados
- sub-agentes com prompts curtos e poucas ferramentas em vez de um agente monolítico
- workflow-as-tool (chamar workflow n8n como ferramenta do agente)
- injeção de parâmetros pelo LLM via função fromAI (chave + descrição)
- dependência de IDs encadeando ferramentas (get emails → message ID → label/reply)
- regra de lookup de contato antes de ações de e-mail/calendário com participantes
- branch de erro 'on error continue (error output)' gerando resposta 'tente novamente' lida pelo orquestrador
- normalização de entrada voz/texto em um único campo via switch + transcrição
- seleção de modelo por agente/tarefa
- memória conversacional para follow-ups contextuais
- separação de create event com/sem attendees devido a parâmetro obrigatório
- placeholders em corpo HTTP (Tavily) preenchidos pelo modelo

## Ferramentas & pessoas
**Ferramentas:** n8n, Telegram, Gmail, Google Calendar, Airtable, Tavily, OpenAI GPT-4o, Claude 3.5 Sonnet, Call n8n Workflow as Tool, fromAI (expressão n8n), Execute Workflow Trigger, Skool

**Pessoas/orgs:** Nate Herkelman, UpAD Digital

## Claims acionáveis
- Divida o assistente em sub-agentes especializados com prompts curtos e poucas ferramentas, coordenados por um orquestrador que apenas delega, em vez de sobrecarregar um único agente com muitas ferramentas e um prompt enorme
- Exponha sub-workflows ao agente orquestrador via 'Call n8n Workflow as Tool': o workflow chamado deve iniciar com Execute Workflow Trigger e a resposta é lida no último nó
- Imponha no prompt do orquestrador a regra de buscar informações de contato (agente de contatos/Airtable) antes de enviar e-mails ou criar eventos com participantes
- Use a expressão fromAI (chave + descrição opcional) nos parâmetros das ferramentas para o LLM preencher valores diretamente a partir da query, eliminando lógica manual de extração
- Para ferramentas que exigem IDs (message ID, label ID, event ID), instrua o agente a chamar primeiro as ferramentas de 'get' (get emails, get labels, get events) para obter os IDs antes de gravar
- Ative 'On Error → Continue (using error output)' no sub-agente para bifurcar falhas em uma resposta 'unable to perform task, please try again' que o orquestrador pode ler e reenviar a query
- Basta um exemplo one-shot no prompt do orquestrador demonstrando a sequência contato→e-mail para o padrão de delegação funcionar bem
- Forneça data/hora atual no system prompt para consultas relativas a tempo e defina duração padrão de 1 hora quando o evento não especificar
- Normalize entradas de voz e texto do Telegram em um único campo 'text' (switch + download + transcrição) para o agente tratar ambos uniformemente, e responda no mesmo chat ID do trigger
- Selecione modelo por função: GPT-4o para orquestração/e-mail/calendário e Claude 3.5 Sonnet para geração de conteúdo estruturado em HTML
- Separe ferramentas de criação de evento em duas versões (com e sem attendees) porque deixar o parâmetro de attendees vazio faz a requisição falhar
- Use placeholders nomeados com descrição no corpo HTTP (ex.: {{search_term}} para Tavily) para o modelo preencher parâmetros de requisições externas, funcionando como o fromAI

> **Deep dive:** `medium` — Há densidade razoável de padrões acionáveis de orquestração multi-agente no n8n (workflow-as-tool, fromAI, encadeamento de IDs, branch de retry), mas é um tutorial de walkthrough com baixa novidade conceitual e trechos promocionais, sem cobertura de evals, harness ou governança.
