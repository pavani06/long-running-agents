---
title: "Did OpenAI just solve hallucinations?"
type: "extract"
source: "youtube"
video_id: "xGO5Q94XXf0"
url: "https://www.youtube.com/watch?v=xGO5Q94XXf0"
channel: "Matthew Berman"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-did-openai-just-solve-hallucinations--xGO5Q94XXf0.txt]]"
tags: ["analise", "evals", "verification", "gate-design", "decision-discipline", "error-handling", "multi-agent"]
thesis: "Alucinações em LLMs têm causa estrutural nos objetivos de treinamento e nas métricas binárias de avaliação que premiam 'blefe' em vez de abstenção, e podem ser mitigadas via calibração comportamental, limiares de confiança e recompensa por respostas 'não sei'."
concepts: ["alucinação em LLMs", "assimetria geração-verificação", "calibração comportamental", "limiar de confiança para responder", "abstenção ('não sei')", "blefe overconfidente e específico", "métricas binárias de avaliação (acurácia/pass rate)", "degradação de calibração causada por reinforcement learning", "calibração de modelos base", "esquema de pontuação assimétrico (+1 correto, 0 abstenção, negativo para erro)", "momentum de resposta (pressão por completude)", "analogia com provas de múltipla escolha (adivinhar maximiza score esperado)", "verificação por múltiplos agentes", "esparsidade de fatos raros no pré-treinamento (ex.: aniversários)"]
tools: ["GPQA", "MMLU Pro", "Wildbench", "Math", "SWE-bench", "GPT-5", "Notion AI for Work", "RAG", "busca/search", "reasoning/raciocínio"]
people: ["OpenAI", "Anthropic", "Elon Musk", "Notion", "Cole (usuário do Twitter)"]
claims: ["Mesmo com dados de treinamento perfeitamente limpos, os objetivos de otimização do treinamento gerariam erros — alucinação não é apenas herança de dados sujos.", "Verificar se uma resposta é válida é muito mais fácil do que gerá-la, pois há infinitamente mais respostas erradas do que certas.", "Agents revisores verificando saídas de outros agents produzem resultados melhores que geração em passagem única — explorável em pipelines de revisão/verificação.", "Modelos base podem ser bem calibrados, mas o reinforcement learning pós-treinamento os empurra para overconfiança e blefe.", "Benchmarks com correção binária (GPQA, MMLU Pro, Math, SWE-bench) premiam blefe; apenas Wildbench pontua abstenção.", "Para criadores de benchmark: adicionar limiares de confiança e pontuar +1 para resposta certa, 0 para 'não sei' e pontuação negativa para resposta errada.", "Para pós-treinamento: condicionar o modelo a responder apenas acima de um limiar de confiança (ex.: 75%), abstendo-se caso contrário.", "Testar honestidade via calibração comportacional: em 50% de confiança declarada a resposta deve estar correta ~50% das vezes; em 90%, ~90%.", "Ferramentas como search, RAG e reasoning reduzem mas não eliminam alucinações — a correção precisa acontecer na etapa de RL e nas avaliações.", "Fatos raros no pré-treinamento (ex.: ~20% de aniversários aparecendo uma única vez) implicam taxa mínima de alucinação proporcional em modelos base.", "GPT-5 já exibe comportamento de abstenção honesta ('não sei'), indicando adoção emergente dessa estratégia em produção.", "Alucinações são inevitáveis apenas para modelos base; sistemas de QA com banco de respostas e abstenção podem ser não-alucinantes por construção."]
deep_dive: "medium"
deep_dive_reason: "Breakdown divulgativo de paper relevante com implicações acionáveis concretas para design de evals e RL (limiares de confiança, pontuação de abstenção, calibração comportamental), mas sem profundidade arquitetural em harness, agentes ou implementação."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-i-trained-a-reasoning-language-model-with-rl-on-an-unverifiable-task--kxypcfrkUBI|I trained a Reasoning Language Model with RL on an unverifiable task]]", "[[extracts/youtube/ai-learning/2026-09-11-stop-hallucinations-best-n8n-ai-agent-settings-explained--pR51uBNb5es|Stop Hallucinations! Best n8n AI Agent Settings Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-on-what-comes-after-llms--ngBraLDqzdI|Yann LeCun on What Comes After LLMs]]", "[[extracts/youtube/ai-learning/2026-09-11-yann-lecun-s-1b-bet-against-llms-part-1--kYkIdXwW2AE|Yann LeCun's $1B Bet Against LLMs [Part 1]]]", "[[extracts/youtube/ai-learning/2026-09-11-hard-won-lessons-from-building-effective-ai-coding-agents-nik-pash-cline--I8fs4omN1no|Hard Won Lessons from Building Effective AI Coding Agents – Nik Pash, Cline]]", "[[extracts/youtube/ai-learning/2026-09-11-ilya-sutskever-we-re-moving-from-the-age-of-scaling-to-the-age-of-research--aR20FWCCjAs|Ilya Sutskever – We're moving from the age of scaling to the age of research]]"]
---

