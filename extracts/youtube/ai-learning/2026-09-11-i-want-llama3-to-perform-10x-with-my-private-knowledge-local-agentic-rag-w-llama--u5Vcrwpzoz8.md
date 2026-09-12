---
title: "\"I want Llama3 to perform 10x with my private knowledge\" - Local Agentic RAG w/ llama3"
type: "extract"
source: "youtube"
video_id: "u5Vcrwpzoz8"
url: "https://www.youtube.com/watch?v=u5Vcrwpzoz8"
channel: "AI Jason"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-i-want-llama3-to-perform-10x-with-my-private-knowledge-local-agentic-rag-w-llama--u5Vcrwpzoz8.txt]]"
tags: ["knowledge-management", "context-engineering", "context-management", "agent-loop", "agents", "agent-tooling", "arquitetura", "evals", "frameworks", "index", "state", "stack-tooling", "production"]
thesis: "Knowledge management é um dos casos de uso de maior valor para LLMs, mas RAG simples falha em produção, exigindo técnicas avançadas de parsing, chunking, reranking, busca híbrida e padrões agênticos auto-corretivos para alcançar confiabilidade e precisão."
concepts: ["RAG (Retrieval Augmented Generation)", "fine-tuning vs. in-context learning", "bancos de dados vetoriais e embeddings", "preparação/parsing de dados do mundo real (PDF, PowerPoint, web)", "conversão unificada para markdown", "chunk size e trade-offs de contexto", "problema 'lost in the middle' (degradação após ~70k tokens)", "avaliação empírica de chunk size (tempo de resposta, fidelidade, relevância)", "roteamento de documentos por tipo para configuração ótima de RAG", "reranking de resultados top-k", "busca híbrida (vetorial + palavra-chave/SQL)", "agentic RAG", "query translation / step-back prompting (Google DeepMind)", "decomposição de perguntas complexas em sub-queries", "geração e filtragem por metadados com roteamento", "corrective RAG / auto-reflexão", "gradação de documentos, alucinação e utilidade da resposta", "LangGraph: estado compartilhado, nós e arestas condicionais", "execução local de modelos (Ollama + Llama 3)"]
tools: ["LlamaParse", "LlamaCloud", "LlamaHub", "Firecrawl", "PyPDF", "LangChain", "LangGraph", "Ollama", "Llama 3", "GPT4All", "Tavily", "Exa", "LangSmith", "ChatGPT", "Perplexity", "Google Search"]
people: ["Jerry (LlamaIndex)", "Satia (colega do apresentador)", "Google DeepMind", "LlamaIndex", "LangChain", "Mendable", "HubSpot", "Google"]
claims: ["Use LlamaParse para converter PDFs complexos em markdown amigável a LLMs, com prompts customizados por tipo de documento (ex.: reconstruir diálogos de quadrinhos, extrair fórmulas em LaTeX)", "Use Firecrawl para converter websites em markdown limpo com metadados, permitindo unificar todo o pipeline de dados em um único formato", "Evite chunks grandes demais por causa do 'lost in the middle' (modelos de 128k já perdem conteúdo após ~70k tokens de contexto) e pequenos demais por perda de contexto necessário", "Encontre o chunk size ótimo experimentalmente, com critérios de avaliação predefinidos (tempo de resposta, fidelidade, relevância) aplicados a datasets de teste por tipo de documento", "Classifique documentos na ingestão e roteie cada tipo para sua configuração ótima de RAG (parser, prompt, chunk size e método de recuperação)", "Aplique reranking com um modelo dedicado sobre os top-k resultados da busca vetorial para reduzir tokens e ruído antes da geração", "Use busca híbrida (vetorial + palavra-chave) quando a correspondência exata importa, como em e-commerce ou dados tabulares/SQL", "Aplique step-back prompting para abstrair perguntas antes da recuperação (ex.: 'escola entre agosto e novembro de 1954' vira 'histórico educacional') e decomponha perguntas complexas em sub-queries (ex.: vendas 2022-2024 por ano)", "Gere metadados agenticamente (título, ano, país) e filtre o índice antes da busca vetorial para aumentar a relevância dos resultados", "Implemente corrective RAG: grade os documentos recuperados, recorra à busca na web (Tavily) se irrelevantes, verifique alucinação e se a resposta atende à pergunta original, repetindo o loop até passar nas checagens", "Use LangGraph para definir fluxo de controle determinístico (nós, arestas condicionais, estado compartilhado) enquanto usa o LLM em cada etapa, e rode tudo localmente com Ollama (Llama 3) e embeddings GPT4All"]
deep_dive: "medium"
deep_dive_reason: "Oferece táticas concretas e acionáveis para RAG confiável (parsers, chunking, reranking, corrective RAG com demo em LangGraph), mas é em essência um tutorial-síntese de técnicas já estabelecidas com segmento promocional, sem novidade arquitetural profunda."
---

