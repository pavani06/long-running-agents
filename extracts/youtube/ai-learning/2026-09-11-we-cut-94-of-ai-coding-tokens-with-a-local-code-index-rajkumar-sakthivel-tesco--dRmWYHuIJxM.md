---
title: "We Cut 94% of AI Coding Tokens With a Local Code Index - Rajkumar Sakthivel, Tesco"
type: "extract"
source: "youtube"
video_id: "dRmWYHuIJxM"
url: "https://www.youtube.com/watch?v=dRmWYHuIJxM"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-we-cut-94-of-ai-coding-tokens-with-a-local-code-index-rajkumar-sakthivel-tesco--dRmWYHuIJxM.txt]]"
tags: ["context-engineering", "token-budgeting", "context-management", "agent-tooling", "stack-tooling", "index", "evals", "telemetry", "observability", "cross-session", "memory-architecture", "model-selection", "knowledge-management"]
thesis: "Cerca de 90% do custo de ferramentas de coding com IA está no contexto de entrada (input), e uma camada local de busca híbrida com compressão que envia apenas o código relevante reduz tokens em até 94% e custo total em ~61%, tornando a escolha de modelo menos importante do que o que se envia ao modelo."
concepts: ["Distribuição de custo input vs output (90%/10%)", "Token budgeting de contexto de entrada", "Camada local de busca entre codebase e LLM (local-first, sem nuvem)", "Chunking semântico em funções, classes e métodos", "Busca híbrida: semântica (significado) + léxica (palavras exatas)", "Filtragem por score com limiar dinâmico (50% meaning, 30% keyword, 20% recência)", "Compressão de resultados (nome da função + descrição)", "Grafo de chamadas (call graph) para rastrear código conectado", "Índice compartilhado entre múltiplas ferramentas de IA", "Memória persistente cross-sessão e cross-tool", "Telemetria de economia contrafactual (rastreia cada query)", "Trade-off velocidade vs precisão (modelo pequeno e rápido para busca)", "Benchmark público reproduzível"]
tools: ["CCE (ferramenta open-source dos autores)", "Claude Code", "Cursor", "GitHub Copilot", "Codex", "FastAPI (projeto de teste)"]
people: ["Raj", "Fos"]
claims: ["~90% do custo de IA em coding vem do input (arquivos, resultados de busca, contexto); só ~10% é o output gerado", "Encurtar o prompt não economiza: o custo do input já aconteceu antes de o modelo ler o prompt", "Reduzir output em 75% economiza só ~8% do custo total; reduzir input em 94% economiza ~61%", "Busca semântica e busca por palavra, isoladas, erram ~1 em 4 resultados; combinadas erram ~1 em 10, corrigindo as fraquezas uma da outra", "Pedir ao LLM para julgar a relevância dos resultados adiciona 2-3 segundos por query; uma fórmula simples de scoring (50/30/20 com limiar dinâmico) roda em 0,4ms sem chamadas extras de IA", "Benchmark no FastAPI (53 arquivos, 20 perguntas): 83K tokens/query → 4,9K (94% menos), 523 tokens com compressão adicional, com ~90% de acerto em encontrar o código certo", "Em codebase grande e misto (396 arquivos) o recall caiu para quase zero; a abordagem funciona melhor quando cada arquivo tem uma única responsabilidade", "Reindexação leva menos de 1 segundo usando modelo pequeno e rápido", "Em projeto real: 247 queries, 12,4 milhões de tokens salvos, ~US$186 não gastos; 84% da economia veio da camada de busca e o restante da compressão", "Escolha de modelo responde por ~30% do custo; ~70% é o input que se alimenta ao modelo", "Ferramentas como Claude Code, Cursor e Copilot não compartilham contexto entre si; um índice único com memória elimina re-explicar o codebase a cada ferramenta/sessão", "O baseline de 94% é pior caso (ler arquivos inteiros sempre); as economias reais são menores porque ferramentas como Claude Code já são mais eficientes", "Fórmula simples supera modelo complexo na maioria dos casos (small database, duas buscas simples, local em vez de cloud)"]
deep_dive: "medium"
deep_dive_reason: "Apresenta densidade razoável de insight acionável (matemática de custo 90/10, fórmula de scoring com pesos, benchmark reproduzível e telemetria contrafactual) diretamente relevante a context-engineering, mas as técnicas centrais (busca híbrida, indexação local, chunking semântico) são práticas já estabelecidas de retrieval e o fechamento é promocional."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-headroom-a-context-optimization-layer-for-llm-applications-tejas-chopra-netflix--UOWSHg18cL0|Headroom: A Context Optimization Layer for LLM Applications - Tejas Chopra, Netflix, Inc.]]", "[[extracts/youtube/ai-learning/2026-09-11-openai-just-destroyed-ai-coding-codex-2-0--C06FBVXMLCY|OpenAI just destroyed AI coding… Codex 2.0]]", "[[extracts/youtube/ai-learning/2026-09-11-fabio-akita-minha-experiencia-com-agile-vibe-coding--U3bZavG8qQY|Fabio Akita: Minha Experiência com Agile Vibe Coding]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-in-the-sdlc-rethinking-ai-coding-tools-ai-agents--4wMRXmLpdA8|AI in the SDLC: Rethinking AI Coding Tools & AI Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-the-ai-native-company-how-one-founder-becomes-a--Lri2LNYtERM|Stanford CS153 Frontier Systems | The AI Native Company: How One Founder Becomes a 1000x Engineer]]", "[[extracts/youtube/ai-learning/2026-09-11-benchmarking-semantic-code-retrieval-on-claude-code-kuba-rogut-turbopuffer--zKk7sDMGDEQ|Benchmarking semantic code retrieval on Claude Code — Kuba Rogut, Turbopuffer]]"]
theme: "Codificação Agêntica com Claude Code"
---

