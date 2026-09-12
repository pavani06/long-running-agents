---
title: "How Companies Are Building Their Own Intelligence | Sonya Huang, Sequoia Capital"
type: "extract"
source: "youtube"
video_id: "bMMv0bZzONg"
url: "https://www.youtube.com/watch?v=bMMv0bZzONg"
channel: "Sequoia Capital"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-how-companies-are-building-their-own-intelligence-sonya-huang-sequoia-capital--bMMv0bZzONg.txt]]"
tags: ["arquitetura", "frameworks", "model-selection", "evals", "harness-engineering", "context-engineering", "memory-architecture", "stack-tooling", "production", "roadmap", "monitoramento", "process", "investimentos", "documentation-publishing"]
thesis: "Empresas de aplicação devem possuir (\"AI soberana\") as partes estratégicas do seu stack de IA — até os pesos — porque modelos open-weight próximos da fronteira (Kimi K3, GLM 5.2) combinados com post-training, harness engineering, evals e online learning já permitem superar modelos fechados em domínios próprios."
concepts: ["AI soberana / posse da própria inteligência até os pesos", "Own vs rent: framework de 4 fatores (custo, latência/velocidade, performance, dados proprietários)", "\"Not your weights, not your product\" (análogo ao meme crypto \"not your keys\")", "Corrida pela intelligence layer (vs. corrida pela application layer)", "Inteligência centralizada vs. descentralizada", "Empresas de aplicação como \"novos labs de pesquisa\" (applied research)", "Labs leader: perfis de pesquisa vs. engenharia", "Times de-novo vs. hub-and-spoke (não reutilizar o AI platform team)", "Legibilidade externa: pesquisa publicada, labs com marca própria, technical marketing", "Roadmap técnico: estratégia → evals → routers/harnesses → post-training → mid/pre-training (raro) → online learning", "Production stack = harness sobre modelo", "Development stack = monitoramento/evals, dados de alta qualidade e online learning", "Piso mais alto / teto mais baixo do stack fechado via API", "Feedback loop: dados de clientes em produção melhorando o modelo a cada interação", "Context engineering: vector DBs, knowledge graphs, conectores MCP, contexto codificado nos pesos", "Dados para post-training: trajetórias de especialistas, dados sintéticos, ambientes de RL", "Soberania não-binária (0% a 100%, desenhar as linhas por capacidade)"]
tools: ["Claude Opus (Anthropic, API fechada)", "GPT (OpenAI, API fechada)", "Kimi K3 (open-weight)", "GLM 5.2 (open-weight)", "Turbopuffer (vector database)", "Glean (enterprise knowledge graph)", "MCP (conectores open source)", "Engram (contexto/memória codificada nos pesos)"]
people: ["Sequoia (evento para portfolio companies)", "Alex Karp (Palantir)", "Satya Nadella (Microsoft)", "Jensen Huang (NVIDIA)", "Anthropic", "OpenAI", "Harvey", "Winston Weinberg (CEO da Harvey)", "Glean", "Factory", "Open Evidence", "Dan Beerman (Engram)", "Lynn (Fireworks)", "Harrison (Langchain)", "Brendan (Meror)", "Trajectory", "Fireworks", "Langchain", "Meror", "Ramp", "Apple", "Google Brain", "Microsoft", "Pat (slide apresentado no AI Ascent)"]
claims: ["Decida o que possuir vs. alugar com um framework de 4 fatores — custo na estrutura de COGS, latência como P0 ou não, performance no domínio e quão proprietários são os dados — pois soberania não é binária.", "Em coding, agentes ainda são majoritariamente alugados (performance out-of-the-box, latência não crítica), enquanto autocomplete/tab roda majoritariamente em modelos próprios por velocidade e volume/custo de chamadas.", "Empresas mais avançadas em deployment de IA são as primeiras a buscar modelos próprios, porque quanto mais bem-sucedido o produto de IA, maiores os AI COGs.", "Crie um time de-novo separado do AI platform team para a iniciativa soberana: platform teams prestam serviço interno, enquanto o lab precisa jogar ofensiva e produzir pesquisa de fronteira.", "Comece pequeno: a Harvey publica muita pesquisa com um time de apenas sete pessoas.", "Invista em legibilidade externa — publicar pesquisa com boa curadoria, possivelmente com um lab/research group de marca própria — porque compradores estão escolhendo seus \"AI champions\" e querem vendors sofisticados.", "Defina evals logo no início, antes de qualquer post-training: é trabalho não glamuroso, mas quanto mais feito upfront, melhor posicionada a empresa para tudo depois.", "Siga a ordem aproximada do roadmap: estratégia → evals → model routers e harnesses → post-training → (apenas em casos raros) mid-training e pre-training → online learning com dados de produção.", "Com Kimi K3 e GLM 5.2, a baseline open-weight já é próxima da fronteira; strong post-training + prompt/harness engineering + online learning podem superar a fronteira fechada no seu domínio (novo em 2026).", "Trate o production stack como um harness sobre um modelo, e o development stack como monitoramento de evals/drift, coleta de dados de alta qualidade (trajetórias de especialistas, dados sintéticos, ambientes de RL) e setup de online learning.", "O stack fechado via API tem piso mais alto mas teto mais baixo: sem acesso aos pesos, não é possível usar dados de produção próprios para melhorar a própria inteligência.", "Context é determinante para performance: combine vector databases (Turbopuffer), enterprise knowledge graphs (Glean), conectores MCP e abordagens novas como codificar contexto nos próprios pesos (Engram).", "Configure online learning para que cada interação de cliente crie um feedback loop que melhora continuamente o modelo."]
deep_dive: "medium"
deep_dive_reason: "Keynote estratégica com framework e roadmap acionáveis cobrindo own-vs-rent, harness, evals e context-engineering e defendendo tese de arquitetura (production vs development stack, online learning), mas sem detalhes técnicos profundos, que ficam a cargo dos workshops seguintes."
---

