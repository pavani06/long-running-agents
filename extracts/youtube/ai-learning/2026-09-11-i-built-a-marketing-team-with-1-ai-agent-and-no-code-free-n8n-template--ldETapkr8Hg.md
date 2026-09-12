---
title: "I Built a Marketing Team with 1 AI Agent and No Code (free n8n template)"
type: "extract"
source: "youtube"
video_id: "ldETapkr8Hg"
url: "https://www.youtube.com/watch?v=ldETapkr8Hg"
channel: "Nate Herk | AI Automation"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-i-built-a-marketing-team-with-1-ai-agent-and-no-code-free-n8n-template--ldETapkr8Hg.txt]]"
tags: ["agents", "agent-tooling", "agent-loop", "multi-agent", "arquitetura", "context-engineering", "error-handling", "memory-architecture", "model-selection", "runtime", "state", "token-budgeting", "observability", "production", "frameworks"]
thesis: "Um único agente de IA orquestrado no n8n, com seis sub-workflows expostos como ferramentas (criar/editar/buscar imagens, posts de blog/LinkedIn e vídeos), pode operar como uma equipe de marketing completa via Telegram, com padronização de entrada, roteamento por intenção, logging em planilha como memória e custos por operação mapeados."
concepts: ["Agente único com múltiplas ferramentas implementadas como sub-workflows chamáveis", "Padronização de entrada voz/texto em um único campo (text) consumido pelo agente", "Design de system prompt: visão geral, descrição de cada ferramenta e quando usá-la, incluindo sinônimos (make = editar)", "Trigger 'when executed by another workflow' com campos de entrada definidos para expor parâmetros preenchíveis pelo modelo", "Passthrough do Telegram chat ID como variável dinâmica para rotear respostas assíncronas", "Google Sheets como banco de dados de ativos (título, tipo, request, ID, link, post)", "Google Drive como storage de mídia com ID referenciável para edições futuras", "Roteamento por intenção (get vs edit) ramificando o subflow de busca", "Structured output parsers para forçar formatos (título+prompt; nome/ID/link/status; partes 1-4)", "Split out de outputs estruturados para paralelizar geração por cena", "Workaround de timeout em nível de agente: subflow longo entrega resultado direto ao Telegram mesmo com erro no nó do agente", "Polling com loop vs espera fixa (90s) para sincronizar geração assíncrona de imagens/vídeos", "Escape de aspas duplas para simples em strings injetadas em payloads HTTP JSON", "Pipeline encadeado de agentes especializados: pesquisa → conteúdo → prompt de imagem → imagem → vídeo → som → render", "Seleção dinâmica de modelo por custo no endpoint de imagem", "Custeio por operação (preço por imagem, edição, clipe de vídeo e tokens)"]
tools: ["n8n", "Telegram", "OpenAI GPT Image 1 (gpt-image-1)", "OpenAI image edit endpoint", "DALL-E 2", "DALL-E 3", "ChatGPT-4o (modelo de imagem equivalente)", "Flux via PiAPI", "PiAPI", "Runway", "ElevenLabs", "Creatomate", "Google Drive", "Google Sheets", "Tavily", "OpenRouter", "GPT-4.1", "GPT-4.1 mini", "Think tool (n8n)"]
people: ["OpenAI", "n8n", "Google", "Runway", "ElevenLabs", "Tavily", "OpenRouter", "PiAPI", "Creatomate", "Skool (comunidade gratuita do criador)", "Comunidade paga do criador (1100+ membros)"]
claims: ["Padronize voz e texto num único campo (ex.: JSON.text) para o agente tratar ambos os canais de forma idêntica", "Liste no system prompt cada ferramenta e quando usá-la, incluindo sinônimos de comandos do usuário (make indica editar a última imagem)", "Use o trigger Execute Workflow com campos de entrada definidos para que a tool do agente exponha parâmetros que o modelo preenche dinamicamente", "Passe o chat ID do Telegram como variável dinâmica por todos os sub-workflows para garantir que entregas assíncronas voltem à conversa correta", "Logue cada output em planilha (título, tipo, request, ID, link, post) para criar memória consultável e banco de imagens editáveis", "Para editar uma imagem: buscar o ID no banco, baixar o binário do Drive e enviá-lo com o prompt ao endpoint de edição da OpenAI", "Use um parâmetro de intenção (get/edit) no subflow de busca para ramificar entre apenas retornar o ID ou enviar o arquivo completo", "Subflows longos (vídeos de 2-3 min) estouram o timeout do agente no n8n; projete o subflow para enviar o resultado direto ao Telegram mesmo quando o nó do agente falhar", "Substitua aspas duplas por simples em strings de prompt antes de montar o JSON do HTTP request para evitar falhas de parse", "Prefira polling com loop a esperas fixas (ex.: 90s) para não avançar no workflow com geração de imagens incompleta", "Split out de outputs estruturados (partes 1-4) permite gerar imagens e vídeos por cena em paralelo antes do render final", "Gere prompts de som por cena no ElevenLabs (clips de 5s) e renderize vídeo+áudio num template do Creatomate via API", "Custos de referência: ~US$0,19-0,20 por imagem/edição (GPT Image 1), ~US$0,015 por imagem (Flux/PiAPI), ~US$0,25 por clipe de 5s (Runway, ~US$1 por vídeo), n8n cloud ~US$27/mês, ElevenLabs starter US$5/mês, GPT-4.1 a US$2/M entrada e US$8/M saída, 4.1-mini a US$0,40/M e US$1,60/M", "O parâmetro model do endpoint de imagem pode ser dinâmico, permitindo ao agente escolher modelos mais baratos (DALL-E 2/3) conforme a tarefa"]
deep_dive: "medium"
deep_dive_reason: "O vídeo entrega densidade razoável de detalhes arquiteturais acionáveis (sub-workflows como tools, workaround de timeout, polling vs espera fixa, planilha como memória e custeio por operação), mas permanece um tutorial de build em n8n sem novidade ou profundidade em harness, evals, agent-fleets ou governança."
---

