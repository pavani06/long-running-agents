---
title: "/handoff is my new favourite skill"
type: "extract"
source: "youtube"
video_id: "dtAJ2dOd3ko"
url: "https://www.youtube.com/watch?v=dtAJ2dOd3ko"
channel: "Matt Pocock"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-handoff-is-my-new-favourite-skill--dtAJ2dOd3ko.txt]]"
tags: ["context-engineering", "context-management", "cross-session", "token-budgeting", "agent-tooling", "agentic-coding", "multi-agent", "harness", "state", "process", "knowledge-management"]
thesis: "Uma skill mínima de 'handoff' que comprime a fatia relevante de uma sessão em um arquivo markdown descartável permite bifurcar trabalho para sessões novas de agentes — um padrão DIY de sub-agente que preserva a pureza do contexto e funciona entre harnesses diferentes."
concepts: ["context window budgeting (zona inteligente vs zona burra, ~120k tokens efetivos em janelas de 1M)", "compação (/compact e autocompact buffer) como continuação da mesma sessão", "documento de handoff como transferência de contexto entre sessões independentes", "padrão DIY de sub-agente (sessão pai → handoff → sessão filha → handoff de volta)", "grilling sessions (grill me / grill with docs) e separação entre known unknowns e questões que exigem protótipo", "suggested skills section no documento de handoff", "ponteiros para artefatos em vez de duplicação de conteúdo", "artefatos descartáveis salvos no diretório temporário do SO", "redação de segredos (API keys, senhas, PII)", "interoperabilidade entre harnesses via markdown (Claude Code, Codex, Copilot CLI) e revisão adversarial", "manter a sessão atual pura ao delegar tarefas fora de escopo"]
tools: ["Claude Code", "/compact e autocompact", "skill handoff", "skill grill me", "skill grill with docs", "skill diagnose", "skill prototype", "Codex", "Copilot CLI", "Sand Castle", "AI Coding for Real Engineers (curso)"]
people: ["Anthropic", "GitHub"]
claims: ["Embora a janela anunciada seja de ~1M tokens, o desempenho decai após ~120k tokens, então orce o contexto com consciência constante", "Use /compact para sessões únicas longas (ex.: debug iterativo), pois ele resume e continua a mesma sessão, mas sobrescreve o contexto acumulado", "Ao notar uma tarefa fora de escopo durante uma sessão, invoque handoff descrevendo o propósito e o foco da próxima sessão para gerar um markdown focado", "Entregar itens fora de escopo via handoff afia a sessão de grilling atual (ex.: questões colapsam por restrição de escopo)", "Padrão recomendado: durante grilling, faça handoff para uma sessão de protótipo para os bits difíceis (UI, lógica complexa) e depois faça handoff dos aprendizados de volta à sessão planejadora", "O handoff em markdown é agnóstico de harness: uma sessão em Claude Code pode passar o documento para Codex ou Copilot CLI, incluindo revisão adversarial entre agentes", "Inclua no documento uma seção de 'suggested skills' para que a próxima sessão invoque automaticamente as skills certas (ex.: grill with docs, diagnose, prototype)", "Não duplique conteúdo já capturado em outros artefatos; use ponteiros para arquivos, issues e recursos existentes", "Salve os arquivos de handoff no diretório temporário do SO, tratando-os como descartáveis, e não como documentação permanente do codebase", "Redija informações sensíveis (API keys, senhas, PII) de qualquer documento de handoff", "Sempre descreva o propósito e o foco da próxima sessão (via argumentos/ditação) ao invocar handoff; sem isso o documento tende a ser ruim"]
deep_dive: "high"
deep_dive_reason: "Apresenta um padrão arquitetural novo e denso em ações práticas — handoff em markdown como sub-agente DIY com handoff bidirecional, interoperabilidade entre harnesses e regras de design (ponteiros, descartabilidade, redação) — diretamente relevante a context-engineering, harness e cross-session."
---

# /handoff is my new favourite skill

## Tese
Uma skill mínima de 'handoff' que comprime a fatia relevante de uma sessão em um arquivo markdown descartável permite bifurcar trabalho para sessões novas de agentes — um padrão DIY de sub-agente que preserva a pureza do contexto e funciona entre harnesses diferentes.

## Conceitos-chave
- context window budgeting (zona inteligente vs zona burra, ~120k tokens efetivos em janelas de 1M)
- compação (/compact e autocompact buffer) como continuação da mesma sessão
- documento de handoff como transferência de contexto entre sessões independentes
- padrão DIY de sub-agente (sessão pai → handoff → sessão filha → handoff de volta)
- grilling sessions (grill me / grill with docs) e separação entre known unknowns e questões que exigem protótipo
- suggested skills section no documento de handoff
- ponteiros para artefatos em vez de duplicação de conteúdo
- artefatos descartáveis salvos no diretório temporário do SO
- redação de segredos (API keys, senhas, PII)
- interoperabilidade entre harnesses via markdown (Claude Code, Codex, Copilot CLI) e revisão adversarial
- manter a sessão atual pura ao delegar tarefas fora de escopo

## Ferramentas & pessoas
**Ferramentas:** Claude Code, /compact e autocompact, skill handoff, skill grill me, skill grill with docs, skill diagnose, skill prototype, Codex, Copilot CLI, Sand Castle, AI Coding for Real Engineers (curso)

**Pessoas/orgs:** Anthropic, GitHub

## Claims acionáveis
- Embora a janela anunciada seja de ~1M tokens, o desempenho decai após ~120k tokens, então orce o contexto com consciência constante
- Use /compact para sessões únicas longas (ex.: debug iterativo), pois ele resume e continua a mesma sessão, mas sobrescreve o contexto acumulado
- Ao notar uma tarefa fora de escopo durante uma sessão, invoque handoff descrevendo o propósito e o foco da próxima sessão para gerar um markdown focado
- Entregar itens fora de escopo via handoff afia a sessão de grilling atual (ex.: questões colapsam por restrição de escopo)
- Padrão recomendado: durante grilling, faça handoff para uma sessão de protótipo para os bits difíceis (UI, lógica complexa) e depois faça handoff dos aprendizados de volta à sessão planejadora
- O handoff em markdown é agnóstico de harness: uma sessão em Claude Code pode passar o documento para Codex ou Copilot CLI, incluindo revisão adversarial entre agentes
- Inclua no documento uma seção de 'suggested skills' para que a próxima sessão invoque automaticamente as skills certas (ex.: grill with docs, diagnose, prototype)
- Não duplique conteúdo já capturado em outros artefatos; use ponteiros para arquivos, issues e recursos existentes
- Salve os arquivos de handoff no diretório temporário do SO, tratando-os como descartáveis, e não como documentação permanente do codebase
- Redija informações sensíveis (API keys, senhas, PII) de qualquer documento de handoff
- Sempre descreva o propósito e o foco da próxima sessão (via argumentos/ditação) ao invocar handoff; sem isso o documento tende a ser ruim

> **Deep dive:** `high` — Apresenta um padrão arquitetural novo e denso em ações práticas — handoff em markdown como sub-agente DIY com handoff bidirecional, interoperabilidade entre harnesses e regras de design (ponteiros, descartabilidade, redação) — diretamente relevante a context-engineering, harness e cross-session.
