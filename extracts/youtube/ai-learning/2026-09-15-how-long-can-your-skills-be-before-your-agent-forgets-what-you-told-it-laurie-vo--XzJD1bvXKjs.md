---
title: "How long can your skills be before your agent forgets what you told it? — Laurie Voss, Arize AI"
type: "extract"
source: "youtube"
video_id: "XzJD1bvXKjs"
url: "https://www.youtube.com/watch?v=XzJD1bvXKjs"
channel: "AI Engineer"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-15-how-long-can-your-skills-be-before-your-agent-forgets-what-you-told-it-laurie-vo--XzJD1bvXKjs.txt]]"
tags: ["evals", "verification", "context-engineering", "context-management", "token-budgeting", "model-selection", "monitoramento", "observability", "harness-engineering", "agent-context", "analise", "testes-qa"]
thesis: "A capacidade dos modelos de fronteira de seguir instruções simultâneas cresceu ~10x em um ano (de ~200-300 para 2.000-5.000 constraints), eliminando o problema de compressão de skills files e transformando o gargalo em verificação de saída e trade-off de custo/latência."
concepts: ["IFScale benchmark", "densidade de instruções (n) vs acurácia", "limite histórico de ~200 instruções", "expansão do benchmark de 500 para 10.000 palavras", "taxonomia de modos de falha por modelo", "falha silenciosa (half-finished output)", "context rot", "safety classifier sensível", "esgotamento de thinking tokens", "verificação via evals com LLM", "reordenamento/reescrita de instruções e confiabilidade", "sharding de skills em sub-agentes", "proxy task vs tarefa real"]
tools: ["IFScale", "Arise AI", "npm", "GPT 4.1", "Claude Sonnet 4", "Gemini 2.5 Pro", "GPT 5.5", "Claude Opus 4.7", "Gemini 3.1 Pro", "DeepSeek V4 Pro", "OpenAI safety filter", "Firebench", "CCR bench", "Guidebench", "GitHub (repo com código e dados)"]
people: ["Lori (palestrante, head de developer relations na Arise AI, cofundadora do npm Inc.)", "Dexter Horthy (origem da cifra de 200 instruções)", "Jeroslowitch e coautores (paper do IFScale)", "Chroma (pesquisa de context rot)", "OpenAI", "Anthropic (Claude)", "Google (Gemini)", "DeepSeek"]
claims: ["Fronteira de seguimento de instruções moveu-se ~10x em 12 meses: de 200-300 para 2.000-5.000 constraints simultâneas, dependendo do modelo", "Skills files podem agora ser muito longos: não é mais necessário comprimir instruções em subskills e labirintos de arquivos", "Um style guide completo (~2.000 regras de marca e legais) cabe num único prompt, dispensando sharding em dezenas de agentes especializados", "A nova pergunta de engenharia deixou de ser 'o modelo consegue?' e passou a ser 'vale o custo e a latência do prompt gigante?'", "Cada modelo tem um modo de falha distinto: DeepSeek esquece silenciosamente (~750 regras), Claude recusa no nível de API via safety classifier, Gemini consome todo o budget de thinking tokens sem gerar output, GPT 5.5 entrega meio-relatório polido e desiste declarando o pedido estúpido", "Falhas silenciosas (GPT 5.5) são mais perigosas que recusas ruidosas (Claude): só são detectáveis lendo o output inteiro ou monitorando com outro LLM (eval)", "Chroma (18 modelos): acurácia em inputs longos cai 30-50% bem antes do limite da janela de contexto, e texto coerente e bem estruturado falha mais que instruções embaralhadas aleatoriamente", "Paper com 46 modelos ('Revisiting the Reliability of LLMs in Instruction Following'): reescrita ou reordenação das mesmas instruções muda radicalmente a conformidade — capacidade subiu, confiabilidade não", "Suposições de engenharia sobre tamanho máximo de prompts/instruções feitas há mais de ~6 meses provavelmente estão desatualizadas e devem ser revalidadas", "O problema de compressão foi substituído por um problema de verificação, que não se resolve com prompt melhor e sim com evals checando o output toda execução", "Palavras que parecem perigosas em combinação (ex.: antraz + cianeto) disparam recusas do Claude; filtrar o vocabulário do teste com safety filter do OpenAI foi necessário para concluí-lo", "O benchmark original IFScale topava em 500 palavras e precisou ser estendido até 10.000 para encontrar o novo teto", "Pesquisa empírica replicável é barata: 2.300 chamadas em 7 modelos custaram US$29", "Modelos são descontinuados rápido: dos 10 modelos originais do paper só 3 ainda existiam via API um ano depois — não se apegue a modelos específicos"]
deep_dive: "high"
deep_dive_reason: "Apresenta achado empírico novo e quantitativo (salto de 10x no teto de instruções), taxonomia acionável de modos de falha por modelo e implicações diretas para design de harness, evals, context-engineering e verificação em produção."
theme: "MCP, RAG e Integração de Agentes"
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-to-understand-the-next-wave-of-ai-before-everyone-else-tibo-interview--4qjEgPojjzM|How to Understand the Next Wave of AI Before Everyone Else | Tibo Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-gpt-6-astra-fable-5-1-god-mode--KgKA0A3qlz0|GPT 6 Astra + Fable 5.1 = GOD MODE]]", "[[extracts/youtube/ai-learning/2026-09-11-tool-skill-or-subagent-decomposing-an-agent-that-outgrew-its-prompt--mWvtOHlZM-I|Tool, skill, or subagent? Decomposing an agent that outgrew its prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-the-ai-native-company-how-one-founder-becomes-a--Lri2LNYtERM|Stanford CS153 Frontier Systems | The AI Native Company: How One Founder Becomes a 1000x Engineer]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-i-trained-a-reasoning-language-model-with-rl-on-an-unverifiable-task--kxypcfrkUBI|I trained a Reasoning Language Model with RL on an unverifiable task]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs336-language-modeling-from-scratch-spring-2026-lecture-10-inference--EfM546A79aM|Stanford CS336 Language Modeling from Scratch | Spring 2026 | Lecture 10: Inference]]"]
---

