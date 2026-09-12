---
title: "Parallel’s Parag Agrawal: Building a New Web for AI Agents"
type: "extract"
source: "youtube"
video_id: "fUcnE6pjq5w"
url: "https://www.youtube.com/watch?v=fUcnE6pjq5w"
channel: "Sequoia Capital"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-parallels-parag-agrawal-building-a-new-web-for-ai-agents--fUcnE6pjq5w.txt]]"
tags: ["agent-tooling", "agent-loop", "arquitetura", "context-engineering", "token-budgeting", "data-platform", "index", "memory-architecture", "model-selection", "evals", "multi-agent", "agent-fleets", "monitoramento", "analise"]
thesis: "A busca para agentes deve ser reconstruída do zero — com feedback de agentes substituindo dados de cliques humanos, pipelines de recuperação/ranking otimizados para qualidade-custo-latência e um novo modelo de negócio para a web baseado em precificação diferencial e atribuição de valor via valores de Shapley."
concepts: ["busca agêntica (agentic search) vs. busca humana", "feedback de agentes substituindo dados de cliques humanos ('human click data is a bug')", "crawl e indexação incremental — índice como otimização de latência, trocando crawl por compute de inferência", "pipeline multiestágio de recuperação e ranking com modelos crescentes em cascata", "compressão de modelos pré-treinados em pequenos modelos de ranking", "trade-off qualidade-custo-latência como os três eixos do produto", "alocação inteligente de compute entre as camadas de modelo, agente e busca", "orquestração de múltiplos índices especializados (grande, fresco, estruturado/knowledge graph) com rewrite de query por índice", "memória hierárquica para armazenar e acessar o índice rapidamente", "framing da query como 'devolva os mil tokens certos de um trilhão de páginas'", "valores de Shapley para atribuição e repartição de valor entre fontes de conteúdo", "precificação diferencial por qualidade do conteúdo e valor do trabalho que o consome", "alinhamento de incentivos para publicadores na era dos agentes", "web paralela para agentes e publicação dupla (dual publishing: humanos + agentes)", "migração da web de pull para push ('call me if this happens') via feeds de mudanças", "background agents e multiplicadores de volume de busca (100x-1000x por usuário avançado)", "sub-agentes, harnesses de agentes e sistemas multiagente de longa duração (ex.: AI scientist)", "grounding de LLMs com busca web em tempo de inferência", "busca agêntica como substituta de trabalho humano terceirizado de curadoria de dados", "diferenças de interface: queries de agentes mais longas, sem typos e melhor especificadas que keyword search humana"]
tools: ["Parallel Web Systems (Parallel Search, Search Agents, Turbo)", "Shapley Inc. / Shappley.ai (nome original da empresa)", "Twitter", "Google Search", "Bing", "Google Cloud / GCP (enterprise agent APIs, Gemini)", "ChatGPT", "OpenAI", "Notion (agentes personalizados)", "Cloudflare (dados de tráfego web)"]
people: ["Parag Agrawal (fundador da Parallel, ex-CEO do Twitter)", "Elon Musk", "Sonia (anfitriã do podcast Training Data)", "Andrew (co-anfitrião, estreia no podcast)", "Parallel Web Systems", "Twitter", "Google / Google Cloud", "OpenAI", "Sequoia", "James Flynn", "Cloudflare", "Notion", "Facebook e LinkedIn (walled gardens)"]
claims: ["Trate dados de cliques humanos como bug: para busca de agentes, gere feedback de avaliação com modelos (agentes como 'especialistas' baratos) em vez de ratings e cliques humanos.", "Trocar buscas genéricas (Google) por busca agêntica otimizada reduz para menos da metade os tokens do agente, aumenta a precisão e acelera o fluxo ponta a ponta — liberando orçamento de contexto para mais trabalho.", "Estratégia de bootstrap: lance primeiro um search agent que rastreia a web após a query chegar (trocando crawl por compute de inferência) e construa o índice incrementalmente com casos de uso empíricos em vez de evals teóricos.", "Sequência de otimização deliberada: nail em qualidade e custo por ~2 anos ignorando latência (destilar modelos pequenos é arte conhecida), e só depois atacar latência — Turbo derrubou a resposta de 3s para 200ms.", "Wedge de mercado inicial: substituir trabalho humano terceirizado sobre dados da web (underwriting de seguros, claims processing, enriquecimento de vendas, curadoria financeira) — humanos em buscadores são concorrentes mais fáceis que o buscador no dia zero.", "Um search agent típico executa 5-20 buscas mesmo respondendo em segundos; deep research escala para centenas/milhares — cada prompt humano em apps de IA multiplica o volume de buscas em ~1 ordem de grandeza.", "Arquitetura da query: enriquecer a query com modelos, roteá-la com rewrites para múltiplos índices especializados e rodar camadas sucessivas de retrieval/ranking com modelos maiores, reduzindo de dezenas de bilhões de URLs a trechos de parágrafo e por fim ~mil tokens de máximo sinal.", "Cada versão da API de busca lança amounts diferentes de compute nos mesmos estágios para atender a diferentes restrições de latência e custo.", "Para atribuição e pagamento de conteúdo: estime valores de Shapley por simulação (remover uma fonte, medir queda de qualidade em evals, comparar com o compute necessário para recuperar a mesma qualidade); a computação exata custa mais que o pagamento, então treine modelos estimadores sobre dados de simulação.", "Contratos de licenciamento de preço fixo com labs são insustentáveis para publicadores: inference cresce ~7x/ano mas o valor dos contratos não — prefira precificação diferencial (pague mais por conteúdo único e quando trabalho de alto valor o consome).", "Macro: alocar 2-10% do gasto de inference de LLMs em dados da web excederia todos os negócios atuais de dados web fora de walled gardens; estimativa de 12-24 meses até pagamentos significativos para uma faixa ampla de publicadores.", "Crawl 'completionista' (esperar JavaScript lento carregar) é ineficiente para pré-treino (1-2 ordens de grandeza piores em tokens/compute) mas essencial para busca agêntica — crawle o que os labs não crawleam.", "Interface de agentes difere da humana: queries mais longas, sem typos e melhor especificadas permitem resolver uma classe diferente de problemas de matching.", "Publicação dupla: otimize conteúdo (docs de API, earnings calls) para leitura e interpretação correta por agentes — em muitos casos o agente já é a audiência primária.", "Terceiro estágio evolutivo: a web migra de pull para push — feeds de 'o que mudou na web' disparam agentes ('call me if this happens'), alocando compute continuamente sobre toda a web em nome dos clientes.", "Background agents serão limitados por valor vs. gasto — espere racionalização conforme multiplicadores de busca (100x-1000x por usuários avançados) se generalizam.", "Parceria anunciada: Parallel é provedor de busca e grounding nas enterprise agent APIs do Google Cloud, como alternativa ao Google Search para modelos Gemini e outras inference em GCP."]
deep_dive: "high"
deep_dive_reason: "Alta densidade de detalhes arquiteturais acionáveis (pipeline multiestágio de ranking, múltiplos índices especializados, estratégia qualidade-custo-latência com queda de 3s para 200ms, corte de tokens pela metade) combinada com novidade genuína (valores de Shapley para atribuição de conteúdo, feedback de agentes no lugar de cliques humanos, web pull→push) e relevância direta a context-engineering, evals e agent-fleets, apesar do tom parcialmente promocional de entrevista de fundador."
---

