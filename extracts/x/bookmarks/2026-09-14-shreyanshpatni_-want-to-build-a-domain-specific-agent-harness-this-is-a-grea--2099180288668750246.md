---
title: "Construção de harness para agentes"
type: "extract"
source: "x"
status_id: "2099180288668750246"
handle: "shreyanshpatni_"
url: "https://x.com/shreyanshpatni_/status/2099180288668750246"
created_at: "2026-09-13T16:55:56.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-shreyanshpatni_-want-to-build-a-domain-specific-agent-harness-this-is-a-grea--2099180288668750246.json]]"
tags: ["harness", "harness-engineering", "agent-loop", "context-engineering", "agent-tooling", "frameworks", "production", "agents"]
topic: "Construção de harness para agentes"
summary: "Guia prático de Sydney Runkle (LangChain) sobre projetar harnesses customizados para agentes, defendendo que agente = modelo + harness e que a utilidade do agente depende do encaixe entre harness e tarefa. Apresenta create_agent como primitivo minimalista onde middleware composto (lógica determinística, ciclo de vida de tools, estado custom, stream handlers) é o mecanismo de customização."
key_points: ["Agente = model + harness: o harness é o scaffolding que conecta o modelo ao mundo real, e seu trabalho é entregar o contexto certo no momento certo a cada passo do loop.", "Harnesses pré-montados (Deep Agents, Claude Agent SDK) aceleram produção com stack opinativa de memória/gerência de contexto/sandboxing, mas muitos agentes exigem customização mais fina (prompting custom, lógica de negócio, guardrails) — por isso create_agent é propositalmente minimalista: só o agent loop + middleware como primitivo de customização.", "Middleware engancha no loop em pontos determinísticos (antes/depois de chamadas de modelo e tools, startup/teardown), cada peça cuida de uma única preocupação e compõe livremente com as demais, habilitando: lógica determinística (política, troca de modelo por complexidade, compaction), ciclo de vida completo de tools com setup/teardown, estado custom persistente entre hooks, e stream handlers para filtrar/rotear eventos (UI, audit log, monitoring).", "Task-harness fit é o conceito central: um harness de customer service difere radicalmente de um coding agent de longa duração; todos os agentes internos do LangChain (GTM agent, coding agent assíncrono, no-code builder) usam create_agent com stack de middleware sob medida para a missão.", "Middleware é reutilizável entre agentes da organização: novos agentes herdam comportamento testado em batalha sem reconstrução; LangChain shippa middleware pré-construído para os padrões mais comuns, e anything bespoke fica a um middleware custom de distância."]
entities: ["LangChain", "create_agent", "Sydney Runkle", "Shreyansh Patni", "Deep Agents", "Claude Agent SDK", "Pi", "Anthropic Claude", "Harrison Chase"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://langchain.com/blog/how-to-build-a-custom-agent-harness"]
media: ["https://pbs.twimg.com/media/HSHJVwsaQAEzltb.png"]
relates-to: ["[[extracts/x/bookmarks/2026-09-14-hwchase17-in-case-you-want-to-build-a-domain-specific-harness-https-t--2098866608785473858|Harnesses customizados para agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-harness-of-harness-exciting-new-research-on-coding-agents-th--2095172426925801608|Harness-of-Harness: agentes de código autônomos]]", "[[extracts/x/bookmarks/2026-09-14-omarsar0-should-you-build-an-agent-harness-i-see-lots-of-opinions-abo--2099208894866178204|construção de agent harness]]", "[[extracts/x/bookmarks/2026-09-14-omarsar0-learn-to-build-a-harness-folks-it-s-not-surprising-to-me-tha--2098809969252450451|harnesses domain-specific para agentes]]", "[[extracts/x/bookmarks/2026-09-14-mardehaym-the-model-is-the-smallest-most-swappable-part-key-principles--2099175716046643654|harness engineering principles]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-find-the-whole-collection-here-https-t-co-hskmmhjf1l--2097449134202503657|Harness engineering evolução curada]]", "[[extracts/x/bookmarks/2026-09-12-kevinwhinnery-the-era-of-the-dumb-token-pipe-is-ending-agent-harness-apis--2098444890602455431|Agent harness APIs como integração]]", "[[extracts/x/bookmarks/2026-09-12-hwchase17-kai-is-very-cool-and-every-company-should-have-a-kai-this-ep--2097355841183596632|Stripe Kai: agente interno com Deep Agents]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-autosaddler-automatic-harness-optimization-with-durable-upda--2097931902594265474|Otimização automática de agent harness]]", "[[extracts/x/bookmarks/2026-09-12-robotbird01-harness-pi-agent-skill-https-t-co-6eqhirel54--2098044628058689738|Arquitetura de plataforma harness empresarial]]", "[[extracts/x/bookmarks/2026-09-12-yenkel-great-to-see-the-muse-team-took-security-seriously-https-t-c--2097428458120835085|Arquitetura de segurança de agentes pessoais]]", "[[extracts/x/bookmarks/2026-09-12-hwchase17-harnesses-should-make-context-engineering-easy-forking-subag--2097410530717704546|Forking de subagentes em deepagents]]", "[[extracts/x/bookmarks/2026-09-12-sophiamyang-someone-please-tell-me-this-exists-a-meta-harness-kanban-boa--2098112529796878408|orquestração multi-plataforma de agentes]]"]
theme: "Tooling e harness de agentes"
---

# Construção de harness para agentes

**@shreyanshpatni_** · [2099180288668750246](https://x.com/shreyanshpatni_/status/2099180288668750246) · `resource`

## Resumo
Guia prático de Sydney Runkle (LangChain) sobre projetar harnesses customizados para agentes, defendendo que agente = modelo + harness e que a utilidade do agente depende do encaixe entre harness e tarefa. Apresenta create_agent como primitivo minimalista onde middleware composto (lógica determinística, ciclo de vida de tools, estado custom, stream handlers) é o mecanismo de customização.

## Pontos-chave
- Agente = model + harness: o harness é o scaffolding que conecta o modelo ao mundo real, e seu trabalho é entregar o contexto certo no momento certo a cada passo do loop.
- Harnesses pré-montados (Deep Agents, Claude Agent SDK) aceleram produção com stack opinativa de memória/gerência de contexto/sandboxing, mas muitos agentes exigem customização mais fina (prompting custom, lógica de negócio, guardrails) — por isso create_agent é propositalmente minimalista: só o agent loop + middleware como primitivo de customização.
- Middleware engancha no loop em pontos determinísticos (antes/depois de chamadas de modelo e tools, startup/teardown), cada peça cuida de uma única preocupação e compõe livremente com as demais, habilitando: lógica determinística (política, troca de modelo por complexidade, compaction), ciclo de vida completo de tools com setup/teardown, estado custom persistente entre hooks, e stream handlers para filtrar/rotear eventos (UI, audit log, monitoring).
- Task-harness fit é o conceito central: um harness de customer service difere radicalmente de um coding agent de longa duração; todos os agentes internos do LangChain (GTM agent, coding agent assíncrono, no-code builder) usam create_agent com stack de middleware sob medida para a missão.
- Middleware é reutilizável entre agentes da organização: novos agentes herdam comportamento testado em batalha sem reconstrução; LangChain shippa middleware pré-construído para os padrões mais comuns, e anything bespoke fica a um middleware custom de distância.

## Links
- https://langchain.com/blog/how-to-build-a-custom-agent-harness

## Entidades
LangChain, create_agent, Sydney Runkle, Shreyansh Patni, Deep Agents, Claude Agent SDK, Pi, Anthropic Claude, Harrison Chase

> **Revisit:** `high` · **fonte:** `article`
