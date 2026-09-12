---
title: "PI Architecture EXPLAINED | Agent Loop, Tools, TUI and More"
type: "extract"
source: "youtube"
video_id: "gTeujlv8qK0"
url: "https://www.youtube.com/watch?v=gTeujlv8qK0"
channel: "Alejandro AO"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-pi-architecture-explained-agent-loop-tools-tui-and-more--gTeujlv8qK0.txt]]"
tags: ["harness", "harness-engineering", "context-engineering", "context-management", "memory-architecture", "agent-loop", "agents", "agent-tooling", "arquitetura", "analise-estrutural", "token-budgeting", "state", "runtime", "permissions", "knowledge-management", "stack-tooling"]
thesis: "O agente Pi demonstra que um coding agent minimalista pode ser construído do zero com um loop agentic customizado, sessões em JSONL estruturadas como árvore (permitindo forks), compaction baseada nas métricas de uso do LLM e um sistema de skills/extensões que separa o núcleo do agente da camada interativa."
concepts: ["agentic loop customizado (sem bibliotecas de loop)", "inicialização de contexto (system prompt + agents.md + descrições de skills e tools + histórico)", "transformação/compaction de contexto como passo do loop", "sessões em JSONL com append-only", "estrutura de árvore de mensagens via IDs parent/child", "fork de conversas (/tree)", "modo read-only com subconjunto de tools (--tools read,grep,find)", "extensões TypeScript com subscrição a eventos do agent loop", "montagem do system prompt (~20 linhas + seções appended)", "skills como arquivos markdown com lazy loading via tool read", "custom prompts (slash commands) resolvidos na camada interativa", "ponto de entrada CLI (client.ts → main.ts) e modos interactive/RPC/stdio", "TUI custom component-based (sem textual)", "contagem de tokens derivada de usage (input+output+cache read+cache write)", "compaction prompt com checkpoint estruturado (goal, constraints, progress, decisions, next steps, critical context)"]
tools: ["Pi", "read tool", "bash tool", "edit tool", "write tool", "grep", "find", "OpenAI Agents SDK", "Vercel AI SDK", "GPT-5", "Anthropic (modelos)", "Kimi", "MiniMax", "MCP", "VS Code", "TypeScript", "Codex", "Claude Code"]
people: ["Alejandro (apresentador)", "OpenAI", "Anthropic", "Vercel"]
claims: ["O agent loop do Pi é codado do zero, sem bibliotecas prontas como OpenAI Agents SDK ou Vercel AI SDK, e é acessível via RPC ou SDK programático", "As sessões são armazenadas em JSONL sob o diretório home, em pastas mapeadas por working directory, com cada mensagem como um objeto JSON de uma linha (append-only)", "Cada mensagem carrega id e parent id, formando uma árvore que permite bifurcar/forkar conversas e navegar com /tree", "O Pi vem com apenas 4 tools (read, bash, edit, write); grep e find existem mas ficam desabilitados por padrão, ativados para modo read-only via flag --tools", "A checagem de compaction (check_compaction) roda em dois momentos: ao fim de cada turno do agente e antes de cada prompt do usuário", "O Pi não estima tokens dividindo caracteres por 4: usa tokens de contexto retornados pelo provider ou soma usage.input + usage.output + cache.read + cache.write", "O prompt de compaction gera um checkpoint estruturado (goal, constraints, progress, key decisions, next steps, critical context) preservando paths, nomes de funções e mensagens de erro exatas", "Skills não têm conteúdo colado no contexto: a camada interativa injeta nome, descrição e localização, e o agente lê o arquivo com a tool read (lazy loading)", "Custom slash commands são substituídos pelo prompt real na camada interativa e nunca chegam ao core, tornando o core agnóstico de UI", "Extensões em TypeScript podem registrar tools/comandos, atalhos de teclado, flags de CLI, alterar o system prompt e assinar eventos do loop (tool call, agent response, user message)", "O system prompt padrão tem ~20 linhas e concatena agents.md (home e cwd), descrições de skills e tools, data e working directory; é sobreponível via system.md ou --system-prompt", "Pacotes/extensões de terceiros executam código no sistema: revise com o próprio agente antes de instalar", "A TUI é totalmente custom, component-based (cada componente renderiza a si mesmo e assina eventos do core), permitindo substituí-la por outra UI sobre RPC"]
deep_dive: "high"
deep_dive_reason: "Densidade alta de detalhe arquitetural acionável e relevante a harness, context-engineering e memory-architecture (árvore de sessões em JSONL, design de compaction, lazy loading de skills, sistema de eventos), com novidade real sobre como o Pi é construído."
---

