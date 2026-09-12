---
title: "GPT4V + Puppeteer = AI agent browse web like human? 🤖"
type: "extract"
source: "youtube"
video_id: "IXRkmqEYGZA"
url: "https://www.youtube.com/watch?v=IXRkmqEYGZA"
channel: "AI Jason"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-gpt4v-puppeteer-ai-agent-browse-web-like-human--IXRkmqEYGZA.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "arquitetura", "context-engineering", "runtime", "stack-tooling", "error-handling", "analise"]
thesis: "Agentes de IA multimodais como GPT-4V com controle direto do navegador/computador, operando por loop de screenshot + anotação de elementos interativos, podem superar as limitações do RPA tradicional em tarefas não padronizadas com custo de setup muito menor, conforme demonstrado num tutorial passo a passo com Puppeteer."
concepts: ["self-operating computer", "web AI agent", "automação robótica de processos (RPA)", "controle de computador via screenshot + anotação", "abordagem baseada em DOM vs abordagem multimodal", "bounding box / grade percentual como anotação para clicar", "highlight de links com atributo DOM customizado (gpt link text)", "loop de agente: screenshot -> decisão do modelo -> ação (click/URL/resposta)", "reuso de perfil e cookies do Chrome (Chrome Canary) para acessar sites logados como LinkedIn/Instagram", "detecção de scraping evitada com plugin stealth", "match parcial/exato de texto de link para selecionar elemento clicável", "fatores de mercado: RPA frágil a mudanças de layout, agentes adaptáveis por tomarem decisões próprias"]
tools: ["GPT-4V", "GPT-4", "GPT-3.5", "OpenAI API", "Puppeteer", "puppeteer-extra (stealth plugin)", "Selenium", "Playwright", "pyautogui", "self-operating computer framework (open source)", "Chrome Canary", "Google Chrome", "Node.js", "npm", "Python", "Visual Studio Code"]
people: ["HyperWrite (self-operating computer)", "MultiOn", "UiPath", "OpenAI", "HubSpot", "Unconventional Coding", "Nike", "Adidas", "Puma"]
claims: ["Enviar o DOM inteiro ao LLM (estilo taxi/GPT-4) gera muito ruído, é lento, caro e impreciso; screenshot com anotação via GPT-4V é abordagem mais viável", "Anotação em grade percentual para desktop falha com frequência porque o GPT-4V estima mal as coordenadas; restringir ao navegador e desenhar bounding boxes via CSS dá precisão muito maior", "Copiar a pasta 'Default' do perfil do Chrome para o Chrome Canary e apontar o user data directory do Puppeteer permite que o agente acesse sites que bloqueiam scraping (LinkedIn, Instagram, serviços pagos)", "RPA tradicional exige processo específico por site, quebra quando o layout muda e só se justifica em alto volume padronizado (>US$3bi/ano gasto enterprise em 2022); agentes multimodais reduzem custo de setup e adaptam-se a mudanças de formato", "Padronizar a saída do modelo em dois formatos JSON (CLICK <texto do link> ou URL <url>) e casar com atributo DOM 'gpt link text' (match parcial ou exato) torna o clique do agente confiável", "O sistema prompt do agente deve instruir: ler o screenshot sem inventar nomes de links, usar os links destacados em vermelho, ir direto a URL inicial via Google quando possível, e responder em texto normal ao encontrar a resposta", "O demo navega múltiplos sites (ex.: Google -> Instagram -> site oficial) para responder tarefas complexas, mas ainda falta manipulação de formulários e cliques falham com frequência — pontos de melhoria claros", "Entregar 'trabalhadores digitais' úteis exige entender o workflow ponta a ponta da função (ex.: relatório da HubSpot com 1.400+ líderes de vendas), não só a tecnologia"]
deep_dive: "medium"
deep_dive_reason: "Há densidade prática acionável (tradeoffs DOM vs screenshot, truque do perfil Chrome Canary, loop click/URL com highlight de links), mas a arquitetura é rasa (agente único, sem evals, memória ou governança) e inclui trecho promocional do patrocinador."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-finally-this-ai-agent-actually-works--XeWZIzndlY4|FINALLY, this AI agent actually works!]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-rip-to-rpa-how-ai-makes-operations-work--O6DtzLGLNWY|RIP to RPA: How AI Makes Operations Work]]", "[[extracts/youtube/ai-learning/2026-09-11-could-a-swarm-of-autonomous-ai-agents-be-the-ultimate-business-asset-stage-1--UL55C80TEb8|Could a Swarm of Autonomous AI Agents be the Ultimate Business Asset? - Stage 1]]", "[[extracts/youtube/ai-learning/2026-09-11-top-4-must-have-ai-agents-for-beginners-easy-setup-guide--4keUCOVpsxQ|Top 4 Must-Have AI Agents for Beginners – Easy Setup Guide]]", "[[extracts/youtube/ai-learning/2026-09-11-automate-complex-workflows-with-openai-o3--ydJNqND6N_Y|Automate complex workflows with OpenAI o3]]", "[[extracts/youtube/ai-learning/2026-09-11-automatize-todo-o-seu-trabalho-com-a-ia-project-mariner-do-google-incrivel--E0Jbaikf0o4|AUTOMATIZE TODO O SEU TRABALHO com a IA “Project Mariner” do GOOGLE - INCRÍVEL!]]"]
---

