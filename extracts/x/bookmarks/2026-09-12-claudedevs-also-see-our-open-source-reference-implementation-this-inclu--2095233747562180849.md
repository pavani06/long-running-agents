---
title: "implementação de referência de agentes de comércio"
type: "extract"
source: "x"
status_id: "2095233747562180849"
handle: "ClaudeDevs"
url: "https://x.com/ClaudeDevs/status/2095233747562180849"
created_at: "2026-09-02T19:33:47.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-claudedevs-also-see-our-open-source-reference-implementation-this-inclu--2095233747562180849.json]]"
tags: ["agents", "agent-tooling", "gate-design", "runtime", "frameworks", "permissions", "memory-architecture", "production"]
topic: "implementação de referência de agentes de comércio"
summary: "Anthropic abriu o código de dois agentes de comércio construídos sobre Claude (shopping para clientes, merchant para back-office), cada um definido uma vez (prompt, skills, contratos de ferramentas, gates) e executável em três runtimes: Messages API, Claude Agent SDK e Managed Agents. Vale salvar como referência de arquitetura de agentes produtivos, com quatro verticais demo e um plugin do Claude Code que gera agentes contra seu próprio backend."
key_points: ["Cada agente é definido uma vez (prompt, skills, tool contracts, gates) e roda em três caminhos — Messages API, Agent SDK e Managed Agents — com os mesmos guardrails válidos em todos (fencing, gates de proveniência, caps, validação de memória executam dentro da tool call).", "Escrita segura por design: toda escrita do merchant é staged e só aplicada via superfície de aprovação humana; checkout entrega o carrinho ao host e o modelo nunca vê a URL de pagamento; nada cobra cartão ou altera listing ao vivo.", "Integração via interfaces de backend (StorefrontBackend/MerchantBackend): métodos rodam server-side com credencial do host e o modelo só lê o resultado; conectores oficiais (Stripe, Snowflake, BigQuery, Slack etc.) são alvo de integração, com servidores MCP montados no manifest no Managed Agents.", "Plugin Claude Code scaffolding (/scaffold-commerce-agent, /add-commerce-flow, /author-commerce-evals, /review-commerce-agent) cria ou revisa um agente contra seus sistemas usando o repo como referência.", "Configuração progressiva e modularidade: switches enable_* removem ferramentas, linhas de prompt e regra de grounding de sistemas que o negócio não tem; quatro verticais executáveis (retail, travel, telecom, entertainment) demonstram os mesmos pacotes; pilotos podem stubbar métodos sem mudar bytes de prompt."]
entities: ["Anthropic", "Claude", "Claude Code", "Messages API", "Claude Agent SDK", "Managed Agents", "MCP", "ACME", "Snowflake", "BigQuery", "Databricks", "Amplitude", "Stripe", "QuickBooks", "AWS Bedrock", "GCP Vertex AI", "Microsoft Foundry"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/anthropics/commerce-agents"]
media: []
---

# implementação de referência de agentes de comércio

**@ClaudeDevs** · [2095233747562180849](https://x.com/ClaudeDevs/status/2095233747562180849) · `resource`

## Resumo
Anthropic abriu o código de dois agentes de comércio construídos sobre Claude (shopping para clientes, merchant para back-office), cada um definido uma vez (prompt, skills, contratos de ferramentas, gates) e executável em três runtimes: Messages API, Claude Agent SDK e Managed Agents. Vale salvar como referência de arquitetura de agentes produtivos, com quatro verticais demo e um plugin do Claude Code que gera agentes contra seu próprio backend.

## Pontos-chave
- Cada agente é definido uma vez (prompt, skills, tool contracts, gates) e roda em três caminhos — Messages API, Agent SDK e Managed Agents — com os mesmos guardrails válidos em todos (fencing, gates de proveniência, caps, validação de memória executam dentro da tool call).
- Escrita segura por design: toda escrita do merchant é staged e só aplicada via superfície de aprovação humana; checkout entrega o carrinho ao host e o modelo nunca vê a URL de pagamento; nada cobra cartão ou altera listing ao vivo.
- Integração via interfaces de backend (StorefrontBackend/MerchantBackend): métodos rodam server-side com credencial do host e o modelo só lê o resultado; conectores oficiais (Stripe, Snowflake, BigQuery, Slack etc.) são alvo de integração, com servidores MCP montados no manifest no Managed Agents.
- Plugin Claude Code scaffolding (/scaffold-commerce-agent, /add-commerce-flow, /author-commerce-evals, /review-commerce-agent) cria ou revisa um agente contra seus sistemas usando o repo como referência.
- Configuração progressiva e modularidade: switches enable_* removem ferramentas, linhas de prompt e regra de grounding de sistemas que o negócio não tem; quatro verticais executáveis (retail, travel, telecom, entertainment) demonstram os mesmos pacotes; pilotos podem stubbar métodos sem mudar bytes de prompt.

## Links
- https://github.com/anthropics/commerce-agents

## Entidades
Anthropic, Claude, Claude Code, Messages API, Claude Agent SDK, Managed Agents, MCP, ACME, Snowflake, BigQuery, Databricks, Amplitude, Stripe, QuickBooks, AWS Bedrock, GCP Vertex AI, Microsoft Foundry

> **Revisit:** `high` · **fonte:** `article`
