---
title: "How Google DeepMind Runs Agents at Scale — KP Sawhney & Ian Ballantyne, Google DeepMind"
type: "extract"
source: "youtube"
video_id: "7gujZrJ9L5I"
url: "https://www.youtube.com/watch?v=7gujZrJ9L5I"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-google-deepmind-runs-agents-at-scale-kp-sawhney-ian-ballantyne-google-deepmi--7gujZrJ9L5I.txt]]"
tags: ["agents", "agentic-coding", "agent-fleets", "harness-engineering", "context-engineering", "token-budgeting", "evals", "observability", "model-selection", "multi-agent", "code-review", "agent-tooling", "governanca"]
thesis: "Google DeepMind está generalizando seu harness agêntico interno (Antigravity) além do código — tratando etapas de pipelines como deep research como colaboradores num workspace compartilhado — enquanto resolve em escala Google os problemas de custo de tokens, curadoria de skills, avaliação e observabilidade de agentes."
concepts: ["harness agêntico (Antigravity) como plataforma unificada para múltiplos casos de uso", "gerenciamento de quota de tokens por usuário/time", "fallback transparente de modelos sob o harness (pro → flash → local)", "curadoria Darwiniana de skills para evitar sprawling organizacional", "agent trajectory store para diagnóstico de loops e desvios", "colaboração via sistema de arquivos compartilhado vs passagem de blobs de contexto", "mock TPUs para avaliar harness sem gastar compute real", "auto-review de código com modelos fine-tuned por linguagem em style guides", "humano como supervisor numa 'linha de montagem digital' de agentes", "skills + guardrails CLI como alternativa a MCP", "avaliação de fluxos agênticos complexos com datasets e sandboxes", "gerente de agentes integrado ao IDE com controle de browser e inspeção de DOM"]
tools: ["Antigravity", "Gemini (Flash/Pro/Ultra)", "Gemma 4", "Jules", "MCP", "guardrail CLI", "interactions API (deep research agent)", "agent trajectory store (UI de observabilidade interna)", "auto review model (fine-tuned por linguagem)"]
people: ["Ian Valentine", "KP Sony", "Google DeepMind", "Google", "Anthropic", "GitHub", "Kevin (time do Antigravity)"]
claims: ["Substituir a passagem de grandes blobs de texto entre etapas do pipeline de deep research por colaboração num sistema de arquivos compartilhado reduz custo de contexto", "Misturar modelos gratuitos/locais (Gemma 4) com modelos avançados em componentes específicos do sistema agêntico mitiga o custo de tokens", "Usar mock TPUs permite testar harness e fluxo agêntico sem consumir horas reais de TPU", "Um agent trajectory store permite diagnosticar o ponto exato em que o agente entrou em loop ou saiu dos trilhos", "Skills devem passar por seleção quase Darwiniana para que só as melhores sobrevivam em organizações grandes", "A responsabilidade de criar testes para skills específicas é do autor da skill, e agentes também estão sendo usados para desenhar evals (meta-avaliação)", "O fallback entre modelos por esgotamento de quota deve ocorrer de forma transparente sob o harness, sem interromper a tarefa em andamento", "Combinação de skills com interações CLI guardrailadas funciona como substituto prático a MCP, que KP considera possivelmente efêmero (embora seja suportado pela comunidade)", "Modelos de auto-review fine-tuned por linguagem em style guides e bons exemplos de código, complementados por prompts específicos por produto, dão bom sinal de revisão de PRs", "Gestão de quota por usuário é hoje 'força bruta', e o modelo de assinatura não se sustenta para sistemas agênticos famintos por tokens (ex.: Anthropic bloqueou o openclaw)", "Comunicação agente-a-agente eficiente, com o humano supervisionando a 'linha de montagem digital', é a direção futura dos multi-agentes"]
deep_dive: "high"
deep_dive_reason: "Revela práticas internas de Google-scale de harness, context-engineering (workspace compartilhado vs blobs de contexto), evals (mock TPUs, datasets por skill), token-budgeting (fallback de modelos, quotas) e observabilidade (trajectory store), com densidade alta de detalhe arquitetural acionável e novidade, apesar do demo inicial raso."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc|The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-scaling-agents-for-gen-ai-products-anju-kambadur-bloomberg-head-of-ai-engineerin--b2GqTDWtg6s|Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-harness-matters-more-than-the-model-yc-paper-club--n9xKblqyQ28|Why The Harness Matters More Than The Model | YC Paper Club]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-s-applied-ai-team-on-the-evolution-of-agentic-surfaces--K0X9QDRkIdg|Anthropic's Applied AI team on the Evolution of Agentic Surfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-why-senior-engineers-struggle-to-build-ai-agents-philipp-schmid-google-deepmind--3_gYbhABcAE|Why (Senior) Engineers Struggle to Build AI Agents — Philipp Schmid, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-your-coding-agent-should-do-ai-system-engineering-ben-burtenshaw-hugging-face--JomVvNDjGb8|Your Coding Agent Should Do AI System Engineering — Ben Burtenshaw, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-creating-agents-that-co-create-karina-nguyen-openai--1XvN5EBDnDw|Creating Agents that Co-Create — Karina Nguyen, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-what-is-google-s-agentic-ai-strategy-explained-by-google-cloud-s-cto--3tng5VWbWXU|What is Google's Agentic AI Strategy? (Explained by Google Cloud's CTO)]]", "[[extracts/youtube/ai-learning/2026-09-11-hermes-co-founder-on-building-an-ai-agent-that-improves-itself-karan-malhotra--UWjh5Z4s8jY|Hermes Co-Founder on Building an AI Agent That Improves Itself | Karan Malhotra]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-automate-my-own-job-at-hugging-face-using-agents-niels-rogge-hugging-face--FLUoowDJg4I|How I automate my own job at Hugging Face using agents — Niels Rogge, Hugging Face]]", "[[extracts/youtube/ai-learning/2026-09-11-jensen-huang-why-companies-need-open-agent-systems--Yy3JH6dDugc|Jensen Huang: Why companies need open agent systems]]", "[[extracts/youtube/ai-learning/2026-09-11-parallels-parag-agrawal-building-a-new-web-for-ai-agents--fUcnE6pjq5w|Parallel’s Parag Agrawal: Building a New Web for AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-evaluations-at-scale-for-everybody-nicholas-kang-michael-aaron-google-de--Ubwb6NzegyA|Agentic Evaluations at Scale, For Everybody — Nicholas Kang & Michael Aaron, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-stanford-s-elite-student-hackathon-full-documentary-on-treehacks-2026--wApaJjvNZFs|Inside Stanford's Elite Student Hackathon (Full Documentary on TreeHacks 2026)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-create-agent-swarms-with-the-new-openai-assistants-api--8fMnAZI1bdA|How to Create Agent Swarms With the NEW OpenAI Assistants API]]", "[[extracts/youtube/ai-learning/2026-09-11-getting-started-with-omnigent-the-coding-agent-meta-harness--AyV0hum_hA8|Getting Started with Omnigent | The Coding Agent Meta-Harness]]", "[[extracts/youtube/ai-learning/2026-09-11-google-deepmind-developers-how-nano-banana-was-made--I8VUN141MjU|Google DeepMind Developers: How Nano Banana Was Made]]", "[[extracts/youtube/ai-learning/2026-09-11-the-thinking-game-full-documentary-tribeca-film-festival-official-selection--d95J8yzvjbQ|The Thinking Game | Full documentary | Tribeca Film Festival official selection]]"]
theme: "Orquestração Multiagente em Escala"
---

