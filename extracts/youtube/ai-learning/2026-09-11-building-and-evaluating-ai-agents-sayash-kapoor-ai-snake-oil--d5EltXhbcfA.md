---
title: "Building and evaluating AI Agents — Sayash Kapoor, AI Snake Oil"
type: "extract"
source: "youtube"
video_id: "d5EltXhbcfA"
url: "https://www.youtube.com/watch?v=d5EltXhbcfA"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-building-and-evaluating-ai-agents-sayash-kapoor-ai-snake-oil--d5EltXhbcfA.txt]]"
tags: ["evals", "agents", "verification", "model-selection", "testes-qa", "production", "analise"]
thesis: "Agentes de IA falham no mundo real principalmente porque a avaliação é genuinamente difícil, benchmarks estáticos são enganosos e capacidade (pass@k) é confundida com confiabilidade, exigindo que engenheiros de IA tratem o campo como engenharia de confiabilidade de sistemas, com custo e avaliação como cidadãos de primeira classe."
concepts: ["avaliação de agentes (evals como cidadão de primeira classe)", "fronteira de Pareto custo × acurácia", "paradoxo de Jevons aplicado a custo de inferência", "capacidade (pass@k) vs confiabilidade (consistência)", "lacuna de 90% para 99,999% ('cinco noves')", "verificadores com falsos positivos e curvas de inference scaling", "benchmarks estáticos vs ambientes de execução reais", "humano no loop editando critérios de avaliação de LLMs", "limitações de LLM-as-judge", "reward hacking em agentes", "métricas multidimensionais para agentes de propósito específico", "engenharia de IA como engenharia de confiabilidade (analogia ENIAC)", "agentes como componentes de produtos maiores, não produtos autônomos"]
tools: ["OpenAI Operator", "Deep Research (OpenAI)", "ChatGPT", "Claude 3.5", "OpenAI o1", "GPT-4o mini", "text-davinci-003", "DoNotPay", "LexisNexis", "Westlaw", "Sakana AI Scientist", "Agente de otimização de kernels CUDA da Sakana", "CORE-Bench", "HAL (Holistic Agent Leaderboard)", "SWE-bench", "Devin", "HumanEval", "MBPP", "ENIAC", "Humane Pin", "Rabbit R1", "DoorDash"]
people: ["Princeton (equipe do palestrante)", "Stanford (pesquisadores que auditaram produtos jurídicos)", "FTC", "Sakana AI", "Swyx", "Cognition", "Answer.ai", "Berkeley (autores de Who Validates the Validators)", "Jevons (economista)"]
claims: ["Trate avaliação como cidadã de primeira classe no toolkit de engenharia de IA; sem rigor, repetem-se falhas como a multa da FTC ao DoNotPay e as alucinações da LexisNexis/Westlaw", "Inclua custo como eixo explícito junto à acurácia em avaliações de agentes: na fronteira de Pareto, Claude 3.5 custou ~$57 vs ~$664 do o1 com desempenho comparável", "Desconfie de benchmarks estáticos: Devon do Cognition teve alto score no SWE-bench, mas a Answer.ai obteve sucesso em apenas 3 de 20 tarefas reais em um mês de uso", "Inclua especialistas de domínio humanos no loop para editar proativamente os critérios das avaliações com LLM, seguindo 'Who Validates the Validators'", "Otimize para confiabilidade (acerto consistente), não para capacidade (pass@k), ao implantar agentes em decisões consequenciais", "Contabilize falsos positivos em verificadores/unit tests (como os de HumanEval e MBPP), pois eles fazem as curvas de inference scaling dobrarem para baixo", "Espere o paradoxo de Jevons: mesmo com queda de preço por token, o uso agregado e o custo total de agentes tenderão a aumentar", "Enquadre a engenharia de IA como problema de design de sistemas para componentes estocásticos, análogo ao trabalho de confiabilidade dos engenheiros do ENIAC", "Construir avaliações que criam ambientes virtuais para ações de agentes é muito mais difícil que avaliações de input/output de LLMs puros"]
deep_dive: "medium"
deep_dive_reason: "A palestra sintetiza com densidade razoável insights acionáveis sobre evals, custo e confiabilidade de agentes, mas permanece em nível conceitual de keynote, sem profundidade arquitetural ou de implementação."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-agentic-evaluations-at-scale-for-everybody-nicholas-kang-michael-aaron-google-de--Ubwb6NzegyA|Agentic Evaluations at Scale, For Everybody — Nicholas Kang & Michael Aaron, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-the-maturity-phases-of-running-evals-phil-hetzel-braintrust--FB-MLPhL9Ms|The maturity phases of running evals — Phil Hetzel, Braintrust]]", "[[extracts/youtube/ai-learning/2026-09-11-why-senior-engineers-struggle-to-build-ai-agents-philipp-schmid-google-deepmind--3_gYbhABcAE|Why (Senior) Engineers Struggle to Build AI Agents — Philipp Schmid, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-the-production-ai-playbook-deploying-agents-at-enterprise-scale-sandipan-bhaumik--ObTPqBGsEbA|The Production AI Playbook: Deploying Agents at Enterprise Scale — Sandipan Bhaumik, Databricks]]", "[[extracts/youtube/ai-learning/2026-09-11-hard-won-lessons-from-building-effective-ai-coding-agents-nik-pash-cline--I8fs4omN1no|Hard Won Lessons from Building Effective AI Coding Agents – Nik Pash, Cline]]", "[[extracts/youtube/ai-learning/2026-09-11-don-t-ship-skills-without-evals-philipp-schmid-google-deepmind--0vphxNt4wyk|Don't Ship Skills Without Evals — Philipp Schmid, Google DeepMind]]"]
---

# Building and evaluating AI Agents — Sayash Kapoor, AI Snake Oil

## Tese
Agentes de IA falham no mundo real principalmente porque a avaliação é genuinamente difícil, benchmarks estáticos são enganosos e capacidade (pass@k) é confundida com confiabilidade, exigindo que engenheiros de IA tratem o campo como engenharia de confiabilidade de sistemas, com custo e avaliação como cidadãos de primeira classe.

## Conceitos-chave
- avaliação de agentes (evals como cidadão de primeira classe)
- fronteira de Pareto custo × acurácia
- paradoxo de Jevons aplicado a custo de inferência
- capacidade (pass@k) vs confiabilidade (consistência)
- lacuna de 90% para 99,999% ('cinco noves')
- verificadores com falsos positivos e curvas de inference scaling
- benchmarks estáticos vs ambientes de execução reais
- humano no loop editando critérios de avaliação de LLMs
- limitações de LLM-as-judge
- reward hacking em agentes
- métricas multidimensionais para agentes de propósito específico
- engenharia de IA como engenharia de confiabilidade (analogia ENIAC)
- agentes como componentes de produtos maiores, não produtos autônomos

## Ferramentas & pessoas
**Ferramentas:** OpenAI Operator, Deep Research (OpenAI), ChatGPT, Claude 3.5, OpenAI o1, GPT-4o mini, text-davinci-003, DoNotPay, LexisNexis, Westlaw, Sakana AI Scientist, Agente de otimização de kernels CUDA da Sakana, CORE-Bench, HAL (Holistic Agent Leaderboard), SWE-bench, Devin, HumanEval, MBPP, ENIAC, Humane Pin, Rabbit R1, DoorDash

**Pessoas/orgs:** Princeton (equipe do palestrante), Stanford (pesquisadores que auditaram produtos jurídicos), FTC, Sakana AI, Swyx, Cognition, Answer.ai, Berkeley (autores de Who Validates the Validators), Jevons (economista)

## Claims acionáveis
- Trate avaliação como cidadã de primeira classe no toolkit de engenharia de IA; sem rigor, repetem-se falhas como a multa da FTC ao DoNotPay e as alucinações da LexisNexis/Westlaw
- Inclua custo como eixo explícito junto à acurácia em avaliações de agentes: na fronteira de Pareto, Claude 3.5 custou ~$57 vs ~$664 do o1 com desempenho comparável
- Desconfie de benchmarks estáticos: Devon do Cognition teve alto score no SWE-bench, mas a Answer.ai obteve sucesso em apenas 3 de 20 tarefas reais em um mês de uso
- Inclua especialistas de domínio humanos no loop para editar proativamente os critérios das avaliações com LLM, seguindo 'Who Validates the Validators'
- Otimize para confiabilidade (acerto consistente), não para capacidade (pass@k), ao implantar agentes em decisões consequenciais
- Contabilize falsos positivos em verificadores/unit tests (como os de HumanEval e MBPP), pois eles fazem as curvas de inference scaling dobrarem para baixo
- Espere o paradoxo de Jevons: mesmo com queda de preço por token, o uso agregado e o custo total de agentes tenderão a aumentar
- Enquadre a engenharia de IA como problema de design de sistemas para componentes estocásticos, análogo ao trabalho de confiabilidade dos engenheiros do ENIAC
- Construir avaliações que criam ambientes virtuais para ações de agentes é muito mais difícil que avaliações de input/output de LLMs puros

> **Deep dive:** `medium` — A palestra sintetiza com densidade razoável insights acionáveis sobre evals, custo e confiabilidade de agentes, mas permanece em nível conceitual de keynote, sem profundidade arquitetural ou de implementação.