# "I want Llama3 to perform 10x with my private knowledge" - Local Agentic RAG w/ llama3

## Tese
Knowledge management é um dos casos de uso de maior valor para LLMs, mas RAG simples falha em produção, exigindo técnicas avançadas de parsing, chunking, reranking, busca híbrida e padrões agênticos auto-corretivos para alcançar confiabilidade e precisão.

## Conceitos-chave
- RAG (Retrieval Augmented Generation)
- fine-tuning vs. in-context learning
- bancos de dados vetoriais e embeddings
- preparação/parsing de dados do mundo real (PDF, PowerPoint, web)
- conversão unificada para markdown
- chunk size e trade-offs de contexto
- problema 'lost in the middle' (degradação após ~70k tokens)
- avaliação empírica de chunk size (tempo de resposta, fidelidade, relevância)
- roteamento de documentos por tipo para configuração ótima de RAG
- reranking de resultados top-k
- busca híbrida (vetorial + palavra-chave/SQL)
- agentic RAG
- query translation / step-back prompting (Google DeepMind)
- decomposição de perguntas complexas em sub-queries
- geração e filtragem por metadados com roteamento
- corrective RAG / auto-reflexão
- gradação de documentos, alucinação e utilidade da resposta
- LangGraph: estado compartilhado, nós e arestas condicionais
- execução local de modelos (Ollama + Llama 3)

## Ferramentas & pessoas
**Ferramentas:** LlamaParse, LlamaCloud, LlamaHub, Firecrawl, PyPDF, LangChain, LangGraph, Ollama, Llama 3, GPT4All, Tavily, Exa, LangSmith, ChatGPT, Perplexity, Google Search

**Pessoas/orgs:** Jerry (LlamaIndex), Satia (colega do apresentador), Google DeepMind, LlamaIndex, LangChain, Mendable, HubSpot, Google

## Claims acionáveis
- Use LlamaParse para converter PDFs complexos em markdown amigável a LLMs, com prompts customizados por tipo de documento (ex.: reconstruir diálogos de quadrinhos, extrair fórmulas em LaTeX)
- Use Firecrawl para converter websites em markdown limpo com metadados, permitindo unificar todo o pipeline de dados em um único formato
- Evite chunks grandes demais por causa do 'lost in the middle' (modelos de 128k já perdem conteúdo após ~70k tokens de contexto) e pequenos demais por perda de contexto necessário
- Encontre o chunk size ótimo experimentalmente, com critérios de avaliação predefinidos (tempo de resposta, fidelidade, relevância) aplicados a datasets de teste por tipo de documento
- Classifique documentos na ingestão e roteie cada tipo para sua configuração ótima de RAG (parser, prompt, chunk size e método de recuperação)
- Aplique reranking com um modelo dedicado sobre os top-k resultados da busca vetorial para reduzir tokens e ruído antes da geração
- Use busca híbrida (vetorial + palavra-chave) quando a correspondência exata importa, como em e-commerce ou dados tabulares/SQL
- Aplique step-back prompting para abstrair perguntas antes da recuperação (ex.: 'escola entre agosto e novembro de 1954' vira 'histórico educacional') e decomponha perguntas complexas em sub-queries (ex.: vendas 2022-2024 por ano)
- Gere metadados agenticamente (título, ano, país) e filtre o índice antes da busca vetorial para aumentar a relevância dos resultados
- Implemente corrective RAG: grade os documentos recuperados, recorra à busca na web (Tavily) se irrelevantes, verifique alucinação e se a resposta atende à pergunta original, repetindo o loop até passar nas checagens
- Use LangGraph para definir fluxo de controle determinístico (nós, arestas condicionais, estado compartilhado) enquanto usa o LLM em cada etapa, e rode tudo localmente com Ollama (Llama 3) e embeddings GPT4All

> **Deep dive:** `medium` — Oferece táticas concretas e acionáveis para RAG confiável (parsers, chunking, reranking, corrective RAG com demo em LangGraph), mas é em essência um tutorial-síntese de técnicas já estabelecidas com segmento promocional, sem novidade arquitetural profunda.