# Did OpenAI just solve hallucinations?

## Tese
Alucinações em LLMs têm causa estrutural nos objetivos de treinamento e nas métricas binárias de avaliação que premiam 'blefe' em vez de abstenção, e podem ser mitigadas via calibração comportamental, limiares de confiança e recompensa por respostas 'não sei'.

## Conceitos-chave
- alucinação em LLMs
- assimetria geração-verificação
- calibração comportamental
- limiar de confiança para responder
- abstenção ('não sei')
- blefe overconfidente e específico
- métricas binárias de avaliação (acurácia/pass rate)
- degradação de calibração causada por reinforcement learning
- calibração de modelos base
- esquema de pontuação assimétrico (+1 correto, 0 abstenção, negativo para erro)
- momentum de resposta (pressão por completude)
- analogia com provas de múltipla escolha (adivinhar maximiza score esperado)
- verificação por múltiplos agentes
- esparsidade de fatos raros no pré-treinamento (ex.: aniversários)

## Ferramentas & pessoas
**Ferramentas:** GPQA, MMLU Pro, Wildbench, Math, SWE-bench, GPT-5, Notion AI for Work, RAG, busca/search, reasoning/raciocínio

**Pessoas/orgs:** OpenAI, Anthropic, Elon Musk, Notion, Cole (usuário do Twitter)

## Claims acionáveis
- Mesmo com dados de treinamento perfeitamente limpos, os objetivos de otimização do treinamento gerariam erros — alucinação não é apenas herança de dados sujos.
- Verificar se uma resposta é válida é muito mais fácil do que gerá-la, pois há infinitamente mais respostas erradas do que certas.
- Agents revisores verificando saídas de outros agents produzem resultados melhores que geração em passagem única — explorável em pipelines de revisão/verificação.
- Modelos base podem ser bem calibrados, mas o reinforcement learning pós-treinamento os empurra para overconfiança e blefe.
- Benchmarks com correção binária (GPQA, MMLU Pro, Math, SWE-bench) premiam blefe; apenas Wildbench pontua abstenção.
- Para criadores de benchmark: adicionar limiares de confiança e pontuar +1 para resposta certa, 0 para 'não sei' e pontuação negativa para resposta errada.
- Para pós-treinamento: condicionar o modelo a responder apenas acima de um limiar de confiança (ex.: 75%), abstendo-se caso contrário.
- Testar honestidade via calibração comportacional: em 50% de confiança declarada a resposta deve estar correta ~50% das vezes; em 90%, ~90%.
- Ferramentas como search, RAG e reasoning reduzem mas não eliminam alucinações — a correção precisa acontecer na etapa de RL e nas avaliações.
- Fatos raros no pré-treinamento (ex.: ~20% de aniversários aparecendo uma única vez) implicam taxa mínima de alucinação proporcional em modelos base.
- GPT-5 já exibe comportamento de abstenção honesta ('não sei'), indicando adoção emergente dessa estratégia em produção.
- Alucinações são inevitáveis apenas para modelos base; sistemas de QA com banco de respostas e abstenção podem ser não-alucinantes por construção.

> **Deep dive:** `medium` — Breakdown divulgativo de paper relevante com implicações acionáveis concretas para design de evals e RL (limiares de confiança, pontuação de abstenção, calibração comportamental), mas sem profundidade arquitetural em harness, agentes ou implementação.
