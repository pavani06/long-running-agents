---
title: "Build a proactive agent workflow with Claude Code"
type: "extract"
source: "youtube"
video_id: "eSP7PLTXNy8"
url: "https://www.youtube.com/watch?v=eSP7PLTXNy8"
channel: "Claude"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-build-a-proactive-agent-workflow-with-claude-code--eSP7PLTXNy8.txt]]"
tags: ["agent-tooling", "agents", "agentic-coding", "code-review", "documentation-publishing", "escalation", "monitoramento", "multi-agent", "verification", "observability"]
thesis: "A funcionalidade Routines do Claude Code transforma o coding agent de ferramenta reativa em 'teammate' proativo, abstraindo hosting, estado de sessão, autenticação de conectores e triggers (agendados ou baseados em eventos como GitHub/webhooks), com sessões remotas que permanecem observáveis, direcionáveis e retomáveis em tempo real."
concepts: ["agentes proativos vs. reativos (de ferramenta a teammate)", "Routines: prompt + repos + conectores + trigger como definição completa", "triggers agendados (schedule-based) vs. event-based (eventos nativos do GitHub, webhooks custom com payload como contexto)", "framework de 3 decisões: trigger, contexto e steerability", "o contexto fornecido é o teto do desempenho do agente", "agent-on-agent review / padrão generator-critic aplicado a revisão de PRs", "human-in-the-loop vs. human-out-of-the-loop", "sessões interativas e steerable via web, CLI e desktop (watch, steer, resume)", "infraestrutura gerenciada: hosting, session state, connector auth", "escada de autonomia e confiança (escalation progressiva de decisão go/no-go até rollback autônomo)", "verificação de outputs (render das páginas de documentação alteradas)", "automação de documentação via diff entre código-fonte e repo de docs"]
tools: ["Claude Code", "Routines", "Claude Agent SDK", "comando /schedule", "GitHub", "GitHub MCP", "Slack", "Google Drive", "Datadog", "Grafana", "Twilio", "claude.ai (Claude Code on the web)", "cron", "webhooks"]
people: ["Maya (Anthropic, Applied AI team)", "Sarah (engenheira de documentação, Anthropic)", "Anthropic"]
claims: ["Crie uma routine definindo apenas prompt, repositórios, conectores e trigger; o Claude Code gerencia hosting, estado de sessão e autenticação de conectores em infra gerenciada.", "Triggers podem ser agendados ou event-based, com suporte nativo a eventos do GitHub e a POST em webhooks custom com o payload do evento como contexto da sessão.", "Toda routine é uma sessão Claude Code real que pode ser aberta, observada, questionada no meio da execução, redirecionada e retomada via web, CLI ou desktop.", "Use /schedule no terminal do Claude Code: o próprio Claude faz perguntas de esclarecimento (horário, notificações) e gera a routine automaticamente.", "Trate o contexto conectado (repos, Drive, Slack, MCPs) como o teto do sucesso do agente — conecte tudo que ele precisa antes de acionar.", "Aplique o padrão generator-critic: uma routine cria PRs de docs e uma segunda routine dispara na criação do PR para comentar/revisar antes da intervenção humana.", "Verifique outputs do agente renderizando as páginas de documentação alteradas para confirmar o resultado esperado.", "Construa um deploy verifier: trigger via webhook do pipeline de CD, contexto com código-fonte + ferramentas de monitoramento (Datadog/Grafana) e alertas (Slack/Twilio); comece com decisão go/no-go humana e escale gradualmente até permitir rollback autônomo conforme a confiança aumenta.", "Cubra gargalos de documentação com rotinas: revisão semanal de merges vs. repo de docs, trigger em release/branch diff, ou trigger em PRs com label 'need docs'.", "Outros padrões citados: investigador de plantão (on-call investigator) e triagem semanal de backlog (GitHub issues/Slack) com priorização e abertura de PRs pelo agente.", "PRs semanais do Claude Code cresceram 200% desde o início do ano, motivando a automação interna de manutenção de docs na Anthropic."]
deep_dive: "medium"
deep_dive_reason: "Apresenta um recurso novo (Routines) com framework acionável (trigger/contexto/steerability), padrões de multi-agente e escalation de autonomia, mas é essencialmente um demo de produto promocional sem profundidade arquitetural, de evals ou de harness."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-how-the-claude-code-team-uses-claude-code--S-sYlFiGFv8|How the Claude Code team uses Claude Code]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-code-best-practices-code-w-claude--gv0WHhKelSE|Claude Code best practices | Code w/ Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-mastering-claude-code-in-30-minutes--6eBSHbLKuN0|Mastering Claude Code in 30 minutes]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-instantly-build-ai-agents-in-n8n-using-claude--uAtSMEBosGU|How to INSTANTLY Build AI Agents in N8N Using Claude]]", "[[extracts/youtube/ai-learning/2026-09-11-how-founders-build-on-claude-managed-agents--hm8NzEd5io0|How founders build on Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-how-to-get-to-production-faster-with-claude-managed-agents--zenIB7XLZxQ|How to get to production faster with Claude Managed Agents]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-codes-new-intent-md-what-is-it--LoMOPj-lO8U|Claude Codes New INTENT.MD, What is It?]]", "[[extracts/youtube/ai-learning/2026-09-11-building-ai-agents-with-claude-demo--_al9YYnF2xI|Building AI Agents with Claude! (Demo)]]", "[[extracts/youtube/ai-learning/2026-09-11-anthropic-just-dropped-the-biggest-claude-code-update-yet--B-YQANvDOq0|Anthropic Just Dropped the Biggest Claude Code Update Yet]]"]
theme: "Codificação Agêntica com Claude Code"
---

