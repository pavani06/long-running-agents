---
title: "Superpowers: metodologia para coding agents"
type: "extract"
source: "x"
status_id: "2098652326248493447"
handle: "cyrilXBT"
url: "https://x.com/cyrilXBT/status/2098652326248493447"
created_at: "2026-09-12T05:58:00.000Z"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-14-cyrilxbt-every-department-installable-developers-superpowers-https-t--2098652326248493447.json]]"
tags: ["agent-tooling", "agentic-coding", "spec-driven-development", "testes-qa", "code-review", "multi-agent", "harness"]
topic: "Superpowers: metodologia para coding agents"
summary: "Superpowers é uma metodologia completa de engenharia de software para agentes de código, baseada em skills compostáveis que disparam automaticamente — do brainstorm/spec à execução por subagentes com TDD e revisão em dois estágios. Vale salvar como referência concreta de como estruturar workflows obrigatórios (não sugestões) em agentes de código."
key_points: ["Pipeline completo e automático: brainstorming extrai a spec da conversa, apresenta o design em pedaços digeríveis, e após aprovação gera plano de implementação explícito enfatizando TDD vermelho-verde verdadeiro, YAGNI e DRY.", "Subagent-driven-development: um subagente novo por tarefa com revisão em dois estágios (conformidade com a spec, depois qualidade de código); o agente pode trabalhar autonomamente por horas sem desviar do plano.", "Skills são workflows obrigatórios, não sugestões: o agente checa skills relevantes antes de qualquer tarefa; a skill de TDD chega a deletar código escrito antes dos testes; issues críticos de code review bloqueiam progresso.", "Instalável em praticamente todos os harnesses (Claude Code, Codex, Cursor, Gemini, Copilot, Grok, Kimi Code, OpenCode, Devin, Droid, Antigravity, Pi, Hermes), sempre separadamente por harness; skills cobrem também debugging sistemático em 4 fases e verificação antes de declarar conclusão.", "Filosofia explícita: sistemático sobre ad-hoc, simplicidade como objetivo primário, evidência sobre afirmações; MIT, criado por Jesse Vincent/Prime Radiant, com suporte comercial para enterprise e telemetry opcional desativável."]
entities: ["Superpowers", "Jesse Vincent", "Prime Radiant", "Claude Code", "Codex", "Cursor", "GitHub Copilot", "Gemini", "Grok", "Kimi Code", "OpenCode", "Devin", "Context7", "Skill Creator", "MCP Builder", "Webapp Testing", "Claude-Mem"]
content_type: "tool"
revisit: "high"
grounded_in: "article"
thin: false
links: ["https://github.com/obra/superpowers", "https://github.com/upstash/context7", "https://github.com/anthropics/skills"]
media: []
theme: "Agentes para engenharia de código"
relates-to: ["[[extracts/x/bookmarks/2026-09-16-gergelyorosz-here-s-what-openai-s-agentic-software-factory-looks-like-tod--2099945497377091902|Fábrica de software agêntica da OpenAI]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-atpaawej-1-learn-to-read-code-2-learn-to-use-the-terminal-3--2097611379763007870|Habilidades fundamentais para devs na era de agentes]]", "[[extracts/x/bookmarks/2026-09-12-poteto-pstack-now-includes-2-skills-i-recommend-everyone-use-or-cop--2082874054483255805|Skill de verificação para agentes]]", "[[extracts/x/bookmarks/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098020699365355709|Skill ADHD-friendly para agentes de código]]", "[[extracts/x/bookmarks/2026-09-15-trending_repos-trending-repository-of-the-week-i-have-adhd-a-skill-to-stop--2099469831879737663|Skill ADHD-friendly para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-clare_liguori-i-just-published-a-manifesto-for-all-the-developers-out-ther--2097836812958097915|frontier engineering com agentes de IA]]", "[[extracts/x/bookmarks/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098382953235562613|Skill de output direto para coding agents]]", "[[extracts/x/bookmarks/2026-09-15-timothykassis-scientific-agent-skills-a-library-of-procedural-knowledge-fo--2098833771407843787|Biblioteca de habilidades procedurais para agentes científicos]]", "[[extracts/x/bookmarks/2026-09-12-steipete-hit-a-new-record-with-our-autoreview-skill-66-rounds-on-a-gn--2080899298838098034|Autoreview: code review multi-engine]]", "[[extracts/x/bookmarks/2026-09-12-andrebrov-my-biggest-recent-discovery-herdrdev-this-is-wow-i-run-25-ai--2097134891833917946|Console para orquestrar agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-alper-is-right-setting-expectations-on-software-quality-earl--2097710169245323303|expectativas de qualidade com agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-coming-soon-to-mattpocock-skills-retro-gives-you-opportuniti--2098062605407461744|Skill /retro para retroativa de agentes]]", "[[extracts/x/bookmarks/2026-09-12-txbrraa-github-acaba-de-solucionar-el-mayor-problema-del-vibe-coding--2097955506891469272|GitHub Spec Kit e spec-driven development]]", "[[extracts/x/bookmarks/2026-09-15-robshocks-1-000-prs-a-month-what-does-that-agent-workflow-look-like-a--2097381547493978562|Agentic coding workflow (PStack)]]", "[[extracts/x/bookmarks/2026-09-17-mstryoda_-cloudflare-ai-agentlar-icin-security-skill-yaynlams-direkt-y--2099560068362441009|Skill de segurança da Cloudflare]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-just-saw-a-comment-saying-that-i-ve-never-made-a-proper-over--2088290952704151671|Visão geral das 25 skills de agentes]]", "[[extracts/x/bookmarks/2026-09-14-undefinedki-the-founder-of-an-ai-coding-tool-just-walked-through-his-ent--2099145064450494595|Setup de agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-addyosmani-how-do-you-hold-the-bar-on-production-agent-code-1-agree-on--2098662421644853433|padrão de qualidade em código de agentes]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-knowledge-work-is-so-much-harder-to-automate-with-agents-tha--2096906181121818702|agents em código vs conhecimento]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-this-has-ended-up-being-better-than-expected-and-fills-an-in--2094156122441625770|AFK agent workflow vs /implement-spec]]", "[[extracts/x/bookmarks/2026-09-12-poteto-what-questions-do-you-have-about-pstack-https-t-co-lopojdztt--2098634643323142286|pstack agent workflow tool]]", "[[extracts/x/bookmarks/2026-09-12-agenticgirl-ripwire-from-red-hat-emerging-technologies-is-a-remarkably-s--2096612794145911260|contexto de repositório para coding agents]]", "[[extracts/x/bookmarks/2026-09-12-alex_frantic-how-to-graph-max-with-codex-and-5-6-sol-1-draw-a-graph-liter--2080776965070496115|Fluxo desenho-para-código com Codex]]", "[[extracts/x/bookmarks/2026-09-16-grok-outbound-prospector-built-icp-matched-prospect-lists-researc--2099876439663243402|Agente de outbound prospecting com spec]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-wayfinder-lets-you-plan-your-most-ambitious-projects-ever-yo--2082774006189449355|Ferramenta agêntica de planejamento de projetos]]", "[[extracts/x/bookmarks/2026-09-14-jonathan_wilke-how-the-fuck-did-i-not-know-about-https-t-co-93vwcw5dip-so-m--2098801944756154391|Transições UI para agentes de código]]", "[[extracts/x/bookmarks/2026-09-16-tetsuoai-made-a-grok-bot-template-drop-a-lecture-youtube-url-get-a-de--2100109861602357730|Agente que converte aulas em cheat sheets]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-15-months-later-and-i-would-probably-now-describe-the-effect--2094787007184511082|Documentação exemplar do Effect]]"]
---

