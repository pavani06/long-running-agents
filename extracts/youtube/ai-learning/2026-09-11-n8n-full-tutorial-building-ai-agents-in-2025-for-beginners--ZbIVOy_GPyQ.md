---
title: "N8N Full Tutorial: Building AI Agents in 2025 for Beginners!"
type: "extract"
source: "youtube"
video_id: "ZbIVOy_GPyQ"
url: "https://www.youtube.com/watch?v=ZbIVOy_GPyQ"
channel: "AI Foundations"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-n8n-full-tutorial-building-ai-agents-in-2025-for-beginners--ZbIVOy_GPyQ.txt]]"
tags: ["agents", "agent-tooling", "agent-loop", "context-management", "memory-architecture", "multi-agent", "stack-tooling", "curriculo-conteudo", "frameworks"]
thesis: "O vídeo ensina a construir agentes de IA no n8n combinando gatilhos, nós de ação/utilidade/código e o nó AI Agent, que—alimentado por um chat model, memória de janela e ferramentas bem descritas como Airtable—decide dinamicamente quais ferramentas usar e pode chamar outros workflows para formar ecossistemas de agentes aninhados."
concepts: ["sistemas agentivos (agentic systems)", "diferença entre workflows (saída predefinida) e agentes (decisão dinâmica de ferramentas)", "cinco categorias de nós no n8n: triggers, ações, utilidades, código e AI Agent", "seleção dinâmica de ferramentas pelo LLM", "window buffer memory e comprimento da janela de contexto", "mapeamento de session/chat ID na memória", "descrições de ferramentas para guiar o LLM", "credenciais e escopos de tokens de acesso (read/write/schema-read)", "expressão 'from AI' com key, description, type e default", "campos fixos vs. expressões dinâmicas", "encadeamento autônomo de ferramentas (buscar antes de atualizar)", "agentes aninhados e chamada de workflows como ferramentas", "execuções e organização por projetos", "ecossistema agentivo com classificação de tarefas"]
tools: ["n8n", "OpenAI / GPT-4o", "Anthropic", "AWS Bedrock", "Grok", "Llama", "Airtable", "Google Sheets", "Notion", "Gmail", "Outlook", "Google Calendar", "Google Drive", "WhatsApp", "Telegram", "Wikipedia", "Wolfram", "WooCommerce", "Slack", "plataforma Skool"]
people: ["AI Foundations (comunidade)", "Carter (cofundador)", "Anthony (membro)", "John (membro)"]
claims: ["Workflows têm saídas predefinidas, enquanto agentes decidem dinamicamente quais ferramentas e saídas usar com base no input do usuário", "Todo nó AI Agent no n8n exige um chat model conectado (ex.: GPT-4o) para funcionar como 'cérebro' da automação", "Sem memória o agente perde o contexto da conversa; window buffer memory armazena as últimas N interações sem exigir credenciais", "Ao conectar memória via Telegram/WhatsApp é preciso mapear manualmente o chat ID, enquanto o nó de chat nativo mapeia automaticamente", "Tokens de acesso pessoal no Airtable devem ter escopos de leitura/escrita de dados e leitura de schema, restritos à base específica usada", "Descrições de ferramentas específicas fazem o LLM produzir resultados esperados com mais frequência; incluir palavras-chave como 'home inventory' e 'airtable' orienta a seleção", "A expressão 'from AI' (key, description, type, default, separados por vírgulas e entre aspas) permite que o modelo preencha campos dinâmicos sem instruções explícitas", "Declarar type 'number' na expressão from AI evita que o modelo retorne string em campos numéricos", "Campos fixos aceitam dados estáticos, enquanto expressões aceitam dados dinâmicos", "O agente pode encadear ferramentas autonomamente (ex.: buscar o registro antes de atualizá-lo) mesmo sem instruções, mas instruções de sistema aumentam a consistência", "Carregar US$5–10 na conta OpenAI é suficiente para testes", "Agentes podem chamar outros workflows do n8n como ferramentas, executando workflows inteiros e devolvendo o resultado ao agente original", "Um workflow pode ser disparado 'quando chamado por outro workflow', recebendo a query do agente pai e permitindo agentes aninhados", "Um agente com poucas ferramentas deve ser visto como um 'agente de domínio' (ex.: agente de inventário) que outros agentes chamam como uma única ferramenta", "Sistemas agentivos reais exigem múltiplos agentes/nós, não um único AI Agent, com instruções de sistema para classificar tarefas por área"]
deep_dive: "low"
deep_dive_reason: "É um tutorial introdutório de walkthrough do n8n com segmentos promocionais recorrentes: oferece passos práticos básicos (memória, descrições de ferramenta, expressões from AI), mas sem densidade de insight arquitetural, novidade ou profundidade em harness, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-everything-with-ai-agents-here-s-how--XVO3zsHdvio|Build Everything with AI Agents: Here's How]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-ai-agents-you-must-have-beginners-guide--WLvQCIUWebs|5 simple AI Agents you must have - beginners guide]]", "[[extracts/youtube/ai-learning/2026-09-11-3-ai-workflows-step-by-step-beginner-s-guide-to-n8n--06Beyp_iDL0|3 AI Workflows Step-by-Step (Beginner's Guide to n8n)]]", "[[extracts/youtube/ai-learning/2026-09-11-top-4-must-have-ai-agents-for-beginners-easy-setup-guide--4keUCOVpsxQ|Top 4 Must-Have AI Agents for Beginners – Easy Setup Guide]]", "[[extracts/youtube/ai-learning/2026-09-11-n8n-6-exemplos-praticos-ia-chatbots-c-hugo-autotic--DgAu_oJ2-TA|N8N: 6 exemplos práticos (IA & Chatbots) c/ Hugo Autotic]]", "[[extracts/youtube/ai-learning/2026-09-11-i-built-the-ultimate-team-of-ai-agents-in-n8n-with-no-code-free-template--9FuNtfsnRNo|I Built the Ultimate Team of AI Agents in n8n With No Code (Free Template)]]", "[[extracts/youtube/ai-learning/2026-09-11-10-insane-ai-agent-use-cases-in-n8n-steal-these--Dt6u-yFEpsk|10 Insane AI Agent Use Cases in n8n! (steal these)]]", "[[extracts/youtube/ai-learning/2026-09-11-4-agentic-frameworks-for-more-efficient-workflows-in-n8n--nSQnJoqK4DQ|4 Agentic Frameworks for More Efficient Workflows in n8n]]", "[[extracts/youtube/ai-learning/2026-09-11-intro-to-agent-builder--44eFf-tRiSg|Intro to Agent Builder]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-create-any-n8n-workflow-using-chatgpt--lZuxqbw8IX4|How to create any n8n workflow using ChatGPT]]", "[[extracts/youtube/ai-learning/2026-09-11-stop-hallucinations-best-n8n-ai-agent-settings-explained--pR51uBNb5es|Stop Hallucinations! Best n8n AI Agent Settings Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-build-an-agent-in-10-mins-with-ai-sdk-5-with-nico-albanese-from-vercel-ai-demo-d--TjAbtsPC-Sw|Build An Agent in 10 mins with AI SDK 5 with Nico Albanese from Vercel, AI Demo Days]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-use-ai-agents-to-make-money-vibe-marketing-tutorial--PduJ0P6r_8o|How I use AI agents to make money (Vibe Marketing Tutorial)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-lovable-n8n-ai-agents-beginner-s-guide--kUpTUEwKnrk|Build Anything with Lovable + n8n AI Agents (beginner's guide)]]", "[[extracts/youtube/ai-learning/2026-09-11-stop-using-basic-n8n-nodes-these-10-will-change-everything--szGFppZgSI0|STOP Using Basic n8n Nodes! These 10 Will Change Everything]]"]
---

