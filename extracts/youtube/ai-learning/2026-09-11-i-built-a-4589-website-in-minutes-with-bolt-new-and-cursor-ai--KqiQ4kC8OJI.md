---
title: "I Built a $4589 Website in Minutes with Bolt.new and Cursor AI!"
type: "extract"
source: "youtube"
video_id: "KqiQ4kC8OJI"
url: "https://www.youtube.com/watch?v=KqiQ4kC8OJI"
channel: "The Metaverse Guy"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-i-built-a-4589-website-in-minutes-with-bolt-new-and-cursor-ai--KqiQ4kC8OJI.txt]]"
tags: ["agentic-coding", "agent-tooling", "stack-tooling", "process", "model-selection", "token-budgeting"]
thesis: "O vídeo ensina um workflow de replicação de designs premium em que um screenshot de template é convertido pelo ChatGPT em prompt detalhado, gerado como código no bolt.new e refinado iterativamente com screenshots até o handoff final para o Cursor."
concepts: ["replicação de design a partir de imagem de referência", "cadeia/relé de prompts (ChatGPT → bolt.new → Cursor)", "loop de feedback visual com screenshots", "hero section como elemento central do design", "restrição de escopo em prompts para evitar regressões", "handoff de projeto entre ferramentas de IA", "stack gerada Vite + React + TypeScript", "setup automático de projeto vs edição incremental", "animação de imagens flutuantes (floating images)", "deploy local com npm install / npm run dev"]
tools: ["bolt.new", "ChatGPT (GPT-4o)", "Cursor (Composer)", "Webflow", "GoFullPage (extensão Chrome)", "compressjpg.com / PNG size reducer", "Vite", "React", "TypeScript", "Next.js", "npm", "v0.dev", "Vercel", "Visual Studio Code"]
people: ["metav sky (canal do YouTube do apresentador)", "Upwork"]
claims: ["Capture o template de referência com a extensão GoFullPage e gere um prompt detalhado no ChatGPT 4o descrevendo cores, gradientes, tipografia, header e hero antes de enviar ao bolt.new", "bolt.new limita uploads a ~5MB e screenshots a 8000px de dimensão; comprima a imagem e corte seções longas (ex.: footer separado) para contornar o erro", "Itere o design enviando ao bolt.new screenshots do resultado atual com instruções específicas (ex.: 'copie exatamente o fundo e a UI da hero section')", "Evite substituir imagens diretamente no bolt.new; baixe o código-fonte, adicione imagens na pasta public e use o Cursor Composer para inseri-las no código", "Restrinja o escopo dos prompts (ex.: 'não mude mais nada na hero section') para preservar o que já está correto", "Exporte o projeto do bolt.new (~41KB), rode npm install e npm run dev localmente e continue refinando no Cursor, que é mais barato em tokens e melhor para uploads de imagem", "O autor afirma que sites assim construídos em menos de 1 hora podem ser cobrados de clientes a US$5.000–10.000", "O projeto pode ser deployado na Vercel (tutorial separado) e um backend pode ser adicionado depois em Next.js", "Segundo o autor, o ChatGPT 4.1 preview não aceita upload de imagens, exigindo o modelo 4o para esse workflow", "bolt.new oferece cerca de 1 milhão de crédutos gratuitos, suficientes para o primeiro projeto"]
deep_dive: "low"
deep_dive_reason: "Tutorial introdutório e promocional (repetidos pedidos de inscrição) sobre uso de ferramentas no-code/low-code, sem densidade arquitetural nem relevância para harness, evals, context-engineering, agent-fleets ou governança."
---

# I Built a $4589 Website in Minutes with Bolt.new and Cursor AI!

## Tese
O vídeo ensina um workflow de replicação de designs premium em que um screenshot de template é convertido pelo ChatGPT em prompt detalhado, gerado como código no bolt.new e refinado iterativamente com screenshots até o handoff final para o Cursor.

## Conceitos-chave
- replicação de design a partir de imagem de referência
- cadeia/relé de prompts (ChatGPT → bolt.new → Cursor)
- loop de feedback visual com screenshots
- hero section como elemento central do design
- restrição de escopo em prompts para evitar regressões
- handoff de projeto entre ferramentas de IA
- stack gerada Vite + React + TypeScript
- setup automático de projeto vs edição incremental
- animação de imagens flutuantes (floating images)
- deploy local com npm install / npm run dev

## Ferramentas & pessoas
**Ferramentas:** bolt.new, ChatGPT (GPT-4o), Cursor (Composer), Webflow, GoFullPage (extensão Chrome), compressjpg.com / PNG size reducer, Vite, React, TypeScript, Next.js, npm, v0.dev, Vercel, Visual Studio Code

**Pessoas/orgs:** metav sky (canal do YouTube do apresentador), Upwork

## Claims acionáveis
- Capture o template de referência com a extensão GoFullPage e gere um prompt detalhado no ChatGPT 4o descrevendo cores, gradientes, tipografia, header e hero antes de enviar ao bolt.new
- bolt.new limita uploads a ~5MB e screenshots a 8000px de dimensão; comprima a imagem e corte seções longas (ex.: footer separado) para contornar o erro
- Itere o design enviando ao bolt.new screenshots do resultado atual com instruções específicas (ex.: 'copie exatamente o fundo e a UI da hero section')
- Evite substituir imagens diretamente no bolt.new; baixe o código-fonte, adicione imagens na pasta public e use o Cursor Composer para inseri-las no código
- Restrinja o escopo dos prompts (ex.: 'não mude mais nada na hero section') para preservar o que já está correto
- Exporte o projeto do bolt.new (~41KB), rode npm install e npm run dev localmente e continue refinando no Cursor, que é mais barato em tokens e melhor para uploads de imagem
- O autor afirma que sites assim construídos em menos de 1 hora podem ser cobrados de clientes a US$5.000–10.000
- O projeto pode ser deployado na Vercel (tutorial separado) e um backend pode ser adicionado depois em Next.js
- Segundo o autor, o ChatGPT 4.1 preview não aceita upload de imagens, exigindo o modelo 4o para esse workflow
- bolt.new oferece cerca de 1 milhão de crédutos gratuitos, suficientes para o primeiro projeto

> **Deep dive:** `low` — Tutorial introdutório e promocional (repetidos pedidos de inscrição) sobre uso de ferramentas no-code/low-code, sem densidade arquitetural nem relevância para harness, evals, context-engineering, agent-fleets ou governança.
