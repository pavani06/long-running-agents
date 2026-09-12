---
title: "Google's 9 Hour AI Prompt Engineering Course In 20 Minutes"
type: "extract"
source: "youtube"
video_id: "p09yRj47kNM"
url: "https://www.youtube.com/watch?v=p09yRj47kNM"
channel: "Tina Huang"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-google-s-9-hour-ai-prompt-engineering-course-in-20-minutes--p09yRj47kNM.txt]]"
tags: ["agents", "curriculo-conteudo", "context-engineering", "process", "verification", "analise"]
thesis: "Google's Prompting Essentials course condense a prática de prompting em um framework de cinco passos (Task, Context, References, Evaluate, Iterate) e o estende com técnicas avançadas (prompt chaining, chain of thought, tree of thought, meta-prompting) até uma receita de cinco passos para criar agentes de simulação e feedback especializado."
concepts: ["framework de prompting em 5 passos (Task, Context, References, Evaluate, Iterate)", "persona", "formato de saída", "referências / few-shot examples", "métodos de iteração de prompt", "prompting multimodal", "alucinações", "viés em LLMs", "human-in-the-loop", "prompt chaining", "chain of thought", "tree of thought", "meta-prompting", "agentes de IA", "Agent Sim (agente de simulação/role-play)", "Agent X (agente de feedback especializado)", "stop phrase", "biblioteca de prompts (prompt library)"]
tools: ["Google Prompting Essentials", "Gemini", "Google AI Studio", "Google Sheets", "Excel", "PowerPoint", "Google AI Essentials", "StraighterLine"]
people: ["Google", "StraighterLine (patrocinador do vídeo)"]
claims: ["Adicionar persona e formato de saída ao prompt gera resultados mais específicos e estruturados", "Quanto mais contexto fornecido, melhor tende a ser a saída do modelo", "Usar exemplos/referências (few-shot) resolve casos em que o resultado desejado é difícil de descrever em palavras", "Para iterar, aplicar um dos quatro métodos: revisitar o framework, quebrar o prompt em frases curtas, trocar por uma tarefa análoga, ou introduzir restrições", "Sempre verificar saídas com human-in-the-loop porque LLMs alucinam e carregam vieses humanos", "Não inserir dados sensíveis ou confidenciais da empresa em modelos de linguagem públicos", "Usar Google AI Studio quando a tarefa exigir janela de contexto maior (ex.: anexar manuscrito completo)", "Combinar chain of thought e tree of thought pedindo que o modelo explique o raciocínio a cada iteração/ramo", "Quando travar, usar meta-prompting: pedir à própria IA para escrever ou melhorar o prompt", "Criar agentes em 5 passos: persona, contexto detalhado do cenário, regras de interação, stop phrase e resumo final com feedback", "Guardar prompts úteis em uma biblioteca pessoal de prompts para reuso", "Revisar o conteúdo imediatamente após aprender melhora a retenção"]
deep_dive: "low"
deep_dive_reason: "É um resumo didático de curso introdutório: útil e com técnicas acionáveis básicas, mas sem densidade arquitetural, novidade ou profundidade em harness, evals, agent-fleets ou governança, além de conter segmento promocional."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ai-prompt-engineering-a-deep-dive--T9aRN5JkmL8|AI prompt engineering: A deep dive]]", "[[extracts/youtube/ai-learning/2026-09-11-state-of-the-art-prompting-for-ai-agents--DL82mGde6wo|State-Of-The-Art Prompting For AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-next-level-prompts-10-mins-into-advanced-prompting--69bH4IHZivs|\"Next Level Prompts?\" - 10 mins into advanced prompting]]", "[[extracts/youtube/ai-learning/2026-09-11-master-the-perfect-chatgpt-prompt-formula-in-just-8-minutes--jC4v5AS4RIM|Master the Perfect ChatGPT Prompt Formula (in just 8 minutes)!]]", "[[extracts/youtube/ai-learning/2026-09-11-prompting-101-code-w-claude--ysPbXH0LpIE|Prompting 101 | Code w/ Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-the-best-chatgpt-prompt-i-ve-ever-created-i-spent-2-months-curating-this-prompt--ABCqfaTjNd4|The best ChatGPT Prompt I've ever created - I spent 2 months curating this prompt to write prompts]]", "[[extracts/youtube/ai-learning/2026-09-11-the-master-prompt-method-build-your-ai-operating-system--yNpbnrlAFzA|The Master Prompt Method: Build Your AI Operating System]]", "[[extracts/youtube/ai-learning/2026-09-11-the-master-prompt-method-unlock-ais-full-potential-part-1--_K_F_icxtrI|The Master Prompt Method: Unlock AI’s Full Potential (Part 1)]]"]
theme: "Stack de IA e Prompting"
---

# Google's 9 Hour AI Prompt Engineering Course In 20 Minutes

## Tese
Google's Prompting Essentials course condense a prática de prompting em um framework de cinco passos (Task, Context, References, Evaluate, Iterate) e o estende com técnicas avançadas (prompt chaining, chain of thought, tree of thought, meta-prompting) até uma receita de cinco passos para criar agentes de simulação e feedback especializado.

## Conceitos-chave
- framework de prompting em 5 passos (Task, Context, References, Evaluate, Iterate)
- persona
- formato de saída
- referências / few-shot examples
- métodos de iteração de prompt
- prompting multimodal
- alucinações
- viés em LLMs
- human-in-the-loop
- prompt chaining
- chain of thought
- tree of thought
- meta-prompting
- agentes de IA
- Agent Sim (agente de simulação/role-play)
- Agent X (agente de feedback especializado)
- stop phrase
- biblioteca de prompts (prompt library)

## Ferramentas & pessoas
**Ferramentas:** Google Prompting Essentials, Gemini, Google AI Studio, Google Sheets, Excel, PowerPoint, Google AI Essentials, StraighterLine

**Pessoas/orgs:** Google, StraighterLine (patrocinador do vídeo)

## Claims acionáveis
- Adicionar persona e formato de saída ao prompt gera resultados mais específicos e estruturados
- Quanto mais contexto fornecido, melhor tende a ser a saída do modelo
- Usar exemplos/referências (few-shot) resolve casos em que o resultado desejado é difícil de descrever em palavras
- Para iterar, aplicar um dos quatro métodos: revisitar o framework, quebrar o prompt em frases curtas, trocar por uma tarefa análoga, ou introduzir restrições
- Sempre verificar saídas com human-in-the-loop porque LLMs alucinam e carregam vieses humanos
- Não inserir dados sensíveis ou confidenciais da empresa em modelos de linguagem públicos
- Usar Google AI Studio quando a tarefa exigir janela de contexto maior (ex.: anexar manuscrito completo)
- Combinar chain of thought e tree of thought pedindo que o modelo explique o raciocínio a cada iteração/ramo
- Quando travar, usar meta-prompting: pedir à própria IA para escrever ou melhorar o prompt
- Criar agentes em 5 passos: persona, contexto detalhado do cenário, regras de interação, stop phrase e resumo final com feedback
- Guardar prompts úteis em uma biblioteca pessoal de prompts para reuso
- Revisar o conteúdo imediatamente após aprender melhora a retenção

> **Deep dive:** `low` — É um resumo didático de curso introdutório: útil e com técnicas acionáveis básicas, mas sem densidade arquitetural, novidade ou profundidade em harness, evals, agent-fleets ou governança, além de conter segmento promocional.
