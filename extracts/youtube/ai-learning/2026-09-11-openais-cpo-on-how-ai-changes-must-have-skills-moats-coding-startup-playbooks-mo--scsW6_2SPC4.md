---
title: "OpenAI’s CPO on how AI changes must-have skills, moats, coding, startup playbooks, more | Kevin Weil"
type: "extract"
source: "youtube"
video_id: "scsW6_2SPC4"
url: "https://www.youtube.com/watch?v=scsW6_2SPC4"
channel: "Lenny's Podcast"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-openais-cpo-on-how-ai-changes-must-have-skills-moats-coding-startup-playbooks-mo--scsW6_2SPC4.txt]]"
tags: ["evals", "multi-agent", "model-selection", "process", "roadmap", "production"]
thesis: "Construir produtos em IA exige uma mentalidade nova — planejamento leve e bottom-up, 'model maximalism' (mínimo scaffolding porque o modelo melhora a cada ~2 meses), evals como habilidade central do product manager e deploy iterativo em público — já que a base tecnológica muda sob os pés a cada dois meses."
concepts: ["evals (testes/benchmarks para modelos)", "model maximalism", "deploy iterativo (iterative deployment)", "inteligência multidimensional de modelos", "hill climbing sobre evals com fine-tuning", "dados proprietários fora do conjunto de treinamento", "chat como interface universal de baixa restrição", "raciocínio antropomórfico para UX de modelos", "sumarização da chain-of-thought", "ensemble de modelos (grupo ataca o problema + integrador)", "roadmapping trimestral leve e equipes bottom-up", "produto no limite da capacidade do modelo", "'planos são inúteis, planejar é útil' (Eisenhower)"]
tools: ["ChatGPT", "OpenAI API", "Deep Research", "Operator", "ImageGen (modelo de imagem/Ghibli)", "o3-mini-high", "GPT-3", "Claude Sonnet 3.5", "Libra", "Instagram Stories", "Bolt (StackBlitz)", "Eppo", "Persona", "OneSchema FileFeeds"]
people: ["Kevin Weil", "OpenAI", "Sam Altman", "Anthropic", "DeepSeek", "Lenny (Lenny's Newsletter/Podcast)", "Ev Williams", "Mike Krieger", "Sarah Guo", "Vinod (Khosla)", "Elizabeth (esposa de Kevin Weil)", "Instagram", "Twitter/X", "Facebook/Meta", "Planet", "Strava", "Y Combinator", "Black Product Managers Network", "Nature Conservancy"]
claims: ["Escrever evals está se tornando habilidade central para product managers e construtores de produto", "Projete evals simultaneamente ao design do produto: defina hero use cases com respostas ideais, converta em evals e faça hill climbing ao fine-tunar o modelo", "O design do produto depende do limiar de acerto do modelo: 60%, 95% ou 99,5% de confiabilidade exigem produtos completamente diferentes", "Adote model maximalism: não gaste tempo em scaffolding para limitações que o próximo modelo (em ~2 meses) eliminará; construa no limite da capacidade atual", "Se seu produto mal funciona na borda das capacidades do modelo, continue — em poucos meses o modelo melhorará e o produto 'vai cantar'", "Use deploy iterativo: lance mesmo sem conhecer o conjunto completo de capacidades e coevolua com a sociedade em público", "A maior parte do conhecimento mundial é privada (dentro de empresas/governos); o futuro é de modelos amplos fine-tunados com dados proprietários e medidos por evals customizados — oportunidade enorme fora dos fornecedores de modelos-base", "Faça planejamento trimestral leve, esperando descartar o roadmap no meio do caminho; o valor está no ato de planejar, não no plano", "Não bloqueie lançamentos aguardando review de executivos; empodere equipes bottom-up com alinhamento direcional", "Projete UX de modelos por analogia humana: um modelo que 'pensa' por 20s deve dar atualizações breves, não silêncio nem cadeia de pensamento completa; no consumo em escala, sumarize a chain-of-thought em 1-2 frases", "Chat é uma interface poderosa por ser comunicação não estruturada que maximiza banda com o modelo; use-o como catch-all, enquanto casos de alto volume e prescritos merecem interfaces menos flexíveis", "Ensembles multi-modelo (vários atacando o mesmo problema + um modelo integrador) podem gerar melhor raciocínio, análogo ao brainstorming humano", "Explosão de uso interno antes do lançamento é forte sinal de validação para produtos sociais", "Inteligência é multidimensional: diferentes fornecedores liderarão em dimensões distintas, e provar uma capacidade baixa a barreira para os seguidores (efeito 'milha em 4 minutos')", "Há sempre mais gente inteligente fora dos muros da empresa do que dentro — foque em API excelente e deixe 3M+ developers construírem casos de uso verticais"]
deep_dive: "medium"
deep_dive_reason: "Oferece insights acionáveis e originais sobre evals, model maximalism e filosofia de produto em IA, mas em formato de podcast conversacional e parcialmente promocional, sem densidade arquitetural ou técnica suficiente para o tier alto."
---

