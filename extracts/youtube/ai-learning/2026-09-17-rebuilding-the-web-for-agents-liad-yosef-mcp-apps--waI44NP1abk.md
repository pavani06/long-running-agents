---
title: "Rebuilding the web for agents — Liad Yosef, MCP Apps"
type: "extract"
source: "youtube"
video_id: "waI44NP1abk"
url: "https://www.youtube.com/watch?v=waI44NP1abk"
channel: "AI Engineer"
extracted: "2026-09-17"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-17-rebuilding-the-web-for-agents-liad-yosef-mcp-apps--waI44NP1abk.txt]]"
tags: ["agents", "agent-tooling", "arquitetura", "index", "governanca", "observability", "evals", "harness"]
thesis: "A web está migrando de sites navegados por humanos para uma 'web agêntica' quase headless em que assistentes pessoais se tornam o ponto de entrada único, exigindo que sites se tornem 'agent-ready' via specs como MCP apps, feedback dos próprios agentes e uma nova camada de descoberta para recursos agênticos."
concepts: ["MCP apps (spec para injetar UI de servidores MCP em chats)", "Agentic web como mudança de paradigma, não uma 'web de agentes'", "Last mile de interação humano-agente (escolher hotel, assento, visualizar modelos 3D)", "Nearly headless web: agentes interagem headless mas devolvem recursos de UI", "Agent readiness / prontidão de sites para agentes", "Descoberta agêntica além de SEO/GEO/AEO (paralelo: web→busca, mobile→app stores, social→feeds)", "ai-catalog.json e Agentic Resource Discovery como padrões emergentes", "llms.txt é ignorado pelos agentes; eles vão direto aos docs e à homepage", "Feedback do agente define o que o agente precisa (best practices humanas tornam-se obsoletas)", "Browser/computer-use agents e co-browsing (WebMCP) como soluções 'faster horses'", "Split entre agent experience do site e user experience do agente que experiencia o site", "Acessibilidade para agentes correlaciona com acessibilidade humana (LLMs como usuários com deficiência visual)", "Perda de brand loyalty frente a preferências de ferramentas pelo agente"]
tools: ["MCP apps", "Claude / Claude Code", "ChatGPT", "Gemini in Chrome", "GitHub Copilot", "WebMCP", "llms.txt / o.md / pricing.md / x42", "ai-catalog.json", "Agentic Resource Discovery", "Aura (aura.ai, journey.aura.ai, aura.directory)", "OpenClaw", "Eve (harness da Vercel)", "Shopify agentic storefronts", "Booking.com", "Airbnb", "Amazon", "Google", "Jira", "Salesforce", "Sentry", "Cloudflare", "monday.com", "Mixpanel", "PostHog", "Expedia", "Etsy", "AllTrails"]
people: ["Palestrante: co-criador/mantenedor do MCP apps, membro do comitê MCP, co-fundador da Aura, ex-líder de agentic storefronts no Shopify", "David Cramer (Sentry), autor de 'Designing for Agents'", "OpenAI", "Anthropic", "Google", "MCP e A2A (protocolos/organizações)", "Cloudflare (CEO: tráfego de agentes superou tráfego humano)", "Vercel"]
claims: ["Sites como fonte de verdade tendem à obsolescência; assistentes pessoais serão o principal (senão único) gateway para a web", "Salesforce, Cloudflare e Sentry já migraram para modelos headless/API-first, mesmo com UI como diferenciador", "CEO da Cloudflare afirmou que tráfego de agentes já superou o tráfego humano na web", "Cerca de 50% dos sites testados publicam llms.txt, mas quase nenhum agente o usa — os agentes vão direto à página de docs e à homepage", "Dos agentes que usaram llms.txt (~40%), só o fizeram porque os docs apontavam para o arquivo", "OpenAI parou de publicar best practices de tools porque a melhoria dos modelos as torna obsoletas (ex.: descrições de MCP caíram de três parágrafos para três linhas)", "Agentes abandonam produtos cujo uso exige abrir navegador e preferem os com melhor MCP/API (caso Mixpanel vs PostHog recomendado pelo Claude Code)", "Web search tradicional (baseado em SEO/pagerank humano), registros fechados por cliente e registros centrais únicos são insuficientes para descoberta agêntica — o último levanta questões de curadoria e governança", "Melhorar acessibilidade humana do site melhora a acessibilidade para agentes, e vice-versa", "Aura disponibiliza gratuitamente benchmarks de readiness de sites, ferramenta de journey multi-harness (Claude Code, Eve, ChatGPT) e um diretório consultável por agentes via ai-catalog.json"]
deep_dive: "medium"
deep_dive_reason: "Traz dados empíricos inéditos (llms.txt ignorado, jornadas comparadas de múltiplos harnesses) e padrões emergentes de descoberta/governança da web agêntica, mas tem tom parcialmente promocional e pouca profundidade arquitetural em harness ou context-engineering."
---

