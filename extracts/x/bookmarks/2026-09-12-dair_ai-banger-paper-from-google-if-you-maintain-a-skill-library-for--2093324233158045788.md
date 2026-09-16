---
title: "Evolução de skills em agentes"
type: "extract"
source: "x"
status_id: "2093324233158045788"
handle: "dair_ai"
url: "https://x.com/dair_ai/status/2093324233158045788"
created_at: "2026-08-28T13:06:03.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-dair_ai-banger-paper-from-google-if-you-maintain-a-skill-library-for--2093324233158045788.json]]"
tags: ["agents", "memory-architecture", "knowledge-management", "cross-session", "context-management"]
topic: "Evolução de skills em agentes"
summary: "Paper do Google sobre arquitetura de skill-evolution para agentes: em vez de colapsar tudo num único mecanismo, separa traces brutos de execução de uma wiki persistente de conhecimento acumulado (e de uma terceira camada truncada no tweet). Vale salvar como referência para quem mantém bibliotecas de skills/memória de agentes entre sessões."
key_points: ["Sistemas de skill-evolution costumam misturar três preocupações distintas em um só artefato; o paper argumenta por arquitetura em camadas separadas.", "Camadas citadas no tweet: traces brutos de execução e wiki persistente de conhecimento acumulado — a terceira camada está truncada e requer ler o paper linkado.", "Aplicável a manutenção de skill libraries para agentes (estilo Voyager), com implicações diretas para memória e reuso de conhecimento cross-session."]
entities: ["Google", "DAIR.AI"]
content_type: "resource"
revisit: "high"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HQz7S7XaMAEpfUG.jpg"]
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-15-timothykassis-scientific-agent-skills-a-library-of-procedural-knowledge-fo--2098833771407843787|Biblioteca de habilidades procedurais para agentes científicos]]", "[[extracts/x/bookmarks/2026-09-12-zostaff-this-paper-completely-changed-how-i-think-about-agent-memory--2078944176457359536|Arquitetura de memória para agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-baai-if-you-are-building-research-agents-t--2095539831141220620|Skills para research agents]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-great-paper-from-google-and-colleagues-it-proposes-an-intere--2094472291002589452|Degradação de agentes em tarefas long-horizon]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-another-interesting-approach-to-self-evolve-agent-skills-but--2098154641854992676|falhas em auto-evolução de skills de agentes]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-good-work-on-improving-memory-for-long-horizon-agents-they-s--2097555607389896732|Memória para agentes longos]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-this-is-a-brilliant-paper-it-s-of-the-cleanest-long-context--2098140712504332411|Sequential memory agents para long-context]]", "[[extracts/x/bookmarks/2026-09-12-xudong07452910-openai-skills-agents-md-blog-agent-engineering-astra-skill--2098655277197201752|OpenAI ensina Skills e AGENTS.md]]", "[[extracts/x/bookmarks/2026-09-15-snwiki238337-openai-skillskill-githubskill-agent-skills-eval-skillopenai--2099052462653002157|Metodologia de avaliação de skills (OpenAI)]]", "[[extracts/x/bookmarks/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-layer-that-sits-on-t--2098020649662816503|Roteamento e memória no Hermes Agent]]", "[[extracts/x/bookmarks/2026-09-12-0xcodio-anthropic-engineer-built-an-agent-that-keeps-a-map-of-what-i--2095820416069849496|Mapa de lacunas de conhecimento em agentes]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-very-cool-paper-on-memory-compression-for-agents-if-you-run--2098531286319341932|compressão de memória para agentes]]", "[[extracts/x/bookmarks/2026-09-12-tencentai_news-the-open-source-weknora-mit-22k-stars-just-shipped-v0-8-0-a--2098049042773397683|WeKnora v0.8.0: agentic RAG]]", "[[extracts/x/bookmarks/2026-09-15-dani_avila7-ok-this-is-big-mcp-now-defines-an-extension-specifically-for--2099325795822956575|Extensão MCP para Agent Skills]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-i-ve-been-trying-to-use-ai-for-knowledge-work-course-plannin--2097638166232457451|IA para trabalho de conhecimento]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-radixattention-clearly-explained-how-sglang-makes-prefix-cac--2098750998353473776|RadixAttention e prefix caching no SGLang]]"]
theme: "Engenharia de agentes"
---

# Evolução de skills em agentes

**@dair_ai** · [2093324233158045788](https://x.com/dair_ai/status/2093324233158045788) · `resource`

## Resumo
Paper do Google sobre arquitetura de skill-evolution para agentes: em vez de colapsar tudo num único mecanismo, separa traces brutos de execução de uma wiki persistente de conhecimento acumulado (e de uma terceira camada truncada no tweet). Vale salvar como referência para quem mantém bibliotecas de skills/memória de agentes entre sessões.

## Pontos-chave
- Sistemas de skill-evolution costumam misturar três preocupações distintas em um só artefato; o paper argumenta por arquitetura em camadas separadas.
- Camadas citadas no tweet: traces brutos de execução e wiki persistente de conhecimento acumulado — a terceira camada está truncada e requer ler o paper linkado.
- Aplicável a manutenção de skill libraries para agentes (estilo Voyager), com implicações diretas para memória e reuso de conhecimento cross-session.

## Entidades
Google, DAIR.AI

> **Revisit:** `high` · **fonte:** `tweet`
