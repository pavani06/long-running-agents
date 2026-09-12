---
title: "How To Use AI to Write Viral Reel Scripts - Claude Projects Tutorial"
type: "extract"
source: "youtube"
video_id: "uc1lUchiaJ0"
url: "https://www.youtube.com/watch?v=uc1lUchiaJ0"
channel: "100x Engineers"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-use-ai-to-write-viral-reel-scripts-claude-projects-tutorial--uc1lUchiaJ0.txt]]"
tags: ["context-engineering", "knowledge-management", "curriculo-conteudo", "process", "production", "stack-tooling", "model-selection"]
thesis: "Um criador de conteúdo usa o recurso Claude Projects alimentado com um corpus de 300-400 scripts próprios como contexto para automatizar a escrita de roteiros de Instagram Reels, argumentando que expertise de domínio humana continua sendo o pré-requisito para instruir bem modelos de linguagem."
concepts: ["Claude Projects como LLM especializado por tarefa com grande capacidade de contexto", "Upload de corpus próprio (300-400 scripts) como conhecimento de estilo no projeto", "Custom instructions persistentes definindo papel, estrutura e tonalidade", "Estrutura de script hook-body-call-to-action", "Transferência de estilo via exemplos few-shot no knowledge base", "Human-in-the-loop: edição de 10-30% do output para inserir opiniões genuínas", "Limitação do modelo em simular insights derivados de memória/experiência de anos", "Correlação entre tamanho da context window e capacidade de gerar insights comparativos", "Domain expertise como pré-condição para prompt engineering efetivo", "Non-transferibilidade de corpora específicos de estilo entre domínios"]
tools: ["Claude (Anthropic)", "Claude Projects", "Claude Pro Plan (US$ 20/mês)", "Instagram Reels", "Microsoft Omniparser", "Anthropic Computer Use", "GPT-4V (OpenAI Vision)", "Hugging Face (MIT license)", "GitHub (repo self-operating computer)"]
people: ["Shev (apresentador)", "100x Engineers / AI Lab", "Anthropic", "Microsoft", "OpenAI"]
claims: ["Um roteiro escrito pelo Claude alcançou 1,7 milhão de views no Instagram", "Enviar 300-400 scripts consumiu apenas ~16% da capacidade de knowledge do Claude Projects", "O Claude Projects comporta contexto equivalente a um livro de ~500 páginas, revisado a cada geração", "70-90% dos roteiros publicados são gerados por IA e revisados por humanos para autenticidade", "O modelo não gerou comparações históricas (ex: self-operating computer) porque esse contexto não foi fornecido — o output só é tão bom quanto o contexto e a instrução", "Com context windows maiores, essa limitação de insight é temporária e deve diminuir nos próximos anos", "Scripts de instrução detalhada em custom instructions permitem prompts de execução curtos e simples", "Corpora de estilo são específicos por página/domínio e não servem como template genérico para terceiros"]
deep_dive: "low"
deep_dive_reason: "Tutorial introdutório de uso consumer do Claude Projects para geração de conteúdo, com dicas práticas úteis mas sem profundidade arquitetural, evals, harness, governança ou novidade técnica relevante."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-to-instantly-build-ai-agents-in-n8n-using-claude--uAtSMEBosGU|How to INSTANTLY Build AI Agents in N8N Using Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-instantly-generate-n8n-workflows-using-claude--9tj4MxCV6g0|How to INSTANTLY Generate N8N Workflows Using Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-building-ai-agents-with-claude-demo--_al9YYnF2xI|Building AI Agents with Claude! (Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-mastering-claude-code-in-30-minutes--6eBSHbLKuN0|Mastering Claude Code in 30 minutes]]"]
theme: "Codificação Agêntica com Claude Code"
---

# How To Use AI to Write Viral Reel Scripts - Claude Projects Tutorial

## Tese
Um criador de conteúdo usa o recurso Claude Projects alimentado com um corpus de 300-400 scripts próprios como contexto para automatizar a escrita de roteiros de Instagram Reels, argumentando que expertise de domínio humana continua sendo o pré-requisito para instruir bem modelos de linguagem.

## Conceitos-chave
- Claude Projects como LLM especializado por tarefa com grande capacidade de contexto
- Upload de corpus próprio (300-400 scripts) como conhecimento de estilo no projeto
- Custom instructions persistentes definindo papel, estrutura e tonalidade
- Estrutura de script hook-body-call-to-action
- Transferência de estilo via exemplos few-shot no knowledge base
- Human-in-the-loop: edição de 10-30% do output para inserir opiniões genuínas
- Limitação do modelo em simular insights derivados de memória/experiência de anos
- Correlação entre tamanho da context window e capacidade de gerar insights comparativos
- Domain expertise como pré-condição para prompt engineering efetivo
- Non-transferibilidade de corpora específicos de estilo entre domínios

## Ferramentas & pessoas
**Ferramentas:** Claude (Anthropic), Claude Projects, Claude Pro Plan (US$ 20/mês), Instagram Reels, Microsoft Omniparser, Anthropic Computer Use, GPT-4V (OpenAI Vision), Hugging Face (MIT license), GitHub (repo self-operating computer)

**Pessoas/orgs:** Shev (apresentador), 100x Engineers / AI Lab, Anthropic, Microsoft, OpenAI

## Claims acionáveis
- Um roteiro escrito pelo Claude alcançou 1,7 milhão de views no Instagram
- Enviar 300-400 scripts consumiu apenas ~16% da capacidade de knowledge do Claude Projects
- O Claude Projects comporta contexto equivalente a um livro de ~500 páginas, revisado a cada geração
- 70-90% dos roteiros publicados são gerados por IA e revisados por humanos para autenticidade
- O modelo não gerou comparações históricas (ex: self-operating computer) porque esse contexto não foi fornecido — o output só é tão bom quanto o contexto e a instrução
- Com context windows maiores, essa limitação de insight é temporária e deve diminuir nos próximos anos
- Scripts de instrução detalhada em custom instructions permitem prompts de execução curtos e simples
- Corpora de estilo são específicos por página/domínio e não servem como template genérico para terceiros

> **Deep dive:** `low` — Tutorial introdutório de uso consumer do Claude Projects para geração de conteúdo, com dicas práticas úteis mas sem profundidade arquitetural, evals, harness, governança ou novidade técnica relevante.
