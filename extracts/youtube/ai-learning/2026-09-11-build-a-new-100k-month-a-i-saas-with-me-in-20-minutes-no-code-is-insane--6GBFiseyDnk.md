---
title: "Build a NEW $100K/Month A.I SaaS WITH ME in 20 minutes (No-code Is INSANE)"
type: "extract"
source: "youtube"
video_id: "6GBFiseyDnk"
url: "https://www.youtube.com/watch?v=6GBFiseyDnk"
channel: "Kevin Badi | AI Operating Systems "
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-a-new-100k-month-a-i-saas-with-me-in-20-minutes-no-code-is-insane--6GBFiseyDnk.txt]]"
tags: ["agentic-coding", "agent-tooling", "model-selection", "error-handling", "stack-tooling", "testes-qa", "process", "curriculo-conteudo"]
thesis: "Um app de rastreamento calórico por foto (clone do Cal AI, que fatura US$1,12M/mês) pode ser construído sem código via engenharia de prompts iterativa no Bolt usando a API multimodal GPT-4o da OpenAI."
concepts: ["desenvolvimento no-code via prompts iterativos", "API multimodal de visão (imagem + texto)", "migração de modelo deprecado (GPT-4 Vision Preview -> GPT-4o)", "saída estruturada em JSON para parsing", "rastreamento de macros (calorias, proteína, gordura, carboidratos)", "gamificação com calendário verde/vermelho por metas diárias", "consistência de captura de foto (distância fixa de ~30cm do prato)", "codificação de imagem em base64", "depuração iterativa colando trechos da documentação da API", "autenticação de usuários e isolamento de dados por conta", "monetização por assinatura (Stripe)"]
tools: ["Bolt (bolt.new)", "OpenAI API", "GPT-4o", "GPT-4 Vision Preview (deprecado)", "ChatGPT", "Claude API", "Cal AI", "Clonify", "Stripe", "No Code Academy"]
people: ["OpenAI", "Anthropic", "Cal AI (fundador)", "No Code Academy", "Tesla"]
claims: ["Usar GPT-4o em vez do modelo deprecado GPT-4 Vision Preview é necessário para análise multimodal de imagens de comida", "Copiar o formato exato do 'image input request' da documentação da OpenAI corrige erros de análise de imagem no app gerado", "Instruir o usuário a fotografar a ~1 pé (30cm) do prato torna a análise de macros mais consistente", "Exigir no prompt que o modelo responda apenas com JSON em formato exato permite encaminhar os dados para outros componentes da aplicação", "O app Cal AI original gera aproximadamente US$1,12 milhão por mês com funcionalidade de rastreamento calórico por foto", "A conversão da imagem para base64 na URL nem sempre é necessária e pode ser removida quando causa falhas", "O ciclo prompt -> teste -> relatar erro -> novo prompt no Bolt permite adicionar funcionalidades (metas diárias, calendário, timer, histórico) sem escrever código", "Próximos passos naturais do produto: autenticação para isolar dados por usuário, página de preços e cobrança recorrente via Stripe, e notificações push para retenção"]
deep_dive: "low"
deep_dive_reason: "Tutorial no-code essencialmente promocional: os insights limitam-se a correções pontuais de API (modelo deprecado, formato de request) e prompt engineering básico, sem densidade arquitetural nem novidade em harness, evals, context-engineering ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-i-built-a-4589-website-in-minutes-with-bolt-new-and-cursor-ai--KqiQ4kC8OJI|I Built a $4589 Website in Minutes with Bolt.new and Cursor AI!]]", "[[extracts/youtube/ai-learning/2026-09-11-bolt-tutorial-for-beginners-with-the-bolt-ceo-eric-simons--1SfUMQ1yTY8|Bolt tutorial for beginners with the Bolt CEO Eric Simons]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-build-perfect-looking-apps-with-bolt-new-easy-hack--gZKLPNhWXxE|How to Build PERFECT Looking Apps With Bolt.new (Easy Hack)]]", "[[extracts/youtube/ai-learning/2026-09-11-i-built-a-marketing-team-with-1-ai-agent-and-no-code-free-n8n-template--ldETapkr8Hg|I Built a Marketing Team with 1 AI Agent and No Code (free n8n template)]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-lovable-n8n-ai-agents-no-code--EN0-KNqs6aA|Build Anything With Lovable + n8n AI Agents (No-Code)]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-use-ai-to-build-your-saas-startup-lovable-supabase--mJwPvyc4-rk|How to use AI to build your SaaS startup (Lovable, Supabase)]]", "[[extracts/youtube/ai-learning/2026-09-11-i-got-a-private-lesson-on-google-s-new-nano-banana-ai-model--3Zvk4AMCrG8|I got a private lesson on Google's NEW Nano Banana AI Model]]", "[[extracts/youtube/ai-learning/2026-09-11-create-anything-with-nano-banana-pro-heres-how--2VktR2fAmF0|Create Anything with Nano Banana Pro, Here’s How]]", "[[extracts/youtube/ai-learning/2026-09-11-bolt-vs-lovable-which-ai-app-builder-comes-out-on-top--yHDvCGNjIqk|Bolt vs Lovable: which AI app builder comes out on top?]]"]
---