# How Companies Are Building Their Own Intelligence | Sonya Huang, Sequoia Capital

## Tese
Empresas de aplicação devem possuir ("AI soberana") as partes estratégicas do seu stack de IA — até os pesos — porque modelos open-weight próximos da fronteira (Kimi K3, GLM 5.2) combinados com post-training, harness engineering, evals e online learning já permitem superar modelos fechados em domínios próprios.

## Conceitos-chave
- AI soberana / posse da própria inteligência até os pesos
- Own vs rent: framework de 4 fatores (custo, latência/velocidade, performance, dados proprietários)
- "Not your weights, not your product" (análogo ao meme crypto "not your keys")
- Corrida pela intelligence layer (vs. corrida pela application layer)
- Inteligência centralizada vs. descentralizada
- Empresas de aplicação como "novos labs de pesquisa" (applied research)
- Labs leader: perfis de pesquisa vs. engenharia
- Times de-novo vs. hub-and-spoke (não reutilizar o AI platform team)
- Legibilidade externa: pesquisa publicada, labs com marca própria, technical marketing
- Roadmap técnico: estratégia → evals → routers/harnesses → post-training → mid/pre-training (raro) → online learning
- Production stack = harness sobre modelo
- Development stack = monitoramento/evals, dados de alta qualidade e online learning
- Piso mais alto / teto mais baixo do stack fechado via API
- Feedback loop: dados de clientes em produção melhorando o modelo a cada interação
- Context engineering: vector DBs, knowledge graphs, conectores MCP, contexto codificado nos pesos
- Dados para post-training: trajetórias de especialistas, dados sintéticos, ambientes de RL
- Soberania não-binária (0% a 100%, desenhar as linhas por capacidade)

## Ferramentas & pessoas
**Ferramentas:** Claude Opus (Anthropic, API fechada), GPT (OpenAI, API fechada), Kimi K3 (open-weight), GLM 5.2 (open-weight), Turbopuffer (vector database), Glean (enterprise knowledge graph), MCP (conectores open source), Engram (contexto/memória codificada nos pesos)

**Pessoas/orgs:** Sequoia (evento para portfolio companies), Alex Karp (Palantir), Satya Nadella (Microsoft), Jensen Huang (NVIDIA), Anthropic, OpenAI, Harvey, Winston Weinberg (CEO da Harvey), Glean, Factory, Open Evidence, Dan Beerman (Engram), Lynn (Fireworks), Harrison (Langchain), Brendan (Meror), Trajectory, Fireworks, Langchain, Meror, Ramp, Apple, Google Brain, Microsoft, Pat (slide apresentado no AI Ascent)

## Claims acionáveis
- Decida o que possuir vs. alugar com um framework de 4 fatores — custo na estrutura de COGS, latência como P0 ou não, performance no domínio e quão proprietários são os dados — pois soberania não é binária.
- Em coding, agentes ainda são majoritariamente alugados (performance out-of-the-box, latência não crítica), enquanto autocomplete/tab roda majoritariamente em modelos próprios por velocidade e volume/custo de chamadas.
- Empresas mais avançadas em deployment de IA são as primeiras a buscar modelos próprios, porque quanto mais bem-sucedido o produto de IA, maiores os AI COGs.
- Crie um time de-novo separado do AI platform team para a iniciativa soberana: platform teams prestam serviço interno, enquanto o lab precisa jogar ofensiva e produzir pesquisa de fronteira.
- Comece pequeno: a Harvey publica muita pesquisa com um time de apenas sete pessoas.
- Invista em legibilidade externa — publicar pesquisa com boa curadoria, possivelmente com um lab/research group de marca própria — porque compradores estão escolhendo seus "AI champions" e querem vendors sofisticados.
- Defina evals logo no início, antes de qualquer post-training: é trabalho não glamuroso, mas quanto mais feito upfront, melhor posicionada a empresa para tudo depois.
- Siga a ordem aproximada do roadmap: estratégia → evals → model routers e harnesses → post-training → (apenas em casos raros) mid-training e pre-training → online learning com dados de produção.
- Com Kimi K3 e GLM 5.2, a baseline open-weight já é próxima da fronteira; strong post-training + prompt/harness engineering + online learning podem superar a fronteira fechada no seu domínio (novo em 2026).
- Trate o production stack como um harness sobre um modelo, e o development stack como monitoramento de evals/drift, coleta de dados de alta qualidade (trajetórias de especialistas, dados sintéticos, ambientes de RL) e setup de online learning.
- O stack fechado via API tem piso mais alto mas teto mais baixo: sem acesso aos pesos, não é possível usar dados de produção próprios para melhorar a própria inteligência.
- Context é determinante para performance: combine vector databases (Turbopuffer), enterprise knowledge graphs (Glean), conectores MCP e abordagens novas como codificar contexto nos próprios pesos (Engram).
- Configure online learning para que cada interação de cliente crie um feedback loop que melhora continuamente o modelo.

> **Deep dive:** `medium` — Keynote estratégica com framework e roadmap acionáveis cobrindo own-vs-rent, harness, evals e context-engineering e defendendo tese de arquitetura (production vs development stack, online learning), mas sem detalhes técnicos profundos, que ficam a cargo dos workshops seguintes.
