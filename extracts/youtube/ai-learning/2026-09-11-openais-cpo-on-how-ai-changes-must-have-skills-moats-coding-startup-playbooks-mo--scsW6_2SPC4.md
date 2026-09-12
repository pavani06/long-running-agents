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
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-why-ai-is-going-vertical-again-dianne-penn-anthropic--tivaWTTVRhY|Why AI is going vertical (again) | Dianne Penn (Anthropic)]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-cpo-mike-krieger-building-ai-products-from-the-bottom-up--Js1gU6L1Zi8|Anthropic CPO Mike Krieger: Building AI Products From the Bottom Up]]", "[[extracts/youtube/ai-learning/2026-09-11-stanford-cs153-frontier-systems-nikhyl-singhal-from-skip-on-product-management-i--BQrJ4lHAjhc|Stanford CS153 Frontier Systems | Nikhyl Singhal from Skip on Product Management in the AI Era]]", "[[extracts/youtube/ai-learning/2026-09-11-structuring-a-modern-ai-team-denys-linkov-wisedocs--SbUxRluVRwk|Structuring a modern AI team — Denys Linkov, Wisedocs]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-use-ai-to-build-your-saas-startup-lovable-supabase--mJwPvyc4-rk|How to use AI to build your SaaS startup (Lovable, Supabase)]]", "[[extracts/youtube/ai-learning/2026-09-11-startup-ideas-you-can-now-build-with-ai--K4s6Cgicw_A|Startup Ideas You Can Now Build With AI]]", "[[extracts/youtube/ai-learning/2026-09-11-openai-devday-2024-virtual-ama-with-sam-altman-moderated-by-harry-stebbings-20vc--Hn27upT2m_o|OpenAI DevDay 2024 | Virtual AMA with Sam Altman, moderated by Harry Stebbings, 20VC]]", "[[extracts/youtube/ai-learning/2026-09-11-the-new-ai-growth-playbook-for-2026-how-lovable-hit-200m-arr-in-one-year--6qAB6aUMIeA|The new AI growth playbook for 2026 | How Lovable hit $200M ARR in one year]]", "[[extracts/youtube/ai-learning/2026-09-11-how-companies-are-building-their-own-intelligence-sonya-huang-sequoia-capital--bMMv0bZzONg|How Companies Are Building Their Own Intelligence | Sonya Huang, Sequoia Capital]]", "[[extracts/youtube/ai-learning/2026-09-11-mental-models-that-change-how-you-think-bill-gurley--yBBhd0-Os74|Mental Models That Change How You Think | Bill Gurley]]", "[[extracts/youtube/ai-learning/2026-09-11-inside-the-mind-of-anthropic-ceo-dario-amodei-the-circuit-extended-interview--x2VHFgyawPE|Inside the Mind of Anthropic CEO Dario Amodei | The Circuit | Extended Interview]]", "[[extracts/youtube/ai-learning/2026-09-11-how-brian-chesky-is-redesigning-airbnb-for-the-ai-era--eURcW5_uS60|How Brian Chesky Is Redesigning Airbnb for the AI Era]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-harvard-professor-reveals-the-hidden-ai-formula-for-explosive-startup-growth--wNUIhCI_jsw|Ex-Harvard Professor Reveals the Hidden AI Formula for Explosive Startup Growth]]", "[[extracts/youtube/ai-learning/2026-09-11-why-netflix-is-betting-on-systems-thinkersnot-specialistsin-the-ai-era-elizabeth--t0GiTyz4syY|Why Netflix is betting on systems thinkers—not specialists—in the AI era | Elizabeth Stone (CPTO)]]", "[[extracts/youtube/ai-learning/2026-09-11-the-only-trait-for-success-in-the-ai-erahow-to-build-it-carnegie-mellon-universi--xWYb7tImErI|The Only Trait for Success in the AI Era—How to Build It | Carnegie Mellon University Po-Shen Loh]]", "[[extracts/youtube/ai-learning/2026-09-11-emil-michael-the-department-of-war-is-moving-faster-than-silicon-valley-on-ai-th--tL3sXpxpCPs|Emil Michael: The Department of War Is Moving Faster Than Silicon Valley on AI | The a16z Show]]", "[[extracts/youtube/ai-learning/2026-09-11-grant-lee-building-gammas-ai-presentation-company-to-100-million-users--fBfY7tWCecU|Grant Lee: Building Gamma’s AI Presentation Company to 100 Million Users]]", "[[extracts/youtube/ai-learning/2026-09-11-the-ai-product-going-viral-with-doctors-openevidence-with-ceo-daniel-nadler--huR0Oa2odxA|The AI Product Going Viral With Doctors: OpenEvidence, with CEO Daniel Nadler]]"]
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
