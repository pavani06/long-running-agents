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
