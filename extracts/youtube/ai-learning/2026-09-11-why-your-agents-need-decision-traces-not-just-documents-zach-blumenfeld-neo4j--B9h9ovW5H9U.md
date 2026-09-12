---
title: "Why your agents need decision traces, not just documents — Zach Blumenfeld, Neo4j"
type: "extract"
source: "youtube"
video_id: "B9h9ovW5H9U"
url: "https://www.youtube.com/watch?v=B9h9ovW5H9U"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-why-your-agents-need-decision-traces-not-just-documents-zach-blumenfeld-neo4j--B9h9ovW5H9U.txt]]"
tags: ["context-engineering", "knowledge-management", "memory-architecture", "ontologia", "agent-tooling", "stack-tooling", "arquitetura", "frameworks", "index", "data-platform"]
thesis: "Context graphs estendem bases de conhecimento/RAG ao adicionar traces de decisão, precedentes e cadeias causais num grafo, permitindo que agentes não apenas respondam perguntas mas tomem decisões explicáveis (aceitar/rejeitar) com base em histórico."
concepts: ["context graph", "decision traces", "precedentes", "grafo de conhecimento / base de conhecimento", "RAG e graph retrieval", "graph embeddings", "busca híbrida (similaridade semântica + estrutural)", "ontologia / schema de grafo", "memória de curto prazo (histórico de sessão)", "memória de longo prazo (entidades resolvidas)", "resolução e deduplicação de entidades", "pipeline de extração texto-para-grafo (spaCy → GLiNER → fallback LLM)", "causal chains e timestamps nas traces", "vector index", "MCP server", "tipo POLE para entidades/relações"]
tools: ["Neo4j", "Cypher", "Neo4j Graph Data Science (GDS)", "create-context-graph (uvx)", "neo4j-agent-memory", "Claude", "OpenAI Embeddings", "Next.js", "spaCy", "GLiNER", "Pydantic AI", "LangGraph", "CrewAI", "Strands", "Google ADK", "Microsoft Agent Framework", "MCP Server", "conectores GitHub/Notion/Jira/Slack"]
people: ["Zach (palestrante, Neo4j)", "William Lyon (PM, Neo4j)", "Neo4j", "Foundation Capital", "Anthropic", "OpenAI", "Microsoft", "Google"]
claims: ["Armazene traces de decisões passadas e precedentes num context graph para que agentes produzam decisões justificadas (aceitar/rejeitar) em vez de apenas respostas factuais", "Combine busca semântica em vector index com similaridade estrutural via graph embeddings das decision traces para recuperar precedentes difíceis de extrair de documentos não estruturados", "Scaffold uma app full-stack com context graph num único comando (uvx create-context-graph), escolhendo framework de agente (Pydantic AI, LangGraph, CrewAI, Strands, Google ADK, OpenAI) e domínio (22 embutidos ou custom)", "Ao criar domínios custom, o tool gera automaticamente uma ontologia/schema de grafo, com o modelo POLE guiando extração e mapeamento", "Modele memória de agente em três camadas — curto prazo (histórico/sessão), longo prazo (entidades extraídas e resolvidas ao longo do tempo) e raciocínio (traces no grafo) — como no pacote neo4j-agent-memory", "Use pipeline de extração em cascata spaCy → GLiNER → fallback de LLM, seguido de merging, deduplicação e enriquecimento, para converter conversas em entidades de longo prazo", "Adicione timestamps e arestas causais (caused/next) às decision traces para rastrear sequência temporal do raciocínio", "Dados estruturados (CSVs/tabelas) podem ser mapeados diretamente via Cypher; conectores permitem importar dados reais de GitHub, Notion, Jira e Slack em vez de dados demo", "Lacunas abertas reconhecidas: escrita automática de novas decision traces e scores de qualidade/sentimento sobre decisões ainda não estão implementados"]
deep_dive: "medium"
deep_dive_reason: "Há insight arquitetural acionável (memória em 3 camadas, busca híbrida com graph embeddings, pipeline de extração e scaffolding open source), mas é uma palestra de vendor centrada em demo com trechos truncados e sem profundidade em harness, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-context-graphs-for-explainable-decision-aware-ai-agents-andreas-kollegger-zaid-z--abvQEhvRI_c|Context Graphs for Explainable, Decision-Aware AI Agents — Andreas Kollegger & Zaid Zaim, Neo4j]]", "[[extracts/youtube/ai-learning/2026-09-11-why-more-context-makes-your-agent-dumber-and-what-to-do-about-it-nupur-sharma-qo--EcqMYoIV57A|Why More Context Makes Your Agent Dumber and What to Do About It — Nupur Sharma, Qodo]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-development-lifecycle-build-test-deploy-monitor-interrupt-26--jWy39wavbjY|The Agent Development Lifecycle: Build, Test, Deploy, Monitor | Interrupt 26]]", "[[extracts/youtube/ai-learning/2026-09-11-ontology-vs-graph-db-why-use-them-together-talkit-global-191-infasis-pwc-consult--U_YyqxUBNiQ|Ontology vs. Graph DB: Why Use Them Together? [TalkIT Global 191, Infasis, PwC Consulting]]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-solved-context-management-in-agents-sally-ann-delucia--esY99nYXxR4|How we solved Context Management in Agents — Sally-Ann Delucia]]", "[[extracts/youtube/ai-learning/2026-09-11-deep-agents-explained--GbzEDgcuGJU|Deep Agents Explained]]", "[[extracts/youtube/ai-learning/2026-09-11-why-agentic-systems-need-ontologies-frank-coyle-uc-berkeley--Sir59K8ZDPU|Why Agentic Systems Need Ontologies — Frank Coyle, UC Berkeley]]"]
---