# Parallel’s Parag Agrawal: Building a New Web for AI Agents

## Tese
A busca para agentes deve ser reconstruída do zero — com feedback de agentes substituindo dados de cliques humanos, pipelines de recuperação/ranking otimizados para qualidade-custo-latência e um novo modelo de negócio para a web baseado em precificação diferencial e atribuição de valor via valores de Shapley.

## Conceitos-chave
- busca agêntica (agentic search) vs. busca humana
- feedback de agentes substituindo dados de cliques humanos ('human click data is a bug')
- crawl e indexação incremental — índice como otimização de latência, trocando crawl por compute de inferência
- pipeline multiestágio de recuperação e ranking com modelos crescentes em cascata
- compressão de modelos pré-treinados em pequenos modelos de ranking
- trade-off qualidade-custo-latência como os três eixos do produto
- alocação inteligente de compute entre as camadas de modelo, agente e busca
- orquestração de múltiplos índices especializados (grande, fresco, estruturado/knowledge graph) com rewrite de query por índice
- memória hierárquica para armazenar e acessar o índice rapidamente
- framing da query como 'devolva os mil tokens certos de um trilhão de páginas'
- valores de Shapley para atribuição e repartição de valor entre fontes de conteúdo
- precificação diferencial por qualidade do conteúdo e valor do trabalho que o consome
- alinhamento de incentivos para publicadores na era dos agentes
- web paralela para agentes e publicação dupla (dual publishing: humanos + agentes)
- migração da web de pull para push ('call me if this happens') via feeds de mudanças
- background agents e multiplicadores de volume de busca (100x-1000x por usuário avançado)
- sub-agentes, harnesses de agentes e sistemas multiagente de longa duração (ex.: AI scientist)
- grounding de LLMs com busca web em tempo de inferência
- busca agêntica como substituta de trabalho humano terceirizado de curadoria de dados
- diferenças de interface: queries de agentes mais longas, sem typos e melhor especificadas que keyword search humana

