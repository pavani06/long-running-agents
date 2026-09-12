---
title: "The Era of Compound Engineering — Kieran Klaassen, Every/Cora"
type: "extract"
source: "youtube"
video_id: "_ehJyfHg1Vk"
url: "https://www.youtube.com/watch?v=_ehJyfHg1Vk"
channel: "AI Engineer"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-the-era-of-compound-engineering-kieran-klaassen-every-cora--_ehJyfHg1Vk.txt]]"
tags: ["knowledge-management", "memory-architecture", "context-engineering", "agent-loop", "agentic-coding", "agent-tooling", "process", "decision-discipline", "token-budgeting", "verification", "multi-agent", "stack-tooling"]
thesis: "Um único engenheiro com um sistema de conhecimento que compõe — extraindo julgamento e gosto em documentos de solução no repositório — supera equipes inteiras usando IA, porque a implementação fica continuamente mais barata enquanto o julgamento humano não."
concepts: ["compound engineering", "human-AI sandwich (cérebro nas pontas: brainstorm e polish)", "loop: brainstorm → plan → work → review → polish → compound", "extração de aprendizados para nunca se repetir", "sistema de memória evoluído de CLAUDE.md para documentos de solução", "mudança sequencial de bottleneck: código → planos → decidir o que construir → memória", "regra dos 50% (metade do tempo ensinando o sistema)", "documentar o raciocínio, não o código", "eficiência de tokens via respostas já embutidas no contexto", "loops autônomos noturnos em paralelo", "polish como elevação de padrão (não QA)", "postmortems como fonte de aprendizado composto", "dogfooding do próprio produto", "meta: próxima feature mais fácil por causa da atual", "agente nativo (o agente pode fazer tudo que o usuário faz)"]
tools: ["Kora (v1 e v2)", "Compound Engineering plugin (CE)", "CE id8", "CE strategy", "CE doc-review", "CE compound", "CE brainstorm", "LFG", "CE polish", "Claude Code", "CLAUDE.md", "Codex", "Cursor", "Rails (Ruby)", "React", "Linear", "GitHub", "Slack", "Intercom", "MCP", "Sonnet 3.5"]
people: ["Kiran", "Every", "Trevan Chowo"]
claims: ["Dedique 50% do tempo de cada interação à feature e 50% a ensinar o sistema com o que deu errado", "Nunca se repita: ao notar repetição, extraia o conhecimento para o repositório (comando de compound) para que o agente já saiba na próxima vez", "Armazenar soluções corretas no repositório é mais eficiente em tokens a longo prazo, pois elimina pesquisa profunda, revisão e correção", "Documente o raciocínio e as decisões por trás, não o código — generalização exige a razão do porquê", "No brainstorm, calibre o agente para fazer a quantidade mínima certa de perguntas, não 30", "Só deixe o loop rodar sem supervisão (horas, em paralelo, durante a noite) depois de iterar manualmente até o meio funcionar de forma entediante e confiável", "Use polish para elevar o padrão estético/funcional, não para corrigir falhas: se quebrar no polish, o fluxo autônomo falhou", "Gere vídeos/screenshots antes-e-depois dentro do pull request para revisão rápida do que foi construído", "Alinhe a ideação a OKRs, estratégia e experimentos passados armazenados, pontuando ideias contra esse conhecimento acumulado", "Transforme postmortems em aprendizados rastreando qual decisão, de quem ou de qual agente, levou ao incidente", "Padrão de sucesso: a próxima feature deve ser mais fácil de construir porque você entregou a atual, invertendo a complexidade crescente tradicional", "Score ideias vindas de tickets (Linear, GitHub, Slack, Intercom) contra o conhecimento composto antes de priorizar"]
deep_dive: "medium"
deep_dive_reason: "O talk entrega um fluxo acionável e um conceito relativamente novo (compound engineering com memória em documentos de solução e regra dos 50%), mas é parcialmente promocional do plugin e não aprofunda arquitetura de harness, evals ou governança."
---

# The Era of Compound Engineering — Kieran Klaassen, Every/Cora

## Tese
Um único engenheiro com um sistema de conhecimento que compõe — extraindo julgamento e gosto em documentos de solução no repositório — supera equipes inteiras usando IA, porque a implementação fica continuamente mais barata enquanto o julgamento humano não.

## Conceitos-chave
- compound engineering
- human-AI sandwich (cérebro nas pontas: brainstorm e polish)
- loop: brainstorm → plan → work → review → polish → compound
- extração de aprendizados para nunca se repetir
- sistema de memória evoluído de CLAUDE.md para documentos de solução
- mudança sequencial de bottleneck: código → planos → decidir o que construir → memória
- regra dos 50% (metade do tempo ensinando o sistema)
- documentar o raciocínio, não o código
- eficiência de tokens via respostas já embutidas no contexto
- loops autônomos noturnos em paralelo
- polish como elevação de padrão (não QA)
- postmortems como fonte de aprendizado composto
- dogfooding do próprio produto
- meta: próxima feature mais fácil por causa da atual
- agente nativo (o agente pode fazer tudo que o usuário faz)

## Ferramentas & pessoas
**Ferramentas:** Kora (v1 e v2), Compound Engineering plugin (CE), CE id8, CE strategy, CE doc-review, CE compound, CE brainstorm, LFG, CE polish, Claude Code, CLAUDE.md, Codex, Cursor, Rails (Ruby), React, Linear, GitHub, Slack, Intercom, MCP, Sonnet 3.5

**Pessoas/orgs:** Kiran, Every, Trevan Chowo

## Claims acionáveis
- Dedique 50% do tempo de cada interação à feature e 50% a ensinar o sistema com o que deu errado
- Nunca se repita: ao notar repetição, extraia o conhecimento para o repositório (comando de compound) para que o agente já saiba na próxima vez
- Armazenar soluções corretas no repositório é mais eficiente em tokens a longo prazo, pois elimina pesquisa profunda, revisão e correção
- Documente o raciocínio e as decisões por trás, não o código — generalização exige a razão do porquê
- No brainstorm, calibre o agente para fazer a quantidade mínima certa de perguntas, não 30
- Só deixe o loop rodar sem supervisão (horas, em paralelo, durante a noite) depois de iterar manualmente até o meio funcionar de forma entediante e confiável
- Use polish para elevar o padrão estético/funcional, não para corrigir falhas: se quebrar no polish, o fluxo autônomo falhou
- Gere vídeos/screenshots antes-e-depois dentro do pull request para revisão rápida do que foi construído
- Alinhe a ideação a OKRs, estratégia e experimentos passados armazenados, pontuando ideias contra esse conhecimento acumulado
- Transforme postmortems em aprendizados rastreando qual decisão, de quem ou de qual agente, levou ao incidente
- Padrão de sucesso: a próxima feature deve ser mais fácil de construir porque você entregou a atual, invertendo a complexidade crescente tradicional
- Score ideias vindas de tickets (Linear, GitHub, Slack, Intercom) contra o conhecimento composto antes de priorizar

> **Deep dive:** `medium` — O talk entrega um fluxo acionável e um conceito relativamente novo (compound engineering com memória em documentos de solução e regra dos 50%), mas é parcialmente promocional do plugin e não aprofunda arquitetura de harness, evals ou governança.