# Why your agents need decision traces, not just documents — Zach Blumenfeld, Neo4j

## Tese
Context graphs estendem bases de conhecimento/RAG ao adicionar traces de decisão, precedentes e cadeias causais num grafo, permitindo que agentes não apenas respondam perguntas mas tomem decisões explicáveis (aceitar/rejeitar) com base em histórico.

## Conceitos-chave
- context graph
- decision traces
- precedentes
- grafo de conhecimento / base de conhecimento
- RAG e graph retrieval
- graph embeddings
- busca híbrida (similaridade semântica + estrutural)
- ontologia / schema de grafo
- memória de curto prazo (histórico de sessão)
- memória de longo prazo (entidades resolvidas)
- resolução e deduplicação de entidades
- pipeline de extração texto-para-grafo (spaCy → GLiNER → fallback LLM)
- causal chains e timestamps nas traces
- vector index
- MCP server
- tipo POLE para entidades/relações

## Ferramentas & pessoas
**Ferramentas:** Neo4j, Cypher, Neo4j Graph Data Science (GDS), create-context-graph (uvx), neo4j-agent-memory, Claude, OpenAI Embeddings, Next.js, spaCy, GLiNER, Pydantic AI, LangGraph, CrewAI, Strands, Google ADK, Microsoft Agent Framework, MCP Server, conectores GitHub/Notion/Jira/Slack

**Pessoas/orgs:** Zach (palestrante, Neo4j), William Lyon (PM, Neo4j), Neo4j, Foundation Capital, Anthropic, OpenAI, Microsoft, Google

## Claims acionáveis
- Armazene traces de decisões passadas e precedentes num context graph para que agentes produzam decisões justificadas (aceitar/rejeitar) em vez de apenas respostas factuais
- Combine busca semântica em vector index com similaridade estrutural via graph embeddings das decision traces para recuperar precedentes difíceis de extrair de documentos não estruturados
- Scaffold uma app full-stack com context graph num único comando (uvx create-context-graph), escolhendo framework de agente (Pydantic AI, LangGraph, CrewAI, Strands, Google ADK, OpenAI) e domínio (22 embutidos ou custom)
- Ao criar domínios custom, o tool gera automaticamente uma ontologia/schema de grafo, com o modelo POLE guiando extração e mapeamento
- Modele memória de agente em três camadas — curto prazo (histórico/sessão), longo prazo (entidades extraídas e resolvidas ao longo do tempo) e raciocínio (traces no grafo) — como no pacote neo4j-agent-memory
- Use pipeline de extração em cascata spaCy → GLiNER → fallback de LLM, seguido de merging, deduplicação e enriquecimento, para converter conversas em entidades de longo prazo
- Adicione timestamps e arestas causais (caused/next) às decision traces para rastrear sequência temporal do raciocínio
- Dados estruturados (CSVs/tabelas) podem ser mapeados diretamente via Cypher; conectores permitem importar dados reais de GitHub, Notion, Jira e Slack em vez de dados demo
- Lacunas abertas reconhecidas: escrita automática de novas decision traces e scores de qualidade/sentimento sobre decisões ainda não estão implementados

> **Deep dive:** `medium` — Há insight arquitetural acionável (memória em 3 camadas, busca híbrida com graph embeddings, pipeline de extração e scaffolding open source), mas é uma palestra de vendor centrada em demo com trechos truncados e sem profundidade em harness, evals ou governança.
