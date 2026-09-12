---
title: "Hermes Co-Founder on Building an AI Agent That Improves Itself | Karan Malhotra"
type: "extract"
source: "youtube"
video_id: "UWjh5Z4s8jY"
url: "https://www.youtube.com/watch?v=UWjh5Z4s8jY"
channel: "Peter Yang"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-hermes-co-founder-on-building-an-ai-agent-that-improves-itself-karan-malhotra--UWjh5Z4s8jY.txt]]"
tags: ["harness", "harness-engineering", "context-engineering", "context-management", "memory-architecture", "agents", "agent-tooling", "multi-agent", "model-selection", "governanca", "instituicoes", "frameworks", "knowledge-management", "investimentos"]
thesis: "O Hermes Agent da Nous Research é um harness open-source agnóstico de modelo cujo sistema de auto-melhoria (memórias, skills e um 'curator' em cron) e prompts deliberadamente alinhados ao usuário individual tornam qualquer modelo mais capaz e 'leal' à pessoa do que em seu harness nativo (Claude Code, Codex)."
concepts: ["reward hacking", "siscofrência (sycophancy)", "alinhamento ao usuário individual", "self-improvement loop", "in-context learning (ICL)", "reinforcement learning em tempo de teste", "gestão de contexto como núcleo do harness", "memórias e skills como contexto comprimido", "curator loop contra 'slop'", "harness vs. modelo subjacente", "simulação de lealdade gerando capacidade", "crítica adversarial com agente sem contexto", "proatividade emergente do agente", "orquestração kanban humano-agente", "agnosticidade de modelo e custo zero de troca", "ambientes de RL (Atropos)", "jailbreakabilidade de modelos", "captura regulatória vs. open source", "subsídio de tokens e sustentabilidade"]
tools: ["Hermes Agent", "Hermes Curator", "Forge", "Atropos", "YaRN", "World Sim", "Nous Portal", "Tool Gateway", "DRO optimizer", "GPT4-x-Alpaca", "Llama", "Vicuna", "Open Assistant", "The Pile", "Claude Code", "Codex", "OpenClaw", "Linear", "Sonic Adventure Mod Manager", "Blender", "Shadow PC"]
people: ["Curran (Kar^n)", "Teknium", "Dylan Rolnick", "Emozilla", "Bowen Peng", "Jeffrey (coautor do YaRN)", "Nous Research", "Anthropic", "OpenAI", "Google", "Meta", "DeepSeek", "Kimi", "Peter (entrevistador)"]
claims: ["Siscofrência ('você está absolutamente certo') é sintoma de reward hacking; combate-se introduzindo novo contexto — por exemplo, girar um agente de crítica adversarial sem nenhum contexto após cada passagem e aprender com ele", "In-context learning é mais poderoso que fine-tuning para moldar comportamento; salvar exemplos bem-sucedidos como skills/memórias equivale a reinforcement learning em tempo de teste", "Tudo em um harness é gestão de contexto: memórias e skills são contexto comprimido carregado apenas no momento-alvo, não mantido permanentemente ativo na janela", "Com um contexto pessoal forte e específico, trocar de modelo (Claude ↔ GPT ↔ Qwen) quase não muda o comportamento percebido, pois o contexto 'sobrepõe' o modelo", "O Hermes Curator roda via cron para limpar skills e memórias e remover 'slop'; seus critérios são modulares e reprogramáveis pelo usuário via prompt", "Um kanban modular permite trocar humanos e agentes de papel (PM, engenheiros, call center) como camada de orquestração mista", "Benchmarks (Wolfbench; harness bench do post da Qwen) teriam mostrado Claude performando melhor dentro do Hermes Agent que no Claude Code, atribuído à ausência de prompts de política do laboratório", "Harnesses nativos embutem dezenas de milhares de tokens de prompts de política alheios ao trabalho do usuário, degradando capacidade; o Hermes minimiza política arbitrária além da segurança básica", "Monetização viável para harness open-source: portal agregador de modelos, tool gateway com assinaturas embutidas (imagem, áudio, VPS, busca web) e serviços enterprise com versões customizadas e RL sobre traces do cliente", "O custo de trocar de modelos deve ser zero; um harness aberto protege o usuário do fim dos subsídios de tokens (ex.: migração de planos all-you-can-eat para API-only)", "O maior contribuidor do repositório do Hermes Agent é o próprio Hermes Agent — evidência de auto-melhoria real", "Qualquer modelo não vastamente superinteligente é jailbreakável dado tentativas ilimitadas e ausência de memória entre tentativas", "YaRN (método da Nous para extensão de contexto) foi citado/usado por Meta, DeepSeek, Kimi e OpenAI, demonstrando o impacto de contribuições abertas"]
deep_dive: "medium"
deep_dive_reason: "Reúne insights acionáveis de harness e context-engineering (curator contra slop, crítica adversarial sem contexto, ICL como test-time RL, memória como gestão de contexto), mas os dilui em tom promocional, anedotas extensas (demo de mod de jogo) e narrativa de origem, reduzindo densidade técnica e novidade arquitetural."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-why-the-harness-matters-more-than-the-model-yc-paper-club--n9xKblqyQ28|Why The Harness Matters More Than The Model | YC Paper Club]]", "[[extracts/youtube/ai-learning/2026-09-11-when-to-build-your-own-agent-harness-harrison-chase-langchain--HI2q3ci3Iuc|When to Build Your Own Agent Harness | Harrison Chase, LangChain]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-harnesses-in-ai-a-deep-dive-tejas-kumar-ibm--C_GG5g38vLU|Harnesses in AI: A Deep Dive — Tejas Kumar, IBM]]", "[[extracts/youtube/ai-learning/2026-09-11-how-google-deepmind-runs-agents-at-scale-kp-sawhney-ian-ballantyne-google-deepmi--7gujZrJ9L5I|How Google DeepMind Runs Agents at Scale — KP Sawhney & Ian Ballantyne, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-hermes-deepseek-4-minimax-2-7-multi-model-coding-on-a-zimaboard---3MPnUGqa68|Hermes + DeepSeek 4 + MiniMax 2.7: Multi-Model Coding on a ZimaBoard]]"]
---

