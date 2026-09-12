---
title: "Building with Claude Managed Agents and Asana AI teammates"
type: "extract"
source: "youtube"
video_id: "BrpB-h1e--k"
url: "https://www.youtube.com/watch?v=BrpB-h1e--k"
channel: "Claude"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-building-with-claude-managed-agents-and-asana-ai-teammates--BrpB-h1e--k.txt]]"
tags: ["agents", "agent-fleets", "multi-agent", "agent-loop", "agent-tooling", "harness", "context-engineering", "memory-architecture", "knowledge-management", "evals", "verification", "permissions", "governanca", "process", "production"]
thesis: "A Asana entrega AI teammates 'multiplayer' em produção tratando agentes como atores no work graph (memória empresarial compartilhada, RBAC, auditabilidade) enquanto delega a execução multi-step e a verificação de qualidade para o Claude Managed Agents da Anthropic."
concepts: ["agentic enterprise", "agentes como atores no sistema", "modo multiplayer vs single-player de uso de agentes", "memória empresarial compartilhada (enterprise memory)", "work graph: goals → portfolios → projetos → tarefas → approvals", "loop de verificação e grader embutidos", "rubric como prompt", "agent sponsors e RBAC para agentes", "auditabilidade de interações humano-agente", "skills pré-construídas shrink-wrapped", "feedback humano composto em execuções (nudges)", "working backwards dos ideal customer profiles (ICPs)", "agentes proativos", "human-in-the-loop"]
tools: ["Asana AI Teammates", "Claude Managed Agents (CMA)", "Anthropic Messages API", "Claude Console", "MCP", "Google Drive", "Office 365", "Figma"]
people: ["Ara (Asana)", "Asana", "Anthropic", "Bradley (engenheiro Asana)", "Hannah", "Nigel", "Tony", "Google", "Microsoft"]
claims: ["Migrar da Messages API para managed agents eliminou a construção manual de agent loop, gestão de arquivos e execução de código, reduzindo custo e tempo de prototipagem", "O grader embutido itera múltiplas vezes sobre o outcome; passe o contexto empresarial como parte da definição do outcome para alimentar a verificação", "Trate rubrics como qualquer outro prompt: crie evals distintos por outcome e instrumente-os para iterar rápido e decidir com confiança", "Registre nudges e feedback de múltiplos humanos e reenvie-os como contexto em cada execução do managed agent para que a qualidade composto ao longo do tempo", "Persista memória do agente entre usuários para que preferências aprendidas (ex.: mudança de cor primária) não gerem erros repetidos", "Aplique RBAC com sponsors humanos do agente que podem deletar memórias e restringir acesso ao context graph, evitando vazamento entre projetos", "Integre ferramentas de terceiros em dois níveis: diretamente no agent loop próprio e via MCP para os managed agents", "Projete skills pré-construídas working backwards dos ICPs para controlar qualidade, ciclo de vida e release em produto GA shrink-wrapped", "Rastreie toda interação humano-agente em tasks auditáveis conversíveis em approvals, dando aos gestores visibilidade do back-and-forth antes de aprovar", "Rode múltiplos agentes em paralelo para compor planos completos em ações de knowledge workers", "Roadmap: agentes proativos que detectam trabalho não atribuído em kanban boards, geração de dashboards dinâmicos e relatórios de risco com passos de remediação"]
deep_dive: "medium"
deep_dive_reason: "Apresentação de vendor com práticas reais de produção relevantes (memória empresarial, RBAC, verificação via managed agents, integração MCP), porém pesadamente narrada em demo e tom promocional, com profundidade técnica limitada no Q&A."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-founders-build-on-claude-managed-agents--hm8NzEd5io0|How founders build on Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-get-to-production-faster-with-claude-managed-agents--zenIB7XLZxQ|How to get to production faster with Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-s-applied-ai-team-on-the-evolution-of-agentic-surfaces--K0X9QDRkIdg|Anthropic's Applied AI team on the Evolution of Agentic Surfaces]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-ship-your-first-managed-agent--19HDQ9HppOA|Ship your first Managed Agent]]"]
---

# Building with Claude Managed Agents and Asana AI teammates

## Tese
A Asana entrega AI teammates 'multiplayer' em produção tratando agentes como atores no work graph (memória empresarial compartilhada, RBAC, auditabilidade) enquanto delega a execução multi-step e a verificação de qualidade para o Claude Managed Agents da Anthropic.

## Conceitos-chave
- agentic enterprise
- agentes como atores no sistema
- modo multiplayer vs single-player de uso de agentes
- memória empresarial compartilhada (enterprise memory)
- work graph: goals → portfolios → projetos → tarefas → approvals
- loop de verificação e grader embutidos
- rubric como prompt
- agent sponsors e RBAC para agentes
- auditabilidade de interações humano-agente
- skills pré-construídas shrink-wrapped
- feedback humano composto em execuções (nudges)
- working backwards dos ideal customer profiles (ICPs)
- agentes proativos
- human-in-the-loop

## Ferramentas & pessoas
**Ferramentas:** Asana AI Teammates, Claude Managed Agents (CMA), Anthropic Messages API, Claude Console, MCP, Google Drive, Office 365, Figma

**Pessoas/orgs:** Ara (Asana), Asana, Anthropic, Bradley (engenheiro Asana), Hannah, Nigel, Tony, Google, Microsoft

## Claims acionáveis
- Migrar da Messages API para managed agents eliminou a construção manual de agent loop, gestão de arquivos e execução de código, reduzindo custo e tempo de prototipagem
- O grader embutido itera múltiplas vezes sobre o outcome; passe o contexto empresarial como parte da definição do outcome para alimentar a verificação
- Trate rubrics como qualquer outro prompt: crie evals distintos por outcome e instrumente-os para iterar rápido e decidir com confiança
- Registre nudges e feedback de múltiplos humanos e reenvie-os como contexto em cada execução do managed agent para que a qualidade composto ao longo do tempo
- Persista memória do agente entre usuários para que preferências aprendidas (ex.: mudança de cor primária) não gerem erros repetidos
- Aplique RBAC com sponsors humanos do agente que podem deletar memórias e restringir acesso ao context graph, evitando vazamento entre projetos
- Integre ferramentas de terceiros em dois níveis: diretamente no agent loop próprio e via MCP para os managed agents
- Projete skills pré-construídas working backwards dos ICPs para controlar qualidade, ciclo de vida e release em produto GA shrink-wrapped
- Rastreie toda interação humano-agente em tasks auditáveis conversíveis em approvals, dando aos gestores visibilidade do back-and-forth antes de aprovar
- Rode múltiplos agentes em paralelo para compor planos completos em ações de knowledge workers
- Roadmap: agentes proativos que detectam trabalho não atribuído em kanban boards, geração de dashboards dinâmicos e relatórios de risco com passos de remediação

> **Deep dive:** `medium` — Apresentação de vendor com práticas reais de produção relevantes (memória empresarial, RBAC, verificação via managed agents, integração MCP), porém pesadamente narrada em demo e tom promocional, com profundidade técnica limitada no Q&A.
