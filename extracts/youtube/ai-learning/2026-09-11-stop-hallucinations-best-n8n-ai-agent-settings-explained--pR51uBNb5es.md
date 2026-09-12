---
title: "Stop Hallucinations! Best n8n AI Agent Settings Explained"
type: "extract"
source: "youtube"
video_id: "pR51uBNb5es"
url: "https://www.youtube.com/watch?v=pR51uBNb5es"
channel: "FuturMinds"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-stop-hallucinations-best-n8n-ai-agent-settings-explained--pR51uBNb5es.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "model-selection", "memory-architecture", "context-management", "token-budgeting", "stack-tooling", "error-handling", "observability"]
thesis: "Construir agentes de IA de nível profissional em n8n exige configuração deliberada — seleção de modelo por caso de uso (inclusive roteamento dinâmico), ajuste de parâmetros de amostragem, memória externa persistente, system prompt estruturado e output parsers — em vez da montagem ingênua de agente + prompt genérico + ferramentas aleatórias."
concepts: ["Roteamento dinâmico de modelo via agente roteador leve que emite apenas o nome do modelo", "Parâmetros de amostragem: temperature e top P (nucleus sampling)", "Frequency penalty e max tokens como controles de saída", "Context window length na memória de chat (nº de interações passadas compartilhadas)", "Memória simples (só em POCs) vs Postgres chat memory em produção", "Estrutura de system prompt: role, objetivo, conhecimento de domínio, inventário de ferramentas, regras de formatação, estilo/tom, segurança, instruções de raciocínio", "Output parsers: structured, item list e auto-fixing (wrapper que repara formato via LLM)", "Max iterations como limite do loop agente-ferramenta", "Return intermediate steps para debugging, auditoria e transparência", "Trade-off do 'let the model define this parameter' (flexibilidade vs alucinação)", "Regras de seleção de LLM por critério (raciocínio, privacidade, vendor lock-in, custo)", "Suporte a function calling como restrição na escolha de modelo"]
tools: ["n8n", "OpenAI Chat Model (o1, o1-pro, o3, o4-mini, GPT-4.1, GPT-4o, 4.1-mini, GPT-4o-audio)", "OpenRouter", "Anthropic Claude", "Azure OpenAI", "AWS Bedrock", "DeepSeek (R1)", "Google Gemini (2.0 Flash)", "Grok", "Mistral", "Ollama", "Supabase (transaction pooler)", "Postgres Chat Memory", "Simple Memory", "Gmail Tool", "MCP Client", "Structured Output Parser", "Item List Output Parser", "Auto-Fixing Output Parser"]
people: ["OpenAI", "Anthropic", "Google", "AWS", "Microsoft Azure", "n8n", "Supabase", "Mistral AI"]
claims: ["Crie um agente roteador leve (ex.: Gemini 2.0 Flash) com regras de decisão que emite só o nome do modelo, e passe-o dinamicamente via expressão (com trimEnd) ao chat model do OpenRouter para seleção de modelo por query", "DeepSeek R1 não suporta function calling — use modelos o1/o3 da OpenAI quando o agente precisa executar ferramentas", "Temperatura recomendada: 0.2–0.3 para chatbots/FAQ, 0.6–0.9 para conteúdo criativo, 0.1–0.3 para code helpers e tool agents", "Regras gerais: respostas confiáveis com temperature 0.2 e top P 0.7; escrita criativa com temperature 0.5–0.8 e top P 1; JSON estruturado com temperature 0.1 e top P 0.5", "Frequency penalty entre 0.5 e 1.0 reduz repetição na resposta final", "Nunca use Simple Memory em produção (consome memória da máquina e pode travar o n8n); prefira Postgres chat memory via Supabase, que cria a tabela automaticamente", "Aumente o context window length (ex.: de 5 para 10) apenas quando contexto de conversas antigas importa para o caso de uso", "Limite o uso de campos 'let the model define this parameter' ao indispensável para reduzir alucinação em valores de ferramentas", "Aumente max iterations (default 10) para fluxos de análise profunda com muitos back-and-forths agente-ferramenta; mantenha o default para chatbots simples", "Ative return intermediate steps apenas para debugging, auditoria e log de desempenho do agente", "Não inclua regras de formatação no system prompt quando estiver usando output parser", "Use o Auto-Fixing Output Parser para reenviar resposta inválida + erro ao LLM e reparar o formato JSON automaticamente", "Verifique suporte multimodal do LLM antes de habilitar pass-through automático de imagens binárias", "Estruture o system prompt em blocos: role, objetivo primário, conhecimento de domínio, ferramentas com quando/usar por quê, busca em conhecimento, formatação, estilo/tom, segurança/exatidão e raciocínio adicional"]
deep_dive: "medium"
deep_dive_reason: "Conteúdo tutorial com boa densidade de recomendações acionáveis (roteamento dinâmico de modelo, tuning de temperature/top P, escolha de memória, parsers), porém específico de plataforma e sem novidade arquitetural profunda em harness, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-n8n-full-tutorial-building-ai-agents-in-2025-for-beginners--ZbIVOy_GPyQ|N8N Full Tutorial: Building AI Agents in 2025 for Beginners!]]", "[[extracts/youtube/ai-learning/2026-09-11-i-built-the-ultimate-team-of-ai-agents-in-n8n-with-no-code-free-template--9FuNtfsnRNo|I Built the Ultimate Team of AI Agents in n8n With No Code (Free Template)]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-ai-agents-you-must-have-beginners-guide--WLvQCIUWebs|5 simple AI Agents you must have - beginners guide]]", "[[extracts/youtube/ai-learning/2026-09-11-build-everything-with-ai-agents-here-s-how--XVO3zsHdvio|Build Everything with AI Agents: Here's How]]", "[[extracts/youtube/ai-learning/2026-09-11-top-4-must-have-ai-agents-for-beginners-easy-setup-guide--4keUCOVpsxQ|Top 4 Must-Have AI Agents for Beginners – Easy Setup Guide]]", "[[extracts/youtube/ai-learning/2026-09-11-learn-80-of-notebooklm-in-under-13-minutes--EOmgC3-hznM|Learn 80% of NotebookLM in Under 13 Minutes!]]", "[[extracts/youtube/ai-learning/2026-09-11-did-openai-just-solve-hallucinations--xGO5Q94XXf0|Did OpenAI just solve hallucinations?]]"]
---

