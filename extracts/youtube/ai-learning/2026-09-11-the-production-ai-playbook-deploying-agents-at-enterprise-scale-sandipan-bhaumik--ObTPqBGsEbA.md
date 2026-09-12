---
title: "The Production AI Playbook: Deploying Agents at Enterprise Scale — Sandipan Bhaumik, Databricks"
type: "extract"
source: "youtube"
video_id: "ObTPqBGsEbA"
url: "https://www.youtube.com/watch?v=ObTPqBGsEbA"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-production-ai-playbook-deploying-agents-at-enterprise-scale-sandipan-bhaumik--ObTPqBGsEbA.txt]]"
tags: ["evals", "observability", "tracing", "governanca", "multi-agent", "arquitetura", "production", "data-platform", "monitoramento", "error-handling", "model-selection", "testes-qa", "telemetry", "escalation", "process", "stack-tooling"]
thesis: "Levar agentes de IA à produção exige um framework de cinco pilores — avaliação, observabilidade/tracing, fundação de dados, orquestração multiagente e governança — onde a avaliação (métricas de sucesso numéricas e um dataset de teste vivo) é definida antes de qualquer código ou escolha de modelo, invertendo o padrão usual de começar pelo modelo."
concepts: ["Framework de cinco pilares: avaliação, observabilidade, fundação de dados, orquestração, governança", "Três lacunas (gaps): observabilidade, avaliação e governança", "Avaliação como especificação do sistema de IA: sucesso definido em números (acurácia, taxa de deflexão, latência)", "Três camadas de avaliação: determinística (regex, formatos, NER/PII), semântica não-determinística (LLM-as-judge, groundedness) e comportamental (tool calls, loops, chamadas duplicadas de API)", "Dataset de avaliação / golden dataset como sistema vivo que cresce em produção", "Tracing de cada decisão do agente como requisito regulatório e operacional", "Dados de questão (question data) vs dados de rastreamento (tracking/tracing data)", "Padrões de orquestração: orchestrator-worker, choreografia via message bus, human-in-the-loop por limiar de confiança", "Governança de IA: trilhas de auditoria, detecção prévia de PII, versionamento de prompts como gestão de mudança, gestão de mudança de modelos", "Playbook de incidente em produção: detectar → diagnosticar → conter → defletir para humano → corrigir → adicionar casos de teste", "Controle de custo de evals: subconjunto no CI, suíte completa apenas no merge", "Estratégias de resiliência: retry limitado (3 tentativas), fallback, saga/compensação/circuit breaker", "Agentes não perdoam dados ruins: dados historicamente construídos para humanos"]
tools: ["Databricks", "MLflow", "Agent Bricks", "Unity Catalog", "Delta Lake", "Delta Sharing", "Apache Spark", "Mosaic AI", "Databricks Genie", "GPT", "Claude", "LangChain", "CrewAI", "MCP", "Git", "Google Drive", "LinkedIn", "ITSM"]
people: ["Sandy (palestrante, technical lead de Data & AI na Databricks)", "Databricks", "Amazon Web Services (AWS)", "Cliente de retail banking (estudo de caso)", "Reguladores europeus"]
claims: ["Defina sucesso em números de negócio (ex.: 60% de deflexão, 85% de acurácia) antes de escrever qualquer código ou discutir modelos", "Selecione o modelo por último: no estudo de caso, a escolha ocorreu na semana 7 de um POC de 8 semanas, tornando a decisão rápida e baseada em evidência", "Construa o dataset de avaliação a partir de respostas reais de agentes humanos (ponto de partida: ~200 casos), incluindo áreas cinzentas e casos de borda", "Automatize um pipeline que compare respostas vivas do agente contra o dataset de teste e encaminhe para revisão humana respostas abaixo do limiar", "A camada de avaliação comportamental detecta chamadas duplicadas de API (ex.: 3 chamadas ao banco para uma consulta de saldo) que seriam caras em produção", "Sem tracing, disputas de clientes não podem ser investigadas; em indústrias reguladas, tracing e observabilidade são pré-requisitos para colocar IA em produção", "Use monitoramento online com estratégias de fallback e limite de retry (máximo 3 tentativas antes de escalar para humano)", "Trate versionamento de prompt como gestão de mudança empresarial: mensagens de commit devem documentar a falha que motivou a mudança", "Teste modelos atualizados dos provedores no próprio dataset de avaliação, pois benchmarks públicos não refletem o contexto empresarial; evite dependência de modelo único", "Controle o custo de evals comportamentais rodando apenas um subconjunto do dataset no CI e a suíte completa apenas no merge para a main", "Padrão orchestrator-worker dá controle central e logs únicos; choreografia via message bus reduz latência com agentes paralelos e autônomos; human-in-the-loop ativa em limiares de confiança", "No estudo de caso, a queda de satisfação foi diagnosticada via tracing: o documento de política nova não tinha sido reindexado no vector database, gerando respostas desatualizadas", "Aplique validação prévia de PII (regex, NER): o projeto do estudo de caso detectou 47 vazamentos de PII só na fase de teste", "Integre o playbook de incidentes ao ITSM existente para alertar a pessoa certa no momento certo", "Centralize dados de tracing de múltiplos frameworks (LangChain, CrewAI) e nuvens numa camada única para servir dashboards operacionais, LLM-judges e monitoramento de drift"]
deep_dive: "medium"
deep_dive_reason: "Há densidade razoável de insight acionável (camadas de eval, playbook de incidentes, caso bancário com números concretos e governança de custo de evals) relevante a evals, observabilidade e governança, mas o conteúdo arquitetural é em grande parte estabelecido e permeado de promoção de produtos Databricks, sem novidade técnica significativa."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-scaling-agents-for-gen-ai-products-anju-kambadur-bloomberg-head-of-ai-engineerin--b2GqTDWtg6s|Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-why-your-enterprise-tech-stack-isnt-ready-for-ai-agents-christopher-lovejoy-saul--mav15aW9lLM|Why Your Enterprise Tech Stack Isn’t Ready for AI Agents — Christopher Lovejoy & Saul Howard]]", "[[extracts/youtube/ai-learning/2026-09-11-building-gtm-ai-agents-lessons-from-deploying-to-6-000-users-sait-izmit-snowflak--DrTdD-ttjCY|Building GTM AI Agents: Lessons from Deploying to 6,000 Users — Sait Izmit, Snowflake]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-lifecycle-build-test-deploy-monitor-interrupt-26--jWy39wavbjY|The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-26-key-takeaways-from-building-150-agents-in-9-months--jmeGqDu4tPU|26 Key Takeaways from Building 150+ Agents in 9 months]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-tools-for-forward-deployed-engineering-vasuman-moza-varick-agents--l0FLhNqBOic|AI tools for Forward Deployed Engineering — Vasuman Moza, Varick Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-life-cycle-zack-reneau-wedeen-sierra--0vBKv9yAQi4|The Agent Development Life Cycle — Zack Reneau-Wedeen, Sierra]]", "[[extracts/youtube/ai-learning/2026-09-11-the-maturity-phases-of-running-evals-phil-hetzel-braintrust--FB-MLPhL9Ms|The maturity phases of running evals — Phil Hetzel, Braintrust]]", "[[extracts/youtube/ai-learning/2026-09-11-building-and-evaluating-ai-agents-sayash-kapoor-ai-snake-oil--d5EltXhbcfA|Building and evaluating AI Agents — Sayash Kapoor, AI Snake Oil]]", "[[extracts/youtube/ai-learning/2026-09-11-building-closed-loop-evals-for-a-multimodal-agent-at-scale-soumya-gupta-jai-chop--31GUkCBD-Uc|Building Closed-Loop Evals for a Multimodal Agent at Scale — Soumya Gupta & Jai Chopra, Uber]]", "[[extracts/youtube/ai-learning/2026-09-11-we-ve-been-building-ai-agents-wrong-until-now--pC17ge_2n0Q|We've Been Building AI Agents WRONG Until Now]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-evaluations-at-scale-for-everybody-nicholas-kang-michael-aaron-google-de--Ubwb6NzegyA|Agentic Evaluations at Scale, For Everybody — Nicholas Kang & Michael Aaron, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-building-production-ready-rag-applications-jerry-liu--TRjq7t2Ms5I|Building Production-Ready RAG Applications: Jerry Liu]]"]
theme: "Agentes em Produção com Evals"
---

# The Production AI Playbook: Deploying Agents at Enterprise Scale — Sandipan Bhaumik, Databricks

## Tese
Levar agentes de IA à produção exige um framework de cinco pilores — avaliação, observabilidade/tracing, fundação de dados, orquestração multiagente e governança — onde a avaliação (métricas de sucesso numéricas e um dataset de teste vivo) é definida antes de qualquer código ou escolha de modelo, invertendo o padrão usual de começar pelo modelo.

## Conceitos-chave
- Framework de cinco pilares: avaliação, observabilidade, fundação de dados, orquestração, governança
- Três lacunas (gaps): observabilidade, avaliação e governança
- Avaliação como especificação do sistema de IA: sucesso definido em números (acurácia, taxa de deflexão, latência)
- Três camadas de avaliação: determinística (regex, formatos, NER/PII), semântica não-determinística (LLM-as-judge, groundedness) e comportamental (tool calls, loops, chamadas duplicadas de API)
- Dataset de avaliação / golden dataset como sistema vivo que cresce em produção
- Tracing de cada decisão do agente como requisito regulatório e operacional
- Dados de questão (question data) vs dados de rastreamento (tracking/tracing data)
- Padrões de orquestração: orchestrator-worker, choreografia via message bus, human-in-the-loop por limiar de confiança
- Governança de IA: trilhas de auditoria, detecção prévia de PII, versionamento de prompts como gestão de mudança, gestão de mudança de modelos
- Playbook de incidente em produção: detectar → diagnosticar → conter → defletir para humano → corrigir → adicionar casos de teste
- Controle de custo de evals: subconjunto no CI, suíte completa apenas no merge
- Estratégias de resiliência: retry limitado (3 tentativas), fallback, saga/compensação/circuit breaker
- Agentes não perdoam dados ruins: dados historicamente construídos para humanos

## Ferramentas & pessoas
**Ferramentas:** Databricks, MLflow, Agent Bricks, Unity Catalog, Delta Lake, Delta Sharing, Apache Spark, Mosaic AI, Databricks Genie, GPT, Claude, LangChain, CrewAI, MCP, Git, Google Drive, LinkedIn, ITSM

**Pessoas/orgs:** Sandy (palestrante, technical lead de Data & AI na Databricks), Databricks, Amazon Web Services (AWS), Cliente de retail banking (estudo de caso), Reguladores europeus

## Claims acionáveis
- Defina sucesso em números de negócio (ex.: 60% de deflexão, 85% de acurácia) antes de escrever qualquer código ou discutir modelos
- Selecione o modelo por último: no estudo de caso, a escolha ocorreu na semana 7 de um POC de 8 semanas, tornando a decisão rápida e baseada em evidência
- Construa o dataset de avaliação a partir de respostas reais de agentes humanos (ponto de partida: ~200 casos), incluindo áreas cinzentas e casos de borda
- Automatize um pipeline que compare respostas vivas do agente contra o dataset de teste e encaminhe para revisão humana respostas abaixo do limiar
- A camada de avaliação comportamental detecta chamadas duplicadas de API (ex.: 3 chamadas ao banco para uma consulta de saldo) que seriam caras em produção
- Sem tracing, disputas de clientes não podem ser investigadas; em indústrias reguladas, tracing e observabilidade são pré-requisitos para colocar IA em produção
- Use monitoramento online com estratégias de fallback e limite de retry (máximo 3 tentativas antes de escalar para humano)
- Trate versionamento de prompt como gestão de mudança empresarial: mensagens de commit devem documentar a falha que motivou a mudança
- Teste modelos atualizados dos provedores no próprio dataset de avaliação, pois benchmarks públicos não refletem o contexto empresarial; evite dependência de modelo único
- Controle o custo de evals comportamentais rodando apenas um subconjunto do dataset no CI e a suíte completa apenas no merge para a main
- Padrão orchestrator-worker dá controle central e logs únicos; choreografia via message bus reduz latência com agentes paralelos e autônomos; human-in-the-loop ativa em limiares de confiança
- No estudo de caso, a queda de satisfação foi diagnosticada via tracing: o documento de política nova não tinha sido reindexado no vector database, gerando respostas desatualizadas
- Aplique validação prévia de PII (regex, NER): o projeto do estudo de caso detectou 47 vazamentos de PII só na fase de teste
- Integre o playbook de incidentes ao ITSM existente para alertar a pessoa certa no momento certo
- Centralize dados de tracing de múltiplos frameworks (LangChain, CrewAI) e nuvens numa camada única para servir dashboards operacionais, LLM-judges e monitoramento de drift

> **Deep dive:** `medium` — Há densidade razoável de insight acionável (camadas de eval, playbook de incidentes, caso bancário com números concretos e governança de custo de evals) relevante a evals, observabilidade e governança, mas o conteúdo arquitetural é em grande parte estabelecido e permeado de promoção de produtos Databricks, sem novidade técnica significativa.
