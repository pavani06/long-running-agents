---
title: "10 Insane AI Agent Use Cases in n8n! (steal these)"
type: "extract"
source: "youtube"
video_id: "Dt6u-yFEpsk"
url: "https://www.youtube.com/watch?v=Dt6u-yFEpsk"
channel: "Jono Catliff"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-10-insane-ai-agent-use-cases-in-n8n-steal-these--Dt6u-yFEpsk.txt]]"
tags: ["agents", "agent-tooling", "agent-loop", "classification", "multi-agent", "process", "stack-tooling"]
thesis: "O vídeo promociona 10 blueprints gratuitos de agentes de IA construídos no n8n — integração com ChatGPT, web scraping de leads, chamadas de voz, triagem de e-mails, extração de recibos, assistente pessoal, chatbot de site, RAG corporativo, apps via vibe coding e clonagem de voz — como forma de automatizar tarefas diárias de negócio."
concepts: ["agentes de IA no-code no n8n", "integração ChatGPT-n8n via conectores bidirecionais", "web scraping automatizado de leads", "agente de chamadas de voz outbound", "classificação automática de e-mails (inbox zero)", "processamento OCR de recibos e faturas", "assistente pessoal via Telegram", "RAG com vector store de documentos da empresa", "sub-agentes encadeados", "vibe coding com Lovable", "clonagem de voz", "teste com amostras pequenas para controlar custos de API"]
tools: ["n8n", "ChatGPT", "Google Calendar", "Google Sheets", "Google Maps", "Google Drive", "Apollo", "Yellow Pages", "TikTok", "Instagram", "Telegram", "Vapi (transcrito como 'Vappy')", "Slack", "Gmail", "Lovable.dev", "ElevenLabs"]
people: ["Nathan (apresentador/chatbot do site)", "OpenAI", "Google", "Meta/Facebook", "Apollo", "Vapi", "Lovable", "ElevenLabs"]
claims: ["Conectar o ChatGPT a um agente n8n permite executar ações em milhares de apps, como criar eventos no Google Calendar com verificação automática de conflitos via conversa bidirecional", "Um agente de web scraping extrai leads (e-mails, telefones) de Google Maps, Apollo, Yellow Pages e redes sociais e os grava em tempo real no Google Sheets", "Configure limites rígidos e teste automações com amostras pequenas (ex.: 2 buscas) para evitar custos de API que escalam rapidamente", "Chamadas de voz com IA (Vapi) funcionam para tarefas simples como agendar compromissos, mas ainda são inferiores a humanos em vendas ou atendimento complexos — usar com cautela", "Um agente de inbox classifica e-mails por categoria (promocional, social, pessoal, vendas, recrutamento), aplica labels, cria rascunhos, encaminha faturas para o software contábil e envia notificações no Slack para itens importantes", "Recibos em imagem/PDF enviados por Telegram podem ter o texto extraído por um sub-agente de processamento de imagem e os line-items gravados automaticamente no Google Sheets", "Um assistente pessoal via Telegram+n8n pode manipular calendário (criar/editar/buscar eventos), Gmail, listas de tarefas, posts sociais e fazer chamadas em nome do usuário", "Pipeline RAG: extrair texto de PDFs no Google Drive e indexar em um vector store permite que um agente responda clientes via SMS/CRM com informações da empresa (serviços, preços, SOPs, contratos)", "Lovable.dev permite construir web apps personalizados em linguagem natural em minutos; embutir um agente de IA nele transmite autoridade e diferencia negócios de serviço", "ElevenLabs permite clonar a própria voz para responder mensagens de áudio com uma aproximação convincente (porém imperfeita) do timbre original", "Todos os blueprints demonstrados estão disponíveis gratuitamente via links na descrição do vídeo, com instruções passo a passo de instalação"]
deep_dive: "low"
deep_dive_reason: "Conteúdo promocional tipo listicle com demos superficiais de blueprints prontos no n8n, sem profundidade arquitetural nem discussão de harness, evals, context-engineering ou governança."
---

# 10 Insane AI Agent Use Cases in n8n! (steal these)

## Tese
O vídeo promociona 10 blueprints gratuitos de agentes de IA construídos no n8n — integração com ChatGPT, web scraping de leads, chamadas de voz, triagem de e-mails, extração de recibos, assistente pessoal, chatbot de site, RAG corporativo, apps via vibe coding e clonagem de voz — como forma de automatizar tarefas diárias de negócio.

## Conceitos-chave
- agentes de IA no-code no n8n
- integração ChatGPT-n8n via conectores bidirecionais
- web scraping automatizado de leads
- agente de chamadas de voz outbound
- classificação automática de e-mails (inbox zero)
- processamento OCR de recibos e faturas
- assistente pessoal via Telegram
- RAG com vector store de documentos da empresa
- sub-agentes encadeados
- vibe coding com Lovable
- clonagem de voz
- teste com amostras pequenas para controlar custos de API

## Ferramentas & pessoas
**Ferramentas:** n8n, ChatGPT, Google Calendar, Google Sheets, Google Maps, Google Drive, Apollo, Yellow Pages, TikTok, Instagram, Telegram, Vapi (transcrito como 'Vappy'), Slack, Gmail, Lovable.dev, ElevenLabs

**Pessoas/orgs:** Nathan (apresentador/chatbot do site), OpenAI, Google, Meta/Facebook, Apollo, Vapi, Lovable, ElevenLabs

## Claims acionáveis
- Conectar o ChatGPT a um agente n8n permite executar ações em milhares de apps, como criar eventos no Google Calendar com verificação automática de conflitos via conversa bidirecional
- Um agente de web scraping extrai leads (e-mails, telefones) de Google Maps, Apollo, Yellow Pages e redes sociais e os grava em tempo real no Google Sheets
- Configure limites rígidos e teste automações com amostras pequenas (ex.: 2 buscas) para evitar custos de API que escalam rapidamente
- Chamadas de voz com IA (Vapi) funcionam para tarefas simples como agendar compromissos, mas ainda são inferiores a humanos em vendas ou atendimento complexos — usar com cautela
- Um agente de inbox classifica e-mails por categoria (promocional, social, pessoal, vendas, recrutamento), aplica labels, cria rascunhos, encaminha faturas para o software contábil e envia notificações no Slack para itens importantes
- Recibos em imagem/PDF enviados por Telegram podem ter o texto extraído por um sub-agente de processamento de imagem e os line-items gravados automaticamente no Google Sheets
- Um assistente pessoal via Telegram+n8n pode manipular calendário (criar/editar/buscar eventos), Gmail, listas de tarefas, posts sociais e fazer chamadas em nome do usuário
- Pipeline RAG: extrair texto de PDFs no Google Drive e indexar em um vector store permite que um agente responda clientes via SMS/CRM com informações da empresa (serviços, preços, SOPs, contratos)
- Lovable.dev permite construir web apps personalizados em linguagem natural em minutos; embutir um agente de IA nele transmite autoridade e diferencia negócios de serviço
- ElevenLabs permite clonar a própria voz para responder mensagens de áudio com uma aproximação convincente (porém imperfeita) do timbre original
- Todos os blueprints demonstrados estão disponíveis gratuitamente via links na descrição do vídeo, com instruções passo a passo de instalação

> **Deep dive:** `low` — Conteúdo promocional tipo listicle com demos superficiais de blueprints prontos no n8n, sem profundidade arquitetural nem discussão de harness, evals, context-engineering ou governança.
