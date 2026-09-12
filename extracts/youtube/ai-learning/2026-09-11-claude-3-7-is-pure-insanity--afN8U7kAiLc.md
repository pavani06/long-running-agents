---
title: "Claude 3.7 is pure insanity"
type: "extract"
source: "youtube"
video_id: "afN8U7kAiLc"
url: "https://www.youtube.com/watch?v=afN8U7kAiLc"
channel: "AI Search"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-claude-3-7-is-pure-insanity--afN8U7kAiLc.txt]]"
tags: ["analise", "model-selection", "agentic-coding", "stack-tooling", "agents", "evals"]
thesis: "O vídeo é uma review demonstrativa do Claude 3.7 Sonnet, destacando sua força em geração one-shot de código e visualizações interativas (three.js, p5.js, Phaser.js), seu modo extended thinking e liderança em benchmarks de coding, mas com limitações severas como ausência de geração de imagens, modo de voz e busca na web."
concepts: ["Modelo híbrido de raciocínio (hybrid reasoning)", "Extended thinking / modo de pensamento estendido", "Geração de código one-shot em arquivo HTML standalone", "Frases-chave de prompt para melhorar qualidade estética e controles interativos", "Artifacts com preview ao vivo de código", "Simulações com regras de IA (colônia de formigas com trilhas de feromônio)", "Método de Monte Carlo para aproximação de pi", "Clonagem de sites a partir de screenshots", "Comparação entre leaderboards auto-reportados e independentes", "Limitações: censura, sem busca na web, sem voz, sem geração de imagens"]
tools: ["Claude 3.7 Sonnet", "Claude 3.5", "claude.ai", "Monica", "ChatLLM (Abacus AI)", "Poe", "Cursor", "three.js", "p5.js", "p5.js Web Editor", "Phaser.js", "Hugging Face", "HubSpot (recurso gratuito de prompts)", "DeepSeek R1", "OpenAI o1", "OpenAI o3 mini", "GPT-4.5", "Grok 3", "Gemini", "Qwen", "LiveBench", "LMArena", "Artificial Analysis", "Humanity's Last Exam", "Notepad"]
people: ["Anthropic", "HubSpot", "OpenAI", "DeepSeek", "Abacus AI", "Hugging Face", "Google (Gemini)", "xAI (Grok)"]
claims: ["Usar frases-chave como 'make it visually appealing', 'use CSS JS and HTML in a single HTML file' e 'include controls the user can adjust in real time' melhora consistentemente a qualidade e a interatividade do código gerado", "Bibliotecas como three.js, Phaser.js e p5.js frequentemente não renderizam no preview de artifacts do Claude; copie o código para um arquivo HTML standalone ou use o editor online de p5.js para visualizar", "Quando a resposta atinge o comprimento máximo, digitar 'continue from the end' faz o modelo retomar o código de onde parou", "Claude 3.7 Sonet pontuou 62.3% no benchmark de software engineering, muito acima de o3 mini high (49.3%) e DeepSeek R1 (49.2%), sendo atualmente o melhor modelo para coding segundo benchmarks auto-reportados", "Sem extended thinking, o Claude 3.7 fica abaixo de o1, DeepSeek R1 e Grok 3 em questões de nível de pós-graduação; com o modo ativado, iguala o Grok 3", "O extended thinking está disponível apenas em planos pagos e permite inspecionar o processo de raciocínio do modelo", "Claude 3.7 não gera imagens, não tem modo de voz e não busca na web, com cutoff de conhecimento em outubro de 2024 — limitações críticas para pesquisa atualizada", "O claude.ai exige número de telefone para criar conta; alternativas como Monica, ChatLLM (Abacus AI) e Poe não exigem", "O Claude 3.7 consegue construir em um único prompt um jogo estilo Minecraft com castelo construído autonomamente, algo que o1 e Grok 3 não alcançaram em uma tentativa", "Resultados divergem entre leaderboards: no LiveBench o Claude 3.7 thinking lidera (76), mas no Artificial Analysis aparece em 8º lugar e mais caro por milhão de tokens, evidenciando a necessidade de consultar múltiplas fontes"]
deep_dive: "low"
deep_dive_reason: "Conteúdo é uma review entusiasta e promocional de produto, com demonstrações superficiais e insights limitados a frases de prompt e números de benchmark, sem profundidade arquitetural em harness, context-engineering, evals ou governança de agentes."
---

