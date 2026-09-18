---
title: "Escalando CI/test selection para agentic coding"
type: "extract"
source: "x"
status_id: "2099577600159158765"
handle: "addyosmani"
url: "https://x.com/addyosmani/status/2099577600159158765"
created_at: "2026-09-14T19:14:42.000Z"
extracted: "2026-09-16"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-15-addyosmani-at-anthropic-claude-now-writes-80-of-our-code-engineers-ship--2099577600159158765.json]]"
tags: ["agentic-coding", "harness", "performance", "arquitetura", "state", "testes-qa", "observability", "production"]
topic: "Escalando CI/test selection para agentic coding"
summary: "Anthropic relata que agentic coding (Claude escreve 80% do código, engineers ship 8x mais código/trimestre) elevou jobs de CI 25x em 6 meses; a solução sustentável foi redesenhar o serviço de test impact analysis como workers stateless com journal em in-memory store, não aplicar patches incrementais."
key_points: ["Métricas do impacto: 8x mais código por engenheiro por trimestre desde 2021-2025, 80% escrito por Claude, 10x mais testes e 25x mais jobs de CI em 6 meses, com número quase constante de engenheiros.", "Três quick fixes tiveram vida útil decrescente — dobrar cores (70 dias), shard por pacote com um writer por pacote (29 dias), restart (<1 dia) — ilustrando a lição: sempre planejar para o exponencial em vez de half-measures.", "Redesenho final: listener stateless processa qualquer resultado e anexa a um journal em in-memory store; um consumer separado consolida histórico por teste a cada segundos; selector consulta rapidamente — caro, mas horizontalmente escalável e 3 semanas para 1 engenheiro (antes ~um trimestre).", "Agentes mudam o formato de carga: PRs menores e mais granulares, atividade contínua (noites/fins de semana) sobre piso elevado e ainda bursty via humanos — mais razão para seleção determinística de testes em vez de rodar tudo em todo PR.", "Recomendações acionáveis: projetar v0 assumindo 25x de carga em dois trimestres (a bar de over-engineering subiu), instrumentar serviços como 'olhos e ouvidos' do Claude para hill-climbing autônomo, manter estado fora do processo e evitar singletons sem medição/canary."]
entities: ["Anthropic", "Claude", "Claude Tag", "@addyosmani"]
content_type: "resource"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://claude.com/blog/agentic-coding-is-straining-ci-heres-how-we-scaled-test-impact-analysis-at-anthropic"]
media: ["https://pbs.twimg.com/media/HSMyfjPaUAApdN6.jpg"]
theme: "Tooling Agêntico para Código"
relates-to: ["[[extracts/x/bookmarks/2026-09-16-gergelyorosz-here-s-what-openai-s-agentic-software-factory-looks-like-tod--2099945497377091902|Fábrica de software agêntica da OpenAI]]", "[[extracts/x/bookmarks/2026-09-12-ubereng-we-cut-uber-eats-search-latency-in-half-how-measure-identify--2098177194979983830|Uber Eats search latency halving]]", "[[extracts/x/bookmarks/2026-09-12-hackernoon-ai-is-raising-the-baseline-for-software-engineering-this-art--2082839180736889054|AI e plataformas de engenharia]]", "[[extracts/x/bookmarks/2026-09-12-0xdeliriumm-boris-cherny-lead-of-claude-code-at-anthropic-published-a-pi--2081050632727793775|pipeline de code review com agentes]]", "[[extracts/x/bookmarks/2026-09-12-zodchiii-the-creator-of-claude-code-boris-cherny-every-night-i-have-h--2079182515462369399|Engenharia com loops de agentes]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-we-sat-down-with-the-founders-of-wisprflow-useactively-and-p--2097415273645228460|Claude Managed Agents em produção]]", "[[extracts/x/bookmarks/2026-09-17-mattpocockuk-a-great-idea-i-m-stealing-from-dexhorthy-when-you-first-star--2100178563362074889|software factory incremental com agentes]]", "[[extracts/x/bookmarks/2026-09-12-openaidevs-while-we-ve-now-launched-a-rust-rewrite-we-re-sharing-those--2098502031338340416|Escalonando storage Python na OpenAI]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-here-s-how-our-team-uses-claude-tag-for-on-call-when-an-aler--2098508880921899197|On-call automation with Claude]]", "[[extracts/x/bookmarks/2026-09-12-stretchcloud-spotify-s-engineering-team-cut-claude-code-token-usage-by-90--2096439998539321653|Portal: roteamento de dois modelos no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-undefinedki-spotify-just-published-the-internal-setup-their-engineers-us--2095942506433089832|Setup Claude Code no Spotify]]", "[[extracts/x/bookmarks/2026-09-15-robshocks-1-000-prs-a-month-what-does-that-agent-workflow-look-like-a--2097381547493978562|Agentic coding workflow (PStack)]]", "[[extracts/x/bookmarks/2026-09-12-dhh-fable-one-shotted-a-rust-rewrite-of-the-terminaltexteffects--2086590006898958752|AI one-shot Rust rewrite performance]]", "[[extracts/x/bookmarks/2026-09-12-openaidevs-habitat-is-openai-s-online-storage-platform-that-powers-ever--2098502006935814272|Habitat: storage da OpenAI em Rust]]", "[[extracts/x/bookmarks/2026-09-12-zostaff-a-jane-street-engineer-in-a-talk-on-how-an-exchange-is-actua--2081088443698868526|arquitetura de exchanges financeiras]]", "[[extracts/x/bookmarks/2026-09-12-signulll-talked-to-a-guy-from-anthropic-for-a-long-time-last-night-fa--2093042350427881973|hiring em frontier labs]]", "[[extracts/x/bookmarks/2026-09-16-schteppe-the-crap-change-risk-anti-patterns-metric-is-a-software-qual--2099728101366276474|Métrica CRAP de risco de mudança]]"]
---

