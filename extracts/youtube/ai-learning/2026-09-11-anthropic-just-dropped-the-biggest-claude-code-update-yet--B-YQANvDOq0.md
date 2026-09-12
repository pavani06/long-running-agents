---
title: "Anthropic Just Dropped the Biggest Claude Code Update Yet"
type: "extract"
source: "youtube"
video_id: "B-YQANvDOq0"
url: "https://www.youtube.com/watch?v=B-YQANvDOq0"
channel: "Ray Amjad"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-anthropic-just-dropped-the-biggest-claude-code-update-yet--B-YQANvDOq0.txt]]"
tags: ["agentic-coding", "agent-loop", "agent-tooling", "context-engineering", "context-management", "cross-session", "gate-design", "governanca", "harness-engineering", "knowledge-management", "memory-architecture", "observability", "permissions", "production", "state", "verification"]
thesis: "Os 'function hooks' recém-lançados no Claude Code transformam o agente em uma plataforma programável estilo middleware do Express.js, permitindo interceptar e reescrever chamadas de ferramentas, contexto, memória, UI e gates humanos para obter controle determinístico que regras de prompt no CLAUDE.md não garantem."
concepts: ["hooks como controle determinístico vs. regras de prompt que se degradam com contexto cheio", "padrão middleware (matcher + regex) para interceptar tool calls", "rewriting de input de ferramenta (ex.: npm → pnpm install)", "short-circuit de tool calls com cache (web fetch deduplicado via store)", "override de ferramentas nativas (web search roteado para Exa com fallback)", "redação de segredos por detecção de entropia com substituição por ID e cofre em memória", "variable store (visível entre hooks/turnos) vs. persistent store (entre sessões e restarts)", "customização de UI do harness (linhas de status, botões, painéis ao vivo por hook)", "ask/human-in-the-loop gates para ações sensíveis ou destrutivas", "dry-run gating antes de execução real com aviso visual de modo produção", "auditoria/compliance: envio de todos os eventos a log store externo", "injeção de contexto de knowledge base corporativa via palavras-chave + $http", "chamada de modelos a partir de hooks ($model, ex.: Haiku para resumos) + TTS", "migração de regras do CLAUDE.md para hooks.json determinísticos", "plugins de hooks compartilháveis com o time via repositório Git"]
tools: ["Claude Code", "function hooks", "CLAUDE.md", "plugin-authoring (skill nativa)", "/reload plugins", "plugins.json / hooks.json", "supabase-guard", "Supabase CLI", "Exa MCP / Exa API", "Brave Search", "web search tool", "web fetch tool", "Agent Proxy by Infisical", "Vercel", "npm", "pnpm", "Haiku", "Sonnet 5", "$model", "$http", "text-to-speech (voz Apple)", "GitHub", "Codex"]
people: ["Anthropic", "Ray (autor do vídeo / Agentic Coding School)", "Infisical", "Vercel", "Exa"]
claims: ["Ative function hooks com CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude, o que também libera a skill nativa plugin-authoring", "Hooks de shell existentes não conseguem reescrever prompts, anexar contexto, desenhar UI, fazer perguntas ao usuário, adicionar/editar ferramentas ou lembrar entre sessões — function hooks resolvem todas essas limitações", "Function hooks podem reescrever inputs de tool calls, por exemplo substituindo npm por pnpm install automaticamente", "Use o store para short-circuit: retorne cópia cacheada de URLs já buscadas antes de deixar a tool web fetch prosseguir", "Intercepte a tool nativa de web search e roteie para a Exa API quando houver API key, com fallback para a tool padrão em caso de falha ou ausência de chave", "Redija segredos (por entropia, e-mails, IPs) antes de entrarem no transcript, substituindo por ID guardado em cofre em memória e reescrevendo as requisições de saída com o segredo real — padrão similar ao Agent Proxy da Infisical", "Prefira variable store para dados efêmeros entre turnos e persistent store para dados que devem sobreviver a sessões e restarts (não usar para segredos)", "Function hooks permitem adicionar linhas de UI customizadas no Claude Code, como status de deploy Vercel (queued/building/ready + tempo decorrido) com botões de mostrar/ocultar e painel de dados ao vivo por hook", "Combine ask com dry-runs: bloqueie comandos reais até o dry-run rodar e exiba avisos grandes de 'production mode' ou 'dry mode'", "Configure um gate ask para sugerir refatorar arquivos que excedam ~1000 linhas e evitar arquivos monolíticos gerados por modelos", "Hooks podem chamar modelos via $model (ex.: resumir o turno com Haiku) e falar via TTS nativo quando um turno termina", "Gere palavras-chave do prompt do usuário e use $http para consultar a knowledge base corporativa de forma segura e injetar contexto extra na sessão", "Em setores regulados (saúde, pagamentos), envie cada evento do Claude Code a um log store próprio para trilha de auditoria", "Use ask para impedir envio automático de e-mails/newsletters até confirmação explícita e verificação de leitura", "Crie quizzes via $model + ask antes de permitir abrir um PR, garantindo que o humano entenda as mudanças", "Migre regras determinísticas do CLAUDE.md para hooks.json bem definidos e compartilhe plugins com o time via repositório GitHub", "Peça ao /plugin-authoring para analisar seus CLAUDE.md e propor hooks que tornem o comportamento mais determinístico"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de mecanismos acionáveis e arquiteturalmente novos (middleware de tool calls, rewriting de input, stores de memória cross-session, gates humanos, UI do harness, auditoria) diretamente relevantes a harness-engineering, context-engineering, gates e governança, superando o trecho promocional intermediário."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-claude-code-best-practices-code-w-claude--gv0WHhKelSE|Claude Code best practices | Code w/ Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-this-claude-code-x-obsidian-agentic-os-will-be-the-new-meta--njHuj8OxIVI|This Claude Code x Obsidian Agentic OS Will Be The New Meta]]", "[[extracts/youtube/ai-learning/2026-09-11-mastering-claude-code-in-30-minutes--6eBSHbLKuN0|Mastering Claude Code in 30 minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-proactive-agent-workflow-with-claude-code--eSP7PLTXNy8|Build a proactive agent workflow with Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-i-tried-100-claude-code-skills-these-6-are-the-best--eRS3CmvrOvA|I Tried 100+ Claude Code Skills. These 6 Are The Best]]"]
theme: "Codificação Agêntica com Claude Code"
---

