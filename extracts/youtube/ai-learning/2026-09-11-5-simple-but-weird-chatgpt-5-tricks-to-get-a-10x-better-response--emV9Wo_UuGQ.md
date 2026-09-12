---
title: "5 simple (but weird) ChatGPT-5 tricks to get a 10x better response"
type: "extract"
source: "youtube"
video_id: "emV9Wo_UuGQ"
url: "https://www.youtube.com/watch?v=emV9Wo_UuGQ"
channel: "Dylan Davis"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-5-simple-but-weird-chatgpt-5-tricks-to-get-a-10x-better-response--emV9Wo_UuGQ.txt]]"
tags: ["model-selection", "arquitetura", "context-engineering", "evals", "process", "stack-tooling", "analise"]
thesis: "A consolidação dos modelos OpenAI em uma arquitetura com roteador automático que escolhe modelo, nível de raciocínio e verbosidade amplia o gap de valor para usuários e exige prompt engineering deliberado — palavras-gatilho, especificidade, estrutura XML, otimizador de prompts e autorreflexão com rúbrica — para extrair o máximo do GPT-5."
concepts: ["consolidação de modelos (8 legados em 3: GPT-5, Thinking, Pro) e roteamento automático", "níveis de raciocínio configuráveis (minimal/low/medium/high)", "controle de verbosidade da resposta (low/medium/high)", "palavras-gatilho (trigger words) para elevar raciocínio", "value gap crescente entre leigos e experts em prompting", "especificidade lexical e ausência de contradições para evitar overreasoning", "prompts estruturados com tags XML (<context>, <task>, <format>)", "autorreflexão: rúbrica gerada pelo próprio modelo, autoavaliação 1-10 e iteração interna antes da resposta final"]
tools: ["ChatGPT", "GPT-5", "GPT-5 Thinking", "GPT-5 Pro", "OpenAI Prompt Optimizer (platform.openai.com)", "Custom GPTs", "GPT Projects", "XML", "modelos legados: GPT-4o, GPT-4.1, 4.1 mini, o4 mini, o4 mini-high, o3, o3 Pro"]
people: ["OpenAI", "MUA (patrocinador do vídeo)"]
claims: ["Um router intermediário analisa o pedido e o contexto e direciona a chamada para GPT-5, GPT-5 Thinking ou GPT-5 Pro, definindo também o nível de raciocínio e a verbosidade", "Palavras-gatilho como 'think deeply', 'double check your work', 'be extremely thorough' e 'this is critical' aumentam o raciocínio aplicado e tendem a rotear para modelos maiores", "O Prompt Optimizer em platform.openai.com reescreve prompts aplicando boas práticas (eliminar vagueza, contradições, estruturar) por cerca de US$1-2 em créditos de API, explicando cada mudança feita", "Contradições e termos vagos no prompt fazem o GPT-5 overreasonar e se confundir sobre qual direção seguir", "Estruturar prompts em seções XML (<context>, <task>, <format>) melhora a compreensão das instruções pelo modelo; pode-se pedir à própria IA que converta o prompt em XML", "Instruir o modelo a criar uma rúbrica baseada na intenção, avaliar seus rascunhos de 1 a 10 e iterar internamente 2-5 vezes antes de responder eleva a qualidade da única saída retornada ao usuário", "A consolidação de 8 modelos em 3 aumentou drasticamente o gap de valor entre usuários que sabem e não sabem promptear"]
deep_dive: "low"
deep_dive_reason: "Vídeo tutorial consumidor de dicas de prompting com segmentos promocionais e técnicas amplamente conhecidas, sem densidade arquitetural nova em harness, evals ou governança de agentes."
---

# 5 simple (but weird) ChatGPT-5 tricks to get a 10x better response

## Tese
A consolidação dos modelos OpenAI em uma arquitetura com roteador automático que escolhe modelo, nível de raciocínio e verbosidade amplia o gap de valor para usuários e exige prompt engineering deliberado — palavras-gatilho, especificidade, estrutura XML, otimizador de prompts e autorreflexão com rúbrica — para extrair o máximo do GPT-5.

## Conceitos-chave
- consolidação de modelos (8 legados em 3: GPT-5, Thinking, Pro) e roteamento automático
- níveis de raciocínio configuráveis (minimal/low/medium/high)
- controle de verbosidade da resposta (low/medium/high)
- palavras-gatilho (trigger words) para elevar raciocínio
- value gap crescente entre leigos e experts em prompting
- especificidade lexical e ausência de contradições para evitar overreasoning
- prompts estruturados com tags XML (<context>, <task>, <format>)
- autorreflexão: rúbrica gerada pelo próprio modelo, autoavaliação 1-10 e iteração interna antes da resposta final

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, GPT-5, GPT-5 Thinking, GPT-5 Pro, OpenAI Prompt Optimizer (platform.openai.com), Custom GPTs, GPT Projects, XML, modelos legados: GPT-4o, GPT-4.1, 4.1 mini, o4 mini, o4 mini-high, o3, o3 Pro

**Pessoas/orgs:** OpenAI, MUA (patrocinador do vídeo)

## Claims acionáveis
- Um router intermediário analisa o pedido e o contexto e direciona a chamada para GPT-5, GPT-5 Thinking ou GPT-5 Pro, definindo também o nível de raciocínio e a verbosidade
- Palavras-gatilho como 'think deeply', 'double check your work', 'be extremely thorough' e 'this is critical' aumentam o raciocínio aplicado e tendem a rotear para modelos maiores
- O Prompt Optimizer em platform.openai.com reescreve prompts aplicando boas práticas (eliminar vagueza, contradições, estruturar) por cerca de US$1-2 em créditos de API, explicando cada mudança feita
- Contradições e termos vagos no prompt fazem o GPT-5 overreasonar e se confundir sobre qual direção seguir
- Estruturar prompts em seções XML (<context>, <task>, <format>) melhora a compreensão das instruções pelo modelo; pode-se pedir à própria IA que converta o prompt em XML
- Instruir o modelo a criar uma rúbrica baseada na intenção, avaliar seus rascunhos de 1 a 10 e iterar internamente 2-5 vezes antes de responder eleva a qualidade da única saída retornada ao usuário
- A consolidação de 8 modelos em 3 aumentou drasticamente o gap de valor entre usuários que sabem e não sabem promptear

> **Deep dive:** `low` — Vídeo tutorial consumidor de dicas de prompting com segmentos promocionais e técnicas amplamente conhecidas, sem densidade arquitetural nova em harness, evals ou governança de agentes.
