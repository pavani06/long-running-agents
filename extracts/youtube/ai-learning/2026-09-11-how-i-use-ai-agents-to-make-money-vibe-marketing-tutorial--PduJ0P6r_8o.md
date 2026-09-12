---
title: "How I use AI agents to make money (Vibe Marketing Tutorial)"
type: "extract"
source: "youtube"
video_id: "PduJ0P6r_8o"
url: "https://www.youtube.com/watch?v=PduJ0P6r_8o"
channel: "Greg Isenberg"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-i-use-ai-agents-to-make-money-vibe-marketing-tutorial--PduJ0P6r_8o.txt]]"
tags: ["agents", "agent-fleets", "multi-agent", "agent-tooling", "stack-tooling", "model-selection", "agentic-coding", "monitoramento", "process"]
thesis: "Vibe marketing é a combinação de ferramentas de vibe coding com plataformas de agentes/workflows (n8n, GumLoop, Lindy, Manus) que permite a um único marketer com bom gosto orquestrar exércitos de agentes de IA para executar, testar e otimizar campanhas em escala antes possível apenas para grandes equipes."
concepts: ["vibe marketing", "vibe coding", "agent swarms", "workflow automation", "model scorecard / seleção de modelo por tarefa", "closed-loop de estratégia (pull → transform → analyze → apply)", "human-in-the-loop", "manager agents treinados por especialistas humanos", "marketing como high-frequency trading", "arbitragem de conteúdo gerado por IA", "pensar em sistemas, não em campanhas", "build once, distribute forever"]
tools: ["Replit", "Bolt", "Lovable", "n8n", "GumLoop", "Manus", "Tascade", "Lindy.ai", "Claude / Claude 3.7", "OpenRouter", "Sora", "ChatGPT image gen", "Google Sheets", "Google Apps Script", "Perplexity (Sonar / Deep Research)", "Midjourney", "Leonardo AI", "Kling AI", "ElevenLabs", "Airtable", "YouTube API", "Google Cloud Console", "Grok 3", "DeepSeek R1 / DeepSeek Reasoner", "OpenAI o3", "o4-mini"]
people: ["Startup Ideas podcast", "LCA (design agency)", "Boring Marketer (James)", "Jordan Mix", "Late Checkout", "Flo (lindy.ai)", "Jacob Posel", "TikTok", "Reddit", "Startup Empire"]
claims: ["Combine vibe coding tools com plataformas de agentes (GumLoop, n8n, Lindy, Manus) para construir campanhas de marketing sem equipe de desenvolvimento.", "Crie um scorecard comparando LLMs por tarefa (ex.: Claude 3.7 para briefs e blogs) e reavalie constantemente, pois a qualidade dos modelos muda em semanas.", "Use OpenRouter como chave única de API para rotear múltiplos modelos (DeepSeek R1, o3, Grok 3) conforme a tarefa.", "Workflow 'one-click CRM': extensão de browser GumLoop → scrape de transcript → análise + web search → extração de links sociais → outreach personalizado → Airtable → resumo semanal para o time.", "Workflow de escala de conteúdo: minerar subreddits por dores validadas → gerar ideias com OpenAI → armazenar em Sheets → produzir posts LinkedIn, roteiros YouTube e blog com Claude 3.7.", "E-commerce: rodar um SKU da Amazon por 7 agentes de IA (reviews, keywords, comportamento de busca) gerando listing completo (títulos, bullets, termos de back-end, A+ content).", "Newsletter 100% IA: Google Apps Script lê tópico/ponto de vista de uma Sheet → Perplexity para deep research → Claude para escrita → Midjourney para imagens, com humano no loop para evitar 'AI slop'.", "Arbitragem de vídeo: roteiro via ChatGPT + imagens Leonardo AI + animação via Kling AI + voz ElevenLabs para conteúdo nível Pixar enquanto os concorrentes não fazem o mesmo.", "Fórmula básica de workflow: puxar dados de fontes → transformar com IA → analisar resultados → aplicar insights à estratégia → fechar o loop com output.", "Workflows elementares para começar: data analyzer (Sheets + IA), content monitor (scrape Reddit + resumo), competitor alerts, email summarizer semanal.", "Dedique 30 minutos por dia para criar um workflow e pergunte à equipe quais tarefas repetitivas podem ser automatizadas; a maioria das plataformas tem trial gratuito.", "Visão de 12–18 meses: agentes interconectados com contexto compartilhado, geridos por manager agents treinados por especialistas humanos, com metas declaradas ('quero 50k visitantes orgânicos, descubra como') em vez de tarefas pontuais."]
deep_dive: "medium"
deep_dive_reason: "Há densidade razoável de workflows acionáveis (receitas concretas de stack n8n/Sheets/OpenRouter e scorecard de modelos), mas falta profundidade arquitetural em harness/evals/context-engineering e o episódio mistura conteúdo com promoção de produtos próprios."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-i-built-a-marketing-team-with-1-ai-agent-and-no-code-free-n8n-template--ldETapkr8Hg|I Built a Marketing Team with 1 AI Agent and No Code (free n8n template)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-everything-with-ai-agents-here-s-how--XVO3zsHdvio|Build Everything with AI Agents: Here's How]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-a-startup-team-of-ai-agents-n8n-openai-feedhive--Hm0DZtiKUI8|How To Build a Startup Team of AI Agents (n8n, OpenAI, FeedHive)]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-n8n-full-tutorial-building-ai-agents-in-2025-for-beginners--ZbIVOy_GPyQ|N8N Full Tutorial: Building AI Agents in 2025 for Beginners!]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-sell-ai-workflows-without-starting-an-agency--QIsJe-nZ5XE|How to Sell AI Workflows (Without Starting an Agency)]]", "[[extracts/youtube/ai-learning/2026-09-11-zero-click-marketing-how-founders-win-when-google-social-llms-stop-sending-traff--MBxhzARQNeo|Zero-Click Marketing: How Founders Win When Google, Social & LLMs Stop Sending Traffic]]", "[[extracts/youtube/ai-learning/2026-09-11-5-brand-new-digital-marketing-strategies-for-2025-biggest-change-yet--4bZUZeeiacU|5 BRAND NEW Digital Marketing Strategies for 2025 (BIGGEST Change Yet!)]]", "[[extracts/youtube/ai-learning/2026-09-11-windsurf-ai-made-me-rank-1-instantly-free-tool--5XaXLLA4gK0|Windsurf AI Made Me Rank #1 Instantly (FREE TOOL!) 🚀]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-do-digital-marketing-with-0--AtZiJzQSH7k|How to do Digital Marketing with $0]]"]
theme: "Agentes de IA No-Code"
---

