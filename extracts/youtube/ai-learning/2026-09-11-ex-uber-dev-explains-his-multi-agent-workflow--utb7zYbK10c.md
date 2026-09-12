---
title: "Ex-Uber dev explains his Multi-Agent Workflow"
type: "extract"
source: "youtube"
video_id: "utb7zYbK10c"
url: "https://www.youtube.com/watch?v=utb7zYbK10c"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-ex-uber-dev-explains-his-multi-agent-workflow--utb7zYbK10c.txt]]"
tags: ["agents", "agent-fleets", "multi-agent", "context-engineering", "context-management", "memory-architecture", "knowledge-management", "agent-tooling", "stack-tooling", "process"]
thesis: "A próxima onda de IA é o agente 'multiplayer': um teammate incorporado aos canais de colaboração da empresa (Slack, e-mail, docs) com contexto compartilhado autoconstruído, onde o contexto importa mais do que a inteligência bruta do modelo."
concepts: ["Transição de IA single-player para multiplayer (analogia e-mail vs Google Docs)", "Agente de IA como teammate pleno (conta de Slack, endereço de e-mail, acesso a docs)", "Contexto compartilhado como fundamento da experiência multiplayer", "Self-building wiki / 'automatic hydration' da memória da empresa", "Team file system, team memory, team skills e integracoes compartilhadas", "Contexto supera inteligência (analogia do von Neumann sem contexto)", "Base context de ~100k tokens por consulta", "Agentes que constroem suas próprias integrações (scripts, API keys, secrets manager)", "Erosão do fosso de integrações (Zapier/n8n) frente a agentes autônomos", "Vantagem first-mover via dados de treino dos próximos modelos", "Caos embrionário e seleção natural de workflows na adoção interna", "Trabalhar 'no' sistema, não 'no' sistema (Ray Dalio, Principles)", "Loop de software auto-melhorável (agente de código + agente de user research)", "Morte da web UI e agentes como 99% do uso de software", "Zero-setup como requisito de produto", "Cenários de AGI: 'morte ou gato doméstico'"]
tools: ["Lindy / Lindy Teammate", "Claude Code", "Codex", "Cursor", "Deep API (deepi.co)", "Slack", "Google Docs", "GitHub", "Google Calendar", "ElevenLabs", "Zapier", "Make.com", "n8n", "DoorDash CLI", "WhisperFlow", "OpenClaw", "iMessage/Discord/WhatsApp", "Lotus Notes", "Perplexity", "Claude Opus", "GPT-5.6 Pro", "Fable 5"]
people: ["Flo (CEO da Lindy)", "David (host)", "Jeremy", "Ali", "Ray Dalio", "Ray Kurzweil", "Zach Hoggatt", "Lindy", "Listen Labs", "IBM", "Anthropic", "OpenAI"]
claims: ["Dê ao agente a mesma superfície de colaboração de um humano: conta no Slack, endereço de e-mail e permissão de edição em documentos, @mencionável no contexto da conversa", "Substitua wikis estáticas por hidratação automática: um agente que ingere continuamente Slack, reuniões e e-mails em um master memory file e grafo de conhecimento da empresa", "Alimente consultas com base contexts grandes (~100k tokens): modelo de fronteira + contexto completo da empresa gera insights que um gênio sem contexto não produz", "Priorize contexto sobre inteligência ao desenhar teammates de IA; um coworker medíocre com contexto total supera um gênio sem contexto", "Permita que agentes construam integrações ausentes por conta própria (escrever script, solicitar API key, guardar em secrets manager) em vez de manter bibliotecas de conectores", "Construa o scaffold multiplayer — file system, memória, skills e integrações de time compartilhados — para que novos membros (humanos ou agentes) tenham setup zero", "Grave reuniões com notetakers e converta automaticamente em markdown estruturado enviado a um GitHub repo compartilhado, gerando material de treinamento para humanos e agentes", "Líderes devem passar 20+ horas/semana hands-on com IA, reservar dias sem reunião (ex.: quartas-feiras) para experimentar e recompensar publicamente workflows de IA no Slack para catalisar adoção", "Use agentes para rotinas recorrentes: daily brief, triagem e rascunho de e-mails, preparação de reuniões, recrutamento via autores de bons blog posts e interceptação de signups valiosos para outreach rápido", "Mova-se cedo porque o first mover é assado nos dados de treino da próxima geração de modelos e vira default", "Seu trabalho é trabalhar 'no' sistema, não 'no' sistema: configurar e otimizar a máquina de agentes, não operá-la", "Abra mão de padronização no início: deixe caos de workflows por engenheiro (ex.: PR review agents individuais) e padronize apenas quando padrões emergirem", "Dê ao agente acesso ao calendário/time-tracking para destilar centenas de eventos em insights de produtividade e delegação que nenhum humano computaria manualmente"]
deep_dive: "medium"
deep_dive_reason: "Conversa de podcast com trechos promocionais (Deep API, Lindy) que entrega algumas ideias arquiteturais acionáveis e relativamente novas (hidratação automática de contexto compartilhado, agentes como teammates com e-mail/Slack, integrações autoconstruídas), mas sem profundidade técnica em harness, evals ou implementação."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-working-with-ai-not-just-using-it-brendan-o-leary--BEKc4P87XKo|Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary]]", "[[extracts/youtube/ai-learning/2026-09-11-the-future-of-ai-agents-with-andrew-ng-interrupt-26--OaRhpwz_TGM|The Future of AI Agents with Andrew Ng | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-creating-agents-that-co-create-karina-nguyen-openai--1XvN5EBDnDw|Creating Agents that Co-Create — Karina Nguyen, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-ai-how-bots-came-for-our-workflows-and-drudgery-ft-working-it--e85AxYW0Qyk|Agentic AI - how bots came for our workflows and drudgery | FT Working It]]", "[[extracts/youtube/ai-learning/2026-09-11-could-a-swarm-of-autonomous-ai-agents-be-the-ultimate-business-asset-stage-1--UL55C80TEb8|Could a Swarm of Autonomous AI Agents be the Ultimate Business Asset? - Stage 1]]", "[[extracts/youtube/ai-learning/2026-09-11-satya-nadella-on-ai-agents-rebuilding-the-web-the-future-of-work-and-more--_a8EnBX8DSU|Satya Nadella on AI Agents, Rebuilding the Web, the Future of Work, and more]]", "[[extracts/youtube/ai-learning/2026-09-11-research-agent-3-0-build-a-group-of-ai-researchers-here-is-how--AVInhYBUnKs|\"Research agent 3.0 - Build a group of AI researchers\" - Here is how]]", "[[extracts/youtube/ai-learning/2026-09-11-build-ai-agent-workforce-multi-agent-framework-with-metagpt-chatdev--pJwR5pv0_gs|Build AI agent workforce - Multi agent framework with MetaGPT & chatDev]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-automate-my-own-job-at-hugging-face-using-agents-niels-rogge-hugging-face--FLUoowDJg4I|How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-the-weird-future-of-user-interfaces--f32W5BEzWN0|The Weird Future Of User Interfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-build-an-obsidian-system-not-a-second-brain--OZ3ZNhrPbF4|Build an Obsidian SYSTEM Not a Second Brain!]]"]
theme: "Orquestração Multiagente em Escala"
---

# Ex-Uber dev explains his Multi-Agent Workflow

## Tese
A próxima onda de IA é o agente 'multiplayer': um teammate incorporado aos canais de colaboração da empresa (Slack, e-mail, docs) com contexto compartilhado autoconstruído, onde o contexto importa mais do que a inteligência bruta do modelo.

## Conceitos-chave
- Transição de IA single-player para multiplayer (analogia e-mail vs Google Docs)
- Agente de IA como teammate pleno (conta de Slack, endereço de e-mail, acesso a docs)
- Contexto compartilhado como fundamento da experiência multiplayer
- Self-building wiki / 'automatic hydration' da memória da empresa
- Team file system, team memory, team skills e integracoes compartilhadas
- Contexto supera inteligência (analogia do von Neumann sem contexto)
- Base context de ~100k tokens por consulta
- Agentes que constroem suas próprias integrações (scripts, API keys, secrets manager)
- Erosão do fosso de integrações (Zapier/n8n) frente a agentes autônomos
- Vantagem first-mover via dados de treino dos próximos modelos
- Caos embrionário e seleção natural de workflows na adoção interna
- Trabalhar 'no' sistema, não 'no' sistema (Ray Dalio, Principles)
- Loop de software auto-melhorável (agente de código + agente de user research)
- Morte da web UI e agentes como 99% do uso de software
- Zero-setup como requisito de produto
- Cenários de AGI: 'morte ou gato doméstico'

## Ferramentas & pessoas
**Ferramentas:** Lindy / Lindy Teammate, Claude Code, Codex, Cursor, Deep API (deepi.co), Slack, Google Docs, GitHub, Google Calendar, ElevenLabs, Zapier, Make.com, n8n, DoorDash CLI, WhisperFlow, OpenClaw, iMessage/Discord/WhatsApp, Lotus Notes, Perplexity, Claude Opus, GPT-5.6 Pro, Fable 5

**Pessoas/orgs:** Flo (CEO da Lindy), David (host), Jeremy, Ali, Ray Dalio, Ray Kurzweil, Zach Hoggatt, Lindy, Listen Labs, IBM, Anthropic, OpenAI

## Claims acionáveis
- Dê ao agente a mesma superfície de colaboração de um humano: conta no Slack, endereço de e-mail e permissão de edição em documentos, @mencionável no contexto da conversa
- Substitua wikis estáticas por hidratação automática: um agente que ingere continuamente Slack, reuniões e e-mails em um master memory file e grafo de conhecimento da empresa
- Alimente consultas com base contexts grandes (~100k tokens): modelo de fronteira + contexto completo da empresa gera insights que um gênio sem contexto não produz
- Priorize contexto sobre inteligência ao desenhar teammates de IA; um coworker medíocre com contexto total supera um gênio sem contexto
- Permita que agentes construam integrações ausentes por conta própria (escrever script, solicitar API key, guardar em secrets manager) em vez de manter bibliotecas de conectores
- Construa o scaffold multiplayer — file system, memória, skills e integrações de time compartilhados — para que novos membros (humanos ou agentes) tenham setup zero
- Grave reuniões com notetakers e converta automaticamente em markdown estruturado enviado a um GitHub repo compartilhado, gerando material de treinamento para humanos e agentes
- Líderes devem passar 20+ horas/semana hands-on com IA, reservar dias sem reunião (ex.: quartas-feiras) para experimentar e recompensar publicamente workflows de IA no Slack para catalisar adoção
- Use agentes para rotinas recorrentes: daily brief, triagem e rascunho de e-mails, preparação de reuniões, recrutamento via autores de bons blog posts e interceptação de signups valiosos para outreach rápido
- Mova-se cedo porque o first mover é assado nos dados de treino da próxima geração de modelos e vira default
- Seu trabalho é trabalhar 'no' sistema, não 'no' sistema: configurar e otimizar a máquina de agentes, não operá-la
- Abra mão de padronização no início: deixe caos de workflows por engenheiro (ex.: PR review agents individuais) e padronize apenas quando padrões emergirem
- Dê ao agente acesso ao calendário/time-tracking para destilar centenas de eventos em insights de produtividade e delegação que nenhum humano computaria manualmente

> **Deep dive:** `medium` — Conversa de podcast com trechos promocionais (Deep API, Lindy) que entrega algumas ideias arquiteturais acionáveis e relativamente novas (hidratação automática de contexto compartilhado, agentes como teammates com e-mail/Slack, integrações autoconstruídas), mas sem profundidade técnica em harness, evals ou implementação.
