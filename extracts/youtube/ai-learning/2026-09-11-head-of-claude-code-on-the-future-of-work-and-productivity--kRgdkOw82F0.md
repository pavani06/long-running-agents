---
title: "Head of Claude Code on the future of work and productivity"
type: "extract"
source: "youtube"
video_id: "kRgdkOw82F0"
url: "https://www.youtube.com/watch?v=kRgdkOw82F0"
channel: "CNBC Television"
extracted: "2026-09-12"
model: "glm-5.3"
extract_version: 1
transcript: "[[raw/youtube/ai-learning/transcripts/2026-09-11-head-of-claude-code-on-the-future-of-work-and-productivity--kRgdkOw82F0.txt]]"
tags: ["agents", "agentic-coding", "agent-fleets", "model-selection", "governanca", "investimentos", "roadmap"]
thesis: "O criador do Claude Code argumenta que agentes de IA já transformaram a programação em orquestração por prompt — com milhares de agentes em paralelo — e que esse ganho (centenas de pontos percentuais de produtividade) só se materializa quando as empresas reestruturam seus processos colocando a IA no centro."
concepts: ["agent-driven coding (código escrito por agente via prompt)", "orquestração paralela de milhares de agentes", "incubação em Anthropic Labs (Claude Code, MCP, Skills, desktop app)", "descoberta de demanda por usos não previstos (Claude Code usado para não-código → Co-work)", "reestruturação do processo de negócio com IA no centro (analogia ao estudo da HBS dos anos 90 sobre computadores)", "erosão de moats de switching cost por geração de software por IA", "mudança de fase em segurança: modelos como localizadores de vulnerabilidades", "software como habilidade básica universal (analogia à alfabetização/prensa)", "calibração de confiança humano-agente por tarefa e por versão de modelo", "equilíbrio de alocação de compute entre produto e pesquisa"]
tools: ["Claude Code", "Co-work", "Claude Agent SDK", "Anthropic API", "MCP", "Skills (Anthropic)", "Desktop app (Anthropic)", "Colossus 1", "Mythos", "Claude Opus 4.5", "Claude Opus 4.6", "Claude Opus 4.7"]
people: ["Boris Cherny", "Anthropic", "Anthropic Labs", "Mike Krieger", "Meta", "Instagram", "Y Combinator", "SpaceX", "NASA", "Shopify", "OpenAI", "Harvard Business School"]
claims: ["A transição para código escrito por agentes começou em novembro passado com o Opus 4.5 e acelerou com o Opus 4.6 e 4.7; para muitos desenvolvedores isso já é o padrão", "O Co-work nasceu porque ~6 meses após o lançamento usuários usavam o Claude Code para não-código (analytics, gestão de projetos, monitoramento via webcam) — sinal de demanda a ser atendida com produto dedicado", "Ganhos de centenas de pontos percentuais em produtividade exigem reestruturar todo o processo de negócio com a IA no centro, não apenas adicionar a ferramenta à margem", "Moats baseados em switching cost estão erodindo porque agentes podem portar/reescrever software, mas os demais moats permanecem", "Há ~3 meses os modelos passaram por mudança de fase em encontrar vulnerabilidades; a estratégia é dar o melhor modelo primeiro aos defensores", "Não há planos de disponibilizar o Mythos amplamente", "O Claude Code é construído sobre o Claude Agent SDK e a API da Anthropic, ambos abertos a desenvolvedores externos construírem no mesmo stack", "O Colossus 1 foi dedicado a clientes Anthropic via parceria com SpaceX para acompanhar demanda que supera todas as estimativas", "A confiança em agentes deve ser recalibrada a cada nova versão de modelo — recomenda-se testar novamente a cada release", "Para carreiras: aprender as ferramentas sem medo e iniciar startups agora (projeção de 10x–100x mais startups em 10 anos)"]
deep_dive: "low"
deep_dive_reason: "Entrevista promocional de evento com insights estratégicos esparsos (origem do Co-work, reestruturação de processos, fase de segurança), mas sem densidade técnica sobre harness, context-engineering, evals ou arquitetura de agentes."
relates-to: ["[[extracts/youtube/ai-learning/2026-09-11-code-with-claude-opening-keynote--EvtPBaaykdo|Code with Claude Opening Keynote]]", "[[extracts/youtube/ai-learning/2026-09-11-loop-engineering-to-graph-engineering--BOOfy3Yshtw|Loop Engineering to Graph Engineering]]", "[[extracts/youtube/ai-learning/2026-09-11-conductor-ceo-charlie-holtz-walks-us-through-his-ai-coding-setup--fQmlML9Lay4|Conductor CEO Charlie Holtz Walks Us Through His AI Coding Setup]]", "[[extracts/youtube/ai-learning/2026-09-11-boris-cherny-we-cut-80-of-claude-codes-prompt--qyPCVqFUyDo|Boris Cherny: We Cut 80% of Claude Code’s Prompt]]", "[[extracts/youtube/ai-learning/2026-09-11-fabio-akita-minha-experiencia-com-agile-vibe-coding--U3bZavG8qQY|Fabio Akita: Minha Experiência com Agile Vibe Coding]]", "[[extracts/youtube/ai-learning/2026-09-11-75m-founder-reveals-his-agentic-engineering-setup--QBfXiWvM0qc|$75M founder reveals his Agentic Engineering setup]]", "[[extracts/youtube/ai-learning/2026-09-11-everything-we-knew-about-software-has-changed-theo-browne-t3dotgg--xUnRQ9vLXxo|Everything we knew about software has changed — Theo Browne, @t3dotgg ​]]", "[[extracts/youtube/ai-learning/2026-09-11-openai-just-destroyed-ai-coding-codex-2-0--C06FBVXMLCY|OpenAI just destroyed AI coding… Codex 2.0]]", "[[extracts/youtube/ai-learning/2026-09-11-this-claude-code-x-obsidian-agentic-os-will-be-the-new-meta--njHuj8OxIVI|This Claude Code x Obsidian Agentic OS Will Be The New Meta]]", "[[extracts/youtube/ai-learning/2026-09-11-grok-3-5-leaks-ai-takes-software-dev-jobs--0QPf-9El_2s|Grok 3.5 Leaks! AI Takes Software Dev Jobs!]]"]
theme: "Codificação Agêntica com Claude Code"
---

