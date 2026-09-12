---
title: "Beyond Components: Designing Generative UI for MCP Apps — Ruben Casas, Postman"
type: "extract"
source: "youtube"
video_id: "hCMrEfPG2Yg"
url: "https://www.youtube.com/watch?v=hCMrEfPG2Yg"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-beyond-components-designing-generative-ui-for-mcp-apps-ruben-casas-postman--hCMrEfPG2Yg.txt]]"
tags: ["agents", "agent-tooling", "arquitetura", "analise-estrutural", "runtime", "stack-tooling", "frameworks"]
thesis: "A UI generativa para agentes evolui em três níveis — componentes estáticos, declarativo e componentes gerados em runtime — e os MCP apps são hoje o melhor mecanismo de entrega (sandbox, auth, tool calling) rumo a interfaces colaborativas humano-agente."
concepts: ["vibe coding / 'poor man's vibe coding' (copy-paste do ChatGPT)", "UI generativa em três níveis (componentes estáticos, declarativo, componentes gerativos)", "componentes estáticos: agente como orquestrador passando props/dados para componentes predefinidos", "UI declarativa: descritores JSON/YAML/Python mapeados por engine de renderização a componentes de design system", "componentes generativos: HTML/CSS/JS gerado on demand em runtime pelo modelo", "sandbox, contenção e modelo de distribuição para código gerado por LLM", "MCP apps como mecanismo de entrega de UI third-party e first-party", "server-driven UI e personalização (modelo Netflix)", "colaboração humano-agente em artefato/canvas compartilhado", "metáfora de Karpathy: o 'novo computador' está na era do terminal, a GUI ainda não foi inventada", "super app vs. chat em toda parte como duas perguntas distintas (onde a UI roda vs. o que o modelo gera)", "analogia TV/rádio: os primeiros formatos imitam a mídia anterior"]
tools: ["ChatGPT", "GPT 5.2", "Claude Opus 4.5", "AG UI protocol (SDK)", "goose (MCP client)", "goose auto-visualizer", "FastMCP (descritor em Python)", "JSON Render (Vercel)", "MCP apps", "Scaly Draw MCP app", "Gemini"]
people: ["Ruen Casses", "Postman", "Andrew Karpathy", "Anthropic", "Vercel", "Netflix"]
claims: ["Modelos como GPT 5.2 e Opus 4.5 (final de 2025) já escrevem código front-end de alta fidelidade melhor que engenheiros experientes, em tarefas de longo horizonte", "UI declarativa (descritores + componentes estáticos do design system) é hoje o equilíbrio ideal entre flexibilidade e consistência, além de mais rápida e mais barata em tokens que geração completa", "Código gerado por LLM em runtime não merece mais confiança que código de terceiros: UI generativa plena exige sandbox, contenção e um modelo de distribuição", "MCP apps fornece autenticação, tool calling, troca de mensagens UI-agente e sandbox via iframe duplo por padrão, sendo o melhor delivery para UI generativa — validado pela escolha da Anthropic de usá-lo para o visualizer first-party do Claude em vez de criar mecanismo proprietário", "O futuro da UI generativa tende a ir além de componentes para experiências colaborativas humano-agente em artefatos compartilhados (ex.: Scaly Draw MCP app, onde humano e agente editam o mesmo canvas)"]
deep_dive: "medium"
deep_dive_reason: "Apresenta uma taxonomia clara dos três níveis de UI generativa com exemplos concretos e implicações arquiteturais (sandbox, protocolo de entrega), mas permanece em nível de visão geral sem aprofundar harness, evals ou governança."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-the-end-of-the-static-screen-architecting-intent-driven-ux-gus-iwanaga-commercet--QrMcNe2jjt8|The End of the Static Screen: Architecting Intent-Driven UX — Gus Iwanaga, commercetools]]", "[[extracts/youtube/ai-learning/2026-09-11-the-weird-future-of-user-interfaces--f32W5BEzWN0|The Weird Future Of User Interfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-seeing-the-future-from-ai-companions-to-personal-software---KfrrWRl3FA|Seeing The Future from AI Companions to Personal Software]]", "[[extracts/youtube/ai-learning/2026-09-11-ai-interfaces-of-the-future-design-review--DBhSfROq3wU|AI Interfaces Of The Future | Design Review]]", "[[extracts/youtube/ai-learning/2026-09-11-building-agent-interfaces-lessons-from-chrome-devtools-mcp-for-agents-michael-ha--_B4Pv9ttFgY|Building Agent Interfaces: Lessons from Chrome DevTools (MCP) for Agents — Michael Hablich, Google]]", "[[extracts/youtube/ai-learning/2026-09-11-the-agent-ready-web-simplify-user-actions-with-webmcp-tara-agyemang-google--ghJmWQCIHRM|The agent-ready web: Simplify user actions with WebMCP — Tara Agyemang, Google]]"]
---

