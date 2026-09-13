---
title: "Automate complex workflows with OpenAI o3"
type: "extract"
source: "youtube"
video_id: "ydJNqND6N_Y"
url: "https://www.youtube.com/watch?v=ydJNqND6N_Y"
channel: "OpenAI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-automate-complex-workflows-with-openai-o3--ydJNqND6N_Y.txt]]"
tags: ["agent-loop", "agent-tooling", "agents", "analise", "process"]
thesis: "A demonstração argumenta que o modelo o3 da OpenAI combina raciocínio multi-etapa com uso agêntico de múltiplas ferramentas (análise de CSV em Python, busca web, visualização, geração de resumo executivo) para automatizar em ~1 minuto um fluxo de relatório de variação orçamentária que levaria horas."
concepts: ["raciocínio multi-etapas", "uso agêntico de ferramentas", "chain-of-thought visível resumindo ações", "análise de variação orçamentária (threshold de 7%)", "harmonização de dados de planilhas departamentais", "busca web por benchmarks com fontes citáveis", "visualizações interativas com checkpoints", "resumo executivo e post para Slack", "orquestração automática de tarefas discretas em sequência"]
tools: ["OpenAI o3", "ChatGPT", "Python", "busca web do ChatGPT", "Slack", "planilhas CSV"]
people: ["OpenAI", "KPMG", "CFO (papel citado)"]
claims: ["o3 executa cada etapa de um processo manual multi-tarefa chamando diferentes ferramentas conforme avança (analisar CSVs, escrever e rodar código Python, buscar na web, visualizar, redigir)", "na demo, 20 de 25 linhas foram sinalizadas por exceder variação de 7% entre orçado e realizado", "o fluxo completo (harmonização, análise, benchmarks citáveis, visuais interativos, resumo executivo e post de Slack) foi concluído em cerca de um minuto versus horas de trabalho manual", "o chain-of-thought é exibido ao vivo resumindo as ações do agente, permitindo acompanhar a execução passo a passo", "as visualizações geradas incluem takeaways, instruções de leitura e checkpoints para validar os resultados esperados"]
deep_dive: "low"
deep_dive_reason: "Trata-se de uma demo promocional de produto descrevendo um fluxo genérico de automação, sem densidade de insight arquitetural, harness, evals, governança ou novidade técnica além do marketing."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-to-build-your-entire-ai-workforce-in-one-afternoon-live-demo--oulVKbk0umo|How to Build Your Entire AI Workforce in One Afternoon (Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-automate-my-own-job-at-hugging-face-using-agents-niels-rogge-hugging-face--FLUoowDJg4I|How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-from-zero-to-your-first-ai-agent-in-25-minutes-no-coding--EH5jx5qPabU|From Zero to Your First AI Agent in 25 Minutes (No Coding)]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-gpt4v-puppeteer-ai-agent-browse-web-like-human--IXRkmqEYGZA|GPT4V + Puppeteer = AI agent browse web like human? 🤖]]"]
theme: "Agentes de IA No-Code"
---

# Automate complex workflows with OpenAI o3

## Tese
A demonstração argumenta que o modelo o3 da OpenAI combina raciocínio multi-etapa com uso agêntico de múltiplas ferramentas (análise de CSV em Python, busca web, visualização, geração de resumo executivo) para automatizar em ~1 minuto um fluxo de relatório de variação orçamentária que levaria horas.

## Conceitos-chave
- raciocínio multi-etapas
- uso agêntico de ferramentas
- chain-of-thought visível resumindo ações
- análise de variação orçamentária (threshold de 7%)
- harmonização de dados de planilhas departamentais
- busca web por benchmarks com fontes citáveis
- visualizações interativas com checkpoints
- resumo executivo e post para Slack
- orquestração automática de tarefas discretas em sequência

## Ferramentas & pessoas
**Ferramentas:** OpenAI o3, ChatGPT, Python, busca web do ChatGPT, Slack, planilhas CSV

**Pessoas/orgs:** OpenAI, KPMG, CFO (papel citado)

## Claims acionáveis
- o3 executa cada etapa de um processo manual multi-tarefa chamando diferentes ferramentas conforme avança (analisar CSVs, escrever e rodar código Python, buscar na web, visualizar, redigir)
- na demo, 20 de 25 linhas foram sinalizadas por exceder variação de 7% entre orçado e realizado
- o fluxo completo (harmonização, análise, benchmarks citáveis, visuais interativos, resumo executivo e post de Slack) foi concluído em cerca de um minuto versus horas de trabalho manual
- o chain-of-thought é exibido ao vivo resumindo as ações do agente, permitindo acompanhar a execução passo a passo
- as visualizações geradas incluem takeaways, instruções de leitura e checkpoints para validar os resultados esperados

> **Deep dive:** `low` — Trata-se de uma demo promocional de produto descrevendo um fluxo genérico de automação, sem densidade de insight arquitetural, harness, evals, governança ou novidade técnica além do marketing.