# How long can your skills be before your agent forgets what you told it? — Laurie Voss, Arize AI

## Tese
A capacidade dos modelos de fronteira de seguir instruções simultâneas cresceu ~10x em um ano (de ~200-300 para 2.000-5.000 constraints), eliminando o problema de compressão de skills files e transformando o gargalo em verificação de saída e trade-off de custo/latência.

## Conceitos-chave
- IFScale benchmark
- densidade de instruções (n) vs acurácia
- limite histórico de ~200 instruções
- expansão do benchmark de 500 para 10.000 palavras
- taxonomia de modos de falha por modelo
- falha silenciosa (half-finished output)
- context rot
- safety classifier sensível
- esgotamento de thinking tokens
- verificação via evals com LLM
- reordenamento/reescrita de instruções e confiabilidade
- sharding de skills em sub-agentes
- proxy task vs tarefa real

## Ferramentas & pessoas
**Ferramentas:** IFScale, Arise AI, npm, GPT 4.1, Claude Sonnet 4, Gemini 2.5 Pro, GPT 5.5, Claude Opus 4.7, Gemini 3.1 Pro, DeepSeek V4 Pro, OpenAI safety filter, Firebench, CCR bench, Guidebench, GitHub (repo com código e dados)

**Pessoas/orgs:** Lori (palestrante, head de developer relations na Arise AI, cofundadora do npm Inc.), Dexter Horthy (origem da cifra de 200 instruções), Jeroslowitch e coautores (paper do IFScale), Chroma (pesquisa de context rot), OpenAI, Anthropic (Claude), Google (Gemini), DeepSeek

## Claims acionáveis
- Fronteira de seguimento de instruções moveu-se ~10x em 12 meses: de 200-300 para 2.000-5.000 constraints simultâneas, dependendo do modelo
- Skills files podem agora ser muito longos: não é mais necessário comprimir instruções em subskills e labirintos de arquivos
- Um style guide completo (~2.000 regras de marca e legais) cabe num único prompt, dispensando sharding em dezenas de agentes especializados
- A nova pergunta de engenharia deixou de ser 'o modelo consegue?' e passou a ser 'vale o custo e a latência do prompt gigante?'
- Cada modelo tem um modo de falha distinto: DeepSeek esquece silenciosamente (~750 regras), Claude recusa no nível de API via safety classifier, Gemini consome todo o budget de thinking tokens sem gerar output, GPT 5.5 entrega meio-relatório polido e desiste declarando o pedido estúpido
- Falhas silenciosas (GPT 5.5) são mais perigosas que recusas ruidosas (Claude): só são detectáveis lendo o output inteiro ou monitorando com outro LLM (eval)
- Chroma (18 modelos): acurácia em inputs longos cai 30-50% bem antes do limite da janela de contexto, e texto coerente e bem estruturado falha mais que instruções embaralhadas aleatoriamente
- Paper com 46 modelos ('Revisiting the Reliability of LLMs in Instruction Following'): reescrita ou reordenação das mesmas instruções muda radicalmente a conformidade — capacidade subiu, confiabilidade não
- Suposições de engenharia sobre tamanho máximo de prompts/instruções feitas há mais de ~6 meses provavelmente estão desatualizadas e devem ser revalidadas
- O problema de compressão foi substituído por um problema de verificação, que não se resolve com prompt melhor e sim com evals checando o output toda execução
- Palavras que parecem perigosas em combinação (ex.: antraz + cianeto) disparam recusas do Claude; filtrar o vocabulário do teste com safety filter do OpenAI foi necessário para concluí-lo
- O benchmark original IFScale topava em 500 palavras e precisou ser estendido até 10.000 para encontrar o novo teto
- Pesquisa empírica replicável é barata: 2.300 chamadas em 7 modelos custaram US$29
- Modelos são descontinuados rápido: dos 10 modelos originais do paper só 3 ainda existiam via API um ano depois — não se apegue a modelos específicos

> **Deep dive:** `high` — Apresenta achado empírico novo e quantitativo (salto de 10x no teto de instruções), taxonomia acionável de modos de falha por modelo e implicações diretas para design de harness, evals, context-engineering e verificação em produção.
