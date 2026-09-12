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
