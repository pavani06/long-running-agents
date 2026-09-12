---
title: "So I tried Matt's skills..."
type: "extract"
source: "youtube"
video_id: "0oXOOlqVu5M"
url: "https://www.youtube.com/watch?v=0oXOOlqVu5M"
channel: "Theo - t3․gg"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-so-i-tried-matt-s-skills--0oXOOlqVu5M.txt]]"
tags: ["harness", "harness-engineering", "context-engineering", "agent-tooling", "stack-tooling", "agents", "agentic-coding", "multi-agent", "verification", "decision-discipline", "knowledge-management", "process", "documentation-publishing"]
thesis: "Skills em markdown simples — as de Matt Pocock e o PStack de Potato — melhoram drasticamente a qualidade e a disciplina da saída de agentes de codificação, mas devem ser auditadas, testadas e adaptadas seletivamente ao seu fluxo, nunca instaladas às cegas."
concepts: ["AI skills como arquivos markdown", "descrição de skill como gatilho (não documentação)", "user-invoked vs model-invoked (disable model invocation)", "context pointers", "fluxo grill → spec → tickets → implement → code review", "unslop / remoção de padrões de escrita de IA", "blast radius de uma mudança", "trilha de decisão auditável em TSV append-only", "arena: fan-out paralelo + julgamento cruzado + enxerto", "wizard: conduzindo o humano em passos só executáveis por ele", "repo 'fleet' para gerenciar skills entre máquinas", "grilling como entrevista para estressar planos e decisões", "domain modeling / glossário como skill", "writing for agents: agentes escrevem mal instruções para outros agentes", "auditoria de histórico de uso por subagentes para ranquear skills"]
tools: ["Matt Pocock skills repo", "PStack", "Claude Code", "Codex", "Cursor", "Grok", "OpenCode", "T3 code", "Opus 5", "GPT-5.6", "Soul (modelo)", "Depot", "GitHub / GitHub Actions", "Jira", "Linear", "Notion", "React compiler"]
people: ["Matt Pocock", "Lauren Tan (Potato)", "Dylan Moy", "Cursor", "Anthropic", "React core team"]
claims: ["Trate a description de uma skill como um gatilho de invocação, não como documentação precisa: seu papel é fazer o modelo puxar a skill certa no momento certo", "Teste skills de texto sem instalar: copie e cole o markdown diretamente no agente antes de adotar", "Use um agente com pull history e subagentes de auditoria para comparar seu histórico de uso contra um repo de skills e ranquear aderência/benefício", "Ative 'disable model invocation' em skills prescritivas/pesadas e deixe auto-invocação apenas para skills leves como diagnosing bugs", "Instale a skill unslop para remover padrões de IA (puffery, frases de chatbot, jargão) e obter respostas diretas e legíveis dos agentes", "Em blast radius, prove por execução de código os 1-2 fatos críticos dos quais a conclusão depende, pois o histórico do thread não é confiável", "Adote um log TSV append-only (o quê/por quê/evidência/resultado, uma linha por decisão) para trilhas de decisão auditáveis em execuções longas ou autônomas", "Use o padrão arena: fan-out de tentativas paralelas, leitura ponta a ponta, escolha da melhor base, enxerto das melhores ideias e verificação do resultado sintetizado", "Use skills tipo wizard para guiar o humano nos passos que só ele pode executar (dashboards, credenciais, comandos privilegiados)", "Use 'writing for agents' como referência ao escrever skills, CLAUDE.md e prompts para subagentes, porque agentes escrevem mal instruções para outros agentes", "Gerencie todas as suas skills num único repo dedicado ('fleet') replicado entre máquinas, em vez de instalações dispersas", "Não copie setups às cegas: leia o markdown de cada skill antes de instalar, extraia só as partes que servem e edite os arquivos sem medo", "Context pointers: a redação do ponteiro, não o alvo, determina quando e com que confiabilidade o agente alcança o material; alvo crítico atrás de ponteiro mal escrito é bug de variância"]
deep_dive: "high"
deep_dive_reason: "Alta densidade de práticas acionáveis e arquiteturais sobre harness de agentes (gating de invocação, context pointers, trilhas de decisão, verificação por execução) com novidade real e relevância direta a skills, context-engineering e verificação."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-building-great-agent-skills-the-missing-manual--UNzCG3lw6O0|Building Great Agent Skills: The Missing Manual]]", "[[extracts/youtube/ai-learning/2026-09-11-i-tried-100-claude-code-skills-these-6-are-the-best--eRS3CmvrOvA|I Tried 100+ Claude Code Skills. These 6 Are The Best]]", "[[extracts/youtube/ai-learning/2026-09-11-how-i-deleted-95-of-my-agent-skills-and-got-better-results-nick-nisi-workos--vy7o1g2iHY8|How I deleted 95% of my agent skills and got better results — Nick Nisi, WorkOS]]", "[[extracts/youtube/ai-learning/2026-09-11-pstack-is-agent-overkill-use-it-anyway--lUhXa8GiXns|Pstack Is Agent Overkill. Use It Anyway!]]", "[[extracts/youtube/ai-learning/2026-09-11-full-workshop-setting-yourself-up-for-success-jason-liu-openai-codex--il1c1a2FufU|Full Workshop: Setting Yourself Up for Success —Jason Liu, OpenAI Codex]]", "[[extracts/youtube/ai-learning/2026-09-11-don-t-ship-skills-without-evals-philipp-schmid-google-deepmind--0vphxNt4wyk|Don't Ship Skills Without Evals — Philipp Schmid, Google DeepMind]]", "[[extracts/youtube/ai-learning/2026-09-11-handoff-is-my-new-favourite-skill--dtAJ2dOd3ko|/handoff is my new favourite skill]]", "[[extracts/youtube/ai-learning/2026-09-11-9-things-people-get-wrong-with-my-grill-skills--UzMNBN6xLLA|9 Things People Get Wrong With My /grill-* skills]]", "[[extracts/youtube/ai-learning/2026-09-11-i-stopped-using-grill-me-for-coding-heres-what-i-use-instead--6BB6exR8Zd8|I stopped using /grill-me for coding. Here’s what I use instead:]]", "[[extracts/youtube/ai-learning/2026-09-11-wayfinder-nothing-is-too-big-to-plan-anymore--F3lL98Pj90o|/wayfinder: Nothing is too big to plan anymore]]"]
---

# So I tried Matt's skills...

## Tese
Skills em markdown simples — as de Matt Pocock e o PStack de Potato — melhoram drasticamente a qualidade e a disciplina da saída de agentes de codificação, mas devem ser auditadas, testadas e adaptadas seletivamente ao seu fluxo, nunca instaladas às cegas.

## Conceitos-chave
- AI skills como arquivos markdown
- descrição de skill como gatilho (não documentação)
- user-invoked vs model-invoked (disable model invocation)
- context pointers
- fluxo grill → spec → tickets → implement → code review
- unslop / remoção de padrões de escrita de IA
- blast radius de uma mudança
- trilha de decisão auditável em TSV append-only
- arena: fan-out paralelo + julgamento cruzado + enxerto
- wizard: conduzindo o humano em passos só executáveis por ele
- repo 'fleet' para gerenciar skills entre máquinas
- grilling como entrevista para estressar planos e decisões
- domain modeling / glossário como skill
- writing for agents: agentes escrevem mal instruções para outros agentes
- auditoria de histórico de uso por subagentes para ranquear skills

## Ferramentas & pessoas
**Ferramentas:** Matt Pocock skills repo, PStack, Claude Code, Codex, Cursor, Grok, OpenCode, T3 code, Opus 5, GPT-5.6, Soul (modelo), Depot, GitHub / GitHub Actions, Jira, Linear, Notion, React compiler

**Pessoas/orgs:** Matt Pocock, Lauren Tan (Potato), Dylan Moy, Cursor, Anthropic, React core team

## Claims acionáveis
- Trate a description de uma skill como um gatilho de invocação, não como documentação precisa: seu papel é fazer o modelo puxar a skill certa no momento certo
- Teste skills de texto sem instalar: copie e cole o markdown diretamente no agente antes de adotar
- Use um agente com pull history e subagentes de auditoria para comparar seu histórico de uso contra um repo de skills e ranquear aderência/benefício
- Ative 'disable model invocation' em skills prescritivas/pesadas e deixe auto-invocação apenas para skills leves como diagnosing bugs
- Instale a skill unslop para remover padrões de IA (puffery, frases de chatbot, jargão) e obter respostas diretas e legíveis dos agentes
- Em blast radius, prove por execução de código os 1-2 fatos críticos dos quais a conclusão depende, pois o histórico do thread não é confiável
- Adote um log TSV append-only (o quê/por quê/evidência/resultado, uma linha por decisão) para trilhas de decisão auditáveis em execuções longas ou autônomas
- Use o padrão arena: fan-out de tentativas paralelas, leitura ponta a ponta, escolha da melhor base, enxerto das melhores ideias e verificação do resultado sintetizado
- Use skills tipo wizard para guiar o humano nos passos que só ele pode executar (dashboards, credenciais, comandos privilegiados)
- Use 'writing for agents' como referência ao escrever skills, CLAUDE.md e prompts para subagentes, porque agentes escrevem mal instruções para outros agentes
- Gerencie todas as suas skills num único repo dedicado ('fleet') replicado entre máquinas, em vez de instalações dispersas
- Não copie setups às cegas: leia o markdown de cada skill antes de instalar, extraia só as partes que servem e edite os arquivos sem medo
- Context pointers: a redação do ponteiro, não o alvo, determina quando e com que confiabilidade o agente alcança o material; alvo crítico atrás de ponteiro mal escrito é bug de variância

> **Deep dive:** `high` — Alta densidade de práticas acionáveis e arquiteturais sobre harness de agentes (gating de invocação, context pointers, trilhas de decisão, verificação por execução) com novidade real e relevância direta a skills, context-engineering e verificação.
