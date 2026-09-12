---
title: "I Tested Bolt and Lovable Here's What's Best for Your Project"
type: "extract"
source: "youtube"
video_id: "_PgBDk_GhPo"
url: "https://www.youtube.com/watch?v=_PgBDk_GhPo"
channel: "Jelani. The Builder."
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-i-tested-bolt-and-lovable-here-s-what-s-best-for-your-project--_PgBDk_GhPo.txt]]"
tags: ["agentic-coding", "agent-tooling", "stack-tooling", "token-budgeting", "analise", "process"]
thesis: "Uma comparação prática entre bolt.new e lovable.dev, construindo o mesmo app de transcrição de vídeo com prompts idênticos, conclui que bolt.new vence no agregado (preço por tokens, velocidade e melhorias iterativas), enquanto lovable.dev vence em design e conjunto de features (integrações e edição visual), com empate em compreensão de instruções."
concepts: ["construção de apps no-code via linguagem natural", "comparação de ferramentas com prompts idênticos", "modelo de precificação por tokens vs. por mensagens", "integração via webhook para backend externo", "pipeline de transcrição de vídeo (download, transcrição, sumarização)", "iteração de UI por re-prompting", "pré-planejamento de prompts para economizar tokens/mensagens", "recurso diff para reduzir consumo de tokens", "edição visual de elementos (select) vs. prompts textuais", "integração direta com banco de dados e Git"]
tools: ["bolt.new", "lovable.dev", "make.com", "Supabase", "GitHub", "StackBlitz", "Resend", "Stripe", "Cursor", "Windsurf", "AssemblyAI", "Fast Saver API", "Claude", "Tailwind"]
people: ["StackBlitz (empresa por trás do bolt.new)", "Supabase"]
claims: ["O plano gratuito do bolt.new dá ~100 mil tokens/dia (~3 milhões/mês), permitindo mais experimentação do que os 5 mensagens/dia do lovable.dev", "O recurso diff do bolt.new reduz consumo de tokens editando apenas o código alterado em vez de reescrever tudo", "Pré-planejar prompts detalhados economiza tokens (bolt) e mensagens (lovable) e aumenta a chance de gerar o app em um único shot", "lovable.dev tem integração direta com Supabase, GitHub, Resend (e-mail) e Stripe, além do recurso de seleção visual de elementos, que o bolt.new ainda não possui", "bolt.new foi mais rápido na primeira geração do código e mais eficaz em melhorias iterativas (aplicou o esquema de cores pedido, o que lovable falhou na primeira tentativa)", "lovable.dev entregou melhor design inicial (detalhes de sombra), mesmo sem seguir o esquema de cores instruído", "Ambas as ferramentas integraram corretamente um webhook do make.com que encadeia Fast Saver API (download), AssemblyAI (transcrição) e Claude (sumário), retornando o texto ao app", "Na métrica de compreensão houve empate: ambos executaram as mesmas instruções complexas com o mesmo prompt", "Para micro-apps simples, o autor recomenda bolt.new como melhor custo-benefício, sugerindo Cursor ou Windsurf para projetos complexos", "O autor relata ter vendido um app construído com essas ferramentas por US$ 3.000 em ~2 meses de uso"]
deep_dive: "low"
deep_dive_reason: "Comparação consumidor-promocional de ferramentas no-code focada em preço e resultado visual, sem densidade de insight arquitetural sobre harness, evals, context-engineering ou governança de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-bolt-vs-lovable-which-ai-app-builder-comes-out-on-top--yHDvCGNjIqk|Bolt vs Lovable: which AI app builder comes out on top?]]", "[[extracts/youtube/ai-learning/2026-09-11-is-this-the-best-vibe-coding-platform-lovable-ai--3eDrAHjSqXo|Is this the Best Vibe Coding Platform? (Lovable AI)]]", "[[extracts/youtube/ai-learning/2026-09-11-bolt-tutorial-for-beginners-with-the-bolt-ceo-eric-simons--1SfUMQ1yTY8|Bolt tutorial for beginners with the Bolt CEO Eric Simons]]", "[[extracts/youtube/ai-learning/2026-09-11-i-built-a-4589-website-in-minutes-with-bolt-new-and-cursor-ai--KqiQ4kC8OJI|I Built a $4589 Website in Minutes with Bolt.new and Cursor AI!]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-perfect-looking-apps-with-bolt-new-easy-hack--gZKLPNhWXxE|How to Build PERFECT Looking Apps With Bolt.new (Easy Hack)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-lovable-n8n-ai-agents-no-code--EN0-KNqs6aA|Build Anything With Lovable + n8n AI Agents (No-Code)]]"]
theme: "Agentes de IA No-Code"
---

# I Tested Bolt and Lovable Here's What's Best for Your Project

## Tese
Uma comparação prática entre bolt.new e lovable.dev, construindo o mesmo app de transcrição de vídeo com prompts idênticos, conclui que bolt.new vence no agregado (preço por tokens, velocidade e melhorias iterativas), enquanto lovable.dev vence em design e conjunto de features (integrações e edição visual), com empate em compreensão de instruções.

## Conceitos-chave
- construção de apps no-code via linguagem natural
- comparação de ferramentas com prompts idênticos
- modelo de precificação por tokens vs. por mensagens
- integração via webhook para backend externo
- pipeline de transcrição de vídeo (download, transcrição, sumarização)
- iteração de UI por re-prompting
- pré-planejamento de prompts para economizar tokens/mensagens
- recurso diff para reduzir consumo de tokens
- edição visual de elementos (select) vs. prompts textuais
- integração direta com banco de dados e Git

## Ferramentas & pessoas
**Ferramentas:** bolt.new, lovable.dev, make.com, Supabase, GitHub, StackBlitz, Resend, Stripe, Cursor, Windsurf, AssemblyAI, Fast Saver API, Claude, Tailwind

**Pessoas/orgs:** StackBlitz (empresa por trás do bolt.new), Supabase

## Claims acionáveis
- O plano gratuito do bolt.new dá ~100 mil tokens/dia (~3 milhões/mês), permitindo mais experimentação do que os 5 mensagens/dia do lovable.dev
- O recurso diff do bolt.new reduz consumo de tokens editando apenas o código alterado em vez de reescrever tudo
- Pré-planejar prompts detalhados economiza tokens (bolt) e mensagens (lovable) e aumenta a chance de gerar o app em um único shot
- lovable.dev tem integração direta com Supabase, GitHub, Resend (e-mail) e Stripe, além do recurso de seleção visual de elementos, que o bolt.new ainda não possui
- bolt.new foi mais rápido na primeira geração do código e mais eficaz em melhorias iterativas (aplicou o esquema de cores pedido, o que lovable falhou na primeira tentativa)
- lovable.dev entregou melhor design inicial (detalhes de sombra), mesmo sem seguir o esquema de cores instruído
- Ambas as ferramentas integraram corretamente um webhook do make.com que encadeia Fast Saver API (download), AssemblyAI (transcrição) e Claude (sumário), retornando o texto ao app
- Na métrica de compreensão houve empate: ambos executaram as mesmas instruções complexas com o mesmo prompt
- Para micro-apps simples, o autor recomenda bolt.new como melhor custo-benefício, sugerindo Cursor ou Windsurf para projetos complexos
- O autor relata ter vendido um app construído com essas ferramentas por US$ 3.000 em ~2 meses de uso

> **Deep dive:** `low` — Comparação consumidor-promocional de ferramentas no-code focada em preço e resultado visual, sem densidade de insight arquitetural sobre harness, evals, context-engineering ou governança de agentes.
