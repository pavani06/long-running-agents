---
title: "Memória para agentes longos"
type: "extract"
source: "x"
status_id: "2097555607389896732"
handle: "dair_ai"
url: "https://x.com/dair_ai/status/2097555607389896732"
created_at: "2026-09-09T05:20:02.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-dair_ai-good-work-on-improving-memory-for-long-horizon-agents-they-s--2097555607389896732.json]]"
tags: ["memory-architecture", "agents", "context-management", "token-budgeting", "context-engineering", "agent-loop"]
topic: "Memória para agentes longos"
summary: "Destaca trabalho que separa duas funções usualmente colapsadas em sistemas de memória de agentes: como memórias são mescladas na escrita e como o conteúdo recuperado é montado no prompt, sob orçamento de prompt restrito. Vale salvar por formalizar uma distinção arquitetural central para agentes de longo horizonte."
key_points: ["Separa o merge de memórias no momento da escrita da montagem do prompt no momento da recuperação — duas preocupações que papers de memória de agentes costumam tratar como uma só.", "O cenário avaliado opera sob orçamento de prompt restrito, tornando a gestão de contexto um constraint explícito do design.", "A distinção é diretamente aplicável ao desenho de sistemas de memória para agentes de longo horizonte (decidir o que consolidar vs. o que incluir no contexto)."]
entities: ["DAIR.AI"]
content_type: "announcement"
revisit: "high"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HRwDtUeawAA0h5X.png"]
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-zostaff-this-paper-completely-changed-how-i-think-about-agent-memory--2078944176457359536|Arquitetura de memória para agentes]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-this-is-a-brilliant-paper-it-s-of-the-cleanest-long-context--2098140712504332411|Sequential memory agents para long-context]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-google-if-you-maintain-a-skill-library-for--2093324233158045788|Evolução de skills em agentes]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-very-cool-paper-on-memory-compression-for-agents-if-you-run--2098531286319341932|compressão de memória para agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-great-paper-from-google-and-colleagues-it-proposes-an-intere--2094472291002589452|Degradação de agentes em tarefas long-horizon]]", "[[extracts/x/bookmarks/2026-09-12-aicamila_-context-window-management-and-optimization-for-agents-agents--2076155135366135903|Context window management para agentes]]", "[[extracts/x/bookmarks/2026-09-12-sprytixl-stanford-and-anthropic-spent-3-1m-to-prove-your-agent-perfor--2078969602189746340|memória de agentes via grafos]]", "[[extracts/x/bookmarks/2026-09-12-akitaonrails-acabei-de-soltar-a-versao-2-0-do-meu-ai-memory-e-eu-acho-que--2095186765535392249|ai-memory 2.0: memória compartilhada de agentes]]", "[[extracts/x/bookmarks/2026-09-12-roundtablespace-supermemory-is-1st-on-every-major-ai-memory-benchmark-95-rec--2097335398536212741|memória persistente para agentes de IA]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-if-you-give-me-a-drawer-i-will-eventually-fill-it-with-cable--2097238983226868194|Entropia de arquivos markdown por agentes]]", "[[extracts/x/bookmarks/2026-09-12-0xcodio-anthropic-engineer-built-an-agent-that-keeps-a-map-of-what-i--2095820416069849496|Mapa de lacunas de conhecimento em agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-an-anatomy-of-cli-coding-agent-trajectories-bookmark-it-when--2076699431207154069|análise de trajetórias de agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-radixattention-clearly-explained-how-sglang-makes-prefix-cac--2098750998353473776|RadixAttention e prefix caching no SGLang]]", "[[extracts/x/bookmarks/2026-09-12-quxiaoyin-if-you-left-your-coding-agent-alone-for-more-than-1h-don-t-h--2085408811104534754|expiração de cache de prompt em agentes de código]]", "[[extracts/x/bookmarks/2026-09-14-akshay_pachaar-13-attention-mechanisms-ai-engineers-must-know-bookmark-this--2099113391591923822|Mecanismos de atenção em LLMs]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-stateful-vs-stateless-mcp-core-anthropic-s-biggest-mcp-updat--2082454281630961687|Stateful vs. Stateless MCP]]", "[[extracts/x/bookmarks/2026-09-12-duquesadetax-to-vendo-muita-gente-feliz-com-o-adiamento-do-split-obrigato--2094413457407819979|Split payment na reforma tributária]]"]
theme: "Engenharia de Agentes e Loops"
---

# Memória para agentes longos

**@dair_ai** · [2097555607389896732](https://x.com/dair_ai/status/2097555607389896732) · `announcement`

## Resumo
Destaca trabalho que separa duas funções usualmente colapsadas em sistemas de memória de agentes: como memórias são mescladas na escrita e como o conteúdo recuperado é montado no prompt, sob orçamento de prompt restrito. Vale salvar por formalizar uma distinção arquitetural central para agentes de longo horizonte.

## Pontos-chave
- Separa o merge de memórias no momento da escrita da montagem do prompt no momento da recuperação — duas preocupações que papers de memória de agentes costumam tratar como uma só.
- O cenário avaliado opera sob orçamento de prompt restrito, tornando a gestão de contexto um constraint explícito do design.
- A distinção é diretamente aplicável ao desenho de sistemas de memória para agentes de longo horizonte (decidir o que consolidar vs. o que incluir no contexto).

## Entidades
DAIR.AI

> **Revisit:** `high` · **fonte:** `tweet`
