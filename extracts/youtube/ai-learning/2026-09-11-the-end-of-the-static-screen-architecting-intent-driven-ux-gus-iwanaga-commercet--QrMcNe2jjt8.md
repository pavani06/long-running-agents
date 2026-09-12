---
title: "The End of the Static Screen: Architecting Intent-Driven UX — Gus Iwanaga, commercetools"
type: "extract"
source: "youtube"
video_id: "QrMcNe2jjt8"
url: "https://www.youtube.com/watch?v=QrMcNe2jjt8"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-end-of-the-static-screen-architecting-intent-driven-ux-gus-iwanaga-commercet--QrMcNe2jjt8.txt]]"
tags: ["agents", "harness", "harness-engineering", "agent-tooling", "arquitetura", "classification", "context-engineering", "multi-agent", "process", "production", "spec-driven-development", "stack-tooling", "governanca"]
thesis: "Construir UI generativa de nível produtivo exige uma abordagem declarativa intermediária — na qual um orquestrador classifica intenção, invoca ferramentas e emite um UI spec validado por contratos (catálogo de componentes com Zod) e por uma hierarquia de atomic design — em vez de delegar a composição da interface inteiramente ao LLM."
concepts: ["UI generativa / UX generativa", "agente de UX (UX agent harness)", "orquestrador de agentes com classificação de intenção", "espectro de controle: componentes opinativos vs. open-ended vs. declarativo", "UI spec declarativo como contrato", "catálogo de componentes como contrato entre agente e UI", "atomic design (átomos, moléculas, organismos, templates, páginas)", "hierarquia layout → slots → sub-slots → categorias de componentes", "mapeamento invertido: componentes → sub-slots → slots → templates", "conformidade com design system", "arquitetura de informação em UI gerada por IA", "dados sintéticos de queries mapeadas a componentes", "codificação de conhecimento de UX no agente", "carga cognitiva de SaaS estático e onboarding", "os 3 Ps: pessoas, produto e processo"]
tools: ["commercetools", "GPT/ChatGPT", "Claude", "Perplexity", "MCP servers", "Zod", "React", "h2i (Google)", "JSON Render (Vercel)", "OpenUI (Thesis)", "Booking.com (exemplo de componente opinativo)"]
people: ["Gus (palestrante, GM de produto 0-1 na commercetools)", "commercetools (fundador/boss citado)", "Google", "Vercel", "Thesis", "AIE (AI Engineer, fonte dos talks recomendados)"]
claims: ["Escolha o ponto no espectro de controle conforme o negócio: componentes opinativos funcionam para casos tipo Booking.com; geração open-ended (HTML em iframe sandbox, ex. Claude) é arriscada para empresas porque não controla saída nem resultado", "Adote a abordagem declarativa: query → classificação de intenção → invocação de ferramentas (first/third-party, agentes em MCP) → mapeamento de componentes elegíveis do catálogo para entidades das ferramentas → broadcast de um UI spec → renderização em componentes nativos React", "Use schemas Zod no catálogo de componentes para garantir conformidade com os protocolos de UI e com o design system", "Resolva a arquitetura de informação com atomic design: estruture layout → slots → sub-slots → categorias de componentes e faça o mapeamento inverso dos componentes recuperados para templates, permitindo steering determinístico do placement", "Trate o catálogo e o design system como o coração do sistema: toda propriedade de cada componente, slot e layout precisa de curadoria porque o catálogo é o contrato agente-UI", "Nondeterministicidade sem harness causa inconsistência de copy e layout (ex.: 'Q1' virando 'Janeiro a Março' entre turnos) — mitigue com templates e regras codificadas no agente de UX", "Antecipe a mudança de papel dos times: de desenhar pixels para curar schemas, catálogo, regras, dados sintéticos de queries e padrões de interação — gerencie pessoas e processo (3 Ps), inclusive para PMs e designers não técnicos"]
deep_dive: "medium"
deep_dive_reason: "Oferece padrões arquiteturais acionáveis e relativamente novos (espectro de controle, UI spec declarativo, hierarquia slot/sub-slot, catálogo-como-contrato com Zod) diretamente relevantes a harness e context engineering, mas permanece em nível de demo de conferência, sem evals, métricas ou análise profunda de falhas, com tom parcialmente promocional do produto."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-beyond-components-designing-generative-ui-for-mcp-apps-ruben-casas-postman--hCMrEfPG2Yg|Beyond Components: Designing Generative UI for MCP Apps — Ruben Casas, Postman]]", "[[extracts/youtube/ai-learning/2026-09-11-the-weird-future-of-user-interfaces--f32W5BEzWN0|The Weird Future Of User Interfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-bdd-adr-prd-wtf-capturing-decisions-for-humans-and-ai-alike-michal-cichra-safe-i--504PvfXou5Y|BDD, ADR, PRD, WTF: Capturing Decisions for Humans and AI Alike — Michal Cichra, Safe Intelligence]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-interfaces-of-the-future-design-review--DBhSfROq3wU|AI Interfaces Of The Future | Design Review]]", "[[extracts/youtube/ai-learning/2026-09-11-the-pipeline-is-dead-iris-ten-teije-sky-valley-ambient-computing--bRnoEpoK5m4|The Pipeline Is Dead - Iris ten Teije, Sky Valley Ambient Computing]]", "[[extracts/youtube/ai-learning/2026-09-11-no-vibes-allowed-solving-hard-problems-in-complex-codebases-dex-horthy-humanlaye--rmvDxxNubIg|No Vibes Allowed: Solving Hard Problems in Complex Codebases – Dex Horthy, HumanLayer]]"]
---