# How Google DeepMind Runs Agents at Scale — KP Sawhney & Ian Ballantyne, Google DeepMind

## Tese
Google DeepMind está generalizando seu harness agêntico interno (Antigravity) além do código — tratando etapas de pipelines como deep research como colaboradores num workspace compartilhado — enquanto resolve em escala Google os problemas de custo de tokens, curadoria de skills, avaliação e observabilidade de agentes.

## Conceitos-chave
- harness agêntico (Antigravity) como plataforma unificada para múltiplos casos de uso
- gerenciamento de quota de tokens por usuário/time
- fallback transparente de modelos sob o harness (pro → flash → local)
- curadoria Darwiniana de skills para evitar sprawling organizacional
- agent trajectory store para diagnóstico de loops e desvios
- colaboração via sistema de arquivos compartilhado vs passagem de blobs de contexto
- mock TPUs para avaliar harness sem gastar compute real
- auto-review de código com modelos fine-tuned por linguagem em style guides
- humano como supervisor numa 'linha de montagem digital' de agentes
- skills + guardrails CLI como alternativa a MCP
- avaliação de fluxos agênticos complexos com datasets e sandboxes
- gerente de agentes integrado ao IDE com controle de browser e inspeção de DOM

## Ferramentas & pessoas
**Ferramentas:** Antigravity, Gemini (Flash/Pro/Ultra), Gemma 4, Jules, MCP, guardrail CLI, interactions API (deep research agent), agent trajectory store (UI de observabilidade interna), auto review model (fine-tuned por linguagem)

**Pessoas/orgs:** Ian Valentine, KP Sony, Google DeepMind, Google, Anthropic, GitHub, Kevin (time do Antigravity)

## Claims acionáveis
- Substituir a passagem de grandes blobs de texto entre etapas do pipeline de deep research por colaboração num sistema de arquivos compartilhado reduz custo de contexto
- Misturar modelos gratuitos/locais (Gemma 4) com modelos avançados em componentes específicos do sistema agêntico mitiga o custo de tokens
- Usar mock TPUs permite testar harness e fluxo agêntico sem consumir horas reais de TPU
- Um agent trajectory store permite diagnosticar o ponto exato em que o agente entrou em loop ou saiu dos trilhos
- Skills devem passar por seleção quase Darwiniana para que só as melhores sobrevivam em organizações grandes
- A responsabilidade de criar testes para skills específicas é do autor da skill, e agentes também estão sendo usados para desenhar evals (meta-avaliação)
- O fallback entre modelos por esgotamento de quota deve ocorrer de forma transparente sob o harness, sem interromper a tarefa em andamento
- Combinação de skills com interações CLI guardrailadas funciona como substituto prático a MCP, que KP considera possivelmente efêmero (embora seja suportado pela comunidade)
- Modelos de auto-review fine-tuned por linguagem em style guides e bons exemplos de código, complementados por prompts específicos por produto, dão bom sinal de revisão de PRs
- Gestão de quota por usuário é hoje 'força bruta', e o modelo de assinatura não se sustenta para sistemas agênticos famintos por tokens (ex.: Anthropic bloqueou o openclaw)
- Comunicação agente-a-agente eficiente, com o humano supervisionando a 'linha de montagem digital', é a direção futura dos multi-agentes

> **Deep dive:** `high` — Revela práticas internas de Google-scale de harness, context-engineering (workspace compartilhado vs blobs de contexto), evals (mock TPUs, datasets por skill), token-budgeting (fallback de modelos, quotas) e observabilidade (trajectory store), com densidade alta de detalhe arquitetural acionável e novidade, apesar do demo inicial raso.
