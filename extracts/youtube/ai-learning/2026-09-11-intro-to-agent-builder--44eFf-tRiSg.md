---
title: "Intro to Agent Builder"
type: "extract"
source: "youtube"
video_id: "44eFf-tRiSg"
url: "https://www.youtube.com/watch?v=44eFf-tRiSg"
channel: "OpenAI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-intro-to-agent-builder--44eFf-tRiSg.txt]]"
tags: ["agents", "agent-tooling", "classification", "agentes-orquestracao", "stack-tooling", "evals", "runtime", "process"]
thesis: "O vídeo demonstra como construir um agente de viagens visual no Agent Builder da OpenAI usando nós de classificação e ramificação, agentes especializados, widgets e publicação direta em produção sem código."
concepts: ["construtor visual de workflows com nós conectados (sem código)", "nó inicial com variáveis de entrada e de estado", "agente classificador com saída estruturada em JSON", "nó if/else para roteamento baseado na classificação", "agentes especializados (voos vs. itinerário)", "ferramenta de web search para informação atualizada", "widgets como formato de saída rico e interativo", "customização criativa de widgets pelo agente (cor de fundo por destino)", "preview/run para testar o fluxo do agente", "publicação direta e consumo via workflow ID ou Agents SDK", "avaliação embutida (built-in eval) para testar desempenho do agente", "templates como ponto de partida"]
tools: ["OpenAI Agent Builder", "OpenAI Platform", "Widget Studio", "Agents SDK", "Web Search", "Flight Widget (template de widget)", "ChatKit (mencionado como 'jacket' no transcript)"]
people: ["OpenAI", "Christina (apresentadora da OpenAI)", "OpenAI Devs (canal)"]
claims: ["Todo workflow no Agent Builder começa com um start node onde se definem variáveis de entrada e de estado.", "Um agente classificador com saída JSON (propriedade 'classification' com opções 'flight info' ou 'itinerary') combinado a um nó if/else permite rotear mensagens para agentes especializados.", "Conceder acesso a web search ao agente de voos garante informação de voos atualizada.", "Widgets criados no Widget Studio podem ser baixados como template, carregados como formato de saída do agente e customizados por instruções (ex.: cor de fundo baseada no destino, inclusão de fuso horário AM/PM).", "O run preview permite observar a mensagem percorrendo cada nó do workflow (classificador, ramificação, agente especializado, busca).", "Após a construção, o workflow pode ser publicado e integrado a produto via workflow ID (ex.: com ChatKit) ou exportado como código usando o Agents SDK.", "O Agent Builder inclui eval embutido para testar e entender o desempenho dos agentes."]
deep_dive: "low"
deep_dive_reason: "Trata-se de um tutorial promocional de produto que cobre um padrão de roteamento/classificação básico sem densidade de insight arquitetural, novidade técnica ou profundidade em harness, evals ou context-engineering."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-n8n-full-tutorial-building-ai-agents-in-2025-for-beginners--ZbIVOy_GPyQ|N8N Full Tutorial: Building AI Agents in 2025 for Beginners!]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-everything-with-ai-agents-here-s-how--XVO3zsHdvio|Build Everything with AI Agents: Here's How]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-an-agent-in-10-mins-with-ai-sdk-5-with-nico-albanese-from-vercel-ai-demo-d--TjAbtsPC-Sw|Build An Agent in 10 mins with AI SDK 5 with Nico Albanese from Vercel, AI Demo Days]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-lovable-n8n-ai-agents-beginner-s-guide--kUpTUEwKnrk|Build Anything with Lovable + n8n AI Agents (beginner's guide)]]", "[[extracts/youtube/ai-learning/2026-09-11-gpt-builder-2-0-upgrade-custom-gpt-with-parallel-function-calling-advanced-gpts--kBFjvQxKnOs|GPT Builder 2.0 🚀 UPGRADE Custom GPT with Parallel Function Calling 🤯 Advanced GPTs Tutorial]]"]
---

# Intro to Agent Builder

## Tese
O vídeo demonstra como construir um agente de viagens visual no Agent Builder da OpenAI usando nós de classificação e ramificação, agentes especializados, widgets e publicação direta em produção sem código.

## Conceitos-chave
- construtor visual de workflows com nós conectados (sem código)
- nó inicial com variáveis de entrada e de estado
- agente classificador com saída estruturada em JSON
- nó if/else para roteamento baseado na classificação
- agentes especializados (voos vs. itinerário)
- ferramenta de web search para informação atualizada
- widgets como formato de saída rico e interativo
- customização criativa de widgets pelo agente (cor de fundo por destino)
- preview/run para testar o fluxo do agente
- publicação direta e consumo via workflow ID ou Agents SDK
- avaliação embutida (built-in eval) para testar desempenho do agente
- templates como ponto de partida

## Ferramentas & pessoas
**Ferramentas:** OpenAI Agent Builder, OpenAI Platform, Widget Studio, Agents SDK, Web Search, Flight Widget (template de widget), ChatKit (mencionado como 'jacket' no transcript)

**Pessoas/orgs:** OpenAI, Christina (apresentadora da OpenAI), OpenAI Devs (canal)

## Claims acionáveis
- Todo workflow no Agent Builder começa com um start node onde se definem variáveis de entrada e de estado.
- Um agente classificador com saída JSON (propriedade 'classification' com opções 'flight info' ou 'itinerary') combinado a um nó if/else permite rotear mensagens para agentes especializados.
- Conceder acesso a web search ao agente de voos garante informação de voos atualizada.
- Widgets criados no Widget Studio podem ser baixados como template, carregados como formato de saída do agente e customizados por instruções (ex.: cor de fundo baseada no destino, inclusão de fuso horário AM/PM).
- O run preview permite observar a mensagem percorrendo cada nó do workflow (classificador, ramificação, agente especializado, busca).
- Após a construção, o workflow pode ser publicado e integrado a produto via workflow ID (ex.: com ChatKit) ou exportado como código usando o Agents SDK.
- O Agent Builder inclui eval embutido para testar e entender o desempenho dos agentes.

> **Deep dive:** `low` — Trata-se de um tutorial promocional de produto que cobre um padrão de roteamento/classificação básico sem densidade de insight arquitetural, novidade técnica ou profundidade em harness, evals ou context-engineering.
