---
title: "Harness Engineering: What Separates Top Agentic Engineers Right Now"
type: "extract"
source: "youtube"
video_id: "ulNsa0sD8N0"
url: "https://www.youtube.com/watch?v=ulNsa0sD8N0"
channel: "Cole Medin"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-harness-engineering-what-separates-top-agentic-engineers-right-now--ulNsa0sD8N0.txt]]"
tags: ["harness", "harness-engineering", "context-engineering", "agentic-coding", "agent-loop", "multi-agent", "agent-fleets", "code-review", "cross-session", "error-handling", "verification", "testes-qa", "process", "production", "observability", "token-budgeting", "gate-design", "permissions", "spec-driven-development"]
thesis: "Harness engineering é a evolução do context engineering: projetar o wrapper completo ao redor do LLM — dos rules/skills/hooks dentro de uma sessão até a orquestração automatizada de múltiplas sessões de coding agents — adotando o mindset de que cada falha do agente se converte em melhoria do harness em vez de espera pela próxima versão do modelo."
concepts: ["harness engineering", "AI layer (wrapper construído pelo usuário)", "evolução de context engineering para harness engineering", "distinção entre contexto e controle (orquestração, Ralph loops, subagentes)", "skill issue reframe / system evolution: toda falha vira regra, hook ou skill", "seis componentes da AI layer: regras globais, skills, servidores MCP, busca no codebase (LSP/knowledge graphs), hooks, subagentes", "separação de planejamento, implementação e validação em sessões distintas", "artefatos markdown como handoff entre sessões", "pre-tool-use hooks para segurança", "stop validation hook com testes, lint e type-check deterministicos", "lint após cada edição de arquivo", "code review agents paralelos especializados (segurança, corretude, simplicidade)", "Ralph loop: script que divide um PRD em tarefas e itera sessões de coding agent", "condição de saída via done.txt no while loop", "eficiência de tokens via foco por sessão"]
tools: ["Claude Code", "Codex", "Pi", "GPT", "Opus 5", "GPT-6", "MCP", "LSP", "Ralph loop", "Archon", "Google Cloud", "Google Agent CLI", "Google Agent SDK"]
people: ["Cole (apresentador)", "Jeffrey Huntley (criador do Ralph)", "Google Cloud"]
claims: ["Escolher a ferramenta de coding (Claude Code, Codex etc.) já é escolher a primeira camada de harness, pois ela empacota o modelo com capacidades e system prompt", "A AI layer que você constrói compreende seis componentes: regras globais, skills, servidores MCP, busca no codebase (LSP/knowledge graphs), hooks e subagentes", "A diferença real entre harness engineering e context engineering é o controle: orquestrar sessões, subagentes e loops como o Ralph, enquanto o resto (injeção de contexto, tools, persistência, observabilidade) permanece context engineering", "Adote o reframe da 'skill issue': quando o agente erra, não espere a próxima versão do modelo — transforme a falha em regra (agents.md), hook de bloqueio ou skill atualizada", "Rode planejamento, implementação e validação em sessões separadas de coding agent, cada skill produzindo um artefato markdown usado como handoff, para manter cada sessão token-eficiente e focada", "Use pre-tool-use hooks para segurança, por exemplo bloquear leitura de arquivos indesejados no contexto ou remoção destrutiva de diretórios", "Use um stop validation hook para rodar deterministicamente unit tests, linting e type-check quando o agente diz que terminou, forçando iteração até tudo passar", "Rode um lint rápido após cada edição de arquivo para manter o codebase limpo e aumentar a confiabilidade futura dos agentes", "Não entregue um PRD massivo a uma única sessão de coding agent: divida em tarefas focadas e orquestre múltiplas sessões (com subagentes ou sessões reais com handoffs)", "Paralelize code review agents especializados (segurança, corretude, simplicidade) e só crie o pull request se todos passarem, iterando a implementação caso contrário", "O Ralph loop é um script simples (Python ou bash) que recebe um escopo grande, gera um fix plan por iterações, executa sessões sequenciais de coding agent e só sai do while loop quando um done.txt indica que todos os itens do spec foram implementados e validados", "O Google Agent CLI (gratuito e open source) fornece skills que instruem o coding agent a construir agentes com o Google Agent SDK, testá-los localmente com app de chat e fazer deploy de um comando no Google Cloud com playground e traces", "Archon é um builder open source de harnesses customizados ao seu processo e SDLC, como alternativa ao Ralph loop"]
deep_dive: "medium"
deep_dive_reason: "Diretamente relevante a harness com dicas acionáveis concretas (padrões de hooks, handoffs de sessão, mecânica do Ralph loop), mas sintetiza conceitos já existentes e contém segmentos promocionais, sem densidade arquitetural genuinamente nova."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-how-to-build-software-when-humans-steer-agents-execute-ryan--am_oeAoUhew|Harness Engineering: How to Build Software When Humans Steer, Agents Execute — Ryan Lopopolo, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-ryan-lopopolo-harness-engineering-how-to-build-software-when-humans-steer-and-ag--c8bE0cj7vHY|Ryan Lopopolo - Harness Engineering: How to Build Software When Humans Steer and Agents Execute]]", "[[extracts/youtube/ai-learning/2026-09-11-when-to-build-your-own-agent-harness-harrison-chase-langchain--HI2q3ci3Iuc|When to Build Your Own Agent Harness | Harrison Chase, LangChain]]", "[[extracts/youtube/ai-learning/2026-09-11-harnesses-in-ai-a-deep-dive-tejas-kumar-ibm--C_GG5g38vLU|Harnesses in AI: A Deep Dive — Tejas Kumar, IBM]]", "[[extracts/youtube/ai-learning/2026-09-11-why-the-harness-matters-more-than-the-model-yc-paper-club--n9xKblqyQ28|Why The Harness Matters More Than The Model | YC Paper Club]]", "[[extracts/youtube/ai-learning/2026-09-11-the-golden-age-of-ai-engineering-alexander-embiricos-romain-huet-peter-steinberg--pMggiOb18tc|The Golden Age of AI Engineering — Alexander Embiricos & Romain Huet & Peter Steinberger, OpenAI]]", "[[extracts/youtube/ai-learning/2026-09-11-harness-engineering-is-not-enough-why-software-factories-fail-dex-horthy-humanla--Ib5GBkD555M|Harness Engineering is not Enough: Why Software Factories Fail — Dex Horthy, HumanLayer]]", "[[extracts/youtube/ai-learning/2026-09-11-getting-started-with-omnigent-the-coding-agent-meta-harness--AyV0hum_hA8|Getting Started with Omnigent | The Coding Agent Meta-Harness]]"]
---

