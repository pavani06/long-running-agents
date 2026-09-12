---
title: "/wayfinder: Nothing is too big to plan anymore"
type: "extract"
source: "youtube"
video_id: "F3lL98Pj90o"
url: "https://www.youtube.com/watch?v=F3lL98Pj90o"
channel: "Matt Pocock"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-wayfinder-nothing-is-too-big-to-plan-anymore--F3lL98Pj90o.txt]]"
tags: ["agents", "agentic-coding", "agent-tooling", "multi-agent", "cross-session", "context-management", "spec-driven-development", "process", "state", "decision-discipline", "roadmap", "knowledge-management"]
thesis: "Wayfinder é uma skill que orquestra o planejamento de trabalhos maiores que a janela de contexto, gerando um mapa persistente de tickets de decisão (com fronteiras e 'fog of war') em qualquer issue tracker, coordenando múltiplas sessões de agente até produzir uma spec não-persistente que vira implementação."
concepts: ["fog of war no planejamento (decisões ainda não decidadas)", "frontier (conjunto de tickets/decisões atualmente acionáveis)", "tickets de decisão vs. tickets de implementação", "orquestração multi-sessão de planejamento", "tipos de ticket: research, prototype, grilling/discussão e task", "dependências e relações de bloqueio entre tickets", "mapa como issue pai com sub-issues (persistência de estado)", "smart zone da janela de contexto", "spec como documento-destino não-persistente", "rastreabilidade à fonte primária (tickets ligados à spec)", "protótipos como mecanismo anti-waterfall", "issue tracker agnóstico via configuração", "handoff automático para sub-agentes"]
tools: ["Wayfinder", "grill me / grill with docs (skill)", "prototype skill", "handoff skill", "to spec", "to tickets", "setup map skills", "skills repo do autor", "GitHub Issues", "Linear", "Jira", "Claude (sub-agentes)", "CVM (course video manager)", "AI Hero (curso gratuito de 7 lições)"]
people: ["autor do skills repo (narrador, não nomeado)", "John (usuário que construiu um harness próprio inspirado no Wayfinder)", "GitHub", "Linear", "Atlassian/Jira", "AI Hero"]
claims: ["Use planejamento single-session quando o trabalho cabe em uma sessão; reserve o Wayfinder para trabalho com 'fog of war' genuíno", "Modele o trabalho como um mapa: issue pai = mapa, sub-issues = tickets de decisão, permitindo estado persistente entre sessões", "Classifique tickets em quatro tipos (research, prototype, grilling, task) e trate cada um como sessão separada com o agente", "Estabeleça relações de bloqueio entre tickets porque algumas decisões só podem ser tomadas após outras", "Mantenha uma 'fronteira' dinâmica: ao resolver um ticket, reavalie quais novos tickets ele desbloqueia", "Faça o agente escrever a resolução de volta ao mapa pai para manter o histórico de decisões sincronizado", "Use protótipos de alta fidelidade durante o planejamento de baixa fidelidade para evitar que o processo vire waterfall", "Gere a spec a partir do mapa com 'to spec' e depois converta em tickets com 'to tickets' antes de implementar", "Trate specs como não-persistente: feche/delete a issue da spec assim que ela estiver refletida no código", "Link a spec de volta aos tickets de decisão originais para que o agente consulte a fonte primária quando confuso", "Configure o skill para qualquer issue tracker (GitHub, Linear, Jira) via 'setup map skills'", "Invoque o Wayfinder duas vezes: uma para chartar o mapa inicial e outra por ticket (via URL do ticket), opcionalmente automatizando com um handoff skill que gera o prompt e spawna sub-agentes", "Delegue tickets de research a sub-agentes que rodam e reportam sem supervisão; agende tasks do mundo real ou bloqueadas atrás de outros trabalhos", "Aplique o método fora de código (ex.: planejamento de escritório de jardim, cursos, pesquisas de fornecedores)", "Defina o destino livremente: uma spec para rodar num agente AFK ou direto em tickets de implementação"]
deep_dive: "high"
deep_dive_reason: "Apesar do tom promocional, o transcript detalha uma arquitetura concreta e replicável de orquestração cross-session (mapa/fronteira/fog-of-war, tipos de ticket, dependências, writeback de resoluções, spec não-persistente com rastreio à fonte primária) altamente acionável para harness e context-engineering."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-workflow--iQyg-KypKAA|L8 Principal's Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-so-i-tried-matt-s-skills--0oXOOlqVu5M|So I tried Matt's skills...]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-l8-principal-s-agentic-engineering-setup-just-copy-him--8ZgpAXe5V5w|L8 Principal's Agentic Engineering Setup (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-building-great-agent-skills-the-missing-manual--UNzCG3lw6O0|Building Great Agent Skills: The Missing Manual]]"]
---

