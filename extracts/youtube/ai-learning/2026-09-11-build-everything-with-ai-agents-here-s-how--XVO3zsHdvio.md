---
title: "Build Everything with AI Agents: Here's How"
type: "extract"
source: "youtube"
video_id: "XVO3zsHdvio"
url: "https://www.youtube.com/watch?v=XVO3zsHdvio"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-everything-with-ai-agents-here-s-how--XVO3zsHdvio.txt]]"
tags: ["agents", "agent-tooling", "agent-loop", "stack-tooling", "testes-qa", "error-handling", "model-selection", "token-budgeting", "process"]
thesis: "Qualquer pessoa sem experiência em programação pode construir um agente de IA funcional no n8n conectando triggers (Telegram), um modelo de chat (Claude Sonnet) e ferramentas como Gmail e Google Calendar, desde que teste cada etapa do workflow e escreva system prompts e descrições de parâmetros que instruam o modelo corretamente."
concepts: ["agente de IA no-code", "triggers de automação (Telegram, webhook, schedule)", "switch/roteamento de entradas (texto vs. voz)", "transcrição de áudio (OpenAI Whisper)", "tools/ferramentas do agente", "system prompt como fonte de verdade do agente", "knowledge cutoff e injeção da data atual no prompt", "descrições de parâmetros como instruções ao modelo (expressões 'from AI')", "teste incremental a cada nó do workflow", "ativação de workflow em produção", "limites de fetch para controlar custo de tokens"]
tools: ["n8n", "Telegram", "OpenAI (transcrição)", "Anthropic Claude Sonnet 10-22", "Azure OpenAI", "Mistral", "Groq", "Ollama", "Google Gemini", "Gmail", "Google Calendar", "Google Docs", "Google Drive", "Google Sheets", "Slack", "Airtable", "Jira", "MongoDB", "Supabase", "Make.com", "Zapier", "Vectal"]
people: ["David Andre", "Vectal", "New Society", "Anthropic", "OpenAI", "Google", "Telegram", "Zapier", "Make.com", "Todoist"]
claims: ["Teste cada nó imediatamente após configurá-lo no n8n; erros descobertos cedo são muito mais fáceis de depurar do que erros em cadeias longas.", "Arraste os campos reais de saída de um nó para outro em vez de copiar/colar código de tutoriais, pois isso garante o mapeamento correto dos dados.", "Ao usar expressões 'from AI' em parâmetros de ferramenta, escreva descrições claras do campo (ex.: 'raw email address of the recipient') — placeholders genéricos causam erros como endereços de e-mail inválidos.", "Certifique-se de que campos com expressão estejam em modo 'expression', não 'fixed', senão o placeholder é enviado literalmente.", "Inclua a data atual explícita no system prompt e proíba outras datas, pois o modelo não sabe a data de hoje devido ao knowledge cutoff — sem isso, eventos de calendário podem ser criados no ano errado.", "Especifique no system prompt o formato exato de data/hora (ex.: ISO year-month-day com offset) exigido pela ferramenta de calendário.", "Atualize o system prompt sempre que adicionar uma nova ferramenta, descrevendo o que ela faz e quando usá-la.", "Renomeie as ferramentas com nomes descritivos (ex.: 'calendar read', 'Gmail send') para o agente identificá-las melhor.", "Limite a quantidade de itens buscados (ex.: 20 e-mails em vez de 50) para reduzir custo de tokens.", "É possível usar outros workflows do n8n como ferramentas do agente, permitindo composição de automações customizadas.", "Construir esse mesmo agente via API em código levaria horas; no n8n leva cerca de 5 minutos.", "Estratégia de carreira: automatize parte do workflow da própria empresa, demonstre a líderes/CEOs e negocie um aumento; ou construa automações para clientes.", "Comece construindo automações para você mesmo antes de vender ou apresentar para empresas."]
deep_dive: "low"
deep_dive_reason: "É um tutorial introdutório e fortemente promocional (plugs recorrentes de New Society e Vectal) com lições práticas úteis, mas sem novidade nem densidade arquitetural em harness, context-engineering, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-top-4-must-have-ai-agents-for-beginners-easy-setup-guide--4keUCOVpsxQ|Top 4 Must-Have AI Agents for Beginners – Easy Setup Guide]]", "[[extracts/youtube/ai-learning/2026-09-11-n8n-full-tutorial-building-ai-agents-in-2025-for-beginners--ZbIVOy_GPyQ|N8N Full Tutorial: Building AI Agents in 2025 for Beginners!]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-ai-agents-you-must-have-beginners-guide--WLvQCIUWebs|5 simple AI Agents you must have - beginners guide]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-lovable-n8n-ai-agents-no-code--EN0-KNqs6aA|Build Anything With Lovable + n8n AI Agents (No-Code)]]", "[[extracts/youtube/ai-learning/2026-09-11-i-built-the-ultimate-team-of-ai-agents-in-n8n-with-no-code-free-template--9FuNtfsnRNo|I Built the Ultimate Team of AI Agents in n8n With No Code (Free Template)]]", "[[extracts/youtube/ai-learning/2026-09-11-i-built-a-marketing-team-with-1-ai-agent-and-no-code-free-n8n-template--ldETapkr8Hg|I Built a Marketing Team with 1 AI Agent and No Code (free n8n template)]]", "[[extracts/youtube/ai-learning/2026-09-11-10-insane-ai-agent-use-cases-in-n8n-steal-these--Dt6u-yFEpsk|10 Insane AI Agent Use Cases in n8n! (steal these)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-3-ai-workflows-step-by-step-beginner-s-guide-to-n8n--06Beyp_iDL0|3 AI Workflows Step-by-Step (Beginner's Guide to n8n)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-instantly-build-ai-agents-in-n8n-using-claude--uAtSMEBosGU|How to INSTANTLY Build AI Agents in N8N Using Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-a-startup-team-of-ai-agents-n8n-openai-feedhive--Hm0DZtiKUI8|How To Build a Startup Team of AI Agents (n8n, OpenAI, FeedHive)]]", "[[extracts/youtube/ai-learning/2026-09-11-n8n-6-exemplos-praticos-ia-chatbots-c-hugo-autotic--DgAu_oJ2-TA|N8N: 6 exemplos práticos (IA & Chatbots) c/ Hugo Autotic]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-create-any-n8n-workflow-using-chatgpt--lZuxqbw8IX4|How to create any n8n workflow using ChatGPT]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-lovable-n8n-ai-agents-beginner-s-guide--kUpTUEwKnrk|Build Anything with Lovable + n8n AI Agents (beginner's guide)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-use-ai-agents-to-make-money-vibe-marketing-tutorial--PduJ0P6r_8o|How I use AI agents to make money (Vibe Marketing Tutorial)]]", "[[extracts/youtube/ai-learning/2026-09-11-building-the-universal-ai-automation-layer-ft-n8n-ceo-jan-oberhauser--RUHU-w4Lz1I|Building the Universal AI Automation Layer ft n8n CEO Jan Oberhauser]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-super-effective-ai-agents-full-tutorial-cursor-openai--MSO4qCiwTjQ|How to Build Super Effective AI AGENTS - FULL TUTORIAL | Cursor - OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-intro-to-agent-builder--44eFf-tRiSg|Intro to Agent Builder]]", "[[extracts/youtube/ai-learning/2026-09-11-build-n8n-agents-into-full-stack-apps-heres-how--UaJSXjNX3wo|Build n8n agents into full-stack apps, here’s how]]", "[[extracts/youtube/ai-learning/2026-09-11-stop-hallucinations-best-n8n-ai-agent-settings-explained--pR51uBNb5es|Stop Hallucinations! Best n8n AI Agent Settings Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-build-an-agent-in-10-mins-with-ai-sdk-5-with-nico-albanese-from-vercel-ai-demo-d--TjAbtsPC-Sw|Build An Agent in 10 mins with AI SDK 5 with Nico Albanese from Vercel, AI Demo Days]]", "[[extracts/youtube/ai-learning/2026-09-11-como-automatizei-um-escritorio-de-advocacia-com-6-agentes-i-a--bFnY2tONtSs|Como Automatizei um Escritório de Advocacia com 6 Agentes I.A]]", "[[extracts/youtube/ai-learning/2026-09-11-steal-this-ai-agent-idea-today-big-opportunity--lZsZX5p6eHQ|Steal This AI AGENT Idea Today - BIG OPPORTUNITY!]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-sell-ai-workflows-without-starting-an-agency--QIsJe-nZ5XE|How to Sell AI Workflows (Without Starting an Agency)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-instantly-generate-n8n-workflows-using-claude--9tj4MxCV6g0|How to INSTANTLY Generate N8N Workflows Using Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-finally-this-ai-agent-actually-works--XeWZIzndlY4|FINALLY, this AI agent actually works!]]"]
---

