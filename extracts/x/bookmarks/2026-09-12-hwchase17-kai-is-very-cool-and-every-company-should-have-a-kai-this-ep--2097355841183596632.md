---
title: "Stripe Kai: agente interno com Deep Agents"
type: "extract"
source: "x"
status_id: "2097355841183596632"
handle: "hwchase17"
url: "https://x.com/hwchase17/status/2097355841183596632"
created_at: "2026-09-08T16:06:14.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-hwchase17-kai-is-very-cool-and-every-company-should-have-a-kai-this-ep--2097355841183596632.json]]"
tags: ["agents", "agent-tooling", "harness-engineering", "agent-loop", "context-engineering", "context-management", "arquitetura", "production", "governanca", "roadmap"]
topic: "Stripe Kai: agente interno com Deep Agents"
summary: "Estudo de caso de como o Stripe construiu o Kai, agente de produtividade para todos os funcionários sobre o harness open-source Deep Agents (LangChain/LangGraph), detalhando a arquitetura em camadas, middleware de produção e sistema federado de skills. Referência concreta de harness de agente em escala empresarial (83% de adoção semanal)."
key_points: ["Arquitetura em camadas: Deep Agents como base (tool-calling loop, middleware, streaming, state), harness específico do Stripe integrando segurança/infra, camada de configuração para agentes customizados e UI do Kai — 'Deep Agents resolve os problemas não-Stripes para focarmos nos problemas Stripes'.", "Middleware-chave: filesystem virtual em S3 com padrão sync in/sync out para persistência de contexto entre turnos; sandbox exposto como ferramenta (não como ambiente do agente) para execução de código; sumarização ajustável (threshold, modelo, tamanho) para sessões longas e controle de custo via cache.", "Sistema de skills federado: 1000+ skills de 100+ times, 500+ ferramentas MCP internas; seleção de skills pelo LLM faz gate do carregamento dinâmico de ferramentas (two-pass), com skills fundamentais pinadas; degradação de qualidade observada acima de ~150 skills, motivando seleção híbrida com pré-filtro RAG/classificador.", "Velocidade e ROI: versão inicial construída por 1 engenheiro em 1 semana, validando o investimento em Python; atingiu meta trimestral de adoção em 1 semana e cresceu 16x (296 para 5000+ usuários em ~4 semanas); hoje 83% dos funcionários usam semanalmente em 60k+ sessões, com adoção maior em Marketing (95%) e GTM (87%) que em engenharia.", "Roadmap pós-PMF: escala da seleção de skills (seleção híbrida LLM + RAG/classificador), guardrails de governança e compliance, personalização comportamental automática do agente (ML classifiers para decidir planejar vs. responder direto) e colaboração multiusuário entre sessões."]
entities: ["Stripe", "Kai (Knowledge AI Platform)", "LangChain", "LangGraph", "Deep Agents", "Sharadh Krishnamurthy", "Anupam Upadhyay", "Chrissie", "Claude Code", "MCP", "AWS S3", "Harrison Chase"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://www.langchain.com/blog/how-stripe-built-their-knowledge-ai-platform-on-deep-agents"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420|Arquitetura de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-sat-down-with-the-founders-of-wisprflow-useactively-and-p--2097415273645228460|Claude Managed Agents em produção]]", "[[extracts/x/bookmarks/2026-09-12-robotbird01-harness-pi-agent-skill-https-t-co-6eqhirel54--2098044628058689738|Arquitetura de plataforma harness empresarial]]", "[[extracts/x/bookmarks/2026-09-12-kevinwhinnery-the-era-of-the-dumb-token-pipe-is-ending-agent-harness-apis--2098444890602455431|Agent harness APIs como integração]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-agents-api-is-a-bigger-deal-than-it-seems-openai-s-bet-on-ma--2098524621439914375|OpenAI Agents API e harness-as-a-service]]", "[[extracts/x/bookmarks/2026-09-12-hwchase17-harnesses-should-make-context-engineering-easy-forking-subag--2097410530717704546|Forking de subagentes em deepagents]]", "[[extracts/x/bookmarks/2026-09-12-ubereng-we-cut-uber-eats-search-latency-in-half-how-measure-identify--2098177194979983830|Uber Eats search latency halving]]", "[[extracts/x/bookmarks/2026-09-12-0xmovez-spacexai-engineer-lauren-tan-at-spacexai-90-of-engineers-run--2094868247162360099|Uso de agentes GrokBot na SpaceXAI]]", "[[extracts/x/bookmarks/2026-09-12-dhh-fable-one-shotted-a-rust-rewrite-of-the-terminaltexteffects--2086590006898958752|AI one-shot Rust rewrite performance]]"]
thin: false
theme: "Agent Harness e Evals"
---

# Stripe Kai: agente interno com Deep Agents

**@hwchase17** · [2097355841183596632](https://x.com/hwchase17/status/2097355841183596632) · `resource`

## Resumo
Estudo de caso de como o Stripe construiu o Kai, agente de produtividade para todos os funcionários sobre o harness open-source Deep Agents (LangChain/LangGraph), detalhando a arquitetura em camadas, middleware de produção e sistema federado de skills. Referência concreta de harness de agente em escala empresarial (83% de adoção semanal).

## Pontos-chave
- Arquitetura em camadas: Deep Agents como base (tool-calling loop, middleware, streaming, state), harness específico do Stripe integrando segurança/infra, camada de configuração para agentes customizados e UI do Kai — 'Deep Agents resolve os problemas não-Stripes para focarmos nos problemas Stripes'.
- Middleware-chave: filesystem virtual em S3 com padrão sync in/sync out para persistência de contexto entre turnos; sandbox exposto como ferramenta (não como ambiente do agente) para execução de código; sumarização ajustável (threshold, modelo, tamanho) para sessões longas e controle de custo via cache.
- Sistema de skills federado: 1000+ skills de 100+ times, 500+ ferramentas MCP internas; seleção de skills pelo LLM faz gate do carregamento dinâmico de ferramentas (two-pass), com skills fundamentais pinadas; degradação de qualidade observada acima de ~150 skills, motivando seleção híbrida com pré-filtro RAG/classificador.
- Velocidade e ROI: versão inicial construída por 1 engenheiro em 1 semana, validando o investimento em Python; atingiu meta trimestral de adoção em 1 semana e cresceu 16x (296 para 5000+ usuários em ~4 semanas); hoje 83% dos funcionários usam semanalmente em 60k+ sessões, com adoção maior em Marketing (95%) e GTM (87%) que em engenharia.
- Roadmap pós-PMF: escala da seleção de skills (seleção híbrida LLM + RAG/classificador), guardrails de governança e compliance, personalização comportamental automática do agente (ML classifiers para decidir planejar vs. responder direto) e colaboração multiusuário entre sessões.

## Links
- https://www.langchain.com/blog/how-stripe-built-their-knowledge-ai-platform-on-deep-agents

## Entidades
Stripe, Kai (Knowledge AI Platform), LangChain, LangGraph, Deep Agents, Sharadh Krishnamurthy, Anupam Upadhyay, Chrissie, Claude Code, MCP, AWS S3, Harrison Chase

> **Revisit:** `high` · **fonte:** `article`
