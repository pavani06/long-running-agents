---
title: "Claude Code best practices | Code w/ Claude"
type: "extract"
source: "youtube"
video_id: "gv0WHhKelSE"
url: "https://www.youtube.com/watch?v=gv0WHhKelSE"
channel: "Anthropic"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-claude-code-best-practices-code-w-claude--gv0WHhKelSE.txt]]"
tags: ["agentic-coding", "agent-loop", "agent-tooling", "harness", "context-engineering", "context-management", "permissions", "multi-agent", "state", "cross-session", "model-selection", "testes-qa", "verification"]
thesis: "Claude Code é um 'agente puro' — instruções, ferramentas poderosas de terminal e um loop até o modelo decidir terminar, sem indexação/RAG — cujo melhor uso depende de gerenciamento deliberado de contexto (CLAUDE.md, /clear, /compact), permissões e verificação de planos antes da execução."
concepts: ["Agente puro: instruções + ferramentas + loop até o modelo decidir que terminou", "Busca agnética (glob, grep, find) em vez de indexação/embeddings/RAG para entender o codebase", "CLAUDE.md como memória e compartilhamento de estado entre sessões e membros do time", "Sistema de permissões com humano-no-loop: leitura liberada por padrão, escrita e bash gated", "Gerenciamento de janela de contexto de 200k tokens via /clear e /compact com resumo de handoff", "Planejamento antes da execução e to-do lists como mecanismo de verificação e redirecionamento", "Uso do agente como parceiro de pensamento: reportar 2-3 opções antes de escrever arquivos", "Extended thinking entre chamadas de ferramentas (novidade do Claude 4)", "Automação headless/programática via SDK (CI/CD, GitHub Actions)", "Orquestração de múltiplas instâncias paralelas comunicando-se via arquivos markdown compartilhados", "Seleção de modelo em runtime (/model, /config)", "MCP como mecanismo de expansão de ferramentas quando CLI não basta", "Test-driven development e commits regulares como guardrails para agentes de código"]
tools: ["Claude Code", "MCP (Model Context Protocol)", "Claude Code SDK", "VS Code", "JetBrains", "GitHub / gh CLI", "Git", "Docker", "BigQuery", "tmux", "npm", "AWS e GCP (hospedagem do modelo)", "GitHub Actions", "Vim"]
people: ["Cal (palestrante, time de Applied AI e core contributor do Claude Code)", "Anthropic", "Boris (time inicial do Claude Code)", "Cat (time inicial do Claude Code)", "Tony (mentor citado na anedota)"]
claims: ["Coloque um CLAUDE.md no diretório do projeto (versionado para o time) e/ou no home; ele é injetado no prompt em cada inicialização como instruções que o modelo deve seguir de perto.", "Arquivos CLAUDE.md em subdiretórios não são mais carregados automaticamente (evita estourar contexto em monorepos); o Claude deve lê-los quando a busca os tornar relevantes.", "Use referências com @ dentro do CLAUDE.md para importar outros arquivos de instruções que devem sempre ser lidos.", "Configure permissões: leitura é liberada por padrão, mas escrita e bash exigem aprovação; use auto-accept (shift+tab) e pré-aprove comandos recorrentes como npm run test nas settings.", "Quando existir um CLI bem documentado e um servidor MCP para a mesma tarefa, prefira o CLI.", "Ao ver o aviso de contexto cheio, use /clear para recomeçar (preservando CLAUDE.md) ou /compact para gerar um resumo de handoff que semeia a próxima sessão.", "Antes de corrigir bugs, peça que o agente pesquise a causa e apresente um plano sem escrever arquivos, para você validar o rumo antes da execução.", "Monitore a to-do list gerada pelo agente e pressione escape para interromper e redirecionar quando aparecer um item estranho.", "Aplique TDD com agentes: mudanças pequenas, rodar testes após cada mudança, checar TypeScript/linting e commitar regularmente para poder reverter.", "Use screenshots (multimodalidade) para guiar implementações de UI e depurar visualmente.", "Escape interrompe a execução para intervir; escape duplo retrocede na conversa e permite resetar tool expansion.", "Use /model e /config para alternar entre modelos (padrão Sonnet, Opus disponível) conforme a tarefa.", "Claude 4 permite extended thinking entre chamadas de ferramentas; inserir 'think hard' no prompt é útil em tarefas complexas.", "Para coordenar múltiplos agentes (ex.: agente 2 e 3 consumindo contexto do agente 1), escreva estado compartilhado em um markdown (ex.: ticket.md) que os outros agentes leem como nota de outro desenvolvedor.", "Claude 4 segue instruções do CLAUDE.md e do prompt significativamente melhor; migração de modelo é boa ocasião para auditar e podar o arquivo.", "O hábito do modelo de deixar comentários inline redundantes era um problema do modelo (não do prompt), parcialmente contido no Claude 4."]
deep_dive: "medium"
deep_dive_reason: "Contém densidade razoável de práticas acionáveis sobre harness, contexto e permissões (CLAUDE.md, /compact, plano-antes-de-executar, estado via markdown), mas é essencialmente uma visão geral de produto com profundidade arquitetural moderada e caráter parcialmente promocional."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-mastering-claude-code-in-30-minutes--6eBSHbLKuN0|Mastering Claude Code in 30 minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-how-we-claude-code--IlqJqcl8ONE|How we Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-proactive-agent-workflow-with-claude-code--eSP7PLTXNy8|Build a proactive agent workflow with Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-mcp-how-to-modify-your-servers-to-the-next-level--aIAxWr5ix1o|Claude MCP - How To Modify Your Servers To The Next Level]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-just-dropped-the-biggest-claude-code-update-yet--B-YQANvDOq0|Anthropic Just Dropped the Biggest Claude Code Update Yet]]", "[[extracts/youtube/ai-learning/2026-09-11-build-a-claude-knowledge-base-that-self-improves--ib74sLgjIBM|Build A Claude Knowledge Base That Self-Improves!]]", "[[extracts/youtube/ai-learning/2026-09-11-build-anything-with-tmux-here-s-how--z7xyZQVK4Dg|Build Anything with Tmux, Here's How]]"]
theme: "Codificação Agêntica com Claude Code"
---

# Claude Code best practices | Code w/ Claude

## Tese
Claude Code é um 'agente puro' — instruções, ferramentas poderosas de terminal e um loop até o modelo decidir terminar, sem indexação/RAG — cujo melhor uso depende de gerenciamento deliberado de contexto (CLAUDE.md, /clear, /compact), permissões e verificação de planos antes da execução.

## Conceitos-chave
- Agente puro: instruções + ferramentas + loop até o modelo decidir que terminou
- Busca agnética (glob, grep, find) em vez de indexação/embeddings/RAG para entender o codebase
- CLAUDE.md como memória e compartilhamento de estado entre sessões e membros do time
- Sistema de permissões com humano-no-loop: leitura liberada por padrão, escrita e bash gated
- Gerenciamento de janela de contexto de 200k tokens via /clear e /compact com resumo de handoff
- Planejamento antes da execução e to-do lists como mecanismo de verificação e redirecionamento
- Uso do agente como parceiro de pensamento: reportar 2-3 opções antes de escrever arquivos
- Extended thinking entre chamadas de ferramentas (novidade do Claude 4)
- Automação headless/programática via SDK (CI/CD, GitHub Actions)
- Orquestração de múltiplas instâncias paralelas comunicando-se via arquivos markdown compartilhados
- Seleção de modelo em runtime (/model, /config)
- MCP como mecanismo de expansão de ferramentas quando CLI não basta
- Test-driven development e commits regulares como guardrails para agentes de código

## Ferramentas & pessoas
**Ferramentas:** Claude Code, MCP (Model Context Protocol), Claude Code SDK, VS Code, JetBrains, GitHub / gh CLI, Git, Docker, BigQuery, tmux, npm, AWS e GCP (hospedagem do modelo), GitHub Actions, Vim

**Pessoas/orgs:** Cal (palestrante, time de Applied AI e core contributor do Claude Code), Anthropic, Boris (time inicial do Claude Code), Cat (time inicial do Claude Code), Tony (mentor citado na anedota)

## Claims acionáveis
- Coloque um CLAUDE.md no diretório do projeto (versionado para o time) e/ou no home; ele é injetado no prompt em cada inicialização como instruções que o modelo deve seguir de perto.
- Arquivos CLAUDE.md em subdiretórios não são mais carregados automaticamente (evita estourar contexto em monorepos); o Claude deve lê-los quando a busca os tornar relevantes.
- Use referências com @ dentro do CLAUDE.md para importar outros arquivos de instruções que devem sempre ser lidos.
- Configure permissões: leitura é liberada por padrão, mas escrita e bash exigem aprovação; use auto-accept (shift+tab) e pré-aprove comandos recorrentes como npm run test nas settings.
- Quando existir um CLI bem documentado e um servidor MCP para a mesma tarefa, prefira o CLI.
- Ao ver o aviso de contexto cheio, use /clear para recomeçar (preservando CLAUDE.md) ou /compact para gerar um resumo de handoff que semeia a próxima sessão.
- Antes de corrigir bugs, peça que o agente pesquise a causa e apresente um plano sem escrever arquivos, para você validar o rumo antes da execução.
- Monitore a to-do list gerada pelo agente e pressione escape para interromper e redirecionar quando aparecer um item estranho.
- Aplique TDD com agentes: mudanças pequenas, rodar testes após cada mudança, checar TypeScript/linting e commitar regularmente para poder reverter.
- Use screenshots (multimodalidade) para guiar implementações de UI e depurar visualmente.
- Escape interrompe a execução para intervir; escape duplo retrocede na conversa e permite resetar tool expansion.
- Use /model e /config para alternar entre modelos (padrão Sonnet, Opus disponível) conforme a tarefa.
- Claude 4 permite extended thinking entre chamadas de ferramentas; inserir 'think hard' no prompt é útil em tarefas complexas.
- Para coordenar múltiplos agentes (ex.: agente 2 e 3 consumindo contexto do agente 1), escreva estado compartilhado em um markdown (ex.: ticket.md) que os outros agentes leem como nota de outro desenvolvedor.
- Claude 4 segue instruções do CLAUDE.md e do prompt significativamente melhor; migração de modelo é boa ocasião para auditar e podar o arquivo.
- O hábito do modelo de deixar comentários inline redundantes era um problema do modelo (não do prompt), parcialmente contido no Claude 4.

> **Deep dive:** `medium` — Contém densidade razoável de práticas acionáveis sobre harness, contexto e permissões (CLAUDE.md, /compact, plano-antes-de-executar, estado via markdown), mas é essencialmente uma visão geral de produto com profundidade arquitetural moderada e caráter parcialmente promocional.