# Build Everything with AI Agents: Here's How

## Tese
Qualquer pessoa sem experiência em programação pode construir um agente de IA funcional no n8n conectando triggers (Telegram), um modelo de chat (Claude Sonnet) e ferramentas como Gmail e Google Calendar, desde que teste cada etapa do workflow e escreva system prompts e descrições de parâmetros que instruam o modelo corretamente.

## Conceitos-chave
- agente de IA no-code
- triggers de automação (Telegram, webhook, schedule)
- switch/roteamento de entradas (texto vs. voz)
- transcrição de áudio (OpenAI Whisper)
- tools/ferramentas do agente
- system prompt como fonte de verdade do agente
- knowledge cutoff e injeção da data atual no prompt
- descrições de parâmetros como instruções ao modelo (expressões 'from AI')
- teste incremental a cada nó do workflow
- ativação de workflow em produção
- limites de fetch para controlar custo de tokens

## Ferramentas & pessoas
**Ferramentas:** n8n, Telegram, OpenAI (transcrição), Anthropic Claude Sonnet 10-22, Azure OpenAI, Mistral, Groq, Ollama, Google Gemini, Gmail, Google Calendar, Google Docs, Google Drive, Google Sheets, Slack, Airtable, Jira, MongoDB, Supabase, Make.com, Zapier, Vectal

