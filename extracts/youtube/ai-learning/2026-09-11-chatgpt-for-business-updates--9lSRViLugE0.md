---
title: "ChatGPT for Business Updates"
type: "extract"
source: "youtube"
video_id: "9lSRViLugE0"
url: "https://www.youtube.com/watch?v=9lSRViLugE0"
channel: "OpenAI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-chatgpt-for-business-updates--9lSRViLugE0.txt]]"
tags: ["context-engineering", "permissions", "knowledge-management", "agent-tooling", "agent-loop", "agents", "context-management", "stack-tooling"]
thesis: "A OpenAI integra o contexto de trabalho das empresas no ChatGPT por meio de conectores com pesquisa profunda que respeitam permissões, record mode para capturar reuniões faladas e conectores customizados via MCP, transformando o ChatGPT em uma memória e colaborador corporativo."
concepts: ["conectores de dados internos", "deep research agentic sobre fontes privadas", "respeito e enforcement de permissões de usuário em tempo real", "record mode / transcrição de reuniões com resumo estruturado", "MCP (Model Context Protocol)", "conectores customizados publicáveis em registry", "reescrita de queries contextualizadas (recência, filtros de fonte)", "citations e source tab para verificação", "modo automático de análise de dados sobre conhecimento empresarial", "transcrições como parte do corpus pesquisável", "créditos e pricing flexível"]
tools: ["ChatGPT for Business", "Deep Research", "Record Mode", "Responses API", "MCP", "Conector HubSpot", "GitHub", "Gmail", "Google Drive", "SharePoint", "Microsoft Teams", "Outlook", "Dropbox", "Box", "Linear", "Google Calendar", "Outlook Calendar", "Whisker DB (demo fictícia)", "AGI Corp / Animal GPT / Bark to Text (cenário fictício de demo)", "app desktop macOS"]
people: ["Nate", "Neil", "Priya", "Dibbo", "Sandra", "OpenAI", "Equipe de desenvolvedores do HubSpot"]
claims: ["Conectores respeitam e reforçam as permissões existentes do usuário em tempo de query, inclusive quando o acesso a um documento muda durante a sessão", "Deep research sobre fontes privadas (HubSpot, Teams, SharePoint, Outlook) leva 5 a 10 minutos, substituindo horas ou dias de busca manual em CRM, e-mail e mensageria", "O modelo foi pós-treinado para detectar automaticamente quando uma pergunta requer conhecimento interno e disparar a busca, com alternativa de seleção manual de fontes no composer", "O sistema reescreve a pergunta do usuário em uma ou mais queries contextualizadas com atributos de recência e filtros de fonte, e o backend de busca retorna somente resultados que o usuário tem permissão para ver", "Após receber resultados, o modelo decide autonomamente fazer perguntas de follow-up, abrir arquivos, usar outras ferramentas ou responder imediatamente", "O modo de análise de dados extrai automaticamente dados do conhecimento empresarial conectado, eliminando o upload manual de planilhas", "Record mode no app desktop macOS transcreve áudio e gera resumo estruturado com pontos-chave, action items e timestamps que citam o transcript para verificação", "As transcrições de reuniões entram no mesmo corpus pesquisável de docs e dados, permitindo recall de decisões passadas e geração de atualizações para liderança", "Admins de workspaces enterprise/team podem conectar e publicar conectores MCP customizados para toda a organização; usuários pro podem publicá-los no próprio ChatGPT", "O conector do HubSpot foi construído pela equipe de desenvolvedores do HubSpot e é o primeiro conector MCP customizado publicado no registry do ChatGPT", "Por padrão não há treinamento em dados de Teams, Edu e Enterprise, incluindo qualquer dado conectado", "Conectores de armazenamento de arquivos (Google Drive, SharePoint, Dropbox e Box em beta) estão sendo liberados para planos Teams, Enterprise e Edu", "Novos créditos dão aos workspaces existentes acesso completo a modelos e recursos avançados; enterprise disponível imediatamente e team nas semanas seguintes"]
deep_dive: "medium"
deep_dive_reason: "Demo de lançamento com detalhes arquiteturais genuínos (reescrita de queries, enforcement de permissões em tempo real, conectores MCP publicáveis), mas tom majoritariamente promocional e sem profundidade em harness, evals ou design de agent-fleets."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-7-mind-blowing-new-use-cases-for-chatgpt-in-2025-big-changes-ahead--8IUkOAvMP-M|7 Mind-Blowing NEW Use Cases For ChatGPT in 2025 (Big Changes Ahead)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-get-ahead-of-99-of-people-with-ai--0tLHVyd7WtM|How to Get Ahead of 99% of People (with AI)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-novo-chatgpt-acessa-camera-e-tela-do-celular-e-pc--cN6NraQXwHA|NOVO! CHATGPT acessa CÂMERA e TELA do Celular e PC 🤯🤯]]", "[[extracts/youtube/ai-learning/2026-09-11-learn-80-of-notebooklm-in-under-13-minutes--EOmgC3-hznM|Learn 80% of NotebookLM in Under 13 Minutes!]]", "[[extracts/youtube/ai-learning/2026-09-11-build-ai-agent-workforce-multi-agent-framework-with-metagpt-chatdev--pJwR5pv0_gs|Build AI agent workforce - Multi agent framework with MetaGPT & chatDev]]"]
---