# Rebuilding the web for agents — Liad Yosef, MCP Apps

## Tese
A web está migrando de sites navegados por humanos para uma 'web agêntica' quase headless em que assistentes pessoais se tornam o ponto de entrada único, exigindo que sites se tornem 'agent-ready' via specs como MCP apps, feedback dos próprios agentes e uma nova camada de descoberta para recursos agênticos.

## Conceitos-chave
- MCP apps (spec para injetar UI de servidores MCP em chats)
- Agentic web como mudança de paradigma, não uma 'web de agentes'
- Last mile de interação humano-agente (escolher hotel, assento, visualizar modelos 3D)
- Nearly headless web: agentes interagem headless mas devolvem recursos de UI
- Agent readiness / prontidão de sites para agentes
- Descoberta agêntica além de SEO/GEO/AEO (paralelo: web→busca, mobile→app stores, social→feeds)
- ai-catalog.json e Agentic Resource Discovery como padrões emergentes
- llms.txt é ignorado pelos agentes; eles vão direto aos docs e à homepage
- Feedback do agente define o que o agente precisa (best practices humanas tornam-se obsoletas)
- Browser/computer-use agents e co-browsing (WebMCP) como soluções 'faster horses'
- Split entre agent experience do site e user experience do agente que experiencia o site
- Acessibilidade para agentes correlaciona com acessibilidade humana (LLMs como usuários com deficiência visual)
- Perda de brand loyalty frente a preferências de ferramentas pelo agente

## Ferramentas & pessoas
**Ferramentas:** MCP apps, Claude / Claude Code, ChatGPT, Gemini in Chrome, GitHub Copilot, WebMCP, llms.txt / o.md / pricing.md / x42, ai-catalog.json, Agentic Resource Discovery, Aura (aura.ai, journey.aura.ai, aura.directory), OpenClaw, Eve (harness da Vercel), Shopify agentic storefronts, Booking.com, Airbnb, Amazon, Google, Jira, Salesforce, Sentry, Cloudflare, monday.com, Mixpanel, PostHog, Expedia, Etsy, AllTrails

**Pessoas/orgs:** Palestrante: co-criador/mantenedor do MCP apps, membro do comitê MCP, co-fundador da Aura, ex-líder de agentic storefronts no Shopify, David Cramer (Sentry), autor de 'Designing for Agents', OpenAI, Anthropic, Google, MCP e A2A (protocolos/organizações), Cloudflare (CEO: tráfego de agentes superou tráfego humano), Vercel

## Claims acionáveis
- Sites como fonte de verdade tendem à obsolescência; assistentes pessoais serão o principal (senão único) gateway para a web
- Salesforce, Cloudflare e Sentry já migraram para modelos headless/API-first, mesmo com UI como diferenciador
- CEO da Cloudflare afirmou que tráfego de agentes já superou o tráfego humano na web
- Cerca de 50% dos sites testados publicam llms.txt, mas quase nenhum agente o usa — os agentes vão direto à página de docs e à homepage
- Dos agentes que usaram llms.txt (~40%), só o fizeram porque os docs apontavam para o arquivo
- OpenAI parou de publicar best practices de tools porque a melhoria dos modelos as torna obsoletas (ex.: descrições de MCP caíram de três parágrafos para três linhas)
- Agentes abandonam produtos cujo uso exige abrir navegador e preferem os com melhor MCP/API (caso Mixpanel vs PostHog recomendado pelo Claude Code)
- Web search tradicional (baseado em SEO/pagerank humano), registros fechados por cliente e registros centrais únicos são insuficientes para descoberta agêntica — o último levanta questões de curadoria e governança
- Melhorar acessibilidade humana do site melhora a acessibilidade para agentes, e vice-versa
- Aura disponibiliza gratuitamente benchmarks de readiness de sites, ferramenta de journey multi-harness (Claude Code, Eve, ChatGPT) e um diretório consultável por agentes via ai-catalog.json

> **Deep dive:** `medium` — Traz dados empíricos inéditos (llms.txt ignorado, jornadas comparadas de múltiplos harnesses) e padrões emergentes de descoberta/governança da web agêntica, mas tem tom parcialmente promocional e pouca profundidade arquitetural em harness ou context-engineering.
