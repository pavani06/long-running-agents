---
title: "paper sobre model harnesses"
type: "extract"
source: "x"
status_id: "2098986025397977287"
handle: "rohanpaul_ai"
url: "https://x.com/rohanpaul_ai/status/2098986025397977287"
created_at: "2026-09-13T04:04:00.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-rohanpaul_ai-stanford-mit-paper-on-model-harnesses-shows-that-ai-performa--2098986025397977287.json]]"
tags: ["harness", "harness-engineering", "context-engineering", "context-management", "agent-loop", "agents", "performance"]
topic: "paper sobre model harnesses"
summary: "Paper de Stanford + MIT argumenta que o desempenho de sistemas de IA depende do 'harness' — o código do sistema ao redor do modelo — tanto quanto do próprio LLM. Com o mesmo modelo subjacente, resultados diferentes emergem conforme storage, retrieval e fluxo são orquestrados."
key_points: ["O harness decide o que armazenar, recuperar e apresentar ao modelo como contexto", "A lógica de execução do workflow vive no harness, não no modelo", "Mesmo LLM subjacente produz desempenho diferente conforme o harness que o envolve", "Implicação prática: esforço de engenharia deve mirar design do harness, não apenas escolha de modelo"]
entities: ["Stanford", "MIT", "Rohan Paul"]
content_type: "resource"
revisit: "high"
grounded_in: "tweet"
thin: false
links: []
media: ["https://pbs.twimg.com/media/HSEDrGVakAE0hNz.png"]
theme: "Agent Harness Engineering"
relates-to: ["[[extracts/x/bookmarks/2026-09-12-ycombinator-harnesses-often-get-dismissed-as-just-scaffolding-just-promp--2096970626036855197|harness engineering em agentes de IA]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-highly-recommended-model-harness-co-optimization-is-where-yo--2097790938911498494|model-harness co-optimization]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-find-the-whole-collection-here-https-t-co-hskmmhjf1l--2097449134202503657|Harness engineering evolução curada]]", "[[extracts/x/bookmarks/2026-09-12-fchollet-i-would-have-assumed-it-was-fairly-obvious-but-in-case-it-s--2085323411903889876|Harness como arquitetura neurosimbólica]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-harness-engineering-is-a-top-skill-right-now-this-new-meta-p--2098426608793362916|Harness engineering e Auto-RecSys]]", "[[extracts/x/bookmarks/2026-09-14-hwchase17-in-case-you-want-to-build-a-domain-specific-harness-https-t--2098866608785473858|Harnesses customizados para agentes]]", "[[extracts/x/bookmarks/2026-09-14-mardehaym-the-model-is-the-smallest-most-swappable-part-key-principles--2099175716046643654|harness engineering principles]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-harness-engineering-is-a-top-skill-right-now-i-saw-a-great-o--2097449131648197024|coleção de papers sobre harness engineering]]", "[[extracts/x/bookmarks/2026-09-19-omarsar0-build-your-own-harness-folks-this-is-absolute-banger-paper-f--2101074795643494546|SoL-Pi: harness de agente auto-evolutivo]]", "[[extracts/x/bookmarks/2026-09-14-garrytan-either-you-die-a-system-of-record-or-you-live-long-enough-to--2098666551629267324|Systems of record virando harnesses]]", "[[extracts/x/bookmarks/2026-09-17-_avichawla-layers-of-observability-in-ai-systems-explained-visually-if--2100139401842250163|Camadas de observabilidade em sistemas de IA]]"]
---

# paper sobre model harnesses

**@rohanpaul_ai** · [2098986025397977287](https://x.com/rohanpaul_ai/status/2098986025397977287) · `resource`

## Resumo
Paper de Stanford + MIT argumenta que o desempenho de sistemas de IA depende do 'harness' — o código do sistema ao redor do modelo — tanto quanto do próprio LLM. Com o mesmo modelo subjacente, resultados diferentes emergem conforme storage, retrieval e fluxo são orquestrados.

## Pontos-chave
- O harness decide o que armazenar, recuperar e apresentar ao modelo como contexto
- A lógica de execução do workflow vive no harness, não no modelo
- Mesmo LLM subjacente produz desempenho diferente conforme o harness que o envolve
- Implicação prática: esforço de engenharia deve mirar design do harness, não apenas escolha de modelo

## Entidades
Stanford, MIT, Rohan Paul

> **Revisit:** `high` · **fonte:** `tweet`
