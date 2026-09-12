---
title: "The AI Product Going Viral With Doctors: OpenEvidence, with CEO Daniel Nadler"
type: "extract"
source: "youtube"
video_id: "huR0Oa2odxA"
url: "https://www.youtube.com/watch?v=huR0Oa2odxA"
channel: "Sequoia Capital"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-ai-product-going-viral-with-doctors-openevidence-with-ceo-daniel-nadler--huR0Oa2odxA.txt]]"
tags: ["model-selection", "context-engineering", "knowledge-management", "data-platform", "index", "verification", "arquitetura", "production", "instituicoes", "governanca", "analise-estrutural"]
thesis: "OpenEvidence alcançou adoção massiva entre médicos (10–25% dos médicos ativos nos EUA) treinando modelos especializados em ensemble exclusivamente sobre literatura médica revisada por pares — sem nenhuma conexão com a internet pública — fundamentando respostas em referências drill-down e distribuindo via consumidor/prosumer gratuito em vez de vendas enterprise top-down."
concepts: ["Modelos pequenos especializados super-treinados em dados de domínio superam modelos muito maiores em tarefas in-domain", "Arquitetura ensemble de ~meia dúzia de modelos especializados (retrieval, ranking) com handoffs entre si", "Curadoria estrita de corpus: apenas literatura médica revisada por pares, zero internet pública", "Metáfora do JPEG compression (Ilya): a questão decisiva é qual 'mundo' o modelo está comprimindo", "Grounding de respostas com citações verificáveis e drill-down até a fonte", "Conteúdo criado pelo governo dos EUA é domínio público por copyright — bootstrap de dados via FDA e CDC", "Medicina como domínio de tudo-edge-case: superfície enorme e busca na longa cauda de casos raros", "Meia-vida do conhecimento médico e impossibilidade de os médicos acompanharem a literatura", "Go-to-market direto ao prosumer (app gratuita, word-of-mouth) vs. enterprise SaaS hospitalar", "Alucinação como feature em alguns domínios (geração criativa, cenários black swan em finanças)", "Relação simbiótica com editoras e sociedades médicas via tráfego gerado pelas citações", "Ciclos virtuosos: usuários poderosos (conselho editorial da NEJM) geram parcerias de conteúdo por pull"]
tools: ["OpenEvidence", "ChatGPT", "Midjourney", "PubMed", "Google", "Twitter/X", "App Store", "Wikipedia"]
people: ["Daniel Nadler", "OpenEvidence", "Sequoia", "New England Journal of Medicine", "Massachusetts Medical Society", "Kensho", "Zachary Zigler", "Alexander Rush", "Evan Hernandez", "Jacob Andreas", "Eric Lehman", "Harvard", "MIT", "Mayo Clinic", "Cleveland Clinic", "Walter Reed / VA", "FDA", "CDC", "Tesla", "DeepMind", "Ilya Sutskever", "Jensen Huang", "Ray Kurzweil", "Nature"]
claims: ["Modelos menores super-treinados em dados in-domain superam modelos muito maiores nessas tarefas — publicado em 'Do We Still Need Clinical Language Models', best paper em ML Healthcare 2023", "A acurácia necessária em medicina não é atingível com um único LLM; exige ensemble cooperativo de modelos especializados em retrieval e ranking", "Os modelos não têm conexão com a internet pública e treinam apenas em literatura revisada por pares mais conteúdo público do FDA e CDC", "Usar conteúdo de domínio público do governo dos EUA resolve o problema inicial de copyright e permite bootstrap do produto", "Fundamentar respostas em referências drill-down (desde início de 2023) gera confiança dos médicos e tráfego simbiótico às editoras, que passam a pedir indexação", "Distribuição direta ao médico como consumidor (grátis, word-of-mouth estilo Tesla) escala muito mais rápido que ciclos de venda enterprise para redes hospitalares", "Parcerias de conteúdo valiosas (NEJM) emergem por pull quando decisores são power users, não por push comercial ou dinheiro", "Conhecimento médico dobra a cada ~5 anos (estimativa conservadora própria; estudo na Nature dizia 73 dias), tornando metade do aprendizado médico obsoleto durante residência", "Alucinação pode ser explorada como feature em geração criativa e em gestão de risco financeiro (geração de cenários de cauda/black swan)", "Mesmo aplicações construídas sobre APIs de terceiros precisam de infraestrutura tradicional robusta ao escalar; os princípios de engenharia seguem um contínuo, não uma ruptura total", "A maioria dos usos reais do produto está na longa cauda de casos clínicos vistos uma ou duas vezes na carreira do médico — este é o problema central que a busca de evidência resolve"]
deep_dive: "medium"
deep_dive_reason: "Há insights arquiteturais acionáveis e relativamente novos (ensemble de modelos especializados, curadoria de corpus sem internet pública, grounding com citações, bootstrap via domínio público), mas sem profundidade em evals/harness/agent-fleets e com parcela relevante de narrativa promocional de produto."
---