# Stop Hallucinations! Best n8n AI Agent Settings Explained

## Tese
Construir agentes de IA de nível profissional em n8n exige configuração deliberada — seleção de modelo por caso de uso (inclusive roteamento dinâmico), ajuste de parâmetros de amostragem, memória externa persistente, system prompt estruturado e output parsers — em vez da montagem ingênua de agente + prompt genérico + ferramentas aleatórias.

## Conceitos-chave
- Roteamento dinâmico de modelo via agente roteador leve que emite apenas o nome do modelo
- Parâmetros de amostragem: temperature e top P (nucleus sampling)
- Frequency penalty e max tokens como controles de saída
- Context window length na memória de chat (nº de interações passadas compartilhadas)
- Memória simples (só em POCs) vs Postgres chat memory em produção
- Estrutura de system prompt: role, objetivo, conhecimento de domínio, inventário de ferramentas, regras de formatação, estilo/tom, segurança, instruções de raciocínio
- Output parsers: structured, item list e auto-fixing (wrapper que repara formato via LLM)
- Max iterations como limite do loop agente-ferramenta
- Return intermediate steps para debugging, auditoria e transparência
- Trade-off do 'let the model define this parameter' (flexibilidade vs alucinação)
- Regras de seleção de LLM por critério (raciocínio, privacidade, vendor lock-in, custo)
- Suporte a function calling como restrição na escolha de modelo

## Ferramentas & pessoas
**Ferramentas:** n8n, OpenAI Chat Model (o1, o1-pro, o3, o4-mini, GPT-4.1, GPT-4o, 4.1-mini, GPT-4o-audio), OpenRouter, Anthropic Claude, Azure OpenAI, AWS Bedrock, DeepSeek (R1), Google Gemini (2.0 Flash), Grok, Mistral, Ollama, Supabase (transaction pooler), Postgres Chat Memory, Simple Memory, Gmail Tool, MCP Client, Structured Output Parser, Item List Output Parser, Auto-Fixing Output Parser

**Pessoas/orgs:** OpenAI, Anthropic, Google, AWS, Microsoft Azure, n8n, Supabase, Mistral AI

## Claims acionáveis
- Crie um agente roteador leve (ex.: Gemini 2.0 Flash) com regras de decisão que emite só o nome do modelo, e passe-o dinamicamente via expressão (com trimEnd) ao chat model do OpenRouter para seleção de modelo por query
- DeepSeek R1 não suporta function calling — use modelos o1/o3 da OpenAI quando o agente precisa executar ferramentas
- Temperatura recomendada: 0.2–0.3 para chatbots/FAQ, 0.6–0.9 para conteúdo criativo, 0.1–0.3 para code helpers e tool agents
- Regras gerais: respostas confiáveis com temperature 0.2 e top P 0.7; escrita criativa com temperature 0.5–0.8 e top P 1; JSON estruturado com temperature 0.1 e top P 0.5
- Frequency penalty entre 0.5 e 1.0 reduz repetição na resposta final
- Nunca use Simple Memory em produção (consome memória da máquina e pode travar o n8n); prefira Postgres chat memory via Supabase, que cria a tabela automaticamente
- Aumente o context window length (ex.: de 5 para 10) apenas quando contexto de conversas antigas importa para o caso de uso
- Limite o uso de campos 'let the model define this parameter' ao indispensável para reduzir alucinação em valores de ferramentas
- Aumente max iterations (default 10) para fluxos de análise profunda com muitos back-and-forths agente-ferramenta; mantenha o default para chatbots simples
- Ative return intermediate steps apenas para debugging, auditoria e log de desempenho do agente
- Não inclua regras de formatação no system prompt quando estiver usando output parser
- Use o Auto-Fixing Output Parser para reenviar resposta inválida + erro ao LLM e reparar o formato JSON automaticamente
- Verifique suporte multimodal do LLM antes de habilitar pass-through automático de imagens binárias
- Estruture o system prompt em blocos: role, objetivo primário, conhecimento de domínio, ferramentas com quando/usar por quê, busca em conhecimento, formatação, estilo/tom, segurança/exatidão e raciocínio adicional

> **Deep dive:** `medium` — Conteúdo tutorial com boa densidade de recomendações acionáveis (roteamento dinâmico de modelo, tuning de temperature/top P, escolha de memória, parsers), porém específico de plataforma e sem novidade arquitetural profunda em harness, evals ou governança.
