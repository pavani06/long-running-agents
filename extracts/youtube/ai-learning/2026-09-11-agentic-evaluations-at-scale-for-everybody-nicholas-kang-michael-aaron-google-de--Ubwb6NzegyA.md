---
title: "Agentic Evaluations at Scale, For Everybody — Nicholas Kang & Michael Aaron, Google DeepMind"
type: "extract"
source: "youtube"
video_id: "Ubwb6NzegyA"
url: "https://www.youtube.com/watch?v=Ubwb6NzegyA"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-agentic-evaluations-at-scale-for-everybody-nicholas-kang-michael-aaron-google-de--Ubwb6NzegyA.txt]]"
tags: ["evals", "harness", "verification", "testes-qa", "instituicoes", "analise", "production", "model-selection"]
thesis: "Kaggle argumenta que os evals de IA atuais estão quebrados — fragmentados, opacos, criados por uma fração mínima de especialistas — e apresenta quatro frentes (hackathons, exames padronizados para agentes, Game Arena PvP e uma plataforma comunitária de benchmarks) para democratizar e escalar a avaliação de agentes."
concepts: ["saturação de benchmarks", "transparência e verificabilidade de evals", "benchmarks PvP com pontuação ELO (não-saturáveis)", "pareamento Bradley-Terry para reduzir número de partidas", "harness vs. modelo como variável confundidora em evals", "evals comunitários e open source", "exames padronizados de agentes (SAT para agentes)", "asserções programáticas + LLM-as-judge", "jaggedness / bordas cognitivas dos modelos", "compaction via API distorcendo comparações de benchmark", "significância estatística em evals de jogos", "incentivização e gamificação (pontos/medalhas Kaggle) para criação de benchmarks", "avaliação de segurança baseline para agentes consumer", "comparação longitudinal de modelos sob deprecação rápida"]
tools: ["Kaggle", "Kaggle Game Arena", "Kaggle Benchmarks", "Kaggle Simulation Platform", "Kaggle Hackathons", "Agent Exams (MVP)", "OpenSpiel", "LLM model proxy (disponível no Colab)", "Colab", "SWE-bench Pro", "Braintrust", "OpenClaw", "Grok", "Claude (Sonnet 4)", "GitHub", "Morph LLM"]
people: ["Nick (PM, Kaggle Benchmarks)", "Michael (engenheiro de software, Kaggle)", "Google DeepMind (time AGI)", "Morph LLM", "Paige (criadora da tarefa de SVG do XKCD)", "Kaggle (comunidade de 30M+ usuários)", "Google"]
claims: ["Mais de 10 benchmarks de IA novos são publicados por dia e os leaderboards envelhecem rápido porque os autores migram para o próximo paper.", "Resultados de benchmark variam drasticamente conforme a configuração/orquestração: um laboratório obteve números superiores usando compaction disponível apenas na própria API, inviesando a comparação pública.", "Para significância estatística em pôquer foram necessárias ~400.000 mãos; esquemas de pareamento Bradley-Terry são a chave para reduzir o volume de partidas rodadas.", "Benchmarks PvP com ELO nunca saturam, pois sempre há um vencedor e um perdedor entre modelos em competição direta.", "No SWE-bench Pro os seis modelos de fronteira estão a poucos pontos percentuais entre si, mas o harness altera o desempenho em até 22% — ou seja, muitos evals medem o harness, não o modelo.", "O MVP de exames padronizados de agentes atraiu 500+ agentes avaliados na primeira semana sem promoção, indicando demanda reprimida por avaliação de agentes consumer antes da implantação.", "Existe um trade-off de calibração em exames: muito difíceis ninguém termina (tempo/custo); muito fáceis não geram sinal útil.", "Modelos mais recentes são mais aversos a risco e jogam pôquer pior que gerações anteriores — personalidades emergem nos jogos e são comparáveis em ELO.", "Agentes de IA ainda não julgam bem inovação/criatividade, tornando o julgamento humano especialista (e o alinhamento entre especialistas) necessário em hackathons e evals.", "Endpoints de modelos nem sempre são honestos sobre qual modelo roda por trás, dificultando comparações longitudinais conforme modelos são deprecados.", "Apenas ~30 mil pesquisadores criam evals para ~30 milhões de profissionais técnicos; lacunas de avaliação ampliam o 'jaggedness' entre capacidades sobre-humanas e medíocres dos modelos."]
deep_dive: "medium"
deep_dive_reason: "Apresentação panorâmica com insights acionáveis pontuais (variância de 22% por harness, viés de compaction, ~400k mãos para significância, Bradley-Terry), mas com densidade arquitetural e novidade limitadas fora do escopo de evals comunitários."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-building-and-evaluating-ai-agents-sayash-kapoor-ai-snake-oil--d5EltXhbcfA|Building and evaluating AI Agents — Sayash Kapoor, AI Snake Oil]]", "[[extracts/youtube/ai-learning/2026-09-11-hard-won-lessons-from-building-effective-ai-coding-agents-nik-pash-cline--I8fs4omN1no|Hard Won Lessons from Building Effective AI Coding Agents – Nik Pash, Cline]]", "[[extracts/youtube/ai-learning/2026-09-11-the-maturity-phases-of-running-evals-phil-hetzel-braintrust--FB-MLPhL9Ms|The maturity phases of running evals — Phil Hetzel, Braintrust]]", "[[extracts/youtube/ai-learning/2026-09-11-how-google-deepmind-runs-agents-at-scale-kp-sawhney-ian-ballantyne-google-deepmi--7gujZrJ9L5I|How Google DeepMind Runs Agents at Scale — KP Sawhney & Ian Ballantyne, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-don-t-ship-skills-without-evals-philipp-schmid-google-deepmind--0vphxNt4wyk|Don't Ship Skills Without Evals — Philipp Schmid, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-the-production-ai-playbook-deploying-agents-at-enterprise-scale-sandipan-bhaumik--ObTPqBGsEbA|The Production AI Playbook: Deploying Agents at Enterprise Scale — Sandipan Bhaumik, Databricks]]"]
---

# Agentic Evaluations at Scale, For Everybody — Nicholas Kang & Michael Aaron, Google DeepMind

## Tese
Kaggle argumenta que os evals de IA atuais estão quebrados — fragmentados, opacos, criados por uma fração mínima de especialistas — e apresenta quatro frentes (hackathons, exames padronizados para agentes, Game Arena PvP e uma plataforma comunitária de benchmarks) para democratizar e escalar a avaliação de agentes.

## Conceitos-chave
- saturação de benchmarks
- transparência e verificabilidade de evals
- benchmarks PvP com pontuação ELO (não-saturáveis)
- pareamento Bradley-Terry para reduzir número de partidas
- harness vs. modelo como variável confundidora em evals
- evals comunitários e open source
- exames padronizados de agentes (SAT para agentes)
- asserções programáticas + LLM-as-judge
- jaggedness / bordas cognitivas dos modelos
- compaction via API distorcendo comparações de benchmark
- significância estatística em evals de jogos
- incentivização e gamificação (pontos/medalhas Kaggle) para criação de benchmarks
- avaliação de segurança baseline para agentes consumer
- comparação longitudinal de modelos sob deprecação rápida

## Ferramentas & pessoas
**Ferramentas:** Kaggle, Kaggle Game Arena, Kaggle Benchmarks, Kaggle Simulation Platform, Kaggle Hackathons, Agent Exams (MVP), OpenSpiel, LLM model proxy (disponível no Colab), Colab, SWE-bench Pro, Braintrust, OpenClaw, Grok, Claude (Sonnet 4), GitHub, Morph LLM

**Pessoas/orgs:** Nick (PM, Kaggle Benchmarks), Michael (engenheiro de software, Kaggle), Google DeepMind (time AGI), Morph LLM, Paige (criadora da tarefa de SVG do XKCD), Kaggle (comunidade de 30M+ usuários), Google

## Claims acionáveis
- Mais de 10 benchmarks de IA novos são publicados por dia e os leaderboards envelhecem rápido porque os autores migram para o próximo paper.
- Resultados de benchmark variam drasticamente conforme a configuração/orquestração: um laboratório obteve números superiores usando compaction disponível apenas na própria API, inviesando a comparação pública.
- Para significância estatística em pôquer foram necessárias ~400.000 mãos; esquemas de pareamento Bradley-Terry são a chave para reduzir o volume de partidas rodadas.
- Benchmarks PvP com ELO nunca saturam, pois sempre há um vencedor e um perdedor entre modelos em competição direta.
- No SWE-bench Pro os seis modelos de fronteira estão a poucos pontos percentuais entre si, mas o harness altera o desempenho em até 22% — ou seja, muitos evals medem o harness, não o modelo.
- O MVP de exames padronizados de agentes atraiu 500+ agentes avaliados na primeira semana sem promoção, indicando demanda reprimida por avaliação de agentes consumer antes da implantação.
- Existe um trade-off de calibração em exames: muito difíceis ninguém termina (tempo/custo); muito fáceis não geram sinal útil.
- Modelos mais recentes são mais aversos a risco e jogam pôquer pior que gerações anteriores — personalidades emergem nos jogos e são comparáveis em ELO.
- Agentes de IA ainda não julgam bem inovação/criatividade, tornando o julgamento humano especialista (e o alinhamento entre especialistas) necessário em hackathons e evals.
- Endpoints de modelos nem sempre são honestos sobre qual modelo roda por trás, dificultando comparações longitudinais conforme modelos são deprecados.
- Apenas ~30 mil pesquisadores criam evals para ~30 milhões de profissionais técnicos; lacunas de avaliação ampliam o 'jaggedness' entre capacidades sobre-humanas e medíocres dos modelos.

> **Deep dive:** `medium` — Apresentação panorâmica com insights acionáveis pontuais (variância de 22% por harness, viés de compaction, ~400k mãos para significância, Bradley-Terry), mas com densidade arquitetural e novidade limitadas fora do escopo de evals comunitários.
