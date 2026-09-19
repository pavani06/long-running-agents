---
title: "Monid: gateway unificado de ferramentas para agentes"
type: "extract"
source: "x"
status_id: "2100331009015480519"
handle: "shengkunye"
url: "https://x.com/shengkunye/status/2100331009015480519"
created_at: "2026-09-16T21:08:29.000Z"
extracted: "2026-09-18"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-17-shengkunye-repo-here-https-t-co-piqc19b4jk--2100331009015480519.json]]"
tags: ["agent-tooling", "agents", "agentic-coding", "spec-driven-development", "arquitetura", "testes-qa", "stack-tooling", "gate-design"]
topic: "Monid: gateway unificado de ferramentas para agentes"
summary: "Monid é um 'OpenRouter para ferramentas de agentes': uma base URL e uma chave dão acesso a 2.000+ ferramentas em 72+ providers, com o repo definindo a camada de conectores declarativos. Conectores são contratos que um coding agent consegue escrever, então adicionar uma API vira um pull request, com billing ancorado na resposta crua e seleção de endpoint dinâmica por preço/latência/saúde."
key_points: ["Conectores são totalmente declarativos (defineProvider/defineEndpoint em zod, sem client/adaptor por provider): aponte um coding agent para AGENT.md + docs da sua API + connectors/exa/ como exemplo, e ele produz o provider, schemas e testes — revisar é checar se o conector descreve a API corretamente, não se roda", "discover ranqueia o catálogo inteiro por chamada: retorna preço, health ao vivo, p50/p95 observados e dicas de endpoint mais barato/melhor — a API é escolhida em runtime contra tudo disponível, não pinada em código meses antes", "Uso é medido na resposta crua (raw envelope) antes de qualquer output mapping; erro de vendor ou resultado vazio completa como dado e settle em zero — o que é cobrado é o que voltou pelo wire", "Execução em sealed unit: funções viram referências por content-hash internadas estilo git-blob; o mesmo artefato roda local (com sua chave), em CI por replay de fixtures sem rede (188 testes, sem vendor keys) e no hosted (credenciais injetadas dentro do transporte, nunca no engine)", "Scaffold para Apify actors: deno task apify:scaffold lê o input schema publicado do actor e gera o schema/inputs.ts em zod estático para revisar e commitar; stack é Deno 2.x, MIT, com openspec/ como registro de decisões"]
entities: ["Monid", "OpenRouter", "TinyFish", "Apify", "Deno", "Exa", "GitHub"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/monid-ai/monid"]
media: []
theme: "Ecossistema Claude e Agent Tooling"
relates-to: ["[[extracts/x/bookmarks/2026-09-17-shengkunye-we-just-killed-monid-ourselves-monid-is-now-open-source-the--2100330818958975088|Monid: OpenRouter para tools de agentes]]", "[[extracts/x/bookmarks/2026-09-17-teddyinmedia-your-ai-agent-can-now-collect-data-from-almost-any-website-x--2099859887102558507|Agent Reach: acesso web para agentes]]", "[[extracts/x/bookmarks/2026-09-17-nateberkopec-for-the-last-3-months-i-ve-been-telling-all-my-clients-to-mo--2099995262802641129|Executor: gateway MCP para agentes]]", "[[extracts/x/bookmarks/2026-09-12-andrebrov-my-biggest-recent-discovery-herdrdev-this-is-wow-i-run-25-ai--2097134891833917946|Console para orquestrar agentes de código]]", "[[extracts/x/bookmarks/2026-09-16-tom_doerr-manages-your-obsidian-vault-with-a-crew-of-8-ai-agents-and-1--2099928503487517062|Crew de agentes AI para Obsidian]]", "[[extracts/x/bookmarks/2026-09-12-svpino-the-frontieragent-framework-is-here-star-the-repo-https-t-co--2098489264749334565|FrontierAgent: runtime de agentes e evals]]"]
---

# Monid: gateway unificado de ferramentas para agentes

**@shengkunye** · [2100331009015480519](https://x.com/shengkunye/status/2100331009015480519) · `tool`

## Resumo
Monid é um 'OpenRouter para ferramentas de agentes': uma base URL e uma chave dão acesso a 2.000+ ferramentas em 72+ providers, com o repo definindo a camada de conectores declarativos. Conectores são contratos que um coding agent consegue escrever, então adicionar uma API vira um pull request, com billing ancorado na resposta crua e seleção de endpoint dinâmica por preço/latência/saúde.

## Pontos-chave
- Conectores são totalmente declarativos (defineProvider/defineEndpoint em zod, sem client/adaptor por provider): aponte um coding agent para AGENT.md + docs da sua API + connectors/exa/ como exemplo, e ele produz o provider, schemas e testes — revisar é checar se o conector descreve a API corretamente, não se roda
- discover ranqueia o catálogo inteiro por chamada: retorna preço, health ao vivo, p50/p95 observados e dicas de endpoint mais barato/melhor — a API é escolhida em runtime contra tudo disponível, não pinada em código meses antes
- Uso é medido na resposta crua (raw envelope) antes de qualquer output mapping; erro de vendor ou resultado vazio completa como dado e settle em zero — o que é cobrado é o que voltou pelo wire
- Execução em sealed unit: funções viram referências por content-hash internadas estilo git-blob; o mesmo artefato roda local (com sua chave), em CI por replay de fixtures sem rede (188 testes, sem vendor keys) e no hosted (credenciais injetadas dentro do transporte, nunca no engine)
- Scaffold para Apify actors: deno task apify:scaffold lê o input schema publicado do actor e gera o schema/inputs.ts em zod estático para revisar e commitar; stack é Deno 2.x, MIT, com openspec/ como registro de decisões

## Links
- https://github.com/monid-ai/monid

## Entidades
Monid, OpenRouter, TinyFish, Apify, Deno, Exa, GitHub

> **Revisit:** `high` · **fonte:** `article`