# How I use AI agents to make money (Vibe Marketing Tutorial)

## Tese
Vibe marketing é a combinação de ferramentas de vibe coding com plataformas de agentes/workflows (n8n, GumLoop, Lindy, Manus) que permite a um único marketer com bom gosto orquestrar exércitos de agentes de IA para executar, testar e otimizar campanhas em escala antes possível apenas para grandes equipes.

## Conceitos-chave
- vibe marketing
- vibe coding
- agent swarms
- workflow automation
- model scorecard / seleção de modelo por tarefa
- closed-loop de estratégia (pull → transform → analyze → apply)
- human-in-the-loop
- manager agents treinados por especialistas humanos
- marketing como high-frequency trading
- arbitragem de conteúdo gerado por IA
- pensar em sistemas, não em campanhas
- build once, distribute forever

## Ferramentas & pessoas
**Ferramentas:** Replit, Bolt, Lovable, n8n, GumLoop, Manus, Tascade, Lindy.ai, Claude / Claude 3.7, OpenRouter, Sora, ChatGPT image gen, Google Sheets, Google Apps Script, Perplexity (Sonar / Deep Research), Midjourney, Leonardo AI, Kling AI, ElevenLabs, Airtable, YouTube API, Google Cloud Console, Grok 3, DeepSeek R1 / DeepSeek Reasoner, OpenAI o3, o4-mini

**Pessoas/orgs:** Startup Ideas podcast, LCA (design agency), Boring Marketer (James), Jordan Mix, Late Checkout, Flo (lindy.ai), Jacob Posel, TikTok, Reddit, Startup Empire

## Claims acionáveis
- Combine vibe coding tools com plataformas de agentes (GumLoop, n8n, Lindy, Manus) para construir campanhas de marketing sem equipe de desenvolvimento.
- Crie um scorecard comparando LLMs por tarefa (ex.: Claude 3.7 para briefs e blogs) e reavalie constantemente, pois a qualidade dos modelos muda em semanas.
- Use OpenRouter como chave única de API para rotear múltiplos modelos (DeepSeek R1, o3, Grok 3) conforme a tarefa.
- Workflow 'one-click CRM': extensão de browser GumLoop → scrape de transcript → análise + web search → extração de links sociais → outreach personalizado → Airtable → resumo semanal para o time.
- Workflow de escala de conteúdo: minerar subreddits por dores validadas → gerar ideias com OpenAI → armazenar em Sheets → produzir posts LinkedIn, roteiros YouTube e blog com Claude 3.7.
- E-commerce: rodar um SKU da Amazon por 7 agentes de IA (reviews, keywords, comportamento de busca) gerando listing completo (títulos, bullets, termos de back-end, A+ content).
- Newsletter 100% IA: Google Apps Script lê tópico/ponto de vista de uma Sheet → Perplexity para deep research → Claude para escrita → Midjourney para imagens, com humano no loop para evitar 'AI slop'.
- Arbitragem de vídeo: roteiro via ChatGPT + imagens Leonardo AI + animação via Kling AI + voz ElevenLabs para conteúdo nível Pixar enquanto os concorrentes não fazem o mesmo.
- Fórmula básica de workflow: puxar dados de fontes → transformar com IA → analisar resultados → aplicar insights à estratégia → fechar o loop com output.
- Workflows elementares para começar: data analyzer (Sheets + IA), content monitor (scrape Reddit + resumo), competitor alerts, email summarizer semanal.
- Dedique 30 minutos por dia para criar um workflow e pergunte à equipe quais tarefas repetitivas podem ser automatizadas; a maioria das plataformas tem trial gratuito.
- Visão de 12–18 meses: agentes interconectados com contexto compartilhado, geridos por manager agents treinados por especialistas humanos, com metas declaradas ('quero 50k visitantes orgânicos, descubra como') em vez de tarefas pontuais.

> **Deep dive:** `medium` — Há densidade razoável de workflows acionáveis (receitas concretas de stack n8n/Sheets/OpenRouter e scorecard de modelos), mas falta profundidade arquitetural em harness/evals/context-engineering e o episódio mistura conteúdo com promoção de produtos próprios.
