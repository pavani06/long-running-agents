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
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-claudedevs-read-the-full-announcement-https-t-co-cdudn3gvhd--2095233748719817153|Blueprint de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-retailers-running-shopping-agents-on-claude-have-seen-carts--2095233746366808420|Arquitetura de agentes de comércio com Claude]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-re-open-sourcing-claude-commerce-agents-this-is-a-bluepri--2095233745167282602|agentes de comércio open-source]]", "[[extracts/x/bookmarks/2026-09-16-undefinedki-this-is-a-goldmine-anthropic-just-published-the-full-archite--2099839040241516872|arquitetura de agentes de comércio em produção]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-sat-down-with-the-founders-of-wisprflow-useactively-and-p--2097415273645228460|Claude Managed Agents em produção]]", "[[extracts/x/bookmarks/2026-09-16-tom_doerr-manages-your-obsidian-vault-with-a-crew-of-8-ai-agents-and-1--2099928503487517062|Crew de agentes AI para Obsidian]]", "[[extracts/x/bookmarks/2026-09-12-svpino-the-frontieragent-framework-is-here-star-the-repo-https-t-co--2098489264749334565|FrontierAgent: runtime de agentes e evals]]", "[[extracts/x/bookmarks/2026-09-12-tom_doerr-hyperresearch-turns-claude-code-into-a-research-agent-that-i--2097841937642332595|Agente de pesquisa profunda para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-andrewcurran_-a-man-in-australia-asked-his-agent-claude-running-on-opencla--2086567854850384054|agente explora vulnerabilidade em agendamento]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-ve-added-ant-apply-to-the-ant-cli-now-you-can-declare-cla--2095651107645145538|ant apply: agentes como código]]", "[[extracts/x/bookmarks/2026-09-14-illscience-had-many-conversations-this-weekend-re-instinct-muse-consume--2099205025797144669|Consumer agents e commerce]]", "[[extracts/x/bookmarks/2026-09-15-shanyanggm-github-1-tradingagents-ai-agent-https-t-co-nz1jbk3dkr-2-libr--2098941338297458746|Framework multi-agente de trading LLM]]", "[[extracts/x/bookmarks/2026-09-12-realfxw-multi-agent-victor-dibia-designing-multiagent-systems-picoag--2097956088792396200|Arquitetura multi-agente do zero]]", "[[extracts/x/bookmarks/2026-09-12-hnshah-im-late-to-this-party-but-https-t-co-2qvqvyamhq-just-showed--2098603214065332290|Lançamento agent-native com demo de Excel]]", "[[extracts/x/bookmarks/2026-09-14-treytaylorceo-illscience-agents-are-largely-extensions-of-people-in-the-co--2099208649411321980|incentivos e preferências em agentes comerciais]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-the-qwen-team-if-you-evaluate-agents-on-an--2094872928240447665|Benchmark longitudinal de agentes e-commerce]]"]
theme: "Tooling e infra de agentes"
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
