---
title: "Harnesses customizados para agentes"
type: "extract"
source: "x"
status_id: "2098866608785473858"
handle: "hwchase17"
url: "https://x.com/hwchase17/status/2098866608785473858"
created_at: "2026-09-12T20:09:29.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-hwchase17-in-case-you-want-to-build-a-domain-specific-harness-https-t--2098866608785473858.json]]"
tags: ["harness", "harness-engineering", "agent-loop", "agents", "context-engineering", "agent-tooling", "frameworks", "arquitetura", "context-management"]
topic: "Harnesses customizados para agentes"
summary: "Artigo do LangChain defende que agent = model + harness e que a utilidade de um agente depende do fit entre o harness e a tarefa; create_agent é o primitivo minimalista para construir harnesses sob medida, customizados via middleware. Vale salvar como referência de engenharia de harness/harness fit."
key_points: ["Agente = modelo + harness: o harness é o scaffolding que conecta o modelo ao mundo real e cujo trabalho é entregar o contexto certo ao modelo a cada passo do loop", "create_agent é propositalmente minimalista (implementa só o agent loop), em contraste com harnesses pré-montados e opinativos como Deep Agents e Claude Agent SDK, que não suportam fine-grained customization (prompting próprio, business logic, guardrails)", "Middleware engancha no loop em pontos específicos (antes/depois de chamadas de modelo e tools, startup/teardown) e oferece 4 alavancas: lógica determinística, ciclo de vida completo de tools, estado customizado persistente entre hooks, e stream handlers para filtrar/rotear eventos", "Middleware é composável e reutilizável: cada peça isolada pode ser compartilhada pela organização, fazendo novos agentes herdarem comportamento testado em batalha sem reconstrução", "Task-harness fit é o conceito-chave: todos os agentes internos do LangChain (GTM agent, coding agent assíncrono, no-code agent builder) são construídos sobre create_agent com stack de middleware ajustada à missão de cada agente"]
entities: ["LangChain", "Harrison Chase", "Sydney Runkle", "create_agent", "Deep Agents", "Claude Agent SDK", "Pi", "Anthropic"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://www.langchain.com/blog/how-to-build-a-custom-agent-harness"]
media: ["https://pbs.twimg.com/media/HSCsDIpXQAEQ0wV.jpg"]
relates-to: ["[[extracts/x/bookmarks/2026-09-14-shreyanshpatni_-want-to-build-a-domain-specific-agent-harness-this-is-a-grea--2099180288668750246|Construção de harness para agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-harness-of-harness-exciting-new-research-on-coding-agents-th--2095172426925801608|Harness-of-Harness: agentes de código autônomos]]", "[[extracts/x/bookmarks/2026-09-14-omarsar0-should-you-build-an-agent-harness-i-see-lots-of-opinions-abo--2099208894866178204|construção de agent harness]]", "[[extracts/x/bookmarks/2026-09-17-langchain-the-biggest-challenge-facing-an-agent-harness-is-context-eng--2100235963339313648|Context engineering em agent harnesses]]", "[[extracts/x/bookmarks/2026-09-14-omarsar0-learn-to-build-a-harness-folks-it-s-not-surprising-to-me-tha--2098809969252450451|harnesses domain-specific para agentes]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-find-the-whole-collection-here-https-t-co-hskmmhjf1l--2097449134202503657|Harness engineering evolução curada]]", "[[extracts/x/bookmarks/2026-09-14-mardehaym-the-model-is-the-smallest-most-swappable-part-key-principles--2099175716046643654|harness engineering principles]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-highly-recommended-model-harness-co-optimization-is-where-yo--2097790938911498494|model-harness co-optimization]]", "[[extracts/x/bookmarks/2026-09-15-omarsar0-on-building-an-agent-harness-from-scratch-got-so-many-questi--2099545598156288292|Construir agent harness do zero]]", "[[extracts/x/bookmarks/2026-09-12-kevinwhinnery-the-era-of-the-dumb-token-pipe-is-ending-agent-harness-apis--2098444890602455431|Agent harness APIs como integração]]", "[[extracts/x/bookmarks/2026-09-14-rohanpaul_ai-stanford-mit-paper-on-model-harnesses-shows-that-ai-performa--2098986025397977287|paper sobre model harnesses]]", "[[extracts/x/bookmarks/2026-09-15-omarsar0-if-you-build-your-own-harness-you-can-drive-that-cost-down-e--2099548107327275488|harness próprio vs. pronto]]", "[[extracts/x/bookmarks/2026-09-17-jacquelinesyc19-a-few-weeks-ago-i-wrote-that-our-whole-team-at-artie-uses-he--2100262432413528336|Hermes como harness de agentes por equipe]]", "[[extracts/x/bookmarks/2026-09-12-hwchase17-harnesses-should-make-context-engineering-easy-forking-subag--2097410530717704546|Forking de subagentes em deepagents]]", "[[extracts/x/bookmarks/2026-09-12-fchollet-i-would-have-assumed-it-was-fairly-obvious-but-in-case-it-s--2085323411903889876|Harness como arquitetura neurosimbólica]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-harness-engineering-is-a-top-skill-right-now-i-saw-a-great-o--2097449131648197024|coleção de papers sobre harness engineering]]", "[[extracts/x/bookmarks/2026-09-12-hwchase17-kai-is-very-cool-and-every-company-should-have-a-kai-this-ep--2097355841183596632|Stripe Kai: agente interno com Deep Agents]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-autosaddler-automatic-harness-optimization-with-durable-upda--2097931902594265474|Otimização automática de agent harness]]", "[[extracts/x/bookmarks/2026-09-14-dexhorthy-not-that-i-disagree-but-is-domain-specific-harness-just-a-re--2099208596622062031|Terminologia: domain specific harness vs AI agent]]", "[[extracts/x/bookmarks/2026-09-16-langchain-new-in-our-langsmith-essentials-course-a-capstone-weve-added--2099875992139415786|Capstone no curso LangSmith Essentials]]"]
theme: "Agent Harness Engineering"
---

# Harnesses customizados para agentes

**@hwchase17** · [2098866608785473858](https://x.com/hwchase17/status/2098866608785473858) · `resource`

## Resumo
Artigo do LangChain defende que agent = model + harness e que a utilidade de um agente depende do fit entre o harness e a tarefa; create_agent é o primitivo minimalista para construir harnesses sob medida, customizados via middleware. Vale salvar como referência de engenharia de harness/harness fit.

## Pontos-chave
- Agente = modelo + harness: o harness é o scaffolding que conecta o modelo ao mundo real e cujo trabalho é entregar o contexto certo ao modelo a cada passo do loop
- create_agent é propositalmente minimalista (implementa só o agent loop), em contraste com harnesses pré-montados e opinativos como Deep Agents e Claude Agent SDK, que não suportam fine-grained customization (prompting próprio, business logic, guardrails)
- Middleware engancha no loop em pontos específicos (antes/depois de chamadas de modelo e tools, startup/teardown) e oferece 4 alavancas: lógica determinística, ciclo de vida completo de tools, estado customizado persistente entre hooks, e stream handlers para filtrar/rotear eventos
- Middleware é composável e reutilizável: cada peça isolada pode ser compartilhada pela organização, fazendo novos agentes herdarem comportamento testado em batalha sem reconstrução
- Task-harness fit é o conceito-chave: todos os agentes internos do LangChain (GTM agent, coding agent assíncrono, no-code agent builder) são construídos sobre create_agent com stack de middleware ajustada à missão de cada agente

## Links
- https://www.langchain.com/blog/how-to-build-a-custom-agent-harness

## Entidades
LangChain, Harrison Chase, Sydney Runkle, create_agent, Deep Agents, Claude Agent SDK, Pi, Anthropic

> **Revisit:** `high` · **fonte:** `article`