# Beyond Components: Designing Generative UI for MCP Apps — Ruben Casas, Postman

## Tese
A UI generativa para agentes evolui em três níveis — componentes estáticos, declarativo e componentes gerados em runtime — e os MCP apps são hoje o melhor mecanismo de entrega (sandbox, auth, tool calling) rumo a interfaces colaborativas humano-agente.

## Conceitos-chave
- vibe coding / 'poor man's vibe coding' (copy-paste do ChatGPT)
- UI generativa em três níveis (componentes estáticos, declarativo, componentes gerativos)
- componentes estáticos: agente como orquestrador passando props/dados para componentes predefinidos
- UI declarativa: descritores JSON/YAML/Python mapeados por engine de renderização a componentes de design system
- componentes generativos: HTML/CSS/JS gerado on demand em runtime pelo modelo
- sandbox, contenção e modelo de distribuição para código gerado por LLM
- MCP apps como mecanismo de entrega de UI third-party e first-party
- server-driven UI e personalização (modelo Netflix)
- colaboração humano-agente em artefato/canvas compartilhado
- metáfora de Karpathy: o 'novo computador' está na era do terminal, a GUI ainda não foi inventada
- super app vs. chat em toda parte como duas perguntas distintas (onde a UI roda vs. o que o modelo gera)
- analogia TV/rádio: os primeiros formatos imitam a mídia anterior

## Ferramentas & pessoas
**Ferramentas:** ChatGPT, GPT 5.2, Claude Opus 4.5, AG UI protocol (SDK), goose (MCP client), goose auto-visualizer, FastMCP (descritor em Python), JSON Render (Vercel), MCP apps, Scaly Draw MCP app, Gemini

**Pessoas/orgs:** Ruen Casses, Postman, Andrew Karpathy, Anthropic, Vercel, Netflix

## Claims acionáveis
- Modelos como GPT 5.2 e Opus 4.5 (final de 2025) já escrevem código front-end de alta fidelidade melhor que engenheiros experientes, em tarefas de longo horizonte
- UI declarativa (descritores + componentes estáticos do design system) é hoje o equilíbrio ideal entre flexibilidade e consistência, além de mais rápida e mais barata em tokens que geração completa
- Código gerado por LLM em runtime não merece mais confiança que código de terceiros: UI generativa plena exige sandbox, contenção e um modelo de distribuição
- MCP apps fornece autenticação, tool calling, troca de mensagens UI-agente e sandbox via iframe duplo por padrão, sendo o melhor delivery para UI generativa — validado pela escolha da Anthropic de usá-lo para o visualizer first-party do Claude em vez de criar mecanismo proprietário
- O futuro da UI generativa tende a ir além de componentes para experiências colaborativas humano-agente em artefatos compartilhados (ex.: Scaly Draw MCP app, onde humano e agente editam o mesmo canvas)

> **Deep dive:** `medium` — Apresenta uma taxonomia clara dos três níveis de UI generativa com exemplos concretos e implicações arquiteturais (sandbox, protocolo de entrega), mas permanece em nível de visão geral sem aprofundar harness, evals ou governança.