## Ferramentas & pessoas
**Ferramentas:** Parallel Web Systems (Parallel Search, Search Agents, Turbo), Shapley Inc. / Shappley.ai (nome original da empresa), Twitter, Google Search, Bing, Google Cloud / GCP (enterprise agent APIs, Gemini), ChatGPT, OpenAI, Notion (agentes personalizados), Cloudflare (dados de tráfego web)

**Pessoas/orgs:** Parag Agrawal (fundador da Parallel, ex-CEO do Twitter), Elon Musk, Sonia (anfitriã do podcast Training Data), Andrew (co-anfitrião, estreia no podcast), Parallel Web Systems, Twitter, Google / Google Cloud, OpenAI, Sequoia, James Flynn, Cloudflare, Notion, Facebook e LinkedIn (walled gardens)

## Claims acionáveis
- Trate dados de cliques humanos como bug: para busca de agentes, gere feedback de avaliação com modelos (agentes como 'especialistas' baratos) em vez de ratings e cliques humanos.
- Trocar buscas genéricas (Google) por busca agêntica otimizada reduz para menos da metade os tokens do agente, aumenta a precisão e acelera o fluxo ponta a ponta — liberando orçamento de contexto para mais trabalho.
- Estratégia de bootstrap: lance primeiro um search agent que rastreia a web após a query chegar (trocando crawl por compute de inferência) e construa o índice incrementalmente com casos de uso empíricos em vez de evals teóricos.
- Sequência de otimização deliberada: nail em qualidade e custo por ~2 anos ignorando latência (destilar modelos pequenos é arte conhecida), e só depois atacar latência — Turbo derrubou a resposta de 3s para 200ms.
- Wedge de mercado inicial: substituir trabalho humano terceirizado sobre dados da web (underwriting de seguros, claims processing, enriquecimento de vendas, curadoria financeira) — humanos em buscadores são concorrentes mais fáceis que o buscador no dia zero.
- Um search agent típico executa 5-20 buscas mesmo respondendo em segundos; deep research escala para centenas/milhares — cada prompt humano em apps de IA multiplica o volume de buscas em ~1 ordem de grandeza.
- Arquitetura da query: enriquecer a query com modelos, roteá-la com rewrites para múltiplos índices especializados e rodar camadas sucessivas de retrieval/ranking com modelos maiores, reduzindo de dezenas de bilhões de URLs a trechos de parágrafo e por fim ~mil tokens de máximo sinal.
- Cada versão da API de busca lança amounts diferentes de compute nos mesmos estágios para atender a diferentes restrições de latência e custo.
- Para atribuição e pagamento de conteúdo: estime valores de Shapley por simulação (remover uma fonte, medir queda de qualidade em evals, comparar com o compute necessário para recuperar a mesma qualidade); a computação exata custa mais que o pagamento, então treine modelos estimadores sobre dados de simulação.
- Contratos de licenciamento de preço fixo com labs são insustentáveis para publicadores: inference cresce ~7x/ano mas o valor dos contratos não — prefira precificação diferencial (pague mais por conteúdo único e quando trabalho de alto valor o consome).
- Macro: alocar 2-10% do gasto de inference de LLMs em dados da web excederia todos os negócios atuais de dados web fora de walled gardens; estimativa de 12-24 meses até pagamentos significativos para uma faixa ampla de publicadores.
- Crawl 'completionista' (esperar JavaScript lento carregar) é ineficiente para pré-treino (1-2 ordens de grandeza piores em tokens/compute) mas essencial para busca agêntica — crawle o que os labs não crawleam.
- Interface de agentes difere da humana: queries mais longas, sem typos e melhor especificadas permitem resolver uma classe diferente de problemas de matching.
- Publicação dupla: otimize conteúdo (docs de API, earnings calls) para leitura e interpretação correta por agentes — em muitos casos o agente já é a audiência primária.
- Terceiro estágio evolutivo: a web migra de pull para push — feeds de 'o que mudou na web' disparam agentes ('call me if this happens'), alocando compute continuamente sobre toda a web em nome dos clientes.
- Background agents serão limitados por valor vs. gasto — espere racionalização conforme multiplicadores de busca (100x-1000x por usuários avançados) se generalizam.
- Parceria anunciada: Parallel é provedor de busca e grounding nas enterprise agent APIs do Google Cloud, como alternativa ao Google Search para modelos Gemini e outras inference em GCP.

> **Deep dive:** `high` — Alta densidade de detalhes arquiteturais acionáveis (pipeline multiestágio de ranking, múltiplos índices especializados, estratégia qualidade-custo-latência com queda de 3s para 200ms, corte de tokens pela metade) combinada com novidade genuína (valores de Shapley para atribuição de conteúdo, feedback de agentes no lugar de cliques humanos, web pull→push) e relevância direta a context-engineering, evals e agent-fleets, apesar do tom parcialmente promocional de entrevista de fundador.
