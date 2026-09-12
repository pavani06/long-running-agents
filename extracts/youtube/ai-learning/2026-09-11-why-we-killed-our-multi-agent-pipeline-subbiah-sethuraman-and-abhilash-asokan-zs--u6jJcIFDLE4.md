---
title: "Why We Killed Our Multi-Agent Pipeline — Subbiah Sethuraman and Abhilash Asokan, ZS Associates"
type: "extract"
source: "youtube"
video_id: "u6jJcIFDLE4"
url: "https://www.youtube.com/watch?v=u6jJcIFDLE4"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-we-killed-our-multi-agent-pipeline-subbiah-sethuraman-and-abhilash-asokan-zs--u6jJcIFDLE4.txt]]"
tags: ["multi-agent", "agent-loop", "agentes-orquestracao", "arquitetura", "context-engineering", "ontologia", "knowledge-management", "gate-design", "decision-discipline", "verification", "analise", "production"]
thesis: "Construíram um pipeline multi-agent para análise comercial farmacêutica que falhou por perda de contexto em handoffs e falta de domínio compartilhado, e o resolveram separando detecção determinística de investigação agêntica, consolidando o raciocínio em um único agente e usando um knowledge graph como control plane que delimita hipóteses de investigação."
concepts: ["split determinístico vs. agêntico em workflows", "detecção de sinais via métodos estatísticos com guardrails e thresholds antes do agente", "agente investiga, não identifica sinais (signal queue acorda o agente)", "perda de contexto em handoffs entre múltiplos agentes", "agente único dono do raciocínio end-to-end", "sub-agentes dinâmicos para tarefas focadas retornando resultados, não julgamento", "knowledge graph como control plane (não camada de lookup)", "cada aresta do grafo é uma hipótese avaliável contra os dados", "traversal loop: entidade → vizinhança do grafo → hipótese → dados → evidência → próxima aresta", "ontologia de domínio: geografia, payer, account, brand, KPI, KPIs secundários/terciários", "workflow analítico de 4 passos: detecção de sinal, causa-raiz, ação, outlook", "source localization e driver attribution", "orquestrador de agentes", "derivar arquitetura por observação (Claude Code com bash + banco) em vez de impor design humano"]
tools: ["Claude Code (referido como \"cloud code\")", "bash", "banco de dados SQL", "métodos estatísticos (pipeline determinístico de detecção)", "fila de sinais (queue)"]
people: ["ZS", "Suba", "Abilash (Ablash)", "especialistas de domínio farmacêutico da ZS", "empresas farmacêuticas (top pharmas)"]
claims: ["Não use LLM para detecção de sinais: construa pipeline determinístico com métodos estatísticos, guardrails, thresholds e priorização, colocando sinais numa fila que acorda o agente para investigar", "Separe partes determinísticas e agênticas de workflows complexos; nunca deixe agentes executarem a parte determinística", "Consolide o raciocínio/julgamento em um único agente dono do end-to-end; distribua apenas investigações focadas para sub-agentes dinâmicos que devolvem resultados sem o julgamento", "A perda de contexto em cada handoff entre agentes causa saídas incoerentes (causa correta com ação errada)", "Construa um knowledge graph com especialistas de domínio mapeando entidades, KPIs (ex.: TRX) e relações de influência antes de escalar o sistema", "Trate o knowledge graph como control plane que restringe caminhos, vizinhanças e hipóteses de investigação do agente — cada aresta é uma hipótese", "Observe um agente de código genérico (Claude Code + bash + banco) num diretório vazio para derivar a arquitetura em vez de redesenhar topologia/schemas por intuição", "Não imponha restrições organizacionais/humanas (mimetizar o workflow do analista) na arquitetura de agentes", "Resultado: o sistema final (50+ turns, muitos tokens) produz em 20–30 minutos o que um analista levava 3–4 semanas"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de lições arquiteturais acionáveis e não óbvias (split determinístico/agêntico, agente único dono do raciocínio, grafo como control plane com arestas-como-hipóteses) diretamente relevantes a orquestração de agentes, context-engineering e ontologia, com resultados quantificados."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-scaling-agents-for-gen-ai-products-anju-kambadur-bloomberg-head-of-ai-engineerin--b2GqTDWtg6s|Scaling Agents for Gen AI Products - Anju Kambadur, Bloomberg Head of AI Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-the-multi-agent-architecture-that-actually-ships-luke-alvoeiro-factory--ow1we5PzK-o|The Multi-Agent Architecture That Actually Ships — Luke Alvoeiro, Factory]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-tools-for-forward-deployed-engineering-vasuman-moza-varick-agents--l0FLhNqBOic|AI tools for Forward Deployed Engineering — Vasuman Moza, Varick Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-why-more-context-makes-your-agent-dumber-and-what-to-do-about-it-nupur-sharma-qo--EcqMYoIV57A|Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo]]", "[[extracts/youtube/ai-learning/2026-09-11-building-gtm-ai-agents-lessons-from-deploying-to-6-000-users-sait-izmit-snowflak--DrTdD-ttjCY|Building GTM AI Agents: Lessons from Deploying to 6,000 Users — Sait Izmit, Snowflake]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-context-graphs-for-explainable-decision-aware-ai-agents-andreas-kollegger-zaid-z--abvQEhvRI_c|Context Graphs for Explainable, Decision-Aware AI Agents — Andreas Kollegger & Zaid Zaim, Neo4j]]"]
theme: "Agentes em Produção com Evals"
---