# N8N Full Tutorial: Building AI Agents in 2025 for Beginners!

## Tese
O vídeo ensina a construir agentes de IA no n8n combinando gatilhos, nós de ação/utilidade/código e o nó AI Agent, que—alimentado por um chat model, memória de janela e ferramentas bem descritas como Airtable—decide dinamicamente quais ferramentas usar e pode chamar outros workflows para formar ecossistemas de agentes aninhados.

## Conceitos-chave
- sistemas agentivos (agentic systems)
- diferença entre workflows (saída predefinida) e agentes (decisão dinâmica de ferramentas)
- cinco categorias de nós no n8n: triggers, ações, utilidades, código e AI Agent
- seleção dinâmica de ferramentas pelo LLM
- window buffer memory e comprimento da janela de contexto
- mapeamento de session/chat ID na memória
- descrições de ferramentas para guiar o LLM
- credenciais e escopos de tokens de acesso (read/write/schema-read)
- expressão 'from AI' com key, description, type e default
- campos fixos vs. expressões dinâmicas
- encadeamento autônomo de ferramentas (buscar antes de atualizar)
- agentes aninhados e chamada de workflows como ferramentas
- execuções e organização por projetos
- ecossistema agentivo com classificação de tarefas

## Ferramentas & pessoas
**Ferramentas:** n8n, OpenAI / GPT-4o, Anthropic, AWS Bedrock, Grok, Llama, Airtable, Google Sheets, Notion, Gmail, Outlook, Google Calendar, Google Drive, WhatsApp, Telegram, Wikipedia, Wolfram, WooCommerce, Slack, plataforma Skool