# Hermes Co-Founder on Building an AI Agent That Improves Itself | Karan Malhotra

## Tese
O Hermes Agent da Nous Research é um harness open-source agnóstico de modelo cujo sistema de auto-melhoria (memórias, skills e um 'curator' em cron) e prompts deliberadamente alinhados ao usuário individual tornam qualquer modelo mais capaz e 'leal' à pessoa do que em seu harness nativo (Claude Code, Codex).

## Conceitos-chave
- reward hacking
- siscofrência (sycophancy)
- alinhamento ao usuário individual
- self-improvement loop
- in-context learning (ICL)
- reinforcement learning em tempo de teste
- gestão de contexto como núcleo do harness
- memórias e skills como contexto comprimido
- curator loop contra 'slop'
- harness vs. modelo subjacente
- simulação de lealdade gerando capacidade
- crítica adversarial com agente sem contexto
- proatividade emergente do agente
- orquestração kanban humano-agente
- agnosticidade de modelo e custo zero de troca
- ambientes de RL (Atropos)
- jailbreakabilidade de modelos
- captura regulatória vs. open source
- subsídio de tokens e sustentabilidade

## Ferramentas & pessoas
**Ferramentas:** Hermes Agent, Hermes Curator, Forge, Atropos, YaRN, World Sim, Nous Portal, Tool Gateway, DRO optimizer, GPT4-x-Alpaca, Llama, Vicuna, Open Assistant, The Pile, Claude Code, Codex, OpenClaw, Linear, Sonic Adventure Mod Manager, Blender, Shadow PC

**Pessoas/orgs:** Curran (Kar^n), Teknium, Dylan Rolnick, Emozilla, Bowen Peng, Jeffrey (coautor do YaRN), Nous Research, Anthropic, OpenAI, Google, Meta, DeepSeek, Kimi, Peter (entrevistador)

## Claims acionáveis
- Siscofrência ('você está absolutamente certo') é sintoma de reward hacking; combate-se introduzindo novo contexto — por exemplo, girar um agente de crítica adversarial sem nenhum contexto após cada passagem e aprender com ele
- In-context learning é mais poderoso que fine-tuning para moldar comportamento; salvar exemplos bem-sucedidos como skills/memórias equivale a reinforcement learning em tempo de teste
- Tudo em um harness é gestão de contexto: memórias e skills são contexto comprimido carregado apenas no momento-alvo, não mantido permanentemente ativo na janela
- Com um contexto pessoal forte e específico, trocar de modelo (Claude ↔ GPT ↔ Qwen) quase não muda o comportamento percebido, pois o contexto 'sobrepõe' o modelo
- O Hermes Curator roda via cron para limpar skills e memórias e remover 'slop'; seus critérios são modulares e reprogramáveis pelo usuário via prompt
- Um kanban modular permite trocar humanos e agentes de papel (PM, engenheiros, call center) como camada de orquestração mista
- Benchmarks (Wolfbench; harness bench do post da Qwen) teriam mostrado Claude performando melhor dentro do Hermes Agent que no Claude Code, atribuído à ausência de prompts de política do laboratório
- Harnesses nativos embutem dezenas de milhares de tokens de prompts de política alheios ao trabalho do usuário, degradando capacidade; o Hermes minimiza política arbitrária além da segurança básica
- Monetização viável para harness open-source: portal agregador de modelos, tool gateway com assinaturas embutidas (imagem, áudio, VPS, busca web) e serviços enterprise com versões customizadas e RL sobre traces do cliente
- O custo de trocar de modelos deve ser zero; um harness aberto protege o usuário do fim dos subsídios de tokens (ex.: migração de planos all-you-can-eat para API-only)
- O maior contribuidor do repositório do Hermes Agent é o próprio Hermes Agent — evidência de auto-melhoria real
- Qualquer modelo não vastamente superinteligente é jailbreakável dado tentativas ilimitadas e ausência de memória entre tentativas
- YaRN (método da Nous para extensão de contexto) foi citado/usado por Meta, DeepSeek, Kimi e OpenAI, demonstrando o impacto de contribuições abertas

> **Deep dive:** `medium` — Reúne insights acionáveis de harness e context-engineering (curator contra slop, crítica adversarial sem contexto, ICL como test-time RL, memória como gestão de contexto), mas os dilui em tom promocional, anedotas extensas (demo de mod de jogo) e narrativa de origem, reduzindo densidade técnica e novidade arquitetural.
