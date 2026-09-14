---
title: "How To Build a Startup Team of AI Agents (n8n, OpenAI, FeedHive)"
type: "extract"
source: "youtube"
video_id: "Hm0DZtiKUI8"
url: "https://www.youtube.com/watch?v=Hm0DZtiKUI8"
channel: "Simon Høiberg"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-build-a-startup-team-of-ai-agents-n8n-openai-feedhive--Hm0DZtiKUI8.txt]]"
tags: ["agents", "multi-agent", "agent-loop", "context-engineering", "model-selection", "gate-design", "evals", "stack-tooling", "memory-architecture", "agent-tooling"]
thesis: "Um fundador pode substituir boa parte da equipe de conteúdo de uma startup combinando um modelo fine-tuned (estilo de escrita), um brand brief como contexto e um pipeline multi-agente no n8n que gera ideias, escreve, recebe feedback com nota 0-1 em loop e publica automaticamente no FeedHive."
concepts: ["Fine-tuning de modelos com exemplos reverso-engenheirados (prompt→output)", "Formato JSONL de treinamento (messages user/assistant, 20-50 exemplos)", "Brand brief como contexto de identidade (valores, temas, dislikes, opositores)", "Distinção entre custom GPT com system prompt vs. agente real", "Pipeline multi-agente: gerador de ideias → escritor → crítico → refinamento em loop", "Gate de qualidade com score 0-1 e critérios no system message", "Sub-workflows do n8n usados como tools de um agente", "Memória de janela (window buffer) no agente", "Orquestração: split-out + loop sobre sugestões com session ID por item", "Publicação automática via HTTP request para webhook do FeedHive"]
tools: ["OpenAI platform (fine-tuning)", "GPT-4o", "GPT-4o Mini", "ChatGPT", "JSONL", "n8n", "Notion", "FeedHive", "Zapier", "Make", "Vercel", "Netlify", "Google Docs", "Founder Stack"]
people: ["Simon (narrador)", "OpenAI", "FeedHive (time do autor)", "Founder Stack"]
claims: ["Custom GPTs baseados só em system prompt raramente geram bons resultados; fine-tune com 20-50 exemplos captura estilo de escrita de forma superior", "Reverso-engenheie o prompt que teria gerado cada post de exemplo (manualmente ou via ChatGPT) para montar o dataset de fine-tuning", "Monte o dataset em JSONL com um par user/assistant por linha e use \n para quebras de linha; treine sobre GPT-4o com defaults da plataforma", "Fine-tune resolve o 'como escrever', mas não o 'o que defender': escreva um brand brief em texto simples (valores, temas, posições, dislikes) e forneça-o como contexto no playground/workflow", "Use GPT-4o Mini para subtarefas baratas (gerar 10 ideias, dar feedback com score 0-1 em JSON) e reserve o modelo fine-tuned para a escrita final", "Estruture o pipeline no n8n como sub-workflows: brand brief (fetch Notion → aggregate → join), get content ideas, get content feedback (crítico com critérios em system message)", "Transforme os sub-workflows em tools do AI Agent node; o agente decide quando chamar cada um conforme a descrição de objetivo no system message", "Configure o loop gerador-crítico: o agente escritor itera com o feedback até o post alinhar-se à marca e atingir qualidade, sem intervenção humana", "Feche o ciclo com HTTP request para o webhook de automação do FeedHive, enviando o output do agente como rascunho agendável", "Use split-out + loop com session ID = item index para processar cada sugestão de conteúdo em execuções independentes do agente", "n8n self-hosted oferece execuções ilimitadas de workflow gratuitamente", "FeedHive tem versão leve embutida desse fluxo (IA avalia e sugere melhorias no post), porém sem fine-tune no seu conteúdo específico", "O mesmo padrão de workflows é replicável para outras tarefas de time de startup, não só criação de conteúdo"]
deep_dive: "medium"
deep_dive_reason: "Há densidade prática real (fine-tuning passo a passo, gate de score 0-1, loop gerador-crítico e orquestração no n8n com tools como sub-workflows), mas o padrão é pouco novel e o vídeo carrega forte viés promocional do bundle do autor."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-i-built-a-marketing-team-with-1-ai-agent-and-no-code-free-n8n-template--ldETapkr8Hg|I Built a Marketing Team with 1 AI Agent and No Code (free n8n template)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-everything-with-ai-agents-here-s-how--XVO3zsHdvio|Build Everything with AI Agents: Here's How]]", "[[extracts/youtube/ai-learning/2026-09-11-i-built-the-ultimate-team-of-ai-agents-in-n8n-with-no-code-free-template--9FuNtfsnRNo|I Built the Ultimate Team of AI Agents in n8n With No Code (Free Template)]]", "[[extracts/youtube/ai-learning/2026-09-11-could-a-swarm-of-autonomous-ai-agents-be-the-ultimate-business-asset-stage-1--UL55C80TEb8|Could a Swarm of Autonomous AI Agents be the Ultimate Business Asset? - Stage 1]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-use-ai-agents-to-make-money-vibe-marketing-tutorial--PduJ0P6r_8o|How I use AI agents to make money (Vibe Marketing Tutorial)]]", "[[extracts/youtube/ai-learning/2026-09-11-building-the-universal-ai-automation-layer-ft-n8n-ceo-jan-oberhauser--RUHU-w4Lz1I|Building the Universal AI Automation Layer ft n8n CEO Jan Oberhauser]]", "[[extracts/youtube/ai-learning/2026-09-11-build-n8n-agents-into-full-stack-apps-heres-how--UaJSXjNX3wo|Build n8n agents into full-stack apps, here’s how]]"]
theme: "Agentes de IA No-Code"
---

