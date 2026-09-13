---
title: "How to use Cursor Agent for beginners"
type: "extract"
source: "youtube"
video_id: "2gBcO3ht0ws"
url: "https://www.youtube.com/watch?v=2gBcO3ht0ws"
channel: "David Ondrej"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-use-cursor-agent-for-beginners--2gBcO3ht0ws.txt]]"
tags: ["agentic-coding", "agent-tooling", "context-management", "model-selection", "code-review", "error-handling", "process", "stack-tooling", "roadmap"]
thesis: "O vídeo argumenta que o novo agente do Cursor (edição multi-arquivo autônoma, execução de comandos no terminal e indexação completa do codebase) permite até não-desenvolvedores construir apps full-stack rapidamente, desde que guiado com prompts iterativos, referências visuais e arquivos de regras por projeto."
concepts: ["agentic coding com edição multi-arquivo autônoma", "indexação do codebase para contexto completo (vs. pulling aleatório de trechos)", "execução de comandos no terminal pelo agente", "system prompt global ('Rules for AI') vs. arquivo .cursorrules por projeto", "iteração de prompt: cancelar, editar e reenviar revertendo mudanças parciais", "grounding visual com screenshots como referência para geração de UI", "roadmap.md como plano de desenvolvimento passo a passo", "tagging de arquivos relevantes no prompt para direcionar o agente", "revisão de diffs compactos antes de aceitar mudanças", "ciclo de depuração com descrição do erro em linguagem simples", "comparação de ferramentas: MVP rápido (Bolt) vs. IDE sério (Cursor, fork do VS Code)", "curva de aprendizado comprimida: fundamentos em 5-20h vs. milhares de horas antes"]
tools: ["Cursor", "Claude Sonnet 3.5", "GPT-4o", "o1 mini", "Next.js", "Twilio", "Voiceflow", "Bolt", "VS Code", "ChatGPT (web search)", "Chrome DevTools", "Vectal AI"]
people: ["David (apresentador)", "David Erens (sugestão do app)", "Cursor (empresa, avaliada em US$ 2,5 bi)", "New Society (comunidade do criador)", "Vectal AI (startup do apresentador)", "Google/Google Docs"]
claims: ["O modo agent do Cursor só funciona com modelos Claude — selecione Sonnet 3.5 nas configurações de modelos", "Configure 'Rules for AI' como system prompt global e crie um arquivo .cursorrules com instruções específicas por projeto para tornar o agente mais produtivo", "Envie screenshots da UI desejada como referência visual; screenshots parciais focados na parte relevante funcionam melhor", "Ao atualizar um prompt durante a execução, use 'submit from previous message' para reverter as mudanças de arquivo pela metade e reexecutar com o prompt melhorado", "Marque (tag) os arquivos relevantes no prompt (ex.: block.tsx) para apontar o agente na direção certa", "Use prompts como 'implemente o fix da forma mais simples possível, quanto menos linhas melhor' para manter mudanças concisas e focadas", "Abra terminais longos (ex.: servidor de front-end) em terminal separado/pop-out para não bloquear o agente, e renomeie os terminais", "Crie um roadmap.md com passos numerados para guiar o desenvolvimento incremental com o agente", "Use o chat paralelamente enquanto o agente executa para planejar e aprender, em vez de aceitar mudanças às cegas", "Bolt serve para mockups/MVPs em 5-10 minutos; Cursor (fork do VS Code) é melhor para apps funcionais com backend e fine-tuning sério", "Iniciantes são os que mais se beneficiam de ferramentas como Cursor; invista 5-20 horas nos fundamentos para não travar nos erros comuns", "Revise o diff antes de aceitar (obrigatório em codebase funcional; aceitar rápido é aceitável em protótipos novos)"]
deep_dive: "low"
deep_dive_reason: "É um tutorial introdutório com viés promocional recorrente (New Society, waitlist da startup): entrega dicas práticas úteis mas amplamente conhecidas, sem densidade arquitetural ou novidade em harness, evals ou context-engineering."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-cursor-ai-agents-work-like-10-developers-cursor-vp-live-demo--8QN23ZThdRY|Cursor AI Agents Work Like 10 Developers (Cursor VP Live Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-super-effective-ai-agents-full-tutorial-cursor-openai--MSO4qCiwTjQ|How to Build Super Effective AI AGENTS - FULL TUTORIAL | Cursor - OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-i-built-a-4589-website-in-minutes-with-bolt-new-and-cursor-ai--KqiQ4kC8OJI|I Built a $4589 Website in Minutes with Bolt.new and Cursor AI!]]", "[[extracts/youtube/ai-learning/2026-09-11-bolt-tutorial-for-beginners-with-the-bolt-ceo-eric-simons--1SfUMQ1yTY8|Bolt tutorial for beginners with the Bolt CEO Eric Simons]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-ai-agents-you-must-have-beginners-guide--WLvQCIUWebs|5 simple AI Agents you must have - beginners guide]]", "[[extracts/youtube/ai-learning/2026-09-11-coding-with-openai-o1-in-cursor-can-we-replace-claude-3-5-now--wwC86t5k77Y|Coding With OpenAI-o1 in Cursor - Can We Replace Claude 3.5 Now?]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-tmux-here-s-how--z7xyZQVK4Dg|Build Anything with Tmux, Here's How]]"]
theme: "Agentes de IA No-Code"
---

# How to use Cursor Agent for beginners

## Tese
O vídeo argumenta que o novo agente do Cursor (edição multi-arquivo autônoma, execução de comandos no terminal e indexação completa do codebase) permite até não-desenvolvedores construir apps full-stack rapidamente, desde que guiado com prompts iterativos, referências visuais e arquivos de regras por projeto.

## Conceitos-chave
- agentic coding com edição multi-arquivo autônoma
- indexação do codebase para contexto completo (vs. pulling aleatório de trechos)
- execução de comandos no terminal pelo agente
- system prompt global ('Rules for AI') vs. arquivo .cursorrules por projeto
- iteração de prompt: cancelar, editar e reenviar revertendo mudanças parciais
- grounding visual com screenshots como referência para geração de UI
- roadmap.md como plano de desenvolvimento passo a passo
- tagging de arquivos relevantes no prompt para direcionar o agente
- revisão de diffs compactos antes de aceitar mudanças
- ciclo de depuração com descrição do erro em linguagem simples
- comparação de ferramentas: MVP rápido (Bolt) vs. IDE sério (Cursor, fork do VS Code)
- curva de aprendizado comprimida: fundamentos em 5-20h vs. milhares de horas antes

## Ferramentas & pessoas
**Ferramentas:** Cursor, Claude Sonnet 3.5, GPT-4o, o1 mini, Next.js, Twilio, Voiceflow, Bolt, VS Code, ChatGPT (web search), Chrome DevTools, Vectal AI

**Pessoas/orgs:** David (apresentador), David Erens (sugestão do app), Cursor (empresa, avaliada em US$ 2,5 bi), New Society (comunidade do criador), Vectal AI (startup do apresentador), Google/Google Docs

## Claims acionáveis
- O modo agent do Cursor só funciona com modelos Claude — selecione Sonnet 3.5 nas configurações de modelos
- Configure 'Rules for AI' como system prompt global e crie um arquivo .cursorrules com instruções específicas por projeto para tornar o agente mais produtivo
- Envie screenshots da UI desejada como referência visual; screenshots parciais focados na parte relevante funcionam melhor
- Ao atualizar um prompt durante a execução, use 'submit from previous message' para reverter as mudanças de arquivo pela metade e reexecutar com o prompt melhorado
- Marque (tag) os arquivos relevantes no prompt (ex.: block.tsx) para apontar o agente na direção certa
- Use prompts como 'implemente o fix da forma mais simples possível, quanto menos linhas melhor' para manter mudanças concisas e focadas
- Abra terminais longos (ex.: servidor de front-end) em terminal separado/pop-out para não bloquear o agente, e renomeie os terminais
- Crie um roadmap.md com passos numerados para guiar o desenvolvimento incremental com o agente
- Use o chat paralelamente enquanto o agente executa para planejar e aprender, em vez de aceitar mudanças às cegas
- Bolt serve para mockups/MVPs em 5-10 minutos; Cursor (fork do VS Code) é melhor para apps funcionais com backend e fine-tuning sério
- Iniciantes são os que mais se beneficiam de ferramentas como Cursor; invista 5-20 horas nos fundamentos para não travar nos erros comuns
- Revise o diff antes de aceitar (obrigatório em codebase funcional; aceitar rápido é aceitável em protótipos novos)

> **Deep dive:** `low` — É um tutorial introdutório com viés promocional recorrente (New Society, waitlist da startup): entrega dicas práticas úteis mas amplamente conhecidas, sem densidade arquitetural ou novidade em harness, evals ou context-engineering.