# Claude 3.7 is pure insanity

## Tese
O vídeo é uma review demonstrativa do Claude 3.7 Sonnet, destacando sua força em geração one-shot de código e visualizações interativas (three.js, p5.js, Phaser.js), seu modo extended thinking e liderança em benchmarks de coding, mas com limitações severas como ausência de geração de imagens, modo de voz e busca na web.

## Conceitos-chave
- Modelo híbrido de raciocínio (hybrid reasoning)
- Extended thinking / modo de pensamento estendido
- Geração de código one-shot em arquivo HTML standalone
- Frases-chave de prompt para melhorar qualidade estética e controles interativos
- Artifacts com preview ao vivo de código
- Simulações com regras de IA (colônia de formigas com trilhas de feromônio)
- Método de Monte Carlo para aproximação de pi
- Clonagem de sites a partir de screenshots
- Comparação entre leaderboards auto-reportados e independentes
- Limitações: censura, sem busca na web, sem voz, sem geração de imagens

## Ferramentas & pessoas
**Ferramentas:** Claude 3.7 Sonnet, Claude 3.5, claude.ai, Monica, ChatLLM (Abacus AI), Poe, Cursor, three.js, p5.js, p5.js Web Editor, Phaser.js, Hugging Face, HubSpot (recurso gratuito de prompts), DeepSeek R1, OpenAI o1, OpenAI o3 mini, GPT-4.5, Grok 3, Gemini, Qwen, LiveBench, LMArena, Artificial Analysis, Humanity's Last Exam, Notepad

**Pessoas/orgs:** Anthropic, HubSpot, OpenAI, DeepSeek, Abacus AI, Hugging Face, Google (Gemini), xAI (Grok)

## Claims acionáveis
- Usar frases-chave como 'make it visually appealing', 'use CSS JS and HTML in a single HTML file' e 'include controls the user can adjust in real time' melhora consistentemente a qualidade e a interatividade do código gerado
- Bibliotecas como three.js, Phaser.js e p5.js frequentemente não renderizam no preview de artifacts do Claude; copie o código para um arquivo HTML standalone ou use o editor online de p5.js para visualizar
- Quando a resposta atinge o comprimento máximo, digitar 'continue from the end' faz o modelo retomar o código de onde parou
- Claude 3.7 Sonet pontuou 62.3% no benchmark de software engineering, muito acima de o3 mini high (49.3%) e DeepSeek R1 (49.2%), sendo atualmente o melhor modelo para coding segundo benchmarks auto-reportados
- Sem extended thinking, o Claude 3.7 fica abaixo de o1, DeepSeek R1 e Grok 3 em questões de nível de pós-graduação; com o modo ativado, iguala o Grok 3
- O extended thinking está disponível apenas em planos pagos e permite inspecionar o processo de raciocínio do modelo
- Claude 3.7 não gera imagens, não tem modo de voz e não busca na web, com cutoff de conhecimento em outubro de 2024 — limitações críticas para pesquisa atualizada
- O claude.ai exige número de telefone para criar conta; alternativas como Monica, ChatLLM (Abacus AI) e Poe não exigem
- O Claude 3.7 consegue construir em um único prompt um jogo estilo Minecraft com castelo construído autonomamente, algo que o1 e Grok 3 não alcançaram em uma tentativa
- Resultados divergem entre leaderboards: no LiveBench o Claude 3.7 thinking lidera (76), mas no Artificial Analysis aparece em 8º lugar e mais caro por milhão de tokens, evidenciando a necessidade de consultar múltiplas fontes

> **Deep dive:** `low` — Conteúdo é uma review entusiasta e promocional de produto, com demonstrações superficiais e insights limitados a frases de prompt e números de benchmark, sem profundidade arquitetural em harness, context-engineering, evals ou governança de agentes.