# The AI Product Going Viral With Doctors: OpenEvidence, with CEO Daniel Nadler

## Tese
OpenEvidence alcançou adoção massiva entre médicos (10–25% dos médicos ativos nos EUA) treinando modelos especializados em ensemble exclusivamente sobre literatura médica revisada por pares — sem nenhuma conexão com a internet pública — fundamentando respostas em referências drill-down e distribuindo via consumidor/prosumer gratuito em vez de vendas enterprise top-down.

## Conceitos-chave
- Modelos pequenos especializados super-treinados em dados de domínio superam modelos muito maiores em tarefas in-domain
- Arquitetura ensemble de ~meia dúzia de modelos especializados (retrieval, ranking) com handoffs entre si
- Curadoria estrita de corpus: apenas literatura médica revisada por pares, zero internet pública
- Metáfora do JPEG compression (Ilya): a questão decisiva é qual 'mundo' o modelo está comprimindo
- Grounding de respostas com citações verificáveis e drill-down até a fonte
- Conteúdo criado pelo governo dos EUA é domínio público por copyright — bootstrap de dados via FDA e CDC
- Medicina como domínio de tudo-edge-case: superfície enorme e busca na longa cauda de casos raros
- Meia-vida do conhecimento médico e impossibilidade de os médicos acompanharem a literatura
- Go-to-market direto ao prosumer (app gratuita, word-of-mouth) vs. enterprise SaaS hospitalar
- Alucinação como feature em alguns domínios (geração criativa, cenários black swan em finanças)
- Relação simbiótica com editoras e sociedades médicas via tráfego gerado pelas citações
- Ciclos virtuosos: usuários poderosos (conselho editorial da NEJM) geram parcerias de conteúdo por pull

## Ferramentas & pessoas
**Ferramentas:** OpenEvidence, ChatGPT, Midjourney, PubMed, Google, Twitter/X, App Store, Wikipedia

**Pessoas/orgs:** Daniel Nadler, OpenEvidence, Sequoia, New England Journal of Medicine, Massachusetts Medical Society, Kensho, Zachary Zigler, Alexander Rush, Evan Hernandez, Jacob Andreas, Eric Lehman, Harvard, MIT, Mayo Clinic, Cleveland Clinic, Walter Reed / VA, FDA, CDC, Tesla, DeepMind, Ilya Sutskever, Jensen Huang, Ray Kurzweil, Nature

## Claims acionáveis
- Modelos menores super-treinados em dados in-domain superam modelos muito maiores nessas tarefas — publicado em 'Do We Still Need Clinical Language Models', best paper em ML Healthcare 2023
- A acurácia necessária em medicina não é atingível com um único LLM; exige ensemble cooperativo de modelos especializados em retrieval e ranking
- Os modelos não têm conexão com a internet pública e treinam apenas em literatura revisada por pares mais conteúdo público do FDA e CDC
- Usar conteúdo de domínio público do governo dos EUA resolve o problema inicial de copyright e permite bootstrap do produto
- Fundamentar respostas em referências drill-down (desde início de 2023) gera confiança dos médicos e tráfego simbiótico às editoras, que passam a pedir indexação
- Distribuição direta ao médico como consumidor (grátis, word-of-mouth estilo Tesla) escala muito mais rápido que ciclos de venda enterprise para redes hospitalares
- Parcerias de conteúdo valiosas (NEJM) emergem por pull quando decisores são power users, não por push comercial ou dinheiro
- Conhecimento médico dobra a cada ~5 anos (estimativa conservadora própria; estudo na Nature dizia 73 dias), tornando metade do aprendizado médico obsoleto durante residência
- Alucinação pode ser explorada como feature em geração criativa e em gestão de risco financeiro (geração de cenários de cauda/black swan)
- Mesmo aplicações construídas sobre APIs de terceiros precisam de infraestrutura tradicional robusta ao escalar; os princípios de engenharia seguem um contínuo, não uma ruptura total
- A maioria dos usos reais do produto está na longa cauda de casos clínicos vistos uma ou duas vezes na carreira do médico — este é o problema central que a busca de evidência resolve

> **Deep dive:** `medium` — Há insights arquiteturais acionáveis e relativamente novos (ensemble de modelos especializados, curadoria de corpus sem internet pública, grounding com citações, bootstrap via domínio público), mas sem profundidade em evals/harness/agent-fleets e com parcela relevante de narrativa promocional de produto.
