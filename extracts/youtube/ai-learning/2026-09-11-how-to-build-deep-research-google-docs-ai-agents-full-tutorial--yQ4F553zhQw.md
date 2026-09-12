---
title: "How to Build Deep Research Google Docs AI AGENTS - Full Tutorial"
type: "extract"
source: "youtube"
video_id: "yQ4F553zhQw"
url: "https://www.youtube.com/watch?v=yQ4F553zhQw"
channel: "All About AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-build-deep-research-google-docs-ai-agents-full-tutorial--yQ4F553zhQw.txt]]"
tags: ["agent-loop", "agents", "multi-agent", "agent-tooling", "context-management", "gate-design", "monitoramento", "error-handling", "memory-architecture", "process"]
thesis: "Um sistema de pesquisa autônomo pode ser construído com dois agentes (buscador e redator) que se coordenam via um Google Doc compartilhado como canal de mensagens e memória, acrescido de um terceiro agente 'LLM-as-a-judge' que avalia se há dados suficientes, escreve o relatório final e encerra todos os processos automaticamente."
concepts: ["agentes autônomos em loop", "multi-agentes orquestrados por documento compartilhado", "Google Docs como barramento de mensagens e memória", "LLM-as-a-judge (gate true/false)", "function calling / ferramentas de busca", "queries de busca auto-geradas pelo agente", "monitoramento por intervalo (polling de mudanças no doc)", "append de contexto em vez de substituição", "condição de término autônoma / shutdown de scripts", "threshold de entradas (5) para reavaliação"]
tools: ["Google Docs API", "Google Drive API", "Brave Search API", "Gemini 2.0 Flash (experimental)", "OAuth 2.0 (credentials.json)", "Cursor", "Python", "Claude (Anthropic)", "GitHub da comunidade do canal"]
people: ["Google", "Brave", "Anthropic", "Cursor (empresa)", "criador do vídeo (canal de membros, não nomeado)"]
claims: ["Dois agentes podem coordenar-se autonomamente usando um Google Doc compartilhado: mudanças no documento (nova query ou novo resultado de busca) disparam o próximo passo de cada agente", "O agente redator lê o conteúdo atual mais os resultados de busca, anexa novo conteúdo sem substituir o existente e gera a próxima query (máx. 4 palavras, formato de uma única query Google)", "O fetcher agent usa function calling com a Brave Search API e monitora o doc em intervalos configuráveis (30-60s) para detectar novas queries", "Um agente principal no padrão LLM-as-a-judge avalia a cada 5 entradas se o material é adequado; se negativo, os outros agentes coletam mais 5 entradas antes de nova checagem", "Quando o juiz aprova, o relatório final é escrito em um documento novo e todos os scripts são encerrados automaticamente, eliminando gasto contínuo de tokens e permitindo execução desassistida", "Erro ao atualizar documento vazio foi corrigido com retry (insert sem delete) e tratamento de docs vazios", "Melhores resultados de busca produziriam melhor contexto e relatórios; o prompting do agente principal ficou inalterado e é área explícita de melhoria", "Todo o fluxo foi implementado ao vivo no Cursor com um único prompt, demonstrando viabilidade de oneshot em agentic coding para esse escopo", "O código completo é disponibilizado apenas em GitHub para membros do canal"]
deep_dive: "medium"
deep_dive_reason: "Há detalhe de implementação acionável e padrões úteis (doc compartilhado como canal de mensagens, gate LLM-as-a-judge, shutdown autônomo), mas o conteúdo é um tutorial demo de nível hobby, sem profundidade arquitetural, evals ou novidade suficiente para tier alto, com leve caráter promocional."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-research-agent-3-0-build-a-group-of-ai-researchers-here-is-how--AVInhYBUnKs|\"Research agent 3.0 - Build a group of AI researchers\" - Here is how]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-super-effective-ai-agents-full-tutorial-cursor-openai--MSO4qCiwTjQ|How to Build Super Effective AI AGENTS - FULL TUTORIAL | Cursor - OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-could-a-swarm-of-autonomous-ai-agents-be-the-ultimate-business-asset-stage-1--UL55C80TEb8|Could a Swarm of Autonomous AI Agents be the Ultimate Business Asset? - Stage 1]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-automate-my-own-job-at-hugging-face-using-agents-niels-rogge-hugging-face--FLUoowDJg4I|How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-building-docs-for-agents-not-humans-inside-openwiki--XNX-1h2K-9U|Building Docs for Agents, Not Humans: Inside OpenWiki]]", "[[extracts/youtube/ai-learning/2026-09-11-automatize-todo-o-seu-trabalho-com-a-ia-project-mariner-do-google-incrivel--E0Jbaikf0o4|AUTOMATIZE TODO O SEU TRABALHO com a IA “Project Mariner” do GOOGLE - INCRÍVEL!]]"]
---