# Head of Claude Code on the future of work and productivity

## Tese
O criador do Claude Code argumenta que agentes de IA já transformaram a programação em orquestração por prompt — com milhares de agentes em paralelo — e que esse ganho (centenas de pontos percentuais de produtividade) só se materializa quando as empresas reestruturam seus processos colocando a IA no centro.

## Conceitos-chave
- agent-driven coding (código escrito por agente via prompt)
- orquestração paralela de milhares de agentes
- incubação em Anthropic Labs (Claude Code, MCP, Skills, desktop app)
- descoberta de demanda por usos não previstos (Claude Code usado para não-código → Co-work)
- reestruturação do processo de negócio com IA no centro (analogia ao estudo da HBS dos anos 90 sobre computadores)
- erosão de moats de switching cost por geração de software por IA
- mudança de fase em segurança: modelos como localizadores de vulnerabilidades
- software como habilidade básica universal (analogia à alfabetização/prensa)
- calibração de confiança humano-agente por tarefa e por versão de modelo
- equilíbrio de alocação de compute entre produto e pesquisa

## Ferramentas & pessoas
**Ferramentas:** Claude Code, Co-work, Claude Agent SDK, Anthropic API, MCP, Skills (Anthropic), Desktop app (Anthropic), Colossus 1, Mythos, Claude Opus 4.5, Claude Opus 4.6, Claude Opus 4.7

**Pessoas/orgs:** Boris Cherny, Anthropic, Anthropic Labs, Mike Krieger, Meta, Instagram, Y Combinator, SpaceX, NASA, Shopify, OpenAI, Harvard Business School

## Claims acionáveis
- A transição para código escrito por agentes começou em novembro passado com o Opus 4.5 e acelerou com o Opus 4.6 e 4.7; para muitos desenvolvedores isso já é o padrão
- O Co-work nasceu porque ~6 meses após o lançamento usuários usavam o Claude Code para não-código (analytics, gestão de projetos, monitoramento via webcam) — sinal de demanda a ser atendida com produto dedicado
- Ganhos de centenas de pontos percentuais em produtividade exigem reestruturar todo o processo de negócio com a IA no centro, não apenas adicionar a ferramenta à margem
- Moats baseados em switching cost estão erodindo porque agentes podem portar/reescrever software, mas os demais moats permanecem
- Há ~3 meses os modelos passaram por mudança de fase em encontrar vulnerabilidades; a estratégia é dar o melhor modelo primeiro aos defensores
- Não há planos de disponibilizar o Mythos amplamente
- O Claude Code é construído sobre o Claude Agent SDK e a API da Anthropic, ambos abertos a desenvolvedores externos construírem no mesmo stack
- O Colossus 1 foi dedicado a clientes Anthropic via parceria com SpaceX para acompanhar demanda que supera todas as estimativas
- A confiança em agentes deve ser recalibrada a cada nova versão de modelo — recomenda-se testar novamente a cada release
- Para carreiras: aprender as ferramentas sem medo e iniciar startups agora (projeção de 10x–100x mais startups em 10 anos)

> **Deep dive:** `low` — Entrevista promocional de evento com insights estratégicos esparsos (origem do Co-work, reestruturação de processos, fase de segurança), mas sem densidade técnica sobre harness, context-engineering, evals ou arquitetura de agentes.
