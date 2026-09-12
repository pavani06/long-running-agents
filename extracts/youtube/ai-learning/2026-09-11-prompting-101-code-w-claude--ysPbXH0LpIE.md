---
title: "Prompting 101 | Code w/ Claude"
type: "extract"
source: "youtube"
video_id: "ysPbXH0LpIE"
url: "https://www.youtube.com/watch?v=ysPbXH0LpIE"
channel: "Anthropic"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-prompting-101-code-w-claude--ysPbXH0LpIE.txt]]"
tags: ["context-engineering", "context-management", "verification", "error-handling", "process", "decision-discipline", "analise", "curriculo-conteudo", "token-budgeting"]
thesis: "A equipe de AI aplicada da Anthropic demonstra, via um caso real de seguradora sueca de automóveis, que prompts de produção eficazes são construídos iterativamente estruturando contexto (papel, tom, esquema estático do documento no system prompt, instruções ordenadas, exemplos few-shot e lembretes finais) com tags XML, caching e formatação de saída para transformar Claude em um analista confiável de formulários manuscritos e sketches de acidentes."
concepts: ["prompt engineering como ciência empírica e iterativa", "estrutura de prompt: descrição da tarefa, conteúdo dinâmico, instruções detalhadas, exemplos, lembretes finais", "system prompt para conhecimento estático do documento (esquema do formulário)", "tags XML como delimitadores semânticos", "few-shot examples com imagens em base64", "prompt caching para conteúdo imutável", "preenchimento de resposta (prefill) para saída estruturada", "extended thinking como ferramenta de depuração do raciocínio", "mitigação de alucinação via exigência de confiança e citação de evidências", "ordem de análise de documentos (formulário estruturado antes do sketch ambíguo)", "calibração de confiança e recusa quando dados são ilegíveis", "histórico de conversa como contexto adicional", "temperature 0 para tarefas de extração determinística"]
tools: ["Anthropic Console", "Claude API", "Claude 4 Sonnet", "prompt caching", "extended thinking", "Claude plays Pokémon (demo citada)"]
people: ["Hannah (Anthropic, Applied AI)", "Christian (Anthropic, Applied AI)", "Anthropic", "seguradora de automóveis sueca (cliente anonimizado)"]
claims: ["Estruture prompts de tarefa única na ordem: descrição da tarefa/papel → conteúdo dinâmico → instruções passo a passo → exemplos → lembretes de diretrizes críticas.", "Coloque conhecimento estático (ex.: esquema de um formulário que nunca muda) no system prompt e use prompt caching, pois reduz esforço de interpretação e custo por query.", "Use tags XML para rotular seções do prompt, permitindo que o modelo referencie informações específicas posteriormente.", "Instrua o modelo a responder apenas quando confiante e a citar a evidência do documento (ex.: 'box 2 está marcado') para cada alegação factual, prevenindo alucinações.", "A ordem de análise importa: processe primeiro o artefato estruturado (formulário com checkboxes) e só depois o artefato ambíguo (sketch), cruzando os achados.", "Codifique casos difíceis rotulados por humanos como few-shot examples (inclusive imagens base64) no system prompt para conduzir o modelo em cenários cinzentos.", "Descreva imperfeições esperadas de preenchimento humano (círculos, rabiscos, X fora da caixa) para melhorar leitura de formulários manuscritos.", "Use prefill (ex.: '{' ou uma tag XML de abertura) para forçar saída serializável/parseável sem preâmbulo.", "Analise os transcripts de extended thinking como crutch de prompt engineering: revela como o modelo raciocina e informa melhorias no system prompt de forma mais token-eficiente.", "Configure temperature 0 e max tokens alto para tarefas de extração e julgamento determinísticos.", "Estabeleça casos de teste (ex.: 'deve reconhecer acidente veicular, não esqui') e refine o prompt iterativamente contra eles antes de implantar.", "Peça saída final encapsulada em tags específicas (ex.: <final_verdict>) para consumo direto por aplicações ou bancos de dados."]
deep_dive: "medium"
deep_dive_reason: "Conteúdo é um tutorial introdutório bem estruturado com conselhos acionáveis de context-engineering (system prompt, XML, prefill, caching, extended thinking), mas sem novidade arquitetural ou profundidade em harness/evals/agent-fleets que justifique tier alto."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ai-prompt-engineering-a-deep-dive--T9aRN5JkmL8|AI prompt engineering: A deep dive]]", "[[extracts/youtube/ai-learning/2026-09-11-the-prompting-playbook--G2B0YWuJUgI|The prompting playbook]]", "[[extracts/youtube/ai-learning/2026-09-11-state-of-the-art-prompting-for-ai-agents--DL82mGde6wo|State-Of-The-Art Prompting For AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-next-level-prompts-10-mins-into-advanced-prompting--69bH4IHZivs|\"Next Level Prompts?\" - 10 mins into advanced prompting]]", "[[extracts/youtube/ai-learning/2026-09-11-google-s-9-hour-ai-prompt-engineering-course-in-20-minutes--p09yRj47kNM|Google's 9 Hour AI Prompt Engineering Course In 20 Minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-the-master-prompt-method-unlock-ais-full-potential-part-1--_K_F_icxtrI|The Master Prompt Method: Unlock AI’s Full Potential (Part 1)]]"]
theme: "Stack de IA e Prompting"
---

# Prompting 101 | Code w/ Claude

## Tese
A equipe de AI aplicada da Anthropic demonstra, via um caso real de seguradora sueca de automóveis, que prompts de produção eficazes são construídos iterativamente estruturando contexto (papel, tom, esquema estático do documento no system prompt, instruções ordenadas, exemplos few-shot e lembretes finais) com tags XML, caching e formatação de saída para transformar Claude em um analista confiável de formulários manuscritos e sketches de acidentes.

## Conceitos-chave
- prompt engineering como ciência empírica e iterativa
- estrutura de prompt: descrição da tarefa, conteúdo dinâmico, instruções detalhadas, exemplos, lembretes finais
- system prompt para conhecimento estático do documento (esquema do formulário)
- tags XML como delimitadores semânticos
- few-shot examples com imagens em base64
- prompt caching para conteúdo imutável
- preenchimento de resposta (prefill) para saída estruturada
- extended thinking como ferramenta de depuração do raciocínio
- mitigação de alucinação via exigência de confiança e citação de evidências
- ordem de análise de documentos (formulário estruturado antes do sketch ambíguo)
- calibração de confiança e recusa quando dados são ilegíveis
- histórico de conversa como contexto adicional
- temperature 0 para tarefas de extração determinística

## Ferramentas & pessoas
**Ferramentas:** Anthropic Console, Claude API, Claude 4 Sonnet, prompt caching, extended thinking, Claude plays Pokémon (demo citada)

**Pessoas/orgs:** Hannah (Anthropic, Applied AI), Christian (Anthropic, Applied AI), Anthropic, seguradora de automóveis sueca (cliente anonimizado)

## Claims acionáveis
- Estruture prompts de tarefa única na ordem: descrição da tarefa/papel → conteúdo dinâmico → instruções passo a passo → exemplos → lembretes de diretrizes críticas.
- Coloque conhecimento estático (ex.: esquema de um formulário que nunca muda) no system prompt e use prompt caching, pois reduz esforço de interpretação e custo por query.
- Use tags XML para rotular seções do prompt, permitindo que o modelo referencie informações específicas posteriormente.
- Instrua o modelo a responder apenas quando confiante e a citar a evidência do documento (ex.: 'box 2 está marcado') para cada alegação factual, prevenindo alucinações.
- A ordem de análise importa: processe primeiro o artefato estruturado (formulário com checkboxes) e só depois o artefato ambíguo (sketch), cruzando os achados.
- Codifique casos difíceis rotulados por humanos como few-shot examples (inclusive imagens base64) no system prompt para conduzir o modelo em cenários cinzentos.
- Descreva imperfeições esperadas de preenchimento humano (círculos, rabiscos, X fora da caixa) para melhorar leitura de formulários manuscritos.
- Use prefill (ex.: '{' ou uma tag XML de abertura) para forçar saída serializável/parseável sem preâmbulo.
- Analise os transcripts de extended thinking como crutch de prompt engineering: revela como o modelo raciocina e informa melhorias no system prompt de forma mais token-eficiente.
- Configure temperature 0 e max tokens alto para tarefas de extração e julgamento determinísticos.
- Estabeleça casos de teste (ex.: 'deve reconhecer acidente veicular, não esqui') e refine o prompt iterativamente contra eles antes de implantar.
- Peça saída final encapsulada em tags específicas (ex.: <final_verdict>) para consumo direto por aplicações ou bancos de dados.

> **Deep dive:** `medium` — Conteúdo é um tutorial introdutório bem estruturado com conselhos acionáveis de context-engineering (system prompt, XML, prefill, caching, extended thinking), mas sem novidade arquitetural ou profundidade em harness/evals/agent-fleets que justifique tier alto.