# I Built a Marketing Team with 1 AI Agent and No Code (free n8n template)

## Tese
Um único agente de IA orquestrado no n8n, com seis sub-workflows expostos como ferramentas (criar/editar/buscar imagens, posts de blog/LinkedIn e vídeos), pode operar como uma equipe de marketing completa via Telegram, com padronização de entrada, roteamento por intenção, logging em planilha como memória e custos por operação mapeados.

## Conceitos-chave
- Agente único com múltiplas ferramentas implementadas como sub-workflows chamáveis
- Padronização de entrada voz/texto em um único campo (text) consumido pelo agente
- Design de system prompt: visão geral, descrição de cada ferramenta e quando usá-la, incluindo sinônimos (make = editar)
- Trigger 'when executed by another workflow' com campos de entrada definidos para expor parâmetros preenchíveis pelo modelo
- Passthrough do Telegram chat ID como variável dinâmica para rotear respostas assíncronas
- Google Sheets como banco de dados de ativos (título, tipo, request, ID, link, post)
- Google Drive como storage de mídia com ID referenciável para edições futuras
- Roteamento por intenção (get vs edit) ramificando o subflow de busca
- Structured output parsers para forçar formatos (título+prompt; nome/ID/link/status; partes 1-4)
- Split out de outputs estruturados para paralelizar geração por cena
- Workaround de timeout em nível de agente: subflow longo entrega resultado direto ao Telegram mesmo com erro no nó do agente
- Polling com loop vs espera fixa (90s) para sincronizar geração assíncrona de imagens/vídeos
- Escape de aspas duplas para simples em strings injetadas em payloads HTTP JSON
- Pipeline encadeado de agentes especializados: pesquisa → conteúdo → prompt de imagem → imagem → vídeo → som → render
- Seleção dinâmica de modelo por custo no endpoint de imagem
- Custeio por operação (preço por imagem, edição, clipe de vídeo e tokens)

## Ferramentas & pessoas
**Ferramentas:** n8n, Telegram, OpenAI GPT Image 1 (gpt-image-1), OpenAI image edit endpoint, DALL-E 2, DALL-E 3, ChatGPT-4o (modelo de imagem equivalente), Flux via PiAPI, PiAPI, Runway, ElevenLabs, Creatomate, Google Drive, Google Sheets, Tavily, OpenRouter, GPT-4.1, GPT-4.1 mini, Think tool (n8n)

**Pessoas/orgs:** OpenAI, n8n, Google, Runway, ElevenLabs, Tavily, OpenRouter, PiAPI, Creatomate, Skool (comunidade gratuita do criador), Comunidade paga do criador (1100+ membros)

## Claims acionáveis
- Padronize voz e texto num único campo (ex.: JSON.text) para o agente tratar ambos os canais de forma idêntica
- Liste no system prompt cada ferramenta e quando usá-la, incluindo sinônimos de comandos do usuário (make indica editar a última imagem)
- Use o trigger Execute Workflow com campos de entrada definidos para que a tool do agente exponha parâmetros que o modelo preenche dinamicamente
- Passe o chat ID do Telegram como variável dinâmica por todos os sub-workflows para garantir que entregas assíncronas voltem à conversa correta
- Logue cada output em planilha (título, tipo, request, ID, link, post) para criar memória consultável e banco de imagens editáveis
- Para editar uma imagem: buscar o ID no banco, baixar o binário do Drive e enviá-lo com o prompt ao endpoint de edição da OpenAI
- Use um parâmetro de intenção (get/edit) no subflow de busca para ramificar entre apenas retornar o ID ou enviar o arquivo completo
- Subflows longos (vídeos de 2-3 min) estouram o timeout do agente no n8n; projete o subflow para enviar o resultado direto ao Telegram mesmo quando o nó do agente falhar
- Substitua aspas duplas por simples em strings de prompt antes de montar o JSON do HTTP request para evitar falhas de parse
- Prefira polling com loop a esperas fixas (ex.: 90s) para não avançar no workflow com geração de imagens incompleta
- Split out de outputs estruturados (partes 1-4) permite gerar imagens e vídeos por cena em paralelo antes do render final
- Gere prompts de som por cena no ElevenLabs (clips de 5s) e renderize vídeo+áudio num template do Creatomate via API
- Custos de referência: ~US$0,19-0,20 por imagem/edição (GPT Image 1), ~US$0,015 por imagem (Flux/PiAPI), ~US$0,25 por clipe de 5s (Runway, ~US$1 por vídeo), n8n cloud ~US$27/mês, ElevenLabs starter US$5/mês, GPT-4.1 a US$2/M entrada e US$8/M saída, 4.1-mini a US$0,40/M e US$1,60/M
- O parâmetro model do endpoint de imagem pode ser dinâmico, permitindo ao agente escolher modelos mais baratos (DALL-E 2/3) conforme a tarefa

> **Deep dive:** `medium` — O vídeo entrega densidade razoável de detalhes arquiteturais acionáveis (sub-workflows como tools, workaround de timeout, polling vs espera fixa, planilha como memória e custeio por operação), mas permanece um tutorial de build em n8n sem novidade ou profundidade em harness, evals, agent-fleets ou governança.
