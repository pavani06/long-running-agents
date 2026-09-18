---
title: "FrontierAgent: runtime de agentes e evals"
type: "extract"
source: "x"
status_id: "2098489264749334565"
handle: "svpino"
url: "https://x.com/svpino/status/2098489264749334565"
created_at: "2026-09-11T19:10:03.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-svpino-the-frontieragent-framework-is-here-star-the-repo-https-t-co--2098489264749334565.json]]"
tags: ["agents", "multi-agent", "agent-loop", "agentes-orquestracao", "agent-tooling", "evals", "harness", "runtime", "frameworks", "permissions", "state", "tracing", "verification"]
topic: "FrontierAgent: runtime de agentes e evals"
summary: "Apodex lança o FrontierAgent, runtime open-source de agentes com TUI, workflows ReAct e Agent Team (coordenador + sub-agentes paralelos), sandbox de arquivos e harness de avaliação, junto ao modelo Apodex-1.1 via endpoint OpenAI-compatível. Vale salvar como referência de arquitetura de agentes e por benchmarks fortes (ex.: GDPval 78.8 e HLE 56.1 no Agent Team vs 59.3 e 49.0 no Apodex-1.0)."
key_points: ["Dois workflows nativos: ReAct (um agente stateful que pesquisa, lê/escreve arquivos, roda comandos e itera) e Agent Team (coordenador mantém task board, delega trabalho paralelo limitado a sub-agentes, coleta relatórios estruturados e sintetiza o resultado)", "Sandbox de arquivos por tarefa com política de caminhos: /inputs somente leitura, /workspace estado de trabalho, /outputs entregáveis persistentes; falhas de autorização e sandbox são fail-closed", "Intervenção assíncrona: digitar durante a execução enfileira uma instrução injetada no próximo limite seguro de turno sem descartar o run ativo; em Agent Team direciona o coordenador e sub-agentes em curso terminam", "Governança de execução: operações mutantes mostram diff e exigem aprovação (salvo --yes), sessões são checkpointadas, toda ação é tracejada localmente, /revert desfaz mudanças e --resume retoma runs", "Avaliação embutida: harness roda benchmarks em subprocessos isolados com coleta determinística de artefatos, concorrência e re-execução de falhas; suporta BrowseComp, GDPval, HLE, FrontierSearchBench e outros, com Apodex-1.1 Agent Team superando o 1.0 em todos os benchmarks listados"]
entities: ["FrontierAgent", "Apodex", "Apodex-1.1", "ApodexAI", "SGLang", "Hugging Face", "BrowseComp", "GDPval", "Humanity's Last Exam", "@svpino"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
links: ["https://github.com/ApodexAI/FrontierAgent", "https://huggingface.co/collections/apodex/apodex-11", "https://www.apodex.ai/"]
media: []
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-stevendcoffey-today-we-re-launching-the-agents-api-a-brand-new-way-to-buil--2098130889486274820|OpenAI Agents API launch]]", "[[extracts/x/bookmarks/2026-09-16-tom_doerr-manages-your-obsidian-vault-with-a-crew-of-8-ai-agents-and-1--2099928503487517062|Crew de agentes AI para Obsidian]]", "[[extracts/x/bookmarks/2026-09-12-akitaonrails-acabei-de-soltar-a-versao-2-0-do-meu-ai-memory-e-eu-acho-que--2095186765535392249|ai-memory 2.0: memória compartilhada de agentes]]", "[[extracts/x/bookmarks/2026-09-12-pythonhub-autosaddler-automatic-harness-optimization-with-durable-upda--2097931902594265474|Otimização automática de agent harness]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-finally-an-open-source-runtime-security-layer-for-your-agent--2098042808221511836|runtime security layer para agentes]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-also-see-our-open-source-reference-implementation-this-inclu--2095233747562180849|implementação de referência de agentes de comércio]]", "[[extracts/x/bookmarks/2026-09-17-teddyinmedia-your-ai-agent-can-now-collect-data-from-almost-any-website-x--2099859887102558507|Agent Reach: acesso web para agentes]]", "[[extracts/x/bookmarks/2026-09-12-hnshah-im-late-to-this-party-but-https-t-co-2qvqvyamhq-just-showed--2098603214065332290|Lançamento agent-native com demo de Excel]]", "[[extracts/x/bookmarks/2026-09-12-xudong07452910-agent-agent-scheduler-loopx-codexclaude-codecursorpi-agent--2085526335506592087|LoopX: orquestração cross-session de agentes]]", "[[extracts/x/bookmarks/2026-09-15-shanyanggm-github-1-tradingagents-ai-agent-https-t-co-nz1jbk3dkr-2-libr--2098941338297458746|Framework multi-agente de trading LLM]]", "[[extracts/x/bookmarks/2026-09-12-sophiamyang-someone-please-tell-me-this-exists-a-meta-harness-kanban-boa--2098112529796878408|orquestração multi-plataforma de agentes]]", "[[extracts/x/bookmarks/2026-09-12-elune0x-10-agent-evals-every-ai-engineer-should-know-1-golden-set-a--2080710242929697122|agent evals e golden set]]", "[[extracts/x/bookmarks/2026-09-18-josharosen-i-just-open-sourced-foreman-a-software-factory-foreman-built--2100573432089866717|Foreman: supervisor de coding agents]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-stanford-researchers-did-it-again-they-just-built-the-agent--2086079311279493389|versionamento agent-native de estado]]", "[[extracts/x/bookmarks/2026-09-12-realfxw-multi-agent-victor-dibia-designing-multiagent-systems-picoag--2097956088792396200|Arquitetura multi-agente do zero]]", "[[extracts/x/bookmarks/2026-09-17-nateberkopec-for-the-last-3-months-i-ve-been-telling-all-my-clients-to-mo--2099995262802641129|Executor: gateway MCP para agentes]]", "[[extracts/x/bookmarks/2026-09-12-guanlan-exo-harness-now-runs-natively-on-runta-in-frontierharness-ev--2098103620080369854|Exo Harness custo por tarefa]]", "[[extracts/x/bookmarks/2026-09-12-andrewyng-openworker-an-open-source-agent-that-doesn-t-just-chat-but-c--2092315079576555806|OpenWorker: agente open source de tarefas locais]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-brilliant-new-paper-from-the-qwen-team-it-provides-insights--2095880318146507139|Ambientes de treino de agentes]]", "[[extracts/x/bookmarks/2026-09-17-shengkunye-repo-here-https-t-co-piqc19b4jk--2100331009015480519|Monid: gateway unificado de ferramentas para agentes]]", "[[extracts/x/bookmarks/2026-09-16-dair_ai-is-bash-all-you-need-interesting-paper-from-microsoft-if-you--2099925472629150164|Comparando interfaces de ferramentas para agentes]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-this-has-ended-up-being-better-than-expected-and-fills-an-in--2094156122441625770|AFK agent workflow vs /implement-spec]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-the-qwen-team-if-you-evaluate-agents-on-an--2094872928240447665|Benchmark longitudinal de agentes e-commerce]]", "[[extracts/x/bookmarks/2026-09-18-completeskeptic-game-race-from-one-wikipedia-page-to-another-using-only-link--2099925688925184171|Wikipedia race como benchmark de agentes]]"]
theme: "Ecossistema Claude e Agent Tooling"
---