# GPT4V + Puppeteer = AI agent browse web like human? 🤖

## Tese
Agentes de IA multimodais como GPT-4V com controle direto do navegador/computador, operando por loop de screenshot + anotação de elementos interativos, podem superar as limitações do RPA tradicional em tarefas não padronizadas com custo de setup muito menor, conforme demonstrado num tutorial passo a passo com Puppeteer.

## Conceitos-chave
- self-operating computer
- web AI agent
- automação robótica de processos (RPA)
- controle de computador via screenshot + anotação
- abordagem baseada em DOM vs abordagem multimodal
- bounding box / grade percentual como anotação para clicar
- highlight de links com atributo DOM customizado (gpt link text)
- loop de agente: screenshot -> decisão do modelo -> ação (click/URL/resposta)
- reuso de perfil e cookies do Chrome (Chrome Canary) para acessar sites logados como LinkedIn/Instagram
- detecção de scraping evitada com plugin stealth
- match parcial/exato de texto de link para selecionar elemento clicável
- fatores de mercado: RPA frágil a mudanças de layout, agentes adaptáveis por tomarem decisões próprias

## Ferramentas & pessoas
**Ferramentas:** GPT-4V, GPT-4, GPT-3.5, OpenAI API, Puppeteer, puppeteer-extra (stealth plugin), Selenium, Playwright, pyautogui, self-operating computer framework (open source), Chrome Canary, Google Chrome, Node.js, npm, Python, Visual Studio Code

**Pessoas/orgs:** HyperWrite (self-operating computer), MultiOn, UiPath, OpenAI, HubSpot, Unconventional Coding, Nike, Adidas, Puma

## Claims acionáveis
- Enviar o DOM inteiro ao LLM (estilo taxi/GPT-4) gera muito ruído, é lento, caro e impreciso; screenshot com anotação via GPT-4V é abordagem mais viável
- Anotação em grade percentual para desktop falha com frequência porque o GPT-4V estima mal as coordenadas; restringir ao navegador e desenhar bounding boxes via CSS dá precisão muito maior
- Copiar a pasta 'Default' do perfil do Chrome para o Chrome Canary e apontar o user data directory do Puppeteer permite que o agente acesse sites que bloqueiam scraping (LinkedIn, Instagram, serviços pagos)
- RPA tradicional exige processo específico por site, quebra quando o layout muda e só se justifica em alto volume padronizado (>US$3bi/ano gasto enterprise em 2022); agentes multimodais reduzem custo de setup e adaptam-se a mudanças de formato
- Padronizar a saída do modelo em dois formatos JSON (CLICK <texto do link> ou URL <url>) e casar com atributo DOM 'gpt link text' (match parcial ou exato) torna o clique do agente confiável
- O sistema prompt do agente deve instruir: ler o screenshot sem inventar nomes de links, usar os links destacados em vermelho, ir direto a URL inicial via Google quando possível, e responder em texto normal ao encontrar a resposta
- O demo navega múltiplos sites (ex.: Google -> Instagram -> site oficial) para responder tarefas complexas, mas ainda falta manipulação de formulários e cliques falham com frequência — pontos de melhoria claros
- Entregar 'trabalhadores digitais' úteis exige entender o workflow ponta a ponta da função (ex.: relatório da HubSpot com 1.400+ líderes de vendas), não só a tecnologia

> **Deep dive:** `medium` — Há densidade prática acionável (tradeoffs DOM vs screenshot, truque do perfil Chrome Canary, loop click/URL com highlight de links), mas a arquitetura é rasa (agente único, sem evals, memória ou governança) e inclui trecho promocional do patrocinador.