# Build a proactive agent workflow with Claude Code

## Tese
A funcionalidade Routines do Claude Code transforma o coding agent de ferramenta reativa em 'teammate' proativo, abstraindo hosting, estado de sessão, autenticação de conectores e triggers (agendados ou baseados em eventos como GitHub/webhooks), com sessões remotas que permanecem observáveis, direcionáveis e retomáveis em tempo real.

## Conceitos-chave
- agentes proativos vs. reativos (de ferramenta a teammate)
- Routines: prompt + repos + conectores + trigger como definição completa
- triggers agendados (schedule-based) vs. event-based (eventos nativos do GitHub, webhooks custom com payload como contexto)
- framework de 3 decisões: trigger, contexto e steerability
- o contexto fornecido é o teto do desempenho do agente
- agent-on-agent review / padrão generator-critic aplicado a revisão de PRs
- human-in-the-loop vs. human-out-of-the-loop
- sessões interativas e steerable via web, CLI e desktop (watch, steer, resume)
- infraestrutura gerenciada: hosting, session state, connector auth
- escada de autonomia e confiança (escalation progressiva de decisão go/no-go até rollback autônomo)
- verificação de outputs (render das páginas de documentação alteradas)
- automação de documentação via diff entre código-fonte e repo de docs

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Routines, Claude Agent SDK, comando /schedule, GitHub, GitHub MCP, Slack, Google Drive, Datadog, Grafana, Twilio, claude.ai (Claude Code on the web), cron, webhooks

**Pessoas/orgs:** Maya (Anthropic, Applied AI team), Sarah (engenheira de documentação, Anthropic), Anthropic

## Claims acionáveis
- Crie uma routine definindo apenas prompt, repositórios, conectores e trigger; o Claude Code gerencia hosting, estado de sessão e autenticação de conectores em infra gerenciada.
- Triggers podem ser agendados ou event-based, com suporte nativo a eventos do GitHub e a POST em webhooks custom com o payload do evento como contexto da sessão.
- Toda routine é uma sessão Claude Code real que pode ser aberta, observada, questionada no meio da execução, redirecionada e retomada via web, CLI ou desktop.
- Use /schedule no terminal do Claude Code: o próprio Claude faz perguntas de esclarecimento (horário, notificações) e gera a routine automaticamente.
- Trate o contexto conectado (repos, Drive, Slack, MCPs) como o teto do sucesso do agente — conecte tudo que ele precisa antes de acionar.
- Aplique o padrão generator-critic: uma routine cria PRs de docs e uma segunda routine dispara na criação do PR para comentar/revisar antes da intervenção humana.
- Verifique outputs do agente renderizando as páginas de documentação alteradas para confirmar o resultado esperado.
- Construa um deploy verifier: trigger via webhook do pipeline de CD, contexto com código-fonte + ferramentas de monitoramento (Datadog/Grafana) e alertas (Slack/Twilio); comece com decisão go/no-go humana e escale gradualmente até permitir rollback autônomo conforme a confiança aumenta.
- Cubra gargalos de documentação com rotinas: revisão semanal de merges vs. repo de docs, trigger em release/branch diff, ou trigger em PRs com label 'need docs'.
- Outros padrões citados: investigador de plantão (on-call investigator) e triagem semanal de backlog (GitHub issues/Slack) com priorização e abertura de PRs pelo agente.
- PRs semanais do Claude Code cresceram 200% desde o início do ano, motivando a automação interna de manutenção de docs na Anthropic.

> **Deep dive:** `medium` — Apresenta um recurso novo (Routines) com framework acionável (trigger/contexto/steerability), padrões de multi-agente e escalation de autonomia, mas é essencialmente um demo de produto promocional sem profundidade arquitetural, de evals ou de harness.
