---
title: "The Search Engine for the Agentic Web — Will Bryk, Exa"
type: "extract"
source: "youtube"
video_id: "59AA5kIoqjA"
url: "https://www.youtube.com/watch?v=59AA5kIoqjA"
channel: "AI Engineer"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-17-the-search-engine-for-the-agentic-web-will-bryk-exa--59AA5kIoqjA.txt]]"
tags: ["agents", "agent-tooling", "index", "token-budgeting", "context-management", "data-platform", "knowledge-management", "production", "roadmap"]
thesis: "A busca na web está migrando massivamente de humanos para agentes de IA, e a Exa constrói um motor de busca neural baseado em embeddings projetado especificamente para esses agentes, visando 'busca perfeita' (comportamento de banco de dados sobre toda a informação do mundo) em vez de um motor de recomendação como o Google."
concepts: ["busca neural via embeddings vs. busca por palavras-chave", "busca perfeita / banco de dados da informação mundial vs. motor de recomendação", "retrieval externo permanente para LLMs (modelos sempre minúsculos frente à internet)", "pré-computação de embeddings como otimização de custo (~US$10M por busca se rodar transformer em cada documento)", "extração eficiente de tokens para reduzir custo downstream de LLM", "saída estruturada para agentes", "customização por cliente (5.000 motores de busca para 5.000 clientes)", "marketplace de dados privados para agentes (Exon)", "bitter lesson / empilhar mais camadas", "volume de buscas por IA excedendo buscas humanas", "informação como infraestrutura-chave e problema de coordenação social"]
tools: ["Exa", "Exon", "Metaphor (nome anterior da Exa)", "Google", "GPT-3", "ChatGPT", "Cursor", "HubSpot", "SimilarWeb"]
people: ["Exa", "Y Combinator", "Google", "HubSpot", "Cursor", "SimilarWeb", "OpenAI"]
claims: ["Em 2026 o número de buscas feitas por sistemas de IA deve exceder o de humanos, e em poucos anos ser ~1000x maior", "Mesmo modelos gigantes futuros (GPT-6/7) sempre precisarão de retrieval externo porque são minúsculos comparados à internet, criando demanda permanente por APIs de busca para agentes", "Rodar um transformer sobre cada documento para cada query custaria ~US$10 milhões por busca; pré-processar documentos em embeddings captura a inteligência da rede a custo viável", "Embeddings resolvem queries semânticas como 'camisas sem listras' que falham em motores de palavra-chave; frequentemente é preciso combinar embeddings e keywords", "A Exa serve 5.000+ empresas e 400.000+ desenvolvedores, incluindo agentes de código (Cursor), GTM (HubSpot) e financeiros", "Existe endpoint de busca em 200ms, crítico para agentes de voz onde cada milissegundo impacta a latência de resposta", "A extração de tokens retorna apenas ~100 tokens mais importantes de 10 documentos, reduzindo drasticamente o custo de LLM downstream", "Saída estruturada permite, por exemplo, que um agente de recrutamento receba paper mais citado, faculdade e ano de formatura como campos prontos", "Queries complexas (ex.: todas as startups de IA financiadas pela YC com batch e status) levam minutos mas retornam resultados exaustivos estilo banco de dados", "Na prática a Exa opera ~5.000 motores customizados com restrições por domínio, janela temporal e exclusões (ex.: nunca retornar páginas de produto)", "O Exon cria um mercado onde provedores de dados privados (ex.: SimilarWeb) são pagos por agentes/developes que acessam seus dados, combinando web pública e fontes privadas na mesma query"]
deep_dive: "medium"
deep_dive_reason: "Keynote de produto com sinais arquiteturais relevantes para tooling de agentes (embeddings, extração de tokens, saída estruturada, marketplace de dados), mas com profundidade técnica limitada e tom parcialmente promocional."
---

# The Search Engine for the Agentic Web — Will Bryk, Exa

## Tese
A busca na web está migrando massivamente de humanos para agentes de IA, e a Exa constrói um motor de busca neural baseado em embeddings projetado especificamente para esses agentes, visando 'busca perfeita' (comportamento de banco de dados sobre toda a informação do mundo) em vez de um motor de recomendação como o Google.

## Conceitos-chave
- busca neural via embeddings vs. busca por palavras-chave
- busca perfeita / banco de dados da informação mundial vs. motor de recomendação
- retrieval externo permanente para LLMs (modelos sempre minúsculos frente à internet)
- pré-computação de embeddings como otimização de custo (~US$10M por busca se rodar transformer em cada documento)
- extração eficiente de tokens para reduzir custo downstream de LLM
- saída estruturada para agentes
- customização por cliente (5.000 motores de busca para 5.000 clientes)
- marketplace de dados privados para agentes (Exon)
- bitter lesson / empilhar mais camadas
- volume de buscas por IA excedendo buscas humanas
- informação como infraestrutura-chave e problema de coordenação social

## Ferramentas & pessoas
**Ferramentas:** Exa, Exon, Metaphor (nome anterior da Exa), Google, GPT-3, ChatGPT, Cursor, HubSpot, SimilarWeb

**Pessoas/orgs:** Exa, Y Combinator, Google, HubSpot, Cursor, SimilarWeb, OpenAI

## Claims acionáveis
- Em 2026 o número de buscas feitas por sistemas de IA deve exceder o de humanos, e em poucos anos ser ~1000x maior
- Mesmo modelos gigantes futuros (GPT-6/7) sempre precisarão de retrieval externo porque são minúsculos comparados à internet, criando demanda permanente por APIs de busca para agentes
- Rodar um transformer sobre cada documento para cada query custaria ~US$10 milhões por busca; pré-processar documentos em embeddings captura a inteligência da rede a custo viável
- Embeddings resolvem queries semânticas como 'camisas sem listras' que falham em motores de palavra-chave; frequentemente é preciso combinar embeddings e keywords
- A Exa serve 5.000+ empresas e 400.000+ desenvolvedores, incluindo agentes de código (Cursor), GTM (HubSpot) e financeiros
- Existe endpoint de busca em 200ms, crítico para agentes de voz onde cada milissegundo impacta a latência de resposta
- A extração de tokens retorna apenas ~100 tokens mais importantes de 10 documentos, reduzindo drasticamente o custo de LLM downstream
- Saída estruturada permite, por exemplo, que um agente de recrutamento receba paper mais citado, faculdade e ano de formatura como campos prontos
- Queries complexas (ex.: todas as startups de IA financiadas pela YC com batch e status) levam minutos mas retornam resultados exaustivos estilo banco de dados
- Na prática a Exa opera ~5.000 motores customizados com restrições por domínio, janela temporal e exclusões (ex.: nunca retornar páginas de produto)
- O Exon cria um mercado onde provedores de dados privados (ex.: SimilarWeb) são pagos por agentes/developes que acessam seus dados, combinando web pública e fontes privadas na mesma query

> **Deep dive:** `medium` — Keynote de produto com sinais arquiteturais relevantes para tooling de agentes (embeddings, extração de tokens, saída estruturada, marketplace de dados), mas com profundidade técnica limitada e tom parcialmente promocional.
