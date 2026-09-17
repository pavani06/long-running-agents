---
title: "Design at the Speed of Adjectives — Paul Bakaus, Renaissance Geek, Inc."
type: "extract"
source: "youtube"
video_id: "v42opQpCy60"
url: "https://www.youtube.com/watch?v=v42opQpCy60"
channel: "AI Engineer"
extracted: "2026-09-15"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-15-design-at-the-speed-of-adjectives-paul-bakaus-renaissance-geek-inc--v42opQpCy60.txt]]"
tags: ["agent-tooling", "harness", "agentic-coding", "agent-context", "context-engineering", "decision-discipline", "model-selection", "process", "verification"]
thesis: "O palestrante argumenta que não é possível resolver design com um único prompt (one-shot) nem delegar totalmente a agentes autônomos: a abordagem eficaz é dar ao humano exatamente o nível certo de controle para direcionar o agente iterativamente por meio de adjetivos e verbos de design cujo significado é definido no contexto do projeto, como implementado na skill Impeccable."
concepts: ["Design na velocidade de adjetivos e verbos (bolder, quieter, distill, polish, denser, harden, overdrive)", "Impossibilidade de one-shot design: design exige contexto rico e iteração multi-shot", "Altitude de controle: manipulação direta (pixel) é baixa demais, agência total gera AI slop; o meio-terma é inexplorado", "Inserir o humano no loop no momento exato (human-in-the-loop)", "Adjetivos como 'leichtes Wort' (palavra leve): palavras imbuídas de significado traduzidas para o domínio de interesse", "Um adjetivo sem definição é apenas um prompt mais bonito: é preciso dizer ao agente o que a palavra significa no seu contexto", "Padrões de AI slop: gradientes roxos (2022), 'Claude beige', instrument serif, itálicos, uniformidade algorítmica", "Amplified craft: gosto (taste) pode ser amplificado e afiado, mas não cultivado em laboratório; gosto é contextual e cultural", "Desfoque de papéis entre engenheiro e designer (design engineers); colapso do handoff waterfall", "Mapeamento de workflow do usuário-alvo com pontos de injeção ao longo do processo não-linear de design (shaping → crafting → iterating → hardening/polish → design system cleanup)", "Autoavaliação do agente: 'mostre seu trabalho e diga que a IA tornou isso mais ousado; se acreditarem em você, você falhou'", "Nenhum modo automático: recusa deliberada de automação total, o objetivo é steering humano"]
tools: ["Impeccable", "Claude Code", "GitHub Copilot", "Cursor", "Codex", "GPT-5.5 (extra high)", "Claude", "Opus", "Figma", "Webflow", "Radiant Shaders (biblioteca de shaders do autor)"]
people: ["Paul (palestrante)", "Matt Puk", "Anthropic (implícito via Claude)", "OpenAI (implícito via GPT/Codex)"]
claims: ["Não é possível fazer design em um único prompt: design efetivo exige contexto rico (público, referências, intenção) e iteração multi-shot", "Defina cada adjetivo dentro do contexto do projeto — em Impeccable, 'bolder' significa hierarquia, escala e tipografia decisiva, não gradientes, glassmorphism ou neon", "Um adjetivo sem definição é apenas um prompt mais bonito; o modelo inventará a própria interpretação se você não disser o que significa", "Instrua o agente a se autoavaliar com heurísticas tipo 'mostre a alguém e diga que a IA fez; se acreditarem, você falhou' para provocar reflexão e melhoria", "Mapeie o workflow completo do usuário-alvo e identifique pontos de injeção para o tool ao longo de cada estágio do processo não-linear", "Recuse automação total: há (e haverá) request/pull de 'modo auto' que deve ser fechado porque o propósito é dar steering humano, não eliminar decisões", "Escolha a ferramenta/modelo adequada ao trabalho (ex.: não usar Opus para centralizar um diff)", "IA cobre bem os primeiros 80–95% do trabalho, mas humanos ainda são necessários para os últimos 5–20% que levam de bom a ótimo", "Teste comandos experimentais com a comunidade antes de consolidá-los (ex.: comando 'overdrive')", "Gosto (taste) pode ser amplificado com ferramentas, mas não ser gerado em laboratório; replicação universal dilui o gosto em uniformidade"]
deep_dive: "medium"
deep_dive_reason: "Oferece heurísticas acionáveis de design de skills (definir adjetivos em contexto, autoavaliação do agente, mapeamento de workflow com pontos de injeção) relevantes a harness e context-engineering, mas permanece conceitual e parcialmente promocional sobre uma ferramenta específica, sem densidade arquitetural ou de evals para justificar tier alto."
theme: "Agentic Coding: Skills & Evals"
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-ai-interfaces-of-the-future-design-review--DBhSfROq3wU|AI Interfaces Of The Future | Design Review]]", "[[extracts/youtube/ai-learning/2026-09-11-ex-nasa-dev-reveals-his-agentic-engineering-workflow--xgkjtF89-44|Ex-NASA dev reveals his Agentic Engineering Workflow]]", "[[extracts/youtube/ai-learning/2026-09-11-the-end-of-the-static-screen-architecting-intent-driven-ux-gus-iwanaga-commercet--QrMcNe2jjt8|The End of the Static Screen: Architecting Intent-Driven UX — Gus Iwanaga, commercetools]]", "[[extracts/youtube/ai-learning/2026-09-11-thariq-claude-code-anthropic--IHbsfvbfAto|Thariq (Claude Code) @ Anthropic]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-working-with-ai-not-just-using-it-brendan-o-leary--BEKc4P87XKo|Agentic Engineering: Working With AI, Not Just Using It — Brendan O'Leary]]", "[[extracts/youtube/ai-learning/2026-09-11-full-walkthrough-workflow-for-ai-coding-matt-pocock---QFHIoCo-Ko|Full Walkthrough: Workflow for AI Coding — Matt Pocock]]"]
---

# Design at the Speed of Adjectives — Paul Bakaus, Renaissance Geek, Inc.

## Tese
O palestrante argumenta que não é possível resolver design com um único prompt (one-shot) nem delegar totalmente a agentes autônomos: a abordagem eficaz é dar ao humano exatamente o nível certo de controle para direcionar o agente iterativamente por meio de adjetivos e verbos de design cujo significado é definido no contexto do projeto, como implementado na skill Impeccable.

## Conceitos-chave
- Design na velocidade de adjetivos e verbos (bolder, quieter, distill, polish, denser, harden, overdrive)
- Impossibilidade de one-shot design: design exige contexto rico e iteração multi-shot
- Altitude de controle: manipulação direta (pixel) é baixa demais, agência total gera AI slop; o meio-terma é inexplorado
- Inserir o humano no loop no momento exato (human-in-the-loop)
- Adjetivos como 'leichtes Wort' (palavra leve): palavras imbuídas de significado traduzidas para o domínio de interesse
- Um adjetivo sem definição é apenas um prompt mais bonito: é preciso dizer ao agente o que a palavra significa no seu contexto
- Padrões de AI slop: gradientes roxos (2022), 'Claude beige', instrument serif, itálicos, uniformidade algorítmica
- Amplified craft: gosto (taste) pode ser amplificado e afiado, mas não cultivado em laboratório; gosto é contextual e cultural
- Desfoque de papéis entre engenheiro e designer (design engineers); colapso do handoff waterfall
- Mapeamento de workflow do usuário-alvo com pontos de injeção ao longo do processo não-linear de design (shaping → crafting → iterating → hardening/polish → design system cleanup)
- Autoavaliação do agente: 'mostre seu trabalho e diga que a IA tornou isso mais ousado; se acreditarem em você, você falhou'
- Nenhum modo automático: recusa deliberada de automação total, o objetivo é steering humano

## Ferramentas & pessoas
**Ferramentas:** Impeccable, Claude Code, GitHub Copilot, Cursor, Codex, GPT-5.5 (extra high), Claude, Opus, Figma, Webflow, Radiant Shaders (biblioteca de shaders do autor)

**Pessoas/orgs:** Paul (palestrante), Matt Puk, Anthropic (implícito via Claude), OpenAI (implícito via GPT/Codex)

## Claims acionáveis
- Não é possível fazer design em um único prompt: design efetivo exige contexto rico (público, referências, intenção) e iteração multi-shot
- Defina cada adjetivo dentro do contexto do projeto — em Impeccable, 'bolder' significa hierarquia, escala e tipografia decisiva, não gradientes, glassmorphism ou neon
- Um adjetivo sem definição é apenas um prompt mais bonito; o modelo inventará a própria interpretação se você não disser o que significa
- Instrua o agente a se autoavaliar com heurísticas tipo 'mostre a alguém e diga que a IA fez; se acreditarem, você falhou' para provocar reflexão e melhoria
- Mapeie o workflow completo do usuário-alvo e identifique pontos de injeção para o tool ao longo de cada estágio do processo não-linear
- Recuse automação total: há (e haverá) request/pull de 'modo auto' que deve ser fechado porque o propósito é dar steering humano, não eliminar decisões
- Escolha a ferramenta/modelo adequada ao trabalho (ex.: não usar Opus para centralizar um diff)
- IA cobre bem os primeiros 80–95% do trabalho, mas humanos ainda são necessários para os últimos 5–20% que levam de bom a ótimo
- Teste comandos experimentais com a comunidade antes de consolidá-los (ex.: comando 'overdrive')
- Gosto (taste) pode ser amplificado com ferramentas, mas não ser gerado em laboratório; replicação universal dilui o gosto em uniformidade

> **Deep dive:** `medium` — Oferece heurísticas acionáveis de design de skills (definir adjetivos em contexto, autoavaliação do agente, mapeamento de workflow com pontos de injeção) relevantes a harness e context-engineering, mas permanece conceitual e parcialmente promocional sobre uma ferramenta específica, sem densidade arquitetural ou de evals para justificar tier alto.
