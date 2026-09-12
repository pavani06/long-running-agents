---
title: "Coding With OpenAI-o1 in Cursor - Can We Replace Claude 3.5 Now?"
type: "extract"
source: "youtube"
video_id: "wwC86t5k77Y"
url: "https://www.youtube.com/watch?v=wwC86t5k77Y"
channel: "All About AI"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-coding-with-openai-o1-in-cursor-can-we-replace-claude-3-5-now--wwC86t5k77Y.txt]]"
tags: ["model-selection", "agentic-coding", "agent-tooling", "testes-qa", "error-handling", "context-management", "stack-tooling", "verification"]
thesis: "Um teste prático mostra que o modelo o1 da OpenAI no Cursor consegue one-shot integrações complexas (WebRTC Realtime API, Whisper, structured outputs) com latência aceitável, posicionando-se como complemento ao Claude 3.5 e não como substituto."
concepts: ["one-shot prompting", "latência de modelos de raciocínio", "reasoning tokens e ausência de streaming", "seleção e alternância de modelos no editor", "WebRTC com Realtime API", "transcrição de áudio com Whisper", "structured outputs em JSON", "extração de dados com GPT-4o", "iteração para correção de erros (CORS)", "injeção de documentação extensa no contexto (~2000 linhas)", "benchmarks de coding (LiveBench)"]
tools: ["OpenAI o1", "Cursor", "OpenAI Realtime API (WebRTC)", "Whisper", "GPT-4o", "Structured Outputs", "Claude 3.5", "LiveBench", "Python http.server", "Node (server.js)"]
people: ["OpenAI"]
claims: ["o1 one-shot gerou um app HTML funcional de voz via WebRTC com dropdown de vozes, monitor de conexão e botão start/stop na primeira tentativa", "cada edição pequena com o1 levou aproximadamente 10-20 segundos, e a geração do projeto maior (~arquivo longo) levou 40-50 segundos", "o1 no Cursor não faz streaming, tornando a experiência mais lenta que a do Claude 3.5", "o segundo projeto (gravação MP3 + Whisper + structured outputs + GPT-4o) não foi one-shot: falhou com erro de CORS, mas foi corrigido em poucas iterações (~50 linhas adicionadas)", "a pipeline extraiu com sucesso sentimento (positive), tópico (Christmas Eve/buying presents) e data (December 19th) da conversa gravada, salvando em data.json", "colar cerca de 2000 linhas de documentação como contexto foi suficiente para o modelo escrever a integração completa", "o1 está no topo do LiveBench em coding na época do vídeo", "o usuário planeja alternar entre o1 e Claude 3.5 em vez de substituir um pelo outro, usando o1 quando travar no Claude"]
deep_dive: "medium"
deep_dive_reason: "Teste informal mas com observações acionáveis concretas (latências medidas, capacidade de one-shot, estratégia de alternância de modelos e padrão de documentação-no-contexto), porém sem profundidade arquitetural em harness, evals, governança ou ontologia."
---

# Coding With OpenAI-o1 in Cursor - Can We Replace Claude 3.5 Now?

## Tese
Um teste prático mostra que o modelo o1 da OpenAI no Cursor consegue one-shot integrações complexas (WebRTC Realtime API, Whisper, structured outputs) com latência aceitável, posicionando-se como complemento ao Claude 3.5 e não como substituto.

## Conceitos-chave
- one-shot prompting
- latência de modelos de raciocínio
- reasoning tokens e ausência de streaming
- seleção e alternância de modelos no editor
- WebRTC com Realtime API
- transcrição de áudio com Whisper
- structured outputs em JSON
- extração de dados com GPT-4o
- iteração para correção de erros (CORS)
- injeção de documentação extensa no contexto (~2000 linhas)
- benchmarks de coding (LiveBench)

## Ferramentas & pessoas
**Ferramentas:** OpenAI o1, Cursor, OpenAI Realtime API (WebRTC), Whisper, GPT-4o, Structured Outputs, Claude 3.5, LiveBench, Python http.server, Node (server.js)

**Pessoas/orgs:** OpenAI

## Claims acionáveis
- o1 one-shot gerou um app HTML funcional de voz via WebRTC com dropdown de vozes, monitor de conexão e botão start/stop na primeira tentativa
- cada edição pequena com o1 levou aproximadamente 10-20 segundos, e a geração do projeto maior (~arquivo longo) levou 40-50 segundos
- o1 no Cursor não faz streaming, tornando a experiência mais lenta que a do Claude 3.5
- o segundo projeto (gravação MP3 + Whisper + structured outputs + GPT-4o) não foi one-shot: falhou com erro de CORS, mas foi corrigido em poucas iterações (~50 linhas adicionadas)
- a pipeline extraiu com sucesso sentimento (positive), tópico (Christmas Eve/buying presents) e data (December 19th) da conversa gravada, salvando em data.json
- colar cerca de 2000 linhas de documentação como contexto foi suficiente para o modelo escrever a integração completa
- o1 está no topo do LiveBench em coding na época do vídeo
- o usuário planeja alternar entre o1 e Claude 3.5 em vez de substituir um pelo outro, usando o1 quando travar no Claude

> **Deep dive:** `medium` — Teste informal mas com observações acionáveis concretas (latências medidas, capacidade de one-shot, estratégia de alternância de modelos e padrão de documentação-no-contexto), porém sem profundidade arquitetural em harness, evals, governança ou ontologia.
