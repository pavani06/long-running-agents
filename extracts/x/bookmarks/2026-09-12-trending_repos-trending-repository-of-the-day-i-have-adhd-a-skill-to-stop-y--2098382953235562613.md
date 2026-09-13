---
title: "Skill de output direto para coding agents"
type: "extract"
source: "x"
status_id: "2098382953235562613"
handle: "trending_repos"
url: "https://x.com/trending_repos/status/2098382953235562613"
created_at: "2026-09-11T12:07:36.000Z"
extracted: "2026-09-13"
model: "glm-5.3"
extract_version: 2
item: "[[raw/x/bookmarks/items/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098382953235562613.json]]"
tags: ["agent-tooling", "agentic-coding", "context-engineering"]
topic: "Skill de output direto para coding agents"
summary: "Repositório i-have-adhd é um skill/plugin para Claude Code que obriga o agente a entregar a resposta direto: ação primeiro, passos numerados e zero preâmbulos. Vale salvar como referência de prompt-engineering para reduzir ruído em saídas de agentes de código."
key_points: ["10 regras em SKILL.md: lead com a próxima ação, numerar tarefas multi-passo, terminar com um próximo passo concreto, suprimir tangentes e reestabelecer estado a cada turno", "Regras adicionais: estimativas de tempo específicas (minutos), erros tratados de forma objetiva, listas limitadas a 5 itens, sem preâmbulo/recap/encerramento tipo 'Hope this helps!'", "Instalável via claude plugin marketplace; para customizar, faça fork, edite skills/i-have-adhd/SKILL.md e troque a cópia upstream pela sua", "Baseado no livro The Adult ADHD Tool Kit (Ramsay & Rostain), adaptado para como um LLM deve responder, não para organização pessoal humana", "Padrão portátil: as regras funcionam como template de system prompt para qualquer assistente de código, independente do plugin"]
entities: ["i-have-adhd", "Claude Code", "GitHub", "ayghri", "The Adult ADHD Tool Kit", "J. Russell Ramsay", "Anthony L. Rostain"]
content_type: "tool"
revisit: "medium"
grounded_in: "article"
links: ["https://github.com/ayghri/i-have-adhd"]
media: []
relates-to: ["[[extracts/x/bookmarks/2026-09-12-trending_repos-trending-repository-of-the-day-i-have-adhd-a-skill-to-stop-y--2098020699365355709|Skill ADHD-friendly para agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-david_tornai-people-are-using-notebooklm-to-mass-produce-specialized-clau--2093337464215932962|Criar Claude Skills com NotebookLM]]", "[[extracts/x/bookmarks/2026-09-12-trq212-we-removed-80-of-the-claude-code-system-prompt-for-our-newes--2080710971228918066|System prompts e CLAUDE.md para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-poteto-pstack-now-includes-2-skills-i-recommend-everyone-use-or-cop--2082874054483255805|Skill de verificação para agentes]]", "[[extracts/x/bookmarks/2026-09-12-rlancemartin-i-recently-added-this-command-to-the-claude-api-skill-run-it--2095170001175199771|Comando prompt-audit para Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-dani_avila7-anthropic-shipped-a-skill-called-discernment-nudge-that-does--2090266638356566321|Skill discernment-nudge da Anthropic]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-coming-soon-to-mattpocock-skills-retro-gives-you-opportuniti--2098062605407461744|Skill /retro para retroativa de agentes]]", "[[extracts/x/bookmarks/2026-09-12-daniel_mac8-oh-boy-this-is-amazingly-cool-very-happy-i-found-this-diagra--2097795113237762544|Skill de design de diagramas para agentes de código]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-just-saw-a-comment-saying-that-i-ve-never-made-a-proper-over--2088290952704151671|Visão geral das 25 skills de agentes]]", "[[extracts/x/bookmarks/2026-09-12-rohanpaul_ai-claude-code-creator-boris-cherny-bcherny-for-people-who-aren--2082695402953031825|Podar configuração do Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-our-ci-team-s-on-call-first-responder-is-claude-tag-it-reads--2097437571634639035|Agente Claude on-call para incidentes]]", "[[extracts/x/bookmarks/2026-09-12-mattpocockuk-mattpocock-skills-v1-2-is-out-we-re-now-the-19th-most-starre--2084985277102031137|Lançamento mattpocock/skills v1.2]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-new-in-claude-code-claude-plugin-eval-see-what-value-your-pl--2098500999656923145|Claude Code plugin evals]]", "[[extracts/x/bookmarks/2026-09-12-natebjones-psa-if-you-are-tired-of-claude-lish-or-chat-lish-tell-your-a--2089457435459404093|guia de estilo para IA]]", "[[extracts/x/bookmarks/2026-09-12-milesdeutscher-this-is-the-one-github-repo-that-everyone-needs-to-save-the--2079048927593275868|Vault Obsidian de Claude Skills]]", "[[extracts/x/bookmarks/2026-09-12-trq212-we-heard-feedback-that-it-s-hard-to-know-if-your-skills-are--2098531560643539440|Claude plugin evals]]", "[[extracts/x/bookmarks/2026-09-12-coreyhainesco-i-made-a-skill-that-watches-videos-for-me-watch-video-youtub--2083953532903059846|AI skill para assistir vídeos]]", "[[extracts/x/bookmarks/2026-09-12-bcherny-your-input-needed-would-you-use-this-this-is-an-early-look-a--2095590515765060076|Function Hooks no Claude Code]]", "[[extracts/x/bookmarks/2026-09-12-claudedevs-evals-call-the-model-so-they-use-tokens-and-results-vary-pil--2098501003666702344|Evals de plugins no Claude Code]]"]
thin: false
---

# Skill de output direto para coding agents

**@trending_repos** · [2098382953235562613](https://x.com/trending_repos/status/2098382953235562613) · `tool`

## Resumo
Repositório i-have-adhd é um skill/plugin para Claude Code que obriga o agente a entregar a resposta direto: ação primeiro, passos numerados e zero preâmbulos. Vale salvar como referência de prompt-engineering para reduzir ruído em saídas de agentes de código.

## Pontos-chave
- 10 regras em SKILL.md: lead com a próxima ação, numerar tarefas multi-passo, terminar com um próximo passo concreto, suprimir tangentes e reestabelecer estado a cada turno
- Regras adicionais: estimativas de tempo específicas (minutos), erros tratados de forma objetiva, listas limitadas a 5 itens, sem preâmbulo/recap/encerramento tipo 'Hope this helps!'
- Instalável via claude plugin marketplace; para customizar, faça fork, edite skills/i-have-adhd/SKILL.md e troque a cópia upstream pela sua
- Baseado no livro The Adult ADHD Tool Kit (Ramsay & Rostain), adaptado para como um LLM deve responder, não para organização pessoal humana
- Padrão portátil: as regras funcionam como template de system prompt para qualquer assistente de código, independente do plugin

## Links
- https://github.com/ayghri/i-have-adhd

## Entidades
i-have-adhd, Claude Code, GitHub, ayghri, The Adult ADHD Tool Kit, J. Russell Ramsay, Anthony L. Rostain

> **Revisit:** `medium` · **fonte:** `article`