# /wayfinder: Nothing is too big to plan anymore

## Tese
Wayfinder é uma skill que orquestra o planejamento de trabalhos maiores que a janela de contexto, gerando um mapa persistente de tickets de decisão (com fronteiras e 'fog of war') em qualquer issue tracker, coordenando múltiplas sessões de agente até produzir uma spec não-persistente que vira implementação.

## Conceitos-chave
- fog of war no planejamento (decisões ainda não decidadas)
- frontier (conjunto de tickets/decisões atualmente acionáveis)
- tickets de decisão vs. tickets de implementação
- orquestração multi-sessão de planejamento
- tipos de ticket: research, prototype, grilling/discussão e task
- dependências e relações de bloqueio entre tickets
- mapa como issue pai com sub-issues (persistência de estado)
- smart zone da janela de contexto
- spec como documento-destino não-persistente
- rastreabilidade à fonte primária (tickets ligados à spec)
- protótipos como mecanismo anti-waterfall
- issue tracker agnóstico via configuração
- handoff automático para sub-agentes

## Ferramentas & pessoas
**Ferramentas:** Wayfinder, grill me / grill with docs (skill), prototype skill, handoff skill, to spec, to tickets, setup map skills, skills repo do autor, GitHub Issues, Linear, Jira, Claude (sub-agentes), CVM (course video manager), AI Hero (curso gratuito de 7 lições)

**Pessoas/orgs:** autor do skills repo (narrador, não nomeado), John (usuário que construiu um harness próprio inspirado no Wayfinder), GitHub, Linear, Atlassian/Jira, AI Hero

## Claims acionáveis
- Use planejamento single-session quando o trabalho cabe em uma sessão; reserve o Wayfinder para trabalho com 'fog of war' genuíno
- Modele o trabalho como um mapa: issue pai = mapa, sub-issues = tickets de decisão, permitindo estado persistente entre sessões
- Classifique tickets em quatro tipos (research, prototype, grilling, task) e trate cada um como sessão separada com o agente
- Estabeleça relações de bloqueio entre tickets porque algumas decisões só podem ser tomadas após outras
- Mantenha uma 'fronteira' dinâmica: ao resolver um ticket, reavalie quais novos tickets ele desbloqueia
- Faça o agente escrever a resolução de volta ao mapa pai para manter o histórico de decisões sincronizado
- Use protótipos de alta fidelidade durante o planejamento de baixa fidelidade para evitar que o processo vire waterfall
- Gere a spec a partir do mapa com 'to spec' e depois converta em tickets com 'to tickets' antes de implementar
- Trate specs como não-persistente: feche/delete a issue da spec assim que ela estiver refletida no código
- Link a spec de volta aos tickets de decisão originais para que o agente consulte a fonte primária quando confuso
- Configure o skill para qualquer issue tracker (GitHub, Linear, Jira) via 'setup map skills'
- Invoque o Wayfinder duas vezes: uma para chartar o mapa inicial e outra por ticket (via URL do ticket), opcionalmente automatizando com um handoff skill que gera o prompt e spawna sub-agentes
- Delegue tickets de research a sub-agentes que rodam e reportam sem supervisão; agende tasks do mundo real ou bloqueadas atrás de outros trabalhos
- Aplique o método fora de código (ex.: planejamento de escritório de jardim, cursos, pesquisas de fornecedores)
- Defina o destino livremente: uma spec para rodar num agente AFK ou direto em tickets de implementação

> **Deep dive:** `high` — Apesar do tom promocional, o transcript detalha uma arquitetura concreta e replicável de orquestração cross-session (mapa/fronteira/fog-of-war, tipos de ticket, dependências, writeback de resoluções, spec não-persistente com rastreio à fonte primária) altamente acionável para harness e context-engineering.
