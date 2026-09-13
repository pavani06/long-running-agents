---
title: "Arquitetura de agentes de comércio com Claude"
type: "extract"
source: "x"
status_id: "2095233746366808420"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2095233746366808420"
created_at: "2026-09-02T19:33:47.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420.json]]"
tags: ["agents", "agent-loop", "arquitetura", "agent-tooling", "evals", "performance", "context-management", "token-budgeting", "harness", "production", "model-selection"]
topic: "Arquitetura de agentes de comércio com Claude"
summary: "Guia da Anthropic sobre agentes de e-commerce em produção com Claude: um agente único com skills (em vez de subagentes por domínio), ferramentas construídas sobre sistemas core, UI-como-tool e práticas de latência e evals. Deployments enterprise reportam carrinhos até 35% maiores e 60% mais compras concluídas."
key_points: ["Agente único com skills supera consistentemente tanto o design one-prompt-for-everything quanto subagente-por-domínio em qualidade, muitas vezes com menor custo e latência: cada handoff é state-lossy, multiplica tokens e adiciona segundos; subagentes só valem para tarefas estreitas e autocontidas (ex.: deep research) ou hand-off real para agentes com compliance próprio (farmácia, financeiro).", "Regra de colocação prompt vs skill: instruções relevantes a ≥1/3 do tráfego vão no system prompt (ex.: busca de produtos); o resto em skills; regras críticas de segurança/legal/marca e fatos do usuário (ex.: alergias) sempre no prompt; skills previsíveis por sinal (página de origem) devem ser injetadas pelo harness antes da primeira chamada, poupando um turno.", "Ferramentas devem chamar os sistemas core existentes (busca/ranking, carrinho, inventário, promoções) em vez de reimplementá-los — o limite da tool é onde a lógica deles termina e o julgamento do modelo começa; resultados de tool são contexto: retornar só os campos que o modelo usa (URLs de imagem por linha de busca são o ofensor comum) e usar instruções de erro em vez de códigos genéricos.", "UI como tool: o modelo chama present_products/present_itinerary com argumentos tipados, o servidor valida/enriquece e o cliente renderiza; por estarem no formato nativo de messages, preservam histórico sem re-parse e dão ao agente o registro do que está na tela ('o primeiro hotel') — os argumentos devem espelhar o layout renderizado; eager_input_streaming:true devolve streaming em nível de token ao custo da garantia de schema no servidor.", "Latência de conclusão = Σ por turno (time-to-last-token + processamento de tool); alavancas: menos turnos (contexto pré-carregado, modelos mais inteligentes que planejam melhor, chamadas paralelas de tools independentes), tools mais rápidos e tokens mais rápidos — minimizar a soma; qualidade do resultado move retenção/carrinho mais que ganhos marginais de latência, então gerenciar também a latência percebida."]
entities: ["Anthropic", "Claude", "Claude Sonnet"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://claude.com/blog/the-anatomy-of-effective-commerce-agents"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-claudedevs-also-see-our-open-source-reference-implementation-this-inclu--2095233747562180849|implementação de referência de agentes de comércio]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-read-the-full-announcement-https-t-co-cdudn3gvhd--2095233748719817153|Blueprint de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-re-open-sourcing-claude-commerce-agents-this-is-a-bluepri--2095233745167282602|agentes de comércio open-source]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-sat-down-with-the-founders-of-wisprflow-useactively-and-p--2097415273645228460|Claude Managed Agents em produção]]", "[[extracts/x/bookmarks/2026-09-12-stretchcloud-spotify-s-engineering-team-cut-claude-code-token-usage-by-90--2096439998539321653|Portal: roteamento de dois modelos no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-tom_doerr-hyperresearch-turns-claude-code-into-a-research-agent-that-i--2097841937642332595|Agente de pesquisa profunda para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-hwchase17-kai-is-very-cool-and-every-company-should-have-a-kai-this-ep--2097355841183596632|Stripe Kai: agente interno com Deep Agents]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-here-s-how-our-team-uses-claude-tag-for-on-call-when-an-aler--2098508880921899197|On-call automation with Claude]]", "[[extracts/x/bookmarks/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-layer-that-sits-on-t--2098020649662816503|Roteamento e memória no Hermes Agent]]", "[[extracts/x/bookmarks/2026-09-12-andrewcurran_-a-man-in-australia-asked-his-agent-claude-running-on-opencla--2086567854850384054|agente explora vulnerabilidade em agendamento]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-our-ci-team-s-on-call-first-responder-is-claude-tag-it-reads--2097437571634639035|Agente Claude on-call para incidentes]]", "[[extracts/x/bookmarks/2026-09-12-dani_avila7-anthropic-shipped-a-skill-called-discernment-nudge-that-does--2090266638356566321|Skill discernment-nudge da Anthropic]]", "[[extracts/x/bookmarks/2026-09-12-trevin-using-fable-5-1-add-this-to-your-claude-md-file-to-help-its--2095410064492507274|Prompting Claude Fable 5.1]]", "[[extracts/x/bookmarks/2026-09-12-ubereng-we-cut-uber-eats-search-latency-in-half-how-measure-identify--2098177194979983830|Uber Eats search latency halving]]", "[[extracts/x/bookmarks/2026-09-12-daniel_mac8-fable-advisor-now-uses-opus-5-as-orchestrator-opus-5-shines--2081056595555868752|fable-advisor com Opus 5 como orquestrador]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-the-qwen-team-if-you-evaluate-agents-on-an--2094872928240447665|Benchmark longitudinal de agentes e-commerce]]", "[[extracts/x/bookmarks/2026-09-12-a16z-an-hour-of-agentic-computer-use-may-now-be-cheaper-than-an-h--2086906363947737406|custo de agentes vs trabalho humano]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-before-creating-a-session-and-sending-it-events-took-separat--2080009527467114737|Seeding de eventos na criação de sessão]]", "[[extracts/x/bookmarks/2026-09-12-zostaff-a-jane-street-engineer-in-a-talk-on-how-an-exchange-is-actua--2081088443698868526|arquitetura de exchanges financeiras]]"]
thin: false
theme: "Ecossistema Claude e Agentic Coding"
---

# Arquitetura de agentes de comércio com Claude

**@ClaudeDevs** · [2095233746366808420](https://x.com/ClaudeDevs/status/2095233746366808420) · `resource`

## Resumo
Guia da Anthropic sobre agentes de e-commerce em produção com Claude: um agente único com skills (em vez de subagentes por domínio), ferramentas construídas sobre sistemas core, UI-como-tool e práticas de latência e evals. Deployments enterprise reportam carrinhos até 35% maiores e 60% mais compras concluídas.

## Pontos-chave
- Agente único com skills supera consistentemente tanto o design one-prompt-for-everything quanto subagente-por-domínio em qualidade, muitas vezes com menor custo e latência: cada handoff é state-lossy, multiplica tokens e adiciona segundos; subagentes só valem para tarefas estreitas e autocontidas (ex.: deep research) ou hand-off real para agentes com compliance próprio (farmácia, financeiro).
- Regra de colocação prompt vs skill: instruções relevantes a ≥1/3 do tráfego vão no system prompt (ex.: busca de produtos); o resto em skills; regras críticas de segurança/legal/marca e fatos do usuário (ex.: alergias) sempre no prompt; skills previsíveis por sinal (página de origem) devem ser injetadas pelo harness antes da primeira chamada, poupando um turno.
- Ferramentas devem chamar os sistemas core existentes (busca/ranking, carrinho, inventário, promoções) em vez de reimplementá-los — o limite da tool é onde a lógica deles termina e o julgamento do modelo começa; resultados de tool são contexto: retornar só os campos que o modelo usa (URLs de imagem por linha de busca são o ofensor comum) e usar instruções de erro em vez de códigos genéricos.
- UI como tool: o modelo chama present_products/present_itinerary com argumentos tipados, o servidor valida/enriquece e o cliente renderiza; por estarem no formato nativo de messages, preservam histórico sem re-parse e dão ao agente o registro do que está na tela ('o primeiro hotel') — os argumentos devem espelhar o layout renderizado; eager_input_streaming:true devolve streaming em nível de token ao custo da garantia de schema no servidor.
- Latência de conclusão = Σ por turno (time-to-last-token + processamento de tool); alavancas: menos turnos (contexto pré-carregado, modelos mais inteligentes que planejam melhor, chamadas paralelas de tools independentes), tools mais rápidos e tokens mais rápidos — minimizar a soma; qualidade do resultado move retenção/carrinho mais que ganhos marginais de latência, então gerenciar também a latência percebida.

## Links
- https://claude.com/blog/the-anatomy-of-effective-commerce-agents

## Entidades
Anthropic, Claude, Claude Sonnet

> **Revisit:** `high` · **fonte:** `article`