# PI Architecture EXPLAINED | Agent Loop, Tools, TUI and More

## Tese
O agente Pi demonstra que um coding agent minimalista pode ser construído do zero com um loop agentic customizado, sessões em JSONL estruturadas como árvore (permitindo forks), compaction baseada nas métricas de uso do LLM e um sistema de skills/extensões que separa o núcleo do agente da camada interativa.

## Conceitos-chave
- agentic loop customizado (sem bibliotecas de loop)
- inicialização de contexto (system prompt + agents.md + descrições de skills e tools + histórico)
- transformação/compaction de contexto como passo do loop
- sessões em JSONL com append-only
- estrutura de árvore de mensagens via IDs parent/child
- fork de conversas (/tree)
- modo read-only com subconjunto de tools (--tools read,grep,find)
- extensões TypeScript com subscrição a eventos do agent loop
- montagem do system prompt (~20 linhas + seções appended)
- skills como arquivos markdown com lazy loading via tool read
- custom prompts (slash commands) resolvidos na camada interativa
- ponto de entrada CLI (client.ts → main.ts) e modos interactive/RPC/stdio
- TUI custom component-based (sem textual)
- contagem de tokens derivada de usage (input+output+cache read+cache write)
- compaction prompt com checkpoint estruturado (goal, constraints, progress, decisions, next steps, critical context)

## Ferramentas & pessoas
**Ferramentas:** Pi, read tool, bash tool, edit tool, write tool, grep, find, OpenAI Agents SDK, Vercel AI SDK, GPT-5, Anthropic (modelos), Kimi, MiniMax, MCP, VS Code, TypeScript, Codex, Claude Code

**Pessoas/orgs:** Alejandro (apresentador), OpenAI, Anthropic, Vercel

## Claims acionáveis
- O agent loop do Pi é codado do zero, sem bibliotecas prontas como OpenAI Agents SDK ou Vercel AI SDK, e é acessível via RPC ou SDK programático
- As sessões são armazenadas em JSONL sob o diretório home, em pastas mapeadas por working directory, com cada mensagem como um objeto JSON de uma linha (append-only)
- Cada mensagem carrega id e parent id, formando uma árvore que permite bifurcar/forkar conversas e navegar com /tree
- O Pi vem com apenas 4 tools (read, bash, edit, write); grep e find existem mas ficam desabilitados por padrão, ativados para modo read-only via flag --tools
- A checagem de compaction (check_compaction) roda em dois momentos: ao fim de cada turno do agente e antes de cada prompt do usuário
- O Pi não estima tokens dividindo caracteres por 4: usa tokens de contexto retornados pelo provider ou soma usage.input + usage.output + cache.read + cache.write
- O prompt de compaction gera um checkpoint estruturado (goal, constraints, progress, key decisions, next steps, critical context) preservando paths, nomes de funções e mensagens de erro exatas
- Skills não têm conteúdo colado no contexto: a camada interativa injeta nome, descrição e localização, e o agente lê o arquivo com a tool read (lazy loading)
- Custom slash commands são substituídos pelo prompt real na camada interativa e nunca chegam ao core, tornando o core agnóstico de UI
- Extensões em TypeScript podem registrar tools/comandos, atalhos de teclado, flags de CLI, alterar o system prompt e assinar eventos do loop (tool call, agent response, user message)
- O system prompt padrão tem ~20 linhas e concatena agents.md (home e cwd), descrições de skills e tools, data e working directory; é sobreponível via system.md ou --system-prompt
- Pacotes/extensões de terceiros executam código no sistema: revise com o próprio agente antes de instalar
- A TUI é totalmente custom, component-based (cada componente renderiza a si mesmo e assina eventos do core), permitindo substituí-la por outra UI sobre RPC

> **Deep dive:** `high` — Densidade alta de detalhe arquitetural acionável e relevante a harness, context-engineering e memory-architecture (árvore de sessões em JSONL, design de compaction, lazy loading de skills, sistema de eventos), com novidade real sobre como o Pi é construído.
