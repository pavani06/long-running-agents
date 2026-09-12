---
title: "Google Gemini 2.0 is AMAZING - Realtime Stream TESTED | Multimodal API"
type: "extract"
source: "youtube"
video_id: "38N8pgnNANQ"
url: "https://www.youtube.com/watch?v=38N8pgnNANQ"
channel: "All About AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-google-gemini-2-0-is-amazing-realtime-stream-tested-multimodal-api--38N8pgnNANQ.txt]]"
tags: ["agents", "agent-tooling", "analise", "stack-tooling", "context-management", "model-selection"]
thesis: "O vídeo é uma demo de primeiro contato com o Gemini 2.0 Flash Experimental via Stream Realtime no Google AI Studio, mostrando tutoria de código Python passo a passo por voz com compartilhamento de tela, saída em texto no chat com manutenção de contexto, além de demos de geração nativa de imagens e uso nativo de ferramentas (execução de código e Google Search), que o apresentador considera competitivo com a OpenAI."
concepts: ["Gemini 2.0 Flash Experimental", "Multimodal Live API", "Stream Realtime (compartilhamento de tela/câmera em tempo real)", "Interação por voz em tempo real", "Modo de saída em texto (respostas no chat em vez de voz)", "Tutoria de programação passo a passo guiada por visão de tela", "Correção de erros em tempo real (sintaxe Python, parênteses, indentação)", "Manutenção de contexto de conversa via lista de contents/histórico", "Uso nativo de ferramentas (code execution + Google Search)", "Geração nativa de imagens na conversa (um único modelo para raciocínio e geração)", "Early Access allowlist (speech generation, image generation)", "Grounding com Google Search"]
tools: ["Google AI Studio", "Gemini 2.0 Flash Experimental", "Gemini API (API key)", "Stream Realtime", "Multimodal Live API", "Google Search (ferramenta nativa)", "Code execution (ferramenta nativa)", "Python (módulo random)", "python-dotenv (from dotenv load)", "Cursor / VS Code", "OpenAI Realtime API", "Dark Reader"]
people: ["Google", "OpenAI", "The Verge"]
claims: ["O Stream Realtime permite selecionar câmera ou tela como fonte de vídeo e o modelo descreve e acompanha o conteúdo em tempo real", "O Gemini atuou como tutor de Python, guiando passo a passo import, random.randint, variáveis, print, definição de função, indentação e correção de erros de sintaxe detectados visualmente na tela", "Alternando o output format para texto, as respostas aparecem no chat mesmo com compartilhamento de tela ativo, permitindo copiar código gerado a partir do que o modelo vê", "O modelo escreveu código funcional da API Gemini (carregamento de API key via dotenv, função chat(contents)) e depois a versão completa com input do usuário no terminal e lista de conversa para manter contexto", "O modelo conseguiu manter contexto multi-turno (lembrar 'um código para somar dois inteiros' na pergunta seguinte) e consolidar múltiplos resumos de artigos em um resumo final", "Gemini 2.0 gera imagens nativamente na conversa (ex.: transformar um carro em conversível com um prompt simples), sem mascaramento manual ou prompts complexos", "Uso nativo de ferramentas (code execution + Google Search) combinado com áudio em tempo real permite operações como criar e modificar gráficos de barras por voz", "O Stream Realtime está disponível gratuitamente no momento do vídeo", "O apresentador não tem acesso ainda a speech generation e image generation via Early Access allowlist", "A latência de resposta é boa mas não hiper-rápida, com crashes ocasionais e sem bugs graves", "O apresentador considera a oferta do Google melhor que a da OpenAI em multimodalidade e está animado para testar a API com tool calling"]
deep_dive: "low"
deep_dive_reason: "É uma demo introdutória/promocional de produto com tutoriais básicos de uso, sem densidade de insight arquitetural, evals, harness ou engenharia de contexto além de menção superficial a histórico de conversa."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-web-scraping-has-never-been-easier-use-google-gemini-2-0--8oD7juOSEN0|Web Scraping Has Never Been Easier  - Use Google Gemini 2.0]]", "[[extracts/youtube/ai-learning/2026-09-11-novo-chatgpt-acessa-camera-e-tela-do-celular-e-pc--cN6NraQXwHA|NOVO! CHATGPT acessa CÂMERA e TELA do Celular e PC 🤯🤯]]", "[[extracts/youtube/ai-learning/2026-09-11-i-got-a-private-lesson-on-google-s-new-nano-banana-ai-model--3Zvk4AMCrG8|I got a private lesson on Google's NEW Nano Banana AI Model]]", "[[extracts/youtube/ai-learning/2026-09-11-sora-da-openai-e-lancada-primeiras-impressoes-das-funcoes--TBmcvEmPXJ4|SORA da OPENAI é LANÇADA! PRIMEIRAS IMPRESSÕES das FUNÇÕES 🤯]]", "[[extracts/youtube/ai-learning/2026-09-11-full-interview-googles-sundar-pichai-reveals-future-of-ai-in-candid-talk-with-ma--1G-X70bnJEg|FULL INTERVIEW: Google’s Sundar Pichai Reveals Future of AI in Candid Talk with Marc Benioff | AI1G]]", "[[extracts/youtube/ai-learning/2026-09-11-automatize-todo-o-seu-trabalho-com-a-ia-project-mariner-do-google-incrivel--E0Jbaikf0o4|AUTOMATIZE TODO O SEU TRABALHO com a IA “Project Mariner” do GOOGLE - INCRÍVEL!]]"]
theme: "Stack de IA e Prompting"
---

# Google Gemini 2.0 is AMAZING - Realtime Stream TESTED | Multimodal API

## Tese
O vídeo é uma demo de primeiro contato com o Gemini 2.0 Flash Experimental via Stream Realtime no Google AI Studio, mostrando tutoria de código Python passo a passo por voz com compartilhamento de tela, saída em texto no chat com manutenção de contexto, além de demos de geração nativa de imagens e uso nativo de ferramentas (execução de código e Google Search), que o apresentador considera competitivo com a OpenAI.

## Conceitos-chave
- Gemini 2.0 Flash Experimental
- Multimodal Live API
- Stream Realtime (compartilhamento de tela/câmera em tempo real)
- Interação por voz em tempo real
- Modo de saída em texto (respostas no chat em vez de voz)
- Tutoria de programação passo a passo guiada por visão de tela
- Correção de erros em tempo real (sintaxe Python, parênteses, indentação)
- Manutenção de contexto de conversa via lista de contents/histórico
- Uso nativo de ferramentas (code execution + Google Search)
- Geração nativa de imagens na conversa (um único modelo para raciocínio e geração)
- Early Access allowlist (speech generation, image generation)
- Grounding com Google Search

## Ferramentas & pessoas
**Ferramentas:** Google AI Studio, Gemini 2.0 Flash Experimental, Gemini API (API key), Stream Realtime, Multimodal Live API, Google Search (ferramenta nativa), Code execution (ferramenta nativa), Python (módulo random), python-dotenv (from dotenv load), Cursor / VS Code, OpenAI Realtime API, Dark Reader

**Pessoas/orgs:** Google, OpenAI, The Verge

## Claims acionáveis
- O Stream Realtime permite selecionar câmera ou tela como fonte de vídeo e o modelo descreve e acompanha o conteúdo em tempo real
- O Gemini atuou como tutor de Python, guiando passo a passo import, random.randint, variáveis, print, definição de função, indentação e correção de erros de sintaxe detectados visualmente na tela
- Alternando o output format para texto, as respostas aparecem no chat mesmo com compartilhamento de tela ativo, permitindo copiar código gerado a partir do que o modelo vê
- O modelo escreveu código funcional da API Gemini (carregamento de API key via dotenv, função chat(contents)) e depois a versão completa com input do usuário no terminal e lista de conversa para manter contexto
- O modelo conseguiu manter contexto multi-turno (lembrar 'um código para somar dois inteiros' na pergunta seguinte) e consolidar múltiplos resumos de artigos em um resumo final
- Gemini 2.0 gera imagens nativamente na conversa (ex.: transformar um carro em conversível com um prompt simples), sem mascaramento manual ou prompts complexos
- Uso nativo de ferramentas (code execution + Google Search) combinado com áudio em tempo real permite operações como criar e modificar gráficos de barras por voz
- O Stream Realtime está disponível gratuitamente no momento do vídeo
- O apresentador não tem acesso ainda a speech generation e image generation via Early Access allowlist
- A latência de resposta é boa mas não hiper-rápida, com crashes ocasionais e sem bugs graves
- O apresentador considera a oferta do Google melhor que a da OpenAI em multimodalidade e está animado para testar a API com tool calling

> **Deep dive:** `low` — É uma demo introdutória/promocional de produto com tutoriais básicos de uso, sem densidade de insight arquitetural, evals, harness ou engenharia de contexto além de menção superficial a histórico de conversa.