# Why We Killed Our Multi-Agent Pipeline — Subbiah Sethuraman and Abhilash Asokan, ZS Associates

## Tese
Construíram um pipeline multi-agent para análise comercial farmacêutica que falhou por perda de contexto em handoffs e falta de domínio compartilhado, e o resolveram separando detecção determinística de investigação agêntica, consolidando o raciocínio em um único agente e usando um knowledge graph como control plane que delimita hipóteses de investigação.

## Conceitos-chave
- split determinístico vs. agêntico em workflows
- detecção de sinais via métodos estatísticos com guardrails e thresholds antes do agente
- agente investiga, não identifica sinais (signal queue acorda o agente)
- perda de contexto em handoffs entre múltiplos agentes
- agente único dono do raciocínio end-to-end
- sub-agentes dinâmicos para tarefas focadas retornando resultados, não julgamento
- knowledge graph como control plane (não camada de lookup)
- cada aresta do grafo é uma hipótese avaliável contra os dados
- traversal loop: entidade → vizinhança do grafo → hipótese → dados → evidência → próxima aresta
- ontologia de domínio: geografia, payer, account, brand, KPI, KPIs secundários/terciários
- workflow analítico de 4 passos: detecção de sinal, causa-raiz, ação, outlook
- source localization e driver attribution
- orquestrador de agentes
- derivar arquitetura por observação (Claude Code com bash + banco) em vez de impor design humano

## Ferramentas & pessoas
**Ferramentas:** Claude Code (referido como "cloud code"), bash, banco de dados SQL, métodos estatísticos (pipeline determinístico de detecção), fila de sinais (queue)

**Pessoas/orgs:** ZS, Suba, Abilash (Ablash), especialistas de domínio farmacêutico da ZS, empresas farmacêuticas (top pharmas)

## Claims acionáveis
- Não use LLM para detecção de sinais: construa pipeline determinístico com métodos estatísticos, guardrails, thresholds e priorização, colocando sinais numa fila que acorda o agente para investigar
- Separe partes determinísticas e agênticas de workflows complexos; nunca deixe agentes executarem a parte determinística
- Consolide o raciocínio/julgamento em um único agente dono do end-to-end; distribua apenas investigações focadas para sub-agentes dinâmicos que devolvem resultados sem o julgamento
- A perda de contexto em cada handoff entre agentes causa saídas incoerentes (causa correta com ação errada)
- Construa um knowledge graph com especialistas de domínio mapeando entidades, KPIs (ex.: TRX) e relações de influência antes de escalar o sistema
- Trate o knowledge graph como control plane que restringe caminhos, vizinhanças e hipóteses de investigação do agente — cada aresta é uma hipótese
- Observe um agente de código genérico (Claude Code + bash + banco) num diretório vazio para derivar a arquitetura em vez de redesenhar topologia/schemas por intuição
- Não imponha restrições organizacionais/humanas (mimetizar o workflow do analista) na arquitetura de agentes
- Resultado: o sistema final (50+ turns, muitos tokens) produz em 20–30 minutos o que um analista levava 3–4 semanas

> **Deep dive:** `high` — Alta densidade de lições arquiteturais acionáveis e não óbvias (split determinístico/agêntico, agente único dono do raciocínio, grafo como control plane com arestas-como-hipóteses) diretamente relevantes a orquestração de agentes, context-engineering e ontologia, com resultados quantificados.
