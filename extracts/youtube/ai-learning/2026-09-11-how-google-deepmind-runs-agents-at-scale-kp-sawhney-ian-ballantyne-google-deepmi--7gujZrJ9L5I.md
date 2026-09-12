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