# Build a NEW $100K/Month A.I SaaS WITH ME in 20 minutes (No-code Is INSANE)

## Tese
Um app de rastreamento calórico por foto (clone do Cal AI, que fatura US$1,12M/mês) pode ser construído sem código via engenharia de prompts iterativa no Bolt usando a API multimodal GPT-4o da OpenAI.

## Conceitos-chave
- desenvolvimento no-code via prompts iterativos
- API multimodal de visão (imagem + texto)
- migração de modelo deprecado (GPT-4 Vision Preview -> GPT-4o)
- saída estruturada em JSON para parsing
- rastreamento de macros (calorias, proteína, gordura, carboidratos)
- gamificação com calendário verde/vermelho por metas diárias
- consistência de captura de foto (distância fixa de ~30cm do prato)
- codificação de imagem em base64
- depuração iterativa colando trechos da documentação da API
- autenticação de usuários e isolamento de dados por conta
- monetização por assinatura (Stripe)

## Ferramentas & pessoas
**Ferramentas:** Bolt (bolt.new), OpenAI API, GPT-4o, GPT-4 Vision Preview (deprecado), ChatGPT, Claude API, Cal AI, Clonify, Stripe, No Code Academy

**Pessoas/orgs:** OpenAI, Anthropic, Cal AI (fundador), No Code Academy, Tesla

## Claims acionáveis
- Usar GPT-4o em vez do modelo deprecado GPT-4 Vision Preview é necessário para análise multimodal de imagens de comida
- Copiar o formato exato do 'image input request' da documentação da OpenAI corrige erros de análise de imagem no app gerado
- Instruir o usuário a fotografar a ~1 pé (30cm) do prato torna a análise de macros mais consistente
- Exigir no prompt que o modelo responda apenas com JSON em formato exato permite encaminhar os dados para outros componentes da aplicação
- O app Cal AI original gera aproximadamente US$1,12 milhão por mês com funcionalidade de rastreamento calórico por foto
- A conversão da imagem para base64 na URL nem sempre é necessária e pode ser removida quando causa falhas
- O ciclo prompt -> teste -> relatar erro -> novo prompt no Bolt permite adicionar funcionalidades (metas diárias, calendário, timer, histórico) sem escrever código
- Próximos passos naturais do produto: autenticação para isolar dados por usuário, página de preços e cobrança recorrente via Stripe, e notificações push para retenção

> **Deep dive:** `low` — Tutorial no-code essencialmente promocional: os insights limitam-se a correções pontuais de API (modelo deprecado, formato de request) e prompt engineering básico, sem densidade arquitetural nem novidade em harness, evals, context-engineering ou governança.