# OpenAI’s CPO on how AI changes must-have skills, moats, coding, startup playbooks, more | Kevin Weil

## Tese
Construir produtos em IA exige uma mentalidade nova — planejamento leve e bottom-up, 'model maximalism' (mínimo scaffolding porque o modelo melhora a cada ~2 meses), evals como habilidade central do product manager e deploy iterativo em público — já que a base tecnológica muda sob os pés a cada dois meses.

## Conceitos-chave
- evals (testes/benchmarks para modelos)
- model maximalism
- deploy iterativo (iterative deployment)
- inteligência multidimensional de modelos
- hill climbing sobre evals com fine-tuning
- dados proprietários fora do conjunto de treinamento
- chat como interface universal de baixa restrição
- raciocínio antropomórfico para UX de modelos
- sumarização da chain-of-thought
- ensemble de modelos (grupo ataca o problema + integrador)
- roadmapping trimestral leve e equipes bottom-up
- produto no limite da capacidade do modelo
- 'planos são inúteis, planejar é útil' (Eisenhower)

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, OpenAI API, Deep Research, Operator, ImageGen (modelo de imagem/Ghibli), o3-mini-high, GPT-3, Claude Sonnet 3.5, Libra, Instagram Stories, Bolt (StackBlitz), Eppo, Persona, OneSchema FileFeeds

**Pessoas/orgs:** Kevin Weil, OpenAI, Sam Altman, Anthropic, DeepSeek, Lenny (Lenny's Newsletter/Podcast), Ev Williams, Mike Krieger, Sarah Guo, Vinod (Khosla), Elizabeth (esposa de Kevin Weil), Instagram, Twitter/X, Facebook/Meta, Planet, Strava, Y Combinator, Black Product Managers Network, Nature Conservancy

## Claims acionáveis
- Escrever evals está se tornando habilidade central para product managers e construtores de produto
- Projete evals simultaneamente ao design do produto: defina hero use cases com respostas ideais, converta em evals e faça hill climbing ao fine-tunar o modelo
- O design do produto depende do limiar de acerto do modelo: 60%, 95% ou 99,5% de confiabilidade exigem produtos completamente diferentes
- Adote model maximalism: não gaste tempo em scaffolding para limitações que o próximo modelo (em ~2 meses) eliminará; construa no limite da capacidade atual
- Se seu produto mal funciona na borda das capacidades do modelo, continue — em poucos meses o modelo melhorará e o produto 'vai cantar'
- Use deploy iterativo: lance mesmo sem conhecer o conjunto completo de capacidades e coevolua com a sociedade em público
- A maior parte do conhecimento mundial é privada (dentro de empresas/governos); o futuro é de modelos amplos fine-tunados com dados proprietários e medidos por evals customizados — oportunidade enorme fora dos fornecedores de modelos-base
- Faça planejamento trimestral leve, esperando descartar o roadmap no meio do caminho; o valor está no ato de planejar, não no plano
- Não bloqueie lançamentos aguardando review de executivos; empodere equipes bottom-up com alinhamento direcional
- Projete UX de modelos por analogia humana: um modelo que 'pensa' por 20s deve dar atualizações breves, não silêncio nem cadeia de pensamento completa; no consumo em escala, sumarize a chain-of-thought em 1-2 frases
- Chat é uma interface poderosa por ser comunicação não estruturada que maximiza banda com o modelo; use-o como catch-all, enquanto casos de alto volume e prescritos merecem interfaces menos flexíveis
- Ensembles multi-modelo (vários atacando o mesmo problema + um modelo integrador) podem gerar melhor raciocínio, análogo ao brainstorming humano
- Explosão de uso interno antes do lançamento é forte sinal de validação para produtos sociais
- Inteligência é multidimensional: diferentes fornecedores liderarão em dimensões distintas, e provar uma capacidade baixa a barreira para os seguidores (efeito 'milha em 4 minutos')
- Há sempre mais gente inteligente fora dos muros da empresa do que dentro — foque em API excelente e deixe 3M+ developers construírem casos de uso verticais

> **Deep dive:** `medium` — Oferece insights acionáveis e originais sobre evals, model maximalism e filosofia de produto em IA, mas em formato de podcast conversacional e parcialmente promocional, sem densidade arquitetural ou técnica suficiente para o tier alto.
