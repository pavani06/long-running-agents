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
