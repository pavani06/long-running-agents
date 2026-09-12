---
title: "Field Guide to Fable — Thariq Shihipar, Anthropic"
type: "extract"
source: "youtube"
video_id: "9fubhllmsBU"
url: "https://www.youtube.com/watch?v=9fubhllmsBU"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-field-guide-to-fable-thariq-shihipar-anthropic--9fubhllmsBU.txt]]"
tags: ["harness", "context-engineering", "context-management", "agents", "process", "knowledge-management", "verification", "decision-discipline", "analise"]
thesis: "Para aproveitar uma nova classe de modelos como Fable, é preciso 'desbloquear' o modelo entendendo seu crescimento espiky de capacidades (capability overhang) e simplificando o harness, enquanto se mapeia ativamente os próprios desconhecidos (mapa vs. território) com técnicas como blind spot pass, entrevistas, referências e notas de implementação."
concepts: ["capability overhang (capacidade latente)", "modelos são cultivados, não projetados (grown, not designed)", "crescimento espiky de capacidades", "o mapa não é o território", "matriz de known knowns / known unknowns / unknown knowns / unknown unknowns", "blind spot pass", "notas de implementação (logging de desvios)", "entrevistas com o modelo", "referências como mapas alternativos", "contexto em vez de restrições no system prompt", "trade-offs não são reais / ser irrazoável", "construir ficou fácil, gerar valor continua difícil"]
tools: ["Claude Code", "Fable (modelo)", "Claude Tag", "Sonnet 3.5", "Opus 4", "Opus 4.5", "Opus 4.8", "Bash tool", "Ask User Question tool", "relatórios HTML", "paper 'On the Biology of a Large Language Model'"]
people: ["Thor (Tariq) Shihipar — Anthropic", "Cat Woo", "Simon Wilson", "Anthropic", "Y Combinator (YC)"]
claims: ["Anthropic removeu 80% do system prompt do Claude Code porque a nova classe de modelos prefere contexto a restrições, e exemplos tendem a constrangê-la", "Peça ao modelo um 'blind spot pass' sobre um codebase/campo desconhecido para descobrir unknown unknowns antes de promptar", "Gere múltiplos protótipos com decisões de design radicalmente diferentes para externalizar unknown knowns (saber-reconhecendo)", "Instrua o modelo a entrevistá-lo priorizando perguntas que mudariam a arquitetura", "Forneça código/mockup de referência como mapa em vez de escrever specs do zero", "Peça ao modelo para logar unknowns e desvios durante a execução como notas de implementação", "Peça ao modelo que o teste (quiz) sobre o trabalho para garantir entendimento no PR/merge", "Modelos com execução de código resolvem tarefas que chat puro não resolve (exemplo dos Pokémon terminados em 'aw'), ilustrando capability overhang", "A progressão do Ask User Question tool mostra que a capacidade de elicitar informação do usuário saltou entre gerações de modelos", "Force a realidade a revelar trade-offs em vez de priorizar implicitamente: 'bom, rápido, barato' agora é 'escolha os três'", "Use skills proativas/multiplayer (estilo Claude Tag) como a próxima onda de agentes"]
deep_dive: "medium"
deep_dive_reason: "Oferece práticas acionáveis de harness/context-engineering e dados concretos (remoção de 80% do system prompt, técnicas de mapeamento de unknowns) com novidade sobre a nova classe de modelos, mas boa parte do talk é motivacional/autobiográfica sem densidade arquitetural profunda."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-thariq-claude-code-anthropic--IHbsfvbfAto|Thariq (Claude Code) @ Anthropic]]", "[[extracts/youtube/ai-learning/2026-09-11-gpt-6-astra-fable-5-1-god-mode--KgKA0A3qlz0|GPT 6 Astra + Fable 5.1 = GOD MODE]]", "[[extracts/youtube/ai-learning/2026-09-11-matt-pococks-agentic-engineering-workflow-just-copy-him--nQwJVHCtDDY|Matt Pocock’s Agentic Engineering Workflow (just copy him)]]", "[[extracts/youtube/ai-learning/2026-09-11-agentic-engineering-explained-by-a-10x-developer--FU5_kpTAVDo|Agentic Engineering, explained by a 10x developer]]", "[[extracts/youtube/ai-learning/2026-09-11-claude-fable-5-use-cases-you-must-do-now-or-lose-thousands-in-1-week--lplVBFr0Ndc|Claude Fable 5 Use Cases You Must Do NOW (Or Lose Thousands in 1 Week)]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]"]
---

# Field Guide to Fable — Thariq Shihipar, Anthropic

## Tese
Para aproveitar uma nova classe de modelos como Fable, é preciso 'desbloquear' o modelo entendendo seu crescimento espiky de capacidades (capability overhang) e simplificando o harness, enquanto se mapeia ativamente os próprios desconhecidos (mapa vs. território) com técnicas como blind spot pass, entrevistas, referências e notas de implementação.

## Conceitos-chave
- capability overhang (capacidade latente)
- modelos são cultivados, não projetados (grown, not designed)
- crescimento espiky de capacidades
- o mapa não é o território
- matriz de known knowns / known unknowns / unknown knowns / unknown unknowns
- blind spot pass
- notas de implementação (logging de desvios)
- entrevistas com o modelo
- referências como mapas alternativos
- contexto em vez de restrições no system prompt
- trade-offs não são reais / ser irrazoável
- construir ficou fácil, gerar valor continua difícil

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Fable (modelo), Claude Tag, Sonnet 3.5, Opus 4, Opus 4.5, Opus 4.8, Bash tool, Ask User Question tool, relatórios HTML, paper 'On the Biology of a Large Language Model'

**Pessoas/orgs:** Thor (Tariq) Shihipar — Anthropic, Cat Woo, Simon Wilson, Anthropic, Y Combinator (YC)

## Claims acionáveis
- Anthropic removeu 80% do system prompt do Claude Code porque a nova classe de modelos prefere contexto a restrições, e exemplos tendem a constrangê-la
- Peça ao modelo um 'blind spot pass' sobre um codebase/campo desconhecido para descobrir unknown unknowns antes de promptar
- Gere múltiplos protótipos com decisões de design radicalmente diferentes para externalizar unknown knowns (saber-reconhecendo)
- Instrua o modelo a entrevistá-lo priorizando perguntas que mudariam a arquitetura
- Forneça código/mockup de referência como mapa em vez de escrever specs do zero
- Peça ao modelo para logar unknowns e desvios durante a execução como notas de implementação
- Peça ao modelo que o teste (quiz) sobre o trabalho para garantir entendimento no PR/merge
- Modelos com execução de código resolvem tarefas que chat puro não resolve (exemplo dos Pokémon terminados em 'aw'), ilustrando capability overhang
- A progressão do Ask User Question tool mostra que a capacidade de elicitar informação do usuário saltou entre gerações de modelos
- Force a realidade a revelar trade-offs em vez de priorizar implicitamente: 'bom, rápido, barato' agora é 'escolha os três'
- Use skills proativas/multiplayer (estilo Claude Tag) como a próxima onda de agentes

> **Deep dive:** `medium` — Oferece práticas acionáveis de harness/context-engineering e dados concretos (remoção de 80% do system prompt, técnicas de mapeamento de unknowns) com novidade sobre a nova classe de modelos, mas boa parte do talk é motivacional/autobiográfica sem densidade arquitetural profunda.
