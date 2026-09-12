---
title: "The Easiest Way to Use Community Nodes in n8n"
type: "extract"
source: "youtube"
video_id: "WI8ikp5YyRw"
url: "https://www.youtube.com/watch?v=WI8ikp5YyRw"
channel: "Nate Herk | AI Automation"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-easiest-way-to-use-community-nodes-in-n8n--WI8ikp5YyRw.txt]]"
tags: ["agent-tooling", "stack-tooling", "process", "verification"]
thesis: "n8n liberou a instalação de nodes de comunidade diretamente no n8n Cloud (versão 1.94+), substituindo chamadas HTTP manuais por nodes nativos verificados, com fluxos distintos de instalação para cloud, self-hosted e ambientes locais."
concepts: ["nodes de comunidade", "nodes verificados", "requisição HTTP manual vs node nativo", "gestão de credenciais/API keys", "ferramentas para agentes de IA", "triggers em nodes de comunidade", "instalação via npm", "self-hosting vs cloud vs hospedagem local", "ecossistema de pacotes mantidos pela comunidade"]
tools: ["n8n", "Tavily", "ElevenLabs", "Browserflow", "SerpAPI", "PDF.co", "Chat Data", "Swift Gum", "npm", "Docker", "GitHub"]
people: ["n8n", "Tavily", "ElevenLabs"]
claims: ["É necessário rodar n8n versão 1.94 ou posterior para usar community nodes no cloud", "Ative a opção 'verify community nodes' no admin panel e salve (isso reinicia o workspace, então salve seus workflows antes)", "No cloud e self-hosted é possível instalar pacotes de community nodes direto do painel de settings, buscando por nome ou navegando a lista", "Community nodes abstraem a autenticação: basta colar a API key sem lidar com prefixos como 'bearer' ou headers manuais", "Community nodes podem ser usados como ferramentas anexadas a AI agents e alguns suportam triggers (ex.: Swift Gum, Chat Data)", "Na instalação local é preciso acessar o docker shell, criar/navegar até o diretório de nodes do n8n, rodar o npm install do pacote e reiniciar o n8n", "Existe um repositório GitHub catalogando o top 100 community nodes por categorias (comunicação, automação de browser, processamento de dados, integrações de API)", "O catálogo inicial no cloud tem 25 nodes verificados e será expandido gradualmente"]
deep_dive: "low"
deep_dive_reason: "É um tutorial procedural de produto (instalação de nodes no n8n) com passos práticos mas sem densidade de insight arquitetural, novidade ou relevância para harness, evals ou governança de agentes."
---

# The Easiest Way to Use Community Nodes in n8n

## Tese
n8n liberou a instalação de nodes de comunidade diretamente no n8n Cloud (versão 1.94+), substituindo chamadas HTTP manuais por nodes nativos verificados, com fluxos distintos de instalação para cloud, self-hosted e ambientes locais.

## Conceitos-chave
- nodes de comunidade
- nodes verificados
- requisição HTTP manual vs node nativo
- gestão de credenciais/API keys
- ferramentas para agentes de IA
- triggers em nodes de comunidade
- instalação via npm
- self-hosting vs cloud vs hospedagem local
- ecossistema de pacotes mantidos pela comunidade

## Ferramentas & pessoas
**Ferramentas:** n8n, Tavily, ElevenLabs, Browserflow, SerpAPI, PDF.co, Chat Data, Swift Gum, npm, Docker, GitHub

**Pessoas/orgs:** n8n, Tavily, ElevenLabs

## Claims acionáveis
- É necessário rodar n8n versão 1.94 ou posterior para usar community nodes no cloud
- Ative a opção 'verify community nodes' no admin panel e salve (isso reinicia o workspace, então salve seus workflows antes)
- No cloud e self-hosted é possível instalar pacotes de community nodes direto do painel de settings, buscando por nome ou navegando a lista
- Community nodes abstraem a autenticação: basta colar a API key sem lidar com prefixos como 'bearer' ou headers manuais
- Community nodes podem ser usados como ferramentas anexadas a AI agents e alguns suportam triggers (ex.: Swift Gum, Chat Data)
- Na instalação local é preciso acessar o docker shell, criar/navegar até o diretório de nodes do n8n, rodar o npm install do pacote e reiniciar o n8n
- Existe um repositório GitHub catalogando o top 100 community nodes por categorias (comunicação, automação de browser, processamento de dados, integrações de API)
- O catálogo inicial no cloud tem 25 nodes verificados e será expandido gradualmente

> **Deep dive:** `low` — É um tutorial procedural de produto (instalação de nodes no n8n) com passos práticos mas sem densidade de insight arquitetural, novidade ou relevância para harness, evals ou governança de agentes.