# ChatGPT for Business Updates

## Tese
A OpenAI integra o contexto de trabalho das empresas no ChatGPT por meio de conectores com pesquisa profunda que respeitam permissões, record mode para capturar reuniões faladas e conectores customizados via MCP, transformando o ChatGPT em uma memória e colaborador corporativo.

## Conceitos-chave
- conectores de dados internos
- deep research agentic sobre fontes privadas
- respeito e enforcement de permissões de usuário em tempo real
- record mode / transcrição de reuniões com resumo estruturado
- MCP (Model Context Protocol)
- conectores customizados publicáveis em registry
- reescrita de queries contextualizadas (recência, filtros de fonte)
- citations e source tab para verificação
- modo automático de análise de dados sobre conhecimento empresarial
- transcrições como parte do corpus pesquisável
- créditos e pricing flexível

## Ferramentas & pessoas
**Ferramentas:** ChatGPT for Business, Deep Research, Record Mode, Responses API, MCP, Conector HubSpot, GitHub, Gmail, Google Drive, SharePoint, Microsoft Teams, Outlook, Dropbox, Box, Linear, Google Calendar, Outlook Calendar, Whisker DB (demo fictícia), AGI Corp / Animal GPT / Bark to Text (cenário fictício de demo), app desktop macOS

**Pessoas/orgs:** Nate, Neil, Priya, Dibbo, Sandra, OpenAI, Equipe de desenvolvedores do HubSpot

## Claims acionáveis
- Conectores respeitam e reforçam as permissões existentes do usuário em tempo de query, inclusive quando o acesso a um documento muda durante a sessão
- Deep research sobre fontes privadas (HubSpot, Teams, SharePoint, Outlook) leva 5 a 10 minutos, substituindo horas ou dias de busca manual em CRM, e-mail e mensageria
- O modelo foi pós-treinado para detectar automaticamente quando uma pergunta requer conhecimento interno e disparar a busca, com alternativa de seleção manual de fontes no composer
- O sistema reescreve a pergunta do usuário em uma ou mais queries contextualizadas com atributos de recência e filtros de fonte, e o backend de busca retorna somente resultados que o usuário tem permissão para ver
- Após receber resultados, o modelo decide autonomamente fazer perguntas de follow-up, abrir arquivos, usar outras ferramentas ou responder imediatamente
- O modo de análise de dados extrai automaticamente dados do conhecimento empresarial conectado, eliminando o upload manual de planilhas
- Record mode no app desktop macOS transcreve áudio e gera resumo estruturado com pontos-chave, action items e timestamps que citam o transcript para verificação
- As transcrições de reuniões entram no mesmo corpus pesquisável de docs e dados, permitindo recall de decisões passadas e geração de atualizações para liderança
- Admins de workspaces enterprise/team podem conectar e publicar conectores MCP customizados para toda a organização; usuários pro podem publicá-los no próprio ChatGPT
- O conector do HubSpot foi construído pela equipe de desenvolvedores do HubSpot e é o primeiro conector MCP customizado publicado no registry do ChatGPT
- Por padrão não há treinamento em dados de Teams, Edu e Enterprise, incluindo qualquer dado conectado
- Conectores de armazenamento de arquivos (Google Drive, SharePoint, Dropbox e Box em beta) estão sendo liberados para planos Teams, Enterprise e Edu
- Novos créditos dão aos workspaces existentes acesso completo a modelos e recursos avançados; enterprise disponível imediatamente e team nas semanas seguintes

> **Deep dive:** `medium` — Demo de lançamento com detalhes arquiteturais genuínos (reescrita de queries, enforcement de permissões em tempo real, conectores MCP publicáveis), mas tom majoritariamente promocional e sem profundidade em harness, evals ou design de agent-fleets.