**Pessoas/orgs:** AI Foundations (comunidade), Carter (cofundador), Anthony (membro), John (membro)

## Claims acionáveis
- Workflows têm saídas predefinidas, enquanto agentes decidem dinamicamente quais ferramentas e saídas usar com base no input do usuário
- Todo nó AI Agent no n8n exige um chat model conectado (ex.: GPT-4o) para funcionar como 'cérebro' da automação
- Sem memória o agente perde o contexto da conversa; window buffer memory armazena as últimas N interações sem exigir credenciais
- Ao conectar memória via Telegram/WhatsApp é preciso mapear manualmente o chat ID, enquanto o nó de chat nativo mapeia automaticamente
- Tokens de acesso pessoal no Airtable devem ter escopos de leitura/escrita de dados e leitura de schema, restritos à base específica usada
- Descrições de ferramentas específicas fazem o LLM produzir resultados esperados com mais frequência; incluir palavras-chave como 'home inventory' e 'airtable' orienta a seleção
- A expressão 'from AI' (key, description, type, default, separados por vírgulas e entre aspas) permite que o modelo preencha campos dinâmicos sem instruções explícitas
- Declarar type 'number' na expressão from AI evita que o modelo retorne string em campos numéricos
- Campos fixos aceitam dados estáticos, enquanto expressões aceitam dados dinâmicos
- O agente pode encadear ferramentas autonomamente (ex.: buscar o registro antes de atualizá-lo) mesmo sem instruções, mas instruções de sistema aumentam a consistência
- Carregar US$5–10 na conta OpenAI é suficiente para testes
- Agentes podem chamar outros workflows do n8n como ferramentas, executando workflows inteiros e devolvendo o resultado ao agente original
- Um workflow pode ser disparado 'quando chamado por outro workflow', recebendo a query do agente pai e permitindo agentes aninhados
- Um agente com poucas ferramentas deve ser visto como um 'agente de domínio' (ex.: agente de inventário) que outros agentes chamam como uma única ferramenta
- Sistemas agentivos reais exigem múltiplos agentes/nós, não um único AI Agent, com instruções de sistema para classificar tarefas por área

> **Deep dive:** `low` — É um tutorial introdutório de walkthrough do n8n com segmentos promocionais recorrentes: oferece passos práticos básicos (memória, descrições de ferramenta, expressões from AI), mas sem densidade de insight arquitetural, novidade ou profundidade em harness, evals ou governança.
