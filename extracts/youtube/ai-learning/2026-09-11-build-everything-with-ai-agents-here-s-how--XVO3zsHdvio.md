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