# FrontierAgent: runtime de agentes e evals

**@svpino** · [2098489264749334565](https://x.com/svpino/status/2098489264749334565) · `announcement`

## Resumo
Apodex lança o FrontierAgent, runtime open-source de agentes com TUI, workflows ReAct e Agent Team (coordenador + sub-agentes paralelos), sandbox de arquivos e harness de avaliação, junto ao modelo Apodex-1.1 via endpoint OpenAI-compatível. Vale salvar como referência de arquitetura de agentes e por benchmarks fortes (ex.: GDPval 78.8 e HLE 56.1 no Agent Team vs 59.3 e 49.0 no Apodex-1.0).

## Pontos-chave
- Dois workflows nativos: ReAct (um agente stateful que pesquisa, lê/escreve arquivos, roda comandos e itera) e Agent Team (coordenador mantém task board, delega trabalho paralelo limitado a sub-agentes, coleta relatórios estruturados e sintetiza o resultado)
- Sandbox de arquivos por tarefa com política de caminhos: /inputs somente leitura, /workspace estado de trabalho, /outputs entregáveis persistentes; falhas de autorização e sandbox são fail-closed
- Intervenção assíncrona: digitar durante a execução enfileira uma instrução injetada no próximo limite seguro de turno sem descartar o run ativo; em Agent Team direciona o coordenador e sub-agentes em curso terminam
- Governança de execução: operações mutantes mostram diff e exigem aprovação (salvo --yes), sessões são checkpointadas, toda ação é tracejada localmente, /revert desfaz mudanças e --resume retoma runs
- Avaliação embutida: harness roda benchmarks em subprocessos isolados com coleta determinística de artefatos, concorrência e re-execução de falhas; suporta BrowseComp, GDPval, HLE, FrontierSearchBench e outros, com Apodex-1.1 Agent Team superando o 1.0 em todos os benchmarks listados

## Links
- https://github.com/ApodexAI/FrontierAgent
- https://huggingface.co/collections/apodex/apodex-11
- https://www.apodex.ai/

## Entidades
FrontierAgent, Apodex, Apodex-1.1, ApodexAI, SGLang, Hugging Face, BrowseComp, GDPval, Humanity's Last Exam, @svpino

> **Revisit:** `high` · **fonte:** `article`