# Escalando CI/test selection para agentic coding

**@addyosmani** · [2099577600159158765](https://x.com/addyosmani/status/2099577600159158765) · `resource`

## Resumo
Anthropic relata que agentic coding (Claude escreve 80% do código, engineers ship 8x mais código/trimestre) elevou jobs de CI 25x em 6 meses; a solução sustentável foi redesenhar o serviço de test impact analysis como workers stateless com journal em in-memory store, não aplicar patches incrementais.

## Pontos-chave
- Métricas do impacto: 8x mais código por engenheiro por trimestre desde 2021-2025, 80% escrito por Claude, 10x mais testes e 25x mais jobs de CI em 6 meses, com número quase constante de engenheiros.
- Três quick fixes tiveram vida útil decrescente — dobrar cores (70 dias), shard por pacote com um writer por pacote (29 dias), restart (<1 dia) — ilustrando a lição: sempre planejar para o exponencial em vez de half-measures.
- Redesenho final: listener stateless processa qualquer resultado e anexa a um journal em in-memory store; um consumer separado consolida histórico por teste a cada segundos; selector consulta rapidamente — caro, mas horizontalmente escalável e 3 semanas para 1 engenheiro (antes ~um trimestre).
- Agentes mudam o formato de carga: PRs menores e mais granulares, atividade contínua (noites/fins de semana) sobre piso elevado e ainda bursty via humanos — mais razão para seleção determinística de testes em vez de rodar tudo em todo PR.
- Recomendações acionáveis: projetar v0 assumindo 25x de carga em dois trimestres (a bar de over-engineering subiu), instrumentar serviços como 'olhos e ouvidos' do Claude para hill-climbing autônomo, manter estado fora do processo e evitar singletons sem medição/canary.

## Links
- https://claude.com/blog/agentic-coding-is-straining-ci-heres-how-we-scaled-test-impact-analysis-at-anthropic

## Entidades
Anthropic, Claude, Claude Tag, @addyosmani

> **Revisit:** `high` · **fonte:** `article`
