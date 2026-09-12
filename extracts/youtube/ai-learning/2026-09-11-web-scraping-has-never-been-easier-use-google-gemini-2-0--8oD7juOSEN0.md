---
title: "Web Scraping Has Never Been Easier  - Use Google Gemini 2.0"
type: "extract"
source: "youtube"
video_id: "8oD7juOSEN0"
url: "https://www.youtube.com/watch?v=8oD7juOSEN0"
channel: "Yaron Been"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-web-scraping-has-never-been-easier-use-google-gemini-2-0--8oD7juOSEN0.txt]]"
tags: ["agents", "model-selection", "stack-tooling", "analise"]
thesis: "O recurso \"stream real time\" do Gemini 2.0 Flash no Google AI Studio permite interação em tempo real com o que o modelo vê na tela/webcam, possibilitando extrair dados estruturados (JSON) de qualquer página visível sem código de scraping tradicional."
concepts: ["streaming multimodal em tempo real (vídeo da tela ou webcam como fonte)", "extração de dados estruturados (JSON/CSV) a partir da visão de tela", "scraping via modelo de visão em vez de código", "trade-off entre saída em áudio vs. texto para dados estruturados", "opções de execução: code execution, function calling, grounding", "interrupção de sessão ao trocar de abas durante o streaming", "agente companheiro/assistente com percepção de tela"]
tools: ["Gemini 2.0 Flash", "Google AI Studio (aistudio.google.com)", "Instant Data Scraper (extensão Chrome)", "Chrome", "Airbnb", "Apollo", "Google Maps", "Craigslist"]
people: ["Google"]
claims: ["Acesse aistudio.google.com, selecione o recurso 'stream real time', escolha webcam ou tela como fonte de vídeo e o modelo Gemini 2.0 Flash.", "Configure a saída como texto (não áudio) quando o objetivo é gerar JSON ou dados estruturados, pois o modo áudio degrada a precisão do texto gerado.", "Abrir novas abas durante uma sessão pode corromper a captura de tela pelo modelo; inicie uma nova sessão para restaurar o funcionamento.", "O modelo consegue extrair campos específicos visíveis na tela (nome, datas, preço por noite, rating, cargo, horário de funcionamento) e estruturá-los em JSON, demonstrado em Airbnb, Apollo, Google Maps e Craigslist.", "É possível ativar/desativar code execution, function calling e grounding na interface do stream real time conforme o caso de uso.", "O modelo identifica itens nomeados na tela (ex.: nome de uma extensão Chrome) e lê em voz alta ou registra conteúdo destacado pelo usuário."]
deep_dive: "low"
deep_dive_reason: "Demo tutorial superficial e de tom promocional, mostrando casos de uso básicos de extração de dados por visão de tela sem densidade de insight arquitetural, harness, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-google-gemini-2-0-is-amazing-realtime-stream-tested-multimodal-api--38N8pgnNANQ|Google Gemini 2.0 is AMAZING - Realtime Stream TESTED | Multimodal API]]", "[[extracts/youtube/ai-learning/2026-09-11-novo-chatgpt-acessa-camera-e-tela-do-celular-e-pc--cN6NraQXwHA|NOVO! CHATGPT acessa CÂMERA e TELA do Celular e PC 🤯🤯]]", "[[extracts/youtube/ai-learning/2026-09-11-automatize-todo-o-seu-trabalho-com-a-ia-project-mariner-do-google-incrivel--E0Jbaikf0o4|AUTOMATIZE TODO O SEU TRABALHO com a IA “Project Mariner” do GOOGLE - INCRÍVEL!]]", "[[extracts/youtube/ai-learning/2026-09-11-i-got-a-private-lesson-on-google-s-new-nano-banana-ai-model--3Zvk4AMCrG8|I got a private lesson on Google's NEW Nano Banana AI Model]]", "[[extracts/youtube/ai-learning/2026-09-11-create-anything-with-nano-banana-pro-heres-how--2VktR2fAmF0|Create Anything with Nano Banana Pro, Here’s How]]"]
---

# Web Scraping Has Never Been Easier  - Use Google Gemini 2.0

## Tese
O recurso "stream real time" do Gemini 2.0 Flash no Google AI Studio permite interação em tempo real com o que o modelo vê na tela/webcam, possibilitando extrair dados estruturados (JSON) de qualquer página visível sem código de scraping tradicional.

## Conceitos-chave
- streaming multimodal em tempo real (vídeo da tela ou webcam como fonte)
- extração de dados estruturados (JSON/CSV) a partir da visão de tela
- scraping via modelo de visão em vez de código
- trade-off entre saída em áudio vs. texto para dados estruturados
- opções de execução: code execution, function calling, grounding
- interrupção de sessão ao trocar de abas durante o streaming
- agente companheiro/assistente com percepção de tela

## Ferramentas & pessoas
**Ferramentas:** Gemini 2.0 Flash, Google AI Studio (aistudio.google.com), Instant Data Scraper (extensão Chrome), Chrome, Airbnb, Apollo, Google Maps, Craigslist

**Pessoas/orgs:** Google

## Claims acionáveis
- Acesse aistudio.google.com, selecione o recurso 'stream real time', escolha webcam ou tela como fonte de vídeo e o modelo Gemini 2.0 Flash.
- Configure a saída como texto (não áudio) quando o objetivo é gerar JSON ou dados estruturados, pois o modo áudio degrada a precisão do texto gerado.
- Abrir novas abas durante uma sessão pode corromper a captura de tela pelo modelo; inicie uma nova sessão para restaurar o funcionamento.
- O modelo consegue extrair campos específicos visíveis na tela (nome, datas, preço por noite, rating, cargo, horário de funcionamento) e estruturá-los em JSON, demonstrado em Airbnb, Apollo, Google Maps e Craigslist.
- É possível ativar/desativar code execution, function calling e grounding na interface do stream real time conforme o caso de uso.
- O modelo identifica itens nomeados na tela (ex.: nome de uma extensão Chrome) e lê em voz alta ou registra conteúdo destacado pelo usuário.

> **Deep dive:** `low` — Demo tutorial superficial e de tom promocional, mostrando casos de uso básicos de extração de dados por visão de tela sem densidade de insight arquitetural, harness, evals ou governança.
