---
title: "Building Production-Ready RAG Applications: Jerry Liu"
type: "extract"
source: "youtube"
video_id: "TRjq7t2Ms5I"
url: "https://www.youtube.com/watch?v=TRjq7t2Ms5I"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-building-production-ready-rag-applications-jerry-liu--TRjq7t2Ms5I.txt]]"
tags: ["context-engineering", "evals", "production", "agents", "agent-tooling", "data-platform", "model-selection", "knowledge-management", "token-budgeting", "index"]
thesis: "Para levar aplicações RAG a produção é preciso primeiro estabelecer benchmarks de avaliação e então escalar progressivamente de técnicas básicas (chunking, filtros de metadados, busca híbrida) para recuperação avançada (small-to-big, embeddings de referências), arquiteturas de agentes que tratam documentos como ferramentas e fine-tuning de embeddings e LLMs."
concepts: ["RAG (retrieval-augmented generation)", "retrieval augmentation vs fine-tuning como paradigmas de conhecimento", "ingestão de dados e pipeline de consulta (retrieval + synthesis)", "precisão e recall na recuperação", "lost in the middle", "métricas de ranking (hit rate, MRR, nDCG)", "avaliação end-to-end com LLM-as-judge", "datasets sintéticos de avaliação (queries, respostas de referência)", "ajuste de chunk size", "busca híbrida", "filtros de metadados com consulta estruturada (WHERE clause + busca semântica)", "small-to-big retrieval", "embeddings de referências (resumos, perguntas geradas, chunk pai)", "multi-document agents", "documentos modelados como ferramentas (sumarização + QA)", "recuperação sobre ferramentas (tool retrieval)", "fine-tuning de embeddings via adapter (evita reindexar o corpus)", "destilação de modelos grandes em menores para síntese RAG"]
tools: ["LlamaIndex", "Chroma", "Pinecone", "Unstructured", "GPT-4", "GPT-3.5 Turbo", "Llama 2 7B", "Arize"]
people: ["Jerry (cofundador e CEO da LlamaIndex)", "Simon (cofundador da LlamaIndex)", "Anton (Chroma)", "LlamaIndex", "Arize"]
claims: ["Antes de otimizar qualquer coisa em RAG, defina um benchmark de avaliação medindo tanto a solução end-to-end quanto componentes isolados (retrieval e síntese)", "Comece pelas 'table stakes' — tuning de chunk size, busca híbrida e filtros de metadados — antes de partir para técnicas avançadas", "Mais tokens recuperados não implica melhor resposta; reranking pode até aumentar métricas de erro por causa de 'lost in the middle'", "Existe um chunk size ótimo por dataset que deve ser determinado empiricamente", "Inferir filtros estruturados de metadados (ex.: year = 2021) combinados à busca semântica melhora a precisão em queries como fatores de risco de 10-Qs da SEC", "Use small-to-big retrieval: embuta unidades pequenas (sentenças/chunks menores) e expanda a janela de contexto na síntese, permitindo top-k menor (ex.: k=2) e mitigando lost in the middle", "Embutions de referências — resumos, perguntas que o chunk responde ou chunk pai — em vez do texto bruto melhoram a qualidade da recuperação", "Modele cada documento como um conjunto de ferramentas (sumarização + QA) para agentes multi-documento e recupere sobre essas ferramentas para escalar a milhares de documentos", "Gere datasets sintéticos de queries a partir dos chunks com LLMs para fine-tune do modelo de embeddings; ajustar apenas um adapter no lado da query evita reindexar o corpus", "Destile GPT-4 em modelos mais fracos (ex.: GPT-3.5 Turbo) via dataset sintético para melhorar síntese de resposta, structured outputs e raciocínio em pipelines RAG"]
deep_dive: "medium"
deep_dive_reason: "Palestra com boa densidade de técnicas acionáveis e alinhada a context-engineering/evals/agent-tooling, mas combina conteúdo introdutório de RAG com trechos promocionais da LlamaIndex, sem aprofundamento arquitetural de ponta a ponta que justificaria o tier alto."
---

# Building Production-Ready RAG Applications: Jerry Liu

## Tese
Para levar aplicações RAG a produção é preciso primeiro estabelecer benchmarks de avaliação e então escalar progressivamente de técnicas básicas (chunking, filtros de metadados, busca híbrida) para recuperação avançada (small-to-big, embeddings de referências), arquiteturas de agentes que tratam documentos como ferramentas e fine-tuning de embeddings e LLMs.

## Conceitos-chave
- RAG (retrieval-augmented generation)
- retrieval augmentation vs fine-tuning como paradigmas de conhecimento
- ingestão de dados e pipeline de consulta (retrieval + synthesis)
- precisão e recall na recuperação
- lost in the middle
- métricas de ranking (hit rate, MRR, nDCG)
- avaliação end-to-end com LLM-as-judge
- datasets sintéticos de avaliação (queries, respostas de referência)
- ajuste de chunk size
- busca híbrida
- filtros de metadados com consulta estruturada (WHERE clause + busca semântica)
- small-to-big retrieval
- embeddings de referências (resumos, perguntas geradas, chunk pai)
- multi-document agents
- documentos modelados como ferramentas (sumarização + QA)
- recuperação sobre ferramentas (tool retrieval)
- fine-tuning de embeddings via adapter (evita reindexar o corpus)
- destilação de modelos grandes em menores para síntese RAG

## Ferramentas & pessoas
**Ferramentas:** LlamaIndex, Chroma, Pinecone, Unstructured, GPT-4, GPT-3.5 Turbo, Llama 2 7B, Arize

**Pessoas/orgs:** Jerry (cofundador e CEO da LlamaIndex), Simon (cofundador da LlamaIndex), Anton (Chroma), LlamaIndex, Arize

## Claims acionáveis
- Antes de otimizar qualquer coisa em RAG, defina um benchmark de avaliação medindo tanto a solução end-to-end quanto componentes isolados (retrieval e síntese)
- Comece pelas 'table stakes' — tuning de chunk size, busca híbrida e filtros de metadados — antes de partir para técnicas avançadas
- Mais tokens recuperados não implica melhor resposta; reranking pode até aumentar métricas de erro por causa de 'lost in the middle'
- Existe um chunk size ótimo por dataset que deve ser determinado empiricamente
- Inferir filtros estruturados de metadados (ex.: year = 2021) combinados à busca semântica melhora a precisão em queries como fatores de risco de 10-Qs da SEC
- Use small-to-big retrieval: embuta unidades pequenas (sentenças/chunks menores) e expanda a janela de contexto na síntese, permitindo top-k menor (ex.: k=2) e mitigando lost in the middle
- Embutions de referências — resumos, perguntas que o chunk responde ou chunk pai — em vez do texto bruto melhoram a qualidade da recuperação
- Modele cada documento como um conjunto de ferramentas (sumarização + QA) para agentes multi-documento e recupere sobre essas ferramentas para escalar a milhares de documentos
- Gere datasets sintéticos de queries a partir dos chunks com LLMs para fine-tune do modelo de embeddings; ajustar apenas um adapter no lado da query evita reindexar o corpus
- Destile GPT-4 em modelos mais fracos (ex.: GPT-3.5 Turbo) via dataset sintético para melhorar síntese de resposta, structured outputs e raciocínio em pipelines RAG

> **Deep dive:** `medium` — Palestra com boa densidade de técnicas acionáveis e alinhada a context-engineering/evals/agent-tooling, mas combina conteúdo introdutório de RAG com trechos promocionais da LlamaIndex, sem aprofundamento arquitetural de ponta a ponta que justificaria o tier alto.