# We Cut 94% of AI Coding Tokens With a Local Code Index - Rajkumar Sakthivel, Tesco

## Tese
Cerca de 90% do custo de ferramentas de coding com IA está no contexto de entrada (input), e uma camada local de busca híbrida com compressão que envia apenas o código relevante reduz tokens em até 94% e custo total em ~61%, tornando a escolha de modelo menos importante do que o que se envia ao modelo.

## Conceitos-chave
- Distribuição de custo input vs output (90%/10%)
- Token budgeting de contexto de entrada
- Camada local de busca entre codebase e LLM (local-first, sem nuvem)
- Chunking semântico em funções, classes e métodos
- Busca híbrida: semântica (significado) + léxica (palavras exatas)
- Filtragem por score com limiar dinâmico (50% meaning, 30% keyword, 20% recência)
- Compressão de resultados (nome da função + descrição)
- Grafo de chamadas (call graph) para rastrear código conectado
- Índice compartilhado entre múltiplas ferramentas de IA
- Memória persistente cross-sessão e cross-tool
- Telemetria de economia contrafactual (rastreia cada query)
- Trade-off velocidade vs precisão (modelo pequeno e rápido para busca)
- Benchmark público reproduzível

## Ferramentas & pessoas
**Ferramentas:** CCE (ferramenta open-source dos autores), Claude Code, Cursor, GitHub Copilot, Codex, FastAPI (projeto de teste)

**Pessoas/orgs:** Raj, Fos

## Claims acionáveis
- ~90% do custo de IA em coding vem do input (arquivos, resultados de busca, contexto); só ~10% é o output gerado
- Encurtar o prompt não economiza: o custo do input já aconteceu antes de o modelo ler o prompt
- Reduzir output em 75% economiza só ~8% do custo total; reduzir input em 94% economiza ~61%
- Busca semântica e busca por palavra, isoladas, erram ~1 em 4 resultados; combinadas erram ~1 em 10, corrigindo as fraquezas uma da outra
- Pedir ao LLM para julgar a relevância dos resultados adiciona 2-3 segundos por query; uma fórmula simples de scoring (50/30/20 com limiar dinâmico) roda em 0,4ms sem chamadas extras de IA
- Benchmark no FastAPI (53 arquivos, 20 perguntas): 83K tokens/query → 4,9K (94% menos), 523 tokens com compressão adicional, com ~90% de acerto em encontrar o código certo
- Em codebase grande e misto (396 arquivos) o recall caiu para quase zero; a abordagem funciona melhor quando cada arquivo tem uma única responsabilidade
- Reindexação leva menos de 1 segundo usando modelo pequeno e rápido
- Em projeto real: 247 queries, 12,4 milhões de tokens salvos, ~US$186 não gastos; 84% da economia veio da camada de busca e o restante da compressão
- Escolha de modelo responde por ~30% do custo; ~70% é o input que se alimenta ao modelo
- Ferramentas como Claude Code, Cursor e Copilot não compartilham contexto entre si; um índice único com memória elimina re-explicar o codebase a cada ferramenta/sessão
- O baseline de 94% é pior caso (ler arquivos inteiros sempre); as economias reais são menores porque ferramentas como Claude Code já são mais eficientes
- Fórmula simples supera modelo complexo na maioria dos casos (small database, duas buscas simples, local em vez de cloud)

> **Deep dive:** `medium` — Apresenta densidade razoável de insight acionável (matemática de custo 90/10, fórmula de scoring com pesos, benchmark reproduzível e telemetria contrafactual) diretamente relevante a context-engineering, mas as técnicas centrais (busca híbrida, indexação local, chunking semântico) são práticas já estabelecidas de retrieval e o fechamento é promocional.
