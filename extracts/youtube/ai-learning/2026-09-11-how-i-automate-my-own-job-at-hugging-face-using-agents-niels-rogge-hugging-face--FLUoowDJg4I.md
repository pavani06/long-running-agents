---
title: "How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face"
type: "extract"
source: "youtube"
video_id: "FLUoowDJg4I"
url: "https://www.youtube.com/watch?v=FLUoowDJg4I"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-i-automate-my-own-job-at-hugging-face-using-agents-niels-rogge-hugging-face--FLUoowDJg4I.txt]]"
tags: ["agents", "agent-loop", "agent-tooling", "agent-fleets", "arquitetura", "production", "observability", "tracing", "model-selection", "evals", "stack-tooling", "process"]
thesis: "Um engenheiro do Hugging Face automatizou seu trabalho de outreach científico evoluindo de um workflow determinístico noturno (cron + LLM API) para agentes autônomos (Claude Agent SDK + GLM 5.2 + Modal em lote) que abrem e respondem milhares de issues no GitHub, demonstrando que modelos abertos recentes permitem substituir milhares de linhas de pipeline por um agente mínimo com um CLI, uma skill e um sandbox."
concepts: ["workflow determinístico vs agente autônomo (LLM em loop com tools)", "descobribilidade de artefatos de pesquisa (model cards, dataset cards, metadata tags)", "paper pages do Hugging Face vinculadas ao arXiv", "cron jobs noturnos com GitHub Actions", "tracing e observabilidade de agentes", "batch processing de containers: um agent loop por issue", "CLI como ferramenta única + skill como especificação", "agentes respondendo a agentes (interação bot-a-bot)", "evitar slop via avaliação de LLMs", "substituição de modelos fechados por modelos abertos", "não divulgar identidade de bot para preservar engajamento", "autocompletar templates de model card a partir de README/paper"]
tools: ["Hugging Face Hub", "Hugging Face CLI", "Hugging Face Inference Providers", "GitHub Actions", "Langfuse", "Claude Agent SDK", "GLM 5.2", "Modal", "Cursor (Composer 2.5)", "Excalidraw MCP Server", "Slack", "Gemini", "arXiv", "DeepSeek v4", "Cursor Bench", "PostTrain Bench", "Together AI", "Fireworks", "Daily Papers (X/Twitter)", "Papers with Code", "Google Drive", "Dropbox", "Zenodo"]
people: ["Niels (Hugging Face, Community Science)", "Hugging Face", "Anthropic", "Cursor", "Langfuse", "Modal", "Hamel Husain", "Margaret Mitchell", "Apple", "Google DeepMind", "PaddleOCR", "NVIDIA", "Meta", "NeurIPS", "KU Leuven"]
claims: ["Prefira workflows determinísticos (chamadas de LLM em pipeline predefinido, sem framework) quando previsibilidade e controle importam mais que flexibilidade, seguindo o conselho da Anthropic em Building Effective Agents (2024).", "Com modelos atuais, agentes autônomos podem superar workflows: a Cursor relatou substituir cerca de 12.000 linhas de código de workflow por ~200 linhas de skill.", "GitHub Actions com tier gratuito é o melhor ponto de entrada para cron jobs: um cron noturno em Python com LLM API processa centenas de papers do arXiv por dia.", "Um agente de follow-up viável precisa apenas de um CLI como ferramenta (o HF CLI), uma skill e um sandbox — arquitetura mínima suficiente.", "O batch processing do Modal cria containers paralelos, cada um rodando um agent loop por issue do GitHub, com inicialização rápida, adequado para agentes rodando em background/overnight.", "Use Langfuse para tracing (inputs, outputs, prompts, custo, latência) a fim de observar o que o LLM de fato está fazendo em produção.", "Não revelar que o interlocutor é um bot preservou o engajamento: de milhares de issues abertas, apenas duas reações negativas foram registradas.", "Avaliação é indispensável para evitar que agentes publiquem slop; o LLM evals FAQ de Hamel Husain é a referência recomendada.", "Modelos abertos (GLM 5.2 via HF Inference Providers) já substituem modelos fechados com desempenho competitivo em benchmarks e menor custo.", "O mesmo pipeline alimenta o bot Daily Papers no X (~90 mil seguidores), com Gemini escolhendo a melhor figura para cada tweet.", "Agentes podem completar automaticamente o template de model card a partir do README e do paper, por vezes incluindo créditos não solicitados."]
deep_dive: "medium"
deep_dive_reason: "Caso real de produção com stack e decisões arquiteturais concretas (cron, tracing, frota de agentes em lote, CLI+skill), mas com viés promocional e pouca profundidade em evals, tratamento de erros ou engenharia de harness."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-your-coding-agent-should-do-ai-system-engineering-ben-burtenshaw-hugging-face--JomVvNDjGb8|Your Coding Agent Should Do AI System Engineering — Ben Burtenshaw, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-how-google-deepmind-runs-agents-at-scale-kp-sawhney-ian-ballantyne-google-deepmi--7gujZrJ9L5I|How Google DeepMind Runs Agents at Scale — KP Sawhney & Ian Ballantyne, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-2025-ai-agent-masterclass-learn-how-to-build-anything-with-llms--HkFDWwmtZ-M|2025 AI AGENT Masterclass - Learn How To Build ANYTHING With LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-uber-dev-explains-his-multi-agent-workflow--utb7zYbK10c|Ex-Uber dev explains his Multi-Agent Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-automate-complex-workflows-with-openai-o3--ydJNqND6N_Y|Automate complex workflows with OpenAI o3]]", "[[extracts/youtube/ai-learning/2026-09-11-building-ai-agents-with-claude-demo--_al9YYnF2xI|Building AI Agents with Claude! (Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-deep-research-google-docs-ai-agents-full-tutorial--yQ4F553zhQw|How to Build Deep Research Google Docs AI AGENTS - Full Tutorial]]", "[[extracts/youtube/ai-learning/2026-09-11-building-docs-for-agents-not-humans-inside-openwiki--XNX-1h2K-9U|Building Docs for Agents, Not Humans: Inside OpenWiki]]", "[[extracts/youtube/ai-learning/2026-09-11-hermes-deepseek-4-minimax-2-7-multi-model-coding-on-a-zimaboard---3MPnUGqa68|Hermes + DeepSeek 4 + MiniMax 2.7: Multi-Model Coding on a ZimaBoard]]", "[[extracts/youtube/ai-learning/2026-09-11-fine-tune-the-biggest-open-source-models-even-with-a-bad-pc--kxstlfc8Lw4|Fine-Tune the biggest open-source models (even with a bad PC)]]", "[[extracts/youtube/ai-learning/2026-09-11-introducing-openwiki-an-open-source-agent-for-repo-documentation--nIVu3zfYprI|Introducing OpenWiki, an open source agent for repo documentation]]"]
---

# How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face

## Tese
Um engenheiro do Hugging Face automatizou seu trabalho de outreach científico evoluindo de um workflow determinístico noturno (cron + LLM API) para agentes autônomos (Claude Agent SDK + GLM 5.2 + Modal em lote) que abrem e respondem milhares de issues no GitHub, demonstrando que modelos abertos recentes permitem substituir milhares de linhas de pipeline por um agente mínimo com um CLI, uma skill e um sandbox.

## Conceitos-chave
- workflow determinístico vs agente autônomo (LLM em loop com tools)
- descobribilidade de artefatos de pesquisa (model cards, dataset cards, metadata tags)
- paper pages do Hugging Face vinculadas ao arXiv
- cron jobs noturnos com GitHub Actions
- tracing e observabilidade de agentes
- batch processing de containers: um agent loop por issue
- CLI como ferramenta única + skill como especificação
- agentes respondendo a agentes (interação bot-a-bot)
- evitar slop via avaliação de LLMs
- substituição de modelos fechados por modelos abertos
- não divulgar identidade de bot para preservar engajamento
- autocompletar templates de model card a partir de README/paper

## Ferramentas & pessoas
**Ferramentas:** Hugging Face Hub, Hugging Face CLI, Hugging Face Inference Providers, GitHub Actions, Langfuse, Claude Agent SDK, GLM 5.2, Modal, Cursor (Composer 2.5), Excalidraw MCP Server, Slack, Gemini, arXiv, DeepSeek v4, Cursor Bench, PostTrain Bench, Together AI, Fireworks, Daily Papers (X/Twitter), Papers with Code, Google Drive, Dropbox, Zenodo

**Pessoas/orgs:** Niels (Hugging Face, Community Science), Hugging Face, Anthropic, Cursor, Langfuse, Modal, Hamel Husain, Margaret Mitchell, Apple, Google DeepMind, PaddleOCR, NVIDIA, Meta, NeurIPS, KU Leuven

## Claims acionáveis
- Prefira workflows determinísticos (chamadas de LLM em pipeline predefinido, sem framework) quando previsibilidade e controle importam mais que flexibilidade, seguindo o conselho da Anthropic em Building Effective Agents (2024).
- Com modelos atuais, agentes autônomos podem superar workflows: a Cursor relatou substituir cerca de 12.000 linhas de código de workflow por ~200 linhas de skill.
- GitHub Actions com tier gratuito é o melhor ponto de entrada para cron jobs: um cron noturno em Python com LLM API processa centenas de papers do arXiv por dia.
- Um agente de follow-up viável precisa apenas de um CLI como ferramenta (o HF CLI), uma skill e um sandbox — arquitetura mínima suficiente.
- O batch processing do Modal cria containers paralelos, cada um rodando um agent loop por issue do GitHub, com inicialização rápida, adequado para agentes rodando em background/overnight.
- Use Langfuse para tracing (inputs, outputs, prompts, custo, latência) a fim de observar o que o LLM de fato está fazendo em produção.
- Não revelar que o interlocutor é um bot preservou o engajamento: de milhares de issues abertas, apenas duas reações negativas foram registradas.
- Avaliação é indispensável para evitar que agentes publiquem slop; o LLM evals FAQ de Hamel Husain é a referência recomendada.
- Modelos abertos (GLM 5.2 via HF Inference Providers) já substituem modelos fechados com desempenho competitivo em benchmarks e menor custo.
- O mesmo pipeline alimenta o bot Daily Papers no X (~90 mil seguidores), com Gemini escolhendo a melhor figura para cada tweet.
- Agentes podem completar automaticamente o template de model card a partir do README e do paper, por vezes incluindo créditos não solicitados.

> **Deep dive:** `medium` — Caso real de produção com stack e decisões arquiteturais concretas (cron, tracing, frota de agentes em lote, CLI+skill), mas com viés promocional e pouca profundidade em evals, tratamento de erros ou engenharia de harness.