# The End of the Static Screen: Architecting Intent-Driven UX — Gus Iwanaga, commercetools

## Tese
Construir UI generativa de nível produtivo exige uma abordagem declarativa intermediária — na qual um orquestrador classifica intenção, invoca ferramentas e emite um UI spec validado por contratos (catálogo de componentes com Zod) e por uma hierarquia de atomic design — em vez de delegar a composição da interface inteiramente ao LLM.

## Conceitos-chave
- UI generativa / UX generativa
- agente de UX (UX agent harness)
- orquestrador de agentes com classificação de intenção
- espectro de controle: componentes opinativos vs. open-ended vs. declarativo
- UI spec declarativo como contrato
- catálogo de componentes como contrato entre agente e UI
- atomic design (átomos, moléculas, organismos, templates, páginas)
- hierarquia layout → slots → sub-slots → categorias de componentes
- mapeamento invertido: componentes → sub-slots → slots → templates
- conformidade com design system
- arquitetura de informação em UI gerada por IA
- dados sintéticos de queries mapeadas a componentes
- codificação de conhecimento de UX no agente
- carga cognitiva de SaaS estático e onboarding
- os 3 Ps: pessoas, produto e processo

## Ferramentas & pessoas
**Ferramentas:** commercetools, GPT/ChatGPT, Claude, Perplexity, MCP servers, Zod, React, h2i (Google), JSON Render (Vercel), OpenUI (Thesis), Booking.com (exemplo de componente opinativo)

**Pessoas/orgs:** Gus (palestrante, GM de produto 0-1 na commercetools), commercetools (fundador/boss citado), Google, Vercel, Thesis, AIE (AI Engineer, fonte dos talks recomendados)

## Claims acionáveis
- Escolha o ponto no espectro de controle conforme o negócio: componentes opinativos funcionam para casos tipo Booking.com; geração open-ended (HTML em iframe sandbox, ex. Claude) é arriscada para empresas porque não controla saída nem resultado
- Adote a abordagem declarativa: query → classificação de intenção → invocação de ferramentas (first/third-party, agentes em MCP) → mapeamento de componentes elegíveis do catálogo para entidades das ferramentas → broadcast de um UI spec → renderização em componentes nativos React
- Use schemas Zod no catálogo de componentes para garantir conformidade com os protocolos de UI e com o design system
- Resolva a arquitetura de informação com atomic design: estruture layout → slots → sub-slots → categorias de componentes e faça o mapeamento inverso dos componentes recuperados para templates, permitindo steering determinístico do placement
- Trate o catálogo e o design system como o coração do sistema: toda propriedade de cada componente, slot e layout precisa de curadoria porque o catálogo é o contrato agente-UI
- Nondeterministicidade sem harness causa inconsistência de copy e layout (ex.: 'Q1' virando 'Janeiro a Março' entre turnos) — mitigue com templates e regras codificadas no agente de UX
- Antecipe a mudança de papel dos times: de desenhar pixels para curar schemas, catálogo, regras, dados sintéticos de queries e padrões de interação — gerencie pessoas e processo (3 Ps), inclusive para PMs e designers não técnicos

> **Deep dive:** `medium` — Oferece padrões arquiteturais acionáveis e relativamente novos (espectro de controle, UI spec declarativo, hierarquia slot/sub-slot, catálogo-como-contrato com Zod) diretamente relevantes a harness e context engineering, mas permanece em nível de demo de conferência, sem evals, métricas ou análise profunda de falhas, com tom parcialmente promocional do produto.
