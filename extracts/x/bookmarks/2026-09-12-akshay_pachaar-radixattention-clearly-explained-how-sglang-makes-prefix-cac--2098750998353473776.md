---
title: "RadixAttention e prefix caching no SGLang"
type: "extract"
source: "x"
status_id: "2098750998353473776"
handle: "akshay_pachaar"
url: "https://x.com/akshay_pachaar/status/2098750998353473776"
created_at: "2026-09-12T12:30:05.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-akshay_pachaar-radixattention-clearly-explained-how-sglang-makes-prefix-cac--2098750998353473776.json]]"
tags: ["performance", "arquitetura", "runtime", "agents"]
topic: "RadixAttention e prefix caching no SGLang"
summary: "Explicação de como o RadixAttention do SGLang torna o prefix caching eficiente quando requisições derivam (branching) de contextos compartilhados, como conversas de assistentes de código. Vale salvar porque o compartilhamento de prefixos longos (system prompt + repositório) é determinante para latência e throughput em serving de LLMs e cargas agênticas."
key_points: ["Prefix caching parece simples até que requisições começam a derivar de um mesmo contexto, exigindo uma estrutura que compartilhe KV cache entre ramificações.", "RadixAttention organiza o KV cache em uma árvore radix, permitindo reuso de prefixos comuns entre múltiplas requisições.", "O exemplo central usa um assistente de código cujas conversas compartilham system prompt e contexto de repositório Python — cenário típico também para agentes com prompts longos repetidos.", "SGLang aproveita essa redundância com caching e agendamento conscientes de prefixo, evitando recomputação de atenção sobre contexto já processado."]
entities: ["RadixAttention", "SGLang", "Akshay Pachaar"]
content_type: "thread"
revisit: "high"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/tweet_video_thumb/HSBC53PawAEXZLa.jpg"]
relates-to: ["[[extracts/x/bookmarks/2026-09-12-dair_ai-good-work-on-improving-memory-for-long-horizon-agents-they-s--2097555607389896732|Memória para agentes longos]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-this-is-a-brilliant-paper-it-s-of-the-cleanest-long-context--2098140712504332411|Sequential memory agents para long-context]]", "[[extracts/x/bookmarks/2026-09-12-zostaff-this-paper-completely-changed-how-i-think-about-agent-memory--2078944176457359536|Arquitetura de memória para agentes]]", "[[extracts/x/bookmarks/2026-09-12-akitaonrails-acabei-de-soltar-a-versao-2-0-do-meu-ai-memory-e-eu-acho-que--2095186765535392249|ai-memory 2.0: memória compartilhada de agentes]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-very-cool-paper-on-memory-compression-for-agents-if-you-run--2098531286319341932|compressão de memória para agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-google-if-you-maintain-a-skill-library-for--2093324233158045788|Evolução de skills em agentes]]", "[[extracts/x/bookmarks/2026-09-12-_avichawla-why-kv-cache-stores-k-and-v-vectors-but-never-q-a-popular-te--2093962020962083139|KV cache sem Q em LLMs]]", "[[extracts/x/bookmarks/2026-09-12-marwan_3atef-cloudflare-ai-gateway-custom-costs-finally-understand-prompt--2098027728624570486|Cloudflare AI Gateway custo com prompt caching]]", "[[extracts/x/bookmarks/2026-09-12-aravsrinivas-we-re-open-sourcing-lily-perplexity-s-local-inference-engine--2095264908762140823|Perplexity Lily inferência local]]"]
thin: false
---

# RadixAttention e prefix caching no SGLang

**@akshay_pachaar** · [2098750998353473776](https://x.com/akshay_pachaar/status/2098750998353473776) · `thread`

## Resumo
Explicação de como o RadixAttention do SGLang torna o prefix caching eficiente quando requisições derivam (branching) de contextos compartilhados, como conversas de assistentes de código. Vale salvar porque o compartilhamento de prefixos longos (system prompt + repositório) é determinante para latência e throughput em serving de LLMs e cargas agênticas.

## Pontos-chave
- Prefix caching parece simples até que requisições começam a derivar de um mesmo contexto, exigindo uma estrutura que compartilhe KV cache entre ramificações.
- RadixAttention organiza o KV cache em uma árvore radix, permitindo reuso de prefixos comuns entre múltiplas requisições.
- O exemplo central usa um assistente de código cujas conversas compartilham system prompt e contexto de repositório Python — cenário típico também para agentes com prompts longos repetidos.
- SGLang aproveita essa redundância com caching e agendamento conscientes de prefixo, evitando recomputação de atenção sobre contexto já processado.

## Entidades
RadixAttention, SGLang, Akshay Pachaar

> **Revisit:** `high` · **fonte:** `tweet`
