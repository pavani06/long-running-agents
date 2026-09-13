---
title: "ai-memory 2.0: memória compartilhada de agentes"
type: "extract"
source: "x"
status_id: "2095186765535392249"
handle: "AkitaOnRails"
url: "https://x.com/AkitaOnRails/status/2095186765535392249"
created_at: "2026-09-02T16:27:06.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-akitaonrails-acabei-de-soltar-a-versao-2-0-do-meu-ai-memory-e-eu-acho-que--2095186765535392249.json]]"
tags: ["memory-architecture", "multi-agent", "cross-session", "agent-tooling", "harness", "knowledge-management", "context-management", "evals", "state", "production"]
topic: "ai-memory 2.0: memória compartilhada de agentes"
summary: "Fabio Akita lança a ai-memory 2.0, servidor de memória de longo prazo para agentes de código, agora com formato aberto OKF nativo, embeddings locais ligados por padrão e suporte real a múltiplos harnesses e a um time inteiro no mesmo projeto. Vale salvar como referência densa de arquitetura de memória multi-agente, com benchmark reproduzível e comparação detalhada com concorrentes."
key_points: ["Formato aberto OKF nativo: a wiki já é um bundle válido (Markdown + metadados padronizados do Open Knowledge Format do Google), sem passo de exportação divergente — legível com grep, Obsidian ou Git, e empacotável com 'ai-memory export-okf'; tese central: modelo e harness são alugados, a memória do projeto é sua.", "Embeddings locais ligados por padrão: provider em Rust puro (candle, all-MiniLM-L6-v2, ~87MB com checksum fixo, sem API/GPU/dados externos) eleva hit@5 no LongMemEval-S de 0.617 (full-text) para 0.779; desativável com embedding_provider = \"none\".", "Concorrência multi-harness no mesmo projeto: ponteiro de 'projeto atual' por ator, identidade do projeto pelo nome do checkout (portátil entre máquinas), regravação cria nova versão na cadeia em vez de sobrescrever, e todas as escritas passam por um único writer com fila e backpressure — desenho que evita a corrupção de escrita concorrente que derrubou concorrentes; testes de aceitação com Claude, Codex, OpenCode, Pi, Crush e outros na mesma workstream.", "Modo time: servidor central (SQLite, HTTPS via proxy reverso), atribuição por pessoa com log de auditoria, handoff como bastão de dono único (um accept não rouba o bastão) e slots pessoais que não vazam no briefing do time; sem permissão por página por design — o histórico registra autoria.", "Outros pontos: SemVer de verdade a partir da 2.0 com migração que aborta o boot se o backup verificado falhar; links tipados (causes, fixes, contradicts) alimentando checagem de contradição sem LLM; consulta as_of por data; passada opcional de 'experiência' entre sessões; análise competitiva (agentmemory, basic-memory, cognee, MemPalace com benchmark inflado, Zep, Letta/MemGPT, Mem0) e números do projeto (1500+ commits, 371 PRs, ~70 contribuidores)."]
entities: ["Fabio Akita", "ai-memory", "OKF (Open Knowledge Format)", "Google", "all-MiniLM-L6-v2", "candle", "LongMemEval-S", "SQLite", "Obsidian", "Git", "Claude Code", "Codex", "OpenCode", "Pi", "Crush", "Ollama", "agentmemory", "basic-memory", "cognee", "MemPalace", "Zep", "Letta", "MemGPT", "Mem0", "Djalma Júnior", "Samir Hanna Verza"]
content_type: "announcement"
revisit: "high"
grounded_in: "article"
links: ["https://akitaonrails.com/2026/09/02/ai-memory-2-0-melhor-sistema-memoria-agentes-e-times/"]
media: ["https://pbs.twimg.com/media/HROZPMnW4AIgtv2.jpg"]
---

# ai-memory 2.0: memória compartilhada de agentes

**@AkitaOnRails** · [2095186765535392249](https://x.com/AkitaOnRails/status/2095186765535392249) · `announcement`

## Resumo
Fabio Akita lança a ai-memory 2.0, servidor de memória de longo prazo para agentes de código, agora com formato aberto OKF nativo, embeddings locais ligados por padrão e suporte real a múltiplos harnesses e a um time inteiro no mesmo projeto. Vale salvar como referência densa de arquitetura de memória multi-agente, com benchmark reproduzível e comparação detalhada com concorrentes.

## Pontos-chave
- Formato aberto OKF nativo: a wiki já é um bundle válido (Markdown + metadados padronizados do Open Knowledge Format do Google), sem passo de exportação divergente — legível com grep, Obsidian ou Git, e empacotável com 'ai-memory export-okf'; tese central: modelo e harness são alugados, a memória do projeto é sua.
- Embeddings locais ligados por padrão: provider em Rust puro (candle, all-MiniLM-L6-v2, ~87MB com checksum fixo, sem API/GPU/dados externos) eleva hit@5 no LongMemEval-S de 0.617 (full-text) para 0.779; desativável com embedding_provider = "none".
- Concorrência multi-harness no mesmo projeto: ponteiro de 'projeto atual' por ator, identidade do projeto pelo nome do checkout (portátil entre máquinas), regravação cria nova versão na cadeia em vez de sobrescrever, e todas as escritas passam por um único writer com fila e backpressure — desenho que evita a corrupção de escrita concorrente que derrubou concorrentes; testes de aceitação com Claude, Codex, OpenCode, Pi, Crush e outros na mesma workstream.
- Modo time: servidor central (SQLite, HTTPS via proxy reverso), atribuição por pessoa com log de auditoria, handoff como bastão de dono único (um accept não rouba o bastão) e slots pessoais que não vazam no briefing do time; sem permissão por página por design — o histórico registra autoria.
- Outros pontos: SemVer de verdade a partir da 2.0 com migração que aborta o boot se o backup verificado falhar; links tipados (causes, fixes, contradicts) alimentando checagem de contradição sem LLM; consulta as_of por data; passada opcional de 'experiência' entre sessões; análise competitiva (agentmemory, basic-memory, cognee, MemPalace com benchmark inflado, Zep, Letta/MemGPT, Mem0) e números do projeto (1500+ commits, 371 PRs, ~70 contribuidores).

## Links
- https://akitaonrails.com/2026/09/02/ai-memory-2-0-melhor-sistema-memoria-agentes-e-times/

## Entidades
Fabio Akita, ai-memory, OKF (Open Knowledge Format), Google, all-MiniLM-L6-v2, candle, LongMemEval-S, SQLite, Obsidian, Git, Claude Code, Codex, OpenCode, Pi, Crush, Ollama, agentmemory, basic-memory, cognee, MemPalace, Zep, Letta, MemGPT, Mem0, Djalma Júnior, Samir Hanna Verza

> **Revisit:** `high` · **fonte:** `article`