**Pessoas/orgs:** David Andre, Vectal, New Society, Anthropic, OpenAI, Google, Telegram, Zapier, Make.com, Todoist

## Claims acionáveis
- Teste cada nó imediatamente após configurá-lo no n8n; erros descobertos cedo são muito mais fáceis de depurar do que erros em cadeias longas.
- Arraste os campos reais de saída de um nó para outro em vez de copiar/colar código de tutoriais, pois isso garante o mapeamento correto dos dados.
- Ao usar expressões 'from AI' em parâmetros de ferramenta, escreva descrições claras do campo (ex.: 'raw email address of the recipient') — placeholders genéricos causam erros como endereços de e-mail inválidos.
- Certifique-se de que campos com expressão estejam em modo 'expression', não 'fixed', senão o placeholder é enviado literalmente.
- Inclua a data atual explícita no system prompt e proíba outras datas, pois o modelo não sabe a data de hoje devido ao knowledge cutoff — sem isso, eventos de calendário podem ser criados no ano errado.
- Especifique no system prompt o formato exato de data/hora (ex.: ISO year-month-day com offset) exigido pela ferramenta de calendário.
- Atualize o system prompt sempre que adicionar uma nova ferramenta, descrevendo o que ela faz e quando usá-la.
- Renomeie as ferramentas com nomes descritivos (ex.: 'calendar read', 'Gmail send') para o agente identificá-las melhor.
- Limite a quantidade de itens buscados (ex.: 20 e-mails em vez de 50) para reduzir custo de tokens.
- É possível usar outros workflows do n8n como ferramentas do agente, permitindo composição de automações customizadas.
- Construir esse mesmo agente via API em código levaria horas; no n8n leva cerca de 5 minutos.
- Estratégia de carreira: automatize parte do workflow da própria empresa, demonstre a líderes/CEOs e negocie um aumento; ou construa automações para clientes.
- Comece construindo automações para você mesmo antes de vender ou apresentar para empresas.

> **Deep dive:** `low` — É um tutorial introdutório e fortemente promocional (plugs recorrentes de New Society e Vectal) com lições práticas úteis, mas sem novidade nem densidade arquitetural em harness, context-engineering, evals ou governança.