# Superpowers: metodologia para coding agents

**@cyrilXBT** · [2098652326248493447](https://x.com/cyrilXBT/status/2098652326248493447) · `tool`

## Resumo
Superpowers é uma metodologia completa de engenharia de software para agentes de código, baseada em skills compostáveis que disparam automaticamente — do brainstorm/spec à execução por subagentes com TDD e revisão em dois estágios. Vale salvar como referência concreta de como estruturar workflows obrigatórios (não sugestões) em agentes de código.

## Pontos-chave
- Pipeline completo e automático: brainstorming extrai a spec da conversa, apresenta o design em pedaços digeríveis, e após aprovação gera plano de implementação explícito enfatizando TDD vermelho-verde verdadeiro, YAGNI e DRY.
- Subagent-driven-development: um subagente novo por tarefa com revisão em dois estágios (conformidade com a spec, depois qualidade de código); o agente pode trabalhar autonomamente por horas sem desviar do plano.
- Skills são workflows obrigatórios, não sugestões: o agente checa skills relevantes antes de qualquer tarefa; a skill de TDD chega a deletar código escrito antes dos testes; issues críticos de code review bloqueiam progresso.
- Instalável em praticamente todos os harnesses (Claude Code, Codex, Cursor, Gemini, Copilot, Grok, Kimi Code, OpenCode, Devin, Droid, Antigravity, Pi, Hermes), sempre separadamente por harness; skills cobrem também debugging sistemático em 4 fases e verificação antes de declarar conclusão.
- Filosofia explícita: sistemático sobre ad-hoc, simplicidade como objetivo primário, evidência sobre afirmações; MIT, criado por Jesse Vincent/Prime Radiant, com suporte comercial para enterprise e telemetry opcional desativável.

## Links
- https://github.com/obra/superpowers
- https://github.com/upstash/context7
- https://github.com/anthropics/skills

## Entidades
Superpowers, Jesse Vincent, Prime Radiant, Claude Code, Codex, Cursor, GitHub Copilot, Gemini, Grok, Kimi Code, OpenCode, Devin, Context7, Skill Creator, MCP Builder, Webapp Testing, Claude-Mem

> **Revisit:** `high` · **fonte:** `article`
