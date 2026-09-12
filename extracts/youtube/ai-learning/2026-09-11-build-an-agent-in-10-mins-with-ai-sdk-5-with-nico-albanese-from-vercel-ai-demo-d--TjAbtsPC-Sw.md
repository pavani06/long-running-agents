---
title: "Build An Agent in 10 mins with AI SDK 5 with Nico Albanese from Vercel, AI Demo Days"
type: "extract"
source: "youtube"
video_id: "TjAbtsPC-Sw"
url: "https://www.youtube.com/watch?v=TjAbtsPC-Sw"
channel: "AI Demo Days"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-an-agent-in-10-mins-with-ai-sdk-5-with-nico-albanese-from-vercel-ai-demo-d--TjAbtsPC-Sw.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "context-management", "frameworks", "model-selection", "stack-tooling", "production", "arquitetura"]
thesis: "Construir agentes úteis resume-se a compor um modelo de linguagem com ferramentas bem descritas e condições de parada explícitas, algo que o AI SDK v5 da Vercel abstrai via camada unificada de providers e controles declarativos do loop de agente."
concepts: ["agent loop como while loop com condição de parada", "tool calling (descrição, parâmetros, execução)", "condições de parada declarativas (stopWhen, limite de steps)", "camada unificada de providers", "system prompt para moldar comportamento", "streaming de saída (streamText vs generateText)", "gestão de contexto: separar mensagens de UI vs mensagens enviadas ao modelo", "separação da camada de transporte no useChat", "modelos de raciocínio para tarefas de escrita final", "padrão leitura (coleta de dados) vs escrita (geração de relatório)", "especificação v1 do SDK revisada para modelos multimodais, reasoning e streaming de dados arbitrários"]
tools: ["AI SDK (Vercel)", "AI SDK v5 (alpha)", "generateText", "streamText", "stopWhen", "useChat", "GPT-4.1 Mini (OpenAI)", "o4-mini (OpenAI)", "Sonar (Perplexity)", "Exa", "TypeScript", "Crunchbase", "PitchBook", "LinkedIn", "Slack", "LM Studio", "Ollama"]
people: ["Vercel", "Nico", "Damian", "Natalie", "James", "Granola", "OpenAI", "Perplexity", "Anthropic", "Azure", "AWS Bedrock", "Grok"]
claims: ["Trocar de modelo/provider exige alterar uma única linha de código, com suporte a ~48 providers incluindo OpenAI, Anthropic, Bedrock, Grox e modelos locais via LM Studio/Ollama", "Uma ferramenta (tool) precisa de três elementos: descrição (que determina se o modelo decide usá-la), schema de parâmetros e o código de execução", "Agentes são essencialmente loops que rodam até uma condição de parada; o AI SDK 5 permite declarar isso via stopWhen (ex.: limite de steps, parar após uso de uma tool, limite de tokens)", "Separar as mensagens exibidas na UI (com metadados e modelo usado) das mensagens efetivamente enviadas ao modelo resolve um problema clássico de gestão de contexto", "O redesign do useChat na v5 separa a camada de transporte, abrindo caminho para suporte a websockets", "Padrão eficaz: tools de leitura para coletar informação com modelos baratos e uma tool de escrita distinta usando um modelo de raciocínio mais forte (o4-mini) com system prompt customizado para gerar o artefato final", "Um agente de due diligence completo com 9 ferramentas rodou em ~30 segundos custando ~10 centavos, produzindo um memo estruturado em markdown", "A v5 é a primeira major release em mais de um ano com breaking changes derivados da reescrita completa da especificação da camada unificada para suportar multimodalidade e reasoning"]
deep_dive: "medium"
deep_dive_reason: "Demo introdutória e parcialmente promocional do AI SDK v5, mas com detalhes acionáveis de API (anatomia de tools, stopWhen, separação de mensagens e de transporte) relevantes a harness e context-management sem densidade arquitetural alta."
---

# Build An Agent in 10 mins with AI SDK 5 with Nico Albanese from Vercel, AI Demo Days

## Tese
Construir agentes úteis resume-se a compor um modelo de linguagem com ferramentas bem descritas e condições de parada explícitas, algo que o AI SDK v5 da Vercel abstrai via camada unificada de providers e controles declarativos do loop de agente.

## Conceitos-chave
- agent loop como while loop com condição de parada
- tool calling (descrição, parâmetros, execução)
- condições de parada declarativas (stopWhen, limite de steps)
- camada unificada de providers
- system prompt para moldar comportamento
- streaming de saída (streamText vs generateText)
- gestão de contexto: separar mensagens de UI vs mensagens enviadas ao modelo
- separação da camada de transporte no useChat
- modelos de raciocínio para tarefas de escrita final
- padrão leitura (coleta de dados) vs escrita (geração de relatório)
- especificação v1 do SDK revisada para modelos multimodais, reasoning e streaming de dados arbitrários

## Ferramentas & pessoas
**Ferramentas:** AI SDK (Vercel), AI SDK v5 (alpha), generateText, streamText, stopWhen, useChat, GPT-4.1 Mini (OpenAI), o4-mini (OpenAI), Sonar (Perplexity), Exa, TypeScript, Crunchbase, PitchBook, LinkedIn, Slack, LM Studio, Ollama

**Pessoas/orgs:** Vercel, Nico, Damian, Natalie, James, Granola, OpenAI, Perplexity, Anthropic, Azure, AWS Bedrock, Grok

## Claims acionáveis
- Trocar de modelo/provider exige alterar uma única linha de código, com suporte a ~48 providers incluindo OpenAI, Anthropic, Bedrock, Grox e modelos locais via LM Studio/Ollama
- Uma ferramenta (tool) precisa de três elementos: descrição (que determina se o modelo decide usá-la), schema de parâmetros e o código de execução
- Agentes são essencialmente loops que rodam até uma condição de parada; o AI SDK 5 permite declarar isso via stopWhen (ex.: limite de steps, parar após uso de uma tool, limite de tokens)
- Separar as mensagens exibidas na UI (com metadados e modelo usado) das mensagens efetivamente enviadas ao modelo resolve um problema clássico de gestão de contexto
- O redesign do useChat na v5 separa a camada de transporte, abrindo caminho para suporte a websockets
- Padrão eficaz: tools de leitura para coletar informação com modelos baratos e uma tool de escrita distinta usando um modelo de raciocínio mais forte (o4-mini) com system prompt customizado para gerar o artefato final
- Um agente de due diligence completo com 9 ferramentas rodou em ~30 segundos custando ~10 centavos, produzindo um memo estruturado em markdown
- A v5 é a primeira major release em mais de um ano com breaking changes derivados da reescrita completa da especificação da camada unificada para suportar multimodalidade e reasoning

> **Deep dive:** `medium` — Demo introdutória e parcialmente promocional do AI SDK v5, mas com detalhes acionáveis de API (anatomia de tools, stopWhen, separação de mensagens e de transporte) relevantes a harness e context-management sem densidade arquitetural alta.
