---
title: "Escalonando storage Python na OpenAI"
type: "extract"
source: "x"
status_id: "2098502031338340416"
handle: "OpenAIDevs"
url: "https://x.com/OpenAIDevs/status/2098502031338340416"
created_at: "2026-09-11T20:00:47.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-openaidevs-while-we-ve-now-launched-a-rust-rewrite-we-re-sharing-those--2098502031338340416.json]]"
tags: ["performance", "production", "arquitetura", "observability", "data-platform", "monitoramento"]
topic: "Escalonando storage Python na OpenAI"
summary: "OpenAI detalha como escalou o Habitat, sua plataforma de storage online escrita em Python, a 70M+ requisições/s e 500 PB para 1B de usuários semanais, tratando a escolha do Python como dívida técnica estratégica (com rewrite em Rust depois facilitado por Codex/GPT). O post é rico em diagnósticos concretos de tail latency, asyncio e falhas metastáveis."
key_points: ["Migraram Habitat de library client-side para serviço standalone porque coordenar deploys retrocompatíveis across dezenas de serviços era frágil — um episódio de rollback de um único time causou a outage que tentavam evitar; o serviço criou ponto único de controle para deploy, observabilidade e segurança (access control, audit logging).", "Aceitaram as ineficiências do Python deliberadamente ('incursão estratégica de dívida técnica') para priorizar desbloqueio de produto e estabilidade, apostando que Codex/GPT tornariam a migração futura viável — aposta que se confirmou com o rewrite em Rust.", "Em serviços Python de alta escala, a tail latency é dominada por scheduling delay do asyncio (GIL impede paralelismo de CPU para roteamento, compressão, criptografia, checksumming, shadowing); medem empiricamente o atraso do event loop via delta entre execução esperada e real de background tasks, e mantêm poucas requisições concorrentes por processo escalando massivamente o número de workers.", "CPU profiling em produção revelou causa-raiz de stalls: polling do Statsig (feature flags) a cada minuto sem jitter, com config gigante de todas as regras, em até 8 processos/pod — fix: config menor e direcionada, intervalo maior de refresh e jitter nas tasks de fundo.", "Connection pooling client-side era antitético ao balanceamento: o reuse LIFO do TCPConnector do aiohttp causou falha metastável em que pods sobrecarregados atraíam cada vez mais tráfego até degradação runaway; limitar a duração máxima de reuse de conexões mitigou o problema."]
entities: ["OpenAI", "Habitat", "ChatGPT", "Azure Cosmos DB", "Statsig", "aiohttp", "asyncio", "Python", "Rust", "Codex", "GPT"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
links: ["https://openai.com/index/scaling-storage-one-billion-users-part-one"]
media: []
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-openaidevs-habitat-is-openai-s-online-storage-platform-that-powers-ever--2098502006935814272|Habitat: storage da OpenAI em Rust]]", "[[extracts/x/bookmarks/2026-09-12-openaidevs-python-allowed-for-rapid-prototyping-of-our-platform-to-supp--2098502018998649036|Python em escala na OpenAI]]", "[[extracts/x/bookmarks/2026-09-12-ubereng-we-cut-uber-eats-search-latency-in-half-how-measure-identify--2098177194979983830|Uber Eats search latency halving]]", "[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-sat-down-with-the-founders-of-wisprflow-useactively-and-p--2097415273645228460|Claude Managed Agents em produção]]", "[[extracts/x/bookmarks/2026-09-12-dhh-fable-one-shotted-a-rust-rewrite-of-the-terminaltexteffects--2086590006898958752|AI one-shot Rust rewrite performance]]", "[[extracts/x/bookmarks/2026-09-12-zostaff-a-jane-street-engineer-in-a-talk-on-how-an-exchange-is-actua--2081088443698868526|arquitetura de exchanges financeiras]]"]
theme: "Tooling de IA e Performance"
---

# Escalonando storage Python na OpenAI

**@OpenAIDevs** · [2098502031338340416](https://x.com/OpenAIDevs/status/2098502031338340416) · `resource`

## Resumo
OpenAI detalha como escalou o Habitat, sua plataforma de storage online escrita em Python, a 70M+ requisições/s e 500 PB para 1B de usuários semanais, tratando a escolha do Python como dívida técnica estratégica (com rewrite em Rust depois facilitado por Codex/GPT). O post é rico em diagnósticos concretos de tail latency, asyncio e falhas metastáveis.

## Pontos-chave
- Migraram Habitat de library client-side para serviço standalone porque coordenar deploys retrocompatíveis across dezenas de serviços era frágil — um episódio de rollback de um único time causou a outage que tentavam evitar; o serviço criou ponto único de controle para deploy, observabilidade e segurança (access control, audit logging).
- Aceitaram as ineficiências do Python deliberadamente ('incursão estratégica de dívida técnica') para priorizar desbloqueio de produto e estabilidade, apostando que Codex/GPT tornariam a migração futura viável — aposta que se confirmou com o rewrite em Rust.
- Em serviços Python de alta escala, a tail latency é dominada por scheduling delay do asyncio (GIL impede paralelismo de CPU para roteamento, compressão, criptografia, checksumming, shadowing); medem empiricamente o atraso do event loop via delta entre execução esperada e real de background tasks, e mantêm poucas requisições concorrentes por processo escalando massivamente o número de workers.
- CPU profiling em produção revelou causa-raiz de stalls: polling do Statsig (feature flags) a cada minuto sem jitter, com config gigante de todas as regras, em até 8 processos/pod — fix: config menor e direcionada, intervalo maior de refresh e jitter nas tasks de fundo.
- Connection pooling client-side era antitético ao balanceamento: o reuse LIFO do TCPConnector do aiohttp causou falha metastável em que pods sobrecarregados atraíam cada vez mais tráfego até degradação runaway; limitar a duração máxima de reuse de conexões mitigou o problema.

## Links
- https://openai.com/index/scaling-storage-one-billion-users-part-one

## Entidades
OpenAI, Habitat, ChatGPT, Azure Cosmos DB, Statsig, aiohttp, asyncio, Python, Rust, Codex, GPT

> **Revisit:** `high` · **fonte:** `article`