# Anthropic Just Dropped the Biggest Claude Code Update Yet

## Tese
Os 'function hooks' recém-lançados no Claude Code transformam o agente em uma plataforma programável estilo middleware do Express.js, permitindo interceptar e reescrever chamadas de ferramentas, contexto, memória, UI e gates humanos para obter controle determinístico que regras de prompt no CLAUDE.md não garantem.

## Conceitos-chave
- hooks como controle determinístico vs. regras de prompt que se degradam com contexto cheio
- padrão middleware (matcher + regex) para interceptar tool calls
- rewriting de input de ferramenta (ex.: npm → pnpm install)
- short-circuit de tool calls com cache (web fetch deduplicado via store)
- override de ferramentas nativas (web search roteado para Exa com fallback)
- redação de segredos por detecção de entropia com substituição por ID e cofre em memória
- variable store (visível entre hooks/turnos) vs. persistent store (entre sessões e restarts)
- customização de UI do harness (linhas de status, botões, painéis ao vivo por hook)
- ask/human-in-the-loop gates para ações sensíveis ou destrutivas
- dry-run gating antes de execução real com aviso visual de modo produção
- auditoria/compliance: envio de todos os eventos a log store externo
- injeção de contexto de knowledge base corporativa via palavras-chave + $http
- chamada de modelos a partir de hooks ($model, ex.: Haiku para resumos) + TTS
- migração de regras do CLAUDE.md para hooks.json determinísticos
- plugins de hooks compartilháveis com o time via repositório Git

## Ferramentas & pessoas
**Ferramentas:** Claude Code, function hooks, CLAUDE.md, plugin-authoring (skill nativa), /reload plugins, plugins.json / hooks.json, supabase-guard, Supabase CLI, Exa MCP / Exa API, Brave Search, web search tool, web fetch tool, Agent Proxy by Infisical, Vercel, npm, pnpm, Haiku, Sonnet 5, $model, $http, text-to-speech (voz Apple), GitHub, Codex

**Pessoas/orgs:** Anthropic, Ray (autor do vídeo / Agentic Coding School), Infisical, Vercel, Exa

## Claims acionáveis
- Ative function hooks com CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1 claude, o que também libera a skill nativa plugin-authoring
- Hooks de shell existentes não conseguem reescrever prompts, anexar contexto, desenhar UI, fazer perguntas ao usuário, adicionar/editar ferramentas ou lembrar entre sessões — function hooks resolvem todas essas limitações
- Function hooks podem reescrever inputs de tool calls, por exemplo substituindo npm por pnpm install automaticamente
- Use o store para short-circuit: retorne cópia cacheada de URLs já buscadas antes de deixar a tool web fetch prosseguir
- Intercepte a tool nativa de web search e roteie para a Exa API quando houver API key, com fallback para a tool padrão em caso de falha ou ausência de chave
- Redija segredos (por entropia, e-mails, IPs) antes de entrarem no transcript, substituindo por ID guardado em cofre em memória e reescrevendo as requisições de saída com o segredo real — padrão similar ao Agent Proxy da Infisical
- Prefira variable store para dados efêmeros entre turnos e persistent store para dados que devem sobreviver a sessões e restarts (não usar para segredos)
- Function hooks permitem adicionar linhas de UI customizadas no Claude Code, como status de deploy Vercel (queued/building/ready + tempo decorrido) com botões de mostrar/ocultar e painel de dados ao vivo por hook
- Combine ask com dry-runs: bloqueie comandos reais até o dry-run rodar e exiba avisos grandes de 'production mode' ou 'dry mode'
- Configure um gate ask para sugerir refatorar arquivos que excedam ~1000 linhas e evitar arquivos monolíticos gerados por modelos
- Hooks podem chamar modelos via $model (ex.: resumir o turno com Haiku) e falar via TTS nativo quando um turno termina
- Gere palavras-chave do prompt do usuário e use $http para consultar a knowledge base corporativa de forma segura e injetar contexto extra na sessão
- Em setores regulados (saúde, pagamentos), envie cada evento do Claude Code a um log store próprio para trilha de auditoria
- Use ask para impedir envio automático de e-mails/newsletters até confirmação explícita e verificação de leitura
- Crie quizzes via $model + ask antes de permitir abrir um PR, garantindo que o humano entenda as mudanças
- Migre regras determinísticas do CLAUDE.md para hooks.json bem definidos e compartilhe plugins com o time via repositório GitHub
- Peça ao /plugin-authoring para analisar seus CLAUDE.md e propor hooks que tornem o comportamento mais determinístico

> **Deep dive:** `high` — Alta densidade de mecanismos acionáveis e arquiteturalmente novos (middleware de tool calls, rewriting de input, stores de memória cross-session, gates humanos, UI do harness, auditoria) diretamente relevantes a harness-engineering, context-engineering, gates e governança, superando o trecho promocional intermediário.
