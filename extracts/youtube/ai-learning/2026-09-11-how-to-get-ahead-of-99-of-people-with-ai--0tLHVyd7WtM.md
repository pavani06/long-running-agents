---
title: "How to Get Ahead of 99% of People (with AI)"
type: "extract"
source: "youtube"
video_id: "0tLHVyd7WtM"
url: "https://www.youtube.com/watch?v=0tLHVyd7WtM"
channel: "Dan Martell"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-to-get-ahead-of-99-of-people-with-ai--0tLHVyd7WtM.txt]]"
tags: ["context-engineering", "context-management", "stack-tooling", "process", "knowledge-management", "agent-tooling"]
thesis: "O uso avançado do ChatGPT depende de empilhar camadas de contexto persistente (master prompt, custom instructions, projects) e destilar system prompts a partir de saídas iteradas em canvas, encapsulando o resultado em custom GPTs para tarefas repetíveis."
concepts: ["master prompt (documento de preferências e contexto do usuário)", "system prompt (define o comportamento desejado do modelo)", "custom instructions (padrões de formato/voz aplicados a todo chat)", "projects/pastas de projeto (contexto persistente por área)", "canvases (edição iterativa sem reescrever do zero)", "engenharia reversa de prompts (pedir ao modelo o system prompt que geraria a saída ideal)", "custom GPTs (encapsular system prompts como ferramentas compartilháveis)", "prompt como propriedade intelectual do negócio", "habit stacking para adoção de IA", "mitigação de alucinação via refinação iterativa"]
tools: ["ChatGPT", "ChatGPT Pro", "Canvases", "Projects", "Custom Instructions", "Custom GPTs", "GPT Store", "dictação por voz (voice-to-text)"]
people: ["Rob Dyrdek", "Gary Vaynerchuk", "Sara Blakely", "Google (cofundador não nomeado, sobre ameaçar modelos)"]
claims: ["Assinar ChatGPT Pro desbloqueia os recursos necessários para os hacks apresentados", "Gere seu master prompt pedindo ao próprio ChatGPT para entrevistá-lo (via dictação de voz) sobre cargo, contexto da empresa, valores, restrições e visão, e salve como PDF para anexar em toda sessão", "Refine a saída desejada em um canvas e então peça ao modelo que escreva o system prompt que teria gerado aquela saída desde o início; esse prompt vira ativo reutilizável", "Use Projects para concentrar documentos e histórico por área (ex.: compra de imóvel, finanças, contratações), evitando reexplicar contexto a cada chat", "Configure custom instructions (somente via desktop) para fixar formato, tom e remoção de vícios de linguagem do modelo em todas as conversas", "Converta system prompts validados em custom GPTs para padronizar tarefas repetíveis do time, com atualização centralizada e possibilidade de monetização no GPT Store", "Segundo clipe citado do cofundador do Google, ameaçar modelos pode melhorar a conformidade das respostas (afirmação não verificada)", "Use canvases para editar saídas manualmente e ajustar nível de leitura e comprimento sem que o modelo reescreva tudo do zero", "Empilhe hábitos: anexe o uso de IA a uma rotina diária existente para torná-la comportamento padrão", "Meta de delegar ~92% do trabalho repetível à IA, reservando ~8% para o toque humano"]
deep_dive: "low"
deep_dive_reason: "Apesar de algumas técnicas práticas de gestão de contexto (master prompt, system prompt reverso, projects), o conteúdo é um listicle promocional de nível iniciante, sem profundidade arquitetural nem relevância para harness, evals ou agent-fleets."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-master-prompt-method-unlock-ais-full-potential-part-1--_K_F_icxtrI|The Master Prompt Method: Unlock AI’s Full Potential (Part 1)]]", "[[extracts/youtube/ai-learning/2026-09-11-5-simple-but-weird-chatgpt-5-tricks-to-get-a-10x-better-response--emV9Wo_UuGQ|5 simple (but weird) ChatGPT-5 tricks to get a 10x better response]]", "[[extracts/youtube/ai-learning/2026-09-11-7-mind-blowing-new-use-cases-for-chatgpt-in-2025-big-changes-ahead--8IUkOAvMP-M|7 Mind-Blowing NEW Use Cases For ChatGPT in 2025 (Big Changes Ahead)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-master-prompt-method-build-your-ai-operating-system--yNpbnrlAFzA|The Master Prompt Method: Build Your AI Operating System]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-master-ai-powered-creativity-in-just-13-minutes-jeremy-utley--wv779vmyPVY|How to Master AI Powered Creativity in Just 13 Minutes | Jeremy Utley]]", "[[extracts/youtube/ai-learning/2026-09-11-5-notebooklm-hacks-that-will-blow-your-mind--Es5Qb9weRmA|5 NotebookLM Hacks That Will Blow Your Mind!]]", "[[extracts/youtube/ai-learning/2026-09-11-chatgpt-for-business-updates--9lSRViLugE0|ChatGPT for Business Updates]]", "[[extracts/youtube/ai-learning/2026-09-11-9-usos-do-notebooklm-que-vao-explodir-sua-cabeca-incrivel--WFD2wMiduIE|9 USOS do NotebookLM que vão EXPLODIR SUA CABEÇA (INCRÍVEL!!!)]]", "[[extracts/youtube/ai-learning/2026-09-11-learn-80-of-notebooklm-in-under-13-minutes--EOmgC3-hznM|Learn 80% of NotebookLM in Under 13 Minutes!]]", "[[extracts/youtube/ai-learning/2026-09-11-gpt-builder-2-0-upgrade-custom-gpt-with-parallel-function-calling-advanced-gpts--kBFjvQxKnOs|GPT Builder 2.0 🚀 UPGRADE Custom GPT with Parallel Function Calling 🤯 Advanced GPTs Tutorial]]", "[[extracts/youtube/ai-learning/2026-09-11-let-s-build-gpt-from-scratch-in-code-spelled-out--kCc8FmEb1nY|Let's build GPT: from scratch, in code, spelled out.]]"]
theme: "Stack de IA e Prompting"
---

# How to Get Ahead of 99% of People (with AI)

## Tese
O uso avançado do ChatGPT depende de empilhar camadas de contexto persistente (master prompt, custom instructions, projects) e destilar system prompts a partir de saídas iteradas em canvas, encapsulando o resultado em custom GPTs para tarefas repetíveis.

## Conceitos-chave
- master prompt (documento de preferências e contexto do usuário)
- system prompt (define o comportamento desejado do modelo)
- custom instructions (padrões de formato/voz aplicados a todo chat)
- projects/pastas de projeto (contexto persistente por área)
- canvases (edição iterativa sem reescrever do zero)
- engenharia reversa de prompts (pedir ao modelo o system prompt que geraria a saída ideal)
- custom GPTs (encapsular system prompts como ferramentas compartilháveis)
- prompt como propriedade intelectual do negócio
- habit stacking para adoção de IA
- mitigação de alucinação via refinação iterativa

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, ChatGPT Pro, Canvases, Projects, Custom Instructions, Custom GPTs, GPT Store, dictação por voz (voice-to-text)

**Pessoas/orgs:** Rob Dyrdek, Gary Vaynerchuk, Sara Blakely, Google (cofundador não nomeado, sobre ameaçar modelos)

## Claims acionáveis
- Assinar ChatGPT Pro desbloqueia os recursos necessários para os hacks apresentados
- Gere seu master prompt pedindo ao próprio ChatGPT para entrevistá-lo (via dictação de voz) sobre cargo, contexto da empresa, valores, restrições e visão, e salve como PDF para anexar em toda sessão
- Refine a saída desejada em um canvas e então peça ao modelo que escreva o system prompt que teria gerado aquela saída desde o início; esse prompt vira ativo reutilizável
- Use Projects para concentrar documentos e histórico por área (ex.: compra de imóvel, finanças, contratações), evitando reexplicar contexto a cada chat
- Configure custom instructions (somente via desktop) para fixar formato, tom e remoção de vícios de linguagem do modelo em todas as conversas
- Converta system prompts validados em custom GPTs para padronizar tarefas repetíveis do time, com atualização centralizada e possibilidade de monetização no GPT Store
- Segundo clipe citado do cofundador do Google, ameaçar modelos pode melhorar a conformidade das respostas (afirmação não verificada)
- Use canvases para editar saídas manualmente e ajustar nível de leitura e comprimento sem que o modelo reescreva tudo do zero
- Empilhe hábitos: anexe o uso de IA a uma rotina diária existente para torná-la comportamento padrão
- Meta de delegar ~92% do trabalho repetível à IA, reservando ~8% para o toque humano

> **Deep dive:** `low` — Apesar de algumas técnicas práticas de gestão de contexto (master prompt, system prompt reverso, projects), o conteúdo é um listicle promocional de nível iniciante, sem profundidade arquitetural nem relevância para harness, evals ou agent-fleets.