# How to Build Deep Research Google Docs AI AGENTS - Full Tutorial

## Tese
Um sistema de pesquisa autônomo pode ser construído com dois agentes (buscador e redator) que se coordenam via um Google Doc compartilhado como canal de mensagens e memória, acrescido de um terceiro agente 'LLM-as-a-judge' que avalia se há dados suficientes, escreve o relatório final e encerra todos os processos automaticamente.

## Conceitos-chave
- agentes autônomos em loop
- multi-agentes orquestrados por documento compartilhado
- Google Docs como barramento de mensagens e memória
- LLM-as-a-judge (gate true/false)
- function calling / ferramentas de busca
- queries de busca auto-geradas pelo agente
- monitoramento por intervalo (polling de mudanças no doc)
- append de contexto em vez de substituição
- condição de término autônoma / shutdown de scripts
- threshold de entradas (5) para reavaliação

## Ferramentas & pessoas
**Ferramentas:** Google Docs API, Google Drive API, Brave Search API, Gemini 2.0 Flash (experimental), OAuth 2.0 (credentials.json), Cursor, Python, Claude (Anthropic), GitHub da comunidade do canal

**Pessoas/orgs:** Google, Brave, Anthropic, Cursor (empresa), criador do vídeo (canal de membros, não nomeado)

## Claims acionáveis
- Dois agentes podem coordenar-se autonomamente usando um Google Doc compartilhado: mudanças no documento (nova query ou novo resultado de busca) disparam o próximo passo de cada agente
- O agente redator lê o conteúdo atual mais os resultados de busca, anexa novo conteúdo sem substituir o existente e gera a próxima query (máx. 4 palavras, formato de uma única query Google)
- O fetcher agent usa function calling com a Brave Search API e monitora o doc em intervalos configuráveis (30-60s) para detectar novas queries
- Um agente principal no padrão LLM-as-a-judge avalia a cada 5 entradas se o material é adequado; se negativo, os outros agentes coletam mais 5 entradas antes de nova checagem
- Quando o juiz aprova, o relatório final é escrito em um documento novo e todos os scripts são encerrados automaticamente, eliminando gasto contínuo de tokens e permitindo execução desassistida
- Erro ao atualizar documento vazio foi corrigido com retry (insert sem delete) e tratamento de docs vazios
- Melhores resultados de busca produziriam melhor contexto e relatórios; o prompting do agente principal ficou inalterado e é área explícita de melhoria
- Todo o fluxo foi implementado ao vivo no Cursor com um único prompt, demonstrando viabilidade de oneshot em agentic coding para esse escopo
- O código completo é disponibilizado apenas em GitHub para membros do canal

> **Deep dive:** `medium` — Há detalhe de implementação acionável e padrões úteis (doc compartilhado como canal de mensagens, gate LLM-as-a-judge, shutdown autônomo), mas o conteúdo é um tutorial demo de nível hobby, sem profundidade arquitetural, evals ou novidade suficiente para tier alto, com leve caráter promocional.
