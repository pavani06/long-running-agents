---
title: "Arquitetura de memória para agentes"
type: "extract"
source: "x"
status_id: "2078944176457359536"
handle: "zostaff"
url: "https://x.com/zostaff/status/2078944176457359536"
created_at: "2026-07-19T20:44:51.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-zostaff-this-paper-completely-changed-how-i-think-about-agent-memory--2078944176457359536.json]]"
tags: ["memory-architecture", "agents", "context-management"]
topic: "Arquitetura de memória para agentes"
summary: "Recomendação de um paper que propõe um pipeline estruturado de 5 estágios para acesso à memória de agentes (Rewrite → Tag → Traverse → Prune → Reconstruct), em vez de armazenamento/recuperação brutos. Vale salvar como blueprint reutilizável para projetar sistemas de memória persistente em agentes."
key_points: ["Pipeline de memória em 5 passos: Rewrite → Tag → Traverse → Prune → Reconstruct, cada estágio com função definida na transformação do diálogo em memória consultável", "Rewrite normaliza cada turno de diálogo numa sentença autocontida: pronomes resolvidos para entidades e tempos relativos convertidos em absolutos, eliminando dependência de contexto externo", "Abordagem muda o paradigma de acesso à memória: pré-processamento estruturado do que é armazenado, e não apenas recuperação por similaridade"]
entities: ["zostaff"]
content_type: "resource"
revisit: "high"
grounded_in: "tweet"
links: []
media: ["https://pbs.twimg.com/media/HNnAEWpWoAAVfzm.jpg"]
thin: false
relates-to: ["[[extracts/x/bookmarks/2026-09-12-dair_ai-good-work-on-improving-memory-for-long-horizon-agents-they-s--2097555607389896732|Memória para agentes longos]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-this-is-a-brilliant-paper-it-s-of-the-cleanest-long-context--2098140712504332411|Sequential memory agents para long-context]]", "[[extracts/x/bookmarks/2026-09-12-dair_ai-banger-paper-from-google-if-you-maintain-a-skill-library-for--2093324233158045788|Evolução de skills em agentes]]", "[[extracts/x/bookmarks/2026-09-12-witcheer-a-hermes-agent-community-member-built-a-layer-that-sits-on-t--2098020649662816503|Roteamento e memória no Hermes Agent]]", "[[extracts/x/bookmarks/2026-09-12-0xcodio-anthropic-engineer-built-an-agent-that-keeps-a-map-of-what-i--2095820416069849496|Mapa de lacunas de conhecimento em agentes]]", "[[extracts/x/bookmarks/2026-09-12-roundtablespace-supermemory-is-1st-on-every-major-ai-memory-benchmark-95-rec--2097335398536212741|memória persistente para agentes de IA]]", "[[extracts/x/bookmarks/2026-09-16-hwchase17-memory-has-been-a-hot-topic-for-the-past-2-years-every-time--2099858455079026817|memória em agentes de IA]]", "[[extracts/x/bookmarks/2026-09-12-omarsar0-very-cool-paper-on-memory-compression-for-agents-if-you-run--2098531286319341932|compressão de memória para agentes]]", "[[extracts/x/bookmarks/2026-09-12-aicamila_-context-window-management-and-optimization-for-agents-agents--2076155135366135903|Context window management para agentes]]", "[[extracts/x/bookmarks/2026-09-12-polydao-claude-obsidian-loop-engineering-a-vault-that-runs-itself-th--2098288931620184216|Claude + Obsidian vault como estado do agente]]", "[[extracts/x/bookmarks/2026-09-12-akshay_pachaar-radixattention-clearly-explained-how-sglang-makes-prefix-cac--2098750998353473776|RadixAttention e prefix caching no SGLang]]"]
theme: "Engenharia de agentes"
---

# Arquitetura de memória para agentes

**@zostaff** · [2078944176457359536](https://x.com/zostaff/status/2078944176457359536) · `resource`

## Resumo
Recomendação de um paper que propõe um pipeline estruturado de 5 estágios para acesso à memória de agentes (Rewrite → Tag → Traverse → Prune → Reconstruct), em vez de armazenamento/recuperação brutos. Vale salvar como blueprint reutilizável para projetar sistemas de memória persistente em agentes.

## Pontos-chave
- Pipeline de memória em 5 passos: Rewrite → Tag → Traverse → Prune → Reconstruct, cada estágio com função definida na transformação do diálogo em memória consultável
- Rewrite normaliza cada turno de diálogo numa sentença autocontida: pronomes resolvidos para entidades e tempos relativos convertidos em absolutos, eliminando dependência de contexto externo
- Abordagem muda o paradigma de acesso à memória: pré-processamento estruturado do que é armazenado, e não apenas recuperação por similaridade

## Entidades
zostaff

> **Revisit:** `high` · **fonte:** `tweet`