# How To Build a Startup Team of AI Agents (n8n, OpenAI, FeedHive)

## Tese
Um fundador pode substituir boa parte da equipe de conteúdo de uma startup combinando um modelo fine-tuned (estilo de escrita), um brand brief como contexto e um pipeline multi-agente no n8n que gera ideias, escreve, recebe feedback com nota 0-1 em loop e publica automaticamente no FeedHive.

## Conceitos-chave
- Fine-tuning de modelos com exemplos reverso-engenheirados (prompt→output)
- Formato JSONL de treinamento (messages user/assistant, 20-50 exemplos)
- Brand brief como contexto de identidade (valores, temas, dislikes, opositores)
- Distinção entre custom GPT com system prompt vs. agente real
- Pipeline multi-agente: gerador de ideias → escritor → crítico → refinamento em loop
- Gate de qualidade com score 0-1 e critérios no system message
- Sub-workflows do n8n usados como tools de um agente
- Memória de janela (window buffer) no agente
- Orquestração: split-out + loop sobre sugestões com session ID por item
- Publicação automática via HTTP request para webhook do FeedHive

## Ferramentas & pessoas
**Ferramentas:** OpenAI platform (fine-tuning), GPT-4o, GPT-4o Mini, ChatGPT, JSONL, n8n, Notion, FeedHive, Zapier, Make, Vercel, Netlify, Google Docs, Founder Stack

**Pessoas/orgs:** Simon (narrador), OpenAI, FeedHive (time do autor), Founder Stack

## Claims acionáveis
- Custom GPTs baseados só em system prompt raramente geram bons resultados; fine-tune com 20-50 exemplos captura estilo de escrita de forma superior
- Reverso-engenheie o prompt que teria gerado cada post de exemplo (manualmente ou via ChatGPT) para montar o dataset de fine-tuning
- Monte o dataset em JSONL com um par user/assistant por linha e use 
 para quebras de linha; treine sobre GPT-4o com defaults da plataforma
- Fine-tune resolve o 'como escrever', mas não o 'o que defender': escreva um brand brief em texto simples (valores, temas, posições, dislikes) e forneça-o como contexto no playground/workflow
- Use GPT-4o Mini para subtarefas baratas (gerar 10 ideias, dar feedback com score 0-1 em JSON) e reserve o modelo fine-tuned para a escrita final
- Estruture o pipeline no n8n como sub-workflows: brand brief (fetch Notion → aggregate → join), get content ideas, get content feedback (crítico com critérios em system message)
- Transforme os sub-workflows em tools do AI Agent node; o agente decide quando chamar cada um conforme a descrição de objetivo no system message
- Configure o loop gerador-crítico: o agente escritor itera com o feedback até o post alinhar-se à marca e atingir qualidade, sem intervenção humana
- Feche o ciclo com HTTP request para o webhook de automação do FeedHive, enviando o output do agente como rascunho agendável
- Use split-out + loop com session ID = item index para processar cada sugestão de conteúdo em execuções independentes do agente
- n8n self-hosted oferece execuções ilimitadas de workflow gratuitamente
- FeedHive tem versão leve embutida desse fluxo (IA avalia e sugere melhorias no post), porém sem fine-tune no seu conteúdo específico
- O mesmo padrão de workflows é replicável para outras tarefas de time de startup, não só criação de conteúdo

> **Deep dive:** `medium` — Há densidade prática real (fine-tuning passo a passo, gate de score 0-1, loop gerador-crítico e orquestração no n8n com tools como sub-workflows), mas o padrão é pouco novel e o vídeo carrega forte viés promocional do bundle do autor.