# Harness Engineering: What Separates Top Agentic Engineers Right Now

## Tese
Harness engineering é a evolução do context engineering: projetar o wrapper completo ao redor do LLM — dos rules/skills/hooks dentro de uma sessão até a orquestração automatizada de múltiplas sessões de coding agents — adotando o mindset de que cada falha do agente se converte em melhoria do harness em vez de espera pela próxima versão do modelo.

## Conceitos-chave
- harness engineering
- AI layer (wrapper construído pelo usuário)
- evolução de context engineering para harness engineering
- distinção entre contexto e controle (orquestração, Ralph loops, subagentes)
- skill issue reframe / system evolution: toda falha vira regra, hook ou skill
- seis componentes da AI layer: regras globais, skills, servidores MCP, busca no codebase (LSP/knowledge graphs), hooks, subagentes
- separação de planejamento, implementação e validação em sessões distintas
- artefatos markdown como handoff entre sessões
- pre-tool-use hooks para segurança
- stop validation hook com testes, lint e type-check deterministicos
- lint após cada edição de arquivo
- code review agents paralelos especializados (segurança, corretude, simplicidade)
- Ralph loop: script que divide um PRD em tarefas e itera sessões de coding agent
- condição de saída via done.txt no while loop
- eficiência de tokens via foco por sessão

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Codex, Pi, GPT, Opus 5, GPT-6, MCP, LSP, Ralph loop, Archon, Google Cloud, Google Agent CLI, Google Agent SDK

**Pessoas/orgs:** Cole (apresentador), Jeffrey Huntley (criador do Ralph), Google Cloud

## Claims acionáveis
- Escolher a ferramenta de coding (Claude Code, Codex etc.) já é escolher a primeira camada de harness, pois ela empacota o modelo com capacidades e system prompt
- A AI layer que você constrói compreende seis componentes: regras globais, skills, servidores MCP, busca no codebase (LSP/knowledge graphs), hooks e subagentes
- A diferença real entre harness engineering e context engineering é o controle: orquestrar sessões, subagentes e loops como o Ralph, enquanto o resto (injeção de contexto, tools, persistência, observabilidade) permanece context engineering
- Adote o reframe da 'skill issue': quando o agente erra, não espere a próxima versão do modelo — transforme a falha em regra (agents.md), hook de bloqueio ou skill atualizada
- Rode planejamento, implementação e validação em sessões separadas de coding agent, cada skill produzindo um artefato markdown usado como handoff, para manter cada sessão token-eficiente e focada
- Use pre-tool-use hooks para segurança, por exemplo bloquear leitura de arquivos indesejados no contexto ou remoção destrutiva de diretórios
- Use um stop validation hook para rodar deterministicamente unit tests, linting e type-check quando o agente diz que terminou, forçando iteração até tudo passar
- Rode um lint rápido após cada edição de arquivo para manter o codebase limpo e aumentar a confiabilidade futura dos agentes
- Não entregue um PRD massivo a uma única sessão de coding agent: divida em tarefas focadas e orquestre múltiplas sessões (com subagentes ou sessões reais com handoffs)
- Paralelize code review agents especializados (segurança, corretude, simplicidade) e só crie o pull request se todos passarem, iterando a implementação caso contrário
- O Ralph loop é um script simples (Python ou bash) que recebe um escopo grande, gera um fix plan por iterações, executa sessões sequenciais de coding agent e só sai do while loop quando um done.txt indica que todos os itens do spec foram implementados e validados
- O Google Agent CLI (gratuito e open source) fornece skills que instruem o coding agent a construir agentes com o Google Agent SDK, testá-los localmente com app de chat e fazer deploy de um comando no Google Cloud com playground e traces
- Archon é um builder open source de harnesses customizados ao seu processo e SDLC, como alternativa ao Ralph loop

> **Deep dive:** `medium` — Diretamente relevante a harness com dicas acionáveis concretas (padrões de hooks, handoffs de sessão, mecânica do Ralph loop), mas sintetiza conceitos já existentes e contém segmentos promocionais, sem densidade arquitetural genuinamente nova.
