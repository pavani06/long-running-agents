---
title: "I stopped using /grill-me for coding. Here’s what I use instead:"
type: "extract"
source: "youtube"
video_id: "6BB6exR8Zd8"
url: "https://www.youtube.com/watch?v=6BB6exR8Zd8"
channel: "Matt Pocock"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-i-stopped-using-grill-me-for-coding-heres-what-i-use-instead--6BB6exR8Zd8.txt]]"
tags: ["context-engineering", "ontologia", "knowledge-management", "documentation-publishing", "spec-driven-development", "agentic-coding", "agent-tooling", "harness-engineering", "decision-discipline", "cross-session", "memory-architecture", "token-budgeting", "arquitetura"]
thesis: "Sustentar um glossário de linguagem ubíqua persistente (context.md) e ADRs, combinado com uma skill que faz o LLM interrogar o usuário até o entendimento compartilhado (grill with docs), produz alinhamento quase 'mágico' entre humano e IA — as técnicas de Domain-Driven Design que funcionam com humanos também funcionam com agentes."
concepts: ["Grill Me / Grill with Docs: skill que faz o LLM entrevistar relentless até entendimento compartilhado, percorrendo a árvore de decisão", "Linguagem ubíqua (Domain-Driven Design, livro 'big blue' de Eric Evans): linguagem compartilhada entre codebase, devs e especialistas de domínio", "Bounded context e context map para escalar glossários em monorepos enormes", "context.md como glossário vivo na raiz do repositório, referenciado por ponteiro no CLAUDE.md local", "Architectural Decision Records (ADRs) para decisões não-óbvias difíceis de reverter", "Colisões terminológicas e desafio de linguagem difusa durante sessões de spec", "Cardinalidade de entidades (1:N pitch↔standalone video) e cascata de deleção (onDelete restrict) derivadas da linguagem", "Economia de tokens via vocabulário compartilhado (respostas e traces de raciocínio mais concisos)", "Nomes de variáveis e arquivos gerados derivam do glossário — precisão linguística vira qualidade de código", "Pitch como 'embalagem antes do conteúdo' (axioma estilo Mr. Beast) como nova entidade de domínio", "Evitar bike-shedding: ship com linguagem 'boa o suficiente' e refatorar a linguagem depois"]
tools: ["Grill Me (skill)", "Grill with Docs (skill)", "Ubiquitous Language (skill)", "context.md", "CLAUDE.md (local, com ponteiro para o glossário)", "ADRs (arquivos markdown no repositório)", "Claude", "WhisperFlow (ditado)", "newsletter 'AI Skills for Real Engineers'", "skills repo (GitHub)"]
people: ["Eric Evans", "Mr. Beast", "Anthropic (Claude)"]
claims: ["Use Grill with Docs quando houver codebase; use Grill Me quando não houver (ex.: escrever um eulogio, planejamento geral)", "Crie um context.md na raiz do repositório documentando a linguagem compartilhada e referencie-o via ponteiro no CLAUDE.md local", "Durante a sessão de grilling, o agente deve desafiar a linguagem contra o glossário existente, afiar termos difusos, discutir cenários concretos, referenciar o código e atualizar o glossário em tempo real", "Crie ADRs apenas para decisões difíceis de reverter, surpreendentes sem contexto e resultado de trade-offs reais — decisões intercambiáveis não merecem ADR", "Escale para monorepos enormes com um context map e múltiplos bounded contexts, cada um com seu próprio context.md", "Resolva primeiro a linguagem (terminologia, cardinalidade, status) e só depois os detalhes de implementação — a resposta a uma questão de vocabulário molda UI, cascata de deleção e todo o código gerado", "Peça ao agente para salvar o estado da conversa no context.md e grillar você sobre pontos pendentes antes de gravar as mudanças", "Vocabulário compartilhado documentado reduz o número de tokens nas respostas e nos traces de raciocínio do modelo, e o alinhamento se acumula entre sessões", "Não bike-shed indefinidamente: defina a linguagem como 'boa o suficiente', ship e refatore a linguagem depois"]
deep_dive: "high"
deep_dive_reason: "Apresenta um padrão arquitetural concreto e replicável (glossário ubíquo persistente + ADRs + skill de interrogatório) que integra DDD clássico a context-engineering e harness de agentes com impacto medível em tokens, alinhamento cross-session e navegação do código."
---

# I stopped using /grill-me for coding. Here’s what I use instead:

## Tese
Sustentar um glossário de linguagem ubíqua persistente (context.md) e ADRs, combinado com uma skill que faz o LLM interrogar o usuário até o entendimento compartilhado (grill with docs), produz alinhamento quase 'mágico' entre humano e IA — as técnicas de Domain-Driven Design que funcionam com humanos também funcionam com agentes.

## Conceitos-chave
- Grill Me / Grill with Docs: skill que faz o LLM entrevistar relentless até entendimento compartilhado, percorrendo a árvore de decisão
- Linguagem ubíqua (Domain-Driven Design, livro 'big blue' de Eric Evans): linguagem compartilhada entre codebase, devs e especialistas de domínio
- Bounded context e context map para escalar glossários em monorepos enormes
- context.md como glossário vivo na raiz do repositório, referenciado por ponteiro no CLAUDE.md local
- Architectural Decision Records (ADRs) para decisões não-óbvias difíceis de reverter
- Colisões terminológicas e desafio de linguagem difusa durante sessões de spec
- Cardinalidade de entidades (1:N pitch↔standalone video) e cascata de deleção (onDelete restrict) derivadas da linguagem
- Economia de tokens via vocabulário compartilhado (respostas e traces de raciocínio mais concisos)
- Nomes de variáveis e arquivos gerados derivam do glossário — precisão linguística vira qualidade de código
- Pitch como 'embalagem antes do conteúdo' (axioma estilo Mr. Beast) como nova entidade de domínio
- Evitar bike-shedding: ship com linguagem 'boa o suficiente' e refatorar a linguagem depois

## Ferramentas & pessoas
**Ferramentas:** Grill Me (skill), Grill with Docs (skill), Ubiquitous Language (skill), context.md, CLAUDE.md (local, com ponteiro para o glossário), ADRs (arquivos markdown no repositório), Claude, WhisperFlow (ditado), newsletter 'AI Skills for Real Engineers', skills repo (GitHub)

**Pessoas/orgs:** Eric Evans, Mr. Beast, Anthropic (Claude)

## Claims acionáveis
- Use Grill with Docs quando houver codebase; use Grill Me quando não houver (ex.: escrever um eulogio, planejamento geral)
- Crie um context.md na raiz do repositório documentando a linguagem compartilhada e referencie-o via ponteiro no CLAUDE.md local
- Durante a sessão de grilling, o agente deve desafiar a linguagem contra o glossário existente, afiar termos difusos, discutir cenários concretos, referenciar o código e atualizar o glossário em tempo real
- Crie ADRs apenas para decisões difíceis de reverter, surpreendentes sem contexto e resultado de trade-offs reais — decisões intercambiáveis não merecem ADR
- Escale para monorepos enormes com um context map e múltiplos bounded contexts, cada um com seu próprio context.md
- Resolva primeiro a linguagem (terminologia, cardinalidade, status) e só depois os detalhes de implementação — a resposta a uma questão de vocabulário molda UI, cascata de deleção e todo o código gerado
- Peça ao agente para salvar o estado da conversa no context.md e grillar você sobre pontos pendentes antes de gravar as mudanças
- Vocabulário compartilhado documentado reduz o número de tokens nas respostas e nos traces de raciocínio do modelo, e o alinhamento se acumula entre sessões
- Não bike-shed indefinidamente: defina a linguagem como 'boa o suficiente', ship e refatore a linguagem depois

> **Deep dive:** `high` — Apresenta um padrão arquitetural concreto e replicável (glossário ubíquo persistente + ADRs + skill de interrogatório) que integra DDD clássico a context-engineering e harness de agentes com impacto medível em tokens, alinhamento cross-session e navegação do código.
